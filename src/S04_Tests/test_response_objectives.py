"""Matched-objective semantics, not evidence of real-data performance."""
from dataclasses import replace
import math
from pathlib import Path
import sys
import unittest
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from S01_Package.response_basis import (
    ResponseBatch, SharedOrthogonalBasis, aggregate, full_response_coefficients,
    losses, select_basis, sparse_coordinate_loss, train_basis,
)

torch.set_num_threads(1)


def study(seed, n=8):
    generator = torch.Generator().manual_seed(seed)
    x = torch.randn(n, 3, generator=generator, dtype=torch.float64)
    x[:, 0] *= 3
    vf = torch.randn(n, 6, 3, generator=generator, dtype=torch.float64) * .2
    vs = torch.randn(n, 16, 3, generator=generator, dtype=torch.float64) * .2
    w = torch.tensor([.7, -.5, .3], dtype=torch.float64)
    base = torch.tanh(x @ w)
    df = base[:, None] - torch.tanh((x[:, None] - vf) @ w)
    ds = base[:, None] - torch.tanh((x[:, None] - vs) @ w)
    b = ResponseBatch.build(vf, df, vs, ds, torch.zeros(n, dtype=torch.int64),
                            [f'{seed}:{i}' for i in range(n)])
    return b, x


class ObjectiveTests(unittest.TestCase):
    def test_reconstruction_is_actual_k_term_error(self):
        b, x = study(81)
        model = SharedOrthogonalBasis(3)
        with torch.no_grad(): model.angles.copy_(torch.tensor([.3, -.2, .4]))
        A = model.matrix()
        z = x @ A.T
        ix = z.abs().topk(1, dim=1).indices
        sparse = torch.zeros_like(z).scatter(1, ix, z.gather(1, ix))
        direct = (x - sparse @ A).square().sum(1)
        self.assertTrue(torch.allclose(sparse_coordinate_loss(A, x, 1), direct, atol=1e-12))
        self.assertTrue(torch.equal(sparse_coordinate_loss(A, x, 3), torch.zeros(len(x))))

    def test_spherical_reconstruction_is_a_degenerate_control(self):
        # A rotation permutes this uniform-circle quadrature. In contrast,
        # the same rotation changes reconstruction of anisotropic real inputs.
        n = 1024
        angles = torch.arange(n, dtype=torch.float64) * (2*math.pi/n)
        circle = torch.stack([angles.cos(), angles.sin()], 1)
        a = angles[37]
        A = torch.stack([torch.stack([a.cos(), -a.sin()]),
                         torch.stack([a.sin(), a.cos()])])
        I = torch.eye(2, dtype=torch.float64)
        base = sparse_coordinate_loss(I, circle, 1).mean()
        rotated = sparse_coordinate_loss(A, circle, 1).mean()
        self.assertAlmostEqual(float(base), float(rotated), places=14)
        x = torch.tensor([[3., 0.], [-3., 0.]], dtype=torch.float64)
        self.assertEqual(float(sparse_coordinate_loss(I, x, 1).mean()), 0.)
        self.assertGreater(float(sparse_coordinate_loss(A, x, 1).mean()), .1)

    def test_coefficients_use_fit_responses_only(self):
        b, _ = study(82)
        beta = full_response_coefficients(b, .01)
        altered_score = replace(b, score_d=b.score_d + 10.)
        self.assertTrue(torch.equal(beta, full_response_coefficients(altered_score, .01)))
        for i, (V, d) in enumerate(zip(b.fit_v, b.fit_d)):
            expected = torch.linalg.solve(V.T @ V/len(V) + .01*torch.eye(3), V.T @ d/len(V))
            self.assertTrue(torch.allclose(beta[i], expected))
        self.assertFalse(beta.requires_grad)

    def test_concentration_proxy_is_not_already_sparse(self):
        I = torch.eye(3, dtype=torch.float64)
        beta = torch.tensor([[1., 2., 3.], [0., 0., 0.]], dtype=torch.float64)
        value = sparse_coordinate_loss(I, beta, 1, normalized=True)
        self.assertAlmostEqual(float(value[0]), 5/14)
        self.assertEqual(float(value[1]), 0.)
        self.assertTrue(torch.equal(value, sparse_coordinate_loss(I, beta*7, 1, normalized=True)))

    def test_proxy_gradient_matches_fixed_support_finite_difference(self):
        x = torch.tensor([[3., 1., .2], [2., -.3, .7]], dtype=torch.float64)
        model = SharedOrthogonalBasis(3)
        val = sparse_coordinate_loss(model.matrix(), x, 1).mean()
        val.backward()
        grad = float(model.angles.grad[0])
        perturbed = []
        for eps in (1e-6, -1e-6):
            with torch.no_grad(): model.angles[0] = eps
            perturbed.append(float(sparse_coordinate_loss(model.matrix(), x, 1).mean().detach()))
        self.assertAlmostEqual(grad, (perturbed[0]-perturbed[1])/2e-6, places=7)

    def test_all_objectives_have_same_candidate_and_selection_rules(self):
        train, x = study(83)
        selection, _ = study(84)
        for name in ('response', 'reconstruction', 'coefficient_sparsity'):
            candidates, history = train_basis(train, k=1, ridge=.01, steps=6,
                learning_rate=.02, checkpoint_every=2, objective=name, inputs=x,
                aggregation='mean')
            self.assertEqual(len(candidates), 4)
            self.assertEqual(len(history), 6)
            A, j, values = select_basis(candidates, selection, k=1, ridge=.01, aggregation='mean')
            self.assertEqual(j, min(range(len(values)), key=values.__getitem__))
            reference = losses(candidates[0], selection, 1, .01)
            for candidate, value in zip(candidates, values):
                expected = (losses(candidate, selection, 1, .01)-reference).mean()
                self.assertAlmostEqual(value, float(expected), places=12)
            self.assertTrue(torch.allclose(A @ A.T, torch.eye(3, dtype=A.dtype), atol=1e-12))

    def test_proxy_training_does_not_use_scoring_response(self):
        b, x = study(85)
        alternate = replace(b, score_d=b.score_d + 30.)
        for name in ('reconstruction', 'coefficient_sparsity'):
            kw = dict(k=1, ridge=.01, steps=3, learning_rate=.02, checkpoint_every=1,
                      objective=name, inputs=x)
            first, _ = train_basis(b, **kw)
            second, _ = train_basis(alternate, **kw)
            self.assertTrue(all(torch.equal(a, c) for a, c in zip(first, second)))

    def test_actual_input_required_and_aggregation_explicit(self):
        b, _ = study(86)
        with self.assertRaisesRegex(ValueError, 'actual development inputs'):
            train_basis(b, k=1, ridge=.01, steps=1, learning_rate=.02,
                        checkpoint_every=1, objective='reconstruction')
        values = torch.tensor([0., 0., 3.])
        groups = torch.tensor([0, 0, 1])
        self.assertEqual(float(aggregate(values, groups, 'mean')), 1.)
        self.assertEqual(float(aggregate(values, groups, 'worst_group')), 3.)
        with self.assertRaises(ValueError): aggregate(values, groups, 'unknown')

if __name__ == '__main__':
    unittest.main()

"""Scientific checks for matched objective controls; not real-data evidence."""
import sys
import unittest
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from S01_Package.objective_controls import (
    attribution_tail_losses,
    dense_ridge_coefficients,
    sparse_reconstruction_losses,
)
from S01_Package.response_basis import aggregate_losses
from S01_Package.response_geometry import oracle_sparse_risk


class ObjectiveControlTests(unittest.TestCase):
    def setUp(self):
        s = 2.0 ** -0.5
        self.A = torch.tensor([[s, s], [-s, s]], dtype=torch.float64)
        self.I = torch.eye(2, dtype=torch.float64)
        self.x = torch.tensor([[1.0, 0.0], [2.0, 0.0], [3.0, 0.0]],
                              dtype=torch.float64)

    def test_full_reconstruction_and_l2_magnitude_are_rotation_invariant(self):
        full = (self.x @ self.A.T) @ self.A
        torch.testing.assert_close(full, self.x, atol=1e-12, rtol=1e-12)
        beta = self.x
        torch.testing.assert_close(
            (beta @ self.A.T).square().sum(-1),
            beta.square().sum(-1),
            atol=1e-12,
            rtol=1e-12,
        )

    def test_topk_controls_are_nondegenerate(self):
        rec_identity = float(sparse_reconstruction_losses(self.I, self.x, 1).mean())
        rec_rotated = float(sparse_reconstruction_losses(self.A, self.x, 1).mean())
        attr_identity = float(attribution_tail_losses(self.I, self.x, 1).mean())
        attr_rotated = float(attribution_tail_losses(self.A, self.x, 1).mean())
        self.assertEqual(rec_identity, 0.0)
        self.assertEqual(attr_identity, 0.0)
        self.assertAlmostEqual(rec_rotated, 7.0 / 3.0, places=12)
        self.assertAlmostEqual(attr_rotated, 7.0 / 3.0, places=12)

    def test_attribution_tail_equals_oracle_risk_in_isotropic_linear_limit(self):
        sigma2 = 2.0
        beta = np.array([1.0, 0.0])
        M = sigma2 * np.eye(2)
        b = M @ beta
        c = float(beta @ b)
        risk = oracle_sparse_risk(M, b, c, self.A.numpy(), 1)[0]
        tail = float(attribution_tail_losses(
            self.A, torch.tensor(beta[None, :], dtype=torch.float64), 1
        )[0])
        self.assertAlmostEqual(risk, sigma2 * tail, places=12)

    def test_anisotropic_population_reverses_tail_and_response_ranking(self):
        theta = 3.0 * np.pi / 8.0
        A = np.array([
            [np.cos(theta), np.sin(theta)],
            [-np.sin(theta), np.cos(theta)],
        ])
        beta = np.array([3.0, 3.0])
        M = np.diag([1000.0, 1.0])
        b = M @ beta
        c = float(beta @ b)

        beta_t = torch.tensor(beta[None, :], dtype=torch.float64)
        tail_identity = float(attribution_tail_losses(self.I, beta_t, 1)[0])
        tail_rotated = float(attribution_tail_losses(
            torch.tensor(A, dtype=torch.float64), beta_t, 1
        )[0])
        risk_identity = oracle_sparse_risk(M, b, c, np.eye(2), 1)[0]
        risk_rotated = oracle_sparse_risk(M, b, c, A, 1)[0]

        self.assertLess(tail_rotated, tail_identity)
        self.assertGreater(risk_rotated, risk_identity)
        self.assertAlmostEqual(tail_identity, 9.0, places=12)
        self.assertAlmostEqual(risk_identity, 9.0, places=12)

    def test_dense_ridge_matches_direct_batched_solve(self):
        V = torch.tensor(
            [[[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]],
            dtype=torch.float64,
        )
        d = torch.tensor([[1.0, -0.5, 0.5]], dtype=torch.float64)
        ridge = 0.2
        beta = dense_ridge_coefficients(V, d, ridge)[0]
        gram = V[0].T @ V[0] / len(V[0])
        cross = V[0].T @ d[0] / len(V[0])
        expected = torch.linalg.solve(gram + ridge * self.I, cross)
        torch.testing.assert_close(beta, expected, atol=1e-12, rtol=1e-12)

    def test_aggregation_is_explicit_and_changes_only_unit_weighting(self):
        values = torch.tensor([0.0, 4.0, 1.0, 1.0], dtype=torch.float64)
        groups = torch.tensor([0, 0, 1, 1], dtype=torch.int64)
        self.assertAlmostEqual(float(aggregate_losses(values, groups, "mean")), 1.5)
        self.assertAlmostEqual(float(aggregate_losses(values, groups, "worst_group")), 2.0)
        with self.assertRaises(ValueError):
            aggregate_losses(values, groups, "unknown")


if __name__ == "__main__":
    unittest.main()

"""Checks of equalities, counterexamples and conditional bounds; not PHM evidence."""
import sys
import unittest
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from S01_Package.response_geometry import moments, support_solution, oracle_sparse_risk, ridge_excess_bound


class GeometryTests(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(31)

    def test_uncentered_nonlinear_exact_risk_decomposition(self):
        v = self.rng.normal(size=(90, 5)) + 0.7
        d = np.sin(v[:, 0]) + v[:, 1] ** 2 - 0.5 * v[:, 2]
        M, b, c = moments(v, d)
        beta = np.linalg.pinv(M) @ b
        A, _ = np.linalg.qr(self.rng.normal(size=(5, 5)))
        a = self.rng.normal(size=5)
        actual = np.mean((v @ A.T @ a - d) ** 2)
        diff = A.T @ a - beta
        expected = c - b @ beta + diff @ M @ diff
        self.assertAlmostEqual(actual, expected, places=11)
        self.assertGreater(np.linalg.norm(M - np.cov(v, rowvar=False, bias=True)), 0.1)

    def test_singular_moments_and_pseudoinverse(self):
        z = self.rng.normal(size=(80, 2))
        v = np.column_stack([z, z[:, 0] + z[:, 1], 2*z[:, 0]])
        d = z[:, 0] ** 2 + z[:, 1]
        M, b, c = moments(v, d)
        a, risk = support_solution(M, b, c, np.eye(4), [0, 1, 2, 3])
        self.assertLess(np.linalg.norm(M @ np.linalg.pinv(M) @ b - b), 1e-10)
        self.assertAlmostEqual(risk, np.mean((v @ a - d)**2), places=10)

    def test_sparse_oracle_equals_direct_fits(self):
        v = self.rng.normal(size=(50, 5))
        d = np.tanh(v[:, 0] + v[:, 3])
        M, b, c = moments(v, d)
        A, _ = np.linalg.qr(self.rng.normal(size=(5, 5)))
        risk, coeff, support = oracle_sparse_risk(M, b, c, A, 2)
        fit = np.linalg.lstsq((v @ A.T)[:, support], d, rcond=None)[0]
        self.assertAlmostEqual(risk, np.mean(((v @ A.T)[:, support] @ fit-d)**2), places=11)
        self.assertLessEqual(np.count_nonzero(coeff), 2)

    def test_full_budget_invertible_invariance_nonzero_residual(self):
        v = self.rng.normal(size=(100, 4))
        d = np.sin(v[:, 0]) + v[:, 2]**2
        M, b, c = moments(v, d)
        A = self.rng.normal(size=(4, 4)) + 4*np.eye(4)
        _, r0 = support_solution(M, b, c, np.eye(4), list(range(4)))
        _, r1 = support_solution(M, b, c, A, list(range(4)))
        self.assertAlmostEqual(r0, r1, places=10)
        self.assertGreater(r0, 0.1)

    def test_haar_helpful_and_harmful(self):
        A = np.array([[1., 1.], [1., -1.]])/np.sqrt(2)
        for w, expected in [(np.array([1., 1.])/np.sqrt(2), (0.5, 0.)),
                            (np.array([1., 0.]), (0., 0.5))]:
            r0 = oracle_sparse_risk(np.eye(2), w, 1., np.eye(2), 1)[0]
            r1 = oracle_sparse_risk(np.eye(2), w, 1., A, 1)[0]
            np.testing.assert_allclose([r0, r1], expected, atol=1e-12)

    def test_anisotropic_gradient_ranking_fails(self):
        M = np.diag([100., 1.]); w = np.array([0.2, 1.])
        b = M @ w; c = w @ b
        _, gradient_choice = support_solution(M, b, c, np.eye(2), [1])
        _, optimal_choice = support_solution(M, b, c, np.eye(2), [0])
        self.assertAlmostEqual(gradient_choice, 4.)
        self.assertAlmostEqual(optimal_choice, 1.)

    def test_smooth_remainder_distance_bound(self):
        v = self.rng.normal(size=(400, 3))*0.1
        w = np.array([0.2, 0.8, -0.3])
        linear = v @ w; nonlinear = linear + 0.3*v[:, 0]**2
        A, _ = np.linalg.qr(self.rng.normal(size=(3, 3)))
        r0 = oracle_sparse_risk(*moments(v, linear), A, 1)[0]
        r1 = oracle_sparse_risk(*moments(v, nonlinear), A, 1)[0]
        remainder = np.sqrt(np.mean((nonlinear-linear)**2))
        self.assertLessEqual(abs(np.sqrt(r0)-np.sqrt(r1)), remainder+1e-10)

    def test_relu_kink_invalidates_zero_hessian_argument(self):
        x, v = 0.1, 0.2
        response = max(x, 0)-max(x-v, 0)
        tangent_response = v
        self.assertGreater(abs(response-tangent_response), 0.)

    def test_fixed_support_ridge_perturbation_bound(self):
        for _ in range(20):
            X = self.rng.normal(size=(5, 5)); G = X.T@X + 2*np.eye(5)
            b = self.rng.normal(size=5)
            noise = self.rng.normal(size=(5, 5))*0.01
            Ghat = G+(noise+noise.T)/2; bhat = b+self.rng.normal(size=5)*0.01
            ridge=0.05
            a = np.linalg.solve(Ghat+ridge*np.eye(5), bhat)
            delta = a-np.linalg.solve(G,b)
            self.assertLessEqual(delta@G@delta, ridge_excess_bound(G,b,Ghat,bhat,ridge)+1e-12)

    def test_query_hidden_subspace_and_revealed_direction_counterexample(self):
        p, Q = 7, 3
        directions, _ = np.linalg.qr(self.rng.normal(size=(p,p)))
        residual_cov = np.eye(p)-directions[:,:Q]@directions[:,:Q].T
        self.assertAlmostEqual(np.trace(residual_cov), p-Q, places=12)
        # Revealing the score direction first permits a single exact linear query.
        v, w = self.rng.normal(size=(2,p))
        self.assertAlmostEqual(float((v@w)), float(np.linalg.norm(v)*(v/np.linalg.norm(v)@w)))

    def test_four_term_risk_decomposition_with_estimated_support(self):
        v = self.rng.normal(size=(120, 5)) + 0.3
        d = np.sin(v[:, 0]) + 0.2*v[:, 1]**2 + v[:, 4]
        M, b, c = moments(v, d)
        A, _ = np.linalg.qr(self.rng.normal(size=(5, 5)))
        full = c-b @ np.linalg.pinv(M) @ b
        oracle = oracle_sparse_risk(M,b,c,A,2)[0]
        S = [0,3]
        astar, rS = support_solution(M,b,c,A,S)
        estimated = astar.copy(); estimated[S] += [0.2,-0.1]
        G = A @ M @ A.T
        difference = estimated[S]-astar[S]
        coefficient = difference @ G[np.ix_(S,S)] @ difference
        actual = np.mean((v @ A.T @ estimated-d)**2)
        self.assertAlmostEqual(actual, full+(oracle-full)+(rS-oracle)+coefficient, places=11)
        self.assertGreaterEqual(rS-oracle, -1e-12)

    def test_diagnostic_enumeration_and_nonfinite_fail(self):
        with self.assertRaises(ValueError):
            oracle_sparse_risk(np.eye(13),np.ones(13),13.,np.eye(13),2)
        with self.assertRaises(ValueError):
            moments([[float('nan')]], [0.])
        with self.assertRaises(ValueError):
            ridge_excess_bound(np.zeros((1,1)),[0.],np.eye(1),[1.],1.)

if __name__ == '__main__':
    unittest.main()

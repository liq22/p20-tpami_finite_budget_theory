"""Population response geometry; exhaustive support search is diagnostic-only."""
from itertools import combinations
import numpy as np


def moments(perturbations, responses):
    """Return uncentered moments. Deletion interventions need not have mean zero."""
    v = np.asarray(perturbations, dtype=float)
    d = np.asarray(responses, dtype=float)
    if v.ndim != 2 or d.shape != (v.shape[0],) or v.shape[0] == 0:
        raise ValueError("expected nonempty perturbations [Q,p] and responses [Q]")
    if not (np.isfinite(v).all() and np.isfinite(d).all()):
        raise ValueError("response moments require finite values")
    return v.T @ v / len(v), v.T @ d / len(v), float(d @ d / len(v))


def support_solution(M, b, c, A, support):
    """Least-squares population solution, including rank-deficient second moments."""
    M, b, A = map(lambda x: np.asarray(x, dtype=float), (M, b, A))
    p = len(b)
    S = np.asarray(support, dtype=int)
    if M.shape != (p, p) or A.shape != (p, p) or S.ndim != 1:
        raise ValueError("incompatible moment, basis, or support dimensions")
    if len(set(S.tolist())) != len(S) or np.any(S < 0) or np.any(S >= p):
        raise ValueError("support must contain unique coordinate indices")
    if not (np.isfinite(M).all() and np.isfinite(b).all()
            and np.isfinite(A).all() and np.isfinite(c)):
        raise ValueError("moments and basis must be finite")
    if not np.allclose(M, M.T, atol=1e-10) or np.linalg.eigvalsh(M).min() < -1e-9:
        raise ValueError("second moment must be symmetric positive semidefinite")
    a = np.zeros(p)
    if len(S) == 0:
        return a, float(c)
    G = A @ M @ A.T
    z = A @ b
    sub = G[np.ix_(S, S)]
    coeff = np.linalg.pinv(sub, hermitian=True) @ z[S]
    if not np.allclose(sub @ coeff, z[S], rtol=1e-7, atol=1e-9):
        raise ValueError("inconsistent moments: cross moment outside Gram range")
    a[S] = coeff
    return a, float(c - z[S] @ coeff)


def oracle_sparse_risk(M, b, c, A, k):
    """Exact cardinality oracle for p <= 12; never replace it by a heuristic."""
    p = len(b)
    if not isinstance(k, int) or not 0 <= k <= p:
        raise ValueError("k must be an integer in [0,p]")
    if p > 12:
        raise ValueError("exact support enumeration is restricted to p <= 12")
    best = None
    # Exactly k includes the at-most-k optimum: coefficients may be zero.
    for S in combinations(range(p), k):
        coeff, risk = support_solution(M, b, c, A, S)
        if best is None or risk < best[0]:
            best = (risk, coeff, S)
    return best


def ridge_excess_bound(G, b, Ghat, bhat, ridge):
    """Conditional fixed-support bound; it is not a data-derived confidence bound."""
    G, b, Ghat, bhat = [np.asarray(x, float) for x in (G, b, Ghat, bhat)]
    mu = np.linalg.eigvalsh(G).min()
    epsilon_G = np.linalg.norm(Ghat - G, 2)
    if ridge < 0 or mu <= 0 or epsilon_G >= mu:
        raise ValueError("requires ridge >= 0 and epsilon_G < lambda_min(G)")
    astar = np.linalg.solve(G, b)
    numerator = np.linalg.norm(bhat - b) + (epsilon_G + ridge) * np.linalg.norm(astar)
    radius = numerator / (mu - epsilon_G + ridge)
    return float(np.linalg.eigvalsh(G).max() * radius ** 2)

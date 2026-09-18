"""Non-degenerate matched objectives for orthogonal coordinate studies.

These controls share the same coordinate family as response-basis learning.
They deliberately avoid full reconstruction and L2 attribution magnitude,
which are invariant under an orthogonal change of coordinates.
"""
from __future__ import annotations

import math
import torch

from .response_basis import check_basis


def hard_topk(values: torch.Tensor, k: int) -> torch.Tensor:
    """Retain the k largest-magnitude entries on the final axis."""
    if values.ndim < 1 or not torch.isfinite(values).all():
        raise ValueError("top-k values must be a finite tensor")
    p = values.shape[-1]
    if not isinstance(k, int) or not 1 <= k <= p:
        raise ValueError("requires 1 <= k <= coordinate dimension")
    if k == p:
        return values.clone()
    indices = values.detach().abs().topk(k, dim=-1).indices
    kept = torch.zeros_like(values)
    return kept.scatter(-1, indices, values.gather(-1, indices))


def sparse_reconstruction_losses(A: torch.Tensor, x: torch.Tensor, k: int) -> torch.Tensor:
    """Best k-term orthogonal reconstruction error for each independent unit."""
    if x.ndim != 2 or len(x) == 0 or not torch.isfinite(x).all():
        raise ValueError("x must be finite [units,features]")
    if A.dtype != x.dtype or A.device != x.device:
        raise ValueError("basis and anchors must share dtype and device")
    check_basis(A, x.shape[1])
    z = x @ A.T
    tail = z - hard_topk(z, k)
    return tail.square().sum(dim=-1)


def attribution_tail_losses(A: torch.Tensor, beta: torch.Tensor, k: int) -> torch.Tensor:
    """Best k-term tail energy of dense raw-coordinate response vectors."""
    if beta.ndim != 2 or len(beta) == 0 or not torch.isfinite(beta).all():
        raise ValueError("beta must be finite [units,features]")
    if A.dtype != beta.dtype or A.device != beta.device:
        raise ValueError("basis and response vectors must share dtype and device")
    check_basis(A, beta.shape[1])
    coordinate_beta = beta @ A.T
    tail = coordinate_beta - hard_topk(coordinate_beta, k)
    return tail.square().sum(dim=-1)


def dense_ridge_coefficients(V: torch.Tensor, d: torch.Tensor, ridge: float) -> torch.Tensor:
    """Fit one dense raw-coordinate response vector per unit from a response table."""
    if V.ndim != 3 or d.shape != V.shape[:2] or len(V) == 0:
        raise ValueError("requires V [units,queries,features] and d [units,queries]")
    if not torch.isfinite(V).all() or not torch.isfinite(d).all():
        raise ValueError("response table contains nonfinite values")
    if not math.isfinite(ridge) or ridge <= 0:
        raise ValueError("dense ridge requires an explicit positive coefficient")
    q, p = V.shape[1], V.shape[2]
    gram = torch.einsum("nqp,nqr->npr", V, V) / q
    cross = torch.einsum("nqp,nq->np", V, d) / q
    eye = torch.eye(p, dtype=V.dtype, device=V.device).expand(len(V), -1, -1)
    return torch.linalg.solve(gram + ridge * eye, cross.unsqueeze(-1)).squeeze(-1)

"""Matched finite-budget comparators for fixed-response studies.

This module is deliberately small. It evaluates frozen coordinate dictionaries;
it does not train predictors or infer labels from filenames.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
import torch


@dataclass(frozen=True)
class ComparatorResult:
    prediction: torch.Tensor
    support: tuple[int, ...]


def fit_sparse_design(Z: torch.Tensor, d: torch.Tensor, *, k: int, ridge: float) -> ComparatorResult:
    """OMP support selection plus restricted ridge on an arbitrary fixed design."""
    if Z.ndim != 2 or d.shape != (len(Z),):
        raise ValueError("requires Z [queries,atoms] and d [queries]")
    if not 1 <= k <= Z.shape[1] or ridge <= 0:
        raise ValueError("invalid k or ridge")
    if not torch.isfinite(Z).all() or not torch.isfinite(d).all():
        raise ValueError("nonfinite design or response")
    chosen: list[int] = []
    residual = d.detach()
    coeff = Z.new_empty(0)
    for _ in range(k):
        norms = Z.detach().square().sum(0)
        eligible = norms > torch.finfo(Z.dtype).eps
        if chosen:
            eligible[chosen] = False
        if not eligible.any() or torch.linalg.vector_norm(residual) == 0:
            break
        gains = torch.full_like(norms, -torch.inf)
        gains[eligible] = (Z.detach()[:, eligible].T @ residual).square() / norms[eligible]
        chosen.append(int(gains.argmax()))
        design = Z[:, chosen]
        gram = design.T @ design / len(Z)
        cross = design.T @ d / len(Z)
        coeff = torch.linalg.solve(
            gram + ridge * torch.eye(len(chosen), dtype=Z.dtype, device=Z.device), cross
        )
        residual = (d - design @ coeff).detach()
    full = Z.new_zeros(Z.shape[1])
    if chosen:
        full[torch.tensor(chosen, device=Z.device)] = coeff
    return ComparatorResult(full, tuple(chosen))


def response_mse(V_fit, d_fit, V_score, d_score, A, *, k: int, ridge: float) -> float:
    Z_fit = V_fit @ A.T
    Z_score = V_score @ A.T
    fitted = fit_sparse_design(Z_fit, d_fit, k=k, ridge=ridge)
    return float(((Z_score @ fitted.prediction - d_score) ** 2).mean())


def union_response_mse(V_fit, d_fit, V_score, d_score, bases: Sequence[torch.Tensor], *,
                       k: int, ridge: float) -> float:
    if not bases:
        raise ValueError("static union requires at least one frozen basis")
    Z_fit = torch.cat([V_fit @ A.T for A in bases], dim=1)
    Z_score = torch.cat([V_score @ A.T for A in bases], dim=1)
    fitted = fit_sparse_design(Z_fit, d_fit, k=k, ridge=ridge)
    return float(((Z_score @ fitted.prediction - d_score) ** 2).mean())


def select_best_single(selection_losses: torch.Tensor) -> int:
    if selection_losses.ndim != 2 or len(selection_losses) == 0:
        raise ValueError("selection losses must be [units,candidates]")
    return int(selection_losses.mean(0).argmin())


def fit_group_router(selection_losses: torch.Tensor, groups: torch.Tensor) -> dict[int, int]:
    """Choose one candidate per declared pre-response group using selection units only."""
    if selection_losses.ndim != 2 or groups.shape != (len(selection_losses),):
        raise ValueError("loss/group shape mismatch")
    route: dict[int, int] = {}
    for value in torch.unique(groups):
        mask = groups == value
        route[int(value)] = int(selection_losses[mask].mean(0).argmin())
    return route


def apply_group_router(losses: torch.Tensor, groups: torch.Tensor, route: dict[int, int]) -> torch.Tensor:
    if losses.ndim != 2 or groups.shape != (len(losses),):
        raise ValueError("loss/group shape mismatch")
    values = []
    for i, group in enumerate(groups):
        key = int(group)
        if key not in route:
            raise ValueError(f"unseen routing group {key}")
        values.append(losses[i, route[key]])
    return torch.stack(values)


def routing_headroom(population_losses: torch.Tensor) -> float:
    """Exact finite-table version of T6; rows are units, columns frozen candidates."""
    if population_losses.ndim != 2 or len(population_losses) == 0:
        raise ValueError("loss table must be nonempty [units,candidates]")
    best_single = population_losses.mean(0).min()
    routed_oracle = population_losses.min(1).values.mean()
    return float(best_single - routed_oracle)


def context_matched_union(V_fit, d_fit, V_score, bases, selected: int, *, k: int, ridge: float):
    """Emulate a routed decoder in the fixed union dictionary, using the same information.

    The union coefficients are zero outside the selected block. Materializing the
    union is only a numerical identity check, not a deployment-time requirement.
    Returns routed and union predictions on the same fresh scoring displacements.
    """
    if not 0 <= selected < len(bases):
        raise ValueError("selected basis is outside the frozen candidate family")
    A = bases[selected]
    a = fit_sparse_design(V_fit @ A.T, d_fit, k=k, ridge=ridge).prediction
    union_a = a.new_zeros(sum(B.shape[0] for B in bases))
    offset = sum(B.shape[0] for B in bases[:selected])
    union_a[offset:offset + len(a)] = a
    union_design = torch.cat([V_score @ B.T for B in bases], dim=1)
    return V_score @ A.T @ a, union_design @ union_a

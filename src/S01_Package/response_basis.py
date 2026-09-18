"""Learn shared orthogonal coordinates for sparse fixed-response prediction.

The predictor never enters the optimizer. All queries are collected before basis
learning; only development units may choose the shared basis.
"""
from dataclasses import dataclass
from typing import Sequence
import math
import numpy as np
import torch
from torch import nn


def finite_tensor(value, name):
    tensor = torch.as_tensor(value, dtype=torch.float64)
    if not torch.isfinite(tensor).all():
        raise ValueError(f"{name} contains nonfinite values")
    return tensor


@dataclass(frozen=True)
class ResponseBatch:
    fit_v: torch.Tensor
    fit_d: torch.Tensor
    score_v: torch.Tensor
    score_d: torch.Tensor
    groups: torch.Tensor
    unit_ids: tuple[str, ...]

    @classmethod
    def build(cls, fit_v, fit_d, score_v, score_d, groups, unit_ids):
        vf, df, vs, ds = [finite_tensor(v, n) for v, n in
                          zip((fit_v, fit_d, score_v, score_d),
                              ("fit_v", "fit_d", "score_v", "score_d"))]
        if vf.ndim != 3 or vs.ndim != 3 or min(vf.shape) < 1 or min(vs.shape) < 1:
            raise ValueError("perturbations must be nonempty [units, queries, features]")
        if vf.shape[0] != vs.shape[0] or vf.shape[2] != vs.shape[2]:
            raise ValueError("fit and score must share units and feature coordinates")
        if df.shape != vf.shape[:2] or ds.shape != vs.shape[:2]:
            raise ValueError("responses must have shape [units, queries]")
        if len({t.device for t in (vf, df, vs, ds)}) != 1:
            raise ValueError("fit and score tensors must share an explicit device")
        g = torch.as_tensor(groups, device=vf.device)
        ids = tuple(str(x) for x in unit_ids)
        if g.shape != (len(vf),) or g.dtype not in (torch.int32, torch.int64):
            raise ValueError("groups must be integer labels for each independent unit")
        if len(ids) != len(vf) or len(set(ids)) != len(ids):
            raise ValueError("one unique unit_id is required for each row")
        # Exact shared nonzero queries cause evaluation leakage. Fresh draws must
        # also be independent by design; this guard cannot prove independence.
        for a, b in zip(vf, vs):
            overlap = (a[:, None, :] == b[None, :, :]).all(dim=-1)
            nonzero = a.ne(0).any(dim=-1)
            if (overlap & nonzero[:, None]).any():
                raise ValueError("fit and score reuse a nonzero intervention")
        return cls(vf, df, vs, ds, g.to(torch.int64), ids)


def require_disjoint(*batches):
    seen = set()
    for batch in batches:
        ids = set(batch.unit_ids)
        if seen & ids:
            raise ValueError("development, selection and evaluation units overlap")
        seen.update(ids)


def check_basis(A, p):
    if A.shape != (p, p) or not torch.isfinite(A).all():
        raise ValueError("basis must be finite and square in input coordinates")
    eye = torch.eye(p, dtype=A.dtype, device=A.device)
    if not torch.allclose(A @ A.T, eye, atol=1e-8, rtol=1e-8):
        raise ValueError("basis must be orthogonal; scaling is not permitted")


class SharedOrthogonalBasis(nn.Module):
    """Dense reference model A=exp(S), S=-S^T; one basis for all inputs."""
    def __init__(self, features: int):
        super().__init__()
        if not isinstance(features, int) or features < 1 or features > 256:
            raise ValueError("dense reference basis requires 1 <= features <= 256")
        indices = torch.triu_indices(features, features, offset=1)
        self.register_buffer("indices", indices)
        self.register_buffer("eye", torch.eye(features, dtype=torch.float64))
        self.angles = nn.Parameter(torch.zeros(indices.shape[1], dtype=torch.float64))

    def matrix(self):
        S = torch.zeros_like(self.eye)
        S[self.indices[0], self.indices[1]] = self.angles
        return torch.matrix_exp(S - S.T)

    def forward(self, x):
        return x @ self.matrix().T

    def inverse(self, z):
        return z @ self.matrix()


def sparse_decoder(V, d, A, k: int, ridge: float):
    """OMP support and restricted ridge fit, not the exhaustive population oracle.

    Support selection is discrete. Autograd differentiates the restricted solve
    on the currently selected support, not the argmax operation.
    """
    if V.ndim != 2 or d.shape != (len(V),):
        raise ValueError("decoder needs V [queries,features] and d [queries]")
    p = V.shape[1]
    if not isinstance(k, int) or not 1 <= k <= p or not math.isfinite(ridge) or ridge <= 0:
        raise ValueError("requires 1 <= k <= features and explicit positive ridge")
    Z = V @ A.T
    chosen = []
    residual = d.detach()
    for _ in range(k):
        norms = Z.detach().square().sum(0)
        eligible = norms > torch.finfo(Z.dtype).eps
        if chosen:
            eligible[chosen] = False
        if not eligible.any() or torch.linalg.vector_norm(residual) == 0:
            break
        gains = torch.full_like(norms, -torch.inf)
        gains[eligible] = (Z.detach()[:, eligible].T @ residual).square() / norms[eligible]
        j = int(gains.argmax())
        chosen.append(j)
        design = Z[:, chosen]
        gram = design.T @ design / len(V)
        cross = design.T @ d / len(V)
        coeff = torch.linalg.solve(gram + ridge*torch.eye(len(chosen), dtype=Z.dtype,
                                                       device=Z.device), cross)
        residual = (d-design@coeff).detach()
    a = Z.new_zeros(p)
    if chosen:
        a = a.index_copy(0, torch.tensor(chosen, device=Z.device), coeff)
    return a, tuple(chosen)


def losses(A, batch: ResponseBatch, k: int, ridge: float):
    check_basis(A, batch.fit_v.shape[-1])
    values = []
    for vf, df, vs, ds in zip(batch.fit_v, batch.fit_d, batch.score_v, batch.score_d):
        a, _ = sparse_decoder(vf, df, A, k, ridge)
        values.append(((vs @ A.T @ a-ds)**2).mean())
    return torch.stack(values)


def aggregate_losses(values, groups, mode: str):
    """Aggregate per-unit losses without changing the underlying objective."""
    if values.ndim != 1 or groups.shape != (len(values),):
        raise ValueError("values and groups must describe the same independent units")
    if mode == "mean":
        return values.mean()
    if mode == "worst_group":
        unique = torch.unique(groups)
        if len(unique) == 0:
            raise ValueError("worst-group aggregation requires at least one group")
        return torch.stack([values[groups == g].mean() for g in unique]).max()
    raise ValueError("aggregation must be 'mean' or 'worst_group'")


def worst_group(values, groups):
    """Compatibility wrapper for the explicit worst-group ablation."""
    return aggregate_losses(values, groups, "worst_group")


def train_basis(batch: ResponseBatch, *, k: int, ridge: float, steps: int,
                learning_rate: float, checkpoint_every: int,
                aggregation: str = "mean"):
    """Return a frozen finite trajectory; no selection/evaluation data are accepted."""
    if steps < 1 or checkpoint_every < 1 or not math.isfinite(learning_rate) or learning_rate <= 0:
        raise ValueError("steps, checkpoint_every and learning_rate must be positive")
    if batch.fit_v.shape[-1] == 1:
        raise ValueError("one feature has no learnable orthogonal coordinate rotation")
    model = SharedOrthogonalBasis(batch.fit_v.shape[-1]).to(batch.fit_v.device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    identity = model.eye.detach().clone()
    with torch.no_grad():
        reference = losses(identity, batch, k, ridge)
    candidates = [identity]
    history = []
    for step in range(1, steps+1):
        optimizer.zero_grad()
        objective = aggregate_losses(
            losses(model.matrix(), batch, k, ridge)-reference,
            batch.groups,
            aggregation,
        )
        if not torch.isfinite(objective):
            raise ValueError("nonfinite development objective; no candidate substituted")
        if not objective.requires_grad:
            raise ValueError("responses provide no trainable basis signal")
        objective.backward()
        optimizer.step()
        history.append(float(objective.detach()))
        if step % checkpoint_every == 0 or step == steps:
            candidates.append(model.matrix().detach().clone())
    return candidates, history


def select_basis(candidates: Sequence[torch.Tensor], selection: ResponseBatch, *, k, ridge,
                 aggregation: str = "mean"):
    """Independent minimax selection. Identity must be candidate zero; ties keep it."""
    if not candidates:
        raise ValueError("candidate family must contain identity")
    p = selection.fit_v.shape[-1]
    identity = torch.eye(p, dtype=selection.fit_v.dtype, device=selection.fit_v.device)
    if not torch.allclose(candidates[0], identity, atol=1e-10, rtol=1e-10):
        raise ValueError("candidate zero must be identity")
    values = []
    with torch.no_grad():
        reference = losses(identity, selection, k, ridge)
        for A in candidates:
            values.append(float(aggregate_losses(
                losses(A, selection, k, ridge)-reference,
                selection.groups,
                aggregation,
            )))
    index = int(np.argmin(values))
    return candidates[index].detach().clone(), index, values


def fixed_responses(predictor, x, perturbations, targets):
    """Collect fixed-target scalar differences without gradients or predictor updates.

    Counts measure model examples, not batched Python calls. The Q+1 forward
    evaluations are charged here; scoring evaluations are separate from Q.
    """
    if predictor.training:
        raise ValueError("predictor must already be in eval mode")
    if x.ndim != 2 or perturbations.ndim != 3 or perturbations.shape[::2] != x.shape:
        raise ValueError("expected x [units,p], perturbations [units,Q,p]")
    targets = torch.as_tensor(targets, device=x.device)
    if targets.dtype not in (torch.int32, torch.int64) or targets.shape != (len(x),):
        raise ValueError("explicit integer target required for each unit")
    with torch.no_grad():
        base = predictor(x)
        q = perturbations.shape[1]
        changed = predictor((x[:, None, :]-perturbations).reshape(-1, x.shape[1]))
        if base.ndim != 2 or changed.shape != (len(x)*q, base.shape[1]):
            raise ValueError("predictor must return [batch,targets]")
        if targets.min() < 0 or targets.max() >= base.shape[1]:
            raise ValueError("target outside predictor output")
        a = base.gather(1, targets[:, None])
        b = changed.reshape(len(x), q, -1).gather(2, targets[:,None,None].expand(-1,q,1)).squeeze(-1)
        responses = a-b
        if not torch.isfinite(responses).all():
            raise ValueError("predictor produced nonfinite responses")
    return responses, {"forward_examples": len(x)*(q+1), "backward_examples": 0}

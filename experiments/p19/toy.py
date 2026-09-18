#!/usr/bin/env python3
"""Fixed-response toy with a same-information union-emulation negative control."""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import sys
import torch
from torch import nn

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from S01_Package.response_basis import fixed_responses  # noqa: E402
from comparators import (  # noqa: E402
    apply_group_router,
    context_matched_union,
    fit_group_router,
    response_mse,
    routing_headroom,
    select_best_single,
    union_response_mse,
)


def dct_matrix(p: int) -> torch.Tensor:
    t = torch.arange(p, dtype=torch.float64)
    A = torch.cos(torch.pi / p * (t[None, :] + 0.5) * t[:, None]) * math.sqrt(2 / p)
    A[0] /= math.sqrt(2)
    return A


def block_basis(signal_basis: torch.Tensor) -> torch.Tensor:
    p = signal_basis.shape[0]
    A = torch.eye(p + 1, dtype=torch.float64)
    A[:p, :p] = signal_basis
    return A


class ContextGatedPredictor(nn.Module):
    """One fixed nonlinear predictor with two local response directions.

    The last coordinate is a pre-response context variable and is never perturbed.
    Group 0 is sparse in identity coordinates; group 1 is sparse in DCT coordinates.
    """
    def __init__(self, signal_dim: int):
        super().__init__()
        I = torch.eye(signal_dim, dtype=torch.float64)
        D = dct_matrix(signal_dim)
        self.register_buffer("w0", I[0])
        self.register_buffer("w1", D[0])

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        signal, context = x[:, :-1], x[:, -1]
        s0 = signal @ self.w0
        s1 = signal @ self.w1
        score = torch.tanh(torch.where(context >= 0, s1, s0))
        return torch.stack([score, -score], dim=-1)


def frozen_bases(signal_dim: int, count: int, generator: torch.Generator) -> tuple[list[str], list[torch.Tensor]]:
    if count < 2:
        raise ValueError("need identity, DCT and optionally random distractor bases")
    names = ["identity", "dct"]
    bases = [block_basis(torch.eye(signal_dim, dtype=torch.float64)), block_basis(dct_matrix(signal_dim))]
    for i in range(count - 2):
        q, _ = torch.linalg.qr(torch.randn(signal_dim, signal_dim, generator=generator, dtype=torch.float64))
        names.append(f"random_{i:02d}")
        bases.append(block_basis(q))
    return names, bases


def make_units(*, predictor, n: int, q_fit: int, q_score: int, scale: float,
               generator: torch.Generator, prefix: str):
    signal_dim = predictor.w0.numel()
    groups = torch.arange(n, dtype=torch.int64) % 2
    x = torch.zeros(n, signal_dim + 1, dtype=torch.float64)
    margins = torch.where(groups == 0, 0.7, -0.4)
    margins = margins + 0.15 * torch.randn(n, generator=generator, dtype=torch.float64)
    for i, group in enumerate(groups):
        w = predictor.w0 if int(group) == 0 else predictor.w1
        x[i, :-1] = margins[i] * w
        x[i, -1] = -2.0 if int(group) == 0 else 2.0
    v = torch.zeros(n, q_fit + q_score, signal_dim + 1, dtype=torch.float64)
    v[:, :, :-1] = scale * torch.randn(
        n, q_fit + q_score, signal_dim, generator=generator, dtype=torch.float64
    )
    d, access = fixed_responses(predictor, x, v, torch.zeros(n, dtype=torch.int64))
    return {
        "groups": groups,
        "fit_v": v[:, :q_fit],
        "fit_d": d[:, :q_fit],
        "score_v": v[:, q_fit:],
        "score_d": d[:, q_fit:],
        "unit_ids": [f"{prefix}:{i}" for i in range(n)],
        "access": access,
    }


def candidate_losses(data, bases, *, k: int, ridge: float) -> torch.Tensor:
    rows = []
    for vf, df, vs, ds in zip(data["fit_v"], data["fit_d"], data["score_v"], data["score_d"]):
        rows.append(torch.tensor([
            response_mse(vf, df, vs, ds, A, k=k, ridge=ridge) for A in bases
        ], dtype=torch.float64))
    return torch.stack(rows)


def union_losses(data, bases, *, k: int, ridge: float) -> torch.Tensor:
    return torch.tensor([
        union_response_mse(vf, df, vs, ds, bases, k=k, ridge=ridge)
        for vf, df, vs, ds in zip(data["fit_v"], data["fit_d"], data["score_v"], data["score_d"])
    ], dtype=torch.float64)


def run(args):
    torch.set_num_threads(1)
    gen = torch.Generator().manual_seed(args.seed)
    predictor = ContextGatedPredictor(args.signal_dim).eval()
    names, bases = frozen_bases(args.signal_dim, args.candidates, gen)
    rows = []
    summary = {
        "evidence_kind": "controlled_synthetic_only",
        "fixed_predictor": "ContextGatedPredictor",
        "seed": args.seed,
        "signal_dim": args.signal_dim,
        "candidate_count": args.candidates,
        "k": args.k,
        "ridge": args.ridge,
        "intervention_scale": args.scale,
        "routing_descriptor": "pre-response context group; never perturbed",
        "claim_boundary": "Synthetic estimator contrast, not routing-class superiority or measured deployment savings.",
        "same_information_control": "Union emulation receives the identical descriptor, fitted group rule and Q response transcript.",
        "cross_budget_pairing": "Within each Q methods are paired; different Q values use fresh units.",
        "budgets": {},
    }
    for q_fit in args.q_fit:
        selection = make_units(
            predictor=predictor, n=args.selection_units, q_fit=q_fit, q_score=args.q_score,
            scale=args.scale, generator=gen, prefix=f"select-q{q_fit}"
        )
        test = make_units(
            predictor=predictor, n=args.test_units, q_fit=q_fit, q_score=args.q_score,
            scale=args.scale, generator=gen, prefix=f"test-q{q_fit}"
        )
        select_loss = candidate_losses(selection, bases, k=args.k, ridge=args.ridge)
        test_loss = candidate_losses(test, bases, k=args.k, ridge=args.ridge)
        static_loss = union_losses(test, bases, k=args.k, ridge=args.ridge)
        best_index = select_best_single(select_loss)
        route = fit_group_router(select_loss, selection["groups"])
        routed_loss = apply_group_router(test_loss, test["groups"], route)
        hindsight_loss = test_loss.min(1).values
        matched_losses, prediction_errors = [], []
        for i, group in enumerate(test["groups"]):
            pred_route, pred_union = context_matched_union(
                test["fit_v"][i], test["fit_d"][i], test["score_v"][i],
                bases, route[int(group)], k=args.k, ridge=args.ridge
            )
            matched_losses.append(((pred_union - test["score_d"][i]) ** 2).mean())
            prediction_errors.append((pred_route - pred_union).abs().max())
        matched_loss = torch.stack(matched_losses)
        shuffle_gen = torch.Generator().manual_seed(args.seed + 10000 + q_fit)
        shuffled_groups = test["groups"][torch.randperm(len(test["groups"]), generator=shuffle_gen)]
        shuffled_loss = apply_group_router(test_loss, shuffled_groups, route)
        methods = {
            "reference_identity": test_loss[:, 0],
            "best_single": test_loss[:, best_index],
            "static_union": static_loss,
            "dynamic_group_route": routed_loss,
            "context_matched_union": matched_loss,
            "shuffled_descriptor_route": shuffled_loss,
            "test_candidate_hindsight_min": hindsight_loss,
        }
        for method, values in methods.items():
            for uid, group, value in zip(test["unit_ids"], test["groups"], values):
                rows.append({
                    "q_fit": q_fit,
                    "unit_id": uid,
                    "group": int(group),
                    "method": method,
                    "response_mse": float(value),
                    "k": args.k,
                    "q_score": args.q_score,
                    "candidate_count": args.candidates,
                })
        summary["budgets"][str(q_fit)] = {
            "selected_best_single": names[best_index],
            "group_route": {str(g): names[j] for g, j in route.items()},
            "hindsight_table_gap_not_population_headroom": routing_headroom(test_loss),
            "max_route_union_prediction_error": float(torch.stack(prediction_errors).max()),
            "means": {method: float(values.mean()) for method, values in methods.items()},
            "static_dictionary_columns": args.candidates * (args.signal_dim + 1),
            "routed_dictionary_columns": args.signal_dim + 1,
            "fit_forward_examples_per_test_unit": q_fit + 1,
            "score_forward_examples_per_test_unit": args.q_score,
        }
    return rows, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--signal-dim", type=int, default=12)
    parser.add_argument("--candidates", type=int, default=10)
    parser.add_argument("--k", type=int, default=1)
    parser.add_argument("--q-fit", type=int, nargs="+", default=[3, 6, 12, 24])
    parser.add_argument("--q-score", type=int, default=128)
    parser.add_argument("--selection-units", type=int, default=40)
    parser.add_argument("--test-units", type=int, default=120)
    parser.add_argument("--ridge", type=float, default=1e-4)
    parser.add_argument("--scale", type=float, default=0.5)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output path exists; no overwrite is allowed")
    if args.candidates < 2 or args.signal_dim < 2 or args.k < 1 or min(args.q_fit) < 1:
        parser.error("invalid dimensions or budget")
    args.output.mkdir(parents=True)
    rows, summary = run(args)
    with (args.output / "toy_comparators.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (args.output / "toy_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

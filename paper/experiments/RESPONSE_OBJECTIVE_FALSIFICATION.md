# Minimal real falsification experiment for Contribution II

## Question

Does response-trained shared-coordinate learning reduce held-out finite-query
response error beyond matched coordinate objectives and support priors, when the
predictor, response target, intervention law, information and budgets are held
fixed?

This is the next decisive experiment. It is not a benchmark sweep.

## 1. Frozen scientific objects

Before any basis training, freeze:

- predictor checkpoint;
- scalar explanatory target;
- original-space intervention law (mu_x);
- independent unit definition;
- train / selection / test unit split;
- coordinate dimension (p);
- sparsity budget (k);
- construction-query budgets (Q);
- ridge coefficient and support-search rule;
- development-scoring budget;
- primary aggregation: mean over independent units.

Windows from one recording, bearing, machine or subject must remain inside one
independent unit. No row-wise random split is allowed.

## 2. Matched response table

For every anchor input (x_u), materialize once:

[
x_u,quad
V^{\rm fit}_u,quad
d^{\rm fit}_u,quad
V^{\rm score}_u,quad
d^{\rm score}_u,
]

where

[
d_x(v)=s(x)-s(x-v).
]

Every matched coordinate method consumes the same stored table. Predictor calls
are therefore not regenerated per method.

Required study arrays for each split are:

```text
x          [N, p]
fit_v      [N, Q_max, p]
fit_d      [N, Q_max]
score_v    [N, R, p]
score_d    [N, R]
groups     [N]          # only if a prespecified group analysis is used
unit_ids   [N]
```

Smaller (Q) values take a frozen prefix of `fit_v/fit_d`; they do not redraw
easier queries.

## 3. Primary matched objective comparison

Use one orthogonal family (A_\theta=\exp(S_\theta)), one optimizer budget,
one checkpoint schedule and one independent selection split. Every trainable
objective emits the same number of frozen trajectory candidates. To prevent the
selection rule itself from favoring one native objective, **all trajectories use
the same response-MSE selector on the independent selection units**. Native
training losses never inspect test units.

### M0 — Identity

No coordinate training.

### M1 — Best fixed transform

Response-MSE selection-set choice among prespecified identity / DCT /
wavelet-like fixed orthogonal transforms. The candidate set is frozen before
seeing test units.

### M2 — Sparse-reconstruction-trained coordinates

Train with

[
J_{\mathrm{rec},k}(A)
=
\mathbb E
\|Ax-H_k(Ax)\|_2^2.
]

Full reconstruction is prohibited because it is identically zero for an
orthogonal full-dimensional basis.

### M3 — Attribution-tail-trained coordinates

From the same development response table, estimate a dense raw-coordinate
response vector (widehat\beta_u) with one declared ridge rule, then train

[
J_{\mathrm{attr},k}(A)
=
\mathbb E
\|A\widehat\beta_u-H_k(A\widehat\beta_u)\|_2^2.
]

An L2 norm of (A\widehat\beta) is prohibited because it is rotation
invariant.

### M4 — Response-trained coordinates

Train with the fresh response error of the actual (Q,k) sparse decoder:

[
J_{\mathrm{resp},Q,k}(A)
=
\mathbb E
(\widehat a_{Q,k}(A)^\top Av-d(v))^2.
]

The primary comparison M2–M4 uses the mean unit loss. Worst-group aggregation is
a separate common-aggregation ablation, not part of the method contrast.

## 4. Support-search controls

The response-trained basis must also be compared with:

- plain union-OMP over the frozen transform family;
- a prespecified structured/block union using only development information;
- best selected single fixed basis.

The structured control is required because lower finite-(Q) error can come
from a smaller admissible support family rather than a better coordinate
approximation.

Routing may appear only as a diagnostic paired with its same-information union
emulator. It is not a primary method.

## 5. Faithful external baselines

Run faithful original implementations separately from the matched-family
objective test:

- TRIM;
- Adaptive Wavelet Distillation;
- task-driven dictionary learning;
- time-series / PHM transformed-domain explainers when their native estimand is
  compatible enough to evaluate.

Do not rewrite a native SHAP, mask-retention or gradient objective into the
linear-response decoder and then label it as the original method. Record model
access, offline training and online queries for each external baseline.

## 6. Primary estimand and statistics

For independent test unit (u),

[
\Delta_u(m)
=
L_u(\mathrm{resp})
-
L_u(m),
]

where (L_u) is fresh response MSE using identical scoring displacements.

Report for every contrast:

- paired mean (overline\Delta);
- unit-level bootstrap or paired permutation interval/test;
- median and interquartile range as descriptive robustness;
- per-(Q) result;
- selected basis checkpoint and selection-set objective;
- (R_{\rm full}), coordinate oracle gap, support gap and coefficient gap on
  tractable diagnostic subsets.

Do not treat repeated queries or windows from one unit as independent samples.

## 7. Minimal PHM pilot

Start with one vibration-diagnosis task that supplies:

1. a frozen predictor with verified labels/split/checkpoint/metric;
2. recording- or machine-level independent units;
3. raw input dimension small enough for the dense orthogonal reference, or a
   frozen reduced coordinate interface declared before basis training.

Required order:

```text
predictor verification
→ one stored matched response table
→ M0–M4
→ structured support control
→ paired unit statistics
→ scientific decision
```

Do not expand to HAR, PAMAP2, PTB-XL, Sleep-EDF or forecasting until this pilot
shows that M4 has independent value.

## 8. Go / no-go rule

Proceed to broad cross-family evaluation only if all three conditions hold on
the independent PHM pilot:

1. M4 improves held-out response MSE over identity and the strongest M2/M3
   matched objective;
2. the improvement is not removed by the strongest prespecified
   structured-support control;
3. the paired unit-level uncertainty is consistent with a practically nonzero
   improvement rather than a few repeated windows or selected test cases.

If any condition fails, retain the null/negative result and narrow Contribution
II. Do not add a router or change the target to recover a positive result.

## 9. Evidence state

As of this protocol, the only executed evidence is the controlled synthetic
routing/emulation study already recorded in
`paper/experiments/EXECUTED_20260918.md`. No real-data M2–M4 comparison has
been executed yet.

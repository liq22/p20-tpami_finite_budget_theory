# Goal G5 — Statistics, stability and net cost

Scientific question: Does a surviving C2 effect persist across prespecified budgets, intervention semantics and predictor variation, and is its size large enough to justify added offline complexity?

Hypothesis: The primary effect is not a single-cell, single-law, single-checkpoint or group-objective artefact, and its online/offline cost is transparent.

Estimand: Paired independent-unit effects under frozen secondary contrasts. Seeds and checkpoints are repeated algorithmic conditions, not independent observations.

## Inputs

```text
E2 primary analysis lock
E3 decision
E4 admitted methods, if any
complete raw unit-level loss tables
Benchmark logs and runtime/device information
```

## Fixed conditions

- Primary final-test result remains unchanged.
- Secondary grid, alternative intervention law and multiplicity rule were frozen before final-test inspection.
- Unit bootstrap resamples independent units; stratification is used only for prespecified strata.
- Failed runs are included in the stability account and never silently discarded.

## Changed variables and competing explanations

| Contrast | Competing explanation ruled out |
|---|---|
| Prespecified `k,Q` grid | One favourable sparsity/query cell explains the result |
| Primary vs alternative intervention law | Perturbation semantics manufacture the advantage |
| Mean-risk vs worst-group objective, only with valid groups | Group-DRO rather than coordinate objective explains the gain |
| Optimization seeds `[0,1,2]` | One local optimum explains the result |
| Second frozen predictor seed or architecture, only after primary support | One checkpoint/model explains a broad claim |
| Orthogonal response basis vs admitted non-orthogonal task-driven dictionary | Orthogonality/capacity rather than response objective explains the result |

## Execution

1. Compute the primary paired mean, median, win fraction and 95% unit-bootstrap interval.
2. For secondary cells, report simultaneous intervals or multiplicity-adjusted inferential decisions when making cell-wise claims. Otherwise label them descriptive.
3. Repeat the locked methods under `mu_sensitivity`; do not retune objectives separately to each law unless that adaptation is the declared experiment.
4. If valid groups exist, compare mean-risk and worst-group training with all other settings fixed. If groups do not exist, use one group and mark the ablation not applicable.
5. After a positive primary result only, train/evaluate a second frozen predictor seed or architecture using the same protocol before making model-independent claims.
6. Record cost separately:

```text
offline predictor training time
response-table forward examples
coordinate-training time and device
online Q scalar perturbation responses per observation
scoring responses used only for evaluation
per-observation explanation latency
peak CPU/GPU memory
saved basis/dictionary size
feature dimension p
```

Do not report a Python batch call as one model query.

## Validation

- Every summary row can be regenerated from raw unit rows.
- No seed or failed configuration is missing.
- Units, not windows or seeds, determine inferential sample size.
- Runtime measurement excludes unrelated data download and includes declared warm-up policy.
- GPU model/device and software environment are recorded from the native run; no two-GPU run is needed for this experiment.

## Required artifacts

```text
reports/p20/E5_primary_statistics.csv
reports/p20/E5_secondary_grid.csv
reports/p20/E5_intervention_sensitivity.csv
reports/p20/E5_group_objective.csv, if applicable
reports/p20/E5_predictor_replication.csv, if admitted
reports/p20/E5_cost.csv
reports/p20/E5_summary.json
reports/p20/E5_failures.md
```

## Acceptance criteria

- A broad C2 claim requires consistent direction under the primary and sensitivity laws, no dependence on one unplanned grid cell, and predictor replication.
- A regime-specific result is acceptable only with a narrowed claim naming that regime.
- If the effect is smaller than the predeclared minimum relevant effect or requires disproportionate cost, report negative net value even if a p-value is small.

## Failure handling

Preserve sensitivity reversals, unstable seeds and cost overruns as scientific outcomes. Do not retune per scenario after final-test access.

## Sync

Commit analysis code, compact tables, environment/cost summaries and failure records to the Benchmark branch. Keep raw large artifacts in the native result directory. Target a PR to `dev` after focused and repository checks pass.

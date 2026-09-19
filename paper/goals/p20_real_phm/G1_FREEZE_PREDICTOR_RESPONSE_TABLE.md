# Goal G1 — Freeze the predictor and shared response table

Scientific question: Can one real PHM predictor be frozen and queried under one declared original-space intervention law without changing labels, splits, preprocessing or test access across methods?

Hypothesis: The admitted Benchmark task can produce a non-degenerate frozen classifier and a single construction/scoring response table that every coordinate method can reuse.

Estimand: Predictor quality is an admission diagnostic. The later explanation estimand is unit-level fresh response MSE; no coordinate-method comparison is performed in G1.

## Inputs

```text
admitted dataset and unit split from G0
native Benchmark config under configs/experiments/p20/
selected predictor family
local machine config
G0_ADMISSION.md
```

## Fixed conditions

- Train/select/test unit membership is frozen before training.
- Predictor preprocessing and normalization are fit on development-train only.
- One checkpoint is selected using development-selection metrics and then frozen.
- For classification, the default scalar target is the unperturbed predicted-class score `t(x)=argmax_c s_c(x)`; freeze `t(x)` before perturbations. Any different rule requires an explicit paper-level decision before execution.
- Construction and scoring perturbations are independent draws conditional on `x`; numerically equal draws are allowed.
- All later methods receive the exact same stored response table.

## Changed variable

G1 changes only the predictor configuration during development selection. Coordinate method, objective and support search are absent.

## Execution

1. Run the admitted predictor through the native lifecycle:

```bash
phmfactory preflight \
  --config configs/experiments/p20/<dataset>_frozen_predictor.yaml \
  --local-config configs/local/p20_machine.yaml

phmfactory \
  --config configs/experiments/p20/<dataset>_frozen_predictor.yaml \
  --local-config configs/local/p20_machine.yaml
```

Use the emitted `result_dir`, `best_checkpoint`, `run_summary` and test metrics directly. The expected native result lifecycle includes `all_results.csv`, `run_summary.json`, per-iteration `test_result_*.csv`, checkpoint and logs; do not create a parallel run authority.

2. Validate the selected checkpoint by restoring it through the native trainer/test path. Record classification metrics only as predictor diagnostics; they are not evidence for C2.

3. Freeze two intervention laws before opening explanation results:

```text
mu_primary:
  one original-input perturbation justified by the local README and sensor model

mu_sensitivity:
  one scientifically reasonable alternative, also in original input coordinates
```

Allowed examples include additive sensor-noise perturbations or contiguous measurement attenuation only when the data documentation justifies them. Do not choose the law after seeing which favours the proposed method. Do not mask transformed coordinates.

4. Add the smallest Benchmark-native response collector. Reuse the actual dataset/model/checkpoint loading path. It must not import from the P20 paper repository or duplicate a reader.

5. Collect and freeze, for every observation nested within an independent unit:

```text
x or the exact actual input needed by the reconstruction objective
unit_id and observation_id
fixed within-unit weight
split and any prespecified group
target_index
fit_v[N,Q,p] and fit_d[N,Q]
score_v[N,R,p] and score_d[N,R]
base score and perturbed score
intervention law/config and seeds
checkpoint/result_dir/config paths
```

Use a binary tensor artifact such as NPZ for arrays plus a readable CSV index and JSON contract. Do not store substitute or regenerated responses per method.

6. Verify table independence and immutability by running at least these focused tests:

```text
changing final-test responses cannot alter training candidates or selected references
all methods load identical unit IDs, targets, fit responses and scoring responses
no train/select/test unit overlap
no scoring response is copied from a construction table
repeated independent discrete draws are not rejected merely for equal values
reconstruction receives actual x, never v or synthetic x
```

## Validation

- Frozen checkpoint restores and reproduces its recorded test metrics within deterministic tolerance.
- Predictor output is finite and non-degenerate on all admitted units.
- Response arrays have the declared shapes and finite values.
- Unit and split identities survive windowing.
- The table is generated once and read-only for E2–E5.
- Feature dimension obeys the admitted method boundary.

## Required artifacts

```text
native predictor result_dir
selected checkpoint path
run_summary.json
all_results.csv and test_result_*.csv
reports/p20/G1_PREDICTOR.md
reports/p20/response_contract.json
reports/p20/response_index.csv
results/experiments/p20/<dataset>/response_table.npz
reports/p20/G1_FAILURES.md, including empty success section when no failure occurs
```

Do not commit raw signals or a large checkpoint to Git. Commit the compact response index/contract and keep the full table/checkpoint under the native result directory unless repository policy explicitly admits them.

## Acceptance criteria

One checkpoint and one shared response table are frozen before any objective comparison. No final-test response participates in coordinate training, candidate generation, hyperparameter selection or primary-reference selection.

## Failure handling

If predictor performance is degenerate, response values are non-finite, unit IDs are lost, or dimension exceeds the admitted method, record the failure and stop. Do not change model, target, split or intervention law retrospectively to obtain a positive method result.

## Sync

Commit Benchmark code/config/tests and compact contracts only after the native run and focused tests pass. Preserve failed result directories. Push the topic branch; do not modify paper Results.

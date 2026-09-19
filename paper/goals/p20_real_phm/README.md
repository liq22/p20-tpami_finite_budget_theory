# P20 real-PHM falsification Goal package

## Goal

Execute one minimum sufficient real-data study that can support, narrow or reject C2:

> Under a fixed predictor, scalar response target, original-space intervention law, development information, independent-unit split and finite `(k,Q)`, does direct response-objective coordinate learning improve fresh response prediction beyond matched objectives and structured support priors?

This package is handed to a local Agent with access to:

```text
/home/user/data/PHMbenchdata/PHM-Vibench/metadata.xlsx
/home/user/data/PHMbenchdata/PHM-Vibench/README.md
```

The files were not available when this package was written. The Agent must inspect them before selecting a dataset, unit, label, reader or split.

## Authority and repository boundary

```text
Paper repository:
  scientific contract and these Goals only

PHMbench/PHM-Vibench:
  all executable code
  experiment configs
  model/checkpoint execution
  response-table collection
  evaluation/statistics
  plotting source
  real artifacts and failure records
```

Do not import executable P20 modules from the paper repository. Do not copy or fork a loader. Use the Benchmark's current `src/data_factory/`, config resolver, model/task/trainer factories, native checkpoint restore and direct result paths.

## Execution order

```text
G0_DATA_RUNTIME_ADMISSION
→ G1_FREEZE_PREDICTOR_RESPONSE_TABLE
→ G2_MATCHED_OBJECTIVE_MAIN
→ G3_STRUCTURED_SUPPORT_CONTROL
→ G4_CLOSEST_METHOD_EXTERNAL_VALIDITY
→ G5_STATISTICS_STABILITY_COST
→ G6_ANALYSIS_FIGURES_SYNC
```

G0 and G1 are admission gates. G3–G5 are conditional gates, not an instruction to keep running after the central hypothesis fails.

## Common invariants

Every compared method must share:

```text
frozen predictor checkpoint
scalar target rule
original-space intervention law
construction and scoring response tables
independent unit split and within-unit weights
coordinate dimension and coordinate family for matched objectives
sparse decoder
k and Q
ridge-selection rule
candidate/checkpoint schedule
optimizer budget for matched objectives
development information
final-test access policy
```

## Benchmark branch and outputs

Start from current Benchmark `dev` and use one bounded topic branch:

```bash
git switch dev
git pull --ff-only origin dev
git switch -c feat/p20-response-falsification
```

Research configurations belong under `configs/experiments/p20/`. Keep complete local outputs under the config-declared result directory. Commit only source, configs, tests, compact real prediction/metric tables, failure records and figure data allowed by repository policy. Do not commit raw datasets or large checkpoints; retain their exact native result paths in `run_summary.json` and the experiment report. Do not create hashes, receipts, a second registry or a result manager.

## Non-negotiable prohibitions

The local Agent must not:

- redesign the paper or rewrite Contributions;
- infer metadata semantics from column names without checking the local README and reader;
- treat windows as independent units;
- change test results into selection data;
- create substitute data, checkpoints, labels or expected curves;
- silently fall back to another dataset, model, device, metric or intervention law;
- rerun seeds until the desired direction appears;
- delete or overwrite failed runs;
- report a literature score as a local reproduction;
- merge to `main`.

## Completion decision

The local run is complete when it produces one of three valid decisions:

```text
SUPPORT:
  response objective beats the matched reference and survives structured support

NARROW:
  effect exists only in a prespecified regime or is explained by support search

REJECT:
  matched reference is indistinguishable or better on final-test units
```

All three are scientifically valid outcomes and must be preserved.

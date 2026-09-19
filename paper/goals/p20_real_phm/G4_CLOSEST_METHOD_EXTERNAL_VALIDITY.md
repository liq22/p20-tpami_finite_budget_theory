# Goal G4 — Closest published method and external validity

Scientific question: After E2 and E3 support an independent effect, does the proposed response-trained coordinate mechanism remain useful relative to the closest published representation/explanation paradigms under an honest same-protocol comparison?

Hypothesis: The response-trained method retains a practically relevant finite-budget response advantage while its scope remains distinct from native mask, attribution and information-retention objectives.

Estimand: Primary response-MSE comparisons use only methods for which a mathematically valid response decoder can be constructed without changing their defining mechanism. Native temporal-XAI metrics are reported separately and are not numerically pooled with response MSE.

## Inputs

```text
E2/E3 supported frozen configuration
P20 literature matrix and original papers
existing Benchmark implementations or legally usable author code
same real data split/checkpoint/response table
```

## Fixed conditions

- Reported literature scores are context only; they are never entered as local reproduced results.
- Faithful implementations preserve native objectives, model access, perturbation semantics and output objects.
- Matched-family proxies remain labelled as proxies and cannot be renamed as faithful AWD/TRIM/TimeX++/ContraLSP/TIMING reproductions.
- All method admission decisions are made before final-test comparison.

## Changed variable

Published method mechanism and, where unavoidable, its explicitly disclosed information or model-access contract.

## Baseline priority

1. `simple reference`: identity / fixed DCT already completed in E2.
2. `strong conventional`: best fixed basis and reconstruction-trained coordinates already completed in E2.
3. `closest transform method`: faithful Adaptive Wavelet Distillation when its wavelet/model-access assumptions are compatible with the admitted signal and frozen predictor.
4. `closest optimization paradigm`: a task-driven dictionary comparator when a fair response-task instantiation is possible without duplicating the proposed arm.
5. `recent temporal-XAI external validity`: ContraLSP, TimeX++, TIMING or ORTE only when their native task/output and code/license are compatible. Report native metrics and method access separately.

TRIM is a transformed-explanation framework rather than a unique numerical algorithm; do not create a meaningless `TRIM score` without a concrete transformation and attribution method.

## Execution

For each candidate baseline, create an admission row:

```text
original source/version
peer-reviewed venue
available code and license
native objective/output
required model access
compatible dataset/task
adaptation required
same-protocol response metric valid? yes/no
native metric
status: ADMITTED / PROXY_ONLY / NOT_APPLICABLE / BLOCKED
```

Run only admitted methods. Use the same unit split and final-test access rule. When a method requires retraining the predictor, report it as a different experimental question rather than a fixed-predictor response comparison.

## Validation

- Original-paper equations and author-code behavior agree for each faithful arm.
- No published number is mixed with local unit metrics.
- Adaptation does not remove the defining mechanism.
- Model access, offline information, queries, labels and compute are reported.

## Required artifacts

```text
reports/p20/E4_baseline_admission.csv
reports/p20/E4_method_contracts.md
reports/p20/E4_unit_metrics.csv
reports/p20/E4_native_metrics.csv
reports/p20/E4_summary.json
reports/p20/E4_failures.md
```

## Acceptance criteria

A method may appear in a same-protocol quantitative table only if `ADMITTED`. `PROXY_ONLY` belongs in the matched-objective analysis with its proxy name. `NOT_APPLICABLE` and `BLOCKED` remain documented limitations, not zero scores.

## Failure handling

If faithful code cannot run because of a genuine semantic or licensing mismatch, retain the exact reason and continue G5. Do not recreate a simplified method and label it faithful.

## Sync

Commit legal source adapters, configs, tests, compact artifacts and admission records to the Benchmark branch. Large external weights remain outside Git under declared paths. Target Benchmark `dev` through a focused PR.

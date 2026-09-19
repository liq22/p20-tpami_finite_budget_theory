# Minimum sufficient experiment set for the real PHM falsification

## Scope

This document converts the current P20 claim structure into the smallest experiment sequence that can change the paper decision. It does not report real-data results. All executable code, configurations, evaluators, response-table generation, statistics and plotting must live in `PHMbench/PHM-Vibench`; this paper repository stores only the scientific contract and local-Agent Goals.

Audit snapshot used for this design:

- P20 PR #1 head: `71703f8ad48d86006deb1a3285ba3b22bacb24f7`;
- P20 target branch: `dev`; PR remains open because hosted workflow runs are absent;
- PHMFactory/PHM-Vibench `dev` observed at `99725e6841ecb99e6c31aa9ca68e775a43dfe8a1`;
- local data requested at `/home/user/data/PHMbenchdata/PHM-Vibench/metadata.xlsx` and `/home/user/data/PHMbenchdata/PHM-Vibench/README.md`;
- those local files were not mounted in the environment that produced this plan, so their schema, dataset families, labels, unit IDs, licenses and raw-file coverage remain unverified.

The Benchmark has no public object named `DataPort` at the audited revision. The actual data boundary is the existing `src/data_factory/` plus config resolution and any provider/version metadata. Do not introduce a second data abstraction merely to match terminology.

## Contributions and evidence status

| Contribution | Required evidence | Existing evidence | Missing evidence | Decision |
|---|---|---|---|---|
| C1. Fixed-response risk geometry | Correct derivation, counterexamples, numerical checks under singular/non-centred moments and finite `k,Q` | Theory, targeted tests and synthetic diagnostics already exist | No additional experiment is required for the bounded mathematical claim | Do not rerun unless the theory or implementation changes |
| C3. Same-information union containment | Proof plus pathwise numerical equality using identical information and queries | Proof and exact equality control at `Q={3,6,12,24}` already exist | No real-data rerun is needed unless routing re-enters a major claim | Preserve as a negative control; do not market routing superiority |
| C2. Independent value of the response objective | Independent-unit real experiment; same coordinate family, decoder, information, `k,Q`, split and optimizer budget; response objective must beat the strongest development-selected matched proxy | A synthetic matched-objective run is null: response training does not establish incremental benefit over coefficient concentration | One admitted real dataset family, one frozen predictor, shared response table, matched objectives, paired unit inference | Execute E1–E3; stop expansion on a null or reversed primary result |
| Practical TPAMI claim | Strong closest baseline, regime stability, intervention sensitivity and transparent cost | Protocol only | Faithful/adapted closest method where semantically compatible; stability and cost after a positive C2 result | Conditional on C2 surviving E2 and E3 |

## Sequential experiment matrix

The order is a scientific gate, not a project-management preference.

| ID | Scientific question | Treatment | Primary control | Estimand / metric | Statistical unit | Gate |
|---|---|---|---|---|---|---|
| G0 | Is one real PHM task scientifically and technically admissible? | Actual metadata, raw files, native Benchmark runtime and proposed predictor configuration | Repository Dummy smoke and current data/config contracts | Admission facts only: unit identity, split, input dimension, labels, checkpoint lifecycle, file coverage | Highest non-overlapping entity named by metadata/README | No training study proceeds until all admission criteria pass |
| E1 | Can one frozen predictor and one response table be generated without leakage or semantic drift? | Native PHMFactory training plus original-space response collection | Same predictor evaluated without coordinate learning | Predictor metrics; response-table invariants; zero test feedback into training/selection | Recording, bearing, machine run, subject or equivalent | Produces the single immutable input used by all later methods |
| E2 | Does direct response training outperform matched non-response objectives? | Shared orthogonal coordinates trained on fresh finite-query response error | Strongest development-selected member of reconstruction and coefficient-concentration objectives; identity, DCT and best fixed basis are mandatory references | `Delta_u=L_u(response)-L_u(reference)` on final-test units; paired mean and unit-bootstrap 95% interval | Independent unit, not window or seed | Provisional support only if the upper interval is below zero and the effect exceeds a predeclared minimum relevant effect |
| E3 | Is any E2 gain merely a support-search or structure-prior effect? | Response-trained shared coordinates | Plain union and information-matched structured/block union built from non-response/fixed bases | Paired unit response-MSE difference; identical `k,Q` and response table | Independent unit | If structured support removes the E2 gain, narrow C2 to a search/conditioning mechanism |
| E4 | Does the surviving effect remain competitive with the closest published paradigm? | Response-trained coordinates | Faithful AWD or another admitted learned-transform method; task-driven dictionary comparator when its model-access contract is compatible | Same-protocol response MSE plus each method's native metric where meaningful | Independent unit | Run only after E2 and E3 support an independent effect; reported literature scores never enter the table as reproduced values |
| E5 | Is the conclusion stable and worth its cost? | Frozen primary method/configuration | Prespecified `k,Q`, intervention-law, objective, predictor and group-risk contrasts | Paired effects, sensitivity, offline/online time, scalar queries, memory | Independent unit; algorithm seeds are repeated runs, not sample size | Required before broad or model-independent claims |
| E6 | Can every figure be regenerated from actual artifacts without inference inside plotting? | Analysis of frozen CSV/JSON/NPZ artifacts | Raw artifact and failure records | Figure-data equality, labels, units and uncertainty | Same units as analysis | No expected curves; plotting reads data only |

## Minimum configuration family

The local Agent must create a bounded experiment slice in the Benchmark, not in this repository:

```text
configs/experiments/p20/
scripts/p20/
test/test_p20_*.py
reports/p20/
```

Use the current native CLI and result lifecycle. The audited CWRU demo is only a starting candidate:

```text
configs/demo/01_cross_domain/cwru_dg.yaml
configs/base/data/base_cross_domain.yaml
configs/base/model/backbone_dlinear.yaml
configs/base/task/dg.yaml
configs/base/trainer/default_single_gpu.yaml
```

Do not assume it is admissible. At the audited revision it uses `window_size: 4096`, while the current dense P20 basis is limited to `p<=256`; it also exposes ratio-based split fields whose unit-level leakage properties must be traced in source. Do not silently shorten windows, project inputs, or reinterpret windows as independent units to make the method run. Either admit a scientifically justified native input with `p<=256`, or record that the dense method is inapplicable and stop before producing a misleading real result.

## Primary estimand

For fixed within-unit weights and fresh scoring perturbations,

$$
L_u(m)=\sum_j w_{uj}\frac{1}{R}\sum_{r=1}^{R}
\left(\widehat d_{ujm}(v_r)-d_{uj}(v_r)\right)^2.
$$

Let the development-selected matched non-response reference be

$$
m_{ref}\in\{m_{reconstruction},m_{concentration}\}.
$$

The confirmatory effect is

$$
\Delta_u=L_u(m_{response})-L_u(m_{ref}),
\qquad
\Delta=\frac{1}{N}\sum_u\Delta_u.
$$

Negative values favour direct response training. Resample independent units, optionally stratified by a prespecified class/regime; never resample windows as independent observations. The final-test table is opened once after the primary pair, target rule, intervention law, ridge rule, `k,Q`, candidate schedule and minimum relevant effect are frozen from development data.

## Global stop rules

1. If G0 cannot identify a leakage-safe independent unit, valid scalar target, complete raw files, native checkpoint lifecycle or admissible dimension, stop and record the blocker.
2. If E2 is null or reversed relative to the strongest matched objective, reject an independent C2 advantage and stop E3–E5 expansion except cost and failure reporting.
3. If E2 is positive but E3 removes the gain, retain only a conditional support-search/conditioning finding.
4. Only a result surviving E2 and E3 admits the closest published baseline and broader robustness work.
5. Do not add routing, a larger predictor, a different split or an unplanned dataset to rescue a failed central hypothesis.

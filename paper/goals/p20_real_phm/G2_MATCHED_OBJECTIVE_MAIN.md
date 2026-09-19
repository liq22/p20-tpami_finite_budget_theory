# Goal G2 — Matched-objective main falsification

Scientific question: Under identical coordinates, decoder, information and budgets, does direct finite-query response training improve fresh response prediction beyond the strongest matched non-response objective?

Hypothesis: A shared orthogonal basis trained on fresh response error has lower final-test unit response MSE than the development-selected stronger member of reconstruction and coefficient-concentration objectives.

Estimand:

$$
\Delta_u=L_u(m_{response})-L_u(m_{ref}),
\qquad
m_{ref}=\arg\min_{m\in\{reconstruction,concentration\}}
\widehat L_{select}(m).
$$

Negative `Delta_u` favours response training. The primary statistic is the paired unit mean with a 95% bootstrap interval over independent units.

## Inputs

```text
G1 frozen checkpoint
G1 response_table.npz, response_index.csv and response_contract.json
actual train x for reconstruction
configs/experiments/p20/<dataset>_response_objectives.yaml
predeclared optimizer seeds: [0, 1, 2]
```

## Fixed conditions

- Same shared orthogonal parameterization, initialization rule, optimizer budget, candidate/checkpoint schedule and selection units.
- Same sparse decoder, ridge-selection rule, `k,Q`, response table, scoring responses and aggregation.
- Same development information and no final-test feedback.
- Algorithm seeds are repeated optimization runs; they do not increase the independent-unit sample size.
- Identity, DCT/domain-standard fixed transform and a development-selected finite best-fixed family are mandatory references.

## Changed variable

Only the outer coordinate-learning objective changes:

```text
reconstruction:
  k-coordinate reconstruction error on actual development x

coefficient concentration:
  prespecified concentration penalty on full fitted response coefficients

response:
  fresh-within-development finite-Q response MSE
```

Do not give one objective extra queries, gradients, candidate count or optimization steps.

## Dataset / split

Use exactly the G0/G1 admitted dataset and independent-unit split. Final-test units remain unopened until the primary reference, one primary `(k,Q)` pair, ridge rule, intervention law and minimum relevant effect are frozen from development data.

## Configuration

Prespecify a small secondary budget grid before final testing. Unless the admitted dimension requires a stricter set, use:

```text
k_grid: values representing severe, moderate and relaxed sparsity, all <= p
Q_grid: three levels with Q>k, including one strongly query-limited level
R_score: large enough that scoring Monte Carlo error is smaller than the declared minimum relevant effect
```

Do not select the strongest final-test cell. One primary `(k,Q)` pair is chosen on development data; the remaining cells are secondary mechanism analyses.

## Execution

1. Run focused tests for objective equality of all non-objective inputs.
2. Train each objective for exactly seeds `[0,1,2]`; save every candidate trajectory and failure.
3. Select one candidate per objective and the strongest matched non-response reference using development-selection units only.
4. Write an analysis lock containing:

```text
primary reference
primary k,Q
ridge rule
intervention law
minimum relevant effect
unit weights/bootstrap scheme
secondary grid and multiplicity rule
```

5. Open final-test losses once and compute paired unit effects.
6. Report all prespecified seeds and cells. Do not rerun or exclude seeds because their effect is weak or reversed.

## Baselines / ablations

Mandatory in the same output table:

```text
identity
DCT or admitted domain-standard fixed transform
best fixed single basis selected on development-selection
reconstruction-trained shared basis
coefficient-concentration-trained shared basis
response-trained shared basis
```

These are not six independent innovations; they isolate whether the outer response objective contributes beyond capacity and optimization.

## Validation

- Final-test arrays cannot influence any selected basis or reference.
- Every method uses the same fit/scoring rows and common `Q`.
- Selected bases remain orthogonal and reconstruct inputs within numerical tolerance.
- Unit-level paired effects can be regenerated from raw prediction/response rows.
- No method is dropped after observing final-test performance.

## Required artifacts

```text
reports/p20/E2_ANALYSIS_LOCK.md
reports/p20/E2_candidate_records.csv
reports/p20/E2_selection_metrics.csv
reports/p20/E2_unit_losses.csv
reports/p20/E2_paired_effects.csv
reports/p20/E2_summary.json
reports/p20/E2_failures.md
actual objective configs and logs
saved selected bases under the native result directory
```

## Acceptance criteria

`PROVISIONAL_SUPPORT` requires both:

```text
upper endpoint of the paired 95% unit-bootstrap interval < 0
absolute effect exceeds the minimum relevant effect frozen before final-test access
```

Otherwise assign `NULL_OR_REVERSED`, preserve the outcome and stop C2 expansion. A confidence interval containing zero does not establish equivalence.

## Failure handling

If one matched objective fails for a genuine implementation reason, fix that objective and rerun all methods only if final-test outcomes have not been opened. If final-test outcomes were opened, version the entire comparison as exploratory and create a new untouched confirmation split; do not patch one arm selectively.

If E2 is null/reversed, continue only compact cost reporting and failure analysis. Do not proceed to additional datasets or add routing to rescue C2.

## Sync

Commit validated Benchmark code/config/tests and compact real unit-level artifacts. Open a PR to Benchmark `dev` with the exact commands and decision. Do not write paper Results until the second prompt.

# Goal G3 — Strongest competing explanation: support search

Scientific question: If E2 is positive, is the gain attributable to a uniquely useful response-trained coordinate system, or can an information-matched structured search over existing fixed/non-response bases obtain the same benefit?

Hypothesis: Response-trained coordinates retain lower final-test response MSE than a structured/block-union estimator that receives the same response table, `k,Q` and all admissible pre-response information.

Estimand:

$$
\Delta^{support}_u=L_u(m_{response})-L_u(m_{structured\ union}).
$$

## Inputs

```text
E2 frozen primary configuration and response table
identity, fixed, reconstruction and concentration bases selected without final-test access
any pre-response descriptor admitted in G0
```

## Fixed conditions

- Same frozen predictor, target, intervention law, response rows, decoder ridge rule, `k,Q`, unit weights and final-test units.
- Total scalar support budget is `k` across every comparator.
- A descriptor may be used only if it exists before response fitting and is available to all compared methods.
- No additional model query is assigned to routing or structured search.

## Changed variable

Only the admissible support family/search changes.

## Execution

1. Evaluate `plain_union`: concatenate admitted fixed/non-response bases and run global OMP-ridge with total support `k`.
2. Evaluate `structured_union`: apply a declared block/model-based support rule to the same union and then fit at most `k` scalar coefficients.
3. If a valid descriptor exists, evaluate a descriptor-conditioned block rule and its exact same-information zero-padded union emulator. If no descriptor exists, mark this arm `NOT_APPLICABLE`; do not invent one from final labels.
4. On a low-dimensional diagnostic subset only when tractable, compare support search with exact enumeration to estimate search excess. Do not project or truncate solely to make enumeration possible.
5. Compare every arm on identical final-test scoring displacements.

## Validation

```text
same-information routed and zero-padded union predictions agree pathwise
plain and structured unions obey the same total k
no final-test labels or responses define the support prior
dictionary atoms and blocks are frozen before final-test evaluation
```

## Required artifacts

```text
reports/p20/E3_support_definitions.md
reports/p20/E3_unit_losses.csv
reports/p20/E3_paired_effects.csv
reports/p20/E3_search_diagnostics.csv, when tractable
reports/p20/E3_summary.json
reports/p20/E3_failures.md
```

## Acceptance criteria

- If response training still beats the strongest structured control under the E2 primary configuration, mark `SURVIVES_SUPPORT_CONTROL` and admit G4/G5.
- If the effect disappears or reverses, mark `EXPLAINED_BY_SUPPORT_SEARCH`; narrow C2 to a finite-query search/conditioning mechanism.
- If only plain union is available and no credible structured control is implemented, mark `UNRESOLVED`; do not claim an independent coordinate advantage.

## Failure handling

A blocked structured-support implementation does not justify replacing it with plain union and declaring victory. Record the blocker and keep C2 unresolved. Continue only independent cost or literature-admission work.

## Sync

Commit the bounded control, focused tests, configs and real unit-level artifacts to the Benchmark topic branch. Preserve all failed arms and target a PR to `dev`.

# Contribution-to-evidence map

| Contribution | Positive prior boundary | Precise question | Figure object | Mechanism / algorithm step | Contrast and metric | Evidence and decision |
|---|---|---|---|---|---|---|
| C1: budgeted coordinate geometry | Infidelity supplies quadratic response loss; sparse/dictionary theory supplies support classes | Which term changes under fixed response semantics? | Fixed response; candidate/union dictionaries | Moments; oracle support solution; fitted-support decomposition | Exact versus fitted risk; full-budget/singular/anisotropic controls | Analytic derivation and numerical tests. Do not call the least-squares identity novel |
| C2: shared-coordinate response objective | TRIM/AWD, transformed-domain PHM SHAP, task-driven dictionaries and query-efficient explanation already cover coordinate changes, outer objectives and black-box access | Does actual finite-query response training add value beyond non-degenerate matched transform objectives? | Shared orthogonal family and fixed k,Q | OMP-ridge inner solve; fresh response score; explicit mean aggregation; independent selection | Response versus best-k reconstruction versus attribution-tail objective; same family/split/aggregation; structured-support controls; paired unit MSE | Full reconstruction and L2 attribution controls are proven degenerate; linear-isotropic oracle equivalence is explicit. Real-data benefit unresolved |
| C3: information-matched containment | Structured sparsity and REAL-X/FastSHAP already motivate structure and confound controls | Does a route beat a same-information union class or merely one solver? | Routed block; zero-padded union equality | Same rule, descriptor and Q transcript; independent union multiplication | Max prediction discrepancy; plain-union and shuffled-descriptor unit MSE | Exact zero discrepancy; synthetic plain-union gap not a routing-class advantage |

## Frozen controlled experiment

`python experiments/p19/toy.py --output results/paired_control`

Seed 7; 12 signal dimensions + unperturbed context; fixed tanh predictor; identity,
DCT and eight random bases; k=1; Q=3,6,12,24; 128 scoring queries; 40 selection and
120 test units per budget; ridge=1e-4; Gaussian signal displacement scale=0.5.
No predictor training or label inference occurs. All methods share responses
within Q; separate Q values have fresh units. The descriptor is constructed with
the synthetic response mechanism, so it is not independently demonstrated real
context. The shuffled descriptor is a negative control, not a fair replacement
for a valid learned descriptor.

The recorded `toy_summary.json` and unit CSV derive from that command. At Q=3,
plain union MSE=0.1818393713, route=0.0432767485, matched union=0.0432767485 and
shuffled route=0.2082589102. Max route/union prediction discrepancy=0 for all four
budgets. These are executed observations, not expected values or population rates.

## Remaining decisive test

Freeze a real predictor and independent-unit data. Materialize one matched table
containing each anchor input, its construction displacements/responses and fresh
scoring displacements/responses. Under one orthogonal family, one $k$, one
development split, one mean aggregation and one selection rule, compare:
response-trained coordinates; best-$k$ sparse-reconstruction coordinates; and
best-$k$ attribution-tail coordinates whose dense response vector is estimated
from the declared development table. Full reconstruction and L2 attribution
magnitude are prohibited controls because orthogonality makes them invariant.

Then test the selected response basis against the best fixed single basis, plain
union and a prespecified structured/block union. Preserve faithful original
TRIM/AWD and task-driven-dictionary comparisons separately from matched-family
adaptations because their native objectives and access differ. Record offline
queries, online queries and actual compute separately. A null result narrows or
rejects C2; it must not be hidden by a larger architecture, different aggregation,
router, intervention law or test set. The complete protocol is
`paper/experiments/RESPONSE_OBJECTIVE_FALSIFICATION.md`.

The paper's E1–E6 name scientific contrasts, not already implemented benchmark
adapters. PHMFactory, external native readers and faithful SOTA reproduction remain
uncompleted. This writing slice does not change a PHMFactory pointer.

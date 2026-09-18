# Contribution-to-evidence map

| Contribution | Positive prior boundary | Precise question | Figure object | Mechanism / algorithm step | Contrast and metric | Evidence and decision |
|---|---|---|---|---|---|---|
| C1: budgeted coordinate geometry | Infidelity supplies quadratic response loss; sparse/dictionary theory supplies support classes | Which term changes under fixed response semantics? | Fixed response; candidate/union dictionaries | Moments; oracle support solution; fitted-support decomposition | Exact versus fitted risk; full-budget/singular/anisotropic controls | Analytic derivation and numerical tests. Do not call the least-squares identity novel |
| C2: shared-coordinate response objective | TRIM/AWD change explanatory coordinates; task-driven dictionaries use outer objectives | Does actual finite-query response training add value over matched objectives? | Shared family and fixed k,Q | OMP-ridge inner solve; fresh-within-training outer score; independent selection | Response versus reconstruction/sparsity objective with common family and budget; paired independent-unit response MSE | Implementation/reference tests exist. Real-data benefit unresolved |
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

The decisive C2 experiment is specified in
`paper/experiments/REAL_FALSIFICATION_PROTOCOL.md`.

Freeze one real predictor and split independent units into development-train,
development-select and final-test. Reuse identical response arrays, target,
intervention law, k, Q and development information for all matched-family
coordinates. The primary estimand is the paired independent-unit difference in
fresh response MSE between response-trained coordinates and the strongest
development-selected non-response coordinate objective. Test reconstruction and
response-coefficient-sparsity objectives in the same orthogonal family, then add
plain-union and information-matched structured-support controls. Preserve faithful
original TRIM/AWD/task-driven-dictionary comparisons separately from matched-family
adaptations.

Strengthen C2 only if the final-test paired effect survives the strongest
matched-family objective and is not removed by the structured-support control.
A regime-specific effect narrows C2. A null or reversed result rejects an
independent response-objective advantage and must be preserved rather than
recovered by a larger architecture, router, predictor, or changed split.

The paper's E1–E6 name scientific contrasts, not already implemented benchmark
adapters. PHMFactory, external native readers and faithful SOTA reproduction remain
uncompleted. This writing slice does not change a PHMFactory pointer.

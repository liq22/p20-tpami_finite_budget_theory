# Formulation, mechanism and evidence map

The manuscript uses Chapter 2 for prior foundations and the controlled problem;
Chapter 3 specifies the learned mechanism and comparison controls. Related Work
is retained as Chapter 4. Internal review remains outside the manuscript.

| Scientific item | Status | Equation / variable | Figure position | Method / algorithm | Experiment and claim |
|---|---|---|---|---|---|
| Fixed response and quadratic projection | Foundation: Yeh et al. | (1)–(4), s, mu_x, M, b | Fig. 1, fixed semantics and two response tables | Collection, Algorithm 1 step 1 | E1: unchanged target, uncentered/singular geometry |
| Budgeted risk decomposition | Adaptation of projection and sparse approximation | (5), (7), C_k, G_support, E_coef | Fig. 1 attribution gap; Fig. 2 actual decoder | Section 3.1, step 2 | E1/E2: distinguish approximation from estimation; not a recovery guarantee |
| Shared orthogonal coordinates | Reused representation family | (8), A_theta | Fig. 2a, shared basis | Section 3.2, steps 2/4 | Fixed family, k/Q/compute controls; not a novel transform claim |
| Actual finite-query response objective | Proposed response-specific mechanism, real-data benefit unresolved | (9)–(11), fitted a, fresh outer loss | Fig. 2a, heavy-outline loss and update | Section 3.3, step 2 | E4: response vs actual-input reconstruction vs full-coefficient concentration |
| Independent common deployment selection | Reused selection principle, matched adaptation | (12), selected A_o | Fig. 2b | Section 3.4, step 3 | E4: common response selection; frozen reference and budget, no test oracle |
| Information-matched union emulation | Containment/control result | (13), zero-padded coefficients | Fig. 2 external-control footer, not a learned module | Section 3.5; comparator experiment | E3: exact prediction equality; not a baseline that must be beaten |
| Independent-unit paired effect | Evaluation estimand | (6), L_u, Delta | Fig. 1 output; Fig. 2c scoring | Step 5 | E4/E5: negative Delta favors method; an imprecise null is unresolved |

## Retained routing evidence

The previous controlled experiment remains unchanged:
`python experiments/p19/toy.py --output results/paired_control`.
At Q=3 its recorded plain-union MSE is 0.1818393713; route and matched union
both have 0.0432767485. Their maximum prediction discrepancy is zero at
Q=3,6,12,24. This is constructed synthetic containment evidence, not C2 evidence.

## Executed matched-objective diagnostic

```bash
python src/S03_Scripts/run_response_basis.py \
  --synthetic --matched-objectives --aggregation mean \
  --steps 80 --output results/matched_synthetic
```

Seed 19; fixed four-dimensional tanh score; 24 training, 24 selection and 64 test
units; k=1, Q=24, R=48, ridge=1e-4, Adam learning rate=0.04. Each learned family
has identity plus eight checkpoints; the fixed family has ten bases. All six
methods reuse the same collected responses. The executed output has 384
unit-method rows, selected bases, candidate records and the paired estimate.

| Method | Mean test response MSE |
|---|---:|
| Identity | 0.006601735870767763 |
| DCT | 0.0055559469155895495 |
| Best fixed single | 0.001058112102890632 |
| Actual-input reconstruction | 0.0016412358483061038 |
| Coefficient concentration | 0.00005732089893958622 |
| Response | 0.000057859595378613675 |

The primary reference, chosen on development-selection data, is coefficient
concentration. The response-minus-reference paired mean is
+5.386964390274398e-7, with a 2,000-resample unit-bootstrap percentile interval
[-1.0280295640159047e-7, 1.2758767844321443e-6]. This does not demonstrate an
incremental response-objective advantage and does not demonstrate equivalence.
The original input law is spherical in this diagnostic, so reconstruction is
population-rotation-invariant here too. Its poor result is not evidence against
reconstruction on informative, non-spherical real inputs. Manuscript Section 5.2
reports this boundary alongside the full matched table.

## Executable and sampling corrections

`--matched-objectives` now instantiates Algorithm 1's three candidate-generation
objectives, common response selection, fixed-basis controls and paired scoring.
Supplied data must include actual `train_x` aligned with `train_unit_ids`.
The runner retains one row per independent unit; it does not implement a
multiple-window real-data aggregation or the separate structured-support study.

The former nonzero fit/score value-overlap rejection was removed. Independent
discrete draws can coincide. A binary counterexample shows why discarding such
coincidences would change the scoring law (zero-decoder risk 0.5 becomes 0 when
matches to the fixed construction value 1 are discarded). The old implementation
rejected coincident tables; it did not itself perform that biased filtering.
Sampling independence must be established by collection, not value inequality.

The retrieved scientific subset passed 28 tests: 12 response-basis, 8 objective,
and 8 runner tests. These include an altered-final-test-response experiment that
leaves all selected bases, trajectories and primary reference unchanged. This is
not the full repository suite, hosted CI, or real-data validation. The existing
reading build produced a 15-page PDF with 40 cited and defined keys, no missing
or unused key, and both SVGs regenerated and visually inspected. Their text and
boxes remain independently editable. The full workflow must still run before
merge into dev.

## Next discriminating experiment

Execute `REAL_FALSIFICATION_PROTOCOL.md` on one real dataset family and one
frozen predictor, with actual inputs, independent units and frozen primary
(k,Q,reference). Run the matched objectives and fixed baselines, then the
prespecified information-matched structured-support contrast. The current
synthetic finding prevents claiming an independent response-objective advantage;
it does not settle the real-data question or justify changing test units.
Native TRIM/AWD and temporal-XAI comparisons remain distinct external-validity
work. No PHMFactory pointer or submission-readiness claim is advanced.

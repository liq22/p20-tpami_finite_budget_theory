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

## Current evidence

The previous controlled experiment remains unchanged:
`python experiments/p19/toy.py --output results/paired_control`.
At Q=3 its recorded plain-union MSE is 0.1818393713; route and matched union
both have 0.0432767485. Their maximum prediction discrepancy is zero at
Q=3,6,12,24. This is constructed synthetic containment evidence, not C2 evidence.

The Chapter 2/3 implementation slice adds actual-input reconstruction and
same-Q full-coefficient concentration to the existing basis learner. Local
validation on the retrieved scientific subset passed 18 tests: 10 existing
response-basis tests and 8 matched-objective tests. This is not the full repository
suite, real-data validation or hosted CI. The spherical reconstruction test shows
why reconstruction of isotropic perturbations cannot identify a population
coordinate preference; the protocol now uses actual inputs.

## Next discriminating experiment

Execute `REAL_FALSIFICATION_PROTOCOL.md` on one real dataset family and one
frozen predictor. The minimum new input requirement is actual development x,
aligned with the response table's independent unit IDs. The library implements
all three objectives; the current response-only CLI does not execute the complete
matched-objective real study. Preserve this execution boundary.

The primary question is the paired response-objective effect against the strongest
development-selected matched proxy. Fixed-basis and structured-search controls
identify limits, while exact emulation remains a class-identity check. Native
TRIM/AWD and temporal-XAI comparisons remain distinct external-validity work.
No PHMFactory pointer, real-data claim, or submission-readiness status is advanced.

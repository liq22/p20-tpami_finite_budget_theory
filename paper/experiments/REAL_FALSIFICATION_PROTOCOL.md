# Real-data falsification protocol for C2

## Question

Does response-driven shared-coordinate learning improve finite-budget response
prediction on independent real units beyond existing transform objectives and
support priors, when predictor, response target, original-space intervention law,
development information, k, Q and unit split are fixed?

This protocol tests Contribution II only. It does not test physical
interpretability, predictor accuracy, causal validity, or state-of-the-art
diagnostic performance.

## Experimental unit and split

The independent unit is the highest non-overlapping entity available before
windowing: recording, bearing/machine run, patient, subject, or equivalent.
Windows from one unit may be used internally to form responses but must never be
counted as independent test units.

Use three disjoint unit sets:

- development-train: optimize trainable coordinate objectives;
- development-select: choose checkpoints and any finite candidate/baseline;
- final-test: compute the confirmatory estimand once.

No test unit may affect preprocessing parameters, candidate generation,
hyperparameters, support priors, checkpoint selection, or basis selection.

## Fixed response contract

For every method, hold fixed:

- frozen predictor and scalar target score s;
- original-space displacement law mu_x;
- exact fit-response table and exact fresh scoring-response table;
- k nonzero coordinate budget;
- Q scalar fitting-response budget;
- development units and final-test units;
- target labels/indices and preprocessing of predictor inputs.

The primary response is

$$
d_x(v)=s(x)-s(x-v).
$$

Every coordinate method is scored by the same fresh-response MSE after fitting
the same k-sparse decoder from the same Q responses.

## Primary estimand

For test unit u and method m,

$$
L_u(m)=\frac{1}{R}\sum_{r=1}^{R}
\left(\hat d_{u,m}(v_r)-d_u(v_r)\right)^2.
$$

Against a prespecified reference r, report the paired unit effect

$$
\Delta_u(m,r)=L_u(m)-L_u(r),
\qquad
\Delta(m,r)=\frac{1}{N}\sum_{u=1}^{N}\Delta_u(m,r).
$$

Negative Delta favors m. The primary comparison is response-trained coordinates
versus the strongest development-selected matched-family non-response objective,
not versus identity alone.

Report the unit-level paired mean difference with a 95% bootstrap confidence
interval resampling independent units. Also report median paired difference,
win fraction, mean MSE, and predefined group means as descriptive diagnostics.
Do not resample windows as if they were independent units.

## Comparator ladder

### Tier A: same coordinate family and same decoder

Mandatory:

1. identity;
2. fixed DCT or domain-standard fixed orthogonal transform;
3. best fixed single basis chosen on development-select only;
4. reconstruction-trained orthogonal coordinates;
5. response-coefficient-sparsity-trained orthogonal coordinates;
6. response-trained orthogonal coordinates.

Items 4-6 must use the same orthogonal parameterization, optimizer budget,
candidate/checkpoint schedule, unit splits, k and Q. Only the outer objective may
change.

For reconstruction training, minimize fresh sparse reconstruction error of the
same development perturbations under a k-coordinate truncation. For
response-coefficient sparsity, minimize a declared concentration penalty on
response coefficients estimated from development data; the scoring response MSE
remains untouched until comparison. These are matched-family controls, not
claims of faithful AWD/TRIM reproduction.

### Tier B: support-search controls

Mandatory:

7. plain union with global k support budget;
8. structured/block union with the same available descriptor or prior used by
   any routed/structured method;
9. information-matched routed/block-restricted decoder when such a contrast is
   reported.

The structured union is required because a route-versus-plain-union gap can be a
support-search effect. Routing is not a separate estimator-class contribution
unless it survives the same-information containment control.

### Tier C: faithful prior methods

When feasible, keep faithful TRIM, Adaptive Wavelet Distillation, and a
task-driven dictionary baseline separate from Tier A. Preserve their native
objectives and report any unavoidable difference in model access or offline
training. Do not silently rewrite them into the proposed method's coordinate
family.

## Budget grid

The minimum confirmatory grid is

- k in a small prespecified set spanning severe to moderate sparsity;
- Q in at least three levels including Q close to k and a clearly less
  query-limited regime;
- one fixed ridge rule selected without final-test access.

A method claim must not depend on one cherry-picked (k,Q) pair. The paper may
summarize one primary pair only if it was declared before final-test inspection.

## Attribution diagnostics

For each method and (k,Q), decompose or estimate:

1. oracle coordinate approximation C_k when computationally tractable on a
   diagnostic subset;
2. support-search excess using a stronger/exhaustive support comparator on low
   dimension or a controlled subset;
3. coefficient-estimation excess conditional on the selected support;
4. final finite-Q response MSE.

These diagnostics are mechanism evidence. Only item 4 is the primary empirical
endpoint.

## Minimum real experiment

Start with one dataset family and one frozen predictor.

Required outputs:

- explicit unit IDs and train/select/test split;
- predictor checkpoint and scalar target definition;
- perturbation law;
- exact k,Q grid;
- one response table shared by all compared methods;
- unit-level response MSE table;
- paired effect table and confidence intervals;
- selection-only record for every trainable/fixed candidate;
- offline training cost, online scalar queries, and measured runtime reported
  separately.

Do not expand to additional benchmark families until this experiment can
distinguish the response objective from matched objectives and support priors.

## Go / revise / stop rule

Strengthen C2 only if response-trained coordinates improve the primary paired
estimand over the strongest matched-family control on final-test units and the
effect is not removed by the structured-support control.

Revise C2 to a conditional mechanism claim if gains appear only at particular
(k,Q) regimes or only through easier support search.

Reject an independent response-coordinate advantage if the matched-family
control is indistinguishable or better across the prespecified grid. Preserve
that null result; do not add routing, MoE, a larger predictor, or a different
test split to recover the claim.

## Expansion after the first falsification test

Only after the first real experiment supports a stable effect, extend to
multiple external time-series families. Each added family must preserve the same
scientific contract even if the native predictor architecture and physical
meaning of a unit differ.

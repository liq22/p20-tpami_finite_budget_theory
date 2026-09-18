# Real-data falsification protocol for C2

## Question and scope

Does directly training shared coordinates on finite-query response error improve
fresh prediction of the same frozen model response beyond matched reconstruction,
coefficient-concentration, fixed-basis and support-prior controls?

This is a fixed-response claim. Response MSE alone does not establish diagnostic
accuracy, physical meaning, temporal localization or generic explanation quality.

## Independent units and fixed information

Start with one real dataset family and one frozen predictor. Choose the
independent unit before windowing: subject, patient, recording, machine run or
another defensible non-overlapping entity. Keep development-training,
development-selection and final-test units disjoint. Freeze predictor input
preprocessing, checkpoint provenance, scalar target rule, original-space
intervention law, query counts and unit weighting.

All methods have the same actual input vectors, context availability,
construction responses and separate scoring responses. A scalar response is

$$d_x(v)=s(x)-s(x-v).$$

Charge Q perturbed evaluations and one reusable base evaluation per new input.
Report development, selection, construction and evaluation calls separately.
Do not charge a gradient as one scalar query or regard offline training as free.

The current reference batch supports one input per independent unit. Choose that
input with a rule frozen before outcome inspection. A multiple-window study
needs explicit within-unit weighting, not window IDs masquerading as unit IDs.
No test outcome may choose preprocessing, training groups, candidates or priors.

## Primary estimand and analysis lock

For fixed within-unit weights summing to one,

$$
L_u(m)=\sum_j w_{uj}\frac1R\sum_r
[\widehat d_{uj,m}(v_{ujr})-d_{x_{uj}}(v_{ujr})]^2,
\qquad \Delta_u(m,m_0)=L_u(m)-L_u(m_0).
$$

Negative Delta favors m. Freeze the primary (k,Q) pair, primary matched-family
reference, ridge rule, group aggregation and statistical rule on development
units. The primary reference is the strongest development-selected matched
proxy objective, not identity alone. Do not select a reference by test losses.

Report the paired unit mean, a 95% unit-resampling bootstrap interval, raw MSE,
and descriptive median difference, win fraction and predefined group means.
Prespecify stratified resampling or a target group mixture when that is the
estimand. Do not resample windows or queries as independent observations.

An interval containing zero is inconclusive, not proof of equivalence. A claim
of negligible practical benefit requires a justified prespecified margin and
sufficient precision. Do not impose an arbitrary 1–2% effect cutoff or require a
positive result to justify retaining an experiment.

Keep a small prespecified grid of k and at least three Q levels, including a
query-limited and a less limited regime. Other cells are secondary; separate
inferential claims require multiplicity adjustment or simultaneous uncertainty.
Do not choose significant cells after final-test inspection.

## Tier A: matched coordinate objectives

Mandatory comparisons: identity; DCT or a fixed domain transform; the best
selection-chosen fixed basis; reconstruction-trained coordinates;
coefficient-concentration-trained coordinates; response-trained coordinates.

The three trained objectives share A=exp(S), identity initialization, optimizer,
step budget, checkpoint schedule, decoder, k, Q, ridge and available information.
Only the outer objective changes. Use a common aggregation and select all
candidate families by fresh response error on separate selection units.
This isolates candidate-generation objectives, not entirely response-free
pipelines. Record fixed-family and learned-family candidate counts separately.

Let H_k retain the k largest-magnitude coordinates:

$$
\ell_{\rm rec}(A;x)=\|x-A^T H_k(Ax)\|^2,
$$

$$
\widehat\beta_x=(V^TV/Q+\lambda I)^{-1}V^Td/Q,
\quad
\ell_{\rm coef}(A;x)=
\frac{\|A\widehat\beta_x-H_k(A\widehat\beta_x)\|^2}{\|\widehat\beta_x\|^2}
$$

with the coefficient loss defined as zero for zero beta_hat. The response
objective uses fresh development outer error of the actual Q-query decoder.

**Reconstruction uses actual input x.** Full orthogonal reconstruction is
identically zero; population truncation loss on spherical perturbations is
rotation invariant. Do not build the competing reconstruction objective solely
from that degenerate law. **Concentration uses full fitted coefficients**, not
an already k-sparse decoder. Do not give this proxy extra queries or gradients.

These are matched-family controls, not faithful TRIM or AWD implementations.
`train_basis` implements all three at library level. The existing response-only
CLI is not yet the complete three-objective real-data runner; the next execution
slice must supply actual input vectors and retain unit identities.

## Tier B: support controls and mechanism attribution

Compare plain union search under a total global k budget with an
information-matched structured/block union when a descriptor or support prior is
available. No structured method receives an otherwise unavailable descriptor.

A same-information fixed union can exactly emulate a routed decoder by block
zero-padding. This is an equality control for the routing interpretation, not a
performance hurdle. Within the stated assumptions routing cannot escape that
prediction class merely by outperforming plain union-OMP.

When tractable, estimate coordinate approximation, selected-support excess and
coefficient excess separately. Use an exact low-dimensional oracle or an
independent diagnostic response set. Additional diagnostic queries are evaluation
costs, not construction information, and must not choose the deployed basis,
support or primary reference. Estimated component differences need not inherit
the population decomposition's nonnegativity at finite sample size.

If a gain vanishes against structured search, support identification is a
plausible mechanism, not a proved mediation effect. Narrow the claim and inspect
the component diagnostics rather than asserting independent approximation gain.

## Tier C: faithful methods and external validity

Keep faithful TRIM, AWD and task-driven dictionary methods separate from Tier A.
Add ContraLSP, TimeX++ and TIMING when their native task and model-access
requirements apply. Preserve native objectives and report differing predictor
access, offline training, intervention semantics and explanation outputs.

Use native localization, retention or signed-attribution metrics where
compatible. Do not turn masks or path attributions into response coefficients
without a mathematical adaptation, or rank incomparable raw metrics. These
comparisons address external validity, not the primary objective intervention.

## Robustness and computational boundary

Use one group for the first study unless meaningful groups are available before
fitting. For a multi-group study, compare mean training with worst-group excess
using the same group definitions across objectives. Worst-group excess over
identity is not worst absolute risk.

The dense model has p<=256, O(p^2) matrix storage and O(p^3) matrix-exponential
updates. Report actual dimension, training/selection time, online fitting time,
peak memory and query counts. Do not claim long-sequence scalability by silently
reducing input dimension. A structured family is a separate future intervention.

Before a broad claim, repeat under a prespecified reasonable alternative
intervention law or restrict the conclusion explicitly to the primary law.
Preserve ranking reversals. A second frozen predictor or initialization is
required for model-independent generality, not for the first conditional test.

## Required outputs and decision

Retain input/unit split, predictor checkpoint and target, intervention law,
(k,Q,lambda), trained/fixed candidate selection, unit loss rows, paired effect
intervals and separated costs. Do not report a complete baseline comparison
until all mandatory implemented methods have actually run.

Strengthen a finite-budget C2 claim when the primary paired effect shows
improvement with adequate precision against the matched reference; use the
prespecified other controls and budget cells to delimit that statement.
Do not require significance against every method in every cell to support a
narrow, prespecified claim.

Revise to a regime-specific or support-identification finding when evidence
supports only that interpretation. Treat imprecise nulls as unresolved. Reject
an asserted useful advantage when a precise comparison excludes the prespecified
useful effect or a control is reliably better. Retain all null/reversed results;
do not rescue the claim by changing the predictor, split or primary budget.

Only after the first real study yields an interpretable decision should the
experiment expand to additional time-series families.

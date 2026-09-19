# Fixed-union containment and finite-query emulation

## Definitions

Fix a predictor, target, original-space intervention law and finite collection
$\mathcal A=\{A_0,\ldots,A_{J-1}\}$. Condition on all information used to construct
that collection. A new explanation has input $x$, descriptor $z$, development
information $\mathcal D$, and a transcript $T_Q$ of $Q$ scalar model responses.
Construction responses are not fresh scoring responses. The output support
budget $k$ counts nonzero scalar coefficients, not blocks or basis size.

The fixed union is $\Psi(v)=[A_0v;\ldots;A_{J-1}v]$. “Fixed” refers to its
candidate dictionary, not to per-input coefficients or support decisions.

## Proposition 1: oracle containment

For every input and common displacement law,

$$R_{k,\mathrm{union}}^*(x)\le\min_j R_k^*(A_j;x).$$

**Proof.** Embed any feasible $a$ for candidate $j$ as the coefficient block $j$
of the union, with all other blocks zero. The support count remains at most $k$
and the predictions agree for every displacement. Take the infimum over union
coefficients, then over each candidate and over $j$. No invertibility, moment
conditioning, or orthogonality is needed for containment. Finite second moments
are needed only if one wants finite squared risks.

## Proposition 2: same-information finite-query emulation

Let an arbitrary measurable routed algorithm map $(\mathcal D,x,z,T_Q,\xi)$ to
$(j,\widehat a)$, with $\|\widehat a\|_0\le k$, where $\xi$ is its random seed.
Assume $j$ and $\widehat a$ are fixed before the fresh scoring displacement is
revealed. Then a union algorithm receiving the same information and random seed
can satisfy, simultaneously for every scoring displacement,

$$\widetilde a^\top\Psi(v)=\widehat a^\top A_jv,
\qquad \|\widetilde a\|_0\le k.$$

**Proof.** Run the same routed algorithm. Set the union coefficient vector to
zero, and put $\widehat a$ in block $j$. The inner product reduces to the routed
inner product. No additional model query is required. For adaptive construction,
the union can reproduce the same query choices inductively from the same history.
Coupling the random seed gives pathwise equality, hence equal conditional,
unconditional, empirical and population loss under any common loss function.

This is a class-containment observation, not a new sparse-recovery theorem.
Structured-support methods already motivate restrictions on a union's admissible
supports [@baraniuk2010]. The present statement identifies the necessary control
for the proposed finite-response comparison.

## Consequences

1. Finite $Q$ alone cannot establish that the routed estimator class is better
   than a union class permitted the same information and support rule.
2. Plain union-OMP can lose to a routed implementation. That identifies a
   difference between particular support-search procedures, not a contradiction
   of either proposition.
3. If context is available only to the route, information has changed. If it is
   available to both but only one uses it, this is an inductive-bias or algorithm
   comparison; the zero-padded emulator supplies the missing control.
4. Union materialization is unnecessary for emulation. A lazy implementation
   may compute only the selected block. An efficiency claim must specify actual
   resource restrictions rather than assign dense costs to all union methods.
5. A gate depending on each fresh scoring displacement changes the explanatory
   function class; it is not the fixed-per-explanation gate studied above.

## Headroom and estimation must not be conflated

For genuine conditional risks $r_j(x)$, the quantity

$$H=\min_j\mathbb E[r_j(X)]-\mathbb E[\min_jr_j(X)]\ge0$$

measures an oracle's headroom over a globally fixed candidate. It says nothing
about superiority over the union. Replacing $r_j$ by noisy test MSE and minimizing
on that same test table creates hindsight selection; it is not an unbiased
estimate of the population minimum. The numerical routine reports this only as
`hindsight_table_gap_not_population_headroom`.

## Direct numerical check

`context_matched_union` independently computes routed and union predictions.
Tests cover multiple dictionaries, query and support budgets, redundant atoms,
and zero responses. The controlled nonlinear experiment also evaluates a
shuffled descriptor. Its maximum route/emulator prediction difference is zero
at $Q\in\{3,6,12,24\}$. This identity control uses the same selected rule; it is
not a newly learned competitor and is not evidence that every union optimizer
will find the same solution.

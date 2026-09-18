# Nonlinearity and query limits

## T3. Nonlinear approximation uses distance to a decoder class

For a fixed x define the linearized response d_lin(v)=grad s(x)^T v. Let
F_k(A)={v -> a^TAv: ||a||_0<=k}. For square-integrable responses, distance to
any nonempty subset of a normed space is 1-Lipschitz. Therefore

$$|\sqrt{R_k^*(A;d)}-\sqrt{R_k^*(A;d_{lin})}|
\le \|d-d_{lin}\|_{L^2}.$$

**Proof.** For every f in F_k, ||d-f|| <= ||d_lin-f||+||d-d_lin||. Take infima
and repeat with d and d_lin exchanged. Convexity of F_k is not required.

If the Hessian operator norm is at most H along every segment x-t v, t in[0,1],
Taylor's theorem gives

$$\|d-d_{lin}\|_{L^2}\le {H\over2}\sqrt{E\|v\|^4}.$$

Consequently a new upper endpoint below the baseline lower endpoint certifies
strict oracle improvement. A smaller upper bound alone does not.

For ReLU networks crossing an activation boundary, a zero almost-everywhere
Hessian does not justify H=0. Example: s(x)=max(0,x), x=0.1, v=0.2; the response
is 0.1 whereas its local linearization predicts 0.2. Use the exact moment
characterization or a valid path remainder, not the smooth theorem.

If reconstruction and intervention implementation deviate from the original
inputs by eps_rec and eps_int, and s is L_s-Lipschitz, the response discrepancy
is at most L_s(eps_rec+eps_int). Our orthogonal reference implementation avoids
reconstruction loss; interventions are always collected in original coordinates.

## T4. Restricted coefficient estimation

Fix A and support S. Assume the population G_SS has eigenvalues in [mu,Lambda],
mu>0. Write ||hatG-G||op<=eps_G<mu and ||hatb-b||<=eps_b. For lambda>=0,

$$\hat a=(\hat G+\lambda I)^{-1}\hat b,\qquad a^*=G^{-1}b.$$

Then

$$E_{coef}\le\Lambda
\left[{\epsilon_b+(\epsilon_G+\lambda)\|a^*\|
\over\mu-\epsilon_G+\lambda}\right]^2.$$

**Proof.** Subtract the two normal equations:
(hatG+lambda I)(hat-a-a*)=(hatb-b)-(hatG-G+lambda I)a*.
The inverse operator norm is at most 1/(mu-eps_G+lambda); applying triangle and
spectral bounds gives the result.

This is a deterministic fixed-support bound, not an automatic confidence bound
from Q samples. Statistical use requires valid moment concentration uniformly
over data-selected supports/bases, or separate support-selection and fitting
data. The implemented OMP-ridge decoder is not given an unsupported finite-Q
confidence claim. Singular population risk is defined by T1, but this estimation
bound needs restricted conditioning. Ridge stabilizes a solve; it does not
create missing information.

## Query budget and information boundary

The implementation charges Q construction responses per new explanation,
requiring Q+1 forward examples when the unperturbed prediction is not cached.
Development-basis learning costs and score-only reference evaluations are
reported separately. Batch calls are not counted as one oracle example.

For an unknown w~N(0,I_p), suppose Q<p noiseless scalar linear measurements of w
are acquired adaptively before a fresh isotropic scoring direction v is revealed.
There is no previous information about this w. Posterior covariance retains
trace at least p-Q: each scalar measurement removes at most one direction.
Thus any estimator has Bayes response risk at least sigma_v²(p-Q).

Adaptivity does not evade this bound: conditional on a realized history, the
selected measurement vectors impose at most Q linear constraints; the remaining
Gaussian orthogonal subspace has unit variance. This argument requires measurable
adaptive queries and the stated oracle. It does not cover access to the weights,
a complete gradient vector, a basis learned using the same unknown w, or queries
chosen after the scoring direction is revealed. In the latter case one query
along v reveals the response exactly. The reference model's amortized development
information means this lower bound is a boundary example, not its performance
bound.

Checks include the smooth remainder inequality, the ReLU counterexample,
fixed-support coefficient bound and hidden-subspace query example.

# Fixed-response geometry

## Object and prior-art boundary

Fix a predictor, an output target and an input x. Draw an original-space
intervention v from a declared distribution and define d(v)=s(x)-s(x-v).
The explanation predicts this scalar response; it is not a causal account of
the data-generating mechanism. Infidelity already studies this loss and its
unrestricted least-squares solution [yeh2019]. We specialize that geometry to
coordinate budgets, singular intervention moments and an estimated decoder.

An invertible linear basis A and a decoder a predict a^T A v. A sparse
explanation has at most k nonzero coordinates of a. The pretrained function and
distribution of v do not change when A changes. Gradients, IG contributions and
occlusion effects are not interchangeable coefficient vectors [sundararajan2017].
The implemented method fits a response decoder rather than relabeling these
native attribution outputs.

## T1. Exact decomposition, including singular moments

**Assumptions.** E||v||² and E[d²] are finite; A is invertible; no intercept is
included. Define the uncentered moments

$$M=E[vv^T],\quad b=E[vd],\quad c=E[d^2],\quad \beta=M^\dagger b.$$

Then b is in range(M), and

$$R(A,a)=E[(a^TAv-d)^2]
=R_{full}+\|A^Ta-\beta\|_M^2,\qquad R_{full}=c-b^TM^\dagger b.$$

**Proof.** If z is in ker(M), then E[(z^Tv)²]=0, so z^Tv=0 almost surely
and z^Tb=0. Thus b is orthogonal to ker(M) and is in range(M). Expanding the
quadratic and using M beta=b completes the square. This proof does not require
zero-mean interventions; replacing M by covariance generally gives a different
problem.

For a fixed support S, let G=AMA^T and t=Ab. The minimum-norm solution and risk are

$$a_S^*=G_{SS}^\dagger t_S,\qquad R_S^*=c-t_S^TG_{SS}^\dagger t_S.$$

The same null-space argument proves t_S belongs to range(G_SS), so the formula
also holds for a singular support Gram matrix. The exact k-coordinate oracle is

$$R_k^*(A)=\min_{|S|\le k}R_S^*(A)
=R_{full}+C_k(A),\quad C_k(A)=\min_{\|a\|_0\le k}\|A^Ta-\beta\|_M^2.$$

The exhaustive solver is restricted to p<=12. The learned model uses greedy
support selection; it is never reported as this oracle.

## T2. Four terms separate representation from estimation

For any chosen support S and coefficient estimate hat-a on S, define

$$G_{support}(A,S)=R_S^*(A)-R_k^*(A)\ge0,$$

$$E_{coef}(A,S,\hat a)=
(\hat a_S-a_S^*)^TG_{SS}(\hat a_S-a_S^*)\ge0.$$

The exact identity is

$$\boxed{R(A,\hat a)=R_{full}+C_k(A)+G_{support}(A,S)+E_{coef}(A,S,\hat a).}$$

**Proof.** Add and subtract R_S* and R_k*. The restricted normal equations make
the cross term in R(A,hat-a)-R_S* zero, including singular G_SS. This gives the
last quadratic term. The other two differences follow from minimization.

The identity is pointwise in the fitted support and coefficients. Population
risk uses a fresh intervention, independent of the fitting queries. Taking an
expectation over those queries preserves the decomposition. Training residuals
are not an unbiased substitute for population risk after support selection.

A lower oracle error C_k does not guarantee a lower actual error: support-search
or coefficient error can erase the gain. If an upper bound E_new is available,

$$C_k(A_{new})+G_{support}(A_{new},S_{new})+E_{new}<C_k(A_{base})$$

is sufficient for improvement over even the baseline's oracle. This condition
is deliberately stronger than comparing two upper bounds.

## Consequences and limits

**Full budget.** For k=p all invertible linear A span the same decoder class,
so R_p*(A)=R_full. It need not be zero for nonlinear d. For Gaussian v and
 d=w^Tv+lambda v_1², R_full=3 lambda². An arbitrary nonlinear representation
changes the decoder class; full-budget invariance then needs pullback closure.

**Isotropic linear case.** If d=w^Tv and M=sigma² I with orthogonal A,
R_k*=sigma²||Aw-H_k(Aw)||². Haar sends (1,1)/sqrt(2) to one coordinate, but
spreads (1,0) over two. There is no universally helpful fixed basis. If w is
isotropic on the sphere and A is fixed independently of w, Aw and w have the
same distribution, giving equal expected tail energy.

**Anisotropy.** M=diag(100,1), w=(0.2,1), k=1: gradient magnitude selects the
second coordinate and incurs risk 4; the first coordinate incurs risk 1.
Therefore training directly on response error is preferable to assuming that
attribution sparsity always predicts response fidelity.

**Interpretability.** A dense learned coordinate is not automatically a named
physical concept. Report its loadings and response semantics, not causal or
physical meaning without independent validation.

Checks: `test_response_geometry.py` covers singular moments, uncentered
interventions, exact fits, full-budget invariance and beneficial/harmful bases.

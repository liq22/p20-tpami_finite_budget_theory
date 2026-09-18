# Matched objective controls for shared orthogonal coordinates

## Why the control objectives must be defined before the real experiment

Contribution II asks whether coordinates trained on the response error of the
actual finite-query sparse decoder add value beyond more conventional transform
objectives. For an orthogonal basis, two superficially natural controls are
degenerate and therefore cannot answer this question.

Let \(A\in\mathbb R^{p\times p}\) be orthogonal and let \(H_k(u)\) retain the
\(k\) largest-magnitude entries of \(u\).

## 1. Two invalid controls

### Full reconstruction is invariant

For any \(x\),

\[
A^\top A=I
\quad\Longrightarrow\quad
\|x-A^\top A x\|_2^2=0.
\]

Thus a full-dimensional orthogonal autoencoding loss cannot rank candidate
bases. A basis-dependent value from this objective indicates an implementation
or protocol mismatch rather than a learned reconstruction advantage.

### L2 attribution magnitude is invariant

For any raw-coordinate coefficient vector \(\beta\),

\[
\|A\beta\|_2^2=\|\beta\|_2^2.
\]

Therefore an L2 attribution penalty also cannot train an orthogonal basis. The
control must reward concentration, not total energy.

## 2. Non-degenerate matched controls

### Sparse reconstruction

Use the exact best \(k\)-term reconstruction loss in the same orthogonal family:

\[
J_{\mathrm{rec},k}(A)
=
\mathbb E_x
\left[
\|x-A^\top H_k(Ax)\|_2^2
\right]
=
\mathbb E_x
\left[
\|Ax-H_k(Ax)\|_2^2
\right].
\]

This asks whether the coordinates compact the observed signal, without using
the predictor response as the training target.

### Attribution-tail sparsity

Estimate a dense raw-coordinate local response vector \(\widehat\beta\) from
the declared development response table and minimize its best \(k\)-term tail:

\[
J_{\mathrm{attr},k}(A)
=
\mathbb E
\left[
\|A\widehat\beta-H_k(A\widehat\beta)\|_2^2
\right].
\]

The dense vector must be computed from the same development units and declared
response information used by the matched comparison. Gradient or Integrated
Gradients access is a different information regime and belongs in a faithful
external-method comparison, not this control.

### Finite-query response objective

The proposed objective remains the fresh response error of the actual decoder:

\[
J_{\mathrm{resp},Q,k}(A)
=
\mathbb E
\left[
(\widehat a_{Q,k}(A)^\top Av-d(v))^2
\right],
\]

where \(\widehat a_{Q,k}(A)\) is obtained by the declared support search and
restricted coefficient fit from \(Q\) construction responses. Fresh
development-scoring responses enter the outer objective and final evaluation
uses independent units.

All three matched objectives use the same orthogonal parameterization,
development units, candidate-selection split and \(k\). Predictor-response
tables are made available under one declared protocol; a control may ignore
information that its native objective does not require, but no control receives
additional hidden information.

## 3. Limiting-case equivalence and the finite-query penalty

The isotropic-linear consequence of T1 already gives the relevant null model.
If

\[
d(v)=\beta^\top v,
\qquad
\mathbb E[vv^\top]=\sigma^2 I,
\]

then for orthogonal \(A\),

\[
\boxed{
R_k^*(A)
=
\sigma^2
\|A\beta-H_k(A\beta)\|_2^2.
}
\]

Thus attribution-tail sparsity is exactly the coordinate-oracle objective up to
the constant \(\sigma^2\). This is prior geometry reused as a matched control,
not a second theorem.

Taking the expectation of T2 over the \(Q\) construction queries, define

\[
\Gamma_{Q,k}(A)
=
\mathbb E_{T_Q}
\left[
G_{\mathrm{support}}(A,S(T_Q))
+
E_{\mathrm{coef}}(A,S(T_Q),\widehat a(T_Q))
\right]
\ge 0.
\]

For a fixed input,

\[
\boxed{
\mathcal J_{Q,k}(A)
=
R_{\mathrm{full}}
+
C_k(A)
+
\Gamma_{Q,k}(A).
}
\]

This identity locates the finite-query mechanism tested by Contribution II. In
the isotropic-linear oracle limit,
\(C_k(A)=\sigma^2J_{\mathrm{attr},k}(A)\). Outside that limit,
attribution-tail can cease to rank bases by response risk because intervention
anisotropy changes the \(M\)-geometry, while finite \(Q\) introduces
basis-dependent support and conditioning penalties through
\(\Gamma_{Q,k}\).

The objectives therefore separate when nonlinear response residuals,
anisotropic or correlated intervention moments, finite-query support search or
coefficient estimation matter. The real experiment asks whether directly
optimizing an empirical counterpart of \(C_k+\Gamma_{Q,k}\) improves held-out
response prediction beyond objectives that target signal compression or an
oracle-style attribution tail. A null result means the estimator-aware term has
no practically detectable value in the tested regime.

## 4. Aggregation is not part of the claimed objective gain

A second confound is aggregation across units. Define an explicit operator
\(\rho\) applied to per-unit losses. The primary matched-objective comparison
uses

\[
\rho_{\mathrm{mean}}(\ell)
=
\frac{1}{n}\sum_{u=1}^n\ell_u.
\]

A predefined worst-group operator may be reported as a robustness ablation, but
if used it must be applied identically to response, reconstruction and
attribution-tail objectives. A gain from changing mean aggregation to
worst-group aggregation cannot be credited to response-driven coordinates.

## 5. Falsifiable decision

Contribution II survives its first real-data test only if the response-trained
basis reduces paired held-out response MSE relative to both non-degenerate
matched objectives and the strongest fixed/structured-support control under the
same response semantics and budgets.

A null result is scientifically informative: it reduces the method to an
objective-equivalent coordinate learner under the tested regime. The result
must not be rescued by adding a router, changing the intervention law, changing
the aggregation, or selecting the best method on the evaluation units.

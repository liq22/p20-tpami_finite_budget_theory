---
name: scientific-critical-thinking
description: Pressure-test one scientific claim, method, interpretation, or design by identifying the strongest competing explanation and the few validity threats that would change the conclusion or next experiment.
---

# Scientific Critical Thinking

## Purpose

Improve a scientific decision through proportionate criticism. The product is a
stronger claim, experiment, method, or interpretation—not a comprehensive bias
catalogue, GRADE worksheet, or multi-file audit trail.

## Workflow

1. State the exact claim or decision under review and its current scope.
2. Identify the evidence that directly supports it and separate:

   ```text
   observation
   inference
   mechanism interpretation
   generalization
   ```

3. Formulate the strongest plausible competing explanation.
4. Check only validity threats that could change the conclusion, such as:
   - leakage or unfair information access;
   - wrong experimental/independent unit;
   - confounding or selection;
   - mismatch between question, estimand, method, and metric;
   - implementation–method mismatch;
   - selective reporting or post-hoc storytelling;
   - unsupported causal or general claims;
   - uncertainty too large for the stated conclusion.
5. Identify the smallest observation, intervention, analysis, or source check that
   distinguishes the explanations.
6. Decide the strongest conclusion currently allowed: retain, narrow, revise,
   reject, or leave unresolved.
7. When authorized, apply the correction directly to the claim, method,
   experiment, or manuscript. Otherwise return the decision-changing finding.

Use a formal risk-of-bias, GRADE, reporting-standard, or ethics framework only
when the study type or user request requires it. Do not apply every framework to
every paper.

## Output Contract

Produce:

- the claim or decision being tested;
- the strongest supporting evidence;
- the strongest competing explanation;
- at most five material validity threats;
- the decisive test or correction;
- the conclusion and boundary that remain justified.

Classify issues only when useful:

```text
P0: invalidates the central conclusion
P1: major missing evidence or reasoning
P2: important but non-fatal
P3: presentation
```

## Boundaries

- Do not require every concern to quote an artifact, name a formal fallacy, carry
  a GRADE score, or update several logs in order to be actionable.
- Do not manufacture bias, ethics, reproducibility, or statistical concerns to
  appear thorough.
- Do not run a repository-wide claim audit when one claim or experiment is under
  review.
- Do not block critique because a target journal or reporting guideline is unset.
- Do not treat a checklist item as evidence that the scientific issue is solved.
- Do not create review packets, provenance records, hashes, receipts, or finding
  ledgers.
- Do not use Python to score claim quality or enumerate theoretical failure
  combinations.
- Do not change a claim when no scientific basis changed; if evidence is missing,
  say exactly what remains unknown.

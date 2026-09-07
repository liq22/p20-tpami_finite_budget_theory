---
name: peer-review
description: Review a manuscript or selected claim with only the scientific lenses needed, prioritize new independent P0/P1 issues, and stop expanding review when additional lenses no longer change the revision decision.
---

# Peer Review

## Purpose

Pressure-test the paper before submission or revision. The product is a short set
of decision-changing scientific concerns and concrete revisions. Review is not a
quota of personas, sections, standards, checklists, or findings.

## Workflow

1. Fix the review scope: full paper, selected section, named claim, or reviewer
   concern.
2. State the paper's central question, current claim, strongest evidence,
   hypothesis provenance, largest uncertainty, and intended contribution.
3. Record the P0/P1 issues already known so repetition is not counted as new
   information.
4. Select only the lenses required by the paper:
   - novelty and closest-prior-art falsification;
   - theory, counterexamples, and mechanism;
   - methodology and implementation fidelity;
   - experimental information fairness and statistics;
   - generalization and failure boundary;
   - domain validity and reproducibility;
   - positioning, writing, figure function, or venue fit;
   - adversarial rejection.
5. Test the six paper questions:

   ```text
   What is the scientific problem?
   Why are current methods insufficient?
   What new idea is introduced?
   Why should it work?
   What evidence shows when it works and fails?
   What new understanding remains?
   ```

6. For each review lens report:

   ```text
   Decision:
   New independent P0/P1 issue:
   Weakest claim:
   Evidence missing:
   Strongest alternative explanation or counterexample:
   Required revision:
   ```

7. Prioritize:

   ```text
   P0: invalidates the central conclusion
   P1: seriously weakens the contribution
   P2: important but non-fatal
   P3: presentation
   ```

8. Return at most three P0/P1 concerns overall and a small number of P2/P3 items.
   Do not manufacture concerns to fill categories.
9. Stop adding reviewer lenses when consecutive independent lenses no longer find
   a new P0/P1 issue. Repetition of an existing issue does not count as new
   information.
10. When revision is requested, pass the concerns into the actual revision loop:

   ```text
   concern -> root cause -> required evidence -> experiment/theory/method/analysis/rewrite
   -> observed result -> claim update
   ```

A reporting-standard, ethics, image-integrity, citation, or reproducibility check
is invoked only when the manuscript type or user explicitly requires it.

## Output Contract

Produce a concise review containing:

- recommendation: accept / minor / major / reject, when requested;
- central contribution that currently survives;
- new independent P0/P1 issues in priority order;
- fatal flaw status;
- weakest claim and missing evidence;
- strongest prior art, alternative explanation, or counterexample;
- required experiment/theory/method/analysis/rewrite;
- important failure or generalization boundary;
- one ordered revision plan;
- review stop decision and whether another lens is expected to add new major
  scientific information.

Write `paper/reviews/ai_review.md` only when the user requests a persistent review
artifact. Do not automatically mirror findings into multiple logs or response
files.

## Boundaries

- Do not require a complete section-by-section audit, fixed reviewer count,
  reporting-standard checklist, ethics checklist, figure-integrity checklist,
  reference-balance check, and reproducibility audit for every manuscript.
- Do not count the same concern expressed by several reviewer personas as several
  independent issues.
- Do not continue reviewer theatre after the marginal number of new P0/P1 issues
  has fallen to zero.
- Do not require every finding to populate `open_questions`, `change_log`,
  `decision_log`, and `response_to_reviewers`.
- Do not treat missing internal matrices or logs as manuscript flaws when the
  scientific evidence can be inspected directly.
- Do not block review solely because venue metadata or one supporting record is
  missing; qualify the affected judgment.
- Do not invent reviewer comments, experiments, source support, or fatal flaws.
- Do not use hashes, receipts, reviewer packets, PASS matrices, or full project
  validation as review evidence.
- Do not let wording and formatting comments displace unresolved P0/P1 science.
- Review-only mode does not silently edit the manuscript. Revision mode changes
  the manuscript first and then explains the change.

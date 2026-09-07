---
name: 05-claim-evidence
description: Decide what the current theory, experiments, analyses, and verified literature justify saying, track hypothesis provenance, separate fact from inference, and select only the missing evidence that could change the conclusion.
---

# 05 Claim Evidence

## Purpose

Align paper conclusions with the actual scientific basis. The product is an
accurate claim, a narrower boundary, or a decision to reject or test the claim
further—not a provenance or matrix-completion exercise.

## Workflow

1. State the exact claim at risk and classify its intended level: descriptive,
   associational, mechanistic, causal, generalization, or design principle.
2. Identify the largest unresolved uncertainty threatening that claim and the
   strongest competing explanation.
3. Inspect the relevant completed results, analysis, theory, and verified sources.
4. Separate:

   ```text
   fact: directly observed or established by the source
   inference: reasonably derived from facts and assumptions
   exploratory finding: observed but not independently confirmed
   hypothesis: plausible but unresolved
   ```

5. Mark evidence state:

   ```text
   literature-supported
   theory-supported
   exploratory evidence
   independent confirmation
   post-hoc interpretation
   unsupported
   ```

6. Mark hypothesis provenance:

   ```text
   H0: proposed before observing the relevant result
   H1: inspired by exploratory evidence
   H2: independently confirmed by new evidence
   H3: still a post-hoc interpretation
   ```

   Do not rewrite H1 or H3 as H0.
7. Identify the strongest counterexample, assumption being relied on, and the
   condition under which the claim should fail.
8. Check whether the evidence distinguishes the claimed mechanism from the
   competing explanation or merely correlates with it.
9. Rewrite the claim at the strongest honest level and state its object,
   environment, task, data, statistical/generalization boundary, and provenance.
10. Name one additional experiment, analysis, proof obligation, or source only
    when at least one possible outcome would materially change the conclusion.
11. Update supporting records once only when the claim decision makes them stale.

## Output Contract

Produce:

- allowed conclusion wording;
- claim level and evidence state;
- hypothesis provenance H0/H1/H2/H3;
- exact result, theory, or source that supports it;
- fact–inference–exploratory–hypothesis separation;
- strongest counterexample or alternative explanation;
- explicit boundary and largest remaining uncertainty;
- one highest-value missing test, only when its outcomes could change the claim.

## Boundaries

- Do not turn claim review into a provenance report, source-count exercise,
  strength score, promotion workflow, or independent-review requirement.
- Do not require hashes, artifact receipts, or evidence packages for ordinary
  claim wording.
- Do not infer a mechanism from performance alone or a causal claim from
  association alone.
- Do not write unsupported, exploratory, or post-hoc content as established fact.
- Do not invent a pre-result hypothesis after observing a favorable result.
- Do not use Python to score evidence strength or count supporting items.
- Planned, failed, invalid, missing, or unverified results cannot support a
  positive factual claim; scientifically negative completed results remain
  evidence.
- When new evidence rejects the original claim, change the claim rather than the
  interpretation of the evidence.

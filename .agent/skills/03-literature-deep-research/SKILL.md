---
name: 03-literature-deep-research
description: Falsify or defend a bounded novelty claim by finding the strongest prior art, equivalent terminology, competing mechanisms, and verified source evidence needed for the next research or writing decision.
---

# 03 Literature Deep Research

## Purpose

Use verified literature to change a research, novelty, or writing decision. The
first task is to search for evidence that could invalidate the preferred novelty
claim—not to maximize citations or support a predetermined gap.

## Workflow

1. State the exact question, failure, mechanism, manuscript claim, and novelty
   assertion under review.
2. Identify the largest literature uncertainty: unknown closest prior art,
   equivalent terminology, theoretical equivalence, reported failure, or disputed
   result.
3. Search the smallest authoritative set needed, including:
   - foundational and recent representative work;
   - closest direct competitors;
   - equivalent, historical, and neighboring-field terms;
   - the same mechanism under another name;
   - theory relevant to the mechanism;
   - conference, journal, preprint, benchmark, and reproduction versions;
   - studies reporting the same failure or boundary;
   - sources that directly weaken novelty.
4. Verify the original paper or official record. Search snippets, generated
   summaries, citation counts, venue prestige, and author reputation are not
   evidence for the scientific claim.
5. For every load-bearing source extract:

   ```text
   citation and verified source
   research question
   method and core assumption
   main result
   known limitation
   exact overlap with our work
   remaining distinction
   evidence that the distinction matters
   ```

6. Compare shared dimensions rather than listing papers. Identify agreement,
   disagreement, non-comparability, alternative explanations, and source gaps.
7. Produce the adversarial novelty result:

   ```text
   Strongest prior art against novelty:
   Exact overlap:
   Difference that remains:
   Evidence that the difference matters:
   Novelty verdict: invalid / weak / defensible / strong
   Required repositioning:
   ```

8. When prose revision was requested, revise the target section in the same task
   and represent the strongest prior work fairly.
9. Recheck only the load-bearing citations and factual statements actually used.
10. Stop when the bounded novelty or positioning decision is resolved well enough
    to choose the next research action.

## Output Contract

Produce one of:

- a novelty-falsification verdict;
- a concise competition/explanation map;
- a revised Introduction or Related Work section with verified citations and a
  scientifically meaningful remaining distinction.

State unresolved source gaps directly. Distinguish source findings from the
paper's own synthesis, inference, and hypothesis.

## Boundaries

- Do not produce an annotated bibliography, database quota, PRISMA workflow,
  quality-score table, raw-search archive, or completeness proof for an ordinary
  bounded research-paper question.
- Do not treat low publication count, terminology difference, missing exact
  keyword match, citation count, or venue prestige as novelty evidence.
- Do not stop after finding supportive papers; actively search the closest prior
  art that could invalidate novelty.
- Do not spend the task formatting a matrix, bibliography, or search log.
- Do not use Python to count papers, score prose, rank authors, or prove source
  completeness.
- Do not create citation hashes, immutable snapshots, receipts, or source ledgers.
- Do not silently promote abstract-level claims into full mechanisms,
  experiments, or deployment conclusions.
- Systematic-review artifacts are used only when the review method is itself the
  research contribution or the user explicitly requests them.

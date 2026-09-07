---
name: literature-review
description: Find, verify, compare, and synthesize the literature needed to position one research question, explain a failure, or revise a specific paper section without turning the task into a compulsory systematic-review pipeline.
---

# Literature Review

## Purpose

Build the competitive explanation space for one scientific decision. The product
is a source-grounded synthesis, a corrected reference set, or the requested
manuscript section—not a large search archive, citation-count ranking, or PRISMA
workflow unless the paper is itself a systematic review.

## Workflow

1. Fix the bounded question: research object, environment, task, failure, and the
   decision that the literature must inform.
2. Search in this order as needed:
   - foundational work;
   - recent representative work;
   - closest direct competitors;
   - theory relevant to the proposed mechanism;
   - benchmark/dataset/protocol papers;
   - studies reporting the same failure or boundary;
   - high-quality reviews for field structure.
3. Verify load-bearing claims from the original paper or official record. Search
   snippets and citation counts are discovery aids only.
4. For each source actually used, extract the research question, method, main
   assumption, main result, known limitation, and relation to the current work.
5. Compare sources by shared scientific dimensions. Identify agreement,
   disagreement, non-comparability, alternative explanations, and the unresolved
   gap.
6. Converge the positioning:

   ```text
   foundational line
   -> dominant assumptions
   -> strongest alternatives
   -> unresolved failure or contradiction
   -> our entry point
   ```

7. Update `paper/refs/reading_matrix.md` and `references.bib` only for sources
   used by the decision or text. When a section was requested, revise that
   section in the same bounded task.
8. Recheck only the citations and factual claims changed.

For a systematic/scoping review whose search method is itself a scientific
contribution, add the databases, queries, screening criteria, deduplication, and
flow counts required by that review design. Do not impose those artifacts on an
ordinary research-paper related-work task.

## Output Contract

Produce one or more direct products required by the request:

- a concise literature map organized by assumptions, mechanisms, results, and
  boundaries;
- verified bibliography entries for the cited sources;
- a revised Introduction/Related Work/review section with a defensible gap;
- one explicit source gap that prevents a scientific decision.

The synthesis must distinguish verified source findings from author inference.
A low publication count is not sufficient novelty evidence.

## Boundaries

- Do not require three databases, raw JSON exports, PRISMA counts, quality grades,
  citation thresholds, venue prestige, or author reputation for an ordinary
  bounded literature question.
- Do not prioritize papers by citation count or journal name instead of direct
  relevance and evidence.
- Do not fabricate citations, DOI, publication status, results, or limitations.
- Do not treat an abstract claim as a verified mechanism when the needed support
  is in the full text.
- Do not produce an annotated bibliography or study-by-study list when synthesis
  is requested.
- Do not create source hashes, immutable snapshots, audit ledgers, or search
  receipts.
- Do not use Python to prove search completeness, count papers, or score prose.
- Stop when the bounded question is answered well enough to make the next
  research or writing decision.

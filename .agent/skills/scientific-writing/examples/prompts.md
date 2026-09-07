# scientific-writing — invocation scenarios

Realistic two-stage (outline → prose) invocations for the single-paper workflow. Each
scenario shows the inputs read from `paper/` and the artifacts written back.

## Scenario 1: Draft the Results section from finalized evidence

Context: the experiments are done and frozen; figures/tables have captions and first
callouts. The Results section still does not exist as prose.

Prompt:
> Read `paper/refs/target_journal.md` for the citation style and word limit, then read
> `paper/experiments/evidence_matrix.md`, `paper/experiments/statistics.md`, and
> `paper/experiments/run_ledger.md`. Build a bullet outline of the Results section in
> `paper/draft/results_outline.md` that names, for each finding, the figure/table callout,
> the exact statistic, and the evidence-matrix row. Then expand that outline into flowing
> prose in `paper/draft/results.md` — full sentences only, no bullet lists in the final
> draft, inline citations keyed to `paper/refs/references.bib`. Flag any number that does
> not trace back to `statistics.md` or `run_ledger.md` into `paper/logs/open_questions.md`
> instead of writing it.

Inputs: `paper/refs/target_journal.md`, `paper/refs/references.bib`,
`paper/experiments/evidence_matrix.md`, `paper/experiments/statistics.md`,
`paper/experiments/run_ledger.md`, `paper/assets/figures/`, `paper/assets/tables/`.

Outputs: `paper/draft/results_outline.md` (scaffolding), `paper/draft/results.md` (final
prose), gaps appended to `paper/logs/open_questions.md`.

## Scenario 2: Revise the Discussion to address a reviewer critique

Context: `paper/reviews/ai_review.md` flags over-interpretation of a secondary outcome
and a missing comparison to a recent prior study. The Discussion already exists as
markdown under `paper/draft/`.

Prompt:
> Read the two critiques in `paper/reviews/ai_review.md`. For each, locate the offending
> passage in `paper/draft/discussion.md`, pull the correct framing and the comparison
> study from `paper/refs/references.bib` and `paper/experiments/statistics.md`, and
> rewrite only the affected paragraphs into flowing prose — keep past tense for our
> results, present tense for established facts, and do not introduce claims that lack an
> evidence-matrix row. Then append a reviewer-response entry to
> `paper/reviews/response_to_reviewers.md` that re-states each critique, the change made,
> and the supporting citation/statistic. Log the reframing decision in
> `paper/logs/decision_log.md`.

Inputs: `paper/reviews/ai_review.md`, `paper/draft/discussion.md`,
`paper/refs/references.bib`, `paper/experiments/statistics.md`,
`paper/experiments/evidence_matrix.md`.

Outputs: revised paragraphs in `paper/draft/discussion.md`, new entries in
`paper/reviews/response_to_reviewers.md`, a row in `paper/logs/decision_log.md`. If any
required evidence is missing, stop and record an open question rather than fabricating
the comparison.

## Scenario 3: Compose a journal-conformant abstract

Context: all sections are drafted; `paper/refs/target_journal.md` specifies a 250-word
unstructured abstract in Vancouver style.

Prompt:
> Read `paper/refs/target_journal.md` to confirm abstract format (unstructured, ≤250 words,
> Vancouver citations) and reporting guideline. Synthesize the finished Methods, Results,
> and Discussion from `paper/draft/` into a single flowing-paragraph abstract — no labeled
> Background/Methods/Results/Conclusions sections, no bullet lists, every number traced to
> `paper/experiments/statistics.md`. Write the result to `paper/draft/abstract.md` and
> record the word count and any guideline checklist gaps in `paper/logs/open_questions.md`.

Inputs: `paper/refs/target_journal.md`, `paper/draft/methods.md`,
`paper/draft/results.md`, `paper/draft/discussion.md`,
`paper/experiments/statistics.md`.

Outputs: `paper/draft/abstract.md`, a word-count note and any checklist gaps in
`paper/logs/open_questions.md`.

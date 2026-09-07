# peer-review — invocation scenarios

Realistic prompts for invoking the peer-review skill inside the
Auto-01-tiny-research workspace. Each scenario names the `paper/` inputs it
reads, the artifacts it writes, and the boundary where it hands off to another
skill.

## Scenario 1: Pre-submission self-review of a finished draft

Context: the full manuscript draft exists under `paper/draft/` and the target
venue in `paper/refs/target_journal.md` is a clinical journal expecting a
CONSORT-compliant randomized-trial report. Before the draft is frozen into
`paper/tex/`, the team wants a rigorous internal peer review so that obvious
flaws are caught before external review.

Prompt:
> Read `paper/refs/target_journal.md` to confirm the venue, article type, and
> that CONSORT is the applicable reporting standard. Load the rubrics in
> `references/reporting_standards.md` and `references/common_issues.md`. Read the
> full draft under `paper/draft/`, then run a section-by-section review: methods
> reproducibility and controls, statistical reporting in results (effect sizes,
> confidence intervals, multiple-testing correction), discussion conclusions vs
> data, and reference completeness against `paper/refs/references.bib`. Cross-
> check every quantitative claim against `paper/experiments/statistics.md`,
> `paper/experiments/evidence_matrix.md`, and `paper/experiments/ablation.md`,
> and verify reproducibility claims against `paper/experiments/reproducibility.md`
> and `paper/experiments/run_ledger.md`. Inspect the visuals in
> `paper/assets/figures/` and `paper/assets/tables/` for clarity and integrity.
> Run the CONSORT checklist and record any unmet item. Write the structured
> review to `paper/reviews/ai_review.md` with a recommendation, numbered major
> comments (each with issue, rationale, remediation, manuscript location, and
> whether it is essential for publication), numbered minor comments, and
> questions for authors. Append unresolved major comments to
> `paper/logs/open_questions.md`.

Inputs: `paper/draft/*.md`, `paper/refs/target_journal.md`,
`paper/refs/references.bib`, `paper/experiments/{evidence_matrix,statistics,
ablation,reproducibility,run_ledger}.md`, `paper/assets/figures|tables/`.

Outputs: `paper/reviews/ai_review.md`, major comments appended to
`paper/logs/open_questions.md`, review metadata in `paper/logs/change_log.md`.
Do not edit the manuscript — hand revision to `13-reviewer-response`, and hand
any figure redesign to `15-figure-table-design`.

## Scenario 2: Reviewing against reviewer comments before drafting the rebuttal

Context: two reviewer reports have arrived. Before `13-reviewer-response` writes
the rebuttal, the team wants an independent internal review that mirrors each
reviewer concern, checks whether it is scientifically valid against the
project's own evidence, and decides accept/partially-accept/clarify/disagree for
each point.

Prompt:
> The reviewer comments are pasted below. For each comment, treat it as a
> hypothesis and verify it against the manuscript (`paper/tex/`, since the paper
> is now frozen) and the project's evidence in `paper/experiments/`. Use
> `references/common_issues.md` to classify each statistical or methodological
> point. Run the venue's reporting-standard checklist from
> `references/reporting_standards.md` against any claim the reviewers raise about
> completeness. Write the internal review to `paper/reviews/ai_review.md` with,
> for each reviewer point: the original comment, a verdict
> (accept / partially_accept / clarify / respectfully_disagree), the evidence that
> supports the verdict (with a pointer into `paper/experiments/`), and the
> manuscript location affected. Seed every point that needs a response into
> `paper/reviews/response_to_reviewers.md` so `13-reviewer-response` can take
> ownership, and append unresolved blockers to `paper/logs/open_questions.md`.
> Do not begin drafting the rebuttal itself — that is `13-reviewer-response`'s
> job. Post-freeze, record any implied manuscript change in
> `paper/logs/change_log.md`.

Inputs: pasted reviewer comments, `paper/tex/*.tex`, `paper/refs/target_journal.md`,
`paper/experiments/{evidence_matrix,statistics,reproducibility}.md`.

Outputs: `paper/reviews/ai_review.md`, points seeded into
`paper/reviews/response_to_reviewers.md`, blockers in
`paper/logs/open_questions.md`, metadata in `paper/logs/change_log.md`. Do not
edit `paper/tex/` directly — formal edits are owned by `13-reviewer-response`.

# scientific-critical-thinking — invocation scenarios

Realistic invocation scenarios for the single-paper workflow. Each scenario names the
`paper/` artifacts read, the critique the skill runs, and the artifacts written back to
`paper/reviews/` and `paper/logs/`. Critical thinking never writes prose, runs
experiments, or generates figures — it evaluates methodology, statistics, bias, evidence
quality, and reasoning, and records actionable, evidence-bound findings.

## Scenario 1: Pre-submission critical review of the draft and statistics

Context: the markdown draft in `paper/draft/` is feature-complete and the numbers live in
`paper/experiments/statistics.md` and `paper/experiments/run_ledger.md`. The scientist
wants an internal review to catch methodological and statistical weaknesses before the
manuscript is frozen in `paper/tex/`. `paper/refs/target_journal.md` says the venue
expects a Cochrane RoB 2 assessment and CONSORT reporting (it is an RCT-style study).

Prompt:
> Read `paper/refs/target_journal.md`, the full draft in `paper/draft/`,
> `paper/experiments/evidence_matrix.md`, `paper/experiments/statistics.md`,
> `paper/experiments/run_ledger.md`, `paper/experiments/ablation.md`, and
> `paper/experiments/reproducibility.md`. Run a structured critical review: (1) methodology
> critique against the research question, including randomization/blinding adequacy and
> internal/external/construct/statistical-conclusion validity; (2) bias and confounding
> review (confirmation, attrition, p-hacking, unmeasured confounding); (3) statistical
> evaluation — a priori power, test appropriateness and assumption checks,
> multiple-comparison correction across `ablation.md`, exact p-values vs. "p<.05",
> effect sizes with confidence intervals, missing-data handling; (4) GRADE per major claim,
> listing downgrade/upgrade factors; (5) logical-fallacy and claim-proportionality scan of
> the Discussion. Write the result to `paper/reviews/ai_review.md` as Summary → Strengths →
> Concerns (Critical/Important/Minor, each quoting a specific sentence/table/figure and a
> named principle) → Specific Recommendations → Overall Assessment. Route unresolved
> methodological/statistical unknowns to `paper/logs/open_questions.md` and log any
> Critical concern that changes a claim's strength in `paper/logs/decision_log.md`. Do not
> rewrite the draft or recompute statistics — only critique and point to evidence.

Inputs: `paper/refs/target_journal.md`, `paper/refs/references.bib`,
`paper/experiments/evidence_matrix.md`, `paper/experiments/run_ledger.md`,
`paper/experiments/statistics.md`, `paper/experiments/ablation.md`,
`paper/experiments/reproducibility.md`, `paper/draft/*.md`,
`paper/logs/decision_log.md`.

Outputs: `paper/reviews/ai_review.md` (full structured critique with per-claim GRADE and
RoB ratings), new entries in `paper/logs/open_questions.md`,
`paper/logs/decision_log.md`, `paper/logs/change_log.md`. No prose rewrite, no new
experiment, no fabricated statistic.

## Scenario 2: Evaluate whether the Discussion's causal claims are supported

Context: the Discussion in `paper/tex/discussion.tex` (post-freeze) makes several causal
claims ("our method *causes* a 12% reduction in X", "eliminates the Y failure mode") that
the scientist worries overstate the evidence. The underlying design is observational /
correlational per `paper/experiments/run_ledger.md`, and
`paper/experiments/statistics.md` reports only association tests. The scientist wants the
claims stress-tested.

Prompt:
> Read `paper/tex/discussion.tex`, `paper/experiments/run_ledger.md`,
> `paper/experiments/statistics.md`, `paper/experiments/evidence_matrix.md`, and
> `paper/refs/references.bib`. Evaluate every causal or strong interpretive claim in the
> Discussion against the actual design and tests: flag correlation-as-causation, post hoc
> reasoning, hasty generalization beyond the sample, and any claim whose strength exceeds
> the evidence (GRADE: would it survive a downgrade for indirectness, imprecision, or
> unmeasured confounding?). Name the specific fallacy and quote the offending sentence for
> each finding, and propose the hedging language or additional evidence that would make the
> claim defensible. Record the critique in `paper/reviews/ai_review.md`; route the
> suggested rewrites (not the rewrites themselves) to
> `paper/reviews/response_to_reviewers.md` as critique→evidence entries; put the
> unresolved claim-strength questions in `paper/logs/open_questions.md`; and log any claim
> that must be weakened in `paper/logs/decision_log.md`. Do not edit `paper/tex/` — this
> skill only critiques; scientific-writing applies the change.

Inputs: `paper/tex/discussion.tex`, `paper/experiments/run_ledger.md`,
`paper/experiments/statistics.md`, `paper/experiments/evidence_matrix.md`,
`paper/refs/references.bib`, `paper/logs/decision_log.md`.

Outputs: causal-claim evaluation section in `paper/reviews/ai_review.md` (per-claim
fallacy name, quoted sentence, GRADE downgrade factors, suggested hedging),
critique→evidence pointers in `paper/reviews/response_to_reviewers.md`, new questions in
`paper/logs/open_questions.md`, claim-strength changes in `paper/logs/decision_log.md`.
The frozen `paper/tex/` artifact is never overwritten by this skill.

## Scenario 3: Risk-of-bias and publication-bias audit of the cited literature

Context: the manuscript cites ~40 studies from `paper/refs/references.bib`, summarized in
`paper/refs/reading_matrix.md`. A reviewer is likely to ask whether the cited evidence base
is biased toward positive results. The scientist wants a literature-side critique before
submission.

Prompt:
> Read `paper/refs/references.bib` and `paper/refs/reading_matrix.md`. Conduct a
> risk-of-bias and publication-bias audit of the cited evidence: apply the appropriate tool
> per study type (Cochrane RoB 2 for RCTs, ROBINS-I for non-randomized, Newcastle-Ottawa
> for observational), look for selective citation of supporting results (cherry-picking),
> and assess whether the cited set shows signs of publication bias (missing null/negative
> results, clustering of small-study positive findings). Assign a GRADE rating to the body
> of cited evidence for each of the manuscript's main claims, listing the downgrade factors
> (risk of bias, inconsistency, indirectness, imprecision, publication bias) and any upgrade
> factors. Write the audit to `paper/reviews/ai_review.md` as a literature-evidence section;
> flag missing or cherry-picked citations (do not invent replacements) in
> `paper/logs/open_questions.md`; and record any claim whose GRADE rating forces a strength
> reduction in `paper/logs/decision_log.md`.

Inputs: `paper/refs/references.bib`, `paper/refs/reading_matrix.md`,
`paper/refs/target_journal.md`, `paper/experiments/evidence_matrix.md`.

Outputs: literature risk-of-bias / publication-bias audit and per-claim GRADE ratings in
`paper/reviews/ai_review.md`, flagged citation gaps in `paper/logs/open_questions.md`,
claim-strength changes in `paper/logs/decision_log.md`. No new citations are fabricated;
only existing references are evaluated.

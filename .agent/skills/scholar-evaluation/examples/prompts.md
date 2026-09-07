# scholar-evaluation — invocation scenarios

Realistic prompts for invoking the scholar-evaluation external skill inside the
Auto-01-tiny-research workspace. Each scenario shows the kind of request that
should trigger this skill, the workspace inputs it reads, the (optional) network
calls it makes, and the artifacts it must produce. scholar-evaluation is a TIER C
external skill: its deterministic rubric-based scoring runs offline, while the
optional LLM-assisted critique step requires network access and a user-provided
`OPENROUTER_API_KEY`; it never invents or stores credentials.

## Scenario 1: Comprehensive pre-submission scoring of the current draft

> Before we freeze, score the current draft at `paper/draft/02_methods.md` and
> `paper/draft/04_results.md` comprehensively against ScholarEval, so I know where
> it's weakest relative to the venue in `paper/refs/target_journal.md`. I have an
> `OPENROUTER_API_KEY` in my shell if you want the LLM critique; otherwise just
> do the rubric pass. Write the result to `paper/reviews/ai_review.md` and append
> a score row to `paper/logs/decision_log.md`.

This triggers scholar-evaluation: a comprehensive evaluation of the draft's
methods and results. The skill loads `references/evaluation_framework.md`, scores
each applicable dimension (problem formulation, methodology, data collection,
analysis, results, writing, citations — dropping any that don't apply with a
stated reason) on the 1–5 rubric, citing the exact section for every score. It
checks claims against `paper/experiments/evidence_matrix.md` and
`paper/experiments/statistics.md`. With `OPENROUTER_API_KEY` present, it augments
the rubric pass with an LLM-assisted critique (reading the key from the
environment, never logging it); if absent, it proceeds offline and notes the
skip. It runs `scripts/calculate_scores.py` (offline, stdlib-only) to produce the
weighted aggregate, writes the structured evaluation to
`paper/reviews/ai_review.md` (per-dimension scores, strengths, improvements,
critical issues, section refs, overall band, ranked recommendations), and appends
a version-stamped score row to `paper/logs/decision_log.md` and
`paper/logs/change_log.md`. It does NOT edit the draft or touch
`paper/refs/references.bib`.

## Scenario 2: Targeted re-evaluation of methodology after a revision

> We just rewrote the methodology to fix the reproducibility gap. Re-evaluate only
> the methodology and analysis dimensions of `paper/tex/03_methods.tex` and
> compare the score to the previous version in `paper/logs/decision_log.md`. No
> LLM step — rubric pass only, fully offline.

This triggers scholar-evaluation: a targeted, comparative re-evaluation. Scope is
explicitly limited to methodology + analysis; all other dimensions are noted as
out-of-scope rather than scored. The skill runs entirely offline (no
`OPENROUTER_API_KEY` requested), scores the two dimensions against
`references/evaluation_framework.md` with section-level citations, runs
`scripts/calculate_scores.py` with a `--weights` JSON that zeroes the
out-of-scope dimensions, and reports the delta versus the previous version's
recorded scores. It updates `paper/reviews/ai_review.md` with a new version
block, appends a score row to `paper/logs/decision_log.md`, and routes any
remaining methodology weakness to `paper/logs/insights.md` (and any unresolved
judgment call about whether the fix is sufficient to `paper/logs/open_questions.md`).
It does not produce the formal reviewer-response letter — that is
`13-reviewer-response`'s job.

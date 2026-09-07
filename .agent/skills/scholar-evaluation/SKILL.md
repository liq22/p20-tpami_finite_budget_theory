---
name: scholar-evaluation
description: Score the single draft on the ScholarEval rubric across research-quality dimensions and write cited feedback to paper/reviews/ai_review.md. Do not use for literature search, bibliography work, drafting, experiments, or the reviewer letter. Optional LLM critique needs network and a user-provided OPENROUTER_API_KEY; never invent or store secrets.
---

# Scholar Evaluation

## Purpose

Apply the **ScholarEval** framework (Moussa et al., 2025) to systematically evaluate
scholarly work — a draft chapter, a research proposal, or (in this repo) the single
paper under development — across eight research-quality dimensions, producing both
qualitative critique and a quantitative 1–5 score per dimension. In
Auto-01-tiny-research this is a **TIER C external skill**: its core scoring workflow
is deterministic and runs offline against `references/evaluation_framework.md`, but
the optional LLM-assisted critique steps issue network calls and consume a
user-provided `OPENROUTER_API_KEY`. The skill complements — it does not replace —
the human `peer-review` skill and the formal `13-reviewer-response` stage.

The deliverable is a structured evaluation record routed to `paper/reviews/`, plus
optional score artifacts that let the author track quality across revisions.

## Use When

- Scoring the current draft across the ScholarEval dimensions to find its weakest
  areas before submission (feeds `paper/reviews/ai_review.md`).
- Re-evaluating specific dimensions after a revision to verify a weakness was
  actually fixed and to track score drift across versions.
- Assessing publication readiness of the draft for the venue named in
  `paper/refs/target_journal.md`, against rubric thresholds.
- Providing structured, evidence-based critique on methodology, analysis, or
  results sections, grounded in the dimension rubrics rather than personal taste.
- Benchmarking one's own draft against a comparison paper listed in
  `paper/refs/reading_matrix.md`.

Do **not** use this skill for: live database / literature search
(`paper-lookup`), thematic synthesis of the literature (`literature-review`),
formatting or DOI-verifying the bibliography (`citation-management`), drafting or
polishing manuscript prose (`scientific-writing`, `10-language-polish`), running
experiments or generating figures (`06-experiment-ops`, `15-figure-table-design`),
or producing the formal response-to-reviewers letter once a real editor has
responded (`13-reviewer-response`). It is also not a replacement for genuine
double-blind peer review — its judgment is framework-structured, not expert.

## Required Inputs

- The work to evaluate: a markdown/LaTeX draft under `paper/draft/` (pre-freeze)
  or `paper/tex/` (post-freeze), or a specific section thereof. State the file
  path explicitly so every score cites the section it was derived from.
- The evaluation scope: **comprehensive** (all eight dimensions), **targeted**
  (named dimensions, e.g. methodology + analysis), or **comparative** (the draft
  benchmarked against one or more papers from `paper/refs/`).
- Workspace context: `paper/refs/target_journal.md` (venue norms and rigor bar),
  `paper/refs/reading_matrix.md` (what the literature establishes), and
  `paper/experiments/` (`evidence_matrix.md`, `statistics.md`, `reproducibility.md`)
  so claims can be checked against recorded evidence.
- `references/evaluation_framework.md` — load this before scoring; it holds the
  per-dimension rubrics and 1–5 quality indicators that every score must cite.
- **Network access** for the *optional* LLM-assisted critique step — this step
  cannot run offline. The deterministic scoring path runs offline regardless.
- **A user-provided `OPENROUTER_API_KEY`** for the optional LLM-assisted critique,
  passed in the user's environment only. This environment variable is documented
  here for reference; it is **not** declared in the frontmatter. The user must
  provide it; never hardcode, echo, or persist a key, token, or credential in
  this skill, its scripts, or any `paper/` file. Treat any encountered key string
  as `<user-provided-key>`.

## Workflow

1. **Define scope.** Identify the work type (empirical / theoretical / review
   paper, proposal, thesis chapter, abstract), the file path being evaluated, and
   the scope (comprehensive / targeted / comparative). Ask the user to clarify if
   ambiguous; record the chosen scope in the output.
2. **Load the rubric.** Read `references/evaluation_framework.md` and select the
   applicable dimensions. Drop dimensions that do not apply (e.g. data collection
   for a purely theoretical paper) and say so explicitly rather than scoring them.
3. **Score dimension by dimension.** For each applicable dimension — problem
   formulation, literature review, methodology, data collection, analysis,
   results, scholarly writing, citations — assess quality, then assign a 1–5
   score citing the specific rubric level and the exact section/paragraph that
   justifies it. Record 2–3 concrete strengths, 2–3 concrete improvement points,
   and any critical issue.
4. **(Optional) LLM-assisted critique.** If the user opts in *and* has supplied
   `OPENROUTER_API_KEY`, augment the deterministic rubric pass with an LLM
   critique drafted from the rubric criteria. Read the key from the environment
   only; never log it. If the key is absent, proceed with the offline rubric pass
   and note that the LLM step was skipped.
5. **Aggregate scores.** Compute weighted dimension scores using
   `scripts/calculate_scores.py` (default weights in the script; user may pass a
   custom `--weights` JSON). The script is stdlib-only and writes a plain-text
   report — it performs no network calls.
6. **Synthesize the overall assessment.** Produce: an overall quality judgment
   tied to the rubric band, 3–5 major strengths, 3–5 critical weaknesses ranked by
   impact, and a publication-readiness note against `paper/refs/target_journal.md`.
7. **Turn findings into actionable feedback.** Each recommendation must reference
   a specific section/paragraph, name the dimension it maps to, and be ranked by
   impact × feasibility. Frame weaknesses as improvement opportunities, grounded
   in the rubric.
8. **Contextualize.** Adjust the rigor bar to the work's stage (early draft →
   conceptual/structural; advanced draft → refinement; final → comprehensive
   check) and to disciplinary norms recorded in `target_journal.md`.
9. **Hand off.** Route the structured evaluation to `paper/reviews/ai_review.md`;
   append a version-stamped score row to `paper/logs/decision_log.md` and
   `paper/logs/change_log.md` so revision-to-revision drift is traceable; route
   unresolved judgment calls to `paper/logs/open_questions.md` and surprising
   weaknesses to `paper/logs/insights.md`.

## Output Contract

- A structured evaluation record written to `paper/reviews/ai_review.md`,
  containing: scope + work type + file path evaluated, a per-dimension block
  (score, rubric level cited, strengths, improvements, critical issues, section
  refs), the aggregate score with band label, the overall assessment, and the
  ranked actionable recommendations.
- Optional score artifacts produced by `scripts/calculate_scores.py`
  (e.g. `paper/reviews/scholar_eval_scores.json` inputs and a `.txt` report),
  kept under `paper/reviews/` so versions are comparable.
- A version-stamped score summary appended to `paper/logs/decision_log.md`
  (dimensions, weights, aggregate, band, file+commit evaluated) and a corresponding
  entry in `paper/logs/change_log.md`.
- Judgment calls routed to `paper/logs/open_questions.md`; non-obvious weaknesses
  routed to `paper/logs/insights.md`.
- The skill does **not** write `paper/reviews/response_to_reviewers.md` (that is
  `13-reviewer-response`), does not edit the draft itself, and does not modify
  `paper/refs/references.bib`.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only scholar-evaluation`
- `python src/S03_Scripts/validate_project.py`
- Every dimension score cites both a rubric level from
  `references/evaluation_framework.md` and a concrete section/paragraph of the
  evaluated draft — no unsupported numeric scores.
- `scripts/calculate_scores.py` runs with no network access (verify by running it
  offline against a sample `paper/reviews/scholar_eval_scores.json`); it imports
  only stdlib modules.
- Any optional LLM-assisted critique path is gated on a user-supplied
  `OPENROUTER_API_KEY` and degrades cleanly to the offline rubric pass when the
  key is absent.
- No API key, token, or credential appears in any output file — grep
  `paper/reviews/` and `paper/logs/` for `sk-`, `gh[pousr]_`, `AKIA`,
  `OPENROUTER_API_KEY=` and `YOUR_KEY` placeholders before finishing; replace any
  live value with `<user-provided-key>`.

## Boundaries

- **Network required for the optional LLM step only.** The deterministic
  rubric-based scoring runs entirely offline; only the optional LLM-assisted
  critique issues live network calls and only when the user opts in. Tell the
  user clearly when a step cannot reach the network.
- **Credentials are user-provided only.** The optional `OPENROUTER_API_KEY` is
  read from the user's environment when present; this skill never generates,
  stores, transcribes, or commits a secret. Any key encountered in inputs or
  logs is replaced with `<user-provided-key>`.
- **Framework judgment, not expert review.** ScholarEval provides a structured,
  rubric-grounded assessment; it does not substitute for domain-expert double-blind
  peer review or for the editorial decision of the target venue. It complements
  the `peer-review` skill.
- **Scope of work.** Evaluates existing scholarly work (a draft or proposal). It
  does not search literature, format bibliographies, draft prose, run
  experiments, generate figures, or write the reviewer-response letter — defer to
  `paper-lookup`, `citation-management`, `scientific-writing`, `06-experiment-ops`,
  `15-figure-table-design`, and `13-reviewer-response` respectively.
- **Rubric fidelity.** Scores must trace to `references/evaluation_framework.md`;
  do not invent dimensions or invent science beyond the framework. Drop
  non-applicable dimensions explicitly rather than forcing a score.
- **Bundled AI schematic scripts are intentionally not ported.** The upstream
  `generate_schematic*.py` scripts depend on external image-generation APIs and a
  Nano Banana / Gemini pipeline; schematic generation belongs to the separate
  `scientific-schematics` skill. Only the stdlib `calculate_scores.py` is ported.

## Stop With

- A complete `paper/reviews/ai_review.md` record covering every applicable
  dimension, each with a rubric-cited score and concrete section references, plus
  the aggregate score, overall assessment, and ranked recommendations.
- A version-stamped score summary appended to `paper/logs/decision_log.md` and
  `paper/logs/change_log.md`.
- Every non-applicable dimension explicitly noted as dropped (with reason), and
  every judgment call routed to `paper/logs/open_questions.md`.
- All outputs scrubbed of any key or token; no live credential is present in any
  `paper/` file, and any optional LLM step either ran with a user-provided key or
  was cleanly skipped and noted.

## References

- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Framework rubric (load before scoring):
  `.agent/skills/scholar-evaluation/references/evaluation_framework.md`.
- Aggregate-score script (stdlib-only, no network):
  `.agent/skills/scholar-evaluation/scripts/calculate_scores.py`
  (see `scripts/README.md` for purpose/inputs/outputs).
- Workspace artifacts read: `paper/refs/target_journal.md`,
  `paper/refs/reading_matrix.md`, `paper/experiments/evidence_matrix.md`,
  `paper/experiments/statistics.md`, `paper/experiments/reproducibility.md`,
  `paper/draft/` or `paper/tex/` (the work under evaluation).
- Workspace artifacts written: `paper/reviews/ai_review.md`,
  `paper/reviews/scholar_eval_scores.json` (optional),
  `paper/logs/decision_log.md`, `paper/logs/change_log.md`,
  `paper/logs/open_questions.md`, `paper/logs/insights.md`.
- Sibling skills: `peer-review` (human-style review), `scientific-critical-thinking`
  (argument scrutiny), `13-reviewer-response` (formal reviewer letter),
  `scientific-schematics` (diagrams).
- Source paper: Moussa, H. N., Da Silva, P. Q., Adu-Ampratwum, D., East, A., Lu,
  Z., Puccetti, N., Xue, M., Sun, H., Majumder, B. P., & Kumar, S. (2025).
  *ScholarEval: Research Idea Evaluation Grounded in Literature.* arXiv:2510.16234.
  https://arxiv.org/abs/2510.16234

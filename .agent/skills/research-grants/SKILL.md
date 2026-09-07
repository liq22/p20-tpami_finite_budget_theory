---
name: research-grants
description: Draft research-funding proposals for NSF, NIH, DOE, DARPA, and Taiwan NSTC — aims, narratives, broader impacts, significance, and budgets for paper/draft/. Do not use for manuscript writing, literature search, experiments, or publication figures. Optional AI diagrams need network plus a user-provided API key; never invent or store credentials.
---

# Research Grants

This is a **TIER C external skill**. Its core grant-writing guidance needs no
network, but the optional AI-figure path (`scientific-schematics`) issues live
calls to the OpenRouter API and may consume a user-provided `OPENROUTER_API_KEY`.
It never generates, stores, transcribes, or commits a secret.

## Purpose

Produce competitive funding-proposal components for U.S. and Taiwan science
agencies — NSF (PAPPG, Intellectual Merit + Broader Impacts), NIH (Specific Aims +
Research Strategy, Significance/Innovation/Approach), DOE (Office of Science,
ARPA-E, EERE), DARPA (BAAs, technical volumes, phase-based milestones), and Taiwan
NSTC (CM03 form, bilingual abstract, innovation/feasibility review). Each agency
has distinct review criteria, page limits, and strategic priorities; this skill
adapts a single research project to those formats and writes the results into the
single-paper workspace so downstream skills (scientific-writing, citation-management,
peer-review) can consume them. It treats every claim of significance, innovation,
or feasibility as something the evidence base and `paper/experiments/` must
support.

## Use When

- Writing a new proposal or resubmission for NSF, NIH, DOE, DARPA, or NSTC.
- Drafting the NIH Specific Aims page, NSF Project Summary, or NSTC CM03 form.
- Developing broader-impacts (NSF), significance/innovation (NIH), or DARPA
  "what if you succeed / who cares" framing.
- Preparing budget justifications and personnel/person-month allocation plans.
- Building project timelines, Gantt charts, and milestone/go-no-go plans.
- Responding to reviewer comments in an A1 resubmission (NIH Introduction).
- Reformatting the paper's already-established evidence (aims, preliminary data)
  into an agency-specific narrative.

Do not use for: drafting the journal manuscript (`scientific-writing`), searching
or screening literature (`literature-review`, `paper-lookup`), running
experiments or computing statistics (`06-experiment-ops`,
`statistical-analysis`), formatting the publication bibliography
(`citation-management`), or producing the final venue submission package
(`12-submission-pack`).

## Required Inputs

- The funding opportunity: agency, mechanism (e.g. NSF CAREER, NIH R01/R21,
  DOE ARPA-E, DARPA BAA, NSTC CM03), solicitation number, and deadline.
- The research project context already in the workspace: `paper/refs/target_journal.md`
  (field/vocabulary conventions), `paper/refs/references.bib` (prior-work citations),
  `paper/experiments/evidence_matrix.md`, `paper/experiments/statistics.md`, and any
  preliminary data figures under `paper/assets/figures/`.
- The review criteria / page limits of the target solicitation (load the matching
  `references/<agency>_guidelines.md`).
- Team and budget facts the user supplies: PI/co-I roles, person-months, equipment
  over $5k, subawards, F&A rate, and any cost-sharing commitment.
- **Network access** — only if AI-generated diagrams are requested via the
  `scientific-schematics` skill; the drafting guidance itself works offline.
- **`OPENROUTER_API_KEY` (user-provided, optional).** Needed solely for the
  optional `scientific-schematics --doc-type grant` figure path. The user must
  provide it out of band; never hardcode, echo, or persist a key, token, or
  credential in this skill, its scripts, or any `paper/` file. Treat any
  encountered key string as `<user-provided-key>`. This variable is documented
  here only — it is **not** declared in the frontmatter.

## Workflow

1. **Classify the target.** Identify agency, mechanism, and the governing document
   (NSF PAPPG 24-1, NIH parent announcement, DOE FOA, DARPA BAA, NSTC CM03).
   Load `references/<agency>_guidelines.md` for page limits and review criteria.
2. **Map the project to the evidence base.** Pull significance and innovation
   claims from `paper/refs/reading_matrix.md` and preliminary data from
   `paper/experiments/evidence_matrix.md`; flag any claim that lacks supporting
   evidence rather than inventing it.
3. **Draft aims/objectives first.** Write the NIH Specific Aims page (or NSF
   objectives / DARPA technical objectives) using action verbs, testable
   hypotheses, and parallel structure across aims.
4. **Build the technical narrative.** Develop Significance / Innovation / Approach
   (NIH), Intellectual Merit + Broader Impacts (NSF), or the DOE/DARPA/NSTC
   equivalent, each tied to specific rows in `paper/experiments/`.
5. **Articulate broader impact / significance.** Use `references/broader_impacts.md`
   and `references/specific_aims_guide.md`; pick concrete, measurable activities
   rather than generic statements.
6. **Plan timeline, milestones, and risk.** Produce a phased Gantt with go/no-go
   criteria; for DARPA add quarterly deliverables and exit criteria.
7. **Prepare budget and justification.** Itemize personnel, equipment, travel,
   materials, subawards, and F&A; respect agency rules (NIH modular ≤$250k/yr,
  NIH salary cap, NSF 2-month summer salary, ARPA-E cost share). Use
   `assets/budget_justification_template.md`.
8. **Optional figures.** If a timeline/workflow/architecture diagram helps and the
   user opts in, call `scientific-schematics --doc-type grant` (requires network +
   user-provided `OPENROUTER_API_KEY`); otherwise build figures in the user's
   usual tools. Never transmit unpublished sensitive details the user has not
   approved for the third-party API.
9. **Resubmission path.** If revising, draft the NIH Introduction (1 page) or NSF
   revision addressing every major criticism, and record the changes in
   `paper/logs/change_log.md`.
10. **Self-review against criteria.** Run a mock review using the agency's scored
    criteria (NIH 1–9, NSF Intellectual Merit + Broader Impacts, NSTC
    innovation/feasibility/capability/value); log gaps in `paper/logs/open_questions.md`.

## Output Contract

- `paper/draft/grant_<agency>_aims.md` — Specific Aims / objectives page.
- `paper/draft/grant_<agency>_narrative.md` — project description / research
  strategy / technical volume (pre-freeze markdown).
- `paper/draft/grant_<agency>_broader_impacts.md` (NSF) or significance/innovation
  sections (NIH), as applicable.
- `paper/draft/grant_<agency>_budget_justification.md` — line-item justification.
- `paper/draft/grant_<agency>_timeline.md` — phased milestones and Gantt.
- Optional figures in `paper/assets/figures/` (e.g. `timeline.png`,
  `workflow.png`).
- `paper/submission/` — final agency-formatted components when frozen.
- `paper/logs/decision_log.md` — agency/mechanism choice and strategic rationale.
- `paper/logs/change_log.md` — resubmission diff against prior version.
- `paper/logs/open_questions.md` — unresolved reviewer-concern gaps.
- All outputs scrubbed of any key or token; no live credential in any `paper/` file.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only research-grants`
- `python src/S03_Scripts/validate_project.py`
- Every drafted section respects the agency's page limit and required headings
  (spot-check against `references/<agency>_guidelines.md`).
- Each significance/innovation/feasibility claim traces to an entry in
  `paper/experiments/evidence_matrix.md` or `paper/refs/reading_matrix.md`; no
  invented preliminary data.
- Budget arithmetic balances (personnel + equipment + travel + materials +
  subawards + F&A = total direct + indirect); NIH modular years are in $250k
  increments.
- No API key, token, or credential appears in any output file — grep
  `paper/draft/`, `paper/submission/`, and `paper/logs/` for `sk-`,
  `gh[pousr]_`, `AKIA`, and key placeholders before finishing; replace any live
  value with `<user-provided-key>`.

## Boundaries

- **Network required only for optional figures.** Grant-writing guidance works
  offline; the optional `scientific-schematics --doc-type grant` path issues live
  calls to the OpenRouter API and is blocked without network access. Tell the user
  when an AI figure cannot be generated.
- **Credentials are user-provided only.** `OPENROUTER_API_KEY` is read from the
  user's environment when present and only if the user opts into AI figures; this
  skill never generates, stores, transcribes, or commits a secret. Any key
  encountered in inputs or logs is replaced with `<user-provided-key>`.
- **Proposal writing, not science creation.** It adapts existing evidence into
  agency formats; it does not invent preliminary data, fabricate citations, run
  experiments, or assert results that `paper/experiments/` does not support.
- **Agency scope.** NSF, NIH, DOE, DARPA, and Taiwan NSTC only. For foundation,
  industry, or non-listed-agency proposals, adapt the closest reference but flag
  the mismatch in `paper/logs/open_questions.md`.
- **Not the manuscript.** Outputs are pre-freeze proposal drafts under
  `paper/draft/`; they are not the journal article. Hand off to
  `scientific-writing` and `09-tex-freeze-formalize` for publication.
- **Disclosure on AI figures.** AI schematic generation sends the user's prompt
  to a third-party API; do not include unpublished sensitive details unless the
  user has approved that transmission.

## Stop With

- Agency-formatted Specific Aims / objectives, technical narrative, broader-impacts
  or significance section, budget justification, and timeline are written to
  `paper/draft/` (and `paper/submission/` when frozen).
- Every claim of significance, innovation, or feasibility traces to the evidence
  base; gaps are listed in `paper/logs/open_questions.md` rather than invented.
- For resubmissions, a point-by-point response to prior critiques is recorded in
  `paper/logs/change_log.md` and `paper/reviews/response_to_reviewers.md` where
  relevant.
- Budget arithmetic balances and respects agency rules (page limits, modular
  increments, salary cap, cost share).
- All outputs are scrubbed of any key or token; no live credential is present in
  any `paper/` file.

## References

- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Agency references bundled with this skill:
  `.agent/skills/research-grants/references/nsf_guidelines.md`,
  `nih_guidelines.md`, `doe_guidelines.md`, `darpa_guidelines.md`,
  `nstc_guidelines.md`, `broader_impacts.md`, `specific_aims_guide.md`.
- Templates: `.agent/skills/research-grants/assets/nsf_project_summary_template.md`,
  `nih_specific_aims_template.md`, `budget_justification_template.md`.
- Workspace consumers: `paper/refs/target_journal.md`, `paper/refs/references.bib`,
  `paper/experiments/evidence_matrix.md`, `paper/draft/`, `paper/submission/`,
  `paper/logs/decision_log.md`, `paper/logs/change_log.md`,
  `paper/logs/open_questions.md`.

---
name: venue-templates
description: Apply venue-specific LaTeX classes, formatting limits, and writing style for the manuscript's target journal or conference, and map each onto the paper/ workspace. Do not use for writing prose, running experiments, literature search, or figure generation, which belong to their own skills.
---

# Venue Templates

## Purpose

This skill is the single source of truth for *how the manuscript must look and read* at its target publication venue. It supplies ready-to-use LaTeX classes and templates for journals (Nature, Science, PLOS, Cell Press, IEEE, ACM, Elsevier), ML/CS conferences (NeurIPS, ICML, ICLR, CVPR, CHI, EMNLP), research posters, and grant proposals (NSF, NIH, DOE, DARPA); the formatting requirements that govern them (page limits, fonts, margins, citation style, figure specs, anonymization); and the per-venue writing-style guides that describe how prose should read at each venue rather than just how it should render. In the single-paper workflow it consumes a frozen manuscript and the venue decision, and produces venue-conformant formal artifacts under `paper/tex/`, `paper/assets/`, and `paper/submission/`.

## Use When

- `paper/refs/target_journal.md` has fixed a target venue and you must enforce its page limits, citation style, abstract format, and class file.
- A manuscript draft in `paper/draft/` is being frozen into formal LaTeX under `paper/tex/` (hand-off with `09-tex-freeze-formalize`) and needs the correct venue class/template.
- You must check a compiled PDF or `.tex` against a venue's formatting requirements (page count, margins, fonts, citation style).
- You need to adapt the tone, structure, or abstract shape of a draft to a specific venue's writing style (e.g. Nature story-driven, NeurIPS contribution bullets, Cell graphical abstract, medical structured abstract).
- A reviewer response requires restating venue-specific expectations (see `references/reviewer_expectations.md`) in `paper/reviews/response_to_reviewers.md`.
- Preparing a research poster for a conference, or a grant-specific document (NSF Project Summary, NIH Specific Aims) alongside the paper.

## Required Inputs

- `paper/refs/target_journal.md` — the fixed target venue; without it the formatting requirements and citation style are undefined and the skill stops.
- `paper/refs/references.bib` — bibliography, so citation style and reference formatting can be checked against actual entries.
- `paper/tex/` — frozen formal manuscript sections (post-freeze). Pre-freeze markdown drafts in `paper/draft/` are read-only for format checking until frozen.
- `paper/assets/figures/` and `paper/assets/tables/` — finalized visuals, so figure resolution/orientation limits can be verified per venue.
- `paper/logs/decision_log.md` and `paper/logs/open_questions.md` — record any venue-conformance gap rather than silently dropping it.

**Optional LLM-assisted schematic/image generation** (e.g. an upstream OpenRouter key used by AI image scripts) is *not* required by this skill: any such key is user-provided out of band; never hardcode, store, echo, or persist a key, token, or credential in this skill, its scripts, or any workspace file. Treat any encountered secret string as `<user-provided-key>`.

## Workflow

1. **Read the venue decision.** Open `paper/refs/target_journal.md` for the venue name, document type (journal article / conference paper / poster / grant), citation style, word/page limit, abstract format, anonymization policy, and required class file. If the venue is unset, stop (see Stop With).
2. **Load formatting requirements.** Match the venue to the right reference: `references/journals_formatting.md`, `references/conferences_formatting.md`, `references/posters_guidelines.md`, or `references/grants_requirements.md`. Record the binding constraints (page limit, min font, margins, citation style, figure resolution/format, supplementary limits) into `paper/logs/decision_log.md`.
3. **Select the template/class.** Locate the bundled LaTeX template under `assets/journals/`, `assets/grants/`, or `assets/posters/`, or query it via `scripts/query_template.py --venue <name> --type <type>`. Prefer the official venue class when one is bundled (e.g. `nature_article.tex`, `neurips_article.tex`, `plos_one.tex`, Elsevier `elsarticle-*`).
4. **Adapt the writing style.** Load the matching style guide (`references/venue_writing_styles.md` plus the per-venue file: `nature_science_style.md`, `cell_press_style.md`, `medical_journal_styles.md`, `ml_conference_style.md`, `cs_conference_style.md`). Use the worked examples in `assets/examples/` (Nature abstract, NeurIPS intro, Cell summary, medical structured abstract) as section-level targets. Flag any structural mismatch between the existing draft and the venue's expected shape into `paper/logs/open_questions.md`.
5. **Freeze into the venue class.** Hand off to `09-tex-freeze-formalize`: the manuscript is moved from `paper/draft/*.md` into `paper/tex/*.tex` using the chosen class. This skill supplies the class and the requirements; the freeze skill performs the conversion and records it in `paper/logs/change_log.md`.
6. **Customize placeholders.** Substitute title, authors, affiliations, and correspondence via `scripts/customize_template.py` (or by hand) into a working `.tex`. Never enter real author identities into a double-blind submission; keep anonymization per `target_journal.md`.
7. **Validate format.** Run `scripts/validate_format.py --file <pdf-or-tex> --venue <name> --check-all` (page count, margins, fonts, citation style, figure specs). Route any failure into `paper/logs/open_questions.md` and, if it affects submission, `paper/logs/change_log.md`.
8. **Compile and review.** Compile with `pdflatex`/`bibtex`/`latexmk` and walk the venue's review checklist (sections present, citations render, figures captioned and within limits, anonymization intact, supplementary prepared). Outputs feed `12-submission-pack`.
9. **Reviewer-aware revisions.** When `paper/reviews/ai_review.md` raises venue-style critiques, restate the relevant expectation from `references/reviewer_expectations.md` in `paper/reviews/response_to_reviewers.md` alongside the change and evidence.

## Output Contract

- `paper/tex/*.tex` — formal manuscript sections in the venue's class (post-freeze), edited only with a change record.
- `paper/assets/figures/` and `paper/assets/tables/` — visuals confirmed to meet the venue's resolution/orientation limits (this skill checks; figure creation is owned by figure/table-design).
- `paper/submission/` — venue-conformant submission artifacts (class file, compiled PDF, source bundle) handed to `12-submission-pack`.
- `paper/checklists/` — venue formatting/compliance checklist (page limit, citation style, figure specs, anonymization, supplementary).
- `paper/logs/decision_log.md` — the binding venue constraints recorded before formatting begins.
- `paper/logs/change_log.md` — every edit to a frozen `paper/tex/` artifact, with rationale.
- `paper/logs/open_questions.md` — any venue-conformance gap that cannot be resolved immediately (e.g. page-limit overflow, missing official class).
- `paper/reviews/response_to_reviewers.md` — venue-expectation restatements when addressing reviewer critiques.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only venue-templates`
- `python src/S03_Scripts/validate_project.py`
- `scripts/validate_format.py --file <compiled.pdf> --venue <name> --check-all` reports no ERROR.
- Every citation in the formal `.tex` resolves to an entry in `paper/refs/references.bib` and follows the venue's citation style (numbered superscript, numbered brackets, or author-year).
- Page count, min font, and margins are within the venue's limits recorded in `paper/logs/decision_log.md`.
- Double-blind submissions contain no author-identifying metadata; single-blind/open venues record the policy in `paper/refs/target_journal.md`.
- No frozen `paper/tex/` artifact is overwritten without a corresponding entry in `paper/logs/change_log.md`.

## Boundaries

- Do not write manuscript prose — that is owned by `scientific-writing`; this skill supplies the venue's class, formatting limits, and writing-style *targets* only.
- Do not run experiments, compute statistics, or generate figures/tables — consume finalized assets from `paper/experiments/` and `paper/assets/`; this skill only verifies they meet venue specs.
- Do not perform the literature search or curate `references.bib` — read what is there; gaps go to open questions.
- Do not perform the markdown→TeX freeze itself — that is `09-tex-freeze-formalize`; this skill provides the class and requirements that the freeze consumes.
- Do not build the final submission zip or handle journal portals — hand off to `12-submission-pack`.
- Do not generate AI schematics or images over the network; the upstream image-generation scripts are intentionally not ported (see `scripts/README.md`). Use the visualization/figure-design skills instead.
- Do not hardcode, echo, or persist any API key, token, or credential; any LLM-assisted key is user-provided out of band.
- A template matching a venue is necessary but not sufficient: always cross-check against the venue's current official author guidelines, which change yearly.

## Stop With

- `paper/refs/target_journal.md` is missing or does not name a venue, so formatting requirements and citation style are undefined.
- No bundled or official class exists for the chosen venue and the user has not supplied one — record an open question rather than improvising a class.
- The manuscript is not yet frozen into `paper/tex/` and the user asks to validate formatting against a venue (format checks operate on frozen artifacts; pre-freeze `paper/draft/*.md` is read-only for this skill).
- A formatting check fails in a way that changes scope (e.g. serious page-limit overflow requiring structural cuts) — surface it in `paper/logs/open_questions.md` and to the user rather than silently editing frozen content.
- The task asks to overwrite a frozen/already-submitted `paper/tex/` or `paper/submission/` artifact without explicit confirmation.

## References

- Formatting requirements: `references/journals_formatting.md`, `references/conferences_formatting.md`, `references/posters_guidelines.md`, `references/grants_requirements.md`.
- Writing style guides: `references/venue_writing_styles.md`, `references/nature_science_style.md`, `references/cell_press_style.md`, `references/medical_journal_styles.md`, `references/ml_conference_style.md`, `references/cs_conference_style.md`, `references/reviewer_expectations.md`.
- Worked examples: `assets/examples/nature_abstract_examples.md`, `assets/examples/neurips_introduction_example.md`, `assets/examples/cell_summary_example.md`, `assets/examples/medical_structured_abstract.md`.
- LaTeX templates: `assets/journals/` (nature, neurips, plos_one, Elsevier elsarticle), `assets/grants/` (nsf, nih), `assets/posters/` (beamerposter).
- Helper scripts: `scripts/query_template.py`, `scripts/customize_template.py`, `scripts/validate_format.py` (see `scripts/README.md` for purpose/inputs/outputs).
- Workspace artifacts: `paper/refs/target_journal.md`, `paper/refs/references.bib`, `paper/tex/`, `paper/draft/`, `paper/assets/figures/`, `paper/assets/tables/`, `paper/submission/`, `paper/checklists/`, `paper/reviews/response_to_reviewers.md`, `paper/logs/decision_log.md`, `paper/logs/change_log.md`, `paper/logs/open_questions.md`.
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT); see NOTICE.md and `.agent/references/scientific_agent_skills_source.md`.

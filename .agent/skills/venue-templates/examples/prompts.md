# venue-templates — invocation scenarios

Realistic invocations for the single-paper workflow. Each scenario shows the venue
decision read from `paper/`, the formatting/style requirements applied, and the artifacts
written back under `paper/`.

## Scenario 1: Freeze a draft into the NeurIPS class and check the page limit

Context: `paper/refs/target_journal.md` fixes the target as NeurIPS (8 pages main text +
unlimited references/appendix, double-blind). The Methods/Results/Discussion are drafted
in `paper/draft/*.md` and ready to freeze into formal LaTeX.

Prompt:
> Read `paper/refs/target_journal.md` to confirm the venue is NeurIPS and that
> double-blind anonymization is required. Load the formatting requirements from
> `references/conferences_formatting.md` and the writing style from
> `references/ml_conference_style.md`, then locate the bundled class via
> `scripts/query_template.py --venue NeurIPS --type article` (expected:
> `assets/journals/neurips_article.tex`). Record the binding constraints (8-page main
> limit, 10pt two-column, numbered bracket citations, anonymization) in
> `paper/logs/decision_log.md`. Hand off to `09-tex-freeze-formalize` to move
> `paper/draft/*.md` into `paper/tex/*.tex` on the NeurIPS class. Then run
> `scripts/validate_format.py --file paper/submission/main.pdf --venue NeurIPS --check-all`;
> route any page-limit overflow or anonymization leak into `paper/logs/open_questions.md`
> and `paper/logs/change_log.md`.

Inputs: `paper/refs/target_journal.md`, `paper/draft/*.md`, `paper/refs/references.bib`,
`references/conferences_formatting.md`, `references/ml_conference_style.md`,
`assets/journals/neurips_article.tex`.

Outputs: binding constraints in `paper/logs/decision_log.md`, frozen `.tex` in `paper/tex/`,
validation report, gaps in `paper/logs/open_questions.md`, change records in
`paper/logs/change_log.md`, compliance checklist in `paper/checklists/`.

## Scenario 2: Adapt an existing draft to Nature's style and abstract format

Context: a finished markdown draft was written for a generic venue; the target has now
been switched to Nature. The prose exists but reads like a CS workshop paper and the
abstract is a 250-word structured block, whereas Nature wants a single flowing paragraph.

Prompt:
> Read `paper/refs/target_journal.md` to confirm the target is Nature, then load
> `references/nature_science_style.md` and `references/journals_formatting.md` for the
> formatting limits (~3000 words, ~5 pages, single column, 12pt, numbered superscript
> citations, 300+ dpi RGB figures). Use the worked abstract in
> `assets/examples/nature_abstract_examples.md` as the target shape and flag, in
> `paper/logs/open_questions.md`, every place where the current `paper/draft/*.md` deviates
> from Nature's expected tone, abstract format, or section weighting — but do not rewrite
> the prose here (that is `scientific-writing`). Supply the bundled class
> `assets/journals/nature_article.tex` to `09-tex-freeze-formalize`, and after freeze run
> `scripts/validate_format.py --file paper/submission/main.pdf --venue Nature --check-all`,
> recording the result in `paper/checklists/`.

Inputs: `paper/refs/target_journal.md`, `paper/draft/*.md`, `paper/assets/figures/`,
`references/nature_science_style.md`, `references/journals_formatting.md`,
`assets/examples/nature_abstract_examples.md`, `assets/journals/nature_article.tex`.

Outputs: a Nature formatting/style gap list in `paper/logs/open_questions.md`, the Nature
class supplied to the freeze step, a compliance checklist in `paper/checklists/`, and any
constraint recorded in `paper/logs/decision_log.md`. The prose itself is left to
`scientific-writing`; this skill only states the targets.

## Scenario 3: Prepare an NSF Project Summary against the PAPPG limits

Context: alongside the paper, the user needs an NSF Project Summary (1 page: Overview,
Intellectual Merit, Broader Impacts) for a proposal.

Prompt:
> Load `references/grants_requirements.md` (NSF PAPPG: Project Summary 1 page, three
> named sections, min 10pt, 1-inch margins) and locate the template via
> `scripts/query_template.py --venue NSF --type summary` (expected:
> `assets/grants/nsf_proposal_template.tex`). Customize it with
> `scripts/customize_template.py --template assets/grants/nsf_proposal_template.tex
> --title <title> --output paper/submission/nsf_project_summary.tex`. Record the PAPPG
> constraints in `paper/logs/decision_log.md` and any open compliance question in
> `paper/logs/open_questions.md`.

Inputs: `references/grants_requirements.md`, `assets/grants/nsf_proposal_template.tex`,
the proposal title.

Outputs: `paper/submission/nsf_project_summary.tex`, PAPPG constraints in
`paper/logs/decision_log.md`, open questions in `paper/logs/open_questions.md`.

# literature-review — invocation scenarios

Realistic invocations for the single-paper workflow. Each scenario lists the
inputs read from `paper/` and the artifacts written back, and follows the skill's
"plan → search → screen → extract → synthesize → verify → write" order.

## Scenario 1: Build the reading matrix and bibliography for a new paper

Context: the research question is frozen and `paper/refs/` is empty. The paper
needs a verified evidence base before claim-evidence and scientific-writing can
proceed.

Prompt:
> Read `paper/refs/target_journal.md` for the citation style (Vancouver) and any
> reporting guideline. From the research question in `02-research-question`, derive
> 2–4 main concepts, list synonyms/abbreviations, and write a search strategy plus
> inclusion/exclusion criteria (2015–today, peer-reviewed + preprints, English) into
> `paper/logs/decision_log.md`. Search at least three complementary sources (broad
> academic web search, PubMed via gget, and Semantic Scholar); save raw JSON exports
> under `paper/refs/raw_search_<source>.json`. Aggregate and deduplicate with
> `scripts/search_databases.py`, screen title → abstract → full text recording the
> count excluded at each stage, assess quality (Newcastle-Ottawa for the observational
> studies, Cochrane RoB for any RCTs), and prioritize high-impact work by citation
> count and venue tier. Then write `paper/refs/reading_matrix.md` (one themed row per
> included study with quality rating and bib key) and `paper/refs/references.bib`.
> Verify every DOI with `scripts/verify_citations.py` until none fail. Log seminal
> papers and gaps into `paper/logs/insights.md` and `paper/logs/open_questions.md`.

Inputs: research question, `paper/refs/target_journal.md`, web/database search access.

Outputs: `paper/refs/reading_matrix.md`, `paper/refs/references.bib`,
`paper/refs/raw_search_<source>.json`, a PRISMA-style screening count record,
entries in `paper/logs/decision_log.md`, `paper/logs/insights.md`,
`paper/logs/open_questions.md`.

## Scenario 2: Verify and repair citations in an existing draft

Context: `paper/draft/related_work.md` already exists with inline citations, but
the references have not been checked and `paper/refs/references.bib` has stale or
unverified entries.

Prompt:
> Run `python .agent/skills/literature-review/scripts/verify_citations.py
> paper/draft/related_work.md` and read the resulting citation report. For each
> failed DOI, attempt to resolve it via CrossRef; if the metadata (authors, title,
> year, venue) does not match, correct it; if a DOI is genuinely dead or wrong,
> exclude the reference and flag it in `paper/logs/open_questions.md`. Reformat
> every surviving entry into the target style from `paper/refs/target_journal.md`
> (see `references/citation_styles.md`) and rewrite `paper/refs/references.bib`
> consistently. Re-run verification until the report is clean. Record every change
> to a frozen bib in `paper/logs/change_log.md`; if the bib feeds a frozen
> `paper/tex/` artifact, stop and confirm before overwriting.

Inputs: `paper/draft/related_work.md`, `paper/refs/references.bib`,
`paper/refs/target_journal.md`.

Outputs: a clean `_citation_report.json`, corrected `paper/refs/references.bib`,
exclusions and mismatches in `paper/logs/open_questions.md`, change records in
`paper/logs/change_log.md` when a frozen artifact is affected.

## Scenario 3: Scope a research question and find the gap

Context: before the question is frozen, the user wants to know whether the field is
crowded and where the novel contribution could sit.

Prompt:
> Treat the candidate question as a scoping review. Run a broad academic web search
> plus two domain databases, deduplicate with `scripts/search_databases.py`, and
> identify the 5–10 most-cited / highest-tier-venue papers (seminal work). Group the
> included studies into 3–5 themes and, for each theme, state the consensus, the
> active controversy, and the under-studied gap. Do not write manuscript prose —
> deliver the result as a structured note in `paper/logs/insights.md` (seminal
> papers, themes, gaps) and a provisional `paper/refs/reading_matrix.md` and
> `references.bib` so later skills can consume it. If screening yields zero studies
> for a theme, say so explicitly rather than filling the gap with speculation.

Inputs: candidate research question, `paper/refs/target_journal.md`, search access.

Outputs: `paper/logs/insights.md` (seminal papers, themes, gaps), provisional
`paper/refs/reading_matrix.md` and `paper/refs/references.bib`, open questions in
`paper/logs/open_questions.md`.

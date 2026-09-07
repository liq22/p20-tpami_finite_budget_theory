# citation-management — invocation scenarios

Realistic prompts for invoking the citation-management skill inside the
Auto-01-tiny-research workspace. Each scenario names the `paper/` inputs it
reads, the artifacts it writes, and the boundary where it hands off to another
skill.

## Scenario 1: Build references.bib from the reading matrix

Context: `paper/refs/reading_matrix.md` lists ~25 candidate papers from the
literature-deep-research stage, but `paper/refs/references.bib` is essentially
empty. The target venue in `paper/refs/target_journal.md` is a high-impact
journal expecting 35–50+ references.

Prompt:
> Read `paper/refs/target_journal.md` to confirm the venue and its citation-count
> standard (target ≥35). Read the candidate shortlist in
> `paper/refs/reading_matrix.md`. For each candidate, extract complete metadata
> with `scripts/extract_metadata.py` from its DOI/PMID/arXiv ID, then enrich any
> entry missing volume, pages, or DOI by web search before writing it. Format
> and de-duplicate with `scripts/format_bibtex.py`, then validate with
> `scripts/validate_citations.py --venue <venue> --report
> paper/logs/citation_validation.json`. Write the result to
> `paper/refs/references.bib`. If the validated count is below the venue target,
> record the gap in `paper/logs/open_questions.md` rather than padding with
> low-quality references.

Inputs: `paper/refs/target_journal.md`, `paper/refs/reading_matrix.md`,
identifier list (DOIs/PMIDs/arXiv IDs).

Outputs: `paper/refs/references.bib`, `paper/logs/citation_validation.json`,
gaps appended to `paper/logs/open_questions.md`. Do not draft prose or perform
thematic synthesis — hand those to scientific-writing and literature-deep-research.

## Scenario 2: Mandatory post-writing citation audit

Context: the full manuscript draft exists under `paper/draft/` and is about to
be frozen into `paper/tex/`. Before freeze, every citation must resolve and
every `references.bib` entry must be cited.

Prompt:
> Run `scripts/validate_citations.py paper/refs/references.bib --venue <venue>
> --manuscript paper/draft/main.md --report paper/logs/citation_validation.json
> --verbose`. Confirm: zero unresolved citation keys (no `[?]` or
> `[citation needed]`), zero dangling entries in `references.bib`, citation
> count meets the venue standard, and every `@article` has author, title,
> journal, year, volume, pages, and DOI. For each error, either fix the
> metadata (re-extract via the scripts) or remove the unused entry; for each
> unresolved in-text key, add the missing reference or remove the citation.
> Re-run validation until the report is clean. Stop and record an open question
> in `paper/logs/open_questions.md` if a DOI genuinely cannot be resolved.

Inputs: `paper/refs/references.bib`, `paper/refs/target_journal.md`,
`paper/draft/main.md` (and any `paper/draft/*.md` it includes).

Outputs: clean `paper/logs/citation_validation.json`, an updated
`paper/refs/references.bib` with no dangling or broken entries, and any
unresolved metadata gaps in `paper/logs/open_questions.md`.

## Scenario 3: Fix a citation disputed by a reviewer

Context: `paper/reviews/ai_review.md` flags that one cited paper is cited with
the wrong volume/pages and another in-text citation points to a preprint when
the published version now exists. The manuscript is already frozen into
`paper/tex/`.

Prompt:
> Read the two citation critiques in `paper/reviews/ai_review.md`. For each,
> re-extract the correct metadata from the DOI via `scripts/doi_to_bibtex.py`
> and update the entry in `paper/refs/references.bib` (replace the preprint
> with the published version). Because the manuscript is frozen, record each
> bib change in `paper/logs/change_log.md` and the rationale in
> `paper/logs/decision_log.md`. Then append a reviewer-response entry to
> `paper/reviews/response_to_reviewers.md` that re-states the critique, the
> corrected reference, and the CrossRef verification source. Re-run
> `scripts/validate_citations.py --manuscript paper/tex/main.tex` to confirm
> nothing else broke.

Inputs: `paper/reviews/ai_review.md`, `paper/refs/references.bib`,
`paper/tex/main.tex`.

Outputs: corrected entries in `paper/refs/references.bib`, new rows in
`paper/logs/change_log.md` and `paper/logs/decision_log.md`, a new entry in
`paper/reviews/response_to_reviewers.md`, a clean validation report. Stop and
record an open question if the published version cannot be verified.

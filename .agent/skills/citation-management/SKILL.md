---
name: citation-management
description: Build, enrich, format, and validate the single-paper bibliography — search Google Scholar/PubMed, extract DOI/PMID/arXiv metadata, and produce a clean references.bib mapped onto paper/refs/. Do not use for thematic literature synthesis, prose drafting, statistics, figures, or venue packaging.
---

# Citation Management

## Purpose

Maintain an accurate, complete, and publication-ready bibliography for the single-paper workflow. This skill searches academic databases (Google Scholar, PubMed, arXiv), extracts verified metadata from paper identifiers (DOI, PMID, arXiv ID, URL), enriches incomplete entries via web search, formats and de-duplicates BibTeX, and validates every citation against venue citation-count standards and against the manuscript body. It is the primary capability behind `paper/refs/references.bib` and works hand-in-hand with the literature-deep-research and scientific-writing skills.

**Critical principle:** no citation enters the manuscript unless its key resolves in `paper/refs/references.bib` with complete, verified fields; no `references.bib` entry survives if it is never cited in the body. The bibliography is evidence-backed, never hand-typed or guessed.

## Use When

- Adding a specific paper to the bibliography from a DOI, PMID, arXiv ID, or URL.
- Searching Google Scholar or PubMed to find candidate papers for `paper/refs/reading_matrix.md`.
- Extracting or repairing incomplete metadata (missing volume, pages, issue, DOI).
- Formatting, sorting, or de-duplicating an existing BibTeX file.
- Auditing the bibliography: broken DOIs, missing required fields, possible duplicates, citation-count below venue standard.
- Performing the mandatory post-writing cross-check between manuscript citations and `references.bib` (no `[?]`, no dangling entries).

## Required Inputs

- `paper/refs/references.bib` — the canonical bibliography this skill owns and updates.
- `paper/refs/reading_matrix.md` — candidate papers and reading priorities that seed searches.
- `paper/refs/target_journal.md` — venue and its citation-count standard / citation style.
- `paper/draft/*.md` (pre-freeze) or `paper/tex/*.tex` (post-freeze) — the manuscript body for the citation↔bibliography cross-check.

**Optional external identifiers / API access.** Several bundled scripts query CrossRef, NCBI E-utilities, arXiv, DataCite, or Google Scholar. Any API key or contact used for higher rate limits — e.g. an `OPENROUTER_API_KEY` for an LLM-assisted enrichment step, `NCBI_API_KEY`, or `NCBI_EMAIL` for Entrez identification — is **user-provided out of band; never hardcode, echo, log, or store** a key, token, or credential in this skill, its scripts, or any workspace file. Treat any encountered key string as `<user-provided-key>`. Network calls are best-effort: prefer caching results into `paper/refs/` over re-querying.

## Workflow

1. **Orient.** Read `paper/refs/target_journal.md` for the venue and its citation-count target (high-impact journals: 35–50+; ML/CS conferences: 30–45+; comprehensive reviews: 40–65+; medical journals: 30–45+). Read `paper/refs/reading_matrix.md` for the candidate-paper shortlist.
2. **Search (seed candidates).** Use `scripts/search_google_scholar.py` and `scripts/search_pubmed.py` (see `references/google_scholar_search.md`, `references/pubmed_search.md`) with targeted queries, year filters, and citation-sort. Favor Tier-1 venues and senior authors; record queries and result counts so the search is reproducible. Outputs feed `reading_matrix.md`, not `references.bib` directly.
3. **Extract metadata.** Convert each chosen identifier to a complete record with `scripts/extract_metadata.py` or `scripts/doi_to_bibtex.py` (CrossRef, PubMed E-utilities, arXiv, DataCite — see `references/metadata_extraction.md`). Pull author, title, year, journal/booktitle, volume, number, pages, DOI.
4. **Enrich incomplete entries (mandatory).** Scan the draft BibTeX for entries missing fields required by entry type (`@article`: author, title, journal, year + volume, pages, DOI; `@inproceedings`: author, title, booktitle, year + pages, DOI; `@book`: author/editor, title, publisher, year + ISBN, DOI). Fill each gap by web search or by re-querying the DOI page/CrossRef; log `[HH:MM:SS] METADATA ENRICHED: [key] - added ...`. If a field genuinely cannot be found, add a `note = {...}` and log `[HH:MM:SS] METADATA INCOMPLETE: [key] ...`.
5. **Format and clean.** Run `scripts/format_bibtex.py` to standardize field order, indentation, title-brace protection (`{AlphaFold}`), page ranges (`--`), author separators (`and`), and citation-key convention; de-duplicate by DOI or author/year/title; sort by year (newest first) or by key (see `references/bibtex_formatting.md`).
6. **Validate.** Run `scripts/validate_citations.py` (see `references/citation_validation.md`): DOI resolution, required-field completeness, year/volume/page format, duplicate detection, citation-count standard against the venue (`--venue` or `--min-count`).
7. **Post-writing cross-check (non-negotiable, before freeze).** Run `validate_citations.py references.bib --manuscript paper/draft/<section>.md` (or `paper/tex/*.tex` post-freeze) to confirm: zero unresolved keys (`[?]`, `[citation needed]`), zero dangling `references.bib` entries, citation count meets venue standard, every entry has complete verified fields. Fix gaps by re-searching rather than padding.
8. **Freeze boundary.** Pre-freeze, edit `paper/refs/references.bib` freely. Once the manuscript is frozen by `09-tex-freeze-formalize`, bibliography changes are edits to a frozen artifact: record each change in `paper/logs/change_log.md` and cite the reason in `paper/logs/decision_log.md`.
9. **Reviewer responses.** When a reviewer disputes a citation, record the original critique in `paper/reviews/ai_review.md`, the corrected entry and its verification source in `paper/reviews/response_to_reviewers.md`, and the bib diff in `change_log.md`.

## Output Contract

- `paper/refs/references.bib` — clean, de-duplicated, venue-compliant bibliography; every entry has the required fields for its type and a verifiable DOI where one exists.
- `paper/refs/reading_matrix.md` — search queries, result counts, and candidate shortlist updates (reproducibility of the search).
- Validation report (JSON) — total/valid/error/warning breakdown; errors routed to `paper/logs/open_questions.md` until resolved.
- Enrichment / incompleteness log lines — recorded so each metadata fix or unfilled gap is auditable.
- Post-freeze bibliography edits — mirrored into `paper/logs/change_log.md` and `paper/logs/decision_log.md`; reviewer-driven citation fixes additionally written to `paper/reviews/response_to_reviewers.md`.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only citation-management`
- `python src/S03_Scripts/validate_project.py`
- `python .agent/skills/citation-management/scripts/validate_citations.py paper/refs/references.bib --venue <venue> --manuscript paper/draft/main.md --report paper/logs/citation_validation.json` — zero unresolved keys, zero dangling entries, count meets venue standard.
- Every `@article` in `paper/refs/references.bib` has author, title, journal, year, volume, pages, and DOI (or a `note` explaining a genuinely unavailable field); no DOI is malformed or unresolved.
- No section of the manuscript contains `[?]`, `[citation needed]`, or a citation key absent from `references.bib`.

## Boundaries

- Do not fabricate citations, DOIs, author lists, page ranges, or years; if metadata cannot be verified, leave the entry out and record an open question in `paper/logs/open_questions.md`.
- Do not hand-type BibTeX entries when an identifier is available — extract via the scripts so fields come from CrossRef/PubMed/arXiv.
- Do not perform thematic literature synthesis, prose drafting, statistical analysis, figure generation, or venue-template packaging — those belong to literature-deep-research, scientific-writing, experiment-ops, figure-table-design, and submission-pack respectively. This skill only handles the technical bibliography.
- Do not leave an `@article` without volume, pages, and DOI after enrichment; an unfilled field must carry an explanatory `note`.
- Do not hardcode, echo, or persist any API key, token, or credential; any LLM-assisted enrichment key (e.g. OpenRouter) or NCBI identifier is user-provided out of band.
- Do not edit a frozen `paper/tex/` or frozen `references.bib` without a change record in `paper/logs/change_log.md`.
- Following a citation-count standard is necessary but not sufficient: padding the bibliography with low-quality or off-topic references does not make a result top-journal convincing.

## Stop With

- `paper/refs/target_journal.md` is missing or unfilled, so the venue citation-count standard and citation style are undefined.
- `paper/refs/reading_matrix.md` is empty, so there is no candidate shortlist to extract metadata from.
- A DOI/PMID/arXiv ID cannot be resolved by any source after enrichment, and the paper cannot be reliably identified.
- The manuscript body does not yet exist, so the post-writing citation↔bibliography cross-check cannot run.
- The task asks to overwrite a frozen or already-submitted `references.bib` without explicit confirmation.
- A citation dispute from a reviewer cannot be resolved because the original publication is irretrievable; stop and record an open question rather than substituting an unverified reference.

## References

- Provenance: Ported (adapted) from `K-Dense-AI/scientific-agent-skills` v2.53.0 (MIT); see `NOTICE.md` and `.agent/references/scientific_agent_skills_source.md`.
- Bundled guides: `references/google_scholar_search.md`, `references/pubmed_search.md`, `references/metadata_extraction.md`, `references/bibtex_formatting.md`, `references/citation_validation.md`.
- Bundled assets: `assets/bibtex_template.bib`, `assets/citation_checklist.md`.
- Bundled scripts: see `scripts/README.md` for the per-script inventory, inputs, outputs, network, and writes.
- Workspace targets: `paper/refs/references.bib`, `paper/refs/reading_matrix.md`, `paper/refs/target_journal.md`, `paper/draft/*.md`, `paper/tex/*.tex`, `paper/reviews/ai_review.md`, `paper/reviews/response_to_reviewers.md`, `paper/logs/open_questions.md`, `paper/logs/change_log.md`, `paper/logs/decision_log.md`.
- External APIs: CrossRef `api.crossref.org`, NCBI E-utilities, arXiv API, DataCite; resolvers `doi.org` and MeSH Browser.

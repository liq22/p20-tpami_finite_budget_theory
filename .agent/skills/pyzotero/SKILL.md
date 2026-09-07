---
name: pyzotero
description: Read, search, create, and export references in a Zotero library via the pyzotero Web API v3 client, landing results in paper/refs/. Use only when the user provides a Zotero User ID and API key out of band (network required). Do not use for de-novo citation search, DOI/PMID metadata extraction, BibTeX formatting, or thematic synthesis.
---

# Pyzotero

## Purpose

Drive an existing Zotero reference library from Python using the `pyzotero`
client (wrapper for the Zotero Web API v3). This skill pulls verified items,
collections, tags, notes, and attachments out of Zotero; pushes new references
created from the single-paper workflow back into Zotero; and exports the library
to BibTeX / CSL-JSON so it can land in `paper/refs/references.bib`. It is the
bridge between a researcher's curated Zotero library and the Auto-01-tiny-research
bibliography workspace; it does not itself invent or verify bibliographic metadata
beyond what Zotero already holds.

Upstream target: pyzotero 1.13.x. Docs: <https://pyzotero.readthedocs.io/>.

## Use When

- The user keeps their references in Zotero and wants to export the relevant collection to `paper/refs/references.bib`.
- Seeding `paper/refs/reading_matrix.md` from a Zotero collection or saved search.
- Searching the Zotero library by tag, author, or full-text to shortlist candidate papers for a section.
- Pushing a citation that originated in the manuscript back into Zotero (e.g. a paper found during drafting).
- Downloading a PDF attachment stored in Zotero into `paper/assets/` for reading or figure extraction.
- Local-only, read-only queries against a running Zotero 7 desktop instance (no API key) via `local=True`.

## Required Inputs

- **Zotero credentials — user-provided out of band; never hardcode, echo, log, or store.**
  - `ZOTERO_LIBRARY_ID` — the numeric Zotero user or group ID.
  - `ZOTERO_API_KEY` — a Zotero Web API key created at <https://www.zotero.org/settings/keys>. Treat any encountered key string as `<user-provided-key>`.
  - `ZOTERO_LIBRARY_TYPE` — optional, `'user'` (default) or `'group'`.
  - Network access to `https://api.zotero.org` is required for the Web API. Local mode (`local=True`) requires Zotero 7 running locally with API access enabled and needs no key (read-only).
- `paper/refs/target_journal.md` — venue and citation style, to choose the right export format.
- `paper/refs/reading_matrix.md` — where Zotero-derived candidates are written.
- `paper/refs/references.bib` — the canonical bibliography that exports land in.
- A collection key, tag, or search query defining which slice of the Zotero library is in scope.

## Workflow

1. **Authenticate from environment.** Construct `Zotero(library_id=os.environ['ZOTERO_LIBRARY_ID'], library_type=os.environ.get('ZOTERO_LIBRARY_TYPE','user'), api_key=os.environ['ZOTERO_API_KEY'])`. Never read a literal key from a file or argument; if a key is missing, stop and ask the user to provide it out of band. See `references/authentication.md`.
2. **Scope the slice.** Identify the target collection (`collections()` / `collections_subcollections`), saved search, or tag set that maps to this paper. Record the collection name and key in `paper/logs/decision_log.md` so the export is reproducible. See `references/collections.md`, `references/saved-searches.md`, `references/tags.md`.
3. **Read and search.** Pull top-level items with `top()` or search with `items(q=..., qmode='everything', itemType='journalArticle', sort='date', direction='desc')`. Use `everything()` for full pagination rather than the 100-item default. See `references/read-api.md`, `references/search-params.md`, `references/pagination.md`.
4. **Seed the reading matrix.** Write the shortlist (title, creators, year, DOI, Zotero item key, collection) into `paper/refs/reading_matrix.md`. Do not write metadata that is absent in Zotero; flag gaps for the citation-management skill instead.
5. **Export to BibTeX.** `zot.add_parameters(format='bibtex')` then dump the scoped slice; write the result to `paper/refs/references.bib` (or a staging file for citation-management to de-duplicate and format). CSL-JSON and bibliography formats are also available. See `references/exports.md`.
6. **Push back (optional).** If a new reference surfaced during drafting, build it from `item_template('journalArticle')`, fill verified fields only, and `create_items([template])`. Mirror the new Zotero item key into the bib entry. See `references/write-api.md`.
7. **Attachments (optional).** Download a PDF attachment with `zot.file(item_key)` into `paper/assets/` when a source PDF is needed for reading or figure extraction; never upload binaries unless explicitly requested. See `references/files-attachments.md`.
8. **Freeze boundary.** Pre-freeze, edits to `paper/refs/references.bib` are free. Post-freeze (`09-tex-freeze-formalize`), every bib change is a frozen-artifact edit: record it in `paper/logs/change_log.md` and justify it in `paper/logs/decision_log.md`. Reviewer-driven Zotero edits also land in `paper/reviews/response_to_reviewers.md`.
9. **Hand off.** De-duplication, field-completeness checks, DOI resolution, and citation-count auditing belong to the citation-management skill. This skill only moves verified Zotero content in and out.

## Output Contract

- `paper/refs/references.bib` — BibTeX exported from the scoped Zotero slice (or a staging `.bib` handed to citation-management).
- `paper/refs/reading_matrix.md` — candidate shortlist with Zotero item keys for traceability.
- `paper/assets/` — downloaded PDF attachments, named by Zotero item key, only when explicitly requested.
- `paper/logs/decision_log.md` — the collection/search scope and any push-back of new items.
- `paper/logs/change_log.md` — every post-freeze bibliography edit and its Zotero source.
- No credential is ever written to any workspace file; API keys live only in the user-provided environment for the lifetime of the call.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only pyzotero`
- `python src/S03_Scripts/validate_project.py`
- Manual credential check: confirm no `ZOTERO_API_KEY` literal appears anywhere under `.agent/skills/pyzotero/` or in any `paper/` file (`grep -rE 'ZOTERO_API_KEY=\S' .agent/skills/pyzotero paper` must return nothing).
- Confirm the scoped export round-trips: the number of `@entry` blocks written to `paper/refs/references.bib` matches `len(zot.everything(zot.collection_items(<key>)))`.
- Post-freeze, every bib diff traced to a Zotero export has a matching entry in `paper/logs/change_log.md`.

## Boundaries

- **External / network + credentials.** The Web API path requires network access to `api.zotero.org` and a user-provided `ZOTERO_API_KEY` plus `ZOTERO_LIBRARY_ID`. Never invent, hardcode, echo, log, commit, or persist a Zotero API key, user ID, or library ID; treat any encountered value as `<user-provided-key>`. If credentials are absent, stop and ask the user rather than guessing or using a placeholder as if real.
- Do not fabricate Zotero items, DOIs, author lists, or attachment contents; if a field is absent in Zotero, leave it out and hand the gap to citation-management rather than guessing.
- Do not perform de novo academic search (Google Scholar / PubMed / arXiv), DOI metadata extraction, BibTeX formatting-rule enforcement, citation-count auditing, or thematic literature synthesis — those belong to citation-management and literature-deep-research. This skill only moves content that already exists in Zotero.
- Do not upload, delete, or trash Zotero items or attachments unless the user explicitly requests it for that operation.
- Do not edit a frozen `paper/tex/` or frozen `paper/refs/references.bib` without a `paper/logs/change_log.md` entry.
- Local mode (`local=True`) is read-only and requires Zotero 7 with local API access enabled; it is not a substitute for the Web API when write-back is needed.

## Stop With

- `ZOTERO_API_KEY` or `ZOTERO_LIBRARY_ID` is not provided by the user out of band.
- Network access to `api.zotero.org` is unavailable and local mode is not an option.
- The named collection / saved search / tag does not exist in the library, so the scoped slice is undefined.
- An item in Zotero lacks a DOI or title and cannot be reliably identified for the bibliography; stop and record the gap in `paper/logs/open_questions.md` rather than exporting a malformed entry.
- The task asks to delete, trash, or overwrite Zotero items, or to upload binaries, without explicit user confirmation.
- A post-freeze bibliography edit is requested without a corresponding `change_log.md` entry.

## References

- Provenance: Ported (adapted) from `K-Dense-AI/scientific-agent-skills` v2.53.0 (MIT); see `NOTICE.md` and `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: <https://pyzotero.readthedocs.io/>, Zotero Web API v3 <https://www.zotero.org/support/dev/web_api/v3/start>.
- Bundled guides: `references/authentication.md`, `references/read-api.md`, `references/write-api.md`, `references/search-params.md`, `references/collections.md`, `references/tags.md`, `references/exports.md`, `references/files-attachments.md`, `references/pagination.md`, `references/full-text.md`, `references/saved-searches.md`, `references/cli.md`, `references/mcp.md`, `references/error-handling.md`.
- Workspace targets: `paper/refs/references.bib`, `paper/refs/reading_matrix.md`, `paper/refs/target_journal.md`, `paper/assets/`, `paper/reviews/response_to_reviewers.md`, `paper/logs/decision_log.md`, `paper/logs/change_log.md`, `paper/logs/open_questions.md`.

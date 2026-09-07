# pyzotero — invocation scenarios

Realistic prompts for invoking the pyzotero skill inside the Auto-01-tiny-research
workspace. Each scenario names the `paper/` inputs it reads, the artifacts it
writes, and the boundary where it hands off to another skill. All Zotero
credentials are user-provided out of band via environment variables.

## Scenario 1: Export a Zotero collection to references.bib

Context: the user keeps their reading list in a Zotero group library named
"Genomics-2026", collection "Selected". `paper/refs/target_journal.md` sets a
Nature-methods-style BibTeX target, and `paper/refs/references.bib` is empty.
The user has exported `ZOTERO_LIBRARY_ID`, `ZOTERO_API_KEY`, and
`ZOTERO_LIBRARY_TYPE=group` in their shell; no key is pasted into the prompt.

Prompt:
> Authenticate to Zotero using the `ZOTERO_*` environment variables (do not ask
> me to paste the key into the chat). Find the collection "Selected" inside the
> group library, retrieve every top-level journal-article item with
> `everything()`, and export them as BibTeX into `paper/refs/references.bib`.
> Record the collection key and item count in `paper/logs/decision_log.md`. Do
> not de-duplicate or fix missing DOIs — hand those to the citation-management
> skill afterwards.

Inputs: `paper/refs/target_journal.md`, Zotero group library + "Selected"
collection (via env-var credentials).

Outputs: `paper/refs/references.bib`, a scope note in
`paper/logs/decision_log.md`. Do not draft prose, run statistics, or modify the
Zotero library — this is a read-only export.

## Scenario 2: Seed the reading matrix and pull a PDF attachment

Context: the manuscript is at the literature-review stage.
`paper/refs/reading_matrix.md` is empty and the user wants to shortlist from
their Zotero "To Read" collection, tagged `ml-genomics`, plus a specific PDF they
need for figure extraction. Credentials are provided via environment variables.

Prompt:
> Using my Zotero credentials from the environment, search the "To Read"
> collection for items tagged `ml-genomics`, sorted by date descending, and write
> the top 20 (title, creators, year, DOI, Zotero item key) into
> `paper/refs/reading_matrix.md`. Then download the PDF attachment of item
> `<ITEMKEY>` into `paper/assets/figures/source_<ITEMKEY>.pdf` so I can extract a
> figure. Do not create, edit, or delete any Zotero item. If any item is missing
> a DOI or title, list it in `paper/logs/open_questions.md` instead of guessing.

Inputs: Zotero "To Read" collection + tag `ml-genomics` (via env-var
credentials), a specific Zotero item key.

Outputs: `paper/refs/reading_matrix.md`, `paper/assets/figures/source_<ITEMKEY>.pdf`,
gaps appended to `paper/logs/open_questions.md`. Do not push references back into
Zotero, run citation-count audits, or perform thematic synthesis — hand those to
the write-API path, citation-management, and literature-deep-research
respectively.

## Scenario 3: Push a newly found reference back into Zotero (write path)

Context: during drafting, a relevant paper was found via citation-management and
added to `paper/refs/references.bib`. The user wants it mirrored into their
Zotero "Manuscript-2026" collection so their library stays in sync.
`ZOTERO_API_KEY` has **write** scope and is provided via the environment.

Prompt:
> Create a new Zotero item in the "Manuscript-2026" collection from the verified
> fields of the `@smith2026deep` entry in `paper/refs/references.bib` (use
> `item_template('journalArticle')`; copy only fields present in the bib entry —
> do not invent a DOI, volume, or pages). Add the tag `from-manuscript` and the
> note "Added via Auto-01-tiny-research on <date>". Return the new Zotero item
> key and append it to the bib entry's `zotero` annotation. Log the push in
> `paper/logs/change_log.md`. If the API key lacks write scope, stop and tell me
> rather than retrying or storing the key anywhere.

Inputs: `paper/refs/references.bib` (`@smith2026deep`), Zotero "Manuscript-2026"
collection (via env-var write-scoped credentials).

Outputs: new Zotero item key written back into `paper/refs/references.bib`, a
`paper/logs/change_log.md` entry. Do not modify any other Zotero item or upload
attachments in this pass.

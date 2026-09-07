---
name: paper-lookup
description: Look up scholarly papers via REST APIs (PubMed, arXiv, OpenAlex, Crossref, Semantic Scholar, Unpaywall) by topic, DOI/PMID, author, or open-access PDF to feed paper/refs/. Do not use for thematic synthesis, prose drafting, or bibliography formatting. Requires network and user-provided API keys; never invent or store credentials.
---

# Paper Lookup

## Purpose

Provide a thin, database-accurate lookup layer over ten academic REST APIs so the
single-paper workflow can resolve real bibliographic records — by topic, DOI, PMID,
PMCID, arXiv ID, ORCID, or open-access link — and hand the raw results to the skills
that own synthesis, drafting, and bibliography formatting. In Auto-01-tiny-research
this is a **TIER C external skill**: it performs live network calls to third-party
databases and may consume user-provided API keys for higher rate limits. It does not
interpret the literature or write the paper — it fetches verified raw records so
`literature-review`, `scientific-writing`, and `citation-management` can build on a
trustworthy evidence base.

The deliverable is the **raw JSON / parsed-XML response** from each queried database,
together with an explicit list of which databases and endpoints were called and which
returned nothing. Every record returned is traceable to the database and query that
produced it.

## Use When

- Resolving a specific paper by DOI / PMID / PMCID / arXiv ID / ORCID / title to a
  verified metadata record before adding it to `paper/refs/references.bib`.
- Finding open-access PDFs for a DOI (Unpaywall, CORE, PMC) to support
  full-text reading for `paper/refs/reading_matrix.md`.
- Pulling citation-graph or author-publication data (Semantic Scholar, OpenAlex) to
  size a field or identify seminal work for `paper/refs/`.
- Fetching preprints by date or DOI (bioRxiv, medRxiv, arXiv) when the question
  demands very recent or unpublished results.
- Cross-referencing identifiers (PMC ID Converter) or converting between
  PMID / PMCID / DOI across databases.
- Backing a comprehensive literature search by querying several databases in
  parallel and exporting raw JSON per source.

Do not use this skill for thematic synthesis or study-by-study summarization
(that is `literature-review`), for drafting manuscript prose (`scientific-writing`),
for running experiments or generating figures, or for final bibliography style
formatting and DOI verification of an already-frozen draft (`citation-management`).
It is also not a general web search engine: it only covers the ten listed databases.

## Required Inputs

- The user's query intent: a topic string, a specific identifier (DOI / PMID / PMCID /
  arXiv ID / OpenAlex ID / ORCID / ISSN), an author, a date range, or a known paper
  to cross-reference.
- The target workspace context: `paper/refs/target_journal.md` (for field and style
  conventions) and the `paper/refs/` directory to receive raw exports.
- **Network access** to the upstream REST endpoints — this skill cannot operate
  offline.
- **Any API keys the user chooses to supply, out of band.** Relevant optional keys
  and their registration pages:

  | Database | Env var | Required? |
  |---|---|---|
  | NCBI (PubMed, PMC) | `NCBI_API_KEY` | No (3 req/s without, 10 with) |
  | CORE | `CORE_API_KEY` | Yes for full text |
  | Semantic Scholar | `S2_API_KEY` | No (shared pool without) |
  | OpenAlex | `OPENALEX_API_KEY` | Recommended |

  These environment variables are noted here for documentation only; they are
  **not** declared in the frontmatter. The user must provide them; never hardcode,
  echo, or persist a key, token, or credential in this skill, its scripts, or any
  `paper/` file. Treat any encountered key string as `<user-provided-key>`. Fully
  open databases (bioRxiv, medRxiv, arXiv, Crossref, Unpaywall) need no key — for
  Crossref and Unpaywall include a `mailto` / `email` parameter for the polite pool.

## Workflow

1. **Classify the query.** Decide whether the user wants a topic search, a specific
   identifier lookup, an author's publications, open-access retrieval, citation-graph
   data, or full text. This determines the database set.
2. **Select database(s).** Use the routing table in
   `references/database-selection.md` (By-Use-Case intent→database table plus the
   Cross-Database Queries table). Match intent to the right source, and prefer
   cross-database queries when coverage should overlap — e.g. PubMed +
   OpenAlex + Semantic Scholar for a comprehensive biomedical search, or Crossref +
   Unpaywall + Semantic Scholar for "everything about one paper".
3. **Read the reference file.** Before any call, read the relevant
   `references/<database>.md` for the exact endpoint, query format, identifier
   conventions, and rate limit. Use `references/identifier-formats.md` (the Common
   Identifier Formats table) to confirm the supplied ID is in the right shape for
   the target database.
4. **Load any user-provided key.** Check the environment for the documented variable
   (e.g. `$NCBI_API_KEY`); if absent, proceed at the lower public rate limit and tell
   the user which key is missing and how to register one. Never invent or persist a key.
5. **Make the call(s).** Use the platform HTTP fetch tool (`WebFetch`, or `curl` via
   Bash as fallback) against the documented endpoint. Respect per-database rate
   limits (NCBI: 3/s public, 10/s with key; arXiv: 1 req per 3 s; Crossref: 5/s
   public, 10/s polite pool). Query independent databases in parallel; if HTTP 429
   occurs, wait briefly and retry once.
6. **Handle format quirks.** arXiv returns Atom XML (parse or extract fields); PMC
   eFetch returns JATS XML for full text — that is expected, not an error.
7. **Error recovery.** If a call fails, check the identifier format against
   `references/identifier-formats.md`, try an alternative identifier
   (DOI → title → PMID), or try a different database (CS paper not in PubMed →
   Semantic Scholar / OpenAlex). Report every failure with the database, error,
   and what was tried.
8. **Export raw results.** Write the raw JSON (or parsed XML) of each source to
   `paper/refs/raw_search_<source>.json` so the screen is reproducible, and log the
   query string, endpoint, date, and hit count. These exports feed
   `paper/experiments/reproducibility.md` when the search is part of the paper's method.
9. **Hand off.** Pass the raw records to `literature-review` (screening, dedup,
   thematic synthesis) and `citation-management` (verified `references.bib`).
   Record any dead-end lookups (wrong-field hits, vanished DOIs) to
   `paper/logs/dead_ends.md` and any scope-affecting findings to
   `paper/logs/insights.md`.

## Output Contract

- Raw JSON / parsed-XML response from each queried database, defaulting to the full
  payload (present a trimmed excerpt only if very large, and note that more is available).
- An explicit **"Databases Queried"** list naming each database and the specific
  endpoint/identifier used; if a query returned zero results, say so explicitly
  rather than omitting it.
- `paper/refs/raw_search_<source>.json` — raw per-source exports, kept for
  reproducibility alongside the search-strategy note (databases, strings, dates, counts).
- A search-strategy / provenance note routed to `paper/logs/decision_log.md` so the
  chosen databases and queries are traceable.
- Identifier mismatches, failed lookups, and recoveries logged to
  `paper/logs/dead_ends.md` (and to `paper/logs/open_questions.md` when they affect scope).
- The skill does **not** write `references.bib` or `reading_matrix.md` directly —
  those are produced by `citation-management` and `literature-review` from these raw
  records.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only paper-lookup`
- `python src/S03_Scripts/validate_project.py`
- Every raw export in `paper/refs/raw_search_*.json` parses as valid JSON (or, for
  arXiv/PMC, as parseable XML) and carries the source database, query string, and date.
- No API key, token, or credential appears in any output file — grep
  `paper/refs/raw_search_*.json` and `paper/logs/` for `sk-`, `gh[pousr]_`,
  `AKIA`, and `YOUR_KEY` placeholders before finishing; replace any live value with
  `<user-provided-key>`.

## Boundaries

- **Network required.** This skill issues live REST calls to external academic
  databases; it cannot function offline and may be blocked by firewalls or rate
  limits. Tell the user when a call cannot reach the network.
- **Credentials are user-provided only.** The optional `NCBI_API_KEY`,
  `CORE_API_KEY`, `S2_API_KEY`, and `OPENALEX_API_KEY` are read from the user's
  environment when present; this skill never generates, stores, transcribes, or
  commits a secret. Any key encountered in inputs or logs is replaced with
  `<user-provided-key>`.
- **Lookup, not synthesis.** Returns raw records; it does not summarize, appraise
  quality, decide inclusion, or draft prose — defer to `literature-review`,
  `scientific-writing`, and `citation-management`.
- **Database scope.** Only the ten named databases. For general web search, use the
  repo's broad search tool; for venue/JCR lookups use `04-journal-fit`.
- **Respect rate limits and ToS.** Honor documented per-database rate limits
  (especially arXiv's 1 req / 3 s and NCBI's ceiling), include a `mailto`/`email`
  for polite pools, and retry at most once on HTTP 429.

## Stop With

- Raw records for every queried database are written to `paper/refs/raw_search_*.json`
  and a "Databases Queried" summary with endpoints and hit counts is returned.
- Every failed or zero-result query is reported explicitly, with the identifier
  format checked and at least one alternative database tried.
- Records are handed to `literature-review` / `citation-management` for screening,
  synthesis, and bibliography formatting — this skill does not produce
  `references.bib` or `reading_matrix.md`.
- All outputs are scrubbed of any key or token; no live credential is present in any
  `paper/` file.

## References

- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT);
  see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Per-database reference files (endpoints, query formats, rate limits, examples):
  `.agent/skills/paper-lookup/references/pubmed.md`, `pmc.md`, `biorxiv.md`,
  `medrxiv.md`, `arxiv.md`, `openalex.md`, `crossref.md`,
  `semantic-scholar.md`, `core.md`, `unpaywall.md`.
- Selection guide (intent→database routing): `references/database-selection.md`.
- Identifier formats (DOI/PMID/arXiv ID shape + cross-DB prefixes):
  `references/identifier-formats.md`.
- Consumed by and hands off to: `paper/refs/reading_matrix.md`,
  `paper/refs/references.bib`, `paper/refs/target_journal.md`,
  `paper/refs/raw_search_<source>.json`, `paper/logs/decision_log.md`,
  `paper/logs/dead_ends.md`, `paper/logs/insights.md`,
  `paper/experiments/reproducibility.md`.
- Sibling skills: `literature-review` (synthesis), `citation-management`
  (bibliography), `04-journal-fit` (venue lookups).

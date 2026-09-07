# paper-lookup — invocation scenarios

Realistic prompts for invoking the paper-lookup external skill inside the
Auto-01-tiny-research workspace. Each scenario shows the kind of request that
should trigger this skill, the workspace inputs it reads, the network calls it
makes, and the raw artifacts it must produce. paper-lookup is a TIER C external
skill: it performs live REST calls against academic databases and may use
user-provided API keys; it returns raw records only and hands them to
literature-review / citation-management for synthesis and bibliography work.

## Scenario 1: Resolve a DOI and fetch its open-access full text

> I have DOI `10.1038/s41586-021-03819-2` and need the verified metadata record
> plus an open-access PDF link so I can read the full text for
> `paper/refs/reading_matrix.md`. The field is molecular biology, so check PMC
> for full text too.

This triggers paper-lookup: a specific-identifier lookup spanning metadata and
open access. The skill reads the DOI, confirms the identifier format
(`10.xxxx/xxxxx`), and queries Crossref for the canonical metadata record,
Unpaywall for the OA status and PDF link, and PMC (eFetch) for any full-text
JATS XML. Calls run in parallel where independent. It writes the raw Crossref
JSON to `paper/refs/raw_search_crossref.json`, the Unpaywall JSON to
`paper/refs/raw_search_unpaywall.json`, and (if found) the PMC XML to
`paper/refs/raw_search_pmc.xml`, then returns a "Databases Queried" list naming
each endpoint and the OA outcome. No key is strictly required here (Crossref
and Unpaywall are open; add a `mailto` for the polite pool). The skill does NOT
add the entry to `references.bib` — it hands the verified record to
`citation-management`.

## Scenario 2: Comprehensive biomedical topic search across three databases

> For `paper/refs/target_journal.md` (a Nature-family clinical journal) I need
> a comprehensive set of recent papers on "CRISPR base editing off-target
> effects", 2022-01-01 onward, across PubMed, OpenAlex, and Semantic Scholar.
> Export raw JSON per source so the screen is reproducible. I have an
> `NCBI_API_KEY` exported in my shell; use it for the higher PubMed rate.

This triggers paper-lookup: a multi-database topic search. The skill reads the
topic and date range, reads `$NCBI_API_KEY` from the environment (without
echoing it) for PubMed's 10 req/s ceiling, and runs esearch+esummary on PubMed,
the OpenAlex `/works?search=...&filter=...` endpoint, and the Semantic Scholar
`/graph/v1/paper/search/bulk` endpoint. arXiv is not appropriate (not CS/physics)
and is skipped with a noted reason. Raw results are written to
`paper/refs/raw_search_pubmed.json`, `paper/refs/raw_search_openalex.json`, and
`paper/refs/raw_search_semantic_scholar.json`, and a search-strategy note
(databases, query strings, date filter, per-source hit counts) is appended to
`paper/logs/decision_log.md`. The records are then handed to literature-review
for dedup, screening, and thematic synthesis. If a 429 is hit on Semantic
Scholar (shared pool), the skill waits briefly and retries once.

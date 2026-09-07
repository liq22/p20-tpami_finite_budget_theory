---
name: research-lookup
description: Look up web research via parallel-cli search, Parallel Chat API, or Perplexity with auto routing, for live cited evidence feeding paper/refs/. Do not use for DB record fetches (paper-lookup), synthesis, drafting, or references.bib. Requires network and user-provided PARALLEL_API_KEY/OPENROUTER_API_KEY; never invent, hardcode, or store secrets.
---

# Research Lookup

## Purpose

Provide a real-time research and general-information lookup layer that goes beyond
the scholarly-database scope of `paper-lookup`. Where `paper-lookup` hits ten fixed
academic REST databases for verified metadata records, `research-lookup` performs
**open web search and deep multi-source synthesis** across the whole web (news,
preprints, technical docs, market data, government statistics) and routes each
query to the most appropriate of three backends. It returns synthesized findings
with inline citations and the underlying source URLs, saved for reproducibility.

In Auto-01-tiny-research this is a **TIER C external skill**: every backend makes
live network calls to a third-party API (`api.parallel.ai`, `openrouter.ai`) and
consumes user-provided credentials. It does not write manuscript prose, screen
studies, or format the bibliography — it gathers cited current information so
`literature-review`, `scientific-writing`, and `citation-management` can build on
a traceable evidence base.

The deliverable is a **synthesized, cited answer** plus the raw saved search
result (JSON or markdown), an explicit "Backend Used" note, and a sources list
preserving every URL and DOI.

## Use When

- Gathering current research context, recent findings, or emerging trends for the
  introduction and discussion sections of `paper/draft/` markdown drafts.
- Verifying facts, statistics, or scientific claims against the current web before
  committing them to `paper/experiments/statistics.md` or manuscript prose.
- Looking up technical protocols, specifications, or methodologies to validate
  methods against current standards (feed `paper/experiments/reproducibility.md`).
- Finding market/industry data, adoption statistics, or competitive intelligence
  relevant to a paper's motivation or `paper/refs/target_journal.md` framing.
- Pulling comparative analysis or background evidence that spans non-academic
  sources (news, technical docs, government data) that `paper-lookup`'s ten
  academic databases do not cover.
- Running an explicitly requested deep, exhaustive, multi-source synthesis (Parallel
  Chat API) for a complex open question.

Do not use this skill for verified scholarly-database record fetches by DOI / PMID /
arXiv ID (that is `paper-lookup`), for study-by-study thematic synthesis and
screening (`literature-review`), for drafting manuscript prose (`scientific-writing`),
for running experiments or generating figures, or for final bibliography formatting
and DOI verification of a frozen draft (`citation-management`). It is also not a
local file search or an offline tool.

## Required Inputs

- The user's query intent: a topic string, a question, an author, a date range, or
  a "find papers on ..." / "cite ..." academic request. The skill auto-routes based
  on keywords (see Workflow).
- The target workspace context: `paper/refs/target_journal.md` (field and style
  conventions) and the directory that will receive saved results
  (`paper/refs/` for raw search exports).
- **Network access** to `api.parallel.ai` and `openrouter.ai` — this skill cannot
  operate offline and may be blocked by firewalls or rate limits.
- **User-provided credentials, supplied out of band.** These are documented here
  for reference only and are **never** declared in the frontmatter:

  | Backend | Env var | Required? |
  |---|---|---|
  | parallel-cli search (default) | `PARALLEL_API_KEY` | Yes for primary backend |
  | Parallel Chat API (deep) | `PARALLEL_API_KEY` (same) | Only for deep mode |
  | Perplexity sonar-pro-search (academic) | `OPENROUTER_API_KEY` | Only for academic mode |

  The user must provide any key they wish to use; never hardcode, echo, log, or
  persist a key, token, or credential in this skill, its scripts, or any `paper/`
  file. Treat any encountered key string as `<user-provided-key>`. If a required
  key is absent, tell the user which variable is missing and how to register one,
  then either fall back to a backend whose key is present or stop with a clear
  error.

## Workflow

1. **Check existing results first.** Before any network call, list
   `paper/refs/research_*.json` / `papers_*.md`. If a prior lookup already covers
   the topic, re-read the saved file instead of spending another API call.
2. **Classify and route the query.** Detect the query type to pick a backend:
   - **Academic keywords** (`find papers`, `cite`, `doi`, `pubmed`, `pmid`,
     `peer-reviewed`, `systematic review`, `meta-analysis`, `seminal`,
     `foundational papers`, `arxiv`, `preprint`) → Perplexity sonar-pro-search
     (academic mode).
   - **Explicit deep request** ("deep research", "exhaustive", "comprehensive
     synthesis") → Parallel Chat API `core` model (60 s–5 min latency).
   - **Everything else** (general research, market data, technical info, current
     events, comparative analysis, fact-checking) → parallel-cli search (default,
     fast, 2–10 s).
3. **Load any user-provided key** for the chosen backend from the environment
   (without echoing it). If absent, fall back to another available backend or stop
   with a clear message naming the missing variable. Never invent or persist a key.
4. **Run parallel-cli search (default).** For scientific/technical queries run two
   searches and merge, leading with academic sources:
   - Academic-focused: `parallel-cli search "<query>" -q "<kw>" ... --json
     --max-results 10 --excerpt-max-chars-total 27000 --include-domains
     "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,semanticscholar.org,
     biorxiv.org,medrxiv.org,nature.com,science.org,cell.com,pnas.org,nih.gov,
     ieee.org,acm.org,springer.com,wiley.com"`.
   - General: same without `--include-domains`.
   - Use `--after-date YYYY-MM-DD` for time-sensitive queries; force a single
     backend via `python scripts/research_lookup.py "<query>" --force-backend
     parallel|perplexity`.
5. **Prioritize quality.** When ranking papers, prefer Tier-1 venues (Nature,
   Science, Cell, NEJM, Lancet, JAMA, PNAS; NeurIPS/ICML/ICLR/ACL/CVPR) and apply
   the citation-by-age thresholds (e.g. 7+ years & 500+ citations = seminal). Note
   tier/classification only — final inclusion decisions belong to
   `literature-review`.
6. **Save every result.** Always write the raw output to `paper/refs/` with the
   `-o` flag so the search is reproducible:
   - parallel-cli JSON → `paper/refs/research_<topic>.json` (or
     `research_<topic>-academic.json`).
   - Parallel deep research / Perplexity → `paper/refs/research_<topic>.md` /
     `paper/refs/papers_<topic>.md`.
   - Batch → `paper/refs/batch_research_<topic>.md`.
   Saved files MUST preserve all citations, source URLs, and DOIs.
7. **Log the lookup.** Append a one-line provenance record to
   `paper/logs/decision_log.md` (backend, query, date, hit count, saved path) so
   the search strategy is auditable, mirroring how `paper-lookup` records its
   database calls.
8. **Hand off.** Pass the synthesized findings and saved raw exports to
   `literature-review` (screening, dedup, thematic synthesis) and
   `citation-management` (verified `references.bib`). Record scope-affecting
   findings to `paper/logs/insights.md` and dead-end lookups (wrong-field hits,
   vanished sources) to `paper/logs/dead_ends.md`.

## Output Contract

- A synthesized, cited answer to the query, with inline citations drawn from the
  search results. For Perplexity/academic mode: 5–8 high-quality citations with
  authors, titles, journals, years, DOIs, citation counts, and venue-tier notes.
- An explicit **"Backend Used"** line naming the backend, model, and latency tier
  (fast / deep), so the cost and source of every answer is visible.
- A **Sources** section listing every referenced URL (and DOI where available),
  grouped by type (academic / general / news / technical). Zero-result queries are
  stated explicitly rather than omitted.
- Raw saved exports under `paper/refs/`:
  - `paper/refs/research_<topic>.json` — parallel-cli JSON (title, URL,
    publish_date, excerpts per result).
  - `paper/refs/research_<topic>.md` / `paper/refs/papers_<topic>.md` — deep /
    academic markdown reports with a `Sources (N):` block and an
    `Additional References (N):` block carrying DOIs.
- A provenance line appended to `paper/logs/decision_log.md`.
- The skill does **not** write `references.bib`, `reading_matrix.md`, or manuscript
  drafts — those are produced by `citation-management`, `literature-review`, and
  `scientific-writing` from these results.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only research-lookup`
- `python src/S03_Scripts/validate_project.py`
- Every saved export in `paper/refs/research_*.json` parses as valid JSON and
  carries the query string, date, and backend; every `.md` export has a non-empty
  `Sources` section.
- No API key, token, or credential appears in any output file — grep
  `paper/refs/research_*` and `paper/logs/` for `sk-`, `gh[pousr]_`, `AKIA`, and
  `PRIVATE KEY` before finishing; replace any live value with
  `<user-provided-key>`.
- Backend selection is explicit: every answer states which backend produced it,
  and any fallback (e.g. parallel-cli → Perplexity on insufficient results) is
  noted with the reason.

## Boundaries

- **Network required.** This skill issues live calls to `api.parallel.ai` (parallel-cli
  search and Parallel Chat API) and `openrouter.ai` (Perplexity); it cannot function
  offline and may be blocked by firewalls, paywalls, or rate limits. Information has
  an upstream cutoff and may not access full text behind paywalls. Tell the user
  when a call cannot reach the network.
- **Credentials are user-provided only.** The optional `PARALLEL_API_KEY` and
  `OPENROUTER_API_KEY` are read from the user's environment when present; this skill
  never generates, stores, transcribes, or commits a secret. Any key encountered in
  inputs or logs is replaced with `<user-provided-key>`.
- **Lookup/synthesis, not bibliography.** Returns cited findings and raw exports; it
  does not verify DOI metadata, decide final inclusion, or format
  `references.bib` — defer to `paper-lookup` (record verification),
  `literature-review` (synthesis), and `citation-management` (bibliography).
- **Scope vs. `paper-lookup`.** Use this skill for open web search, recent news,
  market/technical data, and deep multi-source synthesis. For verified metadata
  records from the ten scholarly databases, use `paper-lookup`. The two are
  complementary, not redundant.
- **Respect rate limits and ToS.** Parallel Chat API ceiling is ~300 req/min;
  Perplexity responds in 5–15 s; retry at most once on HTTP 429 with a brief wait.
  Do not attempt to bypass paywalls or terms of service of any source.

## Stop With

- A synthesized, cited answer is returned, the backend and latency tier are named,
  and a Sources section with every URL (and DOI where available) is present.
- The raw result is saved under `paper/refs/` (`research_*.json` / `*.md` /
  `papers_*.md`) with all citations, URLs, and DOIs preserved, and a provenance
  line is appended to `paper/logs/decision_log.md`.
- Any failed or zero-result query is reported explicitly, with at least one
  alternative backend or query rephrase tried.
- Findings are handed to `literature-review` / `citation-management` for screening,
  synthesis, and bibliography formatting — this skill does not produce
  `references.bib`, `reading_matrix.md`, or manuscript prose.
- All outputs are scrubbed of any key or token; no live credential is present in
  any `paper/` file.

## References

- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT);
  see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Backend reference doc (routing logic, commands, citation-ranking tables):
  `.agent/skills/research-lookup/references/backends.md`.
- Backend driver script (routing, Parallel Chat API, Perplexity via OpenRouter):
  `.agent/skills/research-lookup/scripts/research_lookup.py` (see
  `scripts/README.md` for purpose, inputs, outputs, network calls, and writes).
- Invocation scenarios: `.agent/skills/research-lookup/examples/prompts.md`.
- Consumed by and hands off to: `paper/refs/research_*.json`,
  `paper/refs/papers_*.md`, `paper/refs/target_journal.md`,
  `paper/refs/reading_matrix.md`, `paper/refs/references.bib`,
  `paper/logs/decision_log.md`, `paper/logs/insights.md`,
  `paper/logs/dead_ends.md`, `paper/experiments/reproducibility.md`,
  `paper/experiments/statistics.md`.
- Sibling skills: `paper-lookup` (scholarly-database record fetches),
  `literature-review` (synthesis), `citation-management` (bibliography),
  `scientific-writing` (drafting).

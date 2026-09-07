---
name: bgpt-paper-search
description: Query the BGPT remote MCP server for structured full-text experimental data to feed paper/refs/. Use when a screen must hit live BGPT and abstracts are insufficient. Do not use for synthesis or standard REST DBs (use literature-review, paper-lookup). Needs network to bgpt.pro and a user-provided BGPT_API_KEY for paid results; never store secrets.
---

# BGPT Paper Search

## Purpose

Provide a thin, source-accurate lookup layer over the **BGPT** remote MCP server
(`https://bgpt.pro/mcp/sse`), which indexes a curated database of scientific
papers built from structured experimental data extracted from full-text studies.
Unlike traditional databases that return titles and abstracts, BGPT returns the
methods, quantitative results, sample sizes, effect sizes, quality assessments,
and 25+ metadata fields per paper — exactly the fields needed to populate an
evidence matrix or scoping-review screen.

In Auto-01-tiny-research this is a **TIER C external skill**: it performs live
network calls to a third-party MCP server and may consume a user-provided BGPT
API key for paid results. It does **not** interpret the literature, decide study
inclusion, or write the paper — it fetches verified structured records so
`literature-review`, `scientific-writing`, and `citation-management` can build on
a trustworthy evidence base.

The deliverable is the **raw structured response** from the BGPT
`search_papers` MCP tool, together with an explicit record of the query string,
the call date, and the number of results returned. Every record is traceable to
the query that produced it.

## Use When

- Screening for papers with specific **experimental details** (intervention,
  model organism, assay, protocol) that live in full text, not abstracts.
- Pulling **quantitative results, sample sizes, or effect sizes** across studies
  to populate `paper/experiments/evidence_matrix.md` or a meta-analysis table.
- Comparing **methodologies** or **quality scores / evidence grading** across a
  set of studies for a systematic or scoping review feeding `paper/refs/`.
- Building structured evidence tables for clinical guidelines or
  `paper/draft/` methods sections that cite exact numerical results.
- Needing a single comprehensive search that returns full-text-extracted fields
  rather than abstract-only metadata.

Do not use this skill for thematic synthesis or study-by-study summarization
(that is `literature-review`), for drafting manuscript prose
(`scientific-writing`), for final bibliography style formatting and DOI
verification (`citation-management`), for general web search, or for searches
across the standard REST databases PubMed / OpenAlex / arXiv / Crossref etc.
(that is `paper-lookup`). BGPT is a single specialized source.

## Required Inputs

- The user's **search query intent**: a topic string, a PICO-style question, a
  methods/assay description, or a specific experimental detail to match in full
  text.
- The target workspace context: `paper/refs/target_journal.md` (for field and
  style conventions) and the `paper/refs/` directory to receive raw exports.
- **Network access** to `https://bgpt.pro/mcp/sse` — this skill cannot operate
  offline and may be blocked by firewalls or rate limits.
- **The BGPT MCP server configured in the agent host.** This skill only
  *instructs the agent to call the `search_papers` MCP tool*; it does not enable
  MCP access by itself. The user must add the server to their MCP configuration
  (see `references/bgpt_mcp_setup.md`). A minimal entry is:

  ```json
  {
    "mcpServers": {
      "bgpt": {
        "command": "npx",
        "args": ["mcp-remote", "https://bgpt.pro/mcp/sse"]
      }
    }
  }
  ```

- **Optional `BGPT_API_KEY` for paid results**, the user provides out of band
  (free tier: ~50 searches per network, no key; paid: per-result pricing with a
  key from `bgpt.pro/mcp`). This environment variable is noted here for
  documentation only; it is **not** declared in the frontmatter. The user must
  provide it; never hardcode, echo, or persist a key, token, or credential in
  this skill, its scripts, or any `paper/` file. Treat any encountered key
  string as `<user-provided-key>`.

## Workflow

1. **Confirm the source is the right one.** Verify the query needs BGPT's
   full-text-extracted structured fields rather than abstract-only metadata. If
   the user actually wants PubMed / OpenAlex / arXiv / Crossref, redirect to
   `paper-lookup`.
2. **Verify MCP availability.** Before invoking, confirm the `bgpt` MCP server
   is configured in the host and its `search_papers` tool is exposed. If it is
   not configured, stop and point the user at `references/bgpt_mcp_setup.md`;
   do not attempt to install or configure MCP yourself.
3. **Form the query string.** Express the user's intent as a concise topical or
   PICO query. Prefer specific experimental terms (intervention, model,
   outcome, assay) since BGPT indexes full-text methods and results.
4. **Load any user-provided key.** Check the environment for `$BGPT_API_KEY`; if
   absent, proceed on the free tier (~50 searches per network, no key) and tell
   the user when paid results are skipped because no key was supplied. Never
   invent or persist a key.
5. **Call `search_papers` via the MCP interface** (not via Bash). Pass the query
   string and honor BGPT's result limits. If the call fails with a network or
   auth error, report it explicitly with the endpoint, error, and what was
   tried; retry at most once on a transient failure.
6. **Capture the structured fields.** For each returned record, retain at
   minimum: title, authors, journal, year, DOI, methods, quantitative results,
   sample sizes, quality/evidence scores, and conclusions (25+ fields per
   paper). Do not paraphrase numerical results — copy them verbatim with units.
7. **Export raw results.** Write the raw structured response to
   `paper/refs/raw_search_bgpt.json` (one record per item, carrying the query
   string, endpoint, and date) so the screen is reproducible and feeds
   `paper/experiments/reproducibility.md`.
8. **Hand off.** Pass the raw records to `literature-review` (screening, dedup,
   thematic synthesis), `citation-management` (verified `references.bib`), and
   `paper/experiments/evidence_matrix.md` (structured numerical extraction).
   Record scope-affecting findings to `paper/logs/insights.md` and any dead-end
   queries (wrong-field hits, no key for paid results) to
   `paper/logs/dead_ends.md`. Log the search strategy in
   `paper/logs/decision_log.md`.

## Output Contract

- The **raw structured response** from the BGPT `search_papers` MCP tool,
  including the 25+ fields per paper (title, authors, journal, year, DOI,
  methods, results, sample sizes, quality scores, conclusions). Present a
  trimmed excerpt only if very large, and note that more is available.
- An explicit **"Source: BGPT"** statement naming the MCP endpoint
  (`https://bgpt.pro/mcp/sse`), the query string, the call date, and the result
  count. If the query returned zero results or skipped paid results for lack of
  a key, say so explicitly rather than omitting it.
- `paper/refs/raw_search_bgpt.json` — the raw per-query export, kept for
  reproducibility alongside the search-strategy note.
- A search-strategy / provenance note routed to `paper/logs/decision_log.md` so
  the BGPT query is traceable.
- Failures and skipped paid results logged to `paper/logs/dead_ends.md` (and to
  `paper/logs/open_questions.md` when they affect scope).
- The skill does **not** write `references.bib` or `reading_matrix.md` directly
  — those are produced by `citation-management` and `literature-review` from
  these raw records.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only bgpt-paper-search`
- `python src/S03_Scripts/validate_project.py`
- The raw export in `paper/refs/raw_search_bgpt.json` is valid JSON and carries
  the query string, endpoint (`https://bgpt.pro/mcp/sse`), and date.
- Numerical results in any `paper/experiments/evidence_matrix.md` row trace back
  to a record in `paper/refs/raw_search_bgpt.json` (same DOI/title).
- No API key, token, or credential appears in any output file — grep
  `paper/refs/raw_search_bgpt.json` and `paper/logs/` for `sk-`, `gh[pousr]_`,
  `AKIA`, and `BGPT_API_KEY` values before finishing; replace any live value
  with `<user-provided-key>`.

## Boundaries

- **Network required.** This skill issues a live MCP call to the remote BGPT
  server at `https://bgpt.pro/mcp/sse`; it cannot function offline and may be
  blocked by firewalls, rate limits, or the free-tier search cap. Tell the user
  when a call cannot reach the network or when paid results are unavailable.
- **Credentials are user-provided only.** The optional `BGPT_API_KEY` is read
  from the user's environment when present; this skill never generates, stores,
  transcribes, or commits a secret. Any key encountered in inputs or logs is
  replaced with `<user-provided-key>`.
- **MCP-hosted tool, not self-contained.** This skill only instructs the agent
  to call the `search_papers` MCP tool exposed by a user-configured `bgpt`
  server; it does not install, start, or configure MCP, and it cannot fabricate
  results when the server is absent. **Caution (known upstream issue):** the
  upstream skill's `allowed-tools` declaration is inconsistent with its
  MCP-search workflow — the tool surface it lists does not actually include the
  MCP `search_papers` tool it relies on. Treat the listed tools as advisory; the
  real capability comes from the configured MCP server, and behavior is
  undefined if the host has no `bgpt` server configured. (Recorded in
  `known_upstream_issues`.)
- **Lookup, not synthesis.** Returns raw structured records; it does not
  summarize, appraise quality beyond what BGPT reports, decide inclusion, or
  draft prose — defer to `literature-review`, `scientific-writing`, and
  `citation-management`.
- **Single source.** BGPT is one specialized database. For multi-database
  screens use `paper-lookup`; for venue/JCR lookups use `04-journal-fit`.

## Stop With

- The raw structured BGPT response for the query is written to
  `paper/refs/raw_search_bgpt.json` and a "Source: BGPT" summary with the
  endpoint, query string, date, and hit count is returned.
- Any zero-result query, skipped paid result, or failed call is reported
  explicitly, with the cause (network, auth, free-tier cap) noted.
- Records are handed to `literature-review` / `citation-management` /
  `paper/experiments/evidence_matrix.md` for screening, synthesis, bibliography
  formatting, and structured extraction — this skill does not produce
  `references.bib` or `reading_matrix.md`.
- All outputs are scrubbed of any key or token; no live credential is present
  in any `paper/` file.

## References

- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- MCP setup and pricing notes: `.agent/skills/bgpt-paper-search/references/bgpt_mcp_setup.md`.
- Consumed by and hands off to: `paper/refs/reading_matrix.md`,
  `paper/refs/references.bib`, `paper/refs/target_journal.md`,
  `paper/refs/raw_search_bgpt.json`, `paper/experiments/evidence_matrix.md`,
  `paper/experiments/reproducibility.md`, `paper/logs/decision_log.md`,
  `paper/logs/dead_ends.md`, `paper/logs/insights.md`.
- Sibling skills: `paper-lookup` (standard REST databases),
  `literature-review` (synthesis), `citation-management` (bibliography),
  `04-journal-fit` (venue lookups).

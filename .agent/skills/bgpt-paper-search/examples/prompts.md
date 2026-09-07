# bgpt-paper-search — invocation scenarios

Realistic prompts for invoking the bgpt-paper-search external skill inside the
Auto-01-tiny-research workspace. Each scenario shows the kind of request that
should trigger this skill, the workspace inputs it reads, the network call it
makes via the BGPT MCP server, and the raw artifact it must produce.
bgpt-paper-search is a TIER C external skill: it performs a live MCP call to the
remote BGPT server (`https://bgpt.pro/mcp/sse`) and may use a user-provided
`BGPT_API_KEY` for paid results; it returns raw structured records only and
hands them to `literature-review` / `citation-management` /
`paper/experiments/evidence_matrix.md` for synthesis and bibliography work.

## Scenario 1: Find quantitative experimental results for an evidence matrix

> I am writing the methods and results comparison for a paper on "CRISPR base
> editing off-target effects in human cells". For `paper/refs/target_journal.md`
> (a Nature-family methods journal) I need every study's **assay, cell line,
> sample size, and measured off-target rate** pulled from full text, not just
> abstracts, so I can fill `paper/experiments/evidence_matrix.md`. Try BGPT. I
> have a `BGPT_API_KEY` exported in my shell; use it for the paid results.

This triggers bgpt-paper-search: a full-text structured search where
abstract-only databases are insufficient. The skill confirms the user wants
BGPT's extracted experimental fields (not a standard PubMed/OpenAlex screen),
verifies the `bgpt` MCP server is configured in the host, reads `$BGPT_API_KEY`
from the environment (without echoing or persisting it), and calls the
`search_papers` MCP tool with the query "CRISPR base editing off-target effects
human cells". It retains, per record, the methods, quantitative results, sample
sizes, quality scores, and DOI, copying numerical values verbatim with units.
It writes the raw structured response to `paper/refs/raw_search_bgpt.json`
(carrying the query string, endpoint, and date), returns a "Source: BGPT"
summary with the hit count, and hands the records to `literature-review` (for
screening and dedup) and to `paper/experiments/evidence_matrix.md` (for the
structured numerical rows). The skill does NOT write `references.bib` — that is
`citation-management`. If the MCP server is not configured, it stops and points
the user at `references/bgpt_mcp_setup.md`.

## Scenario 2: Scoping screen for a systematic review when abstracts are too thin

> For `paper/refs/reading_matrix.md` I'm scoping a systematic review on
> "intermittent fasting effects on insulin sensitivity in prediabetic adults".
> Standard databases keep giving me abstract-only hits that hide the sample
> sizes and study designs. Run one BGPT pass so I have the methods, sample
> sizes, and quality scores up front. No key — stay on the free tier and tell
> me if you hit the cap.

This triggers bgpt-paper-search: a single-source scoping pass meant to surface
full-text-extracted structured fields. The skill confirms BGPT is the right
source (the user explicitly rejects abstract-only results), verifies the
`bgpt` MCP server is configured, finds no `$BGPT_API_KEY` in the environment,
and proceeds on the free tier (~50 searches per network), calling the
`search_papers` MCP tool with the PICO-style query. It writes the raw response
to `paper/refs/raw_search_bgpt.json` with the query, endpoint, and date, and
returns a "Source: BGPT" summary noting the free tier and the result count. If
the free-tier cap is reached or paid results are skipped for lack of a key, it
reports that explicitly and logs the limitation in `paper/logs/dead_ends.md`
(and `paper/logs/open_questions.md` if it affects scope). The records are then
handed to `literature-review` for screening and to `citation-management` for
bibliography work. For any follow-up searches that need PubMed / OpenAlex /
arXiv / Crossref, the skill redirects to `paper-lookup`.

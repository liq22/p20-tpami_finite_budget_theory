# research-lookup — invocation scenarios

Realistic prompts for invoking the research-lookup external skill inside the
Auto-01-tiny-research workspace. Each scenario shows the kind of request that
should trigger this skill, the workspace inputs it reads, the network calls it
makes, and the cited artifacts it must produce. research-lookup is a TIER C
external skill: it performs live web calls to `api.parallel.ai` and
`openrouter.ai` and uses user-provided `PARALLEL_API_KEY` / `OPENROUTER_API_KEY`
credentials; it returns cited current information and hands the raw exports to
literature-review / citation-management for synthesis and bibliography work.

## Scenario 1: Fast current-evidence lookup for an introduction (default backend)

> I'm drafting the introduction for `paper/draft/main.md` and need current,
> cited context on "recent advances in transformer attention mechanisms, 2024
> onward" to motivate the gap. Save the raw results so the screen is
> reproducible, and surface academic sources first.

This triggers research-lookup with the **default parallel-cli search** backend
(general research, fast, 2–10 s). The skill first lists `paper/refs/research_*.json`
to avoid a duplicate call, then runs two parallel-cli searches and merges: an
academic-focused search with `--include-domains` covering arXiv, Semantic
Scholar, Nature, Science, IEEE, ACM, and an unrestricted general search. It
writes `paper/refs/research_transformer_attention-academic.json` and
`paper/refs/research_transformer_attention-general.json` (each preserving
`title`, `url`, `publish_date`, `excerpts`), returns a synthesized answer with
inline citations and a Sources section grouped by type, names the backend and
latency tier ("parallel-cli search, fast"), and appends a one-line provenance
record (backend, query, date, hit count, saved paths) to
`paper/logs/decision_log.md`. It does NOT add anything to `references.bib` —
the records are handed to `literature-review` and `citation-management`. Only
`PARALLEL_API_KEY` is needed; if it is absent the skill stops with a clear
message naming the missing variable and how to register one.

## Scenario 2: Academic paper search routed to Perplexity (find foundational papers)

> For `paper/refs/target_journal.md` (a Nature-family ML journal) I need the
> foundational and seminal papers on "quantum error correction" — full
> citations with DOIs, citation counts, and venue tier, so I can build a
> rigorous reference base in `paper/refs/references.bib`.

This triggers research-lookup's **Perplexity sonar-pro-search** backend,
auto-routed by the academic keywords ("foundational papers", "seminal",
"cite"). The skill confirms the routing, loads `OPENROUTER_API_KEY` from the
environment (without echoing it), and issues the academic-mode query. It writes
the markdown report — with 5–8 high-quality citations (authors, titles,
journals, years, DOIs, citation counts, venue-tier notes) and a `Sources (N):`
plus `Additional References (N):` block — to
`paper/refs/papers_quantum_error_correction.md`, names the backend
("Perplexity sonar-pro-search, academic, 5–15 s"), and logs the lookup to
`paper/logs/decision_log.md`. Papers are ranked against the citation-by-age
thresholds and Tier-1 venues (Nature/Science/Cell/PNAS; NeurIPS/ICML/ICLR) as
a note only; final inclusion belongs to `literature-review`. If
`OPENROUTER_API_KEY` is missing the skill falls back to an academic-focused
parallel-cli search (if `PARALLEL_API_KEY` is present) or stops with a clear
error. It does NOT write `references.bib` — verified entries come from
`citation-management`.

## Scenario 3: Explicit deep multi-source synthesis via the Parallel Chat API

> Do an exhaustive deep-research synthesis on "the current state of mRNA
> vaccine platforms for cancer immunotherapy" — I need a multi-source report
> spanning academic, clinical-trial, and industry sources to inform
> `paper/logs/insights.md` and the discussion section. Cost and latency are
> acceptable.

This triggers research-lookup's **Parallel Chat API** (`core` model) backend,
auto-routed by the explicit "exhaustive deep-research" phrasing. The skill
warns the user that this backend takes 60 s–5 min and is more expensive, loads
`PARALLEL_API_KEY`, and issues the deep query. It writes the synthesized
markdown report (with inline citations and a research-basis block of URLs,
reasoning, and confidence levels) to `paper/refs/research_mrna_cancer.md`,
names the backend ("Parallel Chat API `core`, deep, ~minutes"), and logs to
`paper/logs/decision_log.md`. Scope-affecting findings are routed to
`paper/logs/insights.md`. The skill then hands the result to
`literature-review` for screening. If the call exceeds the rate ceiling it
retries once after a brief wait; on a hard failure it reports the error and
offers the parallel-cli fallback. No key is ever persisted.

# research-lookup — Backend Routing Reference

Adapted from the upstream `research-lookup` skill (K-Dense-AI/scientific-agent-skills,
MIT). This document captures the backend selection logic, command patterns, and
citation-ranking tables used by `research-lookup`. It is reference material for the
skill's Workflow step; it does not change the workspace contract in `SKILL.md`.

All backends require **network access** and **user-provided credentials**
(`PARALLEL_API_KEY`, `OPENROUTER_API_KEY`). Never hardcode, log, or persist a key;
treat any encountered credential as `<user-provided-key>`.

## Backends

| Backend | Tool / Model | Latency | Env var | Use for |
|---|---|---|---|---|
| **parallel-cli search** (default) | `parallel-cli search` | 2–10 s | `PARALLEL_API_KEY` | General web search, market/technical data, fast lookups |
| **Parallel Chat API** (deep) | `core` model, OpenAI-SDK-compatible endpoint `https://api.parallel.ai` | 60 s–5 min | `PARALLEL_API_KEY` (same) | Explicit deep/exhaustive multi-source synthesis |
| **Perplexity sonar-pro-search** (academic) | `perplexity/sonar-pro-search` via OpenRouter | 5–15 s | `OPENROUTER_API_KEY` | Academic paper searches, citations, DOIs |

## Routing Logic

```
Query arrives
    |
    +-- Academic keywords? (papers, DOI, journal, peer-reviewed, cite,
    |       systematic review, meta-analysis, seminal, foundational ...)
    |       YES --> Perplexity sonar-pro-search (academic mode)
    |
    +-- Explicit deep request? ("deep research", "exhaustive", "comprehensive")
    |       YES --> Parallel Chat API (core model, 60s-5min)
    |
    +-- Everything else (general research, market data, technical info,
            analysis, fact-checking, current events)
            --> parallel-cli search (fast, default)
```

Manual override: `python scripts/research_lookup.py "<query>"
--force-backend parallel|perplexity`.

## parallel-cli search (DEFAULT)

Fast, cost-effective web search with optional academic source prioritization.
For scientific/technical queries run **two** searches and merge, leading with
academic sources.

```bash
# 1. Academic-focused search
parallel-cli search "your query" -q "kw1" -q "kw2" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,\
semanticscholar.org,biorxiv.org,medrxiv.org,ncbi.nlm.nih.gov,nature.com,\
science.org,ieee.org,acm.org,springer.com,wiley.com,cell.com,pnas.org,nih.gov" \
  -o paper/refs/research_<topic>-academic.json

# 2. General search (catches non-academic sources)
parallel-cli search "your query" -q "kw1" -q "kw2" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o paper/refs/research_<topic>-general.json
```

Useful flags: `--after-date YYYY-MM-DD` (time-sensitive), `--include-domains`
(restrict to specific sources), `--max-results`, `--excerpt-max-chars-total`.

Output JSON per result: `title`, `url`, `publish_date`, `excerpts`.

## Perplexity sonar-pro-search (academic)

Prioritizes scholarly databases and peer-reviewed sources. Use when the query
asks for papers, citations, or DOIs. Response includes 5–8 high-quality
citations with authors, titles, journals, years, DOIs, citation counts, and
venue-tier indicators.

## Parallel Chat API (deep)

OpenAI-SDK-compatible. Model `core`. Returns markdown text with inline citations
plus a research-basis block with URLs, reasoning, and confidence levels. Rate
limit ~300 req/min. Use **only** when the user explicitly asks for deep,
exhaustive, or comprehensive synthesis.

## Paper Quality and Popularity Prioritization

When searching for papers, **always** prefer high-quality, influential work. Note
tier/classification only; final inclusion decisions belong to `literature-review`.

### Citation-Based Ranking

| Paper Age | Citation Threshold | Classification |
|-----------|-------------------|----------------|
| 0–3 years | 20+ citations | Noteworthy |
| 0–3 years | 100+ citations | Highly Influential |
| 3–7 years | 100+ citations | Significant |
| 3–7 years | 500+ citations | Landmark Paper |
| 7+ years | 500+ citations | Seminal Work |
| 7+ years | 1000+ citations | Foundational |

### Venue Quality Tiers

- **Tier 1 — Premier** (always prefer): Nature, Science, Cell, PNAS; NEJM,
  Lancet, JAMA, BMJ; Nature Medicine, Nature Biotechnology, Nature Methods;
  NeurIPS, ICML, ICLR, ACL, CVPR.
- **Tier 2 — High-impact specialized**: journals with Impact Factor > 10; top
  subfield conferences (EMNLP, NAACL, ECCV, MICCAI).
- **Tier 3 — Respected specialized**: journals with Impact Factor 5–10.

## Save Targets (mapped to paper/refs/)

| Backend | Save target | Filename pattern |
|---|---|---|
| parallel-cli JSON (default) | `paper/refs/` | `research_<topic>.json` / `research_<topic>-academic.json` |
| Parallel deep research | `paper/refs/` | `research_<topic>.md` |
| Perplexity (academic) | `paper/refs/` | `papers_<topic>.md` |
| Batch queries | `paper/refs/` | `batch_research_<topic>.md` |

Saved files MUST preserve all citations, source URLs, and DOIs. Always append a
one-line provenance record to `paper/logs/decision_log.md`.

## Complementary Tools

| Task | Tool |
|---|---|
| General/academic web search (fast) | `parallel-cli search` (this skill) |
| Deep multi-source synthesis | this skill via Parallel Chat API |
| Academic paper search | this skill via Perplexity |
| Scholarly-database record fetches (PubMed, arXiv, OpenAlex, ...) | `paper-lookup` |
| Google Scholar / PubMed structured search, DOI→BibTeX | `citation-management` |
| URL content extraction | `parallel-cli extract` (parallel-web) |
| Thematic synthesis, screening | `literature-review` |

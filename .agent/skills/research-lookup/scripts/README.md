# research-lookup/scripts

Backend driver scripts ported (adapted) from K-Dense-AI/scientific-agent-skills
v2.53.0 (MIT). These are convenience drivers for the `research-lookup` skill's
two non-default backends (Parallel Chat API and Perplexity via OpenRouter). The
default backend, `parallel-cli search`, is invoked directly as a shell command
and has no script here.

These scripts are **optional**: the skill is fully usable by calling
`parallel-cli search` directly and only invoking these drivers when the Parallel
Chat API or Perplexity backends are required.

## Files

### `research_lookup.py`

- **Purpose**: Routes a research query to the Parallel Chat API (`core` model,
  deep synthesis) or Perplexity `sonar-pro-search` (academic), with automatic
  keyword-based routing and `--force-backend` override. Mirrors the routing logic
  in `references/backends.md`.
- **Inputs**: query string (positional) or `--batch "q1" "q2" ...`; optional
  `--force-backend {parallel,perplexity}`; optional `-o <path>` output file.
- **Outputs**: markdown research report with a `Sources (N):` block and an
  `Additional References (N):` block carrying DOIs; `--json` emits structured
  citation objects (`url`, `title`, `date`, `snippet`, `doi`, `type`).
- **Network**: YES. Live calls to `https://api.parallel.ai` (OpenAI-SDK-compatible)
  and `https://openrouter.ai/api/v1`. Cannot run offline.
- **Writes**: only the file given via `-o` (the skill contract directs these to
  `paper/refs/research_*.md` or `paper/refs/papers_*.md`); stdout otherwise.
  Does not touch any other workspace file.
- **Credentials**: reads `PARALLEL_API_KEY` and `OPENROUTER_API_KEY` from the
  environment only. Never hardcodes, echoes, or persists a key. The user must
  provide these out of band; treat any encountered key as `<user-provided-key>`.

### `lookup.py`

- **Purpose**: Thin Claude-Code-facing wrapper around `research_lookup.py` that
  formats the result for display (query, model, citations, sources).
- **Inputs**: query string (positional).
- **Outputs**: formatted research result to stdout.
- **Network**: YES (delegates to `research_lookup.py`).
- **Writes**: nothing to the workspace; stdout only.
- **Credentials**: same as `research_lookup.py` (reads env vars only).

## Quick start

```bash
# Default backend is parallel-cli search (invoke directly, no script here):
parallel-cli search "Recent advances in CRISPR gene editing 2025" \
  -q "CRISPR" -q "gene editing" --json --max-results 10 \
  -o paper/refs/research_crispr_advances.json

# Force Perplexity academic search via the driver:
python scripts/research_lookup.py "Find papers on transformer attention in NeurIPS 2024" \
  --force-backend perplexity -o paper/refs/papers_transformer_attention.md

# Force Parallel deep research:
python scripts/research_lookup.py "Deep research on quantum error correction" \
  --force-backend parallel -o paper/refs/research_quantum_ec.md
```

## Not copied from upstream

The upstream skill also shipped `generate_schematic.py` and
`generate_schematic_ai.py`, which generate scientific diagrams via image APIs.
Those belong to the `scientific-schematics` skill, not research-lookup, and were
intentionally not copied. The upstream `examples.py` demo file was replaced by
`examples/prompts.md` (workspace-grounded invocation scenarios).

# BGPT MCP server setup and pricing

BGPT is a **remote MCP server** that exposes a `search_papers` tool over a
curated database of scientific papers built from structured experimental data
extracted from full-text studies. It returns 25+ fields per paper, including
methods, quantitative results, sample sizes, quality/evidence scores, and
conclusions.

This file is reference documentation only. The skill never installs, starts, or
configures MCP itself — the user must add the server to their host's MCP
configuration before any call can succeed.

## MCP endpoint

- SSE endpoint: `https://bgpt.pro/mcp/sse`
- Web / pricing: `https://bgpt.pro/mcp`
- Open-source client wrapper (npm): `https://github.com/connerlambden/bgpt-mcp`

## Configure in Claude Desktop / Claude Code

Add to the host MCP configuration:

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

### npm alternative

```bash
npx bgpt-mcp
```

After configuration the host exposes the `search_papers` tool. The skill calls
it through the agent's MCP interface, **not** via Bash.

## Pricing (verify at bgpt.pro before relying on numbers)

- **Free tier**: ~50 searches per network, no API key required.
- **Paid**: per-result pricing (upstream quotes ~$0.01 per result) with a key
  obtained from `bgpt.pro/mcp`.

Treat these figures as advisory; confirm current pricing on the BGPT site.

## Credentials

- The optional `BGPT_API_KEY` enables paid results.
- The user supplies it out of band (e.g. exported in their shell environment).
- This skill never generates, stores, echoes, or commits a key. Any key string
  found in inputs or logs is replaced with `<user-provided-key>` before any
  `paper/` file is written.

## Fields returned per paper

Representative fields (25+): title, authors, journal, year, DOI, methods
(techniques, models, protocols), quantitative results, sample sizes, effect
sizes where available, quality / evidence-grading scores, conclusions and
implications. Confirm the exact field set against a live query.

# Infographics scripts (local copy)

These scripts are ported (adapted) from
`K-Dense-AI/scientific-agent-skills` v2.53.0 (MIT); see
`.agent/references/scientific_agent_skills_source.md` and the repository
`NOTICE.md`.

They are **Tier C (external)**: they call external model APIs over the
network and require a user-provided credential. They never read or store
secrets themselves — the caller is responsible for providing the key.

## generate_infographic_ai.py (primary)

- **Purpose:** Generate a publication-quality infographic from a natural-language
  prompt via an OpenRouter image model, then have an OpenRouter review model score
  it against a document-type threshold, iterating only when below threshold.
  Optional `--research` mode gathers supporting facts via Perplexity Sonar Pro.
- **Inputs:**
  - `PROMPT` (positional) — content description.
  - `-o/--output` — output PNG path.
  - `-t/--type`, `-s/--style`, `-p/--palette`, `--doc-type`, `--iterations`,
    `--research`, `--api-key` — see `--list-options`.
- **Outputs:**
  - Versioned PNG images plus a `*_review.json` review log (scores, critiques,
    early-stop info) next to the output path.
  - When `--research` is set, a `*_research.json` of raw research data/sources.
- **Network:** YES. Calls `https://openrouter.ai/api/v1` for image generation,
  quality review, and (optionally) web research. Outbound HTTPS is required.
- **Credentials:** requires `OPENROUTER_API_KEY` (env var) or `--api-key`.
  The user must provide it out of band; never hardcode, echo, log, or store a key.
- **Writes:** only to the path given by `-o/--output` and its sibling JSON
  files. It does not touch any other workspace file.

## generate_infographic.py (thin wrapper / reference CLI)

- **Purpose:** Lightweight command-line front-end / options catalogue. Delegates
  to the AI generation flow; useful for `--list-options` and option discovery.
- **Inputs/Outputs/Network/Credentials:** same as above.
- **Writes:** only to the `-o/--output` path (and sibling review JSON).

## Notes

- These scripts are vendored verbatim-with-minor-adaptation. Do not edit them
  to add credentials. If a key appears in any log, treat it as
  `<user-provided-key>` and scrub it.
- Figures produced here for the paper are illustrative / communication assets;
  route quantitative evidence through `scientific-visualization` or
  `scientific-schematics` instead.

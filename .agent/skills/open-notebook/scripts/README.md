# open-notebook/scripts

Lightweight REST API client examples for the self-hosted **Open Notebook**
service (an open-source alternative to NotebookLM). These are thin `requests`-
based clients that demonstrate how to talk to a separately-deployed Open
Notebook server from outside this repo. They are NOT part of the Auto-01
research workflow and contain no science, models, or data.

## Files

| File | Purpose |
|------|---------|
| `notebook_management.py` | Create / list / update / delete notebooks via the REST API. |
| `source_ingestion.py` | Ingest URLs, files, and raw text as sources; poll processing status. |
| `chat_interaction.py` | Build context and run context-aware chat sessions against a notebook. |

## Purpose

Illustrate how an operator would drive an external Open Notebook deployment
(e.g. to build a literature corpus or generate podcasts) from a script. Treat
these as reference examples, not as steps inside the Auto-01 pipeline.

## Inputs

- `OPEN_NOTEBOOK_URL` (env var) — base URL of the running server, e.g.
  `http://localhost:5055`. **User must provide; never hardcode or store.**
- `OPEN_NOTEBOOK_PASSWORD` (env var, optional) — only if the server has UI
  auth enabled. **User must provide; never hardcode or store.**
- A running Open Notebook deployment (Docker Compose) reachable at that URL,
  with at least one AI provider configured on the server side.
- A `notebook_id` (and source/episode/profile IDs) returned by earlier calls.

## Outputs

- These scripts only print JSON responses to stdout. They write **nothing**
  into the Auto-01 `paper/` workspace. Anything you want persisted (notes,
  summaries, podcast audio) must be deliberately copied into
  `paper/refs/`, `paper/experiments/`, or `paper/assets/` by you, with
  provenance recorded in `paper/logs/decision_log.md`.

## Network

- Each script makes outbound HTTPS/HTTP calls to the `OPEN_NOTEBOOK_URL`
  server and, indirectly, to whichever AI provider the server is configured
  to use (OpenAI, Anthropic, Ollama, etc.). No inbound ports are opened.

## Writes

- None inside this repo (stdout only). The server-side state (notebooks,
  sources, notes) lives in the external Open Notebook Docker volumes.

## Safety

- Never embed real API keys, the `OPEN_NOTEBOOK_ENCRYPTION_KEY`, or
  `OPEN_NOTEBOOK_PASSWORD` in these files. All placeholders of the form
  `sk-...` have been scrubbed to `<user-provided-key>`.
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.

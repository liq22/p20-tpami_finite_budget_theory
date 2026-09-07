---
name: open-notebook
description: Drive a self-hosted Open Notebook server to ingest multi-format sources, generate AI notes/summaries, run context-aware cited chat, and build podcasts feeding paper/refs/. Implementation skill - prefer literature-review or scientific-writing as primary. Do not use for drafting, plotting, statistics, ML training, or without a deployed server.
---

# open-notebook

## Purpose

Provide reference material and thin REST-client recipes for **Open Notebook**,
an open-source, self-hosted alternative to Google NotebookLM
(https://github.com/lfnovo/open-notebook, MIT). Open Notebook lets a researcher
organize a corpus of sources, run context-aware chat over them, generate
AI-powered notes and summaries, search with full-text + vector retrieval, and
produce multi-speaker podcasts — all on infrastructure the user controls, with
choice of 16+ AI providers (OpenAI, Anthropic, Google, Ollama, Groq, Mistral,
...).

In Auto-01-tiny-research this is a **TIER B tool / implementation skill**: it
does not own a research-planning stage. It exists to help an operator build and
query an external notebook corpus whose distilled outputs (curated references,
summaries, insight notes) are then deliberately moved into this repo's
`paper/refs/` and `paper/experiments/` artifacts. The relevant planning skills
— `03-literature-deep-research` / `literature-review` for corpus building,
`scientific-writing` for drafting, `scientific-visualization` for figures,
`scikit-learn` / `pytorch-lightning` / `pymc` for modeling — remain primary and
should be preferred wherever they apply.

## Use When

- You are assembling a large multi-format literature corpus (PDFs, arXiv URLs,
  audio/video talks, web pages, Office docs) that is too heterogeneous for
  `paper/refs/references.bib` alone and you want a searchable, self-hosted
  knowledge base before distilling entries into `paper/refs/`.
- You need AI-generated summaries or method extractions across many sources to
  populate `paper/experiments/insights.md` or seed
  `paper/refs/reading_matrix.md`, and you want the AI to cite which source each
  claim came from.
- A reviewer (`paper/reviews/response_to_reviewers.md`) asks a synthesis
  question ("what does the corpus say about X?") best answered by
  context-aware chat over the full source set, with citations.
- You want a multi-speaker podcast or audio brief of the research for
  dissemination / accessibility, generated from the notebook corpus.

Do not use this skill for: drafting the paper itself (use `scientific-writing`
/ `08-markdown-draft` / `09-tex-freeze-formalize`), producing figures or tables
(use `scientific-visualization` / `matplotlib` / `seaborn`), running classical
ML (use `scikit-learn`), deep-learning training engineering (use
`pytorch-lightning`), or Bayesian modeling (use `pymc`). It is also not a
replacement for this repo's own reference management (`citation-management`,
`paper/refs/references.bib`) — Open Notebook is an auxiliary external corpus,
not the system of record. Do not use it if no Open Notebook server is, or will
be, deployed by the user.

## Required Inputs

- A running **Open Notebook** deployment the user has stood up (Docker
  Compose; frontend `:8502`, REST API `:5055`). The user is responsible for
  deploying and operating it; this skill does not host or install it.
- `OPEN_NOTEBOOK_URL` — base URL of the server. **User must provide; never
  hardcode or store.**
- `OPEN_NOTEBOOK_PASSWORD` — only if the server has UI auth enabled. **User
  must provide; never hardcode or store.**
- `OPEN_NOTEBOOK_ENCRYPTION_KEY` — server-side secret for encrypting stored
  provider credentials. **User must provide; never hardcode or store**, and
  never commit it to this repo.
- At least one AI provider configured **on the server side** (e.g.
  `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or local Ollama). These live in the
  Open Notebook deployment, not in this repo; **user must provide; never
  hardcode or store.**
- A target mapping: which notebook/note corresponds to which Auto-01 artifact
  (e.g. "notebook N → `paper/refs/` curation", "summary S →
  `paper/experiments/insights.md`), so anything imported back has provenance.
- Optional: existing entries in `paper/refs/references.bib` /
  `paper/refs/reading_matrix.md` to reconcile against, so the notebook corpus
  and the repo's system of record stay consistent.

## Workflow

1. Confirm the user has a deployed, reachable Open Notebook server and has
   provided `OPEN_NOTEBOOK_URL` (+ optional password). If not deployed and the
   user does not intend to deploy it, stop (see Stop With) — this skill is
   useless without the external service.
2. Create or reuse a notebook scoped to the research question; record the
   notebook name/ID and its intended Auto-01 mapping in
   `paper/logs/decision_log.md` so the external corpus is traceable.
3. Ingest sources (URLs, PDFs, audio/video, text) via the `/api/sources`
   endpoints; see `references/api_reference.md` and
   `scripts/source_ingestion.py`. Prefer sources already cited in
   `paper/refs/references.bib` so the notebook mirrors the repo, not a
   divergent set.
4. Process sources (full-text + vector index) and use `/api/search` (vector or
   full-text) and `/api/search/ask/simple` to answer synthesis questions with
   citations; capture non-trivial findings into
   `paper/experiments/insights.md` and open methodological questions into
   `paper/logs/open_questions.md`.
5. Generate AI notes / summaries via `/api/notes` or custom
   `/api/transformations` (e.g. an "extract_methods" transformation); when a
   note is promoted into the paper, copy its content into the right
   `paper/` artifact and record the source notebook + source ID in
   `paper/logs/decision_log.md`.
6. (Optional) Generate a multi-speaker podcast via `/api/podcasts/generate`
   for dissemination; if retained, store audio under
   `paper/assets/` (a designated media subdir) and note provenance.
7. Reconcile: any reference added to the notebook that should be in the paper
   must also be entered into `paper/refs/references.bib` via the
   `citation-management` skill — the notebook is not the system of record.
8. Record what was imported, from which notebook/source, and any AI provider
   caveats (model id, date) in `paper/experiments/reproducibility.md` so a
   reader can tell which insights came from the external corpus.

## Output Contract

- A decision-log entry in `paper/logs/decision_log.md` naming the notebook,
  its purpose, and the Auto-01 artifact(s) it feeds.
- Distilled content moved into the appropriate `paper/` artifact: curated
  entries into `paper/refs/references.bib` / `paper/refs/reading_matrix.md`,
  synthesis findings into `paper/experiments/insights.md`, method extractions
  into `paper/experiments/` or `paper/draft/`, reviewer-question answers into
  `paper/reviews/response_to_reviewers.md`.
- A reproducibility note in `paper/experiments/reproducibility.md` recording
  the Open Notebook version, the AI provider/model used, and the date of any
  AI-generated note promoted into the paper.
- No change to `paper/tex/` (formal draft is owned by `09-tex-freeze-formalize`)
  and no change to `paper/submission/` from this skill.
- No secrets, `.env`, credentials, or `OPEN_NOTEBOOK_ENCRYPTION_KEY` written
  anywhere in the repo.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only open-notebook`
- `python src/S03_Scripts/validate_project.py`
- Confirm no `OPEN_NOTEBOOK_ENCRYPTION_KEY`, `OPEN_NOTEBOOK_PASSWORD`, or any
  provider API key (e.g. `OPENAI_API_KEY`) value is committed — only env-var
  *names* may appear in docs (grep the skill dir for `sk-`, `gh[pousr]_`,
  `AKIA`, `BEGIN ... PRIVATE KEY`; must be absent).
- Confirm every AI-generated note promoted into `paper/` has a matching
  provenance entry in `paper/logs/decision_log.md` (notebook ID + source ID +
  model + date).
- Confirm references added via the notebook also exist in
  `paper/refs/references.bib` (the notebook is auxiliary, not canonical).
- Confirm nothing under `paper/tex/` or `paper/submission/` was written by
  this skill.

## Boundaries

- Do not draft the paper, produce figures/tables, run ML training, or do
  statistics here — defer to the primary planning skills (`scientific-writing`,
  `scientific-visualization`, `scikit-learn`, `pytorch-lightning`, `pymc`).
- Do not treat Open Notebook as the system of record for references; canonical
  citations live in `paper/refs/references.bib` under `citation-management`.
- Do not write outputs anywhere except the designated `paper/refs/`,
  `paper/experiments/`, `paper/assets/`, and `paper/logs/` artifacts; never
  into `paper/tex/`, `paper/submission/`, or `paper/checklists/`.
- Do not embed real secrets (`OPEN_NOTEBOOK_ENCRYPTION_KEY`, provider keys,
  passwords) in any file; all examples must use `<user-provided-key>`.
- Do not ship heavy ML training/inference scripts; the bundled `scripts/` are
  thin REST clients only (see `scripts/README.md`).
- Do not assume the server is deployed; if it is unreachable and the user will
  not deploy it, stop rather than substitute another tool silently.

## Stop With

- No Open Notebook server is deployed/reachable and the user does not intend
  to deploy one — this skill cannot function without the external service.
- Required connection inputs (`OPEN_NOTEBOOK_URL`, and password if auth is on)
  are not provided by the user; do not guess or hardcode them.
- An AI-generated note cannot be attributed to a concrete source/model/date —
  do not promote un-attributable AI text into the paper; flag it in
  `paper/logs/open_questions.md` instead.
- The notebook corpus and `paper/refs/references.bib` have diverged and the
  user has not decided which is canonical — reconcile before importing.
- The task is actually drafting, plotting, statistics, or modeling — return
  the caller to the relevant primary planning skill instead of improvising.

## References

- API reference: `.agent/skills/open-notebook/references/api_reference.md`
- Configuration (Docker, env vars, providers):
  `.agent/skills/open-notebook/references/configuration.md`
- Architecture: `.agent/skills/open-notebook/references/architecture.md`
- Worked examples: `.agent/skills/open-notebook/references/examples.md`
- REST client scripts (purpose/inputs/outputs/network/writes):
  `.agent/skills/open-notebook/scripts/README.md`
- Invocation scenarios: `.agent/skills/open-notebook/examples/prompts.md`
- Workspace artifacts this skill feeds: `paper/refs/references.bib`,
  `paper/refs/reading_matrix.md`, `paper/experiments/insights.md`,
  `paper/experiments/reproducibility.md`,
  `paper/reviews/response_to_reviewers.md`, `paper/logs/decision_log.md`,
  `paper/logs/open_questions.md`, `paper/assets/`.
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream project: https://github.com/lfnovo/open-notebook (MIT).

---
name: pptx-posters
description: Build an HTML/CSS research poster exportable to PDF/PPTX when the user explicitly requests PowerPoint format, assembling AI poster visuals via a user-provided OPENROUTER_API_KEY and network. Do not use for standard or LaTeX posters, data figures, quantitative plots, or paper evidence — use latex-posters or scientific-visualization instead.
---

# PPTX Research Posters (HTML-Based)

## Purpose

Produce a single research poster for the paper as an HTML/CSS document that can be
previewed in a browser and exported to PDF (and, when explicitly required, converted to
PPTX). The skill is the **non-LaTeX** poster channel: it composes a poster from
AI-generated visual elements (hero banner, simplified flowcharts, summary cards) plus
minimal supporting text, then hands the result to the browser print path or a converter
for final output. It is for outreach and presentation, not evidence — every figure it
emits is illustrative and never binds to a claim/evidence row in
`paper/experiments/evidence_matrix.md`.

Use this skill **only when the user explicitly asks for PPTX / PowerPoint poster
format**. For standard research or conference posters (where LaTeX is available and no
PowerPoint editability is required), use `latex-posters`, which gives better typographic
control and is the default for academic venues.

## Use When

- The user explicitly requests a "PPTX poster", "PowerPoint poster", or "PPT poster",
  or needs to edit the poster in PowerPoint after creation.
- The user specifically asks for an HTML-based poster, or LaTeX is unavailable and a
  non-LaTeX solution is requested.

Do **not** use this skill for:

- A bare "poster" / "research poster" / "conference poster" request with no format
  specified — use `latex-posters`.
- Any mention of LaTeX, tikzposter, beamerposter, or baposter — use `latex-posters`.
- Data figures, quantitative plots, exact-geometry model diagrams, methodology/
  architecture/pathway/circuit diagrams, or any figure bound to a claim/evidence row —
  use `scientific-visualization` (matplotlib/seaborn) or `scientific-schematics`.

## Required Inputs

- Explicit confirmation that **PPTX/PowerPoint poster format** is required (not a generic
  poster request).
- Poster dimensions and orientation: 36×48 inches (default) or A0; portrait (default) or
  landscape. State this before composing.
- A content outline distilled to 1-3 core messages and 3-5 planned visuals, with total
  text held to 300-800 words (50-100 words per section, max 5-6 sections).
- Source material from the workspace: `paper/draft/` markdown drafts (pre-freeze) or
  `paper/tex/` (post-freeze), `paper/experiments/statistics.md` for headline numbers to
  feature, and `paper/refs/target_journal.md` to confirm the venue's poster/format rules.
- An output destination under `paper/assets/figures/` for each generated visual, with an
  `outreach_` / `poster_` prefix to mark the asset as illustrative, non-evidence.

**External credentials:** generating the poster's AI visuals requires an OpenRouter API
key. `OPENROUTER_API_KEY` must be provided by the user out of band (environment variable
or a `.env` the user owns); **never hardcode, echo, log, or store a key, token, or
credential** in this skill, its scripts, or any workspace file. Treat any encountered key
string as `<user-provided-key>`. Network access to `https://openrouter.ai` is required
for the visual-generation step only; the HTML composition, browser preview, and PDF
export themselves do not need network.

## Workflow

1. **Confirm scope.** Verify the user explicitly wants PPTX/PowerPoint poster format and
   that the venue does not classify the result as a numbered figure (check
   `paper/refs/target_journal.md`). If a generic or LaTeX poster was requested, stop and
   route to `latex-posters`.
2. **Plan content and visuals.** Draft 1-3 core messages and a plan for 3-5 ultra-simple
   visuals (hero, intro icons, methods flowchart, results chart, conclusions cards).
   Hold total text to 300-800 words and max 5-6 sections.
3. **Generate poster visuals (AI-powered).** For each planned graphic, run
   `scripts/generate_schematic.py` with `--doc-type poster` and a prompt that enforces
   strict poster readability — 3-4 elements max, <=10 words of text, 50%+ white space,
   giant bold fonts (80pt+ for labels, 120pt+ for key numbers), thick lines, high
   contrast. Write each PNG to `paper/assets/figures/` with an illustrative prefix:
   ```bash
   python .agent/skills/pptx-posters/scripts/generate_schematic.py \
     "POSTER FORMAT for A0. SIMPLE 4-box flowchart: STEP1 -> STEP2 -> STEP3 -> STEP4. \
      GIANT labels (100pt+). Thick arrows. 50% white space. NO sub-steps." \
     -o paper/assets/figures/poster_methods_flow.png --doc-type poster
   ```
   Never feed a data figure as input here; this skill must not edit evidence.
4. **Assemble the HTML poster.** Copy `assets/poster_html_template.html` into the
   workspace, replace the placeholder title/authors with the paper's, insert the generated
   visuals, add minimal supporting text, and update the footer references. Keep the
   three-column block layout; do not exceed the fixed poster dimensions.
5. **Review against the quality checklist.** Run the pre-generation and post-generation
   reviews from `assets/poster_quality_checklist.md` on every visual: at 25% zoom, all
   text must be readable, elements <=4, white space >=50%, one message per graphic.
   Confirm no content is cut off at any edge.
6. **Export.** Open the HTML in Chrome/Firefox and print to PDF (paper size matching the
   poster dimensions, margins removed, background graphics enabled). If PPTX is
   specifically required, convert the PDF via LibreOffice
   (`libreoffice --headless --convert-to pptx`) or assemble directly with `python-pptx`.
   The export checklist is **upstream-incomplete** — the user must manually verify the
   final PDF/PPTX (see Boundaries).
7. **Record.** Log the choice of format, models, illustrative-only status, and any export
   caveat in `paper/logs/decision_log.md`; note reusable prompt patterns in
   `paper/logs/insights.md`.

## Output Contract

- One HTML poster file in the workspace (e.g. `poster.html`), plus the generated visual
  PNGs under `paper/assets/figures/` with illustrative prefixes.
- Optionally one exported PDF and, if explicitly requested, one PPTX, in `paper/submission/`
  or an outreach folder — never promoted into `paper/tex/` unless a human does so via
  another skill.
- No claim/evidence row is created or modified — this skill does not emit evidence.
- A decision-log entry in `paper/logs/decision_log.md` recording format choice, model(s),
  illustrative-only status, and the user-verified export.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only pptx-posters`
- `python src/S03_Scripts/validate_project.py`
- Manual: confirm no `OPENROUTER_API_KEY` value appears in any committed file; confirm
  every output visual is illustrative and not referenced as evidence in
  `paper/experiments/evidence_matrix.md`; confirm at 25% zoom that no poster text is cut
  off and all graphics meet the simplicity rules.

## Boundaries

- **Explicit-format only.** Use only when the user requests PPTX/PowerPoint poster
  format. For standard or conference posters, use `latex-posters`.
- **External service.** The AI visual-generation step depends on network access to
  `https://openrouter.ai` and a user-provided `OPENROUTER_API_KEY`. The user must supply
  the credential; this skill must not invent, hardcode, or persist secrets.
- **Illustrative/non-evidence.** Never produce data figures, quantitative plots,
  exact-geometry model diagrams, methodology/architecture/pathway/circuit diagrams, or
  any paper evidence figure. Route those to `scientific-visualization` or
  `scientific-schematics`. Generated imagery is AI-produced — flag this where disclosure
  is expected.
- **Incomplete export checklist (upstream issue).** The bundled
  `assets/poster_quality_checklist.md` does not fully cover the PDF→PPTX conversion path
  (LibreOffice and `python-pptx` behave differently and can drop background graphics,
  fonts, or vector fidelity). The user **must manually verify** the final exported PDF
  and PPTX edge-to-edge before any submission or print.
- **Content density.** Enforce 300-800 words total and max 5-6 sections; reject posters
  that overflow their fixed dimensions.

## Stop With

- A request for a generic, research, or conference poster, or any LaTeX poster —
  re-route to `latex-posters`.
- A request to generate a data figure, plot, or any diagram bound to evidence — re-route
  to `scientific-visualization` or `scientific-schematics`.
- No user-provided `OPENROUTER_API_KEY` and no network for the visual step — ask the user
  to supply the credential; never fabricate or store one. (HTML composition and PDF
  export can still proceed with already-generated or user-supplied visuals.)
- A poster that would overflow its dimensions or whose visuals fail the 25%-zoom
  readability review — regenerate or cut content before exporting.

## References

- Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT); see NOTICE.md
  and `.agent/references/scientific_agent_skills_source.md`.
- Workspace: `paper/assets/figures/` (illustrative poster visuals), `paper/draft/` and
  `paper/tex/` (source content), `paper/experiments/statistics.md` (headline numbers),
  `paper/experiments/evidence_matrix.md` (the binding this skill must NOT produce),
  `paper/refs/target_journal.md` (venue/format rules), `paper/submission/` (exported
  PDF/PPTX), `paper/logs/decision_log.md` and `paper/logs/insights.md` (records).
- Bundled assets: `assets/poster_html_template.html` (36×48-inch three-column template),
  `assets/poster_quality_checklist.md` (pre/post-generation review — incomplete for the
  PPTX path; see Boundaries), `references/poster_content_guide.md`,
  `references/poster_design_principles.md`, `references/poster_layout_design.md`.
- Bundled runner: `scripts/generate_schematic.py` + `scripts/generate_schematic_ai.py`
  (see `scripts/README.md` for inputs/outputs/network/writes); worked scenarios in
  `examples/prompts.md`.

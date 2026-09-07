# pptx-posters — example invocations

Realistic single-paper scenarios for an HTML/CSS research poster that is exported to PDF
and (when explicitly required) converted to PPTX. These scenarios are for **explicit
PPTX/PowerPoint poster requests only**; for standard or conference posters use
`latex-posters`, and for data figures use `scientific-visualization` or
`scientific-schematics`.

Inputs the user provides out of band:
- `OPENROUTER_API_KEY` exported in the shell or set in a `.env` (never committed).
- Explicit confirmation that PPTX/PowerPoint poster format is required.

## Scenario 1: Conference PPTX poster the author must edit in PowerPoint

The paper (a methods paper on a lightweight forecasting model) has been accepted to a
venue whose poster session requires PowerPoint deliverables, so the author explicitly
asks for a PPTX poster rather than the default LaTeX one. The draft is post-freeze in
`paper/tex/`; headline numbers live in `paper/experiments/statistics.md`.

Step 1 — generate the ultra-simple poster visuals (each prompt enforces 3-4 elements,
<=10 words, 50%+ white space, giant fonts):

```bash
mkdir -p paper/assets/figures

# Hero banner — ONE iconic visual, minimal text
python .agent/skills/pptx-posters/scripts/generate_schematic.py \
  "POSTER FORMAT for A0. Hero banner: 'LIGHTWEIGHT FORECASTING' in HUGE text (120pt+). \
   Dark blue gradient background. ONE iconic clock-and-trend visual. Minimal text. \
   Readable from 15 feet." \
  -o paper/assets/figures/poster_hero.png --doc-type poster

# Methods — 4-step flowchart only
python .agent/skills/pptx-posters/scripts/generate_schematic.py \
  "POSTER FORMAT for A0. SIMPLE 4-box flowchart: ENCODE -> ATTEND -> DECODE -> OUTPUT. \
   GIANT labels (100pt+). Thick arrows (10px). 50% white space. NO sub-steps." \
  -o paper/assets/figures/poster_methods_flow.png --doc-type poster

# Results — 3 bars only, no axis, no legend
python .agent/skills/pptx-posters/scripts/generate_schematic.py \
  "POSTER FORMAT for A0. SIMPLE bar chart with ONLY 3 bars: BASELINE 70%, EXISTING 85%, \
   OURS 95%. GIANT percentages ON bars (120pt+). NO axis, NO legend. 50% white space." \
  -o paper/assets/figures/poster_results.png --doc-type poster
```

Step 2 — assemble the HTML poster:

```bash
cp .agent/skills/pptx-posters/assets/poster_html_template.html poster.html
# Replace placeholder title/authors, insert the three visuals, add <=800 words of
# supporting text, update footer references. Keep the three-column block layout.
```

Step 3 — export (browser print to PDF, then convert to PPTX since PowerPoint was
explicitly required):

```bash
# PDF via Chrome headless (paper size = poster dimensions, no margins, bg graphics on)
google-chrome --headless --print-to-pdf=poster.pdf --print-to-pdf-no-header --no-margins poster.html

# PPTX (explicitly requested) via LibreOffice
libreoffice --headless --convert-to pptx --outdir paper/submission poster.pdf
```

After export:
- Manually verify the PDF and PPTX edge-to-edge (the bundled checklist is incomplete for
  the PPTX path — confirm no background graphics, fonts, or vectors were dropped).
- Record format choice, models, and illustrative-only status in
  `paper/logs/decision_log.md`; confirm in `paper/checklists/` that the visuals are
  illustrative and not bound to `paper/experiments/evidence_matrix.md`.

## Scenario 2: Group-meeting HTML poster for an internal talk

The author wants an in-lab poster for an upcoming group meeting and explicitly prefers an
HTML/PPTX workflow so a collaborator can tweak it in PowerPoint. No PPTX export is needed
this time — a PDF for the shared screen is enough. The draft is still pre-freeze in
`paper/draft/`.

```bash
# Conclusions cards — EXACTLY 3 key findings
python .agent/skills/pptx-posters/scripts/generate_schematic.py \
  "POSTER FORMAT for A0. EXACTLY 3 cards: '95%' (150pt) 'ACCURACY' (60pt), \
   '2X' (150pt) 'FASTER' (60pt), checkmark 'READY' (60pt). 50% white space. NO other text." \
  -o paper/assets/figures/poster_conclusions.png --doc-type poster

# Intro — 3 icons only
python .agent/skills/pptx-posters/scripts/generate_schematic.py \
  "POSTER FORMAT for A0. SIMPLE visual with ONLY 3 icons: DATA -> MODEL -> INSIGHT. \
   ONE-word labels (80pt+). 50% white space. Readable from 8 feet." \
  -o paper/assets/figures/poster_intro.png --doc-type poster
```

Then assemble `poster.html` from the template, review every visual at 25% zoom (all text
readable, <=4 elements, >=50% white space, nothing cut off at the edges), and print to
PDF in the browser. No PPTX conversion this time. Log the illustrative-only status in
`paper/logs/decision_log.md` and note any prompt patterns worth reusing in
`paper/logs/insights.md`.

## Scenario 3: Stop and re-route — a generic poster request

A collaborator says "make me a poster for the paper" without naming a format. This skill
must **not** fire: it is explicit-PPTX-only. Route the request to `latex-posters`
instead, which is the default for academic/conference posters and gives better typographic
control. Only come back to `pptx-posters` if the collaborator later insists on PowerPoint
editability or explicitly asks for a PPTX/HTML poster.

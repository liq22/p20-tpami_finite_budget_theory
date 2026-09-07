---
name: latex-posters
description: "Compose one print-ready LaTeX research poster distilling the paper's validated claims and figures. Use for a conference, symposium, or defense poster. Needs a user-installed local LaTeX toolchain; optional AI schematics need a user-provided API key. Do not use for slides (pptx), journal TeX (09-tex-freeze-formalize), or new claims."
---

# latex-posters

## Purpose

Produce one publication-quality research poster as a print-ready PDF for the
single paper tracked by this repo, using the three mainstream LaTeX poster
classes — `beamerposter`, `tikzposter`, or `baposter`. The poster is a
*distillation* of work that already exists in the project workspace: claims and
evidence come from `paper/experiments/`, figures from `paper/assets/figures/`,
and framing from `paper/refs/target_journal.md`. This skill owns layout,
typography, color, overflow control, font embedding, and PDF QA — it does not
invent science.

This is a **TIER C external** skill: it depends on a LaTeX distribution the user
installs locally, and its optional AI-schematic steps call external image/LLM
APIs that the user must authenticate. The skill never fetches toolchains or
credentials itself.

## Use When

- A conference, symposium, thesis defense, or poster session asks for a poster
  and the underlying paper exists as `paper/draft/*.md` or `paper/tex/*.tex`.
- You need to convert the paper's headline result, key figures, and
  claim→evidence rows (`paper/experiments/evidence_matrix.md`,
  `paper/experiments/statistics.md`) into a visual one-page summary.
- A venue specifies an exact physical size (A0, A1, 36×48", 48×72") and
  orientation that the deliverable must match exactly.
- You want to reuse `paper/assets/figures/` and `paper/assets/tables/` panels on
  a poster that mirrors the paper's claim hierarchy.

Do **not** use for: talk/seminar slide decks (use `pptx`); the formal journal
TeX/PDF build (use `09-tex-freeze-formalize`); generating new figures from raw
data (use `matplotlib` / `scientific-visualization`); or producing new claims,
experiments, or analysis.

## Required Inputs

- **Source content**: a `paper/draft/*.md` or `paper/tex/*.tex` file, or an
  explicit outline from the user. Pull every number, claim, and figure
  exclusively from `paper/experiments/evidence_matrix.md`,
  `paper/experiments/statistics.md`, and `paper/assets/`; do not invent science.
- **Venue spec**: target page size (A0 / A1 / 36×48" / other), orientation
  (portrait / landscape), and any margin/bleed rules from the call for papers.
  Record the chosen size in `paper/submission/` notes.
- **Figures**: existing files under `paper/assets/figures/` (vector PDF/SVG
  preferred; raster ≥ 300 DPI at final print size). Reuse rather than regenerating.
- **Local LaTeX toolchain** (user-provided; never installed by this skill):
  `pdflatex` / `xelatex` / `lualatex` plus the packages `beamerposter`,
  `tikzposter`, `baposter`, `qrcode`, `tcolorbox`, `subcaption`. Install via
  `tlmgr install ...` (TeX Live) or MiKTeX's auto-install.
- **Optional AI schematic generation** — the upstream `generate_schematic*.py`
  helpers call external image and LLM APIs (e.g. OpenRouter) and require an API
  key. If used, **the user must provide the credential**; never hardcode or
  store it. Prefer the already-validated figures in `paper/assets/figures/`.

## Workflow

1. **Confirm inputs and venue.** Verify the source draft exists, the page size
   matches the call for papers, and the key figures are present in
   `paper/assets/figures/`. If a required figure is missing, request it — do not
   generate a placeholder claim to fill the gap.
2. **Pick the class.** `beamerposter` for Beamer-familiar / institutional themes;
   `tikzposter` for modern, colorful, TikZ-driven layouts; `baposter` for
   structured multi-column box layouts. Start from `assets/<class>_template.tex`.
3. **Plan content (≤ 6 sections).** Distill to: Title → Introduction → Methods →
   Results (1–2 figures) → Conclusions. Target 300–800 words total, 50–80 words
   per section. Map each panel to a row in `paper/experiments/evidence_matrix.md`.
4. **Prepare figures for poster readability.** Each graphic conveys ONE message:
   ≤ 3–4 elements, ≤ ~10 words baked in, ≥ 50% white space, label fonts ≥ 80pt
   and key-number fonts ≥ 120pt for A0. Simplify or split dense figures from
   `paper/assets/figures/` into separate poster panels rather than shrinking text.
5. **Assemble.** Drop figures into the template with
   `\includegraphics[width=0.85\linewidth]{...}` (never `1.0\linewidth`); set
   generous margins (`margin=10–25mm`, `innermargin`, `colspace`); keep a 10–15%
   header band and 5–10% footer band.
6. **Compile.** `pdflatex poster.tex` (run twice for references); use
   `xelatex`/`lualatex` if the template needs system fonts or Unicode.
7. **Overflow QA (mandatory).** `grep -i 'overfull\|underfull\|badbox' poster.log`
   — treat any `Overfull \hbox/\vbox` as a defect to fix (cut text, shrink figure
   width to `0.8\linewidth`, or split sections), not a warning. Inspect all four
   edges at 100% zoom.
8. **Pre-print QA.** Run `scripts/review_poster.sh poster.pdf` (local: checks
   page size, font embedding via `pdffonts`, page count, file size). Confirm
   `pdfinfo` page size matches the venue spec exactly and all fonts show
   `emb=yes`.
9. **Deliver.** Write the final `poster.pdf` (and a `.tex` source) to
   `paper/submission/poster/`; log the decision (class chosen, size, font
   embedding status) in `paper/logs/decision_log.md`.

## Output Contract

- `paper/submission/poster/poster.pdf` — single-page PDF whose page size matches
  the venue spec exactly, all fonts embedded, no `Overfull` warnings.
- `paper/submission/poster/poster.tex` — the compilable LaTeX source, plus any
  poster-specific figure copies under `paper/submission/poster/figures/`.
- Optional: a reduced-scale PNG/JPG for email/social, and an A4/Letter handout
  PDF, alongside the main poster.
- A short entry in `paper/logs/decision_log.md` noting the class, page size, and
  QA results; any deferred issues go to `paper/logs/open_questions.md`.
- Do not write into `paper/tex/` (formal track, owned by `09-tex-freeze-formalize`)
  or `paper/refs/` (source material).

## Validation

Run before declaring the poster done:

```bash
# House skill-contract check (this skill)
python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only latex-posters

# Repo project validator
python src/S03_Scripts/validate_project.py

# Poster-specific QA (local toolchain)
pdflatex -interaction=nonstopmode poster.tex
grep -i 'overfull\|underfull\|badbox' poster.log      # must be empty
pdfinfo poster.pdf | grep 'Page size'                  # must match venue spec
pdffonts poster.pdf                                    # every font emb=yes
bash .agent/skills/latex-posters/scripts/review_poster.sh poster.pdf
```

A poster passes only when: page size matches the spec, there are zero `Overfull`
warnings, every font is embedded, and a 100%-zoom edge inspection shows no
content touching or crossing any of the four page boundaries.

## Boundaries

- **External dependencies are user-provided.** This skill does not install a
  LaTeX distribution, fetch packages, or call package mirrors. The user must
  provide a working local `pdflatex`/`xelatex`/`lualatex` toolchain.
- **No invented credentials.** Optional AI schematic generation routes through
  external image/LLM APIs (e.g. OpenRouter) and requires a user-provided API
  key. **The user must supply it**; this skill never hardcodes, stores, or
  transmits secrets. Treat any key as `<user-provided-key>` and read it from the
  user's environment at call time only.
- **No network for the core path.** The recommended path reuses existing
  `paper/assets/figures/` and compiles locally — no network needed. AI
  schematic generation is an optional enhancement, not a requirement.
- **No new science.** Every claim, number, and figure must trace to
  `paper/experiments/` or `paper/assets/`; this skill only lays out and
  distills. It does not run experiments or statistical analysis.
- **No scope creep into other deliverables.** Talk slides → `pptx`; formal
  journal TeX → `09-tex-freeze-formalize`; raw-data figures →
  `scientific-visualization` / `matplotlib`.

## Stop With

- The poster is a single PDF matching the venue page size, all fonts embedded,
  zero overflow warnings, delivered under `paper/submission/poster/`, and the
  decision recorded in `paper/logs/decision_log.md`.
- The venue spec is unreachable (size/orientation unknown) — stop and ask the
  user; do not guess a page size.
- A required figure or claim is missing from `paper/assets/figures/` or
  `paper/experiments/` — stop and request it rather than substituting a
  placeholder.
- The local LaTeX toolchain is absent — stop and tell the user which packages to
  install; do not attempt to install them.
- An optional AI-schematic step is requested but no API key is available — stop
  and ask the user to provide one; never fabricate a key.

## References

- Bundled deep references (copied under this skill): `references/latex_poster_packages.md`
  (beamerposter / tikzposter / baposter comparison and examples),
  `references/poster_layout_design.md` (grid systems and visual flow),
  `references/poster_design_principles.md` (typography, color, accessibility),
  `references/poster_content_guide.md` (section-by-section content guidance),
  `references/README.md`.
- Templates: `assets/beamerposter_template.tex`, `assets/tikzposter_template.tex`,
  `assets/baposter_template.tex`, and `assets/poster_quality_checklist.md`.
- Local QA script: `scripts/review_poster.sh` (page size, fonts, file size,
  page count). Note: the upstream `generate_schematic.py` /
  `generate_schematic_ai.py` helpers are **not** bundled — they call external
  image/LLM APIs; see `scripts/README.md` for how to obtain them from upstream if
  the user opts into AI schematic generation and supplies credentials.
- Workspace inputs: `paper/draft/`, `paper/tex/`, `paper/experiments/evidence_matrix.md`,
  `paper/experiments/statistics.md`, `paper/refs/target_journal.md`,
  `paper/assets/figures/`, `paper/assets/tables/`.
- Workspace outputs: `paper/submission/poster/`, `paper/logs/decision_log.md`,
  `paper/logs/open_questions.md`.
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.

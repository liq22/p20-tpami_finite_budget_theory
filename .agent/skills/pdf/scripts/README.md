# pdf/scripts

Lightweight Python helpers bundled with the `pdf` skill. All are stdlib + common
PDF libraries (`pypdf`, `pdfplumber`, `pdf2image`, `Pillow`); none ship credentials.

| Script | Purpose | Inputs | Outputs | Network | Writes |
|---|---|---|---|---|---|
| `check_fillable_fields.py` | Report whether a PDF has AcroForm fillable fields | argv[1] = PDF path | stdout message | none | none |
| `check_bounding_boxes.py` | Detect overlapping/missing form-field bounding boxes | stdin JSON (from `extract_form_field_info.py`) | stdout messages | none | none |
| `extract_form_field_info.py` | Dump form-field metadata (names, types, rects) | argv[1] = PDF path | stdout JSON | none | none |
| `extract_form_structure.py` | Walk a PDF and emit a form-structure report for annotation-based filling | argv[1] = PDF path | stdout JSON | none | none |
| `convert_pdf_to_images.py` | Render each PDF page to a downsized PNG (max 1000px) for visual review | argv[1] = PDF, argv[2] = output dir | PNG files | none | output dir PNGs |
| `create_validation_image.py` | Build an overlay image showing detected field rectangles over the page | PDF + extracted fields | PNG overlay | none | PNG |
| `fill_fillable_fields.py` | Fill AcroForm fillable fields from a JSON map | argv: PDF, JSON, output PDF | filled PDF | none | output PDF |
| `fill_pdf_form_with_annotations.py` | Stamp field values as page annotations when no AcroForm exists | argv: PDF, JSON, output PDF | filled PDF | none | output PDF |

Notes:
- Network: none of these scripts make outbound calls.
- Dependencies (`pypdf`, `pdfplumber`, `pdf2image`, `Pillow`, plus system
  `poppler-utils`/`tesseract`) are user-provided; never hardcode or store keys.
- Imported from the upstream skill; behavior unchanged.

Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT);
see NOTICE.md and .agent/references/scientific_agent_skills_source.md.

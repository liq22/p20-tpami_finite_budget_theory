---
name: scientific-visualization
description: Generate or revise a scientific figure from actual data by prioritizing the comparison, uncertainty, message, and interpretation boundary before journal formatting or visual styling.
---

# Scientific Visualization

## Purpose

Turn real data into a clear figure that answers one scientific question. The
figure and caption are the product; style reports and metadata are secondary.

## Workflow

1. Fix the reader question, source data, compared groups, units, aggregation, and
   uncertainty.
2. State one evidence-supported message and the interpretation boundary.
3. Choose the simplest honest encoding for the comparison.
4. Generate the actual editable figure and one practical export.
5. Add labels, units, legend, uncertainty definition, sample information, and a
   self-contained caption.
6. Open the final asset at intended size and check data, readability, and whether
   the encoding exaggerates the result.
7. Apply target-journal dimensions or extra export formats only when known and
   actually required.

## Output Contract

Produce:

- an editable figure source;
- one primary vector or high-quality raster export;
- a self-contained caption;
- the data/result path used.

Additional previews, formats, palettes, or logs are optional and should be created
only for a stated need.

## Boundaries

- Do not begin with palette, DPI, font, margin, or multi-panel styling before the
  data comparison and message are correct.
- Do not create decorative panels, significance symbols, or error bars unsupported
  by the actual analysis.
- Do not require a run ledger, evidence matrix, decision log, or target-journal
  file when the data and requested figure are otherwise clear.
- Use Python when it generates or analyzes the actual figure; do not use it for
  formatting scans or proof-of-work reports.
- Do not require multiple simulator passes, screenshot matrices, hashes, or
  repeated export validation.
- Stop when the figure is accurate, readable, and suitable for its stated use.

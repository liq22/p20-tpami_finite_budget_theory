# DOCX authoring and XML reference

Copy-paste-ready `docx-js` authoring patterns and the XML reference for editing
existing `.docx` files. This is the load-bearing detail behind the
**Creating new documents** and **Editing existing documents** workflow steps in
`SKILL.md` — pulled from the upstream skill body so the bundle can produce a
valid `.docx`, not just name the rules.

Conventions:
- DXA units: `1440 DXA = 1 inch`. US Letter content width with 1" margins is
  `12240 - 2880 = 9360 DXA`.
- Use `"Claude"` as the tracked-change / comment author unless told otherwise.
- Install the authoring library with `npm install -g docx`.

---

## 1. Page size

docx-js **defaults to A4, not US Letter** — always set the page size explicitly.

```javascript
sections: [{
  properties: {
    page: {
      size: { width: 12240, height: 15840 },   // US Letter in DXA (8.5" x 11")
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1" margins
    }
  },
  children: [/* content */]
}]
```

| Paper          | Width  | Height | Content width (1" margins) |
|----------------|--------|--------|----------------------------|
| US Letter      | 12,240 | 15,840 | 9,360                      |
| A4 (default)   | 11,906 | 16,838 | 9,026                      |

**Landscape orientation gotcha:** docx-js swaps width/height internally. Pass
**portrait** dimensions (short edge as `width`, long edge as `height`) and set
`orientation` — docx-js performs the swap when it writes the XML:

```javascript
size: {
  width: 12240,   // pass the SHORT edge as width
  height: 15840,  // pass the LONG edge as height
  orientation: PageOrientation.LANDSCAPE   // docx-js swaps them in the XML
},
// Content width = 15840 - left margin - right margin (uses the long edge)
```

---

## 2. Styles (override built-in headings)

Use Arial as the default font (universally supported). **Override built-in
heading IDs exactly** (`"Heading1"`, `"Heading2"`, ...) so Word recognizes them,
and include `outlineLevel` — it is required for the Table of Contents to pick
the heading up.

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 12pt default
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // 0 = H1, required for TOC
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Title")] }),
    ]
  }]
});
```

---

## 3. Lists (never unicode bullets)

**Never** manually insert bullet characters (`"•"` or `"•"`) — they break
numbering, indentation, and screen readers. Use a numbering config with
`LevelFormat.BULLET`.

```javascript
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Bullet item")] }),
      new Paragraph({ numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Numbered item")] }),
    ]
  }]
});
// Each reference creates INDEPENDENT numbering: same reference continues (1,2,3 -> 4,5,6);
// a different reference restarts (1,2,3 -> 1,2,3).
```

---

## 4. Tables (dual-width, always DXA)

**CRITICAL — tables need dual widths:** set `columnWidths` on the table **and**
`width` on every cell. Without both, tables render incorrectly on some
platforms.

```javascript
const border  = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA },         // ALWAYS DXA — PERCENTAGE breaks in Google Docs
  columnWidths: [4680, 4680],                          // must sum to table width
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA },  // also set on each cell, matching its column
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, // CLEAR, never SOLID
          margins: { top: 80, bottom: 80, left: 120, right: 120 }, // internal padding, not added to width
          children: [new Paragraph({ children: [new TextRun("Cell")] })]
        })
      ]
    })
  ]
})
```

Width rules:
- **Always use `WidthType.DXA`** — never `WidthType.PERCENTAGE` (incompatible
  with Google Docs).
- **Table width = sum of `columnWidths`** (and = page content width for a
  full-width table).
- Cell `width` must match the corresponding `columnWidth`.
- Cell `margins` are **internal** padding — they reduce the content area, they
  do **not** add to cell width.

---

## 5. Images, page breaks, hyperlinks, footnotes, tabs, columns, TOC, headers

### Images — `type` is required

```javascript
new Paragraph({
  children: [new ImageRun({
    type: "png",   // REQUIRED: png | jpg | jpeg | gif | bmp | svg
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "Title", description: "Desc", name: "Name" } // all three required
  })]
})
```

### Page breaks — must be inside a Paragraph

```javascript
new Paragraph({ children: [new PageBreak()] })           // CORRECT
new Paragraph({ pageBreakBefore: true, children: [new TextRun("New page")] })
// A standalone PageBreak (not wrapped in a Paragraph) produces invalid XML.
```

### Hyperlinks — external and internal

```javascript
// External link
new Paragraph({
  children: [new ExternalHyperlink({
    children: [new TextRun({ text: "Click here", style: "Hyperlink" })],
    link: "https://example.com",
  })]
})

// Internal link: define a Bookmark, then reference its anchor
new Paragraph({ heading: HeadingLevel.HEADING_1, children: [
  new Bookmark({ id: "chapter1", children: [new TextRun("Chapter 1")] }),
]})
new Paragraph({ children: [new InternalHyperlink({
  children: [new TextRun({ text: "See Chapter 1", style: "Hyperlink" })],
  anchor: "chapter1",
})]})
```

### Footnotes

```javascript
const doc = new Document({
  footnotes: {
    1: { children: [new Paragraph("Source: Annual Report 2024")] },
    2: { children: [new Paragraph("See appendix for methodology")] },
  },
  sections: [{
    children: [new Paragraph({
      children: [
        new TextRun("Revenue grew 15%"),
        new FootnoteReferenceRun(1),
        new TextRun(" using adjusted metrics"),
        new FootnoteReferenceRun(2),
      ],
    })]
  }]
});
```

### Tab stops — right-align and dot-leader

```javascript
// Right-align text on the same line (e.g. a date opposite a title)
new Paragraph({
  children: [ new TextRun("Company Name"), new TextRun("\tJanuary 2025") ],
  tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
})

// Dot leader (TOC-style) via PositionalTab
new Paragraph({
  children: [
    new TextRun("Introduction"),
    new TextRun({ children: [
      new PositionalTab({
        alignment: PositionalTabAlignment.RIGHT,
        relativeTo: PositionalTabRelativeTo.MARGIN,
        leader: PositionalTabLeader.DOT,
      }),
      "3",
    ]}),
  ],
})
```

### Multi-column layouts

```javascript
// Equal-width columns
sections: [{
  properties: {
    column: { count: 2, space: 720, equalWidth: true, separate: true }, // 720 DXA = 0.5"
  },
  children: [/* content flows naturally across columns */]
}]

// Custom-width columns (equalWidth must be false)
sections: [{
  properties: {
    column: {
      equalWidth: false,
      children: [
        new Column({ width: 5400, space: 720 }),
        new Column({ width: 3240 }),
      ],
    },
  },
  children: [/* content */]
}]
// Force a column break with a new section: type: SectionType.NEXT_COLUMN
```

### Table of contents

```javascript
// Headings must use HeadingLevel ONLY — no custom styles on heading paragraphs
new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" })
```

### Headers and footers

```javascript
sections: [{
  properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
  headers: {
    default: new Header({ children: [new Paragraph({ children: [new TextRun("Header")] })] })
  },
  footers: {
    default: new Footer({ children: [new Paragraph({
      children: [new TextRun("Page "), new TextRun({ children: [PageNumber.CURRENT] })]
    })] })
  },
  children: [/* content */]
}]
```

---

## 6. Critical rules for docx-js (checklist)

- **Set page size explicitly** — docx-js defaults to A4; use US Letter
  (12240 × 15840 DXA) for US documents.
- **Landscape: pass portrait dimensions** — docx-js swaps width/height
  internally; pass the short edge as `width`, the long edge as `height`, and
  set `orientation: PageOrientation.LANDSCAPE`.
- **Never use `\n`** — use separate `Paragraph` elements.
- **Never use unicode bullets** — use `LevelFormat.BULLET` with a numbering
  config.
- **`PageBreak` must be in a `Paragraph`** — standalone creates invalid XML.
- **`ImageRun` requires `type`** — always specify `png`/`jpg`/etc.
- **Always set table `width` with DXA** — never `WidthType.PERCENTAGE`
  (breaks in Google Docs).
- **Tables need dual widths** — `columnWidths` array AND cell `width`, both
  must match.
- **Table width = sum of `columnWidths`** — for DXA, ensure they add up
  exactly.
- **Always add cell `margins`** — e.g. `{ top: 80, bottom: 80, left: 120, right: 120 }`.
- **Use `ShadingType.CLEAR`** — never `SOLID` for table shading.
- **Never use tables as dividers/rules** — cells have a minimum height and
  render as empty boxes (including in headers/footers); use a paragraph border
  (`border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } }`)
  instead. For a two-column footer, use tab stops, not a table.
- **TOC requires `HeadingLevel` only** — no custom styles on heading paragraphs.
- **Override built-in styles** — use exact IDs: `"Heading1"`, `"Heading2"`, etc.
- **Include `outlineLevel`** — required for TOC (0 for H1, 1 for H2, ...).

---

## 7. Smart-quote entities for new prose

When adding text with apostrophes or quotes during an edit, use XML entities so
the result is professional smart typography:

```xml
<!-- Use these entities for new content -->
<w:t>Here&#x2019;s a quote: &#x201C;Hello&#x201D;</w:t>
```

| Entity     | Character                  |
|------------|----------------------------|
| `&#x2018;` | ‘ (left single)            |
| `&#x2019;` | ’ (right single / apostrophe) |
| `&#x201C;` | “ (left double)            |
| `&#x201D;` | ” (right double)           |

---

## 8. XML reference (editing existing documents)

### Schema compliance

- **Element order in `<w:pPr>`:** `<w:pStyle>`, `<w:numPr>`, `<w:spacing>`,
  `<w:ind>`, `<w:jc>`, `<w:rPr>` last.
- **Whitespace:** add `xml:space="preserve"` to any `<w:t>` with leading or
  trailing spaces.
- **RSIDs:** must be 8-digit hex (e.g. `00AB1234`).

### Tracked changes

**Insertion:**
```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>
```

**Deletion:** inside `<w:del>`, use `<w:delText>` (not `<w:t>`) and
`<w:delInstrText>` (not `<w:instrText>`).
```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```

**Minimal edits** — mark only what changes:
```xml
<!-- Change "30 days" to "60 days" -->
<w:r><w:t>The term is </w:t></w:r>
<w:del w:id="1" w:author="Claude" w:date="...">
  <w:r><w:delText>30</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="Claude" w:date="...">
  <w:r><w:t>60</w:t></w:r>
</w:ins>
<w:r><w:t> days.</w:t></w:r>
```

**Deleting an entire paragraph / list item** — when removing ALL content from a
paragraph, also mark the **paragraph mark** as deleted so accepting changes
merges it with the next paragraph (otherwise an empty paragraph is left
behind). Add `<w:del/>` inside `<w:pPr><w:rPr>`:
```xml
<w:p>
  <w:pPr>
    <w:numPr>...</w:numPr>  <!-- list numbering, if present -->
    <w:rPr>
      <w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
    <w:r><w:delText>Entire paragraph content being deleted...</w:delText></w:r>
  </w:del>
</w:p>
```

**Rejecting another author's insertion** — nest your deletion inside their
insertion:
```xml
<w:ins w:author="Jane" w:id="5">
  <w:del w:author="Claude" w:id="10">
    <w:r><w:delText>their inserted text</w:delText></w:r>
  </w:del>
</w:ins>
```

**Restoring another author's deletion** — add your insertion as a sibling
after their deletion (do not modify their `<w:del>`):
```xml
<w:del w:author="Jane" w:id="5">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
<w:ins w:author="Claude" w:id="10">
  <w:r><w:t>deleted text</w:t></w:r>
</w:ins>
```

### Comments

After running `comment.py` (Workflow Step 2 in `SKILL.md`) to write the
boilerplate, add the range/reference markers to `document.xml`.

**CRITICAL:** `<w:commentRangeStart>` and `<w:commentRangeEnd>` are **siblings
of `<w:r>`, never inside `<w:r>`** — they are direct children of `<w:p>`.

```xml
<!-- Markers are direct children of w:p, never inside w:r -->
<w:commentRangeStart w:id="0"/>
<w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted</w:delText></w:r>
</w:del>
<w:r><w:t> more text</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
```

**Nested reply** — use `comment.py ... --parent 0`, then nest the child range
markers inside the parent's:
```xml
<w:commentRangeStart w:id="0"/>
  <w:commentRangeStart w:id="1"/>
  <w:r><w:t>text</w:t></w:r>
  <w:commentRangeEnd w:id="1"/>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="1"/></w:r>
```

### Manual image insertion (when not using docx-js)

1. Add the image file to `word/media/`.
2. Register a relationship in `word/_rels/document.xml.rels`:
   ```xml
   <Relationship Id="rId5" Type=".../image" Target="media/image1.png"/>
   ```
3. Add the content type to `[Content_Types].xml` (if not already present):
   ```xml
   <Default Extension="png" ContentType="image/png"/>
   ```
4. Reference it from `document.xml`. EMUs: `914400 EMU = 1 inch`.
   ```xml
   <w:drawing>
     <wp:inline>
       <wp:extent cx="914400" cy="914400"/>
       <a:graphic>
         <a:graphicData uri=".../picture">
           <pic:pic>
             <pic:blipFill><a:blip r:embed="rId5"/></pic:blipFill>
           </pic:pic>
         </a:graphicData>
       </a:graphic>
     </wp:inline>
   </w:drawing>
   ```

---

## Editing guardrails (apply when hand-editing XML)

- **Replace entire `<w:r>` elements** — when adding tracked changes, replace
  the whole `<w:r>...</w:r>` block with `<w:del>...` / `<w:ins>...` as
  siblings. Never inject tracked-change tags inside a run.
- **Preserve `<w:rPr>` formatting** — copy the original run's `<w:rPr>` block
  into your tracked-change runs to keep bold, font size, etc.

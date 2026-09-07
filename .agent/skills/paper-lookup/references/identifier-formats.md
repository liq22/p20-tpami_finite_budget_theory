# Common Identifier Formats

Different databases use different identifier systems. If a query fails, the
identifier format may be wrong. This is the table the canonical SKILL.md Workflow
references at step 3 ("Use the Common Identifier Formats table to confirm the
supplied ID is in the right shape") and step 7 (error recovery).

| Identifier | Format | Example | Used by |
|---|---|---|---|
| DOI | `10.xxxx/xxxxx` | `10.1038/nature12373` | All databases |
| PMID | Integer | `34567890` | PubMed, PMC, Semantic Scholar |
| PMCID | `PMC` + digits | `PMC7029759` | PMC, Europe PMC |
| arXiv ID | `YYMM.NNNNN` | `2103.15348` | arXiv, Semantic Scholar |
| OpenAlex ID | `W` + digits | `W2741809807` | OpenAlex |
| Semantic Scholar ID | 40-char hex | `649def34f8be...` | Semantic Scholar |
| ORCID | `0000-XXXX-XXXX-XXXX` | `0000-0001-6187-6610` | OpenAlex, Crossref |
| ISSN | `XXXX-XXXX` | `0028-0836` | Crossref, OpenAlex |

## Cross-referencing IDs

Semantic Scholar accepts DOI, PMID, PMCID, and arXiv ID via prefixes
(e.g., `DOI:10.1038/nature12373`, `PMID:34567890`, `ARXIV:2103.15348`).
OpenAlex accepts DOI and PMID via prefixes (`doi:10.1038/...`,
`pmid:34567890`). Use the **PMC ID Converter** to translate between PMID,
PMCID, and DOI.

---

*Provenance: restored verbatim from upstream K-Dense-AI/scientific-agent-skills
v2.53.0 `skills/paper-lookup/SKILL.md` lines 63-78, including the
cross-referencing-prefix note for Semantic Scholar and OpenAlex and the PMC ID
Converter mention.*

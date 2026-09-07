"""Conditional cross-file checks for runs, sources, claims, and visuals."""
from __future__ import annotations

from pathlib import Path

from .model import (
    CLAIM_RE,
    EVIDENCE_RE,
    EVIDENCE_STATUSES,
    EVIDENCE_STRENGTHS,
    FIGURE_RE,
    FIGURE_TABLE_STATUSES,
    NON_SUPPORTING_RUN_STATUSES,
    POSITIVE_EVIDENCE_STATUSES,
    READING_STATUSES,
    REF_RE,
    RUN_RE,
    RUN_STATUSES,
    TABLE_RE,
    Reporter,
    ensure_unique,
    extract_ids,
    is_placeholder,
    non_placeholder_rows,
    parse_markdown_table,
)


def _rows_if_present(
    path: Path,
    required_columns: list[str],
    reporter: Reporter,
    *,
    label: str,
    id_column: str,
) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    rows = parse_markdown_table(
        path,
        required_columns,
        reporter,
        label=label,
        allow_empty=True,
    )
    return non_placeholder_rows(rows, id_column)


def _valid_ids(
    rows: list[dict[str, str]],
    column: str,
    pattern,
    reporter: Reporter,
    path: Path,
    *,
    duplicate_code: str,
    invalid_code: str,
    label: str,
) -> set[str]:
    ids = ensure_unique(
        ((row.get(column, ""), f"row {index + 1}") for index, row in enumerate(rows)),
        reporter,
        path,
        code=duplicate_code,
        label=label,
    )
    for value in ids:
        if not pattern.fullmatch(value):
            reporter.error(invalid_code, path, f"invalid {label}: {value!r}")
    return ids


def validate_research_graph(
    root: Path,
    reporter: Reporter,
    claim_ids: set[str],
) -> dict[str, set[str]]:
    """Validate only records that actually exist and contain real identifiers."""
    run_path = root / "paper" / "experiments" / "run_ledger.md"
    run_rows = _rows_if_present(
        run_path,
        [
            "Run ID",
            "Date",
            "Code version",
            "Config",
            "Data/version",
            "Seed",
            "Primary metric",
            "Result",
            "Status",
            "Output path",
        ],
        reporter,
        label="run ledger",
        id_column="Run ID",
    )
    run_ids = _valid_ids(
        run_rows,
        "Run ID",
        RUN_RE,
        reporter,
        run_path,
        duplicate_code="E-DUPLICATE-RUN",
        invalid_code="E-RUN-ID",
        label="run ID",
    )
    run_status_by_id: dict[str, str] = {}
    for row in run_rows:
        run_id = row.get("Run ID", "").strip()
        status = row.get("Status", "").strip()
        if status not in RUN_STATUSES:
            reporter.error("E-RUN-STATUS", run_path, f"invalid status for {run_id}: {status!r}")
        run_status_by_id[run_id] = status
        if status == "completed":
            for column in (
                "Date",
                "Code version",
                "Config",
                "Data/version",
                "Seed",
                "Primary metric",
                "Result",
                "Output path",
            ):
                if is_placeholder(row.get(column)):
                    reporter.error(
                        "E-COMPLETED-RUN-FIELD",
                        run_path,
                        f"completed {run_id} requires {column}",
                    )

    reading_path = root / "paper" / "refs" / "reading_matrix.md"
    reading_rows = _rows_if_present(
        reading_path,
        [
            "Ref ID",
            "Bib key",
            "Verified source",
            "Main evidence",
            "Limitation",
            "Supports/refutes claim",
            "Full text checked",
            "Status",
        ],
        reporter,
        label="reading matrix",
        id_column="Ref ID",
    )
    ref_ids = _valid_ids(
        reading_rows,
        "Ref ID",
        REF_RE,
        reporter,
        reading_path,
        duplicate_code="E-DUPLICATE-REF",
        invalid_code="E-REF-ID",
        label="reference ID",
    )
    ref_status_by_id: dict[str, str] = {}
    for row in reading_rows:
        ref_id = row.get("Ref ID", "").strip()
        status = row.get("Status", "").strip()
        if status not in READING_STATUSES:
            reporter.error("E-REF-STATUS", reading_path, f"invalid status for {ref_id}: {status!r}")
        ref_status_by_id[ref_id] = status
        for claim_id in extract_ids(CLAIM_RE, row.get("Supports/refutes claim", "")):
            if claim_id not in claim_ids:
                reporter.error("E-REF-CLAIM-FK", reading_path, f"{ref_id} references unknown claim {claim_id}")
        if status == "verified":
            for column in ("Bib key", "Verified source", "Main evidence", "Limitation"):
                if is_placeholder(row.get(column)):
                    reporter.error("E-VERIFIED-REF-FIELD", reading_path, f"verified {ref_id} requires {column}")
            if row.get("Full text checked", "").strip().lower() not in {"yes", "true"}:
                reporter.error("E-VERIFIED-REF-FULLTEXT", reading_path, f"verified {ref_id} requires Full text checked=yes")

    evidence_path = root / "paper" / "experiments" / "evidence_matrix.md"
    evidence_rows = _rows_if_present(
        evidence_path,
        [
            "Claim ID",
            "Strength",
            "Evidence ID",
            "Run/ref/artifact",
            "Boundary",
            "Status",
        ],
        reporter,
        label="evidence matrix",
        id_column="Evidence ID",
    )
    evidence_ids = _valid_ids(
        evidence_rows,
        "Evidence ID",
        EVIDENCE_RE,
        reporter,
        evidence_path,
        duplicate_code="E-DUPLICATE-EVIDENCE",
        invalid_code="E-EVIDENCE-ID",
        label="evidence ID",
    )
    for row in evidence_rows:
        claim_id = row.get("Claim ID", "").strip()
        evidence_id = row.get("Evidence ID", "").strip()
        strength = row.get("Strength", "").strip()
        status = row.get("Status", "").strip()
        source = row.get("Run/ref/artifact", "").strip()

        if claim_id and not is_placeholder(claim_id) and claim_id not in claim_ids:
            reporter.error("E-EVIDENCE-CLAIM-FK", evidence_path, f"{evidence_id} references unknown claim {claim_id}")
        if strength not in EVIDENCE_STRENGTHS:
            reporter.error("E-EVIDENCE-STRENGTH", evidence_path, f"invalid strength for {evidence_id}: {strength!r}")
        if status not in EVIDENCE_STATUSES:
            reporter.error("E-EVIDENCE-STATUS", evidence_path, f"invalid status for {evidence_id}: {status!r}")

        run_refs = extract_ids(RUN_RE, source)
        literature_refs = extract_ids(REF_RE, source)
        if status in POSITIVE_EVIDENCE_STATUSES:
            if is_placeholder(source):
                reporter.error("E-SUPPORTED-EVIDENCE-SOURCE", evidence_path, f"{evidence_id} must name a run, verified source, or result path")
            if is_placeholder(row.get("Boundary")):
                reporter.error("E-SUPPORTED-EVIDENCE-BOUNDARY", evidence_path, f"{evidence_id} must state its boundary")

        for run_id in run_refs:
            if run_id not in run_ids:
                reporter.error("E-EVIDENCE-RUN-FK", evidence_path, f"{evidence_id} references unknown run {run_id}")
            elif status in POSITIVE_EVIDENCE_STATUSES and run_status_by_id.get(run_id) in NON_SUPPORTING_RUN_STATUSES:
                reporter.error("E-NON-SUPPORTING-RUN", evidence_path, f"{evidence_id} cites {run_id}={run_status_by_id.get(run_id)}; positive evidence requires a completed run")
        for ref_id in literature_refs:
            if ref_id not in ref_ids:
                reporter.error("E-EVIDENCE-REF-FK", evidence_path, f"{evidence_id} references unknown ref {ref_id}")
            elif status in POSITIVE_EVIDENCE_STATUSES and ref_status_by_id.get(ref_id) != "verified":
                reporter.error("E-NON-VERIFIED-REF", evidence_path, f"{evidence_id} cites {ref_id}={ref_status_by_id.get(ref_id)}; positive evidence requires a verified full-text source")

    figure_path = root / "paper" / "assets" / "figures" / "figure_manifest.md"
    figure_rows = _rows_if_present(
        figure_path,
        [
            "Figure ID",
            "File path",
            "Key message",
            "Claim ref",
            "Evidence ref",
            "Source data/output",
            "First callout",
            "Status",
        ],
        reporter,
        label="figure manifest",
        id_column="Figure ID",
    )
    figure_ids = _valid_ids(
        figure_rows,
        "Figure ID",
        FIGURE_RE,
        reporter,
        figure_path,
        duplicate_code="E-DUPLICATE-FIGURE",
        invalid_code="E-FIGURE-ID",
        label="figure ID",
    )
    for row in figure_rows:
        figure_id = row.get("Figure ID", "").strip()
        status = row.get("Status", "").strip()
        if status not in FIGURE_TABLE_STATUSES:
            reporter.error("E-FIGURE-STATUS", figure_path, f"invalid status for {figure_id}: {status!r}")
        for claim_id in extract_ids(CLAIM_RE, row.get("Claim ref", "")):
            if claim_id not in claim_ids:
                reporter.error("E-FIGURE-CLAIM-FK", figure_path, f"{figure_id} references unknown claim {claim_id}")
        for evidence_id in extract_ids(EVIDENCE_RE, row.get("Evidence ref", "")):
            if evidence_id not in evidence_ids:
                reporter.error("E-FIGURE-EVIDENCE-FK", figure_path, f"{figure_id} references unknown evidence {evidence_id}")
        if status in {"generated", "ready"}:
            for column in ("File path", "Key message", "Source data/output", "First callout"):
                if is_placeholder(row.get(column)):
                    reporter.error("E-FIGURE-READY-FIELD", figure_path, f"{status} {figure_id} requires {column}")

    table_path = root / "paper" / "assets" / "tables" / "table_manifest.md"
    table_rows = _rows_if_present(
        table_path,
        [
            "Table ID",
            "File path",
            "Key message",
            "Claim ref",
            "Evidence ref",
            "Source data/output",
            "First callout",
            "Status",
        ],
        reporter,
        label="table manifest",
        id_column="Table ID",
    )
    table_ids = _valid_ids(
        table_rows,
        "Table ID",
        TABLE_RE,
        reporter,
        table_path,
        duplicate_code="E-DUPLICATE-TABLE",
        invalid_code="E-TABLE-ID",
        label="table ID",
    )
    for row in table_rows:
        table_id = row.get("Table ID", "").strip()
        status = row.get("Status", "").strip()
        if status not in FIGURE_TABLE_STATUSES:
            reporter.error("E-TABLE-STATUS", table_path, f"invalid status for {table_id}: {status!r}")
        for claim_id in extract_ids(CLAIM_RE, row.get("Claim ref", "")):
            if claim_id not in claim_ids:
                reporter.error("E-TABLE-CLAIM-FK", table_path, f"{table_id} references unknown claim {claim_id}")
        for evidence_id in extract_ids(EVIDENCE_RE, row.get("Evidence ref", "")):
            if evidence_id not in evidence_ids:
                reporter.error("E-TABLE-EVIDENCE-FK", table_path, f"{table_id} references unknown evidence {evidence_id}")
        if status in {"generated", "ready"}:
            for column in ("File path", "Key message", "Source data/output", "First callout"):
                if is_placeholder(row.get(column)):
                    reporter.error("E-TABLE-READY-FIELD", table_path, f"{status} {table_id} requires {column}")

    paragraph_path = root / "paper" / "draft" / "00_paragraph_map.md"
    paragraph_rows = _rows_if_present(
        paragraph_path,
        ["Paragraph ID", "Claim ID", "Evidence/ref/run", "Figure/table"],
        reporter,
        label="paragraph map",
        id_column="Paragraph ID",
    )
    ensure_unique(
        ((row.get("Paragraph ID", ""), f"row {index + 1}") for index, row in enumerate(paragraph_rows)),
        reporter,
        paragraph_path,
        code="E-DUPLICATE-PARAGRAPH",
        label="paragraph ID",
    )
    for row in paragraph_rows:
        paragraph_id = row.get("Paragraph ID", "").strip()
        for claim_id in extract_ids(CLAIM_RE, row.get("Claim ID", "")):
            if claim_id not in claim_ids:
                reporter.error("E-PARAGRAPH-CLAIM-FK", paragraph_path, f"{paragraph_id} references unknown claim {claim_id}")
        sources = row.get("Evidence/ref/run", "")
        for evidence_id in extract_ids(EVIDENCE_RE, sources):
            if evidence_id not in evidence_ids:
                reporter.error("E-PARAGRAPH-EVIDENCE-FK", paragraph_path, f"{paragraph_id} references unknown evidence {evidence_id}")
        for run_id in extract_ids(RUN_RE, sources):
            if run_id not in run_ids:
                reporter.error("E-PARAGRAPH-RUN-FK", paragraph_path, f"{paragraph_id} references unknown run {run_id}")
        for ref_id in extract_ids(REF_RE, sources):
            if ref_id not in ref_ids:
                reporter.error("E-PARAGRAPH-REF-FK", paragraph_path, f"{paragraph_id} references unknown ref {ref_id}")
        visuals = row.get("Figure/table", "")
        for figure_id in extract_ids(FIGURE_RE, visuals):
            if figure_id not in figure_ids:
                reporter.error("E-PARAGRAPH-FIGURE-FK", paragraph_path, f"{paragraph_id} references unknown figure {figure_id}")
        for table_id in extract_ids(TABLE_RE, visuals):
            if table_id not in table_ids:
                reporter.error("E-PARAGRAPH-TABLE-FK", paragraph_path, f"{paragraph_id} references unknown table {table_id}")

    return {
        "claims": claim_ids,
        "evidence": evidence_ids,
        "runs": run_ids,
        "refs": ref_ids,
        "figures": figure_ids,
        "tables": table_ids,
    }

"""Validate the minimum scientific argument fields for figures."""
from __future__ import annotations

from pathlib import Path

from .model import (
    FIGURE_TABLE_STATUSES,
    Reporter,
    is_placeholder,
    non_placeholder_rows,
    parse_markdown_table,
)

REQUIRED_ARGUMENT_COLUMNS = (
    "Figure ID",
    "Reader question",
    "Key message",
    "Comparison / encoding",
    "Interpretation boundary",
    "Status",
)


def validate_figure_arguments(root: Path, reporter: Reporter) -> None:
    path = root / "paper" / "assets" / "figures" / "figure_manifest.md"
    if not path.is_file():
        return

    rows = parse_markdown_table(
        path,
        REQUIRED_ARGUMENT_COLUMNS,
        reporter,
        label="figure argument",
        allow_empty=True,
    )
    for row in non_placeholder_rows(rows, "Figure ID"):
        figure_id = row.get("Figure ID", "").strip() or "figure row"
        status = row.get("Status", "").strip()
        if status not in FIGURE_TABLE_STATUSES:
            continue
        if status in {"drafted", "generated", "ready"}:
            for column in (
                "Reader question",
                "Key message",
                "Comparison / encoding",
                "Interpretation boundary",
            ):
                if is_placeholder(row.get(column)):
                    reporter.error(
                        "E-FIGURE-ARGUMENT",
                        path,
                        f"{status} {figure_id} requires {column}",
                    )

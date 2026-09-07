"""Shared constants and lightweight parsing helpers for PaperTrace validation."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required. Install development dependencies with "
        "`python -m pip install -r requirements-dev.txt`."
    ) from exc

# Core files support the smallest useful PaperTrace workspace. Method, experiment,
# figure, TeX, submission, tool, and audit surfaces are validated only when they
# exist or when the active paper stage requires them.
REQUIRED_DIRS = [
    "paper",
    ".agent/skills/00-router",
]

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "paper/paper.yaml",
    ".agent/skills/00-router/SKILL.md",
]

# Retained for compatibility with the validator API. Only the host Router is a
# universal capability; all other Skills are optional/project-specific.
STAGE_SKILLS = ["00-router"]

SKILL_HEADINGS = [
    "## Purpose",
    "## Workflow",
    "## Output Contract",
    "## Boundaries",
]

PAPER_STAGES = [
    "idea",
    "outline",
    "markdown_draft",
    "tex_formalization",
    "submission_ready",
    "submitted",
    "revision",
    "accepted",
]
STAGE_RANK = {stage: index for index, stage in enumerate(PAPER_STAGES)}
MARKDOWN_STAGES = {"idea", "outline", "markdown_draft"}
TEX_STAGES = {"tex_formalization", "submission_ready", "submitted", "revision", "accepted"}

RUN_STATUSES = {
    "planned",
    "running",
    "completed",
    "failed",
    "timeout",
    "cancelled",
    "invalid",
    "to_verify",
}
NON_SUPPORTING_RUN_STATUSES = RUN_STATUSES - {"completed"}
EVIDENCE_STATUSES = {
    "missing",
    "planned",
    "to_verify",
    "supported",
    "partially_supported",
    "refuted",
    "blocked",
}
POSITIVE_EVIDENCE_STATUSES = {"supported", "partially_supported"}
EVIDENCE_STRENGTHS = {"hypothesis", "weak", "moderate", "strong"}
FIGURE_TABLE_STATUSES = {"planned", "drafted", "generated", "ready", "blocked"}
READING_STATUSES = {"to_read", "screened", "full_text_checked", "verified", "excluded"}
GATE_STATUSES = {"pass", "waived", "fail", "blocked"}

CLAIM_RE = re.compile(r"\bC\d+\b")
EVIDENCE_RE = re.compile(r"\bE\d+\b")
RUN_RE = re.compile(r"\bRUN-\d+\b")
REF_RE = re.compile(r"\bR\d+\b")
FIGURE_RE = re.compile(r"\bF\d+\b")
TABLE_RE = re.compile(r"\bT\d+\b")
GATE_ID_RE = re.compile(r"^G-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
SYMBOLIC_PLACEHOLDER_RE = re.compile(
    r"^(?:(?:C|E|R|F|T|RUN|REF|FIG|TABLE|ID)(?:-\d+)?\?)(?:/(?:(?:C|E|R|F|T|RUN|REF|FIG|TABLE|ID)(?:-\d+)?\?))*$"
)
PLACEHOLDERS = {"", "todo", "unknown", "none", "n/a", "na", "-", "?"}


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    path: str
    message: str


class Reporter:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.issues: list[Issue] = []

    def _path(self, path: Path | str | None) -> str:
        if path is None:
            return "."
        candidate = Path(path)
        try:
            return candidate.resolve().relative_to(self.root.resolve()).as_posix()
        except (ValueError, OSError):
            return str(path)

    def error(self, code: str, path: Path | str | None, message: str) -> None:
        self.issues.append(Issue("error", code, self._path(path), message))

    def warning(self, code: str, path: Path | str | None, message: str) -> None:
        self.issues.append(Issue("warning", code, self._path(path), message))

    @property
    def errors(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "warning"]


def is_placeholder(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        cleaned = value.strip().strip("`\"'")
        normalized = cleaned.lower()
        if normalized in PLACEHOLDERS or "todo" in normalized:
            return True
        return bool(SYMBOLIC_PLACEHOLDER_RE.fullmatch(cleaned.upper()))
    return False


def read_text(path: Path, reporter: Reporter) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        reporter.error("E-READ", path, f"cannot read UTF-8 text: {exc}")
        return ""


def load_yaml(path: Path, reporter: Reporter) -> Any:
    text = read_text(path, reporter)
    if not text:
        return None
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as exc:
        reporter.error("E-YAML", path, f"invalid YAML: {exc}")
        return None


def split_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    body = stripped[1:-1] if stripped.endswith("|") else stripped[1:]
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in body:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            current.append(char)
            escaped = True
        elif char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    cells.append("".join(current).strip())
    return cells


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(
        re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells
    )


def parse_markdown_table(
    path: Path,
    required_columns: Iterable[str],
    reporter: Reporter,
    *,
    label: str,
    allow_empty: bool = False,
) -> list[dict[str, str]]:
    """Parse one Markdown table.

    Empty header-only tables are valid for optional PaperTrace records. A file
    that exists but has the wrong columns remains an error because its meaning is
    ambiguous and should not be guessed.
    """
    text = read_text(path, reporter)
    lines = text.splitlines()
    required = list(required_columns)
    for index, line in enumerate(lines):
        headers = split_markdown_row(line)
        if not headers or not all(column in headers for column in required):
            continue
        if index + 1 >= len(lines) or not is_separator_row(
            split_markdown_row(lines[index + 1])
        ):
            reporter.error(
                "E-TABLE-SEPARATOR",
                path,
                f"{label} header is not followed by a separator row",
            )
            return []
        rows: list[dict[str, str]] = []
        for row_line in lines[index + 2 :]:
            if not row_line.lstrip().startswith("|"):
                break
            cells = split_markdown_row(row_line)
            if len(cells) != len(headers):
                reporter.error(
                    "E-TABLE-WIDTH",
                    path,
                    f"{label} row has {len(cells)} cells; expected {len(headers)}",
                )
                continue
            rows.append(dict(zip(headers, cells)))
        if not rows and not allow_empty:
            reporter.error("E-TABLE-EMPTY", path, f"{label} must contain at least one row")
        return rows
    reporter.error("E-TABLE-COLUMNS", path, f"{label} must contain columns: {required}")
    return []


def non_placeholder_rows(
    rows: Iterable[dict[str, str]],
    id_column: str,
) -> list[dict[str, str]]:
    """Ignore template/example rows whose identifier is still a placeholder."""
    return [row for row in rows if not is_placeholder(row.get(id_column))]


def ensure_unique(
    values: Iterable[tuple[str, str]],
    reporter: Reporter,
    path: Path,
    *,
    code: str,
    label: str,
) -> set[str]:
    seen: dict[str, str] = {}
    result: set[str] = set()
    for value, location in values:
        if is_placeholder(value):
            continue
        normalized = value.strip()
        if normalized in seen:
            reporter.error(
                code,
                path,
                f"duplicate {label} {normalized!r}: {seen[normalized]} and {location}",
            )
        else:
            seen[normalized] = location
            result.add(normalized)
    return result


def extract_ids(pattern: re.Pattern[str], value: str) -> set[str]:
    return set(pattern.findall(value or ""))

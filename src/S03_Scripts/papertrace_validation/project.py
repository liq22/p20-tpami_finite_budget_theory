"""Core layout, active-source, and readable paper-state checks."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .model import (
    MARKDOWN_STAGES,
    PAPER_STAGES,
    REQUIRED_DIRS,
    REQUIRED_FILES,
    SKILL_HEADINGS,
    STAGE_SKILLS,
    TEX_STAGES,
    Reporter,
    ensure_unique,
    is_placeholder,
    load_yaml,
    read_text,
)

IDEA_ID_RE = re.compile(r"IDEA-\d+")
CLAIM_ID_RE = re.compile(r"C\d+")


def validate_required_layout(root: Path, reporter: Reporter) -> None:
    """Validate only the universal PaperTrace core.

    Method, experiment, TeX, submission, Office, external-backend, and audit
    surfaces are optional and are validated by their own modules when present.
    """
    for relative in REQUIRED_DIRS:
        if not (root / relative).is_dir():
            reporter.error("E-MISSING-DIR", root / relative, "required core directory is missing")
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            reporter.error("E-MISSING-FILE", root / relative, "required core file is missing")

    for skill in STAGE_SKILLS:
        path = root / ".agent" / "skills" / skill / "SKILL.md"
        if not path.is_file():
            reporter.error("E-MISSING-SKILL", path, "required Router skill is missing")
            continue
        text = read_text(path, reporter)
        for heading in SKILL_HEADINGS:
            if heading not in text:
                reporter.error("E-SKILL-SECTION", path, f"missing substantive heading: {heading}")


def _source_path(
    root: Path,
    paper: dict[str, Any],
    key: str,
    fallback: str,
    reporter: Reporter,
    paper_path: Path,
) -> Path:
    value = paper.get(key)
    if value is None:
        relative = fallback
    elif not isinstance(value, dict):
        reporter.error("E-PAPER-SCHEMA", paper_path, f"{key} must be a mapping")
        relative = fallback
    else:
        relative = str(value.get("path", fallback))
    return root / relative


def validate_paper_state(root: Path, reporter: Reporter) -> tuple[dict[str, Any], set[str]]:
    path = root / "paper" / "paper.yaml"
    data = load_yaml(path, reporter)
    if not isinstance(data, dict):
        reporter.error("E-PAPER-SCHEMA", path, "paper.yaml must contain a YAML mapping")
        return {}, set()

    stage = data.get("paper_stage")
    active = data.get("active_source")
    freeze = data.get("freeze") if isinstance(data.get("freeze"), dict) else {}
    if stage not in PAPER_STAGES:
        reporter.error("E-PAPER-STAGE", path, f"paper_stage must be one of {PAPER_STAGES}; got {stage!r}")
    if active not in {"markdown", "tex"}:
        reporter.error("E-ACTIVE-SOURCE", path, f"active_source must be markdown or tex; got {active!r}")
    if stage in MARKDOWN_STAGES and active != "markdown":
        reporter.error("E-STAGE-SOURCE", path, f"paper_stage={stage} requires active_source=markdown")
    if stage in TEX_STAGES and active != "tex":
        reporter.error("E-STAGE-SOURCE", path, f"paper_stage={stage} requires active_source=tex")
    if active == "tex" and freeze.get("frozen") is not True:
        reporter.error("E-FREEZE", path, "active_source=tex requires freeze.frozen=true")

    draft_path = _source_path(
        root, data, "draft_source", "paper/draft/main.md", reporter, path
    )
    formal_path = _source_path(
        root, data, "formal_source", "paper/tex/main.tex", reporter, path
    )
    active_path = draft_path if active == "markdown" else formal_path
    if active in {"markdown", "tex"} and not active_path.is_file():
        reporter.error(
            "E-ACTIVE-SOURCE-FILE",
            active_path,
            f"active {active} source is missing",
        )

    for key in ("problem_definition", "research_state"):
        value = data.get(key)
        if value is not None and not isinstance(value, dict):
            reporter.error("E-PAPER-SCHEMA", path, f"{key} must be a mapping")

    claims = data.get("main_claims", [])
    claim_values: list[tuple[str, str]] = []
    if not isinstance(claims, list):
        reporter.error("E-CLAIMS", path, "main_claims must be a list")
        claims = []
    for index, claim in enumerate(claims):
        location = f"main_claims[{index}]"
        if not isinstance(claim, dict):
            reporter.error("E-CLAIM-SCHEMA", path, f"{location} must be a mapping")
            continue
        claim_id = str(claim.get("claim_id", ""))
        claim_values.append((claim_id, location))
        if not is_placeholder(claim_id) and not CLAIM_ID_RE.fullmatch(claim_id):
            reporter.error("E-CLAIM-ID", path, f"invalid claim ID: {claim_id!r}")
    claim_ids = ensure_unique(
        claim_values,
        reporter,
        path,
        code="E-DUPLICATE-CLAIM",
        label="claim ID",
    )

    for collection, reference_key, error_code in (
        ("main_contributions", "supporting_claims", "E-CONTRIBUTION-FK"),
        ("required_experiments", "supports_claims", "E-EXPERIMENT-FK"),
    ):
        items = data.get(collection, [])
        if not isinstance(items, list):
            reporter.error("E-PAPER-SCHEMA", path, f"{collection} must be a list")
            continue
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                reporter.error("E-PAPER-SCHEMA", path, f"{collection}[{index}] must be a mapping")
                continue
            references = item.get(reference_key, []) or []
            if not isinstance(references, list):
                reporter.error("E-PAPER-SCHEMA", path, f"{collection}[{index}].{reference_key} must be a list")
                continue
            for claim_id in references:
                if not is_placeholder(claim_id) and claim_id not in claim_ids:
                    reporter.error(error_code, path, f"{collection}[{index}] references unknown claim {claim_id!r}")

    human_gates = data.get("human_gates", {})
    if not isinstance(human_gates, dict):
        reporter.error("E-HUMAN-GATES", path, "human_gates must be a mapping")
        human_gates = {}
    else:
        for key, value in human_gates.items():
            if not isinstance(value, bool):
                reporter.error("E-HUMAN-GATE-TYPE", path, f"human_gates.{key} must be boolean")

    # Direction approval has one authority: idea_selection. A legacy
    # human_gates.idea_selection_approved field, if present in an older project,
    # is ignored instead of creating a second synchronized state.
    selection = data.get("idea_selection")
    if selection is not None:
        if not isinstance(selection, dict):
            reporter.error("E-IDEA-SELECTION", path, "idea_selection must be a mapping")
        else:
            approved = selection.get("approved")
            if not isinstance(approved, bool):
                reporter.error("E-IDEA-SELECTION", path, "idea_selection.approved must be boolean")
                approved = False
            selected_id = str(selection.get("selected_idea_id", ""))
            if not is_placeholder(selected_id) and not IDEA_ID_RE.fullmatch(selected_id):
                reporter.error("E-IDEA-SELECTION", path, f"invalid selected_idea_id: {selected_id!r}")
            if approved:
                if is_placeholder(selected_id):
                    reporter.error("E-IDEA-SELECTION", path, "approved idea selection requires selected_idea_id")
                approved_by = selection.get("approved_by", [])
                if not isinstance(approved_by, list) or not any(not is_placeholder(item) for item in approved_by):
                    reporter.error("E-IDEA-SELECTION", path, "approved idea selection requires approved_by")

    return data, claim_ids

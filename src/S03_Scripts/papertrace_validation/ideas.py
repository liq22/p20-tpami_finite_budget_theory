"""Validate optional first-input data and the idea candidate workspace."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .model import (
    Reporter,
    ensure_unique,
    is_placeholder,
    load_yaml,
    non_placeholder_rows,
    parse_markdown_table,
)

IDEA_ID_RE = re.compile(r"IDEA-\d+")
REF_ID_RE = re.compile(r"R\d+")
IDEA_STATUSES = {"proposed", "retained", "revised", "merged", "eliminated"}


def _mapping(
    parent: dict[str, Any],
    key: str,
    location: str,
    path: Path,
    reporter: Reporter,
) -> dict[str, Any]:
    value = parent.get(key)
    if isinstance(value, dict):
        return value
    reporter.error("E-IDEA-SCHEMA", path, f"{location}.{key} must be a mapping")
    return {}


def _require(
    mapping: dict[str, Any],
    key: str,
    location: str,
    path: Path,
    reporter: Reporter,
) -> None:
    if is_placeholder(mapping.get(key)):
        reporter.error("E-IDEA-CONTENT", path, f"{location}.{key} is required")


def _verified_refs(root: Path, reporter: Reporter) -> set[str]:
    path = root / "paper" / "refs" / "reading_matrix.md"
    if not path.is_file():
        return set()
    rows = parse_markdown_table(
        path,
        ["Ref ID", "Full text checked", "Status"],
        reporter,
        label="reading matrix",
        allow_empty=True,
    )
    return {
        row.get("Ref ID", "").strip()
        for row in non_placeholder_rows(rows, "Ref ID")
        if row.get("Status", "").strip() == "verified"
        and row.get("Full text checked", "").strip().lower() in {"yes", "true"}
    }


def _has_real_legacy_approval(value: Any) -> bool:
    if not isinstance(value, dict):
        return value is not None
    approved_by = value.get("approved_by", [])
    return value.get("approved_for_promotion") is True or (
        isinstance(approved_by, list)
        and any(not is_placeholder(item) for item in approved_by)
    )


def _validate_candidate(
    candidate: dict[str, Any],
    index: int,
    path: Path,
    reporter: Reporter,
    verified_refs: set[str],
) -> str:
    location = f"candidates[{index}]"
    idea_id = str(candidate.get("idea_id", ""))
    if not IDEA_ID_RE.fullmatch(idea_id):
        reporter.error("E-IDEA-ID", path, f"{location}.idea_id must match IDEA-<number>")

    decision = _mapping(candidate, "decision", location, path, reporter)
    status = str(decision.get("status", ""))
    if status not in IDEA_STATUSES:
        reporter.error(
            "E-IDEA-STATUS",
            path,
            f"{location}.decision.status must be one of {sorted(IDEA_STATUSES)}",
        )

    if _has_real_legacy_approval(candidate.get("approval")):
        reporter.error(
            "E-IDEA-AUTHORITY",
            path,
            f"{location}.approval duplicates paper/paper.yaml.idea_selection",
        )

    if status in {"retained", "revised"}:
        _require(candidate, "title", location, path, reporter)
        research_object = _mapping(candidate, "research_object", location, path, reporter)
        core_change = _mapping(candidate, "core_change", location, path, reporter)
        falsifiability = _mapping(candidate, "falsifiability", location, path, reporter)
        neighbor = _mapping(candidate, "nearest_neighbor", location, path, reporter)
        test = _mapping(candidate, "decisive_test", location, path, reporter)

        for key in ("current", "target", "unit_of_analysis"):
            _require(research_object, key, f"{location}.research_object", path, reporter)
        for key in ("before", "after", "changed_object"):
            _require(core_change, key, f"{location}.core_change", path, reporter)
        _require(candidate, "mechanism_sketch", location, path, reporter)
        for key in ("hypothesis", "observable_prediction", "rejection_condition"):
            _require(falsifiability, key, f"{location}.falsifiability", path, reporter)
        for key in ("ref_id", "irreducible_difference"):
            _require(neighbor, key, f"{location}.nearest_neighbor", path, reporter)
        for key in (
            "baseline",
            "intervention",
            "primary_metric",
            "mechanism_metric",
            "failure_signature",
        ):
            _require(test, key, f"{location}.decisive_test", path, reporter)
        _require(decision, "rationale", f"{location}.decision", path, reporter)

        ref_id = str(neighbor.get("ref_id", ""))
        if not is_placeholder(ref_id):
            if not REF_ID_RE.fullmatch(ref_id):
                reporter.error(
                    "E-IDEA-REF",
                    path,
                    f"{location}.nearest_neighbor.ref_id is invalid",
                )
            elif ref_id not in verified_refs:
                reporter.error(
                    "E-IDEA-REF",
                    path,
                    f"{location} uses unverified nearest-neighbor {ref_id}",
                )

    return idea_id


def _validate_optional_intake(path: Path, reporter: Reporter) -> None:
    if not path.is_file():
        return
    intake = load_yaml(path, reporter)
    if not isinstance(intake, dict):
        reporter.error("E-INTAKE-SCHEMA", path, "new_project_intake.yaml must be a mapping")
        return

    for key in ("project", "problem", "research_state", "scope"):
        if key in intake and not isinstance(intake.get(key), dict):
            reporter.error("E-INTAKE-SCHEMA", path, f"{key} must be a mapping")

    idea_workspace = intake.get("idea_workspace")
    if isinstance(idea_workspace, dict) and not is_placeholder(
        idea_workspace.get("selected_idea_id")
    ):
        reporter.error(
            "E-IDEA-AUTHORITY",
            path,
            "idea_workspace.selected_idea_id duplicates paper/paper.yaml.idea_selection",
        )


def _paper_selected_idea(root: Path, reporter: Reporter) -> tuple[str, Path]:
    path = root / "paper" / "paper.yaml"
    if not path.is_file():
        return "", path
    paper = load_yaml(path, reporter)
    if not isinstance(paper, dict):
        return "", path
    selection = paper.get("idea_selection")
    if not isinstance(selection, dict):
        return "", path
    return str(selection.get("selected_idea_id", "")), path


def validate_intake(root: Path, reporter: Reporter) -> None:
    intake_path = root / "paper" / "kickstart" / "new_project_intake.yaml"
    _validate_optional_intake(intake_path, reporter)

    workspace_path = root / "paper" / "kickstart" / "idea_candidates.yaml"
    if not workspace_path.is_file():
        return
    workspace = load_yaml(workspace_path, reporter)
    if not isinstance(workspace, dict):
        reporter.error(
            "E-IDEA-SCHEMA",
            workspace_path,
            "idea_candidates.yaml must be a mapping",
        )
        return
    if workspace.get("schema_version") != 2:
        reporter.error(
            "E-IDEA-VERSION",
            workspace_path,
            "idea_candidates.yaml schema_version must be 2",
        )

    candidates = workspace.get("candidates", [])
    if not isinstance(candidates, list):
        reporter.error("E-IDEA-CANDIDATES", workspace_path, "candidates must be a list")
        return

    verified_refs = _verified_refs(root, reporter)
    ids: list[tuple[str, str]] = []
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            reporter.error(
                "E-IDEA-SCHEMA",
                workspace_path,
                f"candidates[{index}] must be a mapping",
            )
            continue
        idea_id = _validate_candidate(
            candidate,
            index,
            workspace_path,
            reporter,
            verified_refs,
        )
        ids.append((idea_id, f"candidates[{index}]"))

    known_ids = ensure_unique(
        ids,
        reporter,
        workspace_path,
        code="E-DUPLICATE-IDEA",
        label="idea ID",
    )

    provisional_id = str(workspace.get("provisional_front_runner_id", ""))
    if not is_placeholder(provisional_id) and provisional_id not in known_ids:
        reporter.error(
            "E-INTAKE-IDEA-FK",
            workspace_path,
            f"provisional front-runner does not exist: {provisional_id}",
        )

    legacy_selected = str(workspace.get("selected_candidate_id", ""))
    if not is_placeholder(legacy_selected):
        reporter.error(
            "E-IDEA-AUTHORITY",
            workspace_path,
            "selected_candidate_id duplicates paper/paper.yaml.idea_selection",
        )

    selected_id, selected_path = _paper_selected_idea(root, reporter)
    if not is_placeholder(selected_id) and selected_id not in known_ids:
        reporter.error(
            "E-INTAKE-IDEA-FK",
            selected_path,
            f"selected idea does not exist: {selected_id}",
        )

"""Validate only decision-relevant scientific method fields."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .model import Reporter, ensure_unique, is_placeholder, load_yaml

METHOD_PATH = Path("paper/method/method_spec.yaml")
METHOD_SCHEMA_VERSION = 1
METHOD_STATUSES = {"draft", "ready"}
ORIGIN_TYPES = {"promoted_idea", "direct_problem"}
THEORY_STATUSES = {"hypothesis", "analysis", "proposition"}
METHOD_ID_RE = re.compile(r"METH-\d+")
COMPONENT_ID_RE = re.compile(r"MC-\d+")
IDEA_ID_RE = re.compile(r"IDEA-\d+")
CLAIM_ID_RE = re.compile(r"C\d+")


def _mapping(
    parent: dict[str, Any],
    key: str,
    path: Path,
    reporter: Reporter,
) -> dict[str, Any]:
    value = parent.get(key)
    if isinstance(value, dict):
        return value
    reporter.error("E-METHOD-SCHEMA", path, f"{key} must be a mapping")
    return {}


def _require(
    mapping: dict[str, Any],
    key: str,
    location: str,
    path: Path,
    reporter: Reporter,
) -> None:
    if is_placeholder(mapping.get(key)):
        reporter.error("E-METHOD-READY", path, f"{location}.{key} is required")


def validate_method_design(
    root: Path,
    reporter: Reporter,
    paper: dict[str, Any],
    claim_ids: set[str],
) -> None:
    """Validate a ready method as a falsifiable scientific specification.

    Components and assumptions are representation-dependent. They are checked
    only when the method actually uses them; every ready method still needs a
    real failure, competing explanations, a minimal intervention, observable
    predictions, a fair comparison, metrics, and a boundary.
    """
    del paper
    path = root / METHOD_PATH
    if not path.is_file():
        return

    data = load_yaml(path, reporter)
    if not isinstance(data, dict):
        reporter.error("E-METHOD-SCHEMA", path, "method_spec.yaml must be a mapping")
        return

    if data.get("schema_version") != METHOD_SCHEMA_VERSION:
        reporter.error("E-METHOD-VERSION", path, "schema_version must be 1")

    method_id = str(data.get("method_id", ""))
    if not is_placeholder(method_id) and not METHOD_ID_RE.fullmatch(method_id):
        reporter.error("E-METHOD-ID", path, "method_id must match METH-<number>")

    status = str(data.get("status", ""))
    if status not in METHOD_STATUSES:
        reporter.error("E-METHOD-STATUS", path, f"status must be one of {sorted(METHOD_STATUSES)}")

    origin = _mapping(data, "origin", path, reporter)
    origin_type = str(origin.get("type", ""))
    if origin_type not in ORIGIN_TYPES:
        reporter.error("E-METHOD-ORIGIN", path, f"origin.type must be one of {sorted(ORIGIN_TYPES)}")
    source_idea_id = str(origin.get("source_idea_id", ""))
    if not is_placeholder(source_idea_id) and not IDEA_ID_RE.fullmatch(source_idea_id):
        reporter.error("E-METHOD-ORIGIN", path, "origin.source_idea_id must match IDEA-<number> or remain TODO")

    supports_claims = data.get("supports_claims", [])
    if not isinstance(supports_claims, list) or not all(isinstance(item, str) for item in supports_claims):
        reporter.error("E-METHOD-SCHEMA", path, "supports_claims must be a string list")
        supports_claims = []
    for claim_id in supports_claims:
        if is_placeholder(claim_id):
            continue
        if not CLAIM_ID_RE.fullmatch(claim_id):
            reporter.error("E-METHOD-CLAIM", path, f"invalid claim ID: {claim_id}")
        elif claim_id not in claim_ids:
            reporter.error("E-METHOD-CLAIM-FK", path, f"unknown claim: {claim_id}")

    failure = _mapping(data, "failure", path, reporter)
    job = _mapping(data, "scientific_job", path, reporter)
    mechanism = _mapping(data, "mechanism", path, reporter)
    evaluation = _mapping(data, "evaluation_contract", path, reporter)

    components = data.get("components", [])
    if not isinstance(components, list):
        reporter.error("E-METHOD-COMPONENT", path, "components must be a list")
        components = []
    component_ids: list[tuple[str, str]] = []
    for index, component in enumerate(components):
        location = f"components[{index}]"
        if not isinstance(component, dict):
            reporter.error("E-METHOD-COMPONENT", path, f"{location} must be a mapping")
            continue
        component_id = str(component.get("component_id", ""))
        component_ids.append((component_id, location))
        if not is_placeholder(component_id) and not COMPONENT_ID_RE.fullmatch(component_id):
            reporter.error("E-METHOD-COMPONENT", path, f"{location}.component_id must match MC-<number>")
    ensure_unique(
        component_ids,
        reporter,
        path,
        code="E-DUPLICATE-METHOD-COMPONENT",
        label="method component ID",
    )

    if status != "ready":
        return

    if not METHOD_ID_RE.fullmatch(method_id):
        reporter.error("E-METHOD-READY", path, "ready method requires a valid method_id")
    if origin_type == "promoted_idea" and not IDEA_ID_RE.fullmatch(source_idea_id):
        reporter.error("E-METHOD-READY", path, "ready promoted method requires source_idea_id")

    for key in (
        "observed_failure_or_contradiction",
        "why_it_matters",
        "favored_explanation",
        "strongest_competing_explanation",
    ):
        _require(failure, key, "failure", path, reporter)

    for key in ("research_question", "target_decision", "unit_of_analysis"):
        _require(job, key, "scientific_job", path, reporter)

    for key in (
        "changed_object",
        "minimal_intervention",
        "testable_implication",
        "expected_signature",
        "rejection_signature",
        "boundary_signature",
    ):
        _require(mechanism, key, "mechanism", path, reporter)

    theory_status = str(mechanism.get("theory_status", ""))
    if theory_status not in THEORY_STATUSES:
        reporter.error(
            "E-METHOD-READY",
            path,
            f"mechanism.theory_status must be one of {sorted(THEORY_STATUSES)}",
        )
    assumptions = mechanism.get("assumptions", [])
    if not isinstance(assumptions, list):
        reporter.error("E-METHOD-SCHEMA", path, "mechanism.assumptions must be a list")
    elif theory_status == "proposition" and not any(
        not is_placeholder(item) for item in assumptions
    ):
        reporter.error(
            "E-METHOD-READY",
            path,
            "mechanism.assumptions requires at least one value for proposition-level claims",
        )

    for key in (
        "decisive_comparison",
        "baseline_fairness",
        "primary_metric",
        "property_metric",
        "boundary_test",
    ):
        _require(evaluation, key, "evaluation_contract", path, reporter)

    for index, component in enumerate(components):
        if not isinstance(component, dict):
            continue
        if not COMPONENT_ID_RE.fullmatch(str(component.get("component_id", ""))):
            reporter.error("E-METHOD-READY", path, f"components[{index}] requires a valid component_id")
        for key in ("scientific_role", "strongest_alternative", "deletion_test"):
            _require(component, key, f"components[{index}]", path, reporter)

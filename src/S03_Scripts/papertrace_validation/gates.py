"""Minimal checks for consequential paper-stage transitions."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .model import STAGE_RANK, Reporter, is_placeholder


def _require_value(data: dict[str, Any], path: list[str]) -> bool:
    current: Any = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return False
        current = current[key]
    return not is_placeholder(current)


def _has_central_question(paper: dict[str, Any]) -> bool:
    # research_state is the current authority. The legacy top-level key remains
    # readable so existing projects do not need a migration script.
    return _require_value(paper, ["research_state", "central_question"]) or _require_value(
        paper, ["research_question"]
    )


def _require_confirmation(
    paper: dict[str, Any],
    name: str,
    stage: str,
    reporter: Reporter,
    paper_path: Path,
) -> None:
    confirmations = paper.get("human_gates")
    if not isinstance(confirmations, dict) or confirmations.get(name) is not True:
        reporter.error(
            "E-STAGE-CONFIRMATION",
            paper_path,
            f"paper_stage={stage} requires human_gates.{name}=true",
        )


def validate_stage_gates(
    root: Path,
    reporter: Reporter,
    paper: dict[str, Any],
    gate_state: dict[str, Any] | None = None,
) -> None:
    """Protect source freeze and external submission without blocking research."""
    del gate_state
    stage = paper.get("paper_stage")
    if stage not in STAGE_RANK:
        return
    rank = STAGE_RANK[stage]
    paper_path = root / "paper" / "paper.yaml"

    # An outline needs a question, but not a finalized title, venue, claims,
    # method, experiment, author list, or approval package.
    if rank >= STAGE_RANK["outline"] and not _has_central_question(paper):
        reporter.error(
            "E-STAGE-TODO",
            paper_path,
            f"paper_stage={stage} requires research_state.central_question",
        )

    # Markdown -> TeX is a one-way formal-source transition in PaperTrace.
    if rank >= STAGE_RANK["tex_formalization"]:
        _require_confirmation(
            paper,
            "markdown_freeze_approved",
            stage,
            reporter,
            paper_path,
        )
        freeze = paper.get("freeze") if isinstance(paper.get("freeze"), dict) else {}
        if freeze.get("frozen") is not True:
            reporter.error(
                "E-STAGE-FREEZE",
                paper_path,
                f"paper_stage={stage} requires freeze.frozen=true",
            )

    # Submission is an external consequential action and retains all-author
    # confirmation. Readiness details remain the submission skill's job.
    if rank >= STAGE_RANK["submission_ready"]:
        _require_confirmation(
            paper,
            "submission_approved_by_all_authors",
            stage,
            reporter,
            paper_path,
        )

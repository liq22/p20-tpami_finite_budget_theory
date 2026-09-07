from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "S03_Scripts"))

from papertrace_validation.ideas import validate_intake  # noqa: E402
from papertrace_validation.model import Reporter  # noqa: E402
from papertrace_validation.project import validate_paper_state  # noqa: E402


def proposed_candidate() -> dict:
    return {
        "idea_id": "IDEA-001",
        "title": "TODO",
        "decision": {"status": "proposed", "rationale": "TODO"},
    }


def retained_candidate() -> dict:
    return {
        "idea_id": "IDEA-001",
        "title": "Constructive conservation",
        "research_object": {
            "current": "soft conservation penalty",
            "target": "exact conservation by construction",
            "unit_of_analysis": "predicted state transition",
        },
        "core_change": {
            "before": "penalize conservation violations",
            "after": "parameterize only conservation-valid outputs",
            "changed_object": "structural constraint",
        },
        "mechanism_sketch": "closed parameterization restricts outputs to valid states",
        "falsifiability": {
            "hypothesis": "constructive validity improves shifted-domain robustness",
            "observable_prediction": "lower violation and lower shifted-domain error",
            "rejection_condition": "a matched soft penalty performs equivalently",
        },
        "nearest_neighbor": {
            "ref_id": "R1",
            "irreducible_difference": "validity is guaranteed rather than penalized",
        },
        "decisive_test": {
            "baseline": "capacity-matched soft penalty",
            "intervention": "closed parameterization",
            "primary_metric": "shifted-domain error",
            "mechanism_metric": "conservation violation",
            "failure_signature": "no property or task advantage",
        },
        "decision": {
            "status": "retained",
            "rationale": "the mechanism is testable against a matched alternative",
        },
    }


class IdeaWorkflowValidationTests(unittest.TestCase):
    def _root(
        self,
        candidate: dict,
        *,
        ref_status: str = "verified",
        checked: str = "yes",
        selected: str = "TODO",
        include_intake: bool = True,
    ) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        kickstart = root / "paper/kickstart"
        refs = root / "paper/refs"
        kickstart.mkdir(parents=True)
        refs.mkdir(parents=True)

        if include_intake:
            intake = {
                "schema_version": 2,
                "project": {},
                "problem": {},
                "research_state": {},
                "scope": {},
            }
            (kickstart / "new_project_intake.yaml").write_text(
                yaml.safe_dump(intake, sort_keys=False),
                encoding="utf-8",
            )

        workspace = {
            "schema_version": 2,
            "provisional_front_runner_id": "TODO",
            "candidates": [candidate],
        }
        (kickstart / "idea_candidates.yaml").write_text(
            yaml.safe_dump(workspace, sort_keys=False),
            encoding="utf-8",
        )
        (root / "paper/paper.yaml").write_text(
            yaml.safe_dump(
                {
                    "idea_selection": {
                        "selected_idea_id": selected,
                        "approved": False,
                        "approved_by": [],
                    }
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        (refs / "reading_matrix.md").write_text(
            "# Reading Matrix\n\n"
            "| Ref ID | Full text checked | Status |\n"
            "|---|---|---|\n"
            f"| R1 | {checked} | {ref_status} |\n",
            encoding="utf-8",
        )
        return root

    def test_proposed_placeholder_candidate_is_valid(self) -> None:
        root = self._root(proposed_candidate())
        reporter = Reporter(root)
        validate_intake(root, reporter)
        self.assertEqual([], reporter.errors)

    def test_candidate_workspace_validates_without_intake(self) -> None:
        root = self._root(proposed_candidate(), include_intake=False)
        reporter = Reporter(root)
        validate_intake(root, reporter)
        self.assertEqual([], reporter.errors)

    def test_retained_candidate_requires_scientific_content(self) -> None:
        candidate = retained_candidate()
        candidate["mechanism_sketch"] = "TODO"
        root = self._root(candidate)
        reporter = Reporter(root)
        validate_intake(root, reporter)
        self.assertIn("E-IDEA-CONTENT", {issue.code for issue in reporter.errors})

    def test_retained_candidate_requires_verified_neighbour(self) -> None:
        root = self._root(retained_candidate(), ref_status="screened", checked="no")
        reporter = Reporter(root)
        validate_intake(root, reporter)
        self.assertIn("E-IDEA-REF", {issue.code for issue in reporter.errors})

    def test_complete_retained_candidate_is_valid(self) -> None:
        root = self._root(retained_candidate(), selected="IDEA-001")
        reporter = Reporter(root)
        validate_intake(root, reporter)
        self.assertEqual([], reporter.errors)

    def test_legacy_candidate_approval_is_rejected(self) -> None:
        candidate = retained_candidate()
        candidate["approval"] = {
            "approved_for_promotion": True,
            "approved_by": ["author"],
        }
        root = self._root(candidate, selected="IDEA-001")
        reporter = Reporter(root)
        validate_intake(root, reporter)
        self.assertIn("E-IDEA-AUTHORITY", {issue.code for issue in reporter.errors})

    def test_unknown_paper_selection_is_rejected(self) -> None:
        root = self._root(proposed_candidate(), selected="IDEA-999")
        reporter = Reporter(root)
        validate_intake(root, reporter)
        self.assertIn("E-INTAKE-IDEA-FK", {issue.code for issue in reporter.errors})

    def test_paper_approval_requires_selected_idea_and_author(self) -> None:
        root = self._root(retained_candidate())
        paper = {
            "paper_stage": "idea",
            "active_source": "markdown",
            "freeze": {"frozen": False},
            "main_claims": [],
            "main_contributions": [],
            "required_experiments": [],
            "idea_selection": {
                "selected_idea_id": "IDEA-001",
                "approved": True,
                "approved_by": [],
            },
            "human_gates": {
                "markdown_freeze_approved": False,
                "submission_approved_by_all_authors": False,
            },
        }
        path = root / "paper/paper.yaml"
        path.write_text(yaml.safe_dump(paper, sort_keys=False), encoding="utf-8")
        reporter = Reporter(root)
        validate_paper_state(root, reporter)
        self.assertIn("E-IDEA-SELECTION", {issue.code for issue in reporter.errors})


if __name__ == "__main__":
    unittest.main()

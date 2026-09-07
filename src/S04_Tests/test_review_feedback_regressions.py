from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "src" / "S03_Scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from papertrace_validation.ideas import validate_intake  # noqa: E402
from papertrace_validation.model import Reporter  # noqa: E402
from papertrace_validation.project import validate_paper_state  # noqa: E402


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


skill_evals = load_module(
    "papertrace_review_skill_evals",
    ROOT / ".agent/scripts/validate_skill_evals.py",
)


class ReviewFeedbackRegressionTests(unittest.TestCase):
    def _candidate(self) -> dict:
        return {
            "idea_id": "IDEA-001",
            "title": "TODO",
            "research_object": {
                "current": "TODO",
                "target": "TODO",
                "unit_of_analysis": "TODO",
            },
            "core_change": {
                "before": "TODO",
                "after": "TODO",
                "changed_object": "TODO",
            },
            "mechanism_sketch": "TODO",
            "falsifiability": {
                "hypothesis": "TODO",
                "observable_prediction": "TODO",
                "rejection_condition": "TODO",
            },
            "nearest_neighbor": {
                "ref_id": "TODO",
                "irreducible_difference": "TODO",
            },
            "decisive_test": {
                "baseline": "TODO",
                "intervention": "TODO",
                "primary_metric": "TODO",
                "mechanism_metric": "TODO",
                "failure_signature": "TODO",
            },
            "decision": {
                "status": "proposed",
                "rationale": "TODO",
            },
        }

    def _idea_root(self, candidate: dict, *, selected: str = "TODO") -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        kickstart = root / "paper/kickstart"
        refs = root / "paper/refs"
        kickstart.mkdir(parents=True)
        refs.mkdir(parents=True)
        (kickstart / "new_project_intake.yaml").write_text(
            yaml.safe_dump(
                {
                    "schema_version": 2,
                    "project": {},
                    "problem": {},
                    "research_state": {},
                    "scope": {},
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        (kickstart / "idea_candidates.yaml").write_text(
            yaml.safe_dump(
                {
                    "schema_version": 2,
                    "provisional_front_runner_id": "TODO",
                    "candidates": [candidate],
                },
                sort_keys=False,
            ),
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
            "# Reading\n\n"
            "| Ref ID | Full text checked | Status |\n"
            "|---|---|---|\n"
            "| R1 | yes | verified |\n",
            encoding="utf-8",
        )
        return root

    def test_unknown_selected_idea_is_rejected(self) -> None:
        root = self._idea_root(self._candidate(), selected="IDEA-999")
        reporter = Reporter(root)
        validate_intake(root, reporter)
        self.assertIn("E-INTAKE-IDEA-FK", {issue.code for issue in reporter.errors})

    def test_retained_idea_requires_scientific_content(self) -> None:
        candidate = self._candidate()
        candidate["decision"]["status"] = "retained"
        root = self._idea_root(candidate)
        reporter = Reporter(root)
        validate_intake(root, reporter)
        self.assertIn("E-IDEA-CONTENT", {issue.code for issue in reporter.errors})

    def test_legacy_intake_selection_is_rejected(self) -> None:
        root = self._idea_root(self._candidate())
        path = root / "paper/kickstart/new_project_intake.yaml"
        intake = yaml.safe_load(path.read_text(encoding="utf-8"))
        intake["idea_workspace"] = {"selected_idea_id": "IDEA-001"}
        path.write_text(yaml.safe_dump(intake, sort_keys=False), encoding="utf-8")
        reporter = Reporter(root)
        validate_intake(root, reporter)
        self.assertIn("E-IDEA-AUTHORITY", {issue.code for issue in reporter.errors})

    def test_paper_direction_approval_has_single_authority(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / "paper/draft").mkdir(parents=True)
        (root / "paper/draft/main.md").write_text("# Draft\n", encoding="utf-8")
        paper = yaml.safe_load((ROOT / "paper/paper.yaml").read_text(encoding="utf-8"))
        paper["idea_selection"] = {
            "selected_idea_id": "TODO",
            "approved": True,
            "approved_by": [],
        }
        (root / "paper/paper.yaml").write_text(
            yaml.safe_dump(paper, sort_keys=False),
            encoding="utf-8",
        )
        reporter = Reporter(root)
        validate_paper_state(root, reporter)
        self.assertIn("E-IDEA-SELECTION", {issue.code for issue in reporter.errors})

    def test_definition_validation_does_not_claim_host_execution(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = skill_evals.main([])
        self.assertEqual(0, result)
        text = output.getvalue()
        self.assertIn("definitions only", text)
        self.assertIn("behavior not executed", text)

    def test_failed_explicit_routing_results_return_nonzero(self) -> None:
        routing, errors = skill_evals.load_cases(
            ROOT / ".agent/evals/skill_trigger_cases.yaml"
        )
        products, product_errors = skill_evals.load_product_cases(
            ROOT / ".agent/evals/product_surface_cases.yaml"
        )
        self.assertEqual([], errors + product_errors)
        with tempfile.TemporaryDirectory() as directory:
            results = Path(directory) / "results.jsonl"
            rows = [
                {"case_id": case_id, "selected_primary": "none"}
                for case_id in routing
            ]
            rows.extend(
                {
                    "case_id": case_id,
                    "selected_primary": "none",
                    "primary_surface": "governance",
                    "product_changed": False,
                    "audit_used": False,
                    "user_visible_summary": "no product",
                }
                for case_id in products
            )
            results.write_text(
                "\n".join(json.dumps(row) for row in rows) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(1, skill_evals.main(["--results", str(results)]))

    def test_main_product_routes_have_definition_coverage(self) -> None:
        cases, errors = skill_evals.load_cases(
            ROOT / ".agent/evals/skill_trigger_cases.yaml"
        )
        self.assertEqual([], errors)
        expected = {case["expected_primary"] for case in cases.values()}
        self.assertIn("method-design", expected)
        self.assertIn("code-change", expected)
        self.assertIn("code-module-xray", expected)

    def test_aris_backend_remains_hidden_in_product_case(self) -> None:
        cases, errors = skill_evals.load_product_cases(
            ROOT / ".agent/evals/product_surface_cases.yaml"
        )
        self.assertEqual([], errors)
        case = cases["PRODUCT-ARIS-EXECUTION-001"]
        self.assertTrue(case["must_change_product"])
        self.assertFalse(case["audit_allowed"])
        self.assertIn("backend routing", case["must_not_surface"])


if __name__ == "__main__":
    unittest.main()

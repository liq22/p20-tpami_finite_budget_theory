from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "src" / "S03_Scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from papertrace_validation.figures import validate_figure_arguments  # noqa: E402
from papertrace_validation.methods import validate_method_design  # noqa: E402
from papertrace_validation.model import Reporter  # noqa: E402


class ResearchDesignContractTests(unittest.TestCase):
    def test_template_method_and_figure_contracts_validate(self) -> None:
        paper = yaml.safe_load((ROOT / "paper/paper.yaml").read_text(encoding="utf-8"))
        reporter = Reporter(ROOT)
        validate_method_design(ROOT, reporter, paper, set())
        validate_figure_arguments(ROOT, reporter)
        self.assertEqual([], reporter.errors)

    def _ready_method(self) -> dict:
        return {
            "schema_version": 1,
            "method_id": "METH-001",
            "status": "ready",
            "origin": {"type": "direct_problem", "source_idea_id": "TODO"},
            "supports_claims": [],
            "failure": {
                "observed_failure_or_contradiction": "baseline fails under unseen speed",
                "why_it_matters": "the generalization decision depends on it",
                "favored_explanation": "shared bands are entangled with environment",
                "strongest_competing_explanation": "the effect is only extra capacity",
            },
            "scientific_job": {
                "research_question": "Does the intervention improve robustness?",
                "target_decision": "retain or reject the mechanism",
                "unit_of_analysis": "machine run",
            },
            "mechanism": {
                "changed_object": "frequency-aware representation",
                "minimal_intervention": "separate shared and private observable bands",
                "theory_status": "hypothesis",
                "assumptions": [],
                "testable_implication": "shared embeddings remain aligned under shift",
                "expected_signature": "paired shared embeddings remain aligned",
                "rejection_signature": "alignment disappears under matched controls",
                "boundary_signature": "advantage vanishes when shared bands do not overlap",
            },
            "components": [],
            "evaluation_contract": {
                "decisive_comparison": "matched-capacity tokenizer with and without split",
                "baseline_fairness": "same split, inputs, preprocessing and budget",
                "primary_metric": "held-out AUROC",
                "property_metric": "paired shared-space cosine similarity",
                "boundary_test": "non-overlapping observable bands",
            },
        }

    def _write_method(self, root: Path, data: dict) -> None:
        path = root / "paper/method/method_spec.yaml"
        path.parent.mkdir(parents=True)
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def test_ready_empirical_method_allows_empty_components_and_assumptions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_method(root, self._ready_method())
            reporter = Reporter(root)
            validate_method_design(root, reporter, {}, set())
            self.assertEqual([], reporter.errors)

    def test_ready_method_requires_observed_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = self._ready_method()
            data["failure"]["observed_failure_or_contradiction"] = "TODO"
            self._write_method(root, data)
            reporter = Reporter(root)
            validate_method_design(root, reporter, {}, set())
            self.assertIn("E-METHOD-READY", {issue.code for issue in reporter.errors})

    def test_proposition_requires_explicit_assumptions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = self._ready_method()
            data["mechanism"]["theory_status"] = "proposition"
            self._write_method(root, data)
            reporter = Reporter(root)
            validate_method_design(root, reporter, {}, set())
            self.assertIn("E-METHOD-READY", {issue.code for issue in reporter.errors})

    def test_declared_component_requires_deletion_test(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = self._ready_method()
            data["components"] = [
                {
                    "component_id": "MC-01",
                    "scientific_role": "separate shared/private bands",
                    "strongest_alternative": "fixed patch tokenizer",
                    "deletion_test": "TODO",
                }
            ]
            self._write_method(root, data)
            reporter = Reporter(root)
            validate_method_design(root, reporter, {}, set())
            self.assertIn("E-METHOD-READY", {issue.code for issue in reporter.errors})

    def test_drafted_figure_requires_reader_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "paper/assets/figures/figure_manifest.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                """# Figure Manifest

| Figure ID | Reader question | Key message | Comparison / encoding | Interpretation boundary | Status |
|---|---|---|---|---|---|
| F1 | TODO | Main method is more stable | aligned position | tested setting only | drafted |
""",
                encoding="utf-8",
            )
            reporter = Reporter(root)
            validate_figure_arguments(root, reporter)
            self.assertIn("E-FIGURE-ARGUMENT", {issue.code for issue in reporter.errors})


if __name__ == "__main__":
    unittest.main()

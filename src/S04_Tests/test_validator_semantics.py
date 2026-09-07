from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "S03_Scripts" / "validate_project.py"
SPEC = importlib.util.spec_from_file_location("papertrace_validate_project", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


ROUTER = """---
name: 00-router
description: Test fixture router.
---

## Purpose
Route.
## Workflow
Execute.
## Output Contract
Product.
## Boundaries
No audit drift.
"""


class ValidatorFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        (root / ".agent/skills/00-router").mkdir(parents=True)
        (root / "paper/draft").mkdir(parents=True)
        self.write("README.md", "# Test\n")
        self.write("AGENTS.md", "# Agents\n")
        self.write(".agent/skills/00-router/SKILL.md", ROUTER)
        self.write(
            "paper/paper.yaml",
            """schema_version: 1
paper_stage: idea
active_source: markdown
draft_source:
  path: paper/draft/main.md
formal_source:
  path: paper/tex/main.tex
freeze:
  frozen: false
idea_selection:
  selected_idea_id: TODO
  approved: false
  approved_by: []
problem_definition: {}
research_state:
  central_question: TODO
main_claims: []
main_contributions: []
required_experiments: []
human_gates:
  markdown_freeze_approved: false
  submission_approved_by_all_authors: false
""",
        )
        self.write("paper/draft/main.md", "# Draft\n")

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def replace(self, relative: str, old: str, new: str) -> None:
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        if old not in text:
            raise AssertionError(f"replacement target not found in {relative}: {old!r}")
        path.write_text(text.replace(old, new), encoding="utf-8")

    def add_claim(self) -> None:
        self.replace(
            "paper/paper.yaml",
            "main_claims: []",
            """main_claims:
  - claim_id: C1
    text: claim
    status: hypothesis
    evidence_state: exploratory-evidence
    hypothesis_provenance: unknown
    boundary: bounded""",
        )

    def error_codes(self) -> set[str]:
        return {issue.code for issue in validator.validate(self.root).errors}

    def add_run_and_evidence(self, run_status: str, output_path: str = "outputs/result.csv") -> None:
        self.add_claim()
        self.write(
            "paper/experiments/run_ledger.md",
            f"""# Runs

| Run ID | Date | Code version | Config | Data/version | Seed | Primary metric | Result | Status | Output path |
|---|---|---|---|---|---|---|---|---|---|
| RUN-0001 | 2026-08-11 | abc | cfg.yaml | data-v1 | 7 | accuracy | 0.9 | {run_status} | {output_path} |
""",
        )
        self.write(
            "paper/experiments/evidence_matrix.md",
            """# Support

| Claim ID | Strength | Evidence ID | Run/ref/artifact | Boundary | Status |
|---|---|---|---|---|---|
| C1 | weak | E1 | RUN-0001 | bounded | supported |
""",
        )


class ProjectValidatorSemanticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.fixture = ValidatorFixture(Path(self.tempdir.name))

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_minimal_idea_workspace_passes_without_lifecycle_records(self) -> None:
        reporter = validator.validate(self.fixture.root)
        self.assertEqual([], reporter.errors, "\n".join(str(issue) for issue in reporter.errors))

    def test_missing_active_source_fails(self) -> None:
        (self.fixture.root / "paper/draft/main.md").unlink()
        self.assertIn("E-ACTIVE-SOURCE-FILE", self.fixture.error_codes())

    def test_planned_run_cannot_support_positive_claim(self) -> None:
        self.fixture.add_run_and_evidence("planned")
        self.assertIn("E-NON-SUPPORTING-RUN", self.fixture.error_codes())

    def test_completed_run_can_support_positive_claim(self) -> None:
        self.fixture.add_run_and_evidence("completed")
        self.assertNotIn("E-NON-SUPPORTING-RUN", self.fixture.error_codes())

    def test_completed_run_requires_output_path(self) -> None:
        self.fixture.add_run_and_evidence("completed", "TODO")
        self.assertIn("E-COMPLETED-RUN-FIELD", self.fixture.error_codes())

    def test_unverified_reference_cannot_support_positive_claim(self) -> None:
        self.fixture.add_claim()
        self.fixture.write(
            "paper/refs/reading_matrix.md",
            """# Reading

| Ref ID | Bib key | Verified source | Main evidence | Limitation | Supports/refutes claim | Full text checked | Status |
|---|---|---|---|---|---|---|---|
| R1 | key | doi | result | limit | C1 | no | screened |
""",
        )
        self.fixture.write(
            "paper/experiments/evidence_matrix.md",
            """# Support

| Claim ID | Strength | Evidence ID | Run/ref/artifact | Boundary | Status |
|---|---|---|---|---|---|
| C1 | weak | E1 | R1 | bounded | supported |
""",
        )
        self.assertIn("E-NON-VERIFIED-REF", self.fixture.error_codes())

    def test_generated_figure_requires_actual_scientific_fields(self) -> None:
        self.fixture.write(
            "paper/assets/figures/figure_manifest.md",
            """# Figures

| Figure ID | File path | Reader question | Key message | Comparison / encoding | Interpretation boundary | Claim ref | Evidence ref | Source data/output | First callout | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| F1 | TODO | What changes? | TODO | position | tested setting |  |  | TODO | TODO | generated |
""",
        )
        codes = self.fixture.error_codes()
        self.assertIn("E-FIGURE-ARGUMENT", codes)
        self.assertIn("E-FIGURE-READY-FIELD", codes)

    def test_markdown_draft_requires_question_not_approval(self) -> None:
        self.fixture.replace("paper/paper.yaml", "paper_stage: idea", "paper_stage: markdown_draft")
        self.fixture.replace("paper/paper.yaml", "central_question: TODO", "central_question: Why does the baseline fail?")
        codes = self.fixture.error_codes()
        self.assertNotIn("E-STAGE-CONFIRMATION", codes)
        self.assertNotIn("E-STAGE-TODO", codes)

    def test_tex_transition_requires_author_confirmation(self) -> None:
        self.fixture.replace("paper/paper.yaml", "paper_stage: idea", "paper_stage: tex_formalization")
        self.fixture.replace("paper/paper.yaml", "active_source: markdown", "active_source: tex")
        self.fixture.replace("paper/paper.yaml", "central_question: TODO", "central_question: Why does the baseline fail?")
        self.fixture.replace("paper/paper.yaml", "frozen: false", "frozen: true")
        self.fixture.write("paper/tex/main.tex", "\\documentclass{article}\n")
        self.assertIn("E-STAGE-CONFIRMATION", self.fixture.error_codes())


if __name__ == "__main__":
    unittest.main()

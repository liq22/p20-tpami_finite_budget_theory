from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


skill_evals = load_module(
    "papertrace_skill_evals", ROOT / ".agent/scripts/validate_skill_evals.py"
)
wrapper_generator = load_module(
    "papertrace_wrapper_generator",
    ROOT / ".agent/scripts/generate_agent_skill_wrappers.py",
)
wrapper_validator = load_module(
    "papertrace_wrapper_validator",
    ROOT / ".agent/scripts/validate_agent_skill_wrappers.py",
)


class SkillEvalTests(unittest.TestCase):
    def test_perfect_results_score_cleanly(self) -> None:
        cases, errors = skill_evals.load_cases(ROOT / ".agent/evals/skill_trigger_cases.yaml")
        self.assertEqual([], errors)
        results = {
            case_id: {"case_id": case_id, "selected_primary": case["expected_primary"]}
            for case_id, case in cases.items()
        }
        metrics = skill_evals.score_routing(cases, results)
        self.assertEqual(1.0, metrics["exact_accuracy"])
        self.assertEqual(0, metrics["prohibited_triggers"])

    def test_prohibited_route_fails_a_critical_case(self) -> None:
        cases, errors = skill_evals.load_cases(ROOT / ".agent/evals/skill_trigger_cases.yaml")
        self.assertEqual([], errors)
        results = {
            case_id: {"case_id": case_id, "selected_primary": case["expected_primary"]}
            for case_id, case in cases.items()
        }
        results["RQ-001"]["selected_primary"] = "06-experiment-ops"
        metrics = skill_evals.score_routing(cases, results)
        self.assertGreater(metrics["prohibited_triggers"], 0)
        self.assertTrue(metrics["critical_failures"])

    def test_embedded_grill_me_evals_validate(self) -> None:
        summaries, errors = skill_evals.validate_embedded_evals(ROOT / ".agent/skills")
        self.assertEqual([], errors)
        self.assertIn("grill-me", summaries)
        self.assertGreater(summaries["grill-me"]["output_evals"], 0)
        self.assertGreater(summaries["grill-me"]["trigger_queries"], 0)


class WrapperToolingTests(unittest.TestCase):
    def _make_repo(self, root: Path) -> None:
        skill_dir = root / ".agent" / "skills" / "grill-me"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            """---
name: grill-me
description: 'Explicit trigger: pressure-test one decision at a time.'
license: MIT
metadata:
  version: '2.1.0'
---

# Grill Me

## Purpose
Test.
## Workflow
Test.
## Output Contract
Test.
## Boundaries
Test.
""",
            encoding="utf-8",
        )
        override_dir = skill_dir / "wrappers"
        override_dir.mkdir()
        (override_dir / "claude.yaml").write_text(
            "disable-model-invocation: true\nargument-hint: '[plan]'\n",
            encoding="utf-8",
        )

    def test_generator_preserves_frontmatter_and_host_override(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._make_repo(root)
            self.assertEqual(
                0,
                wrapper_generator.main(
                    ["--repo-root", str(root), "--target", "both", "--clean"]
                ),
            )
            claude, claude_error = wrapper_validator.parse_frontmatter(
                root / ".claude" / "skills" / "grill-me" / "SKILL.md"
            )
            codex, codex_error = wrapper_validator.parse_frontmatter(
                root / ".codex" / "skills" / "grill-me" / "SKILL.md"
            )
            self.assertIsNone(claude_error)
            self.assertIsNone(codex_error)
            assert claude is not None and codex is not None
            self.assertEqual({"version": "2.1.0"}, claude["metadata"])
            self.assertTrue(claude["disable-model-invocation"])
            self.assertNotIn("disable-model-invocation", codex)

    def test_validator_detects_wrapper_description_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._make_repo(root)
            self.assertEqual(
                0,
                wrapper_generator.main(
                    ["--repo-root", str(root), "--target", "both", "--clean"]
                ),
            )
            wrapper = root / ".codex" / "skills" / "grill-me" / "SKILL.md"
            text = wrapper.read_text(encoding="utf-8")
            wrapper.write_text(text.replace("pressure-test", "summarize"), encoding="utf-8")
            self.assertEqual(
                1,
                wrapper_validator.main(
                    [
                        "--canonical",
                        str(root / ".agent" / "skills"),
                        "--claude",
                        str(root / ".claude" / "skills"),
                        "--codex",
                        str(root / ".codex" / "skills"),
                    ]
                ),
            )


if __name__ == "__main__":
    unittest.main()

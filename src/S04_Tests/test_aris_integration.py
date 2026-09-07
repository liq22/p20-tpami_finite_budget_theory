from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


adapter_module = load_module(
    "papertrace_aris_adapter", ROOT / "integrations/aris/adapter.py"
)
setup_module = load_module(
    "papertrace_setup", ROOT / "scripts/setup_papertrace.py"
)
check_module = load_module(
    "papertrace_aris_check", ROOT / "scripts/check_aris_backend.py"
)


class ArisIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile_path = ROOT / "integrations/aris/profile.yaml"
        self.profile = yaml.safe_load(self.profile_path.read_text(encoding="utf-8"))

    def test_profile_is_optional_core_first_and_pinned(self) -> None:
        self.assertEqual(1, self.profile["schema_version"])
        submodule = self.profile["submodule"]
        self.assertTrue(submodule["optional"])
        self.assertRegex(submodule["pinned_commit"], r"^[0-9a-f]{40}$")
        self.assertNotIn("fork_plan", submodule)
        self.assertFalse(self.profile["host_exposure"]["expose_aris_skills"])
        self.assertFalse(self.profile["profiles"]["core"]["initialize_submodule"])
        self.assertTrue(self.profile["profiles"]["execution"]["initialize_submodule"])
        self.assertNotIn(
            "recommended",
            self.profile["profiles"]["execution"]["description"].lower(),
        )

    def test_submodule_is_recorded_as_a_gitlink_at_the_profile_pin(self) -> None:
        result = subprocess.run(
            ["git", "ls-files", "--stage", "--", "external/aris"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        fields = result.stdout.split()
        self.assertGreaterEqual(len(fields), 4, result.stdout)
        self.assertEqual("160000", fields[0])
        self.assertEqual(self.profile["submodule"]["pinned_commit"], fields[1])

    def test_execution_profile_allows_tools_but_not_review_or_pipelines(self) -> None:
        adapter = adapter_module.ArisAdapter(profile="execution")
        self.assertEqual("experiments", adapter.authorize("analyze-results"))
        for skill in ("experiment-audit", "research-pipeline", "ablation-planner"):
            with self.assertRaises(adapter_module.ArisIntegrationError):
                adapter.authorize(skill, explicit_review=True)

    def test_review_profile_requires_an_explicit_review_request(self) -> None:
        adapter = adapter_module.ArisAdapter(profile="review")
        with self.assertRaises(adapter_module.ArisIntegrationError):
            adapter.authorize("citation-audit")
        self.assertEqual(
            "explicit_review",
            adapter.authorize("citation-audit", explicit_review=True),
        )

    def test_runtime_requirements_fail_only_for_selected_capability(self) -> None:
        adapter = adapter_module.ArisAdapter(profile="execution")
        with mock.patch.object(adapter_module.shutil, "which", return_value=None):
            status = adapter.runtime_status("paper-compile")
            self.assertEqual(["latexmk"], status["missing_commands"])
            with self.assertRaisesRegex(
                adapter_module.ArisIntegrationError,
                "Install a LaTeX distribution",
            ):
                adapter.ensure_runtime("paper-compile")
        self.assertEqual((), adapter.ensure_runtime("analyze-results"))

    def test_no_aris_skill_is_exposed_as_a_host_entrypoint(self) -> None:
        adapter = adapter_module.ArisAdapter(profile="review")
        names = (
            set(adapter.all_execution_skills())
            | adapter.explicit_review_skills()
            | adapter.disabled_skills()
        )
        exposed: list[str] = []
        for name in sorted(names):
            for host in (".claude/skills", ".codex/skills", ".agents/skills"):
                path = ROOT / host / name
                if path.exists() or path.is_symlink():
                    exposed.append(path.relative_to(ROOT).as_posix())
        self.assertEqual([], exposed)

    def test_adapter_resolves_an_allowed_skill_in_a_fake_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config_dir = root / "integrations/aris"
            aris_root = root / "external/aris"
            skill_dir = aris_root / "skills/skills-codex/analyze-results"
            config_dir.mkdir(parents=True)
            skill_dir.mkdir(parents=True)
            (aris_root / "AGENT_GUIDE.md").write_text(
                "# Fake initialized ARIS checkout\n",
                encoding="utf-8",
            )
            (skill_dir / "SKILL.md").write_text(
                "# Analyze results\n",
                encoding="utf-8",
            )
            config = deepcopy(self.profile)
            config["submodule"]["path"] = "external/aris"
            config_path = config_dir / "profile.yaml"
            config_path.write_text(
                yaml.safe_dump(config, sort_keys=False),
                encoding="utf-8",
            )

            adapter = adapter_module.ArisAdapter(
                root=root,
                config_path=config_path,
                profile="execution",
            )
            resolution = adapter.resolve("analyze-results", host="codex")
            self.assertEqual(skill_dir / "SKILL.md", resolution.path)
            self.assertEqual("experiments", resolution.category)

    def test_malformed_capability_config_fails_instead_of_becoming_empty(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config_path = root / "profile.yaml"
            config = deepcopy(self.profile)
            config["capabilities"]["allowed"] = []
            config_path.write_text(
                yaml.safe_dump(config, sort_keys=False),
                encoding="utf-8",
            )
            adapter = adapter_module.ArisAdapter(
                root=root,
                config_path=config_path,
                profile="core",
            )
            with self.assertRaisesRegex(
                adapter_module.ArisIntegrationError,
                "capabilities.allowed must be a mapping",
            ):
                adapter.all_execution_skills()

    def test_missing_local_state_defaults_to_core(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root / ".papertrace/setup.json"
            with mock.patch.object(setup_module, "LOCAL_STATE", state):
                self.assertEqual("core", setup_module.saved_profile())
            with mock.patch.object(check_module, "LOCAL_STATE", state):
                self.assertEqual("core", check_module.load_local_profile())
            self.assertEqual("core", adapter_module.selected_profile(root))

    def test_corrupt_local_state_fails_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root / ".papertrace/setup.json"
            state.parent.mkdir(parents=True)
            state.write_text("{", encoding="utf-8")
            with mock.patch.object(setup_module, "LOCAL_STATE", state):
                with self.assertRaises(setup_module.SetupError):
                    setup_module.saved_profile()
            with mock.patch.object(check_module, "LOCAL_STATE", state):
                with self.assertRaises(check_module.LocalStateError):
                    check_module.load_local_profile()
            with self.assertRaises(adapter_module.ArisIntegrationError):
                adapter_module.selected_profile(root)

    def test_interactive_profile_choice_defaults_to_core(self) -> None:
        profiles = setup_module.load_profiles()
        with mock.patch("builtins.input", return_value=""):
            self.assertEqual("core", setup_module.choose_profile(profiles))

    def test_noninteractive_core_does_not_require_git_or_aris(self) -> None:
        profiles = setup_module.load_profiles()
        fake_python = ROOT / ".venv/bin/python"
        with (
            mock.patch.object(setup_module, "ensure_papertrace_directory"),
            mock.patch.object(setup_module, "bootstrap_yaml", return_value=None),
            mock.patch.object(setup_module, "load_profiles", return_value=profiles),
            mock.patch.object(setup_module, "ensure_git_repository") as ensure_git,
            mock.patch.object(setup_module, "ensure_venv", return_value=fake_python),
            mock.patch.object(setup_module, "initialize_aris") as initialize_aris,
            mock.patch.object(setup_module, "write_local_state"),
            mock.patch.object(setup_module, "run_checks"),
            mock.patch.object(setup_module, "print_success"),
        ):
            self.assertEqual(
                0,
                setup_module.main(["--non-interactive", "--skip-deps"]),
            )
        ensure_git.assert_not_called()
        initialize_aris.assert_not_called()

    def test_execution_profile_requires_git_and_initializes_aris(self) -> None:
        profiles = setup_module.load_profiles()
        fake_python = ROOT / ".venv/bin/python"
        with (
            mock.patch.object(setup_module, "ensure_papertrace_directory"),
            mock.patch.object(setup_module, "bootstrap_yaml", return_value=None),
            mock.patch.object(setup_module, "load_profiles", return_value=profiles),
            mock.patch.object(setup_module, "ensure_git_repository") as ensure_git,
            mock.patch.object(setup_module, "ensure_venv", return_value=fake_python),
            mock.patch.object(setup_module, "initialize_aris") as initialize_aris,
            mock.patch.object(setup_module, "write_local_state"),
            mock.patch.object(setup_module, "run_checks"),
            mock.patch.object(setup_module, "print_success"),
        ):
            self.assertEqual(
                0,
                setup_module.main(
                    ["--profile", "execution", "--non-interactive", "--skip-deps"]
                ),
            )
        ensure_git.assert_called_once()
        initialize_aris.assert_called_once()

    def test_setup_does_not_run_upstream_installers(self) -> None:
        text = (ROOT / "scripts/setup_papertrace.py").read_text(encoding="utf-8")
        self.assertNotIn("install_aris_codex.sh", text)
        self.assertNotIn("install_aris.sh", text)


if __name__ == "__main__":
    unittest.main()

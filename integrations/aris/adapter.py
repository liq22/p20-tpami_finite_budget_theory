#!/usr/bin/env python3
"""Resolve optional ARIS capabilities without exposing a second router."""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - setup installs requirements-dev
    raise SystemExit(
        "PyYAML is required. Run `python scripts/setup_papertrace.py` first."
    ) from exc

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "integrations/aris/profile.yaml"
PROFILE_NAMES = frozenset({"core", "execution", "review"})


class ArisIntegrationError(RuntimeError):
    """Raised when ARIS configuration or a requested capability is invalid."""


@dataclass(frozen=True)
class Resolution:
    skill: str
    path: Path
    category: str
    explicit_review: bool
    runtime_notes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "skill": self.skill,
            "path": self.path.as_posix(),
            "category": self.category,
            "explicit_review": self.explicit_review,
            "runtime_notes": list(self.runtime_notes),
        }


class ArisAdapter:
    """Small allowlist adapter between PaperTrace and the optional ARIS checkout."""

    def __init__(
        self,
        *,
        root: Path = ROOT,
        config_path: Path = DEFAULT_CONFIG,
        profile: str = "core",
    ) -> None:
        self.root = root.resolve()
        self.config_path = config_path.resolve()
        self.config = self._load_config(self.config_path)

        profiles = self.config.get("profiles")
        if not isinstance(profiles, dict):
            raise ArisIntegrationError("ARIS profile.yaml must contain a profiles mapping.")
        profile_config = profiles.get(profile)
        if not isinstance(profile_config, dict):
            raise ArisIntegrationError(
                f"Unknown PaperTrace profile {profile!r}; choose one of {sorted(profiles)}."
            )
        self.profile_name = profile
        self.profile = profile_config

        submodule = self.config.get("submodule")
        if not isinstance(submodule, dict):
            raise ArisIntegrationError("ARIS profile.yaml must contain a submodule mapping.")
        submodule_path = submodule.get("path")
        if not isinstance(submodule_path, str) or not submodule_path.strip():
            raise ArisIntegrationError("ARIS submodule.path must be a non-empty string.")
        self.submodule_path = self.root / submodule_path

    @staticmethod
    def _load_config(path: Path) -> dict[str, Any]:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            raise ArisIntegrationError(f"Cannot read ARIS profile {path}: {exc}") from exc
        if not isinstance(data, dict) or data.get("schema_version") != 1:
            raise ArisIntegrationError("ARIS profile must be a schema_version: 1 mapping.")
        return data

    @staticmethod
    def _python_package_available(package: str) -> bool:
        try:
            return importlib.util.find_spec(package) is not None
        except (ImportError, ValueError):
            return False

    @staticmethod
    def _string_list(value: Any, location: str) -> list[str]:
        if not isinstance(value, list) or not all(
            isinstance(item, str) and item.strip() for item in value
        ):
            raise ArisIntegrationError(f"{location} must be a list of non-empty strings.")
        return value

    def _capabilities(self) -> dict[str, Any]:
        capabilities = self.config.get("capabilities")
        if not isinstance(capabilities, dict):
            raise ArisIntegrationError("ARIS profile.yaml must contain a capabilities mapping.")
        return capabilities

    @property
    def initialized(self) -> bool:
        return (self.submodule_path / ".git").exists() or (
            self.submodule_path / "AGENT_GUIDE.md"
        ).is_file()

    def all_execution_skills(self) -> dict[str, str]:
        allowed = self._capabilities().get("allowed")
        if not isinstance(allowed, dict):
            raise ArisIntegrationError("capabilities.allowed must be a mapping.")

        result: dict[str, str] = {}
        for category, raw_skills in allowed.items():
            if not isinstance(category, str) or not category.strip():
                raise ArisIntegrationError(
                    "Each capabilities.allowed category must be a non-empty string."
                )
            skills = self._string_list(
                raw_skills,
                f"capabilities.allowed.{category}",
            )
            for skill in skills:
                if skill in result:
                    raise ArisIntegrationError(
                        f"ARIS capability {skill!r} appears in multiple categories."
                    )
                result[skill] = category
        return result

    def explicit_review_skills(self) -> set[str]:
        values = self._string_list(
            self._capabilities().get("explicit_only"),
            "capabilities.explicit_only",
        )
        return set(values)

    def disabled_skills(self) -> set[str]:
        values = self._string_list(
            self._capabilities().get("disabled"),
            "capabilities.disabled",
        )
        return set(values)

    def authorize(self, skill: str, *, explicit_review: bool = False) -> str:
        """Return the capability category or raise a precise policy error."""
        if skill in self.disabled_skills():
            raise ArisIntegrationError(
                f"ARIS skill {skill!r} is disabled because it conflicts with the "
                "PaperTrace route or depends on a disabled upstream pipeline."
            )

        execution = self.all_execution_skills()
        if skill in execution:
            if not bool(self.profile.get("allow_execution_capabilities")):
                raise ArisIntegrationError(
                    f"Profile {self.profile_name!r} does not enable ARIS execution. "
                    "Run `python scripts/setup_papertrace.py --profile execution`."
                )
            return execution[skill]

        if skill in self.explicit_review_skills():
            if not explicit_review:
                raise ArisIntegrationError(
                    f"ARIS skill {skill!r} is explicit-review only. It cannot support a "
                    "normal writing, implementation, experiment, or figure task."
                )
            if not bool(self.profile.get("allow_explicit_review_capabilities")):
                raise ArisIntegrationError(
                    f"Profile {self.profile_name!r} does not enable explicit ARIS review. "
                    "Run `python scripts/setup_papertrace.py --profile review`."
                )
            return "explicit_review"

        raise ArisIntegrationError(
            f"ARIS skill {skill!r} is not in the PaperTrace allowlist."
        )

    def runtime_status(self, skill: str) -> dict[str, Any]:
        all_requirements = self.config.get("runtime_requirements", {})
        if not isinstance(all_requirements, dict):
            raise ArisIntegrationError("runtime_requirements must be a mapping.")
        requirements = all_requirements.get(skill)
        if requirements is None:
            return {
                "missing_commands": [],
                "missing_python_packages": [],
                "install_hint": "",
                "notes": [],
            }
        if not isinstance(requirements, dict):
            raise ArisIntegrationError(
                f"runtime_requirements.{skill} must be a mapping."
            )

        commands = self._string_list(
            requirements.get("commands", []),
            f"runtime_requirements.{skill}.commands",
        )
        packages = self._string_list(
            requirements.get("python_packages", []),
            f"runtime_requirements.{skill}.python_packages",
        )
        install_hint = requirements.get("install_hint", "")
        note = requirements.get("note", "")
        if not isinstance(install_hint, str):
            raise ArisIntegrationError(
                f"runtime_requirements.{skill}.install_hint must be a string."
            )
        if not isinstance(note, str):
            raise ArisIntegrationError(
                f"runtime_requirements.{skill}.note must be a string."
            )

        missing_commands = [
            command for command in commands if shutil.which(command) is None
        ]
        missing_packages = [
            package for package in packages if not self._python_package_available(package)
        ]
        return {
            "missing_commands": missing_commands,
            "missing_python_packages": missing_packages,
            "install_hint": install_hint,
            "notes": [note] if note else [],
        }

    def ensure_runtime(self, skill: str) -> tuple[str, ...]:
        status = self.runtime_status(skill)
        missing: list[str] = []
        if status["missing_commands"]:
            missing.append("commands: " + ", ".join(status["missing_commands"]))
        if status["missing_python_packages"]:
            missing.append(
                "Python packages: " + ", ".join(status["missing_python_packages"])
            )
        if missing:
            hint = status["install_hint"]
            message = (
                f"ARIS capability {skill!r} is allowed but is not ready: "
                f"{'; '.join(missing)}."
            )
            if hint:
                message += f" Suggested setup: {hint}"
            raise ArisIntegrationError(message)
        return tuple(status["notes"])

    def _candidate_roots(self, host: str) -> Iterable[Path]:
        skill_roots = self.config.get("skill_roots")
        if not isinstance(skill_roots, dict):
            raise ArisIntegrationError("skill_roots must be a mapping.")
        if host not in skill_roots:
            raise ArisIntegrationError(f"Unsupported host {host!r}; use codex or claude.")
        roots = self._string_list(skill_roots[host], f"skill_roots.{host}")
        return tuple(self.submodule_path / relative for relative in roots)

    def resolve(
        self,
        skill: str,
        *,
        host: str = "codex",
        explicit_review: bool = False,
    ) -> Resolution:
        category = self.authorize(skill, explicit_review=explicit_review)
        if not self.initialized:
            raise ArisIntegrationError(
                "The optional ARIS backend is not initialized. Run "
                "`python scripts/setup_papertrace.py --profile execution` first."
            )

        runtime_notes = self.ensure_runtime(skill)
        checked: list[str] = []
        for root in self._candidate_roots(host):
            candidate = root / skill / "SKILL.md"
            checked.append(candidate.relative_to(self.root).as_posix())
            if candidate.is_file():
                return Resolution(
                    skill=skill,
                    path=candidate,
                    category=category,
                    explicit_review=explicit_review,
                    runtime_notes=runtime_notes,
                )
        raise ArisIntegrationError(
            f"Allowed skill {skill!r} was not found in the pinned ARIS checkout. "
            f"Checked: {', '.join(checked)}"
        )


def selected_profile(root: Path = ROOT) -> str:
    local_state = root / ".papertrace/setup.json"
    if not local_state.is_file():
        return "core"
    try:
        data = json.loads(local_state.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ArisIntegrationError(
            f"Cannot read local PaperTrace state {local_state}: {exc}. "
            "Repair or remove the file, then select a profile explicitly."
        ) from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ArisIntegrationError(
            f"Local PaperTrace state {local_state} must be a schema_version: 1 mapping."
        )
    profile = data.get("profile")
    if profile not in PROFILE_NAMES:
        raise ArisIntegrationError(
            f"Local PaperTrace state {local_state} has invalid profile {profile!r}."
        )
    return str(profile)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("status", "resolve"))
    parser.add_argument("skill", nargs="?")
    parser.add_argument("--profile", choices=sorted(PROFILE_NAMES))
    parser.add_argument("--host", choices=("codex", "claude"), default="codex")
    parser.add_argument("--explicit-review", action="store_true")
    args = parser.parse_args(argv)

    try:
        profile = args.profile or selected_profile()
        adapter = ArisAdapter(profile=profile)
        if args.command == "status":
            runtime = {
                skill: adapter.runtime_status(skill)
                for skill in sorted(adapter.all_execution_skills())
            }
            print(
                json.dumps(
                    {
                        "profile": profile,
                        "initialized": adapter.initialized,
                        "submodule_path": adapter.submodule_path.relative_to(ROOT).as_posix(),
                        "execution_skills": sorted(adapter.all_execution_skills()),
                        "explicit_review_skills": sorted(adapter.explicit_review_skills()),
                        "runtime": runtime,
                        "host_exposure": False,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        if not args.skill:
            parser.error("resolve requires a skill name")
        resolution = adapter.resolve(
            args.skill,
            host=args.host,
            explicit_review=args.explicit_review,
        )
        print(json.dumps(resolution.as_dict(), ensure_ascii=False, indent=2))
        return 0
    except ArisIntegrationError as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Check the optional ARIS boundary without making Git or ARIS a Core requirement."""
from __future__ import annotations

import argparse
import configparser
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "integrations/aris/profile.yaml"
LOCAL_STATE = ROOT / ".papertrace/setup.json"
ADAPTER_PATH = ROOT / "integrations/aris/adapter.py"
PROFILE_NAMES = frozenset({"core", "execution", "review"})


class LocalStateError(RuntimeError):
    """Raised when a present local setup file is unreadable or invalid."""


def load_adapter_module():
    spec = importlib.util.spec_from_file_location("papertrace_aris_adapter_check", ADAPTER_PATH)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {ADAPTER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


adapter_module = load_adapter_module()


def git(*args: str, cwd: Path = ROOT) -> tuple[int, str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except FileNotFoundError:
        return 127, "git is not installed"
    return result.returncode, result.stdout.strip()


def load_local_profile() -> str:
    if not LOCAL_STATE.is_file():
        return "core"
    try:
        data = json.loads(LOCAL_STATE.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise LocalStateError(
            f"cannot read local PaperTrace state {LOCAL_STATE}: {exc}; "
            "repair or remove the file"
        ) from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise LocalStateError(
            f"local PaperTrace state {LOCAL_STATE} must be a schema_version: 1 mapping"
        )
    profile = data.get("profile")
    if profile not in PROFILE_NAMES:
        raise LocalStateError(
            f"local PaperTrace state {LOCAL_STATE} has invalid profile {profile!r}"
        )
    return str(profile)


def parse_gitmodules() -> tuple[str | None, str | None]:
    path = ROOT / ".gitmodules"
    if not path.is_file():
        return None, None
    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")
    section = 'submodule "external/aris"'
    if section not in parser:
        return None, None
    return parser[section].get("path"), parser[section].get("url")


def index_gitlink(path: str) -> tuple[str | None, str | None]:
    code, output = git("ls-files", "--stage", "--", path)
    if code != 0 or not output:
        return None, None
    first = output.splitlines()[0]
    metadata, _, recorded_path = first.partition("\t")
    fields = metadata.split()
    if len(fields) < 3 or recorded_path != path:
        return None, None
    return fields[0], fields[1]


def in_git_repository() -> bool:
    code, output = git("rev-parse", "--show-toplevel")
    if code != 0 or not output:
        return False
    try:
        return Path(output).resolve() == ROOT.resolve()
    except OSError:
        return False


def selected_skills(adapter: Any) -> set[str]:
    result: set[str] = set()
    if bool(adapter.profile.get("allow_execution_capabilities")):
        result.update(adapter.all_execution_skills())
    if bool(adapter.profile.get("allow_explicit_review_capabilities")):
        result.update(adapter.explicit_review_skills())
    return result


def all_capability_names(adapter: Any) -> set[str]:
    return (
        set(adapter.all_execution_skills())
        | adapter.explicit_review_skills()
        | adapter.disabled_skills()
    )


def skill_exists(adapter: Any, skill: str) -> bool:
    for host in ("codex", "claude"):
        for root in adapter._candidate_roots(host):
            if (root / skill / "SKILL.md").is_file():
                return True
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=sorted(PROFILE_NAMES))
    parser.add_argument(
        "--require-initialized",
        action="store_true",
        help="fail when the optional submodule is not checked out",
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    try:
        profile_name = args.profile or load_local_profile()
    except LocalStateError as exc:
        print(f"ERROR: {exc}")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    try:
        adapter = adapter_module.ArisAdapter(
            root=ROOT,
            config_path=PROFILE_PATH,
            profile=profile_name,
        )
    except adapter_module.ArisIntegrationError as exc:
        print(f"ERROR: {exc}")
        return 1

    config = adapter.config
    submodule_cfg = config.get("submodule")
    if not isinstance(submodule_cfg, dict):
        print("ERROR: ARIS profile.yaml must contain a submodule mapping")
        return 1
    path_value = str(submodule_cfg.get("path", ""))
    url_value = str(submodule_cfg.get("url", ""))
    pin_value = str(submodule_cfg.get("pinned_commit", ""))
    requires_aris = bool(adapter.profile.get("initialize_submodule")) or args.require_initialized
    git_repo = in_git_repository()

    if requires_aris and not git_repo:
        errors.append(
            "this profile requires a Git clone so the pinned ARIS submodule can be initialized"
        )
    if git_repo:
        module_path, module_url = parse_gitmodules()
        if module_path != path_value:
            errors.append(
                f".gitmodules path mismatch: expected {path_value!r}, found {module_path!r}"
            )
        if module_url != url_value:
            errors.append(
                f".gitmodules URL mismatch: expected {url_value!r}, found {module_url!r}"
            )
        mode, index_sha = index_gitlink(path_value)
        if mode != "160000":
            errors.append(f"{path_value} is not recorded as a git submodule (mode 160000)")
        if index_sha != pin_value:
            errors.append(
                f"submodule pin mismatch: profile={pin_value!r}, index={index_sha!r}"
            )
    elif profile_name == "core":
        warnings.append("Git metadata not present; skipped submodule-pin checks in Core mode.")

    initialized = adapter.initialized
    if requires_aris and not initialized:
        errors.append(
            "ARIS is required by this profile but is not initialized. Run "
            "`python scripts/setup_papertrace.py --profile execution`."
        )
    elif not initialized:
        warnings.append("ARIS is not initialized; this is valid for the Core profile.")

    selected = selected_skills(adapter)
    if initialized:
        if git_repo:
            code, head = git("rev-parse", "HEAD", cwd=adapter.submodule_path)
            if code != 0:
                errors.append(f"cannot read ARIS HEAD: {head}")
            elif head != pin_value:
                errors.append(f"ARIS checkout is at {head}, expected pinned commit {pin_value}")
        if not (adapter.submodule_path / "LICENSE").is_file():
            errors.append("initialized ARIS checkout is missing LICENSE")
        for skill in sorted(selected):
            if not skill_exists(adapter, skill):
                errors.append(f"pinned ARIS checkout does not contain allowed skill {skill!r}")

    runtime_warnings: list[str] = []
    if bool(adapter.profile.get("allow_execution_capabilities")):
        for skill in sorted(selected):
            status = adapter.runtime_status(skill)
            missing: list[str] = []
            if status["missing_commands"]:
                missing.append("commands=" + ",".join(status["missing_commands"]))
            if status["missing_python_packages"]:
                missing.append("python=" + ",".join(status["missing_python_packages"]))
            if missing:
                suffix = f"; setup: {status['install_hint']}" if status["install_hint"] else ""
                runtime_warnings.append(f"{skill}: {'; '.join(missing)}{suffix}")

    exposed: list[str] = []
    for skill in sorted(all_capability_names(adapter)):
        for host_root in (".claude/skills", ".codex/skills", ".agents/skills"):
            candidate = ROOT / host_root / skill
            if candidate.exists() or candidate.is_symlink():
                exposed.append(candidate.relative_to(ROOT).as_posix())
    if exposed:
        errors.append(
            "ARIS skills must remain behind PaperTrace 00-router; remove direct host "
            f"exposure: {', '.join(exposed)}"
        )

    print(f"Profile: {profile_name}")
    print(f"Submodule pin: {pin_value}")
    print(f"Git repository: {'yes' if git_repo else 'no'}")
    print(f"ARIS initialized: {'yes' if initialized else 'no'}")
    print("Direct ARIS host exposure: none" if not exposed else "Direct exposure found")
    if runtime_warnings:
        print("Optional capability prerequisites not detected:")
        for warning in runtime_warnings:
            print(f"  - {warning}")
    if args.verbose:
        for skill in sorted(selected):
            for note in adapter.runtime_status(skill)["notes"]:
                print(f"NOTE: {skill}: {note}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED: {len(errors)} ARIS integration issue(s)")
        return 1
    print("PASS: PaperTrace–ARIS integration boundary is consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

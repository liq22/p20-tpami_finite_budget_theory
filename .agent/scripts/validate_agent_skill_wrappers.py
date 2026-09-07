#!/usr/bin/env python3
"""Verify that only approved PaperTrace host entrypoints have wrappers.

Canonical skills are the complete internal library. Claude/Codex wrapper roots
must contain exactly ``HOST_EXPOSED_SKILLS`` intersected with the canonical set,
not a mirror of every internal module.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required. Install development dependencies with "
        "`python -m pip install -r requirements-dev.txt`."
    ) from exc

PROVENANCE_MARKERS = (
    "do not edit manually",
    "canonical content lives under",
)
AT_RE = re.compile(r"(?m)^@\s*(\S+)")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
CANONICAL_KEY_ORDER = (
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
)
CANONICAL_KEYS = set(CANONICAL_KEY_ORDER)
HOST_OVERRIDE_KEYS = {
    "claude": {"disable-model-invocation", "argument-hint"},
    "codex": set(),
}
HOST_EXPOSED_SKILLS = frozenset({"00-router", "grill-me"})


def skill_names(root: Path) -> set[str]:
    if not root.is_dir():
        return set()
    return {
        directory.name
        for directory in root.iterdir()
        if directory.is_dir()
        and (directory / "SKILL.md").is_file()
        and not directory.name.startswith("_")
    }


def parse_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, "missing YAML frontmatter"
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, f"invalid YAML frontmatter: {exc}"
    if not isinstance(data, dict):
        return None, "YAML frontmatter must be a mapping"
    return data, None


def load_host_override(
    canonical_file: Path, host: str
) -> tuple[dict[str, Any], list[str]]:
    path = canonical_file.parent / "wrappers" / f"{host}.yaml"
    if not path.is_file():
        return {}, []
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return {}, [f"{path}: invalid YAML: {exc}"]
    if not isinstance(data, dict):
        return {}, [f"{path}: host override must be a mapping"]
    extra = set(data) - HOST_OVERRIDE_KEYS[host]
    if extra:
        errors.append(f"{path}: unexpected host override keys: {sorted(extra)}")
    return data, errors


def expected_frontmatter(
    canonical_file: Path, host: str
) -> tuple[dict[str, Any] | None, list[str]]:
    canonical, error = parse_frontmatter(canonical_file)
    if canonical is None:
        return None, [f"{canonical_file}: {error}"]
    unexpected = set(canonical) - CANONICAL_KEYS
    errors: list[str] = []
    if unexpected:
        errors.append(
            f"{canonical_file}: unexpected canonical keys: {sorted(unexpected)}"
        )
    expected = {
        key: canonical[key] for key in CANONICAL_KEY_ORDER if key in canonical
    }
    override, override_errors = load_host_override(canonical_file, host)
    errors.extend(override_errors)
    if "name" in override or "description" in override:
        errors.append(
            f"{canonical_file.parent}: host override cannot replace name or description"
        )
    expected.update(override)
    return expected, errors


def check_wrapper(
    wrapper_file: Path,
    canonical_root: Path,
    canonical_file: Path,
    host: str,
) -> list[str]:
    errors: list[str] = []
    text = wrapper_file.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()
    if not any(marker in lowered for marker in PROVENANCE_MARKERS):
        errors.append(f"{wrapper_file}: missing provenance comment")

    match = AT_RE.search(text)
    if not match:
        errors.append(f"{wrapper_file}: missing @<path> reference")
    else:
        target = (wrapper_file.parent / match.group(1)).resolve()
        if not target.exists():
            errors.append(f"{wrapper_file}: @target does not exist -> {target}")
        else:
            try:
                target.relative_to(canonical_root)
            except ValueError:
                errors.append(
                    f"{wrapper_file}: @target outside canonical -> {target}"
                )
            if target != canonical_file.resolve():
                errors.append(
                    f"{wrapper_file}: @target {target} does not match "
                    f"canonical {canonical_file.resolve()}"
                )

    actual, actual_error = parse_frontmatter(wrapper_file)
    if actual is None:
        errors.append(f"{wrapper_file}: {actual_error}")
        return errors
    expected, expected_errors = expected_frontmatter(canonical_file, host)
    errors.extend(expected_errors)
    if expected is not None and actual != expected:
        errors.append(
            f"{wrapper_file}: frontmatter drift; "
            f"expected={expected!r}, actual={actual!r}"
        )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical", default=".agent/skills")
    parser.add_argument("--claude", default=".claude/skills")
    parser.add_argument("--codex", default=".codex/skills")
    args = parser.parse_args(argv)

    canonical = Path(args.canonical).resolve()
    roots = {
        "claude": Path(args.claude).resolve(),
        "codex": Path(args.codex).resolve(),
    }

    canonical_names = skill_names(canonical)
    expected_names = canonical_names & HOST_EXPOSED_SKILLS
    errors: list[str] = []
    counts: dict[str, int] = {}

    if not expected_names:
        errors.append(
            "canonical library contains no approved host entrypoint; "
            f"allowlist={sorted(HOST_EXPOSED_SKILLS)}"
        )

    for host, root in roots.items():
        names = skill_names(root)
        counts[host] = len(names)
        if names != expected_names:
            errors.append(
                f".{host}/skills exposure mismatch; "
                f"missing={sorted(expected_names - names)} "
                f"extra_internal_wrappers={sorted(names - expected_names)}"
            )
        for name in sorted(names & expected_names):
            errors.extend(
                check_wrapper(
                    root / name / "SKILL.md",
                    canonical,
                    canonical / name / "SKILL.md",
                    host,
                )
            )

    print(f"canonical internal skills: {len(canonical_names)}")
    print(
        "approved host entrypoints: "
        f"{len(expected_names)} ({', '.join(sorted(expected_names))})"
    )
    print(f"claude wrappers: {counts.get('claude', 0)}")
    print(f"codex wrappers:  {counts.get('codex', 0)}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED with {len(errors)} error(s).")
        return 1
    print(
        "PASS: wrappers expose only approved entrypoints and match canonical "
        "frontmatter, host overrides, provenance, and @targets."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

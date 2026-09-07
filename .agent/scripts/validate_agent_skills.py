#!/usr/bin/env python3
"""Validate PaperTrace Skills without making every tool part of the core contract.

All Skills need valid frontmatter and a readable body. Skills that appear as an
expected primary in the routing/product case definitions also need the four
substantive execution sections. This avoids imposing workflow structure on
library, Office, lookup, and optional tool references.
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

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
HYPHEN_CASE_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
ALLOWED_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
REQUIRED_SECTIONS = (
    "## Purpose",
    "## Workflow",
    "## Output Contract",
    "## Boundaries",
)
DEFAULT_ROUTING_CASES = Path(".agent/evals/skill_trigger_cases.yaml")
DEFAULT_PRODUCT_CASES = Path(".agent/evals/product_surface_cases.yaml")


def extract_frontmatter(text: str) -> tuple[dict[str, Any] | None, str | None]:
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


def validate_optional_metadata(frontmatter: dict[str, Any], rel: str) -> list[str]:
    errors: list[str] = []
    for key in ("license", "compatibility"):
        value = frontmatter.get(key)
        if value is not None and not isinstance(value, str):
            errors.append(f"{rel}: frontmatter.{key} must be a string")

    allowed_tools = frontmatter.get("allowed-tools")
    if allowed_tools is not None and not (
        isinstance(allowed_tools, str)
        or (
            isinstance(allowed_tools, list)
            and all(isinstance(item, str) for item in allowed_tools)
        )
    ):
        errors.append(
            f"{rel}: frontmatter.allowed-tools must be a string or list of strings"
        )

    metadata = frontmatter.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        errors.append(f"{rel}: frontmatter.metadata must be a mapping")
    return errors


def load_routeable_skills(paths: list[Path]) -> tuple[set[str], list[str]]:
    skills = {"00-router", "grill-me"}
    errors: list[str] = []
    for path in paths:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            errors.append(f"{path}: cannot read route definitions: {exc}")
            continue
        cases = data.get("cases") if isinstance(data, dict) else None
        if not isinstance(cases, list):
            errors.append(f"{path}: cases must be a list")
            continue
        for index, case in enumerate(cases):
            if not isinstance(case, dict):
                errors.append(f"{path}: cases[{index}] must be a mapping")
                continue
            primary = case.get("expected_primary")
            if isinstance(primary, str) and primary not in {"", "none"}:
                skills.add(primary)
    return skills, errors


def validate_skill(skill_dir: Path, *, routeable: bool) -> list[str]:
    errors: list[str] = []
    name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"
    rel = f".agent/skills/{name}/SKILL.md"

    if not skill_file.is_file():
        return [f"{rel}: missing SKILL.md"]
    text = skill_file.read_text(encoding="utf-8", errors="replace")

    frontmatter, error = extract_frontmatter(text)
    if frontmatter is None:
        return [f"{rel}: {error}"]

    frontmatter_name = frontmatter.get("name", "")
    if frontmatter_name != name:
        errors.append(
            f"{rel}: frontmatter name {frontmatter_name!r} != directory {name!r}"
        )
    if frontmatter_name and not HYPHEN_CASE_RE.fullmatch(str(frontmatter_name)):
        errors.append(f"{rel}: name {frontmatter_name!r} is not lower-hyphen-case")

    extra = set(frontmatter) - ALLOWED_KEYS
    if extra:
        errors.append(f"{rel}: unexpected frontmatter keys: {sorted(extra)}")
    errors.extend(validate_optional_metadata(frontmatter, rel))

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{rel}: description is empty or not a string")

    match = FRONTMATTER_RE.match(text)
    body = text[match.end() :].strip() if match else ""
    if not body:
        errors.append(f"{rel}: body is empty")
    if routeable:
        missing = [section for section in REQUIRED_SECTIONS if section not in text]
        if missing:
            errors.append(f"{rel}: routeable primary missing sections: {missing}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", default=".agent/skills")
    parser.add_argument("--only", default=None, help="validate one skill directory")
    parser.add_argument("--routing-cases", type=Path, default=DEFAULT_ROUTING_CASES)
    parser.add_argument("--product-cases", type=Path, default=DEFAULT_PRODUCT_CASES)
    args = parser.parse_args(argv)

    skills_dir = Path(args.skills_dir).resolve()
    if not skills_dir.is_dir():
        print(f"ERROR: skills dir not found: {skills_dir}")
        return 1

    routeable, errors = load_routeable_skills(
        [args.routing_cases.resolve(), args.product_cases.resolve()]
    )
    if args.only:
        target = skills_dir / args.only
        if not target.is_dir():
            print(f"ERROR: --only skill not found: {args.only}")
            return 1
        skill_dirs = [target]
    else:
        skill_dirs = sorted(
            path
            for path in skills_dir.iterdir()
            if path.is_dir() and not path.name.startswith("_")
        )

    missing_routeable = sorted(
        name for name in routeable if not (skills_dir / name / "SKILL.md").is_file()
    )
    if not args.only:
        errors.extend(f"routeable primary missing: {name}" for name in missing_routeable)

    for directory in skill_dirs:
        errors.extend(validate_skill(directory, routeable=directory.name in routeable))

    routeable_scanned = sum(directory.name in routeable for directory in skill_dirs)
    print(
        f"Skills scanned: {len(skill_dirs)} "
        f"({routeable_scanned} routeable primary, {len(skill_dirs) - routeable_scanned} optional/reference)"
    )
    for error in errors:
        print(f"ERROR: {error}")
    print(f"summary: {len(errors)} error(s)")
    if errors:
        print("FAILED")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

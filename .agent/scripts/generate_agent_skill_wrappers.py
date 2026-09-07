#!/usr/bin/env python3
"""Generate the minimal Claude/Codex host entrypoints from canonical skills.

Canonical skills live under ``.agent/skills``. Most are internal modules selected
by ``00-router``; exposing every module to the host creates trigger competition.
Only names in ``HOST_EXPOSED_SKILLS`` receive generated wrappers.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
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


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str | None]:
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


def validate_canonical(skill_key: str, meta: dict[str, Any]) -> str:
    name = meta.get("name")
    description = meta.get("description")
    if name != skill_key:
        return f"frontmatter name {name!r} != directory {skill_key!r}"
    if not isinstance(name, str) or not HYPHEN_CASE_RE.fullmatch(name):
        return f"name {name!r} is not lower-hyphen-case"
    extra = set(meta) - CANONICAL_KEYS
    if extra:
        return f"unexpected frontmatter keys: {sorted(extra)}"
    if not isinstance(description, str) or not description.strip():
        return "description is empty or not a string"
    metadata = meta.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        return "metadata must be a mapping"
    allowed_tools = meta.get("allowed-tools")
    if allowed_tools is not None and not (
        isinstance(allowed_tools, str)
        or (
            isinstance(allowed_tools, list)
            and all(isinstance(item, str) for item in allowed_tools)
        )
    ):
        return "allowed-tools must be a string or list of strings"
    return ""


def canonical_skills(
    source_dir: Path,
) -> tuple[list[tuple[str, Path, dict[str, Any]]], list[str]]:
    """Return valid one-level canonical skills and structural skip reasons."""
    valid: list[tuple[str, Path, dict[str, Any]]] = []
    skipped: list[str] = []
    if not source_dir.exists():
        return valid, skipped
    for skill_dir in sorted(source_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith("_"):
            skipped.append(
                f"{skill_dir.name}: leading underscore (namespace, not a skill)"
            )
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            skipped.append(f"{skill_dir.name}: no SKILL.md")
            continue
        meta, error = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
        if meta is None:
            skipped.append(f"{skill_dir.name}: {error}")
            continue
        reason = validate_canonical(skill_dir.name, meta)
        if reason:
            skipped.append(f"{skill_dir.name}: {reason}")
            continue
        valid.append((skill_dir.name, skill_file, meta))
    return valid, skipped


def exposed_skills(
    skills: list[tuple[str, Path, dict[str, Any]]],
) -> list[tuple[str, Path, dict[str, Any]]]:
    """Filter canonical modules to the deliberately small host allowlist."""
    return [item for item in skills if item[0] in HOST_EXPOSED_SKILLS]


def load_host_override(skill_file: Path, host: str) -> dict[str, Any]:
    path = skill_file.parent / "wrappers" / f"{host}.yaml"
    if not path.is_file():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: host override must be a mapping")
    allowed = HOST_OVERRIDE_KEYS[host]
    extra = set(data) - allowed
    if extra:
        raise ValueError(f"{path}: unexpected host override keys: {sorted(extra)}")
    return data


def expected_frontmatter(
    skill_file: Path, meta: dict[str, Any], host: str
) -> dict[str, Any]:
    result = {key: meta[key] for key in CANONICAL_KEY_ORDER if key in meta}
    override = load_host_override(skill_file, host)
    if "name" in override or "description" in override:
        raise ValueError(
            f"{skill_file.parent}: host override cannot replace name or description"
        )
    result.update(override)
    return result


def render_wrapper(
    skill_key: str,
    skill_file: Path,
    rel_source: str,
    meta: dict[str, Any],
    host: str,
    provenance: str,
) -> str:
    del skill_key  # name is already represented in canonical frontmatter
    frontmatter = expected_frontmatter(skill_file, meta, host)
    dumped = yaml.safe_dump(
        frontmatter,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1000,
    ).rstrip()
    return (
        f"---\n{dumped}\n---\n\n"
        f"<!-- {provenance} -->\n\n"
        f"@{rel_source}\n"
    )


def remove_generated_dir(path: Path, repo_root: Path) -> None:
    resolved = path.resolve()
    allowed = {
        (repo_root / ".claude" / "skills").resolve(),
        (repo_root / ".codex" / "skills").resolve(),
    }
    if resolved not in allowed:
        raise ValueError(f"refusing to clean unexpected directory: {path}")
    if resolved.exists():
        shutil.rmtree(resolved)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate minimal host wrappers from canonical PaperTrace skills."
    )
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument(
        "--source-dir", default=".agent/skills", help="Canonical skill source"
    )
    parser.add_argument(
        "--clean", action="store_true", help="Remove generated wrapper dirs first"
    )
    parser.add_argument(
        "--target", choices=["both", "claude", "codex"], default="both"
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    source_dir = (repo_root / args.source_dir).resolve()
    claude_dir = repo_root / ".claude" / "skills"
    codex_dir = repo_root / ".codex" / "skills"
    provenance = (
        "Generated by .agent/scripts/sync_agent_skill_wrappers.sh. "
        "Do not edit manually."
    )

    canonical, skipped = canonical_skills(source_dir)
    if not canonical:
        raise SystemExit(f"No valid canonical skills found under {source_dir}")
    host_skills = exposed_skills(canonical)
    if not host_skills:
        raise SystemExit(
            "No host-exposed skills found. Expected at least one of "
            f"{sorted(HOST_EXPOSED_SKILLS)} under {source_dir}"
        )

    targets = ["claude", "codex"] if args.target == "both" else [args.target]
    if args.clean:
        if "claude" in targets:
            remove_generated_dir(claude_dir, repo_root)
        if "codex" in targets:
            remove_generated_dir(codex_dir, repo_root)

    generated: dict[str, list[str]] = {"claude": [], "codex": []}
    generation_errors: list[str] = []
    for skill_key, skill_file, meta in host_skills:
        for host in targets:
            target_root = claude_dir if host == "claude" else codex_dir
            rel = os.path.relpath(skill_file, start=target_root / skill_key)
            out = target_root / skill_key / "SKILL.md"
            try:
                content = render_wrapper(
                    skill_key, skill_file, rel, meta, host, provenance
                )
            except ValueError as exc:
                generation_errors.append(str(exc))
                continue
            write_text(out, content)
            generated[host].append(str(out.relative_to(repo_root)))

    print(f"Canonical skills scanned: {len(canonical) + len(skipped)}")
    print(f"Valid canonical skills: {len(canonical)}")
    print(
        "Host-exposed canonical skills: "
        f"{len(host_skills)} ({', '.join(name for name, _, _ in host_skills)})"
    )
    print(f"Internal-only canonical skills: {len(canonical) - len(host_skills)}")
    print("Generated wrappers:")
    for host in targets:
        print(f"  - {host}: {len(generated[host])}")

    if skipped:
        print(f"Skipped invalid/non-skill directories ({len(skipped)}):")
        for reason in skipped:
            print(f"  - {reason}")
    if generation_errors:
        print(f"Generation errors ({len(generation_errors)}):")
        for error in generation_errors:
            print(f"  - {error}")
    if skipped or generation_errors:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run PaperTrace's lean project checks.

The validator protects the active manuscript source and decision-relevant
scientific records that actually exist. It does not require a complete paper
lifecycle skeleton, score writing, calculate hashes, or model hypothetical state
combinations.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from papertrace_validation import (  # noqa: E402
    REQUIRED_DIRS,
    REQUIRED_FILES,
    STAGE_SKILLS,
    Reporter,
    validate_figure_arguments,
    validate_intake,
    validate_method_design,
    validate_paper_state,
    validate_required_layout,
    validate_research_graph,
    validate_stage_gates,
)

DEFAULT_ROOT = Path(__file__).resolve().parents[2]


def validate(root: Path) -> Reporter:
    reporter = Reporter(root)
    validate_required_layout(root, reporter)
    paper, claim_ids = validate_paper_state(root, reporter)
    validate_intake(root, reporter)
    validate_method_design(root, reporter, paper, claim_ids)
    validate_figure_arguments(root, reporter)
    validate_research_graph(root, reporter, claim_ids)
    validate_stage_gates(root, reporter, paper)
    return reporter


def print_human_report(root: Path, reporter: Reporter) -> None:
    print(f"Repository: {root}")
    for issue in reporter.issues:
        print(f"{issue.severity.upper()} [{issue.code}] {issue.path}: {issue.message}")
    print(f"summary: {len(reporter.errors)} error(s), {len(reporter.warnings)} warning(s)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--json", action="store_true", help="emit JSON findings")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    reporter = validate(root)
    if args.json:
        print(
            json.dumps(
                {
                    "repository": str(root),
                    "errors": [asdict(issue) for issue in reporter.errors],
                    "warnings": [asdict(issue) for issue in reporter.warnings],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print_human_report(root, reporter)

    if reporter.errors:
        return 1
    if args.strict and reporter.warnings:
        return 2
    print("PASS: active source and present scientific records are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

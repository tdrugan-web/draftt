#!/usr/bin/env python3
"""Validate a draftt.config.md against docs/CONFIG-SPEC.md (rules C01 to C07).

Usage: python scripts/validate_config.py [--root PATH] CONFIG.md [CONFIG.md ...]
Exit code 1 if any error is found. The core SessionStart hook runs the same checks.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from draftt_common import Report, find_em_dashes, load_artifact_types, split_frontmatter

COMMON_TERMS = {"sprint", "epic", "story", "customer", "user", "release", "squad"}
BELOW_AA = {"wcag-2.2-a"}
BODY_LINE_LIMIT = 150


def validate_config(config_path: Path, schema: dict, types: set[str], report: Report) -> None:
    path = str(config_path)
    text = config_path.read_text(encoding="utf-8")
    fm, body, err = split_frontmatter(text)
    if err:
        report.error(path, "C01", err)
        return

    # C01, C02
    if fm.get("draftt") != 1:
        report.error(path, "C02", f"draftt must be 1, got {fm.get('draftt')!r}")
    errors = [
        e for e in Draft202012Validator(schema).iter_errors(fm)
        if list(e.path) != ["draftt"] and not (not e.path and "'draftt'" in e.message)
    ]
    for e in errors:
        loc = "/".join(str(p) for p in e.path) or "(root)"
        report.error(path, "C01", f"{loc}: {e.message}")
    if errors or fm.get("draftt") != 1:
        return

    # C03
    for key in (fm.get("terminology") or {}):
        if key not in types and key not in COMMON_TERMS:
            report.error(path, "C03", f"terminology key '{key}' is not an artifact type or common term")

    # C04
    for key, value in (fm.get("templates") or {}).items():
        if key not in types:
            report.error(path, "C04", f"templates key '{key}' is not an artifact type")
        if not (config_path.parent / value).is_file():
            report.error(path, "C04", f"template file '{value}' not found next to the config")

    # C05
    level = (fm.get("standards") or {}).get("accessibility")
    if level in BELOW_AA:
        report.error(path, "C05", f"accessibility '{level}' is below the WCAG 2.2 AA floor")

    # C06
    n = len(body.splitlines())
    if n > BODY_LINE_LIMIT:
        report.warn(path, "C06", f"body is {n} lines, keep it under {BODY_LINE_LIMIT}")

    # C07
    for line_no in find_em_dashes(text):
        report.warn(f"{path}:{line_no}", "C07", "em dash")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=Path(__file__).resolve().parent.parent, type=Path)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()

    schema = json.loads((root / "config" / "draftt.config.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    types = load_artifact_types(root)

    report = Report()
    for f in args.files:
        validate_config(f.resolve(), schema, types, report)
    report.print_and_exit("validate_config")


if __name__ == "__main__":
    main()

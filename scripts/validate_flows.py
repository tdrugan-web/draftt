#!/usr/bin/env python3
"""Validate Draftt flows against docs/FLOW-SPEC.md (rules F01 to F10).

Usage: python scripts/validate_flows.py [--root PATH] [FLOW.yaml ...]
With no files, validates every plugins/*/flows/*.yaml.
Exit code 1 if any error is found.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from draftt_common import EM_DASH, Report, load_artifact_types, load_catalog, rel

TOKEN = re.compile(r"\s*(\(|\)|,|and\b|or\b|not\b|has\b|is\b|[a-z0-9]+(?:[.-][a-z0-9]+)*)")


class ConditionError(ValueError):
    pass


def parse_condition(expr: str) -> list[tuple[str, str]]:
    """Parse a `when` expression. Return the (function, reference) calls it makes.

    Grammar:
      expr  := term (("and" | "or") term)*
      term  := "not" term | "(" expr ")" | call
      call  := "has" "(" ref ")" | "is" "(" ref "," value ")"
    """
    tokens: list[str] = []
    pos = 0
    while pos < len(expr):
        if expr[pos:].strip() == "":
            break
        m = TOKEN.match(expr, pos)
        if not m or m.end() == pos:
            raise ConditionError(f"unexpected text at '{expr[pos:].strip()}'")
        tokens.append(m.group(1))
        pos = m.end()
    calls: list[tuple[str, str]] = []
    i = 0

    def peek() -> str | None:
        return tokens[i] if i < len(tokens) else None

    def take(expected: str | None = None) -> str:
        nonlocal i
        tok = peek()
        if tok is None:
            raise ConditionError("expression ends too early")
        if expected and tok != expected:
            raise ConditionError(f"expected '{expected}', got '{tok}'")
        i += 1
        return tok

    def term() -> None:
        tok = peek()
        if tok == "not":
            take()
            term()
        elif tok == "(":
            take("(")
            expr_()
            take(")")
        elif tok in ("has", "is"):
            fn = take()
            take("(")
            ref = take()
            if fn == "is":
                take(",")
                take()
            take(")")
            calls.append((fn, ref))
        else:
            raise ConditionError(f"expected has(), is(), not, or '(', got '{tok}'")

    def expr_() -> None:
        term()
        while peek() in ("and", "or"):
            take()
            term()

    expr_()
    if peek() is not None:
        raise ConditionError(f"unexpected '{peek()}'")
    return calls


def walk_strings(node, path=""):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from walk_strings(v, f"{path}.{k}" if path else str(k))
    elif isinstance(node, list):
        for idx, v in enumerate(node):
            yield from walk_strings(v, f"{path}[{idx}]")


def validate_flow(flow_path: Path, root: Path, schema: dict, ctx: dict, report: Report) -> None:
    path = rel(flow_path, root)
    try:
        flow = yaml.safe_load(flow_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        report.error(path, "F01", f"not valid YAML: {exc}")
        return

    # F01
    errors = sorted(Draft202012Validator(schema).iter_errors(flow), key=lambda e: list(e.path))
    for e in errors:
        loc = "/".join(str(p) for p in e.path) or "(root)"
        report.error(path, "F01", f"{loc}: {e.message}")
    if errors:
        return  # structural checks below assume a valid shape

    # F02
    if flow["id"] != flow_path.stem:
        report.error(path, "F02", f"id '{flow['id']}' does not match file name '{flow_path.stem}'")

    entry = {e["id"]: e for e in flow["entry"]}
    # F09
    if not any(e.get("required") for e in flow["entry"]):
        report.error(path, "F09", "at least one entry input must be required")

    seen_steps: set[str] = set()
    all_ids: list[str] = []

    def check_ref(ref: str, where: str, available: set[str]) -> None:
        kind, name = ref.split(".", 1)
        if kind == "entry" and name not in entry:
            report.error(path, "F06", f"{where}: '{ref}' is not an entry input")
        elif kind == "steps" and name not in available:
            report.error(path, "F06", f"{where}: '{ref}' is not an earlier step")
        elif kind == "workspace" and name not in ctx["types"]:
            report.error(path, "F04", f"{where}: '{ref}' is not an artifact type")

    def check_when(cond: str, where: str, available: set[str]) -> None:
        try:
            calls = parse_condition(cond)
        except ConditionError as exc:
            report.error(path, "F08", f"{where}: when '{cond}': {exc}")
            return
        for fn, ref in calls:
            if not re.match(r"^(entry|steps|workspace)\.[a-z0-9-]+$", ref):
                report.error(path, "F08", f"{where}: '{ref}' is not a reference")
                continue
            check_ref(ref, where, available)
            if fn == "is" and not (ref.startswith("entry.") and entry.get(ref[6:], {}).get("type") == "choice"):
                report.error(path, "F08", f"{where}: is() needs a choice entry input, got '{ref}'")

    def check_skill_step(step: dict, available: set[str]) -> None:
        where = f"step '{step['id']}'"
        all_ids.append(step["id"])
        if step["skill"] not in ctx["catalog"]:
            report.error(path, "F03", f"{where}: skill '{step['skill']}' is not in catalog.yaml")
        if step["produces"] not in ctx["types"]:
            report.error(path, "F04", f"{where}: produces '{step['produces']}', not an artifact type")
        for ref in step["uses"]:
            check_ref(ref, where, available)
        if "when" in step:
            check_when(step["when"], where, available)

    for step in flow["steps"]:
        where = f"step '{step['id']}'"
        if "parallel" in step:
            all_ids.append(step["id"])
            children = {c["id"] for c in step["parallel"]}
            for child in step["parallel"]:
                for ref in child["uses"]:
                    if ref.startswith("steps.") and ref[6:] in children:
                        report.error(path, "F07", f"parallel child '{child['id']}' uses sibling '{ref}'")
                check_skill_step(child, seen_steps)
            if "when" in step:
                check_when(step["when"], where, seen_steps)
            seen_steps |= children
        elif "branch" in step:
            all_ids.append(step["id"])
            for option in step["branch"]:
                all_ids.append(option["id"])
                if "when" in option:
                    check_when(option["when"], f"{where} option '{option['id']}'", seen_steps)
                local = set(seen_steps)
                for child in option["steps"]:
                    check_skill_step(child, local)
                    local.add(child["id"])
            for option in step["branch"]:
                seen_steps |= {c["id"] for c in option["steps"]}
        else:
            check_skill_step(step, seen_steps)
        seen_steps.add(step["id"])

    # F05 (branch option ids share the namespace so references stay unambiguous)
    dupes = sorted({i for i in all_ids if all_ids.count(i) > 1})
    for d in dupes:
        report.error(path, "F05", f"id '{d}' is used more than once")

    for ref in flow["outputs"]:
        check_ref(ref, "outputs", seen_steps)

    # F10
    for loc, value in walk_strings(flow):
        if EM_DASH in value:
            report.error(path, "F10", f"em dash in {loc}")
    for line_no, line in enumerate(flow_path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("#") and EM_DASH in line:
            report.error(f"{path}:{line_no}", "F10", "em dash in comment")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=Path(__file__).resolve().parent.parent, type=Path)
    parser.add_argument("files", nargs="*", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()

    schema = json.loads((root / "docs" / "flow.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    ctx = {"catalog": load_catalog(root), "types": load_artifact_types(root)}
    files = [f.resolve() for f in args.files] or sorted(root.glob("plugins/*/flows/*.yaml"))

    report = Report()
    for f in files:
        validate_flow(f, root, schema, ctx, report)
    print(f"Validated {len(files)} flow(s).")
    report.print_and_exit("validate_flows")


if __name__ == "__main__":
    main()

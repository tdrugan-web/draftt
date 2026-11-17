#!/usr/bin/env python3
"""Lint every Draftt skill against docs/SKILL-STANDARD.md (rules L01 to L20).

Usage: python scripts/lint_skills.py [--root PATH] [--strict]
  --strict  treat warnings as errors
Exit code 1 if any error is found.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

from draftt_common import (
    KEBAB,
    Report,
    find_em_dashes,
    is_text_file,
    load_artifact_types,
    load_catalog,
    load_catalog_plugins,
    rel,
    split_frontmatter,
    split_list,
)

PORTABLE_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
REQUIRED_KEYS = {"name", "description", "license", "metadata"}
# Claude Code-only keys, allowed on flow skills (metadata.surfaces == "plugin").
CLAUDE_CODE_KEYS = {
    "when_to_use", "argument-hint", "arguments", "disable-model-invocation", "user-invocable",
    "disallowed-tools", "model", "effort", "context", "agent", "background", "hooks", "paths", "shell",
}
METADATA_KEYS = [
    "draftt-version", "plugin", "stage", "serves", "produces",
    "hands-from", "hands-to", "surfaces", "evidence",
]
STAGES = {"core", "discover", "define", "design", "validate", "market", "deliver", "lead"}
SERVES = {"pm", "ux", "trio"}
SURFACES = {"plugin", "web"}
EVIDENCE = {"required", "optional", "none"}
SECTIONS = [
    "Purpose", "Before you start", "Workflow", "Output",
    "Evidence rules", "Handoffs", "Surface notes", "References",
]
EVAL_KINDS = {"trigger", "route-elsewhere", "hard-case"}
MARKETING_WORDS = [
    "powerful", "seamless", "seamlessly", "comprehensive", "cutting-edge", "robust",
    "revolutionary", "best-in-class", "world-class", "leverage", "supercharge", "effortless",
]
USE_WHEN = re.compile(r"\buse (when|whenever)\b", re.I)


def h2_sections(body: str) -> dict[str, str]:
    """Map each H2 heading to its text, in order of appearance."""
    out: dict[str, str] = {}
    current = None
    lines: list[str] = []
    in_fence = False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## "):
            if current is not None:
                out[current] = "\n".join(lines).strip()
            current = line[3:].strip()
            lines = []
        elif current is not None:
            lines.append(line)
    if current is not None:
        out[current] = "\n".join(lines).strip()
    return out


def lint_skill(skill_dir: Path, root: Path, ctx: dict, report: Report) -> str | None:
    skill_md = skill_dir / "SKILL.md"
    path = rel(skill_md, root)
    plugin_dir_name = skill_dir.parent.parent.name
    folder = skill_dir.name

    text = skill_md.read_text(encoding="utf-8")
    fm, body, err = split_frontmatter(text)
    if err:
        report.error(path, "L03", err)
        return None

    name = fm.get("name")
    # L01, L02
    if name != folder:
        report.error(path, "L01", f"folder '{folder}' does not match name '{name}'")
    if not isinstance(name, str) or not KEBAB.match(name) or not 3 <= len(name) <= 64:
        report.error(path, "L02", f"name '{name}' must be kebab-case, 3 to 64 characters")
    elif name.startswith(plugin_dir_name + "-"):
        report.error(path, "L02", f"name must not carry the plugin prefix '{plugin_dir_name}-'")

    metadata = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    surfaces = split_list(str(metadata.get("surfaces", "")))
    plugin_only = surfaces == ["plugin"]

    # L03
    for key in REQUIRED_KEYS - fm.keys():
        report.error(path, "L03", f"missing required frontmatter key '{key}'")
    for key in fm.keys() - PORTABLE_KEYS:
        if key in CLAUDE_CODE_KEYS and plugin_only:
            continue
        hint = " (allowed only when metadata.surfaces is 'plugin')" if key in CLAUDE_CODE_KEYS else ""
        report.error(path, "L03", f"frontmatter key '{key}' is not portable{hint}")
    if "license" in fm and fm["license"] != "MIT":
        report.error(path, "L03", "license must be MIT")
    if "compatibility" in fm and len(str(fm["compatibility"])) > 500:
        report.error(path, "L03", "compatibility is over 500 characters")

    # L04, L05, L17, L18
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        report.error(path, "L04", "description is missing or empty")
        desc = ""
    else:
        desc = " ".join(desc.split())
        if len(desc) > 1024:
            report.error(path, "L04", f"description is {len(desc)} characters, max 1024")
        if not USE_WHEN.search(desc):
            report.error(path, "L05", "description needs a 'use when' or 'use whenever' clause")
        if not 400 <= len(desc) <= 700:
            report.warn(path, "L17", f"description is {len(desc)} characters, aim for 400 to 700")
        for word in MARKETING_WORDS:
            if re.search(rf"\b{re.escape(word)}\b", desc, re.I):
                report.warn(path, "L18", f"marketing word in description: '{word}'")

    # L07
    if not isinstance(fm.get("metadata"), dict):
        report.error(path, "L07", "metadata must be a mapping")
    else:
        for key in METADATA_KEYS:
            if key not in metadata:
                report.error(path, "L07", f"metadata is missing '{key}'")
        for key, value in metadata.items():
            if not isinstance(value, str):
                report.error(path, "L07", f"metadata '{key}' must be a string (lists are comma-separated)")
        if metadata.get("plugin") and metadata["plugin"] != plugin_dir_name:
            report.error(path, "L07", f"metadata.plugin '{metadata['plugin']}' but skill lives in '{plugin_dir_name}'")
        if metadata.get("stage") and metadata["stage"] not in STAGES:
            report.error(path, "L07", f"unknown stage '{metadata['stage']}'")
        for value, allowed, key in [
            (metadata.get("serves", ""), SERVES, "serves"),
            (metadata.get("surfaces", ""), SURFACES, "surfaces"),
        ]:
            items = split_list(str(value))
            if key in metadata and not items:
                report.error(path, "L07", f"metadata '{key}' is empty")
            for item in items:
                if item not in allowed:
                    report.error(path, "L07", f"unknown {key} value '{item}'")
        if metadata.get("evidence") and metadata["evidence"] not in EVIDENCE:
            report.error(path, "L07", f"unknown evidence value '{metadata['evidence']}'")

        # L08
        for key in ("hands-from", "hands-to"):
            for target in split_list(str(metadata.get(key, ""))):
                if target not in ctx["catalog"]:
                    report.error(path, "L08", f"{key} names '{target}', which is not in catalog.yaml")
        # L09
        for art in split_list(str(metadata.get("produces", ""))):
            if art not in ctx["types"]:
                report.error(path, "L09", f"produces '{art}', which is not in docs/ARTIFACT-TYPES.md")

    # L19
    entry = ctx["catalog"].get(name)
    if entry is None:
        report.error(path, "L19", f"'{name}' is not in catalog.yaml")
    else:
        if entry.get("plugin") != plugin_dir_name:
            report.error(path, "L19", f"catalog puts '{name}' in '{entry.get('plugin')}', not '{plugin_dir_name}'")
        if entry.get("status") == "planned":
            report.error(path, "L19", f"catalog status is 'planned' but the skill folder exists. Set it to draft or shipped")

    # L10
    n_lines = len(text.splitlines())
    if n_lines > 250:
        report.error(path, "L10", f"SKILL.md is {n_lines} lines, max 250")

    # L11
    sections = h2_sections(body)
    order = [h for h in sections if h in SECTIONS]
    missing = [s for s in SECTIONS if s not in sections]
    if missing:
        report.error(path, "L11", f"missing sections: {', '.join(missing)}")
    elif order != SECTIONS:
        report.error(path, "L11", f"sections out of order: {', '.join(order)}")

    # L12, L13, L14
    for f in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
        frel = rel(f, root)
        inner = f.relative_to(skill_dir).as_posix()
        if inner.split("/")[0] in ("references", "templates") and inner not in text and f.name not in text:
            report.error(frel, "L12", "not linked from SKILL.md")
        if is_text_file(f):
            content = f.read_text(encoding="utf-8", errors="replace")
            if f != skill_md and len(content.splitlines()) > 400:
                report.error(frel, "L13", f"{len(content.splitlines())} lines, max 400")
            for line_no in find_em_dashes(content):
                report.error(f"{frel}:{line_no}", "L14", "em dash")

    # L16
    if set(surfaces) == SURFACES and "scripts/" in body:
        notes = sections.get("Surface notes", "").strip()
        if not notes or notes.rstrip(".").lower() == "none":
            report.error(path, "L16", "references scripts/ on both surfaces but Surface notes says nothing")

    # L15, L06
    lint_evals(name, desc, skill_dir.parent.parent, root, ctx, report)
    return name


GRADER_TYPES = {"regex", "tool_used", "tool_order", "file_exists", "llm", "baseline"}


def skill_grader_matches(grader: dict, name: str) -> bool:
    """True when a tool_used grader checks for a Skill call to this skill."""
    return grader.get("type") == "tool_used" and grader.get("tool") == "Skill" and name in str(grader.get("input_match", ""))


def lint_evals(name: str, desc: str, plugin_dir: Path, root: Path, ctx: dict, report: Report) -> None:
    """Evals use the native `claude plugin eval` layout:
    plugins/<plugin>/evals/<skill>/<case>/prompt.md + graders/<grader>.md
    The case kind is a tag in prompt.md frontmatter: trigger, route-elsewhere, or hard-case.
    A route-elsewhere case also carries a routes-to-<sibling> tag.
    """
    evals_dir = plugin_dir / "evals" / str(name)
    path = rel(evals_dir, root)
    if not evals_dir.is_dir():
        report.error(path, "L15", "missing eval cases folder")
        return
    kinds: set[str] = set()
    cases = sorted(d for d in evals_dir.iterdir() if d.is_dir() and d.name != "results")
    for case in cases:
        cpath = rel(case, root)
        prompt = case / "prompt.md"
        if not prompt.is_file():
            report.error(cpath, "L15", "case has no prompt.md")
            continue
        fm, body, err = split_frontmatter(prompt.read_text(encoding="utf-8"))
        if err or not body.strip():
            report.error(cpath, "L15", f"prompt.md needs frontmatter and a prompt body ({err or 'empty body'})")
            continue
        tags = fm.get("tags") or []
        if not isinstance(tags, list):
            report.error(cpath, "L15", "tags must be a list")
            tags = []
        case_kinds = [t for t in tags if t in EVAL_KINDS]
        if len(case_kinds) != 1:
            report.error(cpath, "L15", "tags must include exactly one of trigger, route-elsewhere, hard-case")
            continue
        kind = case_kinds[0]
        kinds.add(kind)

        graders = []
        gdir = case / "graders"
        for g in sorted(gdir.glob("*.md")) if gdir.is_dir() else []:
            gfm, _, gerr = split_frontmatter(g.read_text(encoding="utf-8"))
            if gerr or gfm.get("type") not in GRADER_TYPES:
                report.error(rel(g, root), "L15", f"grader needs a type, one of {', '.join(sorted(GRADER_TYPES))}")
                continue
            graders.append(gfm)
        if not graders:
            report.error(cpath, "L15", "case needs at least one grader in graders/")
            continue

        fired = [g for g in graders if skill_grader_matches(g, name)]
        if kind == "route-elsewhere":
            targets = [t[len("routes-to-"):] for t in tags if isinstance(t, str) and t.startswith("routes-to-")]
            if len(targets) != 1:
                report.error(cpath, "L15", "route-elsewhere case needs one routes-to-<skill> tag")
            else:
                target = targets[0]
                if target not in ctx["catalog"]:
                    report.error(cpath, "L15", f"routes-to target '{target}' is not in catalog.yaml")
                elif target == name:
                    report.error(cpath, "L15", "route-elsewhere case routes to this same skill")
                elif target not in desc:
                    report.error(path, "L06", f"description should name route-elsewhere sibling '{target}'")
            if not any(g.get("min") == 0 and g.get("max") == 0 for g in fired):
                report.error(cpath, "L15", f"route-elsewhere case needs a tool_used Skill grader for '{name}' with min 0 and max 0")
        elif not fired:
            report.error(cpath, "L15", f"{kind} case needs a tool_used Skill grader that checks '{name}' fired")

    for kind in sorted(EVAL_KINDS - kinds):
        report.error(path, "L15", f"needs at least one '{kind}' case")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=Path(__file__).resolve().parent.parent, type=Path)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args()
    root = args.root.resolve()

    report = Report()
    ctx = {"catalog": load_catalog(root), "types": load_artifact_types(root)}
    known_plugins = load_catalog_plugins(root)

    seen: dict[str, str] = {}
    skill_dirs = sorted(p.parent for p in root.glob("plugins/*/skills/*/SKILL.md"))
    for d in sorted(root.glob("plugins/*/skills/*")):
        if d.is_dir() and not (d / "SKILL.md").exists():
            report.error(rel(d, root), "L01", "skill folder has no SKILL.md")
    for plugin_dir in sorted(p for p in root.glob("plugins/*") if p.is_dir()):
        if plugin_dir.name not in known_plugins:
            report.error(rel(plugin_dir, root), "L19", f"plugin '{plugin_dir.name}' is not in catalog.yaml")

    for d in skill_dirs:
        name = lint_skill(d, root, ctx, report)
        if name:
            if name in seen:
                report.error(rel(d, root), "L02", f"name '{name}' already used by {seen[name]}")
            seen[name] = rel(d, root)

    # L20: catalog entries marked draft or shipped need a folder
    for name, entry in ctx["catalog"].items():
        if entry.get("status") in ("draft", "shipped") and name not in seen:
            report.error("catalog.yaml", "L20", f"'{name}' is {entry['status']} but has no skill folder")

    if args.strict:
        for f in report.findings:
            f.severity = "error"
    print(f"Linted {len(skill_dirs)} skill(s).")
    report.print_and_exit("lint_skills")


if __name__ == "__main__":
    main()

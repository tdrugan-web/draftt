"""Shared helpers for Draftt's repo checks: catalog, artifact types, frontmatter, findings."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

EM_DASH = "\u2014"
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt", ".py", ".sh", ".js", ".ts", ".html", ".csv"}


@dataclass
class Finding:
    path: str
    rule: str
    severity: str  # "error" | "warning"
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.rule} {self.severity}: {self.message}"


class Report:
    def __init__(self) -> None:
        self.findings: list[Finding] = []

    def error(self, path: Path | str, rule: str, message: str) -> None:
        self.findings.append(Finding(str(path), rule, "error", message))

    def warn(self, path: Path | str, rule: str, message: str) -> None:
        self.findings.append(Finding(str(path), rule, "warning", message))

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]

    def print_and_exit(self, label: str) -> None:
        for f in self.findings:
            print(f)
        print(f"{label}: {len(self.errors)} error(s), {len(self.warnings)} warning(s)")
        sys.exit(1 if self.errors else 0)


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def load_catalog(root: Path) -> dict[str, dict]:
    """Return {skill name: entry} from catalog.yaml."""
    data = yaml.safe_load((root / "catalog.yaml").read_text(encoding="utf-8")) or {}
    return {s["name"]: s for s in data.get("skills", [])}


def load_catalog_plugins(root: Path) -> set[str]:
    data = yaml.safe_load((root / "catalog.yaml").read_text(encoding="utf-8")) or {}
    return set((data.get("plugins") or {}).keys())


def load_artifact_types(root: Path) -> set[str]:
    """Artifact types are the first-column code spans of the table in docs/ARTIFACT-TYPES.md."""
    text = (root / "docs" / "ARTIFACT-TYPES.md").read_text(encoding="utf-8")
    return set(re.findall(r"^\|\s*`([a-z0-9-]+)`\s*\|", text, re.M))


def split_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """Split a Markdown file into (frontmatter dict, body, error message).

    The opening --- must be the first line, matching Claude Code's rule.
    """
    if not text.startswith("---\n") and text.strip() != "---":
        return None, text, "file does not start with a --- frontmatter line"
    end = text.find("\n---", 4)
    if end == -1:
        return None, text, "frontmatter has no closing --- line"
    raw = text[4:end]
    after = text[end + 4 :]
    body = after[1:] if after.startswith("\n") else after
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return None, body, f"frontmatter is not valid YAML: {exc}"
    if data is None:
        data = {}
    if not isinstance(data, dict):
        return None, body, "frontmatter is not a YAML mapping"
    return data, body, None


def split_list(value: str) -> list[str]:
    """Split a comma-separated metadata value into trimmed, non-empty items."""
    return [v.strip() for v in value.split(",") if v.strip()]


def find_em_dashes(text: str) -> list[int]:
    """1-based line numbers containing an em dash."""
    return [i for i, line in enumerate(text.splitlines(), 1) if EM_DASH in line]


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES

"""Fixtures that build a throwaway Draftt repo with one valid skill, then let tests break it."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "scripts"

GOOD_DESCRIPTION = (
    "Writes a product requirements document or one-pager from a framed problem, research, "
    "and personas, with goals, non-goals, requirements, risks, and open questions. Use when "
    "someone asks for a PRD, a spec, a one-pager, requirements, a feature brief, or says "
    "'write this up for engineering'. Use whenever a problem frame is approved and the next "
    "step is defining what to build. For user stories and acceptance criteria, use "
    "user-story-writer instead. For framing the problem itself, use problem-framer instead."
)

GOOD_SKILL = """---
name: prd-writer
description: >-
  {description}
license: MIT
metadata:
  draftt-version: "1.0"
  plugin: draftt-product
  stage: define
  serves: pm, trio
  produces: prd, one-pager
  hands-from: problem-framer, interview-synthesizer
  hands-to: user-story-writer, metrics-definer, ux-flow-designer
  surfaces: plugin, web
  evidence: required
---

# PRD writer

## Purpose
Write a PRD the team can build from. Serves PMs first, then the trio.

## Before you start
Read `<draftt-workspace>` if present; otherwise use what the person has shared.

## Workflow
1. Read the problem frame.
2. Draft goals and non-goals.

## Output
Use [the PRD template](templates/prd.md). End with the artifact footer.

## Evidence rules
Tag every user or market claim [E], [A], or [S].

## Handoffs
Comes after problem-framer. Hands to user-story-writer.

## Surface notes
None.

## References
- [templates/prd.md](templates/prd.md): the default PRD structure.
- [references/non-goals.md](references/non-goals.md): load when non-goals are thin.
"""

SKILL_FIRED = """---
type: tool_used
tool: Skill
input_match: '"skill"\\s*:\\s*"(?:[\\w-]+:)?prd-writer"'
{extra}---
"""

RUBRIC = """---
type: llm
---

PASS if the reply contains a PRD with goals and non-goals.
FAIL otherwise.
"""

GOOD_CASES = {
    "trigger-reminders-prd": ("[trigger]", "Write the PRD for clinic appointment reminders.", {"skill-fired.md": SKILL_FIRED.format(extra=""), "has-prd.md": RUBRIC}),
    "route-user-stories": ("[route-elsewhere, routes-to-user-story-writer]", "Break this feature into user stories.",
                           {"not-prd-writer.md": SKILL_FIRED.format(extra="min: 0\nmax: 0\narm: both\n")}),
    "hard-thin-idea": ("[hard-case]", "PRD for Uber for dogs.", {"skill-fired.md": SKILL_FIRED.format(extra="")}),
}


def write_case(evals_dir: Path, name: str, tags: str, prompt: str, graders: dict) -> None:
    case = evals_dir / name
    (case / "graders").mkdir(parents=True, exist_ok=True)
    (case / "prompt.md").write_text(f"---\nmax_turns: 8\ntags: {tags}\n---\n\n{prompt}\n", encoding="utf-8")
    for gname, body in graders.items():
        (case / "graders" / gname).write_text(body, encoding="utf-8")


class FakeRepo:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.skill_dir = root / "plugins" / "draftt-product" / "skills" / "prd-writer"

    def write_skill(self, text: str) -> None:
        (self.skill_dir / "SKILL.md").write_text(text, encoding="utf-8")

    @property
    def evals_dir(self) -> Path:
        return self.root / "plugins" / "draftt-product" / "evals" / "prd-writer"

    def run(self, script: str, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script), "--root", str(self.root), *args],
            capture_output=True, text=True,
        )


@pytest.fixture
def repo(tmp_path: Path) -> FakeRepo:
    root = tmp_path / "draftt"
    (root / "docs").mkdir(parents=True)
    shutil.copy(REPO / "docs" / "ARTIFACT-TYPES.md", root / "docs")
    shutil.copy(REPO / "docs" / "flow.schema.json", root / "docs")
    shutil.copytree(REPO / "plugins" / "draftt-core" / "flows", root / "plugins" / "draftt-core" / "flows")
    (root / "flows").mkdir()
    shutil.copytree(REPO / "config", root / "config")

    catalog = yaml.safe_load((REPO / "catalog.yaml").read_text(encoding="utf-8"))
    for s in catalog["skills"]:
        s["status"] = "draft" if s["name"] == "prd-writer" else "planned"
    (root / "catalog.yaml").write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")

    r = FakeRepo(root)
    (r.skill_dir / "templates").mkdir(parents=True)
    (r.skill_dir / "references").mkdir()
    (r.skill_dir / "templates" / "prd.md").write_text("# [Product] PRD\n", encoding="utf-8")
    (r.skill_dir / "references" / "non-goals.md").write_text("# Non-goals\n", encoding="utf-8")
    r.write_skill(GOOD_SKILL.format(description=GOOD_DESCRIPTION))
    for name, (tags, prompt, graders) in GOOD_CASES.items():
        write_case(r.evals_dir, name, tags, prompt, graders)
    return r

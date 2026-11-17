"""Each test breaks the valid fixture skill in one way and checks the right rule fires."""

from __future__ import annotations

import shutil

import pytest

from conftest import GOOD_DESCRIPTION, GOOD_SKILL, SKILL_FIRED, write_case


def skill(**overrides) -> str:
    text = GOOD_SKILL.format(description=overrides.pop("description", GOOD_DESCRIPTION))
    for old, new in overrides.get("replace", []):
        assert old in text, old
        text = text.replace(old, new)
    return text


def test_valid_skill_passes(repo):
    result = repo.run("lint_skills.py")
    assert result.returncode == 0, result.stdout
    assert "0 error(s)" in result.stdout


@pytest.mark.parametrize(
    "rule, replace",
    [
        ("L01", [("name: prd-writer", "name: prd-maker")]),
        ("L03", [("license: MIT", "license: MIT\nargument-hint: '[idea]'")]),
        ("L07", [("  evidence: required\n", "")]),
        ("L07", [("surfaces: plugin, web", "surfaces: plugin, mobile")]),
        ("L08", [("hands-to: user-story-writer", "hands-to: ticket-writer")]),
        ("L09", [("produces: prd, one-pager", "produces: prd, spec-doc")]),
        ("L11", [("## Handoffs", "## Next steps")]),
        ("L12", [("- [references/non-goals.md](references/non-goals.md): load when non-goals are thin.\n", "")]),
        ("L14", [("Write a PRD the team", "Write a PRD \u2014 the team")]),
    ],
)
def test_rule_fires(repo, rule, replace):
    repo.write_skill(skill(replace=replace))
    result = repo.run("lint_skills.py")
    assert result.returncode == 1
    assert f" {rule} error" in result.stdout, result.stdout


def test_flow_skill_may_use_claude_code_keys(repo):
    repo.write_skill(skill(replace=[
        ("license: MIT", "license: MIT\nargument-hint: '[idea]'"),
        ("surfaces: plugin, web", "surfaces: plugin"),
    ]))
    result = repo.run("lint_skills.py")
    assert " L03 " not in result.stdout, result.stdout


def test_description_rules(repo):
    repo.write_skill(skill(description="Writes PRDs."))
    out = repo.run("lint_skills.py").stdout
    assert " L05 error" in out
    assert " L06 error" in out  # route-elsewhere sibling not named
    assert " L17 warning" in out


def test_marketing_word_warns_and_strict_fails(repo):
    repo.write_skill(skill(description=GOOD_DESCRIPTION.replace("Writes a", "Writes a comprehensive")))
    result = repo.run("lint_skills.py")
    assert result.returncode == 0 and " L18 warning" in result.stdout
    assert repo.run("lint_skills.py", "--strict").returncode == 1


def test_skill_md_too_long(repo):
    repo.write_skill(skill() + "\n".join(f"line {i}" for i in range(260)))
    assert " L10 error" in repo.run("lint_skills.py").stdout


def test_reference_file_too_long(repo):
    (repo.skill_dir / "references" / "non-goals.md").write_text("x\n" * 401, encoding="utf-8")
    assert " L13 error" in repo.run("lint_skills.py").stdout


def test_scripts_need_surface_notes(repo):
    repo.write_skill(skill(replace=[("2. Draft goals", "2. Run scripts/score.py, then draft goals")]))
    assert " L16 error" in repo.run("lint_skills.py").stdout


def test_evals_need_all_kinds(repo):
    shutil.rmtree(repo.evals_dir / "hard-thin-idea")
    assert " L15 error" in repo.run("lint_skills.py").stdout


def test_route_case_must_assert_skill_not_fired(repo):
    shutil.rmtree(repo.evals_dir / "route-user-stories")
    write_case(repo.evals_dir, "route-user-stories", "[route-elsewhere, routes-to-user-story-writer]",
               "Break this into stories.", {"fired.md": SKILL_FIRED.format(extra="")})
    assert "min 0 and max 0" in repo.run("lint_skills.py").stdout


def test_trigger_case_needs_skill_grader(repo):
    (repo.evals_dir / "trigger-reminders-prd" / "graders" / "skill-fired.md").unlink()
    assert "needs a tool_used Skill grader" in repo.run("lint_skills.py").stdout


def test_bad_grader_type(repo):
    (repo.evals_dir / "hard-thin-idea" / "graders" / "x.md").write_text("---\ntype: vibes\n---\n", encoding="utf-8")
    assert " L15 error" in repo.run("lint_skills.py").stdout


def test_planned_skill_with_folder_fails(repo):
    catalog = (repo.root / "catalog.yaml").read_text(encoding="utf-8")
    (repo.root / "catalog.yaml").write_text(
        catalog.replace("name: prd-writer\n  plugin: draftt-product\n  stage: define\n  phase: 1\n  status: draft",
                        "name: prd-writer\n  plugin: draftt-product\n  stage: define\n  phase: 1\n  status: planned"),
        encoding="utf-8",
    )
    assert " L19 error" in repo.run("lint_skills.py").stdout


def test_draft_skill_without_folder_fails(repo):
    catalog = (repo.root / "catalog.yaml").read_text(encoding="utf-8")
    (repo.root / "catalog.yaml").write_text(
        catalog.replace("name: problem-framer\n  plugin: draftt-product\n  stage: define\n  phase: 1\n  status: planned",
                        "name: problem-framer\n  plugin: draftt-product\n  stage: define\n  phase: 1\n  status: draft"),
        encoding="utf-8",
    )
    assert " L20 error" in repo.run("lint_skills.py").stdout

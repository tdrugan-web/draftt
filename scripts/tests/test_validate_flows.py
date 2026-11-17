"""Flow validator tests: the shipped flows pass, and each rule catches its break."""

from __future__ import annotations

import pytest
import yaml

from validate_flows import ConditionError, parse_condition


def write_flow(repo, flow: dict, name: str | None = None):
    path = repo.root / "flows" / f"{name or flow['id']}.yaml"
    path.write_text(yaml.safe_dump(flow, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def base_flow() -> dict:
    return {
        "id": "test-flow",
        "spec": 1,
        "version": 1,
        "title": "Test flow",
        "summary": "A flow for tests.",
        "audience": ["pm"],
        "entry": [
            {"id": "idea", "label": "Idea?", "type": "text", "required": True},
            {"id": "stage", "label": "Stage?", "type": "choice",
             "options": [{"value": "early", "label": "Early"}, {"value": "late", "label": "Late"}]},
        ],
        "steps": [
            {"id": "frame", "skill": "problem-framer", "title": "Frame", "uses": ["entry.idea"],
             "produces": "problem-frame"},
            {"id": "prd", "skill": "prd-writer", "title": "PRD", "uses": ["steps.frame"], "produces": "prd"},
        ],
        "outputs": ["steps.prd"],
    }


def test_shipped_flows_pass(repo):
    result = repo.run("validate_flows.py")
    assert result.returncode == 0, result.stdout


def test_valid_test_flow_passes(repo):
    path = write_flow(repo, base_flow())
    result = repo.run("validate_flows.py", str(path))
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize(
    "rule, mutate",
    [
        ("F01", lambda f: f.update(color="blue")),
        ("F02", lambda f: f.update(id="other-name")),
        ("F03", lambda f: f["steps"][1].update(skill="spec-writer")),
        ("F04", lambda f: f["steps"][1].update(produces="spec")),
        ("F05", lambda f: f["steps"][1].update(id="frame", uses=[])),
        ("F06", lambda f: f["steps"][0].update(uses=["steps.prd"])),
        ("F08", lambda f: f["steps"][1].update(when="exists(entry.idea)")),
        ("F08", lambda f: f["steps"][1].update(when="is(entry.idea, early)")),
        ("F09", lambda f: f["entry"][0].update(required=False)),
        ("F10", lambda f: f.update(summary="A flow \u2014 for tests.")),
    ],
)
def test_rule_fires(repo, rule, mutate):
    flow = base_flow()
    mutate(flow)
    path = write_flow(repo, flow, name="test-flow")
    result = repo.run("validate_flows.py", str(path))
    assert result.returncode == 1
    assert f" {rule} error" in result.stdout, result.stdout


def test_parallel_sibling_reference(repo):
    flow = base_flow()
    flow["steps"].insert(1, {
        "id": "landscape", "title": "Landscape", "parallel": [
            {"id": "comp", "skill": "competitive-analysis", "title": "Comp", "uses": ["steps.frame"],
             "produces": "competitive-analysis"},
            {"id": "size", "skill": "market-sizer", "title": "Size", "uses": ["steps.comp"],
             "produces": "market-sizing"},
        ],
    })
    path = write_flow(repo, flow)
    assert " F07 error" in repo.run("validate_flows.py", str(path)).stdout


def test_branch_outputs_are_referenceable(repo):
    flow = base_flow()
    flow["steps"].insert(1, {
        "id": "evidence", "title": "Evidence", "branch": [
            {"id": "real", "label": "Real", "when": "has(entry.idea)", "steps": [
                {"id": "synth", "skill": "interview-synthesizer", "title": "Synth", "uses": ["steps.frame"],
                 "produces": "research-synthesis"}]},
            {"id": "fake", "label": "Synthetic", "steps": [
                {"id": "gut", "skill": "synthetic-user", "title": "Gut", "uses": ["steps.frame"],
                 "produces": "synthetic-feedback"}]},
        ],
    })
    flow["steps"][2]["uses"] = ["steps.evidence", "steps.frame"]
    path = write_flow(repo, flow)
    result = repo.run("validate_flows.py", str(path))
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize("expr", [
    "has(entry.a)",
    "is(entry.stage, early) and not has(workspace.prd)",
    "(has(steps.a) or has(steps.b)) and not is(entry.stage, late)",
])
def test_condition_parses(expr):
    assert parse_condition(expr)


@pytest.mark.parametrize("expr", ["has(entry.a", "has entry.a", "has(entry.a) and", "len(entry.a)", "has(entry.a) xor"])
def test_condition_rejects(expr):
    with pytest.raises(ConditionError):
        parse_condition(expr)

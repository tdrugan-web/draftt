"""Config validator tests: the example passes, and each rule catches its break."""

from __future__ import annotations

import pytest

EXAMPLE = "config/draftt.config.example.md"


def write_config(repo, text: str):
    path = repo.root / "draftt.config.md"
    path.write_text(text, encoding="utf-8")
    return path


def example(repo) -> str:
    return (repo.root / EXAMPLE).read_text(encoding="utf-8")


def test_example_passes(repo):
    result = repo.run("validate_config.py", str(repo.root / EXAMPLE))
    assert result.returncode == 0, result.stdout
    assert "0 warning(s)" in result.stdout


@pytest.mark.parametrize(
    "rule, old, new",
    [
        ("C01", "size: small", "size: huge"),
        ("C01", "tracker: linear", "tracker: trello"),
        ("C02", "draftt: 1", "draftt: 2"),
        ("C03", "prd: Product brief", "spec: Product brief"),
        ("C04", "templates: {}", "templates:\n  prd: templates/missing.md"),
        ("C05", "accessibility: wcag-2.2-aa", "accessibility: wcag-2.2-a"),
    ],
)
def test_rule_fires(repo, rule, old, new):
    text = example(repo)
    assert old in text
    path = write_config(repo, text.replace(old, new, 1))
    result = repo.run("validate_config.py", str(path))
    assert result.returncode == 1
    assert f" {rule} error" in result.stdout, result.stdout


def test_template_file_found(repo):
    (repo.root / "templates").mkdir()
    (repo.root / "templates" / "our-prd.md").write_text("# PRD\n", encoding="utf-8")
    path = write_config(repo, example(repo).replace("templates: {}", "templates:\n  prd: templates/our-prd.md"))
    assert repo.run("validate_config.py", str(path)).returncode == 0


def test_long_body_and_em_dash_warn(repo):
    text = example(repo) + "\n".join("- note" for _ in range(160)) + "\nA \u2014 dash\n"
    result = repo.run("validate_config.py", str(write_config(repo, text)))
    assert result.returncode == 0
    assert " C06 warning" in result.stdout and " C07 warning" in result.stdout


def test_missing_frontmatter(repo):
    result = repo.run("validate_config.py", str(write_config(repo, "# Just notes\n")))
    assert " C01 error" in result.stdout

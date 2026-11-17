# Contributing to Draftt

Thanks for helping. Draftt is maintained by one person, so small, focused pull requests get reviewed fastest.

## The most useful contribution: misfire reports

A misfire is when a skill fires on a request it shouldn't handle, or doesn't fire when it should. Open an issue with:

- the exact prompt you typed,
- which skill fired (or none),
- which skill you expected.

Each misfire becomes a new eval case, which keeps it from coming back.

## Changing or adding a skill

1. Read the [skill standard](docs/SKILL-STANDARD.md). The linter enforces most of it.
2. For a new skill, find it in [catalog.yaml](catalog.yaml) and change its status from `planned` to `draft`. If it isn't in the catalog, open an issue first so we can check it doesn't overlap an existing skill.
3. Write the skill in `plugins/<plugin>/skills/<name>/` and at least three eval cases in `plugins/<plugin>/evals/<name>/`: a trigger case, a route-elsewhere case, and a hard case.
4. Run the checks:

   ```bash
   pip install -r scripts/requirements.txt
   python scripts/lint_skills.py
   python scripts/validate_flows.py
   cd scripts/tests && python -m pytest -q && cd ../..
   claude plugin validate . && claude plugin validate plugins/<plugin>
   ```

5. If you can, run the plugin's evals with `claude plugin eval plugins/<plugin>` and paste the summary table into your pull request. They cost model usage, so CI doesn't run them for you.
6. Add a line to [CHANGELOG.md](CHANGELOG.md) under Unreleased.

## Writing rules

- No em dashes anywhere. CI fails on them.
- Plain, specific language. No hype words.
- Examples use obviously fictional companies and people. Never invent research findings, metrics, or quotes.
- Describe and cite published frameworks. Don't copy their text.

## Pull requests

Pull requests are squash-merged, so the title becomes the commit message. Write it like a changelog line: "prd-writer: add one-pager format".

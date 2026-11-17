# Draftt repo checks

Three checkers keep skills, flows, and team configs honest. CI runs all of them on every pull request. Run them locally before you push.

```bash
pip install -r scripts/requirements.txt

python scripts/lint_skills.py                 # every skill, rules L01 to L20
python scripts/validate_flows.py              # every plugins/*/flows/*.yaml, rules F01 to F10
python scripts/validate_config.py draftt.config.md   # a team config, rules C01 to C07

cd scripts/tests && python -m pytest -q       # tests for the checkers themselves
```

| Script | Checks against | Spec |
|--------|----------------|------|
| `lint_skills.py` | `catalog.yaml`, `docs/ARTIFACT-TYPES.md`, `evals/` | `docs/SKILL-STANDARD.md` section 10 |
| `validate_flows.py` | `docs/flow.schema.json`, `catalog.yaml`, `docs/ARTIFACT-TYPES.md` | `docs/FLOW-SPEC.md` section 7 |
| `validate_config.py` | `config/draftt.config.schema.json`, `docs/ARTIFACT-TYPES.md` | `docs/CONFIG-SPEC.md` section 4 |

Each finding prints as `path: RULE severity: message`. The exit code is 1 when there's at least one error. Pass `--strict` to `lint_skills.py` to treat warnings as errors.

## Adding a skill

1. Change its `catalog.yaml` status from `planned` to `draft`.
2. Create `plugins/<plugin>/skills/<name>/SKILL.md` and `evals/<name>/evals.yaml`.
3. Run `lint_skills.py` until it's clean.

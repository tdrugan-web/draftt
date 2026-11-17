# Changelog

All notable changes to Draftt. Versions follow [semantic versioning](https://semver.org). Each plugin is versioned on its own and tagged as `<plugin>--v<version>`.

## Unreleased

## 0.1.0 (2026-11-16)

First release: the idea-to-PRD slice.

### draftt-core 0.1.0
- `draftt-context` skill: create, update, check, and explain a team's `draftt.config.md`.
- `strategic-critique` skill: riskiest assumption, strongest objection, evidence check, alternatives, and verdict.
- `idea-to-prd` flow skill: runs `flows/idea-to-prd.yaml` with approve and review checkpoints, saving artifacts to `draftt/<idea>/`.
- `critic` agent: reviews an artifact from a clean context.
- SessionStart hook: loads `draftt.config.md` into each session as team context.
- Flows: `idea-to-prd` (ready) and `idea-to-market` (draft, needs later plugins).

### draftt-product 0.1.0
- `problem-framer` skill: problem frame with users, cost, how-might-we questions, opportunity tree, and riskiest assumptions.
- `prd-writer` skill: full PRD or one-pager with goals, non-goals, prioritized requirements, experience requirements, success measures, risks, and open questions.
- Depends on `draftt-core`.

### Repository
- Skill standard, flow spec, config spec, and artifact type registry.
- Skill linter (L01 to L20), flow validator (F01 to F10), and config validator (C01 to C07), with tests.
- Eval cases in the native `claude plugin eval` format for every skill.

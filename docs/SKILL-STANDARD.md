# Draftt Skill Standard

Version 1.0. Every skill in every Draftt plugin meets this standard before it ships. CI enforces the parts marked **[lint]**. Reviewers check the rest.

This file is the contract between three things: the skills, the plugins that package them, and the website that runs them. If a rule here conflicts with a skill, the skill is wrong.

---

## 1. Principles

1. **One skill, two surfaces.** A skill runs inside Claude (as a plugin skill) and on draftt.com (through our loader). Its logic lives in the skill, never in website code.
2. **Small and composable.** A skill does one job and hands off to the next. If a description needs "and also" twice, it's two skills.
3. **Evidence over confidence.** Anything a skill says about users, markets, or numbers is tagged as evidence, assumption, or synthetic.
4. **Real artifacts.** Skills produce the thing (a PRD, a test plan), not advice about making the thing.
5. **Quiet by default.** Skills ask only when blocked, and otherwise proceed on stated assumptions.

---

## 2. Folder layout

```
plugins/<plugin>/skills/<skill-name>/
  SKILL.md          # required
  references/       # frameworks, checklists, worked examples, loaded on demand
  templates/        # output templates, one per artifact type the skill produces
  scripts/          # only when deterministic code beats prose (plugin surface only, see 8)
plugins/<plugin>/evals/<skill-name>/
  <case>/           # required, at least three, see 9
    prompt.md
    graders/*.md
```

- **[lint]** Folder name equals `name` in frontmatter.
- **[lint]** Every file in `references/` and `templates/` is linked from SKILL.md. Orphans fail.
- **[lint]** No file in the skill folder over 400 lines. Split it.

---

## 3. Frontmatter

### 3.1 Allowed fields

Draftt skills must load in Claude Code, claude.ai, and the Skills API. The last two reject unknown keys, so skills use only the portable set:

| Field | Required | Rule |
|-------|----------|------|
| `name` | yes | kebab-case, 3 to 64 characters, `a-z`, `0-9`, `-`. Unique across all four plugins. Never prefixed with the plugin name |
| `description` | yes | 1,024 characters max. See 3.2 |
| `license` | yes | `MIT` |
| `metadata` | yes | Draftt's own fields. See 3.3 |
| `compatibility` | no | Free text, 500 characters max. Use only when a skill needs something unusual |
| `allowed-tools` | no | Plugin surface only. Never broader than the skill needs |

- **[lint]** Any other key fails the build. That includes Claude Code-only fields like `argument-hint`, `disable-model-invocation`, `context`, `model`, and `hooks`.
- **Exception: flow skills** (`idea-to-prd`, `idea-to-market`) run only in Claude Code, so they may use Claude Code-only fields. They carry `metadata.surfaces: plugin` and the linter allows those fields only when that value is set.

### 3.2 The description

The description decides whether the skill fires. Claude reads every Draftt description side by side, so write for the collision, not the happy path.

Structure, in this order:

1. **What it produces**, in one sentence that starts with a verb. ("Writes a product requirements document...")
2. **When to use it**: the phrases and situations that should trigger it, including indirect ones. ("Use when someone asks for a PRD, a spec, a one-pager, requirements, or says 'write this up for engineering'.")
3. **What it is not for**, naming the sibling that handles it. ("For user stories and acceptance criteria, use user-story-writer instead.")

Rules:

- **[lint]** 1,024 characters max. Aim for 400 to 700.
- **[lint]** Contains at least one "use when" or "use whenever" clause.
- **[lint]** Names at least one sibling skill with "instead" when the evals list a route-elsewhere case for that sibling.
- Third person or imperative, never first person.
- No marketing words (powerful, seamless, comprehensive).

### 3.3 `metadata`

The Skills API spec treats `metadata` as string keys mapped to string values, so every value is a string. Lists are comma-separated.

```yaml
metadata:
  draftt-version: "1.0"            # version of this standard the skill meets
  plugin: "draftt-product"         # core | product | ux | market (full plugin name)
  stage: "define"                  # core | discover | define | design | validate | market | deliver | lead
  serves: "pm, trio"               # pm | ux | trio, primary first
  produces: "prd, one-pager"       # artifact types, see 5.3
  hands-from: "problem-framer, interview-synthesizer"
  hands-to: "user-story-writer, metrics-definer, ux-flow-designer"
  surfaces: "plugin, web"          # plugin | web, or both
  evidence: "required"             # required | optional | none, see 6
```

- **[lint]** All nine keys present, every value a string.
- **[lint]** Every skill named in `hands-from` and `hands-to` exists in `catalog.yaml`.
- **[lint]** Every type in `produces` is in the artifact type registry (`docs/ARTIFACT-TYPES.md`).

---

## 4. The SKILL.md body

### 4.1 Size

- **[lint]** 250 lines max. Claude Code's own ceiling is 500, but loaded skills stay in context across turns, so every line is a recurring cost. On the website, every line also goes into each call's prompt.
- Push frameworks, scoring rubrics, long examples, and checklists into `references/`.

### 4.2 Required sections, in this order

**[lint]** The linter checks that these H2 headings exist, in order.

```markdown
## Purpose
Two or three sentences. What job this does and who it primarily serves.

## Before you start
What to read first (team context, workspace artifacts, attached files),
the inputs this skill needs, and the default used when each is missing.

## Workflow
Numbered steps. Imperative voice. Include the decision rules that change
the output, and say why when the reason changes behavior.

## Output
The artifact's structure, pointing to the template in templates/.
Ends with the artifact footer (see 5).

## Evidence rules
How this skill tags claims (see 6). For evidence: none skills, one line
saying why.

## Handoffs
What usually comes before, what to suggest next, and when to send the
person to a sibling instead.

## Surface notes
Anything that differs between plugin and web. Write "None." if nothing does.

## References
A list of each file in references/ and templates/ with one line on
when to load it.
```

### 4.3 Writing rules

- Speak to Claude in direct imperatives. "Read the problem frame first," not "The skill should read..."
- Give the reason when it changes behavior. "Keep non-goals explicit, because engineering scopes against them."
- **[lint]** No em dashes anywhere in the skill folder.
- No invented facts in examples. Use obvious placeholders: `[Company]`, `[Persona A]`, `[metric]`, `Acme Health (fictional)`.
- Describe and cite published frameworks (RICE, JTBD, Kano). Don't paste their source text. Templates are ours.
- Accessibility (WCAG 2.2) and inclusive design are defaults in every design and research skill, written into the workflow, not tacked on as a section.

---

## 5. Inputs, context, and outputs

### 5.1 Context blocks

Both surfaces deliver context to a skill in the same tagged blocks, so the skill body never needs to know where it's running.

| Block | Plugin surface | Web surface |
|-------|----------------|-------------|
| `<draftt-team-context>` | Injected by the core SessionStart hook from `draftt.config.md`, if present | Built from the workspace's team settings |
| `<draftt-workspace>` | Absent. The skill uses the conversation and attached files | Prior approved artifacts in this workspace, each with its footer |
| `<draftt-input>` | Absent. The skill uses the person's message | The current step's inputs, resolved by the flow runner |
| `<draftt-surface>` | Absent | `web` |

Skills treat a missing block as "use the conversation." Write "Read `<draftt-workspace>` if present; otherwise use what the person has shared," never "Read the workspace."

### 5.2 Questions

- Ask only when a wrong guess would waste the whole output. Otherwise proceed and list assumptions in the artifact.
- Ask at most 3 questions, all at once, each with the default you'd use.
- **Plugin surface:** ask in plain prose.
- **Web surface** (`<draftt-surface>web</draftt-surface>`): output only a fenced `draftt-questions` block and stop. The site renders it as a form.

````markdown
```draftt-questions
- id: audience
  question: Who is the primary user for this product?
  why: The PRD's requirements change completely between buyers and end users.
  default: The end user described in the idea
```
````

### 5.3 The artifact footer

Every artifact a skill produces ends with a fenced `draftt` block (the one exception is `team-config`, see `docs/ARTIFACT-TYPES.md`). The website parses and strips it. The plugin's write-lint hook checks that it's there. It's how chained skills know what they're reading.

````markdown
```draftt
type: prd
skill: prd-writer
version: 1
labels: ai-generated, assumption-heavy
confidence: medium
based-on: problem-frame, persona
open-questions: 3
```
````

| Key | Values |
|-----|--------|
| `type` | An artifact type from `docs/ARTIFACT-TYPES.md` |
| `skill` | The producing skill's `name` |
| `version` | Integer, bumped on each revision |
| `labels` | Always `ai-generated`, plus any of `synthetic`, `assumption-heavy`, `evidence-backed`, `needs-validation` |
| `confidence` | `high`, `medium`, or `low` (see 6.2) |
| `based-on` | Artifact types this was built from, or `none` |
| `open-questions` | Count of open questions listed in the artifact |

Rules:

- `synthetic` is required whenever any content came from `synthetic-user` or from Claude role-playing users. It can't be removed by revision, only by replacing the synthetic input with real evidence.
- `evidence-backed` requires that at least half of the artifact's user or market claims are tagged `[E]`.

---

## 6. Evidence rules

### 6.1 Inline tags

Skills with `evidence: required` tag every claim about users, markets, competitors, or numbers:

| Tag | Meaning | Must include |
|-----|---------|--------------|
| `[E]` | Evidence | The source: transcript, file, or artifact name, and a quote or figure |
| `[A]` | Assumption | Nothing more, but every `[A]` also appears in the artifact's assumptions list |
| `[S]` | Synthetic | Which synthetic persona or roleplay produced it |

Never upgrade a tag. A confident-sounding assumption is still `[A]`.

### 6.2 Confidence

- **high:** most key claims are `[E]` from more than one source.
- **medium:** a mix, and the decision-critical claims are `[E]`.
- **low:** mostly `[A]` or `[S]`. Say so in the artifact's first paragraph, not just the footer.

---

## 7. Adapting to the team

- Read `<draftt-team-context>` when present: terminology, tracker, doc tool, design tool, rituals, template overrides.
- Apply terminology silently. If the team calls PRDs "briefs," the artifact is titled a brief, but `type` in the footer stays `prd`.
- If the team supplies its own template for an artifact type, use theirs and keep the footer.
- With no team context, use the skill's defaults. Never ask for team context.

---

## 8. Surfaces and tools

- **Connectors (plugin surface).** When a matching connector is available (Jira, Linear, Asana, Notion, Confluence, Figma, Google Drive, Slack), the skill may read from it freely. It may write only after the person confirms. With no connector, produce output that pastes cleanly into any tool.
- **Web surface.** No connectors and no tool calls in v1. The skill gets everything through context blocks and returns Markdown. Exports are the website's job.
- **Scripts.** `scripts/` run only on the plugin surface. A skill with scripts must still produce a correct artifact on the web without them, and its Surface notes must say what changes.
- **[lint]** A skill with `surfaces: "plugin, web"` that references `scripts/` must have a non-empty Surface notes section.

---

## 9. Evals

Evals use the native `claude plugin eval` format, so anyone can run them with `claude plugin eval plugins/<plugin>` and get scores against a no-plugin baseline. Cases live in the plugin's `evals/` folder, grouped by skill:

```
plugins/draftt-product/evals/prd-writer/
  trigger-reminders-prd/
    prompt.md
    graders/
      skill-fired.md
      has-non-goals.md
  route-user-stories/
    prompt.md
    graders/
      not-prd-writer.md
  hard-thin-idea/
    prompt.md
    graders/
      skill-fired.md
      states-low-confidence.md
```

**prompt.md** holds the run limits and the case kind in frontmatter, and the prompt as a person would type it (never naming the skill) in the body:

```markdown
---
max_turns: 10
allowed_tools: [Read, Skill]
tags: [trigger]
---

We validated that clinic schedulers lose about five hours a week to no-shows.
Write the PRD for an automated reminder feature.
```

**Case kinds**, one tag per case:

| Tag | What it proves | Required graders |
|-----|----------------|------------------|
| `trigger` | Natural phrasing fires this skill and the output meets the bar | A `tool_used` Skill grader for this skill, plus at least one grader on the output |
| `route-elsewhere` | A nearby request does **not** fire this skill. Add a `routes-to-<sibling>` tag naming the skill that should handle it | A `tool_used` Skill grader for this skill with `min: 0`, `max: 0`, `arm: both` |
| `hard-case` | Thin input, conflicting evidence, or a request on the line between two skills is handled well | A `tool_used` Skill grader for this skill, plus a grader on the hard part |

An eval run loads only the plugin under test, so a route-elsewhere case can't check that the sibling fires when the sibling lives in another plugin. It checks that this skill stays quiet, which is what a misrouted skill gets wrong.

**Graders**, one file each in `graders/`. The skill-fired grader:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?prd-writer"'
---
```

Prefer `regex` graders over `llm` graders for long outputs (they read the whole thing the same way every time), and write `llm` rubrics as concrete PASS and FAIL conditions. A good output grader for Draftt checks something the standard requires, such as the artifact footer (`regex` for "```draftt"), a non-goals section, or a low-confidence opening on thin input.

- **[lint]** At least one case of each kind, each with a `prompt.md` body and at least one grader of a known type.
- **[lint]** The required Skill graders above are present.
- **[lint]** Every `routes-to-` target exists in `catalog.yaml` and is named in this skill's description.
- Run results land in `evals/results/`, which is git-ignored.

---

## 10. Lint rules (summary)

The skill linter (`scripts/lint_skills.py`) runs in CI on every PR. `--strict` turns warnings into errors.

| ID | Check | Severity |
|----|-------|----------|
| L01 | Folder name equals `name` | error |
| L02 | `name` is kebab-case, 3 to 64 chars, unique across plugins | error |
| L03 | Only portable frontmatter keys (flow-skill exception per 3.1) | error |
| L04 | `description` 1,024 chars max | error |
| L05 | `description` has a "use when" clause | error |
| L06 | `description` names each route-elsewhere sibling | error |
| L07 | All nine `metadata` keys present, values are strings | error |
| L08 | `hands-from` and `hands-to` targets exist | error |
| L09 | `produces` types exist in the registry | error |
| L10 | SKILL.md 250 lines max | error |
| L11 | Required H2 sections present and in order | error |
| L12 | No orphaned files in `references/` or `templates/` | error |
| L13 | No file over 400 lines | error |
| L14 | No em dashes in the skill folder | error |
| L15 | Eval cases: all three kinds, prompt and graders present, required Skill graders present | error |
| L16 | Scripts referenced on a dual-surface skill have Surface notes | error |
| L17 | `description` between 400 and 700 chars | warning |
| L18 | Marketing words in `description` | warning |
| L19 | Skill is in `catalog.yaml` under the same plugin, with status `draft` or `shipped` | error |
| L20 | Every `draft` or `shipped` catalog entry has a skill folder | error |

---

## 11. Review checklist (human)

Before merging a new or changed skill:

- [ ] Run its evals and read the outputs, not just the scores.
- [ ] Read its description next to every sibling in the same stage. Would you know which to pick?
- [ ] Run it once on draftt.com staging with only `<draftt-input>`, and once in Claude Code with no context at all.
- [ ] Check that a synthetic input produces the `synthetic` label and a low-confidence opening.
- [ ] Update the catalog, README, and CHANGELOG.

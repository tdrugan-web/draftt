# Draftt Team Config Spec

Version 1.0. A team config tells every Draftt skill how your team works: what you call things, which tools you use, your templates, and your rituals. It's optional. With no config, skills use their defaults and never ask for one.

The config is one Markdown file, `draftt.config.md`. Structured settings go in YAML frontmatter, validated by `config/draftt.config.schema.json`. Anything that doesn't fit a field goes in the body as plain notes, which skills read as context.

Start from `config/draftt.config.example.md`.

---

## 1. Where Draftt looks

**Plugin surface.** The `draftt-core` SessionStart hook looks in this order and uses the first file it finds:

1. `./draftt.config.md` (project root, the usual place for a team config checked into a repo)
2. `./.claude/draftt.config.md`
3. `~/.claude/draftt.config.md` (a personal default across projects)

Configs don't merge. The first one found wins, so a project config fully replaces a personal one.

The hook validates the file and injects it as a `<draftt-team-context>` block. If the file is invalid, the hook injects nothing and prints one warning line naming the first problem. Skills then run on defaults. A broken config never blocks work.

**Web surface.** Each workspace has team settings with the same fields. The website builds the same `<draftt-team-context>` block from them. Visitors can paste a `draftt.config.md` to fill the settings, and export their settings as one.

---

## 2. Fields

Every field is optional. Leave out anything you don't care about.

### `draftt`

The spec version. Always `1`. Required if the file has frontmatter at all, so future versions can migrate old files.

### `team`

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Used in stakeholder updates and doc headers |
| `product` | string | The product or area this team owns |
| `size` | `solo`, `small`, `medium`, `large` | Skills scale ceremony to it. A solo PM doesn't get a RACI chart |
| `industry` | string | Context for examples and compliance prompts, for example `healthcare` or `fintech` |

### `terminology`

Maps a Draftt artifact type (see `docs/ARTIFACT-TYPES.md`) or a common term to your team's word. Skills use your word in titles and prose. The artifact footer `type` never changes.

```yaml
terminology:
  prd: Product brief
  user-stories: Tickets
  persona: Archetype
  sprint: Cycle
```

Keys are artifact types or one of these common terms: `sprint`, `epic`, `story`, `customer`, `user`, `release`, `squad`. Values are free text, 40 characters max.

### `tools`

Tells skills where output will end up, so it pastes cleanly, and which connector to prefer when one is available.

| Field | Values |
|-------|--------|
| `tracker` | `jira`, `linear`, `asana`, `github`, `azure-devops`, `shortcut`, `none` |
| `docs` | `notion`, `confluence`, `google-docs`, `coda`, `sharepoint`, `markdown`, `none` |
| `design` | `figma`, `penpot`, `sketch`, `none` |
| `chat` | `slack`, `teams`, `none` |
| `research` | `dovetail`, `condens`, `notion`, `none` |

Formatting follows the destination. With `tracker: jira`, stories use Jira's fields. With `docs: confluence`, docs avoid Markdown features Confluence mangles.

### `templates`

Overrides a skill's built-in template for an artifact type. Values are paths relative to the config file. Skills use your template's structure and still add the artifact footer.

```yaml
templates:
  prd: templates/our-prd.md
  research-plan: templates/research-plan.md
```

On the web surface, templates are uploaded in workspace settings instead of referenced by path.

### `rituals`

| Field | Type | Notes |
|-------|------|-------|
| `cadence` | `scrum`, `kanban`, `shape-up`, `custom` | How the team plans work |
| `sprint-length` | integer, 1 to 8 | In weeks. Ignored for `kanban` |
| `discovery` | `continuous`, `phase`, `ad-hoc` | Whether research runs every week, in up-front phases, or as needed |
| `design-review` | string | Free text, for example `Weekly crit, Thursdays` |
| `estimation` | `points`, `t-shirt`, `hours`, `none` | Used by story and prioritization skills |

### `standards`

| Field | Values | Default |
|-------|--------|---------|
| `accessibility` | `wcag-2.2-a`, `wcag-2.2-aa`, `wcag-2.2-aaa` | `wcag-2.2-aa`. Teams can raise this, not lower it below AA, because the skill standard makes AA a floor |
| `evidence` | `standard`, `strict` | `standard`. With `strict`, skills treat every untagged claim as an error and default to `low` confidence when fewer than half of key claims are `[E]` |
| `prioritization` | `rice`, `ice`, `moscow`, `kano`, `cost-of-delay` | `rice` |
| `metrics` | `north-star`, `okr`, `heart` | `north-star` |

### `voice`

How written outputs should sound.

| Field | Values |
|-------|--------|
| `tone` | `plain`, `formal`, `friendly` |
| `reading-level` | `general`, `expert` |
| `banned` | list of words or characters to avoid, for example `[leverage, synergy]` |

---

## 3. The body

Everything after the frontmatter is free-form Markdown. Use it for context a field can't hold: who your users are, constraints, compliance notes, links to strategy docs. Skills read it as background.

- Keep it short. It's loaded into every skill call. The validator warns at 150 lines.
- Don't put secrets, customer data, or anything you wouldn't want in a prompt here.

---

## 4. Validation

`scripts/validate_config.py <path>` checks a config against the schema and these rules:

| ID | Check | Severity |
|----|-------|----------|
| C01 | Frontmatter parses as YAML and validates against the schema | error |
| C02 | `draftt` is `1` | error |
| C03 | Every `terminology` key is an artifact type or an allowed common term | error |
| C04 | Every `templates` key is an artifact type, and the file exists | error |
| C05 | `accessibility` is not below AA | error |
| C06 | Body under 150 lines | warning |
| C07 | No em dashes | warning |

The SessionStart hook runs the same checks and skips injection on any error.

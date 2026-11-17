# Draftt config fields

The full reference for `draftt.config.md`, copied from Draftt's CONFIG-SPEC so the skill works when installed on its own. The file is Markdown: settings in YAML frontmatter that starts on line 1, then optional notes.

## Fields

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

Maps a Draftt artifact type (see Artifact types below) or a common term to your team's word. Skills use your word in titles and prose. The artifact footer `type` never changes.

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

## The notes section

Everything after the frontmatter is free-form Markdown. Use it for context a field can't hold: who your users are, constraints, compliance notes, links to strategy docs. Skills read it as background.

- Keep it short. It's loaded into every skill call. The validator warns at 150 lines.
- Don't put secrets, customer data, or anything you wouldn't want in a prompt here.

---

## Artifact types

Keys under `terminology` and `templates` must be one of these artifact types (or, for `terminology`, a common term listed above):

`team-config`, `idea-brief`, `problem-frame`, `critique`, `stakeholder-update`, `meeting-actions`, `research-plan`, `discussion-guide`, `research-synthesis`, `job-map`, `persona`, `journey-map`, `prd`, `one-pager`, `user-stories`, `prioritization`, `metrics-plan`, `information-architecture`, `ux-flow`, `content-guide`, `design-system-audit`, `usability-test-plan`, `heuristic-review`, `experiment-plan`, `synthetic-feedback`, `competitive-analysis`, `market-sizing`, `positioning`, `pricing-strategy`, `business-model`, `go-no-go-memo`, `gtm-plan`, `handoff-spec`, `release-notes`, `launch-checklist`, `retro`, `roadmap`, `okrs`, `team-ritual`

## Validation rules

| Check | Severity |
|-------|----------|
| Frontmatter parses as YAML, starts on line 1, and uses only the fields above | error |
| `draftt` is `1` | error |
| Every `terminology` key is an artifact type or an allowed common term | error |
| Every `templates` key is an artifact type, and the file exists next to the config | error |
| `accessibility` is not below WCAG 2.2 AA | error |
| Notes section under 150 lines | warning |
| No em dashes | warning |
| Whole file under 300 lines, or the session hook won't load it | error |

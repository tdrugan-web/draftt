# Draftt Flow Spec

Version 1.0. A flow chains skills into a guided journey. Flows are configuration, not code: one YAML file in `plugins/draftt-core/flows/` runs on draftt.com (through the flow runner) and in Claude Code (through the `idea-to-prd` and `idea-to-market` flow skills). If the website needs a flow behavior, it goes in this spec first.

Flows live in the `draftt-core` plugin because the flow skills that run them ship there, and an installed plugin contains only its own folder. The website reads them from the same place in the pinned release.

Validate any flow with `scripts/validate_flows.py`, which checks `docs/flow.schema.json` plus the cross-file rules in section 7. CI runs it on every PR.

---

## 1. Shape of a flow

```yaml
id: idea-to-prd                 # kebab-case, matches the file name
spec: 1                         # version of this spec
version: 1                      # version of this flow, bump on any change
title: Idea to PRD
summary: Turn a raw product idea into a framed problem and a reviewed PRD.
audience: [pm, trio]            # pm | ux | trio
estimate: 15-25 min             # what the website shows, human time not model time

entry:                          # what the visitor gives us up front
  - id: idea
    label: What's the idea?
    type: text                  # text | long-text | file | files | choice
    required: true
    help: A sentence or two is enough.

steps:                          # run top to bottom
  - id: frame
    skill: problem-framer
    title: Frame the problem
    uses: [entry.idea]
    produces: problem-frame
    checkpoint: approve

outputs: [steps.frame]          # what the flow hands back at the end
```

---

## 2. Entry inputs

Ask for as little as possible. Every required entry input is a moment a visitor can bounce.

| Field | Rule |
|-------|------|
| `id` | kebab-case, unique within the flow |
| `label` | The question as the visitor reads it. Plain language |
| `type` | `text`, `long-text`, `file`, `files`, or `choice` |
| `required` | Default `false`. Prefer optional inputs with good defaults |
| `help` | One line under the field |
| `options` | Required for `choice`. List of `{value, label}` |
| `accept` | For `file`/`files`: allowed kinds, any of `transcript`, `doc`, `screenshot` |
| `default` | Used when an optional input is left blank |

In Claude Code, the flow skill gathers entry inputs from the person's message and attachments, and asks only for required ones that are missing.

---

## 3. Steps

There are three kinds of step. Each needs a unique `id`.

### 3.1 Skill step (the common case)

| Field | Required | Rule |
|-------|----------|------|
| `skill` | yes | A skill `name` from the catalog |
| `title` | yes | Shown in the progress rail. Verb first: "Frame the problem" |
| `uses` | yes | References this step reads (see 4). May be empty `[]` |
| `produces` | yes | One artifact type from `docs/ARTIFACT-TYPES.md` |
| `checkpoint` | no | `none`, `review`, or `approve`. Default `review` (see 5) |
| `optional` | no | `true` lets the visitor skip the step. Default `false` |
| `when` | no | Condition for running the step (see 6). Skipped silently when false |
| `instructions` | no | One or two lines of step-specific steering passed in `<draftt-input>`. Never more. If it needs more, change the skill |

### 3.2 Parallel step

Runs independent skill steps at the same time. Each child is a skill step. No child may `use` a sibling.

```yaml
- id: landscape
  title: Map the landscape
  parallel:
    - id: competitors
      skill: competitive-analysis
      title: Review competitors
      uses: [steps.frame]
      produces: competitive-analysis
    - id: sizing
      skill: market-sizer
      title: Size the market
      uses: [steps.frame]
      produces: market-sizing
  checkpoint: review
```

The checkpoint sits on the parallel step and covers all children together.

### 3.3 Branch step

The visitor picks one path, or a `when` condition picks it for them. Each option holds its own list of skill steps.

```yaml
- id: evidence
  title: Bring in user evidence
  branch:
    - id: real
      label: I have interview transcripts
      when: has(entry.transcripts)
      steps:
        - id: synthesize
          skill: interview-synthesizer
          title: Synthesize interviews
          uses: [entry.transcripts, steps.research-plan]
          produces: research-synthesis
    - id: synthetic
      label: No research yet, give me a labeled gut check
      steps:
        - id: synthetic-check
          skill: synthetic-user
          title: Run a synthetic gut check
          uses: [steps.frame]
          produces: synthetic-feedback
```

Rules:

- If exactly one option's `when` is true, the runner takes it without asking. Otherwise the visitor chooses.
- An option with no `when` is always offered.
- Steps after a branch refer to branch outputs as `steps.evidence`, which resolves to the last artifact of whichever option ran.

---

## 4. References

`uses` and `outputs` point at things with dotted references:

| Reference | Resolves to |
|-----------|-------------|
| `entry.<input-id>` | An entry input's value or files |
| `steps.<step-id>` | The step's artifact, approved version if the step had `approve` |
| `steps.<parallel-id>` | All of a parallel step's artifacts |
| `steps.<branch-id>` | The last artifact of the branch option that ran |
| `workspace.<artifact-type>` | The latest approved artifact of that type already in the workspace, from an earlier flow or single-skill run |

Rules:

- A step may only reference entry inputs and steps above it.
- A reference to a step that was skipped (`optional` or a false `when`) resolves to nothing. Skills must handle that through their normal "input missing" defaults.
- `workspace.*` references let a flow pick up work done earlier. They resolve to nothing when absent, never to an error.

The runner packs everything a step `uses` into `<draftt-input>` and `<draftt-workspace>` blocks (see SKILL-STANDARD 5.1).

---

## 5. Checkpoints

| Value | Website | Claude Code |
|-------|---------|-------------|
| `none` | Runs and continues. Artifact still visible in the workspace | Continues without pausing |
| `review` | Shows the artifact, the visitor can edit or ask for a revision, and a Continue button moves on | Shows a short summary and continues unless the person says to stop |
| `approve` | The visitor must approve. Later steps read the approved version | Stops and waits for an explicit "approved" or revision request |

Defaults and guidance:

- Use `approve` for any artifact many later steps depend on (problem frame, PRD, positioning). A mistake there compounds.
- Use `review` for most steps.
- Use `none` sparingly, for mechanical steps the visitor won't care to read.
- A revision request reruns the same skill with the current artifact and the feedback, and bumps the footer `version`.

---

## 6. Conditions (`when`)

Conditions are deliberately tiny. Two functions, combined with `and`, `or`, `not`:

| Expression | True when |
|------------|-----------|
| `has(<ref>)` | The reference resolves to something non-empty |
| `is(<ref>, <value>)` | A `choice` entry input equals the value |

Examples: `has(entry.transcripts)`, `is(entry.stage, early) and not has(workspace.prd)`.

Anything more complex belongs in a skill's own logic, not the flow.

---

## 7. Rules the validator checks

| ID | Check |
|----|-------|
| F01 | File validates against `flow.schema.json` |
| F02 | `id` matches the file name |
| F03 | Every `skill` exists in `catalog.yaml` |
| F04 | Every `produces` is in `docs/ARTIFACT-TYPES.md` |
| F05 | Step ids are unique across the whole flow, including children |
| F06 | References point only at entry inputs or earlier steps |
| F07 | No parallel child references a sibling |
| F08 | `when` expressions parse and use only `has`, `is`, `and`, `or`, `not` |
| F09 | At least one entry input is `required` |
| F10 | No em dashes in any string |

---

## 8. Versioning

- Bump `version` on any change to steps, inputs, or checkpoints.
- The website stores `flow id + version` on each flow run, so a workspace mid-flow finishes on the version it started with.
- Bump `spec` only when this document changes in a way old flows can't satisfy.

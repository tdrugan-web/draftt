# Draftt Artifact Types

The registry of artifact `type` values. A skill's `metadata.produces`, its artifact footer, and flow `produces` fields may only use types listed here. Add a type in the same PR as the skill that first produces it.

Types are what an artifact *is*, not what a team calls it. If a team calls PRDs "briefs," the type is still `prd`.

`team-config` is the one type with no artifact footer: it's the team's `draftt.config.md`, loaded into every session, not an artifact in a workspace.

| Type | Produced by | Typical consumers |
|------|-------------|-------------------|
| `team-config` | `draftt-context` | every skill, through `<draftt-team-context>` |
| `idea-brief` | flow intake (website), `problem-framer` | `problem-framer`, `competitive-analysis` |
| `problem-frame` | `problem-framer` | `prd-writer`, `research-planner`, `positioning-builder` |
| `critique` | `strategic-critique`, `design-critique` | the skill that produced the critiqued artifact |
| `stakeholder-update` | `stakeholder-update` | none (terminal) |
| `meeting-actions` | `meeting-to-actions` | `stakeholder-update` |
| `research-plan` | `research-planner` | `interview-synthesizer`, `usability-test-planner` |
| `discussion-guide` | `research-planner` | `interview-synthesizer` |
| `research-synthesis` | `interview-synthesizer` | `persona-builder`, `journey-mapper`, `problem-framer` |
| `job-map` | `jobs-to-be-done` | `persona-builder`, `problem-framer` |
| `persona` | `persona-builder`, `synthetic-user` (labeled `synthetic`) | `prd-writer`, `ux-flow-designer`, `positioning-builder` |
| `journey-map` | `journey-mapper` | `information-architect`, `ux-flow-designer` |
| `prd` | `prd-writer` | `user-story-writer`, `metrics-definer`, `ux-flow-designer` |
| `one-pager` | `prd-writer` | `stakeholder-update`, `prd-writer` |
| `user-stories` | `user-story-writer` | `spec-handoff` |
| `prioritization` | `prioritization` | `roadmap-builder` |
| `metrics-plan` | `metrics-definer` | `experiment-designer`, `okr-writer` |
| `information-architecture` | `information-architect` | `ux-flow-designer` |
| `ux-flow` | `ux-flow-designer` | `content-designer`, `usability-test-planner`, `spec-handoff` |
| `content-guide` | `content-designer` | `ux-flow-designer`, `spec-handoff` |
| `design-system-audit` | `design-system-steward` | `spec-handoff` |
| `usability-test-plan` | `usability-test-planner` | `interview-synthesizer` |
| `heuristic-review` | `heuristic-evaluator` | `ux-flow-designer` |
| `experiment-plan` | `experiment-designer` | `metrics-definer` |
| `synthetic-feedback` | `synthetic-user` (always labeled `synthetic`) | `ux-flow-designer`, `research-planner` |
| `competitive-analysis` | `competitive-analysis` | `positioning-builder`, `problem-framer` |
| `market-sizing` | `market-sizer` | `business-model-designer`, `go-no-go-reviewer` |
| `positioning` | `positioning-builder` | `pricing-strategist`, `gtm-planner`, `prd-writer` |
| `pricing-strategy` | `pricing-strategist` | `business-model-designer` |
| `business-model` | `business-model-designer` | `go-no-go-reviewer` |
| `go-no-go-memo` | `go-no-go-reviewer` | `gtm-planner` |
| `gtm-plan` | `gtm-planner` | `launch-planner` |
| `handoff-spec` | `spec-handoff` | none (terminal) |
| `release-notes` | `release-notes-writer` | none (terminal) |
| `launch-checklist` | `launch-planner` | `retro-facilitator` |
| `retro` | `retro-facilitator` | `roadmap-builder` |
| `roadmap` | `roadmap-builder` | `okr-writer`, `stakeholder-update` |
| `okrs` | `okr-writer` | `roadmap-builder` |
| `team-ritual` | `team-rituals` | none (terminal) |

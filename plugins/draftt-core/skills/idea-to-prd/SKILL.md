---
name: idea-to-prd
description: >-
  Runs the Idea to PRD flow: takes a raw product idea through a problem frame, an optional
  pressure test, and a PRD, pausing at each checkpoint for review or approval and saving every
  artifact to a workspace folder. Use when someone wants to go from an idea to a PRD in one
  guided pass, says "take this idea all the way to a spec", "walk me through defining this", or
  runs /draftt-core:idea-to-prd. For a single artifact on its own, use problem-framer or
  prd-writer directly. For team setup, use draftt-context instead.
license: MIT
argument-hint: "[your product idea]"
metadata:
  draftt-version: "1.0"
  plugin: "draftt-core"
  stage: "core"
  serves: "pm, trio"
  produces: "problem-frame, critique, prd"
  hands-from: "draftt-context"
  hands-to: "problem-framer, strategic-critique, prd-writer"
  surfaces: "plugin"
  evidence: "none"
---

# Idea to PRD

## Purpose
Guide someone from a raw idea to an approved PRD in one session, running each Draftt skill in order and stopping where a person's judgment matters. Serves PMs and the trio. This is the plugin surface's version of the same flow draftt.com runs.

## Before you start
- Read the flow definition at `${CLAUDE_PLUGIN_ROOT}/flows/idea-to-prd.yaml`. It is the source of truth for the steps, their inputs, and their checkpoints; follow it rather than the summary below if they differ.
- The flow's steps use `problem-framer` and `prd-writer` from the draftt-product plugin, and `strategic-critique` from draftt-core. If draftt-product isn't available, stop and say: "This flow needs the draftt-product plugin. Install it with `/plugin install draftt-product@draftt`."
- Entry inputs, from the flow file: `idea` (required), `notes` (optional files), `stage` (optional choice: just an idea, talked to some users, problem validated). Take the idea from the person's message or `$ARGUMENTS`. Ask only for a missing required input; use defaults for the rest and say which you used.
- If `<draftt-team-context>` is present, every step uses it. Don't ask for team details here.

## Workflow
1. **Set up the workspace.** Make a short kebab-case slug from the idea and propose the folder `draftt/<slug>/` in the project. Each step's artifact is saved there as `NN-<step-id>.md` (for example `01-frame.md`), so later steps and later sessions can read them. If the folder exists, list what's in it and ask whether to continue from the last approved artifact or start a new version.
2. **Show the plan.** List the steps from the flow file with their checkpoints in one short block, so the person knows what's coming and that the critique step is optional.
3. **Run each step in order.** For each step, invoke its skill with the inputs the step's `uses` names: entry inputs, earlier artifacts (by reading their files), and the step's `instructions` if present. Save the artifact before moving on.
4. **Honor checkpoints exactly as the flow spec defines them:**
   - `approve`: stop. Summarize the artifact in three lines and highlight the one decision the person must check. Wait for an explicit approval or a change request. Later steps read the approved version.
   - `review`: show the summary, say you'll continue unless they want changes, and continue on their next message unless it asks for changes.
   - `none`: continue.
5. **Handle revisions.** A change request reruns the same skill with the current artifact and the feedback, saves it as the next version (`01-frame.v2.md`), and bumps the footer `version`. Never discard an earlier version.
6. **Handle optional steps.** Offer the critique step and skip it if the person declines; record it as skipped.
7. **Finish.** List the artifacts with their paths and confidence, the open questions that remain, and the next skills that apply (user-story-writer, metrics-definer, ux-flow-designer) with which plugin each needs.

## Output
The artifacts each step produces (`problem-frame`, `critique` if run, `prd`), saved in `draftt/<slug>/` with their artifact footers, plus a short closing summary in the conversation. This skill writes no artifact of its own.

## Evidence rules
None of its own. Each step's skill applies its evidence rules. Never strip evidence tags or labels when passing an artifact to the next step, and carry `synthetic` forward if any input had it.

## Handoffs
- Comes after: draftt-context when the team has set one up; otherwise first.
- Runs: problem-framer, strategic-critique (optional), prd-writer.
- Hands to: user-story-writer, metrics-definer, and ux-flow-designer once they're installed.

## Surface notes
Plugin surface only. On draftt.com the website's flow runner reads the same `idea-to-prd.yaml` and runs the same skills, with checkpoints in the interface instead of the conversation.

## References
- `${CLAUDE_PLUGIN_ROOT}/flows/idea-to-prd.yaml`: the flow definition this skill runs.

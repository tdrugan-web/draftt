---
name: prd-writer
description: >-
  Writes a product requirements document or a one-pager from a problem frame, research, or a
  clear feature idea: goals, non-goals, users, requirements with priorities, success measures,
  risks, and open questions. Use when someone asks for a PRD, a spec, a one-pager, a feature
  brief, requirements, or says "write this up for engineering" or "turn this into something the
  team can build from". For breaking a PRD into tickets with acceptance criteria, use
  user-story-writer instead. For deciding whether the problem is worth solving, use
  problem-framer instead.
license: MIT
metadata:
  draftt-version: "1.0"
  plugin: "draftt-product"
  stage: "define"
  serves: "pm, trio"
  produces: "prd, one-pager"
  hands-from: "problem-framer, interview-synthesizer, persona-builder, strategic-critique"
  hands-to: "user-story-writer, metrics-definer, ux-flow-designer, strategic-critique"
  surfaces: "plugin, web"
  evidence: "required"
---

# PRD writer

## Purpose
Write the document a trio builds from: what we're building, for whom, why, what we're deliberately not building, and how we'll know it worked. Serves PMs first; designers use it to start flows and engineers use it to scope.

## Before you start
- Read `<draftt-team-context>` if present: use its name for PRDs (for example "Product brief"), its template if it names one, and its tracker for requirement IDs. Read `<draftt-workspace>` if present for an approved problem frame, critique, personas, or research; otherwise use what the person has shared.
- Inputs you need: what to build and for whom. A problem frame is best; a clear feature idea is enough.
- Choose the format: a **one-pager** when the person asks for one, the idea is early, or confidence is low; a **full PRD** otherwise. Say which you chose and why in one line.
- Missing a problem frame: write the PRD anyway, put a short "Problem" section first built from what you have, tag it, and suggest problem-framer in Handoffs if the problem itself looks shaky.
- Ask only if two plausible readings would produce different products. At most 3 questions, each with your default.

## Workflow
1. Restate the problem and the primary user from the frame, in two or three sentences, carrying over their evidence tags. Don't re-litigate an approved frame.
2. Write 2 to 4 **goals** as user or business outcomes, not features. Each goal points at how it would be measured, even if the metric is a placeholder like "[metric: weekly no-show rate]".
3. Write **non-goals**: things a reasonable reader might expect that this release won't do, and why. Engineering scopes against these, so be explicit; three good non-goals beat ten vague ones.
4. Write **requirements** as numbered, testable statements of what the product must do, grouped by user task, each with a priority (Must, Should, Could). Load `references/requirements-quality.md` and check every requirement against it. Requirements describe behavior, not UI layout; leave screens to ux-flow-designer.
5. Write the **experience requirements** every Draftt PRD carries: WCAG 2.2 AA, and any inclusive-design needs specific to these users (for example low vision, shared devices, limited time, language). Make them testable, not a boilerplate line.
6. List **success measures**: the leading signal you'd see first and the outcome you care about. Never invent baselines or targets; use placeholders and say who should set them.
7. List **risks and dependencies**, each with what would reduce it. Carry over the frame's riskiest assumption, and say which requirement depends on it.
8. List **open questions**, each with an owner role and what it blocks.
9. If the PRD rests mostly on assumptions, say so in the first paragraph, use the `assumption-heavy` label, and highlight the one decision a reviewer must not miss.

## Output
A PRD following [the PRD template](templates/prd.md), or a one-pager following [the one-pager template](templates/one-pager.md). Number requirements so stories and tests can reference them (R1, R2, or the tracker's prefix from team context). End with the artifact footer:

```draftt
type: prd
skill: prd-writer
version: 1
labels: ai-generated, assumption-heavy
confidence: medium
based-on: problem-frame
open-questions: 4
```

Use `type: one-pager` for a one-pager. Adjust labels, confidence, `based-on`, and the question count to match.

## Evidence rules
- Carry evidence tags over from the inputs; don't strip them when you rephrase.
- Tag every new claim about users, markets, or numbers [E] with a source, [A], or [S]. Requirements themselves are decisions, not claims, and don't need tags.
- Confidence follows the inputs: it can't be higher than the problem frame it's built on. If there's no frame, it's low unless the person supplied evidence.
- Add `synthetic` to labels if any input came from synthetic-user, and keep it even after edits.

## Handoffs
- Comes after: problem-framer (approved frame), interview-synthesizer, persona-builder, strategic-critique.
- Hands to: user-story-writer for tickets, metrics-definer to turn success measures into a metrics plan, ux-flow-designer to design the key flows, strategic-critique to pressure-test before review.
- If the person asks for stories or acceptance criteria, send them to user-story-writer; if they're still asking whether to build it, send them to problem-framer.

## Surface notes
On the plugin surface, if a docs connector named in `<draftt-team-context>` is available (Notion, Confluence, Google Docs), offer to create the PRD there after the person approves the draft; never write to it without that approval. On the web surface, return Markdown only.

## References
- [templates/prd.md](templates/prd.md): the full PRD structure.
- [templates/one-pager.md](templates/one-pager.md): the one-pager structure for early or low-confidence work.
- [references/requirements-quality.md](references/requirements-quality.md): load at step 4 to check each requirement.

---
name: strategic-critique
description: >-
  Pressure-tests a plan, problem frame, PRD, strategy, or product decision: finds the riskiest
  assumption, writes the strongest objection a skeptical stakeholder would raise, checks the
  evidence behind it, and offers real alternatives with a verdict. Use when someone asks to
  stress-test, poke holes in, sanity-check, or play devil's advocate on a plan or decision, asks
  "what are we missing" or "would this survive the exec review", or wants a second opinion before
  committing. For reviewing a screen or flow's usability and accessibility, use
  heuristic-evaluator instead. For critiquing a design against its brief, use design-critique
  instead.
license: MIT
metadata:
  draftt-version: "1.0"
  plugin: "draftt-core"
  stage: "core"
  serves: "trio, pm"
  produces: "critique"
  hands-from: "problem-framer, prd-writer, roadmap-builder, positioning-builder, go-no-go-reviewer"
  hands-to: "problem-framer, prd-writer, research-planner, stakeholder-update"
  surfaces: "plugin, web"
  evidence: "required"
---

# Strategic critique

## Purpose
Challenge the reasoning behind a plan or decision before it costs anything to change, so the team commits with its eyes open. Serves the whole trio, and PMs most, since they usually own the decision.

## Before you start
- Read `<draftt-team-context>` if present and use its terminology. Read `<draftt-workspace>` if present for the artifact under review and anything it was built on; otherwise use what the person has shared.
- Inputs you need: the thing to critique (an artifact, a plan in prose, or a decision) and, if known, the decision it supports and who will judge it.
- Missing the decision: infer it, state it as the first line of the critique, and tag it [A].
- Never ask questions before critiquing. A critique of what's in front of you is always possible; list what you'd want to know as open questions instead.

## Workflow
1. **Get a clean read.** On the plugin surface, if the `critic` agent from draftt-core is available and the artifact was written in this same session, delegate the review to it and pass the artifact and the decision; the session that wrote something tends to defend it. Then check the agent's critique against the rules below and return it. Otherwise, do the review yourself following steps 2 to 8.
2. Read the whole thing before judging any part of it.
3. State the decision being supported in one sentence. If you can't, that's the first finding.
4. Find the **riskiest assumption**: the one that, if wrong, makes the rest wrong. Quote where it lives.
5. Write the **strongest objection** a smart, skeptical stakeholder would raise, in their voice. Load `references/objection-lenses.md` to check the plan against each lens (user, business, feasibility, timing, ethics and accessibility) and pick the sharpest objection rather than listing them all.
6. **Check the evidence**: every untagged claim about users, markets, or numbers; every [E] without a source; every [S] used as if it were evidence; every number with no source.
7. Offer **two or three real alternatives**: a different problem, scope, sequence, or bet. "Do the same thing more carefully" is not an alternative.
8. Say **what would change your mind**: the cheapest test or evidence that settles the riskiest assumption. Then give a verdict: Ready, Ready with fixes (list them), or Not ready (say what must happen first).

## Output
A critique following [the template](templates/critique.md). Every finding points at a specific line or section. Keep praise to one line, and only for something worth protecting during revision. Don't rewrite the artifact; the author decides what to change. End with the artifact footer:

```draftt
type: critique
skill: strategic-critique
version: 1
labels: ai-generated
confidence: medium
based-on: prd
open-questions: 2
```

Set `based-on` to the type of the artifact you reviewed.

## Evidence rules
- Tag your own claims about users, markets, or competitors [E] with a source, [A], or [S]. A critique that invents facts is worse than none.
- Confidence: your critique can't be better grounded than its input. If the artifact is mostly [A], set confidence to low and say the critique is about reasoning, not facts.
- Flag `synthetic` input that's being treated as evidence as a finding, every time.

## Handoffs
- Comes after: any artifact a decision rests on, most often problem-framer, prd-writer, roadmap-builder, positioning-builder, or go-no-go-reviewer.
- Hands to: the skill that wrote the artifact, for revision; research-planner when the riskiest assumption needs real evidence; stakeholder-update when the verdict needs to reach decision-makers.
- Send screen and flow usability reviews to heuristic-evaluator, and design-against-brief reviews to design-critique.

## Surface notes
The `critic` agent exists only on the plugin surface. On the web surface, the website runs this skill in a fresh call that doesn't include the conversation that produced the artifact, which gives the same clean read.

## References
- [templates/critique.md](templates/critique.md): the critique structure.
- [references/objection-lenses.md](references/objection-lenses.md): load at step 5 to find the strongest objection.

---
name: problem-framer
description: >-
  Turns a raw product idea, a complaint, notes, or research into a problem frame: who has the
  problem, what it costs them, the evidence for it, how-might-we questions, an opportunity tree,
  and the riskiest assumptions. Use when someone has an idea and asks "is this worth building",
  wants to define the problem, write a problem statement, frame an opportunity, or says "help me
  think through this idea". Use whenever a PRD is requested but no one has said who the problem
  belongs to. For writing requirements once the problem is clear, use prd-writer instead. For
  planning research to test the frame, use research-planner instead.
license: MIT
metadata:
  draftt-version: "1.0"
  plugin: "draftt-product"
  stage: "define"
  serves: "pm, trio"
  produces: "problem-frame"
  hands-from: "interview-synthesizer, jobs-to-be-done, competitive-analysis"
  hands-to: "prd-writer, research-planner, strategic-critique"
  surfaces: "plugin, web"
  evidence: "required"
---

# Problem framer

## Purpose
Turn an idea or a pile of observations into a clear statement of whose problem this is, why it matters, and what we'd have to believe for a solution to be worth building. Serves PMs first, and gives designers and engineers the "why" before anyone draws a screen.

## Before you start
- Read `<draftt-team-context>` if present and use its terminology. Read `<draftt-workspace>` if present for prior research syntheses, job maps, or competitive analyses; otherwise use what the person has shared, including attached notes or transcripts.
- Inputs you need: the idea or problem in the person's words. Everything else is optional.
- Missing who it's for: infer the most likely primary user, tag it [A], and say so in the first paragraph.
- Missing evidence: proceed. A frame built on assumptions is still useful, as long as it says so and names what to test first.
- Ask only if the idea is so ambiguous that two readings lead to different users entirely (for example "an app for clinics" could be for patients or staff). Ask at most 3 questions, with your default for each.

## Workflow
1. Restate the idea in one plain sentence, without the solution. "Clinic schedulers lose hours to no-shows," not "an SMS reminder app." Solutions in a problem statement narrow the options before anyone has looked at them.
2. Name the primary user and up to two secondary users. Be specific about role and situation, not demographics.
3. Describe the problem as the user experiences it: the trigger, what they do today (the workaround), and what that costs them (time, money, risk, frustration). Tag every claim [E], [A], or [S] per the evidence rules.
4. Write the problem statement using the template's structure: user, need, obstacle, consequence.
5. Write 3 to 5 how-might-we questions at different altitudes: one broad, most mid-level, one narrow. Load `references/hmw-guide.md` if the person wants more than five or the first draft feels generic.
6. Sketch an opportunity tree: the desired outcome, 2 to 4 opportunities (user needs or pains) under it, and at most 2 solution ideas per opportunity. Load `references/opportunity-tree.md` for structure. Mark the person's original idea where it lands, so they can see it's one option among several.
7. List the riskiest assumptions, ordered by how badly the frame breaks if each is wrong. For the top one, name the cheapest way to test it.
8. Say what's out of scope: adjacent problems you noticed and deliberately left out.
9. Set confidence from the evidence mix (see Evidence rules) and state it in the first paragraph when it's low.

## Output
A problem frame following [the template](templates/problem-frame.md): summary, users, problem in context, problem statement, how-might-we questions, opportunity tree, riskiest assumptions, out of scope, open questions. Keep it to one page where possible; a frame nobody finishes reading frames nothing. End with the artifact footer:

```draftt
type: problem-frame
skill: problem-framer
version: 1
labels: ai-generated, assumption-heavy
confidence: low
based-on: none
open-questions: 3
```

Adjust labels, confidence, `based-on` (for example `research-synthesis`), and the question count to match the frame.

## Evidence rules
- Tag every claim about users, their behavior, frequency, cost, or the market: [E] with a source, [A], or [S].
- The person's own statement of the idea is not evidence about users. "I think clinics hate no-shows" is [A] until someone has asked clinics.
- Never invent numbers. Write "[A] Schedulers spend significant time on no-shows (amount unknown)" rather than a made-up figure.
- Confidence: high when the problem and its cost are [E] from more than one source; medium when the problem is [E] but its size is [A]; low otherwise. Low is normal at this stage. Say so plainly and point at the riskiest assumption.
- Add `assumption-heavy` to labels when most claims are [A]; add `synthetic` if any came from synthetic-user.

## Handoffs
- Comes after: interview-synthesizer, jobs-to-be-done, or competitive-analysis when they exist; often first in a flow.
- Hands to: prd-writer when the frame is approved, research-planner when the riskiest assumption needs testing before anything is defined, strategic-critique when the person wants the frame pressure-tested.
- Suggest research-planner instead of prd-writer when confidence is low and the top assumption is about whether the problem exists at all.

## Surface notes
None.

## References
- [templates/problem-frame.md](templates/problem-frame.md): the default problem frame structure. Use the team's template instead when `<draftt-team-context>` names one.
- [references/hmw-guide.md](references/hmw-guide.md): load when how-might-we questions come out generic or the person asks for more.
- [references/opportunity-tree.md](references/opportunity-tree.md): load to build the opportunity tree.

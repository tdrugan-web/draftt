---
name: draftt-context
description: >-
  Sets up, checks, and explains the team's Draftt config (draftt.config.md): terminology, tools,
  templates, rituals, accessibility and evidence standards, and voice, so every other Draftt skill
  adapts to how the team works. Use when someone wants to set up or configure Draftt for their
  team, says "we call PRDs briefs", "we use Linear and Notion", "make Draftt use our template",
  asks why Draftt isn't using their settings, or asks what Draftt knows about their team. For
  running a guided flow from an idea, use idea-to-prd instead.
license: MIT
metadata:
  draftt-version: "1.0"
  plugin: "draftt-core"
  stage: "core"
  serves: "trio"
  produces: "team-config"
  hands-from: ""
  hands-to: "problem-framer, prd-writer, strategic-critique, idea-to-prd"
  surfaces: "plugin, web"
  evidence: "none"
---

# Draftt context

## Purpose
Create and maintain the one file that tells every Draftt skill how this team works, so nobody has to repeat it. Serves the whole trio; whoever sets up Draftt for the team usually runs it once and then rarely.

## Before you start
- Check for an existing config in this order, and use the first one found: `<draftt-team-context>` in the session, then `draftt.config.md` in the project root, then `.claude/draftt.config.md`, then `~/.claude/draftt.config.md`. Configs don't merge.
- Decide the job from the request: **create** (no config yet), **update** (change some fields), **check** (validate or explain why settings aren't applied), or **explain** (what Draftt knows about the team).
- Load `references/config-fields.md` for every field, its allowed values, and the rules. Never invent a field or a value outside that list; the session hook and the validators reject unknown ones.
- Never ask for team context when another skill runs. This skill is the only place Draftt asks.

## Workflow
1. **Create.** Ask for what matters most, in one message, with defaults: team name and product, team size, tracker, doc tool, design tool, and any terms the team uses differently (for example "briefs" for PRDs). Everything else is optional; say you'll use the defaults and the person can change them later. Then write the file from [the template](templates/draftt.config.md), removing fields the person didn't set rather than leaving placeholders.
2. **Update.** Read the current file, change only what was asked, and keep everything else, including the notes section, exactly as it was.
3. **Check.** Validate against `references/config-fields.md`: frontmatter starts on line 1, `draftt: 1` is present, every key and value is allowed, terminology and template keys are artifact types or common terms, template files exist, accessibility is AA or higher, notes stay under 150 lines and hold no secrets or customer data. Report each problem with the line and the fix. If the session has no `<draftt-team-context>` block but a valid file exists, the hook didn't load it: say to start a new session or run `/clear`, and check the file isn't over 300 lines.
4. **Explain.** Summarize what the config makes Draftt do differently, in plain language: "PRDs will be titled 'Product brief'", "stories will use Linear's format".
5. Before writing a file on the plugin surface, show the full content and confirm the location (project root by default, `~/.claude/` for a personal default across projects). Overwriting an existing config needs the person's explicit yes.

## Output
A `draftt.config.md` file with YAML frontmatter and an optional notes section, following [the template](templates/draftt.config.md). The team config is the one Draftt output with no artifact footer, because it is configuration that every session loads, not an artifact in a workspace. For check and explain jobs, reply with the findings instead of a file.

## Evidence rules
None. This skill records the team's own choices; it makes no claims about users or markets.

## Handoffs
- Comes first, before any other skill, or whenever the team's tools or terms change.
- Hands to: every Draftt skill reads the config through `<draftt-team-context>`. After creating one, suggest idea-to-prd or problem-framer as a first run.

## Surface notes
On the plugin surface, the draftt-core SessionStart hook loads the file into each new session as `<draftt-team-context>`; changes apply from the next session or after `/clear`. On the web surface, there is no file: the website keeps the same fields as workspace team settings, so return the config content for the website to save, and accept a pasted `draftt.config.md` to fill those settings.

## References
- [references/config-fields.md](references/config-fields.md): every field, allowed values, and validation rules.
- [templates/draftt.config.md](templates/draftt.config.md): the starting file for new configs.

# Draftt

Claude skills for product and UX teams. Draftt takes a product from a raw idea to a framed problem and a PRD your team can build from. Every claim about users or markets is tagged as evidence, assumption, or synthetic, so nobody mistakes a guess for research.

Draftt is a set of Claude Code plugins. The same skills will also power [draftt.com](https://draftt.com), where anyone can use them without installing anything.

> **Status: v0.1, early.** Five skills across two plugins. More are coming stage by stage: research, design, validation, and market. See the [catalog](#whats-in-it).

## Try it in five minutes

You need [Claude Code](https://code.claude.com). In a Claude Code session:

```
/plugin marketplace add tdrugan-web/draftt
/plugin install draftt-product@draftt
```

Installing `draftt-product` also installs `draftt-core`, which it depends on. Then run your first flow:

```
/draftt-core:idea-to-prd A tool that helps small landlords track tenant repair requests
```

Draftt frames the problem, stops so you can approve it, offers an optional pressure test, then writes the PRD. Each artifact is saved in `draftt/<your-idea>/` in your project, so you can edit it and pick up later.

You don't have to use slash commands. Ask in your own words and the right skill picks it up:

- "Is this idea worth building? Help me figure out the actual problem."
- "Write the PRD for this."
- "Poke holes in this plan before I take it to leadership."

Full setup, including team configuration: [docs/INSTALL.md](docs/INSTALL.md).

## What makes Draftt different

- **Evidence you can see.** Claims carry [E] evidence (with a source), [A] assumption, or [S] synthetic tags. A PRD built on assumptions says so in its first paragraph.
- **Synthetic is never research.** Anything from roleplayed users is labeled "Synthetic, not real users," and the label can't be edited away.
- **Checkpoints, not autopilot.** Flows stop where your judgment matters, and later steps build only on what you approved.
- **Adapts to your team.** One `draftt.config.md` file sets your terminology ("product brief", not "PRD"), tools, templates, and rituals. Every skill reads it.
- **Accessible by default.** WCAG 2.2 AA is a floor in every requirement and design skill, not an afterthought.
- **Tested like code.** Every skill ships with evals you can run yourself with `claude plugin eval`, plus a linter that enforces the [skill standard](docs/SKILL-STANDARD.md).

## What's in it

| Plugin | Skill | What it does |
|--------|-------|--------------|
| draftt-core | `draftt-context` | Sets up and checks your team's Draftt config |
| draftt-core | `strategic-critique` | Pressure-tests a plan, frame, or PRD: riskiest assumption, strongest objection, alternatives, verdict |
| draftt-core | `idea-to-prd` | Guided flow from idea to problem frame to PRD, with checkpoints |
| draftt-product | `problem-framer` | Turns an idea into a problem frame: users, cost, how-might-we questions, opportunity tree, riskiest assumptions |
| draftt-product | `prd-writer` | Writes a PRD or one-pager with goals, non-goals, prioritized requirements, risks, and open questions |

`draftt-core` also includes a **critic** agent that reviews artifacts from a clean context, and a session hook that loads your team config.

The full roadmap is 39 skills in four plugins (`draftt-core`, `draftt-product`, `draftt-ux`, `draftt-market`), listed in [catalog.yaml](catalog.yaml).

## Repository layout

```
.claude-plugin/marketplace.json   the Draftt marketplace
plugins/<plugin>/                 each plugin: skills, agents, hooks, evals
plugins/draftt-core/flows/        guided flows, shared with draftt.com
docs/                             skill standard, flow spec, config spec, artifact types
config/                           example team config and its schema
scripts/                          linter and validators that CI runs
catalog.yaml                      every planned and shipped skill
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Skill misfires (a skill fired when it shouldn't have, or didn't when it should) are the most useful reports.

## License

[MIT](LICENSE) © 2026 Tom Drugan

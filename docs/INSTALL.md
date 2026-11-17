# Install Draftt

## What you need

- [Claude Code](https://code.claude.com), recent enough to support plugin dependencies.

## Install

In a Claude Code session:

```
/plugin marketplace add tdrugan-web/draftt
/plugin install draftt-product@draftt
```

Or from your shell:

```bash
claude plugin marketplace add tdrugan-web/draftt
claude plugin install draftt-product@draftt
```

`draftt-product` depends on `draftt-core`, so installing it installs both. To install only the core plugin (team config, critique, and flows), install `draftt-core@draftt` instead.

Run `/reload-plugins` or start a new session, then type `/draftt` to see the skills.

## Set up your team (optional, two minutes)

Draftt works without any setup. To make it use your team's words and tools, ask:

> Set up Draftt for my team. We use Linear and Notion, and we call PRDs "product briefs".

The `draftt-context` skill writes a `draftt.config.md` to your project root. Commit it so your whole team gets the same behavior. From the next session on, every Draftt skill reads it.

You can also copy [config/draftt.config.example.md](../config/draftt.config.example.md) and edit it by hand. Every field is in [CONFIG-SPEC.md](CONFIG-SPEC.md). Check a hand-edited file with:

```bash
python scripts/validate_config.py draftt.config.md
```

Draftt looks for the config in this order and uses the first one it finds:

1. `draftt.config.md` in your project root
2. `.claude/draftt.config.md`
3. `~/.claude/draftt.config.md`, a personal default for all projects

## Your first run

```
/draftt-core:idea-to-prd A tool that helps small landlords track tenant repair requests
```

What happens:

1. Draftt proposes a folder, `draftt/<idea>/`, for the artifacts.
2. **Frame the problem.** It writes a problem frame and stops for your approval.
3. **Pressure-test the framing** (optional). The critic agent reviews the frame from a clean context.
4. **Write the PRD.** It builds on the approved frame and stops for approval.

Every artifact ends with a small `draftt` block recording its type, confidence, labels, and what it was built from. Leave it in: later skills read it.

## Run the evals

Each plugin ships eval cases in its `evals/` folder. Running them makes real model calls on your account:

```bash
claude plugin eval plugins/draftt-product
```

## Update and remove

```bash
claude plugin update draftt-product
claude plugin uninstall draftt-product
```

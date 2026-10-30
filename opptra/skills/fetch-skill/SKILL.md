---
name: fetch-skill
description: Pulls the latest Opptra skills from github.com/opptra/agent-skills and links them for Cursor, Claude Code, and Codex. Use when a developer asks to fetch, pull, sync, update, or get the latest Opptra skills.
disable-model-invocation: true
---

# Fetch skills

Pull `main` from `https://github.com/opptra/agent-skills.git` and point each tool at the skill folders in that checkout. Do not merge, rebase, or discard local changes.

## Checkout

If the current directory contains `.cursor-plugin/marketplace.json` and `opptra/skills/`, update that directory. Otherwise use `~/agent-skills`, and clone it when it is missing:

```bash
git clone https://github.com/opptra/agent-skills.git ~/agent-skills
```

Stop if the checkout has uncommitted changes or is not on `main`. Tell the developer what is in the way.

## Pull and link

```bash
git pull --ff-only origin main
./install.sh
```

Run that from the checkout. `./install.sh` links every skill into `~/.claude/skills`, `~/.codex/skills`, `~/.cursor/skills`, and `~/.config/opencode/skills`, refreshes the local bare cache at `~/.cache/opptra/sdlc-resources.git`, and verifies the pinned `@fission-ai/openspec` version. Do not put anything in `~/.cursor/skills-cursor`.

Remove a symlink in those three directories only when it points at `opptra/skills/<name>` inside this checkout and that folder no longer contains `SKILL.md`. Leave every other skill alone.

Tell the developer the commit that was pulled and the skill names that are now linked. A new terminal or a new agent chat picks up a skill that was added on this pull.

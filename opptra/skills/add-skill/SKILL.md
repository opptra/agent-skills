---
name: add-skill
description: Adds a new Opptra skill to the opptra/agent-skills repository and opens a pull request. Use when a developer asks to add, create, or publish a skill for the team.
disable-model-invocation: true
---

# Add a skill

A team skill is a folder in this repository at `opptra/skills/<name>/SKILL.md`. Cursor discovers it from that folder. Do not edit `.cursor-plugin/marketplace.json` or `opptra/.cursor-plugin/plugin.json` to register it.

Do not write the skill into `~/.cursor/skills`, `~/.claude/skills`, `~/.codex/skills`, or `~/.cursor/skills-cursor`. Those are install locations. `fetch-skill` links them after the pull request is on `main`.

## Ask

Get the skill name, what it does, when it should run, and whether it is org-wide (mockups, decks, emails, dashboards — no GitHub app) or engineering (`create-app`, `feature`, infra). Both kinds still go in `opptra/skills/<name>/`. The name is lowercase letters, numbers, and hyphens, at most 64 characters, and it does not start or end with a hyphen. If `opptra/skills/<name>/SKILL.md` already exists, stop and say so.

## Where to write

Use the current directory when it contains `.cursor-plugin/marketplace.json` and `opptra/skills/`. Otherwise use `~/agent-skills` when that clone exists. If neither exists, clone `https://github.com/opptra/agent-skills.git` into `~/agent-skills` and use that.

Branch from `main` as `skill/<name>`. Do not commit on `main`.

## SKILL.md

```markdown
---
name: <name>
description: <what it does, in third person>. Use when <the words a developer would say>.
---

# <Title>

<Steps the agent follows. Include the exact commands when the steps must not vary.>
```

The description states what the skill does and when to use it. It is third person, specific, and under 1024 characters. It does not say "I can" or "you can".

Keep the file short. Put long reference material in `reference.md` beside `SKILL.md` and link it once. Omit `disable-model-invocation` on `opptra`, `create-app`, `change-app`, `align-app`, `adopt-terraform`, `feature`, `bug`, `opptra-design-system`, `opptra-branding`, and `opptra-dashboard`. Set `disable-model-invocation: true` on a skill that must be named, including `add-skill`, `modify-skill`, `fetch-skill`, and shared references.

Add one row to the skill table in `README.md`.

## Pull request

Commit on the branch and open one pull request into `main`. The body says what the skill does and when it runs. You do not merge.

If the checkout has no `origin`, leave the branch local and tell the developer the repository has to be on GitHub before the pull request can be opened.

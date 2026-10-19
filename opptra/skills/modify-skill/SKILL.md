---
name: modify-skill
description: Changes an existing Opptra skill in the opptra/agent-skills repository from the developer's instructions and opens a pull request. Use when a developer asks to modify, edit, change, or update an existing skill.
---

# Modify a skill

A team skill is a folder in this repository at `opptra/skills/<name>/SKILL.md`. Change that folder. Do not edit `.cursor-plugin/marketplace.json` or `opptra/.cursor-plugin/plugin.json` to register a skill.

Do not write the skill into `~/.cursor/skills`, `~/.claude/skills`, `~/.codex/skills`, or `~/.cursor/skills-cursor`. Those are install locations. `fetch-skill` links them after the pull request is on `main`.

## Ask

Get the skill name and the change the developer wants. The name is the folder under `opptra/skills/`. If `opptra/skills/<name>/SKILL.md` does not exist, stop and say so. Do not create a new skill here. A new skill follows `add-skill`.

Apply only the change the developer described. Leave the rest of the skill as it is. If the request is ambiguous, ask what to change before editing.

## Where to write

Use the current directory when it contains `.cursor-plugin/marketplace.json` and `opptra/skills/`. Otherwise use `~/agent-skills` when that clone exists. If neither exists, clone `https://github.com/opptra/agent-skills.git` into `~/agent-skills` and use that.

Branch from `main` as `skill/<name>`. Do not commit on `main`. If that branch already exists, stop and say so.

## What may change

- `SKILL.md` frontmatter and body, to match the developer's change
- `reference.md`, `examples.md`, or `scripts/` beside that skill, when the change needs them
- The skill's row in the table in `README.md`, when what it does or when it runs changed

The `name` in frontmatter stays the folder name unless the developer asked to rename the skill. A rename moves `opptra/skills/<old>/` to `opptra/skills/<new>/`, updates the `name` field, the README row, and every mention of the old name in this repository. The new name is lowercase letters, numbers, and hyphens, at most 64 characters, and it does not start or end with a hyphen.

The description states what the skill does and when to use it. It is third person, specific, and under 1024 characters. It does not say "I can" or "you can".

Keep `SKILL.md` short. Put long reference material in `reference.md` beside `SKILL.md` and link it once. Leave `disable-model-invocation` as it is unless the developer asked to change it.

## Pull request

Commit on the branch and open one pull request into `main`. The body says which skill changed and what the developer asked to change. You do not merge.

If the checkout has no `origin`, leave the branch local and tell the developer the repository has to be on GitHub before the pull request can be opened.

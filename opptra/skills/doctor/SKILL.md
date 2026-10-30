---
name: doctor
description: Checks that this machine can use Opptra skills. Use when a developer asks if they are set up, says opptra doctor, or is about to create an app and the tools may be missing. Does not score a repository and does not scaffold one.
---

# Doctor

This skill checks the laptop. It does not write an app, and it does not print the 17-point scorecard. `sdlc.py doctor` is a different command: it aliases `sdlc.py status --table` inside a repository.

Read Pins in `../session/SKILL.md` and print the route banner first:

```text
Route: doctor | Checks: skills, gh, Linear, Python, Node, OpenSpec
Human Gates: none
```

Run the checks. Print one line per check, `ok` or `fix`, and stop. Do not start `create-app` or `align-app` in this turn.

## Checks

1. **Skills commit.** From the agent-skills checkout that contains this skill, `git rev-parse --short HEAD`. If that fails, the fix is `fetch-skill`.
2. **GitHub auth.** `gh auth status` must succeed.
3. **Repo creation in `opptra`.** `gh api orgs/opptra --jq .login` must print `opptra`. Org members can create private repositories. Do not create one during this check.
4. **Linear.** If a Linear tool is available, read one existing issue or list one issue. `ok` when an issue comes back. `fix` when Linear is not connected. Do not invent a ticket id.
5. **Python.** `python3 --version` must run.
6. **Node.** `node --version` must run.
7. **OpenSpec pin.** Source `opptra/pins.env` from the agent-skills checkout (from this skill directory, `../../pins.env`). `openspec --version` must equal `OPENSPEC_VERSION`. If it does not, the fix is `npm install -g "@fission-ai/openspec@${OPENSPEC_VERSION}"`. Do not install `@latest`.

## How to finish

Print the seven lines, then one sentence: what to fix before starting an app. When every line is `ok`, say the next step is `create-app` for a new repository or `align-app` for an existing one.

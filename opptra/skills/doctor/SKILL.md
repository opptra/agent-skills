---
name: doctor
description: Checks that this machine can use Opptra skills. Use when a developer asks if they are set up, says opptra doctor, or is about to create an app and the tools may be missing. Does not score a repository and does not scaffold one.
---

# Doctor

This skill checks the laptop. It does not write an app, and it does not print the 17-point scorecard. `sdlc.py doctor` is a different command: it aliases `sdlc.py status --table` inside a repository.

Read Pins in `../session/SKILL.md` and print the route banner first:

```text
Route: doctor | Checks: skills, generator-cache, gh, Linear, Python, uv, Node, terraform, OpenSpec
Human Gates: Ask once to auto-fix if OpenSpec pin, generator cache, or skill symlinks need updating
```

Run the checks. Print one line per check, `ok` or `fix`. If the only issues are the OpenSpec pin, generator cache, or skill symlinks, offer to run `./install.sh` from the `agent-skills` checkout to fix them automatically. Do not start `create-app` or `align-app` in this turn.

## Checks

1. **Skills commit.** From the agent-skills checkout that contains this skill, `git rev-parse --short HEAD`. If that fails, the fix is `fetch-skill` (`./install.sh`).
2. **Generator cache.** Check `~/.cache/opptra/sdlc-resources.git`. `ok` when present; `fix` (run `./install.sh`) when missing.
3. **GitHub auth.** `gh auth status` must succeed.
4. **Repo creation in `opptra`.** `gh api orgs/opptra --jq .login` must print `opptra`. Org members can create private repositories. Do not create one during this check.
5. **Linear.** If a Linear tool is available, read one existing issue or list one issue. `ok` when an issue comes back. `warn (LOCAL-DRAFT available for local scaffolding; connect Linear MCP before opening PRs)` when Linear is not connected. Do not invent a ticket id.
6. **Python.** `python3 --version` must run (3.12+ recommended).
7. **uv.** `uv --version` must run. If missing, the fix is `curl -LsSf https://astral.sh/uv/install.sh | sh`.
8. **Node.** `node --version` must run.
9. **Terraform.** `terraform --version` (optional locally, used by `make ci` `terraform fmt -check`). `ok` when present, `warn` when missing.
10. **OpenSpec pin.** Source `opptra/pins.env` from the agent-skills checkout (from this skill directory, `../../pins.env`). `openspec --version` must equal `OPENSPEC_VERSION`. If it does not, the fix is `./install.sh` or `npm install -g "@fission-ai/openspec@${OPENSPEC_VERSION}"`. Do not install `@latest`.

## How to finish

Print the ten lines, then one sentence: what to fix before starting an app (or offer to run `./install.sh` for auto-fixable items). When every required line is `ok`, say the next step is `create-app` for a new repository or `align-app` for an existing one.

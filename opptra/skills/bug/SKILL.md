---
name: bug
description: Fixes a Linear bug with a failing test first on a branch off main, following the repository's capability rules. Use when a developer gives a bug ticket id or asks to fix a bug. A product or design choice follows the feature skill; an infra or schedule change follows change-app.
---

# Bug

Before you edit files, print the Route Banner, tell the developer what you will change, and wait for a yes. Before a commit, show the message and the file list and wait. Before a push or a pull request, show the branch, title, and body and wait. Do not commit or push in the same turn as the code unless they already agreed.

## Route Banner

```text
Route: bug | Branch: fix/<ticket-id>-<slug>
Stages: 1. Linear & Rules Check  2. Failing Reproduction Test  3. Minimal Fix  4. Component Gates  5. PR to main
Forbidden in this Route: Editing service.yaml, infra/, .github/workflows/, or cron schedules (use change-app)
```

## Steps

1. Read the Linear issue first. If Linear is not connected, stop and tell the developer to connect Linear in Cursor or Claude. Do not invent a ticket id.
2. Read `service.yaml`, `AGENTS.md` (including `## Product contract`), and `.cursor/rules/*.mdc` (and run `python3 scripts/sdlc.py status --check` if `scripts/sdlc.py` is present).
   - If the fix needs a product or design choice, stop and follow the `feature` skill, including an OpenSpec.
   - If the fix requires changing `service.yaml`, `config/jobs.yaml` schedules, `infra/`, or `.github/workflows/`, stop and follow the `change-app` skill.
3. Branch from `main` as `fix/<ticket-id>-<short-slug>`.
4. Write a test that reproduces the bug and fails on the current code. Then make the fix so the test passes.
5. Run the checks for every component you touched (`uv run ruff check .` and `uv run pytest` for Python; `npm run lint`, `npm run typecheck`, and `npm test --if-present` for UI).
6. Push and open one pull request into `main` with the Linear link, how to reproduce the bug, and the test name.

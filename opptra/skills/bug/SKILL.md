---
name: bug
description: Fixes a Linear bug with a failing test first on a branch off main, reusing the current branch's Linear ticket when related (or creating/reading one after confirming the bug plan), and running local hooks and make ci before committing. Use when a developer gives a bug ticket id or asks to fix a bug.
---

# Bug

Before you edit files, read `../session/SKILL.md` and print the Route Banner with its Pins lines. Tell the developer what you will change, and wait for a yes. Before a commit, run `.githooks/pre-commit` and `make ci`, show the message and the file list, and wait. Before a push or a pull request, show the branch, title, and body and wait. Never pass `--no-verify` to `git commit` or `git push`.

## Route Banner

```text
Route: bug | Branch: fix/<ticket-id>-<slug>
Stages: 1. Plan & Smart Linear Check  2. Failing Reproduction Test  3. Minimal Fix  4. Hooks & make ci  5. PR to main
Forbidden in this Route: Editing service.yaml, infra/, .github/workflows/, or cron schedules (use change-app)
```

## Steps

1. **Understand the bug and resolve the Linear ticket.** Follow Resume in `../session/SKILL.md`. Confirm the root cause and fix plan with the developer, then read and follow `../linear-continuity/SKILL.md`. When you create or update the issue, include the reproduction steps, expected result, and actual result. Add a bug note only when that note is not already on the issue. When the developer approves the plan, write `.sdlc/intent.yaml` with `route: bug` and no `depth`, before the test. Do not invent a ticket id.
2. **Read `service.yaml`, `AGENTS.md` (including `## Product contract`), and `.cursor/rules/*.mdc`:**
   - If the fix needs a product or design choice, stop and follow the `feature` skill, including an OpenSpec.
   - If the fix requires changing `service.yaml`, `config/jobs.yaml` schedules, `infra/`, or `.github/workflows/`, follow `../change-app/SKILL.md` in this same chat. Open that infra pull request first. Set `.sdlc/intent.yaml` `route` to `bug` and `next_step` to `wait-for-infra`. Write the failing test only after the developer says that pull request has merged.
3. **Branch (if not already on the active ticket branch):**
   - Branch from `main` as `fix/<ticket-id>-<short-slug>`.
4. **Failing test first, then minimal fix:**
   - Write a test that reproduces the bug and fails on the current code. Then make the fix so the test passes.
5. **Run hooks and local CI (`make ci`):**
   - Run `.githooks/pre-commit` and `make ci` (or `uv run ruff check . && uv run pytest` for Python; `npm run lint && npm run typecheck && npm test --if-present` for UI).
6. **Push and open (or update) one pull request into `main`** with the Linear link, how to reproduce the bug, and the test name.
7. **Print the ship card and stop.** Follow Ship card in `../session/SKILL.md`, including the rollback line. Do not push `staging` or open the production pull request unless the developer asks.

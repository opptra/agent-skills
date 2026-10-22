---
name: bug
description: Fixes a Linear bug with a failing test first on a branch off main, following the repository's capability rules. Use when a developer gives a bug ticket id or asks to fix a bug. A product or design choice follows the feature skill; an infra or schedule change follows change-app.
---

# Bug

Before you edit files, tell the developer what you will change and wait for a yes. Before a commit, show the message and the file list and wait. Before a push or a pull request, show the branch, title, and body and wait. Do not commit or push in the same turn as the code unless they already agreed.

Read the Linear issue first. If Linear is not connected, stop. Tell the developer to connect Linear in Cursor or Claude. Do not invent a ticket id.

Read `service.yaml` and `.cursor/rules/*.mdc` (and run `python3 scripts/sdlc.py status --check` if `scripts/sdlc.py` is present) so you know which components, test runners, and capability rules (`database.mdc`, `firestore.mdc`, `job.mdc`, `react.mdc`) apply.

- If the fix needs a product or design choice, stop and follow the `feature` skill, including an OpenSpec.
- If the fix requires changing `service.yaml`, `config/jobs.yaml` schedules, `infra/`, or `.github/workflows/`, stop and follow the `change-app` skill.

Otherwise:

1. Branch from `main` as `fix/<ticket-id>-<short-slug>`.
2. Write a test that reproduces the bug and fails on the current code. Then make the fix so the test passes.
3. Run the checks for every component you touched:
   - Python (`api`, `job`, `worker`): `uv run ruff check .` and `uv run pytest`
   - UI (`frontend/`): `npm run lint`, `npm run typecheck`, and `npm test --if-present`
4. Push and open one pull request into `main`.

The body has the Linear link, how to reproduce the bug, and the test name. It has no OpenSpec.

The developer squash-merges as `fix: <ticket-id> <short summary>`, pushes `main` onto `staging`, checks staging, then opens the pull request from `main` to `production`. The issue is Done when production has applied.

A production bug uses this same path. It does not skip staging. A rollback is a revert merged to `main`, then a push to `staging`, then a merge to `production`.

You do not merge, and you do not deploy, unless the developer asks.

---
name: bug
description: Fixes a Linear bug with a failing test first on a branch off main, reusing the current branch's Linear ticket when related (or creating/reading one after confirming the bug plan), and running local hooks and make ci before committing. Use when a developer gives a bug ticket id or asks to fix a bug.
---

# Bug

Before you edit files, print the Route Banner, tell the developer what you will change, and wait for a yes. Before a commit, run `.githooks/pre-commit` and `make ci`, show the message and the file list, and wait. Before a push or a pull request, show the branch, title, and body and wait. Never pass `--no-verify` to `git commit` or `git push`.

## Route Banner

```text
Route: bug | Branch: fix/<ticket-id>-<slug>
Stages: 1. Plan & Smart Linear Check  2. Failing Reproduction Test  3. Minimal Fix  4. Hooks & make ci  5. PR to main
Forbidden in this Route: Editing service.yaml, infra/, .github/workflows/, or cron schedules (use change-app)
```

## Steps

1. **Understand the bug and resolve the Linear ticket (do not create a new ticket on every prompt):**
   - Confirm the root cause and fix plan with the developer first.
   - Check the current Git branch (`git branch --show-current`) and `.sdlc/state.yaml`:
     - **If a ticket branch (`feat/<ticket-id>-...`, `fix/<ticket-id>-...`) is already checked out:**
       - If this bug fix is part of the work on that same ticket, reuse `<ticket-id>`, update the Linear issue with the bug note if not already present, and stay on the current branch.
       - If it is unclear whether the bug belongs to the current branch's ticket or is a separate issue, ask the developer whether to **(a)** keep it on the current ticket `<ticket-id>` or **(b)** switch to `main` and use/create a separate Linear bug ticket.
     - **If on `main`:** Read the Linear issue they named, or once the fix plan is agreed, create **one** Linear bug issue with the reproduction steps, expected result, and actual result. Do not invent a ticket id.
2. **Read `service.yaml`, `AGENTS.md` (including `## Product contract`), and `.cursor/rules/*.mdc`:**
   - If the fix needs a product or design choice, stop and follow the `feature` skill, including an OpenSpec.
   - If the fix requires changing `service.yaml`, `config/jobs.yaml` schedules, `infra/`, or `.github/workflows/`, stop and follow the `change-app` skill.
3. **Branch (if not already on the active ticket branch):**
   - Branch from `main` as `fix/<ticket-id>-<short-slug>`.
4. **Failing test first, then minimal fix:**
   - Write a test that reproduces the bug and fails on the current code. Then make the fix so the test passes.
5. **Run hooks and local CI (`make ci`):**
   - Run `.githooks/pre-commit` and `make ci` (or `uv run ruff check . && uv run pytest` for Python; `npm run lint && npm run typecheck && npm test --if-present` for UI).
6. **Push and open (or update) one pull request into `main`** with the Linear link, how to reproduce the bug, and the test name.

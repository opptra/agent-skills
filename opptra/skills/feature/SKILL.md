---
name: feature
description: Implements a Linear feature by planning with the user first, reusing the current branch's Linear ticket when related (or creating one ticket after plan approval), syncing the OpenSpec to Linear, running local hooks and make ci, and opening one pull request into main. Use when a developer gives a feature ticket id or asks to implement a feature.
---

# Feature

`main` is the default branch and does not deploy. You do not merge. You do not push `staging` or open the production pull request unless the developer asks. A staging try is a direct push of the feature branch to `staging`. Do not merge `main` into `staging`. Production is only a pull request from `main` into `production`.

Before you edit files, print the Route Banner, tell the developer what you will change, and wait for a yes. Before a commit, run `.githooks/pre-commit` and `make ci`, show the message and the file list, and wait. Before a push or a pull request, show the branch, title, and body and wait. Never pass `--no-verify` to `git commit` or `git push`.

## Route Banner

```text
Route: feature | Branch: feat/<ticket-id>-<slug> | Depth: standard (or migration when porting/reconciling)
Stages: 1. Plan & Smart Linear Check  2. OpenSpec & Linear Sync  3. Tests & Code  4. Hooks & make ci  5. PR to main
Forbidden in this Route: Editing service.yaml, infra/, .github/workflows/, or cron schedules (use change-app)
```

## Steps

1. **Understand, plan first, and resolve the Linear ticket (do not create a new ticket on every prompt):**
   - Discuss and clarify what needs to be implemented and agree on the plan with the developer before creating a Linear ticket.
   - Check the current Git branch (`git branch --show-current`) and `.sdlc/state.yaml` first:
     - **If a ticket branch (`feat/<ticket-id>-...`, `fix/<ticket-id>-...`, `infra/<ticket-id>-...`) is already checked out:**
       - If the new ask is clearly part of that same ticket/feature, reuse that `<ticket-id>`, update the existing Linear issue with the added requirements and spec updates, and stay on the current branch.
       - If it is not clear whether the new ask belongs to the current ticket or is a separate task, ask the developer whether to **(a)** add it to the existing Linear issue `<ticket-id>` on this branch or **(b)** switch to `main` and use/create a new Linear issue.
     - **If on `main` (or no ticket branch is active):**
       - If the developer gave a ticket ID, read that issue from Linear.
       - If they did not give a ticket ID, once the developer approves your implementation plan, create **one** Linear issue containing the agreed title, requirements, and acceptance criteria. Do not invent a ticket id.
2. **Verify alignment and capabilities:**
   - Read `service.yaml`, `AGENTS.md` (including `## Product contract`), and `.cursor/rules/*.mdc` (and run `python3 scripts/sdlc.py status --check` if `scripts/sdlc.py` is present).
   - If the feature requires a new cloud resource, database, bucket, queue, secret ID, job entrypoint, or cron schedule change in `service.yaml`, stop and route that part to `change-app` in a separate pull request first.
   - Note the active capabilities (`postgres`, `firestore`, `bigquery`, `bucket`, `queue`, `scheduled-jobs`, `ui`, `api`) so the OpenSpec and tests enforce their rules (`database.mdc`, `firestore.mdc`, `bigquery.mdc`, `job.mdc`, `react.mdc`, and `## Product contract`).
3. **Ensure OpenSpec is ready:**
   - Run `openspec --version`. If missing, install `@fission-ai/openspec@latest`. If `openspec/` is missing, run `openspec init --tools cursor,claude`.
4. **Branch (if not already on the ticket's feature branch):**
   - Branch from `main` as `feat/<ticket-id>-<short-slug>`.
5. **Write or update the OpenSpec and sync it to Linear:**
   - Create or update the change under `openspec/` before writing product code:
     - If `database: postgres` is active and the schema changes, list the Alembic migration. Never run migrations against production from a laptop.
     - If `database: firestore` or `scheduled-jobs` is active, state the idempotency keys (`processed/{job}/items/{id}`), lease lock behavior, and non-zero exit behavior on upstream 429/5xx.
     - If `database: bigquery` is active, list any checked-in SQL DDL changes and verify currency/NULL handling.
   - Push the OpenSpec summary, tasks, and acceptance criteria to the Linear issue (`save_issue` / `save_comment`) so Linear stays the source of truth.
6. **Implement and test:**
   - Implement only the agreed tasks, with unit tests covering the new behavior and edge cases.
7. **Run hooks and local CI (`make ci`):**
   - Run `.githooks/pre-commit` and `make ci` (or `uv run ruff check . && uv run pytest` for Python; `npm run lint && npm run typecheck && npm test --if-present` for UI). Fix any failures before asking to commit.
8. **Commit, push, and open the pull request:**
   - Push the branch and open (or update) one pull request into `main` with the Linear link, OpenSpec path, what changed, commands run, and the risk box.

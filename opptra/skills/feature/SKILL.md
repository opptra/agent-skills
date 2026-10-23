---
name: feature
description: Implements a Linear feature on a branch off main, verifying repo alignment first, writing an OpenSpec and tests that follow the repo's capability rules, and opening one pull request into main. Use when a developer gives a feature ticket id or asks to implement a feature.
---

# Feature

`main` is the default branch and does not deploy. You do not merge. You do not push `staging` or open the production pull request unless the developer asks. A staging try is a direct push of the feature branch to `staging`. Do not merge `main` into `staging`. Production is only a pull request from `main` into `production`.

Before you edit files, print the Route Banner, tell the developer what you will change, and wait for a yes. Before a commit, show the message and the file list and wait. Before a push or a pull request, show the branch, title, and body and wait. Do not commit or push in the same turn as the code unless they already agreed.

## Route Banner

```text
Route: feature | Branch: feat/<ticket-id>-<slug> | Depth: standard (or migration when porting/reconciling)
Stages: 1. Linear & Alignment Check  2. OpenSpec  3. Failing/Unit Tests & Code  4. Component Gates  5. PR to main
Forbidden in this Route: Editing service.yaml, infra/, .github/workflows/, or cron schedules (use change-app)
```

## Steps

1. Read the Linear issue. If Linear is not connected, stop and tell the developer to connect Linear in Cursor or Claude. The ticket id is required for the branch, the commit, and the pull request. Do not invent a ticket id.
2. Read `service.yaml`, `AGENTS.md` (including `## Product contract`), and `.cursor/rules/*.mdc` (and run `python3 scripts/sdlc.py status --check` if `scripts/sdlc.py` is present).
   - If the feature requires a new cloud resource, database, bucket, queue, secret ID, job entrypoint, or cron schedule change in `service.yaml`, stop and route that part to `change-app` in a separate pull request first.
   - Note the active capabilities (`postgres`, `firestore`, `bigquery`, `bucket`, `queue`, `scheduled-jobs`, `ui`, `api`) so the OpenSpec and tests enforce their rules (`database.mdc`, `firestore.mdc`, `bigquery.mdc`, `job.mdc`, `react.mdc`, and `## Product contract`).
3. Run `openspec --version`. If that fails, stop and ask them to install it with `npm install -g @fission-ai/openspec@latest`, then wait. If the repo has no `openspec/` directory, stop and ask them to run `openspec init --tools cursor,claude` from the repo root, then wait.
4. Branch from `main` as `feat/<ticket-id>-<short-slug>`.
5. Create the change with `openspec new` using the ticket slug. Follow `openspec instructions` and write the artifacts under `openspec/` before any product code:
   - If `database: postgres` is active and the schema changes, list the Alembic migration. Never run migrations against production from a laptop.
   - If `database: firestore` or `scheduled-jobs` is active, state the idempotency keys (`processed/{job}/items/{id}`), lease lock behavior, and non-zero exit behavior on upstream 429/5xx.
   - If `database: bigquery` is active, list any checked-in SQL DDL changes and verify currency/NULL handling.
6. Implement only those tasks, with unit tests covering the new behavior and edge cases.
7. From each component you touched, run its checks (`uv run ruff check .` and `uv run pytest` for Python; `npm run lint`, `npm run typecheck`, and `npm test --if-present` for UI).
8. Push the branch and open one pull request into `main` with the Linear link, OpenSpec path, what changed, commands run, and the risk box.

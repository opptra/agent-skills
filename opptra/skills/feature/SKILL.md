---
name: feature
description: Implements a Linear feature on a branch off main, verifying repo alignment first, writing an OpenSpec and tests that follow the repo's capability rules, and opening one pull request into main. Use when a developer gives a feature ticket id or asks to implement a feature.
---

# Feature

`main` is the default branch and does not deploy. You do not merge. You do not push `staging` or open the production pull request unless the developer asks.

Before you edit files, tell the developer what you will change and wait for a yes. Before a commit, show the message and the file list and wait. Before a push or a pull request, show the branch, title, and body and wait. Do not commit or push in the same turn as the code unless they already agreed.

1. Read the Linear issue. If Linear is not connected, stop. Tell the developer to connect Linear in Cursor or Claude. The ticket id is required for the branch, the commit, and the pull request. Do not invent a ticket id.
2. Read `service.yaml` and `.cursor/rules/*.mdc` (and run `python3 scripts/sdlc.py status --check` if `scripts/sdlc.py` is present).
   - If the feature requires a new cloud resource, database, bucket, queue, secret ID, job entrypoint, or cron schedule change in `service.yaml`, stop and tell the developer to run `change-app` in a separate pull request first. Product code and changes to `service.yaml`, `config/jobs.yaml` schedules, `infra/`, or `.github/workflows/` are separate pull requests.
   - Note the active capabilities (`postgres`, `firestore`, `bucket`, `queue`, `scheduled-jobs`, `ui`, `api`) so the OpenSpec and tests follow their rules (`database.mdc`, `firestore.mdc`, `job.mdc`, `react.mdc`, plus any domain rules in `.cursor/rules/`).
3. Run `openspec --version`. If that fails, stop and ask them to install it with `npm install -g @fission-ai/openspec@latest`, then wait. If the repo has no `openspec/` directory, stop and ask them to run `openspec init --tools cursor,claude` from the repo root, then wait. Do not install it or run init until they say yes.
4. Branch from `main` as `feat/<ticket-id>-<short-slug>`.
5. Create the change with `openspec new` using the ticket slug. Follow `openspec instructions` and write the artifacts under `openspec/` before any product code:
   - If `database: postgres` is active and the schema changes, the OpenSpec lists the Alembic migration. Never run that migration against production from the laptop.
   - If `database: firestore` or `scheduled-jobs` is active, the OpenSpec states the idempotency keys (`processed/{job}/items/{id}`), lease lock behavior, and non-zero exit behavior on upstream 429/5xx.
6. Implement only those tasks, and write unit tests covering the new behavior and edge cases.
7. From each component you touched, run its checks:
   - Python (`api`, `job`, `worker`): `uv run ruff check .` and `uv run pytest`
   - UI (`frontend/`): `npm run lint`, `npm run typecheck`, and `npm test --if-present`
8. Push the branch. Open one pull request into `main`.

The pull request body has the Linear link, the OpenSpec path, what changed, the commands you ran, and the risk box.

The developer squash-merges as `feat: <ticket-id> <short summary>`, pushes `main` onto `staging`, verifies staging, and opens a pull request from `main` to `production`. The Linear issue is Done when production has applied.

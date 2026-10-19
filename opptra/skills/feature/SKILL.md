---
name: feature
description: Implements a Linear feature on a branch off main, with an OpenSpec and the code in one pull request into main. Use when a developer gives a feature ticket id or asks to implement a feature.
---

# Feature

`main` is the default branch and does not deploy. You do not merge. You do not push `staging` or open the production pull request unless the developer asks.

Before you edit files, tell the developer what you will change and wait for a yes. Before a commit, show the message and the file list and wait. Before a push or a pull request, show the branch, title, and body and wait. Do not commit or push in the same turn as the code unless they already agreed.

1. Read the Linear issue. If Linear is not connected, stop. Tell the developer to connect Linear in Cursor or Claude. The ticket id is required for the branch, the commit, and the pull request. Do not invent a ticket id.
2. Run `openspec --version`. If that fails, stop and ask them to install it with `npm install -g @fission-ai/openspec@latest`, then wait. If the repo has no `openspec/` directory, stop and ask them to run `openspec init --tools cursor,claude` from the repo root, then wait. Do not install it or run init until they say yes.
3. Branch from `main` as `feat/<ticket-id>-<short-slug>`.
4. Create the change with `openspec new` using the ticket slug. Follow `openspec instructions` and write the artifacts under `openspec/` before any product code.
5. Implement only those tasks.
6. From each component you touched, run its tests. API, job, and worker: `uv run ruff check .` and `uv run pytest`. UI: `npm run lint` and `npm run typecheck`.
7. Push the branch. Open one pull request into `main`.

The pull request body has the Linear link, the OpenSpec path, what changed, the commands you ran, and the risk box. Product code stays out of `infra/`, workflows, and `service.yaml`. Those changes are a separate pull request.

The developer squash-merges. The commit message is `feat: <ticket-id> <short summary>`.

After that, the developer pushes `main` onto `staging`. That push deploys staging. There is no pull request for staging. They open the URL. Then they open a pull request from `main` to `production`. That deploys production. The Linear issue is Done when production has applied.

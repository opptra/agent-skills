---
name: feature
description: Implements a Linear feature on a branch off main, with an OpenSpec and the code in one pull request into main. Use when a developer gives a feature ticket id or asks to implement a feature.
---

# Feature

`main` is the default branch and does not deploy. You do not merge. You do not push `staging` or open the production pull request unless the developer asks.

1. Branch from `main` as `feat/<ticket-id>-<short-slug>`.
2. Read the Linear issue. Write an OpenSpec on that branch: what will change, the approach, and the task list.
3. Implement only those tasks. You may commit as you go.
4. From each component you touched, run its tests. API, job, and worker: `uv run ruff check .` and `uv run pytest`. UI: `npm run lint` and `npm run typecheck`.
5. Push the branch. Open one pull request into `main`.

The pull request body has the Linear link, the OpenSpec path, what changed, the commands you ran, and the risk box. Product code stays out of `infra/`, workflows, and `service.yaml`. Those changes are a separate pull request.

The developer squash-merges. The commit message is `feat: <ticket-id> <short summary>`.

After that, the developer pushes `main` onto `staging`. That push deploys staging. There is no pull request for staging. They open the URL. Then they open a pull request from `main` to `production`. That deploys production. The Linear issue is Done when production has applied.

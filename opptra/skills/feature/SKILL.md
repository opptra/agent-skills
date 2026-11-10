---
name: feature
description: Implements a Linear feature by planning with the user first, reusing the current branch's Linear ticket when related (or creating one ticket after plan approval), choosing express, standard, or migration depth, syncing the OpenSpec to Linear when depth requires it, running local hooks and make ci, and opening one pull request into main. Use when a developer gives a feature ticket id or asks to implement a feature.
---


## Skill version check

Before following this skill, read and follow [Skill freshness](../session/SKILL.md#skill-freshness). Run it once per user request, including when this skill is invoked directly. A route or shared reference within the same request reuses that result. After an update, reread this file and any shared instructions before continuing.

# Feature

`main` is the default branch and does not deploy. You do not merge. You do not push `staging` or open the production pull request unless the developer asks. A staging try is a direct push of the feature branch to `staging` (`git push --force-with-lease origin <branch>:staging`). Do not merge `main` into `staging`. Production is only a pull request from `main` into `production`.

Use a streamlined **2-Gate confirmation flow**:
- **Gate 1 (Plan & OpenSpec):** Read `../session/SKILL.md`, print the Route Banner with its Pins lines, draft/update the OpenSpec (when `standard` or `migration`), present the plan + spec summary, and wait for a yes before editing product files.
- **Gate 2 (Ship Gate):** After implementing tests and product code, run `.githooks/pre-commit` and `make ci` automatically until green, then show the commit message, file list, branch name, and pull request title/body together in **one** prompt and wait for a yes before committing, pushing, and opening the PR. Never pass `--no-verify` to `git commit` or `git push`.

## Route Banner

```text
Route: feature | Branch: feat/<ticket-id>-<slug> | Depth: express | standard | migration
Stages: 1. Plan, Linear & OpenSpec (Gate 1)  2. Tests & Code  3. Auto Hooks & make ci  4. Commit & PR to main (Gate 2)
Human Gates: Gate 1 — Approve Plan & OpenSpec; Gate 2 — Commit, push, and open PR after make ci passes
Infrastructure: Follow the ownership and file map in ../session/SKILL.md.
```

## Steps

1. **Understand, plan first, and resolve the Linear ticket (Gate 1).** Follow Resume in `../session/SKILL.md`. Then read and follow `../linear-continuity/SKILL.md`. Choose depth from Depth in `../session/SKILL.md`.
2. **Verify alignment and capabilities:**
   - Read `service.yaml`, `AGENTS.md` (including `## Product contract`), and `.cursor/rules/*.mdc` (and run `python3 scripts/sdlc.py status --check` if `scripts/sdlc.py` is present).
   - Follow **Find the owner of a deployment setting** in [session](../session/SKILL.md). In an app-owned repo, include coupled Terraform and code changes on this branch and in the same PR. Use a separate infrastructure PR for a prerequisite that must land first. In a generator-owned repo, use `change-app` and preserve the existing stacked PR flow.
   - Note the active capabilities (`postgres`, `firestore`, `bigquery`, `bucket`, `queue`, `scheduled-jobs`, `ui`, `api`) so the OpenSpec and tests enforce their rules (`database.mdc`, `firestore.mdc`, `bigquery.mdc`, `job.mdc`, `react.mdc`, and `## Product contract`).
3. **Ensure OpenSpec is ready and draft the spec (combined into Gate 1)** for `standard` and `migration`. Skip this step on `express`.
   - Follow OpenSpec pin in `../session/SKILL.md`. If `openspec/` is missing, run `openspec init --tools cursor,claude`. Do not install `@latest`.
   - Draft the OpenSpec summary and present it with the implementation plan for **Gate 1** approval:
     - If `database: postgres` is active and the schema changes, list the Alembic migration. Never run migrations against production from a laptop.
     - If `database: firestore` or `scheduled-jobs` is active, state the idempotency keys (`processed/{job}/items/{id}`), lease lock behavior, and non-zero exit behavior on upstream 429/5xx.
     - If `database: bigquery` is active, list any checked-in SQL DDL changes and verify currency/NULL handling.
   - Once the developer approves **Gate 1**, write `.sdlc/intent.yaml`, write the OpenSpec files under `openspec/`, and sync the agreed requirements, acceptance criteria, and OpenSpec summary to the Linear issue (`save_issue` / `save_comment`).
4. **Branch (if not already on the ticket's feature branch):**
   - Branch from `main` (or from `infra/<ticket-id>-<short-slug>` when stacking on an open infra PR) as `feat/<ticket-id>-<short-slug>`.
5. **Implement and test:**
   - Implement only the agreed tasks, with unit tests covering the new behavior and edge cases.
6. **Run hooks and local CI (`make ci`) automatically:**
   - Run `.githooks/pre-commit` and `make ci` (or `uv run ruff check . && uv run pytest` for Python; `npm run lint && npm run typecheck && npm test --if-present` for UI). Fix any failures automatically before prompting the developer.
7. **Commit, push, and open the pull request (Gate 2):**
   - Present the commit message, file list, branch name, and pull request title/body (with the Linear link, OpenSpec path when present, what changed, commands run, and risk box) in a single confirmation prompt. On yes, commit, push, and open (or update) one pull request into `main`.
8. **Print the ship card and stop.** Follow Ship card in `../session/SKILL.md`. Do not push `staging` or open the production pull request unless the developer asks.

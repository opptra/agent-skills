---
name: bug
description: Fixes a Linear bug with a failing test first on a branch off main, reusing the current branch's Linear ticket when related (or creating/reading one after confirming the bug plan), and running local hooks and make ci before committing. Use when a developer gives a bug ticket id or asks to fix a bug.
---


## Skill version check

Before following this skill, read and follow [Skill freshness](../session/SKILL.md#skill-freshness). Run it once per user request, including when this skill is invoked directly. A route or shared reference within the same request reuses that result. After an update, reread this file and any shared instructions before continuing.

# Bug

Use a streamlined **2-Gate confirmation flow**:
- **Gate 1 (Root Cause, Failing Test & Fix Plan):** Read `../session/SKILL.md`, print the Route Banner with its Pins lines, investigate the codebase to find the root cause, present the root cause, reproduction test plan, and minimal fix, and wait for a yes.
- **Gate 2 (Ship Gate):** Write and verify the failing reproduction test, apply the minimal fix, run `.githooks/pre-commit` and `make ci` automatically until green, then show the commit message, file list, branch name, and pull request title/body together in **one** prompt and wait for a yes before committing, pushing, and opening the PR. Never pass `--no-verify` to `git commit` or `git push`.

## Route Banner

```text
Route: bug | Branch: fix/<ticket-id>-<slug>
Stages: 1. Root Cause & Linear Check (Gate 1)  2. Failing Reproduction Test & Minimal Fix  3. Auto Hooks & make ci  4. Commit & PR to main (Gate 2)
Human Gates: Gate 1 — Approve Root Cause & Fix Plan; Gate 2 — Commit, push, and open PR after make ci passes
Infrastructure: Follow the ownership and file map in ../session/SKILL.md.
```

## Steps

1. **Understand the bug, locate the root cause, and resolve the Linear ticket (Gate 1).** Follow Resume in `../session/SKILL.md`. Inspect the code to pinpoint the root cause, confirm the fix plan with the developer, then read and follow `../linear-continuity/SKILL.md`. When you create or update the issue, include the reproduction steps, expected result, and actual result. Add a bug note only when that note is not already on the issue. When the developer approves the plan, write `.sdlc/intent.yaml` with `route: bug` and no `depth`, before the test. Do not invent a ticket id.
2. **Read `service.yaml`, `AGENTS.md` (including `## Product contract`), and `.cursor/rules/*.mdc`:**
   - If the fix needs a product or design choice, stop and follow the `feature` skill, including an OpenSpec.
   - Follow **Find the owner of a deployment setting** in [session](../session/SKILL.md). In an app-owned repo, include coupled Terraform and code changes on this branch and in the same PR. Use a separate infrastructure PR for a prerequisite that must land first. In a generator-owned repo, use `change-app` and preserve the existing stacked PR flow.
3. **Branch (if not already on the active ticket branch):**
   - Branch from `main` (or from `infra/<ticket-id>-<short-slug>` when stacked) as `fix/<ticket-id>-<short-slug>`.
4. **Failing test first, then minimal fix:**
   - Write a test that reproduces the bug and verify it fails on the current code. Then make the minimal fix so the test passes.
5. **Run hooks and local CI (`make ci`) automatically:**
   - Run `.githooks/pre-commit` and `make ci` (or `uv run ruff check . && uv run pytest` for Python; `npm run lint && npm run typecheck && npm test --if-present` for UI). Fix any lint or test failures before prompting the developer.
6. **Commit, push, and open (or update) one pull request into `main` (Gate 2):**
   - Present the commit message, file list, branch name, and pull request title/body (with the Linear link, how to reproduce the bug, and the test name) in one confirmation prompt. On yes, commit, push, and open the PR.
7. **Print the ship card and stop.** Follow Ship card in `../session/SKILL.md`, including the rollback line. Do not push `staging` or open the production pull request unless the developer asks.

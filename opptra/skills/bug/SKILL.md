---
name: bug
description: Fixes a Linear bug with a failing test first, on a branch off main. Use when a developer gives a bug ticket id or asks to fix a bug. A product or design choice follows the feature skill instead.
---

# Bug

If the fix needs a product or design choice, stop and follow the feature skill, including an OpenSpec.

Otherwise:

1. Branch from `main` as `fix/<ticket-id>-<short-slug>`.
2. Write a test that fails on the current code. Then make the fix. The test passes.
3. Run the same checks as a feature for every component you touched.
4. Push and open one pull request into `main`.

The body has the Linear link, how to reproduce the bug, and the test name. It has no OpenSpec.

The developer squash-merges as `fix: <ticket-id> <short summary>`, pushes `main` onto `staging`, checks the URL, then opens the pull request from `main` to `production`. The issue is Done when production has applied.

A production bug uses this same path. It does not skip staging. A rollback is a revert merged to `main`, then a push to `staging`, then a merge to `production`. It is not a branch that redeploys an old image.

You do not merge, and you do not deploy, unless the developer asks.

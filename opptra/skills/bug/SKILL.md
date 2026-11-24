---
name: bug
description: Fixes an incorrect behavior with a failing regression check first, then verifies and delivers the fix using the repository workflow.
---

# Bug

## Skill version check

Before following this skill, read and follow [Skill freshness](../session/SKILL.md#skill-freshness). Run it once per user request, including when this skill is invoked directly. A route or shared reference within the same request reuses that result. After an update, reread this file and any shared instructions before continuing. A [factory job pinned to a provisioned skills revision](../session/delivery.md#chat-and-software-factory) skips automatic updates for that run.

1. Read [repository context and delivery handoff](../session/delivery.md), [Pins and Resume](../session/SKILL.md), and the Product contract when present. Identify the root cause and record expected behavior, observed behavior, and the reproduction. If the task requires a product decision, route to [feature](../feature/SKILL.md).
2. **Gate 1.** Get approval of the minimal fix and regression plan. A factory dispatch with approval for this scope can satisfy the gate. Reuse the matching issue and follow [Linear continuity](../linear-continuity/SKILL.md) where Linear governs the project. Otherwise use the existing tracker or supplied task. Only create or update tracker records when authorized.
3. Trace any deployment change to its actual owner. Keep coupled code and Terraform together for app-owned repos. Use a separate infrastructure PR for a prerequisite that must land first. For generator-owned infrastructure use [change-app](../change-app/SKILL.md) and preserve the repo's stacked PR flow. Branch from the resolved base or agreed dependency branch, using `fix/<ticket>-<slug>` where that convention applies. Record approved work in the ignored SDLC intent file where applicable or the factory task record.
4. Write and run the regression test before applying the fix. Implement the minimal correction and verify the test passes. Keep the before and after evidence.
5. **Gate 2.** Hand off to [task-to-pr](../task-to-pr/SKILL.md) for tests, review, and CI. Once local verification passes, get the required approval of the commit, files, branch, base, and PR payload before any commit, push, or PR write. Resume with valid approval evidence. Report the PR and verification state. Include the [rollback instructions](../session/SKILL.md#ship-card) only where supported by the active release workflow.

---
name: feature
description: Implements a feature from a scoped request or issue, applies the repo's specification conventions, and delivers a verified pull request.
---

# Feature

## Skill version check

Before following this skill, read and follow [Skill freshness](../session/SKILL.md#skill-freshness). Run it once per user request, including when this skill is invoked directly. A route or shared reference within the same request reuses that result. After an update, reread this file and any shared instructions before continuing. A [factory job pinned to a provisioned skills revision](../session/delivery.md#chat-and-software-factory) skips automatic updates for that run.

1. Read [repository context and delivery handoff](../session/delivery.md), [Pins and Resume](../session/SKILL.md), and the repo's Product contract when present. Reuse the current issue and work branch when they match. Apply [Linear continuity](../linear-continuity/SKILL.md) where Linear governs the project. Otherwise use the existing tracker or the supplied task.
2. **Gate 1.** Choose [feature depth](../session/SKILL.md#depth). In the Opptra SDLC workflow, use pinned OpenSpec for standard and migration work, and skip it for express. Else use the repo's existing spec location or the approved task. Where OpenSpec applies, draft the spec before asking for plan approval and sync the approved criteria and spec summary to Linear when authorized. For data and job changes, include affected schema migrations, idempotency, and upstream failure behavior. Use applicable SDLC capability rules for Postgres, Firestore, BigQuery, and scheduled jobs. A dispatched approval can satisfy the gate when it covers this plan.
3. Trace any deployment setting to its owner. Include coupled changes for app-owned Terraform. Use a separate infrastructure PR for a prerequisite that must land first. For generator-owned infrastructure, preserve the existing stacked PR flow and use [change-app](../change-app/SKILL.md). For other repos follow their existing change and release conventions.
4. Branch from the resolved base or agreed dependency branch. Use `feat/<ticket>-<slug>` where the repo uses it. Resume on the matching branch. Record the approved plan in `.sdlc/intent.yaml` where the repo uses the ignored SDLC intent file, or in the factory task record. Implement only the agreed scope.
5. **Gate 2.** Hand off to [task-to-pr](../task-to-pr/SKILL.md) for tests, review, and CI. Once local verification passes, get the required approval of the commit, file list, branch, base, and PR payload before any commit, push, or PR write. Resume with valid approval evidence. Report the PR and verification state. Use the [ship card](../session/SKILL.md#ship-card) for the active Opptra release workflow. Leave staging and production actions to the developer unless the request authorizes them.

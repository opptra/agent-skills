---
name: task-to-pr
description: Delivers an agreed coding task through implementation, verification, independent review, and PR CI. Use with a ready ticket, approved spec, or scoped request.
---

# Deliver a task to a pull request

## Skill version check

Read the [delivery handoff](../session/delivery.md). Follow [Skill freshness](../session/SKILL.md#skill-freshness) once per request unless the factory pins the provisioned skills revision.

1. Resolve scope, acceptance criteria, target, and existing work. Use [requirements](../requirements/SKILL.md) for unresolved product decisions and [plan](../plan/SKILL.md) for work that spans PRs. Use the factory-assigned workspace or the current coding checkout. For a factory job on a detached head, identify or create the work branch from the task record and verified base before writing. Refuse to overwrite another task's work. Resolve the base and reuse the matching branch and PR on resume.
2. Honor the calling route's planning gates and repository conventions. For direct invocation in an Opptra SDLC app, start with the appropriate [feature](../feature/SKILL.md) or [bug](../bug/SKILL.md) route, including its two gates. Continue here at verification when that route hands off. For other repos apply their own planning, tracker, and PR rules. Implement the agreed change with tests. If `feature` or `bug` already implemented the change, start with its verification evidence.
3. Follow [test](../test/SKILL.md) and fix in-scope failures. Use [open-pr](../open-pr/SKILL.md) with any required ship approval before committing, pushing, or publishing. For work awaiting approval, return the proposed payload. A required verification gap blocks declaring the PR ready. A requested draft can record gaps when policy permits.
4. Follow [review](../review/SKILL.md) and check CI on the exact PR head. Address actionable in-scope findings, rerun affected checks, and get a current verdict. An updated commit or PR payload must pass the calling route's applicable ship approval before publication. Keep a draft's publication state unless authorized to change it. Reconcile the PR and latest head before retrying after a timeout. Follow the caller's retry limit when supplied and stop repeating failures when no new evidence is available.
5. Return the PR, head, criterion evidence, verdict, CI status, and pending actions. Leave merge and deployment to the separately authorized workflow.

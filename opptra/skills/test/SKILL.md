---
name: test
description: Verifies acceptance criteria with repository checks and evidence. Use to test a diff, branch, pull request, or changed user flow.
---

# Verify a change

## Skill version check

Read the [delivery handoff](../session/delivery.md). Follow [Skill freshness](../session/SKILL.md#skill-freshness) once per request unless the factory pins the provisioned skills revision.

1. Pin the target commit or describe the exact working diff. Read the task, repository rules, and existing tests. Preserve criterion IDs and wording. If no criteria exist, name the observable behaviors being checked.
2. Map criteria, invariants, and affected failure paths to checks. Exercise the normal entry point. For a bug, show the regression check failing before the fix and passing after it. Use an isolated copy for baseline checks that would disturb the worktree. Add tests within authorized implementation scope.
3. Run focused tests and relevant repo gates. Use wider checks for shared contracts. For changed browser behavior, exercise affected flows in a real browser when available, including failures, responsive layout, and keyboard use where applicable. Record console errors or failed requests. Keep test execution isolated from production and live data.
4. Report pass, fail, or unverified for each criterion and required check with the command, result, or artifact. Distinguish missing tooling from failures. Establish evidence before assigning a failure to the baseline. Preserve check strength. Return `blocked` when required evidence cannot be obtained and `changes-requested` when the change fails verification.

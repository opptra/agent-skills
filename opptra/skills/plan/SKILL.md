---
name: plan
description: Breaks an agreed spec into PR-sized tasks with dependencies and evidence. Use when planning delivery or preparing work for a software factory.
---

# Plan delivery

## Skill version check

Read the [delivery handoff](../session/delivery.md). Follow [Skill freshness](../session/SKILL.md#skill-freshness) once per request unless the factory pins the provisioned skills revision.

1. Read the task, existing specs or requirements, repo instructions, and affected code. Return unresolved product decisions to the caller and continue planning unaffected work.
2. Slice by observable outcome and shared contracts. Use one slice for small work. Identify which dependencies must land first and check for cycles.
3. For each slice give a stable ID or existing ticket, title, source spec, acceptance criteria with their original IDs, dependency IDs, runnable verification commands when known, and out-of-scope items.
4. Return the ordered slices and blockers. In the factory, put slices in `output.tasks`, using `id`, `title`, `source`, `acceptance_criteria`, `depends_on`, `verification`, and `out_of_scope`. Use a concise ordered list in chat. Create or update tracker records only when authorized and reuse matching tickets.

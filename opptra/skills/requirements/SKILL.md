---
name: requirements
description: Defines product requirements, scope, business rules, and observable acceptance criteria. Use to turn a brief or an existing product decision into a requirements record.
---

# Requirements

## Skill version check

Read the [delivery handoff](../session/delivery.md). Follow [Skill freshness](../session/SKILL.md#skill-freshness) once per request unless the factory pins the provisioned skills revision.

1. Read the brief, relevant repository instructions, and the existing PRD, issues, and product evidence. Reuse settled decisions. Identify the users, their problem, and the outcome they need.
2. Capture scope, permissions, business rules, important failure and recovery behavior, and measurable constraints. Distinguish facts and assumptions. Keep implementation details in the technical spec. Ask about decisions that materially change the outcome, or return them to the factory as pending.
3. Give requirements stable IDs and pair them with observable acceptance criteria. Preserve IDs and links already in use.
4. Draft or update the existing requirements record, such as a PRD or Linear issue, when requested and authorized. Use root `REQUIREMENTS.md` when the user wants a durable product document and no destination is established. Keep feature-level technical detail in the repo's spec format. Apply [Linear continuity](../linear-continuity/SKILL.md) when creating an Opptra issue.
5. Return the draft or artifact link, criteria, and open decisions with their impact on delivery. Record an approval only when it was given.

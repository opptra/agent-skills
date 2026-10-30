---
name: linear-continuity
description: Shared Linear ticket continuity rules read by create-app, feature, bug, change-app, align-app, and adopt-terraform. Use only when one of those skills says to read this file before creating or updating a Linear issue.
disable-model-invocation: true
---

# Linear continuity

Plan with the user before creating a Linear issue. Do not create a new Linear ticket on every prompt while still discussing or refining the plan. Check the current Git branch (`git branch --show-current`) first. Ticket identity comes from the branch name or from a ticket id the user gave. Do not read a ticket id from `.sdlc/state.yaml`.

- If a ticket branch is already checked out (`feat/<ticket-id>-...`, `fix/<ticket-id>-...`, or `infra/<ticket-id>-...`) and the new ask is related to that same ticket, reuse that Linear issue. Append the new requirements and spec updates only when they are not already on the issue, and keep working on the current branch.
- If a ticket branch is checked out and it is unclear whether the new ask belongs to that ticket or is a separate task, ask the user whether to add it to the existing Linear issue or switch to `main` and create or use a new Linear issue.
- If on `main` and the user gave a ticket id, read that Linear issue.
- If on `main` with no ticket id given, agree on the overall plan with the user first, then create one Linear issue and push the agreed requirements, acceptance criteria, and spec summary to that Linear issue.
- **Local-only / offline fallback (`LOCAL-DRAFT`):** If the developer is scaffolding a new app locally (`create-app` before GitHub repo creation) or working offline and Linear MCP is not connected yet, allow local progress using placeholder `LOCAL-DRAFT` in `.sdlc/intent.yaml`, and require connecting Linear and resolving a real ticket id before pushing a branch or opening a pull request.

Do not invent a real-looking ticket id (such as `OPP-123`). Only use a real Linear issue id from Linear or `LOCAL-DRAFT` prior to remote push.

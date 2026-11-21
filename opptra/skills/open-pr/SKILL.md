---
name: open-pr
description: Prepares, opens, or updates a pull request for code that is already written. Use to publish existing work with verification evidence.
---

# Open or update a pull request

## Skill version check

Read the [delivery handoff](../session/delivery.md). Follow [Skill freshness](../session/SKILL.md#skill-freshness) once per request unless the factory pins the provisioned skills revision.

1. Resolve the destination repository, base, exact head repository and branch, and intended changes. Look up an existing PR by supplied ID or exact head. Preserve its base unless the user requests a retarget. Resolve conflicting targets before sending.
2. Inspect the complete diff and staged state. Preserve unrelated changes. Reuse an existing commit when it covers the intended changes. If a commit is needed and authorized, follow repo conventions and run applicable hooks. Stage only the intended paths or hunks and never bypass verification. Before any required ship approval, present the commit, files, base, head, and PR payload together.
3. Use the repository's PR template. As a fallback include the issue/spec, what changed and why, verification and gaps, and risk including migration or rollback where relevant. Preserve existing PR metadata and unrelated body content.
4. Open or update the PR through the available repository tool after authorization and required approvals. Push only the authorized work branch. Supply the exact destination and head owner for a fork. Honor draft status and repo policy. If write access is unavailable, return the prepared payload and blocker.
5. Verify the resulting PR URL, base, and remote head revision. After a timeout or duplicate result, look up the exact head again before retrying. Opening a PR does not confer merge or release authority.

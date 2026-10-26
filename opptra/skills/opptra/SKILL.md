---
name: opptra
description: Chooses the Opptra route from a sentence when the developer has not named a skill. Use when someone describes a new app, a bug, a feature, an alignment, a Terraform move, or a capability change and does not say which skill to run.
---

# Opptra

This skill only picks the route. Print one line, then read that skill's `SKILL.md` and follow it. Do not do the work in this file.

```text
Route: <skill> | Why: <one sentence>
```

| What they asked for | Skill |
|---|---|
| A new repository or a scaffold | `create-app` |
| An existing repository onto the SDLC standard | `align-app` |
| `deploy.sh`, Cloud Build, Vercel, Fly, or manual GCP onto Terraform | `adopt-terraform` |
| A database, bucket, queue, secret, job, cron, region, or workload | `change-app` |
| New product behavior | `feature` |
| Broken or incorrect behavior | `bug` |
| Fetch or update the team skills | `fetch-skill` |
| Add a team skill | `add-skill` |
| Change a team skill | `modify-skill` |

A capability change and a product change are two pull requests. Say that `change-app` goes first, then follow `change-app`.

If two routes fit and you cannot tell which, ask once.

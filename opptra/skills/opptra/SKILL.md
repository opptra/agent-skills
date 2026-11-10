---
name: opptra
description: Chooses the Opptra route from a sentence when the developer has not named a skill. Use when someone describes a new app, a bug, a feature, a mockup, a presentation, an email, a dashboard, an alignment, a Terraform move, a capability change, or asks whether they are set up, and does not say which skill to run.
---


## Skill version check

Before following this skill, read and follow [Skill freshness](../session/SKILL.md#skill-freshness). Run it once per user request, including when this skill is invoked directly. A route or shared reference within the same request reuses that result. After an update, reread this file and any shared instructions before continuing.

# Opptra

This skill only picks the route. Print one line, then read that skill's `SKILL.md` and follow it. Do not do the work in this file.

```text
Route: <skill> | Why: <one sentence>
```

| What they asked for | Skill |
|---|---|
| A mockup, wireframe, prototype, or product screen | `opptra-design-system` |
| A presentation, document, email, or chart | `opptra-branding` |
| An internal dashboard or one-page tool (not a new GitHub app) | `opptra-dashboard` |
| A new repository or a scaffold | `create-app` |
| An existing repository onto the SDLC standard | `align-app` |
| `deploy.sh`, Cloud Build, Vercel, Fly, or manual GCP onto Terraform | `adopt-terraform` |
| A database, bucket, queue, secret, job, cron, region, or workload | `change-app` |
| New product behavior | `feature` |
| Broken or incorrect behavior | `bug` |
| Fetch or update the team skills | `fetch-skill` |
| Am I set up, or doctor | `doctor` |
| Add a team skill | `add-skill` |
| Change a team skill | `modify-skill` |

A mockup, deck, email, or one-page dashboard is not a new repository. Do not route those to `create-app`.

For a feature or bug that also changes infrastructure, read the ownership map in [session](../session/SKILL.md). App-owned repositories can include both in one PR. Generator-owned repositories use `change-app` and the legacy stacked PR flow. Stay in this chat while continuing the selected route.

If two routes fit and you cannot tell which, ask once.

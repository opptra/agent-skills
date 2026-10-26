# opptra/agent-skills

The skills every Opptra developer uses to create an app, change an app's capabilities or schedules, implement a feature, fix a bug, align an existing app, add a skill, change a skill, and fetch the latest skills.

| Skill | When |
|---|---|
| `create-app` | A new repository. Reads the Linear issue and any local plan (`MIGRATION_PLAN.md`), infers workloads and capabilities, records any platform gap under `unmet`, writes `service.yaml`, and runs the 5-phase generator (`check` → `init-runtime` → `add-data` → `add-tests` → `sync-infra`) from `opptra/sdlc-resources`. |
| `change-app` | Adding or updating a workload, scheduled job, cron schedule, database (`postgres`, `firestore`, `bigquery`), bucket, queue, or secret on an existing app. Updates `service.yaml`, runs `add-data` → `add-tests` → `sync-infra`, and opens an `infra/<ticket>-<slug>` pull request. |
| `adopt-terraform` | Moving an existing app from `deploy.sh`, Cloud Build, Vercel, or manual GCP resources onto Terraform. Runs `sdlc.py discover-infra`, presents a Terraform Adoption Scorecard, and generates `service.yaml`, `infra/`, and declarative `imports.tf.example` blocks. |
| `align-app` | An existing repository. Runs `sdlc.py status --table`, presents the 15-point scorecard and 10 rule pillars with **What this means for you**, and applies only the rows the developer accepts. |
| `feature` | A Linear feature. Verifies repo alignment and capability rules from `service.yaml`, branches `feat/<ticket>-<slug>` from `main`, writes an OpenSpec and tests, and opens one pull request into `main`. |
| `bug` | A Linear bug. Verifies repo alignment and capability rules, writes a failing test first, makes the fix, and opens one pull request into `main`. |
| `add-skill` | A new team skill. Writes `opptra/skills/<name>/SKILL.md` and opens a pull request into `main`. |
| `modify-skill` | A change to an existing team skill. Edits that skill from the developer's instructions and opens a pull request into `main`. |
| `linear-continuity` | Shared reference read by the skills above before they create or update a Linear issue. Do not run it on its own. |
| `fetch-skill` | Fetches `main` of this repository and links every skill into Cursor, Claude Code, and Codex. |

`opptra/sdlc-resources` stays the library: the mapping, the skeletons, the phase CLI (`scripts/sdlc.py`), the Terraform modules, and the workflows. People do not keep that repo checked out.

`main` does not deploy. A push to `staging` deploys staging. A merge into `production` deploys production.

## Cursor

Add this repository as a team marketplace and set the `opptra` plugin to Required. Cursor installs the skills for everyone on the team.

## First install for Claude Code, Codex, and a local Cursor copy

```bash
git clone https://github.com/opptra/agent-skills.git ~/agent-skills
mkdir -p ~/.claude/skills ~/.codex/skills ~/.cursor/skills
for dir in ~/agent-skills/opptra/skills/*/; do
  name=$(basename "$dir")
  ln -sfn "$dir" ~/.claude/skills/"$name"
  ln -sfn "$dir" ~/.codex/skills/"$name"
  ln -sfn "$dir" ~/.cursor/skills/"$name"
done
```

After that, ask the agent to fetch Opptra skills. The `fetch-skill` skill pulls `main` and refreshes those links, including skills added since the clone.

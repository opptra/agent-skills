# opptra/agent-skills

The skills every Opptra developer uses to create an app, change an app's capabilities or schedules, implement a feature, fix a bug, align an existing app, check a laptop, add a skill, change a skill, and fetch the latest skills. `opptra` only chooses which of those to run.

| Skill | When |
|---|---|
| `opptra` | The developer describes the work and does not name a skill. Prints the route and follows that skill. |
| `create-app` | A new repository. Confirms archetype, name, auth, data, and prod project, runs the 5-phase generator, stops at `make dev`, and creates a private `opptra` repo only after a yes. |
| `change-app` | Adding or updating a workload, scheduled job, cron schedule, database (`postgres`, `firestore`, `bigquery`), bucket, queue, or secret on an existing app. Updates `service.yaml`, runs `add-data` → `add-tests` → `sync-infra`, and opens an `infra/<ticket>-<slug>` pull request. |
| `adopt-terraform` | Moving an existing app from `deploy.sh`, Cloud Build, Vercel, or manual GCP resources onto Terraform. Runs `sdlc.py discover-infra`, presents a Terraform Adoption Scorecard, and generates `service.yaml`, `infra/`, and declarative `imports.tf.example` blocks. |
| `align-app` | An existing repository. Prints the scorecard, then offers three paths: ship today, make the agent safe, or move the host. One yes. |
| `feature` | A Linear feature. If a cloud resource is missing, opens the infra pull request in the same chat first. Otherwise branches `feat/<ticket>-<slug>`, writes an OpenSpec unless the depth is `express`, opens one pull request into `main`, and prints the ship card. |
| `bug` | A Linear bug. Writes a failing test first, opens one pull request into `main`, and prints the ship card including the rollback line. |
| `add-skill` | A new team skill. Writes `opptra/skills/<name>/SKILL.md` and opens a pull request into `main`. |
| `modify-skill` | A change to an existing team skill. Edits that skill from the developer's instructions and opens a pull request into `main`. |
| `linear-continuity` | Shared reference read by the skills above before they create or update a Linear issue. Do not run it on its own. |
| `session` | Shared pins, resume file, and feature depth. Do not run it on its own. |
| `fetch-skill` | Fetches `main` of this repository and links every skill into Cursor, Claude Code, and Codex. |
| `doctor` | Checks this machine: skills commit, `gh`, Linear, Python, Node, and the pinned OpenSpec. Does not scaffold an app. `sdlc.py doctor` is a different command. |

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

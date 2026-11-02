# opptra/agent-skills

The skills every Opptra developer uses to create an app, change an app's capabilities or schedules, implement a feature, fix a bug, align an existing app, check a laptop, add a skill, change a skill, and fetch the latest skills. `opptra` only chooses which of those to run.

| Skill | When |
|---|---|
| `opptra` | The developer describes the work and does not name a skill. Prints the route and follows that skill. |
| `create-app` | A new repository. Confirms archetype, name, auth, data, and prod project, runs the 5-phase generator, stops at `make dev`, and creates a private `opptra` repo only after a yes. |
| `change-app` | Adding or updating a workload, scheduled job, cron schedule, database (`postgres`, `firestore`, `bigquery`), bucket, queue, or secret on an existing app. Updates `service.yaml`, runs `add-data` → `add-tests` → `sync-infra`, and opens an `infra/<ticket>-<slug>` pull request. |
| `adopt-terraform` | Moving an existing app from `deploy.sh`, Cloud Build, Vercel, or manual GCP resources onto Terraform. Runs `sdlc.py discover-infra`, presents a Terraform Adoption Scorecard, and generates `service.yaml`, `infra/`, and declarative `imports.tf.example` blocks. |
| `align-app` | An existing repository. Prints the scorecard, then offers three paths: ship today, make the agent safe, or move the host. One yes. |
| `feature` | A Linear feature. Syncs plain `env:` changes inline; when a stateful cloud resource is missing, opens the `infra/` PR first and immediately stacks `feat/<ticket>-<slug>` on top so product code continues without waiting. Uses a 2-gate confirmation flow and prints the ship card. |
| `bug` | A Linear bug. Investigates root cause and writes a failing reproduction test before Gate 1, applies the minimal fix, verifies `.githooks/pre-commit` and `make ci`, opens one PR into `main`, and prints the ship card including the rollback line. |
| `add-skill` | A new team skill. Writes `opptra/skills/<name>/SKILL.md` and opens a pull request into `main`. |
| `modify-skill` | A change to an existing team skill. Edits that skill from the developer's instructions and opens a pull request into `main`. |
| `linear-continuity` | Shared reference read by the skills above before they create or update a Linear issue (supports `LOCAL-DRAFT` fallback while working locally offline). Do not run it on its own. |
| `session` | Shared pins, local generator cache (`~/.cache/opptra/sdlc-resources.git`), resume file, and feature depth. Do not run it on its own. |
| `fetch-skill` | Fetches `main` of this repository, refreshes the local generator cache, and links every skill into Cursor, Claude Code, Codex, and OpenCode via `./install.sh`. |
| `doctor` | Checks this machine: skills commit, local generator cache, `gh`, Linear, Python, `uv`, Node, `terraform`, and the pinned OpenSpec. Auto-fixes skill links and OpenSpec version when asked. |

`opptra/sdlc-resources` stays the library: the mapping, the skeletons, the phase CLI (`scripts/sdlc.py`), the Terraform modules, and the workflows. `./install.sh` maintains a local bare cache at `~/.cache/opptra/sdlc-resources.git` so generator runs are instant and work offline.

`main` does not deploy. A push to `staging` deploys staging. A merge into `production` deploys production.

## Cursor

Add this repository as a team marketplace and set the `opptra` plugin to Required. Cursor installs the skills for everyone on the team.

## First install for Claude Code, Codex, OpenCode, and a local Cursor copy

```bash
git clone https://github.com/opptra/agent-skills.git ~/agent-skills
~/agent-skills/install.sh
```

`install.sh` also links the **`opptra` CLI** into `~/.local/bin/opptra` (`opptra next`, `opptra doctor [--fix]`, `opptra status`, `opptra check`, `opptra discover`, `opptra sync`, `opptra secrets`).

After that, ask the agent to fetch Opptra skills. The `fetch-skill` skill pulls `main`, refreshes the local generator cache, and re-runs `./install.sh`.

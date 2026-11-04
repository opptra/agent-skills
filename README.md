# opptra/agent-skills

The skills Opptra people use. `opptra` only chooses which of those to run.

Org-wide skills cover mockups, branding, and one-page dashboards. Engineering skills cover creating an app, changing capabilities, implementing a feature, fixing a bug, and aligning a repository. Pointing a coding agent at this repository URL still installs the full set. First-time setup is unchanged: clone this repo and run `./install.sh`, or add it as the Cursor marketplace and enable the `opptra` plugin.

| Skill | When |
|---|---|
| `opptra` | The person describes the work and does not name a skill. Prints the route and follows that skill. |
| `opptra-design-system` | A mockup, wireframe, prototype, HTML dashboard, or product screen. Loads https://opptra.github.io/opptra-design-system/. Does not create a GitHub app. |
| `opptra-branding` | A presentation, document, email, or chart. For web UI, use `opptra-design-system`. |
| `opptra-dashboard` | An internal one-page dashboard or tool (not a new GitHub app). Uses `opptra-design-system` for visuals. |
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

`opptra/sdlc-resources` stays the library: the mapping, the skeletons, the phase CLI (`scripts/odlc.py`), the Terraform modules, and the workflows. `./install.sh` maintains a local bare cache at `~/.cache/opptra/sdlc-resources.git` so generator runs are instant and work offline.

`main` does not deploy. A push to `staging` deploys staging. A merge into `production` deploys production.

## Cursor

Add this repository as a team marketplace and set the `opptra` plugin to Required. Cursor installs the skills for everyone on the team. The plugin name and source stay `opptra`. New skills land under `opptra/skills/` and are picked up by the same install.

## First install for Claude Code, Codex, OpenCode, and a local Cursor copy

```bash
git clone https://github.com/opptra/agent-skills.git ~/agent-skills
~/agent-skills/install.sh
```

`install.sh` also links the agent-facing **`odlc` CLI** into `~/.local/bin/odlc` and removes the old installer-managed `opptra` CLI symlink. Agents use it to reuse the cached generator and run checks, phases, and status commands with less repeated setup. Developers describe their task in chat; manual CLI use is optional. The `opptra` plugin and routing skill keep their names.

After that, ask the agent to fetch Opptra skills. The `fetch-skill` skill pulls `main`, refreshes the local generator cache, and re-runs `./install.sh`.

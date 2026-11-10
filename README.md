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
| `change-app` | Infrastructure-only work. Edits checked-in Terraform and workflows after handoff. Generator-owned repositories still use the pinned bootstrap phases. |
| `adopt-terraform` | Maps live resources to Terraform, verifies staging, and prepares the production cutover and imports. |
| `align-app` | An existing repository. Prints the scorecard, then offers three paths: ship today, make the agent safe, or move the host. One yes. |
| `feature` | A Linear feature. Includes coupled Terraform and code changes in one PR after handoff. Generator-owned repositories keep their stacked PR flow. Uses a 2-gate confirmation flow and prints the ship card. |
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

## Automatic skill freshness

Every Opptra skill starts with the shared freshness check in [session](opptra/skills/session/SKILL.md#skill-freshness). On each new user request, the agent checks the installed checkout against `origin/main`. A clean `main` checkout fast-forwards automatically and refreshes the skill links. The agent then rereads the updated instructions. Nested routes reuse the check for that request.

Keep the installed skills on a clean `main` checkout for automatic updates. Use a separate development clone for editing skills. Local changes, feature branches, and divergent commits are reported and preserved. If GitHub is unavailable, the agent reports that freshness could not be verified and uses its installed version. An installation managed by a plugin host uses that host's update mechanism when it has no Git checkout.

The lightweight check runs `install.sh --skills-only` to refresh skill and CLI links. The normal `install.sh` and explicit `fetch-skill` also check the generator cache and OpenSpec setup. App generator commits and workflow refs keep their explicit upgrade process.

Existing installations need one `fetch-skill` update after this preflight is released. An agent with the older instructions needs that first update before it knows to check automatically.

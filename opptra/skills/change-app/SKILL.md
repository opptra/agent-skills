---
name: change-app
description: Changes an existing Opptra app’s workloads, data resources, IAM, secrets, schedules, or runtime settings. Edits the owning Terraform or pipeline inputs after handoff and uses the pinned generator for legacy repos.
---


## Skill version check

Before following this skill, read and follow [Skill freshness](../session/SKILL.md#skill-freshness). Run it once per user request, including when this skill is invoked directly. A route or shared reference within the same request reuses that result. After an update, reread this file and any shared instructions before continuing.

# Change an app's capabilities or schedules

Use this skill for infrastructure-only work. For a feature or bug with coupled infrastructure, follow that skill and include the changes in the same PR when the app owns its infrastructure.

Before you edit files, read Pins in `../session/SKILL.md`, print the Route Banner with those two lines, tell the developer which owning files will change and which files will be generated if the repo still uses the generator, and wait for a yes (**Gate 1**). After running the phase scripts and verifying `.githooks/pre-commit` and `make ci`, show the commit message, file list, branch name, and pull request title/body together in one prompt and wait for a yes (**Gate 2**).

## App-owned repositories

Read **Find the owner of a deployment setting** in [session](../session/SKILL.md). Reuse the Linear ticket when it covers the request. For standalone work, use `infra/<ticket>-<slug>`. Edit the owning Terraform, environment inputs, or workflow caller. Preserve state keys and resource addresses, and update `.env.example` for new runtime names. Run hooks and `make ci`, review the Terraform plan for the affected environment, and open the infrastructure PR. Use the developer's normal staging and promotion flow.

## 1. Route Banner & Understand for generator-owned repositories

```text
Route: change-app | Branch: infra/<ticket-id>-<slug>
Phases: 1. Update service.yaml  2. add-data  3. add-tests  4. sync-infra  5. Verify 17-Point Scorecard
Human Gates: Gate 1 — Approve service.yaml plan; Gate 2 — Commit, push, and open PR after make ci passes
Script-Owned Paths: infra/, .github/workflows/, managed rule blocks in AGENTS.md & CLAUDE.md
```

1. **Plan first and resolve the Linear ticket.** Agree the capability or schedule change with the developer, then read and follow `../linear-continuity/SKILL.md`. When you create or update the issue, include the planned `service.yaml` changes. Do not invent a ticket id.
2. Read `service.yaml`. If `service.yaml` is missing, stop and run `align-app` first.
3. Run Generator checkout from `../session/SKILL.md`. It sets `$tmpdir` and `$tmpdir/sdlc`. Reuse `generator_sha` when `.sdlc/state.yaml` has one. Clone `main` only when it is missing or the developer asks to upgrade the generator.

## 2. Apply in Phases

1. Branch from `main` as `infra/<ticket-id>-<short-slug>`.
2. Update `service.yaml` (and `config/jobs.yaml` if changing job schedules or `enabled` flags). Ensure any new app-owned external GCP resource (job, service, queue, secret ID) follows the `<prefix>-<resource>` naming standard. When connecting to pre-existing/shared resources, use `postgres_instance` + `postgres_secret` (or `postgres_external: true`), `bigquery_project` + `bigquery_datasets` (supports `project.dataset`), `existing_bucket`, `existing_secrets`, and `secret_map` so Terraform only grants IAM and mounts them without creating duplicates. For additional IAM roles use `extra_roles: ["roles/..."]`; for any other custom GCP resource set `custom_terraform: true` and write the Terraform resource in `infra/custom.keep.tf` (referencing `module.service.runtime_service_account` and `var.project_id`). Reserve `unmet` only for non-repo/org-level gaps.
3. Validate and run the phases:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" check service.yaml
   python3 "$tmpdir/sdlc/scripts/sdlc.py" add-data service.yaml .
   python3 "$tmpdir/sdlc/scripts/sdlc.py" add-tests service.yaml .
   python3 "$tmpdir/sdlc/scripts/sdlc.py" sync-infra service.yaml .
   python3 "$tmpdir/sdlc/scripts/sdlc.py" status . --table
   python3 "$tmpdir/sdlc/scripts/sdlc.py" status . --check
   rm -rf "$tmpdir"
   ```
4. Do not hand-edit `infra/` or `.github/workflows/`.
5. Run `.githooks/pre-commit` and `make ci` (plus `uv run ruff check . && uv run pytest` for any component touched). Never pass `--no-verify` to `git commit` or `git push`.
6. Push the branch and open one pull request into `main`. Read the `terraform plan` comment on the pull request and stop if any unexpected resource destroy appears.
7. When this skill was entered from `feature` or `bug`, stay in that chat. Offer to immediately cut `feat/<ticket-id>-<slug>` (or `fix/<ticket-id>-<slug>`) **stacked on top of `infra/<ticket-id>-<slug>`** (`next_step: code-stacked-on-infra` in `.sdlc/intent.yaml`) so the developer can write and test product code locally right away without waiting for the infra pull request to merge (and rebase onto `main` once the infra PR merges). Only set `next_step: wait-for-infra` if the developer explicitly prefers to pause until the infra pull request merges.

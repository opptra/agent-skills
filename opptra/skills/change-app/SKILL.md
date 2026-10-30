---
name: change-app
description: Adds or updates workloads, scheduled jobs, cron schedules, regions, databases, buckets, queues, or secrets on an existing Opptra app by updating service.yaml and running the phase scripts from opptra/sdlc-resources. Use when a developer asks to add a database, bucket, queue, webhook, job, UI, or schedule change to an existing app.
---

# Change an app's capabilities or schedules

Product code and changes to `service.yaml`, `config/jobs.yaml` schedules, `infra/`, or `.github/workflows/` belong in separate pull requests. Use this skill when an existing app needs a new workload, a new capability (`postgres`, `firestore`, `bigquery`, `bucket`, `queue`, `secrets`, `alerts`), a per-component `region`, a new scheduled job, or a cron/enable flag change.

Before you edit files, read Pins in `../session/SKILL.md`, print the Route Banner with those two lines, tell the developer what you will change in `service.yaml` and which files the phase scripts will regenerate, and wait for a yes. Before a commit, show the message and file list and wait. Before a push or pull request, show the branch, title, and body and wait.

## 1. Route Banner & Understand

```text
Route: change-app | Branch: infra/<ticket-id>-<slug>
Phases: 1. Update service.yaml  2. add-data  3. add-tests  4. sync-infra  5. Verify 17-Point Scorecard
Human Gates: Before editing service.yaml, before commit, and before push/PR
Script-Owned Paths: infra/, .github/workflows/, managed rule blocks in AGENTS.md & CLAUDE.md
```

1. **Plan first and resolve the Linear ticket.** Agree the capability or schedule change with the developer, then read and follow `../linear-continuity/SKILL.md`. When you create or update the issue, include the planned `service.yaml` changes. Do not invent a ticket id.
2. Read `service.yaml`. If `service.yaml` is missing, stop and run `align-app` first.
3. Run Generator checkout from `../session/SKILL.md`. It sets `$tmpdir` and `$tmpdir/sdlc`. Reuse `generator_sha` when `.sdlc/state.yaml` has one. Clone `main` only when it is missing or the developer asks to upgrade the generator.

## 2. Apply in Phases

1. Branch from `main` as `infra/<ticket-id>-<short-slug>`.
2. Update `service.yaml` (and `config/jobs.yaml` if changing job schedules or `enabled` flags). Ensure any new external GCP resource (job, service, queue, secret ID) follows the `<prefix>-<resource>` naming standard. Record any unsupported platform need under `unmet` with a recommendation.
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
7. When this skill was entered from `feature` or `bug`, stay in that chat. Set `.sdlc/intent.yaml` `next_step` to `wait-for-infra` and stop before product code. Product code starts after the developer says this pull request has merged.

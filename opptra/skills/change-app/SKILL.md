---
name: change-app
description: Adds or updates workloads, scheduled jobs, cron schedules, databases, buckets, queues, or secrets on an existing Opptra app by updating service.yaml and running the phase scripts from opptra/sdlc-resources. Use when a developer asks to add a database, bucket, queue, webhook, job, UI, or schedule change to an existing app.
---

# Change an app's capabilities or schedules

Product code and changes to `service.yaml`, `config/jobs.yaml` schedules, `infra/`, or `.github/workflows/` belong in separate pull requests. Use this skill when an existing app needs a new workload, a new capability (`postgres`, `firestore`, `bucket`, `queue`, `secrets`, `alerts`), a new scheduled job, or a cron/enable flag change.

Before you edit files, tell the developer what you will change in `service.yaml` and which files the phase scripts will regenerate, and wait for a yes. Before a commit, show the message and file list and wait. Before a push or pull request, show the branch, title, and body and wait.

## Understand

1. Read the Linear issue. If Linear is not connected, stop and ask the developer to connect it. Do not invent a ticket id.
2. Read the repo's `service.yaml`. If `service.yaml` is missing, stop and run `align-app` first.
3. Clone `main` of `opptra/sdlc-resources` into a temporary directory:
   ```bash
   tmpdir=$(mktemp -d)
   git clone --depth 1 --branch main https://github.com/opptra/sdlc-resources.git "$tmpdir/sdlc"
   ```

## Apply in phases

1. Branch from `main` as `infra/<ticket-id>-<short-slug>`.
2. Update `service.yaml` (and `config/jobs.yaml` if changing job schedules or `enabled` flags). If the developer also asked for something the platform does not generate yet, record it under `unmet` with a recommendation.
3. Validate the manifest:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" check service.yaml
   ```
4. Run the data, test, and infra sync phases:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" add-data service.yaml .
   python3 "$tmpdir/sdlc/scripts/sdlc.py" add-tests service.yaml .
   python3 "$tmpdir/sdlc/scripts/sdlc.py" sync-infra service.yaml .
   python3 "$tmpdir/sdlc/scripts/sdlc.py" status . --check
   rm -rf "$tmpdir"
   ```
5. Do not hand-edit `infra/` or `.github/workflows/`.
6. Run the lint and test checks for any component whose `pyproject.toml` or test fixtures changed (`uv run ruff check . && uv run pytest`).
7. Push the branch and open one pull request into `main`. Read the `terraform plan` comment on the pull request to confirm only the expected resources are added or updated.

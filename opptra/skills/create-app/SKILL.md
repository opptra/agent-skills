---
name: create-app
description: Scaffolds a new Opptra app by reading the Linear issue and any local plan, inferring workloads and capabilities, writing service.yaml, and running the 5-phase generator from opptra/sdlc-resources. Use when a developer asks to create, scaffold, or set up a new app or repository.
---

# Create an app

You fill in facts, run the deterministic phase scripts in `opptra/sdlc-resources`, and customize the application entrypoints, data helpers, and unit tests in between. The generator decides `infra/`, `.github/workflows/`, and the rule files. Never hand-edit `.github/workflows/` or `infra/`.

Do not create the GitHub repository. Do not run `bind-repo.sh` or `protect-branches.sh`. Do not leave a checkout of `opptra/sdlc-resources` on the machine.

Apps Script is not a choice. If the whole request is only Apps Script, say so and stop. When part of a request needs something the platform does not generate yet (such as project-level billing budgets or a data warehouse), scaffold every part the platform does support and record the gap under `unmet` in `service.yaml` with a clear recommendation.

## Understand

1. Read the Linear issue they named. If Linear is not connected, or they did not give an issue, stop and ask them to connect Linear or share the ticket id. Do not invent a ticket id.
2. Check the current directory for an existing architecture or migration plan (such as `MIGRATION_PLAN.md` or a design doc). Treat every decision already stated in that plan—region, jobs, crons, Firestore vs Postgres, buckets, queues, webhook receiver, secrets—as answered. Do not re-ask what the plan already fixed.
3. For anything still undecided, ask one question at a time in plain language using the structured question tool in Cursor (probable options only; the form already provides a write-in).

### Workloads and presets

Map what they described onto the closest preset or component combination:

- **Nothing runs** (only settings, prompts, or skills): archetype `config-only`, auth `none`, parts `[config]`.
- **One background job** on a schedule or queue: archetype `cloud-run-job`, auth `none`, parts `[job]`.
- **Several scheduled jobs sharing one codebase/image, with an optional webhook receiver**: archetype `scheduled-jobs`, auth `none`, parts `[job]`, with a `jobs:` list (each with `name`, `command`, `enabled`, `timezone`, `schedules`, `timeout_seconds`, `memory`, `secrets`) and an optional `receiver:` (`name`, `auth: shared-secret`, `queue`, `secrets`). An HTTP portal login or tracking-page fetch stays on a job; do not move it to a VM.
- **A real browser that must stay open, a long-lived process, or local disk state**: archetype `vm-worker`, auth `none`, parts `[worker]`.
- **A page people open or an HTTP API**: archetype `cloud-run-service`, parts `[api]` (and `ui` when there is a page).

### Who can open a page or call the service

- Opptra staff with their Google account: `iap`
- Users sign in with an account the app manages: `app-login`
- Another system calls a webhook with a secret header (such as Freshdesk): `shared-secret`
- Anyone on the internet with no account: `public`

### Data, files, queues, and secrets

Infer these from the description or plan, and ask only when two choices are still plausible:

- Relational rows, joins, or SQL: `database: postgres` (Cloud SQL Postgres 16)
- Document collections, leases, idempotency keys, or a plan that specifies Firestore: `database: firestore` (the project's `(default)` Firestore database)
- No stored state: `database: none`
- Reports, manuals, exports, or uploaded files: `bucket: private`
- Webhook bursts or queued background tasks: `queue: <queue-name>`
- API keys, SMTP credentials, or portal logins: `secrets: [<secret_id>, ...]` (secret IDs only; never ask for or write secret values)
- Job failure and error log alerting: `alerts: true`

## Recommendation

State what you will create in plain sentences: the workloads/jobs, who can call it, which data store, bucket, queue, and secret IDs it uses, and any item that will be recorded under `unmet` with its recommendation. Ask them to confirm before writing files.

## Execute the 5 Phases

Clone `main` of `opptra/sdlc-resources` into a temporary directory and clean it up when finished:

```bash
tmpdir=$(mktemp -d)
git clone --depth 1 --branch main https://github.com/opptra/sdlc-resources.git "$tmpdir/sdlc"
```

### Phase 1: Manifest (`check`)

Write `service.yaml` with `name`, `purpose`, `prod_project`, `region`, `components`, and any `unmet` items:

```yaml
name: cx-automation
purpose: Run the customer-support automations in asia-south1.
prod_project: opptra-applications
region: asia-south1
components:
  - name: automation
    archetype: scheduled-jobs
    auth: none
    database: firestore
    bucket: private
    queue: cx-tickets
    alerts: true
    parts: [job]
    secrets: [freshdesk_opptra, smtp, webhook_secret]
    receiver:
      name: cx-webhook
      auth: shared-secret
      queue: cx-tickets
      secrets: [webhook_secret]
    jobs:
      - name: report-daily
        command: python -m app.jobs.report_daily
        enabled: true
        timezone: Asia/Kolkata
        schedules: ["0 7,14 * * *"]
        timeout_seconds: 1800
        memory: 1Gi
        secrets: [freshdesk_opptra, smtp]
unmet:
  - name: budget-alerts
    need: Email billing alerts at $10, $20, and $30 monthly spend.
    suggestion: Configure project billing budgets once via docs/gcp-bootstrap.md.
```

Validate it:

```bash
python3 "$tmpdir/sdlc/scripts/sdlc.py" check "$tmpdir/service.yaml"
```

### Phase 2: Runtime & Entrypoints (`init-runtime`)

1. Run the script to scaffold the project structure, Dockerfile, and entrypoints:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" init-runtime "$tmpdir/service.yaml" "<target-dir>" --overwrite
   ```
2. Customize the generated runtime files to match the user's domain (for example: add required OS packages like `tesseract-ocr` or `poppler-utils` to the `Dockerfile`, wire the job commands or initial API/UI routes, and scaffold any one-off migration CLI under `tools/`). Keep business logic migrations for `feature` PRs; scaffold the entrypoints and runner contract here.

### Phase 3: Data, Storage & Secrets (`add-data`)

1. Run the script to install the database, storage, queue, and secret packages and base helpers:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" add-data "$tmpdir/service.yaml" "<target-dir>"
   ```
2. Shape the data/state wrappers in `backend/app/` to match the domain collections or tables described by the user or plan.

### Phase 4: Tests (`add-tests`)

1. Run the script to add the test configuration and capability test files:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" add-tests "$tmpdir/service.yaml" "<target-dir>"
   ```
2. Add passing unit tests in `backend/tests/` covering the entrypoints and platform invariants (such as disabled jobs exiting 0, lease lock contention exiting 0, failed upstream fetches exiting non-zero, and webhook secret checks).
3. Run the lint and test gate for each component (`uv run ruff check . && uv run pytest` for Python; `npm run lint && npm run typecheck && npm test --if-present` for UI) and fix any failure before moving to Phase 5.

### Phase 5: Infra, Workflows & Rules (`sync-infra`)

1. Run the script to generate `infra/`, `.github/workflows/`, `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*.mdc`, and `README.md`:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" sync-infra "$tmpdir/service.yaml" "<target-dir>"
   python3 "$tmpdir/sdlc/scripts/sdlc.py" status "<target-dir>" --check
   rm -rf "$tmpdir"
   ```
2. Do not hand-edit `infra/` or `.github/workflows/`. If the project has domain-specific edge cases (such as Section 6 of a migration plan), add a domain rule file in `.cursor/rules/` and document the runbook in `README.md`.

## Hand-off

Tell the developer to create the empty `opptra/<name>` repository, push `main`, and create `staging` and `production`:

```bash
git init
git add .
git commit -m "feat: <ticket-id> scaffold"
git branch -M main
git remote add origin git@github.com:opptra/<name>.git
git push -u origin main
git branch staging
git branch production
git push -u origin staging
git push -u origin production
```

Then they ask a platform owner to run `scripts/protect-branches.sh` and `scripts/bind-repo.sh` from `opptra/sdlc-resources`.

---
name: create-app
description: Scaffolds a new Opptra app by reading the Linear issue and any local plan, showing a 17-point blueprint table, writing service.yaml, and running the 5-phase generator from opptra/sdlc-resources. Use when a developer asks to create, scaffold, or set up a new app or repository.
---

# Create an app

You fill in facts, run the deterministic phase scripts in `opptra/sdlc-resources`, and customize the application entrypoints, data helpers, and unit tests in between. The generator decides `infra/`, `.github/workflows/`, and the managed rule blocks. Never hand-edit `.github/workflows/` or `infra/`.

Create the GitHub repository only after `make dev` passes and the developer says yes. It is a private repository in `opptra`. Then push `main`, `staging`, and `production`, and create the GitHub environments `staging` and `production`. Do not run `scripts/bind-staging.sh` or `scripts/bind-production.sh` unless they say they have permission and ask you to. Staging bind does not need production IAM. Production bind is a file they send to someone who can change IAM in `prod_project`. Do not run `protect-branches.sh`. Branch protection is an organization ruleset. Do not leave a checkout of `opptra/sdlc-resources` on the machine.

Apps Script is not a choice. If the whole request is only Apps Script, say so and stop. When a request needs a GCP resource outside the built-in modules (such as Pub/Sub, Redis, or Cloud Armor), do not leave it unbuilt in `unmet`: use `extra_roles: ["roles/..."]` for IAM grants, `bigquery_datasets: [...]` for BigQuery datasets, or set `custom_terraform: true` and write the Terraform resource in `infra/custom.keep.tf` (which `sync-infra` preserves across runs). Reserve `unmet` in `service.yaml` only for non-repo/organization prerequisites (such as project-level billing budgets).

## 1. Route Banner, Resume Check & Understand

Read Pins in `../session/SKILL.md`. Print the route banner first, including those two lines, so the developer knows the phases and gates:

```text
Route: create-app | Phases: 1. Manifest  2. Runtime & OpenSpec  3. Data/Cloud  4. Tests  5. Infra/CI/Rules & Local Verification
Human Gates: Gate 1 — Approve short blueprint; Gate 2 — Create private GitHub repo after local make ci passes (and before any bind script)
Script-Owned Paths: infra/, .github/workflows/, managed rule blocks in AGENTS.md & CLAUDE.md
```

1. **Resume check:** If `.sdlc/state.yaml` already exists in the target directory, read it and offer to resume from the next uncompleted phase instead of re-interviewing.
2. **Linear:** Read and follow `../linear-continuity/SKILL.md` before creating or updating a Linear issue. Agree the 17-point blueprint in `reference.md` first. When you create or update the issue, include that blueprint, the requirements, and the acceptance criteria. If Linear MCP is not connected yet, use `LOCAL-DRAFT` so local scaffolding and verification can finish without blocking, and connect Linear before creating the GitHub repository or opening a pull request. `.sdlc/state.yaml` is only for resuming a phase, not for a ticket id.
3. **Local plan check:** Check the current directory for an existing migration or architecture plan (such as `MIGRATION_PLAN.md`). Treat every decision already stated in that plan—region, jobs, crons, Firestore vs Postgres vs BigQuery, buckets, queues, webhook receiver, secrets, domain edge cases—as answered. Do not re-ask what the plan already fixed.
4. **Ask only what is missing:** Ask one question at a time in plain language using the structured question tool in Cursor.

### Workloads, capabilities, and auth

- **Nothing runs** (settings, prompts, or skills only): archetype `config-only`, auth `none`, parts `[config]`.
- **One background job**: archetype `cloud-run-job`, auth `none`, parts `[job]`.
- **Several scheduled jobs sharing one image, with an optional webhook receiver**: archetype `scheduled-jobs`, auth `none`, parts `[job]`, with a `jobs:` list and optional `receiver:` (`auth: shared-secret`). An HTTP portal login or tracking-page fetch stays on a job; do not move it to a VM.
- **A real browser that must stay open, a long-lived process, or local disk state**: archetype `vm-worker`, auth `none`, parts `[worker]`.
- **A page people open or an HTTP API**: archetype `cloud-run-service`, parts `[api]` (and `ui` when there is a page), auth `iap` (staff), `app-login`, `shared-secret` (webhook), or `public`.
- **Per-component region**: Set `region` on a component when it runs in a different GCP region from the app default.
- **Resource prefix (`prefix`)**: Every external resource created in GCP (Cloud Run services/jobs, Scheduler entries, Cloud Tasks queues, Secret Manager secrets, buckets, Cloud SQL instances, service accounts, and alert policies) is prefixed with `prefix` (defaults to `name` in `service.yaml`, e.g. `prefix: cx` → `cx-report-daily`, `cx-smtp`).
- **Data, storage, queues, secrets, IAM, custom Terraform, alerts**:
  - `database: postgres | firestore | bigquery | none`:
    - **When `database: postgres` is chosen, decide between the 3 Postgres modes:**
      1. **Default (`database: postgres` only — do NOT add `postgres_external` or `postgres_instance`):** The new app needs its own dedicated GCP Cloud SQL Postgres 16 instance created and managed by Terraform (`modules/cloud-sql`).
      2. **Existing Cloud SQL (`postgres_instance: <proj>:<region>:<instance>` + `postgres_secret: <id>` — do NOT add `postgres_external`):** The user or plan specifies an existing GCP Cloud SQL connection name to share/connect to via Cloud SQL Unix socket.
      3. **External / TCP Postgres (`postgres_external: true` + `DATABASE_URL` in `secrets`):** The user or plan says the database is hosted outside GCP Cloud SQL (e.g., Neon, Supabase, RDS) or connected via a direct TCP `DATABASE_URL` without a Cloud SQL Unix socket.
    - `firestore`: project `(default)` Native DB.
    - `bigquery`: `modules/bigquery` + optional `bigquery_project` and `bigquery_datasets: [...]` (including cross-project `project.dataset`).
  - `bucket: private` (creates `<project>-<name>-assets` by default; set `existing_bucket: <bucket-name>` to bind IAM to a pre-existing bucket without creating one)
  - `queue: <name>` for Cloud Tasks webhook/event buffering
  - `secrets: [<id>, ...]` for app-owned Secret Manager shells, `existing_secrets: [<ENV>, ...]` for pre-existing/shared secrets (mounts & grants IAM without creating the shell in `module.secrets`), and `secret_map: {<ENV>: <gcp-secret-id>}` for brownfield secret IDs
  - `extra_roles: ["roles/..."]` for additional GCP IAM roles granted to the component's runtime service account
  - `custom_terraform: true` to scaffold and preserve `infra/custom.keep.tf` for custom GCP resources (referencing `var.project_id`, `var.region`, `var.name`, and `module.service.runtime_service_account`)
  - `alerts: true` for failed job / error log alert policies

## 2. Confirm the short blueprint and wait

Before writing any files, confirm archetype, name, auth, data store, `prod_project`, and any `unmet` gap. Ask one question at a time for what is still missing. Wait for a yes.

The 17-point table in `reference.md` is the receipt. Print it after phase 5 from `sdlc.py status --table`. Do not walk all 17 rows before writing files.

## 3. Execute All 5 Phases Autonomously (`script → skill → check`)

Once the developer approves the short blueprint (Gate 1), run Phases 1 through 5 in a single autonomous turn without stopping between phases. Run Generator checkout from `../session/SKILL.md`. It sets `$tmpdir` and `$tmpdir/sdlc` from the local cache. A new app has no `generator_sha` yet, so this first run uses `main`. A resume reuses the recorded sha unless the developer asks to upgrade the generator.

### Phase 1: Manifest (`check`)
Write `service.yaml` and validate it:
```bash
python3 "$tmpdir/sdlc/scripts/sdlc.py" check "<target-dir>/service.yaml"
```

### Phase 2: Runtime, OpenSpec & Entrypoints (`init-runtime`)
1. Run:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" init-runtime "$tmpdir/service.yaml" "<target-dir>" --overwrite
   ```
   (`init-runtime --overwrite` only updates skeleton runtime directories and preserves any existing `.git/`, `.sdlc/`, `openspec/`, or `*PLAN*.md` files.)
2. Install the pinned OpenSpec and initialize it in the app. Follow OpenSpec pin in `../session/SKILL.md`. An empty `openspec/` directory is not enough. Run the install and `openspec init --tools cursor,claude` from `<target-dir>`. If install or init fails, fix that before Phase 3. Do not leave this as a later recommendation. Do not install `@latest`.
3. If Linear is connected in Cursor or Claude, read or update the named issue. If Linear is not connected yet, record `LOCAL-DRAFT` and remind the developer to connect Linear before pushing to GitHub.
4. Customize the runtime files to match the domain (add required OS packages to `Dockerfile`, wire job entrypoints or initial API/UI routes, and scaffold any migration CLI under `tools/`).

### Phase 3: Data, Storage & Secrets (`add-data`)
1. Run:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" add-data "$tmpdir/service.yaml" "<target-dir>"
   ```
2. Customize the state/DB/storage wrappers in `backend/app/` to match the domain collections or tables.

### Phase 4: Tests (`add-tests`)
1. Run:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" add-tests "$tmpdir/service.yaml" "<target-dir>"
   ```
2. Write unit tests in `backend/tests/` for the entrypoints and platform invariants (disabled jobs exiting 0, lease contention exiting 0, failed upstream fetches exiting non-zero, webhook secret verification).
3. Run `uv run ruff check . && uv run pytest` (and `npm run lint && npm run typecheck && npm test --if-present` for UI) and fix any failure before Phase 5.

### Phase 5: Infra, Workflows, Rules, Hooks & Final Scorecard (`sync-infra`)
1. If the user's plan has domain-specific edge cases (such as Section 6 of a migration plan), write them under `## Product contract` in `<target-dir>/AGENTS.md` and `<target-dir>/CLAUDE.md` so `sync-infra` preserves them below the managed SDLC rules block.
2. Run:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" sync-infra "$tmpdir/service.yaml" "<target-dir>"
   python3 "$tmpdir/sdlc/scripts/sdlc.py" status "<target-dir>" --table
   python3 "$tmpdir/sdlc/scripts/sdlc.py" status "<target-dir>" --check
   rm -rf "$tmpdir"
   ```
3. **Run and verify the generated `.githooks/` and `make ci`:**
   - Execute `.githooks/pre-commit` and `make ci` inside `<target-dir>`.
   - `make ci` builds the deploy image with the same `docker build` the shared workflow runs. It also runs `terraform validate` with `-backend=false` when Terraform is installed. That validate does not read state and does not apply.
   - If the image build fails, or `odlc status --json` lists `image_notes`, fix `path`, `docker_context`, or `dockerfile` in `service.yaml` and run `sync-infra` again. Do not edit `infra/` or `.github/workflows/` to retarget the build.
   - If any lint, formatting, or test issue is auto-resolvable, fix it immediately and re-run until `.githooks/pre-commit` and `make ci` exit `0`.
   - If a check fails due to something that cannot be resolved without user input, explain the exact failure and ask the developer whether to provide the input now or disable that specific check (`run_tests: false` or `run_lint: false`) in `service.yaml` (recording the reason under `unmet`).
   - Do not ask to create the GitHub repository until this `make ci` exits 0.
4. Push the agreed requirements and blueprint summary to the Linear issue.
5. Never hand-edit `infra/` or `.github/workflows/`.

## 4. Summary scorecard, then next steps

Do not stop after `status --table` alone. Add a second table, **Built and still to build**, before the summary. One row per thing the plan or the request asked for.

| Item | In the scaffold? | Why | What you do next |
|---|---|---|---|
| Example: eight Cloud Run jobs | Yes | The plan listed them, so the scaffold created the jobs, commands, and crons | Try them with a direct push to staging after bind-staging.sh |
| Example: laptop handler code | No | The scaffold is the platform shell. Porting behaviour is a feature | One `/feature` pull request per cutover slice |

Mark each row Yes or No. A Yes row says why it was included. A No row says it was left out on purpose and what the next pull request is. Include `unmet` items as No.

### Summary

Say what was created: app name, directory, workloads, data store, bucket, queue, auth, and that `openspec/` was initialized. Name the Linear issue id that was read. Name anything still under `unmet`.

### Next steps, in this order

1. **Run and verify locally first (`make setup && make dev && make test && make ci`).**
   The scaffold generated `.devcontainer/devcontainer.json`, `.env.example`, `Makefile`, and `backend/app/config.py` (which reads `.env` when `APP_ENV=local` and Secret Manager in the cloud). Copy `.env.example` to `.env`, fill in any local test values, and run `make setup`, `make dev`, `make test`, and `make ci` on your machine before any GitHub step. `make ci` builds the image Cloud Run will run. Stop here until those commands pass. A failed image build is fixed in `service.yaml`, then `sync-infra` runs again.
2. **Create the private GitHub repository only after they say yes.**
   Ask once: create private `opptra/<name>`? On yes, from the app directory:
   ```bash
   git init
   git add .
   git commit -m "feat: <ticket-id> scaffold"
   git branch -M main
   gh repo create opptra/<name> --private --source=. --remote=origin --push
   git branch staging
   git branch production
   git push -u origin staging
   git push -u origin production
   gh api --method PUT "repos/opptra/<name>/environments/staging"
   gh api --method PUT "repos/opptra/<name>/environments/production"
   ```
   Run Generator checkout again and record the slug. `sdlc.py` is not copied into the app:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" set-github-repo "opptra/<name>" .
   rm -rf "$tmpdir"
   ```
   If `origin` already exists, use `git remote set-url origin`. If a branch already exists on the remote, do not force-push. If they say no, stop. The app stays local. Read `.sdlc/state.yaml` on a later turn so you do not re-ask the scaffold facts.
3. **Explain the two bind scripts and print a ready-to-send Platform Admin handoff block. Do not run them unless they ask.**
   `scripts/bind-staging.sh` needs IAM on `opptra-staging` only. `scripts/bind-production.sh` is for someone who can change IAM in `prod_project`. Neither script deploys, and neither protects branches. Print this copy-paste handoff block for the developer when production IAM is owned by another person:
   ```text
   Handoff for Platform / Production Project Admin:
   Please bind GitHub Actions WIF for opptra/<name> in <prod_project>:
     git clone https://github.com/opptra/<name>.git && cd <name>
     ./scripts/bind-production.sh opptra/<name> <prod_project>
   (Then run the two `gh variable set` commands it prints.)
   ```
   A direct push to `staging` deploys staging. A pull request from `main` into `production` is the only deploy that comes from `main`. Do not merge `main` into `staging`. The steps are in `docs/bind.md` of `opptra/sdlc-resources`.
4. **Build the first feature slice locally with `/feature`.**
   The scaffold is the platform shell. Port or build product behaviour one `/feature` pull request at a time.
5. **Try staging only after bind-staging has succeeded and they ask.** Push the branch directly to `staging` and read the Terraform plan. Confirm the jobs, schedules, and webhook match `service.yaml`. A disabled job must have no Scheduler entry. Merging to `main` does not update staging. Then print the ship card from `../session/SKILL.md`.
6. **Put secret values into Secret Manager and close `unmet` items.** The scaffold only created secret ids. Close each `unmet` item (such as a data import or project billing budget) in its own pull request.

If those feature slices are already known, ask **once**: pause for review after each slice, or run each slice through its checks without stopping.

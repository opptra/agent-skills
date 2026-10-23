---
name: create-app
description: Scaffolds a new Opptra app by reading the Linear issue and any local plan, showing a 14-point blueprint table, writing service.yaml, and running the 5-phase generator from opptra/sdlc-resources. Use when a developer asks to create, scaffold, or set up a new app or repository.
---

# Create an app

You fill in facts, run the deterministic phase scripts in `opptra/sdlc-resources`, and customize the application entrypoints, data helpers, and unit tests in between. The generator decides `infra/`, `.github/workflows/`, and the managed rule blocks. Never hand-edit `.github/workflows/` or `infra/`.

Do not create the empty GitHub repository. The developer creates that. When they give its URL, set the remote and push `main`, `staging`, and `production`. Do not run `scripts/bind-repo.sh` unless they say they have permission and ask you to run it. Do not run `protect-branches.sh`. Branch protection is an organization ruleset. Do not leave a checkout of `opptra/sdlc-resources` on the machine.

Apps Script is not a choice. If the whole request is only Apps Script, say so and stop. When part of a request needs something the platform does not generate yet (such as project-level billing budgets), scaffold every part the platform does support and record the gap under `unmet` in `service.yaml` with a clear recommendation.

## 1. Route Banner, Resume Check & Understand

Print the route banner first so the developer knows the phases and gates:

```text
Route: create-app | Phases: 1. Manifest  2. Runtime & OpenSpec  3. Data/Cloud  4. Tests  5. Infra/CI/Rules
Human Gates: After the 14-Point Blueprint Table, and after Phase 5 (Walking Skeleton)
Script-Owned Paths: infra/, .github/workflows/, managed rule blocks in AGENTS.md & CLAUDE.md
```

1. **Resume check:** If `.sdlc/state.yaml` already exists in the target directory, read it and offer to resume from the next uncompleted phase instead of re-interviewing.
2. **Linear check (#3):** Read the Linear issue when they named one. If Linear is not connected yet, continue the scaffold and connect it in Phase 2 before the run is finished. Do not invent a ticket id.
3. **Local plan check:** Check the current directory for an existing migration or architecture plan (such as `MIGRATION_PLAN.md`). Treat every decision already stated in that plan—region, jobs, crons, Firestore vs Postgres vs BigQuery, buckets, queues, webhook receiver, secrets, domain edge cases—as answered. Do not re-ask what the plan already fixed.
4. **Ask only what is missing:** Ask one question at a time in plain language using the structured question tool in Cursor.

### Workloads, capabilities, and auth

- **Nothing runs** (settings, prompts, or skills only): archetype `config-only`, auth `none`, parts `[config]`.
- **One background job**: archetype `cloud-run-job`, auth `none`, parts `[job]`.
- **Several scheduled jobs sharing one image, with an optional webhook receiver**: archetype `scheduled-jobs`, auth `none`, parts `[job]`, with a `jobs:` list and optional `receiver:` (`auth: shared-secret`). An HTTP portal login or tracking-page fetch stays on a job; do not move it to a VM.
- **A real browser that must stay open, a long-lived process, or local disk state**: archetype `vm-worker`, auth `none`, parts `[worker]`.
- **A page people open or an HTTP API**: archetype `cloud-run-service`, parts `[api]` (and `ui` when there is a page), auth `iap` (staff), `app-login`, `shared-secret` (webhook), or `public`.
- **Per-component region**: Set `region` on a component when it runs in a different GCP region from the app default.
- **Data, storage, queues, secrets, alerts**:
  - `database: postgres` (Cloud SQL), `firestore` (`(default)` DB), `bigquery` (analytical warehouse), or `none`
  - `bucket: private` for reports, manuals, exports, or uploads
  - `queue: <name>` for Cloud Tasks webhook/event buffering
  - `secrets: [<id>, ...]` for Secret Manager shells (IDs only, never values)
  - `alerts: true` for failed job / error log alert policies

## 2. Show the 14-Point Blueprint Table & Wait for Confirmation

Before writing any files, present the **14-Point Blueprint Table** so the developer sees the complete setup:

| # | Area | Planned Setup for This App |
|---|---|---|
| **1** | **Components & Architecture** | Component names, archetypes, regions, and parts |
| **2** | **OpenSpec Setup** | Install `@fission-ai/openspec` if missing, then `openspec init --tools cursor,claude` in the app |
| **3** | **Linear Setup** | Connect Linear in Cursor or Claude and read the issue before the scaffold is called done |
| **4** | **`service.yaml` Manifest** | Root `service.yaml` + any `unmet` items and recommendations |
| **5** | **Agentic Rules (5.1–5.10)** | All 10 rule pillars (`TDD`, `Commit/PR`, `Linear`, `OpenSpec`, `Infra/Terraform`, `Workflows`, `JSON Logging`, `Data Safety`, `Secrets/PII`, plus any domain edge cases under `## Product contract`) |
| **6** | **GitHub Workflows** | `ci.yml`, `plan.yml`, `deploy-staging.yml`, `deploy-production.yml` |
| **7** | **Testing Setup** | `pytest` + `ruff` (and `npm run lint` / `typecheck` / `test` when `ui` is present) |
| **8** | **Deployment & Infrastructure** | Terraform `infra/` + WIF deploy on `staging` push and `production` PR merge |
| **9** | **Git Branches & Governance** | `main`, `staging`, `production`, `.github/CODEOWNERS`, PR template |
| **10** | **Secrets & Security** | Secret Manager shells in `service.yaml` + `.gitignore` |
| **11** | **Database, Warehouse & State** | `postgres`, `firestore`, `bigquery`, or `none` + `bucket` / `queue` |
| **12** | **Authentication** | `iap`, `app-login`, `shared-secret`, `public`, or `none` |
| **13** | **Observability & Alerts** | `/api/health` or job runner + JSON stdout logging + `alerts` |
| **14** | **README & Runbook** | Local run (`make setup`, `make dev`, `make test`), deploy steps, and `unmet` notes |
| **15** | **Local Development & `.env.example`** | `.env.example` with all secrets/config + `Makefile` + `backend/app/config.py` local `.env` loader |

Ask the developer to confirm before running the phases.

## 3. Execute the 5 Phases (`script → skill → check`)

Clone `main` of `opptra/sdlc-resources` into a temporary directory:

```bash
tmpdir=$(mktemp -d)
git clone --depth 1 --branch main https://github.com/opptra/sdlc-resources.git "$tmpdir/sdlc"
```

### Phase 1: Manifest (`check`)
Write `service.yaml` and validate it:
```bash
python3 "$tmpdir/sdlc/scripts/sdlc.py" check "$tmpdir/service.yaml"
```

### Phase 2: Runtime, OpenSpec & Entrypoints (`init-runtime`)
1. Run:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" init-runtime "$tmpdir/service.yaml" "<target-dir>" --overwrite
   ```
2. Install OpenSpec and initialize it in the app. An empty `openspec/` directory is not enough. From `<target-dir>`:
   ```bash
   if ! openspec --version; then
     npm install -g @fission-ai/openspec@latest
   fi
   openspec init --tools cursor,claude
   ```
   If `npm install` or `openspec init` fails, fix that before Phase 3. Do not leave this as a later recommendation.
3. Confirm Linear is connected in Cursor or Claude and that the named issue can be read. Linear is not an app package. It is the IDE connection the later skills use for the ticket id. If it is not connected, connect it in this phase and re-read the issue. Do not invent a ticket id, and do not finish the scaffold while the issue still cannot be read.
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

### Phase 5: Infra, Workflows, Rules & Final Scorecard (`sync-infra`)
1. If the user's plan has domain-specific edge cases (such as Section 6 of a migration plan), write them under `## Product contract` in `<target-dir>/AGENTS.md` and `<target-dir>/CLAUDE.md` so `sync-infra` preserves them below the managed SDLC rules block.
2. Run:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" sync-infra "$tmpdir/service.yaml" "<target-dir>"
   python3 "$tmpdir/sdlc/scripts/sdlc.py" status "<target-dir>" --table
   python3 "$tmpdir/sdlc/scripts/sdlc.py" status "<target-dir>" --check
   rm -rf "$tmpdir"
   ```
3. Never hand-edit `infra/` or `.github/workflows/`.

## 4. Summary scorecard, then next steps

Do not stop after `status --table` alone. Add a second table, **Built and still to build**, before the summary. One row per thing the plan or the request asked for.

| Item | In the scaffold? | Why | What you do next |
|---|---|---|---|
| Example: eight Cloud Run jobs | Yes | The plan listed them, so the scaffold created the jobs, commands, and crons | Try them with a direct push to staging after bind-repo.sh |
| Example: laptop handler code | No | The scaffold is the platform shell. Porting behaviour is a feature | One `/feature` pull request per cutover slice |

Mark each row Yes or No. A Yes row says why it was included. A No row says it was left out on purpose and what the next pull request is. Include `unmet` items as No.

### Summary

Say what was created: app name, directory, workloads, data store, bucket, queue, auth, and that `openspec/` was initialized. Name the Linear issue id that was read. Name anything still under `unmet`.

### Next steps, in this order

1. **Run and verify locally first (`make setup && make dev && make test`).**
   The scaffold generated `.env.example`, `Makefile`, and `backend/app/config.py` (which reads `.env` when `APP_ENV=local` and Secret Manager in the cloud). Copy `.env.example` to `.env`, fill in any local test values, and run `make setup`, `make dev`, and `make test` on your machine before deploying.
2. **Build your first feature slice locally with `/feature`.**
   The scaffold is the platform shell. Port or build product behaviour one `/feature` pull request at a time.
3. **Connect the empty GitHub repository when ready to push.**
   Ask whether the empty GitHub repository already exists. If they paste a URL now or in a later message, store it and push the three branches. Accept `https://github.com/org/repo`, `git@github.com:org/repo.git`, or `org/repo`.
   ```bash
   python3 scripts/sdlc.py set-github-repo "<url>" .
   git init
   git add .
   git commit -m "feat: <ticket-id> scaffold"
   git branch -M main
   git remote add origin "<url>"
   git push -u origin main
   git branch staging
   git branch production
   git push -u origin staging
   git push -u origin production
   ```
   If `origin` already exists, use `git remote set-url origin "<url>"`. If a branch already exists on the remote, do not force-push. If they do not have a repository yet, stop this step and continue when they send the URL. Read `.sdlc/state.yaml` on a later turn so you do not re-ask the scaffold facts.
4. **Explain `scripts/bind-repo.sh` before anyone runs it.** It lets GitHub Actions for this repository impersonate a deployer service account in the production project and in `opptra-staging`. That account can push the image and apply Terraform. The script does not deploy. A direct push to `staging` deploys staging. A pull request from `main` into `production` is the only deploy that comes from `main`. Do not merge `main` into `staging`. Branch protection is already an organization ruleset, so this script does not protect branches. The developer runs `scripts/bind-repo.sh` if they can change IAM in those projects. Otherwise they give that file to someone who can. Do not run it yourself unless they say they have permission and ask you to.
5. **Test on `staging`, then promote `main` to `production`.** After the bind script has succeeded, push the branch you want to try directly to `staging` and read the Terraform plan. Confirm the jobs, schedules, and webhook match `service.yaml`. A disabled job must have no Scheduler entry. Merging to `main` does not update staging.
6. **Put secret values into Secret Manager and close `unmet` items.** The scaffold only created secret ids. Close each `unmet` item (such as a data import or project billing budget) in its own pull request.

If those feature slices are already known, ask **once**: pause for review after each slice, or run each slice through its checks without stopping.

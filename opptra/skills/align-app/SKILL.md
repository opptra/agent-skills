---
name: align-app
description: Inspects an existing repository with the Opptra 14-point SDLC scorecard, strongly recommends OpenSpec and Linear setup, audits all 10 agentic rule pillars, and applies accepted changes in phases without overwriting product rules. Use when a developer asks to align, migrate, audit, or update an existing app to the SDLC standard.
---

# Align an existing app

Run this inside the repository the developer has open. Do not create a new repository. Do not delete a deploy script, move a live host, or run `terraform import` without explicit confirmation. Never overwrite existing domain rules under `## Product contract` in `AGENTS.md` or `CLAUDE.md`.

Before you edit any file, print the Route Banner and the two scorecard tables below, then wait. Apply only the rows the developer accepts. Before a commit or a push, show the message, the files, the branch, and the pull request body, and wait. Do not invent a Linear ticket id.

## 1. Route Banner & Deterministic Scan

Start by printing the route banner so the developer knows the exact stages and gates:

```text
Route: align-app | Mode: 14-Point Audit -> Select Rows -> Apply Phases -> Verify Scorecard
Phases: 1. Deterministic Scan  2. 14-Point & Rule Pillar Tables  3. Apply Selected Rows  4. Post-Align Check
Human Gates: Before writing any file, and before git commit/push
Protected Content: Existing Product Contract in AGENTS.md/CLAUDE.md and custom README sections are preserved
```

If `.sdlc/state.yaml` exists in the repository, read it and offer to resume from the last completed phase.

Clone `main` of `opptra/sdlc-resources` into a temporary directory and run `sdlc.py status`:

```bash
tmpdir=$(mktemp -d)
git clone --depth 1 --branch main https://github.com/opptra/sdlc-resources.git "$tmpdir/sdlc"
python3 "$tmpdir/sdlc/scripts/sdlc.py" status . --json
python3 "$tmpdir/sdlc/scripts/sdlc.py" status . --table
```

If the repo is Apps Script only (`.clasp.json` / `appsscript.json` with no service or job), report that Apps Script is unsupported, remove `$tmpdir`, and stop.

## 2. Propose `service.yaml` & Present the Two Standardized Tables

Inspect the repository layout (`Dockerfile`, `deploy/`, `pyproject.toml`, `requirements.txt`, `package.json`, `src/`, `apps/`, `scripts/`, `tests/`, `.github/workflows`) and propose `service.yaml`:
- Use per-component `region` when components run in different GCP regions (for example, a dashboard in `asia-southeast1` and jobs in `asia-south1`).
- Use per-component `path` and `frontend_path` when code lives in existing folders (such as `path: .` and `frontend_path: apps/web`) instead of `components/<name>`, so `.github/workflows/ci.yml` runs against directories that actually exist.
- Use `database: postgres | firestore | bigquery | none`, `bucket: private | none`, `queue`, `secrets`, `alerts`, and `unmet` for any platform gap.

Always present **both** tables from `sdlc.py status --table`. Every row has a last column, **What this means for you**. Keep that column. If the default sentence does not match this repo, rewrite it in plain language: what the row is checking, and what the developer will do differently once that row is in place.

### Table A: 14-Point Repository Scorecard

| # | Area | Current Setup in Repo | Target Standard | Up to the Mark? | Action / Changes to be Done | What this means for you |
|---|---|---|---|---|---|---|
| **1** | **Components & Architecture** | Services, UIs, scheduled jobs, regions, and actual repo paths found | All components, regions, and paths mapped | Yes / Partial / No | Map components, regions, and `path` / `frontend_path` in `service.yaml` |
| **2** | **OpenSpec Setup** | Whether `openspec` CLI is installed and `openspec/` is initialized | CLI installed and `openspec init` already run | Yes / Partial / No | Install `@fission-ai/openspec` if needed and run `openspec init --tools cursor,claude` in this repo |
| **3** | **Linear Setup** | Whether Linear can read an issue | Linear connected and one issue readable | Yes / Partial / No | Connect Linear in Cursor or Claude in this turn and confirm an issue can be read |
| **4** | **`service.yaml` Manifest** | Missing or present (and whether all components/secrets/regions are valid) | Valid root `service.yaml` | Yes / No | Write or update `service.yaml` and validate with `sdlc.py check` |
| **5** | **Agentic Rules (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`)** | Summary score (`X/10 pillars`) + whether `.cursor/rules/*.mdc` exist | 10/10 pillars + preserved `## Product contract` | Yes / Partial (`X/10`) | Sync managed `<!-- sdlc-rules-start -->` block while keeping Product Contract intact (see Table B) |
| **6** | **GitHub Workflows (`.github/workflows`)** | Existing workflows and whether their `working_directory` paths exist | PR-only `ci.yml` matching actual repo paths + `plan.yml` / `deploy-*.yml` when Terraform is active | Yes / Needs fix / Missing | Generate `ci.yml` (`--ci-only` when still on legacy deploy scripts, or full workflows when Terraform is active) |
| **7** | **Testing Setup & Coverage** | Existing Python/UI test files, `pyproject.toml` / `pytest.ini`, UI `lint`/`typecheck`/`test` scripts | Ruff + pytest for Python; lint + typecheck + test for UI | Yes / Partial / No | Add missing test runner config or run `sdlc.py add-tests` |
| **8** | **Deployment & Infrastructure** | How deployment happens today (`deploy/*.sh`, `vercel.json`, `fly.toml`, Task Scheduler) | Terraform `infra/` + GitHub Actions WIF on `staging` & `production` | Yes / Transitional / Missing | Keep current deploy during initial alignment; run `/adopt-terraform` next to scan deploy scripts, generate `infra/` + `imports.tf.example`, and retire legacy scripts | |
| **9** | **Git Branches & Governance** | Default branch on GitHub, `main` / `staging` / `production`, `CODEOWNERS`, PR template | `main` default, `staging` & `production` branches, `CODEOWNERS`, PR template | Yes / Partial / No | Create missing branches and write `.github/CODEOWNERS` and the PR template. Organization rules protect `main` and `production`. | |
| **10** | **Secrets, Credentials & Security** | `.gitignore` coverage, local `secrets/` or `.env` files, GCP Secret Manager usage | Secret IDs in `service.yaml`; no keys in Git | Yes / Review needed | Ensure `.env*` and `secrets/` are in `.gitignore`; list Secret Manager IDs in `service.yaml` | |
| **11** | **Database, Warehouse & State** | Cloud SQL Postgres, Firestore, BigQuery DDL, GCS buckets, or local caches | Declared in `service.yaml` with matching safety rules | Yes / Partial / No | Set `database: postgres \| firestore \| bigquery \| none` and sync data rules | |
| **12** | **Authentication & Access Control** | Auth on each service/UI/webhook (`iap`, `app-login`, `shared-secret`, `public`) | Explicit `auth` per component (`iap` for staff UIs) | Yes / Needs mapping | Record `auth` on each component in `service.yaml` | |
| **13** | **Observability, Health & Alerts** | `/api/health`, logging format, job exit behavior on 429/5xx, alert policies | `/api/health` + JSON logs + non-zero exit on error + alerts | Yes / Partial / No | Add structured JSON logging rule/helper and `alerts: true` | |
| **14** | **README, Runbook & Local Dev** | Existing `README.md` sections and dependency lockfiles | Purpose, local run, tests, deploy flow, and `unmet` notes | Yes / Incomplete | Update managed SDLC section in `README.md` while keeping existing architecture notes | |
| **15** | **Local Development & `.env.example`** | Whether `.env.example` and `Makefile` (`make setup`, `make dev`, `make test`) exist | `.env.example` + `Makefile` + local `.env` secret fallback | Yes / Missing | Generate `.env.example` and `Makefile` so developers can run locally with `make setup && make dev` | |
| **16** | **External Resource Prefixing (`<prefix>-<resource>`)** | Active `prefix` in `service.yaml` and whether all jobs, services, queues, secrets, and buckets carry `<prefix>-` | All external GCP resources prefixed with `<prefix>-` | Yes / Needs prefixing | Add `prefix` to `service.yaml`, prefix any unprefixed job/service/queue/secret ID, and run `sdlc.py sync-infra` | |
| **17** | **Pre-Commit Hooks & Local CI Gate (`.githooks` + `make ci`)** | Whether `.githooks/pre-commit`, `.githooks/pre-push`, and `make ci` exist and pass | `.githooks/pre-commit` + `.githooks/pre-push` + `make ci` passing | Yes / Missing / Needs fix | Generate `.githooks/` and `make ci`, run them locally, auto-fix resolvable issues, or ask user whether to disable unresolvable checks | |

### Table B: Section 5 Breakdown

Fill **What this means for you** on every row from `sdlc.py status --table`, rewritten in plain language for this repo. — Agentic Rules (`5.1 – 5.10`)

| Sub-step | Rule Pillar | Current State in Repo | Up to the Mark? | Changes to be Done | What this means for you |
|---|---|---|---|---|---|
| **5.1** | **Test-Driven Development (TDD)** | Whether test-first and component test commands are documented | Yes / No | Keep existing TDD rules and include exact repo test commands |
| **5.2** | **Commit, PR & GitHub Flow** | `feat/<ticket>-<slug>`, `feat: <ticket> ...`, `main` / `staging` / `production` flow, infra PR split | Yes / Partial / No | Sync branch, commit, staging push, and infra PR separation rules |
| **5.3** | **Linear Rules** | Mandatory Linear issue check before code, stop if disconnected, no invented IDs | Yes / No | Add mandatory Linear ticket rule |
| **5.4** | **OpenSpec Rules** | Mandatory OpenSpec under `openspec/` before feature code | Yes / No | Add mandatory OpenSpec rule |
| **5.5** | **Infra Rules (GCP, Terraform, Resource Prefix, No Laptop Deploy)** | GCP only, Terraform in `infra/`, `<prefix>-<resource>` naming on all external GCP resources, no `deploy.sh` or laptop `gcloud run deploy` | Yes / Conflicts / No | Add GCP + Terraform + `<prefix>-<resource>` rule; flag any legacy `deploy.sh` as transitional | |
| **5.6** | **GitHub Workflow Guidelines** | Required `ci` and `plan` checks, workflows generated from `service.yaml` | Yes / No | Add workflow check rule |
| **5.7** | **Structured Logging & Job Exit Codes** | JSON stdout (`severity`, `message`, `service`, `environment`), non-zero exit on 429/5xx | Yes / Partial / No | Add JSON logging schema and non-zero job failure rule |
| **5.8** | **Database, Firestore & BigQuery Safety** | Alembic for Postgres, leases/idempotency for Firestore, DDL & currency/NULL rules for BigQuery | Yes / No | Sync `database.mdc`, `firestore.mdc`, or `bigquery.mdc` |
| **5.9** | **Secrets & PII Protection** | Never commit `.env`/keys, never log secrets/tokens/PII/signed URLs | Yes / No | Add secret and PII redaction rules |
| **5.10** | **Product / Domain Contract Preservation** | Existing domain-specific rules in `AGENTS.md` or `CLAUDE.md` | Yes | Preserve 100% under `## Product contract` outside `<!-- sdlc-rules-end -->` |

Ask the developer which rows to apply now (recommending all safe non-host-moving rows `1–7`, `9–12`, `14`, plus initializing `openspec/`).

## 3. Apply Selected Rows & Verify

1. Write `service.yaml` and validate with `python3 "$tmpdir/sdlc/scripts/sdlc.py" check service.yaml`.
2. If the repo still deploys via legacy scripts (`deploy/*.sh`, `vercel.json`, `fly.toml`) and the developer did not ask to generate Terraform `infra/` in this turn, run:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" sync-infra service.yaml . --ci-only
   ```
   Otherwise, run the selected phases (`add-data`, `add-tests`, `sync-infra`).
3. If the developer accepted OpenSpec setup and `openspec` CLI is installed, run `openspec init --tools cursor,claude` (or create `openspec/`).
4. Create `staging` and `production` branches from `main` when missing.
5. If the developer accepted the OpenSpec row, or `openspec/` is missing or only contains `.gitkeep`, install and initialize it in this repository. Do not leave it as a recommendation.
   ```bash
   if ! openspec --version; then
     npm install -g @fission-ai/openspec@latest
   fi
   openspec init --tools cursor,claude
   ```
6. If the Linear rule is missing from the scorecard, or the Linear connection cannot read an issue, connect Linear in Cursor or Claude in this turn. Check the current branch (`git branch --show-current`) first to reuse any active ticket; if none exists, agree on the alignment plan with the user first and then read or create one Linear issue with the alignment plan and requirements. Do not create a new ticket on every prompt, and do not invent a ticket id.
7. **Run and verify the generated `.githooks/` and `make ci`:**
   - Run `.githooks/pre-commit` and `make ci`.
   - Fix any auto-resolvable lint, formatting, or wiring issues automatically and re-run until green.
   - If a check fails due to something that cannot be resolved without user input (such as legacy code errors, missing external credentials, or tests requiring external services), explain the exact failure to the developer and ask whether to **(a)** provide input / fix those files now or **(b)** disable that specific check (`run_tests: false` or `run_lint: false`) in `service.yaml` and record it under `unmet` so commits and PRs are not blocked.
8. Re-run `python3 "$tmpdir/sdlc/scripts/sdlc.py" status . --table` and `--check`, then delete `$tmpdir`.

## 4. Summary and next steps

End with both of these. The scorecard is not the last thing the developer sees.

### Summary

Say which scorecard rows changed, whether OpenSpec is initialized, and whether Linear can read an issue. Name files written. Name what was left on the old deploy path on purpose.

### Next steps, in this order

1. Commit the accepted alignment on a branch and open one pull request into `main`.
2. Connect anything still red on OpenSpec or Linear before the next `/feature` or `/bug`.
3. When this alignment added a deploy workflow, `scripts/bind-repo.sh` is in the repo with the production project filled in. Explain it: the script lets GitHub Actions impersonate a deployer account and apply Terraform. It does not deploy, and it does not protect branches. Organization rules cover `main` and `production`. The developer runs the script if they can change IAM. Otherwise they give the file to someone who can. Do not run `protect-branches.sh`.
4. If `origin` is missing and the developer gives a repository URL now or later, set the remote and push `main`, `staging`, and `production` from the current commit. Record the URL with `python3 scripts/sdlc.py set-github-repo "<url>" .`. Do not force-push. Do not create the empty GitHub repository.
5. After `scripts/bind-repo.sh` has succeeded, try staging by pushing a branch directly to `staging`. Do not merge `main` into `staging`. Production is a pull request from `main` into `production`.
6. Move laptop or other legacy deploy scripts (`deploy.sh`, `cloudbuild.yaml`, `vercel.json`, `fly.toml`) to Terraform with `/adopt-terraform` before deleting them.
7. Port or fix product behaviour with `/feature` and `/bug`. Those skills expect OpenSpec and a real Linear issue.

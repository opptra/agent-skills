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

Always present **both** tables in full so every team member sees the same 14 areas and 10 rule pillars:

### Table A: 14-Point Repository Scorecard

| # | Area | Current Setup in Repo | Target Standard | Up to the Mark? | Action / Changes to be Done |
|---|---|---|---|---|---|
| **1** | **Components & Architecture** | Services, UIs, scheduled jobs, regions, and actual repo paths found | All components, regions, and paths mapped | Yes / Partial / No | Map components, regions, and `path` / `frontend_path` in `service.yaml` |
| **2** | **OpenSpec Setup** | Whether `openspec` CLI is installed and `openspec/` directory exists | `openspec` CLI + `openspec/` initialized | Yes / Partial / No | **Strongly Recommended:** Run `openspec init --tools cursor,claude` now so `/feature` never blocks |
| **3** | **Linear Setup** | Whether Linear MCP is connected and ticket workflow is configured | Linear MCP connected + mandatory ticket rule | Yes / Partial / No | **Strongly Recommended:** Connect Linear MCP and add rule 5.3 |
| **4** | **`service.yaml` Manifest** | Missing or present (and whether all components/secrets/regions are valid) | Valid root `service.yaml` | Yes / No | Write or update `service.yaml` and validate with `sdlc.py check` |
| **5** | **Agentic Rules (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`)** | Summary score (`X/10 pillars`) + whether `.cursor/rules/*.mdc` exist | 10/10 pillars + preserved `## Product contract` | Yes / Partial (`X/10`) | Sync managed `<!-- sdlc-rules-start -->` block while keeping Product Contract intact (see Table B) |
| **6** | **GitHub Workflows (`.github/workflows`)** | Existing workflows and whether their `working_directory` paths exist | PR-only `ci.yml` matching actual repo paths + `plan.yml` / `deploy-*.yml` when Terraform is active | Yes / Needs fix / Missing | Generate `ci.yml` (`--ci-only` when still on legacy deploy scripts, or full workflows when Terraform is active) |
| **7** | **Testing Setup & Coverage** | Existing Python/UI test files, `pyproject.toml` / `pytest.ini`, UI `lint`/`typecheck`/`test` scripts | Ruff + pytest for Python; lint + typecheck + test for UI | Yes / Partial / No | Add missing test runner config or run `sdlc.py add-tests` |
| **8** | **Deployment & Infrastructure** | How deployment happens today (`deploy/*.sh`, `vercel.json`, `fly.toml`, Task Scheduler) | Terraform `infra/` + GitHub Actions WIF on `staging` & `production` | Yes / Transitional / Missing | Keep current deploy during initial alignment; schedule `change-app` PR to generate & import Terraform before retiring scripts |
| **9** | **Git Branches & Governance** | Default branch on GitHub, `main` / `staging` / `production`, `CODEOWNERS`, PR template | `main` default, `staging` & `production` branches, `CODEOWNERS`, PR template | Yes / Partial / No | Create missing branches, write `.github/CODEOWNERS` & PR template, remind platform owner to run `protect-branches.sh` |
| **10** | **Secrets, Credentials & Security** | `.gitignore` coverage, local `secrets/` or `.env` files, GCP Secret Manager usage | Secret IDs in `service.yaml`; no keys in Git | Yes / Review needed | Ensure `.env*` and `secrets/` are in `.gitignore`; list Secret Manager IDs in `service.yaml` |
| **11** | **Database, Warehouse & State** | Cloud SQL Postgres, Firestore, BigQuery DDL, GCS buckets, or local caches | Declared in `service.yaml` with matching safety rules | Yes / Partial / No | Set `database: postgres \| firestore \| bigquery \| none` and sync data rules |
| **12** | **Authentication & Access Control** | Auth on each service/UI/webhook (`iap`, `app-login`, `shared-secret`, `public`) | Explicit `auth` per component (`iap` for staff UIs) | Yes / Needs mapping | Record `auth` on each component in `service.yaml` |
| **13** | **Observability, Health & Alerts** | `/api/health`, logging format, job exit behavior on 429/5xx, alert policies | `/api/health` + JSON logs + non-zero exit on error + alerts | Yes / Partial / No | Add structured JSON logging rule/helper and `alerts: true` |
| **14** | **README, Runbook & Local Dev** | Existing `README.md` sections and dependency lockfiles | Purpose, local run, tests, deploy flow, and `unmet` notes | Yes / Incomplete | Update managed SDLC section in `README.md` while keeping existing architecture notes |

### Table B: Section 5 Breakdown — Agentic Rules (`5.1 – 5.10`)

| Sub-step | Rule Pillar | Current State in Repo | Up to the Mark? | Changes to be Done |
|---|---|---|---|---|
| **5.1** | **Test-Driven Development (TDD)** | Whether test-first and component test commands are documented | Yes / No | Keep existing TDD rules and include exact repo test commands |
| **5.2** | **Commit, PR & GitHub Flow** | `feat/<ticket>-<slug>`, `feat: <ticket> ...`, `main` / `staging` / `production` flow, infra PR split | Yes / Partial / No | Sync branch, commit, staging push, and infra PR separation rules |
| **5.3** | **Linear Rules** | Mandatory Linear issue check before code, stop if disconnected, no invented IDs | Yes / No | Add mandatory Linear ticket rule |
| **5.4** | **OpenSpec Rules** | Mandatory OpenSpec under `openspec/` before feature code | Yes / No | Add mandatory OpenSpec rule |
| **5.5** | **Infra Rules (GCP, Terraform, No Laptop Deploy)** | GCP only, Terraform in `infra/`, no `deploy.sh` or laptop `gcloud run deploy` | Yes / Conflicts / No | Add GCP + Terraform rule; flag any legacy `deploy.sh` as transitional |
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
5. Re-run `python3 "$tmpdir/sdlc/scripts/sdlc.py" status . --table` and `--check` to show the updated scorecard, then delete `$tmpdir`.

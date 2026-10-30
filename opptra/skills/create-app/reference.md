# 17-point blueprint

Print this table after phase 5, from `sdlc.py status --table`. It is the receipt. Before any files, confirm only archetype, name, auth, data store, and prod project.

| # | Area | Planned Setup for This App |
|---|---|---|
| **1** | **Components & Architecture** | Component names, archetypes, regions, and parts |
| **2** | **OpenSpec Setup** | Install the pinned `@fission-ai/openspec` from `opptra/pins.env`, then `openspec init --tools cursor,claude` in the app |
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
| **16** | **External Resource Prefixing (`<prefix>-<resource>`)** | `prefix` in `service.yaml` applied to all Cloud Run services/jobs, Scheduler entries, queues, secrets, and buckets |
| **17** | **Pre-Commit Hooks & Local CI Gate (`.githooks` + `make ci`)** | `.githooks/pre-commit`, `.githooks/pre-push`, and `make ci` verified and self-healed locally |

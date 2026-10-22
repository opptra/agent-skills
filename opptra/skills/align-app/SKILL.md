---
name: align-app
description: Inspects an existing repository with the Opptra SDLC status script, recommends what can be adopted now, fills capability gaps in phases, and records later architectural changes. Use when a developer asks to align, migrate, audit, or update an existing app to the SDLC standard.
---

# Align an existing app

Run this inside the repository the developer has open. Do not create a new repository. Do not delete a deploy script, move a live host, or run `terraform import` without explicit confirmation.

Before you edit any file, show the report below and wait. Apply only the items the developer accepts. Before a commit or a push, show the message, the files, the branch, and the pull request body, and wait. Do not invent a Linear ticket id.

## Inspect the standard and this repository

Clone `main` of `opptra/sdlc-resources` into a temporary directory and run `sdlc.py status --json`:

```bash
tmpdir=$(mktemp -d)
git clone --depth 1 --branch main https://github.com/opptra/sdlc-resources.git "$tmpdir/sdlc"
python3 "$tmpdir/sdlc/scripts/sdlc.py" status . --json
```

Read `$tmpdir/sdlc/docs/align.md`, `$tmpdir/sdlc/mapping.yaml`, and `$tmpdir/sdlc/service.schema.json`.

If the repo is Apps Script only (`.clasp.json` / `appsscript.json` with no service or job), report that Apps Script is unsupported, clean up `$tmpdir`, and stop.

## Propose `service.yaml` and present the 3-bucket report

Propose a `service.yaml` matching what the repository runs or is migrating toward (`cloud-run-service`, `cloud-run-job`, `scheduled-jobs`, `vm-worker`, or `config-only`, plus `database: postgres | firestore | none`, `bucket`, `queue`, `secrets`, `alerts`, and any `unmet` items).

Show three sections and wait for the developer to choose which items to apply:

### 1. Adopt now (safe, no host move)
- `service.yaml` at the repo root.
- `.gitignore` and `.github/CODEOWNERS` when missing.
- `AGENTS.md`, `CLAUDE.md`, and `.cursor/rules/*.mdc` compiled for this repo's capabilities. Quote any missing rules compared to `rules/source/always.md`.
- `README.md` with purpose, local run commands, test commands, any `unmet` recommendations, and deploy steps.
- Pull-request-only `.github/workflows/ci.yml` calling `opptra/sdlc-resources` at `main`.
- `main`, `staging`, and `production` branches when missing.

### 2. Fill capability gaps (phased scripts + skill)
List any capability detected in the code or migration plan that is missing its standard helper, test harness, or Terraform module:
- `sdlc.py add-data` — install and wire missing Postgres (`db.py`, Alembic) or Firestore (`firestore_state.py`, `storage.py`) helpers.
- `sdlc.py add-tests` — add missing entrypoint/health unit tests and local fixtures.
- `sdlc.py sync-infra` — generate `infra/` and deploy workflows when ready to move deployment to GitHub Actions + Terraform.

### 3. Later recommendations
Cite any legacy deploy scripts (`deploy.sh`, `vercel.json`, `cloudbuild.yaml`, laptop Task Scheduler wrappers) or `unmet` items, explain what the standard does, and recommend the follow-up `change-app` or `feature` pull requests.

## Apply

Run only the accepted items using `$tmpdir/sdlc/scripts/sdlc.py` (`check`, `add-data`, `add-tests`, `sync-infra`, or `build_rules.py`), verify with `python3 "$tmpdir/sdlc/scripts/sdlc.py" status . --check` when full alignment was chosen, and remove `$tmpdir`.

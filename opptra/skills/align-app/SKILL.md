---
name: align-app
description: Inspects an existing repository with the Opptra 17-point SDLC scorecard, strongly recommends OpenSpec and Linear setup, audits all 10 agentic rule pillars, and applies accepted changes in phases without overwriting product rules. Use when a developer asks to align, migrate, audit, or update an existing app to the SDLC standard.
---

# Align an existing app

Run this inside the repository the developer has open. Do not create a new repository. Do not delete a deploy script, move a live host, or run `terraform import` without explicit confirmation. Never overwrite existing domain rules under `## Product contract` in `AGENTS.md` or `CLAUDE.md`.

Before you edit any file, print the Route Banner and the two scorecard tables, then wait. Apply only the rows the developer accepts. Before a commit or a push, show the message, the files, the branch, and the pull request body, and wait. Do not invent a Linear ticket id.

## 1. Route Banner & Deterministic Scan

Start by printing the route banner so the developer knows the exact stages and gates:

```text
Route: align-app | Mode: 17-Point Audit -> Select Rows -> Apply Phases -> Verify Scorecard
Phases: 1. Deterministic Scan  2. 17-Point & Rule Pillar Tables  3. Apply Selected Rows  4. Post-Align Check
Human Gates: Before writing any file, and before git commit/push
Protected Content: Existing Product Contract in AGENTS.md/CLAUDE.md and custom README sections are preserved
```

If `.sdlc/state.yaml` exists in the repository, read it and offer to resume from the last completed phase. That file records generator progress. It does not hold a Linear ticket id.

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

Always present both tables from `sdlc.py status --table`. That output is the 17-point scorecard and the 10 rule pillars. Every row has a last column, **What this means for you**. Keep that column. If the default sentence does not match this repo, rewrite it in plain language: what the row is checking, and what the developer will do differently once that row is in place. When you fill a row by hand, use the columns in `reference.md`.

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
6. If the Linear rule is missing from the scorecard, or the Linear connection cannot read an issue, connect Linear in Cursor or Claude in this turn. Read and follow `../linear-continuity/SKILL.md`. When you create or update the issue, include the alignment plan and the rows the developer accepted. Do not invent a ticket id.
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

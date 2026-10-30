---
name: align-app
description: Inspects an existing repository with the Opptra 17-point SDLC scorecard, strongly recommends OpenSpec and Linear setup, audits all 10 agentic rule pillars, and applies accepted changes in phases without overwriting product rules. Use when a developer asks to align, migrate, audit, or update an existing app to the SDLC standard.
---

# Align an existing app

Run this inside the repository the developer has open. Do not create a new repository. Do not delete a deploy script, move a live host, or run `terraform import` without explicit confirmation. Never overwrite existing domain rules under `## Product contract` in `AGENTS.md` or `CLAUDE.md`.

Before you edit any file, read Pins in `../session/SKILL.md`, print the Route Banner with those two lines and the two scorecard tables, then wait. Apply only the rows the developer accepts. Before a commit or a push, show the message, the files, the branch, and the pull request body, and wait. Do not invent a Linear ticket id.

## 1. Route Banner & Deterministic Scan

Start by printing the route banner so the developer knows the exact stages and gates:

```text
Route: align-app | Mode: 17-Point Audit -> Select Rows -> Apply Phases -> Verify Scorecard
Phases: 1. Deterministic Scan  2. 17-Point & Rule Pillar Tables  3. Apply Selected Rows  4. Post-Align Check
Human Gates: Before writing any file, and before git commit/push
Protected Content: Existing Product Contract in AGENTS.md/CLAUDE.md and custom README sections are preserved
```

If `.sdlc/state.yaml` exists in the repository, read it and offer to resume from the last completed phase. That file records generator progress. It does not hold a Linear ticket id.

Run Generator checkout from `../session/SKILL.md`. It sets `$tmpdir` and `$tmpdir/sdlc`. Reuse `generator_sha` when `.sdlc/state.yaml` has one. Then run `sdlc.py status`:

```bash
python3 "$tmpdir/sdlc/scripts/sdlc.py" status . --json
python3 "$tmpdir/sdlc/scripts/sdlc.py" status . --table
```

If the repo is Apps Script only (`.clasp.json` / `appsscript.json` with no service or job), report that Apps Script is unsupported, remove `$tmpdir`, and stop.

## 2. Propose `service.yaml` & Present the Two Standardized Tables

Inspect the repository layout (`Dockerfile`, `deploy/`, `cloudbuild.yaml`, `.env.example`, `pyproject.toml`, `requirements.txt`, `package.json`, `src/`, `apps/`, `scripts/`, `tests/`, `.github/workflows`) and run `python3 "$tmpdir/sdlc/scripts/sdlc.py" discover-infra . --propose-manifest` when `service.yaml` is missing to generate a starting draft. Refine `service.yaml`:
- Use per-component `region` when components run in different GCP regions (for example, a dashboard in `asia-southeast1` and jobs in `asia-south1`).
- Use per-component `path` and `frontend_path` when code lives in existing folders (such as `path: .` and `frontend_path: apps/web`) instead of `components/<name>`, so `.github/workflows/ci.yml` runs against directories that actually exist.
- When existing GCP resources in `prod_project` have legacy unprefixed names, set `legacy_service_name: <existing-service-name>` and `secret_map: { ENV_VAR: existing-secret-id }` on the component so live production secrets and services do not need to be renamed to pass the 17-point scorecard.
- Use `database: postgres | firestore | bigquery | none`, `bucket: private | none`, `queue`, `secrets`, `env`, `alerts`, and `unmet` for any platform gap.

Always present both tables from `sdlc.py status --table`. That output is the 17-point scorecard and the 10 rule pillars. Every row has a last column, **What this means for you**. Keep that column. If the default sentence does not match this repo, rewrite it in plain language: what the row is checking, and what the developer will do differently once that row is in place. When you fill a row by hand, use the columns in `reference.md`.

Offer three paths and one recommendation. Wait for one yes. Do not ask them to tick 17 rows. The scorecard is the receipt.

| Path | When | What you do |
|---|---|---|
| Ship today | They only need a bug or feature merged | Remove `$tmpdir` and stop. Write no files. Tell them to use `bug` or `feature`. |
| Make the agent safe | They said align, and the host can stay | Recommend this when `deploy.sh`, `vercel.json`, `fly.toml`, or `cloudbuild.yaml` is present, and whenever they did not ask to move the host. Apply the steps in section 3. |
| Move the host | They want Terraform to replace the current deploy | Follow `../adopt-terraform/SKILL.md` in this same chat. Do not delete `deploy.sh` in the pull request that introduces Terraform. |

Inside Make the agent safe, honor a single exception such as "skip OpenSpec". Do not turn that into a row-by-row interview.

## 3. Apply the accepted path

Path 1 writes nothing. Path 3 follows `adopt-terraform`. Path 2 does the steps below. If the repo still deploys through `deploy/*.sh`, `vercel.json`, `fly.toml`, or `cloudbuild.yaml`, pass `--ci-only` and leave that deploy path in place.

1. Write `service.yaml` and validate with `python3 "$tmpdir/sdlc/scripts/sdlc.py" check service.yaml`.
2. For a legacy deploy path, run:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" sync-infra service.yaml . --ci-only
   ```
   When there is no legacy deploy path, run `add-data`, `add-tests`, and `sync-infra` without `--ci-only`.
3. Install the pinned OpenSpec unless they skipped it. Follow OpenSpec pin in `../session/SKILL.md`. Do not install `@latest`. Then run `openspec init --tools cursor,claude` when `openspec/` is missing or only contains `.gitkeep`.
4. Create `staging` and `production` branches from `main` when missing.
5. If the Linear rule is missing from the scorecard, or the Linear connection cannot read an issue, connect Linear in Cursor or Claude in this turn. Read and follow `../linear-continuity/SKILL.md`. When you create or update the issue, include the alignment plan and the path they accepted. Do not invent a ticket id.
6. **Run and verify the generated `.githooks/` and `make ci`:**
   - Run `.githooks/pre-commit` and `make ci`.
   - Fix any auto-resolvable lint, formatting, or wiring issues automatically and re-run until green.
   - If a check fails due to something that cannot be resolved without user input (such as legacy code errors, missing external credentials, or tests requiring external services), explain the exact failure to the developer and ask whether to **(a)** provide input / fix those files now or **(b)** disable that specific check (`run_tests: false` or `run_lint: false`) in `service.yaml` and record it under `unmet` so commits and PRs are not blocked.
7. Re-run `python3 "$tmpdir/sdlc/scripts/sdlc.py" status . --table` and `--check`, then delete `$tmpdir`.

## 4. Summary and next steps

End with both of these. The scorecard is not the last thing the developer sees.

### Summary

Say which scorecard rows changed, whether OpenSpec is initialized, and whether Linear can read an issue. Name files written. Name what was left on the old deploy path on purpose.

### Next steps, in this order

1. Commit the accepted alignment on a branch and open one pull request into `main`.
2. Connect anything still red on OpenSpec or Linear before the next `/feature` or `/bug`.
3. When this alignment added a deploy workflow, explain `scripts/bind-staging.sh` and `scripts/bind-production.sh`. Staging bind needs IAM on `opptra-staging` only. Production bind goes to someone who can change IAM in `prod_project`. Neither script deploys, and neither protects branches. Do not run either script unless they ask. Do not run `protect-branches.sh`.
4. If `origin` is missing, ask once. On yes, create a private `opptra/<name>` the way `create-app` does, and push `main`, `staging`, and `production`. If they paste an existing URL, set the remote and push those branches. Do not force-push. Record the slug with Generator checkout and `python3 "$tmpdir/sdlc/scripts/sdlc.py" set-github-repo "<url>" .`, then delete `$tmpdir`.
5. After `scripts/bind-staging.sh` has succeeded, try staging by pushing a branch directly to `staging`. Do not merge `main` into `staging`. Production is a pull request from `main` into `production`. Print the ship card from `../session/SKILL.md`.
6. Move laptop or other legacy deploy scripts (`deploy.sh`, `cloudbuild.yaml`, `vercel.json`, `fly.toml`) to Terraform with `/adopt-terraform` before deleting them.
7. Port or fix product behaviour with `/feature` and `/bug`. Those skills expect OpenSpec and a real Linear issue.

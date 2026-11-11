---
name: adopt-terraform
description: Analyzes an existing repository's deploy scripts, Dockerfiles, and GCP resources, presents a Terraform Adoption Scorecard, and generates service.yaml, infra/, and declarative Terraform import blocks. Use when a developer asks to move an existing app onto Terraform, replace deploy.sh, or set up GCP Terraform for a repo.
---


## Skill version check

Before following this skill, read and follow [Skill freshness](../session/SKILL.md#skill-freshness). Run it once per user request, including when this skill is invoked directly. A route or shared reference within the same request reuses that result. After an update, reread this file and any shared instructions before continuing.

# Adopt Terraform for an existing app

Use this skill when an existing repository deploys through shell scripts (`deploy.sh`), Cloud Build (`cloudbuild.yaml`), Vercel, Fly.io, or manual `gcloud` commands and wants to move its GCP resources under Opptra's standard Terraform (`infra/`) and GitHub Actions workflows without recreating live production services, jobs, or secrets.

Do not delete `deploy.sh` in the same pull request that introduces Terraform. Do not run `terraform apply` against production from a laptop.

Before you edit any file, read Pins in `../session/SKILL.md`, print the Route Banner with those two lines and the Terraform Adoption Scorecard, and wait for the developer to confirm. Before a commit or a push, show the message, the files, the branch, and the pull request body, and wait.

## 1. Route Banner & Deterministic Infra Discovery

Print the route banner first:

```text
Route: adopt-terraform | Branch: infra/<ticket-id>-adopt-terraform
Stages: 1. Discover Repo Infra  2. Adoption Scorecard Table  3. Generate service.yaml, infra/ & imports  4. Verify Plan (0 to destroy)
Human Gates: Before writing files, before commit/push, and on the PR Terraform plan comment
Script-Owned Paths: infra/main.tf, infra/variables.tf, infra/outputs.tf, .github/workflows/
```

1. **Plan first and resolve the Linear ticket.** Agree the Terraform adoption plan with the developer, then read and follow `../linear-continuity/SKILL.md`. When you create or update the issue, include the adoption scorecard summary. Do not invent a ticket id.
2. Run Generator checkout from `../session/SKILL.md`. It sets `$tmpdir` and `$tmpdir/sdlc`. Reuse `generator_sha` when `.sdlc/state.yaml` has one. Then run `discover-infra` (and `--propose-manifest` if `service.yaml` does not exist yet):
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" discover-infra . --json
   python3 "$tmpdir/sdlc/scripts/sdlc.py" discover-infra . --table
   python3 "$tmpdir/sdlc/scripts/sdlc.py" discover-infra . --propose-manifest
   ```

## 2. Present the Terraform Adoption Scorecard Table

Inspect the output of `discover-infra` alongside any Dockerfiles, `deploy/*.sh`, `cloudbuild.yaml`, `.env.example`, `scripts/`, and `service.yaml` in the repo. Present the **Terraform Adoption Scorecard Table** so the developer sees every GCP resource that will be managed:

| Resource Found | Type & Settings (Region, Memory, Timeout, Auth) | Where It Lives Today | Target Terraform Module | Action (`Create` vs `Import`) | What this means for you |
|---|---|---|---|---|---|
| Example: `pm-dashboard` | Cloud Run Service (`asia-southeast1`, `iap`) | `deploy/dashboard/deploy.sh` | `modules/cloud-run-service` | **Import** if live in `prod_project`, **Create** in `opptra-staging` | Replaces `gcloud run deploy` with Terraform; importing prevents a duplicate service |
| Example: `noon-hourly` | Cloud Run Job (`asia-south1`, `2Gi`, `3000s`, cron) | `deploy/noon-pipeline/deploy.sh` | `modules/cloud-run-job` + `modules/schedule` | **Import** job, **Create/Sync** Scheduler | Cron schedules and job settings become PR-reviewed changes in `service.yaml` |
| Example: `slack-bot-token` | Secret Manager secret ID | `--set-secrets` in `deploy.sh` | `modules/secrets` | **Import** secret shell via `secret_map` (versions untouched) | Grants runtime service account `secretAccessor` without renaming live secrets or storing values in Git |

Also highlight any custom flags in `deploy.sh` or `cloudbuild.yaml` (such as per-component regions, `--memory`, `--timeout`, unprefixed legacy resource names mapped via `legacy_service_name` and `secret_map: { ENV_VAR: existing-secret-id }`, pre-existing/shared resources connected via `existing_secrets`, `postgres_instance` / `postgres_secret` / `postgres_external`, `existing_bucket`, `bigquery_project` + `bigquery_datasets`, extra IAM roles via `extra_roles`, or custom GCP resources like Pub/Sub and Redis generated into `infra/custom.keep.tf`) and explain how they map into `service.yaml`. Note that `sdlc.py sync-infra` preserves `infra/custom.keep.tf`, `infra/imports.tf`, and `infra/imports.tf.example` across re-runs.

Ask the developer to confirm which resources already exist in `prod_project` (to be imported) versus which are brand new.

## 3. Bootstrap or continue from existing Terraform

Read the ownership and file map in [session](../session/SKILL.md). If Terraform already deploys staging or the app owns its files, use the checked-in Terraform. Preserve its backend and resource addresses. Use the generator phases below only for a fresh bootstrap. Use read-only discovery against the live project and classify each item as create, import, or reference. For imports, verify the exact project, region, cloud ID, live settings, and target resource address. Keep imports production-scoped, for example through `for_each` with an empty staging map. Shared resources remain references.

### Generate the initial files

1. Branch from `main` as `infra/<ticket-id>-adopt-terraform`.
2. Write or update `service.yaml` with all discovered components, per-component `region`, `path` / `frontend_path`, `jobs` (commands, crons, memory, timeouts), `secrets`, `database`, `bucket`, `queue`, and `alerts`.
3. Validate `service.yaml`, generate `infra/` and the workflows (`plan.yml`, `deploy-staging.yml`, `deploy-production.yml`), and generate the declarative Terraform 1.9+ import blocks:
   ```bash
   python3 "$tmpdir/sdlc/scripts/sdlc.py" check service.yaml
   python3 "$tmpdir/sdlc/scripts/sdlc.py" sync-infra service.yaml .
   python3 "$tmpdir/sdlc/scripts/sdlc.py" discover-infra . --write-imports service.yaml
   python3 "$tmpdir/sdlc/scripts/sdlc.py" status . --table
   rm -rf "$tmpdir"
   ```
4. For resources the developer confirmed already exist in `prod_project`, copy the matching `import {}` blocks from `infra/imports.tf.example` into `infra/imports.tf` (removing any block for a resource that does not exist yet).

## 4. Review parity and rehearse the complete release

Follow [legacy adoption](https://github.com/opptra/sdlc-resources/blob/main/docs/infra-handoff.md#adopt-a-live-production-app). Start with the union of read-only live production inventory, the legacy release entry points and scripts they call, and the proposed Terraform and workflows. Record each item in `docs/terraform-adoption.json`. Cover workloads, triggers, runtime settings, identities and permissions, secret references, data, and release sequencing. Record owner, disposition, and verification evidence. Record verified absence explicitly and surface access gaps. Keep secret payloads out of the report. Have the migration PR reviewer resolve gaps and approve intentional differences.

After generating the initial Terraform and imports, set `infra_management: adoption` and prepare the pinned caller using `odlc setup-promotion service.yaml . --workflow-ref <published-sha> --upgrade`. This preserves Terraform edits during rehearsal and keeps the replacement's production jobs disabled. Leave the legacy production writer active during the rehearsal. On the proposed staging workflow, exercise every required release step and verify workload, trigger, runtime, IAM, secret and data behavior. When applicable, show backup before migration, migration before deployment, and candidate health before traffic switch. Exercise failure paths that should stop a traffic switch. A successful plan alone is insufficient.

Record the successful staging push run ID, commit, and per-item evidence. Change the marker to `app-owned` in the handoff PR, and run `odlc adoption-check --repo <owner/repository>`. The generated caller also verifies the evidence on the handoff PR and on the first production promotion. If the release tree changed, repeat the rehearsal. Preserve existing Terraform state keys and addresses.

## 5. Cut over production

Use the exact live image for the first production import plan. Review expected imports and references with zero resource updates, creates, replacements, or deletes. At cutover, suspend the legacy production writer, merge the reviewed promotion, and verify the application and a clean follow-up plan. Retire the old deploy path and remove the temporary adoption image input. Routine changes use the owning Terraform and workflow files and standard release checks.

---
name: align-app
description: Compares the open repository with the Opptra standard, recommends what can be added now, and researches later changes without applying them. Use when a developer asks to align, migrate, or update an existing app to the SDLC standard.
---

# Align an existing app

Run this inside the repository the developer has open. Do not create a new repository. Do not delete a deploy script, move a host, or import Terraform in this turn.

Before you edit any file, show the two sections below and wait. Apply only the **Add now** lines the developer accepts. Before a commit or a push, show the message, the files, the branch, and the pull request body, and wait. Do not invent a Linear ticket id. If they want a pull request and Linear is not connected, stop and ask them to connect it.

## Read the standard

Clone `main` of the library into a temporary directory and delete it before you finish:

```bash
tmpdir=$(mktemp -d)
git clone --depth 1 --branch main https://github.com/opptra/sdlc-resources.git "$tmpdir/sdlc"
```

Read `$tmpdir/sdlc/docs/align.md`, `$tmpdir/sdlc/mapping.yaml`, and `$tmpdir/sdlc/service.schema.json`.

## Read this repository

Look for a Dockerfile, `pyproject.toml`, `package.json`, `frontend/`, `deploy.sh`, `cloudbuild.yaml`, `vercel.json`, `.github/workflows`, Apps Script or clasp files, and any script that runs `gcloud` against a production project.

Propose a `service.yaml`: `name`, `purpose`, `prod_project`, `region`, and `components`. Use only `cloud-run-service`, `cloud-run-job`, `vm-worker`, or `config-only`. A page plus an API is `ui` and `api`. A scheduled or queued Python program is `job`. A browser or long-lived process is `worker`. No service is `config`.

If the repo is Apps Script, say it is unsupported and stop. Do not change files.

## Report

### Add now

List the lines from **Add now** in `docs/align.md` that this repo still needs. For each line, say why it fits and which files you would write.

Do not skip `AGENTS.md`, `CLAUDE.md`, or `.cursor/rules` because the file exists. Compare them with `$tmpdir/sdlc/rules/source/always.md`. Quote the missing sentences: commit format, Linear link, confirmations, feature-or-bug choice, and OpenSpec. Recommend replacing the stale files.

Skip the README line only when it already has the purpose, the local run commands for the parts that exist, and the deploy steps.

### Later

For each matching item under **Later** in `docs/align.md`, cite the files you found, say what the standard would do, and end with the recommendation from that file. If an item does not match, omit it.

Wait for the developer to choose which **Add now** lines to apply.

## Apply

Write only the accepted lines.

- `service.yaml` at the repo root, using the facts you proposed.
- `AGENTS.md`, `CLAUDE.md`, and `.cursor/rules` from `$tmpdir/sdlc/rules/source/` for the parts this repo has. Include `always`. Include `python`, `react`, `terraform`, `job`, `worker`, or `config` only when that part is present. Replace stale copies when the developer accepts this line. Stamp `<!-- sdlc-rules-version: 1 -->` at the top of `AGENTS.md` and `CLAUDE.md`.
- `README.md` with the purpose, local run commands for the parts that exist, and the deploy steps from `docs/align.md`. Replace a README that is missing those sections when the developer accepts this line.
- A `.github/workflows/ci.yml` that runs on `pull_request` only and calls `opptra/sdlc-resources` at `main`: `python-ci.yml` when Python is present, `frontend-ci.yml` when a Vite or React UI is present, `config-ci.yml` when nothing runs. Keep any existing workflow files.
- Create `staging` and `production` from `main` when those branches are missing. Do not protect `staging`.

Do not remove or rewrite the current deploy path. Do not start a **Later** item. If the developer asks for one, stop and treat that request as a separate feature, with the feature skill.

Delete the temporary clone when the report is done, or when you stop.

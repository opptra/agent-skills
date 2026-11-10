---
name: session
description: Shared pins, resume, and feature depth read by the Opptra route skills. Use only when one of those skills says to read this file.
disable-model-invocation: true
---

# Session

## Skill freshness

At the start of a user request that invokes an Opptra skill, run the shared check using the checkout containing that skill:

```bash
python3 "<skill-directory>/../session/scripts/check_skills.py"
```

Resolve `<skill-directory>` from the actual loaded SKILL.md location. The helper checks `origin/main`, fast-forwards a clean `main` checkout when needed, and refreshes the skill links. It checks on every new user request. Reuse the result when the router invokes another skill or reads a shared reference during the same request.

On `current`, proceed. On `updated`, reread the invoked SKILL.md and any shared instructions, and then proceed. Report `local-development` briefly and use the local instructions for skill development. Report `unverified` when offline or unable to access GitHub and proceed with the installed version. On `busy`, recheck after the other update finishes. On `relink-required`, run `install.sh --skills-only` from that checkout before continuing. A `managed-install` uses the host's plugin update mechanism.

This check updates the skills checkout and links only. Generator commits and app workflow refs follow their own explicit upgrade process. Print the actual skills commit in the route banner. A version check is an instruction the agent executes, so installations need this preflight once before they can check themselves.

## Pins

When you print a route banner, add two lines:

- `Skills:` the short commit of the checkout that contains this skill. From that repository run `git rev-parse --short HEAD`. If that fails, print `Skills: unknown`.
- `Generator:` the short commit of the `opptra/sdlc-resources` clone for this run (`git -C "$tmpdir/sdlc" rev-parse --short HEAD`). Before that clone exists, print `Generator: pending`. After a phase, `.sdlc/state.yaml` field `generator_sha` is the full commit. Print its first 12 characters.

## Generator CLI (`odlc`) & Checkout

When `~/.local/bin/odlc` is installed (via `~/agent-skills/install.sh`), the agent invokes it directly to reuse the cached generator without repeating checkout orchestration. Developers describe their task in chat; do not ask them to run these commands manually when you can run them. Preserve the route's approval gates. Agent commands:

- `odlc next [dir] [--json]`
- `odlc doctor [--fix]`
- `odlc check [service.yaml]`
- `odlc status [dir] [--table|--json|--check]`
- `odlc discover [dir] [--table|--json|--propose-manifest|--write-imports <service.yaml>]`
- `odlc sync [service.yaml] [dest] [--ci-only] [--upgrade]`
- `odlc secrets [dir] [--env staging|prod] [--json]`
- `odlc <phase> <service.yaml> [dest]` (`init-runtime`, `add-data`, `add-tests`, `sync-infra`, `set-github-repo`)

When `odlc` is unavailable, use the checkout below and invoke `python3 "$tmpdir/sdlc/scripts/odlc.py"`. The checkout uses the local bare cache at `~/.cache/opptra/sdlc-resources.git` (or `OPPTRA_SDLC_PATH` when set for local generator development) so generator checkouts take `<100ms` and work offline. It fetches from GitHub only when the cache is missing, the recorded `generator_sha` is not in the cache, or `UPGRADE_GENERATOR=1`.

```bash
tmpdir=$(mktemp -d)
repo="$tmpdir/sdlc"
cache="${HOME}/.cache/opptra/sdlc-resources.git"
sha=""
if [ -f .sdlc/state.yaml ]; then
  sha=$(python3 -c "import pathlib,re; t=pathlib.Path('.sdlc/state.yaml').read_text(); m=re.search(r'(?m)^generator_sha:\s*(\S+)', t); print(m.group(1) if m else '')")
fi
if [ -n "${OPPTRA_SDLC_PATH:-}" ] && [ -d "${OPPTRA_SDLC_PATH}" ]; then
  cp -R "${OPPTRA_SDLC_PATH}" "$repo"
else
  mkdir -p "$(dirname "$cache")"
  if [ ! -d "$cache" ]; then
    git clone --bare https://github.com/opptra/sdlc-resources.git "$cache"
  elif [ -z "$sha" ] || [ "${UPGRADE_GENERATOR:-}" = "1" ] || ! git -C "$cache" cat-file -e "${sha}^{commit}" 2>/dev/null; then
    git -C "$cache" fetch --prune origin "+refs/heads/*:refs/heads/*" || true
  fi
  git clone --shared "$cache" "$repo"
  if [ -n "$sha" ] && [ "${UPGRADE_GENERATOR:-}" != "1" ] && git -C "$repo" cat-file -e "${sha}^{commit}" 2>/dev/null; then
    git -C "$repo" checkout --detach "$sha"
  else
    git -C "$repo" checkout --detach refs/heads/main 2>/dev/null || git -C "$repo" checkout --detach HEAD
  fi
fi
```

Do not leave that checkout on the machine after the phase finishes. `rm -rf "$tmpdir"`.

## OpenSpec pin

Read `OPENSPEC_VERSION` from `opptra/pins.env` in the agent-skills checkout that contains this skill. From `opptra/skills/<name>/` that file is `../../pins.env`. Install that version. Do not pass `@latest`.

```bash
set -a
source ../../pins.env
set +a
npm install -g "@fission-ai/openspec@${OPENSPEC_VERSION}"
openspec init --tools cursor,claude
```

Run the install when `openspec --version` is missing or is not `${OPENSPEC_VERSION}`. Source `opptra/pins.env` from the agent-skills checkout. Do not source a `pins.env` inside the app.

## Ship card

After a feature or bug pull request into `main` is open, print this and stop. Substitute the real branch name. Do not run the push, and do not open the production pull request, unless the developer asks.

```text
Ship card
main does not deploy.
Check active staging runs: gh run list --branch staging --limit 1
Try staging: git push --force-with-lease origin <branch>:staging
Do not merge main into staging.
When staging looks right, open a pull request from main into production. That merge deploys production.
```

On a bug, add this line under the card:

```text
Rollback is a revert on main, not an older image. Push the revert branch to staging if you need to see it, then open main into production.
```

## Find the owner of a deployment setting

Read the root `service.yaml`, then `AGENTS.md` and its Product contract. Use `odlc status --json` to find `infra_management`, `terraform_roots`, and `promotion_workflow`. Inspect the actual workflow callers under `.github/workflows/`, including custom callers, and follow their manifest and component paths. A missing ownership field means generator ownership.

| Change | App-owned location |
|---|---|
| Resources, IAM, schedules, runtime values, and Secret Manager references | `infra/` or `<component>/infra/` and the environment inputs it reads. Trace module calls to the owning resource. |
| When deployment runs, Docker paths, Terraform backend locations, or release hooks | The active caller in `.github/workflows/`, usually `promotion.yml`. Follow its `uses:` ref to inspect the shared implementation. |
| App metadata or inputs consumed by tooling | The root or component `service.yaml` named by the caller. Search for readers before moving a field. |
| Secret payloads | Secret Manager in the relevant environment. In `.env.example`, list variable names with placeholders. |

On an app-owned repo, skip bootstrap phases and use `odlc sync` only to refresh rules. If the recorded generator predates handoff, use the updated CLI with `odlc sync --upgrade` once. Without the updated CLI, verify the generator supports handoff before invoking it on the repo. Treat workflow updates as explicit PRs that preserve the backend bucket, prefix, and Terraform addresses. See [SDLC handoff and promotion](https://github.com/opptra/sdlc-resources/blob/main/docs/infra-handoff.md).

## Resume

`.sdlc/state.yaml` records generator phases. It does not hold a ticket id.

`.sdlc/intent.yaml` records a feature or a bug so a new chat can continue. It is local. The generated `.gitignore` ignores `.sdlc/`.

Read `.sdlc/intent.yaml` before asking the developer to restate a plan. Fields:

```yaml
route: feature
depth: standard
ticket: ABC-123
branch: feat/ABC-123-slug
infra_branch: infra/ABC-123-slug
plan_approved: true
next_step: openspec
summary: One sentence of the agreed plan.
```

`route` is `feature` or `bug`. `depth` is `express`, `standard`, or `migration` for a feature. A bug omits `depth`. `next_step` is `plan`, `openspec`, `test`, `code`, `ci`, `pr`, `code-stacked-on-infra`, or `wait-for-infra`.

If `plan_approved` is true and `branch` is the current branch, continue at `next_step`. Do not ask for the plan again. If `route` does not match the skill you are running, stop and say so.

For an already-open legacy stack, when `next_step` is `code-stacked-on-infra`, the `infra/<ticket-id>-<slug>` pull request is already open against `main` and the current `feat/` or `fix/` branch is stacked on top of `infra/<ticket-id>-<slug>`. Continue writing and testing product code locally right away; rebase onto `main` once the infra pull request merges. When `next_step` is `wait-for-infra` (used only when the developer explicitly asked to wait), pause until the infra pull request has merged.

When the developer approves the plan, write this file before product code. Update `next_step` as each stage finishes.

## Depth

Use this only for a feature.

- `express`: the developer says the change is one file, or the agreed plan touches one existing behavior and adds no workflow. Skip the OpenSpec. Write the test and the code. Still run hooks and open one pull request.
- `standard`: the default. Write or update the OpenSpec before product code.
- `migration`: a local plan such as `MIGRATION_PLAN.md` already decided the shape, or the developer says this is a port or a reconcile. Do not re-ask decisions that plan already fixed. Still write an OpenSpec that lists those decisions as accepted.

If express and standard both fit, ask once.

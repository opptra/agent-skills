---
name: session
description: Shared pins, resume, and feature depth read by the Opptra route skills. Use only when one of those skills says to read this file.
disable-model-invocation: true
---

# Session

## Pins

When you print a route banner, add two lines:

- `Skills:` the short commit of the checkout that contains this skill. From that repository run `git rev-parse --short HEAD`. If that fails, print `Skills: unknown`.
- `Generator:` the short commit of the `opptra/sdlc-resources` clone for this run (`git -C "$tmpdir/sdlc" rev-parse --short HEAD`). Before that clone exists, print `Generator: pending`. After a phase, `.sdlc/state.yaml` field `generator_sha` is the full commit. Print its first 12 characters.

## Generator CLI (`opptra`) & Checkout

When `~/.local/bin/opptra` is installed (via `~/agent-skills/install.sh`), you can run subcommands directly without creating `$tmpdir` manually:
- `opptra next [dir] [--json]`
- `opptra doctor [--fix]`
- `opptra check [service.yaml]`
- `opptra status [dir] [--table|--json|--check]`
- `opptra discover [dir] [--table|--json|--propose-manifest|--write-imports <service.yaml>]`
- `opptra sync [service.yaml] [dest] [--ci-only] [--upgrade]`
- `opptra secrets [dir] [--env staging|prod] [--json]`
- `opptra <phase> <service.yaml> [dest]` (`init-runtime`, `add-data`, `add-tests`, `sync-infra`, `set-github-repo`)

When running `sdlc.py` directly via `$tmpdir/sdlc`, use the local bare cache at `~/.cache/opptra/sdlc-resources.git` (or `OPPTRA_SDLC_PATH` when set for local generator development) so generator checkouts take `<100ms` and work offline. It fetches from GitHub only when the cache is missing, the recorded `generator_sha` is not in the cache, or `UPGRADE_GENERATOR=1`.

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

When `next_step` is `code-stacked-on-infra`, the `infra/<ticket-id>-<slug>` pull request is already open against `main` and the current `feat/` or `fix/` branch is stacked on top of `infra/<ticket-id>-<slug>`. Continue writing and testing product code locally right away; rebase onto `main` once the infra pull request merges. When `next_step` is `wait-for-infra` (used only when the developer explicitly asked to wait), pause until the infra pull request has merged.

When the developer approves the plan, write this file before product code. Update `next_step` as each stage finishes.

## Depth

Use this only for a feature.

- `express`: the developer says the change is one file, or the agreed plan touches one existing behavior and adds no workflow. Skip the OpenSpec. Write the test and the code. Still run hooks and open one pull request.
- `standard`: the default. Write or update the OpenSpec before product code.
- `migration`: a local plan such as `MIGRATION_PLAN.md` already decided the shape, or the developer says this is a port or a reconcile. Do not re-ask decisions that plan already fixed. Still write an OpenSpec that lists those decisions as accepted.

If express and standard both fit, ask once.

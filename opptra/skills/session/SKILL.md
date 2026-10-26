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

## Resume

`.sdlc/state.yaml` records generator phases. It does not hold a ticket id.

`.sdlc/intent.yaml` records a feature or a bug so a new chat can continue. It is local. The generated `.gitignore` ignores `.sdlc/`.

Read `.sdlc/intent.yaml` before asking the developer to restate a plan. Fields:

```yaml
route: feature
depth: standard
ticket: ABC-123
branch: feat/ABC-123-slug
plan_approved: true
next_step: openspec
summary: One sentence of the agreed plan.
```

`route` is `feature` or `bug`. `depth` is `express`, `standard`, or `migration` for a feature. A bug omits `depth`. `next_step` is `plan`, `openspec`, `test`, `code`, `ci`, or `pr`.

If `plan_approved` is true and `branch` is the current branch, continue at `next_step`. Do not ask for the plan again. If `route` does not match the skill you are running, stop and say so.

When the developer approves the plan, write this file before product code. Update `next_step` as each stage finishes.

## Depth

Use this only for a feature.

- `express`: the developer says the change is one file, or the agreed plan touches one existing behavior and adds no workflow. Skip the OpenSpec. Write the test and the code. Still run hooks and open one pull request.
- `standard`: the default. Write or update the OpenSpec before product code.
- `migration`: a local plan such as `MIGRATION_PLAN.md` already decided the shape, or the developer says this is a port or a reconcile. Do not re-ask decisions that plan already fixed. Still write an OpenSpec that lists those decisions as accepted.

If express and standard both fit, ask once.

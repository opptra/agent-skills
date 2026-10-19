---
name: create-app
description: Scaffolds a new Opptra app by recommending an archetype and auth, writing service.yaml, and running the generator from opptra/sdlc-resources. Use when a developer asks to create, scaffold, or set up a new app or repository.
---

# Create an app

You fill in facts. The generator in `opptra/sdlc-resources` decides the files, CI, deploy, and rules. Do not invent a pipeline, a framework, or an archetype that is not listed below.

Do not create the GitHub repository. Do not run `bind-repo.sh` or `protect-branches.sh`. Do not leave a checkout of `opptra/sdlc-resources` on the machine.

Apps Script is not a choice. If the description only fits Apps Script, say so and stop. If no archetype fits, name the closest one and stop.

## Questions

Ask what the app is for. Then ask, in order, and stop at the first match for each runnable part:

1. Config, prompts, or skills only, with no running service? Part `config`, archetype `config-only`, auth `none`.
2. Work on a schedule or a queue, with no page a person waits on? Part `job`, archetype `cloud-run-job`, auth `none`.
3. A real browser, a long-lived process, or a disk Cloud Run will not keep? Part `worker`, archetype `vm-worker`, auth `none`.
4. A page or an API a person or another service calls? Part `api`, and `ui` when there is a page. Archetype `cloud-run-service`.

A console plus a scraper is two components in one `service.yaml`.

Auth is only for `cloud-run-service`:

- Opptra staff, Google account, no separate password: `iap`
- The app signs users in itself: `app-login`
- Anyone on the internet, no account: `public`

Also collect the app name, the production GCP project, and the region. The region default is `asia-south1`. The app name matches `^[a-z][a-z0-9-]{1,48}$`. Each component name matches `^[a-z][a-z0-9-]{1,40}$`.

## Recommendation

Say one sentence that names the components, the archetype, and the auth, and why. Wait until the developer agrees. Do not write files before that.

## Write

Write this shape. `cloud-run-service` requires `api`. Add `ui` only when there is a page. A job, a worker, and config are separate components.

```yaml
name: inventory
prod_project: opptra-applications
region: asia-south1
components:
  - name: console
    archetype: cloud-run-service
    auth: iap
    parts: [ui, api]
```

Clone `main` of the library, generate into the current directory when it is empty, otherwise into `./<name>`, then delete the clone:

```bash
tmpdir=$(mktemp -d)
git clone --depth 1 --branch main https://github.com/opptra/sdlc-resources.git "$tmpdir/sdlc"
python3 "$tmpdir/sdlc/scripts/check_manifest.py" "$tmpdir/service.yaml"
python3 "$tmpdir/sdlc/scripts/generate.py" "$tmpdir/service.yaml" "<empty-directory>"
rm -rf "$tmpdir"
```

The generated tests already pass. A failing test for a Linear issue belongs on a feature branch, not in this scaffold.

Tell the developer to create the empty `opptra/<name>` repository, copy this directory in, and push:

```bash
git init
git add .
git commit -m "feat: scaffold"
git branch -M main
git remote add origin git@github.com:opptra/<name>.git
git push -u origin main
git branch staging
git branch production
git push -u origin staging
git push -u origin production
```

Then they ask a platform owner to run `scripts/protect-branches.sh` and `scripts/bind-repo.sh` from `opptra/sdlc-resources`. Nothing has deployed yet.

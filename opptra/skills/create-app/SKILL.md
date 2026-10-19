---
name: create-app
description: Scaffolds a new Opptra app by understanding a plain description, recommending an archetype and auth, writing service.yaml, and running the generator from opptra/sdlc-resources. Use when a developer asks to create, scaffold, or set up a new app or repository.
---

# Create an app

You fill in facts. The generator in `opptra/sdlc-resources` decides the files, CI, deploy, and rules. Do not invent a pipeline, a framework, or an archetype that is not listed below.

Do not create the GitHub repository. Do not run `bind-repo.sh` or `protect-branches.sh`. Do not leave a checkout of `opptra/sdlc-resources` on the machine.

Apps Script is not a choice. If the description only fits Apps Script, say so and stop. If no archetype fits, name the closest one and stop.

## Understand

Ask what they want to build, in their words: what it does, and who uses it. Do not open with archetype names, part names, or auth codes. The developer may not know those words.

Map what they said onto the choices below. Pick the recommended way yourself. You may recommend more than one component when the app needs it. You may add a recommendation they did not ask for when it fits what they described. Say why, in plain language, and put the technical value in parentheses. Do not invent an archetype that is not listed here.

If you are not sure what is being created, ask more questions until you are. Ask one thing at a time, in everyday language, using the plain wording below. Stop asking when the parts, the archetype, and the auth are clear.

### What runs

- Nothing runs. It is only settings, prompts, or skills. Part `config`, archetype `config-only`, auth `none`.
- It does work on a schedule, or when a message arrives, and nobody is waiting on a page. Part `job`, archetype `cloud-run-job`, auth `none`.
- It needs a real web browser, it has to stay running for a long time, or it saves files on a disk that a normal web app will not keep. Part `worker`, archetype `vm-worker`, auth `none`.
- People open a page in a browser, or another system calls it and gets an answer. Part `api`, and `ui` when there is a page. Archetype `cloud-run-service`.

A page people use, plus a separate job that collects data, is two components in one `service.yaml`.

### Who can open a page or call the app

Only a `cloud-run-service` has auth. Ask this only when you cannot tell from what they already said:

- Only people who work at Opptra, using the Google account they already have: `iap`
- People sign in with an account the app itself creates: `app-login`
- Anyone on the internet, and they do not need an account: `public`

### Names

Also collect the app name, the production GCP project, and the region. Ask in plain language: what to call the app, which production project pays for it, and where it should run. The region default is `asia-south1`. Offer that default instead of making them invent a region.

The app name matches `^[a-z][a-z0-9-]{1,48}$`. Each component name matches `^[a-z][a-z0-9-]{1,40}$`. If their name does not match, suggest a short lowercase name with hyphens and use that after they agree.

## Recommendation

Say what you will create in a few plain sentences: what it is, who can use it, and why this shape fits. Put each component, archetype, and auth in parentheses. Mention any extra recommendation the same way. Wait until the developer agrees. Do not write files before that.

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

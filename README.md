# opptra/agent-skills

The skills every Opptra developer uses to create an app, implement a feature, fix a bug, align an existing app, add a skill, change a skill, and fetch the latest skills.

| Skill | When |
|---|---|
| `create-app` | A new repository. It figures out the archetype and auth from a plain description, asks in everyday language when that is unclear, writes `service.yaml`, clones `main` of `opptra/sdlc-resources`, runs the generator, and deletes the clone. |
| `feature` | A Linear feature. Branch `feat/<ticket>-<slug>` from `main`, OpenSpec, one pull request into `main`. |
| `bug` | A Linear bug. A failing test, then the fix, one pull request into `main`. A design choice uses `feature`. |
| `align-app` | An existing repository. It recommends what can be added now and researches later changes. It applies only the lines the developer accepts. |
| `add-skill` | A new team skill. It writes `opptra/skills/<name>/SKILL.md` and opens a pull request into `main`. |
| `modify-skill` | A change to an existing team skill. It edits that skill from the developer's instructions and opens a pull request into `main`. |
| `fetch-skill` | Fetch `main` of this repository and link every skill into Cursor, Claude Code, and Codex. |

`opptra/sdlc-resources` stays the library: the mapping, the skeletons, the generator, and the workflows. People do not keep that repo checked out.

`main` does not deploy. A push to `staging` deploys staging. A merge into `production` deploys production.

## Cursor

Add this repository as a team marketplace and set the `opptra` plugin to Required. Cursor installs the skills for everyone on the team.

## First install for Claude Code, Codex, and a local Cursor copy

```bash
git clone https://github.com/opptra/agent-skills.git ~/agent-skills
mkdir -p ~/.claude/skills ~/.codex/skills ~/.cursor/skills
for dir in ~/agent-skills/opptra/skills/*/; do
  name=$(basename "$dir")
  ln -sfn "$dir" ~/.claude/skills/"$name"
  ln -sfn "$dir" ~/.codex/skills/"$name"
  ln -sfn "$dir" ~/.cursor/skills/"$name"
done
```

After that, ask the agent to fetch Opptra skills. The `fetch-skill` skill pulls `main` and refreshes those links, including skills added since the clone.

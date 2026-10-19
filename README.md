# opptra/agent-skills

The skills every Opptra developer uses to create an app, implement a feature, fix a bug, add a skill, and pull the latest skills.

| Skill | When |
|---|---|
| `create-app` | A new repository. It recommends the archetype and auth, writes `service.yaml`, clones `main` of `opptra/sdlc-resources`, runs the generator, and deletes the clone. |
| `feature` | A Linear feature. Branch `feat/<ticket>-<slug>` from `main`, OpenSpec, one pull request into `main`. |
| `bug` | A Linear bug. A failing test, then the fix, one pull request into `main`. A design choice uses `feature`. |
| `add-skill` | A new team skill. It writes `opptra/skills/<name>/SKILL.md` and opens a pull request into `main`. |
| `update-skills` | Pull `main` of this repository and link every skill into Cursor, Claude Code, and Codex. |

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

After that, ask the agent to update Opptra skills. The `update-skills` skill pulls `main` and refreshes those links, including skills added since the clone.

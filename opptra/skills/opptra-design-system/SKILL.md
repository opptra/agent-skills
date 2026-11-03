---
name: opptra-design-system
description: Applies Opptra design system 0.1.0 — brand language, semantic tokens, and 27 component contracts — to mockups, wireframes, prototypes, HTML dashboards, and product UI. Use when someone asks to mock up a screen, change a page, design a dashboard, review UI, or make product UI look like Opptra. For presentations, documents, emails, and charts, use opptra-branding instead.
---

# Opptra design system

Use published reference **0.1.0**. Follow the user's scope. Do not create a GitHub app, run `create-app`, or ask for GCP, Linear, or `service.yaml`.

Canonical files (fetch these; they work without repository access):

- https://opptra.github.io/opptra-design-system/manifest.json
- https://opptra.github.io/opptra-design-system/SKILL.md
- https://opptra.github.io/opptra-design-system/guidelines.md
- https://opptra.github.io/opptra-design-system/tokens.json
- https://opptra.github.io/opptra-design-system/tokens.css
- Gallery: https://opptra.github.io/opptra-design-system/

If a fetch fails, apply the rules below and say which files you could not load.

## Core rules

- Spectral for headings. Raleway for body and controls. Georgia / Segoe UI are fallbacks.
- Navy `#131A48` for structure. Orange `#FF5800` for emphasis. Soft yellow `#FFFCE8` for callouts. Canvas `#FAFAF7`.
- Orange actions use navy labels, not white (white on orange is 3.16:1). Small accent links use `#B53F00`.
- Use semantic token names (`--color-action-primary`, `--color-link`), not copied hex, when CSS is available.
- Reuse a component family (C01–C27) before adding a pattern.
- Status needs words and a meaning. Orange is not a generic success or warning color.
- Zero, missing, stale, and restricted data are different states. Name the source and time. Label invented examples as synthetic.
- Cover loading, empty, error, permission, and success when the screen has them.
- Logo: `https://cdn.prod.website-files.com/6933cd7135f6e590ffef0761/6937f6a9040488e80b8e30b0_logo.svg`. Do not redraw or recolor it.

## Apply

1. Read `manifest.json` and `SKILL.md`, then the component sections you will use in `guidelines.md`.
2. Build the user's actual task. Do not reproduce the gallery's synthetic workspace.
3. For HTML, carry `tokens.css` into the artifact. For React in an Opptra app, follow the compiled `react` rule and the vendored `tokens.css`.
4. For a deck, document, email, or chart, stop and follow `opptra-branding`.

## Handoff

State version 0.1.0, the families and tokens reused, and any extension with its reason. This skill does not claim accessibility conformance or stakeholder approval.

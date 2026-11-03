---
name: opptra-branding
description: Applies Opptra brand identity to presentations, documents, emails, charts, and other non-UI assets. Use when someone asks for a deck, slide, memo, email, summary visual, or chart. For web UI, React apps, wireframes, HTML dashboards, or product screens, use opptra-design-system instead.
---

# Opptra branding

Use this skill for presentations, documents, emails, and charts. For product UI, mockups, wireframes, or HTML dashboards, read `../opptra-design-system/SKILL.md` and stop here.

Colors and type match Opptra design system 0.1.0. Do not invent a second palette.

## Colors

| Role | Hex | Use |
|---|---|---|
| Navy | `#131A48` | Structure, titles, dark surfaces, primary fills |
| Orange | `#FF5800` | Emphasis, one highlight series on a chart, large accents |
| Orange hover | `#FF8C4F` | Hover on orange |
| Soft yellow | `#FFFCE8` | Callout boxes, section tint |
| Canvas | `#FAFAF7` | Slide or page background |
| Body text | `#5A5A5A` | Paragraphs |
| White | `#FFFFFF` | Text on navy |
| Link / small orange text | `#B53F00` | Small accent text on white |

Rules:

- Navy plus orange is the pairing. Navy structures. Orange emphasizes.
- Orange fills use navy text, not white (white on orange fails ordinary-text contrast).
- Small orange text or links on white use `#B53F00`, not `#FF5800`.
- Do not use orange as a large background.
- Charts: navy for the base series, orange for the one series that matters. Soft yellow and greys for the rest. No rainbow palettes.
- `#CECECE` is a decorative divider only.

## Type

| Role | Font | Fallback |
|---|---|---|
| Headings | Spectral 300 / 600 / 700 | Georgia |
| Body and labels | Raleway 400 / 500 / 600 | Segoe UI, Arial |

Headings stay Spectral. Body stays Raleway. On a machine without those fonts, use the fallbacks and say so.

## Voice

Take ownership: name the work, the owner, and the next step. Make it concrete: outcome first, then evidence. Keep people moving: short language, a specific recovery when something fails.

## Logo

```
https://cdn.prod.website-files.com/6933cd7135f6e590ffef0761/6937f6a9040488e80b8e30b0_logo.svg
```

Use that asset. Do not redraw or recolor it. Keep clear space around it.

## Handoff

State that branding followed design system 0.1.0. If the user then asks for a product screen, switch to `opptra-design-system`.

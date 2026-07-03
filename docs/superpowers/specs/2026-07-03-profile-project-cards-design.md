# Profile Project Cards Design

## Overview
Add a **Team Projects** section to `README.md` that showcases two repositories —
**EmberExchange** and **RedQuorum** — with short animated workflow diagrams and
badges. The new section must match the existing Nord theme and reuse the same
dark-mode pattern already used for the contribution snake.

## Goals
- Surface the two main team projects in the profile README.
- Explain what each project does at a glance via an animated workflow diagram.
- Keep the visual style consistent with the existing Nord palette and dark-mode
  support.
- Avoid heavy demo recordings; use lightweight self-contained SVG animations.

## Non-Goals
- Do not redesign the whole README; only add a new section.
- Do not build a generic generator script yet (manual SVGs are acceptable for two
  projects).
- Do not add live-site links where none exist (RedQuorum has no public demo URL).

## Projects

### EmberExchange
- Repo: https://github.com/LPuehringerStudent/EmberExchange
- Live: https://emberexchange.xyz
- Workflow steps:
  1. Browse markets
  2. Place order
  3. Trade executes
  4. Portfolio updates

### RedQuorum
- Repo: https://github.com/LPuehringerStudent/RedQuorum
- Live: none
- Workflow steps:
  1. Scan
  2. Analyze
  3. Report

## Design

### Animation style
Each project is represented by a self-contained SVG that loops through its
workflow steps. Each step displays:
- a simple geometric icon,
- a short label below the icon,
- a connecting arrow to the next step.

The active step is highlighted; inactive steps are dimmed. The animation is a
CSS keyframe loop: step 1 appears, holds, step 2 appears, holds, and so on, then
restarts.

### Files
Store the SVGs under `assets/projects/` on the `main` branch:

```
assets/projects/
├── emberexchange-light.svg
├── emberexchange-dark.svg
├── redquorum-light.svg
└── redquorum-dark.svg
```

Two files per project mirror the existing snake dark-mode pattern and avoid
relying on `@media` queries inside a single SVG, which can behave inconsistently
when served through GitHub’s image proxy.

### Theming
Use the same Nord palette as the rest of the profile:

| Element | Light | Dark |
|---------|-------|------|
| Background | `#ECEFF4` | `#2E3440` |
| Text | `#2E3440` | `#D8DEE9` |
| Accent | `#88C0D0` | `#88C0D0` |
| Muted | `#4C566A` | `#81A1C1` |

### README integration
Insert a new `## Team Projects` section in `README.md`. For each project:
- h3 title,
- `<picture>` element selecting the light/dark SVG,
- one-line description,
- badges row.

Example structure:

```html
<div align="center">
  <h3>EmberExchange</h3>
  <picture>
    <source media="(prefers-color-scheme: dark)"
            srcset="https://raw.githubusercontent.com/LPuehringerStudent/LPuehringerStudent/main/assets/projects/emberexchange-dark.svg">
    <source media="(prefers-color-scheme: light)"
            srcset="https://raw.githubusercontent.com/LPuehringerStudent/LPuehringerStudent/main/assets/projects/emberexchange-light.svg">
    <img alt="EmberExchange workflow" src="...emberexchange-light.svg">
  </picture>
  <p><i>Short description here.</i></p>
  <!-- badges -->
</div>
```

### Badges
Use shields.io badges in `flat-square` style with Nord colors.

For EmberExchange:
- `View Code` → repo
- `Live Site` → emberexchange.xyz
- `Tech Stack` → relevant stack badge(s)

For RedQuorum:
- `View Code` → repo
- `Tech Stack` → relevant stack badge(s)

Badges should share the same label color (`#2E3440`) and use Nord accent colors
for the message side.

## Acceptance Criteria
- [ ] `assets/projects/` contains four SVG files.
- [ ] Each SVG animates through the agreed workflow steps in a loop.
- [ ] `README.md` contains a `## Team Projects` section with both projects.
- [ ] Each project card uses `<picture>` to switch between light and dark SVGs.
- [ ] Badges are consistent in style and color.
- [ ] The section renders correctly in both GitHub light and dark themes.

## Maintenance
If a project’s workflow changes, edit the corresponding SVG files directly. If a
third or fourth project is added later, consider building a small generator
script to keep the SVGs maintainable.

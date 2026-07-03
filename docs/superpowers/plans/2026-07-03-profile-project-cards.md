# Profile Project Cards Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a "Team Projects" section to the GitHub profile README with animated, dark-mode-aware workflow SVGs for EmberExchange and RedQuorum.

**Architecture:** A small Python renderer script generates the four SVG files from a per-project config (steps + Nord color palette). The README uses `<picture>` to swap light/dark SVGs and adds shields.io badges for each project.

**Tech Stack:** Python 3, SVG, Markdown, shields.io, GitHub Actions (existing).

---

### Task 1: Create the SVG renderer script

**Files:**
- Create: `scripts/render-project-diagrams.py`

- [ ] **Step 1: Write the script**

  ```python
  #!/usr/bin/env python3
  """Render animated workflow SVGs for GitHub profile project cards."""
  from pathlib import Path

  PROJECTS = [
      {
          "prefix": "emberexchange",
          "steps": ["Browse markets", "Place order", "Trade executes", "Portfolio updates"],
          "colors": {
              "light": {"bg": "#ECEFF4", "text": "#2E3440", "muted": "#4C566A", "accent": "#88C0D0"},
              "dark": {"bg": "#2E3440", "text": "#D8DEE9", "muted": "#81A1C1", "accent": "#88C0D0"},
          },
      },
      {
          "prefix": "redquorum",
          "steps": ["Scan", "Analyze", "Report"],
          "colors": {
              "light": {"bg": "#ECEFF4", "text": "#2E3440", "muted": "#4C566A", "accent": "#88C0D0"},
              "dark": {"bg": "#2E3440", "text": "#D8DEE9", "muted": "#81A1C1", "accent": "#88C0D0"},
          },
      },
  ]


  def pct(value: float) -> str:
      return f"{value:.2f}%"


  def render(prefix: str, steps: list[str], palette: dict[str, str]) -> str:
      n = len(steps)
      center_start = 95
      spacing = 160
      margin_right = 65
      width = center_start + (n - 1) * spacing + margin_right
      height = 130
      cy = 55
      radius = 26

      slot = 100.0 / n
      active_end_ratio = 0.80

      keyframes: list[str] = []
      groups: list[str] = []
      arrows: list[str] = []

      for i, label in enumerate(steps, start=1):
          start = i * slot - slot
          active_end = start + slot * active_end_ratio
          inactive_start = start + slot

          keyframes.extend(
              [
                  f".g{i} .step {{ animation: s{i}s 10s infinite; }}",
                  f".g{i} .num {{ animation: s{i}n 10s infinite; }}",
                  f".g{i} .label {{ animation: s{i}l 10s infinite; }}",
                  f"@keyframes s{i}s {{ "
                  f"0%,{pct(start)},{pct(active_end)},{pct(inactive_start)},100%{{fill:{palette['bg']};stroke:{palette['muted']}}} "
                  f"{pct(start)},{pct(active_end)}{{fill:{palette['accent']};stroke:{palette['accent']}}} "
                  "}",
                  f"@keyframes s{i}n {{ "
                  f"0%,{pct(start)},{pct(active_end)},{pct(inactive_start)},100%{{fill:{palette['muted']}}} "
                  f"{pct(start)},{pct(active_end)}{{fill:{palette['bg']}}} "
                  "}",
                  f"@keyframes s{i}l {{ "
                  f"0%,{pct(start)},{pct(active_end)},{pct(inactive_start)},100%{{fill:{palette['muted']}}} "
                  f"{pct(start)},{pct(active_end)}{{fill:{palette['text']}}} "
                  "}",
              ]
          )

          cx = center_start + i * spacing - spacing
          groups.append(
              f'<g class="g{i}" transform="translate({cx},{cy})">\\n'
              f'    <circle class="step" r="{radius}"/>\\n'
              f'    <text class="num" y="1">{i}</text>\\n'
              f'    <text class="label" y="50">{label}</text>\\n'
              f"</g>"
          )

          if i < n:
              next_cx = center_start + (i + 1) * spacing - spacing
              x1 = cx + radius
              x2 = next_cx - radius
              arrows.append(f'<line class="arrow" x1="{x1}" y1="{cy}" x2="{x2}" y2="{cy}"/>')

      keyframes_css = "\\n    ".join(keyframes)
      groups_svg = "\\n  ".join(groups)
      arrows_svg = "\\n  ".join(arrows)

      return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <style>
      .bg {{ fill:{palette['bg']}; }}
      text {{ font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; text-anchor:middle; }}
      .step {{ fill:{palette['bg']}; stroke:{palette['muted']}; stroke-width:3; }}
      .num {{ font-size:18px; font-weight:700; fill:{palette['muted']}; dominant-baseline:central; }}
      .label {{ font-size:13px; font-weight:600; fill:{palette['muted']}; }}
      .arrow {{ stroke:{palette['muted']}; stroke-width:2; fill:none; }}
      {keyframes_css}
    </style>
    <rect width="100%" height="100%" class="bg"/>
    {groups_svg}
    {arrows_svg}
  </svg>
  '''


  def main() -> None:
      out_dir = Path(__file__).resolve().parents[1] / "assets" / "projects"
      out_dir.mkdir(parents=True, exist_ok=True)

      for project in PROJECTS:
          for theme, palette in project["colors"].items():
              filename = f"{project['prefix']}-{theme}.svg"
              svg = render(project["prefix"], project["steps"], palette)
              (out_dir / filename).write_text(svg, encoding="utf-8")
              print(f"Wrote {filename}")


  if __name__ == "__main__":
      main()
  ```

- [ ] **Step 2: Make it executable**

  ```bash
  chmod +x scripts/render-project-diagrams.py
  ```

- [ ] **Step 3: Commit the script**

  ```bash
  git add scripts/render-project-diagrams.py
  git commit -m "feat: add project workflow SVG renderer"
  ```

### Task 2: Generate the SVG files

**Files:**
- Create: `assets/projects/emberexchange-light.svg`
- Create: `assets/projects/emberexchange-dark.svg`
- Create: `assets/projects/redquorum-light.svg`
- Create: `assets/projects/redquorum-dark.svg`

- [ ] **Step 1: Run the renderer**

  ```bash
  python3 scripts/render-project-diagrams.py
  ```

- [ ] **Step 2: Validate the SVGs**

  ```bash
  python3 - <<'PY'
  import xml.etree.ElementTree as ET
  from pathlib import Path
  for f in Path('assets/projects').glob('*.svg'):
      ET.parse(f)
      print(f"OK {f.name}")
  PY
  ```

  Expected: all four files print `OK`.

- [ ] **Step 3: Commit the generated assets**

  ```bash
  git add assets/projects/
  git commit -m "feat: add animated workflow SVGs for EmberExchange and RedQuorum"
  ```

### Task 3: Add the Team Projects section to the README

**Files:**
- Modify: `README.md` (insert before `## About`)

- [ ] **Step 1: Insert the new section**

  Replace the block immediately before `## About` with:

  ```markdown
  ---

  ## Team Projects

  <div align="center">

    <h3>EmberExchange</h3>

    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/LPuehringerStudent/LPuehringerStudent/main/assets/projects/emberexchange-dark.svg" />
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/LPuehringerStudent/LPuehringerStudent/main/assets/projects/emberexchange-light.svg" />
      <img alt="EmberExchange workflow" src="https://raw.githubusercontent.com/LPuehringerStudent/LPuehringerStudent/main/assets/projects/emberexchange-light.svg" />
    </picture>

    <p><i>Browse markets, place orders, execute trades, and track your portfolio.</i></p>

    <a href="https://emberexchange.xyz">
      <img src="https://img.shields.io/badge/Live_Site-5E81AC?style=flat-square&labelColor=2E3440" alt="Live Site" />
    </a>
    <a href="https://github.com/LPuehringerStudent/EmberExchange">
      <img src="https://img.shields.io/badge/View_Code-88C0D0?style=flat-square&labelColor=2E3440" alt="View Code" />
    </a>

    <br><br>

    <h3>RedQuorum</h3>

    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/LPuehringerStudent/LPuehringerStudent/main/assets/projects/redquorum-dark.svg" />
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/LPuehringerStudent/LPuehringerStudent/main/assets/projects/redquorum-light.svg" />
      <img alt="RedQuorum workflow" src="https://raw.githubusercontent.com/LPuehringerStudent/LPuehringerStudent/main/assets/projects/redquorum-light.svg" />
    </picture>

    <p><i>Run security scans, analyze findings, and generate reports.</i></p>

    <a href="https://github.com/LPuehringerStudent/RedQuorum">
      <img src="https://img.shields.io/badge/View_Code-88C0D0?style=flat-square&labelColor=2E3440" alt="View Code" />
    </a>

  </div>

  ---

  ## About
  ```

- [ ] **Step 2: Commit the README change**

  ```bash
  git add README.md
  git commit -m "feat: add Team Projects section with animated workflow SVGs"
  ```

### Task 4: Push and verify on GitHub

- [ ] **Step 1: Push to main**

  ```bash
  git push origin main
  ```

- [ ] **Step 2: Verify raw SVG URLs load**

  Open each raw SVG URL in a browser and confirm it renders:

  - `https://raw.githubusercontent.com/LPuehringerStudent/LPuehringerStudent/main/assets/projects/emberexchange-light.svg`
  - `https://raw.githubusercontent.com/LPuehringerStudent/LPuehringerStudent/main/assets/projects/emberexchange-dark.svg`
  - `https://raw.githubusercontent.com/LPuehringerStudent/LPuehringerStudent/main/assets/projects/redquorum-light.svg`
  - `https://raw.githubusercontent.com/LPuehringerStudent/LPuehringerStudent/main/assets/projects/redquorum-dark.svg`

- [ ] **Step 3: Check the README on your profile**

  Visit `https://github.com/LPuehringerStudent` in light and dark mode and confirm the Team Projects section appears and switches SVGs.

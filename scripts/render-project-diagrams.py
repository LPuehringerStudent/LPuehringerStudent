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
    active_end_ratio = 0.80  # 80% of the slot is "fully active"

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
            f'<g class="g{i}" transform="translate({cx},{cy})">\n'
            f'    <circle class="step" r="{radius}"/>\n'
            f'    <text class="num" y="1">{i}</text>\n'
            f'    <text class="label" y="50">{label}</text>\n'
            f"</g>"
        )

        if i < n:
            next_cx = center_start + (i + 1) * spacing - spacing
            x1 = cx + radius
            x2 = next_cx - radius
            arrows.append(f'<line class="arrow" x1="{x1}" y1="{cy}" x2="{x2}" y2="{cy}"/>')

    keyframes_css = "\n    ".join(keyframes)
    groups_svg = "\n  ".join(groups)
    arrows_svg = "\n  ".join(arrows)

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

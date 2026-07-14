#!/usr/bin/env python3
"""Render animated workflow SVGs for GitHub profile project cards."""
from pathlib import Path

ICONS = {
    "emberexchange": [
        # Browse markets: line chart
        '<path d="M2 18 L8 12 L14 16 L22 4" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        # Place order: clipboard
        '<rect x="5" y="3" width="14" height="18" rx="2" stroke="currentColor" stroke-width="2" fill="none"/>'
        '<line x1="9" y1="1" x2="15" y2="1" stroke="currentColor" stroke-width="2"/>'
        '<line x1="9" y1="8" x2="15" y2="8" stroke="currentColor" stroke-width="2"/>'
        '<line x1="9" y1="13" x2="15" y2="13" stroke="currentColor" stroke-width="2"/>',
        # Trade executes: opposite arrows
        '<path d="M2 8 L10 8 L8 5 M10 8 L8 11" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M22 16 L14 16 L16 13 M14 16 L16 19" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        # Portfolio updates: bar chart
        '<rect x="3" y="10" width="4" height="12" fill="currentColor"/>'
        '<rect x="10" y="4" width="4" height="18" fill="currentColor"/>'
        '<rect x="17" y="12" width="4" height="10" fill="currentColor"/>',
    ],
    "redquorum": [
        # Scan: target crosshair
        '<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="none"/>'
        '<circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2" fill="none"/>'
        '<line x1="12" y1="1" x2="12" y2="5" stroke="currentColor" stroke-width="2"/>'
        '<line x1="12" y1="19" x2="12" y2="23" stroke="currentColor" stroke-width="2"/>'
        '<line x1="1" y1="12" x2="5" y2="12" stroke="currentColor" stroke-width="2"/>'
        '<line x1="19" y1="12" x2="23" y2="12" stroke="currentColor" stroke-width="2"/>',
        # Analyze: magnifying glass
        '<circle cx="10" cy="10" r="6" stroke="currentColor" stroke-width="2" fill="none"/>'
        '<line x1="14" y1="14" x2="21" y2="21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        # Report: document with checkmark
        '<rect x="5" y="2" width="14" height="20" rx="2" stroke="currentColor" stroke-width="2" fill="none"/>'
        '<line x1="9" y1="8" x2="15" y2="8" stroke="currentColor" stroke-width="2"/>'
        '<line x1="9" y1="13" x2="15" y2="13" stroke="currentColor" stroke-width="2"/>'
        '<path d="M9 17 L11 19 L15 15" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    ],
}

PROJECTS = [
    {
        "prefix": "emberexchange",
        "template": "pipeline-token",
        "steps": ["Browse markets", "Place order", "Trade executes", "Portfolio updates"],
        "colors": {
            "light": {"bg": "#ECEFF4", "text": "#2E3440", "muted": "#4C566A", "accent": "#88C0D0"},
            "dark": {"bg": "#2E3440", "text": "#D8DEE9", "muted": "#81A1C1", "accent": "#88C0D0"},
        },
    },
    {
        "prefix": "redquorum",
        "template": "scanner-beam",
        "steps": ["Scan", "Analyze", "Report"],
        "colors": {
            "light": {"bg": "#ECEFF4", "text": "#2E3440", "muted": "#4C566A", "accent": "#88C0D0"},
            "dark": {"bg": "#2E3440", "text": "#D8DEE9", "muted": "#81A1C1", "accent": "#88C0D0"},
        },
    },
]


def pct(value: float) -> str:
    return f"{value:.2f}%"


def step_keyframes(n: int, i: int, palette: dict[str, str]) -> list[str]:
    """Generate keyframes for a single step's ring, icon, and label."""
    slot = 100.0 / n
    start = i * slot - slot
    active_end = start + slot * 0.80
    inactive_start = start + slot
    idx = i

    return [
        f".g{idx} .step {{ animation: s{idx}s 10s infinite; }}",
        f".g{idx} .icon {{ animation: s{idx}i 10s infinite; }}",
        f".g{idx} .label {{ animation: s{idx}l 10s infinite; }}",
        f"@keyframes s{idx}s {{ "
        f"0%,{pct(start)},{pct(active_end)},{pct(inactive_start)},100%{{fill:{palette['bg']};stroke:{palette['muted']}}} "
        f"{pct(start)},{pct(active_end)}{{fill:{palette['accent']};stroke:{palette['accent']}}} "
        "}",
        f"@keyframes s{idx}i {{ "
        f"0%,{pct(start)},{pct(active_end)},{pct(inactive_start)},100%{{color:{palette['muted']}}} "
        f"{pct(start)},{pct(active_end)}{{color:{palette['bg']}}} "
        "}",
        f"@keyframes s{idx}l {{ "
        f"0%,{pct(start)},{pct(active_end)},{pct(inactive_start)},100%{{fill:{palette['muted']}}} "
        f"{pct(start)},{pct(active_end)}{{fill:{palette['text']}}} "
        "}",
    ]


def render_pipeline_token(prefix: str, steps: list[str], palette: dict[str, str]) -> str:
    """EmberExchange: token moves along the pipeline as steps highlight."""
    n = len(steps)
    center_start = 95
    spacing = 160
    margin_right = 65
    width = center_start + (n - 1) * spacing + margin_right
    height = 130
    cy = 55
    radius = 26

    slot = 100.0 / n

    keyframes: list[str] = []
    groups: list[str] = []
    arrows: list[str] = []

    for i, label in enumerate(steps, start=1):
        cx = center_start + i * spacing - spacing
        keyframes.extend(step_keyframes(n, i, palette))
        icon = ICONS[prefix][i - 1]
        groups.append(
            f'<g class="g{i}" transform="translate({cx},{cy})">\n'
            f'    <circle class="step" r="{radius}"/>\n'
            f'    <g class="icon">{icon}</g>\n'
            f'    <text class="label" y="50">{label}</text>\n'
            f"</g>"
        )
        if i < n:
            next_cx = center_start + (i + 1) * spacing - spacing
            x1 = cx + radius
            x2 = next_cx - radius
            arrows.append(f'<line class="arrow" x1="{x1}" y1="{cy}" x2="{x2}" y2="{cy}"/>')

    token_frames: list[str] = []
    for i in range(n):
        start = i * slot
        active_end = start + slot * 0.80
        inactive_start = start + slot
        cx = center_start + i * spacing
        token_frames.append(f"0%,{pct(start)},{pct(active_end)},{pct(inactive_start)},100%{{transform:translate({cx}px,{cy}px)}}")
    token_kf = "@keyframes tokenMove { " + " ".join(token_frames) + " }"

    keyframes.append(f".token {{ fill:{palette['accent']}; animation:tokenMove 10s infinite; }}")
    keyframes.append(token_kf)

    keyframes_css = "\n    ".join(keyframes)
    groups_svg = "\n  ".join(groups)
    arrows_svg = "\n  ".join(arrows)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .bg {{ fill:{palette['bg']}; }}
    text {{ font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; text-anchor:middle; }}
    .step {{ fill:{palette['bg']}; stroke:{palette['muted']}; stroke-width:3; }}
    .icon {{ color:{palette['muted']}; }}
    .label {{ font-size:13px; font-weight:600; fill:{palette['muted']}; }}
    .arrow {{ stroke:{palette['muted']}; stroke-width:2; fill:none; }}
    {keyframes_css}
  </style>
  <rect width="100%" height="100%" class="bg"/>
  {groups_svg}
  {arrows_svg}
  <circle class="token" r="5"/>
</svg>
'''


def render_scanner_beam(prefix: str, steps: list[str], palette: dict[str, str]) -> str:
    """RedQuorum: a translucent scanner beam sweeps across the steps."""
    n = len(steps)
    center_start = 95
    spacing = 160
    margin_right = 65
    width = center_start + (n - 1) * spacing + margin_right
    height = 130
    cy = 55
    radius = 26

    keyframes: list[str] = []
    groups: list[str] = []
    arrows: list[str] = []

    slot = 100.0 / n
    for i, label in enumerate(steps, start=1):
        cx = center_start + i * spacing - spacing
        keyframes.extend(step_keyframes(n, i, palette))
        icon = ICONS[prefix][i - 1]
        groups.append(
            f'<g class="g{i}" transform="translate({cx},{cy})">\n'
            f'    <circle class="step" r="{radius}"/>\n'
            f'    <g class="icon">{icon}</g>\n'
            f'    <text class="label" y="50">{label}</text>\n'
            f"</g>"
        )
        if i < n:
            next_cx = center_start + (i + 1) * spacing - spacing
            x1 = cx + radius
            x2 = next_cx - radius
            arrows.append(f'<line class="arrow" x1="{x1}" y1="{cy}" x2="{x2}" y2="{cy}"/>')

    scanner_frames: list[str] = []
    for i in range(n):
        start = i * slot
        active_end = start + slot * 0.80
        inactive_start = start + slot
        cx = center_start + i * spacing
        scanner_frames.append(f"0%,{pct(start)},{pct(active_end)},{pct(inactive_start)},100%{{transform:translate({cx}px,{cy}px)}}")
    scanner_kf = "@keyframes scannerMove { " + " ".join(scanner_frames) + " }"

    keyframes.append(f".scanner {{ fill:{palette['accent']}; opacity:0.25; animation:scannerMove 10s infinite; }}")
    keyframes.append(scanner_kf)

    keyframes_css = "\n    ".join(keyframes)
    groups_svg = "\n  ".join(groups)
    arrows_svg = "\n  ".join(arrows)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .bg {{ fill:{palette['bg']}; }}
    text {{ font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; text-anchor:middle; }}
    .step {{ fill:{palette['bg']}; stroke:{palette['muted']}; stroke-width:3; }}
    .icon {{ color:{palette['muted']}; }}
    .label {{ font-size:13px; font-weight:600; fill:{palette['muted']}; }}
    .arrow {{ stroke:{palette['muted']}; stroke-width:2; fill:none; }}
    {keyframes_css}
  </style>
  <rect width="100%" height="100%" class="bg"/>
  {groups_svg}
  {arrows_svg}
  <rect class="scanner" x="-12" y="-35" width="24" height="70" rx="4"/>
</svg>
'''


RENDERERS = {
    "pipeline-token": render_pipeline_token,
    "scanner-beam": render_scanner_beam,
}


def main() -> None:
    out_dir = Path(__file__).resolve().parents[1] / "assets" / "projects"
    out_dir.mkdir(parents=True, exist_ok=True)

    for project in PROJECTS:
        renderer = RENDERERS[project["template"]]
        for theme, palette in project["colors"].items():
            filename = f"{project['prefix']}-{theme}.svg"
            svg = renderer(project["prefix"], project["steps"], palette)
            (out_dir / filename).write_text(svg, encoding="utf-8")
            print(f"Wrote {filename}")


if __name__ == "__main__":
    main()

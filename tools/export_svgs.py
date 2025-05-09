#!/usr/bin/env python3
"""Export selected SVG diagrams in design/ to high-resolution PNGs in paper/figs/.
Requires cairosvg (pip install cairosvg).  Run in CI after notebooks.
"""
import pathlib, cairosvg, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"
OUT = ROOT / "paper" / "figs"
OUT.mkdir(parents=True, exist_ok=True)

# map svg basename -> output png basename (same unless noted)
SVGS = {
    "gauge_stack.svg": "gauge_stack.png",
    "number_tower.svg": "number_tower.png",
    "tests_overview.svg": "tests_overview.png",
}

for svg_name, png_name in SVGS.items():
    svg_path = DESIGN / svg_name
    if not svg_path.exists():
        print(f"!! missing svg {svg_path}", file=sys.stderr)
        continue
    png_path = OUT / png_name
    data = cairosvg.svg2png(url=str(svg_path), output_width=1600)
    png_path.write_bytes(data)
    print("✓", png_path.relative_to(ROOT)) 
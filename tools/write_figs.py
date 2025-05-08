#!/usr/bin/env python3
"""
write_figs.py – append a save-figure cell to each notebook so that CI writes
all required figures into paper/figs/.

Run locally or in CI before notebook execution.
"""

import json
import pathlib
import sys

# ---------------------------------------------------------------------------
# Mapping: notebook filename  ->  [(figure_filename, variable_name), ...]
# ---------------------------------------------------------------------------
MAP = {
    "01_wave_speed.ipynb":      [("wave_speed.png", "plt")],
    "04_coupling_fan_in.ipynb": [("coupling_fan_in.png", "plt")],
    "07_mass_spectrum.ipynb":   [("mass_spectrum.png", "plt")],
    "10_bcs_gap.ipynb":         [("bcs_gap.png", "plt")],

    "06_curvature_map.ipynb":   [("spacetime_curvature.png", "plt")],
    "09_ring_line.ipynb":       [("ring_aperture_line.png", "plt")],
    "09_axial_lepton.ipynb":    [("axial_lepton_spectrum.png", "plt")],

    "13_lattice_colony.ipynb": [
        ("lattice_torus_geometry.png", "plt"),
        ("lattice_growth_curve.png",   "plt"),
        ("lattice_colony.png",         "plt"),
    ],
}

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"
FIG_DIR = ROOT / "paper" / "figs"

missing = False
for nb_name, figs in MAP.items():
    nb_path = NOTEBOOK_DIR / nb_name
    if not nb_path.exists():
        print("!! notebook missing:", nb_path, file=sys.stderr)
        missing = True
        continue

    nb = json.loads(nb_path.read_text())

    # build a single cell that writes every requested figure
    lines = [
        "import matplotlib.pyplot as _plt, pathlib, os",
        "root = pathlib.Path(__file__).resolve().parents[1]",
    ]
    for fname, var in figs:
        lines.append(
            f"{var}.gcf().savefig((root/'paper'/'figs'/'{fname}').as_posix(), "
            "bbox_inches='tight', dpi=300)"
        )

    nb["cells"].append({
        "cell_type": "code",
        "metadata": {},
        "source": [l + "\n" for l in lines],
        "outputs": [],
        "execution_count": None,
    })

    nb_path.write_text(json.dumps(nb, indent=1))

if missing:
    sys.exit(1)
print("All notebooks patched with save-fig cells.") 
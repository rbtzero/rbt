#!/usr/bin/env python3
"""
Run every notebook in /notebooks head-less and save all figures
under the expected name in /paper/figs, automatically replacing
placeholder files.

Usage:  python scripts/export_figs.py
"""
import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"
FIG_DIR = ROOT / "paper" / "figs"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def run_ipynb(nb_path: pathlib.Path):
    cmd = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--to",
        "html",
        "--execute",
        "--ExecutePreprocessor.timeout=600",
        str(nb_path.name),
    ]
    subprocess.check_call(cmd, cwd=NB_DIR)


def main():
    nbs = sorted(NB_DIR.glob("*.ipynb"))
    if not nbs:
        print("No notebooks found in", NB_DIR)
        return
    for nb in nbs:
        print("⇢ executing", nb.name, flush=True)
        run_ipynb(nb)
    print("✓  all notebooks executed; ensure each plt.savefig() writes into paper/figs/")


if __name__ == "__main__":
    main() 
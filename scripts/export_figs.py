#!/usr/bin/env python3
"""
Run every notebook in /notebooks head-less and save all figures
under the expected name in /paper/figs, automatically replacing
placeholder files.

Usage:  python scripts/export_figs.py
"""
import pathlib, subprocess, sys
import os

ROOT = pathlib.Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"
FIG_DIR = ROOT / "paper" / "figs"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def run_ipynb(nb_path: pathlib.Path):
    # Some legacy notebooks use __file__ (undefined in Jupyter) or alias
    # matplotlib.pyplot as _plt.  We patch these patterns on the fly and run
    # the modified notebook in a temporary directory.
    import json, tempfile, shutil

    with nb_path.open() as f:
        try:
            nb_json = json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️  Skipping invalid/notebook file: {nb_path.name}")
            return

    replaced = False
    for cell in nb_json.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        new_lines = []
        for line in cell.get("source", []):
            if "matplotlib.pyplot as _plt" in line:
                line = line.replace("matplotlib.pyplot as _plt", "matplotlib.pyplot as plt")
                replaced = True
            if "_plt." in line:
                line = line.replace("_plt.", "plt.")
                replaced = True
            if "Path(__file__).resolve().parents[1]" in line:
                line = line.replace("Path(__file__).resolve().parents[1]", "Path.cwd().parents[1]")
                replaced = True
            if "Path.cwd().parents[1]" in line:
                # Keep the idea of \"root above\" but point inside the temp dir
                line = line.replace("Path.cwd().parents[1]", "Path.cwd()")
                replaced = True
            if "../paper/figs" in line:
                line = line.replace("../paper/figs", "paper/figs")
                replaced = True
            new_lines.append(line)
        cell["source"] = new_lines

    temp_dir = tempfile.mkdtemp()
    temp_nb = pathlib.Path(temp_dir) / nb_path.name
    with temp_nb.open("w") as f:
        json.dump(nb_json, f)

    # Ensure faux figs path exists (symlink or directory) before execution
    faux_figs = pathlib.Path(temp_dir) / "paper" / "figs"
    faux_figs.mkdir(parents=True, exist_ok=True)
    try:
        # set up an *additional* fallback one directory above the temp dir so that
        # notebooks which compute ROOT = Path.cwd().parents[1] (thereby pointing
        # outside the execution sandbox) can still resolve paper/figs correctly.
        parent_faux_figs = pathlib.Path(temp_dir).parent / "paper" / "figs"
        # The same notebook may be executed multiple times in the same session;
        # guard against races by checking existence and type first.
        if not parent_faux_figs.exists():
            parent_faux_figs.mkdir(parents=True, exist_ok=True)
        if not parent_faux_figs.is_symlink():
            try:
                parent_faux_figs.unlink(missing_ok=True)  # type: ignore[arg-type]
            except Exception:
                pass
            parent_faux_figs.symlink_to(FIG_DIR, target_is_directory=True)  # type: ignore[arg-type]
    except Exception:
        # Nothing mission-critical here: fall back to default behaviour if symlink fails
        pass
    try:
        if not faux_figs.exists():
            faux_figs.symlink_to(FIG_DIR, target_is_directory=True)  # type: ignore[arg-type]
    except Exception:
        pass

    cmd = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--to",
        "html",
        "--execute",
        "--ExecutePreprocessor.timeout=600",
        str(temp_nb),
    ]
    env = os.environ.copy()
    # Ensure that imports like `from splitstep_toe` work from within the sandbox
    env["PYTHONPATH"] = (
        str(ROOT) + (":" + env["PYTHONPATH"] if "PYTHONPATH" in env else "")
    )
    subprocess.check_call(cmd, cwd=temp_dir, env=env)

    # Copy any freshly written figures back to real FIG_DIR
    if faux_figs.exists():
        for f in faux_figs.glob("*"):
            dest = FIG_DIR / f.name
            if not dest.exists():
                shutil.copy2(f, dest)

    shutil.rmtree(temp_dir)


def main():
    # 0. First render the deterministic Matplotlib diagrams that are not notebook-based
    render_script = ROOT / 'tools' / 'render_diagrams.py'
    if render_script.exists():
        print('⇢ rendering static diagrams via', render_script.name, flush=True)
        subprocess.check_call([sys.executable, str(render_script)])

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
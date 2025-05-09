#!/usr/bin/env python3
"""Execute the plotting code snippets defined in bootstrap_notebooks.py to render
all notebook-derived figures without needing nbconvert.  This bypasses the
jinja2/nbconvert dependency issues that were blocking CI locally.
"""
import importlib.util, pathlib, types, sys, os

ROOT = pathlib.Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("bootstrap", ROOT/"tools"/"bootstrap_notebooks.py")
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)  # type: ignore

# run code as if inside notebooks dir so relative savefig paths work
os.chdir(ROOT / "notebooks")

fig_dir = ROOT / "paper" / "figs"
fig_dir.mkdir(parents=True, exist_ok=True)

for nb_name, code in bootstrap.cells_map.items():
    print(f"→ rendering {nb_name} …", flush=True)
    ns = {}
    try:
        exec(code, ns)
    except Exception as e:
        print(f"!! {nb_name} failed: {e}", file=sys.stderr)
        sys.exit(1)
print("✓ all notebook figures written") 
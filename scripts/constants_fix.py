#!/usr/bin/env python3
"""Patch resume_runner.py to ensure exactly one `_default_constants` helper.
Usage (from Colab cell, adjust path if needed):
    !python scripts/constants_fix.py /content/drive/MyDrive/rbt_run_gpu/src/resume_runner.py
The script will:
  • back-up the original file to <file>.bak
  • comment‐out all but the first duplicate definition
  • insert the canonical helper if none exists.
It prints a short report at the end.
"""
import sys, re, shutil, textwrap, pathlib

if len(sys.argv) != 2:
    sys.exit("Usage: constants_fix.py <path/to/resume_runner.py>")
file_path = pathlib.Path(sys.argv[1]).expanduser().resolve()

if not file_path.exists():
    sys.exit(f"❌ {file_path} not found")

backup = file_path.with_suffix(file_path.suffix + ".bak")
shutil.copy(file_path, backup)
print(f"🔒 Backup saved to {backup}")

lines = file_path.read_text().splitlines()
new = []
found_first = False
skip_block = False
indent = ""

def start_of_def(idx: int) -> bool:
    return bool(re.match(r"\s*def\s+_default_constants\s*\(", lines[idx]))

for i, line in enumerate(lines):
    if skip_block:
        if not line.startswith(indent):  # end of previous function body
            skip_block = False  # append and continue processing normally
        else:
            new.append(f"# DUPLICATE REMOVED: {line}")
            continue  # stay inside duplicate block

    if start_of_def(i):
        if not found_first:
            found_first = True
            new.append(line)  # keep the first definition
            indent = re.match(r"^(\s*)", line).group(1) + "    "  # body indent
        else:
            # comment out duplicate def line and enter skip mode for its body
            new.append(f"# DUPLICATE REMOVED: {line}")
            skip_block = True
            indent = re.match(r"^(\s*)", line).group(1) + "    "
        continue

    new.append(line)

if not found_first:
    print("⚠️  No _default_constants() found – inserting canonical helper")
    helper = textwrap.dedent("""


def _default_constants():
    """Return canonical physical constants used by RBT."""
    return {
        "alpha": 7.2973525693e-3,
        "c": 2.99792458e8,
        "hbar": 1.054571817e-34,
        "G": 6.67430e-11,
        "e": 1.602176634e-19,
        "kB": 1.380649e-23,
    }
""")
    # insert after the helpers section marker if present, else append to end
    for idx, ln in enumerate(new):
        if "helpers" in ln.lower():
            new.insert(idx + 1, helper)
            break
    else:
        new.append(helper)

file_path.write_text("\n".join(new))
print("✅ _default_constants patch complete – file updated.") 
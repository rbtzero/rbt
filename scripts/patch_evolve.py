#!/usr/bin/env python3
"""Ensure resume_runner.py defines a public evolve() wrapper.
Run:
    !python scripts/patch_evolve.py /content/drive/MyDrive/rbt_run_gpu/src/resume_runner.py
"""
import sys, pathlib, shutil, textwrap, re

if len(sys.argv) != 2:
    sys.exit("Usage: patch_evolve.py <resume_runner.py>")
fp = pathlib.Path(sys.argv[1]).expanduser().resolve()
if not fp.exists():
    sys.exit(f"❌ {fp} not found")

src = fp.read_text().splitlines()
if any(re.match(r"\s*def\s+evolve\s*\(", l) for l in src):
    print("✅ evolve() already defined – nothing to do")
    sys.exit(0)

# locate insertion point: after import block for _evolve
insert_at = None
for i,line in enumerate(src):
    if re.search(r"evolve_field", line):
        insert_at = i+1
        break
if insert_at is None:
    insert_at = len(src)

block = textwrap.dedent("""

# Public wrapper so main loop can call evolve() agnostic of backend

def evolve(field, dt, const, steps):
    return _evolve(field, dt, const, steps)
""").splitlines()

shutil.copy(fp, fp.with_suffix(fp.suffix+".bak"))
print("🔒 backup saved to", fp.with_suffix(fp.suffix+".bak"))

src[insert_at:insert_at] = block
fp.write_text("\n".join(src))
print("✅ evolve() inserted into", fp) 
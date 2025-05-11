#!/usr/bin/env python3
"""
Convert each lean_proofs/*.lean file into a \lstlisting appendix.

Requires pygments (already in CI image).
"""
import pathlib, pygments, pygments.lexers, pygments.formatters

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC  = ROOT / "lean_proofs"
DST  = ROOT / "paper" / "appendices"
DST.mkdir(exist_ok=True, parents=True)

fmt = pygments.formatters.LatexFormatter(
    style="default", linenos=True, verboptions="frame=single"
)

written=False
for path in SRC.glob("*.lean"):
    code = path.read_text()
    outfile = DST / f"{path.stem}.tex"
    new_tex = "\\begin{lstlisting}[language=Lean]\n" + code + "\n\\end{lstlisting}\n"
    if not outfile.exists() or outfile.read_text() != new_tex:
        outfile.write_text(new_tex)
        print("✓ wrote", outfile)
        written=True

if not written:
    print("✓ no appendix listings changed; skipping commit hook") 
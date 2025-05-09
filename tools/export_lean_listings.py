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

for path in SRC.glob("*.lean"):
    code = path.read_text()
    latex = fmt.format(pygments.lexers.get_lexer_by_name("lean").get_tokens(code))
    outfile = DST / f"{path.stem}.tex"
    outfile.write_text("\\begin{lstlisting}[language=Lean]\n" + code + "\n\\end{lstlisting}\n")
    print("✓ wrote", outfile) 
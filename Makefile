PDF=paper/main.pdf

figs:
	@python scripts/export_figs.py

proofs:
	@bash scripts/export_proofs.sh

pdf:
	@latexmk -pdf -interaction=nonstopmode -quiet $(PDF)

all-ci: figs proofs pdf
	@echo "✓ CI build pipeline completed" 
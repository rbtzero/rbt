#!/usr/bin/env bash
# Convert Lean-generated TeX docs and move them into the appendices
set -e
PROJECT_DIR=$(git rev-parse --show-toplevel)
cd "$PROJECT_DIR/lean_proofs"

lake env lean --doc=tex *.lean
mkdir -p "$PROJECT_DIR/paper/appendices"
mv out/doc/*.tex "$PROJECT_DIR/paper/appendices/" || true

echo "✓  Lean proofs exported." 
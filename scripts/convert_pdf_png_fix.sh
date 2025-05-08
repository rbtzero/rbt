#!/usr/bin/env bash
set -e
for f in paper/figs/*.pdf; do
  if [[ -f "$f" ]]; then
    sig=$(xxd -l4 -p "$f")
    if [[ $sig == "89504e47" ]]; then
      base=${f%.pdf}
      git mv "$f" "$base.png"
    fi
  fi
done
# patch tex files
for tex in paper/sections/*.tex; do
  sed -i '' -E 's/figs\/([a-zA-Z0-9_]+)\.pdf/figs\/\1.png/g' "$tex"
done 
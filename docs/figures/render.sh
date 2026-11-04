#!/usr/bin/env bash
# Render the final paper's original figures without changing the SVG redraws.
set -euo pipefail
FIGURE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PAPER_PATH="$FIGURE_DIR/../flash-atc2026.pdf"
command -v pdftoppm >/dev/null
mkdir -p "$FIGURE_DIR/paper-originals"

pdftoppm -f 5 -l 5 -r 300 -x 1375 -y 742 -W 925 -H 375 \
  -png -singlefile "$PAPER_PATH" "$FIGURE_DIR/paper-originals/figure-4-hybrid-key"
pdftoppm -f 6 -l 6 -r 300 -x 1310 -y 283 -W 962 -H 521 \
  -png -singlefile "$PAPER_PATH" "$FIGURE_DIR/paper-originals/figure-5-dirty-tracking"
pdftoppm -f 10 -l 10 -r 300 -x 338 -y 288 -W 1867 -H 329 \
  -png -singlefile "$PAPER_PATH" "$FIGURE_DIR/checkpoint-latency"

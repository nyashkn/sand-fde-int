#!/usr/bin/env bash
# Render an HTML file to a full-page PNG, trimmed to actual content.
# Usage: shoot.sh <html_path> <png_out>
# ponytail: fixed 12000px tall capture then /opt/homebrew/bin/magick-trim reclaims the true height.
#           If an artifact ever exceeds 12000px it'll clip — bump WINH.
set -euo pipefail
HTML="$1"; OUT="$2"
WINW=1440; WINH=12000
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p "$(dirname "$OUT")"
TMP="${OUT%.png}.raw.png"
"$CHROME" --headless --no-sandbox --hide-scrollbars \
  --force-device-scale-factor=1 --window-size="${WINW},${WINH}" \
  --default-background-color=FFFFFFFF \
  --screenshot="$TMP" "file://$HTML" >/dev/null 2>&1
# Trim uniform border (the white padding below content) and flatten.
/opt/homebrew/bin/magick "$TMP" -trim +repage -bordercolor white -border 24 "$OUT"
rm -f "$TMP"
echo "shot: $OUT ($(/opt/homebrew/bin/magick identify -format '%wx%h' "$OUT"))"

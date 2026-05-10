#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# optimize-images.sh
#
# Convert original archival scans into web-optimized JPEGs.
#
# Usage:
#   ./scripts/optimize-images.sh <source-dir> <output-dir>
#
# Example:
#   ./scripts/optimize-images.sh \
#     /Volumes/Archive/scans/book-01 \
#     src/books/book-01/images/web
#
# Requires: ImageMagick (`brew install imagemagick`)
#
# Settings:
#   - Resizes to max 1800px on the longest dimension
#   - JPEG quality 85
#   - Strips EXIF metadata
#   - Progressive encoding (faster perceived load)
# ─────────────────────────────────────────────────────────────────

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <source-dir> <output-dir>"
  exit 1
fi

SRC="$1"
DEST="$2"

if [ ! -d "$SRC" ]; then
  echo "Error: source directory $SRC not found"
  exit 1
fi

mkdir -p "$DEST"

# Detect ImageMagick
if command -v magick >/dev/null 2>&1; then
  IM="magick"
elif command -v convert >/dev/null 2>&1; then
  IM="convert"
else
  echo "Error: ImageMagick not found. Install with: brew install imagemagick"
  exit 1
fi

count=0
total=$(find "$SRC" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.tif" -o -iname "*.tiff" \) | wc -l | tr -d ' ')

echo "Optimizing $total images from $SRC → $DEST"
echo

for img in "$SRC"/*.{jpg,JPG,jpeg,JPEG,png,PNG,tif,TIF,tiff,TIFF}; do
  [ -f "$img" ] || continue
  count=$((count + 1))

  # Extract just the page number from filenames like "Album_Memories_01_003.JPG"
  # Falls back to the basename if pattern doesn't match
  base=$(basename "$img")
  if [[ "$base" =~ _([0-9]{3,4})\. ]]; then
    page="${BASH_REMATCH[1]}"
    output="$DEST/${page}.jpg"
  else
    name="${base%.*}"
    output="$DEST/${name}.jpg"
  fi

  printf "[%3d/%d] %s → %s\n" "$count" "$total" "$base" "$(basename "$output")"

  $IM "$img" \
    -resize '1800x1800>' \
    -quality 85 \
    -strip \
    -interlace Plane \
    -colorspace sRGB \
    "$output"
done

echo
echo "✓ Done. $count image(s) written to $DEST"

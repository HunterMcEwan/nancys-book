# ─────────────────────────────────────────────────────────────────
# optimize-images.ps1
#
# Convert original archival scans into web-optimized JPEGs.
# Windows-native port of optimize-images.sh — same settings.
#
# Usage:
#   .\scripts\optimize-images.ps1 <source-dir> <output-dir>
#
# Example:
#   .\scripts\optimize-images.ps1 .\scans .\src\books\book-01\images\web
#
# Requires: ImageMagick on PATH (`magick` command).
#   Install: https://imagemagick.org/script/download.php#windows
#
# Settings (mirror the bash version):
#   - Resizes to max 1800px on the longest dimension
#   - JPEG quality 85
#   - Strips EXIF metadata
#   - Progressive encoding (faster perceived load)
#   - sRGB colorspace
# ─────────────────────────────────────────────────────────────────

param(
  [Parameter(Mandatory=$true, Position=0)]
  [string]$SrcDir,

  [Parameter(Mandatory=$true, Position=1)]
  [string]$DestDir
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -Path $SrcDir -PathType Container)) {
  Write-Error "Source directory not found: $SrcDir"
  exit 1
}

if (-not (Get-Command magick -ErrorAction SilentlyContinue)) {
  Write-Error "ImageMagick 'magick' command not found. Install from https://imagemagick.org/script/download.php#windows"
  exit 1
}

New-Item -ItemType Directory -Force -Path $DestDir | Out-Null

$images = Get-ChildItem -Path $SrcDir -File | Where-Object {
  $_.Extension -match '^\.(jpe?g|png|tiff?)$'
}

$total = $images.Count
if ($total -eq 0) {
  Write-Output "No images found in $SrcDir"
  exit 0
}

Write-Output "Optimizing $total images from $SrcDir -> $DestDir"
Write-Output ""

$count = 0
foreach ($img in $images) {
  $count++

  # Extract page number from filenames like "Album_Memories_01_003.JPG".
  # Falls back to the full basename if pattern doesn't match.
  if ($img.Name -match '_(\d{3,4})\.[^.]+$') {
    $page = $matches[1]
    $output = Join-Path $DestDir "$page.jpg"
  } else {
    $name = [System.IO.Path]::GetFileNameWithoutExtension($img.Name)
    $output = Join-Path $DestDir "$name.jpg"
  }

  Write-Output ("[{0,3}/{1}] {2} -> {3}" -f $count, $total, $img.Name, (Split-Path $output -Leaf))

  & magick $img.FullName `
    -resize "1800x1800>" `
    -quality 85 `
    -strip `
    -interlace Plane `
    -colorspace sRGB `
    $output

  if ($LASTEXITCODE -ne 0) {
    Write-Error "ImageMagick failed for $($img.Name) (exit $LASTEXITCODE)"
    exit 1
  }
}

Write-Output ""
Write-Output "Done. $count image(s) written to $DestDir"

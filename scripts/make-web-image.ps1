# -----------------------------------------------------------------
# make-web-image.ps1
#
# Optimize a single archival scan to a web-ready JPEG using only
# Windows built-in .NET libraries (System.Drawing). Use this when
# ImageMagick is not installed; the result is "good enough" for web
# display (1800px max, quality 85). For bulk optimization with the
# full feature set (EXIF stripping, progressive JPEG, sharpening),
# prefer scripts/optimize-images.sh / .ps1 with ImageMagick.
#
# Usage:
#   .\scripts\make-web-image.ps1 -Source <path> -Destination <path>
#
# Example:
#   .\scripts\make-web-image.ps1 `
#     -Source 'scans\Album Memories 01_001.JPG' `
#     -Destination src\books\book-001\images\web\001.jpg
# -----------------------------------------------------------------

param(
  [Parameter(Mandatory=$true)] [string]$Source,
  [Parameter(Mandatory=$true)] [string]$Destination,
  [int]$MaxDimension = 1800,
  [int]$Quality = 85
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$srcPath = [System.IO.Path]::GetFullPath($Source)
$dstPath = [System.IO.Path]::GetFullPath($Destination)

if (-not (Test-Path -LiteralPath $srcPath)) {
  Write-Error "Source not found: $srcPath"
  exit 1
}

$dstDir = Split-Path -Parent $dstPath
if ($dstDir -and -not (Test-Path -LiteralPath $dstDir)) {
  New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
}

$src = [System.Drawing.Image]::FromFile($srcPath)
try {
  $ratio = [Math]::Min($MaxDimension / $src.Width, $MaxDimension / $src.Height)
  if ($ratio -gt 1.0) { $ratio = 1.0 }
  $newWidth  = [int]($src.Width  * $ratio)
  $newHeight = [int]($src.Height * $ratio)

  $bmp = New-Object System.Drawing.Bitmap $newWidth, $newHeight
  $bmp.SetResolution($src.HorizontalResolution, $src.VerticalResolution)

  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.InterpolationMode  = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.SmoothingMode      = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
  $g.PixelOffsetMode    = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
  $g.DrawImage($src, 0, 0, $newWidth, $newHeight)
  $g.Dispose()

  $encoder = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() |
    Where-Object { $_.MimeType -eq 'image/jpeg' }
  $params = New-Object System.Drawing.Imaging.EncoderParameters 1
  $params.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter(
    [System.Drawing.Imaging.Encoder]::Quality, [int64]$Quality)

  $bmp.Save($dstPath, $encoder, $params)
  $bmp.Dispose()
} finally {
  $src.Dispose()
}

$srcMB = [Math]::Round((Get-Item -LiteralPath $srcPath).Length / 1MB, 2)
$dstKB = [Math]::Round((Get-Item -LiteralPath $dstPath).Length / 1KB, 0)
Write-Output "$Source ($srcMB MB) -> $Destination ($dstKB KB, ${newWidth}x${newHeight})"

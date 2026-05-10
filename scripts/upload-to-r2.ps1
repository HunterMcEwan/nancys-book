# -----------------------------------------------------------------
# upload-to-r2.ps1
#
# Bulk-upload archival scans from /scans/ to a Cloudflare R2 bucket.
# 4000px originals stay out of git; the site links to them via R2.
#
# Usage:
#   .\scripts\upload-to-r2.ps1 -BucketName <bucket> [-DryRun]
#
# Naming convention: source files like "Album Memories 01_NNN.JPG" are
# renamed to "book-NNN/NNN.jpg" in the bucket.
#
#   "Album Memories 01_" -> book-001
#   "Family book_"       -> book-002
#   "Photo Memories 01_" -> book-003
#
# Requires:
#   - wrangler logged in: `wrangler login`
#   - R2 enabled in Cloudflare account
#   - Bucket already created (this script does not create it)
#
# Re-runnable: R2 PUT overwrites, so a partial run can be resumed by
# running again. Use -DryRun to preview the mapping without uploading.
# -----------------------------------------------------------------

param(
  [Parameter(Mandatory=$true)]
  [string]$BucketName,

  [Parameter()]
  [string]$ScansDir = "scans",

  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -Path $ScansDir -PathType Container)) {
  Write-Error "Scans directory not found: $ScansDir"
  exit 1
}

# wrangler is installed locally as a devDep; put node_modules\.bin on PATH
# so we can call `wrangler` directly without npx overhead per-invocation.
$projectRoot = Split-Path $PSScriptRoot -Parent
$nodeBin = Join-Path $projectRoot "node_modules\.bin"
if (-not (Test-Path $nodeBin)) {
  Write-Error "node_modules not found at $nodeBin. Run 'npm install' from the project root."
  exit 1
}
$env:Path = "$nodeBin;$env:Path"

if (-not (Get-Command wrangler -ErrorAction SilentlyContinue)) {
  Write-Error "wrangler not found after adding $nodeBin to PATH. Try 'npm install'."
  exit 1
}

$mapping = [ordered]@{
  "Album Memories 01_" = "book-001"
  "Family book_"       = "book-002"
  "Photo Memories 01_" = "book-003"
}

$files = Get-ChildItem -Path $ScansDir -File
$total = $files.Count
Write-Output "Found $total files in $ScansDir"
if ($DryRun) { Write-Output "(dry run -- no uploads)" }
Write-Output ""

$count = 0
$uploaded = 0
$skipped = 0

foreach ($file in $files) {
  $count++
  $matched = $false

  foreach ($prefix in $mapping.Keys) {
    if ($file.Name.StartsWith($prefix)) {
      $matched = $true
      $rest = $file.Name.Substring($prefix.Length)

      if ($rest -match '^(\d{3,4})\.(?i)jpe?g$') {
        $book = $mapping[$prefix]
        $pageNum = $matches[1]
        $key = "$book/$pageNum.jpg"

        Write-Output ("[{0,4}/{1}] {2} -> {3}" -f $count, $total, $file.Name, $key)

        if (-not $DryRun) {
          & wrangler r2 object put "$BucketName/$key" --file $file.FullName --remote
          if ($LASTEXITCODE -ne 0) {
            Write-Error "Upload failed for $key (exit $LASTEXITCODE)"
            exit 1
          }
        }
        $uploaded++
      } else {
        Write-Warning "Unexpected filename format (skipping): $($file.Name)"
        $skipped++
      }
      break
    }
  }

  if (-not $matched) {
    Write-Warning "Unknown prefix (skipping): $($file.Name)"
    $skipped++
  }
}

Write-Output ""
if ($DryRun) {
  Write-Output "Dry run complete. Would upload $uploaded, skipping $skipped."
} else {
  Write-Output "Done. Uploaded $uploaded, skipped $skipped."
}

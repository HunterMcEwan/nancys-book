<#
.SYNOPSIS
  Preflight check: detect People-list slug collisions across all page frontmatter.

.DESCRIPTION
  Eleventy generates one /people/<slug>/index.html per unique person. If two
  distinct names slugify to the same value, the build fails with "Output
  conflict: multiple input files are writing to ./_site/people/<slug>/index.html".

  This script mirrors Eleventy's slugify() exactly:
    1. NFD-normalize the string.
    2. Strip Unicode combining marks (\p{Mn}) — so Serré -> Serre.
    3. Lower-case.
    4. Replace any run of non-[a-z0-9] with a single hyphen.
    5. Trim leading/trailing hyphens.

  We then walk every src/books/*/pages/*.md, extract the people: list, slugify
  each name, and report any slug that maps to multiple distinct names.

  Earlier inline preflights skipped the NFD/combining-mark step, so a
  Margaret Serre / Margaret Serré pair slipped through and broke the build.
  This script encodes the correct algorithm in one place.

.EXAMPLE
  pwsh scripts/check-people-slugs.ps1
#>

function Get-EleventySlug {
  param([string]$Str)
  if ([string]::IsNullOrEmpty($Str)) { return "" }
  $nfd = $Str.Normalize([System.Text.NormalizationForm]::FormD)
  $stripped = $nfd -replace '\p{Mn}',''
  $lower = $stripped.ToLowerInvariant()
  $hyphenated = [System.Text.RegularExpressions.Regex]::Replace($lower, '[^a-z0-9]+', '-')
  return ($hyphenated -replace '^-+|-+$','')
}

$slugMap = @{}

$pageFiles = Get-ChildItem -Path "src/books" -Recurse -Filter "*.md" -File

foreach ($file in $pageFiles) {
  $lines = Get-Content -LiteralPath $file.FullName
  $inFrontmatter = $false
  $inPeople = $false
  $frontmatterCount = 0
  foreach ($line in $lines) {
    if ($line -match '^---\s*$') {
      $frontmatterCount++
      if ($frontmatterCount -eq 1) { $inFrontmatter = $true; continue }
      if ($frontmatterCount -eq 2) { break }
    }
    if (-not $inFrontmatter) { continue }
    if ($line -match '^people:\s*$') { $inPeople = $true; continue }
    if ($inPeople) {
      if ($line -match '^\s*-\s+(.+?)\s*$') {
        $name = $Matches[1].Trim()
        $name = $name -replace '^["'']|["'']$',''
        $slug = Get-EleventySlug -Str $name
        if (-not $slugMap.ContainsKey($slug)) {
          $slugMap[$slug] = New-Object System.Collections.Generic.HashSet[string]
        }
        $null = $slugMap[$slug].Add($name)
      } elseif ($line -match '^[a-zA-Z_]+:') {
        $inPeople = $false
      }
    }
  }
}

$collisions = $slugMap.GetEnumerator() | Where-Object { $_.Value.Count -gt 1 }

if ($collisions.Count -eq 0) {
  Write-Output "CLEAN: $($slugMap.Count) unique people slugs across $($pageFiles.Count) pages."
  exit 0
} else {
  Write-Output "COLLISIONS FOUND ($($collisions.Count)):"
  foreach ($entry in $collisions) {
    $names = ($entry.Value | Sort-Object) -join " | "
    Write-Output "  $($entry.Key)  <-  $names"
  }
  exit 1
}

<#
.SYNOPSIS
  Preflight check: detect People- and Places-list slug collisions across all
  page frontmatter.

.DESCRIPTION
  Eleventy generates one /people/<slug>/index.html and one /places/<slug>/index.html
  per unique entry. If two distinct entries slugify to the same value, the build
  fails with "Output conflict: multiple input files are writing to
  ./_site/<people|places>/<slug>/index.html".

  This script mirrors Eleventy's slugify() exactly:
    1. NFD-normalize the string.
    2. Strip Unicode combining marks (\p{Mn}) — so Serré -> Serre.
    3. Lower-case.
    4. Replace any run of non-[a-z0-9] with a single hyphen.
    5. Trim leading/trailing hyphens.

  We walk every src/books/*/pages/*.md, extract the people: and places: lists,
  slugify each entry, and report any slug that maps to multiple distinct names.

  Past collision classes the inline preflight has missed:
    - Margaret Serre / Margaret Serré        (NFD diacritic strip)
    - Anne O. Bryan / Anne O'Bryan           (apostrophe vs period)
    - Wm / Wm.                               (honorific period)
    - Mulberry plantation / Mulberry Plantation  (capitalization)
    - Walhalla SC / Walhalla, SC             (punctuation)
  All collapse to one slug because Eleventy strips all non-alphanumerics.

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

function Find-Collisions {
  param(
    [string]$ListKey,
    [System.IO.FileInfo[]]$Files
  )
  $slugMap = @{}
  foreach ($file in $Files) {
    $lines = Get-Content -LiteralPath $file.FullName
    $inFrontmatter = $false
    $inList = $false
    $frontmatterCount = 0
    foreach ($line in $lines) {
      if ($line -match '^---\s*$') {
        $frontmatterCount++
        if ($frontmatterCount -eq 1) { $inFrontmatter = $true; continue }
        if ($frontmatterCount -eq 2) { break }
      }
      if (-not $inFrontmatter) { continue }
      if ($line -match "^${ListKey}:\s*$") { $inList = $true; continue }
      if ($inList) {
        if ($line -match '^\s*-\s+(.+?)\s*$') {
          $name = $Matches[1].Trim()
          $name = $name -replace '^["'']|["'']$',''
          $slug = Get-EleventySlug -Str $name
          if (-not $slugMap.ContainsKey($slug)) {
            $slugMap[$slug] = New-Object System.Collections.Generic.HashSet[string]
          }
          $null = $slugMap[$slug].Add($name)
        } elseif ($line -match '^[a-zA-Z_]+:') {
          $inList = $false
        }
      }
    }
  }
  return $slugMap
}

$pageFiles = Get-ChildItem -Path "src/books" -Recurse -Filter "*.md" -File

$exitCode = 0

foreach ($listKey in @('people', 'places')) {
  $slugMap = Find-Collisions -ListKey $listKey -Files $pageFiles
  $collisions = @($slugMap.GetEnumerator() | Where-Object { $_.Value.Count -gt 1 })

  $label = $listKey.Substring(0,1).ToUpper() + $listKey.Substring(1)
  if ($collisions.Count -eq 0) {
    Write-Output "${label}: CLEAN — $($slugMap.Count) unique slugs across $($pageFiles.Count) pages."
  } else {
    Write-Output "${label}: COLLISIONS FOUND ($($collisions.Count)):"
    foreach ($entry in $collisions) {
      $names = ($entry.Value | Sort-Object) -join " | "
      Write-Output "  $($entry.Key)  <-  $names"
    }
    $exitCode = 1
  }
}

exit $exitCode

# -----------------------------------------------------------------
# rebuild-master-index.ps1
#
# Regenerates data/master-index.csv from the frontmatter of every
# transcription .md file under src/books/*/pages/.
#
# The .md files are the source of truth; the CSV is a derived
# tabular index for human reference. Run this after adding /
# editing pages.
#
# Usage:
#   .\scripts\rebuild-master-index.ps1
# -----------------------------------------------------------------

$ErrorActionPreference = "Stop"

$root = Split-Path $PSScriptRoot -Parent
$pagesGlob = Join-Path $root "src\books\*\pages\*.md"
$csvPath  = Join-Path $root "data\master-index.csv"

function ParseFrontmatter([string]$text) {
  if ($text -notmatch '(?s)^---\r?\n(.*?)\r?\n---') { return $null }
  return $matches[1]
}

function GetScalar([string]$fm, [string]$key) {
  if ($fm -match "(?m)^${key}:\s*(.*)$") {
    $v = $matches[1].Trim()
    if ($v.StartsWith('"') -and $v.EndsWith('"')) { $v = $v.Substring(1, $v.Length - 2) }
    return $v
  }
  return ""
}

function GetList([string]$fm, [string]$key) {
  $lines = $fm -split "`n"
  $start = $false
  $items = @()
  foreach ($line in $lines) {
    if ($line -match "^${key}:\s*$") { $start = $true; continue }
    if ($start) {
      if ($line -match '^\s*-\s+(.+)$') {
        $items += $matches[1].Trim()
      } elseif ($line -match '^\S' -or $line -match '^---') {
        break
      }
    }
  }
  return ($items -join '; ')
}

function CsvEscape([string]$v) {
  if (-not $v) { return "" }
  if ($v -match '[,"\n\r]') {
    $v = $v -replace '"', '""'
    return '"' + $v + '"'
  }
  return $v
}

# Filename prefix per book (so we can reconstruct the source filename)
$prefixForBook = @{
  1 = "Album_Memories_01_"
  2 = "Family_book_"
  3 = "Photo_Memories_01_"
}

$files = Get-ChildItem -Path $pagesGlob -File | Sort-Object @{
  Expression = {
    if ($_.DirectoryName -match 'book-(\d+)\\pages$') { [int]$matches[1] } else { 999 }
  }
}, @{
  Expression = {
    if ($_.BaseName -match '^(\d+)$') { [int]$matches[1] } else { 999 }
  }
}

$rows = @("filename,book,page,image_type,date_range,people,places,content_types,transcribed,transcription_file,notes")

foreach ($file in $files) {
  # Read as UTF-8 explicitly. PS 5.1 Get-Content defaults to system codepage,
  # which mangles em-dash/en-dash and other non-ASCII chars in our .md files.
  $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.UTF8Encoding]::new($false))
  $fm = ParseFrontmatter $content
  if (-not $fm) { Write-Warning "No frontmatter: $($file.FullName)"; continue }

  $bookNum = 0
  if ($file.DirectoryName -match 'book-(\d+)\\pages$') { $bookNum = [int]$matches[1] }

  $page = GetScalar $fm 'pageNumber'
  if (-not $page) { Write-Warning "No pageNumber: $($file.FullName)"; continue }
  $pagePadded = $page.PadLeft(3, '0')

  $date  = GetScalar $fm 'date_range'
  $note  = GetScalar $fm 'notes'
  $trans = if ((GetScalar $fm 'transcribed') -eq 'true') { 'Y' } else { 'N' }

  $people = GetList $fm 'people'
  $places = GetList $fm 'places'
  $types  = GetList $fm 'content_types'

  $prefix = $prefixForBook[$bookNum]
  if (-not $prefix) { $prefix = "unknown_book${bookNum}_" }
  $filename = "$prefix${pagePadded}.JPG"

  $bookPadded = $bookNum.ToString('000')
  $transFile = "src/books/book-${bookPadded}/pages/${pagePadded}.md"

  $row = @(
    $filename,
    $bookNum,
    $page,
    "scrapbook page",
    (CsvEscape $date),
    (CsvEscape $people),
    (CsvEscape $places),
    (CsvEscape $types),
    $trans,
    $transFile,
    (CsvEscape $note)
  ) -join ','

  $rows += $row
}

# Write UTF-8 without BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($csvPath, ($rows -join "`r`n") + "`r`n", $utf8NoBom)

Write-Output "Wrote $($rows.Count - 1) rows to $csvPath"

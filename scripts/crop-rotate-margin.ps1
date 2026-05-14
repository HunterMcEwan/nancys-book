param(
    [Parameter(Mandatory=$true)][string]$Source,
    [Parameter(Mandatory=$true)][string]$Destination,
    [int]$LeftPx = 0,
    [int]$TopPx = 0,
    [int]$Width = 400,
    [int]$Height = 0,
    [ValidateSet("None","Rotate90","Rotate180","Rotate270")][string]$Rotate = "Rotate270"
)
Add-Type -AssemblyName System.Drawing
$src = [System.Drawing.Image]::FromFile((Resolve-Path $Source).Path)
if ($Height -eq 0) { $Height = $src.Height - $TopPx }
$rect = New-Object System.Drawing.Rectangle($LeftPx, $TopPx, $Width, $Height)
$cropped = New-Object System.Drawing.Bitmap($Width, $Height)
$g = [System.Drawing.Graphics]::FromImage($cropped)
$g.DrawImage($src, (New-Object System.Drawing.Rectangle(0,0,$Width,$Height)), $rect, [System.Drawing.GraphicsUnit]::Pixel)
$g.Dispose()
switch ($Rotate) {
    "Rotate90"  { $cropped.RotateFlip([System.Drawing.RotateFlipType]::Rotate90FlipNone) }
    "Rotate180" { $cropped.RotateFlip([System.Drawing.RotateFlipType]::Rotate180FlipNone) }
    "Rotate270" { $cropped.RotateFlip([System.Drawing.RotateFlipType]::Rotate270FlipNone) }
}
$destPath = if ([System.IO.Path]::IsPathRooted($Destination)) { $Destination } else { Join-Path (Get-Location) $Destination }
$cropped.Save($destPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$cropped.Dispose()
$src.Dispose()
Write-Output "Saved $destPath ($Width x $Height, rotated $Rotate)"

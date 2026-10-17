# Lossless local derivation: only the generated doorway enters the accepted card.
# The full generated facade is reference material, never runtime authority.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$projectRoot = Split-Path $PSScriptRoot -Parent
$sourcePath = Join-Path $projectRoot 'assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png'
$generatedPath = Join-Path $projectRoot 'assets_src/sky_lagoon/castle_open_entrance_20261017/generated_open_castle.png'
$outputPath = Join-Path $projectRoot 'assets/sprites/sky_lagoon/sky_lagoon_castle_open_v1.png'
$source = [System.Drawing.Bitmap]::new($sourcePath)
$generated = [System.Drawing.Bitmap]::new($generatedPath)
$result = $source.Clone()
$graphics = [System.Drawing.Graphics]::FromImage($result)
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
# Trace the interior edge of the original doorway. The stone arch, threshold,
# bridge, stained glass and all surrounding source pixels remain untouched.
$coordinates = @(@(411,766),@(411,666),@(416,636),@(430,609),@(450,588),@(475,573),@(497,565),@(520,571),@(547,587),@(569,610),@(584,638),@(591,665),@(591,767))
$points = [System.Drawing.PointF[]]@($coordinates | ForEach-Object { [System.Drawing.PointF]::new($_[0], $_[1]) })
$clip = [System.Drawing.Drawing2D.GraphicsPath]::new()
$clip.AddPolygon($points)
$graphics.SetClip($clip)
$graphics.DrawImage($generated, [System.Drawing.Rectangle]::new(0,0,$source.Width,$source.Height))
$graphics.Dispose()
$result.Save($outputPath,[System.Drawing.Imaging.ImageFormat]::Png)
$clip.Dispose()
$source.Dispose()
$generated.Dispose()
$result.Dispose()
Write-Output $outputPath

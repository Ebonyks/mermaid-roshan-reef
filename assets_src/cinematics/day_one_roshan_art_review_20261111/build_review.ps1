param([string]$Root = $PSScriptRoot)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$geometry = Get-Content -LiteralPath (Join-Path $Root 'registration.json') -Raw | ConvertFrom-Json
$outlines = Get-Content -LiteralPath (Join-Path $Root 'references/fixture_outlines.json') -Raw | ConvertFrom-Json
$reference = Join-Path $Root 'references'
$takes = Join-Path $Root 'takes'
$art = Join-Path $Root 'art'
$evidence = Join-Path $Root 'evidence'
$dirty = Join-Path $reference 'dirty_room.png'
$clean = Join-Path $reference 'clean_room.png'
$sink = Join-Path $art 'sink_clean_registered.png'
$toilet = Join-Path $art 'toilet_clean_registered.png'
$water = Join-Path $art 'tub_water_registered.png'
$duck = Join-Path $art 'rubber_duck.png'

function Write-Png([string]$Path, [string[]]$ArgsForFfmpeg) {
    & ffmpeg -hide_banner -loglevel error -y -filter_threads 1 -filter_complex_threads 1 @ArgsForFfmpeg -frames:v 1 -threads 1 -pix_fmt rgba $Path
    if ($LASTEXITCODE) { throw "FFmpeg could not write $Path" }
}

function Write-Matte([string]$Path, [object[]]$Polygons, [double]$Inset) {
    $bitmap = [System.Drawing.Bitmap]::new(1024, 576)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
        $graphics.Clear([System.Drawing.Color]::Black)
        foreach ($polygon in $Polygons) {
            $cx = ($polygon | ForEach-Object { $_[0] } | Measure-Object -Average).Average
            $cy = ($polygon | ForEach-Object { $_[1] } | Measure-Object -Average).Average
            for ($i = 1; $i -le 20; $i++) {
                $scale = 1.0 - (1.0 - $Inset) * $i / 20
                $value = [int][Math]::Round(255 * $i / 20)
                $brush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb($value,$value,$value))
                try {
                    [System.Drawing.PointF[]]$points = @(foreach ($pair in $polygon) {
                        [System.Drawing.PointF]::new($cx + ($pair[0] - $cx) * $scale,
                            $cy + ($pair[1] - $cy) * $scale)
                    })
                    $graphics.FillPolygon($brush, $points)
                } finally { $brush.Dispose() }
            }
        }
        $bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    } finally {
        $graphics.Dispose()
        $bitmap.Dispose()
    }
}

$sinkMatte = Join-Path $evidence 'sink_matte.png'
$toiletMatte = Join-Path $evidence 'toilet_matte.png'
$tubMatte = Join-Path $evidence 'tub_interior_matte.png'
$toiletWaterMatte = Join-Path $evidence 'toilet_water_matte.png'
Write-Matte $sinkMatte @($outlines.sink,$geometry.faucet) $geometry.fixture_mask.sink_inset
Write-Matte $toiletMatte @(,$outlines.toilet) $geometry.fixture_mask.toilet_inset
Write-Matte $tubMatte @(,$geometry.tub_water) .975
Write-Matte $toiletWaterMatte @(,$geometry.toilet_water) .89

# Apply the clean finish as a color-only change to the exact dirty geometry.
# The oversized ImageGen crop is a finish reference. Its shifted contours
# are never sampled. The toilet uses only a small clean water paint chip.
Write-Png $sink @('-i',$dirty,'-i',$sinkMatte,'-filter_complex',
    '[0:v]eq=contrast=1.025:brightness=0.040:saturation=1.16,format=rgba[rgb];[1:v]format=gray[a];[rgb][a]alphamerge')
Write-Png $toilet @('-i',$dirty,'-i',(Join-Path $takes 'toilet_take01.png'),'-i',$toiletWaterMatte,'-i',$toiletMatte,'-filter_complex',
    '[0:v]eq=contrast=1.025:brightness=0.055:saturation=1.19,format=rgba[base];[1:v]crop=200:13:385:731,scale=54:13:flags=lanczos,pad=1024:576:802:252:color=black,format=rgba[w];[2:v]format=gray[wm];[w][wm]alphamerge[water];[base][water]overlay=0:0:format=rgb[paint];[3:v]format=gray[fm];[paint][fm]alphamerge')
Write-Png $water @('-i',$clean,'-i',$tubMatte,'-filter_complex',
    '[0:v]crop=111:20:166:233,scale=252:36:flags=lanczos,pad=1024:576:109:232:color=black,format=rgba[w];[1:v]format=gray[a];[w][a]alphamerge')
Write-Png $duck @('-i',(Join-Path $reference 'duck_sheet.png'),'-vf',
    'crop=176:165:39:90,format=rgba,scale=88:83:flags=lanczos,pad=92:87:2:2:color=0x00000000')

Write-Png (Join-Path $art 'shoulder_screen_left.png') @('-i',(Join-Path $reference 'atlas_shoulder.png'),
    '-vf','crop=150:108:424:333')
Write-Png (Join-Path $art 'shoulder_screen_right.png') @('-i',(Join-Path $reference 'atlas_shoulder.png'),
    '-vf','crop=130:124:568:337')

function Crop-Filter([object[]]$Rect) {
    'crop={0}:{1}:{2}:{3}' -f $Rect[2],$Rect[3],$Rect[0],$Rect[1]
}
$alpha = "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='clip((alpha(X,Y)-8)*255/245,0,255)'"
foreach ($entry in $geometry.hands) {
    $name,$rect,$wrist = $entry
    $scale = $geometry.hand_scale
    $width = [int][Math]::Round($rect[2] * $scale)
    $height = [int][Math]::Round($rect[3] * $scale)
    $x = $geometry.hand_anchor[0] - [int][Math]::Round(($wrist[0] - $rect[0]) * $scale)
    $y = $geometry.hand_anchor[1] - [int][Math]::Round(($wrist[1] - $rect[1]) * $scale)
    $filter = "{0},format=rgba,{1},scale={2}:{3}:flags=lanczos,pad=128:128:{4}:{5}:color=0x00000000" -f (Crop-Filter $rect),$alpha,$width,$height,$x,$y
    Write-Png (Join-Path $art "hand_$name.png") @('-i',(Join-Path $takes 'hands_take01.png'),'-vf',$filter)
}

$softPatch = "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='clip((alpha(X,Y)-8)*255/245,0,255)*clip(min(min(X,Y),min(W-1-X,H-1-Y))/8,0,1)'"
foreach ($entry in $geometry.features) {
    $name,$rect = $entry
    $filter = "{0},format=rgba,{1}" -f (Crop-Filter $rect),$softPatch
    Write-Png (Join-Path $art "face_$name.png") @('-i',(Join-Path $takes 'face_take01.png'),'-vf',$filter)
}
foreach ($entry in $geometry.underlays) {
    $name,$rect = $entry
    $filter = "{0},format=rgba,{1},scale=iw/2:ih/2:flags=lanczos" -f (Crop-Filter $rect),$alpha
    Write-Png (Join-Path $art "$name.png") @('-i',(Join-Path $takes 'neck_take01.png'),'-vf',$filter)
}
Write-Png (Join-Path $evidence 'bathroom_registered_preview.png') @('-i',$dirty,'-i',$sink,'-i',$toilet,'-i',$water,'-i',$duck,'-filter_complex',
    '[0:v][1:v]overlay=0:0:format=rgb[a];[a][2:v]overlay=0:0:format=rgb[b];[b][3:v]overlay=0:0:format=rgb[c];[4:v]scale=22:21:flags=lanczos[d];[c][d]overlay=285:231:format=rgb')
Write-Png (Join-Path $evidence 'grime_reuse_preview.png') @('-i',(Join-Path $evidence 'bathroom_registered_preview.png'),
    '-i',(Join-Path $reference 'sink_grime.png'),'-i',(Join-Path $reference 'tub_grime.png'),'-filter_complex',
    '[1:v]format=rgba,colorchannelmixer=aa=0.74,split[sg][tg];[sg]scale=92:30[s];[tg]scale=48:18[t];[2:v]format=rgba,colorchannelmixer=aa=0.74,scale=133:43[u];[0:v][s]overlay=514:182:format=rgb[a];[a][u]overlay=183:219:format=rgb[b];[b][t]overlay=808:250:format=rgb')
Write-Output "Built registered room overlays, reusable duck, six hands, seven facial donors, and two hidden joint donors."

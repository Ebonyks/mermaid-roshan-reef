param([string]$AsepritePath = 'C:\Program Files\Aseprite\Aseprite.exe')
$ErrorActionPreference = 'Stop'
$taskRepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../..')).Path
$taskPreviousLocation = Get-Location
if (-not (Test-Path -LiteralPath $AsepritePath -PathType Leaf)) { throw 'Native Aseprite is required; do not substitute image generation for sprite repairs.' }
try {
 Set-Location -LiteralPath $taskRepoRoot
 $taskSteps = @(
  @('export_baby_eagle.lua', ''),
  @('recover_furniture_sources.lua', 'FURNITURE_RECOVERY.json'),
  @('repair_castle_sprite_pixels.lua', 'PIXEL_EDITS.json'),
  @('repack_roshan_frames.lua', 'ROSHAN_REPACK.json'),
  @('recover_crossing_cells.lua', 'CELL_RECOVERY.json'),
  @('recover_blocks.lua', 'BLOCKS_RECOVERY.json'),
  @('register_repaired_cells.lua', 'REGISTRATION.json'),
  @('repair_rumi_transparency.lua', '')
 )
 foreach ($taskStep in $taskSteps) {
  $taskArguments = @('-b')
  if ($taskStep[1]) { $taskArguments += @('--script-param', ('spec=assets_src/repairs/visual_polish_2026-09-26/' + $taskStep[1])) }
  $taskArguments += @('--script', ('tools/aseprite/' + $taskStep[0]))
  $taskProcess = Start-Process -FilePath $AsepritePath -ArgumentList $taskArguments -WindowStyle Hidden -Wait -PassThru
  if ($taskProcess.ExitCode -ne 0) { throw ('Aseprite failed: ' + $taskStep[0]) }
 }
 # Verification must match the reviewed records; never auto-accept new hashes.
 python tools/build_baby_eagle_cutout.py --check
 if ($LASTEXITCODE -ne 0) { throw 'Eagle provenance drift' }
 python tools/audit_visual_pixel_repairs.py
 if ($LASTEXITCODE -ne 0) { throw 'Pixel/source provenance drift' }
 python tools/normalize_castle_interaction_v2_sheets.py --check
 if ($LASTEXITCODE -ne 0) { throw 'Frame placement drift' }
 Write-Output 'ASEPRITE_VISUAL_REBUILD|ALL OK'
} finally {
 Set-Location -LiteralPath $taskPreviousLocation.Path
}

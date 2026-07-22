param(
	[switch]$Strict
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$concept = Join-Path $repo "assets_src\concepts\ember_fortress_claude_2026-07-22"
$expansion = Join-Path $concept "expansion_40"
$handoff = Join-Path $repo "CLAUDE_EMBER_FORTRESS_BLENDER_HANDOFF_2026-07-22.md"
$ledger = Join-Path $repo "audit\ember_visual_inventory_2026-07-22.csv"
$manifest = Join-Path $concept "CLAUDE_EXPORT_MANIFEST.csv"
$expansionLedger = Join-Path $repo "audit\ember_expansion_inventory_2026-07-22.csv"
$expansionManifest = Join-Path $expansion "CLAUDE_EXPANSION_40_MANIFEST.csv"
$expectedBoards = @(
	"01_world_layout.png",
	"02_citadel_architecture.png",
	"03_landmark_turnarounds.png",
	"04_overworld_props.png",
	"05_dungeon_kit.png",
	"06_combat_kit.png"
)

foreach ($path in @($handoff, $ledger, $manifest, $expansionLedger, $expansionManifest)) {
	if (-not (Test-Path -LiteralPath $path)) {
		throw "Missing required handoff file: $path"
	}
}

Add-Type -AssemblyName System.Drawing
$boardReport = @()
foreach ($name in $expectedBoards) {
	$path = Join-Path $concept $name
	if (-not (Test-Path -LiteralPath $path)) {
		throw "Missing concept board: $path"
	}
	$image = [System.Drawing.Image]::FromFile($path)
	try {
		$longest = [Math]::Max($image.Width, $image.Height)
		$boardReport += [PSCustomObject]@{
			Name = $name
			Dimensions = "$($image.Width)x$($image.Height)"
			Longest = $longest
		}
		if ($Strict -and $longest -gt 1024) {
			throw "Concept board exceeds 1024px rule: $name ($longest px)"
		}
	} finally {
		$image.Dispose()
	}
}

$expansionCards = @(Get-ChildItem -LiteralPath $expansion -Filter "*.png" |
	Where-Object { $_.BaseName -match '^\d{2}_' } |
	Sort-Object Name)
$expansionContacts = @(Get-ChildItem -LiteralPath $expansion -Filter "contact_*.png" |
	Sort-Object Name)
if ($Strict -and $expansionCards.Count -ne 40) {
	throw "Expected 40 expansion cards, found $($expansionCards.Count)"
}
if ($Strict -and $expansionContacts.Count -ne 4) {
	throw "Expected 4 expansion contact sheets, found $($expansionContacts.Count)"
}
foreach ($file in @($expansionCards + $expansionContacts)) {
	$image = [System.Drawing.Image]::FromFile($file.FullName)
	try {
		$longest = [Math]::Max($image.Width, $image.Height)
		if ($Strict -and $longest -gt 1024) {
			throw "Expansion image exceeds 1024px rule: $($file.Name) ($longest px)"
		}
	} finally {
		$image.Dispose()
	}
}

$inventory = @(Import-Csv -LiteralPath $ledger)
$exports = @(Import-Csv -LiteralPath $manifest)
$expansionInventory = @(Import-Csv -LiteralPath $expansionLedger)
$expansionExports = @(Import-Csv -LiteralPath $expansionManifest)
if ($Strict -and $inventory.Count -ne 42) {
	throw "Expected 42 inventory roles, found $($inventory.Count)"
}
if ($Strict -and $exports.Count -ne 39) {
	throw "Expected 39 Blender exports, found $($exports.Count)"
}
if ($Strict -and $expansionInventory.Count -ne 40) {
	throw "Expected 40 expansion roles, found $($expansionInventory.Count)"
}
if ($Strict -and $expansionExports.Count -ne 40) {
	throw "Expected 40 expansion Blender exports, found $($expansionExports.Count)"
}

$premature = @(Get-ChildItem -LiteralPath (Join-Path $repo "assets\ember_fortress") -Filter *.glb -ErrorAction SilentlyContinue)
if ($Strict -and $premature.Count -gt 0) {
	throw "Concept branch contains premature Ember GLBs; start Claude Blender work on its own branch"
}

$branch = (git -C $repo branch --show-current).Trim()
$head = (git -C $repo rev-parse --short HEAD).Trim()
$status = @(git -C $repo status --short)

Write-Output "Claude Ember Fortress Blender handoff"
Write-Output "Repository: $repo"
Write-Output "Branch: $branch"
Write-Output "HEAD: $head"
Write-Output "Concept boards: $($boardReport.Count)"
$boardReport | Format-Table -AutoSize | Out-String | Write-Output
Write-Output "Inventory roles: $($inventory.Count)"
Write-Output "Expansion cards: $($expansionCards.Count)"
Write-Output "Expansion contact sheets: $($expansionContacts.Count)"
Write-Output "Expansion roles: $($expansionInventory.Count)"
Write-Output "Required Blender exports: $($exports.Count + $expansionExports.Count) (core $($exports.Count) + expansion $($expansionExports.Count))"
Write-Output "Premature runtime GLBs: $($premature.Count)"
Write-Output "Worktree status:"
if ($status.Count -eq 0) {
	Write-Output "(clean)"
} else {
	$status | Write-Output
}
Write-Output ""
Get-Content -LiteralPath $handoff

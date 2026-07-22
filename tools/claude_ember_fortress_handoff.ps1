[CmdletBinding()]
param(
	[switch]$Strict
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)

$repoRoot = Split-Path -Parent $PSScriptRoot
$handoffPath = Join-Path $repoRoot "CLAUDE_EMBER_FORTRESS_GRAPHICS_HANDOFF_2026-07-21.md"
$ledgerPath = Join-Path $repoRoot "audit/ember_visual_inventory_2026-07-21.csv"
$runtimeEvidence = Join-Path $repoRoot "audit/ember_runtime_2026-07-21"
$assetDir = Join-Path $repoRoot "assets/ember_fortress"
$expectedBranch = "codex/bowser-world-graphics"

foreach ($required in @($handoffPath, $ledgerPath, $runtimeEvidence, $assetDir)) {
	if (-not (Test-Path -LiteralPath $required)) {
		throw "Missing handoff dependency: $required"
	}
}

$branch = (git -c core.excludesFile= -C $repoRoot branch --show-current).Trim()
if ($LASTEXITCODE -ne 0) {
	throw "Unable to read the Git branch for $repoRoot"
}

$head = (git -c core.excludesFile= -C $repoRoot rev-parse --short HEAD).Trim()
if ($LASTEXITCODE -ne 0) {
	throw "Unable to read HEAD for $repoRoot"
}

$statusLines = @(git -c core.excludesFile= -C $repoRoot status --short)
if ($LASTEXITCODE -ne 0) {
	throw "Unable to read the worktree status for $repoRoot"
}

if ($branch -ne $expectedBranch) {
	$message = "Expected branch '$expectedBranch', found '$branch'. Do not apply this handoff from the wrong checkout."
	if ($Strict) {
		throw $message
	}
	Write-Warning $message
}

$statusText = if ($statusLines.Count -eq 0) {
	"(clean)"
} else {
	$statusLines -join [Environment]::NewLine
}

$assetCount = @(Get-ChildItem -LiteralPath $assetDir -Filter "*.glb" -File).Count
$captureCount = @(Get-ChildItem -LiteralPath $runtimeEvidence -Filter "*.png" -File |
	Where-Object { $_.Name -ne "contact_mobile.png" }).Count
$ledgerRows = @(Import-Csv -LiteralPath $ledgerPath).Count

if ($Strict -and ($assetCount -ne 39 -or $captureCount -ne 10 -or $ledgerRows -ne 42)) {
	throw "Handoff evidence mismatch: assets=$assetCount captures=$captureCount ledger_rows=$ledgerRows"
}

$handoff = Get-Content -LiteralPath $handoffPath -Raw -Encoding UTF8

@"
You are continuing the Mermaid Roshan: Reef of Light Ember Fortress graphics pass.

Repository: $repoRoot
Expected branch: $expectedBranch
Current branch: $branch
Current HEAD: $head
Kit GLBs: $assetCount (expected 39)
Runtime captures: $captureCount (expected 10, excluding contact sheet)
Inventory roles: $ledgerRows (expected 42)

Current worktree status:
$statusText

Follow the complete continuation contract below. Do not weaken probes, do not
introduce branded IP, and do not claim a score above the available Mobile
runtime evidence.

$handoff
"@

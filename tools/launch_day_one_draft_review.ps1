[CmdletBinding()]
param(
	[string]$GodotPath,
	[switch]$DryRun,
	[switch]$Visible
)

$projectPath = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($GodotPath)) {
	$candidates = @(
		(Join-Path $projectPath 'tmp/godot472_handoff_validation/Godot_v4.7.2-stable_win64_console.exe'),
		(Join-Path $projectPath '../../tmp/godot472_handoff_validation/Godot_v4.7.2-stable_win64_console.exe'),
		(Join-Path $projectPath 'Godot_v4.7.2-stable_win64_console.exe'),
		'Godot_v4.7.2-stable_win64_console.exe'
	)
	$GodotPath = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
}
if ([string]::IsNullOrWhiteSpace($GodotPath) -or -not (Test-Path -LiteralPath $GodotPath)) {
	throw 'Godot 4.7.2-stable executable was not found. Pass -GodotPath explicitly.'
}
$engineVersion = (& $GodotPath --version | Select-Object -First 1)
if ($engineVersion -notmatch '^4\.7\.2\.stable\.') {
	throw "Exact Godot 4.7.2-stable is required; got $engineVersion"
}

# The project has no --probe-user-root command-line contract. Isolate the
# Windows Godot app-data root instead of touching the child's normal save.
$reviewRoot = Join-Path ([IO.Path]::GetTempPath()) ('reef-day-one-draft-review-' + [guid]::NewGuid().ToString('N'))
$draftArgs = @('--path', ('"' + $projectPath + '"'), '--rendering-method', 'mobile', '--', '--day-one-draft-movies')
$display = if ($Visible) { 'Normal' } else { 'Hidden' }
Write-Output ('Godot=' + (Resolve-Path -LiteralPath $GodotPath).Path)
Write-Output ('Project=' + (Resolve-Path -LiteralPath $projectPath).Path)
Write-Output ('IsolatedAppData=' + $reviewRoot)
Write-Output ('Args=' + ($draftArgs -join ' '))
if ($DryRun) { return }

New-Item -ItemType Directory -Path $reviewRoot -Force | Out-Null
$oldAppData = $env:APPDATA
$oldLocalAppData = $env:LOCALAPPDATA
try {
	$env:APPDATA = $reviewRoot
	$env:LOCALAPPDATA = $reviewRoot
	Start-Process -FilePath (Resolve-Path -LiteralPath $GodotPath).Path `
		-ArgumentList $draftArgs -WorkingDirectory $projectPath -WindowStyle $display
}
finally {
	$env:APPDATA = $oldAppData
	$env:LOCALAPPDATA = $oldLocalAppData
}

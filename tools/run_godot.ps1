param([Parameter(ValueFromRemainingArguments = $true)][string[]]$GodotArguments)
$ErrorActionPreference = 'Stop'
$reefRoot = Split-Path -Parent $PSScriptRoot
$reefGodot = & python -B (Join-Path $PSScriptRoot 'resolve_godot.py')
if ($LASTEXITCODE -ne 0) { throw 'No exact approved stable Godot executable is available.' }
& $reefGodot --path $reefRoot @GodotArguments
exit $LASTEXITCODE

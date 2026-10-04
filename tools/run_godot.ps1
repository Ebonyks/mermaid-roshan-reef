# Launch the exact approved Godot build with this project's path.
# No param() block on purpose: an advanced-script parameter binds Godot's -d, -v
# and -e flags to PowerShell's common parameters (-Debug, -Verbose, -ErrorAction).
$ErrorActionPreference = 'Stop'
$reefRoot = Split-Path -Parent $PSScriptRoot
$reefGodot = & python -B (Join-Path $PSScriptRoot 'resolve_godot.py')
if ($LASTEXITCODE -ne 0) { throw 'No exact approved stable Godot executable is available.' }
& $reefGodot --path $reefRoot @args
exit $LASTEXITCODE

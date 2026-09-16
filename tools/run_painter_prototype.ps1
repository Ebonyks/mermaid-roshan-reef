param(
    [string]$GodotPath = (Join-Path $env:LOCALAPPDATA 'Programs\MermaidReefTools\Godot\4.7.2\godot_console.exe'),
    [switch]$FreePaint
)
$ErrorActionPreference = 'Stop'
$painterRoot = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path -LiteralPath $GodotPath -PathType Leaf)) {
    throw 'Godot 4.7.2-stable is required. Pass its executable using -GodotPath.'
}
$painterVersion = (& $GodotPath --version | Out-String).Trim()
if ($painterVersion -ne '4.7.2.stable.official.ed1daf0bf') {
    throw "Expected official Godot 4.7.2; found $painterVersion"
}
$painterArguments = @('--path', $painterRoot, '--windowed', '--resolution', '1280x720', 'scenes/painter_prototype.tscn')
if ($FreePaint) { $painterArguments += @('--', '--free-paint') }
& $GodotPath @painterArguments
exit $LASTEXITCODE

$ErrorActionPreference = "Stop"

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$source = Join-Path $PSScriptRoot "assets"

Get-ChildItem -LiteralPath $source -File -Recurse | ForEach-Object {
	$relative = [System.IO.Path]::GetRelativePath($source, $_.FullName)
	$destination = Join-Path (Join-Path $repo "assets") $relative
	New-Item -ItemType Directory -Force -Path (Split-Path $destination) | Out-Null
	Copy-Item -LiteralPath $_.FullName -Destination $destination -Force
	Write-Host "restored assets/$($relative.Replace('\', '/'))"
}

[CmdletBinding()]
param(
	[switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

trap {
	[Console]::Error.WriteLine("error: $($_.Exception.Message)")
	exit 2
}

# FFmpeg's official download page lists gyan.dev as a Windows binary provider.
# Keep this version and checksum pinned so a moving "latest" archive can never be
# installed silently.
$ffmpegVersion = "8.1.2"
$archiveName = "ffmpeg-$ffmpegVersion-essentials_build.zip"
$archiveUrl = "https://www.gyan.dev/ffmpeg/builds/packages/$archiveName"
$expectedSha256 = "db580001caa24ac104c8cb856cd113a87b0a443f7bdf47d8c12b1d740584a2ec"

$repoRoot = Split-Path -Parent $PSScriptRoot
$toolRoot = Join-Path $repoRoot ".video-tools"
$downloadRoot = Join-Path $toolRoot "downloads"
$installName = "ffmpeg-$ffmpegVersion-essentials_build"
$installRoot = Join-Path $toolRoot $installName
$ffmpegExe = Join-Path $installRoot "bin\ffmpeg.exe"
$ffprobeExe = Join-Path $installRoot "bin\ffprobe.exe"
$archivePath = Join-Path $downloadRoot $archiveName
$partialPath = "$archivePath.part"

function Test-ExpectedArchive {
	param([Parameter(Mandatory = $true)][string]$Path)

	if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
		return $false
	}
	$actualSha256 = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
	return $actualSha256 -eq $expectedSha256
}

if ((Test-Path -LiteralPath $ffmpegExe -PathType Leaf) -and
		(Test-Path -LiteralPath $ffprobeExe -PathType Leaf) -and
		-not $Force) {
	Write-Host "FFmpeg $ffmpegVersion is already installed locally:"
	Write-Host "  $ffmpegExe"
	& $ffmpegExe -hide_banner -version | Select-Object -First 1
	exit 0
}

if ((Test-Path -LiteralPath $installRoot) -and -not $Force) {
	throw "The local FFmpeg directory is incomplete. Re-run with -Force to replace it: $installRoot"
}

New-Item -ItemType Directory -Path $downloadRoot -Force | Out-Null

if (-not (Test-ExpectedArchive -Path $archivePath)) {
	if (Test-Path -LiteralPath $archivePath -PathType Leaf) {
		Remove-Item -LiteralPath $archivePath -Force
	}
	if (Test-Path -LiteralPath $partialPath -PathType Leaf) {
		Remove-Item -LiteralPath $partialPath -Force
	}

	Write-Host "Downloading pinned FFmpeg $ffmpegVersion essentials build..."
	Invoke-WebRequest -Uri $archiveUrl -OutFile $partialPath -UseBasicParsing

	$actualSha256 = (Get-FileHash -LiteralPath $partialPath -Algorithm SHA256).Hash.ToLowerInvariant()
	if ($actualSha256 -ne $expectedSha256) {
		Remove-Item -LiteralPath $partialPath -Force
		throw "FFmpeg archive checksum mismatch. Expected $expectedSha256 but received $actualSha256."
	}
	Move-Item -LiteralPath $partialPath -Destination $archivePath
} else {
	Write-Host "Using the verified cached archive:"
	Write-Host "  $archivePath"
}

if (Test-Path -LiteralPath $installRoot) {
	$resolvedToolRoot = (Resolve-Path -LiteralPath $toolRoot).Path
	$resolvedInstallRoot = (Resolve-Path -LiteralPath $installRoot).Path
	if (-not $resolvedInstallRoot.StartsWith($resolvedToolRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
		throw "Refusing to replace a directory outside the repository-local tool root: $resolvedInstallRoot"
	}
	Remove-Item -LiteralPath $resolvedInstallRoot -Recurse -Force
}

$extractRoot = Join-Path $toolRoot ".extract-$PID"
if (Test-Path -LiteralPath $extractRoot) {
	Remove-Item -LiteralPath $extractRoot -Recurse -Force
}

try {
	Write-Host "Extracting FFmpeg into .video-tools..."
	Expand-Archive -LiteralPath $archivePath -DestinationPath $extractRoot -Force
	$expandedRoot = Join-Path $extractRoot $installName
	if (-not (Test-Path -LiteralPath (Join-Path $expandedRoot "bin\ffmpeg.exe") -PathType Leaf)) {
		throw "The verified FFmpeg archive did not contain the expected directory: $installName"
	}
	Move-Item -LiteralPath $expandedRoot -Destination $installRoot
} finally {
	if (Test-Path -LiteralPath $extractRoot) {
		Remove-Item -LiteralPath $extractRoot -Recurse -Force
	}
}

$encoderList = (& $ffmpegExe -hide_banner -encoders 2>&1) -join "`n"
foreach ($encoder in @("libtheora", "libvorbis", "libx264")) {
	if ($encoderList -notmatch "(?m)\b$encoder\b") {
		throw "The installed FFmpeg build is missing the required $encoder encoder."
	}
}

Write-Host ""
Write-Host "Local video tools are ready:"
Write-Host "  $ffmpegExe"
Write-Host "  $ffprobeExe"
Write-Host ""
Write-Host "Next:"
Write-Host "  tools\encode_cartoon.cmd <frames> build/cartoons/cartoon.ogv -ReviewMp4"

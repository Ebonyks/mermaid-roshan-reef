<#
.SYNOPSIS
Encodes cartoon frames or an existing video into a Godot-ready OGV.

.DESCRIPTION
The output extension selects the primary format. Use .ogv for Ogg Theora
playback in Godot 4.4, or .mp4 for an H.264 review copy. A frame directory is
naturally sorted and defaults to 18 fps. Source files are never modified.

.PARAMETER InputPath
A directory of same-format image frames, or an existing FFmpeg-readable video.

.PARAMETER OutputPath
The primary .ogv or .mp4 output path.

.PARAMETER Fps
Frame rate. Frame directories default to 18; existing videos preserve their
source rate unless this is supplied.

.PARAMETER Size
Even WIDTHxHEIGHT output dimensions, or "source". The default is 1280x720.

.PARAMETER Audio
An audio file to add to a frame sequence or use instead of source-video audio.

.PARAMETER NoAudio
Writes video without audio.

.PARAMETER ReviewMp4
Also writes an H.264 MP4 next to a primary OGV.

.PARAMETER Overwrite
Deliberately replaces existing output files.

.PARAMETER DryRun
Prints the FFmpeg command without writing video.

.EXAMPLE
.\tools\encode_cartoon.ps1 frames build\cartoons\opening.ogv -Fps 18 -ReviewMp4

.EXAMPLE
.\tools\encode_cartoon.ps1 draft.mp4 build\cartoons\draft.ogv
#>
[CmdletBinding()]
param(
	[Parameter(Position = 0)]
	[string]$InputPath,

	[Parameter(Position = 1)]
	[string]$OutputPath,

	[ValidateRange(0, 240)]
	[double]$Fps = 0,

	[string]$Size = "1280x720",

	[string]$Audio,

	[switch]$NoAudio,

	[switch]$ReviewMp4,

	[ValidateRange(1, 10)]
	[int]$OgvQuality = 6,

	[ValidateRange(0, 51)]
	[int]$Mp4Crf = 18,

	[switch]$Overwrite,

	[switch]$DryRun,

	[Alias("?")]
	[switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

trap {
	[Console]::Error.WriteLine("error: $($_.Exception.Message)")
	exit 2
}

if ($Help) {
	Get-Help $PSCommandPath -Detailed
	exit 0
}
if (-not $InputPath -or -not $OutputPath) {
	throw "Usage: tools\encode_cartoon.cmd <frames-or-video> <output.ogv|output.mp4> [-ReviewMp4]"
}

$frameExtensions = @(".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp")
$localFfmpegVersion = "8.1.2"
$defaultFrameRate = 18.0
$repoRoot = Split-Path -Parent $PSScriptRoot

function Resolve-OutputFile {
	param([Parameter(Mandatory = $true)][string]$Path)

	if ([System.IO.Path]::IsPathRooted($Path)) {
		return [System.IO.Path]::GetFullPath($Path)
	}
	return [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $Path))
}

function Find-VideoTool {
	param(
		[Parameter(Mandatory = $true)][string]$Name,
		[string]$SiblingOf
	)

	$environmentName = "MERMAID_$($Name.ToUpperInvariant())"
	$configured = [Environment]::GetEnvironmentVariable($environmentName)
	if ($configured) {
		$configuredPath = [System.IO.Path]::GetFullPath(
			[Environment]::ExpandEnvironmentVariables($configured)
		)
		if (Test-Path -LiteralPath $configuredPath -PathType Leaf) {
			return $configuredPath
		}
		throw "$environmentName does not point to a file: $configuredPath"
	}

	if ($SiblingOf) {
		$sibling = Join-Path (Split-Path -Parent $SiblingOf) "$Name.exe"
		if (Test-Path -LiteralPath $sibling -PathType Leaf) {
			return (Resolve-Path -LiteralPath $sibling).Path
		}
	}

	$preferred = Join-Path $repoRoot (
		".video-tools\ffmpeg-$localFfmpegVersion-essentials_build\bin\$Name.exe"
	)
	if (Test-Path -LiteralPath $preferred -PathType Leaf) {
		return (Resolve-Path -LiteralPath $preferred).Path
	}

	$localBuilds = @(
		Get-ChildItem -LiteralPath (Join-Path $repoRoot ".video-tools") `
			-Directory -Filter "ffmpeg-*-essentials_build" -ErrorAction SilentlyContinue |
			Sort-Object Name -Descending
	)
	foreach ($build in $localBuilds) {
		$candidate = Join-Path $build.FullName "bin\$Name.exe"
		if (Test-Path -LiteralPath $candidate -PathType Leaf) {
			return $candidate
		}
	}

	$onPath = Get-Command $Name -CommandType Application -ErrorAction SilentlyContinue
	if ($onPath) {
		return $onPath.Source
	}

	throw "Could not find $Name. Run .\tools\setup_video_tools.ps1 first."
}

function Get-NaturalSortKey {
	param([Parameter(Mandatory = $true)][string]$Name)

	return [regex]::Replace(
		$Name.ToLowerInvariant(),
		"\d+",
		{ param($match) $match.Value.PadLeft(24, "0") }
	)
}

function Get-FrameFiles {
	param([Parameter(Mandatory = $true)][string]$Directory)

	$frames = @(
		Get-ChildItem -LiteralPath $Directory -File |
			Where-Object { $frameExtensions -contains $_.Extension.ToLowerInvariant() } |
			Sort-Object @{ Expression = { Get-NaturalSortKey -Name $_.Name } }
	)
	if ($frames.Count -eq 0) {
		throw "No supported frames found in $Directory ($($frameExtensions -join ', '))."
	}

	$suffixes = @($frames | ForEach-Object { $_.Extension.ToLowerInvariant() } | Select-Object -Unique)
	if ($suffixes.Count -ne 1) {
		throw "Frame directories must use one image format. Found: $($suffixes -join ', ')"
	}
	return $frames
}

function New-FrameStage {
	param(
		[Parameter(Mandatory = $true)][object[]]$Frames,
		[Parameter(Mandatory = $true)][string]$Directory
	)

	$extension = $Frames[0].Extension.ToLowerInvariant()
	for ($index = 0; $index -lt $Frames.Count; $index++) {
		$destination = Join-Path $Directory ("frame_{0:D8}{1}" -f ($index + 1), $extension)
		try {
			New-Item -ItemType HardLink -Path $destination -Target $Frames[$index].FullName `
				-ErrorAction Stop | Out-Null
		} catch {
			Copy-Item -LiteralPath $Frames[$index].FullName -Destination $destination
		}
	}
	return (Join-Path $Directory "frame_%08d$extension")
}

function Get-VideoFilter {
	param(
		[string]$RequestedSize,
		[double]$RequestedFps,
		[bool]$IncludeFps
	)

	$filters = @()
	if ($IncludeFps -and $RequestedFps -gt 0) {
		$filters += "fps=$($RequestedFps.ToString('0.########', [Globalization.CultureInfo]::InvariantCulture))"
	}

	if ($RequestedSize.ToLowerInvariant() -eq "source") {
		$filters += "pad=ceil(iw/2)*2:ceil(ih/2)*2"
	} else {
		if ($RequestedSize -notmatch "^(\d+)[xX](\d+)$") {
			throw "Size must be WIDTHxHEIGHT (for example 1280x720) or source."
		}
		$width = [int]$Matches[1]
		$height = [int]$Matches[2]
		if ($width -lt 2 -or $height -lt 2 -or $width % 2 -ne 0 -or $height % 2 -ne 0) {
			throw "Video width and height must be even numbers of at least 2."
		}
		$filters += "scale=${width}:${height}:force_original_aspect_ratio=decrease:flags=lanczos"
		$filters += "pad=${width}:${height}:(ow-iw)/2:(oh-ih)/2:color=black"
	}
	$filters += "setsar=1"
	return ($filters -join ",")
}

function Get-VideoCodecArguments {
	param([Parameter(Mandatory = $true)][string]$Destination)

	$extension = [System.IO.Path]::GetExtension($Destination).ToLowerInvariant()
	if ($extension -eq ".ogv") {
		return @(
			"-c:v", "libtheora",
			"-q:v", "$OgvQuality",
			"-g:v", "64",
			"-pix_fmt", "yuv420p"
		)
	}
	if ($extension -eq ".mp4") {
		return @(
			"-c:v", "libx264",
			"-preset", "medium",
			"-crf", "$Mp4Crf",
			"-pix_fmt", "yuv420p",
			"-movflags", "+faststart"
		)
	}
	throw "Output must end in .ogv or .mp4."
}

function Get-AudioCodecArguments {
	param([Parameter(Mandatory = $true)][string]$Destination)

	if ([System.IO.Path]::GetExtension($Destination).ToLowerInvariant() -eq ".ogv") {
		return @("-c:a", "libvorbis", "-q:a", "6", "-ac", "2")
	}
	return @("-c:a", "aac", "-b:a", "160k", "-ac", "2")
}

function New-EncoderArguments {
	param(
		[Parameter(Mandatory = $true)][string]$Source,
		[Parameter(Mandatory = $true)][string]$Destination,
		[string]$FramePattern,
		[Nullable[double]]$FrameDuration
	)

	$commandArguments = @(
		"-hide_banner",
		"-loglevel", "warning",
		"-stats",
		$(if ($Overwrite) { "-y" } else { "-n" })
	)

	if ($FramePattern) {
		$fpsText = $Fps.ToString("0.########", [Globalization.CultureInfo]::InvariantCulture)
		$commandArguments += @(
			"-framerate", $fpsText,
			"-start_number", "1",
			"-i", $FramePattern
		)
	} else {
		$commandArguments += @("-i", $Source)
	}

	$externalAudioIndex = $null
	if ($script:audioPath) {
		$externalAudioIndex = 1
		$commandArguments += @("-i", $script:audioPath)
	}

	$commandArguments += @("-map", "0:v:0")
	$audioIndex = $null
	if (-not $NoAudio) {
		if ($null -ne $externalAudioIndex) {
			$audioIndex = $externalAudioIndex
		} elseif (-not $FramePattern) {
			$audioIndex = 0
		}
	}

	if ($null -eq $audioIndex) {
		$commandArguments += "-an"
	} else {
		$commandArguments += @("-map", "${audioIndex}:a:0?")
	}

	$includeFpsFilter = (-not $FramePattern) -and $Fps -gt 0
	$commandArguments += @(
		"-vf", (Get-VideoFilter -RequestedSize $Size -RequestedFps $Fps `
			-IncludeFps $includeFpsFilter)
	)
	$commandArguments += Get-VideoCodecArguments -Destination $Destination

	if ($null -ne $audioIndex) {
		$commandArguments += Get-AudioCodecArguments -Destination $Destination
		if ($script:audioPath) {
			$commandArguments += @("-af", "apad", "-shortest")
		}
	}

	if ($null -ne $FrameDuration) {
		$durationText = ([double]$FrameDuration).ToString(
			"0.#########",
			[Globalization.CultureInfo]::InvariantCulture
		)
		$commandArguments += @("-t", $durationText, "-fps_mode", "cfr")
	}

	$commandArguments += @(
		"-map_metadata", "-1",
		"-map_chapters", "-1",
		"-color_primaries", "bt709",
		"-color_trc", "bt709",
		"-colorspace", "bt709",
		$Destination
	)
	return $commandArguments
}

function Format-CommandLine {
	param(
		[Parameter(Mandatory = $true)][string]$Executable,
		[Parameter(Mandatory = $true)][object[]]$Arguments
	)

	$display = @($Executable) + @($Arguments) | ForEach-Object {
		$value = "$_"
		if ($value -match "[\s`"]") {
			'"' + $value.Replace('"', '\"') + '"'
		} else {
			$value
		}
	}
	return ($display -join " ")
}

function Invoke-Encoder {
	param(
		[Parameter(Mandatory = $true)][string]$Executable,
		[Parameter(Mandatory = $true)][object[]]$Arguments
	)

	Write-Host ""
	Write-Host (Format-CommandLine -Executable $Executable -Arguments $Arguments)
	Write-Host ""
	if ($DryRun) {
		return
	}

	& $Executable @Arguments
	if ($LASTEXITCODE -ne 0) {
		throw "FFmpeg exited with status $LASTEXITCODE."
	}
}

function Test-EncodedVideo {
	param(
		[Parameter(Mandatory = $true)][string]$ProbeExecutable,
		[Parameter(Mandatory = $true)][string]$Destination,
		[Nullable[double]]$ExpectedDuration,
		[object]$ExpectedAudio
	)

	$probeArguments = @(
		"-v", "error",
		"-show_entries",
		"stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt:format=duration,size",
		"-of", "json",
		$Destination
	)
	$probeJson = (& $ProbeExecutable @probeArguments 2>&1) -join [Environment]::NewLine
	if ($LASTEXITCODE -ne 0) {
		throw "FFprobe could not read ${Destination}:`n$probeJson"
	}
	$probe = $probeJson | ConvertFrom-Json
	$video = $probe.streams | Where-Object { $_.codec_type -eq "video" } | Select-Object -First 1
	if (-not $video) {
		throw "No video stream was found in $Destination."
	}
	$audioStream = $probe.streams |
		Where-Object { $_.codec_type -eq "audio" } |
		Select-Object -First 1
	if ($null -ne $ExpectedAudio) {
		if ([bool]$ExpectedAudio -and -not $audioStream) {
			throw "No audio stream was found in $Destination."
		}
		if (-not [bool]$ExpectedAudio -and $audioStream) {
			throw "Unexpected audio stream found in $Destination."
		}
	}

	$extension = [System.IO.Path]::GetExtension($Destination).ToLowerInvariant()
	$expectedCodec = if ($extension -eq ".ogv") { "theora" } else { "h264" }
	if ($video.codec_name -ne $expectedCodec) {
		throw "$Destination uses $($video.codec_name), expected $expectedCodec."
	}
	if ($video.pix_fmt -ne "yuv420p") {
		throw "$Destination is not using the mobile-safe yuv420p pixel format."
	}

	if ($Size.ToLowerInvariant() -ne "source") {
		$null = $Size -match "^(\d+)[xX](\d+)$"
		$expectedWidth = [int]$Matches[1]
		$expectedHeight = [int]$Matches[2]
		if ($video.width -ne $expectedWidth -or $video.height -ne $expectedHeight) {
			throw "$Destination is $($video.width)x$($video.height), expected $Size."
		}
	}

	$duration = [double]::Parse(
		"$($probe.format.duration)",
		[Globalization.CultureInfo]::InvariantCulture
	)
	if ($null -ne $ExpectedDuration) {
		$expectedSeconds = [double]$ExpectedDuration
		$tolerance = [Math]::Max(0.075, 1.5 / $Fps)
		if ([Math]::Abs($duration - $expectedSeconds) -gt $tolerance) {
			throw (
				"$Destination is {0:F3}s, expected {1:F3}s." -f
				$duration, $expectedSeconds
			)
		}
	}

	$sizeBytes = [long]$probe.format.size
	$audioDescription = if ($audioStream) { "$($audioStream.codec_name) audio" } else { "silent" }
	Write-Host (
		"Verified: {0} | {1} | {2}x{3} | {4} fps | {5} | {6:F3}s | {7:F2} MiB" -f
		$Destination,
		$video.codec_name,
		$video.width,
		$video.height,
		$video.r_frame_rate,
		$audioDescription,
		$duration,
		($sizeBytes / 1MB)
	)
}

$sourcePath = (Resolve-Path -LiteralPath $InputPath -ErrorAction Stop).Path
$primaryOutput = Resolve-OutputFile -Path $OutputPath
$primaryExtension = [System.IO.Path]::GetExtension($primaryOutput).ToLowerInvariant()
if ($primaryExtension -notin @(".ogv", ".mp4")) {
	throw "Output must end in .ogv or .mp4."
}
if ($ReviewMp4 -and $primaryExtension -ne ".ogv") {
	throw "-ReviewMp4 requires a primary .ogv output."
}

$script:audioPath = $null
if ($Audio) {
	$script:audioPath = (Resolve-Path -LiteralPath $Audio -ErrorAction Stop).Path
}
if ($script:audioPath -and $NoAudio) {
	throw "-Audio and -NoAudio cannot be used together."
}

$sourceItem = Get-Item -LiteralPath $sourcePath
if (-not $sourceItem.PSIsContainer -and
		$frameExtensions -contains $sourceItem.Extension.ToLowerInvariant()) {
	throw "For still images, pass the directory containing the frame sequence."
}
if ($sourceItem.PSIsContainer -and $Fps -eq 0) {
	$Fps = $defaultFrameRate
}

# Validate size before downloading tools or staging frames.
$null = Get-VideoFilter -RequestedSize $Size -RequestedFps $Fps -IncludeFps $false

$outputs = @($primaryOutput)
if ($ReviewMp4) {
	$outputs += [System.IO.Path]::ChangeExtension($primaryOutput, ".mp4")
}
foreach ($destination in $outputs) {
	if ((Test-Path -LiteralPath $destination -PathType Leaf) -and -not $Overwrite -and -not $DryRun) {
		throw "Output already exists (pass -Overwrite deliberately): $destination"
	}
	if (-not $DryRun) {
		$parent = Split-Path -Parent $destination
		if ($parent) {
			New-Item -ItemType Directory -Path $parent -Force | Out-Null
		}
	}
}

$ffmpeg = Find-VideoTool -Name "ffmpeg"
$ffprobe = Find-VideoTool -Name "ffprobe" -SiblingOf $ffmpeg

$temporaryRoot = Join-Path ([System.IO.Path]::GetTempPath()) (
	"mermaid-cartoon-video-" + [guid]::NewGuid().ToString("N")
)
$framePattern = $null
$frameDuration = $null
$expectedAudio = $null
if ($NoAudio -or ($sourceItem.PSIsContainer -and -not $script:audioPath)) {
	$expectedAudio = $false
} elseif ($script:audioPath) {
	$expectedAudio = $true
}

try {
	if ($sourceItem.PSIsContainer) {
		New-Item -ItemType Directory -Path $temporaryRoot | Out-Null
		$frames = @(Get-FrameFiles -Directory $sourcePath)
		$framePattern = New-FrameStage -Frames $frames -Directory $temporaryRoot
		$frameDuration = [double]$frames.Count / $Fps
		Write-Host (
			"Input: {0} frames at {1:g} fps ({2:F3}s)" -f
			$frames.Count, $Fps, $frameDuration
		)
	} else {
		Write-Host "Input: $sourcePath"
	}

	foreach ($destination in $outputs) {
		$encoderArguments = New-EncoderArguments `
			-Source $sourcePath `
			-Destination $destination `
			-FramePattern $framePattern `
			-FrameDuration $frameDuration
		Invoke-Encoder -Executable $ffmpeg -Arguments $encoderArguments
		if (-not $DryRun) {
			Test-EncodedVideo `
				-ProbeExecutable $ffprobe `
				-Destination $destination `
				-ExpectedDuration $frameDuration `
				-ExpectedAudio $expectedAudio
		}
	}
} finally {
	if (Test-Path -LiteralPath $temporaryRoot) {
		$resolvedTemp = (Resolve-Path -LiteralPath $temporaryRoot).Path
		$systemTemp = [System.IO.Path]::GetFullPath(
			[System.IO.Path]::GetTempPath()
		).TrimEnd("\", "/")
		if (-not $resolvedTemp.StartsWith(
			"$systemTemp\mermaid-cartoon-video-",
			[System.StringComparison]::OrdinalIgnoreCase
		)) {
			throw "Refusing to clean an unexpected staging path: $resolvedTemp"
		}
		Remove-Item -LiteralPath $resolvedTemp -Recurse -Force
	}
}

if ($DryRun) {
	Write-Host "Dry run complete; no video was written."
} else {
	Write-Host ""
	Write-Host "Cartoon video encoding complete."
}

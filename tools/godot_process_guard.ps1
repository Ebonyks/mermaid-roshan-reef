<#
.SYNOPSIS
Stops stale background Godot jobs for Mermaid Roshan when a new Godot window starts.

.DESCRIPTION
Watches for newly started Godot process IDs. When a non-headless Godot process
starts, the guard stops older headless Godot processes that can be tied to this
repository and use the same Godot executable. It deliberately ignores godot-ai.exe
and never stops another foreground/editor Godot process.

Use install_godot_process_guard.ps1 to start this guard automatically at logon.

.PARAMETER ProjectRoot
The Mermaid Roshan repository root. Defaults to the parent of this script's tools
directory.

.PARAMETER StartupGraceMilliseconds
How long to let a newly started foreground Godot initialize before cleanup.

.PARAMETER Once
Perform one cleanup pass immediately instead of watching for new Godot processes.

.PARAMETER SelfTest
Run matching tests without inspecting or stopping live processes.

.EXAMPLE
.\tools\godot_process_guard.ps1 -Once -WhatIf

.EXAMPLE
.\tools\godot_process_guard.ps1
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
	[string]$ProjectRoot,

	[ValidateRange(250, 10000)]
	[int]$StartupGraceMilliseconds = 1500,

	[ValidateRange(500, 10000)]
	[int]$PollMilliseconds = 1000,

	[switch]$Once,

	[switch]$SelfTest,

	[string]$LogPath = (Join-Path ([Environment]::GetFolderPath("LocalApplicationData")) "MermaidRoshan\godot-process-guard.log")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $ProjectRoot) {
	$ProjectRoot = Split-Path -Parent $PSScriptRoot
}
$ProjectRoot = [IO.Path]::GetFullPath($ProjectRoot).TrimEnd([char[]]@(92, 47))
$projectLeaf = Split-Path -Leaf $ProjectRoot
$normalizedProjectRoot = $ProjectRoot.Replace("\", "/").ToLowerInvariant()

function Write-GuardLog {
	param([Parameter(Mandatory = $true)][string]$Message)

	$line = "{0:yyyy-MM-dd HH:mm:ss.fff zzz} {1}" -f [DateTimeOffset]::Now, $Message
	try {
		$logDirectory = Split-Path -Parent $LogPath
		if ($logDirectory -and -not (Test-Path -LiteralPath $logDirectory -PathType Container)) {
			New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
		}
		Add-Content -LiteralPath $LogPath -Value $line -Encoding UTF8
	} catch {
		Write-Warning "Could not write the Godot process guard log: $($_.Exception.Message)"
	}
	Write-Verbose $line
}

function Test-GodotProcessName {
	param([AllowEmptyString()][string]$Name)

	if (-not $Name) {
		return $false
	}
	# Matches godot.exe and official versioned names, but never godot-ai.exe.
	return $Name -match "^(?i:godot(?:_v.*)?(?:_console)?)\.exe$"
}

function Test-HeadlessGodotCommand {
	param([AllowEmptyString()][string]$CommandLine)

	return [bool]($CommandLine -match "(?i)(?:^|\s)--headless(?:\s|$)")
}

function Test-MermaidProjectProcess {
	param([Parameter(Mandatory = $true)]$ProcessInfo)

	$commandLine = [string]$ProcessInfo.CommandLine
	$executablePath = [string]$ProcessInfo.ExecutablePath
	$normalizedCommand = $commandLine.Replace("\", "/").ToLowerInvariant()
	$normalizedExecutable = $executablePath.Replace("\", "/").ToLowerInvariant()

	if ($normalizedCommand.Contains($normalizedProjectRoot)) {
		return $true
	}
	if ($projectLeaf -and $normalizedCommand.Contains($projectLeaf.ToLowerInvariant())) {
		return $true
	}

	# Local probes often use --path . or a relative -s scripts/probe_*.gd, so
	# their command lines do not contain the repository's absolute path. The
	# MermaidReefTools Godot install plus a probe script is the narrow fallback.
	$usesProjectGodot = $normalizedExecutable.Contains("/mermaidreeftools/godot/")
	$usesRelativeProbe = $normalizedCommand -match '(?i)(?:^|\s)(?:-s|--script)\s+"?scripts/probe[^\s"]*\.gd(?:"|\s|$)'
	return $usesProjectGodot -and $usesRelativeProbe
}

function Get-GodotProcessInfo {
	param([uint32]$ProcessId = 0)

	if ($ProcessId -gt 0) {
		$items = @(Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId" -ErrorAction SilentlyContinue)
	} else {
		$items = @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue)
	}
	return @($items | Where-Object { Test-GodotProcessName -Name ([string]$_.Name) })
}

function Get-LiveGodotProcessKeys {
	$processKeys = @{}
	# Asking Windows for only these names is substantially cheaper than
	# enumerating every process once per poll. The patterns intentionally do
	# not match godot-ai.
	foreach ($process in @(Get-Process -Name "godot", "Godot_v*" -ErrorAction SilentlyContinue)) {
		try {
			$startTicks = $process.StartTime.ToUniversalTime().Ticks
		} catch {
			$startTicks = 0
		}
		$key = "{0}:{1}" -f $process.Id, $startTicks
		$processKeys[$key] = [uint32]$process.Id
	}
	return $processKeys
}

function Test-SameExecutable {
	param(
		[Parameter(Mandatory = $true)]$Left,
		[Parameter(Mandatory = $true)]$Right
	)

	$leftPath = [string]$Left.ExecutablePath
	$rightPath = [string]$Right.ExecutablePath
	if (-not $leftPath -or -not $rightPath) {
		return $false
	}
	return $leftPath.Equals($rightPath, [StringComparison]::OrdinalIgnoreCase)
}

function Stop-MermaidBackgroundProcess {
	param([Parameter(Mandatory = $true)]$ProcessInfo)

	$processId = [uint32]$ProcessInfo.ProcessId
	$commandLine = [string]$ProcessInfo.CommandLine
	if ($PSCmdlet.ShouldProcess("PID $processId ($commandLine)", "Stop stale Mermaid Roshan headless Godot process")) {
		try {
			Stop-Process -Id $processId -Force -ErrorAction Stop
			Write-GuardLog "Stopped PID ${processId}: $commandLine"
		} catch [Microsoft.PowerShell.Commands.ProcessCommandException] {
			# Exiting between discovery and Stop-Process is harmless.
			Write-GuardLog "PID $processId exited before it could be stopped."
		}
	}
}

function Invoke-TriggeredCleanup {
	param([Parameter(Mandatory = $true)]$TriggerProcess)

	if (Test-HeadlessGodotCommand -CommandLine ([string]$TriggerProcess.CommandLine)) {
		return
	}

	Start-Sleep -Milliseconds $StartupGraceMilliseconds
	$triggerId = [uint32]$TriggerProcess.ProcessId
	$liveTrigger = @(Get-GodotProcessInfo -ProcessId $triggerId) | Select-Object -First 1
	if ($null -eq $liveTrigger) {
		return
	}

	$triggerCreated = [datetime]$liveTrigger.CreationDate
	foreach ($candidate in @(Get-GodotProcessInfo)) {
		if ([uint32]$candidate.ProcessId -eq $triggerId) {
			continue
		}
		if (-not (Test-SameExecutable -Left $liveTrigger -Right $candidate)) {
			continue
		}
		if (-not (Test-HeadlessGodotCommand -CommandLine ([string]$candidate.CommandLine))) {
			continue
		}
		if (-not (Test-MermaidProjectProcess -ProcessInfo $candidate)) {
			continue
		}
		if ([datetime]$candidate.CreationDate -ge $triggerCreated) {
			continue
		}
		Stop-MermaidBackgroundProcess -ProcessInfo $candidate
	}
}

function Invoke-OneShotCleanup {
	foreach ($candidate in @(Get-GodotProcessInfo)) {
		if (-not (Test-HeadlessGodotCommand -CommandLine ([string]$candidate.CommandLine))) {
			continue
		}
		if (-not (Test-MermaidProjectProcess -ProcessInfo $candidate)) {
			continue
		}
		Stop-MermaidBackgroundProcess -ProcessInfo $candidate
	}
}

function Invoke-GuardSelfTest {
	$tests = @(
		@("plain Godot name", (Test-GodotProcessName -Name "godot.exe"), $true),
		@("versioned Godot name", (Test-GodotProcessName -Name "Godot_v4.7.1-stable_win64.exe"), $true),
		@("godot-ai exclusion", (Test-GodotProcessName -Name "godot-ai.exe"), $false),
		@("headless flag", (Test-HeadlessGodotCommand -CommandLine "godot.exe --headless --path ."), $true),
		@("foreground command", (Test-HeadlessGodotCommand -CommandLine "godot.exe --editor"), $false)
	)

	$absoluteProject = [pscustomobject]@{
		CommandLine = "godot.exe --headless --path `"$ProjectRoot`" -s scripts/probe_audit.gd"
		ExecutablePath = "C:\Godot\godot.exe"
	}
	$relativeProjectProbe = [pscustomobject]@{
		CommandLine = "godot.exe --headless --path . -s scripts/probe_fetch.gd"
		ExecutablePath = "C:\Users\Example\AppData\Local\Programs\MermaidReefTools\Godot\4.7.1\godot.exe"
	}
	$unrelatedProbe = [pscustomobject]@{
		CommandLine = "godot.exe --headless --path . -s scripts/probe_other.gd"
		ExecutablePath = "C:\Godot\godot.exe"
	}
	$tests += @(
		@("absolute project path", (Test-MermaidProjectProcess -ProcessInfo $absoluteProject), $true),
		@("relative Mermaid probe", (Test-MermaidProjectProcess -ProcessInfo $relativeProjectProbe), $true),
		@("unrelated relative probe", (Test-MermaidProjectProcess -ProcessInfo $unrelatedProbe), $false)
	)

	foreach ($test in $tests) {
		$name = [string]$test[0]
		$actual = [bool]$test[1]
		$expected = [bool]$test[2]
		if ($actual -ne $expected) {
			throw "Self-test failed: $name (expected $expected, received $actual)"
		}
	}
	Write-Host "Godot process guard self-test: OK ($($tests.Count) checks)"
}

if ($SelfTest) {
	Invoke-GuardSelfTest
	exit 0
}

if ($Once) {
	Invoke-OneShotCleanup
	exit 0
}

$hashProvider = [Security.Cryptography.SHA256]::Create()
try {
	$hashBytes = $hashProvider.ComputeHash([Text.Encoding]::UTF8.GetBytes($normalizedProjectRoot))
	$rootHash = [BitConverter]::ToString($hashBytes).Replace("-", "").Substring(0, 16)
} finally {
	$hashProvider.Dispose()
}
$mutexName = "Local\MermaidRoshanGodotProcessGuard_$rootHash"
$createdMutex = $false
$guardMutex = [Threading.Mutex]::new($true, $mutexName, [ref]$createdMutex)
if (-not $createdMutex) {
	$guardMutex.Dispose()
	exit 0
}

try {
	$knownProcesses = Get-LiveGodotProcessKeys
	Write-GuardLog "Watching for foreground Godot launches every $PollMilliseconds ms. Project root: $ProjectRoot"
	while ($true) {
		Start-Sleep -Milliseconds $PollMilliseconds
		$currentProcesses = Get-LiveGodotProcessKeys
		foreach ($processKey in @($currentProcesses.Keys)) {
			if ($knownProcesses.ContainsKey($processKey)) {
				continue
			}
			$startedProcessId = [uint32]$currentProcesses[$processKey]
			$startedProcess = $null
			for ($attempt = 0; $attempt -lt 5 -and $null -eq $startedProcess; $attempt++) {
				$startedProcess = @(Get-GodotProcessInfo -ProcessId $startedProcessId) | Select-Object -First 1
				if ($null -eq $startedProcess) {
					Start-Sleep -Milliseconds 200
				}
			}
			if ($null -ne $startedProcess -and
					-not (Test-HeadlessGodotCommand -CommandLine ([string]$startedProcess.CommandLine))) {
				Invoke-TriggeredCleanup -TriggerProcess $startedProcess
			}
		}
		$knownProcesses = $currentProcesses
	}
} finally {
	$guardMutex.ReleaseMutex()
	$guardMutex.Dispose()
}

<#
.SYNOPSIS
Installs or removes the Mermaid Roshan Godot process guard for the current user.

.DESCRIPTION
Creates a per-user Scheduled Task that starts godot_process_guard.ps1 hidden at
logon. The guard then reacts whenever a foreground Godot process starts.

.PARAMETER Uninstall
Stops and removes the Scheduled Task.

.PARAMETER NoStart
Install the task without starting it in the current login session.

.EXAMPLE
.\tools\install_godot_process_guard.ps1

.EXAMPLE
.\tools\install_godot_process_guard.ps1 -Uninstall
#>
[CmdletBinding()]
param(
	[switch]$Uninstall,
	[switch]$NoStart
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

trap {
	[Console]::Error.WriteLine("error: $($_.Exception.Message)")
	exit 2
}

$taskName = "Mermaid Roshan Godot Process Guard"
$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceGuardPath = Join-Path $PSScriptRoot "godot_process_guard.ps1"
$installRoot = Join-Path ([Environment]::GetFolderPath("LocalApplicationData")) "MermaidRoshan"
$installedGuardPath = Join-Path $installRoot "godot_process_guard.ps1"
$windowsPowerShell = Join-Path $env:SystemRoot "System32\WindowsPowerShell\v1.0\powershell.exe"

if ($Uninstall) {
	$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
	if ($null -eq $existingTask) {
		Write-Host "The Godot process guard is not installed."
		exit 0
	}
	Stop-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
	Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
	if (Test-Path -LiteralPath $installedGuardPath -PathType Leaf) {
		Remove-Item -LiteralPath $installedGuardPath -Force
	}
	Write-Host "Removed Scheduled Task: $taskName"
	exit 0
}

if (-not (Test-Path -LiteralPath $sourceGuardPath -PathType Leaf)) {
	throw "Guard script not found: $sourceGuardPath"
}
if (-not (Test-Path -LiteralPath $windowsPowerShell -PathType Leaf)) {
	throw "Windows PowerShell not found: $windowsPowerShell"
}
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($null -ne $existingTask) {
	Stop-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Path $installRoot -Force | Out-Null
Copy-Item -LiteralPath $sourceGuardPath -Destination $installedGuardPath -Force

$escapedGuardPath = $installedGuardPath.Replace('"', '\"')
$escapedRepoRoot = $repoRoot.Replace('"', '\"')
$taskArguments = "-NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$escapedGuardPath`" -ProjectRoot `"$escapedRepoRoot`""
$action = New-ScheduledTaskAction -Execute $windowsPowerShell -Argument $taskArguments -WorkingDirectory $repoRoot
$trigger = New-ScheduledTaskTrigger -AtLogOn -User ([Security.Principal.WindowsIdentity]::GetCurrent().Name)
$settings = New-ScheduledTaskSettingsSet `
	-AllowStartIfOnBatteries `
	-DontStopIfGoingOnBatteries `
	-MultipleInstances IgnoreNew `
	-RestartCount 3 `
	-RestartInterval (New-TimeSpan -Minutes 1) `
	-ExecutionTimeLimit ([TimeSpan]::Zero)

Register-ScheduledTask `
	-TaskName $taskName `
	-Action $action `
	-Trigger $trigger `
	-Settings $settings `
	-Description "Stops stale Mermaid Roshan headless Godot jobs when a new foreground Godot starts." `
	-Force | Out-Null

if (-not $NoStart) {
	Start-ScheduledTask -TaskName $taskName
}

$installedTask = Get-ScheduledTask -TaskName $taskName
Write-Host "Installed Scheduled Task: $taskName"
Write-Host "State: $($installedTask.State)"
Write-Host "Guard: $installedGuardPath"
Write-Host "Log: $([IO.Path]::Combine([Environment]::GetFolderPath('LocalApplicationData'), 'MermaidRoshan', 'godot-process-guard.log'))"
Write-Host "Dry-run cleanup: tools\godot_process_guard.ps1 -Once -WhatIf"

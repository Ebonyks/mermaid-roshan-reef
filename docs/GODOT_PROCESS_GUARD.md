# Mermaid Roshan Godot process guard

`tools/godot_process_guard.ps1` prevents abandoned headless Mermaid Reef Godot
jobs from slowing down the Windows development machine. It checks lightweight
process identifiers once per second. When a new foreground Godot editor,
project manager, or game process starts, it terminates older matching
`--headless` jobs.

The guard is deliberately narrow:

- It never stops the newly launched Godot process.
- It never stops another foreground or editor process.
- It excludes `godot-ai.exe` and unrelated programs with `godot` in their name.
- It requires the old process to match this repository and use the same Godot
  executable as the new process.
- A headless Godot launch does not trigger cleanup, so sequential or parallel
  probe commands do not kill each other.

## Install

Run once in PowerShell from the repository root:

```powershell
.\tools\install_godot_process_guard.ps1
```

This creates and starts the per-user Scheduled Task
`Mermaid Roshan Godot Process Guard`. It launches hidden at each logon and uses
negligible CPU between one-second checks. Administrator rights are not required
for a current-user task. The installer copies the guard to
`%LOCALAPPDATA%\MermaidRoshan\godot_process_guard.ps1`, so changing Git branches
does not break the installed task. Re-run the installer after updating the
repository copy.

The activity log is stored at:

```text
%LOCALAPPDATA%\MermaidRoshan\godot-process-guard.log
```

## Safe checks and manual cleanup

Run the matcher self-test:

```powershell
.\tools\godot_process_guard.ps1 -SelfTest
```

Preview background processes that a one-time cleanup would stop:

```powershell
.\tools\godot_process_guard.ps1 -Once -WhatIf
```

Perform that cleanup immediately:

```powershell
.\tools\godot_process_guard.ps1 -Once
```

## Uninstall

```powershell
.\tools\install_godot_process_guard.ps1 -Uninstall
```

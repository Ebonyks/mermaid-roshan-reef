$ErrorActionPreference='Stop'
& python (Join-Path $PSScriptRoot 'run_full_project_gates.py')
exit $LASTEXITCODE

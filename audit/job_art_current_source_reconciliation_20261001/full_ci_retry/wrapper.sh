#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
python3() { /c/Users/Peter/AppData/Local/Python/bin/python.exe -X utf8 -B "$@"; }
export -f python3
export GODOT="C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe"
export TMPDIR="$PWD/tmp"
bash scripts/ci.sh
result=$?
printf '%s\n' "$result" > tmp/job_art_reconciled_full_ci_retry.exit
exit "$result"

#!/usr/bin/env bash
set -uo pipefail
cd '/c/Users/Peter/Documents/mermaid-roshan-reef/tmp/day2_graphics_audit_20260930'
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
python3() { /c/Users/Peter/AppData/Local/Python/bin/python.exe -X utf8 -B "$@"; }
export -f python3
export GODOT="C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe"
export TMPDIR="$PWD/tmp"
bash scripts/ci.sh
result=$?
printf '%s\n' "$result" > audit/day_one_pool_live_refinement_v2_20261001/full_ci_current_v1/process.exit
exit "$result"

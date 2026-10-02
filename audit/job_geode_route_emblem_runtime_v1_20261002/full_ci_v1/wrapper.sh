#!/usr/bin/env bash
set -uo pipefail
cd '/c/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef'
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
python3() { /c/Users/Peter/AppData/Local/Python/bin/python.exe -X utf8 -B "$@"; }
export -f python3
export GODOT="C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe"
export TMPDIR="$PWD/tmp"
bash scripts/ci.sh
result=$?
printf '%s\n' "$result" > audit/job_geode_route_emblem_runtime_v1_20261002/full_ci_v1/process.exit
exit "$result"

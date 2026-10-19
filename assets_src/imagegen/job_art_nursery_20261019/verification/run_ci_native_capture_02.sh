#!/usr/bin/env bash
set -uo pipefail
cd '/c/Users/Peter/.codex/worktrees/art-ci-control-20261018/mermaid-roshan-reef'
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
python3() { /c/Users/Peter/AppData/Local/Python/bin/python.exe -X utf8 -B "$@"; }
timeout() { /c/Users/Peter/AppData/Local/Python/bin/python.exe -X utf8 -B C:/Users/Peter/.codex/worktrees/art-ci-control-20261018/mermaid-roshan-reef/assets_src/imagegen/job_art_nursery_20261019/verification/windows_native_capture_02.py "$@"; }
export -f python3 timeout
export GODOT='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe'
export TMPDIR=/c/Users/Peter/AppData/Local/Temp
bash --noprofile --norc scripts/ci.sh
exit "$?"

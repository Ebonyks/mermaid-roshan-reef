#!/usr/bin/env bash
set -uo pipefail
cd '/c/Users/Peter/.codex/worktrees/art-astronaut-20261018/mermaid-roshan-reef'
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
python3() { /c/Users/Peter/AppData/Local/Python/bin/python.exe -X utf8 -B "$@"; }
timeout() { /c/Users/Peter/AppData/Local/Python/bin/python.exe -X utf8 -B C:/Users/Peter/.codex/worktrees/art-astronaut-20261018/mermaid-roshan-reef/assets_src/imagegen/job_art_astronaut_20261018/verification/windows_timeout_retry_03.py "$@"; }
export -f python3 timeout
export TMPDIR=/c/Users/Peter/AppData/Local/Temp
bash --noprofile --norc scripts/ci.sh
exit "$?"

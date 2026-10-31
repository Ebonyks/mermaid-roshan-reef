#!/usr/bin/env bash
set -uo pipefail
cd '/c/Users/Peter/Documents/mermaid-roshan-reef'
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
python3() { /c/Users/Peter/AppData/Local/Python/bin/python.exe -X utf8 -B "$@"; }
timeout() { /c/Users/Peter/AppData/Local/Python/bin/python.exe -X utf8 -B C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/artwork-quality-20261018/windows_timeout.py "$@"; }
export -f python3 timeout
export TMPDIR=/c/Users/Peter/AppData/Local/Temp
bash --noprofile --norc scripts/ci.sh
exit "$?"

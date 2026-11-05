#!/bin/bash
# Run Godot 4.7.2 headless with a fresh APPDATA/LOCALAPPDATA, the way
# scripts/ci.sh isolates each probe, and keep a log per label.
# Run from the repository root of a checkout of the Boxer branch.
# usage: harness/run_iso.sh <label> <timeout> <godot args...>
#   e.g. docs/handoffs/codex_boxer_engine_2026-11-01/harness/run_iso.sh geometry 15m -s tmp/claude_boxer_eval/geometry_check.gd
set -u
GODOT="${GODOT:-$(python -B tools/resolve_godot.py)}"
OUT="${BOXER_EVAL_OUT:-tmp/claude_boxer_eval/out}"
label=$1; shift
limit=$1; shift
iso="$OUT/iso/$label"
rm -rf "$iso"
mkdir -p "$iso/appdata" "$iso/localappdata" "$iso/data" "$iso/config" "$OUT/logs"
if command -v cygpath >/dev/null 2>&1; then
	appdata="$(cygpath -w "$iso/appdata")"; localappdata="$(cygpath -w "$iso/localappdata")"
else
	appdata="$iso/appdata"; localappdata="$iso/localappdata"
fi
APPDATA="$appdata" LOCALAPPDATA="$localappdata" \
	XDG_DATA_HOME="$iso/data" XDG_CONFIG_HOME="$iso/config" \
	timeout "$limit" "$GODOT" --headless --path . "$@" 2>&1 | tee "$OUT/logs/$label.log"
echo "EXIT ${PIPESTATUS[0]}"

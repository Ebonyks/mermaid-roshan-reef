#!/usr/bin/env bash
set -uo pipefail
cd '/c/Users/Peter/Documents/mermaid-roshan-reef/tmp/day2_graphics_audit_20260930'
export GODOT='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
probe_home='/c/Users/Peter/Documents/mermaid-roshan-reef/tmp/day2_graphics_audit_20260930/tmp/mg2d_exact_process_retry_v1'
probe_appdata="$(cygpath -w "$probe_home/appdata")"
probe_localappdata="$(cygpath -w "$probe_home/localappdata")"
probe_rc=0
APPDATA="$probe_appdata" LOCALAPPDATA="$probe_localappdata" XDG_DATA_HOME="$probe_home/data" XDG_CONFIG_HOME="$probe_home/config" timeout 8m "$GODOT" --headless -s scripts/probe_mg2d.gd -- --touch --classic-touch-test 2>&1 | tee 'audit/day_one_pool_live_refinement_v2_20261001/probe_mg2d_process_retry_v1/probe_output.log' || probe_rc=$?
printf '%s\n' "$probe_rc" > 'audit/day_one_pool_live_refinement_v2_20261001/probe_mg2d_process_retry_v1/process.exit'
exit "$probe_rc"

#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/../.."
export GODOT="C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe"
export PYTHONIOENCODING=utf-8
export PYTHONUTF8=1
export TEMP="C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v2_20261007_2050/temp"
export TMP="$TEMP"
export TMPDIR="$(cygpath -u "$TEMP")"
export ASTRO_FULL_CI_TMP_C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v2_20261007_2050="$(realpath -m -- "$(cygpath -u 'C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v2_20261007_2050')")"
export APPDATA="C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v2_20261007_2050/appdata"
export LOCALAPPDATA="C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v2_20261007_2050/localappdata"
export XDG_DATA_HOME="C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v2_20261007_2050/data"
export XDG_CONFIG_HOME="C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v2_20261007_2050/config"
rm() {
    local candidate resolved
    for candidate in "$@"; do
        case "$candidate" in -*) continue ;; esac
        resolved="$(realpath -m -- "$candidate")" || return 1
        case "$resolved" in "$ASTRO_FULL_CI_TMP_C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v2_20261007_2050"/*) ;; *) echo "OWNED TEMP CLEANUP GUARD REJECTED: $resolved" >&2; return 1 ;; esac
    done
    command rm "$@"
}
export -f rm
printf 'ASTRO_FULL_CI_V2_START|%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
timeout 3300s bash scripts/ci.sh
ci_rc=$?
printf 'ASTRO_FULL_CI_V2_EXIT|%s|%s\n' "$ci_rc" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
exit "$ci_rc"

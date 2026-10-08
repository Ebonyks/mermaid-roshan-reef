#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
export GODOT="C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe"
export PYTHONIOENCODING=utf-8
export PYTHONUTF8=1
export TEMP="C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v3_20261007_2053/temp"
export TMP="$TEMP"
export TMPDIR="$(cygpath -u "$TEMP")"
export ASTRO_FULL_CI_TMP_ROOT="$(realpath -m -- "$(cygpath -u 'C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v3_20261007_2053')")"
export APPDATA="C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v3_20261007_2053/appdata"
export LOCALAPPDATA="C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v3_20261007_2053/localappdata"
export XDG_DATA_HOME="C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v3_20261007_2053/data"
export XDG_CONFIG_HOME="C:/Users/Peter/AppData/Local/Temp/astronaut_full_ci_v3_20261007_2053/config"
verify_owned_temp() {
    local resolved
    resolved="$(realpath -m -- "$1")" || return 1
    case "$resolved" in "$ASTRO_FULL_CI_TMP_ROOT"/*) return 0 ;; *) return 1 ;; esac
}
rm() {
    local candidate
    for candidate in "$@"; do
        case "$candidate" in -*) continue ;; esac
        verify_owned_temp "$candidate" || { echo "OWNED TEMP CLEANUP GUARD REJECTED: $candidate" >&2; return 1; }
    done
    command rm "$@"
}
export -f verify_owned_temp rm
if [ "${1:-}" = "--self-test" ]; then
    verify_owned_temp "$TMPDIR/disposable-profile"
    if verify_owned_temp "$PWD"; then echo 'CLEANUP GUARD SELF-TEST FAIL'; exit 1; fi
    if verify_owned_temp "$ASTRO_FULL_CI_TMP_ROOT/../outside"; then echo 'CLEANUP GUARD TRAVERSAL FAIL'; exit 1; fi
    printf 'CLEANUP GUARD SELF-TEST PASS|%s\n' "$ASTRO_FULL_CI_TMP_ROOT"
    exit 0
fi
printf 'ASTRO_FULL_CI_V3_START|%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
set +e
timeout 3240s bash scripts/ci.sh
ci_rc=$?
set -e
printf 'ASTRO_FULL_CI_V3_EXIT|%s|%s\n' "$ci_rc" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
exit "$ci_rc"

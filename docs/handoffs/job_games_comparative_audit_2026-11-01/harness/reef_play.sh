#!/usr/bin/env bash
# Reef of Light Opera career playthrough harness wrapper.
# Usage:
#   reef_play.sh CAREER POLICY SEED OUT_DIR [MODE=fast|rendered] [MAX_SECONDS=600]
# Env:
#   REEF_DISPLAY  X display number for rendered mode (default 56; must be YOUR display)
#   REEF_FPS      fixed fps for fast mode (default 60). REEF_RENDER_FIXED_FPS=N makes
#                 rendered mode deterministic (game time decoupled from wall time).
#   REEF_KEEP_USERDIR=1  keep the temporary user:// dir (for inspection)
#   REEF_INPUT    finger (default: Input.parse_input_event + OS touch->mouse
#                 emulation, i.e. the tablet path) | touch_only (emulation off; diagnostic)
# Exit status: 0 run finished (completed or not; see run.json), 2 harness error.
set -u
if [ $# -lt 4 ]; then
  sed -n 2,12p "$0"; exit 2
fi
CAREER="$1"; POLICY="$2"; SEED="$3"; OUT="$4"; MODE="${5:-fast}"; MAXS="${6:-600}"
PROJ=/home/claude/ebonyks/mermaid-roshan-reef
GODOT="$PROJ/Godot_v4.7.2-stable_linux.x86_64"
mkdir -p "$OUT"; rm -rf "$OUT/frames" "$OUT/run.json" "$OUT/isolation.json"
OUT="$(cd "$OUT" && pwd)"

# Save isolation: user:// lives under $XDG_DATA_HOME/godot/app_userdata/<name>.
# Every run gets a fresh, empty data home, so the player's real save is never
# read or written. The real default dir is fingerprinted before/after as proof.
REAL_USER="$HOME/.local/share/godot/app_userdata/Mermaid Roshan Reef of Light"
fp() { if [ -d "$REAL_USER" ]; then find "$REAL_USER" -maxdepth 1 -type f -name '*.json' -printf '%f %s %T@\n' 2>/dev/null | sort | md5sum | cut -c1-12; else echo none; fi; }
FP_BEFORE="$(fp)"
TMP_DATA="$(mktemp -d /tmp/reef_userdata.XXXXXX)"
export XDG_DATA_HOME="$TMP_DATA"

ARGS=(--path "$PROJ" --audio-driver Dummy --resolution 1280x720)
WALL=$(( ${MAXS%.*} * 4 + 120 ))
if [ "$MODE" = "rendered" ]; then
  DNUM="${REEF_DISPLAY:-56}"
  export DISPLAY=":$DNUM" XDG_RUNTIME_DIR="/tmp/xdg$DNUM"
  mkdir -p "$XDG_RUNTIME_DIR"; chmod 700 "$XDG_RUNTIME_DIR"
  if ! xdpyinfo -display ":$DNUM" >/dev/null 2>&1; then
    Xvfb ":$DNUM" -screen 0 1280x720x24 >/dev/null 2>&1 &
    sleep 2
  fi
  ARGS+=(--windowed --position 0,0 --max-fps 30)
  if [ -n "${REEF_RENDER_FIXED_FPS:-}" ]; then ARGS+=(--fixed-fps "$REEF_RENDER_FIXED_FPS"); fi
else
  ARGS+=(--headless --fixed-fps "${REEF_FPS:-60}")
fi

cd "$PROJ"
timeout "$WALL" "$GODOT" "${ARGS[@]}" -s res://audit_local/reef_play.gd -- \
  "career=$CAREER" "policy=$POLICY" "seed=$SEED" "out=$OUT" "mode=$MODE" "max_seconds=$MAXS" "input=${REEF_INPUT:-finger}" \
  > "$OUT/godot.log" 2>&1
RC=$?
FP_AFTER="$(fp)"
SAVE_WRITTEN="no"
if [ -f "$TMP_DATA/godot/app_userdata/Mermaid Roshan Reef of Light/reef_save.json" ]; then SAVE_WRITTEN="yes(temp dir only)"; fi
printf '{"real_userdir_fingerprint_before":"%s","real_userdir_fingerprint_after":"%s","real_save_untouched":%s,"temp_user_dir":"%s","temp_save_written":"%s","godot_exit":%d}\n' \
  "$FP_BEFORE" "$FP_AFTER" "$([ "$FP_BEFORE" = "$FP_AFTER" ] && echo true || echo false)" \
  "$TMP_DATA" "$SAVE_WRITTEN" "$RC" > "$OUT/isolation.json"
if [ -z "${REEF_KEEP_USERDIR:-}" ]; then rm -rf "$TMP_DATA"; fi
grep -h "REEF_PLAY|" "$OUT/godot.log" | tail -3
if [ ! -f "$OUT/run.json" ]; then echo "REEF_PLAY|no run.json (godot exit $RC); see $OUT/godot.log"; exit 2; fi
exit 0

#!/usr/bin/env bash
# Full local gate: fresh import + every trusted probe.  Probe user data is
# isolated so one bot cannot make the next bot pass by pre-winning content.
set -uo pipefail
GODOT="${GODOT:-godot}"
cd "$(dirname "$0")/.."
# fast static gates first (no Godot needed): syntax, then the ':=' Variant
# inference shape that broke main.gd twice on 2026-07-11 - a parse error in
# main.gd makes every probe idle to its 8m timeout, so catching it here
# turns a 30-minute opaque job timeout into a 5-second message
python3 -m gdtoolkit.parser scripts/*.gd scripts/arena/*.gd scripts/games/*.gd \
	|| { echo "PARSE FAIL (gdtoolkit)"; exit 1; }
python3 tools/lint_inference.py scripts/*.gd scripts/arena/*.gd scripts/games/*.gd \
	|| { echo "LINT FAIL (:= from Variant)"; exit 1; }
import_log="$(mktemp)"
timeout 12m "$GODOT" --headless --path . --import 2>&1 | tee "$import_log" \
	|| { echo "IMPORT FAIL"; exit 1; }
grep -qE "SCRIPT ERROR|Parse Error|Compile Error|ERR_FILE_CORRUPT|Error importing|Failed loading resource|Cannot open file|Cannot load resource" "$import_log" \
	&& { echo "IMPORT FAIL (resource or script error)"; exit 1; }
rc=0
for p in probe_audit probe_passive probe_load probe_save_recovery probe_galaxy_state probe_mg2d probe_dance probe_l2 probe_l2_reenter probe_crown probe_train probe_verbs probe_skins probe_touch_look probe_voice probe_kart_feel probe_combat probe_dungeon; do
	[ -f "scripts/$p.gd" ] || { echo "PROBE $p MISSING: scripts/$p.gd is required"; rc=1; continue; }
	echo "=== $p ==="
	probe_home="$(mktemp -d)"
	mkdir -p "$probe_home/data" "$probe_home/config"
	XDG_DATA_HOME="$probe_home/data" XDG_CONFIG_HOME="$probe_home/config" \
		timeout 8m "$GODOT" --headless -s "scripts/$p.gd" -- --touch 2>&1 \
		| tee "/tmp/$p.out" || rc=1
	grep -qE "FAIL|FAILED|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error" "/tmp/$p.out" \
		&& { echo "PROBE $p reported a failure marker"; rc=1; }
	rm -rf "$probe_home"
done
exit $rc

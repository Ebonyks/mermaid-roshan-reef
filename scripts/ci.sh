#!/usr/bin/env bash
# Full local gate: fresh import + every trusted probe. Fails on any FAIL line.
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
KART_RUNTIME_ERROR_RE='SCRIPT ERROR|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)'
timeout 12m "$GODOT" --headless --import . || { echo "IMPORT FAIL"; exit 1; }
rc=0
for p in probe_audit probe_passive probe_load probe_mg2d probe_dance probe_l2 probe_train probe_verbs probe_skins probe_kart_feel probe_combat probe_dungeon; do
	echo "=== $p ==="
	timeout 8m "$GODOT" --headless -s "scripts/$p.gd" 2>&1 | tee "/tmp/$p.out" || rc=1
	grep -q "FAIL" "/tmp/$p.out" && { echo "PROBE $p reported FAIL"; rc=1; }
	# a script that cannot compile leaves the probe waiting on a world that
	# never builds - bail on the whole gate instead of timing out per-probe
	grep -qE "Parse Error|Compile Error" "/tmp/$p.out" \
		&& { echo "PROBE $p hit a script compile error - aborting gate"; exit 1; }
	if [ "$p" = "probe_kart_feel" ]; then
		grep -qE "$KART_RUNTIME_ERROR_RE" "/tmp/$p.out" \
			&& { echo "PROBE $p reported a missing resource or script error"; rc=1; }
	fi
done
exit $rc

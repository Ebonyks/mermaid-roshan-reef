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
# parse the full tree (probes included) so a new scripts/ subdir or a broken
# probe cannot slip past the hardcoded globs below
python3 -m gdtoolkit.parser $(find scripts -name '*.gd') \
	|| { echo "PARSE FAIL (gdtoolkit)"; exit 1; }
python3 tools/lint_inference.py scripts/*.gd scripts/arena/*.gd scripts/games/*.gd \
	|| { echo "LINT FAIL (:= from Variant)"; exit 1; }
python3 tools/audit_fairy_art_v2.py \
	|| { echo "FAIRY ART FAIL (texture or GLB contract)"; exit 1; }
RUNTIME_ERROR_RE='SCRIPT ERROR|Invalid assignment of property or key|The tweened property .* does not exist|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)'
FAILURE_RE='FAIL|FAILED|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error'
import_log="$(mktemp)"
timeout 12m "$GODOT" --headless --path . --import 2>&1 | tee "$import_log" \
	|| { echo "IMPORT FAIL"; exit 1; }
grep -qE "$RUNTIME_ERROR_RE|Parse Error|Compile Error|ERR_FILE_CORRUPT|Error importing|Cannot load resource" "$import_log" \
	&& { echo "IMPORT FAIL (resource or script error)"; exit 1; }
rc=0
for p in probe_reef_districts probe_audit probe_passive probe_load probe_save_recovery probe_galaxy_state probe_collection probe_mg2d probe_fetch probe_audio probe_dance probe_l2 probe_l2_reenter probe_crown probe_northern probe_human_art_audit probe_train probe_verbs probe_skins probe_touch_look probe_voice probe_kart_feel probe_combat probe_dungeon probe_opera probe_kitchen_props probe_bathroom_props probe_bathroom_integration probe_fairy_art; do
	[ -f "scripts/$p.gd" ] || { echo "PROBE $p MISSING: scripts/$p.gd is required"; rc=1; continue; }
	echo "=== $p ==="
	probe_home="$(mktemp -d)"
	mkdir -p "$probe_home/data" "$probe_home/config"
	probe_rc=0
	XDG_DATA_HOME="$probe_home/data" XDG_CONFIG_HOME="$probe_home/config" \
		timeout 8m "$GODOT" --headless -s "scripts/$p.gd" -- --touch 2>&1 | tee "/tmp/$p.out" || probe_rc=$?
	if [ "$probe_rc" -ne 0 ]; then
		# Known engine flaw (2026-07-18): Godot 4.4 sometimes deadlocks at EXIT
		# after a probe printed its complete verdict (seen after kart-heavy
		# probes, always AFTER an ALL OK line). Accept a timeout kill (124)
		# only when the transcript ends with a final verdict marker; the
		# failure greps below still veto bad content. Anything else is real.
		if [ "$probe_rc" -eq 124 ] && tail -n 5 "/tmp/$p.out" | grep -qE "ALL OK|RESULT"; then
			echo "PROBE $p reached its verdict; engine hung at exit and was reaped - accepted"
		else
			rc=1
		fi
	fi
	grep -qE "$FAILURE_RE" "/tmp/$p.out" \
		&& { echo "PROBE $p reported a failure or runtime script error"; rc=1; }
	# a script that cannot compile leaves the probe waiting on a world that
	# never builds - bail on the whole gate instead of timing out per-probe
	grep -qE "Parse Error|Compile Error" "/tmp/$p.out" \
		&& { echo "PROBE $p hit a script compile error - aborting gate"; exit 1; }
	grep -qE "$RUNTIME_ERROR_RE" "/tmp/$p.out" \
		&& { echo "PROBE $p reported a resource or property runtime error"; rc=1; }
	# positive floor: a probe that exits 0 while printing nothing asserted
	# nothing - a startup crash swallowed before any output must not pass
	[ -s "/tmp/$p.out" ] \
		|| { echo "PROBE $p produced no output - silent no-op treated as failure"; rc=1; }
	rm -rf "$probe_home"
done
exit $rc

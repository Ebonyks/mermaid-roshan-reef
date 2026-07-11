#!/usr/bin/env bash
# Full local gate: fresh import + every trusted probe. Fails on any FAIL line.
set -uo pipefail
GODOT="${GODOT:-godot}"
cd "$(dirname "$0")/.."
timeout 12m "$GODOT" --headless --import . || { echo "IMPORT FAIL"; exit 1; }
rc=0
for p in probe_audit probe_passive probe_load probe_mg2d probe_l2 probe_verbs probe_skins probe_kart_feel; do
	echo "=== $p ==="
	timeout 8m "$GODOT" --headless -s "scripts/$p.gd" 2>&1 | tee "/tmp/$p.out" || rc=1
	grep -q "FAIL" "/tmp/$p.out" && { echo "PROBE $p reported FAIL"; rc=1; }
done
exit $rc

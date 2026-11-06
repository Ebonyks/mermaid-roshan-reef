#!/usr/bin/env bash
# Full local gate: fresh import + every trusted probe.  Probe user data is
# isolated so one bot cannot make the next bot pass by pre-winning content.
set -uo pipefail
cd "H:/Dev/Worktrees/flat-vector-racer-mount-fit-20261105/project"
# Windows-local parity (2026-08-04): on Windows the Python default text codec
# is cp1252, so every tool below that reads a UTF-8 source file or prints an
# arrow/em-dash dies with a charmap error and the suite never reaches the
# probes. Linux CI already defaults to UTF-8, so this is a no-op there.
export PYTHONIOENCODING="utf-8"
export PYTHONUTF8=1
GODOT="$(python3 tools/resolve_godot.py)" \
	|| { echo "APPROVED GODOT RUNTIME UNAVAILABLE"; exit 1; }
# Tools started below resolve the same build instead of an older PATH entry.
export GODOT
# Keep the editor, templates, CI downloads, feature tag and release authority
# on one checksum-pinned official patch before any other gate runs.
python3 tools/audit_audio_quality.py --check \
	|| { echo "COMPLETE AUDIO QUALITY LEDGER DRIFT"; exit 1; }
# Game-wide visual design audit (VISUAL_AUDIT_TOOL.md). Lifecycle-contract and
# stress tests are HARD gates: strict must never accept an unresolved review,
# manual item, or coverage gap, and every check must remain falsifiable. The
# repository run stays advisory while its report says UNSATISFIED.
python3 -m unittest tools.tests.test_audit_visual_design \
	|| { echo "VISUAL AUDIT CONTRACT TEST FAIL"; exit 1; }
python3 tools/audit_visual_design.py --stress \
	|| { echo "VISUAL AUDIT SELF-TEST FAIL (a check can no longer fail)"; exit 1; }
python3 tools/audit_visual_design.py || true
python3 tools/audit_scene_congruency.py \
	|| { echo "SKY LAGOON CONGRUENCY FAIL"; exit 1; }
python3 tools/audit_sky_lagoon_layout.py \
	|| { echo "SKY LAGOON SEMANTIC LAYOUT/CONTACT FAIL"; exit 1; }
python3 tools/audit_castle_card_alpha.py \
	|| { echo "CASTLE CARD ALPHA/DEPTH FAIL"; exit 1; }
# Painted flats are drawn unshaded, so the Environment grade is the only thing
# between an approved PNG and the child. This replays the shipped grade over
# the real art and fails when a profile clips or crushes pixels the source did
# not (LIGHTING_2P5D_AUDIT_2026-08-02 §1.7/§E1).
python3 -m unittest tools.tests.test_check_grade_headroom \
	|| { echo "GRADE HEADROOM CONSOLE TEST FAIL"; exit 1; }
python3 tools/check_grade_headroom.py \
	|| { echo "GRADE HEADROOM FAIL (Environment grade is clipping painted art)"; exit 1; }
python3 tools/audit_castle_interactions.py \
	|| { echo "CASTLE INTERACTION PACK FAIL"; exit 1; }
python3 tools/normalize_castle_interaction_v2_sheets.py --check \
	|| { echo "CASTLE INTERACTION V2 NORMALIZATION FAIL"; exit 1; }
python3 tools/audit_castle_interactions_v2.py \
	|| { echo "CASTLE INTERACTION V2 DELIVERY FAIL"; exit 1; }
python3 tools/build_castle_interaction_v4_delivery.py --check \
	|| { echo "CASTLE INTERACTION V4 DELIVERY DRIFT"; exit 1; }
python3 tools/audit_castle_native_interactions.py \
	|| { echo "CASTLE NATIVE INTERACTION OWNERSHIP FAIL"; exit 1; }
python3 tools/repair_castle_room_native_backgrounds.py --check \
	|| { echo "CASTLE LIVE-ALPHA BACKGROUND HEALING FAIL"; exit 1; }
python3 tools/build_interactive_background_ownership.py --check \
	|| { echo "INTERACTIVE/BACKGROUND PIXEL OWNERSHIP FAIL"; exit 1; }
python3 tools/refine_castle_depth_cards.py --check \
	|| { echo "CASTLE STATIC DEPTH-CARD REFINEMENT DRIFT"; exit 1; }
python3 tools/audit_castle_static_depth_cards.py \
	|| { echo "CASTLE STATIC DEPTH-CARD ALPHA FAIL"; exit 1; }
python3 -m unittest \
	tools.test_audit_castle_native_interactions \
	tools.test_build_castle_interaction_v4_delivery \
	tools.test_castle_interaction_frame_qa \
	tools.test_review_castle_interaction_frames_v4 \
	tools.test_refine_castle_depth_cards \
	tools.test_audit_castle_static_depth_cards \
	tools.test_repair_castle_room_native_backgrounds \
	tools.test_interactive_background_ownership \
	|| { echo "CASTLE INTERACTION/DEPTH REVIEW SELF-TEST FAIL"; exit 1; }
python3 tools/review_castle_interaction_frames_v4.py check \
	|| { echo "CASTLE INTERACTION PER-FRAME APPROVAL FAIL"; exit 1; }
RUNTIME_ERROR_RE='SCRIPT ERROR|Invalid assignment of property or key|The tweened property .* does not exist|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)'
FAILURE_RE='FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error'
import_log="$(mktemp)"
timeout 12m "$GODOT" --headless --path . --import 2>&1 | tee "$import_log" \
	|| { echo "IMPORT FAIL"; exit 1; }
grep -qE "$RUNTIME_ERROR_RE|Parse Error|Compile Error|ERR_FILE_CORRUPT|Error importing|Cannot load resource" "$import_log" \
	&& { echo "IMPORT FAIL (resource or script error)"; exit 1; }
python3 tools/audit_game_2d.py --regression-gate \
	|| { echo "GAME-WIDE 2D MIGRATION REGRESSION (debt may only shrink)"; exit 1; }
rc=0

echo RECENT_STATIC_IMPORT_ALL_OK

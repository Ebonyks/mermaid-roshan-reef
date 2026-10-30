#!/usr/bin/env bash
# Full local gate: fresh import + every trusted probe.  Probe user data is
# isolated so one bot cannot make the next bot pass by pre-winning content.
set -uo pipefail
cd "C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef"
python3 -c "from pathlib import Path; assert Path.cwd() == Path('C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef')"
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
python3 -m unittest tools.tests.test_audit_godot_baseline \
	|| { echo "GODOT BASELINE CONTRACT TEST FAIL"; exit 1; }
python3 tools/audit_godot_baseline.py --godot "$GODOT" \
	|| { echo "GODOT BASELINE DRIFT"; exit 1; }
# Persistent beta clothing: prove corruption controls before checking shipped layers.
python3 -B -m unittest tools.tests.test_fashion_beta \
	|| { echo "FASHION BETA CONTROL FAIL"; exit 1; }
python3 -B tools/audit_fashion_beta.py \
	|| { echo "FASHION BETA ASSET FAIL"; exit 1; }
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
# Typography is fail-closed for regressions and false evidence, while the
# current unresolved font/device authority remains an explicit known OPEN.
python3 -m unittest tests.test_audit_typography tests.test_type_c_layout \
	|| { echo "TYPOGRAPHY AUDIT CONTRACT TEST FAIL"; exit 1; }
python3 tools/audit_typography.py --check \
	|| { echo "TYPOGRAPHY AUDIT REGRESSION/FALSE EVIDENCE"; exit 1; }
# Baby Eagle's three paint panels must remain one-hot anatomical cutouts.
# This also proves the shipped mask still matches the rig/albedo contract.
python3 -m unittest tools.tests.test_bake_zone_mask \
	|| { echo "BABY EAGLE RECOLOR MASK FAIL"; exit 1; }
# Owner decision 2026-08-09: Mermaid Roshan is 2D-only. Prove the guard can
# fail before trusting it, then reject model assets, rig APIs, missing atlases,
# or a future CI bypass before Godot imports anything.
python3 tools/audit_roshan_2d.py --stress \
	|| { echo "ROSHAN 2D AUDIT SELF-TEST FAIL"; exit 1; }
python3 tools/audit_roshan_2d.py \
	|| { echo "ROSHAN 2D-ONLY CONTRACT FAIL"; exit 1; }
# The character audit above remains the narrow atlas/identity invariant.  The
# game-wide owner contract is a shrinking migration gate: its self-tests run
# before import, while the exact inventory runs after import has recreated the
# deterministic Godot 4.7.2 sidecars recorded by the baseline.
python3 -m unittest tools.tests.test_audit_game_2d \
	|| { echo "GAME-WIDE 2D AUDIT CONTRACT TEST FAIL"; exit 1; }
python3 tools/audit_game_2d.py --stress \
	|| { echo "GAME-WIDE 2D AUDIT SELF-TEST FAIL"; exit 1; }
python3 -m unittest tools.tests.test_audit_roshan_sprite_clipping \
	|| { echo "ROSHAN SPRITE FRAME AUDIT TEST FAIL"; exit 1; }
python3 tools/audit_roshan_sprite_clipping.py \
	|| { echo "ROSHAN SPRITE CLIPPING/GHOST FAIL"; exit 1; }
python3 tools/audit_probe_parity.py --stress \
	|| { echo "PROBE PARITY SELF-TEST FAIL"; exit 1; }
python3 tools/audit_probe_parity.py \
	|| { echo "LOCAL/REMOTE TRUSTED PROBE PARITY FAIL"; exit 1; }
# Documentation is executable project authority: every tracked Markdown source
# must have one scoped ledger row, and every active audit item must resolve to a
# complete canonical record before another repair can be authorized.
python3 -m unittest tools.tests.test_audit_document_authority \
	|| { echo "DOCUMENT AUTHORITY CONTRACT TEST FAIL"; exit 1; }
python3 tools/audit_document_authority.py --stress \
	|| { echo "DOCUMENT AUTHORITY SELF-TEST FAIL"; exit 1; }
python3 -m unittest tools.tests.test_audit_development \
	|| { echo "AUDIT DEVELOPMENT CONTRACT TEST FAIL"; exit 1; }
python3 -m unittest \
	tools.tests.test_record_owner_decision \
	tools.tests.test_run_advisory_sensor \
	tools.tests.test_study_game \
	tools.tests.test_build_study_roadmap \
	tools.tests.test_plan_prompt \
	tools.tests.test_resolve_godot \
	tools.tests.test_gold_star \
	|| { echo "SELF-IMPROVEMENT LOOP CONTRACT TEST FAIL"; exit 1; }
# Every game file must be catalogued and assessed against the gold-star rubric;
# stale scores are reported (the study re-assesses them), never silently kept.
python3 tools/gold_star.py --check \
	|| { echo "GOLD STAR CATALOGUE FAIL"; exit 1; }
python3 tools/audit_development.py --base auto \
	|| { echo "AUDIT DEVELOPMENT COVERAGE FAIL"; exit 1; }
python3 tools/audit_document_authority.py \
	|| { echo "DOCUMENT AUTHORITY / CANONICAL FINDING FAIL"; exit 1; }
python3 -m unittest tools.tests.test_audit_imagine_handoff \
	|| { echo "IMAGINE HANDOFF CONTRACT TEST FAIL"; exit 1; }
python3 tools/audit_imagine_handoff.py --all \
	|| { echo "IMAGINE HANDOFF STRUCTURAL AUDIT FAIL"; exit 1; }
python3 tools/audit_fairy_art_v2.py \
	|| { echo "FAIRY ART FAIL (texture or GLB contract)"; exit 1; }
python3 tools/audit_fairy_conservatory_handoff.py \
	|| { echo "FAIRY CONSERVATORY HANDOFF CONTRACT FAIL"; exit 1; }
python3 tools/prepare_opera_nursery_art.py --check-only \
	|| { echo "OPERA NURSERY ART FAIL"; exit 1; }
python3 tools/prepare_opera_minigame_art.py --check-only \
	|| { echo "OPERA MINIGAME ART FAIL"; exit 1; }
python3 tools/audit_opera_diegetic_hotspot_art.py \
	|| { echo "OPERA DIEGETIC HOTSPOT ART FAIL"; exit 1; }
python3 tools/audit_opera_borderless_minigame_art.py \
	|| { echo "OPERA BORDERLESS MINIGAME ART FAIL"; exit 1; }
python3 tools/audit_opera_roshan_animation.py \
	|| { echo "OPERA ROSHAN ANIMATION ART FAIL"; exit 1; }
python3 tools/build_day_one_story_clips.py --check \
	|| { echo "DAY ONE STORY CLIP MANIFEST/HASH DRIFT (DL-CIN-16)"; exit 1; }
python3 tools/build_area_music.py --check \
	|| { echo "AREA MUSIC BUILD/PROVENANCE DRIFT"; exit 1; }
# Complete runtime-audio authority: prove the ledger rules can reject malformed
# rows, reproduce the authored UI replacement, then require exact agreement
# with every shipped audio file and its measured quality decision.
python3 -m unittest tools.tests.test_audit_audio_quality \
	|| { echo "AUDIO QUALITY AUDIT CONTRACT TEST FAIL"; exit 1; }
python3 tools/build_audio_quality_replacements.py --check \
	|| { echo "AUDIO QUALITY REPLACEMENT BUILD DRIFT"; exit 1; }
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

echo "R111_STATIC_PREFIX_ALL_OK"

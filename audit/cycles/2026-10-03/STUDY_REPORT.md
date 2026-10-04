# Game study — 2026-10-03

Status: `SUPPORTING_CURRENT` advisory draft. Machine evidence, owner review, device and child acceptance remain separate.

## 0. Cycle header

- Studied head: `30d82725661044de63b682f5b13ba8f19101892b`; as of 2026-10-03.
- Working tree: changed; measurements include listed uncommitted changes.
- Previous cycle: baseline_measurement. Changes: 0 commits, 78 paths.
- CI: MEASURED; https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/37138772061.

## 1. What changed since the last cycle

- `self-improvement-loop-implementation-20261003`: Implement LP0-LP10 of the commissioned feedback-loop handoff: measured study cycles, evidence-backed candidate strengths, owner-decision intake, validated lessons, prompt recipes, generated roadmap/history/verification sweep and truthful advisory sensor results. LP11 schedules and real owner/device/child cycles remain gated. Existing dirty animation-policy work is preserved separately on rescue/peter-windows-20261003-self-improvement-start at f558ead4 and is excluded from this implementation. Owner scope extension: verify latest stable Godot across project, align remaining 4.7.1 capture constraints to canonical 4.7.2, and prevent default local PATH 4.7.1 use. Current production pins already match the official latest stable; historical version evidence remains unchanged. (design/audit_impacts/self-improvement-loop-implementation-20261003.json).

## 2. Strengths observed

No structured strengths observations recorded. Candidate register evidence is reviewed through the roadmap/recipe workflow.

## 3. Weaknesses and sensor coverage

| Sensor | Collection | Evidence status / gap |
|---|---|---|
| document_authority | MEASURED | Read measured summary in study.json |
| game_2d | MEASURED | UNSATISFIED |
| typography | MEASURED | OPEN |
| visual_profile | MEASURED | FINDINGS_RECORDED |
- Advisory `Dust boss balance playtest (advisory)`: MEASURED — Explicit terminal result recorded; no human acceptance inferred.
- Advisory `Opera balance playtest (advisory)`: CAPPED — At least one simulation reached its cap.
- Advisory `Publish opera art manifest (advisory)`: NOT_MEASURED — No explicit terminal result in the advisory log.
- Advisory `Upload opera art manifest`: MEASURED — Exact-run nonempty artifact exists; upload does not prove capture quality.
- Advisory `Capture first-world visual review`: FAIL — Failure, timeout, empty artifact or NOT_MEASURED appears in advisory output.
- Advisory `Capture legacy human-art diagnostic`: NOT_MEASURED — No explicit terminal result in the advisory log.
- Advisory `Upload legacy human-art diagnostic`: NOT_MEASURED — Expected nonempty upload artifact is absent or expired.
- Advisory `Capture Sky Lagoon visual review`: FAIL — Failure, timeout, empty artifact or NOT_MEASURED appears in advisory output.
- Advisory `Upload Sky Lagoon visual review`: NOT_MEASURED — Expected nonempty upload artifact is absent or expired.
- Advisory `Capture northern-world visual review`: NOT_MEASURED — No explicit terminal result in the advisory log.
- Advisory `Upload northern-world visual review`: MEASURED — Exact-run nonempty artifact exists; upload does not prove capture quality.
- Advisory `Capture dust-boss arena review`: NOT_MEASURED — No explicit terminal result in the advisory log.
- Advisory `Upload dust-boss arena review`: MEASURED — Exact-run nonempty artifact exists; upload does not prove capture quality.
- Advisory `Capture pearl-castle visual review`: NOT_MEASURED — No explicit terminal result in the advisory log.
- Advisory `Upload pearl-castle visual review`: NOT_MEASURED — Expected nonempty upload artifact is absent or expired.
- Advisory `Upload advisory sensor receipts`: NOT_MEASURED — Expected nonempty upload artifact is absent or expired.
- CI attribution gap: 118 result/verdict lines have no proven advisory owner; retained in study.json and excluded from passing measurements.
  - probes / UNKNOWN STEP / 2026-10-03T17:02:29.3165602Z ^[[36;1m# pass proves every rule can fail before the real project is gated.^[[0m
  - probes / UNKNOWN STEP / 2026-10-03T17:02:29.3168497Z ^[[36;1m# exhaustive ledger/canonical-record checks can fail, then gate the^[[0m
  - probes / UNKNOWN STEP / 2026-10-03T17:02:48.1413014Z ROSHAN2D| RESULT: ALL OK - active project is 2D Roshan only
  - probes / UNKNOWN STEP / 2026-10-03T17:02:55.8968980Z PROBE_PARITY|result: ALL OK
  - probes / UNKNOWN STEP / 2026-10-03T17:02:57.0897645Z AUDITDEV|RESULT|ALL OK
  - probes / UNKNOWN STEP / 2026-10-03T17:02:58.5383141Z DOCAUTH|RESULT|ALL OK
  - probes / UNKNOWN STEP / 2026-10-03T17:03:10.9513890Z HOTSPOT_ART|result: ALL OK (4 hashes, 2 alpha states, 1 connected object)
  - probes / UNKNOWN STEP / 2026-10-03T17:03:11.1300785Z OPERA_BORDERLESS_ART|result: ALL OK (2 subjects, exact hashes, connected alpha, no chroma spill)
  - probes / UNKNOWN STEP / 2026-10-03T17:03:11.4565315Z OPERA_ROSHAN_ART|result: ALL OK (13 careers, 208 reviewed frames)
  - probes / UNKNOWN STEP / 2026-10-03T17:04:02.5073297Z ^[[36;1mtimeout 20m godot --headless --path . --import 2>&1 | tee /tmp/import.out || (echo "IMPORT FAIL (hang or error)" && exit 1)^[[0m
  - probes / UNKNOWN STEP / 2026-10-03T17:04:02.5074003Z ^[[36;1mif grep -qE 'SCRIPT ERROR|Invalid assignment of property or key|The tweened property .* does not exist|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)|Parse Error|Compile Error|ERR_FILE_CORRUPT|Error importing|Cannot load resource' /tmp/import.out; then^[[0m
  - probes / UNKNOWN STEP / 2026-10-03T17:04:02.5074595Z ^[[36;1m  echo "IMPORT FAIL (resource or script error)"^[[0m
  - probes / UNKNOWN STEP / 2026-10-03T17:05:05.5003911Z ##[group]Run FAILED=0
  - probes / UNKNOWN STEP / 2026-10-03T17:05:05.5004385Z ^[[36;1m  if ! OUT=$(timeout 60 godot --headless --check-only --script "$f" 2>&1); then^[[0m
  - probes / UNKNOWN STEP / 2026-10-03T17:05:05.5004637Z ^[[36;1m    echo "COMPILE FAIL: $f"; echo "$OUT" | head -20; FAILED=1^[[0m
  - probes / UNKNOWN STEP / 2026-10-03T17:05:05.5005064Z ^[[36;1mexit $FAILED^[[0m
  - probes / UNKNOWN STEP / 2026-10-03T17:11:38.8912736Z ^[[36;1mRUNTIME_ERROR_RE='SCRIPT ERROR|Invalid assignment of property or key|The tweened property .* does not exist|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)'^[[0m
  - probes / UNKNOWN STEP / 2026-10-03T17:11:38.8913251Z ^[[36;1mFAILURE_RE='FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error'^[[0m
  - probes / UNKNOWN STEP / 2026-10-03T17:11:38.8919937Z ^[[36;1m    FAILED=1^[[0m
  - probes / UNKNOWN STEP / 2026-10-03T17:11:38.8922538Z ^[[36;1m    timeout 8m godot --headless -s "scripts/$p.gd" -- --touch "$TOUCH_TEST_MODE" 2>&1 | tee "/tmp/$p.out" || PROBE_RC=$?^[[0m
  - Report excerpt capped at 20 lines; all 118 lines remain in study.json.
- `MA-VIS-002` needs source recheck: scripts/probe_sky_lagoon_art.gd.
- `MA-ACCESS-003` needs source recheck: scripts/games/seek.gd.
- `MA-CI-004` needs source recheck: .github/workflows/probes.yml, scripts/ci.sh.
- `MA-CODE-003` needs source recheck: scripts/combat_arena.gd, scripts/dungeon_puzzle_room.gd, scripts/stuffie_battle.gd.
- `MA-PERF-002` needs source recheck: scripts/main.gd.
- `MA-PERF-003` needs source recheck: scripts/companion.gd, scripts/day_one_director.gd, scripts/main.gd, scripts/opera_gesture_surface.gd.
- `MA-SAVE-001` needs source recheck: scripts/arena/castle_rooms_25d.gd.
- `MA-AUDIO-002` needs source recheck: scripts/mic_input.gd.
- `MA-CI-008` needs source recheck: .github/workflows/probes.yml, scripts/probe_opera_2d_balance.gd.
- `MA-TYPE-004` needs source recheck: audit/typography_manifest.json, scripts/audio_director.gd, scripts/games/dust_boss.gd.
- Motion `2026-09-06-chapter2-lawn-ember-alpha` (character): 0 recorded human/owner verdict entries; Owner review of gameplay composition and synthetic narration, aspect-ratio/device performance and touch, child comprehension/pacing, green integrated dev APK; all nine clean cinematic first frames and external generation bindings, full-frame delivery provenance and human acceptance. Three arrival first-frame candidates are unaccepted for scale/costume/position drift. No whole-game audit satisfaction or cinematic acceptance claimed. The bounded lawn ignition implementation is covered under the new DL-INT-02 clarification, but target-device/child/owner action review and other MA-PLAY-004 jobs remain open..
- Motion `2026-09-06-chapter2-scale-handoff` (character): 0 recorded human/owner verdict entries; Owner visual, target-device and child acceptance pending. Archive publication does not grant generator readiness or cinematic delivery acceptance..
- Motion `hall-art-followup-2026-09-06` (character): 0 recorded human/owner verdict entries; Current captures cover only configured phase states. Complete performance action/cadence, natural navigation, target-phone quality/performance, child and owner acceptance remain open. Game-wide 4.5 is not met. Python pixel cleanup remains unauthorised and no CLI/API generation is authorised..
- Motion `2026-09-12-roshan-grok-auditions` (character): 0 recorded human/owner verdict entries; Generation is blocked on exact human approval of two new opening compositions and remote binding promotion. No videos have been generated; later motion selection, sprite construction, runtime/device/child/owner acceptance and independent cinematic delivery remain outstanding. Local uninterrupted suite failure is preserved, missing probe evidence recovered by two complete fresh-profile reruns; exact-head remote CI is required before any dev integration. No runtime integration or release is claimed. MA-VIS-006 and global strict 2D/visual satisfaction remain open. Archive publication must be established by a separate exact-commit remote receipt..
- Motion `2026-09-13-roshan-grok-video-first` (character): 0 recorded human/owner verdict entries; Exact opening approval and actual video-tool/input-binding evidence remain pending. No returned video was inspected or accepted. MA-VIS-006 remains open; no runtime, device, child, cinematic delivery or release acceptance..
- Motion `sky-lagoon-local-animation-20260930` (object): 0 recorded human/owner verdict entries; All outputs are reference drafts. Spatial source resampling/articulation is explicit; not human hand drawing, fresh independent frame redraws or accepted AI motion. Owner selection, production topology/contact/loop, engine sampling, phone/child and full-frame cinematic/release gates remain open. Backend credentials and applicable IMAGE_1 layout approval block external generation, not review publication. Related MA-VIS-002/006 lifecycles unchanged..
- Motion `sky-lagoon-moderate-animation-20260930` (object): 0 recorded human/owner verdict entries; Reference samples only; visual continuity/contact, new owner selection, runtime/device/child and full-frame cinematic gates remain open..
- Motion `sky-lagoon-motion-owner-qc-20260930` (object): 2 recorded human/owner verdict entries; Current set fails the owner animation brief; swing axis is explicitly rejected. New pilot, other fresh motion poses, fresh frame redraws, owner selection, runtime/device/child and full-frame cinematic acceptance remain unfulfilled. New generation is bounded to the absent swing perspective poses; existing approved art supplies identity/style only. Built-in image generation is a pose-reference trial, not a Chinese video API success claim..
- Motion `sky-lagoon-review-v3-20261001` (object): 0 recorded human/owner verdict entries; References only. Agent inspection does not grant final runtime, Mobile, device, child, owner or cinematic acceptance; no finding closed..
- Motion `sky-lagoon-v14-animation-20260916` (character): 0 recorded human/owner verdict entries; Owner art/crop acceptance, interface-specific minimum, device review, clean alpha in motion and runtime implementation remain open. Draft cards are not generation-ready. MA-VIS-002 unchanged; archive completeness is verified at content commit 23179829b6452ff9b2ac6e4a58662935bffe340f. No claim of 4.9 or cinematic acceptance. Integration ready-card validator still requires reconciliation with the owner minimum-duration profile and native input aspect; cards remain DRAFT..

## 4. Loop health

Open findings: 61; without a history entry for 30 days: 38; fixed pending verification: 12.
Impact records: 79; structured lessons: 2; pending validations: 38; failed validations retained: 36.

| Health target | Value | Target | Status |
|---|---|---|---|
| stale_open_fraction | 0.6229508196721312 | <=0.10 | NEEDS_ATTENTION |
| old_unverified_fixes | 7 | 0 | NEEDS_ATTENTION |
| lessons_fraction_since_lp4 | NOT_MEASURED | >=0.50 | NOT_MEASURED |
| repeated_owner_corrections | 0 | 0 | NOT_MEASURED |
| roadmap_current_cycle | True | regenerated this cycle | ON_TARGET |
| handoffs_waiting_two_cycles | NOT_MEASURED | all listed | NOT_MEASURED |

| Metric since previous observation | Previous | Current | Delta |
|---|---|---|---|
| fixed_pending_verification | 12 | 12 | 0 |
| stale_open | 38 | 38 | 0 |
| structured_lessons_fraction | None | 0.012658227848101266 | NOT_COMPARABLE |

Day Two library: MEASURED; 52 changed watched sources, 5 stale art hashes. Previous observation comparison: NOT_COMPARABLE.

## 5. Roadmap delta

Handoffs inventoried: 8. Unmerged fetched branches: 193. Target presence is not implementation or acceptance.
Run tools/build_study_roadmap.py with this study.json to generate Repair, Grow and Strengthen lanes.

## 6. Next prompts

1. "Repair the reported advisory sensor gaps" — `INT-REPAIR`; use exact results and preserve acceptance gaps.
2. "Study the game" — `INT-STUDY`; retain this cycle as the previous observation.

## 7. Owner questions and external evidence

The handoff defaults apply. Scheduled automation remains deferred until two complete manual cycles and owner agreement. No telemetry collected. Owner/device/child sessions need actual evidence; this generated draft cannot supply it.

## 8. Lessons recorded

Cycle evidence: EVIDENCE_RECORDED_REQUIRES_REVIEW. Recorded owner decisions: 8; operating defaults: 8.

- `self-improvement-loop-implementation-20261003`: {"lesson": "A successful mandatory CI run does not prove that advisory pacing/capture sensors measured anything; studies must retain each sensor verdict and unavailable evidence.", "write_back": "tools/study_game.py"}; write-back named; design/audit_impacts/self-improvement-loop-implementation-20261003.json.
- `self-improvement-loop-implementation-20261003`: {"lesson": "A recipe must include the intentional action that creates its promised result; a fresh bakery plan exposed a missing baking/retrieval transition and unproven native background coverage.", "write_back": "tools/plan_prompt.py"}; write-back named; design/audit_impacts/self-improvement-loop-implementation-20261003.json.

PENDING entries with matching finished CI are proposed for record reconciliation only; source records remain unchanged.
- `2026-09-06-audit-development-contract`: No exact matching CI result collected.
- `2026-09-06-chapter2-lawn-ember-alpha`: No exact matching CI result collected.
- `2026-09-06-next-art-priorities`: No exact matching CI result collected.
- `2026-09-06-next-art-priorities`: No exact matching CI result collected.
- `2026-09-06-stage-pathfinding`: No exact matching CI result collected.
- `2026-09-09-day-one-toilet-clean`: No exact matching CI result collected.
- `2026-09-11-roshan-animation-language`: No exact matching CI result collected.
- `arborist-art-recovery-20260929`: No exact matching CI result collected.
- `codex-opera-imp-contest-handoff-20260930`: No exact matching CI result collected.
- `codex-opera-imp-contest-handoff-rev2-20260930`: No exact matching CI result collected.
- `codex-opera-imp-contest-handoff-rev3-20260930`: No exact matching CI result collected.
- `codex-opera-imp-contest-handoff-rev4-20260930`: No exact matching CI result collected.
- `day-one-bathroom-touch-dirt-20261002`: No exact matching CI result collected.
- `day-one-cleanup-clips-per-room-20260923`: No exact matching CI result collected.
- `day-one-continue-softlock-20260923`: No exact matching CI result collected.
- `day-one-rebuild-handoff-20260923`: No exact matching CI result collected.
- `day-one-story-clips-runtime-20260923`: No exact matching CI result collected.
- `day-one-two-alpha-20260930`: No exact matching CI result collected.
- `day-one-usability-fixes-20260912`: No exact matching CI result collected.
- `day-two-objective-handoff-20260930`: No exact matching CI result collected.
- `day2-art-library-20260930`: No exact matching CI result collected.
- `job-game-takeover-audit-20260930`: No exact matching CI result collected.
- `job-platform-architecture-handoff-20260930`: No exact matching CI result collected.
- `lagoon-roshan-facing-20260923`: No exact matching CI result collected.
- `main-gd-dead-code-and-storage-plan-20260930`: No exact matching CI result collected.
- `master-audit-refinement-handoff-20260930`: No exact matching CI result collected.
- `opera-job-playtest-20260930`: No exact matching CI result collected.
- `rainbow-friend-follower-20260923`: No exact matching CI result collected.
- `reference-consolidation-handoff-20260930`: No exact matching CI result collected.
- `remove-3d-reef-20260923`: No exact matching CI result collected.
- `roshan-art-repairs-handoff-20260930`: No exact matching CI result collected.
- `roshan-canvas-swim-anchor-20260923`: No exact matching CI result collected.
- `roshan-identity-analysis-20260930`: No exact matching CI result collected.
- `self-improvement-loop-handoff-20261003`: No exact matching CI result collected.
- `self-improvement-loop-implementation-20261003`: No exact matching CI result collected.
- `start-menu-new-game-hold-cue-20260923`: No exact matching CI result collected.
- `start-menu-options-hold-20260923`: No exact matching CI result collected.
- `visual-design-language-handoff-20260930`: No exact matching CI result collected.

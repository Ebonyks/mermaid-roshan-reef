# Minigame art and animation audit — 5 September 2026

> Reconciliation note: this report's captures and scores are historical evidence from the original `775ceee1`-based worktree. The source repairs are now reconciled onto clean dev base `f4a5de339f3a8b7b9e4081924f4d3127d54959d7`, but no old capture is promoted to a current-candidate review. Game-wide coverage and the 4.5 threshold remain open. See `audit/minigame_art_quality_2026-09-05/current_scope_addendum.md`, `missing_coverage.md`, and `art_repair_backlog.md`.

**Status: IN PROGRESS / standard not met.** This is a review and repair candidate, not a release, owner acceptance, or closure of the master audit. The art scope is game-wide; the previously requested practice → stage mechanics remain confined to Ballerina, Magician and Pop Star in the Opera Hall.

The user's impression of inconsistency is supported by the inspected images. Richly painted characters, rooms and large props sit beside simpler activity boards, diagrams and effects. Some individually attractive character sheets contain separate poses that the runtime treats as short animation loops. Composition, action meaning and contact are therefore as important as replacing weak PNGs.

## Read the detailed findings

- [Opera: all fifteen career families, scores and live art owners](../audit/minigame_art_quality_2026-09-05/opera_review.md)
- [Non-Opera minigames: inspected assets, missing evidence and replacement specifications](../audit/minigame_art_quality_2026-09-05/nonopera_review.md)
- [Animation: pose selection, timing, anatomy and missing action states](../audit/minigame_art_quality_2026-09-05/animation_review.md)
- [Racer replacement attempt and independent rejection](../audit/minigame_art_quality_2026-09-05/racer_reaudit.md)
- [Machine-readable open registry](../audit/minigame_art_quality_2026-09-05/registry.json) and [repeatable review protocol](../audit/minigame_art_quality_2026-09-05/protocol.md)

Sol reviewed the master criteria, Opera surfaces, animation sheets and repair candidates. Luna traced non-Opera callers, inspected weak source assets and prepared state captures. The parent reviewed evidence and implementation claims, rejected stale/obscured captures and corrected diagnoses that did not match live code. In particular, shipping hold/circle/swipe activities already route through painted widget families: deleting their unused generic fallback would not improve the current game.

## Scores: strengths, weaknesses and specific next work

These are subjective **baseline composition scores**, not complete eight-dimension acceptance. Historical captures are dated in the detailed report and cannot establish a changed candidate's score. No family is certified at 4.5. A weak state cannot be averaged into a passing family.

| Career | Baseline /5 | Keep | Weakness to repair | Specific next batch |
|---|---:|---|---|---|
| Chef | 3.6 | Kitchen, costume and painted baking vocabulary | Bowl/fill/contact cues look diagrammatic beside the room | Consistent bowl and pitcher states; bind pour to the actual vessel and visible fill |
| Detective | 4.1 | Clue board, magnifier, costume | Weak slot contrast and excessive vignette/cursor dominance | Larger painted clue cards; local lens reveal and settle |
| Ballerina | 4.0 | Accepted held poses, room and music box | Large ribbon/twirl guides resemble instrumentation | Fabric ribbon progression and shell checkpoints; retain the `DL-MOT-09` pose restriction |
| Candy Maker | 3.4 | Factory and characters | Framed syrup composition and mismatched activity layers | One factory-compatible mold/pour/wrapper family with transparent boundaries |
| Stuffie Doctor | 3.8 | Clinic, costume and patient art | Activity emphasis and diagnostic widgets compete with the patient | Increase patient/contact ownership; local scan, wash and bandage states |
| Farmer | 3.1 | Garden beds and approved plants | Flat seed treatment; incomplete material/contact relationship | One consistent seed → sprout → mature plant kit; preserve distinct plant roles |
| Boxer | 4.2 | Room, imp, mitts and belt | Foreground glove/telegraph finish is simpler | Matched glove anticipation/contact/recoil; small local telegraphs |
| Magician | 4.1 | Cabinet, rope, hat, characters | Small objects and schematic task presentation | Large object-specific choices, cabinet and reveal states |
| Painter | 3.3 | Paint garden, easel and palette vocabulary | Canvas/trace/progress feels detached | Anchor the canvas to one easel; truthful progressive paint coverage |
| Astronaut | 2.8 | Lab, rocket and costume | Pipes and connection grid look like diagrams | Coherent brass/aqua pipe pieces, sockets, flow and valve states |
| Racer | 4.1 | Existing driving engine, circuit, kart and finish | Large lower control, small/crowded drivers, unfinished feedback | Correctly identified directional control and clearer cockpit composition; see rejected tire experiment |
| Pop Star | 3.8 | Stage, singer, costumed imp | Oversized flat pads and schematic practice card | Painted shell-note pads with beat/contact feedback tied to actual notes |
| Nursery | 3.1 | Nursery setting and character identity | Catch/feed/wash interaction art reads as diagrams | Readable baby/cradle roles and authored catch/contact/settle states |
| Geologist | 2.7 | Rebuilt four mechanics and complete-fin costume poses | Striped fallback backdrop, empty board, coarse pan/geode/fossil materials | Cave/workbench composition plus fossil, pan, geode and mineral action kits |
| Teacher | 3.5 | Library, teacher costume, simple learning progression | Worksheet-like surface and jumping pointer poses | Coherent classroom manipulatives and pointer-to-target staging; preserve mathematical shape/count meaning |

Racer's later independent repair review scored the attempted tire-thumb control 4.44, with a critical meaning score of 3.8; the full inspected scene scored 3.9. This is a different dated review, not an averaged replacement for the baseline number. The tire experiment was rejected and removed.

Directly inspected weak non-Opera source assets include `assets/mg/carrot.png` (3.0), `wateringcan.png` (2.5), `k_sprout.png` (3.0), and the five live mature results `k_flower1.png`, `flower.png`, `flower2.png`, `k_flower2.png`, `flower3.png` (3.0 each). The watering can includes unwanted source/background material. The carrot and garden family have much simpler material and contour treatment than neighboring painted props. `flower4.png` exists but is not in the current live garden list; it must not drive an unnecessary commission.

The broader registry names 33 known surfaces/families and 56 source records, including the eight weak picture props and all fifteen actor sheets. It is an initial source-bound inventory, **not an exhaustive list of every raster, atlas cell and indirect runtime dependency**. Uncaptured families remain unscored. Grand Puff's rebuild is integrated in the development base; its changed runtime needs fresh capture and source-hash review before grading.

The four active picture cards were also inspected at 1280×720: Snowman 3.5, Garden 3.0, Trampoline 3.2 and Xmas 4.1 before the final garden presentation repair. A separate independent reaudit raised Garden to **3.7/5** after that repair, still below threshold. These are observed-state scores, with natural animation cadence still unverified. The retired slide card delegates to the Lagoon playground and is not a fifth active picture card.

## Repairs actually made and their reaudits

1. **Geologist brush reuse.** Bound the existing approved `magic_cleaning_brush.png`, preserved its aspect ratio and placed its bristle contact at the finger. No source pixels were changed. Independent isolated-art score: 4.7, keep. Current contact presentation: 3.5, still open; the scene needs visible excavation/contact and better material context. A good brush does not make the workbench pass.
2. **Geologist and Teacher pose playback.** The previous 7 fps work cycle revisited unrelated poses every approximately 0.57 seconds. Geologist's crystal repeatedly appeared/disappeared; Teacher's pointer changed direction abruptly. Held semantic cells replace these loops, and Geologist menu/idle avoid the two incomplete-fin cells. Celebrations now play once at 2 fps and hold. Originals are preserved. Independent review accepts this as containment, while authored-action completeness remains 2.5: proper idle, travel and work sequences are still required.
3. **Racer trial and rejection.** Reused a painted wheel as a drag token, captured center/left/right/lap states, then independently reaudited it. It was actually a tire, not a steering wheel. Its finish could not compensate for uncertain interaction meaning. Restored the prior clearer control and retained only the small lap flags, which explain the existing lap dials. Driving, steering hit area, turbo and save behavior are unchanged.
4. **Generated washing pan trial and rejection.** The new pan has an attractive painted surface but arrived as RGB with a painted checkerboard. It is not a transparent cutout and was never loaded into runtime. The original, exact prompt, references, hashes and rejected disposition are preserved in `assets_src/minigame_art_quality_2026-09-05/`. No false alpha acceptance and no destructive source repair.
5. **Picture-game composition and payoff.** Gave the objective, roll instruction, hint and success labels explicit layout boxes; objectives had been wrapping one letter wide. Moved the garden sun below the header. Kept the five mature flowers visible and disabled through the reward instead of hiding their owning buttons, and removed the large button panels behind the plants while preserving touch areas. A new regression check confirms that all five flowers remain visible at completion. The weak source flower and watering-can art remain open replacements.

## Master criteria and acceptance process

Authority remains [the canonical master audit](../audit/MASTER_AUDIT_2026-08-09.md) and [the comprehensive design language](06_COMPREHENSIVE_DESIGN_LANGUAGE.md). This supporting review does not weaken them.

Review each live item for identity, painted finish, contours/alpha edges, phone readability, animation/contact, scene ownership, consistency and technical integrity. A 4.5 candidate needs every applicable dimension at least 4.5, current runtime evidence for every declared relevant state and no unresolved blocking defect. Static props may mark animation inapplicable with a specific reason. A required animated subject may not use that exception. A source illustration score is separate from its scene presentation score. Owner runtime acceptance remains necessary for 5/5 under `DL-VIS-07`.

For each item:

1. Freeze the current source/hash and capture the failing state. Identify the live caller, touch bounds, visual anchor, palette, light, layer and contact point.
2. Inventory approved equivalents. Reuse only when the object and state mean the same thing; a tire cannot automatically substitute for a steering wheel, and two flowers cannot replace five distinct mature results.
3. Repair composition or routing before commissioning pixels. Generate only the named missing object/state or scene. Preserve originals, rejected attempts, prompts, hashes and provenance. Respect native per-screen background coverage; enlargement is not native detail.
4. Inspect source edges, identity, topology, padding and material. Reject painted transparency, contaminated cutouts, missing fins, duplicated props and inconsistent neighboring states before import.
5. Import and exercise real input. Capture idle/demo, active contact, changed state, payoff and settle at Mobile 1280×720 and a representative phone aspect. Record actual renderer, source hashes and state. A frozen simulation sequence is not a real-time motion or target-device performance test.
6. Have a different Sol/Luna reviewer inspect the candidate. Preserve prior and candidate scores. Rejection returns the item to production; do not round up or average away a critical weakness.
7. Run focused gameplay and asset gates, then the full repository gate. Retain no-fail play, one-finger input, voice/pointer objectives, save compatibility and protected art.
8. Repeat the dependency inventory and independent runtime audit before claiming game-wide completion. Keep owner, child and device gates explicit.

## Reconciled candidate verification

The gameplay parent `f4a5de339f3a8b7b9e4081924f4d3127d54959d7` passes exact-head [CI run 34003370178](https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/34003370178), including the probe and music-provenance jobs. The same commit is integrated into `dev` and also passes [dev CI run 34007118167](https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/34007118167). This verifies the Racer, Geologist, Teacher and Hall mechanics candidate; it does not certify the additional art repairs or art quality.

The art registry now has nineteen passing focused contract tests and six rejecting stress fixtures. It checks real PNG structure/dimensions, rejects one screenshot relabeled across states, limits static-animation exceptions, and explicitly disclaims master/game-wide provenance authority. Code-source records explicitly normalize UTF-8 CRLF to LF for Windows/Linux portability; images and captures retain exact-byte hashes. Integrity mode passes while strict quality mode deliberately exits nonzero with `UNSATISFIED`. Coverage, Git revision and capture-origin declarations still require the canonical same-process runtime evidence contract and independent review.

The separate art candidate's complete isolated `scripts/ci.sh` run passed all 78 trusted probes on exact Godot 4.7.2. The [reconciled validation manifest](../audit/minigame_art_quality_2026-09-05/validation/reconciled/manifest.json) binds the six changed runtime/probe sources, complete raw log and readable transcript. Art quality remains unaccepted. Earlier focused probes were rerun with isolated user data after a test-profile mistake. The default desktop save and its rolling backup were modified during the initial unisolated runs; available files were preserved locally, but no immediate pre-run snapshot exists. No user save data is included in this publication.

The [native-source follow-up](../audit/minigame_art_quality_2026-09-05/opera_native_coverage_followup.md) found no authored same-room native-detail 2048×2048 source for any of the fifteen career rooms. This is a provenance/2K-screen benchmark gap, not a blanket regeneration order: Opera is a fixed 1280×720 Canvas scene and each route must be reviewed at actual shipping scale. Teacher was corrected in that follow-up: its live Library route uses eight `interactions_v4` tiles reconstructed from a 3640×2048 master, but the current master (`SHA-256 8c4dd2…618a2`) is the recorded whole-canvas Lanczos normalization of the 1672×941 generated ownership source, so it supplies geometric coverage without native authored detail. Smaller approved sources remain continuity references; padding or enlargement cannot establish native detail by metadata alone. The [repair backlog](../audit/minigame_art_quality_2026-09-05/art_repair_backlog.md) records per-game work and required states. The additional watering-can trial also failed actual alpha and stays outside runtime.

## Historical verification and remaining work

The following records describe the preserved pre-reconciliation art candidate. Its typography failures and counts are historical, not the current gameplay parent's status.

- Godot 4.7.2 Mobile import completed. Current visual diagnostics use a desktop RTX 3060 Ti, not the target Android device.
- Full Opera runtime probe: **ALL OK**, fifteen careers and seventy playable phases, including the new held-pose contracts.
- Existing Opera atlas integrity gate: **ALL OK**, thirteen careers and 208 reviewed cells. It excludes Geologist and Teacher and does not prove animation smoothness.
- Picture-game runtime probe: **OK**, all four active cards, ten garden growth steps, final-flower visibility, and feedback teardown/re-entry.
- True-2D regression gate: **NO_REGRESSION**, zero model files and 56 remaining production 3D files. The canonical migration remains **UNSATISFIED**; this art pass adds no 3D debt.
- Document authority: **ALL OK**, 530 inventory/ledger entries after classifying the supporting reports.
- New registry validator: twelve unit tests and six deliberately bad fixtures pass/reject as expected. Each claimed state must independently have current Mobile/HUD evidence; one good idle capture cannot legalize stale or diagnostic payoff evidence.
- Full `scripts/ci.sh`: **blocked by two existing typography contract failures**, including the stale U+2019 allowance and exact-line Dust Boss fixture. The full suite did not reach a green result. No integration or release is claimed.
- The registry deliberately reports **UNSATISFIED**. Missing asset-level coverage, action sequences, physical scene kits and target-device review are open work.

The pending production choice is explicit authorization for non-destructive Python cutout cleanup of generated RGB candidates. The image-editing tool instructions require that authorization; it has not been inferred from elapsed time. Until answered, rejected checkerboard art remains outside runtime. Background native-resolution gaps remain separate and cannot be solved by cutout cleanup.

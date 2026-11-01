# Roshan boxer, racer and pop star — native 2D source review

**FROZEN REVIEW DRAFT / COMPATIBILITY BLOCKED.** Three functional outfit/object-action prototypes are prepared, with editable Aseprite masters and exact native captures. They are not accepted skins, a complete interchangeable wardrobe or production character. The November demo freeze remains: no dev/master adoption, game scene/save/objective/voice/reward change or release.

## Inspect the actual work

[Overview](review/frozen_v3/outfits_and_glove_perspective.png): boxer contact, two-hand steering, supported microphone adjustment and a different boxer palm surface. Silent8second review clips: [boxer](review/frozen_v3/boxer_object_action.mp4), [racer](review/frozen_v3/racer_object_action.mp4), [popstar](review/frozen_v3/popstar_object_action.mp4). Native PNG keys and editable beat boards cover0,1.5,3.2,4,5.2,7 and8seconds; [mapping](review/frozen_v3/timeline.json).

| Active outfit | Existing game source | Native action and object ownership |
|---|---|---|
| boxer | Friendly padded championship | Guard, short fore-and-aft jab with authored guard/knuckle/palm surfaces, padded-mitt contact, return. Glove worn by left hand; mitt fixed. |
| racer | Opera Grand Prix, steering/TURBO | Both hands meet a complete wheel rim, turn left/right, release. Axle fixed; rim defines both grip targets. Mount is a diagnostic line. |
| popstar | Starlight Sound-Off, approved shell microphone | Reach to stand clamp, adjust supported upper microphone angle, release. Base fixed, upper microphone pivots at clamp, left hand supports it. |

These are presentations of existing job objects, not new gameplay objectives, story, failure states or audio. Ribbon Glide attentive work and a quiet available endpoint guide the study. Basic-animation praise does not accept these performances.

## One shared source rig

The corrected replacement seed is now pinned to published [cbf8b5b6](https://github.com/Ebonyks/mermaid-roshan-reef/tree/cbf8b5b6f9ff4313202d74ca1eafc4ba914bd539/assets_src/animation/native_rig_costumes_20261031/replacement_v6). [Anonymous verification](evidence/upstream_seed_remote_verification.json) checks all257required files and exact local render-input matches. The source remains render_v8 despite its replacement_v6 container name. The old26bd6d1f overlay is OWNER_REJECTED and is never a fallback.

The local pinned contract is `roshan.canvas.shared`1.0.0 in `contract/rig_v1.json`. All14Bone2D nodes/rest transforms,6902original common vertices/weights and original arm_bend/blink/tail_bend curve/timing text remain. Nine garment support vertices interpolate the original weights, making6911Body vertices; no bone/topology/rest fork. Headwear is a separate rigid Head-bound painted sprite. [Mesh proof](evidence/mesh_derivation.json), [curves](evidence/curve_identity.json).

The shared-contract chat alone owns skeleton/rest and common waist conventions. Its trial still has outline/visual failures and is not accepted/published. `contract/consumer_limits.json` is a provisional fit proposal, not a shared authority. Front is the sole available binding view; quarter/profile remain source gaps. Equality of fresh/live states never proves garment fit.

## Artwork, sources and bounded work

[Inventory](inventory.json) covers actual approved job cards/sheets, Fashion Designer items and real game objects before generation. [References](references/provenance.json) include exact room/background, character, prop and appearance images. New garments have complete RGBA replacement silhouettes. Clean anatomy removes old clothing; no old sleeves, blouse or tail clothing fills the new skins. Seed identity plates are retained; approved card gripping-hand crops substitute visibly during contact, and headgear may occlude hair. Whole-output hair/hand pixel identity is not claimed.

Five builtin ImageGen calls supplied one garment take per job, one glove-view sheet and one clean complete wheel. Native outputs remain unchanged under `native/`; exact prompts/tool invocation IDs/counts and unexposed model/provider/seed/usage fields are in [generation.json](generation.json) and `job_cards/`. Zero external paid API calls does not imply zero total cost. Aseprite performs raster isolation, uniform registration, recorded row mapping, source-bound parts/caps and declared local fabric/alpha repairs. Python measures pixels/geometry and verifies archives; inherited destructive counterexamples are test data, never delivery art.

The first90minute bound was exceeded at93.83minutes; [deviation](evidence/budget_deviation.json). A declared method revision kept the original start and cumulative120minute bound, freezing v3 at117.82minutes. No generation, drawing, cleanup, controller or animation edits follow that freeze. Five calls never reset. Active cleanup was not separately instrumented; the full117.82minute production window conservatively bounds it. Verification, lossless packaging and documentation continue separately. Earlier failed trials and exact v2 inputs remain under `evidence/` and `source_snapshots/v2/`.

Current source-v3 uses correct alpha-over below untouched painted anatomy and a five-pixel strip of the racer's own fabric under a rigid torso panel. Rounded source-arm overlaps and soft source-derived elbow caps do not establish anatomically natural or polished joints. No protected book, voice or friend original is altered. [Per-file sources, hashes, dimensions and license scope](asset_provenance.json).

## Machine verification — pass and fail are separate

[Summary](evidence/verification_v3/native_summary.json), [exact frozen inputs](evidence/verification_v3/final_frozen_input_check.json).

- **PASS:** all189frozen inputs unchanged; three full-set original-motion geometry/motion regressions at inherited floors. The boxer wrapper's1200second timeout is retained; only unfinished meshes resumed using exact completed subreports.
- **PASS:** new actions meet speed/acceleration, uniform bone scale, fixed fixtures, numerical grip/painted-wrist contact and exact loop endpoints. Boxer knuckle/target error stays below0.022native pixels; all three authored glove surfaces are used.
- **FAIL:** all3new actions fail attachment alpha, including the right wrist; boxer also fails right shoulder occupancy. Numerical contact does not waive missing visible tissue. [Action audit](evidence/verification_v3/object_action_audit.json).
- **PASS for state only:**216combinations,648exact fresh/live pairs,20736live swaps, zero matrix drift or eye leaks, atomic invalid binding rejection.
- **FAIL:**138/648mixed original-motion snapshots fail independent outline/contact checks;9/9strict original-seed restoration comparisons fail. An independent diagnostic isolates23opaque fin pixels differing by one colour level and about1.79e-7transform error. No exact-restoration waiver. [Switching](evidence/verification_v3/switch_receipt.json), [outlines](evidence/verification_v3/mixed_outline_audit.json), [diagnostic](evidence/original_restore_diagnostic/pixel_delta.json).
- **FAIL overall:**108mixed body/tail object-contact poses all meet numerical support/grip tolerances, but only7/108pass full sampled outline/attachment. Headwear matches the action; this is not every head/view/time combination. [Mixed contact](evidence/verification_v3/mixed_action_audit.json).
- **PASS:**16applicable actual rendered faults detected; racer/popstar glove-view controls explicitly inapplicable.7394old-clothes survey pixels have zero retained clothing;27source-poison cases have zero leak. [Controls](evidence/verification_v3/controls_audit.json).
- **PASS:**55current Aseprite layers and10archive prop layers reopen/export with identical RGBA pixels. All723native action frames reconstruct byte-for-byte from separate lossless RGB/alpha tracks in `*_native_rgba.mkv`; [receipt/decoder commands](review/frozen_v3/lossless_archive_receipt.json). Review MP4s are separate lossy1280x720square-pixel30fpsencodes, not exact evidence.

The mixed-contact helper hid the diagnostic racer support line and left caller visibility hidden for one complete-scene comparison. [Targeted proof](evidence/verification_v3/racer_fixture_visibility_diagnostic.json) reproduces731changed pixels and restores zero differences by restoring only that verifier visibility. Original data remains; no source defect or controller repair is claimed. Avatar outline/contact measurements are unaffected. [Verifier limits](evidence/verification_v3/verifier_limits.json).

## Production regression and audit authority

[Latest baseline coverage](evidence/baseline_gate_resolution.json) has actual passing results for import/all82trusted probes and all56existing static commands on unchanged production. The initial full runtime sequence passed79/82; the failed3focused retries pass. Initial static audio/visual commands hit local900second bounds; the unchanged audio audit passes at1190.43seconds, and61successful visual-test cases plus34resumed unchanged cases cover95/95. These are latest individual results with retained history, not a claimed uninterrupted green whole invocation. Exact published-head CI remains a separate claim.

[Production unchanged](evidence/production_unchanged.json). No assertion/floor, gameplay, voice, save or CI workflow changed. The2Dregression inventory passes NO_REGRESSION while global strict migration remains UNSATISFIED. Structural [document/coverage checks](evidence/governance_receipt.json) print ALL OK. [Impact](../../../design/audit_impacts/roshan-job-rig-sport-stage-20261101.json) names exact baseline/changed paths, DL rules and MA-ROSHAN-005/006 context. Both findings remain OPEN/unchanged; no master-audit satisfaction.

## Visual and external acceptance

[Static key inspection](evidence/verification_v3/static_visual_review.json) **rejects** shoulder continuity, segmented elbow/wrist/cuff finish, coarse gripping-hand detail and abrupt material boundaries. The racer mount is diagnostic. Source pose/contact/outline transitions require exact normal-speed and frame-step human review; smooth metrics are insufficient. Physical Lenovo/older-phone30fps, owner, child and final-character/release acceptance remain pending.

`ARCHIVE_COMPLETE`, `GENERATION_READY` and `DELIVERY_ACCEPTED` are independent. No external video-generation job is commissioned; generator readiness and delivery acceptance remain false. A published review packet never accepts these performances or permits production adoption.

## Open the adult source demo

Use exactly Godot4.7.2-stable, Mobile rendering, `--path assets_src/animation/roshan_job_rig_sport_stage_20261101/demo`. The standalone project never opens the game/save.1/2/3select jobs,4/5/6original motions, Space pauses, arrows step30fps, H/J/Kcycle head/body/tail over six current families. Orestores original slots; its independent pixel-exact seed comparison currently fails as recorded above.

## Publication and next work

Destination is the owner-authorized `Ebonyks/mermaid-roshan-reef`, isolated branch `codex/roshan-job-rig-sport-stage-20261101`. Commit/push is review-only after existing gate/governance coverage; never dev/master adoption. `MANIFEST.json` lists source/provenance/roles/hashes and a deterministic payload hash. `evidence/remote_verification.json` must name the exact immutable revision, anonymously fetch every required file and match all bytes before any verified-publication claim. Local paths and an unpushed commit are staging only.

Compatibility remains blocked. A new bounded repair brief and accepted shared waist/outline authority must address exact original restoration, right-arm attachment and mixed/paint continuity. Owner/device/child/human acceptance is separate. [Current blocked compatibility record](evidence/HANDOFF_BLOCKED.json).

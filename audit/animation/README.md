# Character animation — master audit branch

Owner commission: 2026-09-09 initial direction request, expanded and integrated
2026-09-11. Status: `SUPPORTING_CURRENT` production coverage register under
the [master audit](../MASTER_AUDIT_2026-08-09.md#development-task-index).
This branch organizes animation work by character, beginning with Roshan.
It does not create findings, close existing ones, or declare game-wide satisfaction.

## Start an animation task here

1. Read the [canonical motion rules](../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md#9-motion-acting-feedback-and-rewards)
   and the character's individual movement profile.
2. Use the [production protocol](../../design/animation/ANIMATION_PRODUCTION_PROTOCOL.md)
   to bind intention, approved sources, timing, contact, event ownership and
   evidence. Use the [profile template](../../design/templates/CHARACTER_MOVEMENT_PROFILE_V1.md)
   for a character not yet covered; verify its canon and roster authority first.
3. Inspect existing art and callers before commissioning missing poses or
   changing playback. Register the exact scoped action and acceptance gaps.
4. Implement and review only the commissioned work. Update this coverage row
   and its evidence when their facts change, with an audit-impact record.

## Character coverage

| Character | Direction document | Working direction | Authored candidates for this profile | Runtime/machine evidence for this profile | Visual/device/child/owner acceptance |
|---|---|---|---|---|---|
| Mermaid Roshan | [Movement language v1](../../design/animation/ROSHAN_MOVEMENT_LANGUAGE.md) | Ribbon Glide everyday; Playful Dolphin for delight. Pilot selection remains open. | Not produced by this documentation task; existing atlas inventory is linked in the profile | Not implemented or tested as a new movement suite; existing scoped game evidence is not transferred | All remain open for the proposed suite |

This table is a **profile commission inventory**, not a claim that only one
character exists or that the game has no prior animation. Add each next
commissioned character as an individual row, with verified source/canon links.
Do not infer personalities from filenames or copy Roshan's rhythm to fill a
blank. Career costumes remain Roshan and inherit her profile; record their
specific actions and special pose constraints as extensions. Distinct actors
receive distinct identity/profile IDs even when they share a species or room.

## Roshan work queue

| Order | Bounded deliverable | Question it resolves | Required next evidence |
|---|---|---|---|
| 1 | Asset-to-action coverage review | Which existing chronological frames support the new phrasing? | Exact paths/cells, source hashes, directions, anchors, keep/gap rationale; no speculative regeneration |
| 2 | Matched ten-second A/B studies | Does the gentle glide or eager pulse best express her? | Same scene/scale/route/camera; exact candidates, normal-speed review, recorded selection and remaining owner review |
| 3 | One real work/contact study and carry turn | Is she still recognizable while actually helping? | Before/contact/after, prop ownership, support and interruption evidence |
| 4 | Bounded gameplay integration | Does the chosen performance preserve agency and saved truth? | Valid input, arrival/contact, cancellation, passive negative, pause/re-entry and required local/CI gates |
| 5 | In-context acceptance | Does it read on the child's device? | Exact build, Mobile/Speedy captures, target-device frame timing, child comprehension and owner review |

This is a proposed production sequence, not a new runtime commission. The
current task delivers documentation and routing. Missing dependent evidence
blocks the dependent claim, not independent drafting or source inspection.

## Evidence record for each character/action

Record character/profile version, action ID, source revision, artifact paths
and hashes, register, environment/support, directional coverage, contact and
effect markers, validation command/log, reviewer/date, decision and remaining
gaps. Keep rejected candidates and specific correction reasons. Profile or
source changes require reviewing affected descendants; unrelated acceptance
does not transfer or reset automatically.

Report these claims separately:

| Claim | Evidence that supports it | What it does not prove |
|---|---|---|
| Direction documented | Profile plus source/authority review | Approved visual performance |
| Candidate selected | Exact comparison clips and recorded selection | Final acceptance or implemented behavior |
| Authored art reviewed | Identity/anatomy/contact/temporal review of exact sources | Correct engine sampling or device behavior |
| Runtime machine verified | Exact code/assets, relevant probes and required gates | Child comprehension or owner preference |
| In-context visual reviewed | Exact build/settings and normal-speed/captured review | Actual target-device performance |
| Device/child/owner accepted | Each named reviewer/session/build and outcome | Whole-game master-audit satisfaction |

External cinematic `ARCHIVE_COMPLETE`, `GENERATION_READY`, and
`DELIVERY_ACCEPTED` are additional independent claims governed by the existing
cinematic contract. An animation profile or motion-reference movie supplies
none of them by itself. No new lifecycle taxonomy replaces the master findings.

## Existing findings and authority

- [MA-PLAY-004](../findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-004): Roshan
  travels and visibly works at each real target. This profile supports future
  repairs but does not close the remaining job cases.
- [MA-VIS-006](../findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-006): current
  runtime visual acceptance remains scoped to its actual evidence.
- [MA-PERF-001](../findings/ACTIVE_FINDINGS_2026-08-13.md#ma-perf-001): device
  measurements remain necessary; fluid-looking desktop playback is insufficient.

Rule coverage: `DL-MOT-01` through `DL-MOT-16`, with applicable touch, child,
contact, medium, cinematic, save and performance rules. Canonical finding
lifecycles/history remain unchanged because this commission defines direction
and production protocol rather than repairing or verifying runtime defects.

Change/evidence: [2026-09-11 audit impact](../../design/audit_impacts/2026-09-11-roshan-animation-language.json).

## Branch history

- 2026-10-07 (latest): owner named rig-pilot take g1 the best wave draft and directed its repair: "weak frames are regenerated as keyframes in ltx so they can be edited into the aesprite animation. This can be done through after completion self audit" (`ODR-RIG-PILOT-G1-REPAIR-20261007`); the outfit art is to be redrawn (`ODR-OUTFIT-ART-REDRAW-20261007`). The [Codex handoff](../../docs/handoffs/codex_roshan_wave_g1_repair_and_outfits_2026-10-07/README.md) gives the full g1 recipe, a per-frame defect inventory, a four-times-slower LTX keyframe retake locked to g1's clean frames, an eyes-only blink, the self-audit loop and per-view outfit art. [Impact](../../design/audit_impacts/codex-wave-g1-repair-outfits-handoff-20261007.json). No runtime or finding change.
- 2026-10-07 (later): the rig pilot's [run-2 takes](../../assets_src/cinematics/claude_rig_pilot_20261007/README.md#run-2-results) spent all 8 local takes under `ODR-RIG-PILOT-TRIALS-20261007`. Guides now move the whole outline (lean, head tilt, hair, tail) and, from run 6, keep the waving hand outside the hair, face and body. Size held on 7 of 8 takes (g1: figure 0.63%, head 0.74%). Hand smear tracks hand speed over busy detail inside LTX-2.5's 8-frame latent groups. Every blink request shut the eyes for 11 to 26 frames. Best candidate g1 still has a soft hand in 17 frames (5 to 12, 25 to 33) and no blink. Outfits: all four on 41/41 frames of every take, spread ≤ 3.5%, drift ≤ 0.88 px. [Impact](../../design/audit_impacts/claude-rig-pilot-20261007.json). No runtime or finding change.
- 2026-10-07 (earlier still): owner rejected rig-pilot revision 2 ("No, these are failures. there are overdraw errors, the figure doesn't move as a whole, there are some rough crop issues as well"), then asked to "Continue, trial methods until satisfied" and to make sure clothes keep working with animation (`ODR-RIG-PILOT-REV2-REJECTED-20261007`, `ODR-RIG-PILOT-TRIALS-20261007`, `ODR-RIG-PILOT-COSMETICS-20261007`). The cut-out rig is closed for acting; rig-guided LTX takes a1/a2 are queued on the RTX 3060 Ti through a bounded [PC runner](../../assets_src/cinematics/claude_rig_pilot_20261007/README.md#running-the-takes-on-the-rtx-3060-ti). [Outfits on clips](../../assets_src/cinematics/claude_rig_pilot_20261007/README.md#cosmetics-the-game-outfits-on-an-animation-clip): the production outfit builder bakes ribbon, party, garden and disguise onto every frame of a whole-frame clip from a constant-size, bodice-tracked fit (Union take 1: 41/41 frames, clothing area spread ≤ 2.3%, drift ≤ 0.35 px).
- 2026-10-07 (earlier): owner reviewed rig pilot run 1 as a rough take but frozen, with frame-by-frame artifacts, and asked for full-body movement with the wave, a blink and hair flowing in the water (`ODR-RIG-PILOT-REV2-20261007`). [Revision 2](../../assets_src/cinematics/claude_rig_pilot_20261007/README.md#run-1-revision-2-whole-body-blink-hair-owner-review-2026-10-07) smooths the LTX arm path (max acceleration 76 to 13 °/frame²), authors anticipation, lift, lean, head tilt, free-arm and tail counter-swing on one master phase with short lags, adds an underwater idle with a travelling hair wave, and blinks with pilot-only painted lids (no approved front-facing closed eyes exist). Size still PASS. [Impact](../../design/audit_impacts/claude-rig-pilot-20261007.json). No runtime or finding change.
- 2026-10-07 (later): owner asked for a deterministic-rig pilot with LTX animations as the motion guide, then for two test runs: one ignoring the rules, then the rules back where it falls short (`ODR-RIG-PILOT-GUIDES-20261007`, `ODR-RIG-PILOT-IMAGE-EXCEPTION-20261007`, `ODR-RIG-PILOT-RULES-OFF-TEST-20261007`). The [rig pilot](../../assets_src/cinematics/claude_rig_pilot_20261007/README.md) solves Union take 1 onto one fixed-length rig. Run 1 renders a Godot 4.7.2 Skeleton2D Roshan: one size (figure 0.05%, head 0.16%, W3 PASS) but part layers, an arm moving alone and a hand swap. Run 2 restores the rules: proportion-locked guides (W3 0.0%) on one master phase, with a controlled-comparison runner for the next take, not run here. The fit also measured take 1's own arm at +34% raised and −55% lowering, both asked for by the Union guide. [Impact](../../design/audit_impacts/claude-rig-pilot-20261007.json). No runtime or finding change.
- 2026-10-07: owner rejected the whole-frame bending wave ("roshan mutates in size still") and set a game-wide rule ("sprites need to be drawn whole, as a single unit, in this game"): `ODR-ROSHAN-CONSTANT-SIZE-20261007`, `ODR-SPRITE-WHOLE-UNIT-20261007`. Measured: the approved wave keys differ in head size (about 2.5%) and upper-arm length (15.3–26.7 px); Codex's Union take 1 holds size (0.11% figure, 0.34% head). The [Codex wave handoff](../../docs/handoffs/codex_roshan_wave_whole_sprites_2026-10-07/README.md) sets the size and arm-proportion contract and a numbers-only check. [Impact](../../design/audit_impacts/roshan-wave-whole-sprites-20261007.json). No runtime or finding lifecycle change.
- 2026-10-05 (later): owner rejected the cut-out-arm wave: "No arm moves as a single figure, the whole body moves at once, drawn as a whole frame" (`ODR-ROSHAN-WHOLE-FRAME-20261005`, written back to the [production protocol](../../design/animation/ANIMATION_PRODUCTION_PROTOCOL.md#preserve-crisp-contours-and-figure-wide-continuity)). The [whole-frame wave](../../assets_src/cinematics/claude_whole_frame_wave_20261005/README.md) draws every frame from one complete approved key bent as one figure, with the whole body on one timing curve and one drawing change per beat. Named gap: one whole-figure arm-out key. [Impact](../../design/audit_impacts/claude-whole-frame-wave-20261005.json). No runtime or finding change.
- 2026-10-05: owner asked for Codex's hand-raising wave replicated by another method ("LTX is an option, but not the only option"). The [2D whole-figure deformation wave](../../assets_src/cinematics/claude_2d_deform_wave_20261005/README.md) keeps Codex's 41-frame timeline and canvas and builds every frame from the four approved `roshan_gesture_a.png` keys: arm/body layers, MLS body deformation through all four drawn geometries, per-segment arm warp, hair/tail/forearm lag and drawing switches without blending; hands stay painted. [Impact](../../design/audit_impacts/claude-2d-deform-wave-20261005.json). Known seam/elbow defects and all human/device/child/owner gates remain open; no runtime or finding change.

- 2026-10-04: [continuous-scale filter v2](../../assets_src/cinematics/ltx25_scale_filter_v2_20261004/README.md) corrects v1 anatomy-based bypass and1/64 quantization without another generation. All41 exported frames meet root/global-scale limits; seven internal geometry failures, cropped hand, torn fingers/blur and seam remain review failures. Common-stage Grok controls feed the binding protocol. No runtime/finding acceptance.

- 2026-10-04 (later): [size/focus repair analysis](../../assets_src/cinematics/ltx25_focus_repair_20261004/README.md) records the owner's remaining visible errors and permission for a different corrective workflow. Native detail variation and mixed-detail guides motivate coherent whole-figure structural-video conditioning, then temporal detail repair. Actual same-latent decoder ablation rejects two-step decode for added grain; zero new transformer/ImageGen jobs. Preferred adapters remain locally untested, with separate access/8 GB checks; no runtime/finding/owner acceptance.

- 2026-10-04 (subsequent trial): [Union structural-control footage](../../assets_src/cinematics/ltx25_union_trial_20261004/README.md) runs two complete two-pass41-frame LTX-2.5 W4A8/Union takes on8GB, with actual GPU patch proof, full Aseprite guides/native masters and same-timeline comparison.173s/7152MiB and71s/7470MiB have different cache states. Native internal size is steadier in inspected poses, but hand/focus/strict guide-root fail; weaker opening lock adds texture. No runtime/finding/owner acceptance or temporal-detail execution.

- 2026-10-04: [LTX-2.5 8 GB wave/blur study](../../assets_src/cinematics/ltx25_8gb_wave_20261004/README.md) records five actual W4A8 takes, active NAG/48fps limits and Aseprite multi-anchor scale filtering. All eight source guides pass;32/41 post-filter frames pass, nine need redraw and torn fingers remain. Native outputs/editable masters retained; no production/runtime/finding acceptance.

- 2026-10-04 (later): owner answers — left/right orientation only; a rich, comprehensive set rather than limited animation; test animations, workflow and style first, then every room and game; a slower, more modest Sky Lagoon swim; production through LTX locally by a Codex script with Aseprite into the game, Grok packets as test documents. Revision 2 adds the [Roshan animation template](../../docs/handoffs/codex_roshan_motion_language_2026-10-04/TEMPLATE.md) (scene analysis, per-interaction decision, model routing, card, style rules) and the [shot-card audit](../../docs/handoffs/codex_roshan_motion_language_2026-10-04/SHOT_CARD_AUDIT.md). No clip, runtime or acceptance change.

- 2026-10-04: [two-pass portrait wave comparison](../../assets_src/cinematics/ltx_two_pass_wave_20261004/README.md) verifies the installed 2B 7-step pass, learned latent upscale/AdaIN and 3-step refinement, with whole-figure Aseprite guides and conditional quantized 2.3 comparison. Native anatomy/timing failures remain visible; no runtime acceptance or finding closure.

- 2026-10-04: owner asked how Roshan should move and what to refine in the Grok and Aseprite work. The [motion analysis](../../docs/handoffs/codex_roshan_motion_language_2026-10-04/ANALYSIS.md) keeps the v1 acting language, proposes ten motion locks and a fourteen-clip canonical set (section 10 is the work queue's asset-to-action coverage review), records `MA-ROSHAN-006` and hands RM0–RM8 to Codex ([handoff](../../docs/handoffs/codex_roshan_motion_language_2026-10-04/README.md), [impact](../../design/audit_impacts/roshan-motion-language-20261004.json)). No clip, runtime, art or acceptance change.

- 2026-10-04: owner prioritizes the [8 GB retake and whole-figure Aseprite repair trial](../../assets_src/cinematics/ltx_retake_repair_20261004/README.md). The [bounded protocol](../../design/animation/ANIMATION_PRODUCTION_PROTOCOL.md#iterative-repair-with-aseprite-and-temporal-retakes) preserves native frames, coherent body motion and separate hardware/quality acceptance; caps include failed attempts. No runtime finding is repaired.

- 2026-10-03: owner permits final animation workflows with identity/motion/provenance/device checks and prefers Aseprite as the bridge. [Research](../../design/animation/WORKFLOW_OPTIONS_2026-10-03.md), [job card](../../design/templates/ANIMATION_JOB_CARD_V1.md) and [impact](../../design/audit_impacts/animation-workflow-policy-20261003.json) record 8 GB local limitations, API costs, method selection and bounded retries. Prior rejected/reference studies retain their scope; no runtime/device/child/owner acceptance or finding closure is claimed.

- 2026-09-13: [video-first handoff revision](../../assets_src/cinematics/roshan_swim_motion_auditions_2026-09-12/README.md#video-first-revision--2026-09-13) requires actual image-to-video capability and attached source inputs, one returned/reviewed RSW-01 video before the larger batch, and no still-board substitute. Publication now has a committed hash-bound envelope, separate from opening approval and video acceptance. [Impact](../../design/audit_impacts/2026-09-13-roshan-grok-video-first.json). No art pixels changed, no videos generated, no finding closed.
- 2026-09-12: owner requests [eight Grok swimming-performance auditions](../../assets_src/cinematics/roshan_swim_motion_auditions_2026-09-12/README.md), allowing selection or compatible beat combinations. The local swim-scull-v6 prototype is rated 3.5/5 by the owner, superseding earlier agent 4.5 motion scores; static source-art approval does not accept that performance. Two new opening compositions remain pending exact human approval. [Scope and evidence](../../design/audit_impacts/2026-09-12-roshan-grok-auditions.json); no live findings closed or runtime changed.
- 2026-09-11: created the character animation branch, Roshan's expanded
  movement language, reusable character template and production protocol;
  integrated canonical motion rules and art/chapter/cinematic navigation.
  No motion study, runtime change, new art or acceptance is claimed.

- 2026-10-04: owner commissioned the [registered Roshan wave sample](../../assets_src/cinematics/ltx_registered_wave_20261004/README.md) using existing artwork, local LTX-Video 2B and Aseprite. [Impact](../../design/audit_impacts/ltx-registered-wave-20261004.json) tracks source-only evidence: native hand blur persists, owner rejects fixed-body limb-only finishing, and the whole-figure root/prompt trial preserves coordinated body scope but fails motion sharpness; a final81-frame native take reduces the lowering smear while retaining transition-hand defects. No runtime, owner/device/child acceptance or finding closure.

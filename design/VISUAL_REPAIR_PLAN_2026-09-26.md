# Visual repair and aesthetic production plan — 2026-09-26

Status: SUPPORTING_CURRENT implementation plan and progress record. This is not release or visual acceptance. Owner request: remove the backpack-crop Eagle completely from the game, repair the reported defects, redraw an undersized four-floor Opera in four panels, and use native Aseprite pixel work for new sprites.

Baseline: `6a38bc8caa1c153e8ebb05a15f7ab6696bb4d1f4` on dev. Work branch: `codex/visual-polish-repairs-20260926`. The pre-existing unrelated dirty checkout was preserved untouched on `rescue/peter-2026-09-26-visual-polish-start`, commit `ce4905a473ccd76c16e4f5b71900290aae53d65d`.

## 1. Validated scope and authority

The September 25 handoff's 78 payloads match their recorded bytes/hashes. Its 345 draws, 217 texture regions, 53 sheets, 301 occlusion records and 54 flagged-cell measurements were checked. Static sheet inspection does not establish current device appearance. The absence of a Parallax2D node does not prove absent parallax: Sky Lagoon already uses distinct canvas movement factors.

Rules: DL-AUTH-05/06/07; DL-MED-01/04; DL-VIS-06/07; DL-READ-02/05/06; DL-LAY-01/05/07; DL-MOT-02 and animation production rules; DL-ASSET-01/03/04; DL-SAVE-01/04; DL-PERF-01/04; DL-QA-01/03/07. Findings: MA-VIS-006/007, MA-PLAY-003, MA-OPERA-012, MA-SAVE-001, MA-PERF-001. Their broader lifecycle states remain open/pending; these local repairs do not close them.

## 2. Repair register

| Item | Method and current state | Remaining acceptance |
|---|---|---|
| T1 Rumi fragments | Native Aseprite pixel clearing in four reviewed edge regions; original hidden layer and source hash retained | Pool context and all eight poses reviewed at phone scale |
| T2 backpack Eagle | Deleted old PNG/import sidecar; every script consumer redirected to the approved isolate; adoption skips painting; stale colour callbacks rejected. Runtime export corrected to original 290x512 canvas | Castle bounds pass after export correction; all consumer contexts and phone review remain |
| T3 settee | Full right edge recovered from the source furnishing sheet; interior cushion alpha restored without RGB repaint | Review against actual Movie Lounge floor |
| T4 quilt | Reviewed interior alpha correction; one missing cloth pixel copied from adjacent intact cloth, recorded explicitly | Sleepover context review |
| T5 blocks | Complete three-block states recovered from the original chroma master through Aseprite, with one shared scale and fixed bottom pivot | Inspect all eight states in context; Castle interaction audit passes |
| T6 footlights | Reviewed foreign edge fragments cleared in Aseprite | Full tap timeline in Opera Hall |
| T7 books | Four foreign edge slivers cleared | Full Library tap timeline |
| T8 idea board | Two left slivers cleared; intentional detached paint jars retained | Craft Room timeline |
| T9 curtains | Reported frame-six sliver cleared | Curtain timeline; retain unrelated intentional marks |
| T10 trash | Complete wrapper recovered across old cell boundary and contain-fitted; foreign continuation removed from next cell | Pool gameplay, wrapper silhouette and pickup target |
| T11 furniture | Full feet recovered from original sheet, same runtime canvases, safe gutters | Dining/Royal Bedroom scale, floor contact and source-region review |
| T12 Roshan | Isolated approved frame windows in native Aseprite atlases; all retained visible RGBA pixels identical; legacy screen offsets preserved. Audit now reports zero clipping/zero ghosts; ghosts now fail the gate | Runtime pose/anchor checks, contact sheets and phone animation review |
| T13 Grand Puff | Complete ring recovered across old boundary with gutter; other puffs retained | Live jump/landing/contact timing and source ownership review |
| T14 bunny swoosh | Preserved; intent remains unconfirmed | Confirm intentional motion mark before altering artwork |
| T15 movie | Picture draws above the opaque screen, within its existing aperture | Screenshot of the actual movie state |
| T16 rescue pointer | Effects z-index; guard prevents creation after rescue | Pending/rescued visual states; focused probe passed |
| Additional capture finding | Removed the redundant decorative bunny-family overlay from the playroom; the two interactive pinning bunnies remain | Rescue composition and focused dressing probe |
| O1 captions | Main Hall/Day One cleanup captions use the upper band; other rooms retain their established band. Duplicate lower HUD caption suppressed; voice and pointer remain | Check top HUD/doors, all cleanup phases and narrow/wide layouts |

Exact operations and source/output hashes are under `assets_src/repairs/visual_polish_2026-09-26/`. The source references and native files are excluded from Android export. Historical archived handoff references and Git history are evidence, not game fallback assets.

## 3. Finish repairs before adding aesthetic features

1. Review T5 source-owned reconstruction in context. Each frame now keeps its complete three-block group; the fixed pivot, shared scale and eight-frame sequence are preserved.
2. Refresh relevant runtime and source manifests, contact sheets, license records and pixel verification. Ensure deterministic rebuilds preserve these corrections instead of silently restoring old defective exports.
3. Run focused runtime probes on exact Godot 4.7.2. The broader Castle probe caught an oversized replacement Eagle; preserve that regression check and fix the asset, not its assertion.
4. Capture every changed room, all repaired animation frames, rescue pending/completed, Eagle adoption, follower and minigame uses, and the real boss jump. Evaluate silhouette, alpha, gutters, layer order, floor contact and tap occlusion separately.
5. Run parser/inference, all applicable static audits, full trusted probes, passive/load/save checks and master-audit contract gates. Do not integrate a red or partially checked branch.

## 4. Replay implementation

Preserve the Library magic book's Chapter Two detective action when that action owns the current beat. Add picture-first replay access only when completion permits it. Persist additive `day_one_completed_once`, `day_one_replay_active` and `day_one_replay_clips_seen` state; retain earned rewards, companions, room art, story history and Chapter Two progress.

Reset the director's complete 26-key Day One route through its normalizer, plus rescue/bunny flags and pending boss state. Use a replay-specific clip-seen set. Completion and a visible Back to Today action must restore the completed present-day state. Do not use New Game, delete keys, or let Chapter Two normalization infer permanent completion solely from the temporarily reset boss-defeated flag. Preserve state ownership on main.

Add a trusted replay probe covering legacy saves, first completion, repeated replays, mid-replay save/load, clip-once-per-replay, safe exit, no repeated reward grant, Chapter Two preservation and zero-input no-win behavior. Add Day Two only after its safe reset/return loop is demonstrated; otherwise show no misleading playable card.

## 5. Four-floor Opera production and integration

The rescue branch's native venue is 1672x941 and does not meet the background coverage rule. It is a layout/reference input only. The newer owner direction commissions a four-floor venue; it does not silently reinstate the obsolete three-floor hub or owner-cut boss slots.

Produce four coordinated native 2048x1152 panels in a 2x2 arrangement, yielding a continuous 4096x2304, 16:9 master. Preserve all four floors, sixteen door positions (fifteen live and one mystery), lifts, routes and established foreground anchors. Keep a shared layout-coordinate map, fixed seam landmarks, palette reference, source hashes and generation settings for all four jobs. Reconcile each seam before acceptance; upscaling a smaller candidate does not meet native coverage.

Extract readable cross-boundary objects once, heal their background footprints and reinsert their approved artwork as single Canvas cards. Never independently invent both halves of a door, column or lift. Retain originals and rejected candidates as evidence. Slice the accepted combined master into non-overlapping runtime textures satisfying the 1024/POT rule, and prove exact reconstruction with a tile manifest.

Three built-in generation attempts returned 1672x941 despite requested native panel dimensions; none qualifies. API/CLI fallback permission was requested and remains pending; OPENAI_API_KEY is also not configured. This is an artwork-production block, not a reason to declare the low-resolution branch ready.

Selectively port the four-floor implementation from `d664da1877cb2bb963789352122251118bd49298`; do not merge its old audit, voice, export or main-state files wholesale. Reconcile room routing, additive saves, music/voice keys, arrival/return, lift affordances, touch-safe doors, mystery behavior, current Chapter Two routes and the current CI baseline. Update DL-INT-12 / MA-OPERA-012 expectations with the new owner topology when implementing that change, keeping runtime implementation and visual acceptance separate.

## 6. Aesthetic methods and workflow requirements

| Proposal | Appropriate workflow | Evidence before rollout |
|---|---|---|
| Performance tiers | Inventory current tier guards first; add explicit effect budgets per scene | Mobile/Speedy frame time and transparent overdraw on Lenovo Tab M11; 30 fps floor |
| Water/window movement | Source-owned water masks, static bank/fixture holdouts, local Canvas shader and restrained UV motion | No moving architecture, leaks, seams or touch obstruction; before/after in motion |
| Lamps and breathing light | Small authored emission masks and restrained canvas overlays; prove the actual Canvas path | Art colour/identity stays stable; no 3D lights or unverified Environment grading |
| Bubbles/sparkles | Reuse approved particles, sparse bounded emitters, per-tier limits and reduced-motion behavior | Composition stays readable; no persistent cue confusion or overdraw spike |
| Curtains/plants | Extract source-owned cutout and heal its painted duplicate first; choose authored Aseprite cels or small pivot motion according to contact requirements | No double image, floating anchor, stretched silhouette or movement of fixed architecture |
| Grounding | Reuse source-owned contact shadows; explicit feet/seat/water contact anchors | Contact does not drift during movement or changing poses |
| Depth/camera | Inventory existing parallax first; separate background/playable/foreground ownership | No duplicated existing Sky behavior, exposed holes, target drift or motion discomfort |
| Feedback/transitions | Small reusable effect contracts, cancellation and input-state rules; brief feedback tied to actual actions | One-finger success, no blocked save/exit, no accidental passive completion |
| Colour grade | Bounded, measurable Canvas colour treatment with protected-art exclusions where needed | Compare on actual Mobile renderer; approved identity colours remain recognizable |
| UI | Safe-area and occlusion layout, picture cues, voice, large targets | Phone-scale captures, no reading-dependent progress and no new target overlap |
| Flat-room repaint proposals | Separate reconstruction jobs with a fixed composition/prop/hotspot inventory; preserve approved furnishings | Native source coverage, healed cards, identity/style review, then context acceptance |
| New sprite/animation proposals | Native Aseprite pixel/cel workflow below | Identity, topology, anchors, timing, interruption and export tests |

A blanket shader or scene-wide particle pass cannot replace these workflows. Begin with one measured room/effect prototype; compare against the unchanged baseline and expand only after it meets the art, interaction and device gates. Room repaints and new movement cycles are proposals, not automatically accepted replacements for the approved art.

## 7. Aseprite pixel and animation protocol

The requested named protocol was not found in the available repository/skills; its location was requested. Until supplied, the explicit user requirement governs: use native `.aseprite` sources for sprite drawing and pixel corrections. `tools/aseprite/rebuild_visual_polish.ps1` replays the dependency-ordered native operations and verifies recorded hashes; it never auto-accepts new exports. Run this repair pipeline after a legacy source builder, which otherwise reconstructs its older extraction. Current work uses scripted Aseprite `Image:drawPixel` operations with reviewed ownership regions; it must not be described as hand-drawn new animation.

For a new Rumi or other character cycle: lock the approved identity/pose references; specify action, frame count, timings, silhouette, costume and topology; define anatomical pivot, contact anchor, shadow and interrupt rules; retain original reference layers; author each new cel pixel by pixel in Aseprite; review onion-skin motion and every cel individually; export deterministic atlas rectangles with gutters and pivot data; check alpha, frame ownership, timing and source hashes. Do not generate a replacement character design, tween a still to simulate new acting, or repack an accepted sheet merely for convenience.

Review a low-frame-count keyed action first. Inbetweens come only after poses, contact and identity are sound. Existing Rumi repair clears foreign fragments and does not commission a redesigned Rumi.

## 8. Delivery gates and current limits

Implementation, machine verification, visual review, device/child acceptance and release are separate claims. Focused Eagle, interaction, full Castle bounds and Sky probes pass after the size correction. Pixel preservation and Castle interaction/dream-house audits pass for the measured candidates. Final desktop Mobile still captures are recorded in `audit/visual_polish_2026-09-26/REVIEW.json`; 76 assertion probes pass; one display-only headless capture reports SKIP in recorded local CI stages, while exact remote CI, all-frame animation and target-device acceptance remain pending. No task-complete, integrated-dev, stable APK or master-audit satisfaction claim is made.

Commit/push only after required gates and complete impact coverage. Reconcile fresh dev, require exact-head green CI, then integrate under the established workflow. This request does not authorize stable promotion.

Local verification update (2026-09-27): parser/inference pass for all 11 changed scripts; authority and development coverage pass; native Aseprite reconstruction reproduces exact hashes; 76 assertion probes pass; the display-only headless capture reports SKIP. Earlier normalization, hidden-RGB and V4 binding failures were corrected and are preserved with their subsequent evidence in the review receipt. The V4 refresh preserves existing review because every candidate field except the whole-file Castle script hash is identical, including all 96 per-frame hashes. No new owner approval is asserted.

## Follow-up: Rumi tails and room alpha (2026-09-30)

The September 30 review found that clearing foreign fragments did not recover Rumi's cut contours or missing split fins in upright poses 0, 2 and 3. Native Aseprite recovery uses complete source-owned contours and the authored split tail from pose 1, preserves the pool swimming row, and clears additional craft-board fragments in frames 2 and 6, and restores solid backing inside all eight board states using adjacent intact board colors. Exact source/export hashes: `assets_src/repairs/rumi_transparency_2026-09-30/REPAIR.json`; scope and gates: `design/audit_impacts/rumi-transparency-20260930.json`. Native reconstruction, alpha/ownership, Castle interaction, authority and development checks pass. Full local Godot 4.7.2 CI exits 0 with 77 probe processes exiting 0 (one display-only headless SKIP); see `audit/rumi_transparency_2026-09-30/REVIEW.json`. Exact remote CI and integration remain pending; no device or owner acceptance is asserted. The separate unseen-story-clip visual fixture and extended reveal staging remain unaccepted.

Kitchen pan dark rims are authored outlines; foreground card fragments meet the stage edge intentionally. Craft ribbon gaps, hollow table spaces, brush poses and board-to-paint-jar separation are intentional transparency, consistent with the original audit's Reviewed and not errors section. These classifications do not waive runtime alpha review.

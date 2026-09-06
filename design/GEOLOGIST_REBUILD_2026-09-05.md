# Geologist: mechanics rebuild and reference review

> Historical individual-candidate report on base `775ceee1`. For the combined candidate reconciled onto `8aab459c` and current validation status, see [Opera reconciliation](OPERA_TWO_ACT_PERFORMANCES_2026-09-05.md#reconciliation-onto-current-dev--2026-09-05). Earlier green probes and typography blockers below retain their original scope.
Date: 2026-09-05
Scope: Opera act 16, The Crystal Cave Discovery. Supporting implementation and review evidence; not release, final-art, device, or child acceptance.
Base: `775ceee1b9f20118abec25ce933db292bb3c847e` (`origin/dev` at task start).
Working branch: `codex/geologist-rebuild-20260905`.

## Decision
Replace the former layer/swipe, fossil/swipe, specimen-choice and crystal-tap sequence with a small geology expedition. The old version changed its subject more than its interaction. The replacement makes the child's hand alter the material: dig a water channel, uncover and assemble a fossil, wash gravel, then open a geode.

The four activities are implemented inside the existing Opera route, character, voice, celebration and save framework. They remain cooperative, one-finger and without a fail state. The existing Geologist costume is preserved. This branch does not contain the separate, uncommitted Racer worktree.

## Reference analysis
These are primary-source mechanic references, reviewed on 2026-09-05. This was a source and implementation review, not a hands-on competitor playtest. Store descriptions and developer videos do not establish measured tutorial durations, input latency or preschool usability. No competitor artwork, code, audio or branding was imported.

| Reference | Specific mechanic worth adapting | Introduction and polish lesson | What Roshan should omit |
|---|---|---|---|
| [Tinybop — The Earth](https://tinybop.com/apps/the-earth), [official handbook](https://tinybop.com/assets/handbooks/the-earth/Tinybop-EL05-Earth-Handbk-EN.pdf) | Manipulating landscapes reveals erosion, deposition and other physical changes. Geological systems respond directly to gestures. | Let the landscape explain the result immediately; reveal one cause and effect at a time. The handbook supports exploration rather than a scored task ladder. | Reading requirements, broad encyclopedic scope and a claim that a simplified grid is a scientific simulation. |
| [Yateland — Jurassic Dig](https://yateland.com/apps/jurassic-dig/) | Digging exposes fossils; assembly gives the finds a recognizable whole and a subsequent payoff. The developer targets ages 2–5. | Excavation needs a recognizable object beneath it and a meaningful assembly result. Keep the next action physically attached to the discovered object. | Vehicle/tool menus, extra journey stages and a long preamble before touching the fossil. |
| [Dinosaur Fossil Hunter — developer Steam page](https://store.steampowered.com/app/864700/) | Excavation, cleaning, assembly and museum display turn a find into an object with a history. | Separate coarse discovery from careful finishing. Material changes should be legible, and the final object deserves display time. | Adult tool complexity, damage risk, logistics and management. It is not a mobile preschool benchmark. |
| [Fossil Corner — developer Steam page](https://store.steampowered.com/app/1587710/Fossil_Corner/) | Fossil traits support family-tree puzzles and a personal collection. | A collection can be a visual memory of discoveries, rather than only a score. | Text-heavy lineage deduction. Trait matching is a possible later extension, not part of this first rebuild. |
| [Fossil Quest — developer mechanics devlog](https://unsigneddoublecollective.itch.io/fossil-quest/devlog/1517558/dev-log-may-new-mechanics-new-mini-games-and-wholesome-direct) | Excavation, screen washing and nodule cracking provide distinct physical verbs. | Vary how materials are handled, rather than recoloring one repeated gesture. This is development evidence, not proof of finished product polish. | Its full tool chain or claims of validated commercial usability. |
| [Gold Panning! — developer App Store listing](https://apps.apple.com/us/app/gold-panning/id1602573653?platform=ipad) | Washing sediment reveals retained mineral finds. | A pan should move with the hand; sediment should visibly diminish while the finds stay. | Furnace, upgrades, capacity, currency and value speculation. Its store age rating is not evidence of suitability for Roshan. |
| [AMNH — Layers of Time](https://www.amnh.org/explore/ology/paleontology/layers-of-time2) | Layer order gives fossils geological context. | Later learning should connect a fossil to where it was found. | Required explanatory videos or reading before play. |

The strongest combination is Tinybop's direct causality, Yateland's excavation-to-assembly payoff, and the washing/cracking variety demonstrated by specialist fossil games. Roshan does not need the adult simulation wrapper.

## Implemented mechanics
### 1. Open a stream channel
A 9×5 sediment bed has a spring and an empty basin. Dragging excavates cells within a 46-pixel brush radius. Any connected route between source and basin is accepted; the demonstration is only a suggestion. A detached hole stays dry until joined to the source. The child can explore a different route without resetting.

**Pros:** genuine spatial causality, multiple solutions, immediate feedback, no speed requirement. It now tests connectivity rather than tracing a prescribed stroke count.
**Cons:** the coarse grid remains visible in the rounded channel geometry; water fills connected areas immediately rather than visibly traveling over time. There are no different erosion resistances.
**Next:** tune cell/brush size on the phone; consider a short, interruptible flow-front animation only if it clarifies connectivity. Do not add a timer or failed-channel state.

### 2. Brush and assemble a fossil
Brush locally across a sediment-covered ammonite slab. Each cleared patch stays cleared; 26 of 40 patches reveals the assembly activity. Three large pieces are made from different regions of the same approved fossil image. They snap to corresponding positions within a forgiving 92-pixel radius. A misplaced piece returns to its tray without penalty.

**Pros:** excavation reveals an actual recognizable form; assembly uses one coherent source image; persistent progress makes stopping safe.
**Cons:** the sediment mask is still a coarse patch grid; pieces have vertical cut boundaries rather than naturally broken contours; the transition into assembly is abrupt.
**Next:** use approved transparent fossil/slab art with matching broken contours, add a short spread-to-tray transition, and watch whether the change of verb needs a recorded cue.

### 3. Wash mineral gravel
Drag the pan back and forth. A direction reversal earns washing progress only after at least 46 pixels of travel; nine qualifying reversals reveal three retained finds. Holding still, tiny jitter and another finger do not earn progress. The pan moves with the hand; sediment diminishes.

**Pros:** a distinct tactile action; a material transformation rather than a timer fill; forgiving pace.
**Cons:** this approximates washing, not mineral density; the retained minerals use simple faceted shapes in the existing icon palette. Visual motion and sediment loss need child observation to establish clarity.
**Next:** tune required reversals against fatigue and accidental input, then add differentiated approved mineral shapes. Keep finds out of an economy.

### 4. Crack and open a geode
Tap five large points on the seam, then drag the right half at least 120 pixels to reveal the crystals. Taps must land on unresolved seam points and remain within a small tap-travel tolerance. Pulling early cannot skip the seam work. Partial opening is retained.

**Pros:** anticipation and reveal; two understandable actions on one object; a clear final artifact.
**Cons:** seam targets and crystal interior currently use the existing simple vector language; the reveal has less richness than Roshan's character art.
**Next:** approved closed/open views of the same geode silhouette, restrained contact sound, and a persistent collection display. No smashing, injury imagery or tool-selection screen is needed.

## Introduction, timing and tutorial policy
There is no reading-dependent tutorial page or mandatory video. Existing physical stations open each activity. The hand demonstration runs on a 2.4-second loop and yields to touch. Nine seconds without progress repeats the cue/demo; the existing 20-second station assist can bring Roshan to the station but cannot perform the geology work.

Each completed artifact holds for 2.2 seconds before advancing. The cooperative competition reference duration is now 120 seconds instead of 40. This is pacing metadata, not a deadline or a promise about measured child session time.

**Proposed first child-test targets, not competitor measurements:** approximately 15–30 seconds for the channel, 30–50 for brushing/assembly, 12–25 for washing, and 15–30 for the geode. Aim for roughly 90–150 seconds including discovery and celebration. Revise thresholds after observation rather than making the child match these targets.

The actual recorded brushing line is reused. Other new actions currently use the existing neutral grotto recording with visual demonstrations. Exact spoken instructions for digging, fitting pieces, washing and opening remain a production gap. No voice recording was fabricated or changed. A non-reader release should verify that the visual demo is sufficient and fill these precise voice gaps.

## Art and scene audit
The approved Roshan Geologist atlas and the established navy/purple, aqua, lavender and cream vocabulary are retained. The character is much more polished than the original Geologist vector scenery. This remains the largest presentation weakness.

The first runtime review showed unrelated background trays and a crystal marker showing through the new activity. The rebuild gives the working material an opaque sandstone work surface and keeps Roshan and the guide to its left. The pan, brush and split-rock geometry have been refined within the existing Canvas art language. This is gameplay presentation, not an authored cinematic or a replacement cinematic technique.

Three built-in ImageGen candidates are preserved under `assets_src/geologist_rebuild_2026-09-05/` with exact prompts, source reference, hashes, dimensions and rejection reasons in `generation_manifest.json`:
- The grotto composition has grounded stations, a clear central work plane, consistent light, and a palette that relates well to the existing Opera art. It is **reference-only**: the native output is 1672×941, below the 2048×2048 coverage requirement. Upscaling or padding would not fix native coverage.
- The six-object prop atlas has a recognizable ammonite, related closed/open geode designs, a pan and crystals. It is **rejected for runtime**: the 1254×1254 RGB image has a baked checkerboard.
- The explicit alpha-removal retry also returned a 1254×1254 RGB checkerboard. It is rejected as well.

No rejected candidate is referenced by production scripts, no protected source was modified, and no rejected image was silently relabeled as a finished asset. Remaining art work is specific: deliver a compliant native grotto master plus true-alpha props, preserve closed/open geode topology, and keep each object in exactly one scene layer. The final composition should pass contact, scale, contour, palette, silhouette and phone-size readability review.

## Subjective quality assessment
Scores are design judgments about the implemented local candidate, not measured store ratings.

| Version/dimension | Score | Reason |
|---|---:|---|
| Former Geologist — overall | 1.5/5 | Topic changes did not provide enough distinct handling or payoff; weak vector set compared with Roshan. |
| Rebuild — mechanics | 3.5/5 | Four distinct material interactions, free channel solutions, assembly and a reveal, with interruption recovery. Needs child testing and finer transitions. |
| Rebuild — onboarding | 2.5/5 | Immediate touch and demonstrations are useful; exact recordings are incomplete and some verb transitions need testing. |
| Rebuild — art integration | 2/5 | Better workspace clarity and approved character reuse; scene and object fidelity still lag the rest of the game. New raster candidates are not acceptable runtime assets. |
| Rebuild — overall local candidate | 3/5 | A substantially stronger playable foundation. It is not yet a polished, beta-tested release. |

## Save and integration contract
`opera_geology_checkpoint` is an additive save key. Missing or invalid outer schemas become an empty checkpoint; existing save keys remain intact. The checkpoint stores the phase and earned mechanical state. Brushed cells, excavated cells, fitted pieces, qualifying wash reversals, seam points and partial opening survive interruption. Drag ownership and transient hand position are not restored.

The in-memory checkpoint updates as material changes, disk writes are coalesced to at most approximately once per second during play, and lifecycle/phase completion flushes happen immediately. Failed writes remain pending for retry. Completion saves the next phase. A fully earned current-phase snapshot recovered from disk waits for the activity to open and then awards exactly once. The checkpoint is cleared only after the Opera win is recorded.

The shared main save dictionary owns persistent state; no new global game-state owner was introduced. Four phases preserve Opera's 14 careers/57 phase contract. No 3D world, physics, lighting or model asset was added.

## Verification and remaining gates
Validation details and final logs are recorded in the accompanying local evidence bundle. The final full Opera run used the same explicit touch flags as local CI; an earlier invocation without those flags exited -1 without a verdict and is not acceptance evidence. The exact baseline used is Godot 4.7.2-stable.

The updated full Opera 2D probe has passed all careers and phases, including real ScreenTouch/ScreenDrag completion, passive safety, alternate channel solutions, disconnected dry excavation, wrong-finger/cancel handling, JSON restoration, malformed nested checkpoints and duplicate suppression. Mobile renderer captures cover all four activities at 1280×720 and 1600×720. These are desktop diagnostics, not device or child acceptance. The save-recovery probe passed including actual disk round trips; Chapter 2 passed with zero failed checks; document authority passed at 521/521; parser and inference checks passed. The game-wide 2D gate reports NO_REGRESSION, with its existing 56 production 3D files still UNSATISFIED.

The full local CI command stops at two inherited typography-contract failures: the stale U+2019 allowlist entry, and the stale literal/line fixture for `scripts/games/dust_boss.gd:1118`. The rebuild does not alter those files or waive those checks. Consequently this candidate is local and has not been committed, pushed or merged into dev.

Before release: resolve the repository gate failures; obtain green CI for the work branch; complete native/alpha art and exact voice gaps; verify save interruption and comfortable touch targets on the Tab M11; observe Roshan playing all four activities without reading or coaching. Only then integrate under the normal dev workflow.

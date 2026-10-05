# Codex handoff: Mermaid Pool five-star graphics, animation and evidence (2026-10-04)

Status: `PROPOSED / CANDIDATE`. Written by Claude. The owner asked for the Pool to be refined to five-star standard as the first area of the master audit, with code changed where necessary and new Codex handoffs for graphics and animation. Claude made the code repairs and wrote this; Codex builds every image, board, capture, animation and voice take (CLAUDE.md, owner decision 2026-09-30). Nothing here grants acceptance, `GENERATION_READY` or `DELIVERY_ACCEPTED`.

| Start here | What it is |
|---|---|
| [FRAMEWORK.md](FRAMEWORK.md) | The Pool's five-star definition, beat-by-beat sequence, what this round changed and measured, the gap register and the ordered path to 4/5 and 5/5 |
| [Gold-star scorecard](../../../design/reference/GOLD_STAR.md) | Live rating; `python -B tools/gold_star.py --compare day_one_pool` prints the ordered list |
| [Earlier packet](../codex_gold_star_2026-10-03/README.md) | GS0-GS5. This packet carries GS2-A forward as P2, replaces GS2-B with reuse (done in code) and completes GS5's Pool items |
| [Animation protocol](../../../design/animation/ANIMATION_PRODUCTION_PROTOCOL.md) and [job card](../../../design/templates/ANIMATION_JOB_CARD_V1.md) | Binding for P2, P4 and P5 |

## Rules for every package

- **Claude writes; Codex builds.** Every picture below is described in words and bound to existing files by path and SHA-256. Codex makes the boards, captures and art.
- **Reuse first** (`DL-ASSET-01`, AGENTS.md art budget). Each package names the existing art to try first. Generate only a named gap, recorded in the job card.
- **Animation workflow** (`DL-MOT-12`, `DL-MOT-14` to `DL-MOT-16`). One [job card](../../../design/templates/ANIMATION_JOB_CARD_V1.md) per action, with caps set before work starts: two generated takes per brief by default, then stop and diagnose. Local Aseprite masters with lossless strip-plus-JSON export. No paid job without an existing funded budget.
- **Identity.** Roshan's authority is `assets/characters/roshan_25d/roshan_base.png` and the approved atlas family. Never bind `roshan_sprite.png`. She wears the tiara outside a career costume (`ODR-ROSHAN-Q14`). Her tail is iridescent, so lavender and rainbow are both correct (`ODR-ROSHAN-IRIDESCENT`). Continue the light state of the cell you extend (`ODR-ROSHAN-Q12`). Rumi is the owner-confirmed Violet package under `assets/characters/rumi/`.
- **Protected and runtime rules.** Never modify `assets/book/`, `assets/audio/voices/` (the family recordings) or `assets/characters/friends/`. New textures are at most 1024 px on the longest side or power-of-two. Each new asset gets its `ASSET_LICENSES.md` row in the same commit. True Canvas 2D only. Derivatives go to new paths and keep source hashes.
- **Overdraw.** After any change to a file listed in the Pool's measurement inputs, run `python -B tools/measure_overdraw.py --groups pool`. The Pool must stay inside the budget: mean at most 2.5 layers, at most 10% of the screen with four or more, max 8, peak 32. It must also have no duplicate, no code drawing and no translucent wash.
- **Three claims stay separate.** `ARCHIVE_COMPLETE`, `GENERATION_READY` and `DELIVERY_ACCEPTED` are reported separately, as are machine checks, device, child and owner results.

## The packages, in order

| Package | What it delivers | Why it matters | Blocks |
|---|---|---|---|
| **P1** | Phone-size review captures of every Pool state, for the OD2 look-alike review and the owner's look | The only machine-adjacent gate between the Pool and 4/5 | 4/5 |
| **P2** | Roshan's scoop, scrub and tug as authored actions (scoop pilot first) | Turns a leaning cutout into acting; the strongest visible upgrade | Beyond the bar |
| **P3** | Room-lit prop family: trash, skimmer, basket, mouth trash and scrubber without product-render glow | Removes the last style mismatch and the runtime tints that hide it | Beyond the bar |
| **P4** | Rumi's rise out of the water (only if the owner keeps the in-room rise, QP-1) | The reward beat is the moment the child waits for | Owner QP-1 |
| **P5** | Swimming dust bunny paddle loop, plus a review of the ripple's tint and opacity | Replaces one wobbling sticker with acting; checks Claude's numbers by eye | Beyond the bar |
| **P6** | Water-true catch feedback review (splash, not soap) | Sight matches the event (`DL-MOT-04`) | Beyond the bar |
| **P7** | Voice: per-object skimmer lines, a hint that names pulling, Rumi's line status | Every line is true and teaches the best verb | Beyond the bar |
| **P8** | Device evidence session support | The 5/5 device lane | 5/5 |

### P1. Review captures for OD2 and the owner (do first)

**Goal.** `tools/gold_star.py` holds the Pool's C7 at 1 until the OD2 look-alike review is recorded. OD2 is defined as "painted objects that resemble the active object are not near Roshan or the object being worked; review at phone size with the HUD showing". Claude cannot make the capture. Codex makes it, then Claude or the owner reviews it.

**Build.**
1. Use the candidate at this packet's revision. Use exact Godot 4.7.2-stable, the Mobile renderer and a fresh Day One save. Route through the real castle, as `scripts/probe_overdraw.gd::_measure_pool` does.
2. Capture these states at two shapes: Lenovo Tab M11 (1920x1200, 16:10) and a tall phone (2400x1080, 20:9). Keep the HUD and the global Back button visible.
   - Dirty arrival after the story clip (`start`).
   - Roshan scooping the first piece (`skimmer_contact`).
   - The waterfall with the stroke guide showing.
   - A half-wiped lane (`waterfall_stroke`).
   - The seahorse with the tap guide showing.
   - A mid tug (`seahorse_tug`).
   - The extraction landing in the basket.
   - Rumi mid-rise (`finale`).
   - Rumi waving before the clip.
3. Make one contact sheet per shape, each frame scaled to the device's physical size at arm's length. One way is to reduce to the device's CSS width (about 800 px wide) for the squint test (`DL-READ-02`).
4. Store under `audit/pool_five_star_20261004/` with a JSON sidecar. For each capture, record the state, build hash, window size, renderer and SHA-256. `/audit/*` is git-ignored by default, so add the folder with `git add -f`, as the Chef overdraw evidence was, and push it. A local-only capture is not a delivered review.

**Review questions (Claude or the owner records the answers).**
- Is there any painted or live object that resembles the active one near Roshan or the target? Examples: a pink round shape near the trash, a net-like pattern near the skimmer, a basket-like shape near the basket.
- Does the one job read first in every frame, with the hand pointing at it?
- Is Roshan whole, in her colours, and never covered by the basket, guide hand or foreground rim during work?

**Record.** In `design/reference/games.json` under `day_one_pool.overdraw_review.OD2`, record `{result, evidence}` with the sheet paths and hashes. Then run `--render`. A "fail" names the object and frame.

**Done when** OD2 is recorded and `--compare day_one_pool` lists only the device, child and owner lanes.

### P2. Roshan's three work actions, scoop pilot first (carries GS2-A)

GS2-A's rules all carry forward: identity, clip contract, master/export, wiring and acceptance. This package adds the inventory, timing and contract detail needed to start.

**Today.** Roshan works as one approved directional cell, `assets/characters/roshan_25d/roshan_directional.png`. The cell is region (256, 0, 256, 256), shown at scale 0.95 facing right, with SHA-256 `2bcc6212dddaddedb5823ba095caff1cbecdb762d5bbdc76726d3d5b0e3ee85a`. The hand socket is cell pixel (174, 151). During the scoop the code leans the whole cutout plus or minus 0.055 rad around the socket; during scrub and tug the same cell holds still while soap bubbles mark the work. Both are static-sticker acting, which `DL-MOT-14` rejects as a substitute. The skimmer is held at its handle pixel (100, 580) in `pool_skimmer.png`, and the waterfall scrubber at its measured pink-handle centre, (39, 38) at the 72 px tool size.

**Reuse inventory to test first** (record pass or fail per verb in the job card):

| Source | SHA-256 | Try it for |
|---|---|---|
| `assets/characters/roshan_25d/roshan_gesture_a.png` to `_d.png` | `e70139b2…`, `59daf2a2…`, `43ebe0e4…`, `03cbc593…` | Reach, collect and carry keys whose hand can hold a separate tool |
| `assets/characters/roshan_25d/roshan_swim_front.png`, `roshan_swim_back.png` | `a62c8aee…`, `4e76c3c2…` | Travel to the target instead of a translated still. Needs a measured hand socket per frame; the [anchor tables](../../../scripts/roshan_sprite_anchors.gd) have none for hands |
| `assets/characters/roshan_25d/roshan_base.png` | `69827625…` | Identity authority only, never a pose key |

**Job cards.** One card each: `pool_scoop`, then `pool_scrub` and `pool_tug` only after the owner reviews the scoop.

| Action | Keys (at least four drawn, presentation only) | Contact span | Intention (protocol sentence) |
|---|---|---|---|
| Scoop | Reach forward with the net, dip under the piece, lift with drops, settle | 0.42 s work gate; the lift key lands as the piece leaves | "Roshan glides to the floating cup, dips the skimmer under it and lifts it out, then looks at the clear water." |
| Scrub | Reach up, press the scrubber on the lane, pull down, settle | Plays while her hand is on the lane; the stroke progress stays with the child's finger | "Roshan presses the scrubber to the clogged lane and pulls the grime down where the child strokes." |
| Tug | Grip the trash at the mouth, lean back, pull, settle | One tug per 0.42 s contact; queued taps replay from the first key | "Roshan grips the trash in the seahorse's mouth and leans back to pull it free, gently." |

- **Register.** "Concentrating" from the [movement language](../../../design/animation/ROSHAN_MOVEMENT_LANGUAGE.md): eyes on the tool's contact point, compact reach, quiet tail, no decorative bounce.
- **Geometry.** Same scale and baseline as the directional cell, facing right in every frame (the code never mirrors). A per-frame hand socket goes in the JSON. The tool stays a separate approved prop moved by the socket.
- **Export.** 1024x256 RGBA strip of four 256x256 cells, or a power-of-two atlas if there are more keys. Path: `assets/castle/day_one_pool/activities/roshan_work/pool_<action>.png` plus `.json`, holding frame rects, durations and per-frame `hand_socket`. Keep the editable Aseprite master with provenance under `assets_src/`.
- **Wiring contract** (Codex implements; Claude reviews).
  - `DayOneContactAction2D.avatar` and the skimmer's `RoshanHoldingSkimmer` cutout gain an optional strip.
  - The region follows the JSON by `work_time`, or `_scoop_time` for the skimmer.
  - The tool follows the frame's socket. A retarget restarts at key 0. Cancel or completion restores the room cutout.
  - Progress stays with the contact gate; it never comes from the clip ending (`DL-MOT-12`).
  - Default skin only. The fairy and huluu costumes keep their current single cutout.
- **Probe.** Extend `probe_day_one_pool_cleanup` so that:
  - grip error stays below 1 px on every frame, as the existing grip checks do;
  - the frame advances only while in contact;
  - cancel mid-action restores the room cutout;
  - progress counts are unchanged.
- **Pilot review.** Codex builds a review board for the scoop at full speed and frame by frame, on the room at both P1 shapes. The owner reviews it before scrub and tug are made.
- **Not allowed.** No new outfit, no extra limbs or second tail, no painted-in tools, no text, and no wobble in place of acting.

### P3. Room-lit prop family

**Gap.** The cleanup props were generated in a product-render style: saturated slime green, dense specular droplets and coloured glow auras. The 2026-08-23 [integration spec](../../../audit/DAY_ONE_POOL_NATURAL_INTEGRATION_SPEC_2026-08-23.md) bound the runtime to tame them with modulate tints and small scale. Two measures on the source files:
- the skimmer has 34% of its visible pixels semi-transparent, from its net plus a cyan and violet glow aura;
- the room uses diffuse upper-left light, broad satin value bands and navy or plum contours.

Each prop needs a room-lit variant so the runtime tints can go.

| Source (keep untouched) | SHA-256 | Runtime use today |
|---|---|---|
| `assets/castle/day_one_pool/activities/floating_trash_atlas.png` (1023x682, 3x2 cells) | `3e04bee28ffa4230e3af9d5e7d87bb9560a7462d7320b6ad8557f10fcecbcb33` | Six pieces at 62-88 px with per-piece `TRASH_TINTS` |
| `assets/castle/day_one_pool/activities/pool_skimmer.png` (1024x682) | `308c86843ace9fb3d4a65a0c514d41b367d87ceabaf5f3d3676f54ce9be4b9b3` | At most 205x150 px, held at handle pixel (100, 580), net centre (780, 190) |
| `assets/castle/day_one_pool/activities/cleanup_basket.png` (1024x936) | `30b43ce7b1f2db7098281a399f64db13c26c30fb9fce60f478b5f0cecdfd2910` | One basket, 145x112 px at (980, 560), tint (0.84, 0.88, 0.82, 0.96) |
| `assets/castle/day_one_pool/activities/seahorse_mouth_trash.png` (1024x576) | `9c48ac1ca7be923fcb14902b3e2b62263f34d53e031f11002776bfc4322652f9` | Mouth plug; weed tip at normalised (0.488, 0.184) enters the nozzle |
| `assets/castle/day_one_pool/activities/waterfall_scrubber.png` (962x1024) | `1b29ff463263be093a7e1ac33eb74e4075d6a795dd515d120107f66953b2dc7a` | Held scrubber, 72 px |

**Look to reach.**
- Two or three broad value bands per object, lit from the upper left like the room tiles (`assets/flats/castle/interactions_v4/background_tiles/room_mermaid_pool_background_r0_c1.png`, `8285d08d…`).
- Deep plum or indigo contours at the room's screen weight.
- Saturation and highlight density 15-25% below the source.
- No glow aura, no white sticker rim, no chrome or jewel lighting.
- The slime stays a soft olive-grey, not neon green.
- Every silhouette and every registration anchor stays exactly where it is: handle, net centre, weed tip and grip.

**Method.** Derive first: in an editable Aseprite master (or an equivalent lossless editor), remove the aura from alpha, regrade and recolour the contours. Use ImageGen only for a named object the derivation cannot reach, with the source as the identity reference. The usual two-take cap applies.

**Deliver** at new paths, `assets/castle/day_one_pool/activities/room_lit/<name>.png`, with the same dimensions or a declared power-of-two re-pack. Add a provenance note and `ASSET_LICENSES.md` rows.

**Code change** (Codex implements; Claude reviews):
- point the four activity scripts at the variants;
- remove `TRASH_TINTS` and the basket, skimmer, scrubber, seahorse and mouth-trash `modulate` tints;
- keep the registration constants unchanged, or re-measure them and update the probes that assert them.

**Acceptance.**
- Semi-transparent pixels (alpha 0.1-0.98) are under 5% of visible pixels per object, except the skimmer's net mesh.
- All existing probe registration checks pass unchanged.
- The Pool's overdraw remains in budget.
- P1 captures show the props sitting in the room.

### P4. Rumi's rise out of the water (wait for owner question QP-1)

**Context.** After the seahorse is freed, the room shows its own reveal:
- the authored waterfall sequence and the fountain return;
- Rumi rises from the water at (640, 610) to (650, 350) over 1.15 s, through the approved ripple ring;
- she waves, using two frames of `rumi_eight_pose_runtime.png`;
- Roshan says "We saved the pool and the seahorse! Hi, Rumi!".

Only then does the 17-second room-completion clip `d1_pool_clean` play. That clip also shows Rumi rising and hugging Roshan (`assets_src/cinematics/day_one_story_clips_2026-09-23/CLIP_MANIFEST.json`).

**If the owner keeps the in-room rise** (the default):
- Make a rise action from the approved Rumi package instead of a swim loop slid upward: emerge, break the surface, settle into the wave.
  - `rumi_pool_idle_swim_atlas.png`, `9068a5f6…`
  - `rumi_eight_pose_runtime.png`, `44120bbb…`
- Pair it with one play of the approved breach splash `assets/sprites/fx_water/fx_water_splash_breach_atlas.png` (`12ffe29b…`) at the surface. Its sibling ripple atlas already plays under her.
- Use the job card, pilot review and identity rules above. Keep Rumi's identity: enormous violet braid, pointed ears, navy sea-jacket, shell clasp, aqua-lavender tail, coral fins.

**If the owner lets the clip own the rise,** Codex instead removes the in-room rise and keeps the wave beat: Rumi already at the surface, waving, for at most 2 s before the clip. Claude re-assesses C8 afterwards.

### P5. Swimming dust bunny: paddle loop and ripple review

**Today.**
- `assets/castle/dirty_cleanup_2d/critters/dust_bunny_swimming.png` (1024x683, `d7883664…`) bobs and squashes as one cutout.
- Since this round it sits on a held cell of the approved ripple atlas `assets/sprites/fx_water/fx_water_ripple_ring_atlas.png` (`5fbfa30a…`, cell 3 of 4x2). The ring is tinted halfway to the owner's water colour at opacity 2.5x the old arc alpha: 0.45 in the Pool, 0.65 on the dirty bathtub water and 0.55 in the filled bathtub.
- Claude chose these numbers without seeing them.

**Deliver.**
1. A P1-style capture set of the swimmer in the dirty Pool, the dirty bathtub and the filled bathtub. Recommend exact `self_modulate` values if the ring reads too strong or too faint. Claude changes the constants on your recommendation.
2. A four-key paddle loop (local Aseprite, reuse first), at the same anchor, footprint and scale, so the bunny swims rather than wobbles. Export a strip plus JSON. Both the Pool and the bathtub use it.

### P6. Water-true catch feedback (review first, then a small code change)

**Today.** A scoop shows the Day One clean ring plus three soap bubbles. Soap belongs to scrubbing; a scoop lifts something out of water.

**Proposal.** At the catch point, play one cell sequence of the approved `assets/sprites/fx_water/fx_water_splash_small_atlas.png` (`bdd9233b…`, 4x2) for about 0.5 s at about 90 px. Keep the clean ring for the lane and seahorse completions.

**Steps.**
1. Codex captures both versions in place for the owner (P1 shapes).
2. If the owner prefers the splash, change `PoolSkimmerActivity._spawn_catch_feedback`. Effects must stay off Roshan, at most 0.25 of her, and clear within 1 s (OD4).

### P7. Voice (carries GS2-C)

1. **Per-object pickup lines.** Make the six takes in GS2-C ("The wrapper is out!" and the others) through the Day One filler pipeline, so `skimmer_pickup_line` prefers them. Catalogue rows go through the generator, not by hand.
2. **A hint that teaches the best verb.** Today the seahorse hint says "Tap fast to pull the trash off the seahorse!", yet a deliberate pull earns two tugs (`DL-AGE-05`). Add `day1_pool_seahorse_hint_pull`: "Tap or pull to tug the trash out!". Claude or Codex then switches `IDLE_REPROMPT_LINES` and `_announce_current_activity` (one line each).
3. **Status report.** Every Pool line is a synthetic `filler_v1` placeholder. List each `day1_pool_*` cue with its path, duration and status for the owner's listening session. Never replace or edit the protected family recordings.

### P8. Device evidence support (5/5 device lane)

1. Build the debug APK from the integrated candidate.
2. Run the Pool route on the Lenovo Tab M11 per [the emulation protocol](../../../audit/LENOVO_TAB_M11_EMULATION_PROTOCOL_2026-08-30.md) (`850b4708…`), and on the older phone when available.
3. Record for each P1 state:
   - frame time p95 and p99 (budget 33.3 and 50 ms, `DL-PERF-02`);
   - any hitch over 100 ms;
   - memory;
   - the APK hash.
4. Store the numbers under `audit/pool_five_star_20261004/device/`.

The owner records the device lane in `games.json` only after a real session. An emulation run is evidence, not the device lane.

## Owner questions (copied from the framework)

1. **QP-1.** Rumi rises in the room, then again in the 17 s clip. Keep both, now in sequence (default), or let the clip own the rise?
2. **QP-2.** May other Day One rooms drop the code-drawn wash the way the Pool now does, once each has authored dirt? This is GS5 question 5; the default is yes, room by room.
3. **QP-3.** Should the castle stop drawing the room under a full-screen story clip? The default is yes; it is code-only and Claude or Codex can do it as follow-up F1.

## Delivery

This packet is published on GitHub with a manifest and an anonymous fetch receipt. The links and hashes are in the session report and in the [impact record](../../../design/audit_impacts/pool-five-star-framework-20261004.json).

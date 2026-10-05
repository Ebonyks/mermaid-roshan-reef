# Mermaid Pool: proposed five-star implementation (2026-10-03)

Status: `PROPOSED / CANDIDATE`. This is the owner-requested five-star proposal for the gold-star reference game. Claude did the primary coding. The art and voice generation it still needs is handed to Codex in [section 5](#5-codex-handoff-gs2-art-and-voice-for-the-pool).

**Where it stands.** On the [gold-star scorecard](../../../design/reference/GOLD_STAR.md) this code moved the Pool from 3/5 (17 of 24 points) at dev `87f99268` to 4/5 (22 of 24).

**Correction, 2026-10-04.** The owner asked for overdraw to be analysed specifically, and the refined criteria measure it on the real screen. The Pool's own code is clean, but its screen is not:

- the shared castle dressing draws a 12% dirt wash, grime, drips and cracks in code over the room and over Roshan;
- two identical cleanup baskets overlap;
- a full-screen fill is drawn hidden under the room tiles;
- Rumi's reveal briefly stacks 255 layers.

**Update, 2026-10-04 (later).** Claude repaired the Pool's screen overdraw (`MA-VIS-009`, carved from `MA-VIS-008`, fixed pending verification). The "255-layer burst" turned out to be a meter artifact. The Pool now waits only for the OD2 look-alike review and the human checks. The current plan is the [five-star framework](../codex_pool_five_star_2026-10-04/FRAMEWORK.md) and its [Codex packages](../codex_pool_five_star_2026-10-04/README.md).

So the Pool is **3/5 (19 of 24)** under the refined criteria until [GS5](README.md#gs5-fix-the-measured-overdraw-ma-vis-008) fixes those ([`MA-VIS-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-008)). After that, a rating of 5 ("gold star") also needs three human results, none of them recorded yet:

- a phone session;
- an observed child session;
- the owner's acceptance (`DL-QA-04`, `DL-QA-05`, `DL-QA-06`).

Nothing here claims that acceptance.

## 1. What changed, by criterion

| Criterion | Before (audit at `87f99268`) | After (this change) |
|---|---|---|
| C3 Non-reader objectives | Skimmer lines followed the item index and mostly said "leaf"; the seahorse had no pointer; pointers were emoji glyphs; nothing re-spoke when the child went quiet | The skimmer names the leaf only for the leaf and otherwise uses object-neutral lines (`DayOnePoolCleanup.skimmer_pickup_line`). The approved ghost hand points at the next piece, demonstrates one downward stroke on the next waterfall lane, and taps the seahorse's trash. After 8 quiet seconds the activity's other exact line plays, then its hint again, twice at most |
| C5 No-fail and agency | The seahorse was eight identical taps, and taps made during Roshan's work were silently dropped | Taps during work wait their turn (up to three), each answered at once with bubbles and paid only after its own contact time. A deliberate pull is worth two taps, so pulling is the fastest way through. Focus loss drops the unearned queue. Thirty quiet seconds earn nothing |
| C7 Art and identity | Code-drawn wash rectangles, chevrons, arcs, progress dots and bubbles; emoji pointer and "✦"/"○" glyph effects; the dingy room tint also darkened Roshan | Only approved art (below). Waterfall progress is the authored dirt itself, wiped away from the top where the child strokes. Roshan's cutouts carry the exact inverse of the room tint. Correction (2026-10-04): the shared castle dressing still draws a 12% wash over her in code, so her colours are muted until GS5 |
| C8 Feedback | A wrong-object line could play; dropped taps got no response | Every touch answers at once, and no line names the wrong object |
| C10 Verification | Waterfall and seahorse completion used probe helpers; the idle leg lasted 0.12 s; voice was checked by grepping source | All three activities are completed with real touch events, strokes, taps and pulls. There are thirty-second zero-input, retarget, queue, second-finger, focus-loss and teardown legs. Two mutation tests prove the new checks fail when the behaviour regresses |
| C4, C6, C9 | Already met | Kept. In addition, a touch on another waterfall lane now retargets Roshan's unearned approach instead of vanishing, and a re-tap on the lane she is working never restarts her work |

**Approved art reused, nothing generated.** Each file below already has its row in `ASSET_LICENSES.md`.

| File | SHA-256 | Used for |
|---|---|---|
| `assets/castle/training/ghost_hand.png` | `e484d14899d8137448128314536132dbd16f970cb1f0fabea006e9d51b5435b9` | Pointers. Its fingertip, measured from the alpha channel at (217.5, 447) of 512 px, lands exactly on the target. |
| `assets/castle/dirty_cleanup_2d/effects/fx_soap_bubbles.png` | `394d0fddb89237bf1e152060a31f585e71e37b54a46246bb1444c52454d15d08` | Hand-work bubbles, tug bubbles and the progress row |
| `assets/castle/dirty_cleanup_2d/effects/fx_clean_ring.png` | `f3472eaadd8cffc08d4ea9e0dcf8d4455b5a5e4eea16eb4721a0d945c7cbac62` | Catch, lane-clear, seahorse-free and Rumi-reveal rings |

## 2. Files

**Changed:**
- `scripts/games/day_one_pool_cleanup.gd`: truthful pickup lines; idle re-prompts; counter-tint for Roshan; authored reveal ring.
- `scripts/games/pool_skimmer_activity.gd`: guide hand; authored catch feedback; no code arcs.
- `scripts/games/pool_waterfall_activity.gd`: guide-hand stroke demo; dirt wiped from the top; lane retarget; clear ring.
- `scripts/games/pool_seahorse_rescue_activity.gd`: queued taps; pull gesture; guide hand; authored bubbles and progress row.
- `scripts/day_one_contact_action_2d.gd`: authored hand-work bubbles; exposes Roshan's cutout. This file is shared with the Craft Room, which also loses its code-drawn bubbles.
- `scripts/probe_day_one_pool_cleanup.gd`: real-input completion and the new legs.

**Unchanged:**
- The save keys and their meaning (`day_one_pool_skimmer_mask`, `day_one_pool_waterfall_mask`, `day_one_pool_seahorse_tugs`).
- The voice catalogue and recordings.
- All art files and protected paths.
- The probe-helper API (`probe_collect_next`, `probe_clear_next_lane`, `probe_tap`), still used by the capture probe.

## 3. Verified

Machine verification only, with exact Godot 4.7.2-stable and an isolated `APPDATA`:

- `probe_day_one_pool_cleanup`: 132 checks, PASS.
- Mutation tests: re-dropping queued taps fails 3 checks; restoring index-keyed lines fails 4.
- Also PASS:
  - `probe_day_one_art_attack_state`, which shares the contact action;
  - `probe_day_one_director`, `probe_day_one_integration`, `probe_day_one_voice`, `probe_day_one_handoffs` and `probe_day_one_d8_revisits`;
  - `probe_passive`, `probe_castle_pool_life_2d` and `probe_alpha_milestone_save`.
- The branch's exact-head Probe Suite result is recorded in the [impact record](../../../design/audit_impacts/gold-star-pool-five-star-20261003.json).

## 4. What makes it a gold star: three human checks

Record each result with `tools/gold_star.py`: add it to the game's `acceptance` lane in `design/reference/games.json`, together with the evidence path or owner-decision ID. Then run `--render`.

1. **Phone (device lane).** On the older Android phone, play the pool from a fresh Day One save, or from the pool on an existing save. Watch for the following, and note anything that fails:
   - Roshan swims to each piece and only then scoops;
   - the hand points at the next piece;
   - each waterfall stroke wipes the dirt away from the top;
   - fast taps on the seahorse are never lost, and a pull counts double;
   - Roshan's colours stay bright while the room is dingy;
   - Rumi rises at the end;
   - no stutter.
2. **Child (child lane).** Without helping, watch whether your child understands each of the three jobs from the voice and the hand alone. Note where they hesitate and whether they discover pulling.
3. **Owner (owner lane).** Does the pool look, sound and play right? A "no" is recorded as `not_accepted`, which keeps C12 at 0, exactly as Chef's verdict is.

## 5. Codex handoff: GS2 art and voice for the Pool

Claude writes; Codex builds every image, board and capture (CLAUDE.md, 2026-09-30). These items raise presentation beyond the machine bar. None is required for 4/5; the overdraw repairs in GS5 are.

### GS2-A. Roshan's three work actions (authored frames instead of one leaning cutout)

Today Roshan works with one approved directional cell: `assets/characters/roshan_25d/roshan_directional.png`, region (256, 0, 256, 256), scale 0.95, facing right. Her hand socket is at cell pixel (174, 151), that is (46, 23) from the cell centre. The tool is attached there.

- **Rules.** The owner's 2026-10-03 animation workflow decision applies: `AGENTS.md`, `DL-MOT-12`, `DL-MOT-14` to `DL-MOT-16` and the [production protocol](../../../design/animation/ANIMATION_PRODUCTION_PROTOCOL.md). Complete one [job card](../../../design/templates/ANIMATION_JOB_CARD_V1.md) per action, with its attempt, time and cost caps set before work starts.
- **Method (`DL-MOT-14`, `DL-MOT-16`).**
  - Use the default local character workflow: start from the approved directional cell and the base atlas, and author or key the action in 2D.
  - Use ImageGen only for a named missing key or a local repair, never one job per frame.
  - Default two generated takes per brief. After two nonviable takes, stop, diagnose and change the method or inputs.
  - No paid job without an existing funded budget.
- **Master and export (`DL-MOT-15`).**
  - Keep one editable RGBA Aseprite master per action, tagged `scoop`, `scrub` or `tug`, with the hand socket as per-frame pivot data.
  - Export losslessly to the strip below plus JSON: frame rects, durations and the socket for every frame.
  - Show that the master and the export match, and that Godot samples the exported pixels unchanged.
  - Keep the painted contours and antialiasing; no pixel-art conversion.
- **Identity.** The authority is the base atlas `assets/characters/roshan_25d/roshan_base.png`:
  - never bind `roshan_sprite.png`;
  - she wears the tiara outside a career costume (`ODR-ROSHAN-Q14`);
  - her tail is iridescent, and lavender or rainbow are both correct (`ODR-ROSHAN-IRIDESCENT`);
  - continue the light state of the cell you extend (`ODR-ROSHAN-Q12`).
- **Clip contract (`DL-MOT-12`).** For each action:
  - At least four distinct drawn keys within the 0.42-second contact. Declared durations and animation on twos are allowed if the whole action reads. The settle key is a declared hold, not padding.
    1. Scoop (skimmer): reach forward with the net; dip; lift with drops; settle.
    2. Scrub (waterfall): reach up; press; pull down; settle.
    3. Tug (seahorse): grip; lean back; pull; settle.
  - She faces right in every frame, at the same scale and baseline as the directional cell. The code never mirrors her.
  - The tool hand stays on a measured socket in every frame, and the code moves the tool with it.
  - While she swims to the target, the existing directional cell shows. The action plays only while her hand is in contact.
  - A retarget restarts the action from its first key. Completion or a cancel hides the work cutout and restores her room cutout, so no exit frame is needed.
  - The clip is presentation only. Progress stays with the contact gate and its 0.42-second work time, never with the clip ending.
  - Default skin only. The fairy and huluu costumes keep their current single cutout.
- **Deliverable.** Export each action as one 1024x256 RGBA strip of four 256x256 cells, or a power-of-two atlas if it has more keys, under `assets/castle/day_one_pool/activities/roshan_work/`. Put the JSON beside it, keep the Aseprite master with its provenance, and add rows in `ASSET_LICENSES.md`.
- **Not allowed:**
  - a new outfit, extra limbs or a second tail;
  - painted-in tools (the tool stays a separate approved prop);
  - text;
  - static-sticker wobble in place of acting.
- **Pilot first.** Make the scoop first. The owner reviews its frames at full speed and frame by frame, on a review board that Codex builds, before scrub and tug are made.
- **Wiring.** `DayOneContactAction2D` gains an optional strip: its `avatar` region follows the JSON frames by `work_time`. The skimmer's `RoshanHoldingSkimmer` cutout does the same with its scoop time. Probes assert the socket error stays below 1 px on every frame, as the existing grip checks do.
- **Acceptance.** Delivery grants none. The job card's identity, motion and export reviews come first, then the phone, child and owner checks in section 4.

### GS2-B. Water ripple for the floating pieces and Rumi's rise (optional)

- **What.** A flattened aqua water ring, 512x128 RGBA, transparent, in the style of `fx_clean_ring.png` (navy outline, pastel fill, no sparkles).
- **Where it goes.** It grounds each floating piece on the water, replacing nothing (the code-drawn arcs are gone), and replaces the clean ring under Rumi's rise.
- **Path.** `assets/castle/day_one_pool/activities/fx_water_ripple.png`, with a licence row.

### GS2-C. Exact per-object skimmer lines (voice, through the existing Day One filler pipeline)

- **What.** Six short takes in the same Roshan voice as the `day1_pool_*` lines:
  - "The wrapper is out!"
  - "The cup is out!"
  - "The lid is out!"
  - "The leaf is out!"
  - "The ribbon is out!"
  - "The sponge is out!"
- **IDs.** Cue IDs are `day1_pool_skimmer_item_<wrapper|cup|lid|leaf|ribbon|sponge>`, policy `once_per_session`, route `pool`.
- **Catalogue.** Add the rows through the generator: `scripts/day_one_contextual_voice_catalog.gd` says it is generated, so do not hand-edit it.
- **Wiring.** `skimmer_pickup_line` already prefers a READY per-object row, so no code change is needed once the rows exist.
- **Acceptance.** Owner listening remains pending, as for every synthetic line.
- **Optional.** A hint that names both verbs, "Tap or pull to tug the trash out!" (`day1_pool_seahorse_hint_pull`). Using it is a one-line change in `IDLE_REPROMPT_LINES` and `_announce_current_activity`.

## 6. Limits

- Machine verification only; no phone, child or owner result exists.
- The voices remain synthetic placeholders.
- The Craft Room shares the contact-action change (authored bubbles); its own pointer and glyph effects are untouched.
- No other game, save key, protected asset or workflow changed.

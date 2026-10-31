# Mermaid Pool: the five-star framework (2026-10-04)

Status: `PROPOSED / CANDIDATE`. Written by Claude for the owner's master-audit request: the Pool is the first area to be refined to a five-star standard, with code changed where necessary and new Codex handoffs for graphics and animation. Claude made the code repairs below; Codex builds every image, board, capture and animation ([README.md](README.md), packages P1-P8). Baseline: dev `a52f545f4c5e7cc720b0d1194b374801ece0e24e`. Machine evidence only; no device, child or owner result is claimed.

> **Revision 2, 2026-10-05.** The owner answered QP-1 to QP-3 ([section 11](#11-owner-answers-2026-10-05)). Rumi now rises once, in the `d1_pool_clean` clip: Claude removed the in-room rise, and P4 is withdrawn. The castle and its voice caption stop drawing under every full-screen story clip, closing F1. The answer to QP-2 can be read three ways, so no room's dirt look has changed on it yet; the follow-up question is QP-2a. Baseline for this revision: `356afeb94bef803f3d1d2268adfed3f1405143b7`.

## 1. Where the Pool stands

| | Before this round (dev `a52f545f`) | After this round | Gold star |
|---|---|---|---|
| Rating | 3/5, 19 of 24 | 3/5, 21 of 24 | 5/5, 24 of 24 |
| What holds it | Measured overdraw on its screen (C7 capped at 1); `MA-VIS-008` open (C11 0); no human results (C12 0) | Only the OD2 look-alike review (C7 capped at 1) and the human lanes (C12 0) | Every criterion at 2, every overdraw check passed, phone, child and owner accepted |
| Next step | — | **4/5**: record OD2 from Codex's phone-size captures (P1) | **5/5**: phone, child and owner sessions (section 8) |

The rubric is [`design/reference/gold_star.json`](../../../design/reference/gold_star.json); the live page is [`GOLD_STAR.md`](../../../design/reference/GOLD_STAR.md); `python -B tools/gold_star.py --compare day_one_pool` prints the ordered list at any time.

## 2. What five stars means for the Pool

A five-star Pool is one a four-year-old who cannot read finishes alone, with one finger, without a wrong turn or a dull moment. Roshan is plainly the hero, every action looks and sounds true, and it runs smoothly on the family's phone. The table turns that into checkable bars. Each bar cites the gold-star criterion and the design rules behind it.

| Pillar | The five-star bar for the Pool | Rules | How it is proven | State |
|---|---|---|---|---|
| Reach and framing | The second Day One room opens from a fresh save through the gold hall door. Leaving and returning resumes exactly where the child stopped | C1; `DL-AGE-06`, `DL-SAVE-04` | `probe_day_one_director`, `probe_day_one_integration`, `probe_load` | Met |
| Understood without reading | Each job has its own spoken line and the approved ghost hand on the live object. A quiet child hears the line again, twice at most. Nothing else on screen invites a touch | C3; `DL-AGE-01`, `DL-SND-01`, `DL-READ-03` | `probe_day_one_pool_cleanup` (idle re-prompts, guide hands); `probe_interaction` (no halo on suspended props) | Met (halo repaired this round, `MA-TOUCH-003`) |
| One finger, generous | Fixture-sized hit regions; one touch owns each gesture; a second finger never steals or cancels it | C4; `DL-AGE-02`, `DL-UI-01` | Probe second-finger and far-touch legs | Met |
| Kind and earned | Zero input never advances. A deliberate stroke or pull beats mashing. Taps during Roshan's work wait their turn. No loss, timer or reset | C5; `DL-AGE-03`, `DL-AGE-05` | Thirty-second zero-input leg; queue, pull and retarget legs | Met |
| Truthful action and acting | Roshan travels, her hand makes contact, and only then does the dirt clear; the trash really leaves the mouth; the fixture really changes. At five stars she also *acts* each verb (scoop, scrub, tug) with authored frames | C6; `DL-INT-01`, `DL-INT-02`, `DL-MOT-12`, `DL-MOT-14` | Contact-gate probes; grip error under 1 px | Mechanics met; acting is one leaning cutout (Codex P2) |
| Picture | Approved painted art only, one focal action, Roshan whole and in her own colours. No code-drawn shape, wash, duplicate or hidden layer; inside the fill budget on every play state; props lit like the room | C7, OD1-OD6; `DL-MED-02`, `DL-MED-05`, `DL-READ-01`, `DL-READ-02`, `DL-PERF-03` | `tools/measure_overdraw.py`; OD1 painted-copy and OD2 look-alike reviews | Machine checks pass; OD1 reviewed; OD2 needs P1; props still product-lit (P3) |
| Feedback and reward | Every touch answers within two frames. Sight and sound describe the same event. The reward (light returns, rainbow, fountain, then Rumi's one rise in the clip) plays out before the next scene takes the screen | C8; `DL-AGE-07`, `DL-MOT-04`, `DL-CIN-16` | Probe legs for queued answers and the held reward beat | Met (reward beat repaired, `MA-PLAY-006`; one rise since revision 2, owner QP-1) |
| Sound | Every line is true of what happened and teaches the best verb. Music, ambience and voice are mixed for a phone speaker. Lines are owner-approved, never synthetic placeholders at release | C3, C8; `DL-SND-01`, `DL-SND-04`, `DL-SND-13` | Voice catalogue status; owner listening | Lines true; all are `filler_v1` placeholders; the seahorse hint teaches tapping, not pulling (P7) |
| Lifecycle and save | Every change saves; a restored finish completes once; leave, pause, focus loss and re-entry are clean; the reward hold cannot lose progress | C9; `DL-SAVE-01`, `DL-SAVE-03` | Restore, re-entry, focus-loss and teardown legs | Met |
| Proof | A trusted probe drives every step with real input, a zero-input leg and teardown, and each new guard is shown to fail under a mutation | C10; `DL-QA-02`, `DL-QA-03` | Section 5 | Met |
| No open defect | No Pool finding open as a defect | C11; `DL-QA-10` | Finding register | Met: `MA-VIS-009`, `MA-PLAY-006` and `MA-TOUCH-003` are fixed pending verification |
| Phone, child, owner | 30 fps on the Lenovo Tab M11 and the older phone (p95 at most 33.3 ms, p99 at most 50 ms, no hitch over 100 ms). An observed child finishes without help. The owner accepts the look, sound and play | C12; `DL-PERF-02`, `DL-QA-04`, `DL-QA-05`, `DL-QA-06` | Section 8 | None recorded |

## 3. The child's Pool, beat by beat

| # | Beat | What the child sees, hears and does | State after this round | Five-star target and package |
|---|---|---|---|---|
| 1 | Arrival clip `d1_pool_arrival` (9.5 s, owner-selected cut) | Dirty pool, blocked waterfall, stuck seahorse | Plays between scenes (`DL-CIN-16`); skippable from the global Back | Unchanged; device check (P8) |
| 2 | Dirty room | Dingy declared tint with Roshan counter-tinted. Olive sludge curtain on the waterfall, sick seahorse, six floating pieces, a swimming dust bunny on a ripple and a shore bunny | No code wash, grime or ambient motifs; one basket; swimmer on approved ripple art | Props lit like the room (P3); bunny paddle loop (P5) |
| 3 | Skimmer | Line "Sweep the skimmer…"; ghost hand taps the next piece; Roshan swims to it, dips the net and the piece flies into the basket with a clean ring and bubbles; a true pickup line | Travel, contact and credit; truthful lines | Authored scoop (P2 pilot); per-object lines (P7); water splash instead of soap (P6) |
| 4 | Waterfall | Hint line; the hand demonstrates one downward stroke on the next lane; the child strokes and the authored dirt wipes away from the top; three lanes | Strongest single activity in the game | Authored scrub (P2) |
| 5 | Seahorse | Hint line; the hand taps the trash in the mouth; taps and pulls tug it (a pull counts double); eight tugs and it flies into the basket | Queued taps; pull rewarded | Authored tug (P2); a hint that names pulling (P7) |
| 6 | Finale | Light returns, rainbow waterfall sequence, healthy fountain; "The whole pool is shiny!" | Revision 2: no in-room Rumi (owner QP-1). The clean-pool beat holds 2.4 s from the finale's start, then until the voice lane is quiet, at most 5.6 s, before the room completes | Device and child check |
| 7 | Completion clip `d1_pool_clean` (17 s) | Rumi rises and hugs Roshan: her one rise | Starts after the beat; since revision 2 the castle and its caption stop drawing under it (owner QP-3) | Device check |
| 8 | Handoff | "Back to the hall, then follow the glowing door!" toward the playroom; the gold door cue | Unchanged | Device and child check |

## 4. What this round changed

Claude implemented these on the candidate built from `a52f545f`.

| Change | Files | Why |
|---|---|---|
| The castle dressing's code-drawn wash, grime, drips and cracks move into a child `DayOneCastleGrime` layer, hidden in rooms listed in `AUTHORED_DIRT_ROOMS` (the Pool) | `scripts/arena/day_one_castle_dressing.gd`, new `scripts/arena/day_one_castle_grime.gd` | The Pool shows dirt through authored fixtures and a declared tint with Roshan counter-tinted. A 12% code wash over her undid that (`MA-VIS-009`, GS-19) |
| One cleanup basket: the skimmer hands its pieces to the rescue's basket at the same anchor | `pool_skimmer_activity.gd`, `pool_seahorse_rescue_activity.gd`, `day_one_pool_cleanup.gd` | Two identical baskets were drawn over each other (OD1) |
| The cleanup joins `LivingWorldDirector.QUIET_GROUP`, so code-drawn ambient motifs pause while it is mounted | `scripts/living_world.gd`, `day_one_pool_cleanup.gd` | Ambient code shapes over the job (OD3, GS-20) |
| The swimmer's ripple and Rumi's rise use the approved project-original `fx_water_ripple_ring_atlas.png` | `day_one_dust_bunny_swimmer.gd` (shared with the bathtub), `day_one_pool_cleanup.gd` | Code arcs (OD3); a "clean" ring for a water rise said the wrong thing (`DL-MOT-04`). Reuse replaces GS2-B |
| The Pool finale no longer adds the generic nine-star burst | `scripts/arena/castle_rooms_25d.gd` | Nine copies of one star over Rumi's rise (OD1); the bathroom already avoids it |
| The castle letterbox fills only the bands the fitted stage leaves | `castle_rooms_25d.gd` | A full-screen fill was drawn 98-100% hidden under the room tiles (OD6) |
| The touring touch halo marks only hotspots visible in the tree | `castle_rooms_25d.gd` | It pulsed over props the cleanup had suspended (`MA-TOUCH-003`, GS-22) |
| The room completion waits for Rumi's wave and reply: at least 1.2 s, then until the voice lane is idle, at most 4.5 s | `day_one_pool_cleanup.gd` | The 17 s clip started in the same frame, pausing the tree mid-line (`MA-PLAY-006`, GS-21) |
| The overdraw meter counts a layer spawned during counting once, and sees code shapes drawn through a connected `draw` callback | `scripts/probe_overdraw.gd` | The reported "255-layer burst" was such a layer drawing in its real colours; script-less callback drawing was invisible to OD3 |
| The meter measures Rumi's real reveal at real speed, and records the completion clip separately as a non-play state | `scripts/probe_overdraw.gd`, `gold_star.json` | On the 4x probe clock "finale" had measured the clip, not the reveal |

**Revision 2 (2026-10-05, owner answers).**

| Change | Files | Why |
|---|---|---|
| The finale stages no in-room Rumi: no rise, ripple, wave or "Hi, Rumi!" line. The clean-pool beat (light, waterfall, fountain, "The whole pool is shiny!") holds the room completion for 2.4-5.6 s from the finale's start. After the clip, the persistent Rumi waits in the pool as before | `day_one_pool_cleanup.gd`; `castle_rooms_25d.gd` now owns the Rumi pose-atlas path its persistent Rumi uses | Owner QP-1: "No, only one." The clip, an owner-selected cut that cannot be altered (`DL-CIN-16`), shows her rise, so the room's rise went |
| While a story clip plays, the castle layer's picture and the castle voice caption are hidden, and restored when the clip ends, is skipped or is cancelled. The castle layer itself stays visible, because game logic reads it as "the castle is the surface" | `scripts/main.gd` | Owner QP-3: the castle no longer draws under the video (F1) |

The save keys, voice catalogue, art files and protected paths are unchanged. No new asset was added: the ripple atlas already had its `ASSET_LICENSES.md` row.

## 5. Machine evidence

**Overdraw on the real route.** Exact Godot 4.7.2-stable, Mobile renderer on Vulkan (Mesa llvmpipe under Xvfb, 1920x1080 window), numbers only. "Before" is the same route at the unmodified baseline; "after" is the official `tools/measure_overdraw.py` run recorded in `overdraw.json` (2026-10-05T00:12Z). The table gives mean GPU layers, the share of the screen with four or more layers, and the max and peak. Budget: mean at most 2.5, at most 0.10 with four or more, max 8, peak 32.

| State | Before (`a52f545f`) | After |
|---|---|---|
| start | 3.28, 0.241, max 7; translucent median 1 | 1.40, 0.025, max 5, peak 5; translucent median 0 |
| skimmer contact | 3.50, 0.334, max 7, false peak 155 | 1.39, 0.023, max 5, peak 5 |
| waterfall start | 3.51, 0.327, max 7 | 1.41, 0.013, max 5, peak 5 |
| waterfall stroke | 3.28, 0.220, max 8 | 1.18, 0.008, max 6, peak 6 |
| seahorse start | 3.49, 0.321, max 7 | 1.39, 0.011, max 5, peak 5 |
| seahorse tug | 3.49, 0.327, max 7 | 1.39, 0.011, max 5, peak 5 |
| finale (Rumi's rise) | not measured; the probe caught the clip (4.49, 1.0, max 8; published peak 255) | 1.40, 0.010, max 5, peak 5 |
| story clip (not a play state) | — | 3.39, 0.265, max 7, 21 drawn items: the castle still rendered under the video. Revision 2: 2.02, 0.011, max 6, 3 items (black backdrop, video and the global Back) |

After the repair:
- No duplicate texture pair, code-drawing script or broad translucent layer remains in any play state.
- Effects clear within 1 s and stay off Roshan.
- The published numbers in [`overdraw.json`](../../../design/reference/overdraw.json) come from the final `tools/measure_overdraw.py` run on this candidate.

Revision 2 re-measured all 16 games on its merge base `356afeb9` plus these changes (`overdraw.json`, 2026-10-05T05:53Z). The Pool's play states are unchanged within run-to-run variation, which depends on whether the castle voice caption is up during the sample. Seahorse tug read 1.38 with the caption showing and 1.16 without it, and the published run has it at 1.16. The finale, now without Rumi, reads 1.37 with 22 drawn items, down from 26. The first-arrival state (`entry_transition`, not budgeted) depends on timing. The published run caught the room cross-fade, unchanged at 4.38. One Pool-only run instead caught the arrival clip, which then measured 2.03 with 4 items, as clean as `d1_pool_clean`. No Opera file changed in this revision. Even so, the Opera careers' numbers moved by up to ±0.33 between runs, with the same drawn items each time; the cause is not isolated. In this run the Detective's `task_open` reads 2.51, crossing the 2.5 budget it passed at 2.18. No rating changed, because every career already fails OD3.

**Meter self-test.** Six full-screen layers count exactly 6 (one translucent). A white opaque layer added during counting counts exactly 7, with peak 7. With the late-layer fix disabled, the self-test fails. A connected-draw callback is seen as code drawing.

**Probes and mutations.**

| Probe | New check | Mutation that turns it red |
|---|---|---|
| `probe_day_one_pool_cleanup` | One room basket at the skimmer's landing point | Skimmer basket left visible |
| `probe_day_one_pool_cleanup` | The cleanup quiets the ambient layer | Group join removed |
| `probe_day_one_pool_cleanup` | Swimmer on approved ripple art, no code arcs; Rumi rises through the ripple atlas | — |
| `probe_day_one_pool_cleanup` | Completion waits for the wave and reply; exactly one completion | Immediate emit restored |
| `probe_day_one_castle_dressing` | Authored-dirt Pool draws no code grime; other rooms keep theirs | `AUTHORED_DIRT_ROOMS` emptied |
| `probe_castle_pool_life_2d` | No star burst at the Pool finale; no swimmer code arcs | Burst re-added |
| `probe_living_world` | The quiet group pauses the ambient layer only while mounted | Suspension check removed |
| `probe_interaction` | The halo goes quiet over a suspended hotspot layer and returns after | Old `visible` test restored |
| `probe_day_one_pool_cleanup` (rev. 2) | No in-room Rumi or rise ripple; `d1_pool_clean` owns the rise; the completion waits for the clean-pool beat, then completes once | A Rumi node re-added at the finale; the beat's minimum cut to 0.2 s |
| `probe_day_one_story_clips` (rev. 2) | The castle and its caption stop drawing under a clip, stay the open surface for game logic, and return after a finished, skipped or cancelled clip | Cover call removed; uncover made a no-op |

The full trusted roster (82 probes, isolated user data, as `scripts/ci.sh`) passes on the candidate. The branch's remote Probe Suite run is recorded in the [impact record](../../../design/audit_impacts/pool-five-star-framework-20261004.json).

**Letterbox bands.** Checked at a 2560x1369 window (33 px pillars), the M11's 16:10 (40 px top and bottom) and a 1.3:1 window (132 px top and bottom); a 16:9 window hides both bands.

## 6. Gap register

| ID | Gap | Pillar | Owner | Package |
|---|---|---|---|---|
| G1 | OD2 look-alike review at phone size with the HUD is not recorded | Picture (C7 cap) | Codex captures; Claude or owner reviews | P1 |
| G2 | Roshan acts each verb with one leaning cutout | Truthful acting | Codex | P2 |
| G3 | Props keep product-render lighting and glow auras, hidden by runtime tints | Picture | Codex | P3 |
| G4 | Rumi rises twice (room, then clip); the in-room rise is a swim loop slid upward | Reward | Closed in revision 2: owner QP-1, the clip owns the one rise | P4 withdrawn |
| G5 | The swimming bunny wobbles as one cutout; ripple tint and opacity are unreviewed | Picture | Codex | P5 |
| G6 | Scoop feedback uses soap bubbles for a water event | Feedback | Owner choice from Codex captures | P6 |
| G7 | All lines are synthetic placeholders; the seahorse hint teaches tapping, not pulling; per-object pickup takes missing | Sound | Codex voice pipeline; owner listening | P7 |
| G8 | No phone, child or owner result | Phone, child, owner | Owner and family; Codex supports | P8, section 8 |
| F1 | The castle renders hidden under every full-screen Day One story clip (3.39 mean layers during `d1_pool_clean`) | Performance | Closed in revision 2: owner QP-3; 2.02 mean, 3 items | Done |
| F2 | Other dirty Day One rooms still draw the code wash over Roshan | Shared | Owner QP-2 answered; its scope awaits QP-2a | `MA-VIS-008` |
| F3 | Only the Pool and the Opera careers are measured; the bathroom, craft room and playroom are not | Shared | Claude or Codex | Extend `probe_overdraw.gd` groups |
| F4 | `probe_overdraw.gd` needs a display, so CI cannot gate overdraw; the trusted probes now gate the Pool's structure instead | Proof | Owner authority for workflow changes | GS3-style request |

## 7. The ordered path

1. **To 4/5.** Codex P1 captures, then the OD2 review recorded in `games.json`, `--render`. If OD2 fails, repair the named look-alike and re-measure.
2. **To 5/5.** The phone session (P8 support), the observed child session and the owner's acceptance, recorded in the acceptance lanes. A "not accepted" result keeps C12 at 0 and names what to change.
3. **Beyond the bar** (the difference between passing and delighting): P2 scoop pilot, then scrub and tug; P3; P7; P5; P6 (wait for QP-2a, which may decide it). P4 is withdrawn. After each delivery, re-run `probe_day_one_pool_cleanup` and `measure_overdraw.py --groups pool`, and Claude re-assesses the touched criteria.
4. **Shared follow-ups:** F3; F2 after the owner answers QP-2a. F1 is done.

## 8. Acceptance sessions (the human lanes)

Record each result in `design/reference/games.json`, under `day_one_pool.acceptance.<lane>`, as `{result, evidence}` with the session date, build or APK hash and notes. Then run `python -B tools/gold_star.py --render`.

**Phone (device).**
1. Install the dev APK built from the integrated candidate.
2. From a fresh Day One save, play the bathroom to open the pool, then the whole pool.
3. Repeat once on an existing save that re-enters mid-waterfall.
4. Watch and note:
   - Roshan swims to each piece and only then scoops;
   - the hand points at the next piece;
   - each stroke wipes the dirt from the top;
   - fast taps on the seahorse are never lost, and a pull counts double;
   - Roshan's colours stay bright while the room is dingy;
   - no halo pulses anywhere except the job;
   - the light, rainbow and fountain play out and "The whole pool is shiny!" finishes before the clip, which shows Rumi's one rise; the room never shows through the clip;
   - no stutter;
   - for the M11 numbers, the P8 frame-time table.

**Child (observed).**
1. Say nothing after "Let's play."
2. Note for each job:
   - the seconds until the first correct touch;
   - every touch that went somewhere else, and where;
   - whether the child discovers pulling on the seahorse.
3. Note whether the child watches the clean-pool beat and Rumi's rise in the clip, or reaches for the screen during them.
4. Stop if the child asks for help, and note the moment.

**Owner.**
1. Does the Pool look, sound and play right?
2. Answer QP-2a (section 11). QP-1 to QP-3 were answered on 2026-10-05.
3. A "no" names the frame or line, and it becomes the next repair.

## 9. Keeping it five-star

- **Measurement inputs.** The Pool's measurement is bound to the hashes of its sources, its evidence (including `living_world.gd::_suspended`, the dressing's authored-dirt list and the swimmer's ripple) and every code-drawing script on its screen. Any change makes it stale, and `tools/gold_star.py --check` says so. Re-measure with `python -B tools/measure_overdraw.py --groups pool` before re-scoring.
- **New patterns to copy** (`gold_star.json`):
  - GS-19: an authored-dirt room opts out of the shared code dirt;
  - GS-20: a focused activity quiets shared ambience;
  - GS-21: the reward beat plays out before the next scene;
  - GS-22: an affordance marks only what can be touched now.
- **Shared layers must honour these contracts.** A new shared layer drawn over a castle room must respect `AUTHORED_DIRT_ROOMS` and `LivingWorldDirector.QUIET_GROUP`, or be measured on the Pool's route before it lands.
- **Effects.** New Pool effects use approved art at the contact point, clear within 1 s and stay off Roshan (OD4).

## 10. What this does not claim

- No phone, child, owner, listening or visual acceptance.
- Desktop software rendering measures layers, not phone frame time (`MA-PERF-001`).
- The ripple's tint and opacity, the halo's quiet and the reward hold's timing are machine-checked only.
- The 2.4-5.6 s clean-pool beat and the castle's absence under clips are machine-checked only; nobody has watched them on a phone.
- The other Day One rooms and the Opera careers keep their open overdraw under `MA-VIS-008`.

## 11. Owner answers (2026-10-05)

The owner answered in the session chat, replying to Claude's report. The questions below are the report's wording, which is what the owner read. They are recorded as `ODR-POOL-RUMI-ONE-RISE-20261005`, `ODR-POOL-DIRT-LOOK-20261005` and `ODR-CASTLE-UNDER-CLIPS-20261005` in [`OWNER_DECISIONS.md`](../../../design/reference/OWNER_DECISIONS.md).

| # | Question as asked | Owner answer (verbatim) | What changed |
|---|---|---|---|
| QP-1 | "Rumi rises twice: once in the room, then again in the 17-second video. Keep both, or drop one?" | "No, only one." | The clip is an owner-selected cut that cannot be altered (`DL-CIN-16`), so the clip keeps the one rise. Claude removed the in-room rise and greeting; P4 is withdrawn. Section 4, revision 2 |
| QP-2 | "Should the other rooms lose their code-drawn dirt and wash the same way, as each gets its own painted dirt?" | "Only when dirty objects are specifically being cleaned, which is different from gathering dirt or freeing the seahorse." | Nothing yet. The answer can be read three ways (QP-2a below) |
| QP-3 | "Should the castle keep drawing underneath while a story video plays? That is what makes the video's layering high." | "No." | The castle and its voice caption stop drawing under every story clip. Section 4, revision 2 |

**QP-2a, open.** The owner's rule is that a dirty look belongs to dirty objects that are specifically being cleaned. Gathering dirt (the skimmer) and freeing the seahorse are different jobs. The rule can be applied in three ways:

1. **Dirt shows only on the object being cleaned.** Remove the shared code-drawn edge grime, wash and cracks from every room, the main hall included. Dirt then appears only on objects the child cleans: the bathroom's sink, tub and toilet, which are already painted dirty and scrubbed clean, and the Pool's clogged waterfall. In the Pool, the room-wide dingy tint, which today lightens with every piece scooped and every tug, would also go, or would follow the waterfall alone.
2. **A room drops the wash only when its job is cleaning objects.** The bathroom (scrubbing fixtures) drops the shared code wash now. A room whose job is gathering or freeing keeps it: the playroom, where Baby Eagle is freed. Read strictly, the wash would also come back to the Pool during its skimmer and seahorse jobs.
3. **"Wash" means the washing effects.** Soap bubbles and the clean ring belong to scrubbing a dirty object, such as the waterfall or the bathroom fixtures. Scooping trash out of the water and tugging trash off the seahorse get water and pulling feedback instead. This is P6's splash proposal, extended to the seahorse.

Claude's reading is 1, which is closest to the words "only when dirty objects are specifically being cleaned". Because it changes every room's look and the Pool's light, Claude waits for the owner to choose before changing code.

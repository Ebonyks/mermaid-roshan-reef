# THE EXPLORATION LAYER — Pearl Opera career worlds

Designed against the shipped data and code in
`C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/`:
`scripts/opera_stage_paths.gd`, `scripts/opera_career_world_2d.gd` (1755 lines),
`scripts/opera_world_backdrop_2d.gd`, `scripts/audio_director.gd`,
`scripts/save_state.gd`, `scripts/arena/castle_rooms_25d.gd`,
`OPERA_FRAMING_PACING_ANIMATION_AUDIT_2026-08-03.md`,
`CHAPTER2_PARTY_ROLES_2026-08-03.md`.

---

## THE SPINE — one rule the whole layer hangs on

**Far touch: the painting answers. Near touch: the painting answers, Roshan reacts, she speaks, and she keeps something.**

That single asymmetry does all the teaching. A 4-year-old who never understands "walk over there" still gets a responsive picture on every touch. A 4-year-old who notices that the bird only *gives* her something when she is standing under it has invented walking by herself, with no arrow, no words and no instruction. Every task below is an application of it.

Threshold: **220 px** from `_hero_feet()` (`:1329`) — about one Roshan-width plus a step. Same number the audit proposed for proximity gestures.

---

## THREE STRUCTURAL FACTS I FOUND IN THE CODE THAT BOUND THE DESIGN

1. **All 13 careers draw from 4-tile sets, not the single painting.** `_load_tile_set` (`opera_world_backdrop_2d.gd:50`) finds `world_<career>_c{0,1}r{0,1}.png` for every career; `_draw` prefers tiles (`:98-102`) and only falls back to `painting`. So the "make the painting itself respond" mechanic must sample the **tile quadrants**, not `backdrop_node.painting`. The mapping is exact and cheap: screen half = (640, 360); `col = int(sx >= 640)`, `row = int(sy >= 360)`; source = `Vector2(local.x * 1.6, (row == 0 ? 448.0 : 0.0) + local.y * 1.6)` in that tile. **Source-to-screen ratio is a uniform 1.6x**, so a 160 px screen patch samples 256 source px — plenty to scale to 1.10 without softening. A patch straddling a quadrant seam (chef's clue spot `[0.483, 0.1]` does) needs the patch rect intersected against each quadrant and drawn up to 4 times — ~25 lines, do it once in a helper.

2. **The painted district disappears at the theft.** `backdrop_node.set_stage(phase_index >= steal_index)` (`:687-691`) swaps to the `stage_*` tiles. Chef's `steal_index` is 4. **Therefore every touch-the-world and collecting beat must live in phases 0..steal_index−1** — arrival plus 3 wander windows on 7-phase careers, arrival plus 2 on the 6-phase ones (boxer, racer, popstar). The curtain call runs on the *stage* tiles, so curtain-call touches get sparkle-only responses, never patch bulges. This is a hard boundary, not a preference.

3. **Nursery has no derived geography.** `PATHS` (`:20`) holds 12 careers; nursery falls through to `FALLBACK_PATH` and to `clue_spots()`'s synthetic 8-point spread (`:224-230`), which are *not* on painted details. Gate the patch-bulge on `PATHS.has(career_id)`; nursery gets sparkle-only until its row is derived. **One derivation pass on `world_nursery_c*r*.png` closes the only data gap in the whole design.**

---

## THE ENGINE CHANGE (everything else is content)

Split `_show_phase()` (`:670`) into `_arm_phase()` and `_open_task()`, and add one state:

```
WANDER   -> free walk + world touches + collecting live; no card, no goal, no clock
TASK     -> today's behaviour exactly (card, surface, gestures)
BOP/LENS -> unchanged
```

- `_arm_phase()`: light the station marker, place the helper, run the teaser VO, set `wander_layer.mouse_filter = STOP`. Does **not** open the card.
- `_open_task()`: everything `_show_phase()` does today, minus the `_glide_roshan_to` (`:707`) — she walked here herself.
- Trigger: feet within **150 px** of the lit station, held **0.35 s** (same dwell grammar as the lens's 96 px / 0.45 s at `:1659`).
- New nodes: `wander_layer` (input only, no draw), `discovery_layer` (draw only, sits directly above the backdrop), `affordance_layer` (draw only, rings/breadcrumbs, above markers and below actors), `helper_actor` (`TextureRect`, same `_actor()` factory at `:508`).
- **Probe guard (mandatory):** `probe_opera_2d_balance.gd` pumps `_on_gesture` with `amount = 100` and never walks. If a gesture arrives while state is WANDER, call `_open_task()` immediately and then process the gesture. No probe edits, all 287 assertions hold.

### Input arbitration — hit-test before walking (the castle's own order)

`castle_rooms_25d.gd:1445-1465` already does exactly this: it ray-tests the dust bunny *first*, then falls through to a clamped walk. Mirror it, and honour the binding enemy-forefront tap-priority rule:

| order | target | radius | result |
|---|---|---|---|
| 1 | peekaboo imp | 90 px | bop it (fizzle burst, giggle, drops a favour) |
| 2 | helper | 110 px (`StorybookUI.MIN_TOUCH`) | "show me" (X-task H2) |
| 3 | Roshan's own screen rect | — | she giggles; **never** a walk destination |
| 4 | clue spot | 84 px | the painting answers (Tier A/B/C) |
| 5 | lit station marker | 120 px | walk there and dwell → task opens |
| 6 | anything else | — | walk to `_stage_feet_at_x(tap.x)` |

Draw order (extends the framing audit's list): `backdrop · discovery_layer · station markers · affordance_layer · prop · audience · helper · rival · Roshan · combat_layer · combat_fx · lens_layer · wander_layer(input) · card · plaque · fx_layer`.

---

## 1. FREE WALK

### W1 — WALK THE PROMENADE
- **Child does:** taps anywhere on the painting; Roshan walks there along the painted route. Holding and dragging leads her continuously — the destination follows the finger.
- **Reuses:** `_stage_feet_at_x()` (`:1337`) for the destination — *the identical law the imps already walk by* (`_tick_stage_combat:1316`), so she can never stand in water, in a flower bed or off-screen; `_lens_input`'s event shape (`:1620`) for touch + drag + mouse in one path; `_place_on_stage`'s depth term (`:521`); `flip_h` from `_glide_roshan_to:620`. Integrate with `move_toward` in `_process`, **not** a tween, so she can be re-aimed mid-stride.
- **Data:** `StagePaths.path_points(career)` — 9 waypoints per career; the first/last x ±40 clamp inside `_stage_feet_at_x`.
- **Art:** none. (Later, additive: `sheet_a` row 1 TRAVEL from the animation audit.)
- **Numbers:** 250 px/s cruise, 0.30 s ease in/out, no minimum trip. Chef's route is ~1009 px → 4.0 s end-to-end, 1.2–1.6 s for a typical leg. Contemplation comes from removing auto-advance, not from making her slow — at 1280 px a slow walk reads as input lag.
- **Rhythm:** live from the moment the world fades up, in every wander window, and under the confetti at the curtain call. Off during TASK, BOP and LENS.

### W2 — THE STATION INVITES, IT DOES NOT PULL
- **Child does:** nothing. The lit station breathes; she goes when she goes. Standing near it for 0.35 s opens the job.
- **Reuses:** `_draw_station_marker` (`:601`) — give it three states instead of two: `later` `Color(1,1,1,0.22)`, `current` (existing gold pulse) + `InteractionAffordance.color(INTERACTION, focused)` deep-blue breath, `done` steady warm halo `Color(1.0,0.86,0.42,0.45)` with no pulse. Progress becomes something she reads by *looking at the world* — lamps lit behind her, one still waiting ahead.
- **Data:** `station_for_phase` (`_assign_stations:528`), `station_list` with its `landmark` strings.
- **Art:** none — `station_marker.png` already ships.
- **Rhythm:** the whole wander window.
- **Escape hatches:** a tap on the *lit* marker from anywhere sends her straight there (a child who understands the goal is never made to route-plan). The audit's pull-back ladder runs unchanged — 6 s marker grows + chime, 11 s breadcrumb sparkles along `point_along()` between `nearest_t(points, _hero_feet())` and the station's t, 16 s VO re-prompt (existing 9 s idle timer at `:1708-1715`), 22 s assist via the existing `_glide_roshan_to` with "Let's go together!". **Any touch anywhere resets the clock**, so a child happily poking the painting is never nagged.

### W3 — STOP AND LOOK (the walk's own small reward)
- **Child does:** arrives somewhere with nothing there. She settles for ~1.2 s — breath, a slow head turn — and the nearest untouched painted detail within 260 px twinkles once, unprompted.
- **Reuses:** the `ActorMotion` node from the animation audit's three-node stack (breath formula `player.gd:450`: `y += sin(life)*2`, `scale = (1+sin*0.008, 1−sin*0.006)`); `affordance_layer` gold twinkle (`InteractionAffordance.sparkle_color(ANIMATION)`).
- **Data:** `clue_spots(career)`.
- **Art:** none.
- **Rhythm:** any wander window. This is the beat that teaches "walking somewhere shows you something" without a single word.

---

## 2. TOUCH-THE-WORLD

The 8 `clue_spots` per career are already coordinates of specific painted details, derived visually (`opera_stage_paths.gd:8-14`), and today they are used by **two detective phases only** — dead art in the other eleven careers. 13 × 8 = **104 responsive details for zero new assets.**

### T1 — THE PAINTING ANSWERS (Tier A, all 8 spots, unlimited repeats)
- **Child does:** taps a painted detail anywhere on screen. That patch of the painting moves — and it is *that* bird, *that* lantern, because the patch is cropped from the painting itself.
- **Reuses:** the tile-quadrant sampler above + `draw_texture_rect_region` (the backdrop's own draw call, `:75`); `_bop_burst_at(spot, false)` (`:1122`) for the sparkle; `m.chime` with `pitch_scale`.
- **Data:** `clue_spots(career)` + one new 104-row table (below) naming which of five motions each spot plays.
- **Art:** **none.**
- **The five motions** (all transforms of a redrawn patch, no assets):
  | motion | what it looks like | numbers |
  |---|---|---|
  | `flutter` | a bird/banner lifts and settles | translate −14 px, 3° wobble, 0.45 s |
  | `light` | a lantern/oven/lamp glows | additive warm radial over the patch, 0→0.55→0 alpha, 0.9 s |
  | `sway` | bunting, kelp, curtains | ±4° rotation, 2 cycles, 0.7 s |
  | `dart` | a fish/creature crosses | patch translates 40 px along its own band and back, 0.55 s |
  | `bulge` | anything solid — the default | 1.0 → 1.10 → 1.0, 0.45 s |
- **Rhythm:** every wander window and the arrival beat. **Not** during a task (the card owns input), **not** after the theft (stage tiles replace the district).
- **Worked example, chef** (real coordinates): six of the eight sit in the skyline band — `[0.42,0.095]` and `[0.483,0.10]` ceiling bunting → `sway`; `[0.728,0.12]` → `flutter`; `[0.073,0.185]` far-left prop → `bulge`; `[0.25,0.30]`, `[0.74,0.23]` → `light`. Two sit in the foreground counter — `[0.085,0.815]`, `[0.94,0.775]` fruit bowls / piping bags → `bulge`. **These two were previously covered by the audience row and are free for the first time because of this session's framing fix.**
- **Overlap guard:** the discovery layer sits *below* the actors in draw order, and step 3 of the input table means a tap landing on Roshan or an imp is never routed to a detail. Detective's `[0.42,0.40]` and `[0.125,0.48]` sit at her chest height on the walkway; both rules are needed there.

### T2 — SHE SAYS WHAT IT IS (near touch only)
- **Child does:** touches a detail while standing within 220 px. Roshan names it in 3–6 words: "A little bird!" / "The oven's warm!"
- **Reuses:** `m.show_msg("Roshan", …, "op_<career>_look_<i>")` → `AudioDirector._say` (`:13-38`), which tries `voices/roshan_op_<career>_look_<i>.ogg`, then falls back to `voices/roshan.ogg`, then to the pitched "yay". **So this ships silent-safe and the 104 lines can be recorded whenever.** `min_gap 0.5` prevents chatter.
- **Data:** the same 104-row table carries the line text; the `landmark` strings in `stations` are already written English and are the model for the writing voice.
- **Art:** none. VO optional and gracefully degrading.
- **Rhythm:** wander windows.

### T3 — SHE REACTS (Tier C, near touch only)
- **Child does:** nothing extra — she just happens to be close, and the world touch becomes a character beat.
- **Reuses:** `ActorMotion` only, until costumed sheets land: a 0.07 rad lean toward the spot, a 10 px hop, a 1.06 squash-settle, 0.5 s. **Deliberately not the existing `roshan_25d` gesture atlases** — the animation audit's §5 rejected-shortcuts list is right that a costume swap mid-act is a worse defect than stiffness, and `look`/`point`/`giggle` live on uncostumed sheets.
- **Data:** distance to `_hero_feet()`.
- **Art:** none now. **The additive ask** the animation audit already foreshadowed: `roshan_<career>_sheet_c.png`, 2048x1024, 4x2, 512 cells — row 0 LOOK/POINT, row 1 SIT/REST. 13 files, ~1.5 MB each. The layer ships and is fun without it; the sheets make it beautiful.
- **Rhythm:** wander windows.

### T4 — THE POCKET LENS (give every career the best mechanic in the suite)
- **Child does:** picks up a magnifying glass that hangs at the first station, drags it over the painting, and hidden sparkles reveal on a 0.45 s dwell. Drop it and it flies home.
- **Reuses:** the entire lens stack, unmodified — `_start_lens_phase` (`:1602`), `_lens_input` (`:1620`), `_tick_lens` (`:1640`, 96 px / 0.45 s), `_draw_lens_layer` (`:1668`) including the found-state glint and the dwell arc. The audit ranked this the single best interaction in the project for this age; it currently exists in 2 of 13 careers.
- **Data:** `clue_spots(career)` filtered to the spots not yet touched; the `phase_index * 3` rotation trick (`:1612`) already differentiates windows.
- **Art:** none — `magnifier.png` ships.
- **Modal by grab (important):** `lens_layer` STOPs input when visible, which would eat walk taps. So: tapping the lens icon arms it (`lens_layer` → STOP), tapping/dragging moves it, **1.5 s with no touch disarms it** and it tweens home (→ IGNORE). A 4-year-old understands "pick up the magnifying glass, put it down."
- **Rhythm:** available in every wander window from the first station onward, never during a task. Roshan's lens phases (detective) are untouched.

---

## 3. COLLECTING — the party favours

Chapter 2 canon (`CHAPTER2_PARTY_ROLES_2026-08-03.md`): every career makes one piece for a party that turns out to be **her own birthday**. The candy maker's function is literally *"one for every guest — and one for YOU, Sparkle."* Collecting should be **party favours**, and it should be persistent, because the game already has the right container.

### C1 — FAVOURS IN THE PAINTING
- **Child does:** finds small career-themed favours hidden at painted details and picks them up **by standing under them** — a far touch shows the sparkle, a near touch releases the favour.
- **Reuses:** `_bop_burst_at` for the pop; the gift-flies-to-Roshan tween from `opera_act.gd:1560-1563` verbatim; **the orbiting-sparkle draw at `_draw_combat_fx:1587-1599`** — the same code that makes a stolen sparkle circle an imp now circles *her*. **No HUD, no counter, no strip:** she has three because three sparkles are orbiting her. Zero chrome, which is the whole point of this session's framing work.
- **Data:** `clue_spots()` with a `favour: true` flag in the new table. Budget: **1 in the arrival beat + 1 per wander window + 1 at the workbench (X3)** = 5 on 7-phase careers, 4 on the 6-phase ones (boxer, racer, popstar).
- **Persistence:** `m.opera_pantry` — a `String -> int` dictionary that **already exists, already saves, already round-trips** (`main.gd:295`, `save_state.gd:132/207/465`, and `probe_load.gd:6` asserts it survives). `m.opera_pantry["favour_%s" % career_id] += 1` and a running `"party_favours"`.
- **Art:** none required — the favour is the painting's own patch, lifted out and shrunk to 34 px, exactly as T1 lifts it. (Optional later: 13 tiny 128² favour cards.)
- **Rhythm:** arrival + every wander window, all before the theft.
- **No-fail contract:** the count is **never shown as X of Y**. She has what she has. The pantry accumulates across careers *and across replays*, so a second visit adds more. Nothing is ever lost, nothing is ever counted at her.

### C2 — THE CURTAIN-CALL LAY-OUT
- **Child does:** watches. At `celebrate()` the orbiting favours fly off her one at a time and land in a row on the painted floor beside the returned goal prop, one bounce each, 0.12 s apart.
- **Reuses:** `celebrate()` (`:1235`) and its existing prop-comes-home bounce (`:1242-1250`); `_bounce_actor` (`:1189`).
- **Data:** the orbit list.
- **Art:** none.
- **Rhythm:** curtain call. If she found none, the act ends identically — just fewer sparkles. That is the whole difference.

### C3 — THE FAVOURS MATTER NEXT TIME (the precedent is already shipped)
- **Child does:** nothing — she notices. A later career's content changes because of what she found earlier.
- **Reuses:** the `gift` / `uses` chain that **already exists** in `opera_act.gd` — `m.opera_pantry[gift] += 1` at `:1558`, read at `:3219` where the farmers' carrots turn the chef's cake into a carrot cake and Roshan says so out loud. Point the same mechanism at favours.
- **Data:** `opera_pantry` + one `uses` key per career.
- **Art:** none.
- **Rhythm:** the opening VO of a later act, and the party table in the chapter's climax.

### C4 — THE ONE LEFT OVER (racer only)
- **Child does:** finishes the racer act with one favour still in her hand.
- **Reuses:** dialogue only.
- **Data:** a one-career flag.
- **Art:** none.
- **Rhythm:** curtain call of the racer act. This is `CHAPTER2_PARTY_ROLES` GAP B — the invitation she keeps for the door nobody knocks on, which she hands the Imp Captain at the climax. It converts the chapter's thesis from a surprise into a five-act promise, and it costs one line of text.

---

## 4. QUIET BEATS

What makes stillness rewarding at four: **something changes slowly, and it changes because she stopped.** Every quiet beat below is exitable by one touch and rewards nothing, scores nothing and times nothing.

### Q1 — SIT AND WATCH
- **Child does:** walks to a spot and stays. After 1.2 s of no input she sits down, and the world runs one long ambient event she could not have produced by tapping: five lanterns light in sequence along the promenade; a shoal drifts across the skyline; the mirror ball turns.
- **Reuses:** the T1 patch machinery, chained — 5 patch `light`/`dart` events at 0.5 s intervals along `point_along()`; `ActorMotion` for the sit (12 px drop, 1.04 squash) until `sheet_c` row 1 lands; `_tick_ambience_duck` (`main.gd` → `AudioDirector`) to duck the music 3 dB while she sits.
- **Data:** `clue_spots` + `path_points`.
- **Art:** none now; `sheet_c` SIT row makes it land properly.
- **Rhythm:** offered in the **third** wander window (the longest one). Ends on its own after ~6 s, or instantly on any touch.

### Q2 — THE LISTENING SPOT
- **Child does:** touches one spot per career that holds a *sound* rather than a picture — the oven crackling, the sea under the pier, the empty house applauding.
- **Reuses:** `_set_ambience` + the duck; and the `_fanfare()` trick of pitch-scaling one `chime` player three times (`audio_director.gd:127-142`) — a 5-note career melody costs nothing.
- **Data:** one flagged clue spot per career.
- **Art:** none. **The one place I would spend audio:** 13 × 2–3 s ambient loops. Ships without them on the chime melody.
- **Rhythm:** any wander window.

### Q3 — BREATHING ROOM (the empty beat, and the cheapest win here)
- **Child does:** nothing at all for 2.5 s after finishing a job — and the thing she just made is still on screen while she does it.
- **Reuses:** the completion hold already added this session at `:1103-1112`; extend it from 0.9 s to 2.5 s with a slow bob on the finished widget, then fade the card. **Delete the blank 1.0 s `phase_gap` at `:684`** — the wander window replaces it, so the pause becomes playable instead of dead.
- **Data:** none.
- **Art:** none.
- **Rhythm:** after every non-combat task. The empty beat is only rewarding if her own work is visible during it; that is the entire trick.

### Q4 — THE HELD SHOT AT THE THEFT
- **Child does:** watches the captain haul the cake off.
- **Reuses:** the theft-flee tween (`:737-743`) — the best diegetic beat in the file — plus a 1.5 s hold before the chase arms, with the music dropped out.
- **Data:** `steal_index`.
- **Art:** none.
- **Rhythm:** between beat 3 and the chase. Slowness earns the fast beat that follows.

---

## 5. THE HELPERS

`rival_actor` already exists as a second stage actor with `_place_on_stage`, depth, bounce and a nursery override to `faron_nursery.png` (`:385-390`), and is hidden outside the finale. The helper is the same slot, used the other way round. Cast per career is already assigned in `CHAPTER2_PARTY_ROLES_2026-08-03.md` §2, and `AudioDirector._speaker_key` (`:95-113`) already routes every one of these names to a voice: chef→**Kareem** (`shop`), candymaker→**Sparkle**, painter→**Flower Friend**, ballerina→**Rosalina**, magician→**Evie + Lamba** (`evie`), detective→**Huluu**, farmer→**Chuck**, astronaut→**Mewsha**, racer→**Harper & Fiona** (`harper`), popstar→**Daddy**, boxer→**Wacky**, nursery→**Faron**, doctor→**Evie**.

Portraits that exist today in `assets/characters/friends/`: `daddy.webp`, `huluu.png`, `mama_baby.png` (Evie/Faron), `flower_friend.png`, `wacky_chuck.png` (Wacky + Chuck), `two_friends.png` (Harper & Fiona), `kareem.png`, `pearl_friend.png`. **Missing: Sparkle, Mewsha, Rosalina, Lamba** — 4 cards, or those careers simply get no walking helper.

### H1 — SHE IS NOT ALONE IN THE PAINTING
- **Child does:** notices a friend walking the promenade behind her, keeping up, stopping when she stops.
- **Reuses:** `_actor()` (`:508`), `_place_on_stage` (`:521`), `_stage_feet_at_x` (`:1337`), `StagePaths.roam_range()` (`:178`) so the helper obeys the same walkable envelope the crew imps got this session. Follow at 0.8× her speed with a 140 px trailing offset; idle bob from `_apply_imp_pose`'s default case (`:1404`).
- **Data:** a new `HELPER` table (career → id, portrait, display name); `ROAM`.
- **Art:** 8 of 13 exist today; 4 new portrait cards for full coverage; nursery already has `faron_nursery.png`.
- **Rhythm:** present from the arrival beat through the last wander window, and again at the curtain call. Off during BOP (he steps back) — the fight is hers.
- **Scale note:** hold him to the same contract as the crew — Roshan ~1.3× a helper, never >1.5× (owner rule, 2026-08-03). `helper.size = Vector2(190, 190)`, the rival's existing number.

### H2 — SHOW ME (a hint you ask a person for, not a system)
- **Child does:** taps the helper. He bounces and says one line naming the nearest undiscovered detail — "Look UP at the flags!" — and a gold twinkle fires there for 1.2 s.
- **Reuses:** `_bounce_actor` (`:1189`); `m.show_msg(<helper>, …, "op_<career>_show")` with the `_say` fallback chain; `affordance_layer` twinkle.
- **Data:** `clue_spots` + the `landmark` strings, which are already vivid English ("gold etagere tower displaying yellow, pink, and purple cakes").
- **Art:** none.
- **Rhythm:** always available in wander. **This is the pull-back ladder turned into a character** — the child asks a friend instead of being nagged by a system, which is the difference between help and correction.

### H3 — CARRY IT TOGETHER
- **Child does:** finds a favour far from where she is standing; the helper fetches it, walks it over, and hands it to her.
- **Reuses:** the flight tween from `opera_act.gd:1546-1563`, then the helper's own walk, then `_bounce_actor` on both.
- **Data:** distance from `_hero_feet()` > 300 px.
- **Art:** none.
- **Rhythm:** wander windows. Turns a long distance from a chore into a two-character scene.

### H4 — SIT WITH ME
- **Child does:** sits (Q1) within 200 px of the helper. He sits too. They both watch the ambient event. Nothing happens. Nothing is asked.
- **Reuses:** Q1 + the helper's `ActorMotion`.
- **Data:** proximity.
- **Art:** none now; `sheet_c` SIT row for her, the static card for him.
- **Rhythm:** third wander window. **This is the beat the owner is actually asking for** — the slow, contemplative register, made out of two existing TextureRects and a timer.

### H5 — THE HELPER'S WISH
- **Child does:** hears, at the curtain call, why the thing she made matters to *that* friend: "Save me a slice, Roshan!" / "One for every guest — and one for YOU, Sparkle."
- **Reuses:** `celebrate()` + `show_msg` + one bounce.
- **Data:** the **function lines are already written**, one per career, in `CHAPTER2_PARTY_ROLES_2026-08-03.md` §2.
- **Art:** none. 13 VO lines, optional.
- **Rhythm:** curtain call, immediately after C2's lay-out.

---

## 6. MY ADDITIONS

### X1 — THE WORLD REMEMBERS
- **Child does:** nothing. Every detail she has touched keeps a faint permanent glint. By the finale the painting is dotted with the places she went.
- **Reuses:** the found-state draw at `_draw_lens_layer:1672-1674`, verbatim, moved to `discovery_layer`.
- **Data:** a `touched: Array[bool]` beside `lens_found`.
- **Art:** none.
- **Rhythm:** accumulates all act; visible at the theft and again if she returns. It makes the curtain call a map of her own afternoon, which is the cheapest emotional payoff in this document.

### X2 — PEEKABOO IMPS (wander is not dead air for the child who wants to *do*)
- **Child does:** spots a single imp popping out of a painted landmark every ~12 s, waving, ducking back. Tapping it: kind fizzle, giggle, it drops a favour and runs.
- **Reuses:** `_spawn_stage_imp` (`:837`) **without a brain** — no `ImpAI`, no windup, no contact, no combat state; `_apply_imp_pose`'s `taunt`/`flee` cases (`:1394-1402`) which already read as playful; `imp_mischief_taunt.png` and `imp_mischief_flee.png`, both shipped; `_bop_burst_at(pos, true)`.
- **Data:** `roam_range(career)` for where it may appear; `station_list` for which landmark it hides behind.
- **Art:** none.
- **Rhythm:** one per wander window, max. It keeps the slow beats from feeling empty to a fast child, and it plants the imps as present-and-playful **before** the theft, which makes the theft a betrayal instead of a random event.

### X3 — THE PROP HAS A HOME, AND SHE MEETS IT FIRST
- **Child does:** walks to the goal prop before the theft and touches it. It bobs; she says what it is for — "This cake is for… someone special." One favour lives here.
- **Reuses:** `prop_rect` (`:397-407`), which is already visible from phase 1 until the theft (`:745-746`); the celebrate bob (`:1248-1250`).
- **Data:** a new `workbench` point per career in `PATHS` — **the framing audit already asked for this** (§16); today `prop_rect.position` is a hardcoded `Vector2(890, 330)` for all 13 careers, landing on whatever the painting happens to have there. For chef the workbench is `grand_cake_stage` `[0.86, 0.545]`.
- **Art:** none.
- **Rhythm:** arrival beat and the first two wander windows. Meeting the thing before it is stolen is what makes the theft land at all.

---

## 7. RHYTHM — a concrete act timeline

Chef, 7 phases, `steal_index = 4`, `FINALE_START = 5`. Median 4-year-old.

| # | Beat | Register | Budget | What's live |
|---|---|---|---:|---|
| 1 | **Arrival** — world fades up, she stands at t=0.08, Kareem walks in behind her, three details twinkle in turn, nothing is asked | slow | **12 s** | W1 W3 T1 T2 T3 C1 H1 H2 X3 |
| 2 | IMPS! scuffle — crew **5→3**, they do not engage until she is within 300 px | fast | 8 s | combat |
| 3 | **Wander → mixing_bowl** | slow | **7 s** | + T4 pocket lens, X2 |
| 4 | POUR (goal 5.0 → **3.8**) | fast | 8 s | card |
| 5 | **Breathing room** on the poured bowl | slow | **2.5 s** | Q3 |
| 6 | **Wander → hearth_oven** | slow | **6 s** | full wander set |
| 7 | STIR (4.0 → **3.0**) | fast | 8 s | card |
| 8 | **Breathing room** | slow | **2.5 s** | Q3 |
| 9 | **Wander → cake_tower** — the long one; Sit-and-Watch offered here | slow | **8 s** | + Q1 Q2 H4 |
| 10 | BAKE (6.0 → **4.5**) | fast | 8 s | card |
| 11 | **THE THEFT** — held shot, music out | slow | **2 s** | Q4 |
| 12 | CAKE CHASE — crew **8→6** + captain (his 2 bops stay reserved) | fast | 16 s | combat |
| 13 | Curtain-rise sting (existing, any touch skips) | slow | 2.6 s | — |
| 14 | PIPE (7.0 → **5.6**) on stage | fast | 10 s | card |
| 15 | **Breathing room** | slow | **2 s** | Q3 |
| 16 | TOP (8.0 → **6.4**) | fast | 10 s | card |
| 17 | **Curtain call** — confetti, favours lay out, helper's wish, free walk stays live | slow | **11 s** | W1 C2 H5 |
| | **TOTAL** | | **≈ 124 s (2:04)** | |

**Self-paced share: 55.6 s of 123.6 s = 45%**, against ~4% today (three 1.3 s glides). The act is 14 s longer than today's ~109 s and *feels* like a different medium.

**What shortens to pay for it**
- Opening crew 5→3 (−3 s) and chase crew 8→6 (−7 s), both already recommended by the pacing audit.
- Every non-combat `goal` in `PHASES` (`:36-151`) down 20–25%: chef POUR 5.0→3.8, STIR 4.0→3.0, BAKE 6.0→4.5, PIPE 7.0→5.6, TOP 8.0→6.4.
- The blank 1.0 s `phase_gap` (`:684`) deleted outright — replaced by Q3, which is visible instead of empty.
- The five 1.3 s auto-glides (`:707`) disappear entirely (−6.5 s) and become walking she controls.
- Nothing is cut from the finale's *shape*; the 2.6 s curtain sting stays — it is the act's one earned held breath.

**6-phase careers (boxer, racer, popstar)** have `steal_index = 3`, so they get arrival + 2 wander windows, 4 favours, and land at ≈ 112 s. That is correct, not a defect: those three are the loud careers.

**Levers if 2:04 is too long:** chase 16→13, arrival 12→10, curtain call 11→9 → **116 s**. Do not cut the wander windows; they are the feature.

**Probe impact (say this in the commit or it reads as a regression):** `probe_opera_2d_balance.gd` pumps gestures and never wanders, so its measured time *drops* to roughly 85–100 s — still inside `BAND_LO 70` / `BAND_HI 150`, and the band's own note already concedes it excludes explore time.

---

## 8. NEW DATA — all of it in `opera_stage_paths.gd`, none of it art

| Table | Shape | Rows | Notes |
|---|---|---|---|
| `DETAILS` | career → 8 × `{motion, say, favour}` | 104 | `motion` ∈ flutter/light/sway/dart/bulge; `say` is 3–6 words; the `landmark` strings are the writing model |
| `WORKBENCH` | career → `[x, y]` | 13 | the framing audit's §16 ask; kills the hardcoded `Vector2(890, 330)` |
| `HELPER` | career → `{id, portrait, name}` | 13 | cast already fixed by `CHAPTER2_PARTY_ROLES` §2; `_speaker_key` already routes all 13 |
| `FAVOUR` | career → `{label, pantry_key, uses}` | 13 | `uses` reads `opera_pantry` exactly like the shipped carrot-cake beat |
| `PATHS["nursery"]` | 9 waypoints + 5 stations + 8 clue spots | 1 | **the only real data gap**; derive from `world_nursery_c*r*.png` |

---

## 9. ART LEDGER

**Needs nothing:** W1 W2 W3 · T1 T2 T4 · C1 C2 C3 C4 · Q1 Q2 Q3 Q4 · H2 H3 H5 · X1 X2 X3. That is 19 of 22 tasks.

**Reuses shipped assets:** `magnifier.png`, `station_marker.png`, `fx_bop_puff/dust_puff/stolen_sparkle/telegraph_ring/dizzy_stars`, `imp_mischief_taunt/flee.png`, `goal_<career>.png`, 8 friend portraits, all 52 `world_<career>_c*r*.png` tiles.

**Genuinely new, in priority order:**
1. **4 helper portrait cards** — Sparkle, Mewsha, Rosalina, Lamba. Without them, 4 careers ship with no walking helper (acceptable, not ideal).
2. **`roshan_<career>_sheet_c.png`** — 2048x1024, 4x2, 512 cells; row 0 LOOK/POINT, row 1 SIT/REST. 13 files, ~20 MB. **This is the exact additive request the animation audit predicted** ("if the slow-exploration direction lands, add a sheet_c"). T3 and Q1 ship without it on `ActorMotion` transforms and get visibly better with it. Same content locks: no legs, costume continuity absolute, tail-tip contact row 500 ±2.
3. **13 ambient loops, 2–3 s** for Q2. Chime-melody fallback exists.
4. **~130 short VO lines** (104 detail names + 13 show-me + 13 wishes). All optional — `_say` falls back to the speaker's generic clip, then to the pitched "yay".

---

## 10. BUILD ORDER

1. **`ActorMotion` three-node stack** (`player_actor → ActorMotion → ActorSprite`) with the always-alive breath. It also fixes a live bug: `_bounce_actor` (`:1189`) captures `home_y` and restores a stale value if a glide tween is running on the same property.
2. **W1 walk integrator + `wander_layer` input** with the 6-step hit-test order; keep `_glide_roshan_to` as the assist path only.
3. **Split `_show_phase()` into `_arm_phase()` / `_open_task()`** with the 150 px / 0.35 s dwell; delete `phase_gap`; add the probe auto-open guard.
4. **T1 tile-quadrant patch sampler** (the seam-clipping helper) on all 8 spots, then T2, then T3.
5. **C1/C2 favours** on `opera_pantry` + the orbiting-sparkle draw.
6. **H1/H2 helper** — the biggest emotional return per line of code after W1.
7. **Q1–Q4**, then **X1–X3**.
8. **Retune goals and crew counts** per §7; re-run `probe_opera_2d`, `probe_opera_nursery`, `probe_opera_2d_balance`, `probe_load` and report the new sim band.

**Net new engine code:** roughly one 140-line `wander_layer` (input routing + affordances), a 60-line patch sampler, a 40-line walk integrator, a 70-line helper follower, and the `_show_phase` split. Everything else is table data and wiring.

**Risks, and how each is bounded**
- *Lost* — impossible by construction: one dimension of freedom (`_stage_feet_at_x` clamps to the route), exactly one station lit at a time, no off-path, no off-screen.
- *Bored* — the pull-back ladder plus H2 (ask a friend) plus X2 (something to bop).
- *Input collision* — the hit-test order above, plus the lens's modal-by-grab rule, plus actor-forefront priority.
- *Exploration delaying the ending* — the curtain call's win callback fires on a timer, never on her position.
- *Regression in the fast careers* — 6-phase careers get 2 wander windows, not 3; they stay ~112 s.

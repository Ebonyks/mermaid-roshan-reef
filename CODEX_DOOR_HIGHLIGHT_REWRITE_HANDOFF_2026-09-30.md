# Codex handoff — castle door highlighting rewrite (Door Guidance v2)

Status: `SUPPORTING_CURRENT` implementation work order, 2026-09-30. Owner
request: *"The door highlighting mechanics are weak. Rewrite this, making a
handoff for codex."* Prepared by a Claude Code session for Codex. Baseline:
`origin/dev` `e7899cc095fc326ff007e30226ad7bafea8f1634`. Every file:line
below was verified at that commit.

Authority: subordinate to [the design language](design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md),
the [master audit](audit/MASTER_AUDIT_2026-08-09.md) repair and satisfaction
protocol, and the [stage pathfinding protocol](audit/stage_pathfinding/STAGE_PATHFINDING_PROTOCOL.md).
[`design/07_CASTLE_DOOR_LANGUAGE.md`](design/07_CASTLE_DOOR_LANGUAGE.md)
remains the binding door language until WP-D8 rewrites it to match the shipped
runtime. This handoff proposes; it grants no visual, device, child, or owner
acceptance. Report implementation, machine verification, and outstanding
acceptance separately (`DL-AUTH-05`, `DL-AUTH-06`, `DL-AUTH-07`).

Review evidence (diagnostic PIL composites, **not** runtime evidence under
`DL-QA-03`): [`audit/door_highlight_rewrite_2026-09-30/`](audit/door_highlight_rewrite_2026-09-30/measured_door_geometry.json).
Both scripts there are deterministic and re-runnable from the repo root.

---

## 0. Summary

**What the child sees today.** At phone-glance size the one "golden rainbow
door" is indistinguishable from the doors that are resting
([squint pair](audit/door_highlight_rewrite_2026-09-30/squint_quarter_scale_current_vs_concept.jpg), left half).
The plot cue is a 2.5 px gold line drawn over a cream-and-gold painted frame.
The biggest, prettiest door on the Day One screen is the inert dormant
Moonflower card. In free play a waiting Royal Hall story event is completely
off-screen with nothing pointing at it. The resting doors move more than the
plot door does.

**What to build.** One arbiter chooses at most one highlighted door. That door
gets a lit golden doorway, a soft gold halo with a travelling rainbow, and a
guide star. When the door is off-screen, the star docks in an edge beacon that
you can tap. Every other door is static and calm, and moves only when tapped.
The highlight visibly travels to the next door when a beat completes. Every
guidance moment speaks a line that matches what is on screen. All visuals live
in world space on the door plane, are fitted to measured painted geometry, draw
beneath Roshan, and allocate nothing per frame.

---

## 1. Verified defects (dev `e7899cc0`)

| # | Defect | Evidence | Child impact | Rules |
|---|---|---|---|---|
| D1 | The plot highlight is too faint to read: a 2.5 px inner gold line, a 5–7 px outer line at α 0.18–0.34, six 1.5 px rainbow hairlines at α 0.28, and an 8.5 px star | `scripts/castle_door_cue.gd:120-151` (`band_width` at :135, `star_radius` at :145). Quarter-scale measurement of the current composite: the plot opening is only ~10 luma brighter than the resting openings, and just as cool (mean R − B ≈ −43 for all four) | At the quarter-scale squint the target door looks like every other door | `DL-READ-02`, `DL-READ-03`, `DL-AGE-01` |
| D2 | The gold outline sits on a cream/gold painted frame, so the only visible gold is where the line strays onto the wall | Hall master; [current composite](audit/door_highlight_rewrite_2026-09-30/current_day_one_bubble_bath_entry.jpg) | The cue reads as a stray scratch rather than a promise | `DL-READ-01`, `DL-VIS-04` |
| D3 | Cue geometry is not fitted to the door. `_arch_points()` fits a generic ellipse into the `HALL_PORTALS` hotspot rect, which overhangs every standard painted frame by 15–21 art units on the right. The star lands on the room sign | `castle_door_cue.gd:158-174`; `scripts/arena/castle_rooms_25d.gd:159` (rects); [overlay](audit/door_highlight_rewrite_2026-09-30/measured_door_geometry_overlay.jpg) (yellow rect vs painted frame) | The outline floats off the door on one side and cuts across the sign | `DL-INT-04`, `DL-READ-06` |
| D4 | No off-screen pointer. In free play Roshan spawns at x 380 with the camera at 0, while a Royal Hall event door sits at x 2870+. In Day One the plot door leaves the screen as soon as the child walks away. A search of dev found no edge or off-screen pointer anywhere; the only edge-aware code, `scripts/opera_world_hotspot_2d.gd:119` `_reframe_to_stage`, keeps a hotspot halo on stage and is a useful reference | `castle_rooms_25d.gd:2849` (`_center_player`), `:5224-5284` (a cue is hidden when off-canvas); [free-play composite](audit/door_highlight_rewrite_2026-09-30/current_free_play_royal_event_entry.jpg) | "Follow the golden door" when no golden door is visible | `DL-AGE-01`, `DL-READ-06`, `DL-SND-13` |
| D5 | Resting doors are louder than the plot door. Each draws a full-rect navy veil plus five drifting fog ellipses, redrawn every frame, on up to eight doors | `castle_door_cue.gd:67-107` (`draw_rect` of the whole rect at :87) | Motion attracts the eye to the wrong doors, and the rectangles read as debug boxes | `DL-READ-03`, `DL-MOT-03` |
| D6 | The cue draws above Roshan: it lives in a stage `Control` layer at z 25 while the world root sits at z −1000 | `castle_rooms_25d.gd:1307`, `:1371` | Veil, fog and lines paint over Roshan at the door foot | `DL-READ-05`, `DL-LAY-01` |
| D7 | Each frame the cue is re-fitted to the clipped on-screen rect instead of being clipped | `castle_rooms_25d.gd:5257-5262` | The arch squashes and slides at the screen edge while scrolling | `DL-INT-04` |
| D8 | Two gold doors are possible. The Moonflower cue is hard-set to PLOT and never consults `active_door_highlight_id()`, so it can coexist with a Royal Hall PLOT in free play | `scripts/arena/fairy_conservatory_door_2d.gd:188`, `:250` | Breaks the owner's "at most one highlighted door" promise | `design/07` rule; `DL-READ-03` |
| D9 | The Royal Hall has two resting vocabularies. Its authored mist follows `_royal_hall_event_id()`, while its cue follows `door_state()`. In Day One the mist is hidden (built-in events are non-empty) and the procedural veil shows; in free play both stack | `castle_rooms_25d.gd:3047-3101` | The same "resting" meaning looks different on different days | `DL-READ-03`, `DL-CODE-05` |
| D10 | The dormant Moonflower card is the largest, brightest door in most Day One views, yet it has no resting treatment and no tap feedback (a tap just walks) | `fairy_conservatory_door_2d.gd:227-250` (hotspot only when revealed); [Day One composite](audit/door_highlight_rewrite_2026-09-30/current_day_one_bubble_bath_entry.jpg) | A child's first tap goes to a silent door | `DL-AGE-03`, `DL-AGE-07` |
| D11 | Voice and screen disagree. "A new picture door is glowing!" plays inside the room, where no door is visible. "Back to the hall, then follow the glowing door!" is caption-only, because the clip played is "All clean! The floor is twinkling!". The free-play `castle_home` clip still mentions the removed shell elevator. No line names the destination while travelling. Missing non-required keys fall back to a pitched "yay" | `scripts/main.gd:6703-6710`, `:7138-7142`, `:6134-6140`; `scripts/audio_director.gd:314-318` | A non-reader never hears the instruction, and can hear a success sound on a refusal | `DL-SND-01`, `DL-SND-13`, `DL-AGE-01` |
| D12 | The return from a room re-spawns 600 units left of the *next* door instead of restoring the exit door, and the highlight's move to the next door is never seen | `castle_rooms_25d.gd:1729-1739`, `:2849-2866`, `:2879-2900` | The protocol requires "restore the exact source … camera coordinate"; the child loses continuity | Protocol; `DL-MOT-06` |
| D13 | Per-frame cost: every visible cue runs `queue_redraw()` from `_process`, and `_arch_points()` allocates a `PackedVector2Array` on every draw | `castle_door_cue.gd:67-70`, `:146`, `:166` | CPU and overdraw budget spent on static meaning | `DL-CODE-07`, `DL-CODE-08`, `DL-PERF-03` |

Already fixed on dev, so keep it: Day One courtyard entry snaps the camera
so the plot door starts on screen (`_day_one_hall_spawn_foot`). Exact clips
also exist for the Day One arrival, resting, and new-door lines (§3.6).

---

## 2. Invariants that do not change

- There are four promises: Blocked ("resting"), Open, Bonus, Plot. At most one
  Plot/Bonus door exists at a time, and it is chosen by a sequencer, never by a
  room lighting itself (`design/07`).
- Gold/rainbow means Plot and ruby means Bonus (owner-corrected 2026-08-26).
  See OD-1 for the conflict with prop affordances.
- `DayOneDirector` owns progression and save restore. `CastleDoorLanguage`
  remains the single state resolver, extended in WP-D2. During Day One the
  kitchen is optional Open (`scripts/main.gd:330`).
- Spoken vocabulary that is already recorded and must stay true on screen:
  *golden rainbow door*, *foggy doors are resting*, *that door is napping*,
  *a new picture door is glowing*, *big door, please glow*, *the mist is
  sleepy*.
- Travel follows the protocol: a tap or drag on a door or its proxy leads to
  approach, arrival, then transition. Releasing over the floor commits movement
  only, so there is no doorstep auto-enter. Blocked doors stay tappable and
  answer kindly, without progress mutation.
- No new save keys. The last-shown highlight is runtime-only.
- True 2D Canvas and the Mobile renderer. No 3D, no 3D lights, no new
  spatial debt. Approved art is never modified, and derived masks go to new
  paths.

---

## 3. Door Guidance v2 specification

### 3.1 Guarantees

| ID | Guarantee (each maps to AC in §6) |
|---|---|
| G1 | One highlight. At most one Plot/Bonus door across the hall doors, the Royal Hall and the Moonflower gate, decided by one arbiter (§3.5). |
| G2 | Always findable. Within 2 rendered frames of any hall state with a highlight, either the highlighted frame is ≥ 35% on the 1280×720 stage, or exactly one edge beacon on its side is visible. Hysteresis: dock at < 35%, re-anchor at ≥ 55%. |
| G3 | Unmistakable. In a quarter-scale capture, the highlighted opening has the highest mean luma of all door openings on screen by ≥ 25/255, and it is the only warm opening (mean R − B > 30; resting and open openings < 0). Calibration on the review composites: today Δ ≈ 10 with R − B ≈ −43 (fails); the concept gives Δ ≈ 51 with R − B ≈ +70 against −36 (passes). |
| G4 | Quiet elsewhere. Resting and Open doors have no `_process`, no redraw, and no animated property at rest. Only the highlighted door and the guide star animate. Tap feedback lasts ≤ 0.8 s. |
| G5 | On the door, under Roshan. Door visuals are world-space Canvas nodes on the door plane. They scroll with the art and are clipped, never re-fitted, by the viewport. Signs, mist, Roshan and her shadow render above them. |
| G6 | Fits the painted doorway. Light stays inside the painted opening and the halo starts at the painted frame edge, with ≤ 2 stage px deviation in overlays and captures. |
| G7 | Spoken and truthful. Every guidance moment plays an exact clip whose words match the screen. While a clip is pending, its caption shows with no audio; it never resolves to `talk`, `win`, `yay`, or another line. |
| G8 | Protocol travel. Door, beacon, tap and drag all converge on one idempotent travel request. A floor release only moves Roshan. The return from a room restores the exit door (OD-3). |
| G9 | Cheap. Zero per-frame allocation in cue, guide and tick paths. Resting geometry is built once per hall build. Speedy tier drops the shimmer and threshold pool. Measured transparent overdraw ≤ today's. |

### 3.2 State treatments

Colours are Godot `Color()` values in the same space as the existing cue
constants, with sizes at the 1280×720 stage scale. Treat them as starting
values: tune within ±25% during capture review (OD-6), never beyond without
owner review.

Strength comes from luminance, size, fitted geometry and findability, not from
speed. Keep the owner's restrained timing: `PLOT_PERIOD_SECONDS` 3.2,
`PLOT_SHIMMER_PERIOD_SECONDS` 4.6 and `BONUS_PERIOD_SECONDS` 4.4 stay, so the
timing floors in `probe_castle_door_language.gd` remain valid.

| State | Painted opening | Around the frame | Motion at rest | On tap |
|---|---|---|---|---|
| **Plot** — "golden rainbow door" | Warm light fills the measured opening: vertical gradient `(1.00, 0.75, 0.27)` α 0.47 at the apex to `(1.00, 0.93, 0.67)` α 0.84 at the threshold. The corridor detail stays faintly visible | A 16 px soft halo `(1.00, 0.80, 0.33)` outside the frame and crest silhouette, α 0.85 at the frame edge falling to 0. A six-band segment of the existing `RAINBOW` colours (≈30% of the halo length) travels once around the halo every 4.6 s. A warm threshold pool 160×28 px at the door foot. Guide star 30 px above the room sign | Light and halo breathe ×0.88–1.0 every 3.2 s; the star bobs 6 px every 1.6 s | Light flares +0.15 α for 0.3 s and the star spins into the doorway, then the existing walk-and-enter route runs |
| **Bonus** — ruby door (only when nominated and no Plot exists) | Rose `(1.00, 0.62, 0.58)` α 0.28 to `(1.00, 0.80, 0.76)` α 0.50 | A 10 px ruby halo `(0.96, 0.34, 0.39)`; no rainbow, star, beacon or particles | Breathes once every 4.4 s (owner period) | Same as Plot, without the star |
| **Resting** — "foggy / napping door" | Static cool haze `(0.59, 0.56, 0.75)` α 0.36 to `(0.73, 0.71, 0.86)` α 0.50; the painted depth stays readable but flat | Static fog bank: five soft lavender-grey `(0.77, 0.75, 0.89)` α 0.59 puffs along the threshold. Nothing outside the doorway, and no rectangle | None (built once) | Puffs billow (scale 1.0 → 1.18 → 1.0, 8 px drift, 0.7 s) and the haze rises +0.12 α. The existing curtain swish plays, then the exact resting line (§3.6). The guide star pings toward the real destination |
| **Open** | Authored art only | Nothing | None | Existing walk-and-enter |

Special cases:

- **Royal Hall, resting**: the five authored mist cards *are* the treatment.
  Draw no procedural haze or fog there. The mist is visible exactly when
  `door_state(ROYAL_HALL_ID) == BLOCKED`, not when `_royal_hall_event_id()` is
  empty. **Royal Hall, Plot**: light only the deep-blue corridor between the
  curtains, and give the stairs the threshold pool.
- **Moonflower dormant card**: resting treatment is the fog bank plus tap
  feedback. Its closed painted doors take no haze. **Revealed gate**: Plot
  visuals come from the same cue, fitted to its card art, and only when the
  arbiter chooses it.
- The Day One grime dressing stays grime-only (`independent_door_glows:
  false`).

Target look: compare [current](audit/door_highlight_rewrite_2026-09-30/current_day_one_bubble_bath_entry.jpg)
with [concept](audit/door_highlight_rewrite_2026-09-30/concept_day_one_bubble_bath_entry.jpg).

### 3.3 Guide star and edge beacon

- Exactly one guide star exists while a highlight exists in the visible hall,
  and in a Day One room while an exit handoff is pending (M5). It is the
  castle's only moving pointer (`DL-READ-06`, `DL-CODE-05`). Build it once and
  reuse it rather than cloning another pointer glyph (`MA-CODE-003`).
- **Anchored**: while the door is ≥ 55% visible (hysteresis in G2), the star
  sits 30 px above the room sign, or above the crest for the Royal Hall and the
  Moonflower gate. Its position comes from the door's world anchor through the
  existing world-to-stage transform. The star (≤ 215 px) never overlaps
  Roshan's head (≥ 334 px on the walk lane).
- **Docked**: while the door is < 35% visible, the star docks in an edge beacon
  on the door's side. Centre x is 92 or 1188 and y is 300 (clamped 180–420; the
  global Back control occupies 18–130 top-left). The badge is a 50 px cream
  shell with a 5 px plum keyline and a 5 px gold ring. Inside it shows the
  destination's own room-sign picture; the Royal Hall and the Moonflower gate
  show the star instead. A small star sits on the badge rim, and a gold chevron
  points toward the door and nudges 8 px every 0.9 s. The hit area is 128×128
  (`DL-UI-03`). See the
  [concept](audit/door_highlight_rewrite_2026-09-30/concept_day_one_wandered_left.jpg).
- **A beacon tap is a door tap**: it calls the same
  `_enter_hall_portal(portal_id, foot)` route (walk, arrival, transition). The
  star rides ahead and re-anchors once the door is on screen.
- Moves between anchored, docked and Back-control positions tween over 0.35 s.
  A visible star never teleports.
- Bonus gets no beacon by default (OD-4).

### 3.4 Moments

| Moment | Visual | Voice (§3.6) | Rules |
|---|---|---|---|
| M1 Day One hall arrival from the courtyard | Keep the dev spawn and camera snap. The star pops from Roshan and flies in a 0.9 s arc to the door or beacon; the doorway light fades in over 0.4 s | `day1_arrival_castle` (existing, once per session) | `DL-AGE-01` |
| M2 Free-play hall arrival with a highlight | Spawn unchanged; the star flies from Roshan to the door or beacon | `castle_route_follow_star` (new) | Never the stale `castle_home` clip |
| M3 Blocked tap, including the dormant Moonflower card | Billow, haze flash and star ping; no travel, no progress | `castle_door_resting` (Day One), `castle_mist_resting` (Royal Hall), `castle_door_resting_free_play` (new) | Keep `BLOCKED_DOOR_SFX_COOLDOWN_SECONDS`. Remove the dev second-tap gate so every blocked tap pings |
| M4 Plot door or beacon tap, then travel | Light flare; the star spins into the doorway; Roshan walks; arrival enters | `castle_route_to_<destination>` (new) at travel start | Protocol travel cue |
| M5 Day One room complete, pending exit | The star appears beside the global Back control and bobs, with a soft gold ring behind the control (drawn by the guide; the control itself is not restyled) | `day_one_room_clean` or `day_one_pool_ready` (existing), then `castle_route_back_to_hall` (new). The caption must match the spoken line | Move the in-room `day_one_new_door` and `day_one_all_rooms_clean` calls to M6 |
| M6 Hall return after a beat (transfer) | Roshan appears at the exit door foot with the camera centred on her. The completed door twinkles (≤ 12 pooled sparkles, 0.8 s). The star flies 0.9 s to the new door, whose light fades in over 0.4 s, followed by one fast rainbow sweep | `day_one_new_door`, or `day_one_all_rooms_clean` for the Royal Hall, starting as the new door lights | Any tap completes the transfer at once; it plays once per change |
| M7 Idle in the hall with a highlight | At 8 s the star calls (a doubled bob for 1.2 s and a soft chime). At 20 s it re-flies from Roshan to the target. Any touch resets the timer | At 20 s: `castle_home_day_one` (Day One) or `castle_route_follow_star` (free play); at most two voiced reminders per visit | `DL-AGE-04`: zero input never travels or enters |
| M8 Moonflower reveal | The reveal line plays only when the arbiter chooses the gate | `castle_fairy_open` (existing) | G7 |

For every Day One beat, M6 needs no camera override. With the camera centred on
Roshan at the exit door, the next door is on screen: bath to pool 100%, pool to
playroom 100%, playroom to craft 100%, craft to Royal Hall 52% (stage 1280 /
view 1672 art units).

### 3.5 Arbitration

Add one pure function to `CastleDoorLanguage`, for example
`static func arbitrate(context: Dictionary) -> Dictionary`, returning `{}` or
`{"id": String, "kind": PLOT|BONUS}`. Every consumer reads it: hall cues, the
star and beacon, the Royal Hall mist, the Moonflower gate, blocked feedback,
voice choice, and probes. `door_state()` becomes the winner's kind for the
winner, and the existing Act One or free-play Blocked/Open result for
everything else, with Plot and Bonus stripped. First match wins:

1. Day One active: the Act One sequence (`active_highlight_id`), as Plot.
   Nothing else may highlight during Day One.
2. A custom story event armed through `arm_royal_hall_event()`: the Royal
   Hall, as Plot.
3. The Moonflower gate revealed and not yet opened, as Plot (OD-2).
4. A built-in Royal Hall event (crown, then companion, then combat lesson), as
   Plot.
5. The first nominated Bonus, as Bonus. No production nominator exists at the
   baseline.
6. Otherwise, no highlight.

Unknown ids fail closed (Blocked). The arbiter is pure and probe-tested (AC-1).

### 3.6 Voice map

Exact clips that already exist (`assets/audio/voices/filler_v1/`, Roshan):

| Key | Transcript | Moment |
|---|---|---|
| `day1_arrival_castle` (contextual) | "Follow the one golden rainbow door! Foggy doors are resting until it is their turn." | M1 |
| `castle_home_day_one` | Same transcript | M7 in Day One |
| `castle_door_resting` | "That door is napping. Let's clean the next room!" | M3 in Day One |
| `castle_mist_resting` | "The mist is sleepy. Maybe later, little mist!" | M3 at the Royal Hall |
| `day_one_new_door` | "We cleaned it! A new picture door is glowing!" | M6 (moved from the room) |
| `day_one_all_rooms_clean` | "We cleaned the whole castle! Big door, please glow!" | M6 at the Royal Hall |
| `day_one_room_clean` | "All clean! The floor is twinkling!" | M5 celebration |
| `day_one_pool_ready` | "The sparkle pool is ready! Splash time!" | M5 after the bath |
| `castle_fairy_open` | "The castle found a secret sky door! Touch the shining pearl!" | M8 |

New exact lines. Add each first as a `PENDING_GENERATION` catalog row, then
generate it in Roshan's established synthetic voice through the existing
filler pipeline (`tools/select_filler_voices.py`, then
`tools/master_filler_voices.py`, following `assets/audio/voices/VOICE_MANIFEST.md`).
Keep each line to 8 words or fewer. Never synthesize Daddy, Faron or Chuck.

| Key | Transcript | Moment |
|---|---|---|
| `castle_route_back_to_hall` | "Back to the hall! Follow the star!" | M5 |
| `castle_route_follow_star` | "Follow the star to the glowing door!" | M2, M7 in free play |
| `castle_door_resting_free_play` | "That door is napping. Let's try another door!" | M3 in free play |
| `castle_home_free_play` | "Touch a picture door to visit a room!" | Free-play entry with no highlight; replaces the stale `castle_home` routing |
| `castle_route_to_bubble_bath` | "To the Bubble Bath!" | M4 |
| `castle_route_to_mermaid_pool` | "To the Mermaid Pool!" | M4 |
| `castle_route_to_playroom` | "To the Playroom! Baby Eagle needs us!" | M4 |
| `castle_route_to_craft_room` | "To the Craft Room!" | M4 |
| `castle_route_to_royal_hall` | "To the big royal door!" | M4 |
| `castle_route_to_moonflower` | "To the secret sky door!" | M4 |

Register every key above in an exact-only set, extending
`DAY_ONE_REQUIRED_EVENTS` (`scripts/audio_director.gd:26`) or adding a
sibling `DOOR_GUIDANCE_EXACT_EVENTS`. A missing take then yields caption only,
and today's pitched-"yay" fallback (`audio_director.gd:314-318`) is never
reached for a door line. Listening review stays pending (`DL-SND-15`).

### 3.7 Layering, coordinates and input

- **World space**: a new `Node2D` layer, `CastleDoorLightLayer`, under
  `castle_room_world_root`. Door light, haze and fog go at z 5 and the halo at
  z 6. That places them above the background tiles (0) and below the royal mist
  (40–48), the hall signs (68), and Roshan and her shadow (z ≥ 121). The
  Moonflower card is at z 70, so its visuals go at 71–72.
- **Stage space**: the star and beacon form one `Control` at stage z 27. That is
  above the transparent door hotspots (25) and below the transition cover (100);
  the global navigation `CanvasLayer` 29 stays on top.
- **Input**: door hotspots stay transparent `Button`s at stage z 25, sized from
  measured geometry as the frame bounds plus the threshold pool, with a minimum
  of 112×112 and no overlap between doors. The beacon hit area is 128×128.
  Light, haze and fog nodes are `Node2D` and take no input.

### 3.8 Geometry

- Replace `_arch_points()` with per-door data baked by a new deterministic tool,
  `tools/bake_castle_door_guidance.py` (with `--check`). Record the source tile
  SHA-256 and output hashes, and store stable output under
  `assets/castle/door_guidance/`. Each door needs: the opening polygon, the
  frame and crest silhouette for the halo, the threshold centre, the star
  anchor, and the hit rect, all in hall-art logical units (3344×941).
- Seeds: Appendix A, plus
  [`measured_door_geometry.json`](audit/door_highlight_rewrite_2026-09-30/measured_door_geometry.json).
  The seven standard doors measure HIGH confidence. The Opera Hall and Royal
  Hall defeat the colour scan (curtains, columns, stairs) and need a manual
  re-trace.
- If polygons cannot express the halo cleanly, bake small alpha masks. Follow
  the `tools/prepare_sky_lagoon_castle_symmetry.py::_build_door_highlight`
  precedent: ≤ 1024 px longest side, no VRAM compression on NPOT, with
  `ASSET_LICENSES.md` rows and provenance.

### 3.9 Performance and tiers

- Resting and Open treatments are built once per hall build and do nothing per
  frame. Billows reuse pooled tweens on existing nodes.
- Plot animates modulate or shader uniforms on persistent nodes. One small
  shared `canvas_item` shader for the halo shimmer is acceptable; it must not
  read the screen texture.
- No allocation in `_process`, tick, or draw paths (`DL-CODE-07`).
- Speedy tier drops the shimmer and the threshold pool, keeping a static gold
  halo. Record the budget note (`DL-CODE-08`, `DL-PERF-02`, `DL-PERF-03`).
- Report the before and after transparent-overdraw area. Today that is up to
  eight full-rect cues of about 122×233 px, each redrawn every frame.

---

## 4. Work packages (one PR; land in order)

| WP | Deliverable | Notes |
|---|---|---|
| WP-D0 | Failing baseline. Write the new assertions (§6), run them against `e7899cc0` with exact Godot 4.7.2-stable, and keep the failing logs as evidence. Land the assertions together with the fix so CI stays green | Master audit §9, step 3 |
| WP-D1 | `tools/bake_castle_door_guidance.py`, the geometry data, and an overlay review sheet | Verify against Appendix A; re-trace the Opera Hall and Royal Hall |
| WP-D2 | `CastleDoorLanguage.arbitrate()` (pure). Rewire `door_state()` and `active_door_highlight_id()` to it | Keep the existing static API |
| WP-D3 | Rewrite `scripts/castle_door_cue.gd` as a world-space `Node2D`. Keep `class_name CastleDoorCue`, `set_door_state()`, `pulse_blocked_feedback()` and `pulse_plot_feedback()`. Add `configure(geometry)`. Delete `_arch_points()` and the per-frame `_draw()` | No `Control` cue remains in the hall |
| WP-D4 | New `scripts/castle_door_guide.gd`: a `RefCounted` satellite that receives `main` by reference and owns the star, beacon, transfer, blocked ping, idle timers, exit guidance and voice selection | Use typed fields and no new `m.g[...]` keys (`DL-CODE-04`). Keep `castle_rooms_25d.gd` net-negative in lines (`DL-CODE-02`, currently 5,755) and `main.gd` at ≤ 0 net lines (`DL-CODE-01`) |
| WP-D5 | Make the Royal Hall mist follow `door_state()`. The Moonflower satellite consumes the arbiter, and its dormant card becomes a resting participant | Keep that satellite's hash-isolation contract |
| WP-D6 | Return to the exit door (M6). Keep the courtyard-entry spawn rule, and align `restore_day_one_handoff_view()` | OD-3 |
| WP-D7 | Voice: add the new catalog rows and exact-only registration, move the M5/M6 lines, fix the caption and voice mismatches, and generate the clips | `tools/audit_day_one_contextual_voices.py` |
| WP-D8 | Probes, captures, frame-ledger revalidation, the `design/07` v2 rewrite, ledger rows, `ASSET_LICENSES.md`, and the impact record | §6, §8 |
| WP-D9 | **Separate later PR, after OD-1**: migrate the other live door highlights to the guide-star vocabulary. That covers the Sky Lagoon promenade castle door (a red `Affordance.PLOT` focus mask whose idle α is capped at 0.055 outside Day One, `scripts/arena/sky_lagoon_promenade.gd:826-850`); the Opera venue show doors (every portal button style is transparent and the ghost-hand `guide_pointer` shows only in `chapter2_tutorial_mode`, `scripts/opera_house_venue_2d.gd:359-380`, while `scripts/main.gd:2763` promises "a glowing show door"); and the other ghost-hand pointers | Out of scope for the first PR |

---

## 5. Files

| Action | Paths |
|---|---|
| Create | `scripts/castle_door_guide.gd`, `tools/bake_castle_door_guidance.py`, `assets/castle/door_guidance/*` (data and any masks, each listed individually in the impact record), runtime captures, `design/audit_impacts/<task-id>.json` |
| Rewrite | `scripts/castle_door_cue.gd`, `scripts/probe_castle_door_language.gd` |
| Extend | `scripts/castle_door_language.gd` (arbiter), `scripts/audio_director.gd` (exact-only keys), `scripts/day_one_contextual_voice_catalog.gd` and `audit/DAY_ONE_CONTEXTUAL_VOICE_COVERAGE_2026-09-01.json` (pending rows), gated probes `probe_day_one_handoffs`, `probe_day_one_integration`, `probe_throne`, `probe_day_one_voice`, `probe_passive` |
| Thin delegation only | `scripts/arena/castle_rooms_25d.gd`, `scripts/arena/fairy_conservatory_door_2d.gd`, `scripts/main.gd` |
| Documents | `design/07_CASTLE_DOOR_LANGUAGE.md` (v2), `design/05_DOC_LEDGER.md`, `ASSET_LICENSES.md`, `assets/audio/voices/VOICE_MANIFEST.md`, `assets_src/castle/interactions_v4/castle_interaction_frame_approval_ledger.json` (metadata revalidation only) |
| Never touch | Approved hall tiles, signs, Moonflower cards and mist wisps; protected voices (`daddy*`, `chuck*`, `faron*`, `voice_yay`); `.github/workflows/*` (every probe named here is already gated in both rosters); `CLAUDE.md`, `AGENTS.md`, `SECURITY.md`; the save schema; `InteractionAffordance` colours (OD-1); `master` |

---

## 6. Acceptance criteria

Probe assertions run in the gated probes named in §5, under real state
transitions (`DL-QA-02`), with no state written around the interaction under
test.

| AC | Check |
|---|---|
| AC-1 | Arbiter table test: every Day One beat; free play across custom × built-in Royal Hall events × Moonflower dormant/revealed/opened × Bonus nominee. Assert ≤ 1 highlight, the documented priority, and that unknown ids fail closed. |
| AC-2 | Real hall entry at every Day One beat, reached through save states: within 2 frames the highlighted cue is ≥ 35% on screen or exactly one beacon is visible, and exactly one star exists. |
| AC-3 | Wander: walk to hall x 60 during beats 2–4 and confirm the right-edge beacon appears within 2 frames. A beacon tap travels, the arrival enters the plot room, and no other progress occurs. |
| AC-4 | Blocked tap on every resting door and on the dormant Moonflower card: no travel, no progress, billow timer > 0, star ping, the correct exact key requested, SFX at most once per cooldown. |
| AC-5 | Resting doors are static: across 60 frames at rest, resting nodes report `is_processing() == false`, make no redraw requests, and keep unchanged transforms. |
| AC-6 | Layering: every door light, haze, fog and halo node descends from `castle_room_world_root` with an effective z below Roshan's. A capture of Roshan at the plot door foot shows her unobscured. |
| AC-7 | Scroll: while the camera pans, the cue's offset from the door art stays constant (no re-fit). |
| AC-8 | Geometry: `bake_castle_door_guidance.py --check` passes. Overlays show light inside the opening and the halo from the frame edge within ≤ 2 stage px. |
| AC-9 | Transfer: complete each beat through the real API and press Back. Roshan stands at the exit door foot (±2 px); the star flies to the next door; `day_one_new_door` (or `day_one_all_rooms_clean`) is requested once; a tap mid-flight completes the transfer; re-entry does not replay it. |
| AC-10 | Exit guidance: the star is visible beside the Back control after each completion. The room teardown frees it and leaves no leaked nodes, tweens or voice. |
| AC-11 | Free play with a built-in Royal Hall event and a revealed Moonflower gate highlights exactly the arbiter's choice. The Moonflower no longer self-assigns PLOT. |
| AC-12 | Royal Hall mist authority: in Day One before boss-ready, the authored mist is visible (α > 0.1 after 1 s) with no procedural haze. After boss-ready the mist fades and Plot visuals appear. |
| AC-13 | Zero input: 120 s idle in the hall, in Day One and in free play, enters no room and awards nothing. At most two voiced reminders play, and the star keeps idling (`DL-AGE-04`). |
| AC-14 | Close, pause, focus loss, save/load and re-entry cancel tweens and voice queues. Loading mid-beat restores the correct highlight and plays M1/M2, not a stale M6 (`DL-SAVE-03`, `DL-SND-03`). |
| AC-15 | Zero per-frame allocation in cue, guide and tick paths. A Speedy-tier budget note is recorded, and transparent-overdraw area is ≤ baseline. |
| AC-16 | Every requested key is on the §3.6 map. Ready keys resolve to exact files; pending keys give caption only. No door key reaches `talk`, `win` or `yay`. `tools/audit_day_one_contextual_voices.py` passes in implementation mode. |
| AC-17 | Exact Godot 4.7.2-stable Mobile captures at 1280×720, bound to the commit: Day One beats 1–5 at entry, the wandered-left beacon, a blocked tap mid-billow, a transfer mid-flight, Roshan at the plot door, free-play Royal Hall and Moonflower, each with a quarter-scale squint version checked against G3. |
| AC-18 | `python3 tools/review_castle_interaction_frames_v4.py check` passes after an honest metadata-only revalidation, with all 96 reviewed frame hashes unchanged. |

---

## 7. Owner decisions (Codex proceeds on the default and reports it)

| OD | Question | Default |
|---|---|---|
| OD-1 | Prop affordances (`scripts/interaction_affordance.gd`) say red means plot and gold means only a local animation, while doors say gold means plot and ruby means bonus. The Sky Lagoon promenade castle door is red. | Keep the design/07 colours for castle doors, as the later, narrower domain record (`DL-AUTH-04`). Do not recolour props. WP-D9 recolours the promenade door only after owner confirmation. |
| OD-2 | Free-play priority between the Moonflower gate and a built-in Royal Hall event | The §3.5 order: custom Royal Hall event, then Moonflower, then built-in Royal Hall events |
| OD-3 | Where Roshan appears when returning to the hall from a room | At the exit door foot, per the protocol; the next Day One door is still ≥ 52% on screen (§3.4). Courtyard entry keeps the dev spawn. |
| OD-4 | Whether an off-screen Bonus door gets an edge beacon | No; Bonus stays restrained |
| OD-5 | New lines in Roshan's synthetic voice | Generate through the existing pipeline; family recordings can replace them under the same keys later |
| OD-6 | Treatment intensity | Use §3.2 values, tuned within ±25% during capture review. 5/5 is an owner award (`DL-VIS-07`). |

---

## 8. Gates and delivery

1. Branch `codex/door-guidance-v2` from a fresh `origin/dev`.
2. Before each commit: `python -m gdtoolkit.parser <changed .gd>` and
   `python tools/lint_inference.py <changed .gd>`. Declare explicit types in
   extracted classes.
3. Run the exact Godot 4.7.2-stable import, then `GODOT=… scripts/ci.sh`
   (all trusted probes), then `python3 tools/audit_game_2d.py
   --regression-gate` (no debt growth).
4. Run `python -B tools/audit_document_authority.py`,
   `python -B tools/audit_development.py --base auto`, and
   `python -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development`.
5. Revalidate the frame-review ledger the way commit `1f23231` and the
   2026-09-12 usability repair did: update only the candidate and prior payload
   hashes, the date, and an honest reason, and only when every reviewed frame
   hash is unchanged. Never add an approval.
6. When the work-branch probes are green in CI, merge to `dev` (per the
   `CLAUDE.md` workflow). Do not promote to `master` unless the owner asks.

## 9. Stop and escalate if

- the work would modify approved art, protected voices, save keys, workflows,
  or `InteractionAffordance` colours;
- the frame-review check reports changed frame hashes rather than only a
  payload hash;
- a gated probe would have to be weakened rather than extended;
- `castle_rooms_25d.gd` or `main.gd` would grow;
- the Speedy-tier frame time regresses on measurement;
- the voice pipeline is unavailable. In that case ship the pending captions
  and report the lines `BLOCKED_EXTERNAL`; never use a generic clip;
- G3 cannot be met with §3.2 values ±25%.

## 10. Report

Name the implemented scope and the commit. Report machine verification with
exact commands, results, and the CI run id. List outstanding acceptance: the
visual 5/5 owner award, Lenovo Tab M11 and phone device checks including the
squint test, child observation (`MA-CHILD-001`), voice listening, and the
still-open `MA-PLAY-001`, `MA-PLAY-003` and `MA-ACCESS-001` scopes. Attach the
AC-17 captures.

---

## Appendix A — measured painted-door seeds (hall-art logical units)

Method: an outward scan from each door's centre line for warm frame pixels,
upward from the threshold, on the 7280×2048 master (tile hashes in the JSON).
Frame x is the painted frame's outer edge on the pillars.

| Door | Confidence | Opening x | Apex y | Spring y | Threshold y | Frame outer x | Hotspot x today |
|---|---|---|---|---|---|---|---|
| family_gallery | HIGH | 237.0–339.9 | 382.7 | 417.7 | 597.8 | 218.6–357.8 | 210–370 |
| library | HIGH | 403.3–502.1 | 379.1 | 414.0 | 597.8 | 384.9–520.4 | 380–540 |
| kitchen | HIGH | 568.2–668.3 | 380.0 | 414.0 | 597.8 | 550.3–686.7 | 545–705 |
| opera_hall | LOW, re-trace | 913.9–1123.5 | 279.8 | 311.1 | 597.8 | 899.4–1137.8 | 875–1175 |
| playroom | HIGH | 1963.2–2067.0 | 382.7 | 416.7 | 597.8 | 1944.8–2084.9 | 1940–2100 |
| craft_room | HIGH | 2161.2–2264.5 | 381.8 | 416.7 | 597.8 | 2143.3–2282.9 | 2140–2300 |
| mermaid_pool | HIGH | 2354.1–2457.5 | 379.1 | 415.8 | 597.8 | 2336.2–2475.8 | 2340–2500 |
| bubble_bath | HIGH | 2557.1–2660.5 | 379.1 | 416.7 | 597.8 | 2539.2–2678.9 | 2540–2700 |
| __royal_hall | LOW, re-trace | 2934.3–3157.0 | 216.9 | 305.1 | 469.6 (top stair) | 2905.3–3185.5 | 2870–3220 |

The Moonflower gate is a card (`scripts/arena/fairy_conservatory_door_2d.gd`,
card rect 1396–1948), so measure it in card-local coordinates.

## Appendix B — current code map (dev `e7899cc0`)

| Concern | Location |
|---|---|
| State resolver | `scripts/castle_door_language.gd:40` `resolve_act_one`, `:58` `resolve_free_play`, `:67` `active_highlight_id` |
| Cue drawing | `scripts/castle_door_cue.gd:67` `_process`, `:85` blocked, `:109` bonus, `:120` plot, `:158` `_arch_points` |
| Hall portals | `scripts/arena/castle_rooms_25d.gd:159` `HALL_PORTALS`, `:1657` build, `:5224` per-frame update, `:5286` enter |
| State plumbing | `castle_rooms_25d.gd:1686` `door_state`, `:1698` `active_door_highlight_id`, `:1741` blocked feedback, `:1777` `_pulse_active_door` |
| Spawn and return | `castle_rooms_25d.gd:1729` `_day_one_hall_spawn_foot`, `:2849` `_center_player`, `:2879` `restore_day_one_handoff_view`, `:5740` `_go_back` |
| Royal Hall | `castle_rooms_25d.gd:144` mist cards, `:2998` `arm_royal_hall_event`, `:3047` `_royal_hall_event_id`, `:3063` mist tick |
| Layers | `castle_rooms_25d.gd:1307` world root z −1000, `:1371` door hotspot layer z 25 |
| Moonflower | `scripts/arena/fairy_conservatory_door_2d.gd:178` `_ensure_hotspot` (PLOT at :188), `:227` `_update_hotspot` |
| Day One flow | `scripts/main.gd:322` room map, `:330` optional kitchen, `:6121` hall entry lines, `:6642` resting line, `:6650` room activation, `:7125` room handoff, `:7146` handoff sync |
| Voice | `scripts/audio_director.gd:26` exact-only set, `:194` `_voice_path`, `:238` `_say` (yay fallback at :314) |
| Back control | `scripts/navigation_controller.gd:111` (top-left, 18–130 px) |

## Appendix C — review images

All files are in `audit/door_highlight_rewrite_2026-09-30/`, rendered at the
1280×720 stage scale. `current_*` images replicate today's cue math over the
approved art; `concept_*` images show v2 intent. PIL approximations cannot
stand in for AC-17.

| File | Shows |
|---|---|
| `current_day_one_bubble_bath_entry.jpg`, `concept_day_one_bubble_bath_entry.jpg` | Day One beat 1 at the dev spawn camera |
| `squint_quarter_scale_current_vs_concept.jpg` | The same frame at quarter scale (G3) |
| `current_day_one_wandered_left.jpg`, `concept_day_one_wandered_left.jpg` | Mermaid Pool beat with Roshan at the hall's left end; the concept shows the edge beacon |
| `current_free_play_royal_event_entry.jpg`, `concept_free_play_royal_event_entry.jpg` | Free-play entry with a Royal Hall event waiting off-screen |
| `measured_door_geometry_overlay.jpg`, `measured_door_geometry.json` | Seed geometry: green is the opening, magenta the frame edge, yellow today's hotspot rect |
| `measure_hall_door_geometry.py`, `render_review_mocks.py` | Deterministic generators (Pillow and numpy) |

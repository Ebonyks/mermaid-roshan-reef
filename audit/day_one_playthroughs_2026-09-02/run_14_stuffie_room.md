# Run 14 — Stuffie lover

Persona: Four years old, non-reader, one finger. Her favourite thing in the whole
game is the stuffed friends; she has heard there is a "birdie" in the castle and
she wants to *have* it. She taps anything that looks like a toy or an animal
first, repeats whatever made a noise, and uses the "↩" button freely because it
has always taken her "back". Today she plays a normal-length session and will
stop when she has her stuffie.

Path taken: New Game → Sky Lagoon ocean-gate hub → castle gate → Main Hall
("Follow the one golden rainbow door") → walk right → Bubble Bath (basket, sink
scrub, tub tap, brush) → pool picture button → Mermaid Pool (skimmer, waterfall,
seahorse, Rumi) → Back to the Main Hall → walk right until the Stuffie Playroom
door glows → Playroom: Baby Eagle pinned by two dust bunnies, one tap on the
eagle/star walks Roshan through both contact ellipses and pops both bunnies →
eagle fades → full-screen stuffie picker (one card: Baby Eagle) with the gold
tutorial frame → part icon → colour → "♥ TAKE ALONG!" → picker closes; nothing of
the eagle is visible in the castle → she taps the toys, then Back → Craft Room
glows → Art Room → boss door → Grand Puff → Day Two banner. Her Baby Eagle only
appears beside her once she leaves the castle after the boss.

## Beat log

Coordinates are 1280×720 stage px unless marked "art" (1024×576 playroom art;
×1.25 = stage, `castle_rooms_25d.gd:28,3849-3850`). Rooms outside the playroom
are one row each (not re-traced in this run — flow-map pointers, see Confidence).

| # | Beat | What she sees | What she hears | Input needed | Est. seconds (min / typical / max) | Evidence | Attention (G/Y/R) |
|---|---|---|---|---|---|---|---|
| 1 | New Game → Sky Lagoon arrival | Start menu; plane arrival at the ocean-gate hub (in-engine fallback; Grok movie absent) | Menu tap; arrival voice | 1 tap, then wait | 8 / 20 / 40 | `main.gd:3966-3970` `_launch_from_start_menu` → `_enter_level2_now`; movie only recorded as a request `main.gd:7770-7774` | Y (passive plane) |
| 2 | Walk to castle gate, tap to enter | Lagoon promenade, castle gate | — | taps/drags | 10 / 25 / 60 | flow map (`sky_lagoon_promenade.gd`), not re-traced | G |
| 3 | Main Hall first entry | Fade-cut; 3344-wide hall, Roshan at hall-art (380,835), view 0–1672; the glowing Bubble Bath door is at hall-art 2540–2700 → OFF-SCREEN. Banner text is hidden (hud_layer hidden in castle) | `roshan_talk.ogg` ("Follow the one golden rainbow door…" text hidden); second banner "Dust bunnies!…" 0 s later overwrites it (voice: roshan_talk dedup-suppressed) | tap right floor or the ↕ elevator | 5 / 15 / 40 | `main.gd:6819-6858`, `7783-7786`; hall spawn `castle_rooms_25d.gd:2318-2323`; portal culling `4432`; HUD hidden `967-968` and `hud_msg` lives on `hud_layer` `main.gd:3590,3617` | Y |
| 4 | Bubble Bath tutorial | basket at (940,575), sponge/brush demo, sink circle, tub tap ("No!" swimmer), tub brush | voice lines per protocol | ~6 gesture beats | 60 / 120 / 240 | `main.gd:7231-7252` completion → pool picture button (1035,455) 205×190 `7577-7582` | G |
| 5 | Mermaid Pool | pool picture button → skimmer (6 trash), waterfall (3 lanes), seahorse (8 taps), Rumi reveal | Roshan lines `day_one_pool_cleanup.gd:384-392` | ~17 taps + drags | 60 / 110 / 200 | mount `castle_rooms_25d.gd:1893-1918`; `main.gd:7304-7320` | G |
| 6 | Pool done → leave | Rumi waves/idles; gold room action button (72,520) 132×132 reappears; NO route button, NO "new door glowing" line (that banner only lives in the placeholder branch) | "Thank you, Roshan!… I'm Rumi!" (`rumi_intro.ogg` if present, else fallback); action button → "This room is sparkly clean!" `roshan_win.ogg` | she pokes Rumi/button 1–3×, then ↩ at (28,28) 112×112 | 5 / 15 / 45 | `day_one_pool_cleanup.gd:576-596`; `castle_rooms_25d.gd:2020-2025`; director advances current room to `stuffie` `day_one_director.gd:353-379`; placeholder-only banner `main.gd:7180-7186`; back button `castle_rooms_25d.gd:1240-1246,4863-4874` | G→Y |
| 7 | Main Hall re-entry, find the glowing door | 0.24 s fade; Roshan back at (380,835), view_left 0. Playroom door (hall-art 1940–2100) is off-screen; nothing on screen glows. One tap on the right edge walks her ≤1.05 s and the camera lerps (weight δ×3.5) until the Playroom door shows the PLOT cue: gold arch pulsing 3.2 s, rainbow sheen 4.6 s, gold star. Alternative: ↕ elevator (1116,544) 136×136 → 4×3 picture grid, Playroom picture wears the same PLOT arch. Detour: tapping the neighbouring Craft Room door (2140–2300, BLOCKED) → swish + 0.72 s pulse + "Craft Room is resting…" | "Main Hall" banner → `_say("roshan","home")` has no clip → pitched "yay"; blocked door → pitched "yay" (daddy_hint missing) + `roshan_talk.ogg` | 1–3 taps | 4 / 15 / 60 | fade `castle_rooms_25d.gd:2098-2099`; camera `4251-4270`; portals `150-177`, visibility `4399-4459`; door state `1653-1660` + `castle_door_language.gd:39-53`; PLOT cue `castle_door_cue.gd:111-142`; elevator `1252-1255,1565-1632,1751-1762`; blocked feedback `1700-1718`; `_say` fallback `audio_director.gd:21-45` | Y (no pointer, no voice for "go right") |
| 8 | Tap Playroom door → room | Roshan walks to the door foot (≤1.05 s + 0.04), 0.24 s fade, playroom: Baby Eagle card 116×205 at (659,457) between two bunny cards 166×166 at (556,456) and (724,456); gold star ≈53–61 px pulsing (scale 0.052→0.060, 0.84 s loop) at (640,262) above the eagle; Roshan at (640,650); action button HIDDEN | Banner "Chirp! Two dust bunnies have me! Swim over and bump both away!" is text-hidden; voice = `sparkle.ogg` (a wordless chirp: `sparkle_talk.ogg` does not exist) | none (passive) | 1.5 / 2 / 3 | portal walk `4461-4517`; `show_room` `1772-1864` (button hidden `1841-1846`, banner `1857-1862`); items `222-248`, rebuild `2536-2556`, placement `3817-3827`; pointer `4169-4194`; spawn `2325-2329`; speaker map `audio_director.gd:129`; voice list (no sparkle_talk) | G |
| 9 | First tap: rescue | **Tap A (most likely for her: the birdie or the star)** → no bunny under the finger → clamped floor walk (star → (640,425); eagle → (659,457)); the walk tween passes y≈562 where BOTH contact ellipses (feet (556,562)/(724,562), radii 102×77) overlap at x 621–658 → both bunnies burst mid-glide (~0.37 s). **Tap B (a bunny card)** → pops that one instantly, Roshan does not move; second tap 1–1.5 s later. **Tap C (a toy hotspot: stuffie nook / tent / blocks)** → 8-frame toy animation ≈1.1 s + `toy_blocks.ogg`, then she retries. Per pop: `hop_boing.ogg` at pitch 1.55 / 1.72, pop chime, 20 ms haptic, 8 star motes 0.48 s, card scales ×1.45 + rotates + fades 0.24 s, ⭐ chain pips. No TRIO shake (needs chain ≥3; only two bunnies) | boing, pop ×2 | 1–3 taps | 2 / 5 / 25 | input `2115-2156`; bunny pick `2168-2192`; walk tween/speed 520 px/s, clamp 0.12–0.85 s `2194-2260`, `tween_method` foot `2244-2246`; contacts every tick `1131`, ellipse `4022-4050`; explode `4052-4123`; burst `3724-3772`; TRIO gate `4081-4088`; shake `4272-4282` (not reached); chain `hit_engine.gd:378-390` | G |
| 10 | Rescue complete | `stuffie_wins["rescued_eagle"]`, room `stuffie` completed, current → `art`; bunnies hidden; 16 blue motes (0.72 s); eagle scales ×1.12 and fades (delay 0.34 s, 0.38 s) — its "lift" is +1.25 px DOWN (3D-era magnitude), so it reads as a fade; star pointer removed; action button visible; two synchronous saves | Banner "Chirp! You saved me!…" text-hidden; voice = `sparkle.ogg` chirp again (no `sparkle_win.ogg`) | none | 0.8 / 1 / 1.5 | `4196-4240`; `main.gd:7322-7333`; director `353-379`; door refresh `main.gd:7357-7378` → `1662-1664` | G |
| 11 | Stuffie picker tutorial | CanvasLayer 25, dim 0.76, panel (34,24) 1212×672 "🧸 Choose a stuffie friend!"; ONE card "Baby Eagle" 330×225 at (80,130); live preview 330×330 at (460,130); three part icons 116×116 at y=130 wrapped in a pulsing 8 px gold frame + "▼" (step 0); 8 swatches 110×110 at y 270/386; "♥ TAKE ALONG!" 330×150 at (460,500); "↩" close 112×112 at (1110,32). Tap part icon → frame moves to palette (step 1); tap swatch → preview recolours, frame moves to the heart (step 2); tap heart → done. The heart is live at every step (1-tap minimum). Every swatch tap redraws + says "Beautiful!" | `roshan_talk.ogg` on open ("Which stuffie friend…" text hidden); step lines ("Now tap any big color!", "Beautiful!…") also resolve to `roshan_talk.ogg` and are DROPPED if the previous clip is still playing | 1–3 taps (or many colour taps) | 3 / 12 / 90 | `companion.gd:572-610`, `_draw_picker` `700-828` (single card `727-733`, close `719-724`, icons `780-790`, swatches `792-812`, heart `813-820`), focus `830-872`, steps `641-659`; dedup guard `audio_director.gd:29-35`; probe `probe_stuffie.gd:161-206` | G (agency, colours) |
| 12 | Confirm | Fanfare (`_reward(false)`); `companion="eagle"` + colours saved; picker closes; clean playroom, action button; the 3D sparkle burst is under the castle layer (invisible); NO stuffie appears, NO 🧸 HUD button (`_follow_ctx` false in the castle, hud hidden) | fanfare + "Baby Eagle flies with you now! Peck peck!" = `sparkle.ogg` chirp (text hidden) | 0 | 1 / 2 / 3 | `companion.gd:661-700`; `_reward` `main.gd:8899-8903`; follow gate `companion.gd:192-196`, button `242-246` | G→Y ("where is my birdie?") |
| 13 | Post-adopt play | She taps the Stuffie friends nook (wave), tent, blocks, stacking toy (each ≈1.1 s atlas + SFX); action button → "This room is sparkly clean!" `roshan_win.ogg` | toy SFX, roshan_win | 0–10 taps | 0 / 20 / 90 | items `480-493`, actions `776-787`; `main.gd:7145-7148` | G |
| 14 | ↩ → Main Hall → Craft Room | Craft door (hall-art 2140–2300, right next to the playroom door) now PLOT; tap → Art Room | pitched "yay" (home), roshan_talk | 2–3 taps | 4 / 12 / 40 | `4863-4874`, `1653-1660` | Y |
| 15 | Art Room | 4 materials + 3 grime, desk, attack customizer | Roshan lines | ~12 taps | 90 / 150 / 300 | flow map (`day_one_art_studio.gd`), not re-traced | G |
| 16 | Boss door → Grand Puff | Royal Hall event, 3 rounds × 3 taps | boss lines | ~9–14 timed taps | 60 / 120 / 240 | `main.gd:7761-7769,7794-7798`; not re-traced | G |
| 17 | Day Two banner; later, first sight of Baby Eagle | 4.18 s transition; the eagle cutout spawns beside Roshan only in a free-roam world (courtyard after leaving the castle) with "Here I am! Let's explore together!" | day_two_begins, eagle greeting | 0 | 4 / 4 / 4 (+ walk out) | `main.gd:7086-7108`, `5793` (phase court); `companion.gd:1176-1194` | G |

Stuffie-room slice alone (beats 6–14): **21 / 84 / 357 s**. The rescue itself (beats
8–10) is 4–8 s of real play; the picker is the beat.

## Time budget
- Total: ≈ 318 / 648 / 1481 s (≈ 5.3 / 10.8 / 24.7 min) from the New Game tap to
  the Day Two banner. Typical lands inside the 8–15 min session window; max does not.
- Longest passive span: beat 1 arrival plane (flow map, ~8–20 s) — restless.
  Inside the stuffie beat the longest passive span is the eagle fade → picker,
  0.72 s (`castle_rooms_25d.gd:4228-4235`): fine.
- Longest input-required span with no new feedback: beat 7 — after the pool she
  is dropped at the left end of the hall with the glowing door off-screen and no
  voice/pointer telling her to go right; 5–10 s of "nothing glows" before she
  repeats what worked earlier (walk right / elevator). Second: beat 12→13, the
  adopted eagle gives no visible presence in the castle, so "what happened?"
  silence of 3–8 s.
- Natural stopping points that lose nothing: after either bunny pop (sync
  `_write_save()` `4122`; pins restored `4153-4167`, proven `probe_stuffie.gd:143-160`);
  after the rescue (`4204-4206`); after "♥ TAKE ALONG!" (`companion.gd:693`).
  Stopping *between* the rescue and the heart loses no progress but defers the
  adoption to Day Two (see hazards).

## Pros (as this player experienced it)
- The rescue is one-finger and un-failable: no timer, no damage, the two
  contact ellipses overlap under the eagle (x 621–658 at y≈562), and
  `_check_dust_bunny_contacts` runs every tick during the walk tween, so the
  single most natural tap for a stuffie lover — on the birdie or on the star
  above it — walks Roshan through both bunnies and frees the eagle in ~0.4 s
  (`2123-2156`, `2244-2246`, `1131`, `4036-4048`). Tapping a bunny card directly
  also works from anywhere (`2129-2132`). Combined target per bunny ≈ 166×267 px.
- Persistence is honest: each pin is saved synchronously the instant it pops,
  the cleared pin never respawns, and `m.g` scratch is re-derived from
  `stuffie_wins` on every rebuild (`4118-4123`, `4153-4167`, `save_state.gd:142-143,274`).
- The picker is picture-first: one big eagle card, a live-tinted preview, giant
  swatches (110 px), a 330×150 heart, and a pulsing gold frame + ▼ that moves
  part → colour → heart. The heart is never gated, so the tutorial is optional
  (`companion.gd:813-820`, `830-872`). Colour play is real agency — every swatch
  tap recolours the preview (`641-651`).
- Feedback per pop is rich and cheap: boing at two pitches, pop chime, haptic,
  8 motes, scale/rotate/fade vanish, ⭐ pips (`4093-4111`, `hit_engine.gd:382-390`).
- The castle stage is genuinely true-2D: `castle_rooms_25d.gd` has 0 references
  to Sprite3D/Node3D/Camera3D/Vector3; cards are `Sprite2D`, picking is canvas
  transforms (`2168-2192`, `3875-3897`), the chain engine runs with
  `camera = null` (`975-978`). The rescue guide's Sprite3D staging is stale, not live.

## Cons / friction (as this player experienced it)
- Length/legibility: the "rescue" is over in one or two taps (4–8 s). It is
  legible as *bunnies again* (the verb she learned in the hall), but it does not
  read as "rescue" — the only spoken content in the whole room is a wordless
  chirp (`sparkle.ogg`; `sparkle_talk`/`sparkle_win` do not exist) and every
  banner is text-hidden because the castle hides `hud_layer` (`967-968`,
  `main.gd:3590,3617`). Neither the child nor the adult beside her gets the words
  "bump both away" or "let us learn how stuffie friends come along".
- Transition from cleaning → rescue + picker: the pool gives no hand-off (no
  route button like the bathroom's, no "a new picture door is glowing" line —
  `main.gd:7180-7186` is placeholder-only), the glowing door starts off-screen,
  and the picker appears with a Roshan line whose clip is the generic
  `roshan_talk.ogg`. She lands in a full-screen menu she has never seen with a
  gold frame pointing at three emoji buttons. The frame + ▼ carry it; the voice
  does not.
- Her reward vanishes: after "♥ TAKE ALONG!" nothing changes in the castle — no
  eagle beside Roshan, no 🧸 button, and the celebration sparkle is a 3D burst
  hidden under the castle layer (`companion.gd:192-196`, `242-246`, `695-696`). A
  stuffie lover's whole point of the beat is invisible until after the boss.
- The picker's "↩" (top-right, 112 px) is the same glyph she has used all day to
  go back. If she taps it — or the app is killed with the picker open — the
  offer is gone for the rest of Day One (see hazards). The rescue guide's claim
  that "the playroom action reopens the focused tutorial" is false while Day One
  is active.
- Un-converted 3D magnitudes: the pointer bob is 0.28 px and the eagle's
  farewell "lift" is +1.25 px downward (`4186-4193`, `4228-4229`), so the pointer
  only pulses in size and the eagle just fades.

## Invariant hazards found
| Invariant | Beat | What happens | Evidence | Severity (P1/P2/P3) |
|---|---|---|---|---|
| dead-end (Day One scope) | 11–12 | Close the picker (↩ at (1110,32), or a tap on the 24–34 px dim margin) or kill the app before the heart: `stuffie_rescue_tutorial` is scratch, `companion_id==""`, the room is already `completed` → the action button answers "This room is sparkly clean!" and returns before the `"stuffies"` branch can reopen the tutorial; re-entering the playroom rebuilds without the eagle. The picker is unreachable until Day Two (when `day_one_activate_castle_room` returns false and `4777-4783` runs). Contradicts `STUFFIE_PLAYROOM_RESCUE_GUIDE:79-82` and `STUFFIE_COMPANIONS.md:52-60` | `companion.gd:612-620,719-724`; `main.gd:7140-7148`; `castle_rooms_25d.gd:4763-4783`, `2552-2556`, `4153-4156` | P2 |
| non-reader / dead-air | 8, 10 | The room's objective and completion lines are voiced only as a chirp; captions hidden in the castle. `_say()` technically fires, but no recorded words. Pointer marks the captive, not the captors (works only because the walk-through pops both) | `audio_director.gd:13-27,129,139-173`; `castle_rooms_25d.gd:967-968,1857-1862,4218-4220`; voices dir (sparkle.ogg only) | P2 |
| confusing-feedback (persona) | 12 | Adopting gives no visible companion or HUD badge inside the castle; the reward is deferred for the whole Art Room + boss | `companion.gd:192-196,242-246,1176-1194`; `main.gd:5793` | P2 |
| dead-air / no pointer | 7 | After the pool: no route button, no voice, glowing door off-screen at spawn; she must rediscover walk-right/elevator | `castle_rooms_25d.gd:2318-2323,4432`; `main.gd:7180-7186,7562-7590` (bathroom-only route) | P2 |
| touch-target / confusing-feedback | 11 | Picker close is the familiar "↩" 112×112 in the corner; a habitual "back" tap triggers the P2 dead-end above | `companion.gd:719-724`, `storybook_ui.gd:204-206` | P3 |
| dead-air (voice dedup) | 11 | Step lines all resolve to `roshan_talk.ogg`; the identical-stream guard drops a second call while the first plays, so a quick child hears no line for "Now tap any big color!" | `audio_director.gd:29-35`; `companion.gd:645-650,656-658` | P3 |
| other: 3D staging debt (true-2D rule) | 12, 17 | Castle stage is clean (0 3D refs), but the companion produced by this beat is a `Node3D`+`Sprite3D` billboard cutout, `Vector3` follower maths, `Label3D` den pointers (dead code), and the confirm burst is `_sparkle_burst(Vector3)`; 122 3D refs in `companion.gd`. Docs still describe Sprite3D rescue staging and GLB bodies | `companion.gd:128-187,933-1175,1176-1260,695-696`; `STUFFIE_PLAYROOM_RESCUE_GUIDE:27-28,45-53,96-101`; `STUFFIE_COMPANIONS.md:26-30` | P3 (rule debt, not child-facing) |
| confusing-feedback | 8, 10 | Pointer bob 0.28 px, eagle lift +1.25 px down — Sprite3D world-unit values in 2D tweens | `castle_rooms_25d.gd:4186-4193,4228-4229` | P3 |
| lost-progress | 9–12 | none found: pins, rescue and companion each `_write_save()` synchronously; restore re-derives scratch | `4118-4123,4204-4206`, `companion.gd:693`, `save_state.gd:142-143` | — |
| no-fail | 9 | none: no timer, no penalty, Daddy Splash excluded from rescue pins, spawn cannot pre-pop | `4125-4147`, `probe_stuffie.gd:138-142` | — |

## Tuning proposals (max 6, concrete, numeric where possible)
| # | Change | File:line | Current value → proposed | Why it helps a 4-year-old |
|---|---|---|---|---|
| 1 | Re-arm the adoption offer while Day One is active: before the "sparkly clean" reply, `if logical_room == "stuffie" and companion_id == "": _castle_rooms_ref()._open_playroom_stuffie_tutorial(); return true`; also call it from `_restore_playroom_rescue_clears` when the rescue is done and `companion_id == ""` | `main.gd:7145-7148`; `castle_rooms_25d.gd:4153-4156` | unreachable in Day One → reopens on the gold room button / on re-entry | A habitual ↩ or an app kill can no longer cost her the stuffie until Day Two |
| 2 | Give the room words: route the entry/rescue lines through Roshan (`show_msg("Roshan", …)` or add `_say("roshan","talk",0.8)` after the chirp), or record `sparkle_talk.ogg` / `sparkle_win.ogg`; add a second pulsing star over each pinning bunny (positions (445,300)/(579,300) art) | `castle_rooms_25d.gd:1859-1862,4218-4220,4169-4194` | chirp-only → chirp + spoken instruction; 1 pointer → 3 | The objective gets a real voice line and the pointer sits on the thing to bump |
| 3 | Hand off from the pool like the bathroom does: on `day_one_complete_pool_scene` show the "A new picture door is glowing!" banner + `_say`, and/or a Playroom route picture button (reuse `_show_day_one_pool_route` with target `playroom`), and on Main Hall re-entry tween the hall camera to the PLOT door | `main.gd:7304-7320`, `7562-7590`; `castle_rooms_25d.gd:2318-2323,4251-4270` | no cue, door off-screen → banner + button + auto-pan | Removes the only silent no-pointer span in the beat |
| 4 | Show the adopted friend in the castle: stage a `Sprite2D` cutout of the companion (reuse `_add_creature_preview` layers) beside Roshan on `castle_room_item_visual_layer`, re-positioned in `_position_player_at_foot`; or at minimum keep the 🧸 badge visible in the castle by parenting it to the castle stage | `companion.gd:192-196,242-246`; `castle_rooms_25d.gd:2194-2260` | invisible until after the boss → visible immediately | The reward of the beat becomes visible the moment she earns it |
| 5 | Convert the leftover 3D magnitudes: pointer bob `+0.28` → `+12.0` px; eagle farewell `position.y + 1.25` → `position.y - 80.0` over 0.72 s | `castle_rooms_25d.gd:4187,4228` | 0.28 px / +1.25 px → 12 px / −80 px | The star visibly bobs and the eagle visibly flies up and away |
| 6 | During the rescue tutorial hide the "↩" close (or move it bottom-left and shrink the dim-close to nothing) and voice the step lines with distinct clips or `min_gap` 0 + distinct keys so the dedup guard cannot drop them | `companion.gd:719-724,612-614,645-650,656-658` | ↩ always shown; step lines share `roshan_talk.ogg` | Keeps her on the three-step path and lets each step speak |

## Confidence
- Proven by code: the whole playroom path — item placement and sizes
  (`222-248`, `3817-3827`, `2810-2816`), the input router and the three tap
  outcomes (bunny card / floor / wall-or-letterbox: `2115-2156`), walk speed 520
  px/s with 0.12–0.85 s clamp (`2225`), per-tick contact test during the tween
  (`1131`, `2244-2246`, `4036-4048`), the overlapping contact ellipses (computed
  from `(445,450)/(579,450)×1.25`, radii `(82,62)×1.25`), pop feedback and the
  TRIO gate (`4052-4111`), HitEngine chain (`378-390`), rescue completion, saves
  and the 0.72 s hand-off (`4196-4248`), the picker geometry and tutorial steps
  (`companion.gd:572-872`), the Day-One-scoped dead end (`main.gd:7140-7148` vs
  `castle_rooms_25d.gd:4763-4783`), companion invisibility in the castle
  (`companion.gd:192-196`), captions hidden in the castle (`967-968`,
  `main.gd:3590,3617`), voice resolution (`audio_director.gd:13-45,117-136`) and
  which clips exist (directory listing). `probe_stuffie.gd:80-206` independently
  confirms the half-rescue persistence and the picker opening on the second pop.
- Inferred: all timings that involve the child (child model), the camera settle
  (~1 s from weight δ×3.5), clip lengths (chirp ~1 s, `roshan_talk` 1–3 s), and
  whether `rumi_intro.ogg` exists (not checked). Rows 1–2, 4–5, 15–16 are taken
  from the protocol flow map and earlier runs, not re-traced here.
- Could not determine: what the boss stage does with the 3D companion —
  `dustboss` is not in `HIDE_GAMES` (`companion.gd:189-190`, `main.gd:703`), so
  `_tick_follower` will spawn the Node3D cutout and may show the 🧸 button during
  the fight if `hud_layer` is visible there; whether that is visible under the
  2D boss stage is unverified. Runtime hitch from two synchronous saves in one
  frame when both bunnies pop together (`4122`, `4206`, `main.gd:7331`) is
  plausible on a 3–4-year-old phone but unmeasured.

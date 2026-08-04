# Framing / pacing / animation audit — 2026-08-03

Owner playtest: framing looks terrible (audience row + black header); no ability to explore the backgrounds; Roshan is stiff and low-res.

---

## FRAMING

FRAMING AUDIT — Pearl Opera career worlds (`opera_career_world_2d.gd`)

Files read:
- `C:\Users\Peter\Documents\mermaid-roshan-reef\.worktrees\codex-opera-art-regeneration\scripts\opera_career_world_2d.gd`
- `C:\Users\Peter\Documents\mermaid-roshan-reef\.worktrees\codex-opera-art-regeneration\scripts\storybook_ui.gd`
- `C:\Users\Peter\Documents\mermaid-roshan-reef\.worktrees\codex-opera-art-regeneration\scripts\opera_world_backdrop_2d.gd`
- `C:\Users\Peter\Documents\mermaid-roshan-reef\.worktrees\codex-opera-art-regeneration\scripts\opera_stage_paths.gd`
- Painting: `...\assets\opera\worlds\backdrops\world_chef.png` (1024x576)
- Real captures (these are actual runtime frames, and they show exactly what the owner is complaining about):
  `C:\Users\Peter\Documents\mermaid-roshan-reef\.godot\opera_animation_review_20260803\stress\rapid_input_rest.png`
  `...\stress\early_reentry_01.png` (2560x1369; uniform scale 1.9014, logical viewport 1346x720 — verified: the code's `top` bar at design x 18..1262 measures at pixels 34..2400, an exact match, so every design-space number below is directly confirmed on screen)

===============================================================
1. WHAT IS WRONG — MEASURED
===============================================================
Screen budget: 1280 x 720 = 921,600 px².

TOP HUD STRIP (`_build_world`, lines 336-341)
```
top.color    = Color(0.025, 0.025, 0.11, 0.84)   # ~#060620 at 84% alpha
top.position = Vector2(18, 14)
top.size     = Vector2(1244, 124)
```
- 1244 x 124 = **154,256 px² = 16.7% of the screen**, spanning 97.2% of screen width, y 14..138 (top 19.2% of height).
- Its only always-on content is `title_label` at Rect2(24, 8, 1196, 38) inside the bar → absolute y 22..60. **The lower 78px of the bar (1244 x 78 = 97,032 px² = 10.5% of the screen) is pure empty black on every non-finale beat.**
- Everything else in the bar — `player_bar`, `rival_bar`, `score_label`, `timer_label`, `player_name_label`, `rival_name_label` — is hidden by `_set_finale_visible(false)` (lines 1000-1017). Chef has 7 beats and `FINALE_START["chef"] = 5`, so for **5 of 7 beats (71% of the career) 154,256 px² of near-black covers the painting to display one line of 28px text a non-reader cannot read.**
- Even in the finale the bar's actual ink (2x 430x28 bars + 304x42 + 264x30 + 2x 430x28) fills under 15% of its own area.

AUDIENCE ROW (`_build_audience`, lines 605-620)
```
fan.position = Vector2(18.0 + float(index) * 207.0, 592.0)
fan.size     = Vector2(116, 126)
fan.modulate = Color(1.0, 1.0, 1.0, 0.96)
```
- Union band: x 18..1169, y 592..718 → 1151 x 126 = **145,026 px² = 15.7% of the screen**. Portrait boxes alone: 6 x 116 x 126 = 87,696 px² = 9.5%.
- `crowd_label` at Rect2(430, 595, 420, 42) (line 496) **overlaps portraits 3 and 4** (fan[2] x 432..548, fan[3] x 639..755, both y 592..718). The game's audience-energy readout is drawn on top of its own audience.

TASK CARD (`action_panel`, built line 403-410, resized in `_apply_panel_layout` line 742)
- `action_panel.size = Vector2(440, 384)` = **168,960 px² = 18.3% of the screen**, opaque (`draw_rect(rect.grow(-20.0), Color("#e6f5ff"), true)` + `task_card_frame.png` on top, line 553-555).
- `_card_position_near_station()` (line 751-761) clamps `pos.y = clampf(pos.y, 150.0, 720.0 - 384.0 - 130.0)` → **y ∈ [150, 206], a 56px range**. The card is permanently pinned in the sliver between the black bar (ends 138) and the audience row (starts 592). "Docks beside the station" is a fiction — chef's stations sit at y 382..432 and the card never goes there.

TOTALS
- Chrome with card visible: 154,256 + 145,026 + 168,960 = **468,242 px² = 50.8% of the screen.**
- Vertical chrome bands: 124px top + 126px bottom = 250px of 720 = 34.7%; counting the unusable 14px and 2px slivers, 266px = **36.9% of screen height is edge-to-edge furniture.**
- Painting that survives: a 1280 x 454 letterbox band (y 138..592) minus the card = **412,160 px² = 44.7%**, and it is a C-shaped ribbon, not a picture.

WHICH 44.7% SURVIVES — the worst part
In `world_chef.png` (1024x576 → x1.25 into 720-space): red curtain valance y 0..37; skyline of pastel cake-castles y 37..287; the raised pastry platform (the playfield) y 287..500; the ornate scalloped foreground counter with fruit bowls, cream swirls and piping bags y 500..720.
- The top bar (14..138) covers **100% of the painted curtain valance and ~40% of the skyline.**
- The audience row (592..718) covers **57% of the foreground counter — the most detailed, most expensive band in the painting.**
The two bands the chrome eats are precisely the two bands that make it read as a painting rather than a diorama.

SCALE — the card is bigger than the hero
`player_actor.size = Vector2(250, 288)`, texture `roshan_chef.png` is 512x512, `STRETCH_KEEP_ASPECT_CENTERED` → drawn 250x250 with 19px letterbox top/bottom. `_place_on_stage` at chef station "mixing_bowl" (0.28, 0.6) → feet (358, 432), depth = 0.62 + 432/720*0.55 = 0.95 → **Roshan renders ~238x238 = 56,644 px². The task card is 168,960 px² — 2.98x the on-screen area of Mermaid Roshan.** Her hat crown lands at design y≈188, only 50px below the black bar; in `rapid_input_rest.png` her chef's hat visually touches it.

TWO MORE THINGS COVERING THE PAINTING
- `shade` (lines 325-329): a full-rect ColorRect `Color(0.025, 0.025, 0.11, 0.10)` — a **10% navy wash over the entire painting, permanently**, for no gameplay reason.
- `_draw_spotlights()` in `opera_world_backdrop_2d.gd` (lines 183-194): two ~220x620 accent-tinted polygons at alpha 0.08–0.13 drawn over the painting on **every** career world, not just the stage. The chef world already has painted lanterns and warm hearth light; these add a second, contradictory light source.

THE PAINTING DOESN'T EVEN REACH THE EDGES
Measured on `rapid_input_rest.png` (rows 300..1300, excluding the bar): sharp painted content spans x 130..2330 of 2560 → **design x 68..1225 of a 1346-wide viewport. A 68px blurred smear column on the left and a 121px one on the right.** Confirmed baked into the source art, not the code: in `world_chef_c0r0.png` (1024x1024) the sampled region `Rect2(0, 448, 1024, 576)` has near-zero gradient (0.1–0.4) across columns 0..200 while real detail (3–8) starts around column 850. Hand this to the art auditor — but visually it reads as a third band of dead framing.

Side note for whoever touches the card: `task_card_frame.png` is 1024x1024 drawn via `draw_texture_rect(task_frame_texture, Rect2(0,0,440,384))` — a **15% anamorphic vertical squash** of a square ornate frame. Also, because that branch returns at line 555, the entire hand-built storybook frame below it (lines 556-577) is dead code in shipping.

===============================================================
2. WHY IT LOOKS BAD — THE SPECIFIC VIOLATIONS
===============================================================
a) **An opaque black bar is the one thing you may never put over a painting.** At alpha 0.84 over pastel art the bar is effectively opaque; it has square corners, no border, no shadow, and it is a raw `ColorRect`, not a `Panel`. It reads as a video-player letterbox or a debug overlay, not as part of the world.

b) **It uses the game's "screen is disabled" colour as decoration.** `StorybookUI.DIM = Color(0.025, 0.06, 0.16, 0.76)` is the modal scrim. `top.color = Color(0.025, 0.025, 0.11, 0.84)` is the same family, darker and more opaque. Every other screen in the game teaches the child "dark wash = frozen/modal"; the career world flies that colour permanently as a header.

c) **The UI ignores StorybookUI entirely.** `storybook_ui.gd` defines the language: `panel_style()` → PAPER `Color(0.94,0.98,1.0,0.98)` fill, border = `accent.lerp(PURPLE_DEEP, 0.62)` at 5px, `set_corner_radius_all(34)` (HUD: 30/4px), shadow `Color(0.19,0.10,0.48,0.34)` size 14 offset (0,8); `add_shell_crest()` 116x82 on the top edge; four pearls at the corners; `style_label()` = INK `Color(0.20,0.18,0.48)` with a **white outline** (`font_outline_color Color(1,1,1,0.75)`, `outline_size 4`); `MIN_TOUCH 110x110`. The career world instead uses a local `_label()` helper (lines 296-306) with gold/white/pink text and a **hard black drop shadow** `Color(0.03,0.02,0.12,0.92)` offset (3,3), and bare `ProgressBar.new()` with no theme override at all — Godot's default grey bar, the single most "engine default" thing that can appear in a children's game.

d) **The screen contradicts itself.** `_draw_task_card()` (lines 546-577) is written in perfect storybook — `#e6f5ff` paper, 5px `#4b33a0` contour, radius 44, violet shadow, gold ribbon, corner pearls. It sits 12px below an engine-default black letterbox bar. One screen, two design systems.

e) **The portraits are cutouts on a different rendering style.** Measured source sizes: `daddy.webp` 727x1024 (aspect 0.71), `huluu.png` 640x1039 (0.62), `mama_baby.png` 393x479 (0.82), `flower_friend.png` 389x460 (0.85), `wacky_chuck.png` 339x500 (0.68), `two_friends.png` 480x460 (1.04). All six are forced into the same 116x126 box with `STRETCH_KEEP_ASPECT_CENTERED`, so they render at **78, 85, 89, 103, 107 and 116px wide** — a 49% width spread at the same nominal depth. There is no scale rule. They are photo-derived faces at 100% opacity with hard cut edges, pasted onto a soft painterly render with atmospheric perspective. It is the loudest style break on the screen.

f) **The audience is in front of the performers.** The fans are the **last** children added to `root` (line 619, after `combat_layer`, `combat_fx`, `lens_layer`, actors and props). They occlude Roshan, the imps and every FX burst. An audience that stands in front of the act is not an audience. `_bop_burst_at()` and `celebrate()` then add confetti to `root` too, landing above the fans — the layering is accidental, not designed.

g) **They have no ground contact.** Every other figure is placed by `_place_on_stage()` — feet on `stage_points`, depth scale, flip. The fans get `position = Vector2(18 + i*207, 592)`: no path, no depth, no shadow, no occlusion. They float in the pastry display.

h) **Four text elements and two progress readouts aimed at a non-reader, all duplicating the art.**
   - `title_label` "PASTRY CHEF MINIGAMES" — the largest object on screen, unreadable to the player. The painting already says cake kingdom (giant tiered cake, whisk, macarons) and `m.show_msg()` already speaks it.
   - `player_name_label` "MERMAID ROSHAN" / `rival_name_label` "CHEF IMP" — naming two characters visibly on screen.
   - `score_label` "000 ★ 000" and `timer_label` "⏳ 02" — numerals.
   - `phase_label` "★ POUR" — the widget art already shows the bowl pouring.
   - `phase_fill` ProgressBar duplicates `surface.set_fill(progress)`, which the code's own comment (lines 1046-1049) says already fills the widget art: *"the bowl actually pours, the basin actually fills."* Two readouts of one number, one of them un-themed.
   - `crowd_label` "● ● ● ● ●" duplicates the audience row and is drawn on top of it.

i) **The permanent 10% navy `shade` mutes the very art the owner wants to show off**, and the code-drawn spotlight wedges add a light source the painter did not intend.

===============================================================
3. THE REDESIGN — LET THE PAINTING BREATHE
===============================================================
Principle: **the painting is the interface.** Nothing opaque may touch a screen edge. Every survivor is either deleted, restyled into a small floating storybook plaque with ≥24px margin and a shadow, or pushed into the painting itself.

--- DELETE OUTRIGHT (all in `_build_world` unless noted) ---
1. `top` ColorRect, Rect2(18,14,1244,124) — the whole bar. Reparent survivors to `root`.
2. `title_label` (line 343) — a non-reader gets identity from the painting and the VO.
3. `player_name_label`, `rival_name_label` (lines 366-373).
4. `timer_label` (line 362) — and drop the detective countdown entirely; a clock is the opposite of contemplative pacing.
5. `score_label` (line 358) — no numerals.
6. `crowd_label` Rect2(430,595,420,42) (line 495) — overlaps the audience and duplicates it.
7. `phase_fill` ProgressBar (392x34, line 447) — `surface.set_fill(progress)` is the only progress signal needed.
8. `shade` full-rect ColorRect (lines 325-329) — stop muting the art. If focus dimming is ever needed, use `StorybookUI.add_dim()` as a genuine modal.
9. The six-portrait `audience` array as currently built (lines 605-620) — see §4.
10. `_draw_spotlights()` in `opera_world_backdrop_2d.gd` — gate it behind `if stage_mode:` so it only fires for the proscenium finale, where a spotlight is diegetic.

--- RESTYLE INTO STORYBOOK (only two survivors) ---
11. **Progress pearls, top-left, finale only.** Replace `player_bar`/`rival_bar` with:
```gdscript
var plaque := StorybookUI.add_hud_panel(root, Rect2(24, 22, 300, 92), accent, StorybookUI.PAPER, 30)
StorybookUI.adorn_panel(root, Rect2(24, 22, 300, 92), "OperaProgress")
# player: 7 pearls, one per phase
for i in range(phases.size()):
    StorybookUI.add_pearl(plaque, Vector2(38 + i * 38, 40), 22, "PhasePearl%d" % i)
# rival: smaller echo row, competitive careers only
for i in range(phases.size()):
    StorybookUI.add_pearl(plaque, Vector2(38 + i * 38, 70), 14, "RivalPearl%d" % i)
```
Filled = `PEARL_BLUE`, unfilled = `MUTED` at 0.35 alpha. Rival row visible only when `not competition.is_cooperative() and phase_index >= _finale_start()`. No numbers, no words — "three pearls lit, four to go" is instantly legible at four years old. Footprint **300x92 = 27,600 px² = 3.0%** (down from 16.7%), and at x=24 it clears the chef skyline's hero cake-castle (centred near design x 640).

12. **Task card — shrink, unstretch, and let it move.**
   - Size `Vector2(440, 384)` → **`Vector2(352, 286)` = 100,672 px² = 10.9%** (down from 18.3%). Interior: `surface.position = Vector2(20, 62)`, `surface.size = Vector2(312, 200)` — still nearly 3x `StorybookUI.MIN_TOUCH`.
   - Fix the frame squash: draw `task_card_frame.png` through a `NinePatchRect` with `patch_margin_*` ≈ 180 so the ornate corner shells keep their 1:1 aspect instead of being crushed 15% vertically.
   - Delete the hand-rolled fallback (lines 556-577) and call `StorybookUI.panel_style(accent, StorybookUI.PAPER, 34, 5)` instead, so the card can never drift from the menus.
   - `phase_label` becomes **icon only** at 56px — the phase dicts already carry `"icon"` ("●", "↻", "★", "〰"). Style with `StorybookUI.style_label(phase_label, 56, StorybookUI.INK, 4)` — INK + white outline, never gold-on-black + drop shadow.
   - `action_panel.modulate.a = 0.96` at idle, tween to 1.0 while a finger is down: a card that wakes up rather than a hole punched in the picture.

13. **Card placement — open the clamp.** In `_card_position_near_station()`:
```gdscript
pos.x = clampf(pos.x, 24.0, 1280.0 - 352.0 - 24.0)   # [24, 904]
pos.y = clampf(pos.y, 96.0, 720.0 - 286.0 - 40.0)    # [96, 394]  (was [150, 206])
```
The y range goes from 56px to 298px, so the card genuinely follows the station up and down the walkway instead of sitting in the same slot every beat.
Add the constraint the code currently lacks, in the spirit of the project's no-overlap rule: after computing `pos`, if `Rect2(pos, card_size)` intersects `player_actor`'s screen rect grown by 40px, flip the card to the far side of the station (`anchor.x < 640` → `+60` becomes `-(card_w + 60)`). **The card must never cover Roshan.**

--- MAKE DIEGETIC (into the painting, not over it) ---
14. **Career identity** — already painted. Nothing to add.
15. **Progress lives in the world.** `station_nodes` and `_draw_station_marker()` (lines 580-593) already exist. Give the marker three states instead of two: `later` (dim, `Color(1,1,1,0.22)`), `current` (the existing gold pulse), `done` (a steady warm halo, no pulse, `Color(1.0, 0.86, 0.42, 0.45)`). The child then reads her progress by looking at the *world* — lanterns lit behind her, one ahead still waiting. Zero new screen furniture, and it is exactly the slower, look-around register the owner asked for.
16. **The stolen prop.** `prop_rect` at a hardcoded `Vector2(890, 330)` for all 13 careers lands on whatever the painting happens to have there. Add a `"workbench"` point to each career's `PATHS` entry in `opera_stage_paths.gd` and place the prop on a painted surface. Keep the theft-flee tween (lines 715-721) — it's the best diegetic beat in the file.
17. **Audience energy** → the silhouette gallery, §4(c).

--- DRAW ORDER (new `root` child order; index 0 added first = furthest back) ---
```
0   backdrop_node        full rect          painting; spotlights gated to stage_mode
1   station_nodes[]      walkway markers    diegetic progress
2   prop_rect            per-career workbench point
3   audience_layer       full rect          silhouette gallery / curtain-call fans — BEHIND the actors
4   rival_actor          feet on stage_points
5   player_actor         feet on stage_points
6   combat_layer         full rect, imps, MOUSE_FILTER_STOP during bop
7   combat_fx            full rect, no input
8   lens_layer           full rect
9   action_panel         352x286 storybook card, moves with the station
10  progress_plaque      Rect2(24, 22, 300, 92), finale only
11  fx_layer             full rect, MOUSE_FILTER_IGNORE — new parent for _bop_burst_at + celebrate confetti
```
Two changes carry most of the weight: the audience moves from **last** (in front of everything) to **slot 3** (behind every actor), and confetti/puffs get their own `fx_layer` parent so `_bop_burst_at()` (line 1102) and `celebrate()` (line 1240) stop appending above the fans.

--- RESULT ---
| | before | after |
|---|---|---|
| top strip | 154,256 px² (16.7%) | 27,600 px² (3.0%), floating plaque |
| audience row | 145,026 px² (15.7%) | 0 during play; diegetic silhouette at finale |
| task card | 168,960 px² (18.3%) | 100,672 px² (10.9%), mobile |
| **total chrome** | **468,242 px² (50.8%)** | **128,272 px² (13.9%)** |
| **painting visible** | **412,160 px² (44.7%)**, a C-shaped ribbon, skyline and foreground apron destroyed | **793,328 px² (86.1%)**, full-bleed to all four edges, skyline and foreground apron intact |

===============================================================
4. THE AUDIENCE — SHOULD IT EXIST AT ALL?
===============================================================
**Verdict: remove the six-portrait row from the career worlds entirely. Bring the family back only at the curtain call, and even then as characters standing on the painted floor — never as a permanent row of cutouts.**

WHY IT HAS TO GO
- **Style break.** Photo-derived faces at 100% opacity with hard cut edges, in front of a soft painterly render with atmospheric perspective. Nothing else on screen looks like them.
- **No scale rule.** Six source aspects from 0.62 to 1.04 forced into one 116x126 box → rendered widths 78, 85, 89, 103, 107, 116px at the same nominal depth. They read as six stickers of arbitrary size.
- **No ground contact, wrong depth.** Raw `position` instead of `_place_on_stage()`; last in draw order so they occlude Roshan, the imps and the FX.
- **The world isn't a theatre for most of the career.** `backdrop_node.set_stage(phase_index >= steal_index)` — chef's `steal_index` is 4, so beats 0–3 are explicitly backstage/in-the-district. `world_chef.png`'s foreground is a pastry counter with fruit bowls and piping bags. Six people standing in the dessert display is a category error, and it costs 145,026 px² (15.7%) placed over the painting's best band.
- **It vandalises itself.** `crowd_label` "● ● ● ● ●" is drawn across portraits 3 and 4.

(a) **Beats 0 … finale-1: no audience at all.** These are "learn the job / do the job" beats in a working world. Emptiness at the bottom of the frame is not a gap to fill — it is what lets the painting breathe, and it is precisely the slower, contemplative register the owner asked for in note 2. The screen below y=592 returns to 100% painting.

(b) **Finale beats only: one painted, silhouetted gallery — at the back, below the footlights.**
- One asset, not six: `assets/opera/worlds/ui/audience_gallery.png`, a 2048x256 painted strip of the family crowd rendered in the world's own painterly style — heads and shoulders in shell-box seats, backlit, values held at roughly 30–40% luminance so it never competes with the act.
- Drawn **inside `_draw_stage_frame()`** in `opera_world_backdrop_2d.gd`, i.e. as part of the painting layer (slot 0), not as a UI child. `_draw_stage_frame()` already puts the footlight apron at `size.y - 132` with a brass line at `size.y - 108`; the audience belongs *below* the footlights, in `Rect2(0, 612, 1280, 108)`. Because it is a dark silhouette behind the footlight line, it costs the viewer nothing — it *is* the frame, and it makes the composition read "we are sitting in the house, looking at the stage."
- Visible only when `stage_mode == true`, so it appears exactly when the curtain rises — a payoff, not wallpaper.

(c) **Audience energy re-bound to the silhouette.** `competition.audience_energy()` currently drives `crowd_label`. Point it at the gallery instead: at low energy the silhouette is still; above 0.36, three heads bob on `sin(elapsed * 3.0 + i * 1.7) * 6.0`; above 0.72, five heads bob and small warm pearl-glows (`StorybookUI.GOLD`, 10px, alpha 0.6, rising 40px over 1.2s) drift up from the row. No text, no dots, no numbers — the crowd itself is the meter.

(d) **The six family portraits appear once: at the curtain call.** `celebrate()` (line 1204) is the one moment they earn the screen — the world has stopped, and the child wants to see Daddy and Huluu clapping for her. Move their construction out of `_build_world()` into `celebrate()`, and fix the presentation:
```gdscript
# normalise to ONE height so they are six characters at one distance,
# not six stickers of arbitrary size
var tex := load(portrait_path) as Texture2D
var h := 190.0
fan.size = Vector2(h * float(tex.get_width()) / float(tex.get_height()), h)
# stand them ON the painted floor, same depth rule as everyone else
_place_on_stage(fan, StagePaths.point_along(stage_points, 0.10 + float(index) * 0.16))
# soft contact shadow, or they still float
# ellipse at the feet: Vector2(fan.size.x * 0.7, 22), StorybookUI.PURPLE_DEEP at alpha 0.22
```
- Insert them at **slot 3**, behind `rival_actor` and `player_actor`, so Roshan stays the front-most figure in her own bow.
- Fade in: `modulate:a` 0 → 1 over 0.5s with a 0.06s per-index stagger, *then* run the existing bounce tween (lines 1221-1226). An audience that **arrives** for the bow is an event; an audience that has been standing in the dessert case for four minutes is set dressing.

HANDOFFS TO THE OTHER AUDITORS
- Art: `world_chef_c0r0.png` (and presumably the other 12 tile sets) has a featureless/blurred left margin baked into the sampled region — measured gradient 0.1–0.4 across columns 0..200 vs 3–8 in the detailed area — which produces the 68px / 121px blurred smear columns visible at the screen edges in `rapid_input_rest.png`. Also `opera_world_backdrop_2d.gd` line 67 documents a "2048-square master" while the shipped tiles are 1024x1024; the source rects happen to land close enough that the world reads correctly, but the comment and the assets disagree and should be reconciled.
- Animation: with the black bar gone, Roshan's headroom goes from 50px to 188px, and the card shrinking from 168,960 px² to 100,672 px² takes her from 0.34x the card's area to 0.56x. The framing change alone will not fix stiffness, but it stops actively shrinking her — and every pixel freed above y=138 and below y=592 is room for the `roshan_25d` sprite set to actually move through.


---

## PACING & EXPLORATION

CONTEMPLATIVE MODE — pacing/exploration design for the Pearl Opera career worlds

Files read: `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/scripts/opera_stage_paths.gd`, `.../scripts/opera_career_world_2d.gd` (1724 lines), `.../scripts/opera_world_backdrop_2d.gd`, `.../scripts/roshan_sprite_loop.gd`, `.../scripts/player.gd`, `.../scripts/arena/castle_rooms_25d.gd`, `.../scripts/interaction_affordance.gd`, `.../scripts/interaction_director.gd`, `.../scripts/probe_opera_2d_balance.gd`, `.../OPERA_WIDGET_INPUT_AUDIT_2026-08-02.md`, `.../OPERA_STAGE_INTERACTION_2026-08-02.md`, `.../OPERA_ACT_PACING_2026-07-25.md`, `.../CODEX_OPERA_ANIMATION_HANDOFF_2026-08-03.md`.

THE ONE-SENTENCE FRAME
Every painting was authored as a left-to-right journey ("entry at the left, a continuous route to the right", `opera_stage_paths.gd:5-7`) with five stops on it — and right now the child never travels it: `_glide_roshan_to()` (`opera_career_world_2d.gd:596`) teleports Roshan to the next station in 1.3 s of tween while a card opens on top of her. The contemplative mode is not new content; it is **giving the child the journey the paintings already contain**.

---

## 1. FREE WALK

**Input — tap-to-walk, drag-to-lead. No stick, no D-pad.**
- Tap anywhere on the painting → she walks to `_stage_feet_at_x(tap.x)` (`opera_career_world_2d.gd:1306`). That helper already snaps an arbitrary x onto the painted walkway, interpolates the route's y, and clamps to the route's first/last x ±40 px. Use it rather than `StagePaths.nearest_t()` for the destination: the imps already move by this exact rule (`_tick_stage_combat:1284-1288`), so **Roshan and the imps obey one identical walkway law** and she can never stand in water, in a flower bed, or off-screen.
- Hold and drag → the destination follows the finger continuously (same event shape as `_lens_input:1589-1606`, which already handles touch + drag + mouse for a full-stage drag). A 4-year-old who does not understand "tap there" will discover "drag her along" by accident, and both land in the same code path.
- A tap that lands on nothing still sparkles: reuse `_bop_burst_at(pos, true)` (`:1091`) — the kind fizzle already used for stray bops. No touch is ever inert.

**Speed — 250 px/s cruise, 0.30 s ease in and out, no minimum trip length.**
Do *not* buy "contemplative" by making her slow; at 1280 px wide a slow walk reads as input lag. The chef route is ~1009 px end to end, so 250 px/s is ~4.0 s for the whole world and ~1.2-1.6 s for a typical leg. Contemplation comes from removing the auto-advance, not from sluggish travel. Precedent: castle uses `duration = clampf(distance / 520.0, 0.12, 0.85)` (`castle_rooms_25d.gd:1537`); 250 is deliberately half that because the opera stage is a promenade, not a room she crosses to reach furniture. Drive it with `move_toward` in `_process` rather than a tween so she can be re-aimed mid-stride — the castle tween cannot be interrupted cleanly, and an uninterruptible walk is the one thing that feels broken to this age.
Per frame: recompute depth with the existing `_place_on_stage` formula (`:515`, `depth = clamp(0.62 + feet.y/720 * 0.55, 0.62, 1.1)`) and set `flip_h` from travel direction exactly as `_glide_roshan_to:599` already does.

**Animation — three lines, already shipped.** `player_actor` is a `TextureRect`; `RoshanSpriteLoop.setup_texture_rect()` (`roshan_sprite_loop.gd:56`) drives a `TextureRect` off the 16-frame swim atlas with per-frame region correction, and `opera_act.gd:5553-5555` already does precisely this for the farm cutaway. Call `set_moving(true)` while travelling and `set_moving(false)` on arrival (`roshan_sprite_loop.gd:93`) — the loop then swaps `roshan_swim_front` (8-12 fps, speed-scaled) for the breathing directional idle by itself. Pass `back_view = true` while her destination is upstage of her (target.y < feet.y − 24) to get `roshan_swim_back`. This single change is what makes free walk read as *walking* instead of sliding, and it is the pacing design's hard dependency on the animation workstream.

**What she can approach (four classes, all already in data):**
| Class | Source | Response |
|---|---|---|
| 5 task stations | `StagePaths.stations()` — anchored to real painted landmarks | active one invites (below); inactive ones give a twinkle + her `look` gesture |
| 8 painted details | `StagePaths.clue_spots()` | the discovery layer, section 2 |
| the goal prop | `prop_rect` at (890,330), visible from phase 1 until the theft (`:712-724`) | walk under it → `look`; it bobs. It is the thing she is about to lose, and she should have met it |
| the partner | `rival_actor` (Faron in nursery, `:379-388`) | walk to him → `wave` |

**How a station invites without forcing.**
The active marker already pulses (`_draw_station_marker:580-593` — `station_marker.png`, `pulse = (sin(elapsed * 4.2) + 1) * 0.5`, gold when `station_for_phase[phase_index] == index`). Layer the house touch vocabulary on it: `InteractionAffordance.color(INTERACTION, focused)` — deep-blue breath means "a real activity lives here", gold twinkle means "a local animation lives here" (`interaction_affordance.gd:5-8`). That gives the child a two-colour, non-reading legend that the castle already taught her.
Arrival is a **dwell, not a trigger**: when her feet come within 150 px of the active station and stay there 0.35 s, the marker snaps to focus, a soft chime plays, and the task card opens via the existing `_apply_panel_layout()` / `_card_position_near_station()` (`:732`, `:751`). Brushing past does not yank her into work; she can turn around at any point before the dwell completes and nothing is lost. This is the same dwell grammar as the lens (0.45 s in 96 px, `:1628`) — the audit's #1-ranked mechanic — reused for locomotion.

---

## 2. THINGS TO FIND

The 8 `clue_spots` per career are already coordinates of specific painted details, derived visually from each painting (`opera_stage_paths.gd:8-14`) and spread deliberately across the whole frame — chef's include ceiling bunting at (0.42,0.095), the far-left prop at (0.073,0.185) and the bottom corners (0.085,0.815) / (0.94,0.775). They are currently used by exactly two detective phases and are dead art in the other eleven careers.

**Make them touchable during every wander window.** Three tiers, escalating, all reusing shipped code and zero new art:

- **Tier A — the painting itself responds (all 8 spots, unlimited repeats).** Tap within 84 px of a spot → the painted detail *bulges*: `backdrop_node.painting` is a public `Texture2D` (`opera_world_backdrop_2d.gd:35`) and the backdrop already draws region crops with `draw_texture_rect_region` (`:66-77`). A discovery layer redraws a ~160 px patch of the painting at 1.0 → 1.10 → 1.0 over 0.45 s with a 3° wobble, plus `_bop_burst_at(spot, false)` (`:1091`, uses the shipped `fx_bop_puff` card) and a chime. The bird flutters *because it is that bird*, cropped from the painting and animated. This is the whole trick: it works for 13 careers × 8 details = 104 responsive details with no asset request at all.
- **Tier B — three of the eight are collectible.** Rotate which three with the offset trick already written for the lens (`offset = phase_index * 3`, `_start_lens_phase:1580-1586`). First touch drops a pearl into a small found-strip and leaves a permanent gentle glint at the spot — the exact draw `_draw_lens_layer:1641-1643` already does for `lens_found`. Collection is the strongest single motivator at 4 (the audit says so of the nursery cradle, `OPERA_WIDGET_INPUT_AUDIT` Appendix B, rank 3).
- **Tier C — proximity makes it a character beat.** If her feet are within ~220 px of the touched spot she plays a gesture from the 2.5D set — `point` / `look` / `giggle` / `collect` (`player.gd:99-107`, rows `gesture_b:3`, `gesture_b:0`, `gesture_b:1`, `gesture_c:0`), advanced with `_set_classic_sequence`-style row×4+phase indexing (`player.gd:343`). If she is far, only the painting responds. **That contrast is the entire teaching mechanism for free walk** — the child learns "go over there first" with no instruction, no arrow and no words.

Rules: discovery is never scored, never gates a phase, never appears on the HUD, and is only live during wander windows and the curtain call (during a task, the card owns input — the same `mouse_filter` gating that `combat_layer` already does at `:795` and `:849`).

Reusable inventory, named: the lens dwell + reveal-radius constants (96 px / 118 px / 0.45 s, `:1620-1649`), `_bop_burst_at` (`:1091`), `_bounce_actor` (`:1158`), the five FX cards already loaded in `_build_world` (`fx_stolen_sparkle`, `fx_dust_puff`, `fx_telegraph_ring`, `fx_slash_arc`, `fx_dizzy_stars`, `:474-479`), `StagePaths.clue_spots()` (`:192`), `InteractionAffordance` statics, and `LivingWorldCanvas` (`scripts/living_world_canvas.gd`, a bounded input-transparent `Control` with `configure()` / `set_motion()`) if ambient drift is wanted on top.

---

## 3. THE RHYTHM

Target ~2:05 of real play. The act keeps its canonical five-beat arc (scuffle → learn → do → theft → finale); what changes is that **the two fast beats are now bracketed by slow ones instead of sitting end to end.**

| Beat | now (median child) | proposed | change |
|---|---:|---:|---|
| Arrival — world fades up, she stands at t=0.08, three details twinkle in turn, free walk live before anything is asked | ~1 s | **14 s** | new slow beat |
| IMPS! scuffle — crew 5 → **3**, and they do not engage until she walks to them | ~11 s | 8 s | −3 |
| Wander → station 1 | 1.3 s glide | **7 s** | +6 |
| Task 1 (goal −25 %, completion hold 0.9 → 1.3 s) | 12 s | 9 s | −3 |
| Wander → station 2 | 1.3 s glide | **7 s** | +6 |
| Task 2 | 12 s | 9 s | −3 |
| Wander → station 3 | 1.3 s glide | **7 s** | +6 |
| Task 3 | 12 s | 9 s | −3 |
| THE CHASE — crew 8 → **6** + captain (his 2 bops stay reserved) | ~26 s | 19 s | −7 |
| Finale A on stage (goal −20 %) | 13 s | 11 s | −2 |
| Finale B on stage | 13 s | 11 s | −2 |
| Curtain call — confetti runs, free walk stays live, friends and details still respond | ~6 s | **12 s** | +6 |
| **Total** | **~109 s** | **~123 s** | +14 s |

Self-paced share goes from ~4 % (three 1.3 s glides) to ~40 % (47 s of arrival, wander and curtain call). The act gets *slower to inhabit* while getting only 14 s longer.

**What gets cut to pay for it:** opening crew 5→3 imps; chase crew 8→6; every non-combat `goal` in `PHASES` (`:36-151`) down 20-25 % (e.g. chef POUR 5.0→3.8, STIR 4.0→3.0, BAKE 6.0→4.5); the dead 1.0 s `phase_gap` between phases (`:661-664`) is deleted outright — the wander window replaces it, so the pause becomes playable instead of blank. Nothing is cut from the finale's *shape*, only its length; the 2.6 s curtain sting at `_finale_start()` stays (it is the act's one earned held breath).

**Probe impact:** `probe_opera_2d_balance.gd` pumps gestures and never wanders, so its measured time will *drop* to roughly 85-100 s — still inside `BAND_LO 70` / `BAND_HI 150` (`:16-17`). Say so in the commit, or the band will read as a regression. The band's own note already concedes it excludes "explore" time (`:12-15`).

---

## 4. WHAT ALREADY SUPPORTS THIS (assembly, not invention)

| Need | Already exists | Where |
|---|---|---|
| Walkable geometry per career | 9 waypoints, arc-length `point_along`, `nearest_t`, `path_length`, safe fallback | `opera_stage_paths.gd:162-251` |
| Snap any x to the walkway | `_stage_feet_at_x()` — the rule the imps already walk by | `opera_career_world_2d.gd:1306-1324` |
| Depth-correct standing | `_place_on_stage()` / the depth term in `_glide_roshan_to` | `:515-519`, `:596-602` |
| Where she is now | `_hero_feet()` | `:1298-1303` |
| Station data + markers + pulse + per-phase assignment | `station_list`, `_assign_stations`, `_build_station_markers`, `_draw_station_marker` | `:522-593` |
| Card docked beside the station | `_card_position_near_station()` | `:751-761` |
| Full-stage drag input on a `Control` overlay, with `mouse_filter` gating | `_lens_input` + the STOP/IGNORE flips on `combat_layer` | `:1589-1606`, `:795`, `:849` |
| Dwell-to-collect, the best-ranked mechanic in the suite | `_tick_lens` (96 px, 0.45 s) + `_draw_lens_layer` twinkle/found states | `:1609-1664` |
| Sparkle burst, kind fizzle, bounce | `_bop_burst_at`, `_bounce_actor` | `:1091`, `:1158` |
| Roaming characters on the painted route (proof the route works at runtime) | `_tick_stage_combat` + `ImpAI` ring→walkway projection | `:1246-1294` |
| Tap-to-walk on a painted 2D stage | `_on_room_input` → `_walk_cutout_to` → `_position_player_at_foot` (clamped walk rect, depth lerp, `set_meta("walking")`, shadow) | `castle_rooms_25d.gd:1437-1569` |
| Touch-a-thing-it-responds grammar | `_activate_room_item` / `_roleplay_prop_bounce` / `_item_burst` | `castle_rooms_25d.gd:1992-2091`, `:2655` |
| Animated Roshan on a `TextureRect` | `RoshanSpriteLoop.setup_texture_rect()` / `set_moving()` — 3 lines, already used in this very feature | `roshan_sprite_loop.gd:56,93`; `opera_act.gd:5553-5555` |
| Gesture rows for approach reactions | `ROSHAN_25D_GESTURES` + row×4 sequence indexing | `player.gd:99-113`, `:343-348` |
| Two-colour touch legend | `InteractionAffordance` gold=animation / blue=activity | `scripts/interaction_affordance.gd` |
| Region-crop drawing of the backdrop | `_draw_tile_set` already uses `draw_texture_rect_region`; `painting` is public | `opera_world_backdrop_2d.gd:35,66-77` |

Net new code: one `wander_layer: Control` (draw + input, ~120 lines), a walk integrator in `_process` (~40 lines), and a split of `_show_phase()` (`:648`) into `_arm_phase()` (light the station, play the teaser VO) and `_open_task()` (everything it does today). Everything else is wiring.

**Probe safety (must be in the build, or 287 checks break):** probes drive phases by pumping `_on_gesture` with `amount = 100` (`:1068-1069` comment). Guard it — if a gesture arrives while the world is in the wander state, call `_open_task()` immediately and then process the gesture. No probe edits, no new flags, all existing assertions hold.

---

## 5. THE RISK — and the gentle pull back

Two failure modes at 4: *lost* (she does not know where to go) and *bored* (she knows, but nothing pulls). Both are solved by escalating assistance, which is settled house law (fetch's widening safe zone; melody's verb gating; the audit's "trickle-by-assist, not trickle-by-payout", `OPERA_WIDGET_INPUT_AUDIT` §1).

**Bounded by construction — she cannot get lost:**
- One dimension of freedom. `_stage_feet_at_x` clamps to the route; there is no off-path, no off-screen, no water, no scenery to get stuck behind.
- Exactly one station is lit at a time (`station_for_phase`), so "where next" is never ambiguous.
- No timer, no score, no penalty is attached to wandering. Nothing counts down.

**The pull-back ladder (per wander window, clock resets on any touch):**
| t | What happens |
|---:|---|
| 0 s | Active station breathes blue; her teaser VO plays once ("The oven is warm — come see!") |
| 6 s | Marker grows ~15 % and gains a soft repeating chime; nothing else changes |
| 11 s | A **breadcrumb trail** of 4-5 sparkles appears along the route between her and the station — sample `StagePaths.point_along()` between `nearest_t(points, _hero_feet())` and the station's t. It is the path, drawn. Pure existing math |
| 16 s | The existing 9 s idle re-prompt fires her voice line again (`_process:1677-1684`) and the sparkles run *toward* the station in sequence, one per 0.25 s |
| 22 s | **Assist, never failure:** she walks there herself via the existing `_glide_roshan_to()` (`:596`) at the same 250 px/s, the card opens, and the VO says "Let's go together!" The child never sees a stall, and the ~2 min budget is bounded |

Also: any tap on the *lit* station from anywhere on screen sends her straight there — a child who understands the goal is never forced to route-plan. And discovery touches reset the idle clock, so a child who is happily poking at the painting is never nagged; the ladder only runs when the screen is genuinely still.

**One more guard for the curtain call:** free walk stays live under the confetti, but the win callback fires on a timer, not on her position — exploring must never be able to delay or skip the ending.

BUILD ORDER
1. `RoshanSpriteLoop.setup_texture_rect(player_actor)` + `set_moving()` — the walk cycle. Nothing else is convincing without it.
2. Walk integrator + `wander_layer` tap/drag using `_stage_feet_at_x`; keep `_glide_roshan_to` as the assist path.
3. Split `_show_phase()` into `_arm_phase()` / `_open_task()` with the 150 px / 0.35 s arrival dwell; delete `phase_gap` between non-combat phases; add the probe auto-open guard.
4. Tier A discovery (painting-patch bulge + burst) on all 8 clue spots; then Tier B collectibles, then Tier C proximity gestures.
5. Goal and crew-count retune per the table; re-run `probe_opera_2d`, `probe_opera_nursery`, and `probe_opera_2d_balance` and report the new sim band.

DEPENDENCY ON THE OTHER TWO WORKSTREAMS
The bottom-of-screen audience row (`_build_audience:605`, six 116×126 portraits at y=592) sits on top of the painting's bottom band and covers the bottom-corner clue spots (chef 0.085/0.815 and 0.94/0.775; ballerina 0.05/0.81; candymaker 0.17/0.90). If the framing pass removes or shrinks that row, the discovery layer gains those spots for free — worth sequencing framing first. Free walk is also the payoff argument for more Roshan sprites: with `set_moving()` wired, every additional authored row (a true walk, a lean-and-look, a reach) lands directly in the wander loop with no further engine work.


---

## ROSHAN ANIMATION

# ROSHAN ANIMATION INTEGRATION — opera career worlds

Files read (all absolute, worktree `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/`):
- `assets/characters/roshan_25d/README.md` — the sprite contract
- `assets/characters/roshan_25d/PROMPTS_4X.md` — the accepted generation prompts + identity locks
- `scripts/player.gd` — frame selection source of truth (`_tick_classic_sprite` :370, `_set_classic_sequence` :343, `_tick_always_alive_visual` :450)
- `scripts/roshan_sprite_loop.gd` — **an existing 2D `TextureRect` + `AtlasTexture` Roshan player, already in the repo**
- `scripts/roshan_sprite_frames.gd`, `scripts/roshan_sprite_anchors.gd` — the packing-drift correction tables
- `scripts/opera_career_world_2d.gd` — `_actor` :502, `_place_on_stage` :515, `_glide_roshan_to` :596, `_bounce_actor` :1158, `_hero_feet` :1298, `celebrate` :1204
- `scripts/opera_stage_paths.gd`, `CODEX_ROSHAN_SPRITE_REGENERATION_2026-08-02.md`, `CODEX_OPERA_ANIMATION_HANDOFF_2026-08-03.md`, `AGENTS.md`, `project.godot`

---

## 1. THE RESOLUTION PROBLEM — measured, not estimated

### The scaling chain nobody wrote down

`project.godot` is `window/stretch/mode="canvas_items"`, `aspect="expand"`, base `1280x720`. `AGENTS.md:135` names the target device: **Lenovo Tab M11 (1920x1200)**. So every 2D pixel authored in the 1280x720 design space is drawn at **1.5x on the actual tablet**. Every number below is given in both spaces.

### What the opera actually renders her at

`player_actor` is a `TextureRect`, `size = (250, 288)`, `EXPAND_IGNORE_SIZE` + `STRETCH_KEEP_ASPECT_CENTERED`, source `roshan_<career>.png` at 512x512. Keep-aspect fits a 1:1 source into a 0.868 box, so **she is drawn 250x250 with a 19px dead letterbox top and bottom — 13% of her own box is wasted.** Then `_place_on_stage` multiplies by `depth = clamp(0.62 + feet.y/720*0.55, 0.62, 1.1)`.

I ran the real `_place_on_stage` maths over all 60 painted stations in `opera_stage_paths.gd`. Measured alpha bbox of the 13 portraits is a consistent **488 rows tall** (y 16..504) and 362–482 wide.

| | design px | device px @1.5x |
|---|---|---|
| Her figure height, min (ballerina finale) | 196 | 294 |
| **median (all 60 stations)** | **227** | **340** |
| max (doctor recovery bed) | 254 | 381 |

488 source rows → 340 device rows = **1.44x supersampled**. **The opera portrait is not under-resolved. It is the single sharpest Roshan in the game.**

### Where she *is* under-resolved: the 3D game, today

`player.gd:188` sets `pixel_size = 7.4/256`, camera `fov 38` at boom `(25 back, 9 up)`. She subtends 40.4% of the viewport = 291 design px = **437 device px**, drawn from a 256px cell whose figure occupies ~230 rows. That is a **1.90x upscale**. The owner's "doesn't show in full resolution" is literally true — of the atlases, in the live 3D game, right now. The opera is the one place she is sharp, and it is sharp because it uses a 512 source.

### So: are the existing atlases good enough for the opera? No.

| Source | Figure rows | At 227 design px (today's size) | At 300 design px (recommended) |
|---|---|---|---|
| Today's 512² portrait | 488 | **1.44x supersampled** | 1.09x supersampled |
| Existing 256px atlas cell | ~230 | **1.47x UPSCALED** | 1.96x upscaled |
| New 512px atlas cell | ~490 | 1.44x supersampled | **1.09x supersampled** |

**Dropping the existing 256 atlases into the opera actor slot is a 2.1x drop in effective resolution — she gets measurably blurrier than the static card she replaces.** That is the wrong trade to hand a playtest that already said she is low-res.

### The right cell size is 512, and it is the only POT-clean answer

`AGENTS.md` documents a hard constraint: *"NPOT textures with compress/mode=2 hang the headless importer at 0% CPU."* POT is a build requirement, not a style preference. With 4 columns (the house grammar):

- 512 cells → **2048x2048** (4x4) and **2048x1024** (4x2). POT. Holds 1:1 up to ~325 design px (45% of screen height) on the M11.
- 768 cells → 3072x3072. **Not POT.** Disqualified.
- 1024 cells → 4096x4096, or a 2x2 grid at 2048² (4 frames/file). Disqualified on cost.

**512x512 cells. Locked by arithmetic, not taste.**

Ceiling to state to the owner: 512 cells support her at up to **~340 design px / 47% of screen height** at native sharpness. If she is ever wanted larger than half the screen, that is a different, more expensive request.

### Three framing defects that read as "low resolution" and cost zero art to fix

These came out of the same 60-station sweep and are, I believe, most of what the owner actually saw:

1. **She floats above the walkway.** `_place_on_stage` anchors by `size.y - 12` = 288, but the drawn image ends at 269 and her tail tip at 265. Her contact point lands **~10px above** the painted station.
2. **Her head crosses the black header at 6 of 60 stations** — and because `top` is added to `root` before `player_actor`, she draws *on top of* the 84%-opaque navy strip. Worst offenders are **three of the five finale stations**: ballerina `rose_finale_stage` (75px of head over the bar), magician `moon_pool` (34px), racer `trophy_shell` (34px). The most important shot in the act is the one where her head is pasted across the black bar. This is owner note #1 and #3 being the same defect.
3. **The task card covers 18% of her width at every non-combat station** (mean over all 60; range 13–21%). `action_panel` is added after `player_actor`, and `_card_position_near_station` (:751) offsets by `+60 / -500` px from the station Roshan is standing on, so the card and her body always intersect. She is *literally* not shown in full.

---

## 2. THE INTEGRATION PLAN

### The node change: keep `TextureRect`, drive an `AtlasTexture` region

Do **not** move to `AnimatedSprite2D`. The whole opera lays out in Control space — `_place_on_stage` (:515), `_glide_roshan_to` (:596), `_hero_feet` (:1298, which feeds the imp brain), `_card_position_near_station` (:751) and `_imp_contact` (:1470) all read `player_actor.size`, `.position`, `.scale`. A Node2D swap breaks every one.

**The repo already has the right mechanism and it is already used inside the opera.** `scripts/roshan_sprite_loop.gd` `setup_texture_rect()` (:56) builds an `AtlasTexture`, assigns it to a `TextureRect`, and sets `.region` per frame using the same `RoshanSpriteFrames`/`RoshanSpriteAnchors` correction tables `player.gd` uses. `scripts/opera_act.gd:5555` already calls it (`animator.setup_texture_rect(roshan)` for the farm standee, 150x190). The career world is the only opera surface that ignores it.

### The three-node stack (this is the key structural move)

`player_actor` is written to by four different systems (glide tween, bounce tween, imp shove tween, depth scale). Animation must not join that fight. Mirror `player.gd`'s architecture exactly — it already solved this with `classic_motion_root` (:183-193):

```
player_actor        Control   <- stage code owns position/scale (UNCHANGED call sites)
└─ ActorMotion      Control   <- animator owns breath / bob / lean / recoil
   └─ ActorSprite   TextureRect  <- animator owns texture region + flip_h
```

This also fixes a live bug: `_bounce_actor` (:1158) captures `home_y = actor.position.y` and restores it 0.3s later. If a `_glide_roshan_to` tween (1.3s, or 0.9s in combat) is running on the same property, the bounce restores a **stale** y and she snaps. Same for the `_imp_contact` shove (:1481). Moving both onto `ActorMotion` removes the conflict entirely.

### New script: `scripts/opera_roshan_actor.gd`

Modeled on `roshan_sprite_loop.gd`, reusing `player.gd`'s exact timing grammar (`ROSHAN_25D_KEYFRAMES = 4`, `phase = int(verb_t/verb_len * 4)` — matching it means the opera *feels* like the rest of the game):

```gdscript
const VERBS := {
  "idle":    {"sheet": "a", "row": 0, "len": 2.4, "loop": true},
  "travel":  {"sheet": "a", "row": 1, "len": 0.55, "loop": true},
  "work":    {"sheet": "a", "row": 2, "len": 0.90, "loop": true},
  "cheer":   {"sheet": "a", "row": 3, "len": 1.60, "loop": false},
  "react":   {"sheet": "b", "row": 0, "len": 0.70, "loop": false},
  "present": {"sheet": "b", "row": 1, "len": 2.00, "loop": true},
}
```

`setup(sprite: TextureRect, career: String)` loads `roshan_<career>_sheet_a/b.png`. **If a sheet is missing it falls back to the existing `roshan_<career>.png` and behaves exactly as today** — so the 13 careers can land in batches without a broken build.

### Which atlas serves which opera moment

| Opera moment | Code site | Verb |
|---|---|---|
| Walking the painted path between stations | `_glide_roshan_to` :596 | `travel` (loop), then arrival verb |
| Parked at a station, waiting for the child | `_show_phase` :683-685 | `idle` (loop) |
| Doing the job — every gesture | `_on_gesture` :1051-1053 | `work` (loop); **discrete modes (tap/timing/choice/catch) restart the cycle at frame 0 per hit — one finger stroke = one arm stroke.** Continuous modes (hold/swipe/circle) free-run, rate proportional to `amount`. Keep the existing `bounce_cool = 0.22` gate |
| Phase completed | `_on_gesture` :1072-1081 (the completion hold) | `cheer` (one-shot) → `idle` |
| Taking her mark for a scuffle | `_start_stage_combat` :809 | `travel` → `idle` |
| An imp lands a swipe | `_imp_contact` :1470 | `react` (one-shot) — replaces the raw position shove |
| Curtain call | `celebrate` :1204 | `present` (loop) |
| 9s of no input (the re-prompt) | `_process` :1680 | `idle` restart — she looks around instead of holding one card |

### Reconciling costume with the atlas art

The existing atlases are her default outfit. The opera needs 13 costumes. **You cannot mix the two on one character in one scene.** If travel used the uncostumed atlas and the station used the costumed card, she would change clothes every time she walked — a 4-year-old reads that instantly and it is worse than stiffness.

`CODEX_ROSHAN_SPRITE_REGENERATION_2026-08-02.md` §R4 already flagged the alternative and its failure mode: costume layers *"need to be authored against the same per-frame windows as the base atlas — coordinate before generating, or the layers will drift out of register with her body."* The base atlases pack on a **226.8–250.0 px pitch instead of 256** (§R2 table) and the runtime carries `roshan_sprite_frames.gd` SHIFTS to compensate. Any independently-generated overlay inherits that drift.

**Therefore: costumed frames must be authored as complete figures, per career.** Which is question 3.

---

## 3. THE COSTUME QUESTION — decision and cost

Costs below use the measured PNG sizes of the existing 1024² atlases (730–940 KB for 16 cells of 256) scaled to 512 cells (~4x pixels, ~3–3.5x PNG bytes for painterly art): **≈3.0 MB per 2048x2048 sheet, ≈1.5 MB per 2048x1024 sheet.** VRAM at the project's current `compress/mode=0` (lossless, matching every other Roshan sheet): 16 MB and 8 MB respectively, **one career resident at a time**.

| Option | Files | Frames | Disk | VRAM/career | Verdict |
|---|---|---|---|---|---|
| **(a) Re-author all 9 runtime atlases per costume** | 9 x 13 = **117** | 128 x 13 = **1,664** | **~312 MB** | 24 MB | **Reject.** The boot audit already flags ~130 MB of dead assets and a 30–40s tablet boot. This alone triples the APK |
| **(b) Costume overlay on the base animation** | 9 x 13 = **117** | 1,664 | ~100–120 MB | 24 MB | **Reject.** Same file count as (a), worse result. A chef's hat must track her head through a twirl and a flop — that is a second full animation, not a decal. Plus the §R2 packing drift makes registration unfixable without re-measuring the anchor table on every regeneration |
| **(c) Reduced per-costume set — RECOMMENDED** | **26** (2 per career) | 24 x 13 = **312** | **~58 MB** | 24 MB | **Accept** |
| (c-lite) fallback if 58 MB is too much | **13** (sheet_a only) | 16 x 13 = 208 | **~39 MB** | 16 MB | Loses `react` + `present`; combat and the curtain call fall back to tweened static |

**Option (c), the recommendation:**

- `roshan_<career>_sheet_a.png` — **2048x2048**, 4x4, 512px cells. Row 0 IDLE, row 1 TRAVEL, row 2 WORK, row 3 CHEER.
- `roshan_<career>_sheet_b.png` — **2048x1024**, 4x2, 512px cells. Row 0 REACT, row 1 PRESENT.

Why these six and not fewer: `bop` phases are 2 of 7 beats (~30% of every act) and are the single stiffest moment today — 8 imps swarm a motionless card. `celebrate()` is the payoff shot. Both need `sheet_b`.

Why 4 keyframes per row and not 8/16: it matches `ROSHAN_25D_KEYFRAMES = 4` and every existing gesture row. Consistency with the engine constant is worth more than smoothness here, and 4-frame gestures already read fine in the live game. *If* the slow-exploration direction (owner note #2) lands, add a `sheet_c` (4x2: TRAVEL frames 5–8 + a look-around/point row) — that is a later, additive request, not a blocker.

One import note worth an owner decision, not a mandate: the project has `import_etc2_astc=true`. Switching these two sheets to `compress/mode=2` would cut VRAM from 24 MB to ~6 MB per career, at the risk of block-compression fringing on hard alpha edges. Measure it on the P1 proof before deciding; keep `mode=0` (house default) until then. **If you do test mode 2, the canvases must be POT — which they are — or the headless importer deadlocks (AGENTS.md).**

---

## 4. THE CODEX REQUEST

### Atlas specs

| | `roshan_<career>_sheet_a.png` | `roshan_<career>_sheet_b.png` |
|---|---|---|
| Canvas | **2048 x 2048** (POT, mandatory) | **2048 x 1024** (POT, mandatory) |
| Grid | 4 columns x 4 rows | 4 columns x 2 rows |
| Cell | **512 x 512** | **512 x 512** |
| Format | RGBA8 PNG, straight alpha | same |
| Count | 13 (one per career) | 13 |

**Row order is load-bearing. A row is one animation, read left to right as four chronological keyframes: anticipation → transition → peak → settle/return** (identical grammar to `roshan_gesture_a/b/c`).

`sheet_a`: **row 0 IDLE** (gentle hover, tail sway, hair drift, one blink — must loop seamlessly frame 3 → frame 0) · **row 1 TRAVEL** (mermaid swim cycle, 3/4 travelling, seamless loop) · **row 2 WORK** (the career action below, seamless loop) · **row 3 CHEER** (arms rising to overhead joy, then easing — one-shot).

`sheet_b`: **row 0 REACT** (rocks back, arms up, tail curls, recovers — *surprise and delight, never fear or pain*; the project has no fail state) · **row 1 PRESENT** (open two-handed presenting gesture toward the audience, **hands empty**, holds/loops).

### Pose list — row 2 WORK, per career

Grounded in each career's own `PHASES` verbs and station landmarks in `opera_stage_paths.gd`:

| Career | WORK (4 keyframes) |
|---|---|
| chef | Whisking a big bowl at her hip — reach, sweep, sweep, settle |
| detective | Magnifier low and sweeping, then raised to her eye |
| ballerina | Port de bras into an arabesque, tail arced behind |
| candymaker | Pulling and twisting a taffy ribbon between both hands |
| doctor | Stethoscope to a plushy's chest, then wrapping a soft bandage |
| farmer | Scattering seed from a woven basket |
| boxer | A padded one-two jab out of guard and back to guard |
| magician | Wand sweep from the hat up into an overhead flourish |
| painter | A full brush stroke across an easel |
| astronaut | Both hands turning a big valve wheel |
| racer | Hands on the wheel, leaning into a turn |
| popstar | Mic to mouth, then arm out to the crowd |
| nursery | Rocking a swaddled baby, bottle in the other hand |

IDLE / TRAVEL / CHEER / REACT / PRESENT are the same action in all 13 — **only the costume changes.**

### Naming convention

Runtime path `assets/opera/worlds/actors/` (beside the existing `roshan_<career>.png` and the 156 `rival_<career>_<state>.png` files):

```
roshan_chef_sheet_a.png        roshan_chef_sheet_b.png
roshan_detective_sheet_a.png   roshan_detective_sheet_b.png
... x13 careers: chef, detective, ballerina, candymaker, doctor, farmer,
    boxer, magician, painter, astronaut, racer, popstar, nursery
README_roshan_sheets.md        (row order + cell contract, mirroring
                                assets/characters/roshan_25d/README.md)
```

### Content locks

**Identity (verbatim from the accepted `PROMPTS_4X.md` locks — do not restyle):**
> child face and age · gold aqua-gem tiara · brown wavy hair with rainbow ponytail · **pearlescent lavender/aqua scaled tail with rainbow fins** · clean dark-plum outlines · soft cel shading.

**Opera-specific:**
- **NO LEGS. The tail is always the tail.** Every pose — walking the path, working, cheering, reacting — is a mermaid pose. TRAVEL is a swim/glide, never a walk cycle.
- **Costume continuity is absolute.** Use `assets/opera/worlds/actors/roshan_<career>.png` as the identity *and costume* reference image, exactly the way `PROMPTS_4X.md` used the base atlases as identity refs. The owner approved those 13 costumes; hat, apron, gloves, colour placement must be pixel-consistent. `sheet_a` row 0 frame 0 **must be the same pose as the approved portrait**, so the swap-in is seamless and the anchor can be measured against it.
- **No baked goal prop.** The engine draws `goal_<career>.png` separately (`prop_rect`, :391-401). PRESENT hands are empty or the cake appears twice. (Inverse of the standing "no baked Roshan" lock in `CODEX_OPERA_ANIMATION_HANDOFF_2026-08-03.md` §9.)
- Career tools that are part of the *pose* (whisk, wand, brush, mic, bottle) are allowed and expected; standalone scenery, floors, shadows and reflections are not.
- Lighting per STYLE-HOUSE: warm key upper-left, cool bounce lower-right, hand-inked varying dark-plum contour, no flat fills.
- Flat solid `#00ff00` background for chroma removal (house pipeline, `remove_chroma_key.py`).

### Cell contract — this is the part that retires the correction tables

The existing sheets pack on a 226.8–250.0 px pitch instead of 256, which is why `roshan_sprite_frames.gd` SHIFTS and `roshan_sprite_anchors.gd` exist and must be re-measured on every regeneration. Do not repeat it:

1. Every figure **wholly inside its own 512px cell**, with **≥8 px of fully transparent margin on all four sides**.
2. **Tail-tip contact row identical in every cell: row 500 ±2** of the cell. The opera anchors by that contact point.
3. **Torso centre-line at column 256 ±3** in every cell. This makes `flip_h` symmetric and removes the need for a mirrored anchor correction.
4. Consistent figure scale across all 24 cells of a career — no per-frame zoom drift.
5. No two cells byte-identical (house rule N6).

If 1–4 hold, `opera_roshan_actor.gd` needs **no** SHIFTS/anchor table at all: `region = Rect2(col*512, row*512, 512, 512)`, flat.

### Acceptance (house gate, by reference to `OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md`)

Staging into `assets_src/concepts/`, contact sheets, PROMPTS.md entries, ledger rows, weighted gate **pass ≥ 4.5 / target ≥ 4.7**, one controlled promotion commit, one `ASSET_LICENSES.md` line per accepted asset. Plus:
- **QA render at gameplay scale on the Mobile renderer.** A candidate without a runtime capture caps at 2/5 and must not ship (house rule).
- **The loop test:** play each looping row (IDLE, TRAVEL, WORK, PRESENT) at 7 fps and confirm frame 3 → frame 0 has no pop.
- **The margin/anchor script:** measure every cell's alpha bbox and assert the contract above numerically before staging. `python3 tools/audit_roshan_sprite_clipping.py` is the model.
- **The costume diff:** side-by-side each `sheet_a[0]` against the approved `roshan_<career>.png`. Any costume drift is an automatic rejection.

### P1 — stop after one career

Per the house "stop after P1" protocol: generate **chef only** — `roshan_chef_sheet_a.png` + `roshan_chef_sheet_b.png`, 24 frames, 2 files. Stage, QA-render in the running career world at all six verbs, get owner sign-off on the animation style and the costume match. **Do not batch P1 with anything.** If chef is right, the remaining 12 careers are execution.

---

## 5. WHAT TO BUILD NOW vs. WHAT TO REQUEST

### Build now — no new art, and it addresses most of the complaint

None of this waits on Codex. In rough value order:

1. **Build the three-node actor stack** (`player_actor → ActorMotion → ActorSprite`) and put `_bounce_actor` and `_imp_contact`'s shove onto `ActorMotion`. Fixes the live tween-conflict snap and is the prerequisite for everything else.
2. **Add the always-alive breath to the static portrait** — the exact `_tick_always_alive_visual` (`player.gd:450`) formula: `y += sin(life)*2px`, `scale = (1+sin*0.008, 1-sin*0.006)`, on `ActorMotion` only. This is the single biggest fix for "extremely stiff" and it is ~15 lines.
3. **Give `_glide_roshan_to` a motion language.** Today it is a pure linear position lerp — literally a cardboard cut-out sliding. Add a swim bob (y sine at ~2.4 Hz), a ±0.06 rad lean into travel direction, and a squash/stretch settle on arrival.
4. **Grow the actor box `250x288` → `330x330` and anchor to the real figure bottom.** She becomes ~300 design px tall (from 227) — **+32% presence for free**, and the 512 source is still supersampled 1.09x on the M11. Also removes the 13% letterbox waste and the ~10px float above the walkway.
5. **Clamp her out of the header band** — `_place_on_stage` must keep her top edge below y≈146. Fixes 6 of 60 stations including three of five finale stations.
6. **Move the task card off her body.** Change `_card_position_near_station` (:751) to dock on the side she is *not* on, and assert `card_rect.intersects(actor_rect) == false` before showing. Removes the mean 18% occlusion.
7. **Slow the pacing** (owner note #2, cheapest possible response): `_glide_roshan_to` duration `1.3 → 2.2s` now that travel has motion, and add a short look-around hold on arrival before the card fades in. Zero art.

Items 4–6 are, I think, most of what the owner saw as "low resolution": she is small, floating, cropped by a card and punching through a black bar.

### Genuinely needs new generation

**Only the 26 costumed atlas files.** Nothing else in this workstream is art-blocked.

### Explicitly rejected shortcuts

- **Using the existing uncostumed gesture atlases in the career worlds for celebration/idle.** She would change out of her chef's hat to cheer and back into it to work. A 4-year-old reads a costume swap instantly; it is a worse defect than the stiffness it fixes. The uncostumed atlases stay legitimate where costume is not yet established — the opera lobby and the promenade, where `opera_act.gd:5555` already uses `RoshanSpriteLoop.setup_texture_rect()`.
- **Faking arm motion from one card** (skew, warp, cut-out limb rigging on the 512 portrait). The whole point of `work` is that her arms do the job the finger is doing. You cannot get a whisking arm out of one static image, and every attempt will read as a smeared decal.
- **Dropping the existing 256px atlases straight into the actor slot.** Measured 2.1x resolution loss versus the card it replaces, plus the costume swap above. It is the obvious move and it is the wrong one.

# Audit — the 3D → 2.5D change, measured as playability for a 4-year-old

Date: 2026-07-27
Audited tree: `6ced674` (= `dev` = `master`; probe run #855 green)
Scope: everything the 2.5D redesign changed — the charter, the E2 engine
additions, the Sky Lagoon promenade, and the probe suite that gates them.

---

## Verdict, in one paragraph

**The control change is right and it works. The way it was landed took a large
part of the game off the phone.** Touch-the-world on a painted line is
unambiguously easier for a four-year-old than a virtual stick in a free-swim
volume — the camera problem is genuinely deleted, the "where am I" problem is
genuinely deleted, and the art on screen is better than anything the 3D pipeline
produced. But the Sky Lagoon promenade did not ship *beside* the 3D lagoon
behind the `world_style` toggle the charter specified; it **replaced** it
unconditionally, and the courtyard was the hub that every other world hung off.
Nine destinations, including two entire worlds, are now unreachable by any
sequence of taps. Net for the child today: **easier to move, much less to do.**

Nothing here needs a rollback of the 2.5D direction. It needs the toggle the
charter already called for, and the hub rebuilt as promenade door cards.

---

## 1. What actually landed

| Charter said | Tree says |
|---|---|
| P1: `layers` parallax stack + `walk_tick()` in `side_scroll.gd`, additive | ✅ landed (`scripts/games/side_scroll.gd:207`), plus `flat()`, `prop()` (Jolt standees) and a shared `swell` field |
| P2: **reef** promenade pilot, new `scripts/promenade.gd`, behind additive save key `world_style` (default `"classic"`), new `probe_promenade.gd` | ❌ none of it. No `world_style` key exists anywhere in the tree; no `promenade.gd`; no `probe_promenade.gd` |
| P4: zone-by-zone, one zone per branch, **3D world stays shipped per zone until the promenade passes the device test** | ❌ zone 4 (Sky Lagoon) went first and went in hard: `scripts/main.gd:3987` sets `g["phase"] = "court"` and the very next line hands the build to `SkyLagoonPromenade`, so the entire 3D lagoon builder below it is now dead code on every code path |
| Play plane = "the real rigged 3D Roshan, wardrobe intact" | ❌ `m.player.visible = false` (`sky_lagoon_promenade.gd:261`); she is one static 824×1024 PNG that slides and flips |
| Off-screen objectives get the golden pointer + screen-edge arrow | ❌ not implemented |
| `probe_passive` extends to promenades | ❌ it never enters level2 |

The engine work (P1) is clean, well-commented, additive, and did not disturb
dolls or brawl. The complaint is entirely about how the *zone* was landed.

---

## 2. What genuinely got better

These are real and should not be lost in the fix-up.

1. **The stick is off the critical path.** Tap anywhere → she walks there and
   stops. With a `route` present, `plane_goal()` collapses the tap to the
   painted path (`side_scroll.gd:341`) — a tap in the *sky* still walks her
   correctly. That is exactly the right forgiveness curve for this age.
2. **Getting lost is impossible.** `keep_on_screen` (`side_scroll.gd:391`) plus
   `screen_pan_limit` mean she can never walk off-frame and the lens can never
   pan off the painting. This solves the single most-reported problem in the
   charter.
3. **No camera to manage, ever**, and the lens is pinned per stage (`cam_fov`),
   so the free-swim chase cam can't leave the promenade zoomed wrong.
4. **The art is better.** The panorama is genuinely lovely and reads instantly
   at phone size. This validates the "Codex 2D outranks our 3D" production call.
5. **Two roads into the castle** — tap the painted door, *or* just keep walking
   to the end of the path (`_tick_doorstep`). Redundant affordances for a
   non-reader is correct design, and it's probe-gated both ways.
6. **The depth band is honest but unused**: with a route, `z` is forced to 0. A
   4-year-old gets a 1-D world with 2.5-D looks. Keep this.

---

## 3. Defects, ranked by what they cost the child

### P0-1 — Nine destinations became unreachable

`_populate_courtyard_touch_interactables()` (the whole `court:*` family,
`main.gd:3534–3578`) is never called in `promenade` phase (`main.gd:3523`
returns early), and `_tick_level2` hands off to the promenade before the
Classic-mode proximity triggers in `sky_lagoon.gd` can run. Both input modes
are therefore dead ends. What that removes:

| Lost | Was reached by | Now |
|---|---|---|
| **Northern Kingdom** (whole world: forest, town, castle, 25 authored asset families) | `court:north` / Alpine cave star | `northern_portal_pos` never set — probe_northern asserts its absence and calls `_enter_northern_kingdom()` directly |
| **Butterfly World / Galaxy** | `court:galaxy` | `bw_portal_pos == Vector3.ZERO` |
| **Ember Fortress** | `court:ember` | `ember_portal_pos == Vector3.ZERO`; probe_ember asserts "promenade retires the 3D junction gate" |
| **Rainbow Race + reverse** | `court:kart_a/b` | `kart_legA/B` never built |
| **3 Dream Stars** (the level-2 objective and its crown chain) | `court:star:*` | `l2_stars` stays `[]` |
| **Fairy Pond** (E3 minigame) | courtyard pond | `_build_fairy_pond` is below the early return |
| **Courtyard Train ride** | courtyard | probe_train rewritten to assert the promenade replaces it |
| **Rainbow Slide ride** + **`xmas` picture game** | courtyard memory banners (`sky_lagoon.gd:325`) | banners not built |
| **Ocean kingdom gates** (Caribbean ⟷ Norway) | `court:ocean:*` | probe_ocean_kingdoms asserts `not state.has("ocean_kingdom_gates")` |
| Secret castle back entry | `court:back_entry` | gone |

Still reachable and unharmed: the whole 3D reef and its activities, the castle
interior (bed, wardrobe, easel, bells, chest, **dungeon**, **opera** via
`hall:opera`), and 3 of the 5 picture games.

**The probe suite is green through all of this**, because each affected probe
was rewritten to assert the *new* behaviour and then reach the orphaned world by
calling `main._enter_northern_kingdom()` / `_start_kart_game()` / `_exit_level2_now()`
directly. That is the gate's blind spot, not a probe bug per se — but it means
"green" currently proves those worlds still *build*, not that a child can *get*
to them. CLAUDE.md's refactor rule ("do not patch the probe to match new
behaviour unless the behaviour change was the explicit goal") was applied to
`probe_train` and `probe_northern` for a behaviour change that the charter did
not authorise.

### P0-2 — Walking has no purpose except the door

`handle_touch()` clears `ss_walk_goal` on any target tap and activates from
wherever she stands. Tapping the slide from the far end of the level plays the
giggle without her moving. The Hybrid grammar's **approach** step is missing on
the promenade, so her position is irrelevant to every interaction except
`_tick_doorstep`. For a 4-year-old this drains the meaning out of the one verb
the redesign is built on — she learns "walking is decoration."

### P0-3 — The playground promises three games and delivers a wobble

Slide, swing and seesaw are the loudest affordances in the frame — they are
exactly what a four-year-old reaches for. Second tap = `_bounce()` + a giggle
voice + sparkles (`sky_lagoon_promenade.gd:494`). No game, no ride, no
persistence. This is the most likely source of "she tapped it and looked at me."
Meanwhile the three picture *frames* — abstract objects a child has no reason to
tap — hold all the actual content.

### P1-1 — The instructions are text a non-reader can't read

`show_msg("Roshan", "Back outside! Tap a picture frame once to light it up, then
tap it again to play.")` — 16 words, and `show_msg` only fires a generic
`_say(speaker, "talk")` bark, not a recording of that sentence. CLAUDE.md's hard
rule ("no reading-dependent objectives; any new objective must also fire a voice
line via `_say()` and a visual pointer") is not met on the promenade.

### P1-2 — Roshan loses her wardrobe and her animation

She is `sky_lagoon_roshan.png`, hidden rig, `flip_h` for direction, hover-bob for
life. So: no walk cycle, no swim cycle, no idle verbs, and **none of the outfits
the child unlocked show up** — cosmetics being, per the project's own audit, the
#1 engagement driver at this age. The pose is also a 3/4 over-the-shoulder
portrait, which reads oddly as a side-scroller avatar, and it bakes in the Bluey
backpack that the wardrobe is supposed to toggle.

### P1-3 — Three control grammars in one session

Reef = 3D free-swim + stick/Hybrid. Promenade = touch-the-line, no stick needed,
no action bubble in play. Castle = 3D again. A 4-year-old crossing a portal now
has to re-learn how to move, twice per round trip. The charter's whole argument
is coherence; today's build is the least coherent the game has ever been.

### P1-4 — Scene congruency: the elements do not belong to the same picture

Owner report: there is a visible gap between the background art and the sprites
standing on it. That gap is now measured rather than asserted —
`tools/audit_scene_congruency.py` compares every element of a stage against the
**plate** (the mural it is painted on) across seven criteria, and writes
`audit/congruency_sky_lagoon.json`. Current result: **0 of 10 elements
congruent.**

The plate's measured target values (ground band of panorama tile 1):
`a* −20.8, b* +19.5, median L* 54.2, black point 26.4, white point 72.6,
key light 142°, specular 0.1%, local contrast 2.49, oversample 0.94×`.

| ID | Criterion | Tolerance | Failing |
|---|---|---|---|
| C1 | Lab (a*,b*) centroid distance | ≤ 18 | 8/10 |
| C2 | key / black point / white point | ≤ 16 / 14 / 14 L* | 9/10 |
| C3 | key-light direction | ≤ 45° | 8/10 |
| C4 | specular fraction above plate | ≤ +2.5% | 4/10 |
| C5 | local RMS contrast ratio | 0.53×–1.9× | 1/10 |
| C6 | authored px ÷ displayed px | 1.0–2.5×, ≤2× plate's | 10/10 |
| C7 | contact shadow present | required | 10/10 |

What the numbers say, in plain terms:

1. **C6 is the structural one and it is universal.** The mural is authored at
   **0.94×** the size it is displayed — very slightly soft. Every standee is
   authored at **2.6×–5.9×** (Roshan at 5.9×, i.e. **6.3× the plate's detail
   density**). Three-to-six times the line density arrives on top of a soft
   painting, which is precisely the "sticker pasted on a photo" read. No amount
   of recolouring fixes it: the plate must gain resolution (4×1024px tiles across
   the 144-unit panorama instead of 3×724px, → ~1.33×) and the standees must be
   authored at the size they actually occupy.
2. **The props share a palette the landscape never uses.** castle_gate and swing
   sit at the same point in a*b*; plane and seesaw sit at another. Both pairs are
   cream-and-gold prop palettes 26–42 units from a cool green plate. The two
   elements that *do* pass C1 — the fir (4.4) and the currant (13.8) — are the
   two painted as foliage. **The fir is the style exemplar; everything else
   should be generated against it.**
3. **The stage is unlit** (`shaded = false` on every Sprite3D), so baked gloss has
   nowhere to go: the cloud is 51.5% blown specular and the pearl plane 32.8%,
   against a plate with 0.1%. They read as plastic toys in front of a painting.
4. **Two light sources in one frame.** Eight elements disagree with the plate's
   key by more than 45°; Roshan by 103°, the slide by 96°.
5. **C7 is a code fix, not an art fix.** All ten fail it because the promenade's
   own `_add_sprite()` never builds the contact-shadow quad that
   `SideScrollStage.flat()` already builds. One change clears the criterion for
   every element — do it before regenerating any art.
6. **Not measured but visible:** castle_gate and slide are drawn in ¾ isometric
   with surfaces receding into the picture, while the mural is a straight-on
   elevation. That is why the gate's bridge could never line up with the painted
   door. Projection needs to be part of the art brief, not just colour.

### P2 — Smaller things

- **Night never reaches the lagoon.** `_set_night(true)` (castle bed) flips the
  reef, but the promenade is a fixed daytime mural and `_build_lagoon_night` sits
  below the early return. Sleep, walk out, it is noon.
- **Ghost stick.** `_stick_hint` still shows in the lower-left on the promenade
  where it is never needed — the opposite of the P-final demotion.
- **Two-tap on everything.** Correct for world-changing doors; heavy for a swing.
  Consider first-tap-acts for pure-delight props, two-tap only for transitions.
- **`half_d = 2.6` and `route` ⇒ `z = 0`**: the depth band is dead weight; the
  `flat()` layering primitive and `prop()` Jolt fleet are both built and unused
  by this zone. No harm, but the stage is not yet doing what the layering rule
  describes.
- **`probe_passive` never enters level2**, so the charter's "passive runs still
  win nothing" criterion is unproven for the promenade.

---

## 4. What to change, in order

### First — restore reachability (nothing else matters until this is done)

1. **Land the `world_style` save key the charter specified.** Additive, default
   `"classic"`, pause-menu tile beside Hybrid/Classic. `_enter_level2` branches
   on it instead of hard-coding `phase = "court"` → promenade. That single change
   gives the family a working game tonight and makes every later step reversible.
2. **Give the promenade its hub.** The lost destinations are all *door cards* in
   promenade terms — oversized wordless picture sprites at painted depth, tapped
   like the castle gate:
   - a **Magic Cave** card at the west end → `_enter_northern_kingdom()`
   - a **Rainbow Race arch** card → `_start_kart_game(false, "float")` (+ reverse)
   - **Butterfly World** and **Ember Fortress** cards (same unlock conditions as
     `court:galaxy` / `court:ember`)
   - two **ocean-kingdom gate** cards when `ocean_gate_hub` is true
   - a **Fairy Pond** card → the E3 pond
   - the **train** as a ride target on its own card
   - the **Dream Stars**: three collectible standees along the route, wired to
     the existing `l2_star_progress` / crown chain
   Every one of these is a `_register_target()` call plus the existing handler
   from `main.gd:3665–3686`. This is a day of work, not a redesign.
3. **Extend the route left and right** (or add a second and third promenade page
   with edge exits) so the new cards have somewhere to live without crowding the
   playground screen.

### Second — make walking mean something

4. **Put the approach step back.** On first tap: set `ss_walk_goal` to the
   target's foot position *and* focus it; on arrival, promote to "ready" (the
   gold ring already exists); second tap acts. Then the child's own walking is
   what reaches things — which is the entire premise of the promenade.
5. **Make the playground play.** Slide → the existing rainbow/penguin slide ride.
   Swing → a one-tap rhythm pump (E2 `run_tick` is already sitting there unused).
   Seesaw → a two-tap co-op beat with the companion. Any of the three is better
   than a wobble; all three make the playground screen the best screen in the game.

### Third — comprehension and continuity

6. **Voice every promenade line.** Record the two arrival lines and the per-target
   verbs; route them through `_say()` so nothing depends on reading. Add the
   golden pointer + screen-edge arrow the charter promised for off-screen cards.
7. **Put the rig back on the plane.** Use the real `player` node with the wardrobe
   skin, side-on, with the walk/idle verbs — the E2 brawl mode already proves the
   rig works in this exact rig-on-a-line configuration. Keep the PNG only as the
   fallback if a device pass shows the rig costs frames. Failing that, at minimum
   swap the card per equipped outfit.
8. **Hide the stick hint** whenever `phase == "promenade"` (the P-final demotion,
   scoped to one zone — cheap, and it removes a control the child shouldn't learn).
9. **Give the promenade a night mural** (or tint the existing one) so sleeping in
   the castle changes the world she wakes into.

### Fourth — close the congruency gap, on a loop

The art half of this audit is exported as a Codex-facing work order artifact
(criteria, per-asset failures, prescriptions, the loop):
<https://claude.ai/code/artifact/ec604e78-af2b-45de-896a-edb32f190cca>. Its
machine-readable half is `--json audit/congruency_sky_lagoon.json`; `audit/` is
gitignored, so regenerate it on demand or publish it as a workflow artifact
alongside the opera art manifest.

The loop is deliberately closed — Codex generates against the criteria, the gate
re-measures, and anything still failing is the next batch. No human judgement in
the middle:

**L1.** **Fix C7 in code** (`_add_sprite` gains the contact-shadow quad). Free, and it
   clears one criterion across all ten elements.
**L2.** **Re-plate before re-standeeing.** The mural moves from 3×724px to 4×1024px
   tiles. This changes the target every standee is measured against, so doing it
   second would invalidate any art generated first.
**L3.** **Generate worst-first**, each prompt carrying the plate's measured values as
   the target plus that element's authored-pixel budget, with the fir as the
   style exemplar.
**L4.** **Re-run `python3 tools/audit_scene_congruency.py`.** It exits non-zero while
   anything fails and prints the exact criterion and delta per asset — that
   output *is* the next batch's work list.
**L5.** **Repeat to 10/10, then lock it** into `scripts/ci.sh` and the probes workflow
   beside the other static gates. Not before: adding a gate that currently reads
   0/10 would turn dev red and block the APK. A criterion that isn't enforced is
   a preference, but a gate that lands red is just a broken build.
**L6.** **Then judge it with eyes.** Green means the pieces are measurably the same
   picture; it does not mean the picture is good. The device pass still decides
   that and the gate never overrides it.

Tolerances live in one `TOL` dict, so tightening them after the first green run
is a one-line change. New zones are one entry in `SCENES`; sprite world heights
are parsed out of the stage script so the table cannot drift from the runtime.

### Fifth — close the probe suite's blind spot

10. **Write `probe_promenade.gd`** as the charter specified, and add to it the
    check that is missing everywhere: *for every world the game can reach, assert
    a tap path exists from spawn* — no probe may enter a world by calling
    `_enter_*` directly without a sibling check that a child could have got there.
    That one assertion would have caught this entire audit on run #841.
11. **Extend `probe_passive` into level2**, per the charter's own success criteria.

---

## 5. Answering the question directly

*Does the 2.5D change increase playability for a four-year-old?*

- **Movement and orientation: yes, decisively.** Touch-the-path with a pinned
  lens is the right control model for this child and should be extended to the
  reef next, as the charter originally ordered.
- **Comprehension: mixed.** The picture is clearer than the 3D world ever was,
  but the promenade currently instructs in text, its most inviting objects do
  nothing, and nothing standing on the painting measurably belongs to it
  (0/10 congruent) - the child sees stickers on a landscape.
- **Amount of game: sharply down.** Two worlds, four rides/races, the fairy pond,
  the level's own star objective and both ocean gates are unreachable. Measured
  end-to-end, a child can do *less* today than a week ago.

So: keep the direction, land the toggle, rebuild the hub as door cards, and make
the walking and the playground pay off. After steps 1–5 the answer becomes an
unqualified yes.

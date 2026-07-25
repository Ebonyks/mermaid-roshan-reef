# NAVIGATION AUDIT — why moving around the world and the castle feels bad
### 2026-07-25 · scope: locomotion engine, chase camera, castle spatial design, wayfinding

---

## VERDICT (the three hypotheses in the brief)

**"Is it camera tightness?"** — Yes, and it is measurable, not a matter of taste.
Indoors the chase camera is set to `cam_back = 10.0 / cam_high = 4.2`
(`main.gd:4349-4350`) behind a 38° lens. Roshan's model is **7.03 units tall**
(`player.gd:245-247`: v3/v4 GLB is 1.9u tall × scale 3.7). At that boom the
visible frame is **7.1 units tall** — she fills **99 % of the screen height**.
Outdoors, at `25.0 / 9.0`, she fills 39 %. Walking through the castle door
multiplies her on-screen size by 2.5× and leaves nothing but her back on screen.

**"Something about gameplay?"** — Yes, and this is the *bigger* of the two.
The locomotion model is a single open-ocean tuning applied unchanged to every
space in the game:

| quantity | value | derivation |
|---|---|---|
| top speed | **25.5 u/s** | `43.7 / -ln(0.18)` (`player.gd:742,744`) |
| coast-to-stop distance | **14.9 u** | `v_max / k`, `k = 1.715 /s` |
| turn rate | **1.8 rad/s** | `player.gd:728` |
| 180° turn | **1.75 s** | |
| turning circle at speed | **28.4 u across** | `2·v/ω` |
| vertical control | **none** | `dir` is `(sin yaw, 0, cos yaw)` — y is always 0 |

Now compare against the rooms she has to do that in:

| space | playable size (mesh minus the 1.6u collider pad) | vs 28.4u turning circle |
|---|---|---|
| basement corridor | **11.3 u wide** (`castle_hall.gd:718-725`) | 2.5× too narrow |
| basement side rooms (×4) | **13.3 × 11.3 u** (`castle_hall.gd:755-768`) | 2.1× too narrow |
| music room | **13.1 × 34.8 u** (`castle_hall.gd:987-989`) | 2.2× too narrow |
| bedroom | **17.3 × 17.3 u** (`castle_hall.gd:1086-1088`) | 1.6× too narrow |
| Grand Hall | 65.3 u wide | fits |

Her **stopping distance (14.9 u) is longer than the longest dimension of every
room in the basement wing.** She physically cannot turn around at speed in any
castle room, and cannot stop inside one. That is the feeling being reported.

**"A claustrophobic castle design?"** — No. The castle is *large*: the Grand
Hall is 70 × 80 × 52 units, doorways are ~6.8 u clear, ceilings are 33 u.
What makes it read as claustrophobic is (a) the 10-unit camera in rooms whose
short axis is 11 u, and (b) a movement model whose turning circle is 2–3× the
room. The **rooms are not too small for Roshan; they are too small for her
momentum and for her camera.**

Everything below is the detail, ranked.

---

# PART 1 — THE LOCOMOTION ENGINE (`scripts/player.gd:676-899`)

## N1 (critical) — Tank steering on a touch stick, with a camera welded to the heading

`player.gd:710-713` maps the virtual stick to **rotation + thrust**, not to a
direction:

```gdscript
if absf(tv.x) > 0.10: turn -= tv.x      # stick X  -> yaw RATE
if absf(tv.y) > 0.10: fwd  -= tv.y      # stick Y  -> forward THRUST
...
yaw += turn * 1.8 * delta               # 728
var dir := Vector3(sin(yaw), 0.0, cos(yaw))
```

and the camera then follows that same yaw rigidly (`player.gd:1025`
`var cyaw: float = yaw + cam_orbit`).

Consequences:

1. **Push-left does not go left; it *starts a rotation*.** A non-reader's model
   of a joystick is absolute ("point where I want to go"). Tank steering is a
   learned vehicle convention. This alone accounts for a large share of
   "awkward to navigate".
2. **Steering spins the entire world.** Because the camera yaw *is* the body
   yaw, a correction of 20° rotates the whole screen 20°. There is no camera
   lag and no lead: `cam.look_at(focus)` (`player.gd:1039`) keeps her pinned
   dead-centre every frame, so the frame carries no information about which way
   she is about to move.
3. **A 180° takes 1.75 s while coasting 15 units forward.** Turning around in
   any interior is not possible without hitting a wall first.
4. **Diagonal input curves rather than steers** — up-left is "thrust + spin",
   so the only way to travel in a straight line at an angle is to spin to the
   heading first, then push straight up.

**Fix direction (recommended):** camera-relative planar steering — the stick
vector becomes a *target heading* in camera space; `yaw` slews to it at
~6 rad/s with the existing thrust curve. This is a ~15-line change in
`player.gd:676-730`, keeps every arena/ramp/solid contract intact, and turns
the control into the one a 4-year-old already understands. Keep tank steering
available for the gamepad if desired (it is fine with a real stick + a
separate right stick).

## N2 (critical) — There is no vertical control anywhere, in a game with a four-storey castle

`dir` has `y = 0` unconditionally. The *only* way to gain height is the jump
impulse (`player.gd:722-724`, `vel.y = 16.0`, 0.4 s cooldown) and the only way
to lose height is to stop pressing it and wait for gravity.

Measured with the interior constants (`gravity 13`, drag `k = 1.715`):

* climb rate while holding jump: **≈ 9.5 u/s**
* fall rate: **7.58 u/s terminal**, uncontrollable
* castle vertical extent: undercroft floor `-17.4` → Dreaming-Floor ceiling
  `63.5` = **81 units** (`castle_hall.gd:571-595`)
* therefore: **≈ 8.5 s of held-button climbing, ≈ 10.7 s of un-steerable
  falling, to traverse the castle vertically.**

Falling from the Dreaming Floor to the Grand Hall floor is a **7-second dead
drop with no input authority**. Meanwhile the character model visibly pitches
with `vel.y` (`player.gd:897`) — the animation implies a dive control that
does not exist.

On touch there is additionally **no down affordance at all**: tap = jump,
held second finger = jump/up, drag = camera. Nothing descends.

**Fix direction:** the cheapest real improvement is asymmetric gravity —
interior gravity 13 → ~40 (terminal ≈ 23 u/s) cuts the dead drop from 7 s to
2.3 s without touching the no-fail contract. The correct fix is a dive input
(stick pulled fully back while airborne, or a second bubble on the touch HUD).

## N3 (high) — One drag/turn tuning for the ocean, the lagoon, and a 11-unit corridor

`43.7 / pow(0.18, dt) / 1.8 rad/s` are hard-coded in `player.gd:728-744` with
no venue profile. The ocean (r = 270) and the Sky Lagoon (dome 235) want
floaty, long-glide swimming. The castle basement (11.3 u corridor) wants
roughly **4× the drag and 2× the turn rate**. There is already a venue
concept in `main.gd` (`arena_center / arena_dome / arena_ceil`,
`main.gd:72-74`) — drag, turn rate and gravity belong in the same dictionary.

Suggested interior numbers, chosen so the turning circle fits the corridor:

```
indoor: drag pow(0.033, dt)  (k = 3.41 → top speed 12.8 u/s, stop in 3.8 u)
        turn 3.2 rad/s       (turning circle 8.0 u across — fits 11.3 u)
        gravity 40.0
```

## N4 (medium) — The virtual stick's full deflection is ~7 mm of thumb travel

`touch_ui.gd:31` `const R := 78.0`, with a 22 px dead zone (`TAP_SLOP`), in the
1280×720 stretch space. On a landscape phone that is roughly **7–8 mm from
centre to full lock, with the first 2 mm dead** — under 6 mm of usable analog
band. The comment on that line says it was tuned for *tablets*
("livelier steering on tablets"); the target device is a 3–4-year-old phone.
Combined with N1 (stick X = yaw *rate*), every thumb tremor becomes continuous
heading drift that never self-corrects. Recommend R ≈ 130–150 and re-checking
on the actual handset.

## N5 (medium) — Reverse is full-thrust on touch, 60 % on keyboard

`player.gd:681` gives keyboard back-pedal `fwd -= 0.6`; the stick path
(`player.gd:713`) gives the full `-1.0`. Pulling the stick back accelerates
backwards at the same 43.7 as forwards — a 4-year-old resting a thumb low on
the stick reverses at full speed with the camera in front of her.

---

# PART 2 — THE CAMERA

`CameraKit` (`scripts/camera_kit.gd`, Phase 0 of `CAMERA_AUDIT_2026_07.md`) is
good work and did fix the camera-inside-geometry class. The remaining problems
are framing and the parts of that audit's plan (P1/P2) that were never landed.

## C1 (critical) — The interior boom hand-tune predates the resolver and was never revisited

`main.gd:4349-4350` pulls the boom to `10.0 / 4.2` with the comment *"pull the
chase camera in so it does not clip the hall / back-room walls"*. That
mitigation is now **redundant** — `CameraKit.resolve()` (`player.gd:1036-1038`)
shortens the boom analytically against `arena_solids` — and it is **actively
harmful**: it is what produces the 99 %-of-frame framing computed above.

| where | boom | visible frame (H×W) | Roshan fills |
|---|---|---|---|
| outdoor, boot value (9.0) | 26.1 u | 18.0 × 32.0 | 39 % |
| outdoor, after one castle visit (6.5) | 25.5 u | 17.6 × 31.2 | 40 % |
| **castle interior** | **10.4 u** | **7.1 × 12.7** | **99 %** |

Note the interior boom (10.4 u) is *shorter than the corridor is wide*
(11.3 u) and *shorter than the side rooms are deep* (11.3 u) — so even at this
crushed framing the resolver still clips on almost every heading.

## C2 (critical) — Small rooms cannot host a rear boom at all; they need a different camera

In a 13.3 × 11.3 room, *no* rear boom length works: face the far wall and the
lens is in the doorway wall; face the doorway and it is in the far wall. The
resolver responds by collapsing toward `MIN_BOOM = 0.15` (`camera_kit.gd:21`),
and then `player.gd:1047-1050` **hides the character**:

```gdscript
if visible and boom_len < 2.0:  visible = false
elif not visible and boom_len > 2.6: visible = true
```

So in the basement rooms and against any hall wall, **Roshan disappears** and
the view becomes an accidental first-person 38° lens. Reproduction: back
against any wall in the Grand Hall and turn — focus sits on the padded wall
face, `boom_hit_t` returns ~0, boom collapses, she vanishes.

The pad exemption added on 2026-07-21 (`camera_kit.gd:55-84`) only fires when
the focus is *strictly inside* the pad ring (`st <= 0.0`). Standing flush
against a wall puts the focus a hair *outside* it, `st` is a small positive
number, and the collapse happens with no exemption.

**Fix direction:** replace "shorten the boom" with "**boom-over**": when
`boom_hit_t < 1`, first try raising `cam_high` and re-resolving (pitch down
over the obstacle) before shortening. Interiors under ~20 u on their short
axis should switch to a fixed high-angle room camera — the pattern already
used successfully by `combat_arena.gd:129-135`, `dungeon_puzzle_room.gd:211`
and `stuffie_battle.gd:149`.

## C3 (high) — `cam_high` restore drift: the outdoor camera permanently drops after the first castle visit

Boot value is `cam_high = 9.0` (`player.gd:185`). Every restore writes **6.5**:
`main.gd:4776`, `main.gd:5049`, `main.gd:5085`. There is no path back to 9.0
short of restarting the app. This was flagged as F3 in `CAMERA_AUDIT_2026_07.md`
(2026-07-19) and is still open. A 2.5-unit lower lens means a flatter angle,
which means more terrain and prop occlusion in the *open reef* — i.e. the
castle silently degrades the outdoor camera the child spends most of her time
in. This is likely a direct contributor to "navigating the world feels bad".

## C4 (high) — Camera and player disagree about where the floor is

`CameraKit.ground_y()` claims to mirror the player's floor logic
(`camera_kit.gd:160-161`). It does not:

| | player (`player.gd:785-802`) | CameraKit (`camera_kit.gd:171-188`) |
|---|---|---|
| base floor | `arena_center.y + 2.5` | `arena_center.y + 1.5` |
| overlapping zones | **last match wins** | **`maxf` of all matches** |
| ceiling | **last match wins** | **`minf` of all matches** |

`arena_zones` overlap constantly by design (the castle list has 17 entries with
deliberate overlaps, `castle_hall.gd:571-595`, with comments documenting three
past bugs caused by ordering). Wherever two zones overlap and the *later* one
is not the highest, the lens and the heroine are on different floors.

Related: nothing asserts `floor <= ceil`. The castle zone table can produce
`floor > ceil` in narrow bands (e.g. the undercroft shaft ramp,
`castle_hall.gd:581`, against the basement `ceil: -2.0` of
`castle_hall.gd:577`), where the player is clamped up by the floor and down by
the ceiling in the same frame and pins with `vel.y == 0`.

## C5 (medium) — Camera peek is unusable one-handed, and auto-recenters in under a second

`player.gd:1011-1022`: the touch peek requires a *second* finger dragging while
the first steers (`touch_ui.gd:228-244`). On a phone held in two hands by a
4-year-old, that is not a real control. And once released, the orbit returns
to centre at `1 - pow(0.35, delta)` — a **~0.95 s time constant** — so a peek
cannot be held. Effectively: **there is no way to look around.**

## C6 (medium) — Northern Kingdom has no camera code at all

`grep -n "cam" scripts/arena/northern_kingdom.gd` → **zero hits**. Its grand
hall, mezzanine and roofed town houses all run with whatever `cam_back` was
left over (25 or 6.5), and register **nothing** in `fade_walls`. Open since
F3/F7 of the 2026-07-19 audit.

## C7 (low) — Clip planes are still default

No gameplay camera sets `near`; `player.cam` never sets `far` either
(`player.gd:333-335` sets only `fov`). With `near = 0.05` and `far = 4000` the
depth ratio is 80,000:1, on the Mobile renderer, in a castle built almost
entirely from coplanar 0.28–1.5 u slabs (`castle_hall.gd:360-366`, the floor
segments at `232-235`). Z-fighting flicker on interior surfaces reads as
"the castle looks broken" even when navigation is correct. `near = 0.3` plus a
venue-supplied `far` (300 interior / 900 outdoor) costs nothing.

## C8 (low) — The Sky Lagoon toy-ride camera bypasses the resolver and never snaps back

`sky_lagoon.gd:1899-1903` places the lens by raw lerp with no `CameraKit`
call, and the exit path (`1904-1915`) does not call `player.snap_cam()` — the
chase camera resumes from wherever the toy cam parked it. F4 of the previous
audit, still open for this one site.

---

# PART 3 — CASTLE SPATIAL / STRUCTURAL DEFECTS

## S1 (critical) — The throne dais is not standable; the hall's stated objective can only be reached by an invisible magnet

The HUD tells the child *"Swim up the stairs to Princess Huluu and the Crown
Star!"* (`castle_hall.gd:1275`). What actually happens:

* The royal-stair ramp zone ends at **z = -23.2, floor y = 14.9**
  (`castle_hall.gd:585`).
* The dais solid spans **z -30.8 … -23.2, y -0.8 … 16.8** (`castle_hall.gd:134`,
  size (14,16,6) + pad 0.8).
* `arena_solids` collision is **horizontal-ejection only** (`player.gd:820-839`)
  — a box has no top surface. Nothing can stand on it.
* There is **no `arena_zones` floor over the dais**, so even above y = 16.8
  there is nothing to rest on; she sinks back into the solid and is squirted
  out sideways.

Net: climbing the royal staircase ends at an **invisible wall 3.8 units short
of the throne**, at eye level with Princess Huluu. What rescues it is a
magnet at `castle_hall.gd:1431-1437`:

```gdscript
if in_front and d < 16.0 and ppos.y < crown.position.y - 1.0:
    m.player.position = m.player.position.lerp(crown.position, minf(0.16, delta * 0.5))
```

which drags her ~40 %/s toward the Crown Star while the dais solid pushes her
back out — a tug-of-war between an authored assist and a collider, written
directly to `position` (bypassing all collision) from `main._process`, i.e.
one frame ahead of the player's own solve. **This is the single most awkward
moment in the castle and it is on the critical path of the main objective.**

Fix: add a zone floor over the dais rect (`Rect2(-8, -31, 16, 8)`,
band ≈ 16.5…30, floor 16.8) so the stairs actually arrive somewhere, and
retire the magnet.

## S2 (high) — The Grand Hall has no front wall collider; Roshan can swim out of the castle into the void

Every `_iwall` in `castle_hall.gd` is listed at lines 79-102, 240-242,
438-444, 526-534, 624-647, 723-768, 938-940, 987-989, 1086-1088. **There is no
wall at the hall's entrance (z ≈ +46).** The side walls stop at z = 46
(`castle_hall.gd:95`); the visible entrance facade at z = 45.25
(`castle_hall.gd:360-366`) is built with `_l2_box`, which registers *no*
collider.

The only thing that catches her is the exit trigger — a **sphere of radius 12
around `o + (0, 5, 44)`** (`castle_hall.gd:395`, `1340-1343`). Swim out at
|x| > ~12 and nothing fires: she passes through the painted facade into the
unlit space between the hall and `arena_dome = 90` (`main.gd:4332`), standing
on an invisible plane at `arena_center.y + 2.5` (no zone covers z > 46;
`castle_hall.gd:572` stops at z = 46). Recoverable only by swimming back.

Fix: `_wall_solid` the two entrance panels, or convert the exit test from a
sphere to a z-plane crossing over the full hall width.

## S3 (high) — Vertical navigation is governed by an invisible table that contradicts the visible geometry

**No floor or ceiling slab in the castle has a collider.** Every ceiling
(`castle_hall.gd:112, 239, 452-457, 759, 985, 1084`) is decorative; the
player's vertical bounds come entirely from the 17 hand-authored y-banded
rects in `arena_zones` (`castle_hall.gd:571-595`).

The result is that **some ceilings are swimmable and some are not, with no
visual difference.** Example: the treasure room's y = 33 ceiling
(`castle_hall.gd:239`) is passable — swimming straight up out of the treasure
room lands you in the upper-story Star Chamber (zone `castle_hall.gd:574`,
floor 34.2), bypassing the balcony stairs entirely. The music-room ceiling at
the same height is not passable, because that room lies outside every zone rect
and is capped by the global `arena_ceil = 31` (`main.gd:4333`).

For a non-reader exploring a four-storey building, "which surfaces are real"
is the single most important spatial rule, and it is currently arbitrary.
This is also the root cause class of the three bugs already documented in the
zone table's own comments (`castle_hall.gd:445-451`, `589-591`, `596-600`):
trapped on the top floor, an invisible standable strip, and tunnelling out of
a sealed stairwell.

## S4 (medium) — Every doorway silently loses 3.2 units to collider padding

`_iwall` → `_wall_solid` with the default `pad = 1.6` (`main.gd:1516,1545`).
Since the pad inflates the box on all sides, an aperture between two wall
segments loses 1.6 u from each jamb:

* basement side-room doors: authored 10 u → **6.8 u clear**
* hall back archways: authored 9 u → **5.8 u clear**
* music/bedroom wing doors: authored 10 u → **6.8 u clear**

6.8 u is passable for a point-mass player, but the *camera* also treats the pad
as solid (`camera_kit.gd:72-83` tests the stored, inflated dims when the focus
is outside), so every doorway transit collapses the boom. Combined with C2, a
child walking room-to-room in the basement sees the camera slam in and the
character blink out at every threshold.

## S5 (medium) — The castle's rooms were authored for a top-down read, not for a rear chase camera

The four basement rooms (13.3 × 11.3), the music room (13.1 wide) and the
bedroom (17.3 × 17.3) are all narrower than the outdoor boom (26 u) and
narrower than or comparable to the interior boom (10.4 u). Any of the three
plausible remedies is fine — merge them into fewer, larger rooms; widen them to
≥ 26 u on the short axis; or give rooms under ~20 u a fixed high-angle camera —
but the current combination of "small rooms + rear boom" cannot be tuned into
working.

---

# PART 4 — WAYFINDING

## W1 (high) — Wayfinding is switched OFF in exactly the place that needs it

`_tick_wayfinder` (`main.gd:5949-5958`) explicitly excludes castle interiors:

```gdscript
var level2_court: bool = (game == "level2" and String(g.get("phase","court")) == "court")
if (game != "" and not level2_court) or mg_kind != "" or intro_active:
    return
```

So the sparkle trail runs in the **open reef** (a flat disc, trivially
navigable) and in the lagoon courtyard, and is silent in the **four-storey,
17-zone castle with 12 rooms** — the only genuinely maze-like space in the game.
There is no minimap, no compass and no directional arrow anywhere in the
project (`grep -rn "minimap\|compass" scripts/` → no hits). Castle guidance is
one static three-sparkle Label3D chain toward the Crown Star
(`castle_hall.gd:337-351`) and per-room HUD text a non-reader cannot read.

## W2 (medium) — The trail that does exist points through walls and barely leaves her body

`main.gd:5991-5993` emits three bursts at `t = 0.06, 0.13, 0.20` along the
straight line to the target, every 2.2 s, only when the target is > 22 u away.
It is a straight line, not a path, so it happily points through terrain; and it
covers only the first 20 % of the distance, most of which is inside Roshan's
own 39 %-of-frame silhouette.

---

# PART 5 — TEST COVERAGE GAPS

1. **The camera probes are not in the gate.** `scripts/ci.sh` runs 39 probes;
   `probe_camera.gd` and `probe_castle_cam.gd` — both written specifically for
   the camera audit — are **not among them**. Neither are `probe_upstairs`,
   `probe_basement` or `probe_mouselook`. A camera regression cannot fail CI.
2. **No probe exercises the input layer.** `probe_camera.gd:47` drives with
   `main.player.vel = dir * 16.0`, writing velocity directly. Nothing in the
   suite pushes `touch_ui.stick_vec` and asserts where Roshan ends up, so
   steering, turn rate, drag and the tank-control mapping are untested.
3. **Nothing asserts framing.** No probe checks `boom_len`, the resulting
   on-screen subject size, or `player.visible` — so the "Roshan disappears
   against a wall" behaviour (C2) is invisible to CI.
4. **Nothing asserts the zone table's own invariants.** A static check that no
   `arena_zones` overlap yields `floor > ceil`, and that every ramp's top
   connects to a zone floor rather than a solid's face (S1), would have caught
   the throne dais and at least two of the three bugs already fixed by hand.

---

# PART 6 — RECOMMENDED ORDER OF WORK

Each step is independently shippable and probe-gateable, in the repo's
extract-don't-rewrite style.

**P0 — the two changes that fix most of the felt problem (small, low-risk)**
1. Delete the interior boom hand-tune (`main.gd:4349-4350`) and introduce a
   single `cam_profile` dictionary on main as the one source of truth for
   `back / high / fov / near / far` (this also fixes C3's 9.0-vs-6.5 drift by
   construction). Interior starting point: `back 18 / high 8` (Roshan ≈ 55 % of
   frame), relying on `CameraKit` for clipping.
2. Add venue movement constants next to `arena_dome/arena_ceil`: interior drag
   `pow(0.033, dt)`, turn 3.2 rad/s, gravity 40. Nothing else in the engine
   reads these values, so the change is contained to `player.gd:728-748`.

**P1 — the control scheme**
3. Camera-relative planar steering with a heading slew (N1), touch stick
   `R → ~140` (N4), reverse clamped to 0.6 on the stick (N5).
4. A descend input, or at minimum the asymmetric interior gravity from P0
   step 2 (N2).

**P2 — the castle**
5. Dais floor zone + retire the crown magnet (S1).
6. Entrance wall collider / plane exit test (S2).
7. Give ceilings that are meant to be solid a real collider, or give passable
   ones a visual tell (S3). Audit the zone table for `floor > ceil` (C4).
8. Turn the wayfinder on indoors, targeted at the nearest unvisited room /
   the Crown Star (W1).

**P3 — camera polish**
9. Boom-over before boom-in; room-camera profile for interiors under ~20 u
   (C2). Raise or remove the `visible = false` hack once the boom stops
   collapsing.
10. Reconcile `CameraKit.ground_y/ceil_y` with the player's zone resolution —
    ideally by extracting one shared `floor_ceil_at(m, p)` that both call (C4).
11. `near = 0.3` / venue `far` (C7); Northern Kingdom interior profile and
    `fade_walls` registration (C6); `snap_cam()` on the lagoon toy-ride exit
    (C8).

**P4 — tests**
12. Add `probe_camera` and `probe_castle_cam` to `ci.sh`.
13. New `probe_navigation.gd`: drives through `touch_ui.stick_vec` only, walks
    reef → courtyard → hall → royal stairs → throne → back room → undercroft →
    basement rooms → wings → Dreaming Floor, asserting per frame that
    `player.visible` is true, `boom_len >= 2.6`, the on-screen subject height
    stays inside a 30–65 % band, and that every authored destination is
    reachable without the magnet.

---

## One-paragraph summary for the owner

Navigation feels bad for two independent reasons that compound. First, the
chase camera is set to ten units behind a 38° lens indoors, which makes Roshan
fill 99 % of the screen — the castle isn't small, the camera is. Second, the
swimming model is tuned for open ocean everywhere: she coasts fifteen units
after you let go and needs a twenty-eight-unit circle to turn around, in rooms
eleven to thirteen units wide, with no way to steer up or down at all. Fix the
interior camera distance and add per-venue movement constants and most of the
complaint disappears; after that, the biggest remaining wins are switching the
stick from tank steering to point-where-you-want, making the throne dais
something you can actually stand on, and turning the sparkle wayfinder on
inside the castle instead of only in the wide-open reef.

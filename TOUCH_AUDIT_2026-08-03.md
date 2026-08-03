# Touch control audit — 2026-08-03

Owner report: *"touching the left side of the screen will sometimes cause
motion to the right, specifically in sky lagoon."*

Reproduced by reading the router geometry, not by guessing. Below is what was
wrong, why it was intermittent, what changed, and what now guards it.

---

## 1. Root cause — an invisible d-pad anchored at the far left of a huge bay

`scripts/touch_ui.gd` had three different ideas of where "the movement pad" is:

| definition | rect (viewport-relative) | purpose |
| --- | --- | --- |
| `_stick_hint` | x 26–206, 180 px square, bottom-left | the drawn ghost wheel |
| `rest_zone()` | x 60–280 | "preferred landing spot" |
| `movement_zone()` | x 0 … `max(390, width * 0.34)` | the region that actually claims a press as the stick |

Hybrid `_press()` anchored the stick **origin** to the first of those —
`_fixed_stick_center()`, the centre of the ghost wheel at x ≈ 116 — while
`movement_zone()` claimed presses across the entire lower-left third of the
screen. Every press to the right of x ≈ 138 therefore produced an immediate
**rightward** vector, because that is genuinely which side of the (invisible)
pad centre it landed on.

How much of the thumb bay pushed the wrong way:

| viewport | bay width | share of the bay that pushed RIGHT |
| --- | --- | --- |
| 1280 × 720 | 435 px | 68 % |
| 1600 × 720 (typical phone, landscape) | 544 px | **75 %** |
| 1920 × 864 | 653 px | 79 % |

That is the "sometimes": land left of x ≈ 116 and it steered left correctly;
land anywhere else in the bay — still visually the left edge of the screen —
and it shoved her right, hard, from the first frame.

The premise that made it defensible is gone. `_rest_stick()` hides
`_stick_hint` unconditionally and `probe_ui_system.gd` asserts it stays hidden
("point-to-interact keeps the movement pad renderer hidden"), so the fixed
origin had no visible referent at all. Nothing on screen could tell a
four-year-old where the centre of the pad was.

### Why Sky Lagoon showed it worst

The promenade (`scripts/games/side_scroll.gd::walk_tick`) maps `stick_vec.x`
**straight to screen-space x** at `steer_speed` 18.5 u/s:

```gdscript
if absf(tv.x) > 0.15:
    mx += tv.x
...
x = clampf(x + mx * spd * delta, -half_w, half_w)
```

So a wrong-signed stick is not a slow drift there — it is instant, full-speed
travel in the wrong direction along a side-on stage where left and right are
unambiguous to the player. In the free-swim reef the same wrong sign only
turns the tank-steering yaw, which reads as clumsiness rather than as the
control being backwards.

**Fix:** the hybrid stick origin is now the finger, always
(`scripts/touch_ui.gd::_press`). Drag direction and travel direction are the
same thing everywhere in the bay, which is how Classic mode already worked.
`_fixed_stick_center()` is removed.

---

## 2. The thumb bay was a hole in the world

With the stick claiming the lower-left third, a press there that never became
a drag was swallowed: no stick vector, no world tap, nothing. Tap-to-travel —
the primary verb under the 2.5D charter — simply stopped working in that
corner of the screen.

**Fix:** `_release_stick()` now emits `world_touched` for a hybrid bay press
that never crossed the 22 px slop, so tap-to-travel and tap-to-select work in
the lower-left exactly as everywhere else. A press that *did* drag is
movement and does not also fire a tap. No `TAP_MS` gate on this path: a
four-year-old's deliberate press is slow, and the world-tap owner elsewhere in
the router has no time limit either.

---

## 3. Hold-to-travel walked toward held buttons

`sky_lagoon_promenade.gd::_tick_hold_travel` and
`side_scroll.gd::walk_tick`'s own hold path both read Godot's **emulated
mouse** (`Input.is_mouse_button_pressed` + `get_mouse_position()`). That
pointer knows nothing about touch ownership, and `HOLD_TRAVEL_S` is only
0.20 s. Consequences on the phone:

* Holding the coral **PLAY / JUMP medallion** (bottom-right) for a fifth of a
  second commanded travel toward the bottom-right of the screen — Roshan
  strolled off to the right while the child was just holding the button down.
* A thumb resting in the movement bay drove hold-travel *and* the stick at
  once, with the stick winning every frame (`manual` clears `ss_walk_goal`).

**Fix:** `touch_ui.reserved_zone_hit(pos)` reports when the router already
owns a press at that point (action medallion, thumb bay, pause corner). Both
hold-to-travel paths ask before turning a press into a destination.

---

## 4. What was checked and found correct

* `plane_goal()` / `start_from_screen()` projections — screen-left maps to
  world-left at every camera pan, including when `keep_on_screen` pins the lens
  at a mural edge.
* Multi-finger ownership: a touch keeps one owner for its lifetime; a second
  finger on the medallion does not steal a held stick; overlay open/close
  clears stranded state.
* Focus-loss / app-pause / back-button paths all clear touch state and flush
  the save.
* Classic mode is untouched and remains a genuine runtime rollback.

---

## 5. Guards added

`scripts/probe_touch_stress.gd` (new, in `ci.sh` and the probes workflow, run
with `--hybrid-touch-test`). Everything goes through the real router as
synthetic `InputEventScreenTouch` events — nothing writes `stick_vec` or
`player.position`, because the defect lived entirely in the screen-point →
direction mapping and a probe that pokes `stick_vec` cannot see it.

* **Gate 1 — agreement.** 15 press points across the whole thumb bay × 8 drag
  directions: a press with no drag must steer nowhere, and every drag must
  agree with its own direction to within 0.99. Plus the bay-tap fall-through
  (press taps, drag steers, never both) and the `reserved_zone_hit` contract.
* **Gate 2 — Sky Lagoon.** In the live promenade, taps / holds / drags on the
  left of the screen must carry Roshan **left**, with a wrong-way excursion
  budget of 0.12 stage units, and the mirror case must go right. Includes the
  exact regression point (25 % screen width, deep in the bay) and a 90-frame
  hold on the action medallion that must not move her at all.
* **Gate 3 — churn.** 240 randomized multi-finger events: no frame where the
  stick fights the drag that produced it, and the router must return to rest
  with no leaked owners, no stuck stick and no stuck action.

`scripts/probe_touch_router.gd`'s old assertion — "tapping the visible right
direction must move immediately" — described the fixed pad that no longer
exists and could never have caught this. It is replaced with the
direction-agreement contract, the bay-tap fall-through, and the hold-travel
reservation checks.

### Not covered headlessly

Hold-to-travel itself runs off the emulated mouse, which headless input does
not synthesize from injected touch events. Gate 2 covers taps, holds and drags
through the router; the hold-to-travel path is guarded by its ownership
contract (`reserved_zone_hit`) rather than end-to-end. Confirming the held
medallion on a real phone is still worth one minute of play-testing.

# Reef Grand Prix engine: what is built and how art binds

Status: `IMPLEMENTED_ON_BRANCH` (`claude/reef-kart-engine-20261103`). Machine
checks pass locally. Device, child and owner acceptance are open. Nothing
here is `DELIVERY_ACCEPTED`.

The owner asked Claude to build the engine (2026-11-03) and Codex to produce
all relevant artwork. The engine is original code in the genre's general
manner: a chase camera behind the kart over a projected ground plane, sprite
billboards, speed-raising pickups and item sources. It copies no game's code,
art, sound, track, character, item or name.

## 1. Files

| File | Role |
|---|---|
| `scripts/racer/reef_kart_track.gd` (`ReefKartTrack`) | The Pearl Canal Circuit: centre line, bands, pearls, item bubbles, gem buoys, landmarks, projection, interim floor field |
| `scripts/racer/reef_kart_floor.gdshader` | Canvas shader that projects every ground pixel onto the course plane |
| `scripts/racer/reef_kart_race.gd` (`ReefKartRace`, `Node2D`) | Simulation, steering assist, imp AI, items, camera, sprite/HUD/control drawing |
| `scripts/opera_racer_surface.gd` (`OperaRacerSurface`) | Touch interface and career contract; clocks the engine only while the child plays; existing voice clips |
| `scripts/probe_racer_integration.gd` | Focused engine probe (42 checks with measurements) |
| `scripts/probe_opera_2d.gd` | Trusted career probe; Racer legs updated for the new engine |

The previous engine files (`racer_game_2d.gd`, `kart_driving.gd`,
`kart_canvas_2d.gd`) are untouched; `probe_kart_feel` still covers them.

## 2. Picture and camera (true 2D)

- **Screen.** 1280 x 720, horizon at y 268. Above it: water colour `#2f8fcf`
  and the skyline band (196 px tall, bottom on the horizon).
- **Ground.** One `ColorRect` (1280 x 452) carries the floor shader. A pixel
  `dy` below the horizon is at depth `34 x 560 / dy` world units; its lateral
  offset is `(x - 640) x depth / 560`.
- **Camera.** 82 units behind Roshan's kart at height 34. Its heading follows
  the kart with a 7.5/s ease. The kart's ground contact lands near screen
  (640, 500), and its sprite is about 212 px wide.
- **Billboards.** Pearls, bubbles, buoys, arches, kelp, sparkles, karts and
  landmarks are drawn in depth order by one `Node2D`, at scale 560 / depth.
  Spanning arches are stretched between the lane's two edges.
- **Fixed node tree.** After setup the tree is the engine plus Skyline,
  Ground, Racers, RaceHud and TouchControls. No node is created per frame.

## 3. Driving rules (child-first)

- **Speed.** The kart drives itself at a base top speed of 300 units/s.
  - Each pearl adds 2.5 %, up to 10 pearls, and pearls are never lost.
  - The tan curb (112-140 units off centre) slows the kart to 52 %. The lilac
    wall (140) slides it along at 55 % speed.
  - The zoom item gives 1.4 s at 142 %.
- **Steering assist** (default 0.75):
  - The stick moves the lane she wants, at 120 units/s at full slide.
  - The kart steers itself into that lane and holds it. It follows the
    course heading, corrects toward the lane and feeds the bend's curvature
    forward, so it neither cuts corners nor runs wide.
  - Like traction control, it eases off before a bend the kart cannot hold at
    full speed in her lane.
  - Below 0.75 the raw stick blends back in; at 0 steering is fully manual.
  - Facing the wrong way, the kart turns itself round and a yellow arrow
    shows the way.
- **Items.** She holds one item at a time. The three gem buoys on the front
  straight and the bubble rows under the two pearl arches each deal one after
  a 1 s roulette.
  - Zoom: a boost.
  - Sparkle bubble: flies at 560 units/s or more, homes on the kart ahead and
    spins it for 1 s.
  - Kelp patch: dropped behind; slows whoever drives over it.
  - Pearl bundle: +3 pearls.

  Roshan starts each race holding a zoom. The imp is only dealt zoom or kelp
  and never aims at her.
- **Imp contest** (DL-INT-14). The race is two laps.
  - If the imp crosses first, only the race restarts, after a 1.8 s beat, and
    her pearls are kept.
  - He drives at 88 % after one win and 50 % after two. Ties go to Roshan. He
    spins once early in lap 2.
  - Lead changes and spins trigger existing voice clips (`VOICE.md`).
- **Input gate.** Nothing moves until the first touch. The race freezes 2 s
  after the last held control and on pause or focus loss.

## 4. Touch layout (owner: "Left is control stick, Right is break ... as well as a bubble for the items/boost")

| Control | Geometry (1280 x 720) | Colour now |
|---|---|---|
| Green stick | Grab zone `Rect2(0, 200, 580, 520)`. The ring appears under the finger (clamped to `Rect2(112, 330, 356, 290)`): radius 104, knob radius 52. Steering = sideways slide / 96 px; home (230, 560) | Green `#5fcf7a`, outline `#2f6b46` |
| Item bubble | Centre (1010, 505), radius 70 (+16 hit margin) | Iridescent; shows the held item; pulses when ready |
| Red brake | Centre (1175, 625), radius 80 (+16 hit margin) | Red `#ef5a6f`, white bar |

- One finger owns each control.
- The existing guide hand
  (`assets/opera/worlds/widgets/widget_pipe_guide_hand.png`) sways over the
  stick until she starts, and again after she lets go.
- Keyboard fallback: arrows or A/D steer, Space or Enter uses the item, Down
  or S brakes.

## 5. Art binding contract

Every role below already works with an interim drawing. When the file
exists, the engine uses it instead. No code change is needed to land art.

| Role | Path | Drawn size and anchor |
|---|---|---|
| Course floor | `assets/racer/tracks/pearl_canal/floor.png` | 2048 x 2048; 1 px = 1 world unit; top-left = world (0, 0); mipmaps on |
| Skyline | `assets/racer/tracks/pearl_canal/skyline.png` | 4096 x 256; band in rows 28-256; one camera turn = whole width |
| Standing cards | `assets/racer/tracks/pearl_canal/billboards/<id>.png` | Aspect = w:h in `ReefKartTrack.LANDMARKS`; bottom-centre on the ground |
| Spanning arches | `.../billboards/{pearl_start_arch,ribbon_arch,pearl_arch}.png` | Stretched across the lane between its edges; transparent opening |
| Gem buoys | `assets/racer/pickups/gem_buoy_{teal,lavender,pink}.png` | 56 x 60 world units on the lane; fades to 35 % while popped |
| Pearl pickup | `assets/racer/pickups/pearl.png` | Square, about 16 units across, centre 11 units up |
| Item bubble | `assets/racer/pickups/item_bubble.png` | Square, about 35 units, centre 24 units up |
| Kelp patch | `assets/racer/pickups/kelp_patch.png` | 52 x 22 units, lying on the lane |
| Sparkle bubble | `assets/racer/pickups/sparkle.png` | Square, about 34 units, centre 18 units up |
| Dizzy stars | `assets/racer/pickups/dizzy_stars.png` | 2:1, over a spinning kart |
| Imp kart | `assets/racer/karts/imp_kart_straight.png` (+ `_left`, `_right` optional) | Square, same framing as `assets/kart/chase/kart_straight.png`; lavender runtime tint |
| Item icons | `assets/racer/icons/{zoom,sparkle,kelp,pearls}.png` | Square, shown at 77 px inside the bubble button |

- Roshan's kart keeps the approved chase sprites
  `assets/kart/chase/kart_{straight,left,right,boost}.png`.
- HUD faces are crops of the existing `roshan_racer.png` and
  `rival_racer.png`.
- The interim skyline is the in-game painting's own top band, read from the
  POT tiles.

Rules for every file:

- RGBA PNG, at most 1024 px on the longest side or power-of-two (the floor and
  skyline are POT).
- One `ASSET_LICENSES.md` line in the same commit, naming every source path,
  its SHA-256 and the exact operation.
- A provenance JSON beside the files.

## 6. Measurements (desktop, Godot 4.7.2, headless; numbers only)

| Measure | Value |
|---|---|
| Course length | 4,317.8 world units |
| Tightest bend radius (spline) | 131.5 |
| Closest approach of distant course parts | 533.2 (needs at least 304) |
| Projection round-trip error at the kart's outer limit | 2.5 along, 0.03 across |
| Interim floor field build | 30-77 ms once per process (128 x 128, one channel) |
| Held stick (no steering, no items) | 30.1 s, first attempt, 0 pearls, 0 wall bumps |
| Steering for pearls and using items | 26.0 s, 10 pearls, 4 zooms, 0 curb frames |
| First pearl row, steered into / starting lane | 4 / 0 collected |
| Brake from cruising | 300 to 0 units/s within 1 s |
| Imp win beat | 109 frames (1.8 s) each time; paces 0.88 then 0.50 |
| Average engine step | 144-266 microseconds |

Not measured:

- Device frame time on the Lenovo Tab M11.
- Touch feel and readability.
- Child and owner acceptance.

## 7. Verification

```
GODOT="$(python3 tools/resolve_godot.py)"
$GODOT --headless --path . -s scripts/probe_racer_integration.gd
GODOT=$GODOT scripts/ci.sh
```

Run probes with an isolated `APPDATA`, as `scripts/ci.sh` does.

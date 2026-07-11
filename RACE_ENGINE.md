# Race engine (`scripts/kart.gd`) — reuse guide

The Rainbow Road racer is a self-contained, config-driven arcade race engine.
One node, no scene dependencies: `KartGame.new()` → `configure({...})` (optional)
→ `start(main, finish_cb, reversed)`. Calls `finish_cb(place:int)` and frees itself.

## What it does out of the box
Vehicle select (motorcycle / go-kart / monster truck, distinct handling: speed,
steering rate, slip/drift, wall forgiveness, collision mass) → 3-2-1 countdown →
2-lap race on a banked, width-varying spline loop with zoom strips, shell/star
pickups, pearl rows, a hidden shortcut, mass-weighted kart bumping, rubber-banded
AI (who also fire turbo) → podium celebration → pearl payout into the game economy.

**The core interactive loop:** collecting things charges the TURBO METER; the
player fires it by tap / SPACE / gamepad-A at a moment of their choosing. Camera
FOV and pull-back breathe continuously with speed (boost kicks extra), streak
particles stream past the lens at high speed, and the horizon leans into carves.

**Handling model (see KART_FEEL.md for the full audit):** progress is
curvature-coupled — the inside of a bend is genuinely shorter (±18 % cap), so
the racing line is real and the AI dives for apexes. **SPARKLE DRIFT** is the
skill ceiling: hold a hard steer into a bend to lock a clean carve line
(entry hop), charge SILVER → GOLD → RAINBOW tiers, release for turbo; a wall
scrape spills the charge — the only penalty, no spin-out. Slipstreaming a rival
tows you (+8 %) and trickles meter. Any input held at GO = ROCKET START. Zero
input still finishes every race — assists shape the floor, never the ceiling.
Feel gates run in CI via `scripts/probe_kart_feel.gd`.

A ✕ button (top-right) quits the race at any point before the podium:
`finish_cb` receives **-1** (no payout, no podium), and main restores the
pre-race mode — the player node never moves during a race, so she pops back
out exactly where she entered, with `kart_cool` stopping the same portal from
instantly re-grabbing her.

## Vehicles (assets/vehicles/, licenses in ASSET_LICENSES.md)
| key | model | handling |
|---|---|---|
| `moto` | Cartoony Purple Motorcycle (CC0) | fastest, agile, slippery (drift/lean), fragile on walls, light in bumps |
| `kart` | Go kart (CC-BY, Poly by Google) | balanced baseline |
| `truck` | Quaternius Rover (CC0) | slower, slow-steering, near-immune to walls, shoves everyone (mass 2.0) |
AI racers are assigned vehicles round-robin. A missing GLB falls back to a box
kart, so the engine never breaks on assets.

## Themes & paint jobs
- `theme: "ocean"` (default) — a **seabed race**: sandy caustic-lit track, kelp-glow
  rails, deep-water gradient + fog, rising bubbles, and the game's own corals /
  seaweed / rocks / shells on sand mounds beside the course, plus animated fish
  cruising alongside. `theme: "rainbow"` is the rainbow road, which **orbits
  the Butterfly World** (stage 3) under stage 3's own galaxy-and-aurora sky:
  the meadow planet from galaxy.gd — same shader — raised to loom over the
  inner horizon, wearing the stage's landmarks (amethyst crystal castle at the
  pole, tropical palms + monstera, crystal outcrops — all riding a spin
  carrier so they turn WITH the surface), plus the fresnel atmosphere, two
  candy moons and the seven tinted butterflies. All held inside the loop so
  nothing ever touches the road, the karts or the chase camera; emission-lit,
  no OmniLights, ticked from `_process`. The road wears the GEN2 painted
  rainbow tile `assets/terrain/up_rainbowroad_col.jpg` when present
  (generate with `tools/gen2_rainbow_road.py` — nano banana), falling back
  to procedural stripes; both paths use gentle emission because full-strength
  glow bloomed the near-field road to white on the Mobile renderer.
- **Paint jobs**: after picking a ride, a second select step offers 8 paints
  (Stock, Cherry, Sky, Bubblegum, Lime, Grape, Gold, and **RAINBOW!** — a
  hue-cycling shader). Live preview on the podium; originals cached so repainting
  never compounds. Override the list with `paints` in configure().

## configure() keys (all optional; defaults = ocean course)
`name, theme ("ocean"|"rainbow"), laps, lap_target_sec, road_half,
ctrl (Array[Vector3] loop points), origin, racers (name/col/sprite/player),
vehicles (see VEHICLES for shape), strips / pickups / pearl_rows (u-fraction
placement tables), shortcut:bool, sky_colors:[lo,hi], pearl_payout:bool`

Example — a one-lap lava sprint, no shortcut, same cast:
```gdscript
var g := KartGame.new()
add_child(g)
g.configure({"laps": 1, "lap_target_sec": 24.0, "shortcut": false,
	"sky_colors": [Color(0.08, 0.0, 0.0), Color(0.45, 0.12, 0.02)]})
g.start(self, Callable(self, "_end_kart_game"))
```

Timing was tuned by simulation: moto 42–51s, kart 47–56s, truck 52–61s
(2 laps, before countdown), all inside the target minute. Rubber-banding keeps
the pack tight for any vehicle, so choice = feel, not auto-win.

Known quirk: the go-kart model has a jaunty raised spare wheel baked into its
mesh; it reads as style. If it bothers, swap `vehicles.kart.glb`.

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
FOV kicks + pull-back sell the speed.

## Vehicles (assets/vehicles/, licenses in ASSET_LICENSES.md)
| key | model | handling |
|---|---|---|
| `moto` | Cartoony Purple Motorcycle (CC0) | fastest, agile, slippery (drift/lean), fragile on walls, light in bumps |
| `kart` | Go kart (CC-BY, Poly by Google) | balanced baseline |
| `truck` | Quaternius Rover (CC0) | slower, slow-steering, near-immune to walls, shoves everyone (mass 2.0) |
AI racers are assigned vehicles round-robin. A missing GLB falls back to a box
kart, so the engine never breaks on assets.

## configure() keys (all optional; defaults = Rainbow Road)
`name, laps, lap_target_sec, road_half, ctrl (Array[Vector3] loop points),
origin, racers (name/col/sprite/player), vehicles (see VEHICLES for shape),
strips / pickups / pearl_rows (u-fraction placement tables), shortcut:bool,
sky_colors:[lo,hi], pearl_payout:bool`

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

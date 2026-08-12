# Codex handoff — Mermaid Roshan sprite regeneration requests (2026-08-02)

> **Lifecycle update — 2026-08-09:** R1 is **CLOSED** by the reviewed `_v2`
> frames and the new blocking standalone-frame audit. The source measurements
> below remain historical evidence; later component analysis corrected the
> `_2` rows from “missing hair” to detached generation debris. R2/R3 are
> **DEFERRED OPTIMIZATION**, because the shipped 2D atlas-window table preserves
> every owned pixel and passes its engine-side probes. R4 is **DISMISSED FROM
> THE BUGLIST**: costumes are an optional future design feature, not a defect.
> This handoff is no longer an active work order.

Source audit: `ROSHAN_SPRITE_CUTOFF_AUDIT_2026-08-02.md`.
Measurement tool: `python3 tools/audit_roshan_sprite_clipping.py`.

The runtime slicing bug that clipped Roshan's head across 128 atlas frames is
**already fixed in code** — do not re-fix it in art. What remains below is only
what art can fix: pixels that do not exist in the files, and packing that forces
the runtime to carry a correction table.

Items are ordered by how visible they are to the player.

---

## R1 — Rainbow hair amputated at the canvas edge (highest priority)

Four Sky Lagoon playground sprites have Roshan's rainbow hair lock cut flat
against the PNG border. The pixels are absent from the file, so this is
unrecoverable at runtime.

Path: `assets/sprites/sky_lagoon/roshan_playground/`

| File | Edge | Opaque px on the border | Depth inward | Band rows |
| --- | --- | --- | --- | --- |
| `roshan_slide_3.png` | left (x=0) | 55 | 28 px | y 123–177 |
| `roshan_slide_2.png` | right (x=511) | 49 | 4 px | y 125–173 |
| `roshan_swing_3.png` | left (x=0) | 16 | 1 px | y 149–164 |
| `roshan_swing_2.png` | right (x=511) | 10 | 1 px | y 157–161 |

`_2` and `_3` are mirror images of one another, so this is one authored pose
clipped twice — fixing the source pose fixes both.

**Requested:** regenerate the pose with the full hair lock inside the canvas.
Keep 512×512 and keep the existing figure scale and framing so the Sky Lagoon
placement code needs no change. Target **≥8 px of fully transparent margin on
all four sides**.

**Do not** solve this by scaling Roshan down inside the frame — her size
relative to the playground toys is tuned, and shrinking her would desync the
swing/slide choreography.

---

## R2 — Repack the 2.5D atlases to a true 256 px pitch

`assets/characters/roshan_25d/` — the nine runtime sheets.

The generated sheets pack their figures on a **~236–250 px pitch** instead of
the nominal 256 px cell pitch, and the error accumulates down the sheet:

| Sheet | Real vertical pitch | Drift per row |
| --- | --- | --- |
| `roshan_play_a.png` | 226.8 px | −29.2 px |
| `roshan_gesture_d.png` | 235.0 px | −21.0 px |
| `roshan_swim_front.png` | 239.7 px | −16.3 px |
| `roshan_gesture_c.png` | 240.3 px | −15.7 px |
| `roshan_swim_back.png` | 244.3 px | −11.7 px |
| `roshan_gesture_a.png` | 244.8 px | −11.2 px |
| `roshan_play_b.png` | 246.3 px | −9.7 px |
| `roshan_gesture_b.png` | 246.5 px | −9.5 px |
| `roshan_directional.png` | 250.0 px | −6.0 px |

The runtime compensates with a measured per-frame window table in
`scripts/roshan_sprite_frames.gd`, so nothing is broken today. But the table is
a workaround: it has to be re-measured every time the art is regenerated.

**Requested, whenever these sheets are next regenerated:** place every figure
wholly inside its own 256 px cell, with **≥4 px of transparent margin on all
four sides of the cell**. When that holds, the whole `SHIFTS` table drops to
zero and the workaround retires itself.

**Contract to preserve** (`assets/characters/roshan_25d/README.md` is the
source of truth, and `scripts/player.gd` selects the frames):

- 4 columns per sheet, 256×256 cells, RGBA, power-of-two canvas.
- Row order per sheet is load-bearing — a row is one animation, read left to
  right as four chronological keyframes:
  - `gesture_a`: wave, cheer, clap, twirl
  - `gesture_b`: look, giggle, sleep, point
  - `gesture_c`: collect, boing, hair-twirl, hum
  - `gesture_d`: flop, carry (4×2)
  - `play_a`: swing, climb, ride, land
  - `play_b`: dig-left, dig-right, seated ride, hop
  - `swim_front` / `swim_back`: 16 chronological frames, one seamless cycle
  - `directional` (4×2): front, front-left, left, back-left, back, back-right,
    right, front-right
- Keep her torso anchor stable across frames within a sheet. Two probes assert
  this (`probe_castle_pearl_art`, `probe_l2`) with a **0.11 px** tolerance
  against `scripts/roshan_sprite_anchors.gd`; that anchor table must be
  re-measured alongside any regeneration.

**After landing new sheets, in the same commit:**

```
python3 tools/audit_roshan_sprite_clipping.py --emit-table   # paste into roshan_sprite_frames.gd
python3 tools/audit_roshan_sprite_clipping.py                # must print OK
```

---

## R3 — Frames whose neighbour overlaps their cell

These 13 frames still show a small sliver of the neighbouring figure, because
the two figures overlap far enough that no 256 px window separates them. Only
the first is plausibly noticeable; the rest are listed for completeness.

| Frame | Pose | Ghost | Share of frame |
| --- | --- | --- | --- |
| `play_a[2]` | swing | 715 px | 5.36% |
| `gesture_c[2]` | hair-twirl | 164 px | 1.02% |
| `play_a[1]` | swing | 160 px | 1.19% |
| `gesture_d[3]` | flop | 132 px | 0.87% |
| `play_a[3]` | swing | 34 px | 0.25% |
| `swim_back[4]` | swim | 28 px | 0.24% |
| `gesture_b[8–11]` | sleep | 10–14 px each | ≤0.08% |
| `gesture_c[0]` | collect | 11 px | 0.06% |
| `swim_back[12]` | swim | 9 px | 0.08% |
| `swim_front[12]` | swim | 3 px | 0.02% |

R2's margin rule fixes all of these as a side effect. No separate work needed
if R2 is done.

---

## R4 — Open, not a defect: 2D costume layers

`player.set_costume()` currently records `costume_id` as gameplay state only —
Roshan keeps rendering her base animated atlas, so career costumes are invisible
on the 3D standee. The 13 `assets/opera/worlds/actors/roshan_*.png` costumes
drive the 2D opera career world and lobby only.

All 13 costume PNGs were audited and are **clean** — no clipping, comfortable
margins, no cropping at their placement sites. Nothing to fix.

Flagging only because `scripts/player.gd` carries a standing note that costume
layers can be added "without restoring the retired model path". If costume
layers are wanted on the standee, they need to be authored against the same
per-frame windows as the base atlas — coordinate before generating, or the
layers will drift out of register with her body exactly the way this audit
describes.

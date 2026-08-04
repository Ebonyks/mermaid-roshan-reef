# Codex handoff — animating Mermaid Roshan in the career worlds (2026-08-03)

## The finding

Owner playtest: *"Mermaid Roshan herself is extremely stiff, and often doesn't
show in full resolution. There's a comprehensive animation set already — we
just need to place these sprites over top of it. She may need more sprites."*

Confirmed. A full 2.5D animation set ships in `assets/characters/roshan_25d/`
— an 8-direction atlas, 16-frame swim cycles front and back, and gesture
sheets covering wave, cheer, clap, twirl, look, giggle, sleep, point, collect,
boing, hair-twirl, hum, flop and carry, on a documented sprite contract that
`scripts/player.gd` already drives. **The opera career worlds use none of it.**
They draw one static 512x512 costume portrait per career, tween its `position:y`
for a "bounce", and that is her entire performance across a two-minute act.

## The decision required: how costumes meet animation

The atlases are Roshan in her default outfit. The opera needs her in thirteen
career costumes. Three options were costed against the measured size of the
existing atlases (full working in
`OPERA_FRAMING_PACING_ANIMATION_AUDIT_2026-08-03.md`):

| Option | Files | Frames | Disk | Verdict |
|---|---|---|---|---|
| (a) re-author all 9 runtime atlases per costume | 117 | 1,664 | ~312 MB | **Reject** — triples the APK against a boot audit already flagging 30-40s tablet boot |
| (b) costume overlay on the base animation | 117 | 1,664 | ~100-120 MB | **Reject** — a chef's hat must track her head through a twirl and a flop; that is a second animation, not a decal |
| **(c) reduced per-costume set** | **26** (2 sheets/career) | 312 | **~58 MB** | **RECOMMENDED** |
| (c-lite) fallback | 13 (one sheet/career) | 208 | ~39 MB | loses react + present; combat and curtain call fall back to tweened static |

## The request — option (c)

Two sheets per career, thirteen careers, **26 files**:

- `roshan_<career>_sheet_a.png` — **2048x2048, 4x4 grid of 512x512 cells.**
  Four animations, four chronological keyframes each:
  1. **walk** — the travel cycle along the painted route (she currently glides
     without moving her body)
  2. **work** — the job verb of that career (whisking, sweeping a magnifier,
     piping, patting a baby)
  3. **cheer** — the completion celebration (no beat has one today)
  4. **idle** — a breathing/settle loop for the contemplative pauses
- `roshan_<career>_sheet_b.png` — **2048x1024, 4x2 grid of 512x512 cells.**
  1. **react** — surprise when the imp steals the piece
  2. **present** — the curtain-call bow holding the finished thing

**Why 512 cells, not 256:** she renders at roughly 238x238 on a 1280x720
screen and the existing atlases are 256x256 — she is at or below 1:1 with no
headroom, which is the measured cause of "doesn't show in full resolution."
512 cells give clean headroom at the opera's presentation size and match the
existing 512x512 costume portraits.

**Content locks:** identity per the accepted `roshan_<career>.png` costume
portraits (same outfit, same props, same palette); rainbow tail always, never
legs; consistent cell anchor so frames do not jitter (feet on a common
baseline, horizontal centroid stable); transparent background; POT canvas;
`compress/mode=0` to match every other Roshan sheet.

**Priority:** chef first as the style proof (it is the beat the owner
playtested), then the four other kitchen/stage careers, then the rest.

## Engine work (ours, not codex's)

The opera actor becomes an atlas-driven sprite instead of a static
`TextureRect`: region selection per frame, an animation clock, and a mapping
from opera moments (walking the route, working a station, the steal, the
curtain call) to the six animations above. `player.gd` is the working
reference for frame selection.

## What improved immediately, without new art

Framing fixes already shipped this session (see the audit): the permanent 10%
navy wash over every painting removed; the 1244x124 near-black header replaced
with a compact storybook title plate; the six-portrait audience row — which
covered 57% of the painting's most detailed band — now appears only for the
performance; the crowd meter no longer overlaps the portraits it describes;
and the stage spotlights no longer wash over painted districts. Chrome was
50.8% of the screen; the painting now runs nearly edge to edge.

## One art defect for the backdrop programme (not this handoff)

The career paintings do not reach the screen edges: measured on runtime
frames, a ~68px blurred smear column on the left and ~121px on the right, and
it is **baked into the source art** (`world_chef_c0r0.png` shows near-zero
gradient across columns 0-200 while real detail starts around column 850).
Either the masters need re-rendering full-bleed or the runtime needs a
deliberate framing treatment. Recorded here so it is not mistaken for a
code bug.

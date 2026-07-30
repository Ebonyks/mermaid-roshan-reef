> **Resolution correction (2026-07-29):** This time-bounded audit preserves historical observations below, but its 2172×724/four-tile Sky Lagoon runtime description is superseded. The 2172×724 image is reference-only. Current runtime uses the exact-ratio 6144×2048 v5 master and twelve unscaled 1024×1024 Sprite3D tiles, providing a 2×2 tile group (2048×2048 native coverage) per playable screen. See `SKY_LAGOON_BACKGROUND_RESOLUTION_AUDIT_2026-07-27.md`.
# Visual design audit — the 2.5D redesign, first 48 hours (2026-07-28)

Scope: everything that changed the game's *look* between 2026-07-26 12:00 and
2026-07-28, across `dev` and the branches merged into it. Written against the
two documents the work is accountable to — `GAME_REDESIGN_2P5D_2026-07-27.md`
(the owner charter) and `CODEX_BACKGROUND_FLATS_WORKORDER_2026-07-27.md` (the
art spec).

Every numeric claim below is reproducible:

```
python3 tools/audit_visual_design.py            # the checks, on this repo
python3 tools/audit_visual_design.py --stress   # proof the checks can fail
```

Contract, expansion rules and the Codex workflow: `VISUAL_AUDIT_TOOL.md`.

---

## 1. What landed

| Strand | Where | Author |
|---|---|---|
| E2 engine foundations: parallax `layers` stack + `walk_tick()` promenade travel | `scripts/games/side_scroll.gd` | Claude (P1) |
| Jolt-driven sprite props + shared wave field ("the swell") | `side_scroll.gd` `prop()`, `props_tick()` | Claude |
| **Sky Lagoon rebuilt as a 3-screen 2.5D promenade** | `scripts/arena/sky_lagoon_promenade.gd` (598 lines, new) | Codex |
| Sky Lagoon congruency rebuild: lossless 3:1 panorama, audited standee set | `assets/flats/sky_lagoon/`, `assets/sprites/sky_lagoon/` | Codex |
| Roshan playground animation cards (swing / slide / seesaw, 4 frames each) | `assets/sprites/sky_lagoon/roshan_playground/` | Codex |
| **Fairy pond: 3D GLB reliefs → panoramic sprite stage** | `scripts/games/fairy.gd`, `assets/fairy/` | Codex |
| **Living-world accent layer across 111 stages** | `living_world{,_canvas,_catalog}.gd` (1,395 lines, new) | Codex |
| StorybookUI adopted as the game's UI grammar | `scripts/storybook_ui.gd` | Codex |
| Promenade route, mural-anchored set, lens survival fixes | `sky_lagoon_promenade.gd` | Claude |

That is a genuinely large amount of coherent work in two days, and the parts
that are good are very good.

---

## 2. Pros — what the redesign got right

**The camera problem really is deleted.** `CAM_DIST 47 / CAM_H 9.5 / CAM_FOV 38`
with `look_h == cam_h` is a fixed horizontal lens that cannot be steered,
cannot clip, and cannot lose the player. The charter's second stated reason
for the redesign is fully paid off. This is the single biggest win.

**Navigation collapsed from a volume to a line.** `HALF_D 2.6` against
`HALF_W 72` is a 27:1 ratio — functionally a line the child walks. Combined
with `ROUTE_PAINTED` (nine waypoints from the plane's dock to the castle door)
and `keep_on_screen: true`, getting lost is now structurally impossible in the
Sky Lagoon. Charter reason #1: paid off.

**Touch-the-world is real, and the tap/hold split is right.** `HOLD_TRAVEL_S
0.20` with `touch_travel: false` on the stage config is a careful fix for a
genuine bug (every press used to walk her across the level on the way to
opening a picture frame). Tap belongs to the router, hold on open ground is
travel. That is the correct grammar and it is implemented correctly.

**The art itself is a clear step up.** The panorama is a real painting at
2172×724 native, 3.000000:1, reconstructed losslessly from four unscaled
543×724 tiles with published SHA-256s and a probe that traverses all four
joins at ≤0.3% camera drift. Nothing about that is sloppy. The owner's
judgement that Codex 2D outranks the Blender/Meshy 3D is, on this evidence,
correct.

**Zero fail states preserved throughout.** Two-press activation on the picture
frames, no timers, no losing. The child-safety contract survived a fundamental
rewrite — which is not automatic and deserves saying.

**Rigor is unusually high.** A deterministic congruency gate (`SCENE_CONGRUENCY
10/10`), machine-readable evidence in `audit/`, exact-coordinate previews, and
a new trusted probe for the living-world pass. Codex is not shipping art and
hoping.

**Structural purity of the Sky Lagoon stage.** 44 Sprite3D world cards; zero
MeshInstance3D, zero runtime meshes, zero GLB, zero Sprite2D/Polygon2D world
art, zero shaded world sprites. Whatever else is wrong, the *medium* is
completely consistent — which is exactly what makes the problems below fixable
rather than structural.

---

## 3. Cons — what the redesign got wrong

These are ordered by how much they cost, and every one is measured, not felt.

### 3.1 The 2.5D is 2D. Parallax was traded away to fix a tap bug. `ERROR`

The charter's §1 defines a promenade as "a parallax flat stack — 4–5
Codex-painted layers … sliding at different rates as the camera glides." The
work order defines five layers with `lock` factors from 1.0 (sky) to 0.0
(skirt).

What shipped is **one painting**: four side-by-side tiles of a single
panorama at one depth (`BACKDROP_Z −18.0`). Four files, one layer, zero
parallax. And every standee was then welded to that same plane:

```
DRESS_Z    -17.90      CLOUD_Z    -17.95      LANDMARK_Z -17.85
PLAY_Z     -17.80      FRAME_Z    -17.75      NEAR_Z     -17.70
```

A total depth spread of **0.30 world units** in front of a mural 18 units back
and a lens 47 units back. The code's own comment states the intent plainly:
"0.4 units of separation is under 1% of parallax, far below anything the eye
reads."

The cause is documented and honest: a standee 12 units in front of the mural
parallaxes ~24% faster than the art it stands on, so panning slid the whole
playground across the painted lawn, and the castle-gate tap target drifted
237 px off the painted door. Both were real bugs. But the fix chosen — collapse
the depth axis — pays for a tap-projection bug with the entire visual premise
of the redesign. The correct fix is to project tap targets through the live
lens each frame (the machinery already exists in `_target_at`) and to paint
the mural in separated layers so the playground *belongs* to a mid-ground that
moves with it.

`scripts/games/side_scroll.gd:439` iterates `m.g["ss_layers"]` to apply
per-layer lock glide. On the promenade that array is **empty** — the P1
parallax engine has never once run in the shipped game.

### 3.2 Roshan can never pass behind anything. `ERROR`

The layering rule the owner wrote on 2026-07-27 is explicit: standees stand
"at a real depth inside or around the band" so that "Roshan passes **in front
of or behind** each one depending on her z, sorted by the real depth buffer —
this is what makes her interaction with the stage and its objects read true."

All six world-card depths sit at ≈−17.8. The walk band's far edge is −2.6.
Every card is 15 units behind the deepest point she can reach. She passes in
front of the slide, the swing, the seesaw, the plane, the firs, the castle
gate — all of them, always. The `flat()` primitive that exists precisely to
make this work (alpha-scissor, depth-writing, contact shadow) is not used by
the promenade at all.

The result is a paper-doll on a backdrop, not a diorama. This is the finding
that most directly contradicts the owner's stated heart of the look.

### 3.3 The contrast rule is inverted. `ERROR`

The work order: "the play plane stays LOW detail and LOW saturation relative
to characters and tap targets. Backgrounds frame; they never compete with the
things a finger should find."

Measured mean saturation over opaque pixels:

| | Saturation | Luminance |
|---|---:|---:|
| Panorama tiles (background) | **0.551** | 0.566 |
| Standees + Roshan (foreground) | **0.412** | 0.556 |
| Ratio | **1.34×** | Δ 0.010 |

The background is 34% more saturated than everything standing on it, and the
figure/ground luminance delta is 0.010 — effectively zero. Both channels a
4-year-old uses to find a tap target are working *against* her. The same
inversion, milder, is in the fairy pond (1.12×, Δ 0.039).

This is the most fixable of the three: it is a repaint of the mural, not a
rearchitecture, and it is worth more to the child than anything else on this
list.

### 3.4 The redesign shipped with no way back. `ERROR`

Charter §3 P2: the new world ships "behind an additive save key `world_style`
(`"classic"` default until sign-off, `"storybook"` = the new world), toggled
from the pause menu like Hybrid/Classic."

`world_style` does not exist anywhere in the codebase. The promenade replaced
the 3D Sky Lagoon live, in one commit, with no toggle. Eight substantially
authored legacy stages (gatehouse, courtyard, playground, fairy pond,
castle exterior, rainbow junction, alpine village, alpine mountain) went
unreachable — `LIVING_WORLD_STAGE_AUDIT_2026-07-27.md` records them as
"Authored legacy … the current entry route selects the painted promenade
first."

The charter's reversibility culture is the reason this project can move fast
safely. This is the one finding that is a process failure rather than a craft
one, and it is the one worth fixing first, because it is what makes every
other fix safe to attempt.

### 3.5 The pilot was skipped. `WARN`

Charter §2 orders the migration reef → castle → courtyard → Sky Lagoon,
"chosen so the cheapest, highest-traffic spaces prove the rig first." The
reef pilot exists to have its device test **revise the layer spec** before
other zones commit to it (§3 P3, and the work order's own closing line:
"do not start [batches 3–6] speculatively — the reef pilot's device test may
revise the layer spec").

`scripts/promenade.gd` — the P2 satellite — does not exist. Zone #4 shipped
first, and the three findings above are precisely the kind of spec revision
the pilot was supposed to surface cheaply.

### 3.6 The living-world layer has no depth, and one composition for 111 stages. `WARN`

`living_world_canvas.gd` is a single full-rect `Control` on a `CanvasLayer`
drawing vector motifs with `draw_circle`/`draw_arc`/`draw_polyline`. Per
stage it draws exactly two accents — one at screen x≈48, one at screen
x≈(width−50) — plus one idle event, at alpha 0.25–0.30.

What's right about it: one bounded renderer, no timers/tweens/particles, no
gameplay state, no per-stage cost, probe-gated, and 111 stages covered in one
pass. As engineering it is disciplined and cheap.

What's wrong with it as *visual design*:

- It is **screen-space in a depth-graded world**. The accents cannot occlude,
  be occluded, or parallax. In a redesign whose central rule is "intentional
  layering of 2D designs in 3D space," the newest and largest visual feature
  has no z at all. On the promenade the camera pans and the bubbles stay
  pinned to the screen edge — which reads as UI, not as life.
- **The choreography is identical on every stage.** The motif token changes
  (bubble/fish/frond/sparkle); the two screen positions do not. Wreck Canyon
  and the opera lobby get the same two corners animated the same way.
- It occupies the screen corners — exactly the region the work order reserves
  for the L4 foreground vignette. When real L4 flats land, they will collide.
- At alpha 0.25–0.30 over a 0.55-saturation mural, much of it will simply not
  be visible on the M11.
- The audit doc's claim to "animate every authored stage" overstates what
  happened: the stages are not animated; a flat overlay is drawn in front of
  them. (The promenade's own fir sway, cloud drift and plane bob in
  `_tick_ambient_life()` are real world-space motion — and are better.)

### 3.7 Asset hygiene: three generations of everything still ship. `WARN`

16 of 43 PNGs under the Sky Lagoon roots are referenced by no script or scene
— **8.6 MB** of superseded art in the APK. Seven asset families ship multiple
generations simultaneously:

```
sky_lagoon_slide.png  →  _v3.png  →  _v3_compact.png     (all three shipping)
sky_lagoon_swing.png  →  _v3.png  →  _v3_compact.png
sky_lagoon_seesaw.png →  _v4.png  →  _v4_compact.png
plane, castle_gate, activity_frame, cloud_family          (two each)
flat_..._panorama_tile_{0..2}.png                          (v1, superseded by v2)
```

Also: 14 of 26 Sky Lagoon runtime textures are non-power-of-two (543×724,
294×420, 254×320, …). Legal under the CLAUDE.md rule (≤1024px), but they
cannot VRAM-compress, so **11.2 MB ships uncompressed on the Mali GPU**. And
none of the new art carries a tracked `.import` sidecar — `*.import` is
gitignored for new files while 1,451 historical ones remain tracked — so the
compression mode, mipmap setting, and the NPOT/`compress mode=2` combination
that CLAUDE.md warns deadlocks the importer are all unreviewable in-repo.

Galaxy (11.7 MB, 32/32 PNGs) and Castle (1.8 MB, 6/6) have the same orphan
problem from earlier work; it is not new, but it is now measured.

---

## 4. Zone-by-zone

### Sky Lagoon promenade — `promenade_2p5d`, shipped, 3 screens

**Works.** Fixed lens, unloseable navigation, painted route with nine
waypoints, doorstep arrival with an 8-unit re-arm so returning from the castle
can't re-trigger it, two-press activation on picture frames, Roshan's
dedicated swing/slide/seesaw card sequences with equipment-relative paths
rescaled to the corrected prop sizes, lossless seam-free panorama, structural
purity (44 Sprite3D cards, 0 meshes), `probe_l2` traversing all four tile
joins.

**Doesn't.** One mural layer, not five (§3.1). 0.30 units of total card depth
(§3.1). No occlusion of Roshan by anything (§3.2). Background 1.34× the
foreground saturation with a 0.010 luminance delta (§3.3). No `world_style`
toggle and eight legacy stages stranded (§3.4). Shipped ahead of the pilot
(§3.5). 8.6 MB of orphaned art, 11.2 MB uncompressible (§3.7). The engine's
`layers` API bypassed by hand-placed backdrop cards.

**Highest-value fix, in order:** repaint the mural into L0/L1/L2/L3 with the
play-plane band desaturated → restore standee depth with per-frame tap
projection → add `world_style`.

### Fairy pond — `overhead_2d`, shipped

**Works.** The 3D→sprite migration is exactly the direction the charter set,
and it landed cleanly: GLB reliefs retired, boss stages, bugs, ornaments and
the two readability cues (mint/gold helpful ring, coral/plum danger halo) all
become 1024×1024 alpha cards. `alpha_cut = ALPHA_CUT_DISCARD`, `shaded =
false`, shadows off — correct settings. Nonverbal cue design is genuinely good
child UX. Charter-compliant as an overhead fixed-camera stage (no parallax
expected, and the audit tool does not demand it).

**Doesn't.** Contrast inverted, mildly: background 0.512 vs foreground 0.457
(1.12×), luminance delta 0.039. The `pond_panorama.png` is 4096×1024 — POT and
therefore compressible, but the zone's runtime art still decodes to 68 MB
(~17 MB compressed): thirteen 1024² cards is a lot of texture for one pond
when most of them are one small subject on transparent padding. No `.import`
sidecars.

### Living-world layer — `screen_overlay`, shipped across 111 stages

Covered in §3.6. Summary: excellent engineering discipline, weak as visual
design, and mis-described in its own audit doc. It should be re-homed into
world space — `SideScrollStage.flat()` accents at real depth on staged zones,
and the existing per-zone `tick()` motion elsewhere — with the canvas kept
only for genuinely screen-space moments.

### Reef — `free_swim_3d`, not migrated

The charter's zone #1 and the pilot that was meant to prove the rig. Unstarted:
no `scripts/promenade.gd`, no reef flats, `world_style` absent. This is the
gap that caused §3.5 and, indirectly, §3.1–3.3. Everything learned from the
Sky Lagoon should now flow into the reef set *before* it is painted.

### Pearl Castle — `free_swim_3d`, not migrated (charter #2)

Untouched by the 2.5D work; received the living-world overlay only. 6 orphaned
PNGs (1.8 MB). Its 21 interior stages are, per the charter, "the easiest
flats" — and it is the highest-traffic space in the game after the reef. It
should be zone #2 for real.

### Courtyard (#3), Northern (#5), Ember (#6), Galaxy (#7)

Untouched, overlay only. Galaxy carries 11.7 MB of fully orphaned PNGs and is
the charter's explicit "last, or retired to a picture-game" call — that
decision is now overdue enough to be worth making, because 11.7 MB of dead
weight in the APK is a real cost on a 3-year-old phone.

### Opera house and acts — `staged_2d`, shipped

Active churn in the window (7 commits to `opera_act.gd`, 8 to
`opera_house.gd`). Already compliant per the charter's inventory (staged sets,
flat art, fixed camera) and gated by `probe_opera` + `probe_opera_art` plus
the advisory balance playtest. No new visual regressions found. Its art lives
in GLBs (2.9 MB, 53 files), so it is outside the flat-art checks — declaring
its flats in the spec is the natural next expansion.

### Storybook UI — `ui`, shipped

`StorybookUI` is Godot-native `Control`s only, no flat runtime textures, with
`MIN_TOUCH := Vector2(110, 110)` as an explicit constant. That constant is now
the basis of the tool's `readability.tap_target_size` check. Consistent ink /
paper / lavender / mint / coral / gold palette. This is the cleanest strand of
the 48 hours and the right grammar for the age group.

### Picture games — `canvas_2d`, shipped

Unchanged in substance, K2 canvas, gated by `probe_mg2d`. Compliant.

---

## 5. Verdict

The engineering is strong, the art is better than what it replaced, and the
two charter goals that motivated the redesign — camera and navigation — are
genuinely achieved. What was lost is the third thing the charter was *for*:
the layered depth that makes it 2.5D rather than a painted backdrop with a
sticker on it. That loss was a deliberate, documented trade to fix a real tap
bug, and it is reversible.

The four fixes, in priority order:

1. **Add `world_style`.** Restore the way back before anything else changes.
2. **Repaint the Sky Lagoon mural as L0–L3 with a desaturated play plane.**
   Cheapest change, biggest effect on the child.
3. **Restore standee depth**, with tap targets projected through the live lens
   each frame instead of welded to the mural plane.
4. **Paint the reef set with all of the above already learned** — and run its
   device test before batches 3–6.

None of this is a rollback. It is finishing what the charter described.

---

## 6. The audit tool

This document is a snapshot; the tool is the part that survives. Everything in
§2–§4 that carries a number is a check in `tools/audit_visual_design.py`,
driven by `tools/visual_audit_spec.json`, and provably falsifiable via
`--stress`. Adding a zone is a JSON edit. Adding a rule is a decorated
function plus a stress case — and the stress pass fails if you forget the
case.

Full contract, extension guide and the stress protocol: **`VISUAL_AUDIT_TOOL.md`**.

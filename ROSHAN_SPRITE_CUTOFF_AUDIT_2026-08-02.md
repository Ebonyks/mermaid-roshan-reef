# Mermaid Roshan sprite placement & cutoff audit — 2026-08-02

> **Lifecycle update — 2026-08-09:** Defect A remains closed and its atlas
> audit is now a blocking gate. The four playground-file findings are also
> closed by the versioned `_v2` runtime frames: the `_2` files were re-triaged
> as detached edge debris and cleaned without changing Roshan; the genuinely
> clipped `_3` hair silhouettes were regenerated as complete 2D cutouts.
> `tools/audit_roshan_sprite_clipping.py` now verifies all twelve active
> playground frames, their exact runtime roster, margins, canvas size, alpha,
> and single-component silhouettes. The old four files were removed from the
> export pool. Atlas repacking and optional costume layers are design backlog,
> not current bugs, and are excluded from master-audit closure.

Game-wide audit of where Roshan's 2.5D sprite renders cut off, why, and what
was fixed conservatively in this pass. Every number here is measured from the
shipped art by `tools/audit_roshan_sprite_clipping.py`; nothing is estimated.

**Headline:** the 4-year-old is currently shown a **headless Roshan** during the
Sky Lagoon "land" pose, and a **disembodied floating head** during the "ride"
pose. Both are code-side slicing bugs against correct art, and both are fixed
in this pass without touching a single source pixel.

---

## 1. What was audited

| Surface | Files | Verdict |
| --- | --- | --- |
| 2.5D animation atlases | 9 sheets, 128 frames | **BROKEN — fixed here** |
| Opera career costumes (Roshan) | 13 PNGs | Clean |
| Opera rivals / imps | 10 PNGs | Clean |
| Sky Lagoon playground poses | 12 PNGs | **4 clipped in source art — Codex** |
| Standalone cutouts / skins | `roshan_base`, `roshan_sprite`, `fairy_mermaid`, `sky_lagoon_roshan` | Clean |
| Runtime placement (clip containers, stretch modes) | lobby cards, career world, HUD | Clean |

Two genuinely different defects were found. They need different fixes and are
kept strictly apart below.

---

## 2. Defect A — atlas cell drift (code-side, FIXED)

### The mechanism

`scripts/player.gd` and `scripts/roshan_sprite_loop.gd` slice the 1024×1024
sheets with `hframes`/`vframes`, which assumes each figure sits inside an exact
256 px cell. The generated sheets do not: they pack their figures on a **~236–250 px
pitch**, and the error accumulates down the sheet.

| Sheet | Real vertical pitch | Drift vs the 256 px grid |
| --- | --- | --- |
| `play_a` | 226.8 px | −29.2 px per row |
| `gesture_d` | 235.0 px | −21.0 px |
| `swim_front` | 239.7 px | −16.3 px |
| `gesture_c` | 240.3 px | −15.7 px |
| `swim_back` | 244.3 px | −11.7 px |
| `gesture_a` | 244.8 px | −11.2 px |
| `play_b` | 246.3 px | −9.7 px |
| `gesture_b` | 246.5 px | −9.5 px |
| `directional` | 250.0 px | −6.0 px |

Row 0 is fine, so this never showed up in a spot-check. By row 3 the figure has
drifted up to 65 px above its own cell, which produces **two simultaneous
artifacts**:

1. the top of Roshan's head is sliced off in the lower rows, and
2. the slice reappears as a **ghost sliver of the next pose's head** along the
   bottom edge of the row above.

### Measured damage (before)

**37,531 px of Roshan — 1.93% of all her authored art — never reached the
screen**, and the identical 37,531 px rendered in the wrong frame as ghosting.

Worst frames:

| Frame | Pose | Roshan lost | Ghost shown |
| --- | --- | --- | --- |
| `play_a[12]` | land | **36.23%** | — |
| `play_a[13]` | land | 28.57% | — |
| `play_a[15]` | land | 27.38% | — |
| `play_a[14]` | land | 20.60% | — |
| `play_a[11]` | ride | 16.15% | 3,815 px |
| `gesture_c[14]` | hum | 9.60% | — |
| `swim_front[15]` | swim | 9.46% | — |
| `gesture_c[13]` | hairtwirl | 8.56% | — |
| `play_a[8]` | ride | 0.92% | **5,205 px** |

`play_a` rows 2–3 are the Sky Lagoon climb/ride/land choreography — the poses a
child triggers by playing on the toys, i.e. the most-looked-at frames in the game.

### The fix

`scripts/roshan_sprite_frames.gd` (new) carries a measured per-frame
translation of each frame's **256×256 sampling window** onto the figure that
frame owns. The window size never changes.

Paired with `offset_correction()`, the correction is **provably lossless**. For
a texel at `(X, Y)`, Sprite3D maps screen position as
`x ∝ (X − origin.x) − 128 + offset.x` and `y ∝ 128 − (Y − origin.y) + offset.y`.
Shifting the window by `s` and adding `(s.x, −s.y)` to `offset` cancels exactly:

```
x' = (X − Cx − sx) − 128 + (Ax + sx) = (X − Cx) − 128 + Ax = x
y' = 128 − (Y − Cy − sy) + (Ay − sy) = 128 − (Y − Cy) + Ay = y
```

So **every pixel that renders today keeps its exact screen position** — her
tail, her contact shadow and her ground alignment do not move by a subpixel —
and the clipped art simply reappears. When `flip_h` is set the horizontal term
is negated, matching the convention already used by `RoshanSpriteAnchors`.

`hframes`/`vframes` are deliberately left set, because `CastleRooms25D` still
reads them to derive frame size.

> **CORRECTION (2026-08-03).** This section originally also claimed that
> "Sprite3D ignores `hframes`/`vframes` once `region_enabled` is on". That is
> false — it is `Sprite2D` that behaves that way. `Sprite3D` re-divides
> `region_rect` by the grid, and the mistake made Roshan invisible on the
> phone. See §8; the window arithmetic above is unchanged and still holds.

### Result

```
naive 256px grid :  37531 px of Roshan clipped,  37531 px ghost
shipped windows  :      0 px of Roshan clipped,   1302 px ghost
                   (1.93% -> 0.00% of her art lost)
OK: every Roshan frame renders whole
```

Visual before/after — regenerate on demand with
`python3 tools/audit_roshan_sprite_clipping.py --contact`, which writes
`audit/roshan_sprite/roshan_frame_windows.png` (red = art the naive grid
discards, green = art the fix recovers). `/audit/` is gitignored, so the sheet
is produced locally rather than committed.

### Coverage

Fixing two files covers essentially the whole game, because every Roshan
renderer goes through one of them:

- `scripts/player.gd` — the primary player, all 9 sheets.
- `scripts/roshan_sprite_loop.gd` — the shared standee loop, used by
  `opera_act`, `opera_house`, `kart`, `galaxy`, `ember_fortress`,
  `combat_arena`, `dungeon_puzzle_room`, `arena/castle_rooms_25d` and
  `arena/sky_lagoon_promenade`.

`ember_fortress.gd` and `galaxy.gd` also set `hframes/vframes` directly, but
only to seed frame 0 before handing the sprite to the loop — and frame 0
carries a zero shift on every sheet, so there is no seam.

---

## 3. Defect B — source art clipped at the canvas edge (Codex)

Four Sky Lagoon playground sprites have Roshan's **rainbow hair lock amputated
flat against the PNG border**. These pixels do not exist in the file, so no
runtime change can recover them — this is a regeneration item.

| File | Edge | Opaque pixels on the border | Depth inward |
| --- | --- | --- | --- |
| `roshan_slide_3.png` | left | 55 px | 28 px |
| `roshan_slide_2.png` | right | 49 px | 4 px |
| `roshan_swing_3.png` | left | 16 px | 1 px |
| `roshan_swing_2.png` | right | 10 px | 1 px |

The `_2`/`_3` pairs are mirror images of one another, so this is one authored
pose cut off twice. Details and the requested fix are in
`CODEX_ROSHAN_SPRITE_REGENERATION_2026-08-02.md`.

---

## 4. Costumes — clean

All 13 `assets/opera/worlds/actors/roshan_*.png` career costumes were checked
for border contact and for cropping at their placement sites. **None is
clipped.** Margins are comfortable and consistent (typically L/R 20–70 px,
T ~17 px, B ~8 px inside a 512×512 canvas).

Placement is also safe: the opera lobby card sets `clip_contents = true`, but
the actor rect is `Rect2(18, 8, 190, 240)` inside a 226×336 card, so it cannot
reach the clip boundary. Every Roshan `TextureRect` in the game uses
`STRETCH_KEEP_ASPECT_CENTERED`, which letterboxes rather than crops — no
`KEEP_ASPECT_COVERED` (the cropping mode) is used anywhere.

Note that costumes are currently **gameplay state only**: `player.set_costume()`
records `costume_id` and Roshan keeps rendering her base animated atlas. The
costume PNGs above drive the 2D opera career world and lobby, not the 3D
standee. So the Defect A fix is what governs how she looks in costume scenes
today.

---

## 5. Regression gate

```
python3 tools/audit_roshan_sprite_clipping.py               # exits 1 if any frame clips Roshan
python3 tools/audit_roshan_sprite_clipping.py --emit-table  # regenerate the GDScript table
python3 tools/audit_roshan_sprite_clipping.py --contact     # write the before/after contact sheet
```

The tool parses the `SHIFTS` table out of `scripts/roshan_sprite_frames.gd`, so
it validates **what actually ships**, not a copy of the numbers.

**This must be re-run after any regeneration of `assets/characters/roshan_25d/`.**
New art means new packing, which means the table is stale and Roshan will be
clipped again. Re-emit the table in the same commit that lands new sheets.

This tool is not yet wired into `.github/workflows/probes.yml`; CI workflow
files are explicit-task-only under the CLAUDE.md security rules, so adding the
gate is left as an owner decision. Recommended, and it is a one-line addition.

---

## 6. Residual ghosting — 1,302 px (Codex)

13 frames keep a small ghost because the neighbouring figure genuinely overlaps
into this frame's cell, so no 256 px window separates them. All are ≤1.2% of the
frame except one:

| Frame | Ghost | Share of frame |
| --- | --- | --- |
| `play_a[2]` (swing) | 715 px | 5.36% |
| `gesture_c[2]` (hairtwirl) | 164 px | 1.02% |
| `play_a[1]` (swing) | 160 px | 1.19% |
| `gesture_d[3]` (flop) | 132 px | 0.87% |
| `play_a[3]`, `swim_back[4]`, `gesture_b[8–11]`, `gesture_c[0]`, `swim_back[12]`, `swim_front[12]` | 3–34 px each | ≤0.25% |

Only `play_a[2]` is plausibly noticeable. These are listed for the Codex pass;
they are not worth a code workaround.

---

## 7. What was deliberately NOT done

Per the brief, larger changes are left to the Codex art pass:

- **No source PNG was modified, recompressed or substituted.** The fix is
  entirely a sampling-window change.
- **No repacking of the atlases.** Repacking to a true 256 px pitch is the
  correct long-term fix and would let the whole `SHIFTS` table go to zero — it
  belongs with the regeneration, not with a conservative pass.
- **No canvas expansion** for the four clipped playground sprites.
- **No new costume layers.** Roshan still renders her base atlas while wearing
  a costume id; adding 2D costume layers remains open work.
- **No CI workflow edit** (high-risk file per CLAUDE.md).

---

## 8. Defect C — the corrected window never reached the screen (2026-08-03)

**Owner report:** "Roshan's sprite is not currently visible." Two phone
screenshots: the castle main hall with **no Roshan at all**, and the Sky Lagoon
promenade showing a **hard-edged rectangle containing only her hair**.

Both are the same regression, introduced by the Defect A fix in `ca1381b8`.

### The mechanism

The fix handed each frame's corrected window to `Sprite3D.region_rect` as a
single 256×256 cell, on the belief that a region overrides `hframes`/`vframes`.
That is true of `Sprite2D`. It is **not** true of `Sprite3D`, which treats the
region as the whole atlas and re-divides it (`Sprite3D::_draw`):

```cpp
base_rect    = region ? region_rect : Rect2(0, 0, tex_w, tex_h);
frame_size   = base_rect.size / Size2(hframes, vframes);
frame_offset = Point2(frame % hframes, frame / hframes) * frame_size;
src_rect     = Rect2(base_rect.position + frame_offset, frame_size);
dst_rect     = Rect2(dst_offset, frame_size);          // the quad shrinks too
```

Handing over one cell therefore asked for a **sub-cell of that cell** — 64×64 on
a 4×4 sheet, 64×128 on a 4×2 sheet — sampled at the wrong place and drawn at a
quarter of the intended size. What the child actually saw:

| Where | Frame | Window the engine sampled | Alpha inside it | On screen |
| --- | --- | --- | --- | --- |
| Castle main hall | `directional[0]` | `(0, 0, 64, 128)` | **0.0%** | nothing |
| Sky Lagoon idle | `directional[2]` | `(640, 0, 64, 128)` | 53.6% | a strip of hair |
| Sky Lagoon swim | `swim_back[6]` | `(620, 315, 64, 64)` | 72.4% | a strip of hair |
| Sky Lagoon land | `play_a[12]` | `(0, 895, 64, 64)` | 0.0% | nothing |

64 of the 128 frames sampled a window under 6% alpha — she was simply gone in
half of them, and a sliver in the rest.

### The fix

The window is expressed in the grid the engine actually slices with: the whole
sheet, translated by the shift.

```gdscript
sprite.region_rect = Rect2(shift, Vector2(hframes, vframes) * CELL)
```

The engine's own division then lands on exactly `cell + shift` at the unchanged
256×256 cell size — verified for all 128 frames, all in bounds. Frames with a
zero shift (55 of 128, including every row 0) now disable the region entirely,
so the common case is bit-identical to the pre-`ca1381b8` renderer. Defect A's
recovered pixels and `offset_correction()` are untouched.

One consequential site had to be taught about the region as well:
`SkyLagoonPromenade._start_playground_animation()` takes the card over for the
authored swing/slide/seesaw poses — whole PNGs, not atlas cells — and reset
`hframes`/`vframes`/`frame` but not `region_enabled`, so a stale window sliced
the pose. It now clears it.

### Why the probes were green

Every existing assertion tested the **table's intent** — `region()`, `shift()`,
the anchor rebase — and none tested what `Sprite3D` would do with it. The audit
tool has the same blind spot by construction: it measures the art and the
`SHIFTS` numbers, never the engine's consumption of them.

Three assertions now close that gap, all in probes already gated by CI:

- `probe_castle_pearl_art` → `roshan_frames_sample_their_own_window`: for all
  128 frames of all 9 sheets, the rect Sprite3D will sample (derived with the
  engine's own arithmetic, `RoshanSpriteFrames.sampled_rect()`) must equal the
  window the table intends. This fails loudly on the shipped regression.
- `probe_castle_pearl_art` → `roshan_frames_render_real_art`: every sampled
  window must contain at least 10% lit pixels of the authored PNG. Measured
  floor on the shipped sheets is 17.6%; the broken windows sat at 0.0%.
- `probe_l2` → `sky_lagoon_roshan_samples_her_own_window` and
  `playground_pose_shows_the_whole_authored_png`.

`probe_l2` and `probe_castle_pearl_art` are in both `scripts/ci.sh` and
`.github/workflows/probes.yml`, so no CI workflow file needed editing.

### Standing lesson

A window that is *computed* correctly is not a window that *renders*. Any future
change to how Roshan is sliced must assert the engine-side result, not the
intent — that is what `sampled_rect()` exists for.

# Castle sprite transparency and cut-off audit (2026-09-25)

**Status:** evidence and recommendations only. Prepared by Claude, which made no
game changes; Codex implements. Nothing here grants visual, device, child or
owner acceptance.

**Baseline:** `dev` at `f76a8ba5`, exact Godot 4.7.2, Windows desktop display
build at 1280×720 logical (captured at 2560×1369), isolated test saves.

## What was checked

1. **Every object drawn in the castle.** A capture script
   ([`tools/inventory.gd`](tools/inventory.gd)) booted the real game, visited all
   13 castle rooms in free play plus the four Day One dirty rooms, and recorded
   every visible `Sprite2D`, `AnimatedSprite2D`, `TextureRect`, `TextureButton`
   and `NinePatchRect`, with the exact texture region each one draws: 345 draws,
   217 unique images ([`data/inventory_*.json`](data/)).
2. **Measured each drawn image** ([`tools/analyze.py`](tools/analyze.py)):
   - art touching the card edge (cut off);
   - detached pieces near the edge (bled in from a neighbouring frame);
   - partly transparent areas inside a solid silhouette (see-through);
   - light halos or black matte rims;
   - baked checkerboards;
   - cards with no transparency at all.
3. **Swept every cell of 53 sprite sheets**, not just the frame on screen at
   capture time ([`tools/sweep_sheets.py`](tools/sweep_sheets.py)). This found
   bleed in frames that only appear mid-animation.
4. **Reviewed every flag by eye.** Intended effects were set aside, for example
   dust puffs, a brush lifted mid-dip, ghost-hand halos, shadows, a net and
   outlines (see [Reviewed and not errors](#reviewed-and-not-errors)).

The Grand Puff arena could not be captured in this pass; its sheets were covered
by the cell sweep instead.

## Findings

Severity: **P1** visible in normal play at phone size, **P2** visible when
looking or during an animation, **P3** minor or only in art slated for
repainting.

| ID | Sev | Asset | Where it shows | Error |
|---|---|---|---|---|
| T1 | P1 | `assets/characters/rumi/rumi_eight_pose_runtime.png` | Mermaid Pool hide-and-seek (`ComfyHidden_rumi`), Day One wave | Neighbouring frames' braid and fins bleed into 4 of 8 cells |
| T2 | P1 | `assets/book/baby_eagle.png` | Playroom hide-and-seek, castle companion card, rescue scene | Book crop cut off at the left edge, with backpack and doll |
| T3 | P2 | `assets/flats/castle/dream_house/cloud_settee.png` | Movie Lounge | Seat cushions partly transparent; the red floor shows through |
| T4 | P2 | `assets/flats/castle/dream_house/dream_bed_1.png` | Sleepover Bedroom | Quilt partly transparent (17% of the silhouette) |
| T5 | P2 | `assets/flats/castle/interactions_v2/playroom_blocks_sheet.png` | Playroom blocks, when tapped | Tossed blocks sliced by cell edges in frames 3–5 |
| T6 | P2 | `assets/flats/castle/interactions_v2/opera_hall_footlights_sheet.png` | Opera Hall footlights, when tapped | Pieces of the neighbouring frame's bar at cell edges in 4 frames |
| T7 | P3 | `assets/flats/castle/interactions_v2/library_book_stack_sheet.png` | Library book stack, when tapped | Thin slivers at the left edge of 4 frames |
| T8 | P3 | `assets/flats/castle/interactions_v2/craft_room_idea_board_sheet.png` | Craft Room idea board, when tapped | Slivers at the left edge of 2 frames |
| T9 | P3 | `assets/flats/castle/interactions_v2/opera_hall_curtains_sheet.png` | Opera Hall curtains, when tapped | Sliver at the right edge of 1 frame |
| T10 | P3 | `assets/castle/day_one_pool/activities/floating_trash_atlas.png` | Day One pool trash | Candy-wrapper corner cut at its cell edge; one stray fragment |
| T11 | P3 | `assets/flats/castle/dream_house/` furniture (4 files) | Dining Room, Royal Bedroom | Bases cut flat by the card's bottom edge |
| T12 | P3 | `assets/characters/roshan_25d/` swim and gesture sheets | Roshan everywhere | 1,302 px of neighbouring-figure pixels inside the shipped sampling windows |
| T13 | P3 | `assets/sprites/dust_bunnies/boss/dust_bunny_boss_jump.png` | Grand Puff jump | Dust ring touches the left edge of frame 3 |
| T14 | check | `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_hop.png` | Day One playroom (bunnies pinning Baby Eagle) | Detached swoosh behind the bunny; confirm it is intended |

### T1 — Rumi: neighbouring frames bleed into her cells (P1)

In the pool, a piece of purple braid floats to Rumi's right. Her pose sheet is 4×2
cells of 256×384 px, and the braid and fins of neighbouring poses cross the cell
lines. Foreign pixels sit near the edges of four cells:
- column 2 row 0: 479 px, the braid tip from column 3. This cell is the one used
  by the pool hide-and-seek card and the wave.
- row 1, columns 0–2: 111, 870 and 367 px of neighbouring fins.

![Rumi in the pool with a floating braid fragment to her right](media/evidence/rumi_pool_ingame_zoom.jpg)

![Rumi's drawn cell: left as drawn, right with the detached fragment marked](media/evidence/rumi_pose_cell2_asset.png)

![Rumi's full pose sheet with cell lines; magenta marks foreign pixels near cell edges](media/sheets/rumi_eight_pose_runtime_marked.jpg)

**Fix for Codex:**
- Re-pack the sheet from the approved identity package
  (`assets_src/characters/rumi_2026-08-22/rumi_eight_pose_atlas.png`) with at least
  8 px of clear gutter around every pose, or clear each cell of pixels that belong
  to another pose.
- This moves existing pixels only. Rumi is on IP hold and must not be regenerated.
- Keep the runtime contract in `assets_src/characters/rumi_2026-08-22/PROVENANCE.json`
  in step, and add the cell sweep as a gate.

### T2 — Baby Eagle: the book crop is cut off (P1)

`assets/book/baby_eagle.png` is the whole book crop. The eagle leans over an open
pink backpack with a doll inside, and the art runs into the left edge: one
unbroken stretch of 285 px along the 512 px left edge is solid art. It shows as the playroom hide-and-seek card,
the castle companion card beside Roshan, and in the rescue scene.

![Baby Eagle hide-and-seek card in the playroom](media/evidence/baby_eagle_book_crop_ingame.jpg)

![The book crop, with the cut edges marked in red](media/evidence/baby_eagle_book_crop_asset.png)

**Fix:** use the backpack-free cutout the owner approved on 2026-09-24 (see
[README](README.md#owner-approved-work-queue)). The book file itself is protected
and stays unchanged.

### T3 — Cloud settee: see-through cushions (P2)

The teal seat cushions are drawn at about 69% opacity (mean alpha 175), so the red
lounge floor tints them. The art also touches the card's right edge.

![Cloud settee in the Movie Lounge](media/evidence/cloud_settee_ingame.jpg)

![Cloud settee: yellow marks partly transparent pixels inside the silhouette](media/evidence/cloud_settee_asset.png)

### T4 — Dream bed: see-through quilt (P2)

17% of the bed's silhouette is partly transparent (mean alpha 174), mostly the
quilt.

![Dream bed in the Sleepover Bedroom](media/evidence/dream_bed_ingame.jpg)

![Dream bed: yellow marks partly transparent pixels](media/evidence/dream_bed_asset.png)

**Fix for T3 and T4:** make the cushion and quilt pixels fully opaque. Both
belong to the flat-style rooms that the aesthetics plan recommends repainting, so
fix them there if the repaint comes first.

### T5–T10 — Interaction sheets: slivers and sliced pieces (P2–P3)

The tap animations use 4×2 sheets whose moving parts cross the cell lines, so
pieces are cut or show up in the next frame. In the marked sheets below:
- blue lines are cell borders;
- magenta marks detached pixels near a cell edge;
- red marks art cut by an edge.

Some magenta marks are intended (see the notes under each image).

![Playroom blocks sheet](media/sheets/playroom_blocks_sheet_marked.jpg)

T5: frames 3–5 slice tossed blocks at the cell edges. Frame 6's block in the air
is intended.

![Opera Hall footlights sheet](media/sheets/opera_hall_footlights_sheet_marked.jpg)

T6: frames 1, 2, 5 and 6 carry pieces of the next frame's footlight bar.

![Library book stack sheet](media/sheets/library_book_stack_sheet_marked.jpg)

T7: slivers at the left edge of frames 1, 2, 5 and 6.

![Craft Room idea board sheet](media/sheets/craft_room_idea_board_sheet_marked.jpg)

T8: slivers at the left edge of frames 1 and 5. The detached row of paint jars is
part of the design.

![Opera Hall curtains sheet](media/sheets/opera_hall_curtains_sheet_marked.jpg)

T9: a sliver at the right edge of frame 6.

![Day One floating trash atlas](media/sheets/floating_trash_atlas_marked.jpg)

T10: the candy wrapper touches its cell's right edge.

**Fix for Codex:** re-pack each sheet with clear gutters from its source frames
(the v2 sheets come from `tools/normalize_castle_interaction_v2_sheets.py`; the
pool trash atlas from its own source pack), then rerun the castle interaction
audits. No redrawing is needed.

### T11 — Flat-room furniture cut flat at the base (P3)

The feet of `bedside_table.png`, `dining_seat.png`, `provisions_hutch.png` and
`shell_wardrobe.png` meet the card's bottom edge as a straight cut.

![Bedside table](media/evidence/bedside_table_ingame.jpg)

![Shell wardrobe](media/evidence/shell_wardrobe_ingame.jpg)

![Provisions hutch](media/evidence/provisions_hutch_ingame.jpg)

![Dining seat](media/evidence/dining_seat_ingame.jpg)

These rooms are the ones recommended for repainting; fold the fix into that work.

### T12 — Roshan: ghost pixels from neighbouring figures (P3)

`tools/audit_roshan_sprite_clipping.py` reports that the shipped sampling windows
lose none of Roshan's art (0 px clipped) but still include 1,302 px of
neighbouring figures, down from 37,531 px on a naive grid. Clearing them needs a
re-pack like T1; keep the anchor tables (`scripts/roshan_sprite_anchors.gd`,
`scripts/roshan_sprite_frames.gd`) in step.

### T13 — Grand Puff jump frame 3 (P3)

![Grand Puff jump sheet](media/sheets/dust_bunny_boss_jump_marked.jpg)

The dust ring under frame 3 touches the cell's left edge. The other magenta marks
are Grand Puff's intended dust puffs.

### T14 — Dust bunny swoosh (check)

![Dust bunny pinning Baby Eagle](media/evidence/dust_bunny_hop_ingame.jpg)

![Dust bunny hop art: the detached swoosh is marked](media/evidence/dust_bunny_hop_asset.png)

A separate swoosh shape sits behind the bunny. It reads as a motion mark, but
confirm it is intended.

## Reviewed and not errors

- **Touch-halo gradients and Roshan's contact shadow:** translucent by design.
- **Pool skimmer net:** see-through by design.
- **Grime bubbles around sink and tub targets:** separate bubbles by design.
- **Daddy (library hide-and-seek), Roshan's frames, the chandelier ring and the
  ribbon rack:** the flagged "holes" are real gaps between body parts, correctly
  transparent.
- **Magic book floating over its shell, stacking-toy rings, paint-table brush:**
  intended animation poses.
- **Grand Puff's flinch, angry, laugh and implode puffs, motion lines and
  sparkles:** intended effects.
- **Dark rims on pans, tent, footlights and crests:** the art style's deep-indigo
  outline (`DL-VIS-02`).
- **Clogged waterfall lanes:** three strips meant to butt together.
- **Career portrait cards and crests:** small partial-alpha areas that do not
  read as errors on the card.
- **Foreground framing cards:** meet the stage edge by design.

## Recommended guard

Codex should turn [`tools/sweep_sheets.py`](tools/sweep_sheets.py) into a CI gate
(for example `tools/audit_castle_sprite_alpha.py`). It would:
- check every runtime sprite sheet's cells for foreign pixels near the edges and
  for art cut by an edge;
- allow a reviewed list of intended detached effects;
- fail when any new bleed appears.

The existing castle alpha audits check room cards and backgrounds but not
character sheets or interaction frames, which is why none of T1–T13 were caught.

## Limits

- Captures come from the Windows desktop display build, not the phone. VRAM
  compression on the phone may add alpha noise that this pass does not see.
- The Grand Puff arena and Day One's middle states (for example Rumi rising)
  were not captured live; their sheets were covered by the cell sweep only.
- Heuristic thresholds found candidates; every listed finding was confirmed by
  looking at the marked evidence.

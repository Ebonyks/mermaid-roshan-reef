# Codex handoff — imp state art after the clip system (2026-08-03)

> **STATUS ON MERGE (2026-08-03): this handoff's art order is OBSOLETE — do
> not action it.** It was written to cancel SET 1.4 / SET 5 on the grounds
> that transform clips made per-state sprites unnecessary. Those sprites were
> painted and landed on `dev` anyway (`codex/opera-full-art-regen-20260802`),
> and the roaming imps are now driven by the `imp_ai` brain through
> `_apply_imp_pose`, which resolves painted per-pose art per costume. So
> **SET 1.4 and SET 5 are NOT superseded** — treat
> `CODEX_OPERA_STAGE_COMPLETION_HANDOFF_2026-08-02.md` as standing in full.
> `fx_dizzy_stars.png` (the one asset this document commissioned) already
> exists and is wired up. What survives from the clip system is the
> `state_path` naming convention and the shoo-off pop clip; see the merge note
> at the top of `scripts/opera_imp_clips.gd`. The rest of this file is kept
> only as the record of why the order was briefly cancelled.

Branch: `claude/skins-sprite-animation-reuse-mh1j15`.
Supersedes the art scope of **SET 1.4** and **SET 5** in
`CODEX_OPERA_STAGE_COMPLETION_HANDOFF_2026-08-02.md`. Nothing else in that
document changes; SET 1.1-1.3, SET 2, SET 3, SET 4, and SET 1.5 stand as
written.

## What changed in code, and why the art order shrank

The Pearl Opera scuffle imps now animate through **transform clips over their
own texture** (`scripts/opera_imp_clips.gd`), not through per-state sprites:

- roaming **hop** — squash/stretch and a lean keyed to the route's existing
  bob phase, pivoted at the imp's feet;
- survived **hit** — a decaying recoil wobble (the old tween was silently
  overwritten by the per-frame depth pose and never showed);
- **bopped** — the sprite re-anchors to its centre, squashes, stretches,
  spins, tints and fades, with an optional shared dizzy overlay.

Consequence: a **costume costs exactly one PNG** (`rival_<costume>.png`, which
all twelve already have) and a **state costs one row in `CLIPS`** — never one
file per costume per state. The previously planned 60 files (12 costumes x
{bopped, bow, hop_a, hop_b, taunt}) plus 4 base-imp hops are **not required**
for the crews to animate.

The identity break is also fixed: a costumed imp no longer pops back to the
base purple imp when bopped. `scripts/probe_opera_2d.gd` now asserts this per
career ("keeps its costume through the shoo-off").

## REQUESTED — 1 new file (the only art this work depends on)

### A1 — `fx_dizzy_stars` (shared shoo-off overlay)

This is SET 1.3 of the 08-02 handoff, unchanged in spec and now the single
blocking art item. The runtime already loads it and degrades cleanly to the
clip alone when it is absent, so it can land at any time.

- **asset_id:** `fx_dizzy_stars`
- **Target path:** `assets/opera/worlds/props/fx_dizzy_stars.png`
- **Canvas:** 256x256 RGBA PNG, POT, fully transparent background.
- **Content:** three gold five-point stars spaced around a thin swirl ring;
  **transparent centre** — the engine draws it over the bopped imp's head and
  rotates the whole card a full turn, so nothing may occlude the face.
- **Constraints:** no text, labels, numbers, watermarks, or grid lines. No
  shell, pearl, marine, badge, crest, or target motifs (IMP-IDENTITY in
  `OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md` applies). Storybook
  palette consistent with the existing `fx_bop_puff` card. No baked drop
  shadow; the overlay is composited at 96x96 on screen so keep shapes bold
  and readable at that size.
- **Serves:** all fourteen characters and every costume — one file total, not
  one per costume.
- **License row:** add to `ASSET_LICENSES.md` in the same commit that adds the
  file.

## OPTIONAL — drop-in upgrades, in value order

The runtime prefers painted art wherever it exists and falls back to the clip,
so each of these lands with **no code change**. Deliver only if the owner
wants painted states; the game is complete without them.

### B1 — bopped states as ONE sheet per state, not one file per costume

If painted bopped art is wanted, generate it the way the costumes themselves
were made: `ASSET_LICENSES.md:601-608` records that the eleven costumed rivals
came from a **single** generation (`opera_rival_costume_sheet_master.png`,
eleven costume cells) sliced deterministically by
`tools/prepare_opera_2d_worlds.py`.

- Deliver **one 12-cell sheet** of the bopped pose, all twelve costumes in
  one generation, then slice to
  `assets/opera/worlds/actors/rival_<costume>_bopped.png` (512x512 each) with
  the existing tool.
- That is **1 generation instead of 12**, and cross-costume consistency is
  better because every cell comes from one pass instead of drifting across
  separate calls. Same precedent as the Roshan 4x4 keyframe atlases.
- Costume locks come from each costume's accepted idle. **No baked stars** —
  the engine supplies them from A1.
- The captain needs no separate art: he wears the same costume and is marked
  by a drawn gold ring (`opera_gesture_surface.gd:402`).

### B2 — hop / taunt / bow art is NOT requested

These are covered by clips. Painted hop frames would need a frame-cycling
driver that does not exist and would reintroduce the per-costume file
multiplication the clip system removed. Do not generate them unless the owner
explicitly asks for a frame-cycled walk, in which case it needs a code change
first, not art.

### B3 — Pre-existing defects worth fixing while in these files

Carried over from the 08-02 handoff, still true, independent of this work:

- `imp_captain_bow.png` — alpha hole through the shorts.
- `rival_detective.png` — ghosting/crop, needs full regeneration.
- `rival_boxer.png` — the only rival at 1024x1024; every other costume is
  512x512. Normalize to 512x512 standard framing.
- The ten remaining rival idles are hard-cropped at the last row (feet
  clipped); magician's matte is worst at 56% semi-alpha.

## Notes for whoever picks this up

- `scripts/opera_gesture_surface.gd`'s `_draw_imp()` path is **dead** —
  `set_bop_targets()` has no callers repo-wide since combat moved to the stage
  layer. Do not spend art or code effort there without reviving it first.
- Clip tuning lives in one place: `CLIPS` in `scripts/opera_imp_clips.gd`.
  Adjusting feel is a number change, not an art change.
- The probe gate is CI (`.github/workflows/probes.yml`); a red run must be
  treated exactly like a red local probe.

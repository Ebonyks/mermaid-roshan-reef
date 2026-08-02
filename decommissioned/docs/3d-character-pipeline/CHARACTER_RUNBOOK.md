# Runbook — building the new 3D Roshan (rig + sockets + rainbow hair) in one session

_Authored 2026-06-25. Turnkey sequence for a **Blender + Godot** session (neither
exists in the Claude Code web session, so this is executed elsewhere)._ 

This produces the strand-rigged Roshan that the cosmetic engine and the rainbow
hair physics are waiting on, then wires everything in. Each phase has a **gate** —
don't proceed until it passes.

Companion files: `tools/build_roshan_base.py`, `tools/build_roshan_rig.py`,
`tools/glb_check.py`, `scripts/cosmetics.gd`, `scripts/hair.gd`,
`assets/characters/hair_rainbow.gdshader`, and the design docs
`CHARACTER_PIPELINE.md` / `CHARACTER_CUSTOMIZATION.md`.

---

## Phase 0 — prerequisites
- [ ] Blender 4.x installed; repo checked out on branch
      `claude/replace-assets-free-sources-lnplz7`.
- [ ] Godot (matching `project.godot`) to verify + re-import at the end.
- [ ] The source art: `assets/characters/roshan_sprite.png` (+ the 2K bake
      `roshan_tex_2k.webp`).
- [ ] Decide the geometry route:
  - **A — AI-accelerated (faster):** generate a mesh from the sprite, then reuse our rig.
  - **B — pure manual sculpt (max control):** sculpt onto the existing rig directly.

---

## Phase 1 — get the base mesh

### Route A (AI-accelerated)
1. Generate a mesh from `roshan_sprite.png`:
   - **Tripo 3D** (clean quad topology) or **Hunyuan3D** (free, self-hostable).
   - Aim: full-body mermaid, T/A-pose-ish, mouth closed, hair as a separable mass.
2. Export **GLB**, save as `~/roshan_ai.glb`.
3. **Gate:** opens in Blender; roughly Roshan's proportions; hair is a distinct
   region you can select.

### Route B (manual)
1. `blender --background --python tools/build_roshan_rig.py -- --src assets/characters/roshan.glb --out ~/roshan_start.blend`
2. Open `~/roshan_start.blend`; the proven armature is imported and the old mesh is
   a hidden silhouette reference. Sculpt the new body. **Skip to Phase 3.**

---

## Phase 2 — rig + hair, automatically (Route A only)
One command reuses Roshan's proven 26-bone rig and does the heavy lifting:

```
blender --background --python tools/build_roshan_base.py -- \
    --rig assets/characters/roshan.glb \
    --mesh ~/roshan_ai.glb \
    --hair 12 --segs 3 --weights auto \
    --out ~/roshan_rigged.glb
```
This **automatically**: binds the new mesh to the rig (`--weights auto` =
Blender automatic weights, best for a fresh AI mesh), adds the 7 sockets + 12×3
hair-strand bones, and **generates the rainbow hair as geometry** (tapered ribbon
per strand, weighted to its chain, strand index baked to vertex-colour red). No
sculpting or weight-painting of hair.

- **Gate:** `python3 tools/glb_check.py ~/roshan_rigged.glb` →
  `26 ROSHAN bones present`, sockets listed, **hair strands ≥ 10**.

---

## Phase 3 — review & touch-up (mostly automated now)
Phase 2 already bound the body and generated the hair. What's left is **review,
not authoring** — and most of it is *your taste call*, not artist skill:
1. **Likeness (your call):** does it read as Roshan? If not, **regenerate** in
   Phase 1 (try another seed / a clearer sprite crop) — iterate the AI, don't sculpt.
   Auto-retopo if the mesh is dense: **QuadRemesher** (paid) or free **Instant Meshes**.
2. **Weight check (usually fine):** test-pose `tail1..tail8`, `finTop/finBot`. Auto
   weights are typically good on a stylized body; only touch up if the tail/fin
   *pinches*. This is the one spot that might want a few minutes of weight-paint —
   or a one-off favour from anyone who knows Blender.
3. **Hair tuning (optional):** the strands are generated; tweak `--hair N` (10–15) or
   the ribbon `width` in `generate_hair_cards` and re-run if you want more/fuller hair.
4. **Sockets:** nothing to do — cosmetics attach later; drop part meshes into
   `assets/characters/cosmetics/parts/` when you make them.

- **Gate:** posing a tail/hair bone deforms cleanly; hair ribbons exist with a
  rainbow (vertex-colour R varies across strands — `glb_check` confirms strand count).

> What no tool replaces is the **"does this look like her" judgment** — but that's
> looking and approving, which you can do. Sculpting/weighting/hair are handled.

---

## Phase 4 — export
File → Export → glTF 2.0 (.glb):
- Format **glTF Binary (.glb)**, **+Y Up**, Selected Objects (armature + mesh).
- Mesh: UVs, Normals, Tangents, **Vertex Colors ON** (carries the strand index),
  **Skinning ON**, **Animation OFF** (swim + hair are procedural).
- Save over `assets/characters/roshan.glb`.
- Delete `assets/characters/roshan.glb.import` so Godot re-imports.

- **Gate:** `python3 tools/glb_check.py assets/characters/roshan.glb` →
  26 bones + sockets + **strands ≥ 10**.

---

## Phase 5 — wire it in (Godot)
Open the project in Godot (re-imports `roshan.glb`). Then:

1. **Cosmetics** — in `main.gd`, replace the skin call (`main.gd:1645`,
   `player.set_skin(skin_id, String(s["sprite"]))`) with:
   ```gdscript
   if cosmetics == null:
       cosmetics = CosmeticManager.new(); add_child(cosmetics); cosmetics.setup(player)
   cosmetics.apply_loadout(skin_id)   # "classic" = no-op
   ```
   and point the wardrobe UI at `cosmetics.list_loadouts()` instead of `SKINS`.
2. **Hair physics** — in `player.gd` `_ready()` (after the model loads):
   ```gdscript
   var hs := HairSim.new(); add_child(hs); hs.setup(self)
   ```
   and **remove the old single-chain hair sway** in the swim (`player.gd` lines that
   `_rot_bone("hair1"/"hair2"/"hair3", ...)` — HairSim now owns the hair).
3. **Rainbow shader** — assign `assets/characters/hair_rainbow.gdshader` to the hair
   surface (or have `CosmeticManager` apply it via a `material` cosmetic), and set its
   `caustic` param to `res://assets/terrain/caustics.png`.

---

## Phase 6 — verify in-engine (checklist)
- [ ] Roshan loads at the right size/orientation (chase cam frames her; ×1.55 / y −1.6 still fit).
- [ ] **Swim animation** still plays (tail wave, fins, head bob) — rig contract held.
- [ ] **Hair:** 10–15 streaks sway **independently**, trail when she accelerates, and
      run a full **rainbow** that slowly cycles.
- [ ] **Cosmetics:** `apply_loadout("rainbow_princess")` adds the crown/recolour;
      `apply_loadout("fairy")` adds wings + ear morph + sparkle tail; `"classic"`
      reverts cleanly.
- [ ] No console errors from `CosmeticManager` / `HairSim` (warnings for not-yet-authored
      parts are expected and harmless).

---

## Phase 7 — commit / rollback
- **Commit:** `assets/characters/roshan.glb` (+ deleted `.import`), the `main.gd` /
  `player.gd` wire-in, any new `cosmetics/parts/*.glb`. Push to the branch.
- **Rollback:** `git checkout assets/characters/roshan.glb assets/characters/roshan.glb.import`
  and revert the two wire-in edits — the old model + billboard skins return; the
  scaffold goes back to no-op.

---

## At a glance
```
sprite ──Tripo/Hunyuan3D──▶ ai_mesh.glb
        build_roshan_base.py (weights + sockets + 12 hair strands)
        ──▶ Blender: likeness + weights + hair-strand split + vtx-colour index
        ──▶ export roshan.glb  ──glb_check──▶  Godot re-import
        ──▶ wire: CosmeticManager + HairSim + rainbow shader
        ──▶ verify: swim ok, hair independent+rainbow, loadouts apply
```

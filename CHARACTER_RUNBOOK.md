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

## Phase 2 — transfer the rig (Route A only)
Reuse Roshan's proven 26-bone rig + procedural swim; add sockets + hair bones:

```
blender --background --python tools/build_roshan_base.py -- \
    --rig assets/characters/roshan.glb \
    --mesh ~/roshan_ai.glb \
    --hair 12 --segs 3 \
    --out ~/roshan_rigged.blend.glb
```
This transfers skin weights old→new, keeps the armature, and adds the 7 sockets +
12×3 hair-strand bones. Open the result in Blender to continue.

- **Gate:** `python3 tools/glb_check.py ~/roshan_rigged.blend.glb` →
  `26 ROSHAN bones present`, socket bones listed, **hair strands ≥ 10**.

---

## Phase 3 — the manual art (the part no tool does)
In Blender, on the rigged mesh:
1. **Likeness + cleanup:** match the sprite — face, rainbow hair, proportions; retopo
   if the AI mesh is dense. Keep overall size (player.gd scales ×1.55, offsets y −1.6).
2. **Weight touch-ups:** test-pose `tail1..tail8`, `finTop/finBot`, arms; fix the
   tail/face transfer artifacts. The swim is the truth test.
3. **Hair → strands (the rainbow contract):**
   - Split the hair mass into **10–15 strands**; weight each strand to its
     `hair_<SS>_<J>` chain (strand SS, segment J).
   - Bake each strand's **index into vertex-colour RED** = `SS / (N-1)` (0..1). This
     is what `hair_rainbow.gdshader` reads to spread the rainbow.
   - Assign the hair surface a material (the rainbow shader is applied engine-side;
     just give hair its own material slot so it's selectable).
4. **Sockets (optional now):** leave the 7 socket bones as-is; cosmetics attach to
   them later. Add cosmetic part meshes to `assets/characters/cosmetics/parts/` when ready.

- **Gate:** posing any tail/hair bone deforms the mesh cleanly; hair strands move
  independently when posed; vertex-colour R varies 0→1 across strands.

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

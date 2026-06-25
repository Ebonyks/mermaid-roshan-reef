# Character 3D Pipeline — Roshan + NPC conversion

_Authored 2026-06-25 on branch `claude/replace-assets-free-sources-lnplz7`._

This is the production spec + scaffolding for (1) re-sculpting **Roshan** to a
higher-quality look and (2) converting **all NPC friends** from 2D billboards to
rigged 3D models. The actual sculpting/texturing is **artist work in Blender**;
this repo provides the rigs, contracts, validators, and the engine integration
so the art drops in cleanly.

## 0. Reality check (read first)

- **Roshan is already a real 3D, rigged, animated character.** `roshan.glb` is a
  15,540-tri mesh on a 26-bone skeleton, animated by a bespoke **procedural swim**
  in `scripts/player.gd` (no baked clip). She is *not* a sprite. The "stuffed
  animal" impression is a **sculpt + shading** problem, so the fix is a new body
  on the **same rig** — not a new dimensionality.
- **NPC friends are 2D billboard `.png` sprites** (`_build_friends`, `main.gd:1208`).
  Converting them to 3D is genuine multi-character art work.
- **No Blender exists in the Claude Code web session**, and high-quality character
  sculpt/UV/weight-paint is an artist task, not a headless-scriptable one. So the
  deliverable here is the **correct rig + contract + integration**, executed in a
  Blender-equipped session/by an artist. The `tools/*.py` scripts detect the
  missing Blender and print their instructions instead of failing.
- **No Godot binary here either**, so swaps can't be verified in-engine from this
  session — scale/orientation must be eyeballed by whoever opens the project.

---

## 1. Roshan — re-sculpt on the existing rig

**Goal:** kill the plush/flat read; keep her unmistakably the same character and
keep `player.gd` working with **zero code changes**.

**The rig is the contract.** `player.gd` drives bones *by name*:

| bones | motion | axis |
|---|---|---|
| `tail1..tail8` | sine wave travelling down the tail | `Vector3.RIGHT` |
| `finTop`,`finBot` | flutter | `Vector3.RIGHT` |
| `chest`,`neck` | counter-sway | `Vector3.RIGHT` |
| `head` | bob + idle | `Vector3.BACK` |
| `hair1`,`hair2`,`hair3` | trailing sway | `Vector3.BACK` |

(`hairL1/hairL2`, `armU/armF/hand`, `armU2/armF2/hand2` exist in the rig and must
be preserved, but the swim leaves them at rest.) If a replacement mesh drops any
of these 26 names, `player.gd` warns once and that part goes stiff.

**Art direction (de-plush):**
- Tighten the silhouette — defined waist/tail taper, real facial planes instead of
  rounded blobs; reduce the uniform soft-bevel everywhere.
- PBR-ish skin: subsurface tint, a specular/【wet】highlight, fresnel rim so she
  catches the underwater key light; scaled tail with an actual normal map (the
  repo already ships `assets/terrain/scales_normal.png`).
- Re-author/upscale the texture — `roshan_tex_2k.webp` already exists and
  `player.gd` has an `_upgrade_texture()` hook that swaps the albedo at load.
- Keep overall proportions: `player.gd` scales the model **×1.55** and offsets
  **y −1.6**; a wildly different height/origin will mis-frame the chase camera.

**Workflow:**
1. `blender --background --python tools/build_roshan_rig.py -- --src assets/characters/roshan.glb --out /tmp/roshan_start.blend`
   → imports the proven armature, keeps the old mesh as a hidden silhouette ref.
2. Sculpt/replace the body; weight to the armature; **keep all 26 bone names**.
3. Export per the **EXPORT CONTRACT** the script prints (glTF Binary, +Y up,
   Skinning ON, **Animation OFF** — the swim is procedural).
4. Overwrite `assets/characters/roshan.glb`, delete `roshan.glb.import`, reopen in
   Godot to re-import.
5. Validate: `python3 tools/glb_check.py assets/characters/roshan.glb` → must
   report **26 joints** and "all 26 ROSHAN bones present."

No `player.gd` / `main.gd` edits required if the rig contract holds.

---

## 2. NPCs — billboard → rigged 3D (full cast)

Current cast (sprite file → character). All live in `assets/characters/friends/`
except skins/story art as noted:

| sprite `tex` | character(s) | source |
|---|---|---|
| `pearl_friend` | Evie **and Lamb-a'** (lamb mesh already exists: `lamb.glb`) | `FRIEND_DEFS` |
| `two_friends` | Harper & Fiona (sisters) | `FRIEND_DEFS` |
| `mama_baby` | Faron (+ dolls) | `FRIEND_DEFS` |
| `gabby` | Gabby | `FRIEND_DEFS` |
| `wacky_chuck` | Wacky & Chuck | `FRIEND_DEFS` |
| `huluu` | Princess Huluu | story (`main.gd:325`) |
| `daddy`, `kareem`, `flower_friend` | supporting art | `friends/` |
| `fairy_mermaid` (skin) | Roshan alt-skin | `characters/skins/` |

**Approach:** one **shared 18-bone humanoid rig** (`tools/build_npc_rig.py`) for
every land character, plus a single looping **`idle`** clip authored once on that
rig and reused. Pairs (Wacky & Chuck, Harper & Fiona, Evie & Lamb-a') can be a
single mesh containing both figures, or two meshes — loader handles either.

Bone-name contract (keep identical across all NPCs):
`root, hips, spine, chest, neck, head, armUL/armFL/handL, armUR/armFR/handR,
legUL/legLL/footL, legUR/legLR/footR`.

**Per-character workflow:** build the shared rig once → sculpt each character onto
it → bind → author/reuse the `idle` → export `friends/<tex>.glb` (`+Y` up,
Skinning ON, Animation ON = the idle) → `python3 tools/glb_check.py friends/<tex>.glb`.

> Scope note: this is the largest line item — ~12 human sculpts + rigs + one idle.
> It is multi-session art work, not finishable in a single coding session. The
> rig/contract/integration below make it **incremental**: each `.glb` that lands
> upgrades that character while the rest stay as sprites, no breakage.

---

## 3. Lamb-a'

`lamb.glb` already exists (11k tris, **0 anims**, static). For the Evie & Lamb-a'
encounter, give it a tiny idle (ear/tail wiggle) — either a 3-bone rig via the
same export contract or a procedural wiggle hook in `main.gd` analogous to the
fish. Low priority; it already renders in 3D.

---

## 4. Engine integration — model-aware, sprite-fallback (incremental & safe)

So conversion can land one character at a time without breaking anything, make the
friend renderer **prefer a `.glb` if present, else use today's billboard**. This
is purely additive — with no `.glb` files it behaves exactly as now.

Replace the sprite creation in `_build_friends` (`main.gd:1208-1213`) with:

```gdscript
var tex_name := String(fd["tex"])
var glb_path := "res://assets/characters/friends/%s.glb" % tex_name
var visual: Node3D
if ResourceLoader.exists(glb_path):
    var ps: PackedScene = load(glb_path)
    var m: Node3D = ps.instantiate()
    m.scale = Vector3.ONE * 4.0          # tune vs the old 0.016 px billboard
    m.position = Vector3(x, seabed_y(x, z) + 4.0, z)
    add_child(m)
    var ap := _find_anim_in(m)           # reuse player.gd's _find_anim pattern
    if ap and ap.get_animation_list().size() > 0:
        var clip: String = ap.get_animation_list()[0]   # 'idle'
        ap.get_animation(clip).loop_mode = Animation.LOOP_LINEAR
        ap.play(clip)
    visual = m
else:
    var spr := Sprite3D.new()            # unchanged fallback (today's behaviour)
    spr.texture = load("res://assets/characters/friends/%s.png" % tex_name)
    spr.billboard = BaseMaterial3D.BILLBOARD_ENABLED
    spr.pixel_size = 0.016
    spr.position = Vector3(x, seabed_y(x, z) + 6.5, z)
    add_child(spr)
    visual = spr
# beacon / light pillar / sparkles below stay the same, anchored to `visual.position`
```

Apply the same pattern to:
- **Roshan alt-skins** (`player.gd`, the billboard `skin_sprite` path) — prefer
  `skins/<id>.glb` if present, else the billboard.
- **Story art** lookups in `main.gd` (e.g. `huluu`) for the dialogue/book pop-ins
  if those should become rendered 3D portraits rather than flat art.

This patch is **not yet applied** — it touches the live character path and can't be
verified here without Godot. It's ready to drop in when you want it (ideally in a
session that can open the editor to tune the `scale`/`position` constants).

---

## 5. Suggested order of work

1. **Roshan re-sculpt** (§1) — highest visual payoff, zero engine risk (rig contract).
2. **Integration patch** (§4) — small, safe, unlocks incremental NPC drop-in.
3. **NPC cast** (§2) — start with the most-seen characters (Gabby, Wacky & Chuck,
   Huluu), then the rest; each `.glb` upgrades one character independently.
4. **Lamb-a' idle** (§3) — quick polish.

## 6. Tools index

| tool | run | purpose |
|---|---|---|
| `tools/build_roshan_rig.py` | `blender --background --python … -- --src assets/characters/roshan.glb` | import Roshan's exact rig as a sculpt start |
| `tools/build_npc_rig.py` | `blender --background --python … -- --out /tmp/npc_rig.blend` | the shared 18-bone NPC humanoid rig |
| `tools/glb_check.py` | `python3 tools/glb_check.py <file.glb>` | validate joints/anims/tris + required bone names |

All bone tables in the scripts are the **contract**; `glb_check.py` enforces them.

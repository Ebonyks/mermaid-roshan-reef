# Evaluation — 3D Roshan variants + a flexible cosmetic/customization system

_Authored 2026-06-25 on branch `claude/replace-assets-free-sources-lnplz7`._

You asked for: (1) Roshan's **variants** (fairy version, wardrobe skins) in 3D, not
2D billboards; (2) a **flexible model** so cosmetics can be adjusted / customized;
and (3) an evaluation of a "custom Blender engine" to turn the Roshan **sprite**
into the 3D character. This is the options evaluation + a recommendation.

## 0. Current state (ground truth)

- **One** 3D model — `roshan.glb` ("classic"), 26-bone rig, animated by the
  **procedural swim** in `player.gd` (bone-name-keyed, no baked clips).
- **Every variant is a 2D billboard.** `SKINS` only contains "classic"; `set_skin`
  hides the 3D model and shows a `Sprite3D` for any other skin. The **Fairy
  Mermaid** (`skins/fairy_mermaid.png`) is a billboard used inside the Fairy Pond.
- The rig **already supports attachments**: `player.gd:attach_bone(node, bone)`.
  That is the seed of a modular cosmetic system — it exists, it's just unused.
- A 2K texture re-bake from the source illustration already exists
  (`roshan_tex_2k.webp`, applied via `_upgrade_texture`).

## 1. The constraint that rules out the obvious answer

Two facts make "just AI-generate a rigged 3D Roshan per variant" the *wrong* plan:

1. **She's a mermaid.** Auto-riggers (Meshy, Tripo, etc.) assume a **biped** with
   legs. A tail breaks them, or gets mis-rigged.
2. **The animation is bespoke.** `player.gd` drives **named** bones
   (`tail1..tail8`, `finTop/finBot`, `hair1..3`, …). Any model with a *different*
   skeleton — which every AI auto-rig produces — **will not animate** in this game
   without being re-skinned to the existing 26-bone contract.

So the AI tools' headline feature (instant auto-rig + 500 preset animations) is
**moot here** — we already have the rig and the animator, and they're mermaid-
specific. The model must conform to *our* rig, not bring its own.

**Corollary:** do **not** build N separate full models (one per variant). That's
N× the rig/skin/maintenance, and it's exactly today's billboard problem in 3D.
Build **one shared rigged base + modular cosmetics.**

## 2. Two problems people conflate

- **(A) Producing geometry** — the one-time art of getting 3D shapes from the
  sprite. (The sprite→3D question.)
- **(B) The customization engine** — composing/swapping cosmetics at runtime so a
  kid can dress Roshan up. (The durable system.)

Your "custom Blender engine" is really **B**, plus tooling that *feeds* A. They're
evaluated separately below.

## 3. Option evaluation — (A) producing the geometry

| Approach | Charm/likeness | Fits the mermaid rig? | Modular-ready? | Effort | Cost | Verdict |
|---|---|---|---|---|---|---|
| **Manual Blender sculpt** (sprite as ref, onto existing rig) | ★★★ | ✓ native (skin to the 26 bones) | ✓ author parts separately | high | $0 | **Primary** |
| **AI image→3D** (Meshy / Tripo / Rodin / Hunyuan3D) | ★–★★ (stylized chars inconsistent) | ✗ brings its own biped rig → must re-rig | ✗ single fused mesh | low | $/cloud | **Blockout only** |
| **Hybrid** (AI blockout → retopo → re-skin to our rig → split into parts) | ★★ | ✓ after re-skin | ✓ after splitting | med | $/low | **Accelerator** |
| **Parametric base** (VRoid/MakeHuman/Auto-Rig Pro) | ★★ torso/face, ✗ tail | ✗ biped auto-rig → conform manually | ~ | med | $0 | torso/face start only |

Notes from current (2026) tooling: **Meshy** is the only one that auto-rigs +
animates natively, but humanoid-only; **Tripo** gives clean quad topology fast but
no native rig; **Rodin/Hunyuan3D** are highest fidelity but rig separately
(**Hunyuan3D is free + self-hostable** — relevant to §6). None of them rig a tail
to our named bones, so for *this* character they're at best a geometry head-start.

**Recommendation (A):** sculpt/retopo in Blender **onto the existing 26-bone rig**.
Use AI only as an optional **self-hosted blockout** to get a rough body fast — never
as the rig and never as the finished asset.

## 4. Option evaluation — (B) the customization engine

Three mechanisms; the system should combine all three (they're complementary):

| Mechanism | Best for | How | Cost |
|---|---|---|---|
| **Bone-socket attachments** | crowns, wings, fins, accessories | `attach_bone(mesh, socket)` — already exists; add socket bones (see §5) | cheap |
| **Material / texture variants** | hair colour, tail pattern, the "sparkly" look, skin tints | swap albedo / shader params on the base mesh | **cheapest, huge variety** |
| **Blendshapes (morph targets)** | face/tail shape, fairy ears, fin spread | export morphs on the mesh; drive 0–1 in code | med |

Make it **data-driven and composable** (not mutually exclusive like today's skins):

```
Cosmetic = { id, type: socket|material|morph, target, asset, unlock, layer }
Loadout  = [cosmetic_id, ...]          # e.g. "fairy" = wings + ears morph + sparkle mat + tail tex
```

The **Fairy variant becomes a loadout**, not a separate model: wings attachment +
ear/fin morph + sparkle material on the **same** base. That is precisely "flexible,
adjustable cosmetics." `set_skin(id)` evolves into `apply_loadout([...])`.

## 5. What the "custom Blender engine" should actually be

Reframe it as a **modular assembler**, not an ML sprite→3D pipeline:

- **`tools/build_roshan_cosmetics.py` (bpy):** load the base rig from `roshan.glb`,
  load a **parts library** (`parts/*.glb`: hairstyles, crowns, wings, tail skins),
  compose named variants per a JSON manifest, **validate the 26-bone contract**
  (reuse `tools/glb_check.py`), export either per-part GLBs or one packed GLB with
  toggleable parts.
- **Godot side:** a `CosmeticSet` catalog + loader that instantiates parts, attaches
  them to sockets (`attach_bone`), and applies materials/morphs from the data table;
  the wardrobe UI drives it.
- **Extend the rig contract** with cosmetic **socket bones** so sculpts include them:
  `headTop` (crowns/bows), `backL`/`backR` (wings), `earL`/`earR` (fairy ears),
  `tailTip` (fin variants), `handHold` (props). These are additive to the existing
  26 — keep all the originals.

AI image→3D can *feed the parts library* (generate candidate wing/crown shapes from
concept art) but it is an **input**, not the engine.

## 6. Privacy — considered and dismissed by the owner

Raised and **closed (2026-06-25):** the owner considers Roshan a **stylized avatar
/ character IP, not a likeness of the actual child**, so uploading the sprite to a
cloud 3D generator is acceptable. Cloud tools (Meshy, Tripo, Rodin) are therefore
on the table as a **geometry source**. This does **not** change the verdict in §3:
AI stays a **blockout accelerator**, for the *rig* reason (mermaid tail + the named
26-bone procedural animator), not for privacy. Self-hosted Hunyuan3D remains a fine
free option, now by preference rather than necessity.

## 7. Recommendation

1. **Keep ONE rigged base Roshan**, improved per `CHARACTER_PIPELINE.md §1`.
2. **Variants = modular cosmetics** (sockets + materials + morphs), data-driven and
   composable. Fairy = a loadout, not a model. Retire the billboard-skin swap.
3. **Author geometry in Blender** onto the existing rig (+ new socket bones); AI
   (cloud or self-hosted — privacy is not a constraint, see §6) only as an optional
   **blockout** accelerator — never the rig, never the "engine."
4. **Build the modular assembler + Godot cosmetic catalog** — that's the real
   "custom engine," and it's fully scaffold-able from here (schema, assembler
   skeleton, loader design, socket-bone spec) without Blender/Godot present.

**Effort tiers (each shippable on its own):**
- **T0 — visible customization, zero new sculpt:** material/texture variants on the
  *existing* model (hair/tail recolours, a sparkle shader). Wardrobe gets real
  choices immediately.
- **T1 — attachment cosmetics:** crowns/bows/wings on socket bones.
- **T2 — Fairy loadout + morphs:** the full fairy variant as composed cosmetics.
- **T3 — assembler tooling** to scale the parts library.

> All artifacts above are specs/scaffolding — the sculpting itself is Blender artist
> work (no Blender in this session), and runtime changes need a Godot open to verify.

## 8. Scaffold delivered (2026-06-25)

The cosmetic "engine" backbone is in the repo — **data-driven, fully guarded, and
NOT yet wired into the live game** (zero behaviour change until you opt in). It
degrades to a no-op whenever an asset / socket bone / morph / surface is absent, so
it is safe to merge before any cosmetic art exists.

| File | Role |
|---|---|
| `assets/characters/cosmetics/catalog.json` | the data: cosmetics (socket/material/morph), layers, loadouts. **Fairy = a loadout** here, not a model. |
| `scripts/cosmetics.gd` (`CosmeticManager`) | runtime: `apply_loadout(id)` composes cosmetics on the shared rig; re-applying reverts the previous one cleanly. |
| `tools/build_roshan_cosmetics.py` | Blender assembler: validates socket bones, checks parts, can pre-bake a loadout preview GLB. Reads the same catalog. |
| `assets/characters/cosmetics/parts/` | the part-GLB library (empty; `README.md` documents the contract). |
| `tools/glb_check.py` | now also reports cosmetic **socket bones** on Roshan. |

**Socket bones** (additive to the core 26 — add when re-rigging, keep all originals):
`headTop, backL, backR, earL, earR, tailTip, handHold`.

**Wire-in (one place, when you're ready — needs a Godot open to verify):**
replace the `player.set_skin(...)` call (`main.gd:1645`) with:
```gdscript
if cosmetics == null:
    cosmetics = CosmeticManager.new(); add_child(cosmetics); cosmetics.setup(player)
cosmetics.apply_loadout(skin_id)   # "classic" = clean no-op
```
and have the wardrobe UI list `cosmetics.list_loadouts()` instead of `SKINS`. The
old billboard `set_skin` can stay as a fallback until the 3D cosmetics are authored.

**Build order from here:** author the base improvements + socket bones (Blender) →
drop part GLBs into `parts/` → the catalog/loadouts light up with no further code.

## 9. Automating "author the base" — engine evaluation

Goal: automate step 1 (base mesh + rig + sockets). Honest split — **geometry
automates well; rigging does not, for this character.**

| Tool | Automates | Verdict for Roshan |
|---|---|---|
| **Tripo 3D** | sprite → mesh, clean quad topology, fast | ✅ **geometry source** |
| **Hunyuan3D** | sprite → mesh, free + **self-hostable** | ✅ geometry source (offline) |
| **Meshy / Rodin** | sprite → mesh (+ Meshy auto-rig) | ✅ mesh; ❌ its auto-rig (humanoid) |
| **Meshy / Tripo / AccuRig auto-rig** | one-click humanoid skeleton + retarget | ❌ humanoid-only, **wrong skeleton + bone names** |
| **Auto-Rig Pro (Blender)** | modular rig **with tail chains**, creatures | ⚠️ only real creature auto-rig, still its own skeleton |
| **Unreal MetaHuman creatures** | humanoid + hand-animated tail | ❌ overkill for a Godot kids' game |

**Why one-click fails here:** web auto-riggers assume a **biped with a standard,
canonically-named skeleton** (that's what makes retarget work). Roshan has a
**tail** and an animator that drives bones **by exact name** (`tail1..tail8`, …).
AI rigs bring their own skeleton → won't animate without re-rigging.

**The automatable path = reuse the rig, don't regenerate it.** AI makes the mesh;
`tools/build_roshan_base.py` then **transfers the existing rig's skin weights** onto
it (Blender Data-Transfer), keeps the proven 26-bone armature + procedural swim, and
auto-adds the **socket** and **hair-strand** bones. Manual work shrinks to
fidelity/likeness cleanup + tail/face weight touch-ups.

Pipeline: **Tripo/Hunyuan3D (mesh) → `build_roshan_base.py` (weights + sockets +
hair) → `glb_check.py` (validate)**.

## 10. Rainbow physics hair (10-15+ independent streaks)

Implemented as a rig + runtime + shader combo, scaffolded and guarded (no-op until
the strand-rigged model exists):

- **Rig:** `build_roshan_base.py` fans **12 strands × 3 segments** (configurable
  10-15+ via `--hair`) off the `head` bone, named `hair_<SS>_<J>`. The hair geometry
  is weighted to these chains, with each strand's index baked into **vertex-colour
  red** (0..1).
- **Physics — `scripts/hair.gd` (`HairSim`):** a per-segment **damped spring** drives
  each strand independently — own phase + stiffness jitter, plus a velocity **trail**
  so the whole mane lags when she accelerates. Same primitive as the procedural swim
  (`set_bone_pose_rotation` vs rest), so no engine-node dependency. (Godot's built-in
  `SpringBoneSimulator3D` is the alternative; the custom solver is used for
  deterministic, tunable behaviour.)
- **Colour — `assets/characters/hair_rainbow.gdshader`:** maps each strand's
  vertex-colour index to a hue (full rainbow across the fan) and slowly cycles it via
  `TIME`; adds a caustic shimmer + rim so the hair sits in the reef light. Motion and
  colour are deliberately decoupled (physics = `hair.gd`, colour = shader).

**Wire-in (after the strand-rigged model lands):** `var hs := HairSim.new();
player.add_child(hs); hs.setup(player)` and drop the `hair1/2/3` lines from
`player.gd`'s swim. `glb_check.py` reports the strand count (targets 10-15+).

## Sources
- Meshy — image-to-3D + auto-rig: https://www.meshy.ai/blog/best-ai-tools-for-3d-game-assets
- Tripo (fast, quad topo, no native rig): https://www.tripo3d.ai/content/en/guide/the-best-character-creator-auto-rig-tools
- AI 3D character/avatar comparison 2026: https://www.3daistudio.com/blog/best-ai-3d-character-and-avatar-generators-2026
- TRELLIS vs Meshy vs Tripo vs Hitem3D (Hunyuan3D self-hosted): https://trellis2.app/blog/best-ai-3d-model-generator

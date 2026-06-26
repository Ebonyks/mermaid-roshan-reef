# Art direction — Wind Waker cel-shaded look (game-wide)

_Authored 2026-06-26. Decision + plan._

## Decision

The game adopts a **Zelda: Wind Waker** cel-shaded aesthetic: flat toon colour bands
+ bold ink outlines, on stylised geometry. This was chosen because it **resolves the
2D/3D fusion** (it pulls the 3D into the same illustrated register as the painted
sprites instead of fighting them) and because **cel-shading flatters simple geometry**
— so Roshan's flat-relief body and a light rig read as *intentional and charming*
rather than toy-like. Verified by rendering the existing model toon-shaded with an
outline (see the previews): even unchanged geometry looks deliberately stylised.

Reference for animation: **Link** — expressive, snappy skeletal cycles with squash/
stretch, anticipation, and secondary motion (hair, cloth). Roshan's current rig +
single-sine procedural swim is thin by comparison; richer animation is the second
phase and is coupled to a better (volumetric) body — see “Sequencing”.

## The two shaders (in `assets/shaders/`, inert until applied)

- **`cel.gdshader`** — toon surface: posterised N·L into hard bands + soft Fresnel
  rim, keeps each mesh's own albedo. Godot built-in `diffuse_toon`/`specular_toon`
  render modes + a custom `light()` for crisp banding. Mobile-renderer safe.
- **`outline.gdshader`** — inverted-hull ink line: `cull_front`, grow along normal,
  flat colour. Attach as a material **`next_pass`**. The standard reliable per-object
  outline in Godot 4.

## How it gets applied (and why it's not wired in yet)

Cel-shading is a **game-wide rendering change**, and I can't run Godot in this
environment to verify it — and unverified live render changes already broke the game
twice. So the shader files are committed but **not applied**; applying them is a
deliberate, testable step. Two safe ways to do it:

1. **Per-material `next_pass` + override (recommended, incremental):** a small helper
   walks the scene, sets `material_override` to a `ShaderMaterial` using `cel.gdshader`,
   and assigns `next_pass` = `outline.gdshader`. Gate it behind a single bool
   (`CEL := true`) so it's one-line revertible and can be toggled per mesh group
   (characters first, then reef, terrain, fish).
2. **Screen-space outline (alternative):** a full-screen post-process edge detect on
   depth+normals via a `CanvasLayer`. One global effect, no per-mesh work, but heavier
   to tune; the inverted-hull route is simpler and Mobile-friendly.

The 2D **sprites** (friends, NPCs) already fit a cel world — they're flat illustrations.
Give them a matching thin outline + slight posterise to sit in the same ink language.

## Sequencing

1. **Cel shading first** — biggest visual transformation, independent of the model.
   Apply to Roshan + reef + fish + terrain, behind a toggle, tested in Godot.
2. **Volumetric body** — generate the real 3D body from the sprite (Tripo/Hunyuan3D)
   so she's not a flat relief; cel-shading makes even a rough body look good, so this
   is now lower-risk.
3. **Link-style animation** — author proper swim/idle/turn cycles + secondary motion on
   the better rig (the current single-sine swim is the “thin” part to replace).

## Verifying the look without Godot

`tools/preview_render.py` renders any `.glb` cel-shaded (toon + inverted-hull outline)
via Blender headless on CPU — that's how the previews were made. Use it to preview the
model/cosmetics/animations before they ever touch the game:
```
blender --background --python tools/preview_render.py -- <model.glb> <out.png> <azimuth_deg>
```

> Status: shaders + preview tooling committed (inert). Applying cel-shading game-wide
> is the next step and should be done where it can be tested in Godot (or via a
> one-line toggle for you to test), not blind.

# Lighting & Shader Audit — 2026-07-18

Scope: everything that lights, shades, or post-processes a pixel in Mermaid
Roshan: Reef of Light, plus an inventory of what Godot 4.4 offers that we are
NOT using, several proposed major look shifts with performance analysis, and
ranked recommendations. A working proof-of-concept for most techniques ships
with this audit as the **Lighting Lab** inside developer mode (see §4).

Hard constraint framing every line below: the renderer is **Mobile on every
platform** (owner decision 2026-07-11) and the target device is a 3–4-year-old
Android phone at 1280×720 (×0.8 render scale on Speedy). "Available in Godot"
therefore always means "available under the Mobile rendering method".

---

## 1. What the game uses today (current state)

### 1.1 Environment (one `WorldEnvironment`, env swapped per scene)

| Feature | Setting | Notes |
|---|---|---|
| Background | `BG_SKY` + `ProceduralSkyMaterial` | Teal-to-deep-blue gradient "underwater sky"; arenas build their own envs |
| Ambient | `AMBIENT_SOURCE_SKY`, 0.6 sky contribution, tinted aqua, 0.85–0.9 energy | This is what lifts the cel shadow side (cel.gdshader deliberately has no light floor) |
| Fog | Exponential, density 0.0042, aerial perspective 0.75, sky affect 0.5 | Day/night retint. Cheap and doing a lot of depth work |
| Glow | Custom "Wind Waker bloom": screen blend, HDR threshold 0.96, hand-mixed levels (0/2/4/6), bloom 0.22 | Clamped on Speedy (`_speedy_glow_clamp`). The most tuned system in the stack |
| Tonemap | **ACES**, exposure 1.15, white 1.2 | Per-scene grade profiles (`bright_pastel`, `warm_pastel`, `galaxy`) re-aim exposure/white per arena |
| Adjustments | BCS ≈ 0.96/1.03/0.98 (+ per-scene values) | No color-correction LUT in use |

### 1.2 Lights

- **1 DirectionalLight3D** (sun): cool blue, 2-split PSSM, 90 m max distance,
  shadows **off entirely on Speedy**.
- **~44 OmniLight3D creation sites** (reef pearls, castle hall 16, galaxy 10,
  sky lagoon 6, jellyfish, portals, beacons…). Culling exists: pearl lights
  drop 50 % on Speedy; castle lights register through `_register_castle_light`
  with speedy/night/quality gates. This respects the CLAUDE.md omni budget.
- **0 SpotLight3D. 0 light projectors. 0 Decals. 0 ReflectionProbes.** These
  are all Mobile-capable and unused (see §2).

### 1.3 Shader stack (all Mobile-safe, all custom)

| Shader | Role |
|---|---|
| `cel.gdshader` | Toon: posterized N·L bands + Fresnel rim, per-surface albedo kept. Applied to **gen2 props only** via `_cel_replace` |
| `outline.gdshader` | Inverted-hull ink line as `next_pass` (shared material via `_gen2_outline_mat`) |
| `coral_flow`, `seagrass_sway`, `creature_sway`, `fairy_wing`, `butterfly_flap`, `swing_sway` | Vertex-animated life (wind globals `wind_dir`/`wind_gust`), cel-paired |
| `toon_water` | Stylized water surface |
| `cel_post.gdshader` | Fullscreen posterize + depth-edge ink — **dormant** (Forward+ only, guarded off since the unified-Mobile decision) |
| Inline shaders in `main.gd` | Caustic dapple plane, god-ray blades, fog ring, various additive unshaded overlays |

Plus `_toonify`: every imported CC0 prop gets normals stripped, roughness 1,
metallic 0, pastel-shifted albedo — the world is *already* half cel-shaded by
material discipline rather than by shader.

### 1.4 Fake volumetrics (the right call on Mobile)

God-ray blade meshes (additive, unshaded), the caustics plane that follows
Roshan, plankton GPUParticles, bubble columns. Real volumetric fog is
Forward+-only, so these fakes are the correct architecture and they are
already quality-gated.

### 1.5 Findings (issues, not opinions)

1. **`outline.gdshader` wrote a constant `ALPHA`** — any `ALPHA` write moves a
   spatial material into the transparent pass, so *every outlined prop's
   outline shell* was depth-sorted per frame and skipped early-Z, for zero
   visual difference (the alpha was always 1.0). Ironically `cel.gdshader`'s
   comments warn about exactly this trap. **Fixed in this commit** — outlines
   now render in the opaque pass. Free fill-rate/sorting win on phone.
2. **Speedy kills sun shadows entirely.** The contact grounding of props and
   Roshan disappears on exactly the device that plays most. A 1-split,
   short-distance (≈40 m), lower-atlas shadow may fit the Speedy budget —
   testable live in the new Shadow Lab (§4).
3. **ACES is the only tonemapper ever evaluated.** Godot 4.4 ships AgX, which
   handles saturated blues/purples (our entire palette) with less hue skew but
   desaturates pastel highlights. Needs an on-device A/B — one button now.
4. **`cel_post.gdshader` is dead weight** under the unified-Mobile decision.
   Keep as archive, but the plan of record for cel is per-surface (§3-A).
5. Dev-mode MSAA toggle exists but **FXAA was not exposed** — on old Android,
   FXAA is usually the better price/quality trade at 720p. Now in the lab.

---

## 2. The Godot 4.4 toolbox — what exists, what Mobile allows

### 2.1 Available under the Mobile renderer (usable by this game)

| Tool | Cost on old Android | Fit for this game |
|---|---|---|
| Directional + Omni + **Spot** lights | Spot ≈ omni; per-pixel | Spots are unused: follow-spots, doorway light cones, dramatic castle beams |
| **Light projectors** (texture "cookies" on spot/omni) | Texture fetch per lit pixel | Real light-space caustics, dappled canopy light, stained-glass color splash |
| PSSM splits (1/2/4), `shadow_blur`, `shadow_opacity`, atlas size (`RenderingServer.directional_shadow_atlas_set_size`) | Splits and atlas are the big levers | Tune Speedy shadows instead of deleting them; soft aqua shadows via opacity |
| **Decals** | Moderate (per-pixel blend in decal volume) | Blob contact shadows under cutout characters, story stickers on terrain |
| **ReflectionProbe** | Bake once at load, then cheap-ish sample | Limited: procedural world is built at runtime, but a single static probe could sell the lagoon surface |
| **CameraAttributesPractical DOF** (near/far blur) | Medium — half-res blur passes | Tilt-shift = instant "toy diorama", exactly the art direction |
| Environment: sky (procedural/panorama/**custom sky shader**), exponential fog + aerial perspective, glow (all blend modes, per-level mix), BCS **+ color-correction LUT**, all five tonemappers incl. **AgX** | All cheap-to-free (fog/tonemap/BCS effectively free; glow already paid for) | LUT grading is the one untouched free-ish lever; custom sky shader enables painted-gradient skies with drifting clouds |
| Screen-space `canvas_item` shader reading `hint_screen_texture` | One fullscreen pass — fill-rate bound, fine at 720p | The only post-process route on Mobile (no CompositorEffects). Posterize/vignette/ripple/grain — now in the lab |
| FXAA (`screen_space_aa`), MSAA 2×/4× | FXAA ~free; MSAA 4× meaningful on old GPUs | A/B both in dev mode |
| Per-instance shader uniforms, global shader uniforms | Free | Already used (wind globals); instance uniforms would let cel band-count vary per prop without material duplication |
| **LightmapGI** | Runtime cost tiny (texture sample) | **Poor fit**: requires editor-time baking of static scenes — this world is 100 % procedurally built at runtime. Would need a full authoring-pipeline change |

### 2.2 NOT available under Mobile (do not design toward these)

SDFGI, VoxelGI, SSAO, SSIL, SSR, volumetric fog, TAA, FSR1/FSR2 scaling,
CompositorEffects/RenderingEffects, physical light units / auto-exposure
camera pipeline. Every "make it look like the Zelda remaster" trick that
depends on these needs a faked, authored equivalent — which the game already
does well (god rays, caustic plane, additive overlays).

---

## 3. Proposed major look shifts (with performance analysis)

Each proposal is a coherent art direction move, not a slider tweak. All are
now individually testable on-device via the Lighting Lab before committing.

### A. "Wind Waker complete" — cel-shade the *entire* world
Extend the gen2 pipeline (`_cel_replace` + hull outline) from gen2 props to
terrain, all imported props, and Roshan herself. This is `CEL_SHADING.md`'s
original plan, now finally toggleable live (`Cel-shade the whole world`).

- **Perf:** toon shading is *cheaper* than the StandardMaterial3D PBR path
  (no normal maps, no specular BRDF). The cost is the **outline hull: it
  duplicates every opaque draw call and doubles vertex work.** On a
  4-year-old GPU the game is more fill-rate than vertex bound at 720p, so
  expect roughly −10–20 % headroom; mitigate by outlining only hero-scale
  props (skip terrain + distant flora via visibility ranges) — that keeps
  ~80 % of the read for ~30 % of the cost.
- **Risk:** low — reversible per mesh group; the lab toggle proves the look
  in minutes. The opaque-pass outline fix (§1.5-1) already removed the
  worst hidden cost.

### B. "Toy diorama" — tilt-shift DOF + vignette
`CameraAttributesPractical` far-blur (+ slight near-blur) melts the distant
reef into a miniature; a soft vignette frames it like a book page. Strongest
single-switch push toward "pastel toy playset".

- **Perf:** DOF on Mobile runs as separate half-res blur passes — the most
  expensive single feature proposed here. Budget ~1.5–3 ms on the target
  phone. If it doesn't fit Sparkly, it absolutely won't fit Speedy —
  vignette-only (post lab, ~free) is the graceful fallback.
- **Risk:** medium on perf, zero on art (it *is* the art direction).

### C. "Storybook stage lighting" — spots, projectors, rim
The game has never used a SpotLight3D. Three PoCs now exist: a warm
follow-spot on Roshan, a lavender rim/backlight for silhouette pop against
dark water, and a **caustic light projector** (noise cookie on a downward
spot) that wraps real light-space dapples over geometry — a genuine upgrade
over the additive caustics plane, which only tints the floor plane.

- **Perf:** each shadowless spot costs like an omni of the same radius —
  well inside budget if it *replaces* rather than adds (e.g. projector
  replaces the caustics plane; 2–3 accent omnis retired per new spot).
  Projector adds one texture fetch per lit pixel: fine at these radii.
- **Risk:** low; per-light, incremental, quality-gateable exactly like the
  existing pearl/castle light culls.

### D. "Deeper dusk" — tonemapper + LUT grade pass
Swap/tune the global response: A/B ACES vs AgX on device, then bake the
chosen look plus per-scene tints into a **color-correction LUT** instead of
stacking BCS numbers per arena. One asset, one mental model, zero per-frame
cost difference.

- **Perf:** free (tonemap + adjustments already run every frame).
- **Risk:** low, but *test on the phone's actual panel* — cheap Android
  screens crush exactly the deep blues this game lives in; AgX may read
  muddier there than in preview.

### E. "Painterly frame" — Mobile-safe screen-space post stack
One `canvas_item` fullscreen pass (now built): posterize with highlight
protection (glow sparkles stay round), storybook paper grain, vignette,
underwater ripple. Posterize-over-the-frame approximates the dormant
Forward+ `cel_post` look without the depth buffer.

- **Perf:** one 720p fullscreen pass, few ALU ops — ~0.5–1 ms on old
  hardware. Ripple slightly more (dependent texture read). All-zero
  uniforms hide the layer entirely (zero cost when off).
- **Risk:** low. Keep it OFF during minigames with precise touch targets —
  ripple visually displaces where things are.

### F. What NOT to pursue (negative recommendations)
- **LightmapGI / baked GI:** the world is generated in code at runtime;
  there is nothing for the editor baker to bake. Re-architecting to static
  baked scenes would fight the whole codebase for a subtle win under fog.
- **Real volumetrics / SSAO / SSR:** renderer-unavailable; fakes exist and
  read better in a cel world anyway (SSAO actively fights flat toon bands).
- **More OmniLights:** the budget rule stands; every new idea above spends
  spots/projectors *instead of* omnis, or retires omnis to pay for itself.

---

## 4. The proof of concept: Lighting Lab (implemented in this commit)

Developer mode (F1 / backtick / pause-menu, desktop or `--dev-mode`) gained
three sections. Everything is built lazily on first touch (zero cost for the
child, zero cost in headless probes), is fully restorable, and is deliberately
NOT persisted by Save Look:

- **Lighting Lab (experimental):** tonemapper row (Linear/Reinhard/Filmic/
  ACES/AgX) · cel-shade-the-world toggle · ink-outlines-only toggle ·
  tilt-shift DOF + strength · moon rim light + energy · follow spotlight +
  energy · caustic light projector + energy · flat-ambient toggle with
  Aqua/Lavender/Peach tints · sky restyles (Reef Default / Sunset Glow /
  Night Nebula / Bright Day).
- **Shadow Lab:** PSSM 1/2/4 splits · shadow distance · softness
  (`shadow_blur`) · opacity (aqua-tinted-shadow experiments) · atlas size
  1024/2048/4096 (phone ships at 2048).
- **Post FX Lab:** FXAA toggle · posterize bands · vignette · underwater
  ripple · storybook grain (single Mobile-safe screen pass).

The fps readout now shows frame-time in ms, so every toggle doubles as its
own benchmark on the actual phone. Related fix shipped alongside:
`outline.gdshader` no longer writes `ALPHA` (outlines moved from the
transparent to the opaque pass — same pixels, cheaper frame).

## 5. Ranked recommendations

1. **Adopt A (full cel world) as the flagship shift** — it completes the
   declared art direction, it's perf-*positive* on shading, and the lab
   toggle de-risks it to a phone test. Roll out per mesh group (Roshan →
   props → terrain), outlines on hero props only at first.
2. **Run the D tonemapper A/B on the phone this week** (free), then decide
   LUT consolidation. Keep ACES if AgX mutes the pastels on the real panel.
3. **Land C incrementally**: caustic projector replaces the caustics plane
   if it survives a Speedy-phone test; rim light is the cheapest silhouette
   win in the whole audit and should probably ship regardless.
4. **Prototype B (tilt-shift) but gate to Sparkly only**; fall back to
   vignette-only from E for Speedy.
5. **Fix Speedy shadows via the Shadow Lab findings** (1 split / 40 m /
   atlas 1024 instead of "off") — measure with the ms readout before
   committing.
6. **Do not** pursue baked GI, SSAO/SSR, or real volumetrics (§3-F).

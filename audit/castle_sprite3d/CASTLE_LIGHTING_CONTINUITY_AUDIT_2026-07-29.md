# Pearl Castle lighting and continuity audit — 2026-07-29

> Superseded for runtime fixture presentation, A/B junction treatment, overlap
> clearance, and final tone measurements by
> `CASTLE_SEAM_TONE_OVERLAP_AUDIT_2026-07-29.md`. This file preserves the
> earlier generation/provenance and rejection record.

Status: accepted Codex implementation. This pass supersedes the Main Hall
lighting portions of the 2026-07-28 audit; it does not replace the accepted
two-screen composition, room portals, elevator, throne, or room art.

## Intervention

- The eight Main Hall background tiles remain the preserved 2 x 4 Sprite3D
  grid, but are now shaded light receivers.
- The hall owns one lavender DirectionalLight3D ambient fill and four pooled
  warm SpotLight3D clusters. Only the two clusters belonging to the visible
  half are enabled. Speedy keeps one shadow map active; higher tiers may use
  both visible shadow maps.
- Six identical shell-sconce assemblies are Sprite3D cards at real depth.
  Tapping any assembly toggles its persistent runtime state, changes its
  sprite appearance, plays an existing chime, and recalculates the associated
  engine-light cluster energy.
- Two reused royal shell tapestries replace the implausible aquarium-picture
  emphasis. They are exact-alpha derivatives of the already approved Main
  Hall tapestry, not newly designed art.
- Roshan and all touch props remain real-depth Sprite3D shadow casters.
  Control nodes are used only for HUD and touch routing.

## Asset reuse and generation decision

The repository inventory found an approved royal shell tapestry and the
accepted Main Hall/Opera fixture language, but no reusable clean wall-sconce
cutout: the existing lamp files included their former room backgrounds.
One final built-in ImageGen call was therefore used for the missing opaque
fixture only. Everything else is same-source deterministic reuse.

| Asset | Dimensions | SHA-256 | Provenance |
| --- | ---: | --- |
| `castle_shell_sconce_touchable.png` | 1024 x 1024 | `dd202d48ca3a9d142fbc7f1f0cc738e6ff7c0610f1018982e5223e7d002b761e` | One built-in ImageGen call; 1254 x 1254 chroma source, local alpha removal, then one downsample to the runtime limit |
| `castle_shell_sconce_assembly.png` | 1024 x 1024 | `c3030be711c174cb1e2e9b071e53dee3b8961bbd4d8c87ec02798971e6a91332` | Deterministic architectural mount plus the accepted sconce, built by `tools/build_castle_lighting_assets.py` |
| `castle_royal_tapestry_reuse.png` | 130 x 320 | `1bc0809edd3102dd0dcc0e4605a583078d0d91080b5cad5f84786ab743f83833` | Exact-alpha extraction from the approved 2 x 4 Main Hall reconstruction by the same tool |

The protected originals and the accepted 2048 x 1153 Main Hall masters were
not modified. No new audio, model, GLB, procedural mesh, or Blender source was
introduced.

## Final built-in ImageGen prompt

```text
Use case: illustration-story
Asset type: reusable touchable wall-light sprite for the Pearl Castle main hall in a preschool Godot game
Input images: Images 1 and 2 are strict style references for the current two-screen main hall; Image 3 is a strict fixture-design reference for its gold, navy, pearl, and aqua language.
Primary request: Create exactly one front-facing ornate shell-and-pearl royal wall sconce. It has a pale pink scallop-shell backplate with a warm glowing pearl at its center, small polished gold brackets, one aqua teardrop gem, and a restrained warm halo contained close to the fixture. The silhouette must be simple, chunky, friendly, and immediately tappable for a four-year-old.
Style/medium: match the existing Pearl Castle storybook illustration exactly: polished hand-painted 2D sprite, clean dark plum/navy contour accents, rounded toy-like shapes, pearl highlights, lavender shadows, gold trim, high finish.
Composition/framing: centered single isolated object, straight-on orthographic view, fully visible with generous padding, no perspective wall, no duplicate fixture.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background for removal.
Lighting/mood: fixture is visibly lit with a contained warm cream glow, but no cast shadow and no floor.
Constraints: background must be one uniform #00ff00 with no shadows, gradients, texture, reflections, or lighting variation; do not use #00ff00 anywhere in the subject; no wall fragment; no architecture; no text; no logo; no banner; no watermark; no sea picture; no frame; no second object.
```

Built-in output path at generation time:
`C:\Users\Peter\.codex\generated_images\019fa1a6-6274-77b2-bb27-38aa32e6e4dd\call_GMHtxcTLYWGJvXaEIMUYzNnR.png`.
The project copy was processed with the installed imagegen
`remove_chroma_key.py` helper. The original generated file remains unchanged.

## Runtime node inventory

| Type | Total/visible in Main Hall | Role |
| --- | ---: | --- |
| Sprite3D background cards | 8 / 8 | shaded, depth-tested light receivers |
| Sprite3D touch cards | 11 / 11 | six sconces, one tapestry, four lower-lane dust bunnies |
| Sprite3D character/contact shadow | 2 / 2 | Roshan and her contact shadow |
| Light3D | 5 / 3 | one ambient fill plus two visible-half SpotLight3D clusters |
| Shadowed Light3D on Speedy | 1 | hard mobile cap |
| Modeled or CanvasItem world art | 0 | conforming |

Maximum visible Sprite3D count is 25, below the revised lighting-stage cap of
26. All runtime textures remain at or below the 1024-long-edge rule. The
two-screen background still reconstructs from the original lossless tiles;
no background pixel was stretched, cropped, padded, or replaced in this pass.

## Validation evidence

On/off contact:
`audit/castle_sprite3d/main_hall_lighting_on_off_contact.png`,
SHA-256 `d56e8778d225e692997c3fc110e7c1cc40e11d553f2c630f3f67d578886519a0`.

- lights-on capture: `main_hall.png`, SHA-256
  `19aeb10fb70c20a40a9bb3b95ff3529f9acfbcaeb5237e1acae8f1d6d848b772`
- all Screen A sconces off: `main_hall_lights_off.png`, SHA-256
  `0cfd837343439e263ddaed13e27b7ad37d5fe6bcbc152d54f035bf1deba1a7d4`
- Screen B continuity capture: `main_hall_screen_b.png`, SHA-256
  `eac0d4b56fa966e90198a987dc719f6e66a6d65f7393a41f9b2612907b583ae1`

The Mobile renderer probe reports:

```text
all_eight_rooms_sprite3d_only OK
speedy_visible_card_budget OK maximum visible cards=25
main_hall_native_2x4_sprite3d_grid OK
main_hall_mobile_light_pool OK visible=3 shadowed=1
main_hall_fixture_and_tapestry_continuity OK
main_hall_touch_lighting_engine OK
main_hall_all_lights_off_affects_engine OK
RESULT=OK checks_failed=0
```

Static parser, inference lint, and Python compile gates are clean.

## Rejected iterations

1. Source-master coordinates were rejected after the first Mobile capture
   showed mirrors and lamps overlapping doors. Final sockets use runtime
   2 x 4 reconstruction coordinates.
2. New pearl-mirror inserts were rejected because they read as pale temporary
   panels. They were removed; approved tapestry art is reused instead.
3. A same-source baked-lamp cleanup was rejected for restoration artifacts.
   Its derived master and tiles were removed; accepted originals remain.
4. Shadows-only column cards were rejected because Mobile exposed a horizontal
   shadow seam. They and their texture were removed.

This was the 25th and final built-in ImageGen call in the owner's current
25-call castle ceiling. No further generation was needed after the final
runtime audit passed.

## Subjective re-audit

| Goal | Score | Verdict |
| --- | ---: | --- |
| Lighting depth and touch response | 4.6 / 5 | Pass |
| Cross-screen fixture continuity | 4.6 / 5 | Pass |
| Castle/room style continuity | 4.5 / 5 | Pass |
| Preschool readability | 4.7 / 5 | Pass |
| Speedy-tier discipline | 4.7 / 5 | Pass |
| Overall | 4.62 / 5 | Accepted |

## Dramatic glow/bloom amendment

The owner requested stronger theatrical lighting after the discreet fixture
cleanup. The implementation changes only light/post-process behavior:

| Property | Full | Speedy | Visible-half off |
| --- | ---: | ---: | ---: |
| Glow intensity | 1.12 | 0.75 | 0.24 |
| Bloom | 0.24 | 0.11 | 0.015 |
| HDR threshold | 0.74 | 0.74 | 0.98 |
| Cool fill energy | 0.72 | 0.72 | 0.42 |
| Shadow maps | visible clusters | 1 maximum | 0 |

Every SpotLight3D cluster now has the same maximum energy (`4.6`), range
(`12.5`), cone (`52` degrees), and warm pearl color. The six existing
unshaded fixture cards become HDR bloom emitters while on and return to a dim
lavender state while off. This creates no new Sprite3D card, transparent
overdraw layer, light, particle system, mesh, texture, or generated art.

The castle Environment is scoped to the room shell and restores the previous
world Environment on suspend/close. The hard probe checks environment
activation/restoration, the Speedy glow/shadow clamp, equal cluster energy,
and the full on/off lighting-envelope delta.

## Final Mobile seam and dramatic-lighting validation

The stronger dark state exposed a one-pixel clear row at the horizontal
boundary of the otherwise exact 2 x 4 Main Hall grid. Changing transparency
mode and texture filtering did not solve it and nearest filtering visibly
reduced texture quality, so both experiments were rejected.

The accepted fix reuses only existing approved pixels:

- the four immutable top sources remain 836 x 470;
- each render-only top derivative is 836 x 471;
- rows 0 through 469 match the source top tile pixel-for-pixel;
- row 470 matches the first row of the approved lower tile pixel-for-pixel;
- lower sources, logical source rectangles, pixels-per-meter, aspect ratio,
  card count, depth, navigation, and touch mapping are unchanged;
- linear filtering and the established opaque prepass are retained.

`tools/build_castle_hall_runtime_bleed.py` reproduces the four files and
`castle_main_hall_runtime_seam_bleed.json` records every source and derived
hash. All eight source rectangles are still non-overlapping; only their
render quads share the single approved boundary row.

Forward Mobile (`NVIDIA GeForce RTX 3060 Ti`) captured the final 2560 x 1369
on/off states. In `main_hall_lights_off.png`, no image row contains an
exact-black run 500 pixels or longer. At the former crack row, y=681, the
longest exact-black run is 27 pixels, confined to painted dark details; the
previous defect was a 2560-pixel clear run. The final structural probe reports
all checks green, including the 2 x 4 bleed metadata and texture dimensions.

Additional final hashes:

- seam/bridge capture: `3c850c8df8da806fff7efe0d917e76bac71a5476c7338d355a105bdd3bd57e70`;
- Screen B capture: `eac0d4b56fa966e90198a987dc719f6e66a6d65f7393a41f9b2612907b583ae1`;
- Storybook elevator capture: `e8f26f4380a9d84f6a725c7876c4903d57ec45fb6abcc2f87ee30b935840eaf8`.

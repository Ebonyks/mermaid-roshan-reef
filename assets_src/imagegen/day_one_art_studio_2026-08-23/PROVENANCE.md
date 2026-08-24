# Day One Art Studio — new item direction packet

Prepared 2026-08-23 before final construction under
`design/07_NEW_ITEM_DESIGN_INTAKE.md` at commit `f96e24c2`. The previous
runtime used procedural representational drawings for every focal cleanup
item. Those drawings are retained only as rejection evidence and are not an
appearance anchor.

## Shared direction

- Item ID / runtime role: `brushes`, `pink_paint`, `blue_paint`, `paint_cups`,
  `left_counter`, `desk_counter`, `right_counter`, and `cleaning_brush`.
- Child-facing verb or meaning: tap loose supplies to put them away; tap gentle
  grime to scrub it clean; use the brush to choose attack color and either a
  bubble or splash action.
- Destination scene, layer, and owning script: fixed-camera Craft Room. Touch
  controls/pointer remain on the stage overlay at `z_index` 22, while all
  representational cleanup art is owned by a temporary Node2D under
  `castle_room_world_root` at explicit depths 2.49–4.01. Both are owned and
  torn down by `scripts/day_one_art_studio.gd`; the modal brush is owned by
  `scripts/attack_customizer.gd` on CanvasLayer 18.
- Intended 1024×576 art-space display rect (scaled 1.25 into 1280×720): loose
  brushes 92×62, each bottle 42×56, cup group 92×62, counter grime 82×18,
  desk grime 96×18, and modal brush 208×160 logical screen px. Every supply
  must read from silhouette and two or three color blocks at target size.
- Construction lane: **New 2D item** for five named representational gaps;
  **Direct reuse** for the existing bubble/splash atlases; **Code-native
  interface** for touch surfaces, selection rings, glow, pointer, and sparkles.
- Named gap and why approved reuse is insufficient: approved Craft Room art
  contains supplies painted into counters and shelves, but no separately owned
  loose brush bundle, matching paint-bottle pair, paint-cup group, removable
  grime family, or full-size cleaning-brush card. Extracting those tiny painted
  pixels would not survive the required display size. Existing water FX do
  satisfy the bubble/splash role and must be reused.
- Protected-content status: no protected book, family voice, or friend pixels
  are edited or copied. Protected material is not an input.
- Applicable stable rules: `DL-AGE-01`–`DL-AGE-07`, `DL-MED-01`, `DL-MED-05`,
  `DL-VIS-01`–`DL-VIS-05`, `DL-READ-01`–`DL-READ-06`, `DL-LAY-03`,
  `DL-LAY-09`, `DL-INT-01`–`DL-INT-04`, `DL-UI-01`, `DL-UI-03`,
  `DL-UI-06`, `DL-MOT-03`, `DL-MOT-04`, `DL-PERF-01`, `DL-PERF-04`, and
  `DL-ASSET-01`–`DL-ASSET-06`.

### Reuse inventory

| Candidate path | Current authority/acceptance evidence | Reuse decision and reason |
|---|---|---|
| `assets/flats/castle/rooms/room_craft_room_item_paint_table.png` | 4.6/5 Castle item in `FABLE_CASTLE_ITEM_STYLE_AUDIT_2026-07-28.md` | Appearance anchor only; object pixels are too small and painted into a full table crop. |
| `assets/flats/castle/rooms/room_craft_room_item_palette.png` | 4.6/5 Castle item in the same audit | Appearance anchor only; broad counter pixels prevent reuse as loose cups or bottles. |
| `assets/castle/day_one_pool/activities/waterfall_scrubber.png` | Selected current Day One item with provenance and runtime derivative hash | Appearance anchor only; it is a pool squeegee, not the requested paint/cleaning brush. |
| `assets/castle/day_one_pool/activities/cleanup_basket.png` | Selected current Day One item with provenance and runtime derivative hash | Appearance anchor only; it establishes item-card finish, not studio function. |
| `assets/sprites/fx_water/fx_water_bubble_burst_atlas.png` | Existing authored 4×2 water-FX atlas | **Direct reuse** for the bubbles choice and impact animation. |
| `assets/sprites/fx_water/fx_water_splash_medium_atlas.png` | Existing authored 3×3 water-FX atlas | **Direct reuse** for the splashes choice and impact animation. |

### Appearance anchors

| Approved path or capture | SHA-256 / commit | Exact trait borrowed | Trait explicitly not borrowed |
|---|---|---|---|
| `assets/flats/castle/rooms/room_craft_room.png` | `916522a6fab6691866e8ff768056a5725bfbb76044dba869935eb7b585420eae`, commit `89b004ac` | destination perspective, muted pearl/lavender/cyan palette, thin plum contour, matte painted counters | no copying of embedded supplies, architecture, banners, or room pixels |
| `assets/flats/castle/rooms/room_craft_room_item_paint_table.png` | `b2eb0fc3a5d7c777540af1447827f6b2f98d47a658d2184d9774e407d46627aa`, commit `89b004ac` | simple craft-tool silhouettes, restrained detail, front three-quarter viewing angle | no table, shelf, paper, or neighboring objects |
| `assets/castle/day_one_pool/activities/waterfall_scrubber.png` | `1b29ff463263be093a7e1ac33eb74e4075d6a795dd515d120107f66953b2dc7a`, commit `89b004ac` | complete tool silhouette, rounded handle, clean alpha, pearl hardware, strong target-size contour | no squeegee blade, shell fan ornament, rainbow gloss, or pool-specific identity |
| `assets/castle/day_one_pool/activities/cleanup_basket.png` | `30b43ce7b1f2db7098281a399f64db13c26c30fb9fce60f478b5f0cecdfd2910`, commit `89b004ac` | complete high-quality Day One item card and grouped painted value bands | no basket form, handles, recycling symbol, or shell container identity |

- Motif family and unmistakable functional silhouette: handmade craft
  materials; handles, bristles, squeeze necks, open cup rims, and broad wipeable
  smears remain obvious without text.
- Major shape count and detail clusters: five to eight major shapes per prop;
  two detail clusters maximum (hardware/label, bristle/paint edge).
- Contour color/weight and interior-line limit: deep plum/indigo, 2–4 screen px
  outer contour and 1–2 px interior marks at final display size.
- Three broad value families and material-specific highlight: light local base,
  aqua/lavender cool shadow, restrained deep contour; matte wood/paper/plastic
  gets one cream or pale-cyan highlight, never chrome.
- Palette roles: the room remains the cool field; local coral pink, ocean blue,
  mint, lavender, chestnut, and shell cream identify supplies; warm gold marks
  caps or contact points only.
- Perspective, scale, pivot/contact point, `z_index`, and parallax role:
  shallow front three-quarter loose supplies rest on open floor around
  art-space y=390 with approved contact shadows, bottom-center pivot, world
  depth z=2.50. Existing stored counter supplies remain untouched room art.
  Grime hugs the left/right counter faces at z=4.01 and desk plane at z=2.01;
  modal brush is isolated and centered.
- Required visual states: idle/rest card; prompted pointer/glow; contact sparkle;
  changed state removes the owned card; settle exposes the untouched approved
  room beneath. Attack FX use the existing atlas frames and settle to alpha.
- Touch footprint, pointer/voice cue, and no-reading route: existing 164–282 px
  hit regions remain; the moving hand pointer targets the exact live card and
  Roshan speaks the current verb. No text is required.
- Explicit exclusions and likely drift: no white sticker rim, black grime mass,
  photoreal or glossy plastic, noisy watercolor edge, PBR lighting, cast shadow,
  floor/counter/background pixels, faces, words, logos, rainbow fill, detached
  tool parts, tiny multiple props, or unrelated shell ornament.

## Exact generation prompts

All requests use the built-in image-generation tool and the referenced images
only for the exact mapped traits above.

### A1 — loose brush bundle

Use case: stylized-concept. Asset type: transparent 2D game item card. Primary
request: three complete child-size paintbrushes lying as one loose diagonal
bundle, with three distinct chestnut wooden handles, rounded gold ferrules, and
coral, aqua, and lavender paint-tipped bristles. Style: polished Mermaid Roshan
storybook cel illustration matching the references: confident deep-plum
contours, broad rounded slightly asymmetrical shapes, two or three matte painted
value bands, sparse dry-brush grain inside shapes only. Composition: isolated
wide horizontal bundle, every handle and bristle fully visible, bottom-center
contact, generous transparent padding. Constraints: genuine transparent
background, no cast shadow, no table, no cup, no palette, no text, no logo, no
watermark. Avoid: thick white sticker rim, black outlines, photorealism, glossy
plastic, airbrushed volume, noisy watercolor edges, micro-detail, faces, hands,
extra tools, or cropped parts.

### A2 — paired paint bottles

Use case: stylized-concept. Asset type: strict two-item transparent game atlas.
Primary request: two matching complete child-safe squeeze-paint bottles, pink
on the left and ocean-blue on the right, each with a broad rounded bottle body,
short neck, restrained warm-gold flip cap, blank shell-cream oval label, and one
small pale-cyan material highlight. Style and constraints: the same polished
storybook cel language and matte value bands as A1. Composition: exactly two
separate upright bottles, equal scale and geometry, generous gap, no overlap,
each fully visible. Genuine transparent background; no cast shadow, table,
letters, symbols, logo, watermark, extra bottle, rainbow, face, or cropped part.
Avoid all drift listed in A1.

### A3 — paint cups

Use case: stylized-concept. Asset type: transparent 2D game item card. Primary
request: one loose group of three squat open craft-paint cups in aqua, coral
pink, and lavender, each cup complete with a thick rolled rim, clearly visible
matching paint surface, and one small wooden stirring stick leaning from the
middle cup. Front three-quarter view, broad phone-readable silhouette, five to
eight major color shapes, matte painted cel bands. Genuine transparent
background, no cast shadow, table, brushes, bottle, face, text, logo, watermark,
extra cup, spill, or cropped part. Avoid all drift listed in A1.

### A4 — gentle grime atlas

Use case: stylized-concept. Asset type: strict three-item transparent game
atlas. Primary request: exactly three separate broad wipeable craft-room grime
smears arranged left-to-right, each a different soft irregular silhouette with
rounded edges, muted lavender-grey body, aqua shadow edge, and two or three
small dried-paint flecks in coral/mint/blue. Top-down oblique counter-plane
view; friendly, clearly dirty but never frightening; each patch remains one
calm readable mass at phone size. Genuine transparent background, no counter,
cast shadow, black sludge, puddle depth, drips, text, face, logo, watermark,
overlap, or cropped patch. Avoid photoreal dirt, grit, mold, horror, noise, white
sticker rim, glossy liquid, or tiny scattered debris.

### A5 — magic cleaning brush

Use case: stylized-concept. Asset type: transparent 2D game UI item. Primary
request: one complete magical cleaning brush for a four-year-old's picture-first
attack customizer: short curved chestnut handle, lavender grip, warm-gold ferrule,
broad fan of pearl-white bristles tipped in pale aqua, and one small pearl set
into the handle. It must read unmistakably as a usable cleaning/paint brush,
not a wand or squeegee. Three-quarter diagonal composition, complete silhouette,
matte storybook cel bands, deep-plum contour, generous transparent padding.
Genuine transparent background; no cast shadow, paint puddle, hand, face, text,
logo, watermark, rainbow fill, weapon blade, star wand, extra brush, or cropped
part. Avoid all drift listed in A1.

## Generation record and decisions

All accepted candidates were generated with the built-in OpenAI ImageGen tool
from the exact prompts above. No external artwork was used. The native results
are preserved here before deterministic runtime preparation.

| ID | Attempt / ImageGen result | Decision | Native path and SHA-256 |
|---|---|---|---|
| A1 | 1 / `exec-4d0ef490-ef5a-49f3-b627-bf74ba0ad305.png` | selected; three complete brushes, strong differentiated silhouette and room-compatible coral/aqua/lavender paint | `loose_brush_bundle_native.png` — `dc29f0589d2a1493ba8f3f882ec0c98c2a53bd69248d733203566f839f3309e3` |
| A1 | alpha edit / `exec-5a3a9719-c512-44d3-bac7-919c9c5b02d1.png` | **rejected**; the edit visibly baked a checkerboard into opaque delivery pixels | rejected file removed; it contributes no runtime pixels |
| A2 | 1 / `exec-1149685d-7700-46f7-8468-a969dbfddaf2.png` | selected; equal-scale pink/blue bottle pair with child-readable forms | `paint_bottle_pair_native.png` — `3a6c96005261c88a2b4eabee04f547c9626d3c5d3346652c1072eb86773d3af3` |
| A3 | 1 / `exec-070d758b-a379-4de8-b08f-e8a48c0528ac.png` | selected; three open paint cups read as one complete group | `paint_cups_native.png` — `31edf10d5e0e340bb01248a90ba788c510648562591507b456bb94840107535b` |
| A4 | 1 / `exec-0b039892-32fd-45e0-8897-63a780cdfe8a.png` | **rejected**; glossy puddles and droplets conflicted with the requested matte wipeable grime | rejected result remains outside the project and contributes no runtime pixels |
| A4 | 2 / `exec-2f13d912-f086-48f8-86f9-e1bf5c04da9a.png` | **rejected**; the attempted correction baked an opaque checkerboard | rejected result remains outside the project and contributes no runtime pixels |
| A4 | 3 / `exec-868ebcee-aefe-4c6f-8688-bc7347c7909e.png` | selected; three calm matte craft-residue masses without sludge or liquid depth | `grime_patches_native.png` — `d5a87284962690a1da0960aca2ccf755b532056d3fb637819676c6ffc0ca385a` |
| A5 | 1 / `exec-f4b6f291-d9ac-46cc-adab-407606beedcb.png` | selected; complete magical brush, clearly a brush rather than a wand or weapon | `magic_cleaning_brush_native.png` — `69d3052608520cb0253a1c21445fda6a74c457715024ac23b928cf8354b82f26` |

The selected natives contained high-opacity decorative aura beyond some inked
silhouettes. `tools/prepare_day_one_art_studio.py` derives an alpha mask from
painted subject values, expands it by a bounded 13 px (15 px for grime) to
retain the adjacent authored contour, intersects the original alpha, keeps the
largest connected subject, then performs the documented crop and Lanczos
resize. It never repaints RGB subject pixels. Re-running the tool produces:

| Runtime delivery | Size | SHA-256 |
|---|---:|---|
| `assets/castle/day_one_art_studio/loose_brush_bundle.png` | 768×512 | `7de7cf80939fe62e16d6931d1eb6b377ec2454107b855703b76f445aa8aad99a` |
| `assets/castle/day_one_art_studio/paint_bottle_pink.png` | 384×512 | `089bcaf7b7e27a4760ca70f05cfeb6954e72eb59ac4ecd125fd6b5cfe0ebba4a` |
| `assets/castle/day_one_art_studio/paint_bottle_blue.png` | 384×512 | `ce6adb14e4d877108ae2748138417ef436f6e154b8c4321f69196795114319ff` |
| `assets/castle/day_one_art_studio/paint_cups.png` | 768×512 | `fca25541d66e07bf28ee31a36ff049130af64c495a077759750f291e526780a0` |
| `assets/castle/day_one_art_studio/grime_left.png` | 512×306 | `125978f082934e3b290370c6a7a2c0082b8e5df5044feecbf22f3d5d6dca0ac1` |
| `assets/castle/day_one_art_studio/grime_desk.png` | 512×346 | `586021e28238f3ddba60447a3e7472a51a9af72f5bbc4319f95c79265b0a43bf` |
| `assets/castle/day_one_art_studio/grime_right.png` | 512×307 | `339f248e488bf651749746c0819ba0214373684ec59859ed3815ddfa387bfe28` |
| `assets/castle/day_one_art_studio/magic_cleaning_brush.png` | 936×1024 | `17e76b7f758f31a9b148167ff103a68bdf9543e7aac5794314a97bbd91066ef3` |

## Review status

- Isolated-item comparison against the named Craft Room, paint-table,
  scrubber, and cleanup-basket anchors: **Codex pass, 2026-08-23**. Complete
  silhouettes, broad matte value bands, limited interior detail, room palette,
  and clean runtime alpha were inspected at native and reduced sizes.
- Initial runtime composites: **rejected**. First capture exposed native-size
  TextureRect clamping; the corrected-size stage-level cards still duplicated
  and overpainted source-owned counter props. A dedicated Luna-agent audit
  identified the ownership failure: UI z=22 was structurally above the entire
  depth-composed room.
- Revised runtime composite: **Codex pass, 2026-08-23**, after executing the
  Luna plan. Materials now occupy open floor positions `(344,390)`,
  `(416,390)`, `(608,390)`, `(681,390)` at world depth 2.50 with contact
  shadows. Cleanup invokes the accepted room-owned palette/paint-table
  animations. Grime is constrained to 18-pixel-high marks on the actual
  surface depth. Captures `00_loose_supplies.png` through
  `06_splash_attack_frame.png` were reviewed from the session's
  `day_one_art_runtime_review` folder; room identity, player occlusion, modal
  ownership, selection clarity, and authored attack frame all pass Gate C.
- Target-device, child, and owner review: pending; no approval is inferred.
- License record: `ASSET_LICENSES.md`, Day One Art Studio section.

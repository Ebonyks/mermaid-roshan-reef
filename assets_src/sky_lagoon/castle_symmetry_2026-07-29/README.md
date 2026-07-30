# Sky Lagoon balanced castle correction

Mode: three tightly scoped OpenAI built-in image-generation edits, followed by
deterministic local chroma removal, owner-art restoration, cropping, and
downscaling. The first two edits are rejected design studies retained only as
evidence. The third is the accepted four-tower runtime card and retains the
established in-scene perspective.

## Reuse inventory and generation gap

- The current runtime card
  `assets/sprites/sky_lagoon/sky_lagoon_castle_stained_glass_v1.png`
  supplied the approved palette, painted materials, bridge, and façade style.
- The selected approved turnaround
  `assets_src/sky_lagoon/cohesion_pass_2026-07-19/selected/pearl_castle_exterior_turnaround_v2.png`
  supplied the balanced two-tower front-elevation design.
- The owner panel
  `assets_src/sky_lagoon/reductive_rebuild_2026-07-28/stained_glass_owner_reference.png`
  remains the sole stained-glass source.
- Direct cropping was not viable because the turnaround front occupies only a
  small part of a 1024×683 four-view sheet. Enlarging it to the runtime castle
  size would materially undershoot the native-detail and child-readability bar.
  Generation was therefore limited to reconstructing that already-approved
  balanced architecture at usable resolution.

## Image edit prompt

> Use case: precise-object-edit
>
> Asset type: production Sprite3D depth card for a mobile children's storybook
> game
>
> Input images: Image 1 is the edit target and current approved runtime castle
> card; Image 2 is the approved architectural turnaround reference, especially
> its balanced front elevation.
>
> Primary request: Redesign only the castle architecture in Image 1 so the
> front facade is clearly intentional, centered, and bilaterally balanced like
> the front elevation in Image 2. Remove the accidental unmatched extra rear
> tower. Use exactly two matching round side towers, one on each side, with
> equal height, equal width, matching conical purple roofs, matching shell
> finials, matching turquoise windows, and matching coral/aqua/gold trim.
> Center the main pointed gable, stained-glass opening, coral double door, and
> entry axis. Keep the castle broad, welcoming, and child-readable rather than
> narrow or realistic.
>
> Scene/backdrop: perfectly flat solid #00FF00 chroma-key background for
> background removal.
>
> Style/medium: preserve the exact polished 2D painted storybook style,
> navy/purple outlines, lavender masonry, quilted purple roofs, aqua windows,
> coral shells, and soft dimensional shading of Image 1.
>
> Composition/framing: isolated full castle plus attached drawbridge, fully
> visible with generous padding; straight-on centered front elevation. Keep
> the existing drawbridge perspective from Image 1, centered on the door and
> extending toward the viewer.
>
> Constraints: architecture edit only. Preserve the overall footprint and
> scale needed to replace Image 1. Preserve the existing stained-glass panel
> placement and pointed gold frame as closely as possible; it will be restored
> deterministically afterward from owner art. Preserve the coral door and
> bridge concept. Exactly two side towers total, one left and one right. No
> people outside the stained glass. No scenery. Background must be one uniform
> #00FF00 with no shadows, gradients, texture, reflections, floor plane, or
> lighting variation. Keep crisp antialiased edges. No cast shadow, no contact
> shadow, no text, no watermark.
>
> Avoid: asymmetry, extra towers, unmatched turret, side perspective, skewed
> central gable, duplicated doors, tiny windows, photorealism, 3D render look,
> new symbols, new characters, scenery, clouds, mountains, plants, water.

`castle_balanced_chroma_raw.png` is the untouched first built-in output. It
resolved the architectural symmetry but flattened the camera, so it is retained
only as a design reference and is not loaded by the game.
`castle_balanced_transparent_raw.png` is the local chroma-removal result.

## Rejected two-tower perspective-correction prompt

> Use case: precise-object-edit
>
> Asset type: final production Sprite3D castle depth card for the existing
> three-screen Sky Lagoon scene
>
> Input images: Image 1 is the production edit target and the ONLY
> camera/perspective reference. Image 2 is the approved architectural turnaround
> and supplies the structurally balanced two-tower design. Image 3 is a
> front-elevation design reference only; do NOT copy its straight-on camera or
> centered bridge projection.
>
> Primary request: Redesign the castle architecture in Image 1 so the underlying
> building is an intentional, structurally matched two-tower castle, while
> preserving Image 1's exact in-scene oblique perspective. Remove the accidental
> unmatched extra rear tower. Keep one round side tower on the left and one
> matching round side tower on the right in world design, but project them
> naturally in Image 1's three-quarter view: the nearer tower may appear larger
> and the farther tower smaller due to perspective. Center the main pointed
> gable, stained-glass opening, and coral door on the castle's architectural
> entrance axis in 3D, not on the image canvas.
>
> Perspective lock: preserve Image 1's viewing angle, horizon/eye level,
> vanishing directions, foreshortening, and footprint. The castle must remain
> viewed obliquely from the same side as Image 1, never as a straight-on
> elevation. Preserve Image 1's attached drawbridge direction and trapezoidal
> perspective exactly: it recedes diagonally from the lower-left foreground
> toward the castle door at the upper-right/center of the card. The bridge must
> not become vertically centered, mirror-symmetric on the canvas, or point
> straight down.
>
> Style/medium: preserve Image 1's exact polished 2D painted storybook style,
> lavender masonry, quilted purple roofs, aqua windows, coral/aqua/gold shell
> trim, navy-purple outlines, and soft dimensional shading.
>
> Composition/framing: isolated full castle and entire attached drawbridge, same
> overall silhouette bounds and transparent-card composition as Image 1, with
> generous edge padding.
>
> Scene/backdrop: perfectly flat solid #00FF00 chroma-key background for
> background removal.
>
> Constraints: architecture edit only; structurally balanced in 3D but
> perspective-correct and intentionally asymmetric in 2D projection. Exactly
> two round side towers total, no unmatched third tower. Preserve the existing
> stained-glass panel placement and pointed gold frame as closely as possible;
> owner art will be restored deterministically afterward. Preserve the coral
> door and all bridge posts/rails. No people outside the stained glass. No
> scenery. One uniform #00FF00 background, no shadow, gradient, texture, floor,
> reflection, text, or watermark.
>
> Avoid: straight-on camera, front elevation, bilateral pixel symmetry, centered
> vertical bridge, orthographic projection, extra tower, unmatched turret,
> skewed entrance axis, duplicated doors, photorealism, 3D render look, new
> symbols, new characters, scenery, clouds, mountains, plants, water.

`castle_perspective_chroma_raw.png` is the untouched second built-in output,
and `castle_perspective_transparent_raw.png` is its local chroma-removal
result. Both are rejected, non-runtime studies: this attempt made the castle
smaller, omitted the intended tower hierarchy, and weakened its placement in
the background.

## Accepted four-tower core design

Owner correction after review: the landmark is not a two-tower simplification.
Its intended hierarchy is two lower outer towers, two taller inner towers, and
one central stained-glass gable. The production edit therefore completes the
missing right inner tower while retaining the grand overall mass.

The base card receives no glow, bloom, light pool, color wash, or scene-grade
effect. Runtime loads it as an unshaded Sprite3D with shadows disabled. Any
future lighting treatment must remain a separate reversible post layer.

Final edit prompt:

> Use case: precise-object-edit
>
> Asset type: preview-only repair candidate for the existing Sky Lagoon castle
> Sprite3D card
>
> Input image: Image 1 is the sole edit target and the sole authority for
> camera, scale, placement, silhouette, style, door, stained glass, and
> drawbridge.
>
> Primary request: Complete the intended grand four-tower castle design by
> adding only the missing RIGHT INNER tower. The existing architecture already
> has, from left to right: a lower left outer tower, a taller left inner tower,
> the central stained-glass gable, and the right outer tower. Add one taller
> right inner tower between the central gable and the existing right outer
> tower, corresponding architecturally to the existing taller left inner tower.
> It must sit behind the right wing and be naturally foreshortened in the
> existing oblique perspective. Make the hierarchy read clearly as two lower
> outer towers plus two taller inner towers flanking the central gable. There
> must be exactly four purple conical tower roofs total, two on each side, plus
> the separate central gold shell roof finial.
>
> Surgical edit boundary: change only the roof/wall area needed to insert the
> missing right inner tower and its clean overlap behind the right wing.
> Preserve every existing element elsewhere: the full left outer tower, full
> left inner tower, central gable and roof, gold shell finial, pointed gold
> stained-glass frame and its artwork, coral door, columns, right outer tower,
> lower walls, shell trim, windows, foundations, entire drawbridge, every
> bridge post and rail, all transparent padding, and the existing painted
> perspective.
>
> Perspective and placement lock: keep Image 1's exact oblique viewing angle,
> vanishing directions, castle scale, footprint, image-space position, crop,
> and overall width/height. Keep the drawbridge exactly the same size and
> direction, extending diagonally toward the lower-left foreground. Do not
> recenter, shrink, enlarge, rotate, or move the castle. The output must overlay
> Image 1 everywhere outside the new right-inner-tower region.
>
> Style/medium: match Image 1 exactly—polished 2D storybook painting, lavender
> masonry, quilted purple roofs, aqua windows, coral/aqua/gold shell ornament,
> navy-purple outlines, and soft dimensional shading.
>
> Scene/backdrop: perfectly flat solid #00FF00 chroma-key background for later
> removal, with no shadow, gradient, texture, floor, reflection, scenery, text,
> or watermark.
>
> Constraints: four-tower palace, grand child-readable landmark, original
> overall scale, original bridge landing, exact original stained glass outside
> the edit region.
>
> Avoid: two-tower simplification, three-tower asymmetry, five or more towers,
> straight-on camera, pixel mirroring, centered vertical bridge, smaller castle,
> larger castle, changed bridge, changed stained glass, changed door, redesigned
> facade, new scenery, new symbols, photorealism, 3D-render look.

`four_tower_candidate_chroma_raw.png` is the untouched built-in output and
`four_tower_candidate_transparent_raw.png` is its local chroma-removal result.
The deterministic preparation tool restores the owner glass, creates the
1022×1024 runtime card, and derives its transform from the approved fallback:
equal world width, equal base waterline, and equal bridge-landing coordinate.
The measured contract is recorded in `four_tower_fit_audit.json`, and
`qa_four_tower_fit_2screen.jpg` shows the unchanged playground/castle two-screen
composition with no added lighting or post effect.

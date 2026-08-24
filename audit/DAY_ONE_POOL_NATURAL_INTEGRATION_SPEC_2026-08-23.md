# Day One Pool natural-integration specification — 2026-08-23

## Outcome

The current activity is functionally readable but its generated props do not
yet belong to the Mermaid Pool scene. The approved correction is a bounded
runtime-compositing pass using the existing room and V4 fixture art, guided by
`assets_src/imagegen/day_one_pool_natural_integration_2026-08-23/room_activity_integration_reference_native.png`.
The reference is not production art and must never replace the approved room.

No gameplay GDScript was changed by this visual-reference branch.

## Ranked visual diagnosis

1. The full-screen teal veil, broad translucent radial sectors, target rings,
   pointer, six debris pieces, giant skimmer, basket, waterfall and seahorse
   all compete at nearly equal priority. The result reads as a modal overlay.
2. The new cutouts use product-render lighting: saturated cyan/magenta/lime,
   dense white specular marks, crisp dark edges and isolated halos. The room
   uses diffuse upper-left light and broad matte-to-satin paint.
3. Props lack physical contact. Trash has no narrow waterline occlusion,
   skimmer and basket do not meet a surface, and the mouth plug does not enter
   behind the nozzle edge.
4. Runtime scale is inflated. The approximately 330px skimmer, 122px trash
   cells and 210px basket overwhelm the 1280x720 room.
5. The dirty waterfall and seahorse are redrawn complete fixtures above the
   accepted ones, which exposes any silhouette or registration difference as
   a sticker edge.

## Binding runtime treatment

### Hierarchy and scale

- Show one active action at full emphasis. Hide future task tools and target
  rings; completed/future environmental defects stay at room contrast.
- At 1280x720, stage the moving skimmer at no more than 230-245px wide and
  150-165px high. Preserve a larger invisible touch envelope.
- Stage individual debris at 72-92px apparent width, depending on silhouette.
- Stage the basket at 130-145px wide on the front-right dry promenade, clear
  of the control overlay. Preserve a larger invisible drop target.
- Do not dim the whole room. If focus help is required, use one local pointer
  or low-opacity ring at the active target only.

### Scene contact and depth

- Debris belongs below the brightest water-caustic pass. Add one restrained
  local ripple/contact ellipse per object, only 8-16px beyond its silhouette.
- Soften/tint the bottom 2-4 screen pixels of floating objects toward the
  local aqua water color to imply submersion. Contact shadows are aqua or
  lavender, never black.
- The skimmer net touches the water plane; its lower net edge receives the
  same local aqua occlusion while the handle stays above water.
- The basket rests against the foreground rim/promenade with a short soft
  lavender contact shadow. Where practical, let the foreground rim occlude
  the bottom edge by a few pixels.
- The mouth blockage begins behind the seahorse nozzle edge and receives one
  tiny local plum/aqua seam shadow. Only its tugging tail projects forward.

### Material and color

- Target props use two or three broad value bands. Reduce saturation and
  highlight density from the current generated cutouts by roughly 15-25%.
- Contours are deep plum/indigo at the room's screen weight. No white sticker
  rim, black halo, colored aura, glass handle, chrome, or jewel-lighting.
- Keep the pool aqua visible. Dirty water is a local grey-turquoise condition,
  not a full-canvas tint.

### Fixture authority

- The exact V4 waterfall and seahorse rest cards remain geometry, identity,
  pivot and placement authority. Do not use independently redrawn complete
  fixtures as overlay replacements.
- Clogging is confined to the existing waterfall flow/basin mask: broad muted
  olive-grey bands, fewer highlights, and uneven stagnant darkening at the
  basin contact.
- Seahorse grime is confined to sparse local stains/vine masks over the exact
  canonical card. Do not alter eye, face, snout, crest, curl, coral, pedestal
  or silhouette.

## Asset disposition

| Asset family | Decision |
|---|---|
| Approved room and V4 rest cards | Preserve and reuse as sole production authority |
| Current skimmer, basket and debris | Keep only until runtime modulation/scale/contact pass is captured; do not treat isolated renders as visual acceptance |
| New full-frame integration plate | Accepted reference only; never runtime or identity authority |
| New separable ImageGen attempts | Rejected; not copied into the repository |
| Approved Rumi atlas | Preserve unchanged; integrate only with non-destructive local water contact/caustic treatment |

## Acceptance capture

The next Mobile capture must prove all of the following in the actual
1280x720 composite:

- no global teal wash or multi-target ring field;
- one active action at a time;
- room-scale skimmer, debris and basket;
- local waterline/ripple contact;
- exact V4 fixture silhouettes with no duplicate edge;
- no halo/checkerboard/white fringe;
- center water remains open and Rumi remains the approved identity.

Per `DL-VIS-07`, owner acceptance in runtime remains the final gate.

## Implemented runtime evidence

The integrated 2026-08-23 runtime pass now satisfies this specification in the
exact Godot 4.7.1 Forward Mobile composite:

- the activity is mounted in the room's world/depth hierarchy;
- the global wash, abstract pool redraw, and broad target-ring field are gone;
- visible props are reduced and tinted while the forgiving hit geometry is
  unchanged;
- debris, skimmer, scrubber, mouth obstruction, and basket receive local
  contact staging rather than a shared modal halo;
- waterfall and seahorse replacements use the live V4 source bounds;
- the mouth obstruction uses measured nozzle/tip anchors and visibly enters
  the seahorse's mouth;
- nine captured states pass from dirty arrival through approved Rumi reveal.

Target-device, observed-child, voice, and owner acceptance remain external
gates and are not inferred from the desktop Mobile capture.

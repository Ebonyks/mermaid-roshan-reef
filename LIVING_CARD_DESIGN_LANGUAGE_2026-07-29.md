# Living Card design language — production baseline (2026-07-29)

This is the reusable game-art language established by the Sky Lagoon pilot.
It translates the useful parts of the Sky Lagoon v2/v3 proposals into rules
that fit the repository's actual architecture and current approved art.

## Structural contract

World art is an unshaded `Sprite3D` card at intentional scene depth. No world
character, creature, prop, foreground, midground, or background may be a
`Sprite2D`, `AnimatedSprite2D`, `TextureRect`, custom `CanvasItem`,
`MeshInstance3D`, particle system, model, GLB, or procedural mesh. HUD and
full-screen interface/story overlays remain exempt.

Every animated card records:

- `living_card = true`;
- `motion_class` and `intensity_class`;
- source aspect and measured opaque content-height fraction;
- target world height and touch footprint;
- a deterministic coordinate phase:
  `wrapf(pos.x * 0.73 + pos.z * 1.31, 0.0, TAU)`;
- a contact-shadow Sprite3D when the card is grounded.

The crop is the rig. Grounded source art uses a bottom-center root and keeps
that root visually pinned. Non-grounded ornaments declare their semantic
anchor, such as a chimney mouth.

## Two valid art lanes

1. Extraction lane: preserve the exact approved object pixels, remove them
   from a preserved master copy, heal only inside a declared mask, verify zero
   out-of-mask pixel changes, re-slice without scaling, and reinsert the
   original cutout at real depth.
2. Ornament lane: generate a genuinely new object that does not duplicate a
   painted silhouette. Smoke, a glint, or a drifting leaf can use this lane.

Never paste a second tree, flower bank, cabin, or prop over its painted copy.
If the source master/hash or approved extraction bounds do not match the
working master, stop that extraction rather than guessing.

## Motion hierarchy

- Ambient establishes weather and depth: restrained far-foliage sway, one
  clear-corridor cloud, thin chimney smoke.
- Reactive acknowledges Roshan only when an approved near-depth card already
  exists. It never moves collision or touch bounds.
- Authored staging owns the strongest timing: plane arrival, equipment play,
  castle invitation, and character-specific animation.

Each playable screen has at most one dominant moving landmark and three quiet
support loops. Multiple staggered cards forming one smoke column count as one
loop. Keep the walk lane and touch targets calm.

One bounded stage tick owns all ambient cards. It performs no random calls and
creates no per-frame collections. Stage wind uses a fixed schedule and an
integrated travel accumulator so gust transitions cannot teleport drifting
cards. Mutable state remains on `ReefMain.g` and is explicitly erased during
stage teardown.

## Mobile gates

- Texture longest side is at most 1024 pixels unless POT; generated
  ornaments are normally at most 256 pixels.
- Fix Alpha Border and mipmaps are enabled. NPOT textures use lossless
  compression mode.
- Per framing: at most eight cards individually covering over 10% of the
  screen and no more than 150% cumulative transparent-card coverage.
- Ambient tick cost stays below 1 ms/frame on the Speedy proxy.
- Day and night builds share card placement/phase signatures; backdrop and
  depth cards receive coordinated night tint.
- Build → exit → rebuild frees the old stage/card instances and clears wind,
  clock, distance, and card-list state.
- The stage probe records Day One and revisit inventories separately when a
  temporary arrival asset changes counts.

Capabilities are conditional, not decoration quotas. Do not add a sway shader,
reactive foliage, a second cloud, glints, or leaves merely to satisfy a list.
They ship only when a conforming extracted card and the screen budget justify
them.

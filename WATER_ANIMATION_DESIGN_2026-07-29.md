# Game-wide water animation

## Motion vocabulary

Every water surface uses one of two presets from `scripts/water_motion.gd`.

- `still`: slow single swell, weak counter-wave, quiet normal drift, small
  color breathing, and sparse sparkle. Use for sheltered ponds, fountains,
  baths, and painted Sprite3D water layers.
- `rough`: faster crossed swells, stronger normal drift, moving tint, crest
  highlights, and denser sparkle. Use for the ocean, fjords, rivers, moat, and
  exposed lake water.

Individual builders may override height or sparkle without creating a third
motion language. Existing water textures are reused; no generated art is
required.

## Runtime split

- Real water meshes animate in `toon_water.gdshader`. This keeps the recurring
  work on the GPU and does not rebuild meshes on the CPU.
- Water painted on an isolated Sprite3D layer gets a very small scale, lift,
  and rocking loop. Whole murals are not warped.
- Speedy mode disables depth-texture shoreline reads across every live water
  material. The waves, normal drift, and mesh-edge foam remain active.

## Jolt boundary

Jolt does not provide a fluid-surface solver. The water sheet therefore remains
visual and non-colliding; turning it into a rigid body would not make waves and
would spend the mobile physics budget continuously.

Jolt remains the right engine for the capped physical standee/garnish fleet in
`scripts/games/side_scroll.gd`: awake bodies receive the shared swell as solver
impulses, sleeping Sprite3D-style cards receive cosmetic sway without being
woken, and objectives stay analytic. This is the maximum useful Jolt scope for
water on the target tablet.

## Integrated surfaces

- Reef ocean ceiling
- Sky Lagoon pond, rivers, moat, and fairy pond
- Northern fjords and river
- Fetch-game Lake Michigan
- Butterfly World fairy fountain
- Fairy-flight pond card
- Pearl Castle pool layer and all isolated splash-item cards


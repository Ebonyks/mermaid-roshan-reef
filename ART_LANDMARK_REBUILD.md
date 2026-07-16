# Landmark Art Rebuild

_Audit and implementation date: 2026-07-15_

## Corrected scores

| Runtime family | Prior implementation | Corrected prior score | Replacement |
|---|---|---:|---|
| Sky Lagoon Dream Stars | Unicode `Label3D` glyphs with oversized OmniLights | 1/5 | Layered five-point 3D prisms, ink silhouette, pearl inset, five color details |
| Pearl Castle Crown Star | Billboarded Unicode glyph | 2/5 | Larger gold-and-pearl star with an authored crown silhouette |
| Star Chamber and tree stars | Font glyph decoration | 2/5 | Lightweight inked 3D star variants from the shared family |
| Butterfly Palace chandeliers | Font glyphs plus three OmniLights | 2/5 | Shared 3D star family; existing functional lights retained |
| Butterfly Gates | Marble torus with duplicate whole-butterfly cards in Sky Lagoon; unrelated generic GLB in Butterfly World | 1/5 | One shared butterfly-shaped portal with separate upper/lower wing geometry and subtle wing motion |
| Sky and play-circle clouds | One stretched sphere per cloud | 1/5 | Three clustered storybook profiles with painted cool undersides |
| Kart sleepy clouds | Three translucent spheres | 2/5 | Opaque lavender storybook cloud variant retaining the `z Z z` gameplay cue |

## Runtime coverage

`scripts/landmark_art.gd` is the sole constructor for the rebuilt landmark
families. It is used by `main.gd`, Sky Lagoon, Pearl Castle, Butterfly World,
and kart gameplay. The old `assets/portal/butterfly_gate.glb` runtime route and
whole-butterfly gate cards are retired, while the files remain available in
`backups/art_pre_landmarks_2026-07-15/`.

The geometry is texture-free, low-poly, opaque except for the portal film, and
uses no new OmniLights. This keeps the landmarks compatible with the Mobile
renderer and avoids transparent cloud overdraw.

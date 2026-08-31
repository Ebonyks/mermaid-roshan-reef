# Butterfly Gate castle-state correction provenance

This correction resolves the former asset-state mix-up without redesigning the
approved locations. License: project original and project-runtime derivative,
all rights reserved. URL: none.

## State authority

- `closed`: the existing minimal
  `assets/flats/castle/fairy_conservatory/moonflower_door_closed.png` remains
  the dormant castle relief. It has no hotspot and does not advertise the
  Fairy World before the Chapter 3 plot reveal.
- `revealed`: the wall transforms into
  `assets/flats/castle/fairy_conservatory/butterfly_gate_available.png`, and
  the one-finger hotspot and visual pointer appear.
- `open`: the same available Butterfly Gate remains visible after first entry.
  Entering the route does not replace it with a different architecture.

The plot reveal is therefore the dramatic visual beat: a restrained shell door
becomes the full stained-glass Butterfly Door Gate.

## Delivery-pixel composition

The available card is a deterministic composite built by
`tools/build_fairy_conservatory_gate_art.py`:

1. The exact approved
   `assets/flats/fairy_conservatory_handoff/butterfly_house.png` supplies the
   complete stained-glass Butterfly Gate facade. Its whole 1024-square card is
   translated down 43 pixels so its visible foot lands at `y=992`, exactly the
   dormant door's castle-floor foot. It is not resized, redrawn, or relit.
2. Only the old greenhouse corridor inside the clear central arch is removed.
   No other visible Butterfly Gate pixel changes.
3. A centered upright portrait crop of the approved
   `assets_src/fairy_conservatory_handoff_2026-08-30/masters/handoff_background_master_3640x2048.png`
   fills that aperture. The source sunrise horizon remains at 38.0% of the
   portal view, above the 50% maximum, with sky above and water below.
4. The approved whole cutout
   `assets/fairy/sprites/ornament_lily_cluster.png` is uniformly downsampled to
   a 176-pixel longest edge and placed with its foot exactly at the clear
   aperture threshold. This makes the Lily-Pad Fairy World legible through the
   narrow castle arch while preserving the approved source drawing.

The rainbow walkway is deliberately absent from the castle gate. It remains a
separate playable-stage asset in the Fairy Conservatory handoff and contributes
no delivery pixels here. The former Butterfly House greenhouse corridor also
contributes no delivery pixels inside the corrected aperture.

The runtime card and alpha master are 1024-square RGBA. The two Hall images in
`review/` are deterministic 1280x720 placement evidence over the accepted Main
Hall tiles; they are never runtime or replacement Hall pixels. Their distinct
centers/scales preserve the same `(1672, 620)` castle-floor foot while allowing
the plot-available gate's broad butterfly silhouette to reach the same visual
height as the narrow dormant relief.

## Image-generation exploration rejected

The built-in OpenAI image-generation tool was used in precise-object-edit mode
to test whether a new closed Butterfly Gate center was actually needed. Result
`exec-2da3ddc3-a417-4873-a1b0-078265c3a3ef.png` was rejected: it overdesigned
the dormant state, changed the approved gate architecture, added ornamental
complexity, and returned an RGB checker presentation rather than production
alpha. It was not copied into the repository and contributes no delivery
pixels. Exact reuse of the already-approved minimal shell door better satisfies
the requested before state and conserves the generation budget.

The hash-backed `asset_manifest.json` records every accepted source, runtime,
alpha-master, and review output.

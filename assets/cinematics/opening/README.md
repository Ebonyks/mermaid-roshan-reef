# Opening cinematic drop

Place the final Theora/Vorbis cinematic at:

`assets/cinematics/opening/daddy_roshan_flight.ogv`

It is Stage 1: Daddy Mermaid and Mermaid Roshan fly in the pearl plane to
their new kingdom. The runtime plays this file full-screen on the first launch.
While the edit is absent, it falls back to this exact native master:

`assets/flats/sky_lagoon/main/day_one_promenade_2048x1024.svg`

Delivery contract:

- OGV container, Theora video, Vorbis audio.
- 1280x720 or 1024x576, 30 fps.
- Keep protected family voice recordings in their original files; mix only
  owner-approved masters into the final edit.
- No 3D renders or 3D source assets.

The Stage 3 reveal uses the parallel drop location:

`assets/cinematics/dirty_castle/dirty_castle_reveal.ogv`

Its development fallback is this exact native master:

`assets/flats/dirty_castle/day_one_dirty_castle_2048x1024.svg`

Neither SVG is resized, padded, cropped, or rewritten after authoring. Their
SHA-256 hashes and runtime invariance checks are recorded in
`DAY_ONE_2D_RUNTIME_AUDIT_2026-07-26.md`.
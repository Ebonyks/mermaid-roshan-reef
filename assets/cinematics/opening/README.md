# Opening cinematic drop

Place the final Theora/Vorbis cinematic at:

`assets/cinematics/opening/daddy_roshan_flight.ogv`

It is Stage 1: Daddy Mermaid and Mermaid Roshan fly in the pearl plane to
their new kingdom. The runtime plays this file full-screen on the first launch.
While the edit is absent, the cinematic uses a neutral black fallback; it does
not stretch or crop a background plate.

Delivery contract:

- OGV container, Theora video, Vorbis audio, 30 fps.
- Keep the exact native aspect ratio and framing of the approved movie edit.
- Keep protected family voice recordings in their original files; mix only
  owner-approved masters into the final edit.
- No 3D renders or 3D source assets.

The Stage 2 world preserves its approved panorama separately. Its native
2172x724 master is preserved at `assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_3x1.png`, and
three lossless 724x724 runtime crops reconstruct it with adjacent unshaded
Sprite3D cards at one coherent depth.

The Stage 3 reveal uses the parallel drop location:

`assets/cinematics/dirty_castle/dirty_castle_reveal.ogv`

Its missing-edit fallback is also neutral black until a compliant approved-ratio
background master with a native long edge of at least 2048 exists.

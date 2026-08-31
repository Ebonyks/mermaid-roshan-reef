# Chapter 2 rainbow candle references

These are project-original OpenAI built-in ImageGen concept references created
for the birthday-party plot. No external or protected source image was used as
delivery pixels, and no existing project asset was modified.

The generation gap was a unique plot prop with two causally distinct states:
an unlit rainbow-wax candle for Detective discovery and party preparation, and
a dramatic party state with a single large, phone-readable rainbow flame.

## Preserved outputs

- `rainbow_candle_discovery_unlit_reference.png`
  - ImageGen result: `exec-139aff33-3311-4af7-9206-50f82f4cefd1`
  - SHA-256: `1b57f38425ba76b393b65804ab7b712794a58718a0d8a65f179dd3a8bccd0280`
  - Story role: the candle as Mermaid Roshan first discovers it in Chapter 2.
  - Human direction: accepted as the unlit discovery design.
- `rainbow_candle_large_flame_later_reference.png`
  - ImageGen result: `exec-13f66af4-6172-4963-b85f-744ada0b427f`
  - SHA-256: `688f36ea62a1a2ccb4bccc8e02e2ff42474f7d3aa5beb791b84654773547c3ea`
  - Story role: the party-only ignition beat made by Astronaut Roshan's little
    candle-lighting rocket. The preserved filename records the asset's original
    status before the owner's later Chapter 2 story direction promoted it.
  - Human direction: accepted as the large, legible lit-state design.

## Runtime status

Both native files are 1254×1254 opaque RGB images whose visible checkerboard is
baked into the pixels. The selected natives remain preserved under
`assets_src/`; the game never loads them directly. The accepted designs now
have deterministic 1024×1024 RGBA runtime derivatives:

- `assets/chapter2/birthday/rainbow_candle_unlit.png`
  - SHA-256: `bd1d4edd2b3e6d771c8fbdd83ea180db5efbafcaba996258d3f57dd8d1e0bd7f`
  - Alpha bounds: `(349,366)`–`(669,993)` on the 1024 canvas.
- `assets/chapter2/birthday/rainbow_candle_large_flame.png`
  - SHA-256: `2c00e80e57315283e2612fb301cc9e2ac0c519bab1e0bfa44b4ff3dc4b13ff68`
  - The checker-contaminated pale glow envelope is excluded while the large,
    saturated nested rainbow flame remains intact.

`tools/prepare_chapter2_birthday_art.py` removes only border-connected matte,
reconstructs the antialiased edge against the nearest interior colour, and
uniformly resizes the complete canvas in premultiplied-alpha space. It does not
crop, translate, repaint, relight, or composite the subject. The true-2D
`ChapterTwoRainbowCandle2D` loads the unlit state for Detective discovery and
all preparation scenes. Starting the fully prepared Main Hall party is the only
authored action that swaps to the large-flame state, using the Astronaut-built
rocket. The Ember King then takes the whole glowing candle because he wants it
for his own birthday party. Code-native drawing remains only a missing-resource
fail-safe and has no authority over the accepted art.

License: project original, all rights reserved. URL: none.

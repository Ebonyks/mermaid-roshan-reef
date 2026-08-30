# Chapter 2 rainbow candle references

These are project-original OpenAI built-in ImageGen concept references created
for the birthday-party plot. No external or protected source image was used as
delivery pixels, and no existing project asset was modified.

The generation gap was a unique plot prop with two causally distinct states:
an unlit rainbow-wax candle for Detective discovery, and a later dramatic lit
state with a single large, phone-readable rainbow flame.

## Preserved outputs

- `rainbow_candle_discovery_unlit_reference.png`
  - ImageGen result: `exec-139aff33-3311-4af7-9206-50f82f4cefd1`
  - SHA-256: `1b57f38425ba76b393b65804ab7b712794a58718a0d8a65f179dd3a8bccd0280`
  - Story role: the candle as Mermaid Roshan first discovers it in Chapter 2.
  - Human direction: accepted as the unlit discovery design.
- `rainbow_candle_large_flame_later_reference.png`
  - ImageGen result: `exec-13f66af4-6172-4963-b85f-744ada0b427f`
  - SHA-256: `688f36ea62a1a2ccb4bccc8e02e2ff42474f7d3aa5beb791b84654773547c3ea`
  - Story role: a later lighting beat with a much larger nested rainbow flame.
  - Human direction: accepted as valuable later-state art.

## Runtime status

Both native files are 1254×1254 opaque RGB images whose visible checkerboard is
baked into the pixels. They are therefore reference-only under `assets_src/`
and are never loaded by the game. The runtime prop is a true-2D code-native
`Control`. Chapter 2 always instantiates it unlit and exposes no lighting
action. The large nested rainbow-flame renderer and reference are retained only
for an explicitly authored future-chapter beat.

License: project original, all rights reserved. URL: none.

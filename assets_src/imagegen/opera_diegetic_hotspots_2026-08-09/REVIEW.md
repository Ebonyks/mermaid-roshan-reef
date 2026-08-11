# Magician rope hotspot review — 2026-08-09

Status: **Codex visual review accepted; owner/human review pending.**

Accepted attempt checks:

- one coherent rope and exactly two physically attached shell end caps;
- continuous braided topology with no duplicate strand or accidental limb;
- no crop, plate, UI frame, text, wand, character, shadow, or detached object;
- keyed alpha contains one connected component at alpha ≥16;
- native alpha bbox `(40,509)–(1215,714)` on 1254×1254;
- runtime alpha bbox `(16,22)–(496,106)` on 512×128;
- runtime margins left/top/right/bottom: `16/22/16/22` pixels;
- zero opaque green-spill pixels under the recorded QA heuristic;
- 3,189 antialiased runtime edge pixels and no distant alpha island;
- runtime texture is 512×128 POT and fully contained.

The accepted native did not achieve the prompt's requested 15% horizontal
green margin (39–40 pixels were delivered). This is recorded rather than
misrepresented. The complete object was nevertheless uncut, and the production
normalization creates a registered 512×128 canvas with explicit safe margins.

The first attempt is rejected: it baked a checkerboard into RGB pixels and
added detached purple droplets. It is retained only in the Codex generation
history and is not a delivery asset.


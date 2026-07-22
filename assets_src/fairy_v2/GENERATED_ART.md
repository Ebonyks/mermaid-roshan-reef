# Fairy Pond V2 generated art

The three V2 background concepts are retained as historical sources. Runtime
pond plates were superseded by the continuous V3 texture family on 2026-07-22;
the V2 bug, leaf-shield, and flower-growth masters remain current.

The final game art was generated with the built-in OpenAI image-generation
tool on 2026-07-16, then normalized by `tools/process_fairy_art_v2.py`.
Chroma-key removal uses the installed Codex `remove_chroma_key.py` helper with
a soft matte and despill pass. Pond plates live in `assets/fairy/`; transparent
relief-build masters live in the export-excluded
`assets_src/fairy_v2/runtime_textures/` and are embedded into the runtime GLBs.

All subjects use the project art contract: orthographic top-down camera,
rounded phone-readable silhouette, thin dark-indigo contour, two or three cel
value bands, high-key aqua/lavender light, no face, no text, and no copyrighted
symbols.  The isolated subjects were generated on solid `#FFFF00`; that color
is absent from the subjects themselves.

## Background prompts

- `background_dawn.png`: opening-third enchanted pond at lavender dawn; quiet
  pale-aqua central lane, mossy banks, broad lily pads, sparse ripple ribbons.
- `background_twilight.png`: middle-third firefly twilight pond; open blue-aqua
  lane, mint leaves and lavender reeds at the margins, small cream fireflies.
- `background_clearing.png`: moonlit boss clearing; unobstructed circular aqua
  stage, mint perimeter foliage, lavender ripple halos and sparse sparkles.

## Shadow-bug prompts

- `bug_jewel.png`: complete top-down jewel beetle, six legs, antennae, rounded
  indigo-violet shell and three rose magical markings.
- `bug_moth.png`: complete top-down moon moth, six legs, two broad intact wings,
  mint crescent markings, indigo/teal/violet palette.
- `bug_firefly.png`: complete top-down firefly, six legs, lavender wing covers,
  deep-teal body and a rose-pink lantern-tail marking.

## Leaf-shield prompt

- `boss_leaf.png`: one detached leaf matched directly to the final flower
  reference: sea-glass mint body, violet pointed tip, dark-indigo contour and
  restrained readable veins. Six rotated relief instances form the first boss
  phase without falling back to stock bushes.

## Fairy Flower sequence prompts

Each prompt used the immediately previous generated state as its design
reference so the contour language, mint leaves, violet tips, curled stem and
purple blossom identity remain continuous.

1. `boss_seed.png`: cracked plum-brown seed, curled mint shoot and first folded
   leaf tips.
2. `boss_sprout.png`: four-leaf mint rosette and tiny closed purple bud.
3. `boss_bud.png`: enlarged four-leaf rosette, inner leaf pair and broad closed
   purple bud.
4. `boss_opening.png`: half-open layered purple blossom with all leaves visible.
5. `boss_bloom.png`: giant fully open purple blossom with two petal rings and
   large mint leaves framing it.

The original generated files remain in the Codex generated-image store; these
project copies are the normalized, reproducible masters.

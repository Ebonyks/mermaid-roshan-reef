# Opera diegetic hotspot generation prompts — 2026-08-09

## Scope decision

The 52-phase inventory found reusable, approved transparent art for every
activity except Magician `ROPE`. The old trace card contains the correct rope
design, but no isolated rope cutout. No other semantic hotspot art was
generated.

Reference supplied to both attempts:

- `assets/opera/worlds/widgets/widget_trace_magician.png`
- SHA-256: `7999afc7ea691a47dbd8b7d175e1f902a6d21ed8947f30da548e7f1bea37d1cd`

## Attempt 1 — rejected

Result ID: `exec-21e14c4c-d66c-40be-9c12-c41133917125.png`

Prompt:

> Create one production-ready transparent PNG object cutout for the Mermaid
> Roshan Opera House magician room. Reference image 1 defines the exact
> approved object design and storybook rendering. Isolate and faithfully
> recreate ONLY the complete braided lavender magic rope with both
> gold-and-pearl scallop-shell end caps. Remove the entire UI card, pale panel,
> purple curtains, dark route line, oval badge, shadows from the card, and all
> background pixels. Keep the rope as one coherent gently curved horizontal
> object, with the same lavender braid, navy-purple ink outline, warm gold
> shell caps, pearly highlights, polished 2D storybook/cel-shaded finish, and
> child-readable silhouette. Transparent alpha background. Full object fully
> contained with at least 15% clear padding on every canvas edge. No crop, no
> cut ends, no detached fibers, no extra wand, no character, no text, no
> symbols, no plate, no frame, no floating fragments, no checkerboard baked
> into pixels. Center the rope horizontally on a square 1024 x 1024 canvas.
> Artifact QA priority: exactly two attached end caps; uninterrupted braided
> topology; no accidental limbs, seams, duplicate strands, opaque rectangle,
> or distant alpha islands.

Rejection: the result was RGB-only with a baked checkerboard and contained
detached purple droplets around the caps. It was not copied into the project.

## Attempt 2 — Codex visual acceptance; owner review pending

Result ID: `exec-53dd92c7-cbcc-4dbf-8543-2e7fbe72e365.png`

Prompt:

> Production asset regeneration, second attempt. Reference image 1 defines the
> exact approved Mermaid Roshan magician rope design and storybook rendering.
> Recreate ONLY one complete braided lavender magic rope with exactly two
> attached gold scallop-shell end caps. Make it a single connected,
> uninterrupted object silhouette in a gentle shallow horizontal curve.
> Preserve the lavender braid, navy-purple ink outline, warm gold caps, pearly
> highlights, polished 2D storybook/cel-shaded finish, and child-readable
> topology. IMPORTANT BACKGROUND CONTRACT: fill every background pixel with
> one perfectly uniform flat chroma green RGB #00FF00. Do not output
> transparency, checkerboard, gradient, texture, floor, shadow, glow, or
> scenery. The green must be clean for deterministic key removal. Full object
> fully contained with at least 15% green padding on every canvas edge. No
> crop, no cut end, no knots beyond the two attached end bindings, no separate
> beads, no purple droplets, no dust, no sparkles, no distant fragments, no
> wand, no character, no text, no symbol, no plate, no UI frame. Exactly one
> rope object and nothing else. Square 1024 x 1024 composition. Artifact QA
> priority: both end caps physically connected to rope; continuous braided
> topology; no duplicate strand; no accidental limb; no detached alpha island
> after keying.

Generation method: OpenAI built-in ImageGen with the approved trace card as an
image reference. The native generated canvas is 1254×1254; dimensions were not
silently represented as the requested 1024×1024.


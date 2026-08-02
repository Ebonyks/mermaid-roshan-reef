# Playground Swing 2D Sprite Provenance

Generated with OpenAI built-in image generation on 2026-07-28. The
owner-provided Mermaid Roshan front-view PNG was used only as a style
reference for line weight, cel-painted finish, palette, and child-friendly
proportions. Roshan was not included in either generated asset.

## `play_swing_frame.png`

Generation identifier: `call_4WADIrLM5MfXM1FidtLlHU51`

Prompt:

> Use case: stylized-concept
>
> Asset type: 2.5D mobile game sprite layer for a children's storybook
> playground
>
> Input images: Image 1 is a style reference only for line weight,
> cel-painted storybook finish, pastel aqua/lavender/coral palette, and
> child-friendly proportions; do not include the mermaid or copy her design.
>
> Primary request: create only the STATIC FRAME of a large child-sized
> playground swing set, with two sturdy A-frame side supports and one top
> crossbar. Omit every hanging rope, chain, and seat so a separate animated
> seat layer can be placed beneath the crossbar at runtime.
>
> Style/medium: polished hand-painted 2D sprite cutout, clean dark
> navy-purple outlines, soft cel shading, pastel toy-playset colors, matching
> the reference's storybook game art.
>
> Composition/framing: straight front view with a very slight elevated
> three-quarter readability, full frame visible, centered, symmetrical,
> generous padding. The crossbar must be level and the open space below it
> unobstructed.
>
> Scene/backdrop: perfectly flat solid #ff00ff chroma-key background for
> local background removal. The background must be one uniform color with no
> shadows, gradients, texture, reflections, floor plane, or lighting
> variation.
>
> Constraints: frame only; no ropes; no chains; no seats; no people; no
> mermaids; no background scenery; no cast shadow; crisp silhouette; no
> #ff00ff in the swing; no text; no logo; no watermark; no 3D render
> appearance.

## `play_swing_seat.png`

Generation identifier: `call_ynbmI2SIeEknlYqedOfa90gF`

Prompt:

> Use case: stylized-concept
>
> Asset type: separate animated 2.5D mobile game sprite layer for the
> children's storybook swing frame just created
>
> Input images: Image 1 is a style reference only for line weight,
> cel-painted storybook finish, pastel aqua/lavender/coral palette, and
> child-friendly proportions; do not include the mermaid or copy her design.
>
> Primary request: create only ONE hanging playground swing seat with exactly
> two long straight ropes attached to its left and right corners. Both ropes
> begin at the same top height and hang vertically to the seat. This is a
> separate moving layer that will rotate around its top attachment line at
> runtime.
>
> Style/medium: polished hand-painted 2D sprite cutout, clean dark
> navy-purple outlines, soft cel shading, pastel toy-playset colors, matching
> the companion frame and the reference's storybook game art.
>
> Composition/framing: straight front view, perfectly centered and
> symmetrical; rope tops near the top edge, seat near the lower third; entire
> ropes and seat visible; generous side padding. Keep the area between the
> ropes empty so a character sprite can sit there.
>
> Scene/backdrop: perfectly flat solid #ff00ff chroma-key background for
> local background removal. The background must be one uniform color with no
> shadows, gradients, texture, reflections, floor plane, or lighting
> variation.
>
> Constraints: exactly one seat and exactly two ropes; no support frame; no
> crossbar; no people; no mermaids; no hands; no scenery; no cast shadow;
> crisp silhouette; no #ff00ff in the swing; no text; no logo; no watermark;
> no 3D render appearance.

## Runtime processing

The magenta background was removed with the Codex image-generation helper
using a soft matte and a one-pixel edge contraction. The accepted cutouts
were tightly cropped and Lanczos-resampled to a maximum edge of 1024 pixels:
the frame is 1024×719 and the seat/rope layer is 554×1024.

# Chapter One picture-book design language

Status: `BINDING_DOMAIN` for the static picture book only. Owner direction, 2026-09-20. The [original Gemini prompt](ORIGINAL_GEMINI_BACKGROUND_PROMPT.txt) is preserved separately; the rules below make its placement constraints explicit. Later owner instructions govern conflicts. The game-wide cinematic delivery rules are unchanged.

## Layer scope

The Gemini prompt governs the blank stationery BACKGROUND and integrated border assets. Its clear writing surface is intentional. It does not prohibit the later book-composition layer from placing large existing story illustrations and Sniglet text in that area. Full-art pages have no stationery background at all. This layer distinction follows the user's explicit request for foreground story pictures alternating with full-art pages.

## Background rules

- **BK-BG-01 — Base:** watercolor blue environment, fine dotted perimeter, two low seafloor mounds. Preserve the base aspect ratio. All panels and both mounds remain consistently blue.
- **BK-BG-02 — Exact asset:** preserve each supplied asset's design, color, style and texture. Remove its solid rectangular background; do not redraw, stylize, recolor or generatively reinterpret the supplied object. Keep its alpha silhouette and original aspect ratio.
- **BK-BG-03 — Clear top:** integrated decorative assets must fit entirely in the bottom 15%: normalized top coordinate at least 0.85. Base-native perimeter bubbles remain base elements, not new scattered decorations.
- **BK-BG-04 — Central gap:** the space between left and right mound silhouettes receives no integrated asset, shadow or new ornament. The base wash remains visible there. The writing surface stays empty until the separate foreground page-composition step.
- **BK-BG-05 — Slopes only:** anchor assets exclusively on the left or right mound slope. Record which mound supports each asset; no floating items.
- **BK-BG-06 — Maximum size:** asset bounding width <= 0.12 * canvas width AND height <= 0.12 * canvas height, preserving aspect ratio. Measure before occlusion, not just the visible remainder. Both limits apply.
- **BK-BG-07 — Grounding:** cover the bottom 10% of the placed asset with the existing mound texture and add a low-opacity contact shadow. Use the mound's actual silhouette, not a generic rectangular cover. Shadows also stay out of the central gap and upper restricted zone.
- **BK-BG-08 — One object, one role:** do not repeat a foreground story prop in the border of that page. Select a motif variant without the duplicate. No second brush, paint cup group, character, tool or room thumbnail.
- **BK-BG-09 — Clarity:** native shells, coral, bubbles and mound edges must be crisp and clearly drawn, with high-contrast, vector-like precision in their outlines, clean gradients and crisp paper grain. This does not license changing a supplied asset's texture/style or filling the writing surface with high-detail scenery. No digital speckles, corrupted edges or transparency holes.
- **BK-BG-10 — Publication review:** preserve native originals; keep derivatives separately. Assess at intended print size and resolution. Existing 1060 x 1484 studies are not automatically publication-ready; no claim of compliance until placement, silhouette, grounding and visual checks pass.

## Page composition

- **BK-PG-01 — Rhythm:** blue vignette pages alternate purposefully with border-free full art. Adjacent setup pages are allowed; a run must serve the story, not a repeated template.
- **BK-PG-02 — Cuts:** isolate whole action groups and meaningful objects along authored contours. Preserve contact, faces, hands, tails, location and object identity. Do not use rounded screenshot rectangles as a substitute.
- **BK-PG-03 — Spreads:** story page 1 is recto. Compose pages 2-3, 14-15 and 34-35 as single canvases and divide once. Keep critical action out of the gutter; no duplicate subject from independently cropping each half.
- **BK-PG-04 — Text:** Sniglet; short navy text in quiet image space. No opaque full-width caption strips. Background decorations remain small; foreground story artwork remains large.
- **BK-PG-05 — Source-only narrative:** existing Grok and storyboard/handoff art; no whole-scene redraws. Targeted isolation/inpainting/outpainting remains allowed within owner limits. Missing action art is a gap, never permission to invent a scene.
- **BK-PG-06 — Story:** waterfall clears and turns rainbow. Two dust bunnies hold Baby Eagle. Preserve four-helper soap concealment, rainbow jump, collapse and landing order. No changed landing or omitted-action restoration.
- **BK-PG-07 — Distinct pages:** page 12 shows the obstruction; page 13 must show clearing. Never reuse page 12's source/crop or a cosmetic recrop as page 13's action. Current page 13 has an explicit source gap; pages 14-15 are the rainbow payoff.

## Current study status

The previous seven blue backgrounds are retained as design studies, not accepted implementations of this newly supplied specification. In particular, their generatively rendered props do not prove exact asset extraction, <=12% bounds, 10% mound occlusion or grounded shadow placement. Build future variants from the base plus exact supplied cutouts, with explicit bounds and masks. The art-room composition is the owner's relative quality reference, not a waiver of these constraints.

## Required evidence per composed background

Record base/source paths and SHA-256, canvas size, exact asset source and alpha extraction method, normalized pre-occlusion bounding box, left/right mound, mound-mask reference, occlusion fraction, shadow bounds/opacity, central-gap mask, foreground prop exclusions and human print-size review. No automatic pass from a filename or attractive preview. Original book/reference and protected game assets remain unchanged.

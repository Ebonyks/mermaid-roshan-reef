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
- **BK-PG-03 — Spreads:** the current book uses 7 x 5 inch landscape single pages, 32 story pages plus covers. Wide reveals occupy a single page. No image is split or independently recropped across a gutter. The former 40-page portrait spread assignments are superseded.
- **BK-PG-04 — Text:** Sniglet; short navy text in quiet image space. No opaque full-width caption strips. Background decorations remain small; foreground story artwork remains large.
- **BK-PG-05 — Source-only narrative:** existing Grok and storyboard/handoff art; no whole-scene redraws. Targeted isolation/inpainting/outpainting remains allowed within owner limits. Missing action art is a gap, never permission to invent a scene.
- **BK-PG-06 — Story:** waterfall clears and turns rainbow. Two dust bunnies hold Baby Eagle. Preserve four-helper soap concealment, rainbow jump, collapse and landing order. No changed landing or omitted-action restoration.
- **BK-PG-07 — Distinct pages:** in the landscape edition, page 11 narrates clearing against the obstruction source; page 12 shows the distinct rainbow payoff. The actual clearing-action illustration remains a declared gap. Do not invent an action frame or repeat the obstruction as a cosmetic second page.

## Current study status

The previous seven blue backgrounds are retained as design studies, not accepted implementations of this newly supplied specification. In particular, their generatively rendered props do not prove exact asset extraction, <=12% bounds, 10% mound occlusion or grounded shadow placement. Build future variants from the base plus exact supplied cutouts, with explicit bounds and masks. The art-room composition is the owner's relative quality reference, not a waiver of these constraints.

## Required evidence per composed background

Record base/source paths and SHA-256, canvas size, exact asset source and alpha extraction method, normalized pre-occlusion bounding box, left/right mound, mound-mask reference, occlusion fraction, shadow bounds/opacity, central-gap mask, foreground prop exclusions and human print-size review. No automatic pass from a filename or attractive preview. Original book/reference and protected game assets remain unchanged.

## Owner correction: exactly two image treatments

- **BK-PG-08 — Binary image treatment:** every delivered illustration is either full-art to the page/spread edges OR a genuine object/character silhouette with transparency outside its authored contour. No reduced scene rectangles, rounded rectangles, circles, torn-paper crops, soft scenic blobs or irregular room/floor fragments. There is no third vignette-panel category.
- **BK-PG-09 — Complete cutouts:** a sticker means an unboxed isolated figure, whole object, or connected action group, without an added white sticker stroke. Preserve natural holes and gaps. Never substitute a severed head/hand or partial environmental crop. A naturally rectangular object (paper, book, display) can retain its physical contour; its surrounding scene cannot.
- **BK-PG-10 — Foreground and background ownership:** each reduced page explicitly lists foreground cutouts, left mound assets, right mound assets, removed context and placement. The Gemini 85%/12%/10% restrictions apply to small background integrations, not large foreground story cutouts. Never repeat an object in both roles.
- **BK-PG-11 — Source previews:** raw scene frames may appear only in clearly separated, collapsed source-reference sections of the production plan. They are not proposed reduced-page artwork. A missing cutout remains a production job, not a displayed screenshot substitute.

The previous 40-page plan is preserved as superseded planning evidence. The current 32-page landscape manuscript and per-page assignments live in `landscape/book.json` and `landscape/PAGE_PLAN.md`.

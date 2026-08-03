# Pearl Castle Dream House 2D Repair — ImageGen Provenance

Date: 2026-08-02  
Generator: OpenAI built-in Codex ImageGen (default built-in mode)  
Use case: illustration-story / production game sprite sheets  
Accepted attempts: one accepted generation per sheet  
Runtime medium: transparent unshaded Sprite3D cards extracted from the alpha sheets  
Protected originals modified: no

## Reference roles

The doorway generation used the recent conversation-visible approved Castle portal and Castle room images as style/architecture references. The furnishing generation used the accepted doorway sheet as a style reference, the rejected Blender canopy-bed/dream-bed/settee renders only as identity-and-gameplay-purpose references, and the approved 2D dining-room reference as the visual-quality target. No reference pixel was composited into either generated sheet.

## Sheet 1 — physical doorway family

- Chroma master: `door_family_sheet_chroma.png`
- Native dimensions: 1536×1024
- SHA-256: `5f3afefea59b4dc399a077373ea443776f752422e31cff7776d1c7287e85142a`
- Alpha derivative: `door_family_sheet_alpha.png`
- Alpha SHA-256: `36c4b4176f5038e25217eee78b7a6ac1480a11fe22a11ab949ad61d5fccb349d`
- Post-processing: installed ImageGen `remove_chroma_key.py`; border auto-key, soft matte, thresholds 12/220, despill; no resize, redraw, warp, or interpolation.

Final prompt:

```text
Create one production asset sheet for Mermaid Roshan's Pearl Castle, using the recent supplied Castle images only as style and architecture references.

PURPOSE
Replace the current pasted-picture doorways for the Castle's Dream House Wing with a single coherent family of polished 2D storybook architectural door sprites.

STYLE
Complete flattened hand-painted 2D storybook illustration. Match the approved Castle rooms exactly: rounded pearl-and-shell architecture, lavender carved stone, warm cream pearl trim, restrained aqua and coral accents, warm gold light, crisp dark-purple illustrated outlines, gentle hand-painted texture, charming ornate child's castle. Absolutely no 3D render, Blender look, PBR, realistic material, plastic toy shading, vector-flat geometry, UI button styling, framed-picture appearance, text, letters, logos, watermarks, or characters.

SHEET CONTENT
Five separate front-facing full-height architectural door sprites, arranged cleanly on a uniform pure chroma-green background with generous empty spacing and no overlaps:
1. Family Wing entry: a slightly wider double-shell arch with a tiny house-and-pearl motif integrated as carved ornament.
2. Dining room: standard arch with plate, spoon, and fruit ornament.
3. Royal bedroom: standard arch with crescent moon, pearl, and small crown ornament.
4. Sleepover bedroom: standard arch with three stars and pillow ornament.
5. Movie lounge: standard arch with a tiny stage-curtain and play-triangle ornament.

DESIGN SYSTEM
All five must share exactly the same base arch construction, column height, sill height, lavender stone, ivory pearl moldings, gold edge accents, outline thickness, lighting direction, and scale. Only the carved crest and one restrained accent color may vary. Make each doorway read as architecture installed in a wall, never as a picture frame. Each should have a natural floor-contact plinth, deep open doorway center in dark indigo with only a soft atmospheric glow, and no pasted corridor picture. The opening itself must remain large and child-readable. No closed doors. No floating medallion bubbles. Ornament is carved into the keystone area.

LAYOUT
Orthographic/front elevation, no perspective tilt, no cut-off edges. Use the full sheet efficiently. Three doors in the top row, two centered in the bottom row. Identical baseline within each row. Uniform pure #00FF00 background only; no shadows or glow beyond each sprite silhouette. Preserve clear chroma gaps around every sprite for clean extraction.
```

## Sheet 2 — four-room furnishing family

- Chroma master: `furnishing_family_sheet_chroma.png`
- Native dimensions: 1254×1254
- SHA-256: `441c9528d45ea36925ac467a131815af62b7a3172aa0a6aec152f742422f96e9`
- Alpha derivative: `furnishing_family_sheet_alpha.png`
- Alpha SHA-256: `c188a7e07e04f71e401fc9337815b58fe817472a92b271440c4ab864ca12f631`
- Post-processing: installed ImageGen `remove_chroma_key.py`; border auto-key, soft matte, thresholds 12/220, despill; no resize, redraw, warp, or interpolation.

Final prompt:

```text
Create one production 2D sprite sheet for Mermaid Roshan's Pearl Castle. The recent images show: the newly accepted illustrated doorway family and the rejected low-detail 3D/Blender prop references plus an approved polished dining-room style reference. Preserve the useful identities and gameplay purpose of the referenced furnishings, but redraw every visible prop completely in the approved hand-painted 2D Castle style.

STYLE
Polished flattened 2D storybook illustration matching the approved dining-room image and doorway sheet: rounded pearl-and-shell forms, lavender, aqua, blush, cream pearl and restrained gold, crisp dark-purple illustrated outlines, soft painted texture, clear child-readable silhouettes, warm light painted consistently from upper left. Absolutely no Blender render, no 3D model appearance, no PBR, no realistic material, no plastic toy shading, no ray-traced shadows, no photorealism, no vector-flat geometry, no text, no labels, no logos, no watermarks, and no characters.

SHEET LAYOUT
Exactly a 4-column by 4-row grid on one uniform pure #00FF00 chroma-green background. No visible grid lines or cell boxes. Keep every prop entirely inside its cell with generous green separation and no overlaps, cropping, cast shadows beyond the silhouette, or glow spill. Use consistent three-quarter/front storybook camera angle and consistent scale within object families.

ROW 1 — DINING
1. Large round pearl-castle dining table, rich warm plum wood with shell-carved cream-and-gold pedestal, broad empty tabletop for runtime plates.
2. One low aqua round shell stool matching that table.
3. Teal pearl-and-shell provisions hutch with curved cream top, drawers, a few coral and pearl ornaments; single connected silhouette.
4. One empty child-size dinner place setting: pink scalloped plate, spoon and fork, simple connected arrangement.

ROW 2 — ROYAL BEDROOM
1. Ornate royal canopy bed: lavender frame, cream shell canopy, blush quilt, aqua pillows, pearl finials; cozy and unmistakably illustrated, not metallic.
2. Tall shell wardrobe: lavender body, cream shell doors, gold trim, pearl handles.
3. Small bedside table with a discreet glowing pearl lamp built into it; painted light contained within the object.
4. Plump story cushion shaped like an open shell with one small closed picture book resting on it; no writing.

ROW 3 — SLEEPOVER
1. Pink dream bed: low child bed with pink shell headboard, cream quilt, one star pillow.
2. Pearl dream bed: low child bed with ivory shell headboard, aqua quilt, moon pillow.
3. Purple dream bed: low child bed with lavender shell headboard, blush quilt, cloud pillow.
4. Hanging shell chandelier matching the approved dining-room chandelier, warm pearl light, compact complete silhouette.

ROW 4 — MOVIE LOUNGE
1. Cloud-shaped two-seat settee with cream cloud cushions, aqua seat, tiny pastel rainbow embroidery; broad horizontal silhouette.
2. Round cloud pouf with lavender base, pearl trim, aqua cushion.
3. Ornate freestanding movie-screen frame: lavender shell-and-pearl surround with dark empty indigo inner screen area, no image and no play icon.
4. Small shell popcorn bowl with a few large stylized popcorn pieces, child-readable and charming.

QUALITY
Every object must look authored by the same 2D illustrator as the approved Castle rooms. Avoid tiny noisy detail. Preserve the exact 4x4 order so each cell can be extracted deterministically.
```

## Extraction contract

`tools/build_castle_dream_house_rooms.py` crops only the recorded sheet regions. It uses the largest connected alpha component for furnishing cells except the intentionally disconnected plate/utensil cell. Runtime output is never enlarged, repainted, or sourced from Blender. The full accepted chroma and alpha sheets are preserved here.

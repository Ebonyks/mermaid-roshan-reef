# Opera stage completion prompts — 2026-08-02

Built-in Codex image generation was used. Transparent sprites were generated
against a flat chroma field, matted with the installed `remove_chroma_key.py`
helper, and normalized as complete flattened images.

## imp_captain_bow

### Attempts 1–2 — rejected

References: `assets/opera/worlds/actors/imp_captain_bow.png`,
`assets/opera/worlds/actors/imp_captain.png`, and (attempt 1 only)
`assets_src/concepts/opera_rivals_2026-07-29/authoritative_boxer_imp_reference.png`.

Prompt intent: faithful full-body repair of the existing theatrical bow;
preserve captain identity, plain gold waistband, purple shorts, striped horns,
amber eyes and friendly expression; remove the alpha hole through the shorts;
slim belly/forearms about 10%; flat `#00ff00` removable field; prohibit 3D,
glossy-plastic rendering, costume additions, marine motifs, text and shadows.

Attempt 1 generation id: `exec-13bb99eb-c9a8-4a24-9039-d016baf95383`.
Rejected for glossy/inflated 3D-cartoon style, face drift and proportion drift.

Attempt 2 generation id: `exec-4ed2e97f-ed76-430e-ab0d-e5ab97b60920`.
Rejected because the wide extended arm could not retain both the required
480–490 px height and the required edge margin on a 512×512 canvas.

### Attempt 3 — candidate

References: `assets/opera/worlds/actors/imp_captain_bow.png` (dominant
appearance/pose/style lock) and `assets/opera/worlds/actors/imp_captain.png`
(secondary proportion lock).

Prompt: faithfully redraw the existing bow in the same flat hand-painted 2D
storybook style and character identity; repair the shorts hole; compress the
gesture by bending the extended arm so the full silhouette fits the tall
square framing; subtly slim belly and forearms; preserve face, horns, anatomy,
plain waistband-only costume, palette, brushwork and delicate navy-purple
outlines; complete figure with feet on one baseline and clear margins; one
connected component with no solid-material holes; perfectly uniform flat
`#00ff00` field; no 3D, glossy plastic, thick sticker outline, new mascot face,
marine motifs, text, logos or shadows.

Generation id: `exec-6c2c536a-bd1a-45ca-8d77-6ec0f3dac24a`.

## fx_dizzy_stars

Prompt: exactly three small brushed-gold five-point dizzy stars distributed
around one thin incomplete swirl ring; flat polished 2D storybook cel art,
delicate deep-purple contour and restrained cream-gold highlights; center 45%
empty; readable at 64 px; perfectly uniform flat `#00ff00` removable field;
no character, face, additional sparkles, marine motifs, text, logo or shadow.

Generation id: `exec-eabf8730-af36-4679-a51e-e37823765b8c`.

# UI Prototype Prompt Record - 2026-07-19

Generator: OpenAI built-in image generation/editing tool. No deterministic seed
or model build identifier was exposed, so neither is claimed. Prompts below are
the final request specs used for the retained files.

## `hud_navigation_v1_raw.png`

Use case: `precise-object-edit`.

Edit the current successful reef runtime capture into a practical, shippable,
touch-first exploration HUD for a non-reading four-year-old. Preserve the world,
camera, characters, props, lighting, and composition. Replace only the UI with:
a top-left shell status tray for pearl count, five friend pips, and five trophy
pips; a top-center picture-objective card plus broad golden helping-current
chevron; one isolated 112 px pause control top-right; a high-visibility 150 px
mint-rim joystick bottom-left; and a 148 px warm-coral pictogram action button
bottom-right. Keep the play center clear. Use rounded storybook panels,
navy-purple outlines, aqua/lavender shadows, and warm colors only for touch
targets. No instructional text, labels, map, health bar, tiny icons, overlaps,
watermark, or character redesign.

## `pause_overlay_v1_raw.png`

Use case: `precise-object-edit`.

Add only a pause overlay to the selected HUD prototype. Keep the world and HUD
unchanged under a cool translucent dim. Center a large open-clam storybook panel.
Make a huge mint resume button with play triangle and wave the dominant choice.
Below, use a 2x2 grid of at least 132 px icon tiles: sticker book, neutral open
door back to reef, music toggle, and sparkle/speedy quality toggle. Use shape,
position, outlines, and toggle tracks rather than color alone. No small close,
FPS, developer button, alarming red, loss language, confirmation, text sentence,
watermark, or extra character.

## `craft_studio_v1_raw.png`

Use case: `ui-mockup`.

Create a polished 16:9 touch-first craft studio using the pause prototype as the
interface-style reference and the current round fish line art as the creature
identity reference. Top: pearl count plus exactly three 120 px creature tabs for
fish, cat, and bird. Center-left: one large preview. Right: three 120 px part
selectors using body/fin/accent mini-diagrams. Bottom: one row of eight 110 px
color swatches plus one rainbow swatch. Bottom-right: a 150 px mint fish-swim-away
finish control. Top-right: 112 px neutral back. Selected state uses thick outline
and badge. No protected portraits, sentences, color names, prices, tiny swatches,
dense grid, confirmation, watermark, or logo.

## `craft_studio_v2_raw.png`

Use case: `precise-object-edit`.

Change only the large preview fish's editable fills: body becomes the selected
soft sky-blue and fins/tail become warm coral-pink. Preserve line art, eye, mouth,
silhouette, and every interface element, panel, icon, selection outline, swatch,
lock, background, position, spacing, and crop. No new elements or text.

## `intro_story_v1_raw.png`

Use case: `ui-mockup`.

Create a polished 16:9 picture-first, voice-first story intro using the pause
prototype as interface-style reference. Center a large pop-up storybook frame
with abstract paper-cut placeholders only: one crowned sky-princess silhouette
and one small mermaid-friend silhouette connected by a broad golden helping
current. Top-center: exactly four large shell progress pips with the third active.
Bottom-left: 120 px star/speaker medallion with three voice waves. Bottom-center:
a visually secondary empty caption ribbon. Bottom-right: at least 150 px gold
open-hand/next-shell button. Top-left: quiet 112 px hold-to-skip closed-book icon
with progress ring. No protected likenesses, speech bubbles, sentences, labels,
numerals, tiny hint, hidden edge control, watermark, or extra character.

## Post-processing

Raw outputs were copied into this directory and normalized to 1024x576 with
PowerShell `System.Drawing` high-quality bicubic resampling. No content-aware
post-processing, paint-over, alpha removal, or protected-source modification was
performed.

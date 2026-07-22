# UI Prototype Revisions - 2026-07-19

Status: E1 review-only interface prototypes on `codex/ui-prototype-revisions`.
These files are design evidence for review and later Fable 5 co-construction. They
are not runtime textures, do not change Godot behavior, and must not be promoted
as finished UI without the implementation and device gates below.

## Purpose

Apply the same audit-first, image-prototype-first workflow used by the preceding
Codex art batch to the user interface. The pilot deliberately covers four
representative states before any broad rewrite:

1. exploration HUD and touch controls;
2. pause and neutral activity exit;
3. craft-studio selection and preview feedback;
4. picture-first, voice-first intro progression.

The intended player remains one non-reading four-year-old using one finger on an
older Android phone. Text may remain as a parent-facing backup, but no required
action or objective may depend on it.

## Authority and evidence used

- `AGENTS.md`
- `DESIGN_3_0.md`
- `GAME_AUDIT_v3_49.md`
- `AUDIT_UPGRADE.md`, especially phases U1 and U3
- `ART_STYLE_GUIDE.md`, especially palette, focus, Mobile readability, and
  touch-target rules
- current implementations in `scripts/main.gd`, `scripts/touch_ui.gd`,
  `scripts/intro_overlay.gd`, `scripts/pause_menu.gd`,
  `scripts/wardrobe_ui.gd`, and `scripts/craft_studio.gd`
- successful dev capture artifact `reef-first-world-review` from GitHub Actions
  run `29674202837`, inspected locally but not committed

The reference capture exposed these concrete problems:

- objective text and top-right controls compete for the same space;
- pause and action controls read as an undifferentiated top-right cluster;
- the joystick is too faint to explain itself at phone scale;
- progress is a long text line rather than a quickly scannable shape system;
- the intro's story sentence is the primary explanation;
- pause buttons are 96 px high despite the 110 px interaction contract;
- craft swatches are 84 px and all three color rows are exposed at once;
- craft and wardrobe rely heavily on labels, lock messages, and `Done!` text.

## Shared interaction grammar

All four prototypes use the same rules:

- **Fixed ownership:** progress top-left, current objective top-center, pause or
  back top-right, movement bottom-left, and primary action bottom-right.
- **One obvious next action:** a warm or mint primary control is larger than all
  secondary controls and isolated from them.
- **At least 110 px:** every required touch target has a minimum 110x110 visual
  target or a larger invisible hit envelope. The preferred primary action is
  148-160 px.
- **Voice + motion + icon:** required objectives use narration, a moving sparkle
  current or pulse, and a large object pictogram. Text is optional backup.
- **Never color alone:** selected, locked, complete, and toggle states also use
  outline weight, position, shape, badges, or motion.
- **Cool field, warm focus:** aqua/lavender occupies most of the interface;
  coral, mint, and gold identify actions and rewards.
- **Neutral exits:** leaving an activity uses an open doorway back to the reef,
  not a red X, warning, loss label, or confirmation trap.
- **No edge collisions:** touch controls own safe corner zones; objective cards,
  speech portraits, and captions cannot enter those zones.
- **Immediate response:** accepted input should visibly depress, pulse, or update
  within two rendered frames at the 30 fps target.

## Selected review set

| State | Review image | SHA-256 | Review verdict |
|---|---|---|---|
| Exploration HUD | `ui_prototypes_2026-07-19/hud_navigation_v1_1024x576.png` | `07CD6EF48F5190BE47931648231881BC4970AB039FFE3BD725D4044C3E0FCEB5` | Selected direction. Corner ownership, picture objective, strong joystick, and separated action/pause controls solve the observed overlap. Status tray may shrink after phone testing. |
| Pause overlay | `ui_prototypes_2026-07-19/pause_overlay_v1_1024x576.png` | `3EFBCA58EF42B8AE8170F67661A688F6BE04704B74E45804BB51CC99980E42BB` | Selected direction. Resume is unmistakably dominant; sticker book, neutral exit, sound, and quality form a consistent icon grid. |
| Craft studio | `ui_prototypes_2026-07-19/craft_studio_v2_1024x576.png` | `45F34D6FD9AEBB56927063474E5FC54DA9256EFF72B621B3036578B85FF8AC93` | Selected v2. Large preview, one active color row, part silhouettes, and visible applied selection replace the dense 27-swatch/text layout. |
| Story intro | `ui_prototypes_2026-07-19/intro_story_v1_1024x576.png` | `0F07505C770E8E7CBADA4364AA3999D30127D65C69F0FD48D5651F70FD7D47A2` | Selected layout direction. Story picture and narration state dominate; page progress and next action require no reading. Character silhouettes are placeholders only. |

The 1024x576 files are the review set. Their 1672x941 `*_raw.png` siblings are
retained as generation provenance and remain under the existing `gen2/.gdignore`
boundary.

## Iteration record

`craft_studio_v1_1024x576.png` is retained as a rejected intermediate. It selected
the blue swatch and the body part, but the large preview fish remained white.
That violates immediate, legible input feedback. The v2 edit changed only the
preview state: blue body and coral fins now agree with the selected controls.

This is the intended iteration pattern for later screens: identify one observable
failure, change one thing, and preserve the rest of the layout for comparison.

## Runtime layout contracts

These measurements are implementation targets at the 1280x720 base canvas, not
measurements claimed from the generated rasters.

### Exploration HUD

- Top-left status tray: approximately 250x180, with 48-56 px object icons and
  chunky 32-40 px progress pips. Keep all prose out of this tray.
- Top-center objective card: approximately 250x160. It shows the current target
  object or character icon and a downward/in-world direction cue. Narration fires
  when the target changes; the card pulses once, then settles.
- Pause: 112x112 visual target with at least 128x128 hit envelope, inset from the
  top-right safe edge.
- Joystick: approximately 180 px visual diameter with at least 220 px touch
  envelope; 40-55% fill opacity and a high-contrast mint rim.
- Primary action: 148-160 px visual diameter with at least 176 px hit envelope.
- Hide objective cards after comprehension, but keep the in-world moving helping
  current. A repeat-hint pulse may restore the card without adding prose.

### Pause overlay

- Full-screen cool dim; gameplay freezes but music continues under the existing
  calmer-pause rule.
- Center panel remains inside a 48 px safe margin.
- Resume is the first focus target and at least 300x140.
- Secondary icon tiles are at least 150x132 with 24 px separation.
- Leave Activity appears only in a valid activity context and always returns
  neutrally without granting or removing progress.
- Sound and quality states use a toggle track plus different silhouettes, not
  only a color change.
- FPS and developer controls remain dev-mode-only and outside the child menu.

### Craft studio

- Creature tabs are at least 120x120 and use recognizable silhouettes.
- The preview occupies at least 40% of the canvas and updates within two frames.
- Show exactly one active palette row. Body/fin/accent selectors are at least
  120 px tall and use highlighted mini-diagrams of the same creature.
- Swatches are at least 110x110 including spacing. Pattern marks supplement hue
  for recognition.
- Locked creature tabs show a lock shape and pearl cluster. A voice line explains
  the unlock; price prose is optional parent backup and never blocks navigation.
- Finish is a 160 px-class action with a swim-away pictogram. Completion keeps
  the existing chime, voice, animation, and save behavior.

### Story intro

- Story art remains the primary field; protected character images are inserted
  unchanged at implementation time. The generated silhouettes are layout
  placeholders and must never replace protected art.
- Four large shell pips show position in the sequence.
- Narration begins automatically on every page and has a 120 px-class visible
  speaker/wave indicator.
- Next is at least 150 px and advances only once per press/release.
- Skip is a quiet 112 px book icon with a hold ring (recommended hold: 1.2 s) to
  avoid accidental whole-story skips.
- The caption ribbon is optional parent-facing backup. The player never needs to
  read it to continue.

## Evidence and promotion boundary

- Current evidence class: E1 design proposal.
- Maximum supportable score from these rasters alone: 2/5.
- Runtime pass: not attempted and not claimable.
- Godot scene/script changes: none.
- Protected source files changed: none.
- Mobile renderer capture of implemented UI: none.
- Touch latency, hit geometry, focus traversal, scaling, clipping, contrast on
  device, and screen-reader/accessibility semantics: unproven.
- The background used for HUD/pause comparison came from project-authored runtime
  capture evidence. It is not a new runtime asset.

## Required implementation sequence

1. Owner/Fable 5 review selects or revises the shared grammar.
2. Implement one gold slice only: exploration HUD -> pause -> resume.
3. Add deterministic UI probes for target minimum size, corner-zone overlap,
   focus order, and no required-text-only objective.
4. Run parser and inference lint on changed scripts, then `scripts/ci.sh`.
5. Capture 1280x720 Mobile states: exploration, objective change, speech,
   pause, resume, and activity exit.
6. Review at actual phone scale and measure visible response within two frames.
7. Apply the proven components to intro, craft, wardrobe, sticker book, and
   minigames one screen family at a time.

Do not use the generated pictures as flat runtime overlays. Rebuild the selected
layout from Godot `Control` nodes, shared theme resources, real icons, real state,
and the untouched protected character art.

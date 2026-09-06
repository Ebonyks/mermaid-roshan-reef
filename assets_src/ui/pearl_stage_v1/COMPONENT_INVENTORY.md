# Pearl Stage v1 — reusable UI component inventory

Status: bounded design and implementation inventory, 2026-09-05. This file is
an evidence-backed map for a future Godot-native UI pass. It does not approve
any generated raster as a runtime overlay, select a font, or change runtime
code. The desired direction is a polished painted shell/pearl/rainbow stage:
quiet actionable centers, rich but grouped perimeter dressing, broad contours,
and one-finger choices that remain obvious at phone size.

## Authority and guardrails

The product contract is the non-reader, one-finger, voice/picture-first game in
`AGENTS.md`, `SECURITY.md`, and `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`.
The clauses that directly constrain this inventory are:

- `DL-AGE-01..07`: every required route has voice plus a picture/diegetic cue,
  one finger, no punitive fail state, and an immediate visible response.
- `DL-VIS-01..06`: rounded, slightly asymmetric silhouettes; 2–4 px deep
  indigo/plum contours; high-key values; aqua/lavender shadows; warm rainbow
  accents kept intentional; protected character identity stays authoritative.
- `DL-READ-01..06`: one focal action, quiet play center, object readability with
  HUD at phone size, and a pointer attached to the live target.
- `DL-UI-01..07`: touch-the-world is primary, every required target is at least
  110x110 base-canvas pixels (or has an equivalent generous hit region), one
  touch owns its route, visible pressed/focus states, and one neutral way back.
- `DL-TYPE-01..12`: all text goes through explicit named roles; child-facing
  text is at least 28 px at 1280x720; critical symbols need authored pictograms
  or proven font coverage; longest-string and 130% expansion/device evidence
  remain required. `StorybookUI` currently records the font authority as
  `UNRESOLVED` and fallback authority as `MISSING`.

The 2026-07-19 gen2 UI rasters remain review evidence only. The selected
direction and contracts are documented in
`gen2/UI_PROTOTYPE_REVISIONS_2026-07-19.md`; its 1024x576 images are not
runtime textures and do not prove target-size comprehension, touch latency,
or Mobile/device acceptance.

## Existing reusable runtime pieces

| Existing owner | What is reusable now | Current facts and boundaries | Pearl Stage v1 treatment |
| --- | --- | --- | --- |
| `scripts/storybook_ui.gd` (`StorybookUI`) | The shared canvas stage, palette constants, panel/HUD panel, shell crest, pearl, panel adornment, semantic button, picture button, icon button, neutral back button, labels/HUD labels, selection, and dim overlay. | Fixed `CANVAS_SIZE` is 1280x720; `MIN_TOUCH` is 110x110. `panel_style()` supplies rounded corners, violet contour, aqua/lavender/paper fills, and restrained shadow. `style_button()` and `style_picture_button()` provide normal/hover/pressed/hover-pressed/focus/disabled boxes and named typography. `adorn_panel()` adds one `ShellOrnament` plus four pearl dots. | Canonical token source. Extend through shared helpers only after owner/runtime review. Keep the quiet center and group shell/pearls at the perimeter; do not stack adornment over faces or target art. |
| `scripts/shell_ornament.gd` (`ShellOrnament`) | A scale-safe, input-ignored scallop fan crest drawn on a `Control`. | Runtime vector-style draw: 6 ribs, 6 highlight lobes, central outline/pearl; `mouse_filter = IGNORE`; colors are lavender, pearl, deep purple. | Reuse as the stage crest, title medallion, and edge flourish. It is a native decorative component, not a generated flat panel. Keep count restrained. |
| `scripts/pause_menu.gd` (`PauseMenu`) | Universal navigation layer, cool dim, large resume action, secondary icon grid, neutral activity exit, pause/focus cancellation, and save-safe state refresh. | Upper-left `GlobalNavigationButton` is a 112x112 back/menu control. Pause shell is `Rect2(290,25,700,670)` with 62 px radius. Resume is 580x140; secondary tiles are 280x132 with 24 px gap. FPS is present in code but is developer-facing text and must stay outside the child surface. | Strong structural reference for `PearlStageShell`, `PearlResumeTile`, `PearlNavDoor`, and toggle semantics. Replace ad-hoc text/icon combinations only through scoped runtime work; preserve neutral exit and pause cancellation. |
| `scripts/navigation_controller.gd` (`NavigationController`) | Stack ownership, root/route push/pop, invalid-route pruning, and synchronization of the global corner control. | `sync_button()` delegates to `StorybookUI.style_icon_button()` and switches `☰`/`↩` by route; lock checks live in `PauseMenu`. | Keep route ownership separate from visual styling. Proposed nav component only renders state supplied by this controller. |
| `scripts/touch_ui.gd` (`TouchUI`) | One-touch ownership, virtual stick fallback, action/jump/drag routing, cancellation, and a visual teaching hint. | The visible stick is a fallback, not primary curriculum. Hint/base/knob use shell and mint styling; input has explicit touch indices and cancellation. | Reuse behavior unchanged. A future `PearlStickHint` can wrap the existing hint/ornament while preserving the hidden-unless-needed rule and generous hit envelope. |
| `scripts/encounter_gesture_guide_2d.gd` (`EncounterGestureGuide2D`) | Noninteractive hand, tap/hold chip, halo, press ring, and charge arc demonstration anchored to a live target. | Loads `assets/castle/training/ghost_hand.png`, `verb_chip_tap.png`, and `verb_chip_hold.png`; redraw is 30 fps on Speedy and 60 fps otherwise; ignores input. | Reuse as the behavior of `PearlPointer`/`PearlGestureCue`; keep the hand/chip as picture support, never as required text. Do not redraw a generic corner pointer. |
| `scripts/intro_overlay.gd` (`IntroOverlay`) | Four shell progress pips, protected story art slots, adult-caption backup, repeat-speaker control, next shell, and deliberate 1.2 s hold-to-skip. | Uses `StorybookUI.add_stage/add_panel/adorn_panel`; speaker is 132x132, next is 164x164, skip is 112x112. Caption uses `ROLE_ADULT_CAPTION` at 22 px and is explicitly redundant. | Reuse `PearlProgressRail`, `PearlSpeechCue`, `PearlNextShell`, and `PearlHoldBook` contracts. Preserve the protected art slots and hold-to-skip behavior. |
| `scripts/craft_studio.gd` (`CraftStudio`) | Picture-first creature tabs, large preview panel, part selectors, palette/rainbow swatch, selected/locked state and finish action. | Current implementation still exposes text in 24 px locked cards/status; swatches are individually styled and selected by an 8 px gold border. | Strong consumer for `PearlPictureCard`, `PearlSelectionSeal`, `PearlPaletteRow`, and `PearlFinishTile`. The typography/lock semantics need a bounded follow-up; no new art is implied here. |
| `scripts/wardrobe_ui.gd` (`WardrobeUI`) | Wardrobe preview, picture-backed skin cards, lock/selected refresh, finish action, sticker book shell, and feedback burst. | Uses 28 px child-control role on picture buttons but also embeds lock/check labels. Locked fairy state is dimmed and text-backed. | Reuse shell/card/selection components, then replace critical state dependence with authored lock/check pictograms and voice while retaining labels as supplemental adult backup. |
| `scripts/castle_career_routes.gd` (`CastleCareerRoutes`) | Room-distributed Opera entrance card rail with actor, crest, pearl completion mark, focus/highlight and route mapping. | Card is 154x154 with 22 px gap at y=18; actor `TextureRect` is 112x112; crest is 50x50; completion pearl is 28x28. The room mapping is authoritative for current 13-career routing. | Reuse `PearlPictureCard` and `PearlCompletionPearl` with the same route metadata. Do not make a generic three-floor picker or expose retired Opera routes. |
| `scripts/opera_house_venue_2d.gd` (`OperaHouseVenue2D`) | Canvas Opera portal hit regions, chapter-two guide hand, floor glow, actor and career buttons. | Portal buttons are transparent 54-radius hit regions tied to painted doors; chapter-two guide uses the training ghost hand and points at the live guide button. | Treat as a world-owned `PearlDoorTarget`; its visual belongs to the painted room/door. A shell UI card must not float over or duplicate the door. |
| `scripts/opera_performance_overlay.gd` (`OperaPerformanceOverlay`) | Passive top status, progress/result panel, career accent mapping, token delta/balance labels. | Top rect is 500x126 at y=16; result rect is 600x220. It already uses `UI.panel_style()` and numeric/status role helpers. It is not an input surface. | Reuse `PearlProgressRail`, `PearlResultSeal`, and `PearlNumericBadge`; retain passive status and never make result text the only reward cue. |
| `scripts/opera_teacher_surface.gd` (`OperaTeacherSurface`) | Picture lesson board, counted tokens/numerals, large choice regions, help restart target, one touch owner, kind wrong-answer guidance, restore/checkpoint. | Board is `Rect2(330,105,850,555)`; choice rects are 174–210x170; hint/join/count anchors are explicit; numerals use `ROLE_NUMERIC`. | Reuse `PearlLessonBoard`, `PearlChoiceCard`, `PearlCountToken`, and `PearlGestureCue`. Keep answer geometry and save snapshot logic in the owner. |

Other broad consumers already delegate to the same system: `start_menu.gd`,
`collection_system.gd`, `companion.gd`, `attack_customizer.gd`, `mic_input.gd`,
`games/picture_games.gd`, `games/dance_engine.gd`, `boss_splash_2d.gd`, and
the castle room builders. Their local layout and state remain owners; the
component layer should reduce style drift without moving mutable state.

## Existing visual/reference inventory

These are reuse candidates or continuity references, with their current role
and evidence class. They are not a license to paste a concept into runtime.

| Asset family | Current path | Evidence and proposed use |
| --- | --- | --- |
| Castle room picture buttons | `assets/ui/castle_room_buttons_v2/room_*.png` plus `elevator_picture_icon_manifest.json` | Existing room chooser picture cards for Main Hall, Opera Hall, Kitchen, Library, Playroom, Craft Room, Mermaid Pool, Bubble Bath, Dining Room, Royal Bedroom, Sleepover Bedroom, and Movie Lounge. Reuse as picture identity inside a card; preserve their provenance and manifest. |
| Opera UI anchors | `assets/opera/worlds/ui/task_card_frame.png`, `station_marker.png`, `magnifier.png` | Accepted Opera UI assets from the 2026-08-02 QA ledger; task frame is 1024x1024 with a 200 px nine-patch margin, station marker 512x1024 with icon window metadata, magnifier 512x512 with centered 45° pivot. Good material/shape references for card frame, wayfinding marker, and pointer lens. |
| Opera career crests | `assets/opera/worlds/ui/crests/` | Existing 2D crests for live careers plus historical/cut entries. `CastleCareerRoutes` maps the live 13-career set and teacher/geologist special paths. Reuse only live route identities; retired dragon/phantom/maestro are not route authority. |
| Opera widget family | `assets/opera/worlds/widgets/` | Runtime 2D widget layers: track, trace, target, push, pour, lanes, gauge, crank, charge, catch, basin, clue board and magic-vanish variants, including mover/lit/progress/success states. The 2026-08-02 QA records 154 runtime widget files and accepted transparent mover/shared layers. Reuse as in-activity object art, not as shell chrome. |
| Opera source concepts | `assets_src/concepts/opera_regeneration_2026-08-01/cards/` and its ledgers/contact sheets | Accepted 2048x2048 world/stage masters and 1254x1254 career/prop concept cards are continuity inputs. `OPERA_CODEX_QA_2026-08-02.md` records 27 masters at 2048 and 104 runtime 1024 slices. Use for material/lighting continuity only; generated concepts are not UI delivery pixels. |
| Gesture teaching art | `assets/castle/training/ghost_hand.png`, `verb_chip_tap.png`, `verb_chip_hold.png` | Existing project-owned training art consumed by `EncounterGestureGuide2D` and Opera portal guidance. Reuse for live-target cueing and hold/tap teaching. Keep labels supplemental. |
| Rainbow/shell accents | `assets/mg/rainbow_swatch.png`, `assets/props/gen2/spiralshell_Image_0_flat.png`, `smallfanshell_Image_0_flat.png`, `fanshell_Image_0_flat.png`, and `assets/flats/castle/main_hall_2screen/castle_shell_sconce_*.png` | Existing licensed project-owned shell/rainbow references. They can inform pearl/rainbow accent tokens or a separated decoration card. Do not use a world fixture as an unexplained UI sticker or alter protected originals. |
| Gen2 UI prototypes | `gen2/ui_prototypes_2026-07-19/*_1024x576.png` and raw siblings | Selected review directions: `hud_navigation_v1`, `pause_overlay_v1`, `craft_studio_v2`, `intro_story_v1`; the earlier craft v1 is rejected for stale preview feedback. Review-only, no runtime texture authority. |

### Sol pause visual anchor (review-only)

Sol's first Pearl Stage concept is now staged at
`assets_src/ui/pearl_stage_v1/concepts/pause_menu_pearl_stage_concept_v1.png`.
It is a visual direction anchor only; it is not a runtime panel, a measured
target-size proof, or a replacement for the Godot-native implementation. The
observed component map is:

- one dominant centered scallop resume medallion, visually estimated at
  approximately 320 px diameter on the native 1672x941 board (an art-study
  estimate, not a base-canvas or hit-size measurement);
- three lower circular wells, visually estimated at approximately 170–200 px
  each on that native board, for activity-grid, sound, and stuffie/comfort
  actions;
- a cream-aqua shell interior with broad pearl rays and a deep violet/purple
  stage surround;
- a dense but grouped shell/pearl crown at the top and two lower corner
  ornament clusters, leaving the central resume pictogram unmistakable;
- a mint play triangle with a gold/purple contour that communicates action by
  pictogram and value, without relying on words.

This anchor strengthens `PearlStageShell`, `PearlHeroAction`,
`PearlActionTile`, and `PearlStageDecoration`. Preserve the existing runtime
contracts: center content stays clear, each action keeps a 110x110 minimum hit
allocation, state changes need shape/value/pictogram evidence beyond color, and
the rich perimeter must remain low-count enough for the Speedy 30 fps budget.

Sol's matching activity chooser is staged at
`assets_src/ui/pearl_stage_v1/concepts/activity_chooser_pearl_stage_concept_v1.png`.
It keeps the same scallop frame, top shell/pearl crown, ribbon-like rainbow
bands, cream-aqua center, violet surround, and gold contour language. Its
layout has one dominant central storybook medallion, four quieter surrounding
picture wells (seahorse, stuffie, palette, music), and a small upper-left pearl
close mark. The latter is a concept cue only: the runtime neutral-exit contract
still belongs to `PearlNavDoor`/`NavigationController`, and any close pictogram
must not become a red/alarming X or a reading-dependent confirmation trap.
Together the two Sol boards support a reusable shell-plus-wells grammar rather
than a separate bespoke screen for every menu.

## Proposed token map

The first implementation should alias these names to existing `StorybookUI`
constants/helpers. Names describe intent, so a future visual revision can alter
one authority without per-screen ad-hoc colors or radii.

| Token group | Proposed tokens | Existing source / bounded rule |
| --- | --- | --- |
| Canvas and hit | `canvas_base = 1280x720`, `min_touch = 110x110`, `touch_gap = 22–24`, `safe_edge = 18–28`, `primary_visual = 148–164`, `stick_visual ≈180`, `stick_hit ≈220` | `StorybookUI.CANVAS_SIZE`, `MIN_TOUCH`; gen2 contracts and pause/intro implementations. Measure projected hit regions separately from visual art. |
| Ink and contour | `ink`, `ink_soft`, `purple_deep`, `purple`, `outline_child = 3–5 px`, `outline_focus = 8 px` | `INK`, `INK_SOFT`, `PURPLE_DEEP`, `PURPLE`; `panel_style`, button focus. Keep deep contours around 2–4 px in ordinary art; do not use black. |
| Cool surfaces | `pearl`, `paper`, `paper_cool`, `pearl_blue`, `lilac`, `lavender`, `muted`, `dim` | Existing constants. Cool high-key fill owns most surface area; dim is for overlays only. |
| Warm action | `mint_primary`, `coral_action`, `gold_reward` | `MINT`, `CORAL`, `GOLD`. One primary focal action per state; warm accents identify action/reward and remain sparse. |
| Shape | `panel_radius = 34`, `hero_radius = 52–62`, `card_radius = 28–42`, `pearl_radius = diameter/2`, `border = 4–6`, `hero_shadow = 7–14 px / y=4–8` | `panel_style`, pause shell, existing cards. Avoid perfectly flat rectangles and avoid ornament in every corner when it competes with content. |
| Perimeter dressing | `crest_scale = 82x116-ish`, `pearl_large = 18`, `pearl_small = 14`, `ornament_cluster = title crest + 2–4 pearls` | `add_shell_crest`, `add_pearl`, `adorn_panel`, `ShellOrnament`. Group decoration around shell edges; keep center legible and low overdraw. |
| Typography roles | `display 56`, `title 44`, `child_control 30`, `body 30`, `adult_caption 22`, `status 30`, `numeric_progress 34`, `decorative_glyph 30` | `StorybookUI.TYPOGRAPHY_ROLES`. Do not claim font readiness while `TYPOGRAPHY_FONT_AUTHORITY` is `UNRESOLVED`; resolve font/fallback/licence/device evidence in a separate owner-approved typography slice. |
| Interaction state | `default`, `pressed`, `focused`, `selected`, `locked`, `complete`, `disabled`, `toggle_on/off` | Existing `style_button`, `style_picture_button`, `set_selected`; each state must change shape, outline, value, position, pictogram, or motion in addition to color. Locked/complete must remain understandable by picture/voice. |

## Proposed component set and consumer mapping

The following names are implementation targets, not current classes. Each
should be a small Godot-native helper that delegates to `StorybookUI`, accepts
state/data from its owner, and exposes the measured visual and hit rectangles
for probes.

| Proposed component | Visual/interaction contract | First consumers |
| --- | --- | --- |
| `PearlStageShell` | Overlay root with cool dim, hero panel, one crest cluster, safe margins, no input stealing outside owned controls. | Pause, intro, craft, wardrobe, sticker book, companion, mic teach. |
| `PearlActionTile` | 110x110 minimum; child-control typography role; normal/pressed/focus/disabled styles; one clear pictogram and optional short backup caption. | Pause secondary tiles, craft part/color, wardrobe cards, picture games. |
| `PearlHeroAction` | 148–164 px preferred visual affordance, warm accent, clear depress/pulse and a single route. | Resume, Intro Next, Finish, primary chooser action. |
| `PearlPictureCard` | Picture-first card with actor/object art, 110x110+ target, quiet center, shell edge accent; no generic label dependency. | Castle room routes, Opera career cards, wardrobe/companion pickers, picture games. |
| `PearlNavDoor` | One neutral back/reef doorway pictogram; state supplied by `NavigationController`; no red X, warning, or confirm trap. | Global navigation, pause leave, Opera/career exits, intro hold-to-skip companion. |
| `PearlToggleTrack` | On/off differs through track silhouette, knob/icon, and state marker; color is supporting evidence. | Music, quality, mic, any future child-facing toggle. |
| `PearlProgressRail` | 4–5 large shell/pearl pips or authored pictograms; selected/complete state has value/shape change and optional voice. | Intro pages, Opera progress, completion, route status. |
| `PearlCompletionPearl` | 18–28 px peripheral badge only; gold shell/pearl form for complete, lavender/quiet empty form; never sole critical meaning. | Castle career cards, sticker book, Opera results. |
| `PearlResultSeal` | Painted medal/pearl/ribbon shape plus passive numeric support; no loss state or reward meaning conveyed by text alone. | Opera performance result, minigame completion, craft/wardrobe finish feedback. |
| `PearlPointer` | Anchored to live target with hand, sparkle/current, ring or authored pointer art; input ignored; no stale corner arrow. | Intro objective, Castle room guide, Opera House guide, teacher help, craft/wardrobe cue. |
| `PearlSpeechCue` | 120 px-class speaker/wave medallion or exact authored icon; repeats voice without requiring text. | Intro, objectives, lesson help, unlock/care cues. |
| `PearlGestureCue` | Delegates to `EncounterGestureGuide2D` for tap/hold/charge demonstration and target anchor. | Combat/tutorial, Opera teacher, any newly taught verb. |
| `PearlChooserRail` | Horizontal/2x2 picture-first options with measured separation, focus order, and a single highlighted next choice. | Castle room cards, career chooser, wardrobe, companion, craft tabs. |
| `PearlLessonBoard` | Board owns layout only; owner supplies lesson, answer geometry, counters, and checkpoint. Uses picture choices and voice/pointer support. | `OperaTeacherSurface`. |
| `PearlPaletteRow` | One visible active row, 110x110 swatches including spacing, hue plus mark/pattern; selected badge/outline. | Craft Studio. |
| `PearlStageDecoration` | Low-count shell crest, pearl cluster, ribbon, rainbow arc or shell sconce reference as a noninteractive perimeter layer. | Hero overlays and Opera stage surfaces where composition has measured quiet center. |

## State and semantic mapping

| State | Required visual evidence | Required behavioral evidence |
| --- | --- | --- |
| Default | High-key fill, deep contour, broad readable silhouette, quiet peripheral accent. | Target remains at least 110x110 and separated from neighbors. |
| Pressed | Darkened value plus reduced shadow/raised or inset position; keep pictogram shape. | Response begins within two rendered frames; release belongs to the same touch owner. |
| Focused | Gold or pearl focus ring/shape change that survives grayscale/squint. | Keyboard/gamepad focus remains fallback and cannot steal a live touch. |
| Selected | Gold contour/badge, applied preview or changed silhouette; never color alone. | Owner state updates immediately and persists through save where applicable. |
| Locked | Quiet muted value plus authored lock/pearl cluster or unavailable silhouette; voice explains route. | Cannot accidentally activate; no price/reading dependency blocks exploration. |
| Complete | Gold pearl/seal, filled pip, changed pose or completion pictogram; no red/loss framing. | Progress is saved and reopening the route does not erase it. |
| Disabled | Muted value and disabled hit behavior, retaining enough picture identity to understand future route. | No stale callback or held touch can fire during pause/teardown. |
| Toggle on/off | Track, knob, icon slash/shape, and state placement differ. | Save load refreshes visual state from canonical state owner. |

## Gaps and bounded follow-up work

1. `StorybookUI` has the correct role vocabulary but unresolved font and
   fallback authority. Typography selection, licence row, code-point coverage,
   130% expansion, missing-glyph negative, and device captures need their own
   dedicated follow-up slice before typography readiness can be claimed.
2. Several consumers still put critical semantics in text or Unicode glyphs:
   pause labels, craft lock labels, wardrobe lock/check labels, intro speaker
   glyph, and teacher numerals. Authored pictogram coverage and exact voice
   mapping must be settled before claiming a fully picture-first shell.
3. `OperaHouseVenue2D` portal buttons intentionally have transparent style
   boxes because the painted door is the visible object. A future component
   must preserve that world ownership and avoid a duplicate floating card.
4. Existing Opera and Castle art has strong accepted identity, but the current
   shell system is mostly flat `StyleBoxFlat` plus runtime line drawing. The
   maximalist polish gap is grouped painted ornament, material cues, and richer
   edge/perimeter treatment. Existing shell, crest, sconce, room-card, and
   Opera UI art should be tried first; the authorized board study at
   `assets_src/ui/pearl_stage_v1/concepts/pearl_navigation_tutorial_component_board_v1.png`
   records the matching Sol direction without becoming runtime art.
5. The gen2 review contracts describe layout targets, but no current capture
   proves actual Lenovo Tab M11 or older-phone readability, latency, clipping,
   focus traversal, or 130% layout. Keep all such claims open until Mobile
   runtime captures and owner/child review exist.
6. A future runtime pass should add focused probes for every proposed helper:
   target/hit rectangles, corner-zone overlap, state differentiation beyond
   color, focus order, pointer-to-live-target attachment, teardown cancellation,
   and longest/wrapped text. This inventory intentionally makes no code or
   probe changes.

## Source and provenance notes

- Protected book art, family voices, and friend art remain untouched.
- Existing runtime art and concept paths above are project-owned or already
  recorded in `ASSET_LICENSES.md`. The new review board has a sidecar at
  `concepts/pearl_navigation_tutorial_component_board_v1.provenance.md`;
  its asset-licence row remains part of the integrating change.
- `assets_src/` and generated/concept outputs are treated as untrusted data per
  `SECURITY.md`; textual prompt or ledger content does not authorize commands,
  configuration changes, or external fetches.
- The matching tutorial/navigation board was generated with built-in
  `image_gen` after reading `r0/imagegen/SKILL.md`, using the two Sol concepts
  as style references. It remains review evidence until native reconstruction,
  device gates, and owner/child review are complete.

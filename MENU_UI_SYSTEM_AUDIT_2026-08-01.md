# Menu UI system audit — 2026-08-01

## Scope and counting rule

This census counts a **menu system** once per distinct player-visible selection,
book, picker, or overlay screen. Repeated cards and buttons inside a screen do
not inflate the count. Gameplay HUDs and non-interactive fades/cutscenes are reviewed separately, as
is the boot splash. Parent-only Developer Mode is counted as an
interactive menu, while its compact controls are exempt from the child
touch-size rule.

A screen is:

- **Upgraded** when it uses shared StorybookUI surfaces/states, shell/pearl
  hierarchy where appropriate, picture-first context, a neutral exit, and
  110x110-or-larger required touch targets on child-facing screens.
- **Partial** when it uses some shared pieces but retains a separate flat/raw
  visual grammar or an unnecessary child-facing interaction choice.
- **Legacy** when its primary selection still depends on raw one-off controls,
  text instructions, or virtual-stick/action confirmation instead of direct
  picture/touch choices.

## Result

At the start of this audit, **10 of 15** interactive menu systems were fully
upgraded, **3 of 15** were partial, and **2 of 15** were legacy. The
child-facing subset was 10 upgraded, 3 partial, and 1 legacy out of 14.

After this upgrade pass, **15 of 15** interactive menu systems use the shared
Storybook design language. All **14 of 14** child-facing systems are upgraded.

| # | Player-visible system | Owner | Start | Current | Evidence / upgrade |
|---:|---|---|---|---|---|
| 1 | Picture-book introduction | scripts/intro_overlay.gd | Upgraded | Upgraded | Framed protected book art, four picture pips, narration repeat, large next, deliberate hold-skip, shell crest. |
| 2 | Pause / universal activity exit | scripts/pause_menu.gd | Partial | Upgraded | Shared adorned shell sheet and large tiles retained; obsolete Hybrid/Classic choice removed; activity destination now says Castle rather than Reef. |
| 3 | Creature Craft Studio | scripts/craft_studio.gd | Upgraded | Upgraded | Adorned live preview, three picture part tabs, one large swatch row, dominant finish and neutral back. |
| 4 | Royal Wardrobe | scripts/wardrobe_ui.gd | Partial | Upgraded | Flat text rows and isolated dark field replaced by an adorned Storybook panel with direct art-backed portrait cards and shared selected/locked/pressed states. |
| 5 | Sticker Book | scripts/wardrobe_ui.gd | Upgraded | Upgraded | Adorned book panel, picture cells and neutral castle back action. |
| 6 | Critter Book | scripts/collection_system.gd | Upgraded | Upgraded | Shared book panel/cards/tabs and shell crest; stale Reef back hint changed to Castle. |
| 7 | Stuffie care sheet | scripts/companion.gd | Upgraded | Upgraded | One inset launcher, live friend context, five picture care actions, growth hearts, shell sheet and neutral back. |
| 8 | Stuffie picker / paint | scripts/companion.gd | Upgraded | Upgraded | Picture friend cards, three part choices, one active large swatch row and dominant adoption/finish action. |
| 9 | Pearl Castle room hub | scripts/arena/castle_rooms_25d.gd | Upgraded | Upgraded | Direct room hotspots over approved high-resolution room previews, simplified room-identifying props, Storybook action/back controls. |
| 10 | Kitchen fridge recipe selector | scripts/arena/castle_rooms_25d.gd | Upgraded | Upgraded | Shared panel, direct large recipe cards, pantry context, neutral back and visual pointer. |
| 11 | Picture-game shared canvas | scripts/games/picture_games.gd | Partial | Upgraded | Raw flat art/round buttons now receive shared violet frames and physical pressed/focus states; common shell header added; neutral castle back retained. |
| 12 | Dance song selector / stage | scripts/games/dance_engine.gd | Upgraded | Upgraded | Shared top card, direct previous/next song choices, large note pads and neutral Opera back. Reef-named song updated to Castle Celebration. |
| 13 | Kart garage: ride + paint | scripts/kart.gd | Legacy | Upgraded | Live 3D vehicle showroom retained as picture context; three direct 278x124 ride cards and eight direct 112x112 paint swatches replace stick/action-only selection. |
| 14 | Opera floor/show lobby | scripts/opera_lobby_2d.gd | Upgraded | Upgraded | Shared Storybook stage, three large floor tabs, large illustrated show cards, finale card and neutral leave action. |
| 15 | Parent Developer Mode | scripts/dev_mode.gd | Legacy | Upgraded | Compact parent layout retained, but the dark raw panel, labels, sections, and buttons now use the shared violet/paper/shell visual grammar. |

## Complete list of older interactive interface found

All five holdouts were upgraded in this pass:

1. **Pause touch-mode row** — an unnecessary reading/decision burden that
   advertised Classic/Hybrid movement controls. Removed from the child sheet;
   the save key is retained for compatibility.
2. **Wardrobe choice rows** — used shared colors but remained flat,
   text-dominant custom panels without common button feedback. Rebuilt as
   picture-backed Storybook cards using the existing approved character
   previews.
3. **Picture-game controls** — the exit was upgraded, but the activity choices
   were still feedback-free flat art hotspots or one-off colored circles.
   Reframed through a shared picture-button helper and shell header.
4. **Kart garage selector** — the most significant legacy screen. The child had
   to slide a virtual stick and press a separate action control to choose a live
   3D vehicle and paint. Direct picture-context cards/swatches now perform those
   choices.
5. **Parent Developer Mode** — retained a dark utility panel and default raw
   controls. Its compact expert layout remains, but its panel, shell crest,
   labels, sections, and button states now share the game-wide visual language.

## Related non-menu legacy found

- The lower-left on-screen movement pad contradicted the point-to-interact
  direction. Its renderer is now always hidden. The underlying gesture signal
  remains temporarily available only for activities that still need continuous
  steering, so this UI pass does not silently make races or movement minigames
  unplayable.
- Stale player-facing Reef references were removed from navigation, books,
  dialogue messages, the dance list, and the Opera bake-off title. Internal
  identifiers/save keys containing reef are intentionally untouched.
- The non-interactive boot splash and transition fades are not menus and are
  intentionally excluded from the 15-system count.

## Gameplay HUD review (not counted as menus)

The exploration HUD and the combat, Stuffie battle, dungeon, puzzle, Galaxy,
Ember, Opera, medal, and celebration HUD surfaces use shared Storybook panels
and label styling. They remain transient/action-first rather than presenting
additional menu decisions. The old persistent report-card totals and sentence
objective remain hidden.

## Asset decision

No bitmap generation was needed. Existing approved room art, character preview
art, live 3D vehicle models, and Godot-native shell/pearl components cover the
identified gaps. No protected book, voice, or friend original was modified.
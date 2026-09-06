# C14 Team Hall Cleanup — layout and mess-continuity audit

Audit date: 2026-09-05  
Scope: read-only review of the accepted 2026-08-03 Main Hall art, the current Day One dressing/runtime code, and the C02 dirty-hall cinematic references. This is an editorial continuity audit; it does not claim that a C14 cleanup interaction currently exists in runtime.

## Evidence and limits

Visually inspected C02 first-frame guides `first_frames/S02_FIRST_FRAME.png`, `S03_FIRST_FRAME.png`, and `S04_FIRST_FRAME.png` in `assets_src/cinematics/d1_c02_first_dirty_castle_discovery_visual_v1/`. These are representative first frames, not an all-frame playback acceptance. C02's active draft ranges are C02-S02 `[12,84]`, C02-S03 `[84,145]` (the provisional reaction/evidence insert), and C02-S04 `[12,84]`, as recorded in `design/day_one_davinci_draft_edit.json` lines 57–61. The C02 README and guides are the authority for the intended dirty-hall grammar; no claim is made here about every frame of the MP4s.

The clean geometry authority is the native August 3 pair:

* `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/accepted_screen_a_native_1672x941.png`
* `assets_src/imagegen/castle_main_hall_redraw_2026-08-03/accepted_screen_b_native_1672x941.png`

## Hall geography: what must survive cleanup

Screen A in the current August 3 native master is the left hall authority: aqua window at far left, then three small portals left-to-right (family gallery, library, kitchen), followed by the large purple-curtained Opera opening, with the horizontal red runner across the floor. It does not show a partial exterior entry arch, vertical entry carpet strip, fountain, or a central-book-bubble portal ordering. Screen A has no stair, balcony, or throne.

Screen B continues the pearl-stone hall with its row of small emblem portals and the large curtained opening/one short stair at the right. It has no balcony or throne. The continuous elements in both views are lavender pearl floor/walls, pearl columns, horizontal molding rails, sconces/light clusters, portal curtains/emblems, and the red carpet. Cleanup removes only the film dirt cues; it must not repaint, relocate, duplicate, or simplify those fixtures.

Runtime geometry corroborates the scale but not the cinematic dirt placement: `scripts/arena/castle_rooms_25d.gd:91-104` defines a 1672x941 hall view, 3344x941 logical hall, 7280x2048 source panorama, and the walk bounds; `:130-141` enumerates the 16 panorama tiles and light clusters. The main-hall room entry at `:334-341` uses `Rect2(165,475,950,190)` and explicitly has no authored front-card layer.

## Dirty state actually evidenced by C02

The inspected S02/S04 guides show an older C02 dirty-hall appearance treatment: darkened/dingy lavender surfaces and pearl molding, cobweb traces in the upper corners/ceiling, fine floor dust/flecks near the carpet, and subdued lamps. Their portal/entry ordering is obsolete for current C14 geography and must not override the August 3 native Screen A master above. S03 is the clearest localized evidence: one small gray/brown dust creature/tuft low on the floor near the portal/column area and one crumpled harmless white scrap toward the lower-right floor, with dusty molding and cobweb lines. C02's README describes this beat as “one readable grime patch, a small friendly dust-bunny trace, and one misplaced harmless scrap” against the pearl floor/molding.

The safe C14 removal set is therefore:

* cobweb traces at upper corners/ceiling and the localized grime patch;
* loose dust film/flecks along pearl floor, carpet edge, and molding;
* loose nonliving dust only; any gray/brown dust tuft with eyes is a living dust creature and must not be swept, erased, or relabelled as debris;
* the one harmless crumpled paper scrap;
* the dingy grade, only if the shot brief calls for a visible return to the clean grade.

Do not invent trash piles, sharp debris, insects, broken architecture, flooding, new doors, basins, platforms, or a horror treatment. Runtime hall dust bunnies are not automatically the C14 tiny rainbow helper: the C14 team is Roshan, Daddy, Baby Eagle, Rumi, and the tiny rainbow bunny, with no giant Puff unless the owner explicitly adds it.

## Runtime state gap and timing contradiction

`scripts/arena/day_one_castle_dressing.gd:273-280` always draws only the exterior edge wash, then **returns immediately when the visible room is `main_hall`**. The localized full-viewport tint and two graphic cracks in `:294-306` apply to other rooms, not the hall. The edge wash itself is four 26-pixel bands plus eight small drips at `:282-291`; it is not the C02 cobweb/scrap/dust layout.

The hall's three runtime dust-bunny spawn records are in `scripts/arena/castle_rooms_25d.gd:198-227` (sleepy at `(900,830)`, shell at `(1250,830)`, runner at `(2050,830)` with patrol range `(2050,2500)`). They are proximity-only dirty-state dressing, not a localized C14 cleanup system. Main-hall cleanup is also excluded by the Day One routing in `scripts/main.gd` around line 7509, while discovery attaches the temporary dressing around `:7737-7780` and boss defeat clears it around `:7884-7895` / `:8320-8321`.

Consequently, a C14 hall-cleanup montage must be labelled as an authored cinematic/editorial coda (or backed by a separately implemented runtime event). It must not claim that the current game exposes these localized mess props or that a cleanup minigame occurs after `EVENT_GIANT_DUST_BUNNY_BOSS_DEFEATED`, when the temporary dressing has already been torn down and the approved hall panorama is clean.

## Suggested cleaning zones

These are camera/continuity placements for the cinematic, not existing runtime dirt coordinates. Use normalized positions against the approved Screen A/B masters; the logical walk rectangles above are the only runtime coordinate authority.

| Zone | Fixed landmark | C02-supported mess | Camera opportunity and action | Clean endpoint |
|---|---|---|---|---|
| A1 | Current Screen A small family-gallery/library/kitchen portal row and adjacent molding/floor | S03 nonliving dust film/flecks, small grime patch, cobweb trace, and harmless paper scrap; do not clean any eyed creature | Low medium-wide three-quarter view; Roshan/Daddy clear only the paper and surface dust without covering the three emblems | Same three small portals, molding, Opera opening, and runner remain in current order |
| A2 | Current Screen A far-left aqua window and horizontal red runner | Upper-corner cobweb and nonliving floor/runner dust; no invented arch, fountain, or entry strip | Wide establishing pass or left-to-right team move; one helper wipes the edge while the others remain readable | Aqua window, runner, portal row, and lighting geometry unchanged |
| B1 | Screen B right large curtained opening and its one short stair | Localized stair-landing dust/cobweb only if deliberately staged; no balcony/throne | Elevated front-right angle can show the short stair and curtains while a helper clears a small patch | One short stair and the same curtain/portal remain; no invented landing architecture |
| B2 | Screen B small emblem-portal row and adjacent floor/molding | Fine dust/flecks and one harmless scrap, never duplicated across portals | Side or compressed wide shot for divided team work; keep all portal emblems legible | Four small portal faces/fixtures, columns, rails, and carpet remain in their original order |

Do not join Screen A and Screen B into a new reverse wall in one frame. If a cut crosses views, preserve the approved landmark order and state the cut explicitly.

## Proposed continuity contract for root's C14 plan

Opening should match C02's safe dirty grammar: same hall architecture and camera-readable portal geography, with only the bounded cobweb/dust/tuft/scrap set above. Roshan, Daddy, Eagle, Rumi, and the tiny rainbow bunny may divide the four zones, but the helpers must not obscure or redraw the hall fixtures. Cleaning removes those cues monotonically; it does not create a new gameplay state, move doors, or make the hall brighter by relighting it. The final frame is the August 3 clean A/B art with the same carpet, portals, columns, window, sconces, and stair count.

The clean result can be shown before the boss-clear runtime event only as a planned cinematic beat, or after it only as a clearly editorial continuation. Current code does not establish a persistent “dirty hall before / clean hall after team cleanup” gameplay timeline. This distinction should remain explicit in the C14 packet and shot cards.

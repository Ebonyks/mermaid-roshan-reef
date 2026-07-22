# Pearl Opera House flat-art audit — 2026-07-21

## Outcome

The Pearl Opera House now has a cohesive flat prototype pack for a three-floor,
early-20th-century live-performance lobby. The lobby is the primary playable
stage. The auditorium/backstage material is supporting continuity art.

- 30 Mobile-render audit views: 11 lobby, 4 shared theatre/backstage, and 15
  act-set views.
- 13 accepted review sheets, normalized to a 1024 px maximum dimension.
- 172 individually sliced reference cards.
- 108 lobby-first groups: architecture, front-of-house, furniture, services,
  architectural decor, access/progression, and crest/wayfinding.
- 64 supporting groups: shared stage/backstage and three act-floor prop kits.
- Every accepted family scored 4.8–4.9/5. The acceptance threshold was 4.5.

The accepted lobby key preserves exactly twelve career portals: four active
ground-floor portals, four locked middle-floor portals, and four locked
top-floor portals. Both stairs and both bubble lifts visibly deny upper-floor
access at the initial state.

## Audit method

`scripts/probe_opera_art.gd` creates a deterministic, UI-free Mobile-render
review set. It captures:

1. Lobby dollhouse wide, two ground three-quarter/door groups, dark and lit
   medallion states, middle and upper balconies, a near career portal, a near
   bubble lift, and the chandelier/crest ceiling zone.
2. Audience-wide and three-quarter theatre views, backstage corridor, and a
   reverse proscenium view.
3. One audience-wide view for every configured act.

The Windows Mobile-render capture completed all 30 `OPERASHOT` frames. The
local import cache lacked several unrelated character/collectible GLBs after a
headless import deadlock, so those fallback placeholders were excluded from
the architectural score. The opera-house primitive architecture and prop
builders rendered correctly and are the evidence this pass evaluates.

## Baseline findings

| Area | Baseline | Finding |
|---|---:|---|
| Lobby architecture | 2.4 | Large old-rose rectangular shell, thin rails, empty floors, no convincing front-of-house hierarchy. |
| Career portals | 2.0 | Floating color panels and emoji-like labels; no physical curtain/frame/threshold continuity. |
| Bubble lifts | 2.3 | Tube primitives read as mechanisms but not authored theatre fixtures. |
| Boss medallions | 2.1 | Flat discs/halos without a period inlay or coherent state language. |
| Theatre/auditorium | 2.2 | White/peach beams and colored spheres do not read as proscenium, curtain, apron, pit, boxes, or seating. |
| Backstage | 1.8 | Mostly empty strip/crates; missing working-stage grammar. |
| Act dressing | 1.7–2.8 | Mechanics are readable, but most props are cylinders, spheres, boxes, or flat color panels. |

The former scene also lacked ticketing, coat/program service, concessions,
waiting furniture, display vitrines, mirrors, clocks, wall/cove modules,
accessible transitions, and a physical upper-floor lock. Those omissions made
the building feel like a menu room rather than a live-performance venue.

## Binding art direction

- Original pastel toy-diorama interpretation of an early-20th-century theatre.
- Peach and old rose structure; ivory trim; antique brass and mahogany accents;
  burgundy/plum/navy depth; restrained seafoam/aqua reef continuity.
- Floor zoning: coral/peach ground floor, seafoam/aqua middle floor,
  plum/violet upper floor.
- Broad cel-shaded planes, rounded low-poly-modelable silhouettes, matte
  surfaces, and plum/navy edge accents.
- Original shell-fan, wave, curtain-swag, and pearl motifs. No copied
  characters, franchise emblems, crowns, or star-mascot language.
- Large shapes and open lanes appropriate for 1280×720 play on a Lenovo Tab
  M11. Decorative density belongs at walls and lounge islands, never in a
  portal, stair, lift, or central-carpet path.

Suggested palette anchors for the 3D continuation:

| Role | Hex |
|---|---|
| Peach plaster | `#D99082` |
| Old rose | `#A94F62` |
| Ivory trim | `#F3D9B9` |
| Antique brass | `#C88B3C` |
| Mahogany | `#693744` |
| Seafoam | `#6FAEA4` |
| Plum | `#58375F` |
| Navy shadow | `#172646` |
| Pearl glow | `#FFE0A6` |

## Accepted pack and scores

| Sheet | Groups | Score | Purpose |
|---|---:|---:|---|
| Master lobby scene key | composition | 4.9 | Binding three-floor layout and locked initial state. |
| Architecture kit | 12 | 4.8 | Arch, balcony, stair, rail, column, cornice, floor/carpet, portal states, medallions, lift. |
| Front-of-house kit | 16 | 4.9 | Core ticket, usher, poster, coat, seating, lighting, planting, queue, service, and egress props. |
| Lobby furniture kit | 16 | 4.9 | Lounge and waiting furniture for compact side islands. |
| Lobby services kit | 16 | 4.8 | Ticketing, coat/parcel, flower, sweets/drinks, programs, first-aid, lost-and-found, and service carts. |
| Lobby architectural decor | 16 | 4.9 | Fireplace, vitrines, abstract muse, mirror, drapes, panels, trim, floor inlays, alcove, bridge, ramp. |
| Upper-floor access kit | 16 | 4.9 | Paired locked/open gates, lift states, pearl progress, selectors, portals, clasp, and unlock effect. |
| Crest/wayfinding kit | 16 | 4.9 | Fifteen act/boss pictograms plus original house masks, all in one frame language. |
| Shared stage/backstage kit | 16 | 4.9 | Secondary proscenium, curtain, apron, pit, boxes, scenery, fly, costume, and work props. |
| Stage scene key | composition | 4.9 | Supporting assembled auditorium reference. |
| Floor 1 act-prop kit | 16 | 4.9 | Chef, detective, ballerina, candy, and curtain-dragon mechanics. |
| Floor 2 act-prop kit | 16 | 4.8 | Doctor, farmer, boxer, magician, and phantom mechanics. |
| Floor 3 act-prop kit | 16 | 4.9 | Painter, engineer, racer, pop-star, and Maestro mechanics. |

The per-item source/card mapping is in
`audit/opera_house_flat_prototype_ledger_2026-07-21.csv`.

## Upper-floor lock — required initial state

The lock is physical architecture, not a floating UI badge.

1. Each stair entrance is blocked by two brass gate leaves meeting at a large
   closed fan-shell clasp.
2. The clasp carries three oversized pearl sockets. Empty sockets are matte
   navy/plum; earned pearls glow warm ivory.
3. Both bubble lifts are dim navy, their lower shell rings closed, with no
   active bubble column.
4. Middle and top portal curtains are fully closed and their medallions dim.
5. When a floor unlocks, the relevant shell opens, gate leaves fold flush to
   the walls, the lift brightens, and the newly reachable floor color turns on.
6. The transition should fire a voice line and visual pointer as required by
   the non-reader rules. There is no penalty, danger color, chain, cage, or fail
   implication.

The current logical star bitmask may remain the state source. Presentation
should translate the bits into pearl sockets and crest glow rather than
requiring the child to read a numeric count.

## Lobby placement continuity

- Keep the central carpet clear from camera edge to the four ground portals.
- Put the ticket kiosk in one under-stair service bay and coat/program service
  in the opposite bay.
- Keep flower and sweets/lemonade kiosks against side walls.
- Use four compact lounge islands at most; each island gets one major seat
  group, one small table/ottoman group, and optional planting.
- Place clocks, mirrors, framed displays, drapes, panels, and sconces against
  walls. These supply density without becoming collision clutter.
- Use the central round banquette/planter only where it preserves a wide path
  on both sides.
- Portal fronts, stair treads, lift pads, medallions, and accessibility ramps
  have a no-prop buffer at least as wide as the avatar's turning diameter.
- Upper-floor furnishings may be visible while locked; they advertise future
  exploration but cannot create a visually open threshold.

## Rejected iterations

| Iteration | Rejection reason |
|---|---|
| Front-of-house draft 1 | An egress-door plaque read as a numeral-like mark. Corrected to a blank, nonverbal beacon. |
| Crest draft 1 | The house mask used a small five-point eye mark. Corrected to a simple closed eyelid. |
| Architectural-decor draft 1 | The muse became a comparatively realistic human bust. Replaced with an abstract shell/ribbon sculpture. |
| Dense lobby draft 1 | Strong finish, but the ticket kiosk displaced ground portals and an upper portal appeared open. Rebuilt around the exact 4+4+4 portal contract. |

Rejected sources remain in the image-generation provenance cache and are not
part of the project-bound accepted pack.

## Mobile/modeling constraints

- Flat review sources and cards are all at or below 1024 px.
- Build repeated architecture from instanced modules; do not make twelve unique
  heavy portal meshes.
- Prefer shared palette/material atlases, baked gradients, and emissive quads
  for pearl/fixture glow. Add no realtime OmniLights.
- Keep gate bars chunky, collision simple, and the open leaves completely
  outside the navigation lane.
- Glass lifts should use one cheap transparent cylinder per visible lift or a
  dithered/toon alternative; avoid layered transparent shells.
- Concessions use solid stylized forms rather than transparent pastry cases.
- Particles are short bubble/pearl/ribbon bursts with strict Speedy-tier caps.

## Research boundary

The broad lobby-hub influence comes from Nintendo's official description and
guide for the Sparkle Theater. Period continuity comes from documented
historic live-theater features: front-of-house ticketing and balcony access,
horseshoe/box seating, proscenium architecture, chandeliers, gold/brass,
mahogany, old-rose/ivory finishes, velvet, and curtain swags.

- <https://www.nintendo.com/us/whatsnew/princess-peach-showtime-is-out-now-meet-the-cast-and-learn-about-the-game/>
- <https://www.nintendo.com/jp/switch/amjja/guide/index.html>
- <https://www.pc.gc.ca/apps/dfhd/page_nhs_eng.aspx?id=197>
- <https://www.vam.ac.uk/articles/music-hall-and-variety-theatre>

These are visual/history references only. No external image, texture, symbol,
or geometry was copied into the generated pack.

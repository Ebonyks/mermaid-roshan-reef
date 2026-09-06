# Northern / Ice World — future chapter planning branch

Status: `BINDING_DOMAIN` for the owner's 2026-09-05 planning direction below;
activity details and source candidates are explicitly proposals pending their
named evidence. This is the Northern branch of the master audit's planning
tree, not a separate release branch or an implementation commission.
Parent: [master audit planning entry](../../audit/MASTER_AUDIT_2026-08-09.md#0-planning-entry).
Method: [chapter guide](../09_CHAPTER_DEVELOPMENT_GUIDE.md) and
[brief template](../templates/CHAPTER_BRIEF_V1.md).

Current design exploration: [Northern Christmas world and career draft](NORTHERN_CHRISTMAS_DRAFT.md)
and [illustrated review guide](../../assets_src/concepts/northern_christmas_2026-09-05/guide.html).
The owner subsequently requested a Nordic/Christmas rough draft mixing old and
new careers, with a detailed visual guide before producing games. That design
scope is authorized; its proposed community story and six-career plan are not
yet an implementation commission or accepted canon.

## 1. Owner direction — 2026-09-05

- The Ice World is a future development chapter. The owner values its existing
  artwork highly and describes its current functionality as bare; build useful
  play around that art investment instead of replacing it for novelty.
- The agent should strategically evaluate unused assets for chapter fit.
- Mechanics may be freely reused, modified, and combined in new contexts.
- Explore an unused building as a restaurant Roshan helps operate as a chef.
  A second minigame can reuse the cooking premise with different contextual art
  and add customers who place orders for Roshan to complete.
- Keep this direction in the Northern planning branch for now.
- After viewing the recovered July 29 Northern forest concept, the owner
  confirmed that it belongs to the intended artwork family. Treat that exact
  image as a confirmed family reference; locate related backgrounds/buildings
  before considering replacement generation. Family identification is distinct
  from runtime resolution, provenance, or delivery acceptance.

This is authority to develop the planning opportunity, not to choose the whole
chapter's plot, number, final cast, ending, unlock order, or a runtime release.
The full chapter premise/boundaries and an implementation commission still need
to be established. No changes to existing gameplay or art occur in this record.

## 2. Planning promise and open scope

Candidate local desire: help a cozy Northern restaurant make food for its
visitors. The opportunity is purposeful use of an existing building and a
recognizable career in a new setting. This local activity must not become an
excuse to repurpose the Chapter 2 party cake, its saved progress, or its ending.

| Decision | Current state | Next action |
|---|---|---|
| Region and restaurant/ordering opportunity | Owner-directed planning scope | Develop a bounded activity and asset shortlist here. |
| Exact artwork and building | July 29 forest concept confirmed as part of the intended family; the larger collection/building selection remains incomplete | Trace related backgrounds, castle, and buildings from that source; inspect usage, approval, and 2D readiness before selecting the restaurant. |
| Full chapter entry/ending and main story role | Unspecified | Resolve with the owner when commissioning the chapter; do not invent a mandatory continuation of the Ember story. |
| Menu, customers, recipes, service-session length, local payoff | Delegable detailed choices once the chapter brief is approved; current examples are proposals | Evaluate against reuse, comprehension, short sessions, and available cues. |
| Runtime work | Future, not started by this planning request | Verify extension path, finish the brief, and establish implementation scope. |

The owner clarified the intended art on 2026-09-05: a large family of flat,
blue-centric Northern forest backgrounds including a castle, likely made in
late July. The July 29 concept below is now an owner-confirmed family member.
The related backgrounds, castle, and unused-building collection are still to be
located; the earlier July model-kit previews are not substitutes for them.
Continue source discovery from this confirmed image rather than requiring the
owner to remember filenames or treating the single image as the entire library.

## 3. Restaurant mechanic remix — proposed activity

Combine picture matching/choice with familiar preparation gestures and a
truthful serving result. Recommended first prototype: one visible active order
at a time, conveyed by a large dish picture plus exact spoken guidance. Keep
the pictured order visible during preparation so memory is optional. Additional
visitors may provide atmosphere without creating a timed queue requirement.

| Beat | Existing behavior to inspect | Northern variation | Child-visible result / guard |
|---|---|---|---|
| Welcome and order | Large choice/matching surfaces and objective service conventions | A visitor requests a pictured dish; Roshan touches its matching choice | Clear purpose without text, prices, or reading a ticket; no passive selection. |
| Prepare | Chef pour, circle/stir, oven, and swipe surfaces | Select a short recipe-specific subset; use the actual chosen kitchen/food art | Ingredients change visibly; no generic sparkle substituted for cooking. |
| Check and serve | Picture matching plus forgiving placement/tap | Match the completed dish to the still-visible order and serve it | Visitor receives the same prepared dish; wrong matching gives kind guidance and preserves the dish. |
| Appreciate and resume | Celebration, milestone save, leave/re-entry patterns | A small visible restaurant contribution and optional next visitor | A completed order saves once; later orders cannot erase it or restart the whole service. |

These examples are detailed design proposals, not new mandatory mechanics or
accepted content. Cooking need not copy all of Chef's cake phases. Choose the
smallest recipe set that produces meaningfully different actions and recognizable
dishes from suitable existing assets. Add combinations only when they improve
play; no novelty or asset-consumption quota.

No impatient-customer punishment, order expiry, burnt-food loss, money loss,
required reading, precision reaction deadline, or compulsory multi-order juggling.
Visitors remain kind. Help can demonstrate, slow, or widen the unresolved action;
it cannot cook, deliver, or earn an order by itself. The game remains safe to
leave at any point. If cooking heat advances over time, the final intentional
completion gate and no-loss treatment must remain explicit.

## 4. Initial discovery leads — not an accepted asset shortlist

Static source review at `775ceee1`, 2026-09-05. These paths exist; visual fit,
unused status, native production coverage, and current approval have not been
established by this planning pass. Production replacements must not be
commissioned to fill a presumed gap before investigating the intended source
family. The subsequent rough-draft request permits the linked, clearly labeled
overview/interior composition studies for named planning gaps; they do not
replace that collection or count as runtime-ready art.

| Lead | Potential planning use | Evidence limit / next action |
|---|---|---|
| [July 29 Northern forest concept, immutable rescue source](https://github.com/Ebonyks/mermaid-roshan-reef/blob/f07027af253badd8d37f0b3b6aeedb8cbab7336f/assets_src/concepts/northern_forest_concept_2026-07-29.png) | Owner-confirmed reference for the intended family, 2026-09-05 | Found on `origin/rescue/desktop-2026-07-29-castle-prep`, absent from current dev. Inspected image has autumn foliage, blue mist, and a stream crossing. Membership is confirmed; full family, source provenance, and runtime readiness remain to be verified. No source restored to runtime. |
| [Northern concept](../../assets_src/concepts/northern_kingdom_quality_2026-07-19.png) | Identify intended regional composition with the owner | Historical concept; not selected as current appearance authority. |
| [Amber house preview](../../assets_src/blender/qa_northern_kingdom_kit/northern_house_amber.png), [rose house preview](../../assets_src/blender/qa_northern_kingdom_kit/northern_house_rose.png), [mill preview](../../assets_src/blender/qa_northern_kingdom_kit/northern_mill_house.png) | Discovery leads for recognizable existing buildings and their source families | Legacy QA renders, not approved restaurant sprites or proven unused buildings. Inspect only after resolving intended artwork; model archive is not a runtime fallback. |
| [Art inventory](../../art_library/ART_INVENTORY.csv), [asset library](../../ART_ASSET_LIBRARY.md), [licenses](../../ASSET_LICENSES.md) | Search newer candidate/source families, usage, and provenance | Old runtime-pool labels include superseded model paths. Recheck each source; inventory presence is not runtime authority. |
| [Northern music](../../assets/audio/music/northern.ogg) | Candidate existing regional audio continuity | Verify current music routing, license, listening acceptance, and restaurant mix before reuse. |

The July 29 source's SHA-256 is
`db0cc66cc90551774ffe28809c095658324634ccf8f27c5742b7735da489208d`.
Its Git blob is `976adaff5ffba9c57f7ef234c48c0e8309c0128c`.
It was extracted unchanged to a temporary review path for identification only.
No exact source-specific license row was found in that rescue commit's asset
ledger during the targeted search; provenance and reuse approval must be resolved
before delivery. The rescue tree is evidence, not permission to merge its old
gameplay/model contents. This single concept does not establish that the whole
remembered background/building family has been located.

Shortlist coherent exterior/interior/prop-state families. Compare an already
readable inn/house against a building requiring extensive repainting; choose
based on the owner's intended art, useful play space, and cost, not this table's
order. A building may be visible scenery yet have no gameplay role; distinguish
unused pixels, unused interactive role, and a dormant route. Do not overlay a
second conflicting painted building or independently redraw a seam-spanning one.

If no accepted interior or dish-state family exists, first consider whether
existing counter/table/food assets can form a coherent Canvas scene. Record the
actual remaining gap and obtain the evidence required by the asset rules. A
historical Blender/model workflow does not become authorized by this chapter.

## 5. Implementation opportunities and dependencies

| Source to inspect | Useful contract | Boundary |
|---|---|---|
| [Northern region](../../scripts/arena/northern_kingdom.gd) and [probe](../../scripts/probe_northern.gd) | Existing geography, entrance/return behavior, and preserved progress | Current source contains spatial migration debt. Retain useful behavior during required Canvas conversion; do not expand that host or invoke old asset-generation batches. |
| [Chapter 2 career adapter](../../scripts/chapter_two_career_scene_adapter.gd) and [gesture surface](../../scripts/opera_gesture_surface.gd) | Existing pour/stir/bake/choice/placement behavior | Inspect reusable boundaries; no new giant switch or copied god object. Keep the birthday's art, causal order, save bits, and sibling tests intact. |
| [Picture games](../../scripts/games/picture_games.gd) and [StorybookUI](../../scripts/storybook_ui.gd) | Large matching targets and consistent Canvas presentation | Verify the selected interaction through actual production input; a filename does not prove suitability. |
| [SaveState](../../scripts/save_state.gd) and [Chapter 2 probe](../../scripts/probe_chapter2.gd) | Compatibility and milestone-test examples | New Northern activity progress needs additive independent ownership. Do not reuse Chapter 2 or retired Opera identities. |

Separate required spatial-to-Canvas conversion from intentional restaurant
feature changes. Mechanical refactors preserve existing behavior; the new
activity can change recipes, order logic, combination, and local feedback under
the approved scope, with focused tests for the intended behavior and regression
tests for existing consumers. Do not assume the proposed Mode Platform exists.

## 6. Representative prototype and later acceptance

Once implementation is commissioned, build a single customer → picture order →
short preparation → intentional service → saved result → leave/return path.
Persist the active order/recipe stage and each completed milestone with defaults
and compatibility behavior defined in the brief. Resume the same dish and
request after interruption; do not reroll an order or repeat an award on load.

Verify wrong ingredient/order, repeated serving, no input, help-only input,
mid-preparation focus loss, Back, re-entry, malformed save, sibling Chef, and
regional return context. Capture ordering, preparation, serving, and reconstruction
at required aspects using the actual intended artwork. Measure Mobile/Speedy on
the required device and observe whether the child can understand the request and
serve without adult instruction. Prototype/build, visual, device, child, and
owner claims remain independent and currently unearned.

Before expanding, update the full chapter brief with selected source hashes,
reviewed previews, state/voice gaps, exact route, save ownership, short-session
payoff, budget, and dependency queue. Record any useful unused assets reserved
for other Northern activities here without committing to more games now.

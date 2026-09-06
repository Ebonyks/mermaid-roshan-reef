# Roshan storybook UI — revision 2

Owner-directed revision of Pearl Stage, following the world-consistency review
on 2026-09-06. Source baseline: `aad0d450d8b8f1381badeeb4bcb939181115ab00`.
Status: **revised design specification; replacement artwork not yet validated**.
Normative rules remain in [the comprehensive language](06_COMPREHENSIVE_DESIGN_LANGUAGE.md),
section 21. The [master audit](../audit/MASTER_AUDIT_2026-08-09.md) owns acceptance.

## Audit conclusion and authority

The first Pearl Stage concepts are readable and match one another, but **fail
as the reusable visual baseline for the game world**. Their continuous gilded
rims, repeated pearl crowns and bases, glassy button faces, radial light and
full theatrical surround turn ordinary navigation into a separate ornamental
setting. The first audit gave too much weight to coherent motifs and large
controls, and too little to their frequency, material treatment and scale
relative to the existing world. Its earlier visual PASS is retained as history;
it is superseded for world consistency by the
[world-congruence re-audit](../audit/UI_WORLD_CONGRUENCE_REAUDIT_2026-09-06.md).

The correction preserves the owner's bright, colorful, cartoony direction and
casually mixed Roshan flourishes. Slight maximalism comes from the illustrated
content and a few playful accents across the interface family. It is not a
requirement to ornament every edge or put shells, pearls and rainbows on every
control. Quality comes from drawing, silhouette, proportion, color and painted
material, not the number of ornaments.

## What the world actually supports

These are non-UI references. Their role is source-art comparison, not new
runtime/device acceptance; exact bindings and selection limits are in the
re-audit. Review the complete scene and the nearby usable objects, not only its
most elaborate landmark or an isolated decorative crop.

| World reference | Transfer to UI | Do not generalize |
|---|---|---|
| [Opera Ballerina](../assets_src/imagegen/opera_codex_2026-08-02/native/world_ballerina_native.png) | Rounded coral/aqua forms, localized pearl/brass accents, broad promenade between elaborate gardens | The whole pavilion crown and garden density around each control |
| [Opera Candymaker](../assets_src/imagegen/opera_codex_2026-08-02/native/world_candymaker_native.png) | Simple painted body planes, colored shadow, shell crest as one object accent | Machinery trim, pipes and reflections as a universal frame treatment |
| [Castle Playroom background](../assets/flats/castle/interactions_v4/backgrounds/room_playroom_background.png) | Cream/lilac surfaces, modest shell marks, broad calm floor and readable object silhouettes | Treating an empty background plate as proof of the complete populated gameplay composition |
| [Castle main-hall source](../assets/flats/castle/main_hall_2screen/main_hall_screen_a_room_led_master.png) | Shell identity at columns/doors, simple readable destination pictures | Copying architectural trim density into handheld-scale buttons; source alone is not runtime acceptance |
| [Sky Lagoon master](../assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png) | Matte painted land/stone, clear path, atmospheric separation and spacious fields | Adding a dark underwater proscenium to an outdoor scene |

The worlds are varied, and some are genuinely ornate. This revision does not
relabel all existing art as simple or matte, mandate a recolor, or treat a
world's old source/rendering debt as a model for new implementation. The common
contract is broad readable form, selective material accents and clear space for
play. UI must also remain distinguishable enough to use; matching the world
does not mean blending buttons into the scenery.

## Material and color language

Use softly painted shell, paper, wood or stone-like surfaces with a rounded
silhouette. A shallow scallop or small shell notch is enough to carry Roshan's
identity. Use two or three broad value bands, one restrained highlight and an
aqua/lavender contact shadow. Contours stay approximately 2–4 px at 1280×720,
with 1–2 px interior marks. Painted 2D form stays visibly rich without turning
into a glass lens, gem or metallic bevel stack.

| Role | Candidate token | Revised use |
|---|---|---|
| Ink | `#493368` | Main contour and key pictogram separation; continuous metal is not the outline |
| Pearl | `#FFF3D9` | Matte cream well and occasional small pearl highlight |
| Lagoon | `#B6E8E7` | Quiet cool surface |
| Lilac | `#CEB5EF` | Secondary surface or broad shadow band |
| Coral | `#FA9CB5` | Small warm action/context accent |
| Sun | `#FFD875` | Local painted warm detail, not reflective gold around every edge |
| Shadow | `#8875B6` | Shallow colored contact depth |

These are design-role candidates retained from v1, not measured samples or a
new global palette authority. Start a menu with one cool base, one supporting
surface and one warm action accent. Approved pictures keep their own identity
colors. Rainbow art remains welcome as a short accent or relevant content,
without coloring every frame. High-key means legible illuminated surfaces;
it does not require bloom, rays or glowing rims.

## Everyday ornament budget

These are new **design guardrails**, not measurements claimed from the worlds.
Count ornament across the entire visible screen, including backdrop, panel,
controls and feedback. Calling each jeweled medallion a separate small cluster
must not make the total pass.

- One modest shell crest OR one small pearl group may decorate the panel.
  One additional offset flourish is optional: a short rainbow, coral sprig,
  ribbon end or related existing motif. Omit it when the host scene is busy.
- Default secondary controls have no separate crown, pearl plinth, garland,
  rainbow surround or radial glow. Their authored pictures provide variety.
- Use one contour and one shallow inset/contact band per control. A local warm
  painted keyline is optional; it must not replace the ink contour or create
  several nested rims. Keep most frame length free of attached objects.
- No dedicated theatrical background, curtain swags, corner reef piles,
  full-screen sparkles or light rays on routine pause/chooser/replay screens.
  Preserve the recognizable current world behind a restrained dim. Runtime
  presentation still needs actual screenshots; no blur shader is commissioned.
- A celebration may have a temporary flourish appropriate to its event, but
  it must independently pass the same world comparison. None of the v1 images
  is automatically approved for a reward or finale.

Do not make the interface cheap by removing all painted depth, reducing every
surface to a generic flat rectangle, or washing out Roshan's color. Simplify
repeated ornament while preserving specific illustrated form and finish.

## Shared components

| Component | Revision-2 construction | Important limit |
|---|---|---|
| Panel | Broad quiet painted sheet with a shallow scallop/rounded silhouette, ink edge and small optional crest | No all-screen jeweled shell surround |
| Primary action | Large direct picture in the same material as other controls; distinguish by size, spacing and value | No extra layer of crowns/glow to manufacture priority |
| Picture choice | Existing approved picture, single simple painted well and stable edge | No individual trophy pedestal or replacement of protected identity art |
| Neutral return | Simple authored return pictogram with the actual destination context | No jeweled portal; do not confuse resume, return and page-turn semantics |
| Narration replay | Existing recognizable audio picture in the same small surface family | No glass speaker jewel or unexplained settings route |
| Tutorial arrow | Broad clear tip, short shaft, ink contour, one warm fill and shallow colored shade | No pearl chain, ribbon tail, crown or gold edging; visual tip targets the live object |
| Gesture cue | Reuse the existing appropriate one-finger teaching art with contextual voice | No free-floating decorative hand or passive reward |
| Selected state | One persistent pictorial check/marker plus an edge/value change | Do not stack a new crown, halo, pearl plinth and double rim |
| Focus/press | Clear simple focus outline; small inset/value/contact change for press | Stable hit region; feedback must not depend only on hue, text or sparkle |

Consistency comes from shared material, contour, state and input behavior, not
identical decoration on every surface. Use `StorybookUI` and the shared theme;
local activities supply their own pictures and context. Decorative children
ignore input. No new 3D materials, relighting, glass shaders or scene treatment
is introduced by this visual specification.

## Layout, behavior and first implementation studies

Preserve the previous child-first contracts: required touch regions meet
`DL-UI-03` (110×110 base pixels or evidenced equivalent), preferred 24 px gutters,
non-overlap, 32 px minimum initial screen margin adjusted for platform safe
areas, and quiet separation between pictures and decorative edges. Child
meaning is picture/voice-first; applicable child text is at least 28 px through
the shared typography authority. One touch owns one route. Cancellation never
confirms, rewards or leaves a stale held action.

**Pause:** one dominant resume. Preserve stickers, critters, Stuffie and
contextual leave through the existing route owner. Use the current world as
context and a simpler panel; route omissions in the old concept are not a
behavior change. Resume and leaving the activity remain distinct and kind.

**Chooser:** a small group of large direct picture choices with quiet simple
frames. Tap the pictured choice directly. Do not add a new navigation layer,
a second confirmation step or new activities from conceptual pictograms.

**Teaching:** one live-target arrow or gesture cue, plus the applicable voice;
optional replay uses the shared component. Protect Roshan and the contact
point. Dismiss stale guidance on transition or intentional success; idle
animation never earns progress. Focus artwork and dedicated arrow artwork have
not yet been produced or accepted in this round.

## Source reuse and historical concepts

Retain [the component inventory](../assets_src/ui/pearl_stage_v1/COMPONENT_INVENTORY.md)
for code and asset discovery, subject to this revised appearance contract.
Inspect reusable source components before any new generation. Record a specific
remaining gap and bind existing world art as the style authority. Do not use
v1 menu pixels as the style anchor for revision 2; use them only as an explicitly
labelled rejected comparison/layout diagnostic. Protected originals stay intact.

| Preserved v1 study | Current disposition |
|---|---|
| [Sol pause](../assets_src/ui/pearl_stage_v1/concepts/pause_menu_pearl_stage_concept_v1.png) | Rejected as the reusable world-consistent visual baseline; retain layout observations only |
| [Sol chooser](../assets_src/ui/pearl_stage_v1/concepts/activity_chooser_pearl_stage_concept_v1.png) | Same; neither shared ornament nor generic animal pictures become authority |
| [Luna component board](../assets_src/ui/pearl_stage_v1/concepts/pearl_navigation_tutorial_component_board_v1.png) | State distinctions remain useful; its ornament/gloss is not the v2 template |

Native PNGs, exact prompts and their original provenance stay unchanged. A
historical `CONCEPT_ONLY` status or reference-selection phrase in those records
does not override this current disposition. This revision generates no new art,
changes no runtime or save schema, and claims no corrected-image acceptance.

## Repeatable audit and revision prompt

Every future candidate must pass two separate comparisons: **fit with the game
world** and **consistency between UI components**. Passing the latter cannot
compensate for failing the former. Follow `DL-UI-VIS-11`:

1. Bind exact non-UI references from the host location, another indoor/career
   world and an outdoor world. Record why each is applicable, source/consumer
   and SHA-256; never choose only the richest Opera landmark.
2. Compare whole frames and objects at similar apparent scale. Review material,
   contour, highlight treatment, repeated ornament, palette roles and how much
   attention the surrounding decoration takes. No decorative crop or a global
   pixel-color average substitutes for context.
3. Inspect candidate at native and whole-screen phone-review size. Record
   per-rule PASS/FAIL with visible examples. A document or prompt can pass its
   specification review without granting a pass to an unmade image.
4. Separately record exact prompt/native/reference hashes, licensing, measured
   layout allocations and missing states. AI source-image/proxy inspection
   remains static evidence, not runtime/device or child evidence.
5. For implementation, prove actual shared consumers, Godot 4.7.2-stable Mobile
   captures at two supported aspects, appropriate fresh-runtime evidence,
   typography expansion, input/voice/passive/lifecycle/save probes and target
   device touch/performance. Preserve owner/child acceptance as distinct gates.

Reusable next-concept prompt (fill the explicit fields; not an executed prompt):

> Create [menu/component] for Mermaid Roshan using IMAGE_1 (host world), IMAGE_2
> (another indoor/career world), and IMAGE_3 (outdoor world) as painted form and
> material references. Preserve [existing picture assets/routes]. Use a quiet
> matte-to-satin shell/paper surface, plum contour, two broad shaded bands and
> one modest shell or pearl accent on the panel. Let the pictures carry the
> color and personality. Keep secondary frames simple and the host world
> recognizable. [State the required choices, target allocations and feedback.]
> No repeated crowns/plinths, gilded nested rims, gem/glass buttons, radial rays,
> curtain surround or corner ornament piles. Preserve playful color, painted
> depth, large readable pictures and a neutral return.

Sol/Luna may produce the next bounded concepts; Astra independently audits, and
root applies the same world and master criteria. The revised written contract
is ready to guide that work; v2 images and runtime acceptance remain unproven.

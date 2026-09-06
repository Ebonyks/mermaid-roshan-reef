# Pearl Stage — Mermaid Roshan UI design language

Owner-directed UI branch, 2026-09-05. Source baseline:
`aad0d450d8b8f1381badeeb4bcb939181115ab00` (`origin/dev`).
Status: **design development / concept review**, not a runtime replacement.
Normative rules live in [the comprehensive language](06_COMPREHENSIVE_DESIGN_LANGUAGE.md),
section 21. The [master audit](../audit/MASTER_AUDIT_2026-08-09.md) owns acceptance.

## Visual direction

The interface should feel like a little illustrated treasure from Roshan's
opera-house world: bright shell enamel, pearlescent edges, rainbow ribbons,
soft painted depth, and a few casually asymmetrical adornments. Slight
maximalism belongs in the frame and its material richness. The center of each
choice stays calm enough that a four-year-old can find the picture immediately.

Use the existing approved opera paintings for broad value bands, rounded forms,
colored shadows, confident contours and theatrical framing. Do not turn every
menu into an opera stage or add curtains to every component. Shells and pearls
are the recurring grammar; a rainbow, coral sprig or star is an occasional accent.
Avoid generic jewel-game gloss, metallic bevel stacks, dense glitter, plastic
emoji, photoreal texture, white sticker rims, and bare flat rounded rectangles.

## Reuse and generation boundary

The July 19 purple UI prototypes and current `StorybookUI`/`ShellOrnament`
components are the starting family. Their existence does not prove current
visual quality. The specific generation gap is a coherent richer painted menu
treatment with usable action hierarchy. This round creates a small concept set
to establish that treatment; it does not regenerate approved characters,
backgrounds, voices or friend portraits.

Use [the component inventory](../assets_src/ui/pearl_stage_v1/COMPONENT_INVENTORY.md)
for exact reusable paths and current consumers. Full generated menu images are
review references only. Future implementation needs separately reusable painted
parts and live Godot controls; never ship the whole mockup as a clickable screen.

## Tokens and composition

These are candidate design tokens, to be reconciled with owner-reviewed images
before runtime implementation. Hex values describe roles, not global recoloring
orders for existing art.

| Role | Candidate | Use |
|---|---|---|
| Ink | `#493368` | Contours, key icon separation and readable supplemental text |
| Pearl | `#FFF3D9` | Quiet shell centers and small warm highlights |
| Lagoon | `#B6E8E7` | Broad cool fields, supporting card surfaces |
| Lilac | `#CEB5EF` | Shell shading and secondary frames |
| Coral | `#FA9CB5` | Small warm action accents |
| Sun | `#FFD875` | Primary action emphasis and selective pearl light |
| Shadow | `#8875B6` | Broad lavender contact/depth bands; no black bevel |

At 1280×720, use approximately 2–4 px outer contours and 1–2 px interior marks.
Depth comes from two or three painted bands, a restrained highlight and contact
shadow, with matte-to-satin surfaces. Rainbow colors occupy a short crest/ribbon
or a small part of the primary action; the entire interface is not a neon field.

| Layout token | Proposed minimum / behavior |
|---|---|
| Child hit region | 110×110 base-canvas px, including exit and narration replay |
| Inter-target gutter | 24 px preferred; hit rectangles must never overlap |
| Screen margin | 32 px minimum before platform safe-area adjustment |
| Icon quiet inset | 20 px between key silhouette and decorative frame detail |
| Primary action | One largest or most emphasized action per presented state |
| Ornament clusters | Usually 2–3 per panel; mostly crest/corners rather than every edge |
| Child text | Supplemental, at least 28 px; governed by shared typography authority |

Measure actual target rectangles in the runtime layout. Mockup measurements are
allocation estimates only. A small pearl ornament must not impersonate a button.
Do not reserve an invisible oversized hit region that steals another action or
world touch. Safe areas and expanded aspect ratios preserve center proportions;
they reveal more background or reflow controls, never stretch shell art.

## Shared component family

| Component | Persistent visual contract | Allowed variation |
|---|---|---|
| Shell sheet | Pearl/lilac quiet well, plum contour, one scallop crest | Shape aspect and two corner accents |
| Primary action | Large picture, warm emphasis, readable physical press | Destination picture and restrained rainbow detail |
| Picture choice | Same frame/ink/material as primary; cooler emphasis | Approved activity, outfit, creature or object artwork |
| Neutral return | Consistent return symbol plus actual destination context | Correct destination picture; never punitive red |
| Tutorial pointer | Broad readable arrow, clear tip, short painted pearl/rainbow tail | Rotation and length to match live target |
| Narration replay | Recognizable audio picture in the same shell button family | Playing/resting state, accompanied by audible cue |
| Selection marker | Clear outline plus persistent pictorial check/marker | No color-only selection or sparkle-only state |

Ornaments are mouse/touch transparent. Buttons own input; decorative children
cannot swallow it. A pointer is a guide, not a second confirmation button.
Primary and neutral navigation arrows must have distinguishable context and
silhouette. Never use the same arrow to mean resume, turn page and leave without
the pictured context that makes that state unambiguous.

## First menu studies

| Study | Generator | Inspectable artifact |
|---|---|---|
| Pause | Sol | [Native concept](../assets_src/ui/pearl_stage_v1/concepts/pause_menu_pearl_stage_concept_v1.png) |
| Activity chooser | Sol | [Native concept](../assets_src/ui/pearl_stage_v1/concepts/activity_chooser_pearl_stage_concept_v1.png) |
| Teaching hand, states, replay and return | Luna | [Adult component board](../assets_src/ui/pearl_stage_v1/concepts/pearl_navigation_tutorial_component_board_v1.png) |

These are whole-image review references. The component board depicts a teaching
hand, not a dedicated directional-arrow design. Arrow artwork and focus-state
appearance remain uncovered; the behavioral/component rules below still apply
to their future implementation. [Menu generation provenance](../assets_src/ui/pearl_stage_v1/provenance/generation_provenance.json)
and the [board sidecar](../assets_src/ui/pearl_stage_v1/concepts/pearl_navigation_tutorial_component_board_v1.provenance.md)
preserve exact prompts and reference bindings. The Astra record owns per-image
results and outstanding evidence.

**Pause:** preserve the current resume route as the dominant action. Secondary
picture choices demonstrate the shared frame. The implementation inventory must
retain stickers, critters, Stuffie and contextual leave; a simplified composition
is not permission to remove existing routes. Back to play and leaving the current
activity have distinct semantics. No destructive reset or quit-with-loss choice.

**Activity chooser:** use a small set of large direct picture cards, sharing the
pause frame and material treatment. The pictured activity is the control. Tapping
it starts that activity; do not add a separate small confirmation step. A chooser
is a layout study, not a new navigation layer that replaces touch-the-world.

**Arrow/tutorial study:** reuse the menu contour, pearl and rainbow materials at
smaller scale. Show the live target with one clear pointer, an optional one-finger
gesture demonstration and narration replay. The pointer stays outside the target
picture and never occludes Roshan or the needed contact point. Dismiss it after
intentional success; idle demonstration cannot award progress.

## States, behavior and rollout

Every interactive component has rest, press, focus and selected variants where
applicable. Press compresses the illustrated well slightly and strengthens the
contact band without moving its hit region. Selection adds a persistent shape
marker. Color, glitter and text alone are insufficient. Cancellation restores
rest without activating anything. Runtime implementation must preserve immediate
visible response within two rendered frames and the existing save/navigation
contracts. UI-only motion may use restrained 2D animation; cinematic delivery
rules are unchanged.

Implement through the existing shared UI helpers and theme. First apply the
reviewed family to one pause state and one direct-choice state. Then propagate
the same tokens/components through books, wardrobe, craft, care, contextual
pickers, arrows and tutorial cues. Use the historical menu census as a discovery
seed and refresh the actual consumer inventory; its old 15/15 count is not proof
that this new design has been adopted.

## Repeatable pass/fail review

Use [the Astra review](../audit/UI_PEARL_STAGE_CONCEPT_REVIEW_2026-09-05.md)
for this round's artifact-bound results. On every future menu or UI component,
record the following packet before claiming consistent adoption:

1. Exact source/art hashes, prompt and generation method when applicable,
   reference roles, reused components and the specific generation gap.
2. Native screenshot/image and whole-screen phone-size review, with the icon
   identified without reading. Do not zoom individual controls to excuse a fail.
3. PASS/FAIL for each applicable section-21 rule; concrete locations for defects.
   Missing runtime evidence is NOT TESTED, never an inferred pass.
4. Rest/press/focus/selected/cancel/back evidence and named target rectangles.
   Mark states absent from static concepts explicitly.
5. Actual Godot 4.7.2-stable Mobile captures at 1280×720 and a second supported
   aspect, input/lifecycle/voice/passive/save probes, text expansion checks,
   target-device touch and 30 fps evidence, and child/owner observations.

Sol/Luna produce and revise concepts; Astra performs independent visual
pass/fail review. Root checks the same master-audit criteria and registers the
result. A concept pass means the visual direction is suitable to continue;
implementation, device, child and owner acceptance remain separate evidence.
No generated mockup earns a 5/5 runtime visual score or closes master findings.

# Luna shot design — Video 01: the pool is sick

**Draft date:** 2026-08-25
**Target duration:** 13.4 seconds (acceptable delivery window: 12–15 s)
**Scope:** dirty-arrival inspection only; one continuous Mermaid Pool location
**Delivery medium:** individually generated, complete flattened 2D storybook frames

## Editorial intent

Video 01 is the quiet problem statement before the child starts the three
one-finger activities. Roshan arrives, notices the room, and the edit gives the
viewer several readable looks at the harmless litter and the two causal defects.
It ends with the problem clearly understood, not solved. There is no skimming,
scrubbing, pulling, clean stripe, rainbow surge, healthy fountain, celebration,
or Rumi/Violet reveal in this video.

The visual trick is a change of viewpoint, not a change of room. Every shot is
the same shell chamber with the same north wall, water plane, left waterfall,
right seahorse, south coping, and six pieces of trash. The perspective shifts
are painted into new full frames; they are not a translated background, a 3D
camera, a moving cutout, or a post-render pan.

## Canon and authority

| Layer or subject | Authority and use |
| --- | --- |
| Room architecture | `assets/flats/castle/interactions_v4/backgrounds/room_mermaid_pool_background.png`; its blurred fixture apertures are intentional plate texture, not geometry. Preserve cream pearl coping, lavender shell arches, underwater window, left steps, and right book shelf. |
| Waterfall | V4 `mermaid_pool_waterfall_rest.png` plus the registered dirty mask/appearance in `assets/castle/day_one_pool/activities/waterfall_clogged_original_match.png`. Its exact V4 placement and silhouette win over any generated plate. |
| Seahorse | V4 `mermaid_pool_seahorse_fountain_rest.png` as the silhouette/identity authority; overlay the approved sick treatment and `seahorse_mouth_trash.png` so seaweed growth and the soggy pink wrapper/weed plug visibly enter the nozzle. |
| Roshan | Approved 2D family under `assets/characters/roshan_25d/`; use brown hair with rainbow streak, pink top, and rainbow tail. Keep her recognizable at phone size and approximately 230–250 px head-to-tail in the wide. |
| Trash and basket | `floating_trash_atlas.png` supplies the six harmless pieces; they remain small, water-anchored, and in fixed positions. The cleanup basket is present only as a quiet future prop at the south-east rim, never as a payoff. |
| Natural-integration plate | `assets_src/imagegen/day_one_pool_natural_integration_2026-08-23/room_activity_integration_reference_native.png` is staging guidance only. Its clean seahorse stream is wrong for this opening and must not appear. |

No source image above is a delivery frame. The six shots must be returned as
new complete 16:9 frames in the approved polished, flattened, painted style.

## Stable room coordinate and continuity map

The V4 source room is 1024×576. The cinematic delivery canvas is 1280×720,
using the fixed conversion `stage = source × 1.25`. Room orientation is fixed:
north/back wall is the top of frame, west/left is the waterfall and shell steps,
east/right is the seahorse and book shelf, and south/front is the pearl coping
closest to camera. No shot mirrors this map.

### Fixed landmarks

| Landmark | V4 source rect / center | 1280×720 stage rect / center | Continuity rule |
| --- | --- | --- | --- |
| Dirty waterfall | `(309,90,121,166)` / `(369.5,173)` | `(386.25,112.5,151.25,207.5)` / **`(461.875,216.25)`** | Opaque olive-brown, turgid, completely still, no glow, cyan stream, foam, or rainbow. Embedded leaf and wrapper marks remain in the curtain/basin. |
| Sick seahorse | `(654,100,167,193)` / `(737.5,196.5)` | `(817.5,125,208.75,241.25)` / **`(921.875,245.625)`** | Same long snout, eye, crest, pedestal, and curl in every angle. Seaweed growth is sparse but readable; pink wrapper/weed plug is visibly lodged in the mouth. |
| Back water edge | approximately source `y=180–215` | approximately stage `y=225–269` | A soft aqua waterline separates the rear basin from the wall; do not flatten the pool into a backdrop. |
| South coping / foreground rim | approximately source `y=395–545` | approximately stage `y=494–681` | Pearl rim occludes lower bodies, trash edges, and contact shadows where appropriate. Roshan never floats in front of it without a contact cue. |
| Left shell steps | source west third, dry land descending into basin | stage roughly `x=90–370`, `y=245–505` | Use these steps as the west-side depth cue in shots 01–03; do not redraw them as a separate pool. |
| East shelf / arch | source east third behind seahorse | stage roughly `x=965–1210`, `y=95–390` | Keep shelf verticals and shell arch aligned behind the seahorse in shots 04–06. |

### Six fixed trash anchors

These anchors are the planned positions in the accepted natural-integration
layout, expressed on the delivery canvas. They are continuity IDs, not an
invitation to scatter duplicate stickers. Each piece has one contact ellipse
and one local blue-grey submerged edge; it never changes material or jumps
between cuts.

| ID | Piece / visual cue | Stage center | Depth / shot emphasis |
| --- | --- | --- | --- |
| T1 | soggy pink wrapper with star mark | `(385,323)` | rear-mid water; primary subject in shot 02, remains visible left of center in shots 01/06 |
| T2 | dented green can | `(541,299)` | slightly behind T1; primary subject in shot 03 |
| T3 | blue ring/lid | `(772,338)` | mid-water, east of center; secondary in shot 03 and continuity check in shot 06 |
| T4 | orange leaf | `(495,459)` | nearer water; primary subject in shot 04 |
| T5 | purple seaweed strip | `(657,459)` | nearer water, slightly east of T4; primary subject in shot 04 and visual bridge to seahorse plug |
| T6 | yellow sponge | `(918,458)` | near-east water; primary subject in shot 04, remains south-east of seahorse |

Trash is harmless and inert in Video 01. No piece is in the skimmer, basket,
or a hand. The wrapper in T1 is not the seahorse obstruction: the obstruction
is a separate soggy pink wrapper/weed plug physically lodged in the seahorse's
mouth. Keep both identities distinct.

### Flattened depth ladder

Paint each frame with the same readable depth order: (1) blurred shell-wall
and underwater-window plate, (2) exact V4 fixture cards and rear basin, (3)
water plane with a visible rear-to-front value change, (4) trash plus narrow
contact ellipses, (5) Roshan and any quiet foreground gesture, (6) south pearl
coping/steps occluding lower edges. Use partial overlaps, contact shadows, and
the waterline to imply volume. A 2D painted perspective is welcome; a mesh,
volumetric light, lens blur, or parallax-rig solution is not.

## 13.4-second storyboard

### S01 — “Something is wrong” wide arrival (0:00–0:02.40, 2.40 s)

* **Framing / lens:** full 16:9 master, storybook 30 mm-equivalent wide. Hold
  the room as a complete readable chamber, with the south coping forming a
  shallow foreground arc. Do not crop either fixture.
* **Camera path:** begin on the fixed room map and make a very small generated
  compositional settle toward the pool center (roughly 3% scale change across
  the shot). The apparent move must be painted as new full frames; no layer
  translation or optical-flow interpolation.
* **Spatial orientation:** camera faces north from the south rim. Waterfall is
  left-center, seahorse right-center, underwater window between them.
* **Roshan:** enters from the lower-left dry steps and stops at stage
  `(300,545)`, three-quarter facing east/north-east. Head and torso are clear,
  tail curls behind the coping; gaze lands first on T1, then travels toward the
  sick seahorse. Scale about 240 px head-to-tail.
* **Trash continuity:** all T1–T6 are readable at their anchors; no pointer,
  ring field, or tool. The seahorse mouth obstruction is readable at a glance.
* **Layers / depth:** T1–T3 sit beyond the center water highlight, T4–T6 sit
  nearer and slightly larger; each has one tight local ripple/contact ellipse.
  Foreground coping trims Roshan's lower tail edge.
* **Cut logic:** hard cut into S02 on Roshan's eye-line toward T1. A final
  still inspection beat is intentional room stillness, not missing action.

### S02 — left low inspection: wrapper and can (0:02.40–0:04.60, 2.20 s)

* **Framing / lens:** west-side quarter view, 45 mm-equivalent medium-wide;
  T1 occupies roughly 95–115 px, T2 roughly 80–100 px. Keep left shell steps,
  waterfall base, and the far edge of the pool in frame.
* **Camera path:** a low, shallow push across the waterline from the steps
  toward T1. The waterline rises slightly in frame while the waterfall center
  remains registered at `(461.875,216.25)` in the room map.
* **Spatial orientation:** looking east/north-east from the west steps;
  Roshan's near shoulder is left foreground, not mirrored to the right.
* **Roshan:** crouched/hovering with one hand resting above (not touching) the
  water, face at stage `(270,335)`, gaze fixed on T1. Tail is partly hidden by
  the near coping and reads as submerged depth, not a floating sticker.
* **Trash continuity:** T1 is the focus, T2 is behind/right at the same fixed
  anchor, T3 is a quiet distant blue glint. T4–T6 may sit outside the crop but
  their absence is camera crop, not removal.
* **Layers / depth:** T1's bottom 2–4 px soften into local aqua; a small ripple
  is offset down-right, not a target ring. Waterfall sludge stays fully opaque
  and motionless in the background.
* **Cut logic:** hard cut on the pink of T1 to S03's green T2, with matching
  water value. No dissolve or swish-pan.

### S03 — center oblique: the water has volume (0:04.60–0:06.60, 2.00 s)

* **Framing / lens:** high three-quarter oblique, 55 mm-equivalent; frame a
  diagonal slice of the pool from T2 through T3. This is a painted perspective
  study, not a 3D top camera. T2 is 105–120 px; T3 is 85–100 px.
* **Camera path:** a restrained generated drift from left-rear toward
  center-east, no more than 5% framing change. Preserve the rear water edge,
  underwater-window reflection bands, and the south coping corner as depth
  references.
* **Spatial orientation:** looking south-east from behind the waterfall plane;
  the waterfall remains left of the crop and the seahorse pedestal peeks at the
  far-right edge so the viewer knows this is the same chamber.
* **Roshan:** her upper body and rainbow tail occupy the lower-left quarter,
  leaning forward in a concerned inspection pose. Gaze follows the line from
  T2 to T3; no tool is in hand. Keep the face unobscured and about 190–220 px
  tall in this closer composition.
* **Trash continuity:** T2 is the focal dented can; T3 sits farther east with a
  smaller apparent scale. T1 is a soft pink mark at the west edge; T4–T6 remain
  farther south and are not re-staged.
* **Layers / depth:** stagger the contact ellipses and submerged lower edges;
  one thin aqua caustic band crosses the water, never the trash silhouettes.
  Architecture occludes the rear of T2 slightly so it belongs in the pool.
* **Cut logic:** cut on T3's blue rim to the right-front inspection in S04.
  Keep one still frame at the end for the child to register the object.

### S04 — right-front trash cluster (0:06.60–0:08.70, 2.10 s)

* **Framing / lens:** 50 mm-equivalent east-side medium shot. T4, T5, and T6
  receive three distinct readable beats in one composition rather than three
  simultaneous targets: orange leaf first, purple strip second, sponge last.
  Each is roughly 80–105 px, never giant.
* **Camera path:** a short, curved-looking composition from T4 toward T6,
  achieved by three complete generated views with a stable horizon; no
  translated static layer and no fake rack focus.
* **Spatial orientation:** looking west/north-west from the east shelf side.
  The seahorse pedestal and long snout are present in the rear-right third;
  the left waterfall is only a muted olive vertical at the far-left edge.
* **Roshan:** torso and face remain in the left third, turned east toward the
  trash cluster. One open hand is held near her chest as a noticing gesture,
  never reaching the objects. Scale about 210–230 px head-to-tail; face stays
  clear beside the cluster.
* **Trash continuity:** T4 is nearest and largest, T5 slightly behind/right,
  T6 farther east and slightly smaller. Do not merge T5 with the seahorse's
  mouth plug; the plug remains visibly attached to the nozzle in the rear.
* **Layers / depth:** the front coping can occlude a sliver of T6's lower edge;
  each object has a different contact-ellipse angle, all aqua/lavender and
  local. The seahorse emits no water.
* **Cut logic:** cut from T5's purple shape to the matching purple seaweed at
  the seahorse nozzle in S05, making the causal problem legible without a
  cleanup action.

### S05 — seahorse obstruction and Roshan's reaction (0:08.70–0:11.20, 2.50 s)

* **Framing / lens:** 70 mm-equivalent intimate two-subject composition,
  still a complete 16:9 frame. Seahorse head/nozzle fills the right-center;
  keep eye, crest, pedestal contact, east shelf, and some water volume visible.
  The obstruction must be large enough to read on a phone, but not enlarged
  beyond its canonical snout relationship.
* **Camera path:** a gentle generated push toward the nozzle, then a short
  settle. The fixture center remains `(921.875,245.625)` in the room map; no
  pan drifts it toward frame center by accident.
* **Spatial orientation:** east-side eye-line toward the west; Roshan is in
  the left foreground, seahorse facing left toward her. This is the same
  right-center fixture, not a new animal or reverse angle.
* **Roshan:** three-quarter profile, head and shoulders clear at left, gaze
  locked on the mouth. Her hand stops short of the plug; no gripping, pulling,
  stretching, or rescue contact occurs in Video 01. Tail tip may be a soft
  foreground anchor below-left.
* **Trash continuity:** T1–T6 are out of focus only by composition, never
  recolored or deleted. The separate pink wrapper/weed plug and seaweed growth
  are visibly lodged behind the nozzle edge, with one tiny local plum/aqua seam
  shadow. Do not use the clean seahorse stream from the integration plate.
* **Layers / depth:** nozzle edge occludes the root of the plug; the plug tail
  projects forward. A narrow waterline and pedestal shadow establish that the
  seahorse is standing in the pool, not pasted over it.
* **Cut logic:** hard cut on Roshan's concerned gaze back to the room-wide
  problem map. No sparkle, hand, crop, or motion blur may hide the obstruction.

### S06 — return to the same room / open question (0:11.20–0:13.40, 2.20 s)

* **Framing / lens:** return to the S01 wide, 30–32 mm-equivalent. The six
  trash pieces, left waterfall, right seahorse, and Roshan all read together.
  Match S01's architecture and fixture scale closely enough to prove spatial
  continuity, while allowing a tiny rightward composition bias toward the
  seahorse.
* **Camera path:** a new full-frame pullback/settle, no post-render reverse
  zoom. Keep the south coping as a stable foreground arc and the underwater
  window between fixtures.
* **Spatial orientation:** same south-rim-to-north view as S01. Do not rotate,
  mirror, or relight the room.
* **Roshan:** now centered-left at approximately `(345,535)`, upright and
  attentive, gaze alternating once from the trash field to the seahorse. Tail
  remains behind the coping; no celebratory pose.
* **Trash continuity:** T1–T6 are all readable at their original anchors. The
  wrapper/weed plug remains in the seahorse mouth. The basket is still empty
  at the south-east rim. No object has moved toward it.
* **Layers / depth:** quiet local contacts only; keep the dirty water low-energy
  but not a full-screen teal wash. Preserve the room's broad painted value
  bands and cool/aqua shadows.
* **Cut logic:** end on a clean hard cut or a short authored still into the
  interactive game state. Do not tease the clean waterfall, Rumi, or a reward
  with a hidden glow at the edge of frame.

## Full-frame generation prompt block

Use this as the base prompt for every shot, replacing only the bracketed shot
line. Each changed timeline frame is a newly generated whole 16:9 image and
must carry its own prompt hash, attempt number, neighboring accepted-frame
references, subject geometry, and human identity/topology/style review.

```text
VIDEO 01 / MERMAID POOL / SHOT [S01–S06] / [TIMECODE]

Create one complete newly drawn 16:9 landscape frame in the approved polished
flattened 2D storybook style. This is the SAME Mermaid Pool chamber in every
shot: cream pearl coping, lavender shell arches, left-center pearl waterfall,
central underwater window, right-center long-snouted seahorse fountain, and
east shell bookshelf. Preserve the exact supplied V4 fixture identities,
silhouettes, proportions, pivots, and geography. Use rounded hand-painted
forms, deep navy/plum contours, broad value bands, aqua/lavender shadows, and
restrained wet accents. Make the room feel like a real shallow pool through
waterline occlusion, submerged lower edges, contact ripples, pedestal shadow,
overlap, and a rear-to-front water value change; remain a polished 2D
storybook image, never a photorealistic or 3D render.

CURRENT SHOT BEAT: [paste the exact S01–S06 beat and Roshan/trash staging here]

Continuity map: delivery canvas 1280x720; waterfall center (461.875,216.25),
dirty waterfall V4 bounds (386.25,112.5,151.25,207.5); seahorse center
(921.875,245.625), V4 bounds (817.5,125,208.75,241.25). Roshan is the
approved brown-haired girl with rainbow streak, pink top, rainbow tail. Keep
the six fixed harmless trash anchors and their material identities. The sick
seahorse has seaweed growth and a soggy pink wrapper/weed plug visibly lodged
in its mouth/nozzle; root the plug behind the nozzle edge.

OPENING STATE ONLY: the waterfall is opaque olive-brown turgid rank sludge,
completely still and non-flowing/non-glowing. No rainbow, sparkle, fresh splash,
cyan stream, foam, luminous backlight, or clean stripe. The seahorse emits no
water. Roshan only notices/inspects; she does not skim, scrub, pull, touch the
plug, or trigger a payoff. Rumi/Violet is absent. The basket remains empty.

Natural integration is staging guidance only; do not copy its clean seahorse
flow or any plate pixels. Return a single complete frame, no layers, cutouts,
text, UI, pointer, target rings, global colour wash, second pool, or overlay
graphics.
```

## Explicit do-not list

- Do not show cleanup payoff, clean waterfall, rainbow surge, healthy seahorse,
  celebration, star burst, sparkle reward, or any implied before/after wipe.
- Do not reveal Rumi/Violet, a second mermaid, a face in the pool, or a hidden
  silhouette that reads as a reveal.
- Do not make the waterfall flow, glow, foam, splash, shimmer, or emit cyan
  water. The dirty curtain is opaque, olive-brown, turgid, and still.
- Do not remove, stretch, pull, or relocate the seahorse mouth plug. It stays
  visibly lodged with seaweed growth; no injury or distress acting.
- Do not turn the six trash pieces into giant repeated product renders, labels,
  readable text, hazards, target circles, or floating UI cards. They are small,
  harmless, water-contacted, and fixed by T1–T6.
- Do not use the clean seahorse stream in the natural-integration reference;
  that plate is staging-only and wrong for this opening.
- Do not redraw, move, mirror, enlarge, or independently reinterpret the V4
  waterfall/seahorse fixtures. Background apertures are blurred by design;
  separate V4 cards remain geometry authority.
- Do not flatten the pool into a theater backdrop. Keep architecture, waterline,
  rear-to-front water value, occlusion, pedestal contact, and south coping depth.
- Do not add a second graphic pool, full-screen teal veil, broad ring field,
  pointer, HUD, button, text, checkerboard edge, white halo, sticker rim, black
  outline halo, photorealism, 3D render, mesh, spatial light, or lens effect.
- Do not hide Roshan's face/body in a close shot; her approved identity must
  remain a visible context anchor even when trash is the focal subject.
- Do not use tweening, morphing, optical flow, cross-dissolve, translated
  cutouts, sprite/rig animation, procedural warping, camera-layer translation,
  or duplicated frames to supply motion. Intentional inspection holds are
  allowed only when listed as holds in the regeneration manifest.

## Self-score against the binding rubric

This is a storyboard score, not owner acceptance or a final-frame score.
`DL-VIS-07` means no visual plan can claim 5/5 until the complete frames are
reviewed in runtime context and accepted by the owner.

| Family | Planned score | Evidence / remaining gate |
| --- | ---: | --- |
| `DL-VIS-01–06` identity and painted material | 4/5 | Exact V4 fixture geography, approved Roshan, quiet broad bands, and local aqua contacts are specified; actual generated frames still need identity/style review. |
| `DL-READ-01–06` child-readable hierarchy | 4/5 | One focal trash beat per shot, Roshan visible, six fixed IDs, no words/UI; M11/small-phone squint and observed-child review remain open. |
| `DL-MOT-01–06` acting, contact, camera | 4/5 | Inspection arc has anticipation/settle and gentle predictable reframing; no cleanup action is intentionally shown. Generated frame-to-frame topology and camera continuity remain to be audited. |
| `DL-CIN-01–06` flattened cinematic contract | 4/5 target | Six hard-cut shot groups and explicit full-frame generation are defined; acceptance requires native 1280×720 candidates, hashes, prompt records, neighboring references, and `audit_cinematic.py`. |
| Spatial continuity / depth | 4/5 | Stable 1024→1280 map, exact fixture centers, six trash anchors, occlusion and water-volume cues; final candidate review must reject drift or theater-flat staging. |
| Audio/editorial readiness | 3/5 | Timing and cut points are ready for Luna's later ambience/foley pass; no final music, voice, or protected family recording is assumed here. |

**Overall storyboard target: 4/5, with a credible path to owner-reviewed 5/5.**
The blocking risks are subject drift in generated close views, accidental clean
water/glow, T1 versus the separate mouth plug being conflated, and camera crops
that lose the room landmarks. These are acceptance gates, not reasons to relax
the continuity map.

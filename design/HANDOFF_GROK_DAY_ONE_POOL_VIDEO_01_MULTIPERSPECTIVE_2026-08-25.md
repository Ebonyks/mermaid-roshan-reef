# Owner-run Grok handoff — Mermaid Pool Video 01: The Pool Is Sick

> **SUPERSEDED 2026-08-25:** the owner rejected this storyboard's repeated
> theater-flat camera grammar and style drift. Do not use its frames or prompts
> as Grok authority. The current handoff is
> `HANDOFF_GROK_DAY_ONE_POOL_VIDEO_01_FULL_CHAMBER_2026-08-25.md`; the current
> accepted package is
> `assets_src/imagegen/day_one_pool_video_01_storyboard_replacement_2026-08-25/`.

## Use and authority

This is the shot-specific, copy/pasteable **visual-only** handoff for the first
10–15 second Mermaid Pool film. It supplements, and does not replace, the
larger cleanup-and-Rumi sequence in
`design/HANDOFF_GROK_DAY_ONE_POOL_NEXT_ANIMATION_2026-08-23.md`.

The owner performs every Grok upload, submission, and download. Grok may
produce visual candidates but may not reorder the six shots, start the cleanup,
reveal Rumi, choose audio, or approve its own output. Codex/Luna review is the
technical/editorial gate; owner review in context is final. An automated review
score is capped at 4.9/5 because `DL-VIS-07` reserves 5/5 for owner acceptance.

Do not upload protected family voice files. Do not ask Grok for music, voices,
foley, ambience, or a final mix. Any returned audio is disposable sync
reference. This package makes no public-marketing or external-reuse grant.

## Film outcome

Deliver one **13.4-second, 16:9 landscape, visual-only** candidate. Roshan
enters the same dirty Mermaid Pool bathing chamber, looks across the room, and
the film examines the trash, stagnant waterfall, and blocked seahorse from six
different but spatially continuous perspectives. The final frame ends on
Roshan understanding the problem. Nothing is cleaned in Video 01.

“Life-like and comprehensive” means a convincing inhabited 2D room: continuous
architecture, a real shallow water plane, rear waterline, coping overlap,
pedestal contact, occlusion, local ripples, and consistent near/far scale. It
does **not** mean photorealism, a 3D camera, PBR surfaces, or a theater set.

## Branch and package

- Working branch: `codex/grok-pool-cinematic-handoff`
- Package root:
  `assets_src/imagegen/day_one_pool_video_01_storyboard_2026-08-25/`
- Accepted storyboard natives:
  `assets_src/imagegen/day_one_pool_video_01_storyboard_2026-08-25/accepted/`
- Rejected-attempt evidence:
  `assets_src/imagegen/day_one_pool_video_01_storyboard_2026-08-25/rejected/`
- Prompt/provenance and candidate scores:
  `assets_src/imagegen/day_one_pool_video_01_storyboard_2026-08-25/PROMPTS_AND_PROVENANCE.md`
- Independent Luna rubric/results:
  `design/review/day_one_pool_video_01_2026-08-25/`

## Owner upload set

Upload these five canonical appearance references first:

1. `assets/flats/castle/interactions_v4/backgrounds/room_mermaid_pool_background.png`
2. `assets/castle/day_one_pool/activities/waterfall_clogged_original_match.png`
3. `assets/castle/day_one_pool/activities/seahorse_sick_clear_mouth.png`
4. `assets/castle/day_one_pool/activities/seahorse_mouth_trash.png`
5. `assets/characters/roshan_25d/roshan_base.png`

Then upload the six accepted storyboard frames in order:

1. `accepted/S01_wide_arrival_attempt02.png`
2. `accepted/S02_wrapper_can_attempt02.png`
3. `accepted/S03_center_oblique_attempt01.png`
4. `accepted/S04_right_trash_cluster_attempt01.png`
5. `accepted/S05_seahorse_obstruction_attempt01.png`
6. `accepted/S06_return_wide_attempt02.png`

`STORYBOARD_CONTACT_SHEET.png` is a convenient visual index only. Use the six
individual native frames—not the contact sheet—as the appearance/composition
references for generation.

Reference-role limits:

- The background PNG intentionally has softened/removed fixture apertures.
  Reconstruct the actual fixture identities from the separate dirty waterfall
  and sick seahorse references; never invent a generic fountain.
- The natural-integration plate may be consulted for contact and depth only.
  Its clean flowing seahorse water is wrong for Video 01 and must not appear.
- Storyboard frames set camera, composition, acting, palette, and continuity.
  They are reference-only; Grok must return new complete full frames rather
  than translating or collaging these pixels.

## Non-negotiable room truth

- Fixed orientation: north/back wall at the rear, waterfall west/left-center,
  underwater window center, seahorse east/right-center, south pearl coping in
  the foreground. Never mirror the room.
- Waterfall: opaque olive-brown turgid rank sludge, fully stagnant and blocked.
  No rainbow, cyan flow, foam, splash, shimmer, glow, or luminous backlight.
- Seahorse: the same long-snouted V4 fountain, sick but sympathetic, waterless,
  with sparse seaweed growth and a **bright soggy pink wrapper plus olive
  seaweed plug visibly lodged inside its mouth/nozzle**. The nozzle lip overlaps
  the obstruction root. A green weed clump without the pink wrapper fails.
- Roshan: the approved child mermaid—tiara, brown hair with rainbow
  ponytail/streak, pink ruffled top, pearlescent lavender/aqua tail, rainbow
  fins. Preserve her child face, proportions, costume, and topology.
- Six harmless floating objects keep stable identities and geography: pink
  star wrapper, dented can, blue ring/lid, orange leaf, purple strip, yellow
  sponge. Each has a small local aqua/lavender contact ripple and submerged
  lower edge; none is a UI target or product render.
- Rumi/Violet is absent. No substitute mermaid, face in the water, hidden
  silhouette, cleaning tool, payoff, reward, or clean-state teaser appears.

## Stable 1280×720 continuity map

| Element | Stage anchor | Rule |
|---|---:|---|
| Dirty waterfall center | `(461.875, 216.25)` | left-center, exact V4 identity, stagnant |
| Sick seahorse center | `(921.875, 245.625)` | right-center, exact V4 identity, mouth plug present |
| T1 pink wrapper | `(385, 323)` | rear-mid left water |
| T2 dented can | `(541, 299)` | behind/right of T1 |
| T3 blue ring/lid | `(772, 338)` | mid-water east of center |
| T4 orange leaf | `(495, 459)` | near-left water |
| T5 purple strip | `(657, 459)` | near-center water |
| T6 yellow sponge | `(918, 458)` | near-east water |

Treat these as normalized spatial anchors when the generation canvas differs.
Perspective may change apparent scale and crop, but it may not move an object
to a different part of the room. S02 and S03 intentionally crop the seahorse
head completely out; they do not remove or clean it off-camera.

## Locked 13.4-second shot script

| Shot | Time | Camera and content | Required end beat |
|---|---:|---|---|
| **S01 — wide arrival** | `0:00–0:02.40` | 30 mm-equivalent view north from the south rim. Full room, six trash pieces, waterfall left-center, seahorse right-center. Roshan stops at lower-left coping. Very gentle 3% compositional settle. | Roshan’s gaze lands on T1; pink seahorse mouth plug remains readable. |
| **S02 — wrapper and can** | `0:02.40–0:04.60` | Low west-side 45 mm view from the shell steps. T1 wrapper is primary, T2 can behind/right, T3 a distant glint. Seahorse is fully outside the crop. | Brief still inspection of wrapper/can; waterfall remains opaque and still. |
| **S03 — water-volume oblique** | `0:04.60–0:06.60` | High painted three-quarter 55 mm view across T2 to T3. Rear water edge, window reflections, and south coping corner prove depth. Seahorse head remains outside crop. | Hold long enough to register can and lid at different depths. |
| **S04 — right trash cluster** | `0:06.60–0:08.70` | East-side 50 mm view. Read T4 leaf, then T5 strip, then T6 sponge. Seahorse is rear-right and mouth obstruction remains pink + green. | Match T5 purple shape to the seahorse’s body growth without conflating the two. |
| **S05 — mouth obstruction** | `0:08.70–0:11.20` | Intimate 70 mm two-subject frame. Roshan left foreground; seahorse head/nozzle right-center. Gentle push and settle. | Roshan’s hand stops short; pink wrapper/seaweed plug is clearly inside nozzle. No rescue contact. |
| **S06 — return wide** | `0:11.20–0:13.40` | New full-frame wide matching S01 with a slight rightward bias. Roshan is attentive at center-left; six trash pieces and both fixtures remain dirty. | End on a short authored still, ready to hard-cut into gameplay. No basket or tool. |

Use hard cuts only between shots. Camera motion within a shot is gentle,
predictable, and subordinate to the inspection. Do not use a dissolve, swish
pan, fake rack focus, abrupt yaw, translated background, or motion blur to hide
subject drift.

## Copy/paste Grok master prompt

```text
Create one 13.4-second visual-only 16:9 landscape cinematic called “The Pool
Is Sick,” using the six supplied accepted storyboard frames as ordered camera,
composition, character, palette, and spatial-continuity references. Return to
the SAME Mermaid Pool bathing chamber in all six shots. Use hard cuts at 2.40,
4.60, 6.60, 8.70, and 11.20 seconds. Follow the locked S01–S06 shot script
exactly; do not remove, merge, reorder, or add shots.

Render the established polished flattened 2D children’s storybook style:
rounded hand-painted forms, clean navy/plum contours, broad painted value
bands, aqua/lavender shadows, and restrained wet accents. Make the room feel
spatially comprehensive through continuous shell architecture, a visible rear
waterline, rear-to-front water value, foreground pearl coping, pedestal
contact, partial occlusion, and small local ripples. Remain 2D storybook art;
never become photorealistic, 3D, PBR, or a theater set.

Roshan is the supplied approved child mermaid with tiara, brown hair and
rainbow ponytail/streak, pink ruffled top, pearlescent lavender/aqua scaled
tail, and rainbow fins. Preserve her exact child face, proportions, costume,
anatomy, and identity in every visible frame.

DIRTY OPENING STATE ONLY. The left-center pearl waterfall is blocked by opaque
olive-brown turgid rank sludge and is completely still, non-flowing, and
non-glowing. Never show rainbow, cyan water, foam, splash, sparkle, clean lane,
or luminous backlight. The right-center long-snouted seahorse emits no water,
has sparse seaweed growth, and keeps a bright soggy PINK folded wrapper braided
with olive seaweed visibly jammed INSIDE its mouth/nozzle; the nozzle lip
overlaps the plug root. Do not replace it with only a green weed clump.

Keep the same six harmless trash identities and geography: pink star wrapper,
dented can, blue ring/lid, orange leaf, purple strip, yellow sponge. They stay
inert and naturally water-anchored. Roshan only notices and inspects. No
skimming, scrubbing, pulling, touching the plug, basket, tool, cleaned object,
reward, rainbow surge, healthy fountain, Rumi/Violet, substitute mermaid, or
extra character appears.

No text, UI, pointer, target rings, cards, full-screen tint, second pool,
proscenium, curtain, spotlight, sticker rim, white halo, black outline halo,
watermark, copied layer, translated plate, sprite/cutout animation, rig,
morph, optical flow, cross-dissolve, or duplicated action frame. Produce newly
drawn complete flattened full frames. Any audio is disposable sync reference.
```

## Per-shot Grok reminder

Before each shot request, append the matching row from the locked shot script
and upload that accepted storyboard frame. Repeat these lines every time:

```text
This is one shot of the same room, not a redesign. Preserve fixture identity,
room orientation, Roshan identity, and fixed trash geography. The waterfall is
opaque olive-brown turgid stagnant sludge with zero flow or glow. Whenever the
seahorse mouth is visible, the bright pink wrapper plus olive seaweed plug is
unmistakably lodged inside the nozzle. Return complete full frames; no layers,
cutouts, interpolation, UI, audio decisions, cleanup, reward, or Rumi.
```

## Candidate review and regeneration contract

Every returned shot receives the Luna rubric in
`design/review/day_one_pool_video_01_2026-08-25/LUNA_CANDIDATE_AUDIT.md`.

- Hard threshold: **4.5/5**, no knockout. Automated/documentary maximum: 4.9.
- A failed shot is regenerated as a fresh complete full-frame attempt at the
  same timeline index; use a single targeted repair and increment attempt.
- Maximum: 20 attempts per shot. Attempt 20 never relaxes the gate; unresolved
  work escalates to the owner.
- Preserve every attempt, prompt hash, candidate hash, native dimensions,
  neighboring accepted references, subject geometry, and identity/topology/
  style review. Rejected frames never become continuity authority.
- A cinematic candidate is not delivery merely because Grok produced a smooth
  MP4. Extract and review the exact frame sequence. The binding full-frame rule
  rejects tweening, morphing, optical flow, cross-dissolve, translated cutouts,
  sprite/rig animation, procedural warping, or duplicated frames used to hide
  missing acting or camera action.
- Final score 5/5, device/child acceptance, audio, and release remain owner-led
  external gates.

## Grok completion return package

Return to Codex/Luna, without making editorial changes:

1. native 16:9 visual-only shot clips and combined 13.4-second candidate;
2. lossless extracted frame sequence for every shot;
3. exact prompts and generation settings per attempt;
4. native file hashes and dimensions;
5. declared method and any holds;
6. mapping from every frame to S01–S06 and neighboring accepted references;
7. no protected family audio.

The owner decides whether a candidate may advance. Grok does not self-certify
style, identity, continuity, full-frame compliance, or 5/5 acceptance.

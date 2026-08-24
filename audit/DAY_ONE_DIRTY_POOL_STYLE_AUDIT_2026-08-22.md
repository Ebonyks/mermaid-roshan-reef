# Day One Dirty Pool style congruence audit — updated 2026-08-23

## Verdict

**Overall master-audit rating: 3/5 — usable, with bounded acceptance gaps.**

The generic four-click cleanup has been replaced by three causal, one-finger
activities: skim six visible pieces of trash, scrub three clogged waterfall
lanes, then tap eight times to pull the blockage from the seahorse's mouth.
There is no timer, loss, reset, or reading dependency. Partial progress is
saved monotonically. The first two games must finish before the seahorse rescue
unlocks, and the lighting, rainbow surge, healthy fountain, and Rumi reveal are
reserved for the final extraction.

The replacement waterfall is registered from the live V4 fixture's source
rectangle rather than an independent guessed position. In the dirty arrival it
fully replaces the rainbow with a still olive sludge curtain, embedded litter,
and a blocked basin. Rumi uses the approved Violet identity and the existing
authored swim, wave, and idle art; no substitute mermaid is present.

The feature earns 3/5 rather than 4/5 because several new activity props are
sharper and glossier than the room's soft painted background, and because M11,
small-phone, child, owner, and final voice acceptance are still open. These are
bounded review gaps, not a reason to revert to the prior generic interaction.

## Authority and evidence

- Rating meanings: `audit/MASTER_AUDIT_2026-08-09.md` §1.1.
- Binding families: `DL-VIS-01`–`08`, `DL-READ-01`–`06`,
  `DL-INT-02`–`03`, `DL-MOT-01`–`07`, and `DL-SND-01`–`05` in
  `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`.
- Clean visual anchors: the accepted Mermaid Pool V4 background, waterfall
  rest card and sheet, and seahorse rest card and sheet. The live waterfall
  center resolves to `(461.875, 216.25)` on the 1280×720 stage; the seahorse
  center resolves to `(921.875, 245.625)`.
- Rumi identity authority remains the owner-confirmed Violet package from
  commit `975d7e86291a5e5b69ffb417bfba45cf184ef756` and the existing pool swim
  atlas. Protected character sources were not modified or regenerated.
- `python tools/audit_lighting_images.py assets/castle/day_one_pool/activities
  assets/characters/rumi` scanned nine runtime images with zero unreadable.
  The seven activity assets measure luminance p50 0.32, dynamic range 0.88,
  0% crushed, 0.4% blown, and 10° hue shift. The two approved Rumi atlases
  measure luminance p50 0.33, dynamic range 0.69, 0% crushed, and 0% blown.
- Every new runtime texture is RGBA and no larger than 1024 pixels on its
  longest edge. Native generated files, prompts, hashes, rejected attempts,
  and non-destructive runtime derivations are recorded in
  `assets_src/imagegen/day_one_pool_activities_2026-08-23/PROVENANCE.md`.
- Exact Godot 4.7.1 focused gameplay validation passes all 25 checks with no
  script errors. It covers ordered ownership, passive non-advance, six actual
  catches, three independent scrub lanes, eight monotonic rescue taps,
  persistence, correct V4 registration, stopped pre-finale fixture water,
  Rumi identity/action order, finale, and teardown.
- The dedicated Forward Mobile capture passes all nine states at 2560×1369:
  dirty arrival, skimmer catch, pool clear/clogged fixture, waterfall scrub,
  cleaned-static fixture, midway seahorse tug, trash release, rainbow surge,
  and Rumi reveal.

## Asset and activity findings

| Asset/activity | Rating | Congruent strengths | Remaining gap |
|---|---:|---|---|
| Mermaid Pool V4 room and fixtures | 4/5 anchor | Pastel shell architecture, broad aqua pool, readable pearl waterfall and long-snouted seahorse | Target-device acceptance remains external to this review |
| Skimmer game | 3/5 | Six distinct, harmless objects; oversized net; circular touch targets; catch flight, basket landing, ripples, bubbles, and sparkles make contact truthful | Net, basket, and trash have more specular detail than the room anchor |
| Clogged waterfall game | 3/5 | Uses the live V4 center and aspect; complete stagnant curtain hides the rainbow; three lanes reveal truthfully; no clean animated water before finale | Olive curtain remains visually sharper than the soft architectural paint; owner/M11 review open |
| Seahorse rescue | 3/5 | Correct species/pose and long nozzle; trash visibly projects from the mouth; eight taps stretch the plug toward a basket; healthy card replaces it only after release | Generated sick card is more saturated than the clean rest card; phone identity comparison open |
| Rumi reveal | 4/5 | Correct Violet/Rumi: enormous violet braid, pointed ears, navy sea-jacket, shell clasp, aqua-lavender tail, coral fins; authored swim, wave, idle | Exact authorized spoken thank-you/introduction and device acceptance remain open |
| Ordered composition | 4/5 | One active target, direct pointer, no fail state, truthful removal, progressive light recovery, and a strong final reward | Final child/owner playtest and audio mix remain open |

The superseded `pool_algae_trash.png`, `pool_rim_grime.png`,
`waterfall_growth.png`, `waterfall_clogged_turgid.png`, and old monolithic
`seahorse_sick.png` are not loaded by the new activity controller. They remain
historical provenance only and do not set the live sequence's score.

## Rule-level result

| Rule family | Result | Reason |
|---|---|---|
| True 2D / runtime size | **Pass** | Canvas-only activities and ≤1024 RGBA textures; no new 3D debt |
| Identity | **Pass** | Live V4 fixture registration, corrected mouth obstruction, and approved Rumi art |
| Child readability | **Pass with review gap** | One active subject, oversized tools, picture-first prompts, no loss; smallest-phone playtest pending |
| Truthful interaction/motion | **Pass** | Trash travels into basket, scrubbed lanes uncover the clean card, mouth plug visibly stretches and releases |
| Save/no-fail contract | **Pass** | Monotonic masks/tug count; legacy cleanup step normalized; no timer or reset |
| Material/style congruence | **3/5** | Strong contour/palette family, but props are glossier and higher-frequency than the room anchor |
| Audio | **Coverage gap** | Objectives have visual and `_say()` cues; final authorized Rumi line and Luna mix review require an actual cut |
| Device/owner evidence | **Coverage gap** | Exact desktop Mobile render and probes pass; M11, smallest-phone, child, and owner acceptance remain open |

## Bounded next review

1. Run the nine-state sequence on the M11 and smallest supported phone.
2. Verify that each drag/tap reads without adult explanation and that the mouth
   blockage remains legible under a thumb.
3. Record or authorize Rumi's exact thank-you/introduction line; never replace
   protected family voices.
4. When an actual next-scene cut exists, assign Luna the video for music,
   ambience, foley, timing, and placeholder-voice review. Grok is visual only.
5. Owner acceptance is final; this audit and generator output are advisory.

The copy/pasteable visual-generation brief is in
`design/HANDOFF_GROK_DAY_ONE_POOL_NEXT_ANIMATION_2026-08-23.md`.

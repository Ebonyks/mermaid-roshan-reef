# 4-way basic swim — 2026-09-14

Owner asked for different directional profiles, 4-way, focused on the basic
swimming animation. This is **not** delivery. `DELIVERY_ACCEPTED` stays false.

Launch, arrival, and personality are out of scope for this packet. Those still
live on the front-right take-03 basis (RSW-01 / 06 / 03 / 05).

## Owner inspection — 2026-09-15

Recorded, not repaired in this packet:

- Hair/tail colour corrections remain **outstanding**. Do not treat these
  stills or clips as colour-corrected masters.
- The navy-flattened `locked-4way-*.png` openings **cannot establish clean
  hair alpha**. Do not key, flood-fill, or recover fringe from the navy plates.
- Hair alpha authority remains the existing RGBA 8-view cutouts:
  `references/{front,right,back,left}.png`.
- These remain motion references. Nothing was merged. Runtime is unchanged.

## Method

- IMAGE_1 = painted 8-view cutouts composited onto navy RGB(17,37,54), 1280×720.
  Body height 580px, centered, so the fin has room to travel. No character redraw.
- Tool = `imagine_image_to_video` (animate the still). Not `reference_to_video`.
- Cardinal views only: front, right, back, left.
- Energy: reserved in-place cruise at walking pace, with **broad tail strokes**,
  changing full-body posture, hands near the body, trailing hair.
- Native 10.04s / 1280×720 / 24 fps / AAC stereo. Requested 8s silent still unsupported.

## Openings

Navy plates are observation-field IMAGE_1 only.

| View | Locked opening SHA-256 | 8-view RGBA cutout SHA-256 |
| --- | --- | --- |
| front | `b53d2d6c535179581bdf72988de8b7d53a00f15544cf7c9b1ddef2d5ccf20b02` | `a716ce355dd3bd35add0a6b3fa76219ce23fef25fe7c8c41b90b745c8ab06150` |
| right | `e2062eb39c8a39abb600894a7e1ea9f8ffd67ce6faed68f93b6c2f4587c1a7c4` | `5f2eec477d00de4625c3dc501de71739fcb2e27ce3c76de6aac9dc464dcf5825` |
| back | `a45e0fbec08cc5e87a0c3db9442937449d5166e54d4be4f8ab1c357e8b6261f3` | `aa6c3865a88f608fe82bbee3233daf915f5f3404a5bed459246534c4cd32dfd7` |
| left | `901ac7474a21faba7b2a95836cae339bd1328c95845e623b2984caa4237c319f` | `9c13fccbe44a9a961d7eb27cd7951be507476a99043fc38dd38af4cca6bdc5e4` |

## Takes

| Shot | SHA-256 | Disposition | Measure |
| --- | --- | --- | --- |
| RSW-SWIM-FRONT | `efc7b8669936569d36739f05d10c849e6cbe23ebae56bb94c77353ebbb60e2b9` | comparison_candidate | t4–t5.5 tail. Discard raised arms and end smile. |
| RSW-SWIM-RIGHT | `685bae4461ebe42e9520e33e4a6556d4ca3286b9d8f5709f7e94b3e0065c6550` | comparison_candidate | t4–t8 full stroke. Strongest clip. |
| RSW-SWIM-BACK | `50795b0fcef726419cf74fb127da696982428de0979e6cc7c7e2d6cbd6b0b2fd` | comparison_candidate | t2.5–t5.5 stroke. Discard late 3/4 drift. |
| RSW-SWIM-LEFT | `a619712ab5daafefbedaa0033fe6b202ce95f340df02127e24e43a8364b5e94c` | comparison_candidate | t4–t5.5 tail. Discard late camera ease. |

Reel `FOURWAY_REEL.mp4` SHA-256 `52bbc7cecf5b7ee1446f7215d23a7a736ad9172ae78158878a9ce1a11a0253f1`
(45.15s, navy slates, straight cuts).

## Core art

Identity holds on all four: painted storybook Roshan, gold crown with one gem,
rainbow streak on anatomical left, pink bodice, lilac frills, pearlescent tail.
No bun. No silver crown. No extra fauna. No invented jewelry.

Knockouts that are not identity: front arms rise at t2.5; several clips ease
camera-ward at the end; back drifts off pure back after t8; native 10s + AAC.

No ghosted resets in sampled frames. Do not reuse RSW-07 / RSW-08 as loops.

## Do not

- Treat these as cinematic or Godot / runtime delivery
- Convert here in Aseprite — that is Codex's job
- Recover hair alpha from the navy openings
- Treat colour as corrected
- Adapt take-01
- Merge to master or dev
- Set `DELIVERY_ACCEPTED`

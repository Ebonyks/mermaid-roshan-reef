# D1-C03-S03 - swimming bunny reveal

DRAFT - human first-frame approval pending. Motion reference only.

replace unstable bunny/tub scale while preserving discovery event

Game seam: follows threshold entry; ends before basket/tool reach

Source: C03_bunny_discover.mp4; zero-based half-open select [12, 84].

Weak source evidence: [[12, 84]]. Sampled visual evidence, not every-frame acceptance.

## First frame for approval

Sol: RECOMMEND_APPROVAL. Candidate SHA-256: `ad731205c722ff37ec749750871e7e30051cb187a36fd43cf05cd3f676347ea6`.

![D1-C03-S03 opening](../../first_frames/luna_a_C03-S03_swimming_bunny_attempt02_DIRTY_MURKY.png)

## Narrative board - never bind to Grok

![D1-C03-S03 board](../../storyboards/luna_a_C03-S03_storyboard_2x2_attempt02_DIRTY_MURKY.png)



## Bind only these images after approval

- [IMAGE_1 - approved_clean_first_frame](../../first_frames/luna_a_C03-S03_swimming_bunny_attempt02_DIRTY_MURKY.png)

- [IMAGE_2 - subject_identity](../../references/69827625a8_roshan_base.png)

- [IMAGE_3 - subject_identity](../../references/d788366485_dust_bunny_swimming.png)


## Shot and frame instructions

[Paste-ready single-shot prompt](PROMPT.txt) | [Every target-frame prompt](FRAME_PROMPTS.txt) | [Frame plan JSON](FRAME_PLAN.json) | [Shot card](SHOT_PACKET.json)

```text
locked camera on the first-frame layout in IMAGE_1. 0.00–0.75s: One small purple swimming bunny is separately visible in shallow murky tub water; Roshan watches without reaching in. 0.75–1.50s: The bunny paddles one short gentle arc, staying the same size and clear of the tub rim. 1.50–2.25s: Roshan tracks it with her eyes and a small head tilt; hands remain outside the water. 2.25–3.00s: Hold the discovery with one intact bunny and dirty tub still clearly readable. keep room geometry and bound identities fixed. Exactly one bunny, no mound becoming a character or second bunny. Dirty tub, shallow murky water, sink and mirror do not clean or change scale. No tool, pickup, reaching contact, adult or camera move. no HUD, text, morphing or camera drift. end: One small swimming bunny remains in the murky tub while Roshan watches, ready to help.
Sound: small water ripples and bubbles; no voices.
```

## Direct underlying game references

- [room_bubble_bath_dirty_drained_day_one.png](../../references/1382a8adcb_room_bubble_bath_dirty_drained_day_one.png) - source `assets/flats/castle/rooms/room_bubble_bath_dirty_drained_day_one.png`

- [dust_bunny_swimming.png](../../references/d788366485_dust_bunny_swimming.png) - source `assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_swimming.png`

- [roshan_base.png](../../references/69827625a8_roshan_base.png) - source `assets/characters/roshan_25d/roshan_base.png`


## Current source frames - audit only

![Exact source-frame samples](../../audit/source_frames/D1-C03-S03/AUDIT_SAMPLES.jpg)

[Individual source frames and index manifest](../../audit/source_frames/D1-C03-S03/SAMPLE_MANIFEST.json)


The source game assets above control event/state and location. A gameplay capture or generated board must never supply generation pixels. The first frame controls the new shot only after your explicit approval.

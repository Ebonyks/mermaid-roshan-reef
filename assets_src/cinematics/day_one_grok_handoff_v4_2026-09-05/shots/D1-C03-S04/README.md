# D1-C03-S04 - basket tool precontact

DRAFT - human first-frame approval pending. Motion reference only.

replace hand/tool scale instability; this is precontact only

Game seam: follows bunny discovery; ends before game-owned pickup

Source: C03_S04_v1_tool_reach.mp4; zero-based half-open select [24, 96].

Weak source evidence: [[24, 96]]. Sampled visual evidence, not every-frame acceptance.

## First frame for approval

Sol: RECOMMEND_APPROVAL. Candidate SHA-256: `85935bf017b2693bd1e55f85d4f0b65cb71e1eedbf2a091575842c3d5a0749c9`.

![D1-C03-S04 opening](../../first_frames/luna_a_C03-S04_precontact_reach.png)

## Narrative board - never bind to Grok

![D1-C03-S04 board](../../storyboards/D1-C03-S04_STORYBOARD_candidate02.png)



## Bind only these images after approval

- [IMAGE_1 - approved_clean_first_frame](../../first_frames/luna_a_C03-S04_precontact_reach.png)

- [IMAGE_2 - subject_identity](../../references/69827625a8_roshan_base.png)

- [IMAGE_3 - object_or_material_identity](../../references/7c4f39ef35_tool_star_sponge.png)


## Shot and frame instructions

[Paste-ready single-shot prompt](PROMPT.txt) | [Every target-frame prompt](FRAME_PROMPTS.txt) | [Frame plan JSON](FRAME_PLAN.json) | [Shot card](SHOT_PACKET.json)

```text
locked camera on the first-frame layout in IMAGE_1. 0.00–0.75s: Roshan faces the fixed cleanup basket; its pink sponge is still inside and her reaching hand has a visible gap. 0.75–1.50s: She makes one small forward glide and upper-body lean toward the fixed basket, bringing her reaching hand nearer without stretching the arm; the other hand remains near her chest. 1.50–2.25s: Her fingertip stops visibly short of the sponge; no touch, pickup or movement of basket contents. 2.25–3.00s: Hold the deliberate precontact gap, ready for the game-owned tool pickup. keep room geometry and bound identities fixed. Same dirty bathroom and fixed basket location beside the sink. Exactly one approved pink tool_star_sponge; one reaching arm and one quiet arm. No contact, pickup, clean-room transformation, star cushion, exclamation graphic or extra cast. no HUD, text, morphing or camera drift. end: Roshan's fingertip is visibly short of the pink sponge inside the fixed basket.
Sound: bathroom room tone and light basket rattle; no voices.
```

## Direct underlying game references

- [room_bubble_bath_dirty_drained_day_one.png](../../references/1382a8adcb_room_bubble_bath_dirty_drained_day_one.png) - source `assets/flats/castle/rooms/room_bubble_bath_dirty_drained_day_one.png`

- [cleanup_basket.png](../../references/30b43ce7b1_cleanup_basket.png) - source `assets/castle/day_one_pool/activities/cleanup_basket.png`

- [tool_star_sponge.png](../../references/7c4f39ef35_tool_star_sponge.png) - source `assets/castle/dirty_cleanup_2d/tools/tool_star_sponge.png`

- [roshan_base.png](../../references/69827625a8_roshan_base.png) - source `assets/characters/roshan_25d/roshan_base.png`


## Current source frames - audit only

![Exact source-frame samples](../../audit/source_frames/D1-C03-S04/AUDIT_SAMPLES.jpg)

[Individual source frames and index manifest](../../audit/source_frames/D1-C03-S04/SAMPLE_MANIFEST.json)


The source game assets above control event/state and location. A gameplay capture or generated board must never supply generation pixels. The first frame controls the new shot only after your explicit approval.

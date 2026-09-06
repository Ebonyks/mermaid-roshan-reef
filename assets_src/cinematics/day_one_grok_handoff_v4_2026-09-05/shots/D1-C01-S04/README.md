# D1-C01-S04 - closed-door arrival

DRAFT - human first-frame approval pending. Motion reference only.

owner-requested dry Sky Lagoon castle arrival after the full otter opening; replaces rejected underwater old-gate staging

Game seam: follows owner-selected full otter opening; ends on the dry stone landing before the closed four-tower castle door

Source: Missing coverage; no current source frames; zero-based half-open select None.

Weak source evidence: []. Sampled visual evidence, not every-frame acceptance.

## First frame for approval

Sol: RECOMMEND_APPROVAL. Candidate SHA-256: `c6f0e578f84dffb69364e8481be8de99fac02bed8b04a998c36cc8c13525d091`.

![D1-C01-S04 opening](../../first_frames/D1-C01-S04_OPENING_candidate04_SKY_LAGOON.png)

## Narrative board - never bind to Grok

![D1-C01-S04 board](../../storyboards/OWNER_C01-S04_BOARD_candidate01.png)



## Bind only these images after approval

- [IMAGE_1 - approved_clean_first_frame](../../first_frames/D1-C01-S04_OPENING_candidate04_SKY_LAGOON.png)

- [IMAGE_2 - subject_identity](../../references/2eda6f7676_daddy_daddy_master.png)

- [IMAGE_3 - subject_identity](../../references/69827625a8_roshan_base.png)


## Shot and frame instructions

[Paste-ready single-shot prompt](PROMPT.txt) | [Every target-frame prompt](FRAME_PROMPTS.txt) | [Frame plan JSON](FRAME_PLAN.json) | [Shot card](SHOT_PACKET.json)

```text
locked camera on the approved first-frame layout. 0.00–0.75s: Daddy and Roshan, already holding hands, make one short approach over the dry bridge and foreground stone landing. 0.75–1.50s: Their joined hands remain stable as they ease to a stop before the closed red double door. 1.50–2.25s: They look up at the four-tower castle and Roshan stained glass; neither reaches for a handle. 2.25–3.00s: Hold the dry closed-door arrival tableau. Keep room geometry and bound identities fixed. Current four-tower castle, central Roshan stained glass, wooden bridge and closed red double door stay fixed. Bright Sky Lagoon sky, mountains, meadow vegetation and foreground stone landing remain dry; no moat, stream, seabed or underwater light. Exactly Daddy and child Roshan with joined but separately readable hands; no Rumi, door opening, handle contact, legs or extra cast. No HUD, text, morphing or camera drift. End: Daddy and child Roshan pause hand-in-hand on the dry landing before the closed four-tower castle doors.
Sound: open-sky breeze, meadow ambience and two soft tail swishes; no voices
```

## Direct underlying game references

- [sky_lagoon_castle_four_tower_v4.png](../../references/08e3b85035_sky_lagoon_castle_four_tower_v4.png) - source `assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png`

- [sky_lagoon_panorama_1536.png](../../references/74bc5a0643_sky_lagoon_panorama_1536.png) - source `assets_src/cinematics/day_one_grok_handoff_v4_2026-09-05/references/normalized/sky_lagoon_panorama_1536.png`

- [sky_lagoon_layout.json](../../written_guide/dad9fee760_sky_lagoon_layout.json.txt) - source `scripts/arena/sky_lagoon_layout.json`

- [daddy_daddy_master.png](../../references/2eda6f7676_daddy_daddy_master.png) - source `assets_src/cinematics/day_one_grok_handoff_v3_2026-09-04/scenes/D1-C01/visuals/handoff_art/characters/daddy_daddy_master.png`

- [roshan_base.png](../../references/69827625a8_roshan_base.png) - source `assets/characters/roshan_25d/roshan_base.png`


The source game assets above control event/state and location. A gameplay capture or generated board must never supply generation pixels. The first frame controls the new shot only after your explicit approval.

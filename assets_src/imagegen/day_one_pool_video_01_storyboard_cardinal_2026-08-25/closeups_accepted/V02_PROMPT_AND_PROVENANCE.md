# Dirty seahorse close-up v02 — prompt and provenance

## Candidate record

- Asset: `dirty_seahorse_closeup_v02.png`
- Built-in ImageGen result ID: `exec-aa806da1-9c70-4f74-8338-5668cf05a3bc`
- Generation method: OpenAI built-in ImageGen; fresh complete flattened frame
- Attempt: `3/20` overall seahorse close-up attempts (v01 rejected; v02 attempt 01 rejected for long body/tail vines)
- Intended timeline: locked editorial `CU-SH`, `3.00–4.00 s`, hard cut between CU-WF and S02 East
- Native dimensions: `1672×941` (16:9)
- SHA-256: `C8F6D98C82EC5CAACA1D423168F647460C3D6F1068E2E2184AC337110545630C`
- Prompt SHA-256 (UTF-8 bytes of the exact fenced prompt below): `40d8391d0bf2aa45298c5efa7ab36a2c0429e1dbafbce7f630a27e7998d2d616`
- Status: `AUDIT_PASS_OWNER_PENDING`

## Neighbor references

| Role | Path | SHA-256 |
|---|---|---|
| Previous neighbor, CU-WF | `assets_src/imagegen/day_one_pool_video_01_storyboard_cardinal_2026-08-25/closeups_accepted/dirty_waterfall_closeup_v02b.png` | `9B98443D48373158F1D7CA0F9DE5071B17A5F83BDAC6760BA238463BDFFEFC96` |
| Next neighbor, S02 East `090°` | `assets_src/imagegen/day_one_pool_video_01_storyboard_cardinal_2026-08-25/accepted/S02_E_cardinal.png` | `3ADFE2A3F34F05DDC4FB170F73D0E93FBA40E243B81593FF0CE52A0B6D94E5EA` |
| Upstream room context, S01 North `000°` | `assets_src/imagegen/day_one_pool_video_01_storyboard_cardinal_2026-08-25/accepted/S01_N_cardinal_return.png` | `777F44C65B2C76B3DC4595ADD5C6ED6CC44F297E7BF81A48D116FC3027D65223` |
| Roshan identity reference | `assets/characters/roshan_25d/roshan_base.png` | `69827625A8A795F1303C90A465454DD8529F10D5401C78911D00B90BE8D1E1AB` |

## Source roles

1. `assets/castle/day_one_pool/seahorse_sick.png` — exact blue/turquoise long-snouted fixture anatomy and crest; long body vines explicitly rejected as appearance guidance.
2. `assets/castle/day_one_pool/activities/seahorse_mouth_trash.png` — one pink folded wrapper and modest olive mouth-root obstruction.
3. S01 North — canonical north-wall architecture, dirty pool value and matte storybook style.
4. `assets/characters/roshan_25d/roshan_base.png` — approved child identity for the quiet left-edge context anchor.
5. S02 East — shelf/arch continuity and rightward exit direction.

No source pixels were cropped, composited, pasted, mirrored, translated, interpolated or used as delivery pixels. No position guide was used.

## Geometry and continuity record

Approximate normalized subject geometry in the native frame (`x`, `y`, `w`, `h`):

- Seahorse head-to-pedestal silhouette: `(0.491, 0.145, 0.277, 0.768)`.
- Roshan face/torso/tail context anchor: `(0.002, 0.351, 0.194, 0.536)`; fully readable at the left edge and secondary to the fixture.
- Mouth wrapper/seaweed contact: `(0.523, 0.370, 0.057, 0.080)`; wrapper is visibly lodged at the nozzle with a short rooted tuft.
- Pool waterline: approximately `y=0.625`; shelf/arch remains visible on the right; pedestal contact is visible.

The frame is a modest `1.35–1.55×` equivalent close-up relative to S01 while retaining the full head-to-pedestal silhouette, curled tail, mouth seam, shelf/arch, pool waterline and room context. It exits visually to the right toward S02 East.

## Exact generation prompt

```text
Use case: illustration-story
Asset type: final candidate v02 for the CU-SH dirty-seahorse editorial insert in the Day One Mermaid Pool cinematic handoff
Reference roles: Image 1 supplies only the exact blue/turquoise long-snouted seahorse anatomy and purple crest; explicitly ignore its long decorative body vines. Image 2 supplies only the exact pink folded wrapper and modest olive mouth-root obstruction. Image 3 is the accepted north-wall room, dirty-water palette, matte storybook style, and Roshan scale. Image 4 is the approved Roshan identity. Image 5 is the accepted east-wall neighbor for shelf/arch and rightward continuity.
Hard visual acceptance test before returning: the seahorse’s blue torso, peach belly, curled tail and pearl pedestal must be plainly visible and mostly free of green vine bands. There must be NO continuous vine around the torso, NO vine around the tail, and NO vine wrapping the pedestal. Allow only one short olive seaweed tuft at the mouth root plus two or three tiny algae spots near the crest/neck and one tiny stain on the pedestal. If a long body/tail vine appears, regenerate instead of returning it.
Scene/backdrop: one complete Mermaid Pool north-wall chamber, not a product studio. Preserve the shell masonry, right towel shelf/arch, pearl coping and pedestal contact, murky blue-green pool waterline, and a sliver of the underwater window. Maintain the same room geometry as Image 3.
Subject: the exact sympathetic sick seahorse fixture, blue/turquoise long snout, lavender-pink snout, purple scalloped crest, peach segmented belly, curled tail and pearl-stone pedestal. A single bright-pink folded wrapper is clearly lodged in the mouth, with a short olive seaweed tuft rooted behind the nozzle lip and a contact shadow. No water is emitted.
Roshan context: place exactly one approved Roshan at the far left/lower-left edge, fully readable face, tiara, chest/torso and visible continuous rainbow tail, occupying about 15–25% of the frame as a quiet observer. Keep her small, still, empty-handed and secondary; do not crop her face or make her the focal subject.
Style/medium: complete flattened hand-painted 2D children’s storybook game frame matching Image 3, broad matte value bands, deep indigo/plum contours, aqua/lavender shadows, restrained wet accents, cohesive painted architecture. No glossy product render, no 3D/PBR.
Composition/framing: fresh native 1672×941 landscape 16:9 full frame, modest 1.35–1.55x equivalent close-up relative to Image 3. Show the seahorse’s complete head-to-pedestal silhouette, intact snout/nozzle seam, curled tail, right shelf/arch edge, pool waterline, and enough room context. Seahorse is right-center; Roshan is a small left-edge anchor. This is a newly drawn full room frame, never a crop, zoom, pan, translated plate, composite, cutout, mirror, or overlay.
Lighting/mood: same dingy muted north-wall lighting, subdued olive reflections from stagnant dirty pool, gentle concern and child-safe sympathy.
Constraints: one room, one pool, one seahorse, one Roshan; no water from the mouth; keep wrapper and mouth-root tuft legible; keep the body and tail clean enough to read.
Avoid: long seaweed torso wrap, long seaweed tail wrap, pedestal wrap, excessive growth, algae belt, extra vine, duplicate wrapper, missing wrapper, clean water, stream, spray, foam, rainbow, glow, reward, cleanup, tools, skimmer, basket, Rumi, extra mermaid, UI, text, labels, watermark, photorealism, anime, 3D render, PBR, horror, gore, isolated asset render.
```

The generated source remains at `C:/Users/Peter/.codex/generated_images/01a03b76-a566-7fb2-bb68-eb64ad1b68ce/exec-aa806da1-9c70-4f74-8338-5668cf05a3bc.png`; the package copy is unchanged.

# Day One Mermaid Pool Video 01 storyboard — prompts and provenance

Generated 2026-08-25 with the built-in OpenAI image-generation tool. Each
attempt was one independent fresh complete flattened full-frame generation.
No candidate was made by compositing, translating, tweening, morphing,
optical-flow interpolation, cross-dissolve, sprite/cutout animation, rigging,
procedural warp, or duplicated action frame. No position guide was used.

These images are **storyboard and Grok composition references**, not accepted
cinematic delivery frames. Owner runtime acceptance remains open. The native
files are preserved byte-exact; the `delivery_1280x720/` copies are permitted
whole-canvas resolution normalizations made only after the six natives passed
the independent visual gate.

## Generation method and source roles

- Tool: OpenAI built-in `image_gen`, one call per attempt.
- Use case: `illustration-story`.
- Method declaration: `fresh_full_frame_generation`.
- Position guide: not used; no guide pixels exist.
- Protected sources: not modified or overwritten.
- Appearance references: project-owned room, V4 fixture/activity, Roshan, and
  previously accepted neighboring storyboard frames. A neighbor supplied
  continuity/style context only and contributed no copied delivery pixels.
- Prompt records: the nine `.txt` files under `prompts/` are the verbatim prompt
  strings passed to the built-in tool, transcribed from the tool calls. Their
  hashes below are SHA-256 of the UTF-8 working-tree files with LF endings.

## Attempt ledger

| Shot | Attempt | Status | Built-in result | Native candidate / SHA-256 | Prompt / SHA-256 | Decision |
|---|---:|---|---|---|---|---|
| S01 | 1 | `REJECT_KNOCKOUT` | `exec-4fdbc073-f07f-4dc7-be7d-73a53a9cc29a.png` | `rejected/S01_wide_arrival_attempt01_fail_mouth_contact.png` / `edeacee48b104cbcde266a2d86e2b35a231208b0023de6aa0bf76cdb316d85c2` | `prompts/S01_attempt01_rejected.txt` / `b81b10e527a125e0e3855603ccea753a0b08763bdead418aeb6ddacc0a35bcb2` | Pink wrapper not unmistakable in mouth. |
| S01 | 2 | `AUDIT_PASS_OWNER_PENDING` | `exec-3554129b-a72b-427d-9f0a-45938f95e541.png` | `accepted/S01_wide_arrival_attempt02.png` / `92b354db479b51fe1a3b3fbadd96c007f955c10c484caac9263700d44f119f4b` | `prompts/S01_attempt02.txt` / `6ebd8d297b979dd7cb15b09e94ac79c2eb5e615df2df2bb587198f7213b318e7` | Corrected bright pink wrapper + seaweed contact; 4.70/5. |
| S02 | 1 | `REJECT_KNOCKOUT` | `exec-4791eb86-08c0-48aa-956b-af07485cd5b9.png` | `rejected/S02_wrapper_can_attempt01_fail_mouth_continuity.png` / `544d477d27441cb9da184b5f494a3813fb334b42f25cc22d3dd55f7976b065bb` | `prompts/S02_attempt01_rejected.txt` / `0bc954d7fe321fbe8f33adbc9d1566df1e8580dc1aa96f82365d6d35ddfd6d44` | Distant visible seahorse mouth could not pass the obstruction check. |
| S02 | 2 | `AUDIT_PASS_OWNER_PENDING` | `exec-ecf386f8-7def-41c0-b824-9354ea7d8b89.png` | `accepted/S02_wrapper_can_attempt02.png` / `0f91a01da322f736d09a39048a1a8554912d9d9cfdb4591b22a667adaaee9dc8` | `prompts/S02_attempt02.txt` / `e63530b6fad19e405a1ff6f05f31d31abb3f85f80791b001d7250a7eec5dea25` | Deliberate seahorse crop; strong wrapper/can depth; 4.74/5. |
| S03 | 1 | `AUDIT_PASS_OWNER_PENDING` | `exec-e44a586f-b712-4431-a5f7-5d19bd5da639.png` | `accepted/S03_center_oblique_attempt01.png` / `cf94a2ce739d12500583d2f64aefa2cfdd462700e683b6f796bfca2765fbbcce` | `prompts/S03_attempt01.txt` / `18b01393db1f78778ca4fe85363793f4ebd8cef5e441749c4fc29823480ff588` | Painted oblique water-volume shot; 4.66/5. |
| S04 | 1 | `AUDIT_PASS_OWNER_PENDING` | `exec-ba89ca7b-b239-4e64-9991-e16997fbc57b.png` | `accepted/S04_right_trash_cluster_attempt01.png` / `df479b6273aae9e8d48ba97bcfe01c9dd01c03b72e07934c5e642e8a59510629` | `prompts/S04_attempt01.txt` / `2c6db205b076843f97971292c5f39e848c4a7649eb176ada5b43f2d4b3ee1ec8` | Clear three-object cluster and mouth continuity; 4.72/5. |
| S05 | 1 | `AUDIT_PASS_OWNER_PENDING` | `exec-381524a9-e7ac-48b8-aa7e-072566230745.png` | `accepted/S05_seahorse_obstruction_attempt01.png` / `ab04f23e08c8a95b49ae3da0c880a4fb80110bec7ee4247e0281604d553619af` | `prompts/S05_attempt01.txt` / `c812dcb23c0b5219173502f683d29a4a08644b4e85e59afd722fd168b2ca900a` | Mouth obstruction and stop-short hand are unambiguous; 4.68/5. |
| S06 | 1 | `REJECT_KNOCKOUT` | `exec-f6f6d32e-1d42-4684-a5b1-ecf5436a4e7c.png` | `rejected/S06_return_wide_attempt01_fail_generic_basket.png` / `f3d4662148a95c216f2327ad3dcfadeba2fdd2522699ea015d5759b1b976ea9e` | `prompts/S06_attempt01_rejected.txt` / `002cb47c10312c8415f76e5b8c0757b736ac39d7318522e955c02968691b8a3a` | Generic wicker basket broke scene-specific integration. |
| S06 | 2 | `AUDIT_PASS_OWNER_PENDING` | `exec-bd42de20-a157-4a0d-af4e-2eecd254b05e.png` | `accepted/S06_return_wide_attempt02.png` / `bb3297da6672290da08a8b526f0d7cc6e1bde51fb2182e9c9dfe3be3e403a393` | `prompts/S06_attempt02.txt` / `75592862b81ddb7c8d9e2e384d33320a583fb3e1346261838d2be2191eddca39` | Intentional no-basket opening-film frame; 4.58/5. |

## Accepted timeline, neighbors, and declared state

All accepted natives are `1672×941`, landscape, square-pixel PNGs with no
rotation metadata. The native ratio is `1672 / 941 ≈ 1.7768331562`, a
near-16:9 image-generation output. It is preserved as generated and is not
described as exact 16:9 delivery.

| Shot | Time | Declared action / hold | Previous accepted reference | Next accepted reference |
|---|---:|---|---|---|
| S01 | `0.00–2.40` | Roshan arrival/notice key; short directed inspection settle at end | none | S02 / `0f91a01d…9dc8` |
| S02 | `2.40–4.60` | Wrapper-and-can inspection key; short recognition settle | S01 / `92b354db…9f4b` | S03 / `cf94a2ce…bcce` |
| S03 | `4.60–6.60` | Painted oblique inspection key; directed object-registration hold | S02 / `0f91a01d…9dc8` | S04 / `df479b62…0629` |
| S04 | `6.60–8.70` | Right trash-cluster inspection key; no touch | S03 / `cf94a2ce…bcce` | S05 / `ab04f23e…19af` |
| S05 | `8.70–11.20` | Mouth-obstruction recognition; Roshan’s hand stops short | S04 / `df479b62…0629` | S06 / `bb3297da…a393` |
| S06 | `11.20–13.40` | Return-wide problem map; authored final still before gameplay cut | S05 / `ab04f23e…19af` | none |

The stills above are storyboard keys. They do not authorize duplicating a frame
to conceal required motion in the later film. Every changed delivered frame
must obey the full-frame cinematic contract.

## Approximate normalized subject geometry and contact review

Values are human review estimates on the complete native frames, recorded to
make drift visible in the Grok pass. They are not masks and supplied no pixels
to generation.

| Shot | Roshan bbox `(x,y,w,h)` | Active subject bbox | Fixture / mouth notes | Contact and spatial continuity |
|---|---|---|---|---|
| S01 | `(0.07,0.46,0.24,0.54)` | trash field `(0.27,0.49,0.40,0.30)` | waterfall center ~`(0.35,0.26)`; seahorse ~`(0.71,0.36)`; plug ~`(0.62,0.31,0.08,0.08)` | Six local water ripples; coping occludes Roshan tail; plug root behind nozzle. |
| S02 | `(0.00,0.20,0.34,0.76)` | wrapper/can `(0.38,0.55,0.36,0.27)` | waterfall center ~`(0.55,0.25)`; seahorse intentionally out of crop | Low waterline and coping contact; T1/T2 lower edges submerged. |
| S03 | `(0.00,0.29,0.34,0.70)` | can-to-lid line `(0.40,0.42,0.42,0.29)` | dirty waterfall upper-left; seahorse head intentionally out of crop | Rear water edge, reflection bands, and south coping corner preserve volume. |
| S04 | `(0.04,0.34,0.31,0.59)` | T4–T6 `(0.37,0.64,0.42,0.17)` | waterfall far-left; seahorse ~`(0.78,0.30)`; plug ~`(0.67,0.27,0.08,0.09)` | Three distinct local ripples; pedestal water contact; T5 separate from plug. |
| S05 | `(0.02,0.29,0.45,0.71)` | seahorse/nozzle `(0.63,0.06,0.35,0.85)` | plug ~`(0.64,0.32,0.11,0.15)`; dirty waterfall remains left | Open air gap between Roshan hand and plug; nozzle overlaps plug root; pedestal ripple. |
| S06 | `(0.10,0.45,0.22,0.54)` | trash field `(0.27,0.49,0.39,0.28)` | waterfall ~`(0.35,0.26)`; seahorse ~`(0.71,0.36)`; plug ~`(0.62,0.31,0.08,0.08)` | Matches S01 wide geography; six water contacts; no basket/tool by design. |

## Human identity, topology, style, and phone-readability review

- Sol orchestration review, 2026-08-25: all six accepted frames preserve the
  approved Roshan child identity, one tail, complete visible hands/face,
  storybook material language, and the declared shot. S01, S04, S05, and S06
  visibly show pink wrapper + olive seaweed rooted in the mouth. S02 and S03
  crop the seahorse head entirely by design.
- Independent Luna review, 2026-08-25: scores and per-shot caveats are recorded
  in `design/review/day_one_pool_video_01_2026-08-25/CANDIDATE_AUDIT_RESULTS.md`.
  Every accepted native scored at least 4.5/5 with no visual knockout.
- Phone-size squint review: Roshan, the declared trash focal object, dirty
  waterfall, and—when present—the mouth plug remain legible at reduced view.
  Actual supported-phone/M11, child, and owner acceptance remain open.
- Rumi/extra-mermaid check: not present in any accepted or rejected candidate.
- Method check: each result came directly from one built-in image-generation
  call as a complete flattened image; no local appearance edit was made to a
  native candidate.

## Exact whole-canvas delivery normalization

After the six native storyboard candidates passed the visual gate, FFmpeg
8.1.2 applied one complete-canvas Lanczos scale from `1672×941` to `1280×720`:

```text
ffmpeg -i <accepted-native> -vf scale=1280:720:flags=lanczos -frames:v 1 <delivery-copy>
```

There was no crop, mask, layer isolation, translation, compositing, subject
repair, or alpha edit. Native files and hashes remain above.

| Delivery copy | SHA-256 |
|---|---|
| `delivery_1280x720/S01_wide_arrival_attempt02.png` | `432ca7248eceda6bc117bba7401622d815ba275226d443fd5ce4afa89b79dcbe` |
| `delivery_1280x720/S02_wrapper_can_attempt02.png` | `2c679d373e4c5bda020f3b81881d81b667d49fd84eac614f47275707a40fa4cd` |
| `delivery_1280x720/S03_center_oblique_attempt01.png` | `aa010282528203d837d4a96aefde5dcb0a7bb490319450ef25340cb8c83ba936` |
| `delivery_1280x720/S04_right_trash_cluster_attempt01.png` | `d6b7c0865dd96d3fdf7f8f72c5c0223cbe42a030586869087f8a9d270bff52ba` |
| `delivery_1280x720/S05_seahorse_obstruction_attempt01.png` | `4d7130b4ed45c67e38dd5928ae4bc00c4b44c2c9e1d91ca59525de8180415698` |
| `delivery_1280x720/S06_return_wide_attempt02.png` | `850fa161daca4846c6f6d10325dbdf8a7ceb3a97cb9e4a95ab5d75ba4d7de711` |

`STORYBOARD_CONTACT_SHEET.png` is a deterministic review-only 3×2 layout of
the six exact `1280×720` copies in S01–S06 reading order, with no labels or
appearance edit. It was built by whole-frame downscaling each copy to 640×360
and `xstack` placement only. SHA-256:
`5552fe8ceef5f6dddc39feeae0ab7e20c2e301f514b716e5753d733237c3b31e`.

## Acceptance boundary

The six accepted storyboard frames are `AUDIT_PASS_OWNER_PENDING` for this
reference package only. Scores are capped below 5. They are not final Grok
video frames, do not prove temporal continuity, and do not close the required
`tools/audit_cinematic.py`, target-device, child, audio, or owner gates. The
three rejected attempts remain evidence and must never be used as Grok
continuity references.

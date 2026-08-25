# Luna candidate audit results — Day One Mermaid Pool Video 01

**Review date:** 2026-08-25
**Reviewer:** Luna, independent visual audit
**Shot plan:** `design/review/day_one_pool_video_01_2026-08-25/LUNA_SHOT_DESIGN.md`
**Rubric:** `design/review/day_one_pool_video_01_2026-08-25/LUNA_CANDIDATE_AUDIT.md`

## Overall verdict

All six accepted paths pass the storyboard-reference gate at **≥4.5/5.0** with
no observed knockout. They are `AUDIT_PASS_OWNER_PENDING` for this reference
package, not final cinematic acceptance. The preserved natives are `1672x941`
landscape PNGs (`1672 / 941 ≈ 1.7768331562`), a near-16:9 image-generation
output rather than native `1280x720` delivery. After the visual gate, one
whole-canvas FFmpeg 8.1.2 Lanczos scale produced exact `1280x720` review copies
without crop, mask, compositing, translation, or subject repair; native files
and hashes remain preserved.

Exact per-attempt prompt records/hashes, built-in fresh-full-frame method,
candidate/delivery hashes, neighboring accepted references, declared
action/hold states, approximate normalized geometry, and Sol + independent
Luna identity/topology/style review are recorded in
`assets_src/imagegen/day_one_pool_video_01_storyboard_2026-08-25/PROMPTS_AND_PROVENANCE.md`.
The later Grok film still requires complete temporal/frame evidence,
`tools/audit_cinematic.py`, and owner review of the exact runtime cut.

Common visual pass findings: every accepted frame is a complete flattened
storybook image; the waterfall is opaque olive-brown, still, and non-glowing;
Roshan is the approved brown-haired, rainbow-streak, pink-top, rainbow-tail
identity; the pool has visible waterline/contact ripples and pearl-coping
occlusion; no Rumi/Violet, cleanup action, clean stripe, rainbow surge, UI,
theater-flat overlay, photorealism, or 3D treatment is visible.

## Accepted candidates

Scores are out of 5.0 and capped at 4.9 for this documentary audit. The status
means visual pass pending provenance, target-device, child, and owner review.

| Shot / candidate | Attempt(s) | SHA-256 | Score | Status | Observed evidence / caveat |
|---|---:|---|---:|---|---|
| **S01** `accepted/S01_wide_arrival_attempt02.png` | 2 | `92b354db479b51fe1a3b3fbadd96c007f955c10c484caac9263700d44f119f4b` | **4.70** | `AUDIT_PASS_OWNER_PENDING` | Strong wide room map: all six trash pieces read with local ripples; waterfall remains opaque/still; seahorse has unmistakable bright pink wrapper and seaweed lodged in the nozzle; Roshan is clear at lower-left. Lower tail is naturally cropped by coping. Full prompt/neighbor/method/geometry records and exact 1280×720 review copy are in the package provenance. |
| **S02** `accepted/S02_wrapper_can_attempt02.png` | 2 | `0f91a01da322f736d09a39048a1a8554912d9d9cfdb4591b22a667adaaee9dc8` | **4.74** | `AUDIT_PASS_OWNER_PENDING` | Correct west-side low inspection. T1 pink wrapper and T2 can have water contact and readable scale; Roshan's face/hand/tail depth reads. Seahorse is deliberately cropped completely out, not omitted from the room canon; dirty waterfall stays fully opaque in the background. No mouth check applies inside this crop. |
| **S03** `accepted/S03_center_oblique_attempt01.png` | 1 | `cf94a2ce739d12500583d2f64aefa2cfdd462700e683b6f796bfca2765fbbcce` | **4.66** | `AUDIT_PASS_OWNER_PENDING` | T2 can is the clear center focal subject and T3 blue lid bridges the cut; T1 remains a small west-edge continuity mark; staggered ripples and coping give water volume. Seahorse is deliberately cropped completely out. Slightly tighter oblique crop reduces landmark coverage, so neighbor geometry must be measured before final acceptance. |
| **S04** `accepted/S04_right_trash_cluster_attempt01.png` | 1 | `df479b6273aae9e8d48ba97bcfe01c9dd01c03b72e07934c5e642e8a59510629` | **4.72** | `AUDIT_PASS_OWNER_PENDING` | T4 leaf, T5 purple strip, and T6 sponge are distinct, water-anchored, and not giant cards; Roshan remains readable at left; seahorse is rear-right with bright pink wrapper plus seaweed clearly in the mouth. Dirty waterfall is only a quiet olive vertical at far-left, with no flow/glow. T5 remains separate from the mouth plug. |
| **S05** `accepted/S05_seahorse_obstruction_attempt01.png` | 1 | `ab04f23e08c8a95b49ae3da0c880a4fb80110bec7ee4247e0281604d553619af` | **4.68** | `AUDIT_PASS_OWNER_PENDING` | Intimate two-subject frame preserves the same long-snouted seahorse, eye, crest, pedestal, shelf, and water contact. Bright pink wrapper and green seaweed are unmistakably rooted behind the nozzle; Roshan's hand stops short, with no rescue pull. Waterfall remains a quiet dirty curtain at left; no Rumi/cleanup/payoff. Close framing is near the scale ceiling, so phone-size squint and neighbor fixture-center review remain required. |
| **S06** `accepted/S06_return_wide_attempt02.png` | 2 | `bb3297da6672290da08a8b526f0d7cc6e1bde51fb2182e9c9dfe3be3e403a393` | **4.58** | `AUDIT_PASS_OWNER_PENDING` | Return-wide room map is coherent with S01: six trash pieces, still dirty waterfall, right seahorse, and Roshan all read; bright pink mouth wrapper plus seaweed remain visible; no reward/Rumi/cleanup action. The open south-east coping intentionally contains no basket or tool. The rejected wicker-basket attempt proved why all basket imagery is reserved for later gameplay, not Video 01. |

### Score breakdown

| Shot | Identity / 1.25 | Beat & spatial truth / 1.25 | Natural style / 1.00 | Child read / 0.75 | Cinematic craft / 0.75 | Raw / capped score |
|---|---:|---:|---:|---:|---:|---:|
| S01 | 1.20 | 1.18 | 0.94 | 0.69 | 0.69 | 4.70 |
| S02 | 1.20 | 1.19 | 0.95 | 0.70 | 0.70 | 4.74 |
| S03 | 1.18 | 1.15 | 0.94 | 0.68 | 0.71 | 4.66 |
| S04 | 1.20 | 1.18 | 0.95 | 0.70 | 0.69 | 4.72 |
| S05 | 1.19 | 1.20 | 0.93 | 0.68 | 0.68 | 4.68 |
| S06 | 1.19 | 1.13 | 0.93 | 0.67 | 0.66 | 4.58 |

No accepted candidate is below 4.5, so no further storyboard-frame regeneration
is ordered. Video 01 intentionally contains no basket or cleaning tool; the
approved shell cleanup basket remains available for later gameplay only.

## Preserved rejected attempts

These files remain evidence and are not delivery candidates.

| Shot / rejected candidate | Attempt | SHA-256 | Status | Failure reason |
|---|---:|---|---|---|
| **S01** `rejected/S01_wide_arrival_attempt01_fail_mouth_contact.png` | 1 | `edeacee48b104cbcde266a2d86e2b35a231208b0023de6aa0bf76cdb316d85c2` | `REJECT_KNOCKOUT` | Seahorse mouth reads as a small purple ring/cup-like obstruction; the required bright pink wrapper plus seaweed is not unmistakably lodged in the nozzle. This fails the S01 mouth-contact identity gate despite otherwise dirty room/water. |
| **S02** `rejected/S02_wrapper_can_attempt01_fail_mouth_continuity.png` | 1 | `544d477d27441cb9da184b5f494a3813fb334b42f25cc22d3dd55f7976b065bb` | `REJECT_KNOCKOUT` | Seahorse remains visible in the far-right background instead of being deliberately cropped completely out for S02, and its mouth obstruction is too small to verify. The frame therefore fails both the declared S02 crop grammar and mouth-continuity evidence. |
| **S06** `rejected/S06_return_wide_attempt01_fail_generic_basket.png` | 1 | `f3d4662148a95c216f2327ad3dcfadeba2fdd2522699ea015d5759b1b976ea9e` | `REJECT_KNOCKOUT` | South-east prop is a generic wicker basket, not an allowed Video 01 prop. It reads as a detached generic/clip-art prop and breaks the room-specific natural-integration contract. Accepted S06 correctly removes it; the no-basket opening-film contract is intentional. |

## Next evidence required before final acceptance

- [x] Package one record per candidate: exact timeline index, candidate
  path/hash, prompt hash, attempt, fresh generation method, action/hold state,
  subject geometry, accepted previous/next frame paths/hashes, and human
  identity/topology/style review.
- [x] Preserve `1672x941` natives and create one post-visual-gate whole-canvas
  `1280x720` Lanczos review copy per accepted frame, with hashes and no crop.
- [ ] Run `tools/audit_cinematic.py` with no forbidden method, guide-pixel
  reuse, aspect/orientation, drift, or neighboring-frame failure.
- [ ] Review the exact cut at phone size and on the target device; Luna's score
  does not grant owner, child, or runtime acceptance.
- [x] Keep baskets/tools out of Video 01. The approved shell basket remains for
  later gameplay; never use the rejected generic wicker basket.

## Final evidence reconciliation — 2026-08-25

Luna independently recomputed and matched all six native candidate SHA-256
values, all nine verbatim prompt-file SHA-256 values, and all six normalized
`1280x720` delivery-copy SHA-256 values in
`assets_src/imagegen/day_one_pool_video_01_storyboard_2026-08-25/PROMPTS_AND_PROVENANCE.md`.
The attempt ledger, shot times/states, accepted neighbors, normalized subject
geometry/contact notes, fresh-generation method, and Sol/Luna
identity/topology/style/phone-readability review were inspected and are
present. Native `1672x941` files are correctly described as near-16:9 rather
than exact delivery; normalized copies are exact `1280x720`. The S06 attempt-02
prompt and manifest explicitly require **no basket, container, or tool of any
kind** in this opening film, so all six `AUDIT_PASS_OWNER_PENDING` statuses
remain truthful for storyboard-reference scope only. They do not close
temporal, runtime, target-device, child, audio, or owner acceptance.

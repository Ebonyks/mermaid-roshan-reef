# Racer steering-control pixel re-audit

Date: 2026-09-05
Disposition: **REJECTED_BELOW_4.5**
Scope: the bounded steering-control repair, assessed separately from the complete Racer surface.

## What the asset is

`assets/opera/worlds/widgets/widget_crank_racer_wheel.png` is a painted **tire/spare-wheel token** with a shell hub. It is not a steering wheel. The driver cutout in `assets/opera/worlds/actors/roshan_racer.png` already depicts the in-kart steering wheel. This review therefore assesses the reused asset only as a draggable race-themed token on the left/right rail. It does not describe it as a steering wheel.

The tire is polished and belongs to the same illustrated kart family. Its dark rubber ring, gold shell hub, clean alpha, and strong silhouette hold up at the rendered control size. The long cream capsule, aqua rail, and large left/right chevrons make horizontal dragging legible. The recaptured left/right endpoints show a substantial, truthful position change, and the reported runtime assertions independently reached `race_steer=-1` and `race_steer=+1`.

The semantic problem remains material. A loose tire usually implies a wheel to install, roll, or collect. It does not naturally mean “drag me left and right to steer,” especially while an actual steering wheel is visible in Roshan's hands. The arrows and rail rescue the interaction grammar, but the token itself weakens it. Its subtle rotation is visually plausible tire motion, yet it does not communicate steering angle as clearly as a steering-wheel control. This is a likely semantic regression from the former hub-and-spoke thumb, although no exact before capture is included in this evidence packet, so that comparative statement is not promoted to a proven pixel regression.

## Bounded repair score

| Dimension | Score | Evidence-based judgment |
|---|---:|---|
| Identity | 3.8 | Correct Racer/kart family, but wrong object identity for a steering control; reads as a tire or shell medallion. |
| Finish | 4.7 | Painterly material, highlight, contour, and value treatment match the polished kart art. |
| Edges | 4.7 | Clean transparent silhouette at the displayed size; no visible rectangle, chroma fringe, crop, or disconnected debris. |
| Readability | 4.2 | Large rail, arrows, and endpoint travel explain left/right drag, but the tire does not independently explain steering. |
| Animation/feedback | 4.3 | Position responds clearly at both extremes and rotation is restrained; it remains feedback motion on one static tire and the angle meaning is weak. |
| Ownership | 4.6 | The token remains centered on the same rail and appears aligned with the unchanged drag region; runtime assertions support both extrema. This is not device touch evidence. |
| Consistency | 4.6 | Strong stylistic match to kart materials and world palette, with more authored finish than the surrounding procedural rail. |
| Technical | 4.6 | Crisp at 98 px, safe alpha padding, no observed clipping, and current captures cover ready/left/right/race states. Exact device/performance and same-process provenance acceptance remain outside this review. |

Mean: **4.44/5**. Critical identity, readability, and feedback dimensions are below 4.5, so the repair cannot pass by averaging its strong finish and edges. Under the fail-closed rubric, the bounded repair is rejected.

## Full-surface review

The complete Racer surface remains below 4.5 independently of the tire decision. The painted circuit and finish frame are rich and cohesive, but the live racers are very small against a dense background. Roshan and the rival overlap heavily at several positions; the frozen/cropped upper-body actor, kart, and embedded steering wheel read as a layered cutout rather than coherent driving animation. The cream steering capsule and turbo disc occupy a large part of the lower play field and use flatter procedural forms than the background. The three lap dials now contain meaningful finish-flag icons and show completion/fraction state, so they are no longer empty counters; however, the countdown's three large flat circles remain visually plain and temporarily compete with the track.

Provisional full-surface score: **3.9/5, REVIEW_OPEN**. This is not a substitute for a complete eight-dimension, all-state, device/owner review.

## Required next repair

Retain the existing racing engine, one-finger rail, hit area, left/right chevrons, and exact state behavior. Replace the tire thumb with an approved control whose silhouette truthfully communicates steering or directional dragging. Reuse should be preferred, but the in-kart steering wheel embedded in `roshan_racer.png` is not a separable clean control asset and must not be cropped out casually. If no approved isolated steering control exists, restore the previous clearer control until a bounded art asset can be sourced. Do not alter the driver cutout as part of that control-only repair.

Re-audit ready, maximum-left, maximum-right, release-to-center, countdown, mid-lap, second-lap, and finish states at 1280x720 plus the supported wide-phone aspect. Bind each capture to the current candidate and include touch/device evidence before claiming ownership/readability acceptance.

## Evidence and hashes

All paths below were inspected from the current worktree.

| Path | SHA-256 |
|---|---|
| `tmp/art-quality/racer/02-race-ready.png` | `c1ec138a3c5e32979760e5f2f03180e168eb1c5a1e1063ea9012a9ba9fcf1d61` |
| `tmp/art-quality/racer/02-race-ready-wide.png` | `cabe53c0f717943db4bb9f6e82d6846f15644402e9f36e5913e948053ab8164c` |
| `tmp/art-quality/racer/02-steer-left.png` | `6cd123a2082269c4dc5ce57ac29cdec5c8fd723014500b22f7d217de1f06c047` |
| `tmp/art-quality/racer/02-steer-right.png` | `56c49dc8f7b4581ff83323e405dcc48e4c80649320b71595a49b5c02782a29ce` |
| `tmp/art-quality/racer/03-race-far-bend.png` | `5f8ed10be62065388ae9e767e4cced37594624d43a4d4b044393522cfd7558ef` |
| `tmp/art-quality/racer/04-second-lap.png` | `b99b3ea2d6b3c43b66030770fc298f180a55c6467c53f691b5f67f2e1ffd0716` |
| `tmp/art-quality/racer/05-finish.png` | `b58d22dc88cdb5d66937d9c13cdf37eaaec217622ec85b546e3ef8fcb759c3e9` |
| `assets/opera/worlds/widgets/widget_crank_racer_wheel.png` | `3203d9bc5297fccfb3ee86fddab6c3a217de577943a063ef37404e5276c7e003` |
| `assets/opera/worlds/actors/roshan_racer.png` | `b3e92a0f3204e2277e1fdd06988c9393288223fcfc98a9f4c8e033c8c517c6bc` |
| `scripts/opera_racer_surface.gd` | `ed8e2d7cd3a1bea4cb84402cf6891f50b6e9ffc151c9bc752cb0708ed0e396a0` |

`tmp/art-quality/racer/01-pit-stop.png` was present and hashed (`c89c455abb55d242f5051bd0d3c50c1ef4fe23fc0a180de8fc4e0ded9499f9ba`) but is outside this race-steering repair and was not used to raise its score. The supplied steering assertions were reported with this review request; no repository-relative hashed log file was present in the Racer evidence directory, so they remain reported runtime facts rather than independently provenance-bound evidence.

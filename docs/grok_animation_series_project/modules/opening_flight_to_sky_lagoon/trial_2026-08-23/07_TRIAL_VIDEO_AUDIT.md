# Grok trial video audit — 2026-08-23

## Outcome

**Overall verdict: reject as production footage; retain only as diagnostic evidence.**

The trial proves that Grok can maintain a pleasant broad palette and produce locally readable two-character images, but it does not reliably orchestrate a 42.5-second causal sequence. It responds to a long cinematic request by inventing a montage: required acting disappears, geography is revealed too early, scenic cutaways replace story beats, and spatially impossible transitions appear around the landing.

## Technical audit

| Item | Result |
|---|---|
| Resolution | Pass: 1280×720 |
| Frame rate | Pass: constant 24 fps |
| Video codec | Pass for review: H.264 |
| Audio | Pass: no audio stream |
| Duration | Fail: 46.5s versus authored 42.5s |
| Shot discipline | Fail: 20 detected montage segments, many only 1.5–3s, rather than independently approved shots |
| Production status | `REJECT_DIAGNOSTIC_ONLY` |

## Highest-severity failures

1. **Landing logic is absent.** At 29.5s the airplane is already parked directly on the playground grass/path. There is no approach, touchdown logic, six-step route, two lavender rails, or separate landing platform.
2. **PNW reference leakage becomes story content.** A river otter appears at 29.5s, grows relative to the plane, climbs onto its fuselage, then remains beside the characters. No animal belongs in this sequence.
3. **Scale collapses.** Outside, Roshan and Daddy are taller than the parked airplane cabin; the otter is large enough to climb over the aircraft. The plane cannot contain the cabin seen earlier.
4. **Time and space reverse.** After Roshan and Daddy are already outside with the otter, the video cuts back to them inside the cabin at 36.5s.
5. **The exit route is replaced by a glowing portal.** At 37.5–40.5s they pass through a bright door directly into the kingdom. The countable six-step route and separate platform never exist.
6. **The kingdom is exposed far too early.** Plane/castle aerials appear at 10–15s and again at 23.5–25s, destroying the intended final reveal.
7. **Required acting is omitted.** The chosen handhold, reassuring hug, Daddy's belt demonstration, Roshan copying, and careful descent are either missing, abbreviated beyond readability, or replaced by cutaways.
8. **Final composition is wrong.** The final shot is a front/three-quarter character tableau rather than the small rear-view pair. The characters obscure the foreground path/bridge read; Daddy does not clearly watch Roshan; Roshan's required free-hand wonder gesture is absent or inconsistent.

## Identity and topology

- Roshan drifts toward a generic anime mermaid: simplified pink sleeveless top, reduced costume detail, inconsistent crown/tiara, and unstable tail proportions. Her child scale relative to Daddy is not consistently preserved.
- Daddy is more recognizable, but crown, glasses, hair, coat trim, cape shape, body scale, and tail colors simplify or change between shots.
- Seat belts appear, disappear, or change ownership without the authored release actions.
- Hand ownership is not consistently readable. The inner handhold does not remain continuous through the sequence.
- Character/tail size changes markedly between cabin, exterior landing, doorway, and castle shots.

## Airplane and cabin

- The exterior airplane is a genericized derivative and does not consistently preserve the exact three-window approved shell.
- The interior implies a much larger aircraft than the tiny exterior plane shown on the lawn.
- Cabin window spacing, seat construction, door location, and aisle geometry change across cuts.
- The two-seat rule is approximately present in several frames, but the cabin is not a stable reusable set.
- Touchdown is never causally shown or felt before the exterior parked-plane shot.

## Geography and castle

- Some final frames broadly retain “playground left / castle right,” which is the strongest aspect of the trial.
- The exact geography still is not obeyed closely enough: foreground path, bridge, water boundary, mountain/cabin depth, plant placement, and character platform relationships are simplified or moved.
- The castle resembles the accepted purple shell but changes proportions and detail. The central stained-glass gable is over-emphasized while tower and bridge relationships drift.
- The final characters are too large and central, weakening the required read order: castle/path first, playground second, water/mountains third, small character gesture last.

## Style

The video is attractive in isolation but misses the requested production language. It reads as glossy modern AI storybook/anime illustration with soft volumetric shading. The target is firmer 1990s shōjo television-cel construction: organic navy/violet contours, deliberate two/three-tone paint bands, stronger key poses, fewer continuously morphing details, quieter painted backgrounds, and restrained highlights.

## Editorial and cutaway audit

- The 10–15s castle aerial and castle insert must be removed; they reveal the destination before Roshan's emotional choice and before the threshold crossing.
- The 23.5–25s repeated island aerial is redundant and again reveals the kingdom early.
- The 25–29.5s forest and lakeside shots are visually pleasant but narratively empty. They displace the belt release, hand offer, door approach, and safe-route setup.
- The 29.5–36.5s otter/parked-plane section is unusable and should not be repaired. Regenerate the landing logic from canonical anchors.
- The 36.5–40.5s cabin return/glowing portal section is spatially contradictory and should not be repaired.
- The 40.5–46.5s final location may be used only as a rough diagnostic of palette. Do not use it as a starting frame because it bakes in incorrect character orientation, scale, path obstruction, and geography.

## Salvage list

| Material | Decision | Utility |
|---|---|---|
| 0–2s plane-in-sky | Reject production; concept only | Demonstrates broad sky palette and screen-right travel |
| 2–10s cabin material | Reject production; blocking reference only | Shows that two-character cabin framing is possible |
| 10–15s early kingdom | Reject and never reuse | Spoils final reveal |
| 15–23.5s cabin/standing | Reject production | Some poses may inform prompt wording, not visual conditioning |
| 23.5–29.5s scenic cutaways | Remove from opening | Optional generic world B-roll only after independent style approval |
| 29.5–40.5s landing/exit | Hard reject | Contains the worst causal, scale, animal, and geography failures |
| 40.5–46.5s castle tableau | Reject production; geography diagnostic only | Broad left/right arrangement, but wrong final composition |

## Root cause

This is not primarily a wording defect in one landing sentence. The generation unit was too large. Grok was asked to act simultaneously as writer, continuity supervisor, shot generator, editor, and compositor while holding many assets in context. It selected semantically related PNW material as new subjects and invented cuts to bridge actions it could not animate reliably.

The appropriate fix is a fresh shot-by-shot rebuild from approved still anchors, with Grok used as a bounded renderer rather than the cinematic orchestrator.

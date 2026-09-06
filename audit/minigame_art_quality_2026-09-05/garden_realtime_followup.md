# Garden current independent runtime art review

Date: 2026-09-05
Candidate source HEAD: `9df000999a94572b64537c98f558841f6f3e3260`
Capture provenance: fresh isolated-profile2 run from `tmp/garden-realtime-review/capture.gd`, Mobile renderer, 1280x720, normal processing and actual UI signal callbacks. The earlier 1346x720 run is excluded. These are desktop stills of a diagnostic run; they establish visible composition and state content, not smooth animation, device cadence, or child usability.

**Capture-method correction:** the harness opened the picture canvas from startup without entering Level 2. SceneTree timers and callbacks ran, but the Level 2 owner did not call the picture-game tick. These images remain useful for the callback-built Garden states; they do not establish normal gameplay ticking, watering motion, idle motion, or full animation continuity. The word “realtime” in the retained evidence directory names is not an acceptance claim.

[Source-bound evidence and runner manifest](evidence/garden-realtime-9df/manifest.json). This review applies to published 9df, before the subsequent navigation reconciliation.

## Evidence viewed

All eight current files were opened:

| State | File | SHA-256 |
|---|---|---|
| ready | `garden_ready.png` | `3461A80B871D19C700FC8666082DA5DE1FD10330D02AA86CF083C940CCF388F2` |
| watering/can visible | `garden_can_visible_static.png` | `2522C120B3D1CB3C048B691277B0312154477FA1BAC1F00F9A7579C315AE9443` |
| first sprout | `garden_sprout_first.png` | `EB304877E7026CB7D47B6BD6585BB86E84FC03ACE0279F482AA1CA1BA8C5368D` |
| all sprouts | `garden_sprout_all.png` | `7FA541E81B615A8614D955CD5B20918E020B1FF87F782BBCFC07962306ADAB59` |
| first mature flower | `garden_mature_first.png` | `F634298AD9AF3B4A75FE67FB92B1EF92F44E85D233C5E552AFC18D91D1CA6D27` |
| all five / reward active | `garden_allfive_reward_active.png` | `5F32FA6A7A1D4AA22E65B22AC9FF310B555FB7EA5278667B87E8EF06DAF72D92` |
| reward | `garden_reward.png` | `CAA760C4C7EBDFE1443952A91BBF44EB04F218C4425729D34090B7CD41D1C543` |
| settled reward | `garden_reward_settle.png` | `5A60B0430E57C2882EA6B2388B79540AD84815858C29C982FAC55FEE71D9EC88` |

## What the current frames prove

All five plots are visible and consistently grounded in the final states. Each has a distinct flower color and center treatment; none is clipped or hidden. The stems and leaves remain attached to the soil pads. The reward panel does not remove the flowers, and the settled frame preserves the completed garden.

The current composition is readable: the five plots form a stable bottom row, the watering can and mermaid occupy the right action area, and the instruction/reward panel stays above the playfield. The sun and butterflies add a coherent garden motif. The visibility repair is effective; this does not resolve the separate flower finish and consistency defects.

## Subjective master-criteria review

Scores are for the viewed still state and are not acceptance claims. They use the eight ledger dimensions: identity, finish, edges, readability, animation, ownership, consistency, technical.

| Surface/state | identity | finish | edges | readability | animation* | ownership | consistency | technical | minimum / disposition |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| garden ready / soil + seeds | 4.2 | 3.5 | 4.0 | 4.5 | **unassessed** | 4.0 | 3.2 | 4.2 | **3.2 lowest observed; below gate** |
| watering can action prop | 4.0 | 3.3 | 3.7 | 4.0 | **unassessed** | 3.8 | 3.0 | 3.8 | **3.0 lowest observed; below gate** |
| sprout family | 3.2 | 2.8 | 3.2 | 4.2 | **unassessed** | 3.6 | 2.8 | 3.7 | **2.8 lowest observed; below gate** |
| mature flower family | 4.0 | 3.4 | 3.8 | 4.5 | **unassessed** | 3.8 | 3.2 | 4.0 | **3.2 lowest observed; below gate** |
| final five-flower layout | 4.1 | 3.5 | 3.8 | 4.5 | **unassessed** | 4.0 | 3.4 | 4.1 | **3.4 lowest observed; below gate** |
| reward panel / medal | 4.4 | 4.1 | 4.3 | 4.5 | **unassessed** | 4.3 | 4.0 | 4.3 | **4.0 lowest observed; below gate** |

\*Animation is unassessed from stills. These captures do not prove cadence, contact timing, or device playback. Technical observations are bounded to screenshot structure/composition and do not prove device performance.

## Weaknesses and repair order

1. **P0 — sprout family visual finish and consistency.** The current sprout is a pale, flat two-leaf stem with a gray oval base. It is materially simpler than the richly outlined sun, butterflies, mermaid, and final flowers. The sprouts appear identical in the viewed states, with no authored growth distinction visible beyond placement. First inspect approved story flower/sprout alternatives and preserve the existing touch geometry. Reuse is preferred; generate only if no approved counterpart has the right sprout role. Re-audit ready, first-sprout, and all-sprout states.
2. **P0 — soil plot pads.** Large orange-brown rounded pads have a thick dark outline and a single pale highlight, reading as UI chips rather than planted soil. This is a scene-level consistency defect visible in every state. Prefer a non-destructive shared texture/derived variant or layout treatment before regenerating five plants. Preserve the plot hit areas.
3. **P1 — watering can.** The can is legible and correctly placed, but its heavy magenta fill, dark contour, and blocky silhouette do not match the softer storybook garden props. The spout is visible in the static frame, yet the current still does not prove a convincing pour/contact pose. Inspect the live animation and any approved can alternatives before commissioning a replacement; do not accept a generic recolor.
4. **P1 — mature flower variants.** Distinct colors are successful and all five are anchored, but the family shares a very simple five-petal silhouette and flat fills. Reuse or derive role-specific approved flower variants while retaining color distinction; do not replace all five with one repeated flower.
5. **P1 — reward panel.** The panel is clean and child-readable, with three stars and medal hierarchy. Its pale card and celebratory stars are somewhat detached from the garden’s visual language, but this is lower priority than the plant/soil family. Validate actual reward transition timing separately.

No current frame shows an unanchored flower, hidden plot, or overlap that breaks touch readability. This means no new plants are needed to fix visibility or anchoring; the plant/soil art still remains below the finish and consistency bar and needs reuse, refinement, or replacement. The strongest minimum-change path is to repair/reuse the sprout and soil family first, then review the watering-can action art and flower-family consistency.

## Required re-audit states

After any art or layout change, capture current Mobile 1280x720 frames at: ready, watering/can visible, first sprout, all sprouts, four mature flowers before the final action, fifth mature with the immediate reward transition, reward active, and settled reward. The current callback awards immediately when the fifth flower matures, so an all-five pre-reward state is not claimed. The acceptance packet must include fresh source hashes, a true-device capture, and a motion/contact review; this still packet alone cannot establish the 4.5 game-wide gate.

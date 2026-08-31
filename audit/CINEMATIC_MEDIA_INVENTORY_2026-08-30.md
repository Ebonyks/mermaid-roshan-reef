# Day One cinematic media inventory — 2026-08-30

## Result

The repository and associated live worktrees contain substantial cinematic
development, but **no complete movie currently has `DELIVERY_ACCEPTED` status**.
There are two useful rough editorial families:

1. the older 42.5-second airplane/cabin/landing opening; and
2. the Grok/Resolve airplane-to-castle-arrival recuts.

Both are evidence and editing references, not final films. The first is
mechanically coherent but was artistically rejected. The second improves
motion and location spectacle but drifts character and aircraft identity,
introduces an unrequested giant otter, and does not cleanly finish the promised
action of Roshan and Daddy entering the castle.

The strongest unassembled cinematic work is the paired room storyboard work:
the pool restoration is the best package, the Stuffie Room pair is strong, and
the bathroom cleanup is usable after migration. The bathroom entry board must
be redrawn because its room reads bright and largely clean rather than dirty.

## Scope and method

This inventory reviewed tracked media on all relevant branches, local review
masters and proof encodes, manifests, contact sheets, opening audits, Resolve
project exports, and the current Day One runtime event seams. Video streams
were decoded with local FFmpeg; representative frames were compared as contact
sheets. Existing DaVinci Resolve project packages were evaluated through their
rendered masters, edit manifests, and reports. No protected original was
modified.

Review status is deliberately separated:

- `EDITORIAL_REFERENCE`: timing, shot order, or motion may be studied.
- `BOARD_REFERENCE`: stills may direct future generations but are not delivery
  pixels or approved first frames.
- `REJECTED_DELIVERY`: the item must not ship as a cinematic.
- `DELIVERY_ACCEPTED`: requires the complete full-frame cinematic evidence and
  gates in `AGENTS.md` and `tools/audit_cinematic.py`.

## Principal edited movies

| Candidate | Technical facts | What works | Blocking defects | Verdict |
|---|---|---|---|---|
| `opening_cinematic_v2_final.mp4` | 42.500 s, 1280×720, 24 fps, silent; SHA-256 `B2949CCEA0B78819CDC57DEA205C578C9823B5561919CDB08592042F86AF9E64` | Clear airplane → cabin relationship → landing → castle geography; readable Roshan/Daddy emotional spine. | The exact audit is `MECHANICAL PASS / ARTISTIC REJECTION`, owner 0.5/5; rigid cutout/Flash motion; 126 production-profile findings; not current full-frame evidence. | `EDITORIAL_REFERENCE`, `REJECTED_DELIVERY` |
| `opening_cinematic_v2.mp4` | 42.500 s, 1280×720, 24 fps, silent; SHA-256 begins `F8AA14` | Same broad continuity as the final encode and useful alternate edit evidence. | Same rejected source family; no reason to prefer it over the final review encode. | `EDITORIAL_REFERENCE`, `REJECTED_DELIVERY` |
| opening full assembly | 45.875 s, 1280×720, 24 fps, silent; SHA-256 begins `E854486C` | Preserves all 18 authored beats and is the most complete timing map. | Too long and rigid; lower animatic profile only; production profile remains open/failed. | `EDITORIAL_REFERENCE`, `REJECTED_DELIVERY` |
| opening exact-1020 assembly | 42.500 s, 1280×720, 24 fps, silent; SHA-256 begins `3A98DE24` | Best exact-duration evidence for the old opening. | Its own audit records mechanical pass, artistic rejection; cannot seed final frames. | `EDITORIAL_REFERENCE`, `REJECTED_DELIVERY` |
| `review/audio/intro_sound_design_2026-08-23/intro_sound_design_review.mp4` | 42.133 s, 1280×720, 24 fps, audio; SHA-256 begins `4049E660` | Demonstrates a viable sound-design envelope and edit synchronization. | Dialogue remains blocked pending owner family recordings; picture inherits opening defects. | `EDITORIAL_REFERENCE`, `REJECTED_DELIVERY` |
| `review/video/luna_editorial_recut_2026-08-23/mermaid_roshan_luna_recut_v1_resolve.mp4` | 39.125 s, 1280×720, 24 fps, audio; SHA-256 begins `19782383` | Stronger spectacle, clearer destination reveal, usable examples of arrival pacing. | Invented giant otter subplot; identity, crown, hair, tail-lighting, aircraft-scale, camera, and geography drift; not a clean castle-entry film. | `EDITORIAL_REFERENCE`, `REJECTED_DELIVERY` |
| `review/video/luna_editorial_recut_2026-08-23/otter_recut_v2/mermaid_roshan_otter_wing_recut_v2_resolve.mp4` | 33.643 s, 1280×720, 24 fps, audio; SHA-256 begins `32116206` | A tighter alternate timing study. | Retains the unrequested otter and has a visible dissolve/ghost frame; same identity and continuity problems. | `EDITORIAL_REFERENCE`, `REJECTED_DELIVERY` |
| `tmp/editorial/grok_series_20260823/review/mermaid_roshan_arrival_v1_review_360p_24fps.mp4` | 24.896 s, 640×360, 24 fps, audio; SHA-256 begins `73010117` | Closest extant rough to “Roshan and Daddy walk toward the castle”; useful cadence and blocking evidence. | Review resolution; does not actually complete the castle entry; generated shots drift identity and scale; later variants require the giant otter. | `EDITORIAL_REFERENCE`, `REJECTED_DELIVERY` |

The three opening storyboard animatics are each 22.500 seconds at 1280×720,
12 fps. They are near-duplicates of the airplane/cabin/door/stairs plan. They
remain `BOARD_REFERENCE` only; their limited differences do not establish
three distinct productions.

## Proof clips and character motion studies

The local opening-motion worktree contains many five-second and per-shot
encodes, including articulated, rigged, layered-RIFE, authored-atlas, and
inbetween trials. They document why temporal shortcuts fail: hand contact,
tail topology, body scale, occlusion, and eye motion repeatedly break even when
simple transition metrics pass. Several methods are explicitly forbidden for
delivery under the current full-frame rule. Preserve these clips as failure and
timing evidence only.

The seven Ember Royal MP4/GIF studies on
`origin/codex/grok-animation-series-guide` are 1024×576, 30 fps motion studies:
family walk, King idle/heavy walk/cape fan, and Prince idle/sleek walk/
cinderstep. They are good cadence and scale references, not environment,
contact, or final cinematic evidence.

## Existing room storyboard/handoff work

| Sequence | Existing evidence | Review result | Required action |
|---|---|---|---|
| Bathroom dirty entry | `assets_src/cinematics/day_one_bathroom_entry_v1/` | Character and fixture sources exist, but the seven-panel board reads too bright and too clean. It does not deliver the required shock of entering a dirty room. | Rebuild the board from a convincingly dirty first frame; add reverse doorway and fixture closeups; migrate to V2. |
| Bathroom restoration | `assets_src/cinematics/day_one_bathroom_cleaned_v1/` | Clear final-scrub → water-clear → bunny-recovery → sparkle → next-route sequence. | Preserve causality; split into V2 one-shot cards; replace any gameplay/UI capture used as appearance-bearing generation input. |
| Pool dirty discovery | Cardinal-perspective, dirty-waterfall, and sick-seahorse boards on `codex/grok-pool-cinematic-handoff` | Strong room expansion beyond the theatrical front plate; closeups make trash, turgid waterfall, giant pool, and mouth obstruction readable. | Build a self-contained V2 archive/generator packet and lock the giant-pool topology. |
| Pool restoration/Rumi | Nine accepted storyboard beats on `codex/grok-pool-restoration-handoff` | Strongest package in project: pink-trash extraction, seahorse flow, top-down waterfall ignition, pullback, dual purification, violet glow, correct Rumi reveal, thanks, hug. | Use as the template; migrate each beat to one V2 shot card with two-to-four refs. |
| Stuffie dirty discovery | `assets_src/cinematics/day_one_stuffie_discovery_v2/` at guide head `3af5a8eb7110dab2381c7d0a73b27b880d35e84a` | Strong doorway/reverse/low-floor/pinned-eagle geography and character causality. | Finish immutable links, packet validation, and publication; do not bind storyboard panels as generation pixels. |
| Stuffie restoration | `assets_src/cinematics/day_one_stuffie_basket_clean_v2/` at the same guide head | Strong basket warnings → four bunnies → Baby Eagle sets wings → safe cleaning blast → clean resolve. | Finish immutable links, packet validation, and publication. |

## Historical dirty-castle package

The 36-frame July dirty-castle sequence is not a current movie plan. It depicts
a superseded room list and a full-cast, room-by-room flipbook. It also contains
known duplicate-character corrections. Reuse only these narrative ideas:

- every room has a distinct dirty discovery and clean payoff;
- cleanup is cooperative and immediately legible;
- dust bunnies become helpers/friends rather than refuse;
- the final clean state must be compositionally unmistakable.

Do not reuse its old runtime shell, old room map, frames as delivery pixels, or
multi-room generation approach.

## Bottom line

- Existing rough edited films: **2 narrative families** (opening; arrival).
- Existing current-room board pairs: **3** (bathroom, pool, Stuffie Room).
- Current Day One room pairs still without boards: **1** (Art Room).
- Additional required story films without current boards: dirty-castle
  discovery, boss reveal, and finale.
- `ARCHIVE_COMPLETE`: **false** for the total slate.
- `GENERATION_READY`: **false** for the total slate.
- `DELIVERY_ACCEPTED`: **0 of 13 movies**.

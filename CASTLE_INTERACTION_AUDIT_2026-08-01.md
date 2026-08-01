# Pearl Castle interaction and cutout audit — 2026-08-01

## Outcome

The active castle now contains 38 physical interactive prop instances across
eight rooms (4.75 per room), backed by 33 unique eight-frame atlases. Every
destination room has at least four props. The former whole-card bounce,
rotation, squash, hover, spin, sway, and portal-glow treatments are removed.
Each interaction instead changes a meaningful part of the prop while the card
pivot and chassis remain fixed.

The user-reported Roshan clipping had two alpha-ownership causes: broad legacy
cards retained wall, floor, water, or counter pixels, while a later
color-difference pass punched holes through legitimate low-contrast fixture
pixels. The repair tightens source ownership, preserves every approved refined
silhouette without re-segmenting it, rebuilds the healed architecture plates
and native runtime tiles, removes the duplicate refrigerator glow card, and
adds blocking excess-alpha, silhouette-retention, and Roshan-visibility gates.

## Active interaction inventory

Every line below is an eight-frame sequence. Main Hall sconces share one atlas
but remain six physical fixtures with independent light state.

| Room | Physical items | Normalized interaction | Sound cue |
|---|---:|---|---|
| Main Hall | 1 tapestry | Cloth unfurls/waves from its fixed hanger | `curtain_swish.ogg` |
| Main Hall | 6 shell sconces | Switch click and local pearl-light chase; each fixture still toggles its real light cluster | `light_switch.ogg` |
| Opera Hall | Curtains | Center panels open to the stage, then close | `curtain_swish.ogg` |
| Opera Hall | Chandelier | Bulbs illuminate in a local chase | `light_switch.ogg` |
| Opera Hall | Footlights (new isolation) | Stage bulbs chase across the rail | `light_switch.ogg` |
| Opera Hall | Stage star | Marquee lights chase across the star | `light_switch.ogg` |
| Royal Kitchen | Shell sink | Handle turns, stream starts, basin ripples, stream stops | `faucet_water.ogg` |
| Royal Kitchen | Four copper pans | Pan bodies swing from fixed hooks; one correctly sized rack hotspot triggers one coordinated clang | `pan_clang.ogg` |
| Royal Kitchen | Oven | Door lowers, warm fire/interior appears, door closes | `oven_door.ogg` |
| Royal Kitchen | Refrigerator | Latch releases, door opens to shelves, door closes; recipe menu opens only after the sequence | `fridge_door.ogg` |
| Royal Library | Magic book | Cover/pages open and turn, then close | `page_flip.ogg` |
| Royal Library | Reading pearl table | Pearl wakes and emits a local reading glow | `light_switch.ogg` |
| Royal Library | Pearl lamp | Pearl light switches and blooms locally | `light_switch.ogg` |
| Royal Library | Book stack (new isolation) | Top book opens and turns pages | `page_flip.ogg` |
| Stuffie Playroom | Stuffie nook | Individual friends wave in sequence | `toy_blocks.ogg` |
| Stuffie Playroom | Stacking toy | Rings lift in order and restack | `toy_blocks.ogg` |
| Stuffie Playroom | Blocks | Blocks topple and restack | `toy_blocks.ogg` |
| Stuffie Playroom | Play tent (new isolation) | Tent flap opens and closes | `curtain_swish.ogg` |
| Craft Room | Idea board | Individual notes flip | `page_flip.ogg` |
| Craft Room | Paint table | Brush stirs the paint jars | `craft_brush.ogg` |
| Craft Room | Palette | Brush moves through and mixes the palette colors | `craft_brush.ogg` |
| Craft Room | Ribbon rack (new isolation) | Ribbon unrolls in a wave and retracts | `ribbon_roll.ogg` |
| Mermaid Pool | Waterfall | Water strands surge and cycle | `bubble_water.ogg` |
| Mermaid Pool | Flower float | Petals open/close and create a ripple | `bubble_water.ogg` |
| Mermaid Pool | Bubble fountain | Jet runs while bubbles rise and pop | `bubble_water.ogg` |
| Mermaid Pool | Star float (new isolation) | Float creates expanding pool ripples | `bubble_water.ogg` |
| Bubble Bath | Bathtub | Taps turn; water and bubbles fill/cycle | `bubble_water.ogg` |
| Bubble Bath | Shell sink | Handle turns, stream starts, basin ripples, stream stops | `faucet_water.ogg` |
| Bubble Bath | Royal toilet | Seat flaps through its hinge arc; water swirls and flushes; fixture settles | `toilet_flush.ogg` |
| Bubble Bath | Rubber duck (new isolation) | Duck squeaks, dives, ripples, and pops back up | `duck_squeak.ogg` |

Room totals: Main Hall 7; Opera Hall 4; Royal Kitchen 7; Royal Library 4;
Stuffie Playroom 4; Craft Room 4; Mermaid Pool 4; Bubble Bath 4.

## Cutout and depth repair

- Tightened all destination-room item masks in
  `tools/build_castle_room_layers.py`; six existing painted elements now have
  unique ownership cards: footlights, book stack, play tent, ribbon rack,
  star float, and rubber duck.
- Rebuilt every affected clean room plate, foreground/midground ownership
  card, 2K preservation master, and lossless runtime tile grid. The seven room
  tile sets reconstruct their corresponding rebuilt masters pixel-exactly.
- Runtime atlases keep a one-pixel transparent guard around every populated
  cell so linear texture sampling cannot borrow a depth-writing pixel from an
  adjacent frame.
- Room-derived rest poses preserve the already outline-refined ownership-card
  alpha byte for byte; a second segmentation pass is forbidden. The blocking
  audit retains at least 95% of every approved source silhouette (98.94%
  minimum delivered) while applying a 6-level healed-background comparison.
  Higher-similarity pixels are accepted only on small, sparse props with no
  more than 1,600 such pixels; the delivered maximum fraction is 30.37%.
- The sink, bathtub, toilet, flower float, and bubble fountain could not be
  separated cleanly from their tiny room crops without materially losing the
  fixture. Preservation-focused ImageGen edits were therefore made from only
  the approved item/reference art on flat chroma. Native outputs, accepted
  alpha masters, exact prompts/hashes, helper settings, rejected sink matte,
  and drift reviews are retained in
  `assets_src/imagegen/castle_interactions_2026-08-01/PROMPTS.md`.
- The bathtub master originally includes the approved duck. The deterministic
  builder heals that footprint with adjacent water and extracts the same duck
  by color into its unique card, so no duplicate duck remains in delivery art.
- No protected book, family-voice, or friend-character source was modified.

## Runtime and touch behavior

- `Sprite3D.hframes`, `vframes`, and frame are assigned before placement;
  placement, art rectangles, and touch projection use one frame cell rather
  than the full atlas dimensions.
- Atlas playback records ordered frame visits, starts item-specific Ogg audio
  on frame zero, ends the eight-frame visual on the same instant as the sound,
  returns to frame zero, and clears its busy state. Semantic interaction pitch
  remains 1.0 so the authored timing cannot drift.
- Playback never changes the prop root's position, scale, or rotation.
- The four pan cards retain individual animated bodies but share one rack-sized
  hotspot and one sound, removing the previous overlapping-button ambiguity.
- The refrigerator no longer creates a translucent duplicate depth/effect card
  and does not open the recipe overlay until its door action is complete.
- Hall sconce state remains independent and still controls the corresponding
  real light cluster; its local frame sequence is additive interaction feedback.
  Bloom samples are clamped to the active atlas cell so no adjacent frame can
  leak alpha or light into the fixture.

## Blocking audit contract

`tools/audit_castle_interactions.py` is invoked by `scripts/ci.sh` and fails on:

- a room roster outside the approved 38-instance / 4.75 average contract;
- fewer than four destination-room items;
- a frame count outside 4–12, fewer than four materially unique frames, an
  invalid atlas grid, oversized texture, changed source/atlas hash, or nonblank
  unused cell;
- any depth-writing pixel on a populated cell's outer border, an opaque-card
  footprint, insufficient transparent area, or excessive healed-background
  similarity;
- loss of more than 5% of a refined source silhouette, inaccurate alpha-depth
  evidence, or incomplete visual-review evidence for any of the eight frames;
- missing fixed-pivot/root-transform evidence, discontinuous chassis overlap,
  trivial animation, or action affecting most of the cell;
- missing/misrouted/non-Ogg sound, incorrect semantic action, or unaccepted
  normalized-use review, or any frame-zero/duration mismatch between the
  visual sequence and its synthesized sound;
- a deterministic placement in which Roshan does not remain sufficiently
  visible through the prop's transparent regions.

Current static audit metrics:

- 8 rooms, 33 atlases, 38 physical instances, average 4.75;
- maximum depth coverage 86.27%;
- maximum healed-background-like opaque fraction 30.37% under the conditional
  small/sparse-prop gate;
- minimum retained source silhouette 98.94%;
- minimum fixed-chassis alpha IoU 20.14%;
- minimum sampled Roshan visibility 15.83%;
- minimum material frame change 0.74%;
- maximum animation/audio duration error 0.000 seconds;
- result: `CASTLE INTERACTION AUDIT: ALL OK`.

## Source and delivery files

- Atlas generator: `tools/build_castle_interaction_atlases.py`
- Audio generator: `tools/build_castle_interaction_audio.py`
- Static gate: `tools/audit_castle_interactions.py`
- Runtime manifest: `assets/flats/castle/interactions/castle_interactions.json`
- Audio manifest: `assets/audio/castle/castle_interaction_sfx_manifest.json`
- Visual review board: `audit/castle_interactions/castle_interaction_frames.png`
- Licenses: every new runtime/source/audit asset is listed individually in
  `ASSET_LICENSES.md`.

Final parser, inference lint, Godot analyzer, trusted-probe, branch-CI, dev
integration, and protected master-promotion results are recorded in the commit
and delivery summary after those gates complete.

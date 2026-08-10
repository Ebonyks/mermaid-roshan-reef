# Opera minigame art review — 2026-08-09

Status: **Codex visual QA accepted; owner/human review pending**. The four-cell ImageGen board was visually inspected by Codex before runtime derivation.
All other art is a non-destructive derivative of approved project sources.

## Artifact QA

- Four generated movers: one connected prop each, complete silhouette, no crop, floating part, text, or visible chroma spill.
- Approved-card derivatives: dark presentation field and contact-sheet rules removed with `_remove_edge_field`; source RGB subjects were not repainted.
- Every transparent runtime derivative has a nonzero safe alpha gutter; every output obeys the <=1024/POT texture rule.
- Exact dimensions, alpha bounds, hashes, source hashes, transforms, and the exact generation prompt are in `PROVENANCE.json`.
- `python tools/prepare_opera_minigame_art.py --check-only` is the byte-exact reproducibility gate.

## Source-role audit notes

- Source export labels were audited visually. Candy and Farmer source names are shifted; mappings above follow visible art.
- Chef pieces retain only each topping's approved visible silhouette/lower outline; every serving pedestal/plate/base pixel is excluded.
- Magician cabinet reveal continues VANISH by placing the approved Lamba reveal inside a cabinet shell derived only from approved crops.
- Detective board slots are authored left-to-right; runtime hit targets must use the same horizontal order.

## Runtime derivatives

- `widget_clue_board_complete.png` — 1024x608; alpha bbox `[114, 19, 911, 589]`; complete frame and all three left-to-right silhouettes visible; no grid/frame bleed or crop.
- `widget_clue_board_empty.png` — 1024x608; alpha bbox `[113, 20, 911, 588]`; complete frame and all three left-to-right silhouettes visible; no grid/frame bleed or crop.
- `widget_clue_board_tokens.png` — 768x256; alpha bbox `[20, 20, 748, 237]`; three distinct complete tokens; no cross-cell bleed or clipping.
- `widget_crank_popstar_mover.png` — 256x256; alpha bbox `[16, 30, 240, 227]`; single finale microphone identity, not whole stage; complete mic with intentional sound pulses and no frame bleed.
- `widget_crank_racer.png` — 1024x608; alpha bbox `[0, 0, 1024, 608]`; no racetrack curve; clear pre-repair state has one complete front wheel, one open rear hub, and a non-overlapping toolkit.
- `widget_crank_racer_mover.png` — 256x256; alpha bbox `[35, 37, 221, 219]`; accepted source topology preserved; one complete object; no crop, detached part, or visible green spill.
- `widget_crank_racer_wheel.png` — 256x256; alpha bbox `[22, 22, 234, 234]`; complete isolated wheel with tire, rim, and shell hub; no fender, body fragment, crop, or presentation field.
- `widget_crown_chest_closed.png` — 512x512; alpha bbox `[55, 66, 457, 446]`; closed/open topology coherent; open tiara remains connected and fully visible; no crop.
- `widget_crown_chest_open.png` — 512x512; alpha bbox `[71, 65, 440, 446]`; closed/open topology coherent; open tiara remains connected and fully visible; no crop.
- `widget_gauge_chef_success.png` — 1024x608; alpha bbox `[247, 51, 778, 569]`; finished cake replaces generic green disk; plate, tiers, fruit, and frosting fully visible.
- `widget_magic_cabinet_closed.png` — 512x512; alpha bbox `[83, 62, 429, 450]`; complete cabinet, hinges, shell crest, feet, and handles visible.
- `widget_magic_cabinet_reveal.png` — 512x512; alpha bbox `[83, 62, 429, 450]`; Lamba is fully contained behind the approved open cabinet shell; no opaque plate, hard rectangular seam, floating hat, crop, or source repaint.
- `widget_magic_vanish_hat.png` — 512x512; alpha bbox `[51, 77, 460, 435]`; magic prop/reveal complete and contained; no labels, presentation frame, or clipped silhouette.
- `widget_magic_vanish_reveal.png` — 512x512; alpha bbox `[112, 20, 400, 491]`; clean Lamba-over-hat reveal; both silhouettes complete and contained; no presentation field, blob, hard seam, labels, or crop.
- `widget_magic_vanish_wand.png` — 512x512; alpha bbox `[69, 50, 442, 462]`; magic prop/reveal complete and contained; no labels, presentation frame, or clipped silhouette.
- `widget_portal_magician_mover.png` — 256x256; alpha bbox `[19, 20, 237, 233]`; complete open portal frame, curtains, threshold, and warm opening; no Lamba, hat, stage tableau, or crop.
- `widget_pour_candymaker_mover.png` — 256x256; alpha bbox `[31, 41, 225, 214]`; accepted source topology preserved; one complete object; no crop, detached part, or visible green spill.
- `widget_pour_chef_mover.png` — 256x256; alpha bbox `[21, 46, 234, 209]`; accepted source topology preserved; one complete object; no crop, detached part, or visible green spill.
- `widget_pour_nursery_mover.png` — 256x256; alpha bbox `[75, 22, 181, 234]`; accepted source topology preserved; one complete object; no crop, detached part, or visible green spill.
- `widget_target_astronaut_mark.png` — 128x128; alpha bbox `[9, 9, 119, 119]`; thematic filled stamp remains distinct from hollow invitation ring.
- `widget_target_astronaut_piece_0.png` — 256x256; alpha bbox `[27, 27, 229, 229]`; unique shell/rivet patch silhouette; complete outline and >=24px transparent margin.
- `widget_target_astronaut_piece_1.png` — 256x256; alpha bbox `[27, 23, 229, 234]`; unique shell/rivet patch silhouette; complete outline and >=24px transparent margin.
- `widget_target_astronaut_piece_2.png` — 256x256; alpha bbox `[31, 42, 226, 214]`; unique shell/rivet patch silhouette; complete outline and >=24px transparent margin.
- `widget_target_candymaker_mark.png` — 128x128; alpha bbox `[13, 9, 115, 119]`; thematic filled stamp remains distinct from hollow invitation ring.
- `widget_target_candymaker_piece_0.png` — 256x256; alpha bbox `[27, 18, 230, 238]`; one child-readable complete target prop; no frame bleed, crop, or detached part.
- `widget_target_candymaker_piece_1.png` — 256x256; alpha bbox `[18, 23, 238, 234]`; one child-readable complete target prop; no frame bleed, crop, or detached part.
- `widget_target_candymaker_piece_2.png` — 256x256; alpha bbox `[17, 59, 239, 197]`; one child-readable complete target prop; no frame bleed, crop, or detached part.
- `widget_target_chef_mark.png` — 128x128; alpha bbox `[9, 15, 120, 114]`; thematic filled stamp remains distinct from hollow invitation ring.
- `widget_target_chef_piece_0.png` — 256x256; alpha bbox `[20, 23, 236, 233]`; one complete topping-only token; no serving stand, plate, pedestal, flat cut, frame bleed, or detached part.
- `widget_target_chef_piece_1.png` — 256x256; alpha bbox `[20, 31, 236, 226]`; one complete topping-only token; no serving stand, plate, pedestal, flat cut, frame bleed, or detached part.
- `widget_target_chef_piece_2.png` — 256x256; alpha bbox `[21, 31, 231, 224]`; one complete topping-only token; no serving stand, plate, pedestal, flat cut, frame bleed, or detached part.
- `widget_target_farmer_mark.png` — 128x128; alpha bbox `[15, 9, 113, 119]`; thematic filled stamp remains distinct from hollow invitation ring.
- `widget_target_farmer_piece_0.png` — 256x256; alpha bbox `[29, 17, 227, 239]`; one child-readable complete target prop; no frame bleed, crop, or detached part.
- `widget_target_farmer_piece_1.png` — 256x256; alpha bbox `[24, 17, 233, 239]`; one child-readable complete target prop; no frame bleed, crop, or detached part.
- `widget_target_farmer_piece_2.png` — 256x256; alpha bbox `[18, 25, 238, 232]`; one child-readable complete target prop; no frame bleed, crop, or detached part.
- `widget_target_painter_mark.png` — 128x128; alpha bbox `[18, 8, 111, 120]`; literal coral paint splat replaces generic ring; main splash and intentional droplets fully contained.

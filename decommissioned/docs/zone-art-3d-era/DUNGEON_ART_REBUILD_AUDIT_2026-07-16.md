# Dungeon Art Rebuild Audit - 2026-07-16

## Result

The dungeon wing no longer uses primitive-only focal art. Ten authored, reproducible Blender assets now provide its arena, shell door, enemy, dragon-turtle boss, pepper basket, crystal pedestal, pepper lantern, turtle statue, stepping stone, and pictogram family.

Scores below are provisional production-candidate scores. They are capped at 3/5 until owner review because 4/5 requires representative near, mid, and gameplay-distance human approval.

| Runtime role | Before | After | Evidence |
|---|---:|---:|---|
| Octagonal arena and walls | 1/5 | 3/5 | Scalloped shell masonry, coral-glass buttresses, raised rings, and floor mosaic visible in Mobile gameplay. |
| Exit door | 1/5 | 3/5 | Cohesive shell crown, columns, ribs, bands, and star lock replace box slabs. |
| Mischief imp | 1/5 | 3/5 | Complete body, paired fins, face, feet, and tail replace sphere/cone placeholder anatomy. |
| Dragon-turtle boss | 1/5 | 3/5 | Complete head, muzzle, eyes, horns, shell, scutes, flippers, tail, and claws; both hidden-head shell and peek phases reviewed. |
| Pepper basket | 2/5 | 3/5 | Woven basket, handle, five peppers, and stems replace runtime rings and loose spheres. |
| Crystal pedestal | 1/5 | 3/5 | Faceted base, rim, and pearl inlays replace cylinder pad. |
| Pepper lantern | 1/5 | 3/5 | Stem, leaves, pepper glass, cap, and two-part glow replace torch primitives. |
| Turtle statue | 1/5 | 3/5 | Modeled shell, scutes, head, flippers, and gold nose replace symbolic shell pieces. |
| Stepping stone | 1/5 | 3/5 | Rounded irregular stone with five inlays replaces a flat box. |
| Puzzle pictograms | 0/5 | 3/5 | Eleven modeled symbols replace labels and debug-like geometry; inactive symbols are removed per instance. |

## Runtime verification

The isolated validation project ran Godot 4.4 with the Forward Mobile renderer at 1280x720 on an RTX 3060 Ti. Captures covered combat, the spinning-shell boss state, the boss peek state, crystal sequence, and pepper lantern puzzles.

| Scene | Descendants | Existing limit/result |
|---|---:|---|
| Five-imp combat | 33 | Passes `<100` combat budget. |
| Dragon-turtle boss | 24 | Passes `<100` combat budget. |
| Three-choice crystal puzzle | 60 | Passes `<90` puzzle budget. |
| Four-lantern puzzle | 78 | Below the same 90-node target. |

Geometry is batched by tint role and fixed-detail material slots while preserving gameplay nodes such as `Head`, `Shell`, and `Glow`. The art is integrated through `DungeonArt`; transient shots, popcorn, and the single pearl remain lightweight runtime effects rather than focal assets.

## Reversal and protection

The previous script-built presentation is preserved under `backups/art_pre_dungeon_v2_2026-07-16/` with SHA-256 values. No files under `assets/book/`, `assets/audio/voices/`, or `assets/characters/friends/` were modified, and no stuffed-animal or child-toy art was generated.

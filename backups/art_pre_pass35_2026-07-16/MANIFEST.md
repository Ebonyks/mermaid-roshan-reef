# Pre-Pass-35 Art Backup

This directory mirrors every pre-pass runtime file overwritten by the
2026-07-16 game-wide 3.5-and-lower art pass. Files are byte-for-byte copies
from `origin/master` at `021e235fcdd748e70f19d9f4a9e316b7c9913584`.

## Restore Rules

- Restore only a disputed family, not the entire directory by default.
- Copy the chosen file from this backup to the same path relative to the
  repository root.
- Import the project again after restoring any PNG, JPG, or GLB.
- The `.import` files are retained only as provenance. Godot may regenerate
  them for the current machine.

Example, from the repository root:

```powershell
Copy-Item -LiteralPath "backups/art_pre_pass35_2026-07-16/assets/mg/star.png" -Destination "assets/mg/star.png" -Force
```

## Mirrored Families

| Active path | Backup path | Pass-35 action |
|---|---|---|
| `assets/mg/{butterfly,coal,fish_body,fish_fins,k_bush2,orn1-orn5,star,sun,tree,xtree}.png` | same path beneath this directory | Replaced with transparent OpenAI-generated storybook sprites. |
| `assets/props/gen2/clownfish.glb` | same path beneath this directory | Replaced with an anatomically coherent toon fish. |
| `assets/props/gen2/octopus.glb` | same path beneath this directory | Replaced with a complete eight-arm toon octopus. |
| `assets/props/gen2/coral*.glb` | same path beneath this directory | Replaced with seven undersea-only modeled clump families. |
| `assets/props/gen2/rock*.glb` | same path beneath this directory | Replaced with seven low-poly toon rock families. |
| `scripts/landmark_art.gd` | `scripts/landmark_art.gd.bak` | Preserves the old primitive star, cloud, and butterfly-gate builders. |
| `scripts/games/picture_games.gd` | `scripts/picture_games.gd.bak` | Preserves the pre-pass picture-game routing. |

New files under `assets/art35/`, the new jellyfish/shrimp/projectile GLBs, and
their Blender sources did not replace an older file and therefore have no
backup counterpart. Reverting their integration only requires restoring the
backed-up scripts or removing the relevant new-path call.

# Full Texture Regeneration Candidate Pack - 2026-07-18

This directory is the isolated, game-wide replacement candidate pack produced
from the pass-3.5 audit. It is deliberately **not connected to runtime paths**.
Review and promotion can therefore happen role by role without changing the
current playable branch.

## Status

- Audited roles: **88**
- Generated/rebuilt roles: **85**
- Candidate files: **167** (`137` GLB models and `30` PNG textures)
- Northern Kingdom: **included**, with `17` candidates
- Structural stress: **pass**
- Full-size gallery review: **pass at 4/5 candidate threshold**
- Phone-scale gallery review: **pass at 4/5 candidate threshold**
- Final 5/5 acceptance: **pending owner review**

Automation is not allowed to award its own work 5/5. The two original book
assets are already source-locked at 5/5; all generated candidates remain capped
at 4/5 until the owner accepts them.

## Directory Map

- `models/` - 137 texture-free GLBs with embedded matte palette materials
- `textures/` - 30 normalized PNG candidates, no side over 1024 px
- `source_generations/accepted/` - 28 original image-generation outputs
- `source_generations/rejected/` - rejected attempts retained with the reason in the filename
- `manifest.json` - hashes, role mappings, counts, exclusions, and source records
- `../../assets_src/blender/full_texture_regen_2026-07-18/` - editable Blender source and model manifest
- `../../audit/full_regen_2026-07-18/` - per-file stress results, per-role review, renders, and galleries

`source_generations/` and the Blender source directory are excluded from Godot
imports with `.gdignore`; they remain inside the repository for provenance and
future revision.

## Protected Roles

- `R081_picture_games_carrot`: preserve the original book art exactly.
- `R082_picture_games_watering_can`: preserve the original book art exactly.
- `R083_picture_games_cat_parts`: no auto-generation. Replace only with the
  child's own source material and manual art direction.

No file under `assets/book/`, `assets/audio/voices/`, or
`assets/characters/friends/` was modified or copied into this pack.

## Functional Pairing Rules

- `R044` Butterfly World ground supplies three seam-safe variants. Wrap once per
  authored planet patch or randomize variants between patches. Never repeat one
  variant as a visible grid.
- `R045` and `R046` are different gates. The first is the home gate; the second
  is the inter-world gate. `R047` presents both identities during transition.
- `R075` is the empty Christmas tree used before completion.
- `R076` is the completed tree and contains exactly five ornaments.
- `R084` contains the five separate ornament pieces manipulated by gameplay.
- `R078` is the fish body; all five `R079` fin files stay separate for assembly.
- The three star roles are not interchangeable: `R040` dream, `R041` crown,
  and `R042` chamber focal each use a distinct silhouette and function.
- `R020` rebuilds only frames and placement. Its protected book paintings must
  be mounted unchanged at integration time.

## Review Evidence

Read `audit/full_regen_2026-07-18/candidate_role_review.csv` for the complete
role ledger and `candidate_asset_review.csv` for every candidate file. Contact
sheets include full-size, repeated-tile, and 112 px phone-scale views. The pack
is ready for owner review and selective integration, not automatic wholesale
replacement.

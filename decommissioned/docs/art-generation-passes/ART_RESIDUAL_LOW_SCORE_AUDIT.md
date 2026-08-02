# Residual Low-Score Art Audit

Date: 2026-07-15

Scope: all art with a prior score of 0-2/5, checked against current runtime
consumers after Remediation Batches 01-04. Protected book art, family voice
recordings, and friend cutouts were inspected for routing only and were not
modified.

## Result

There are no remaining active, automatically replaceable 0-2/5 art roles.
The two active low-score families require owner source material or approval.

| Score | Active family | Runtime use | Required next action |
|---:|---|---|---|
| 1 | `assets/mg/cat_body.png`, `cat_accent.png`, `cat_line.png` | Craft Studio paint layers | Do not generate. Rebuild from photographs of the child's own toy. |
| 2 | `assets/mg/bird_body.png`, `bird_accent.png`, `bird_line.png` | Craft Studio paint layers | Do not redesign. Separate approved color and line zones from canonical Baby Eagle source art only after owner approval. |

## Replaced Runtime Roles

| Former score | Former role | Current normal path | Status |
|---:|---|---|---|
| 1-2 | Picture-game coal, growth stages, flowers, bushes, trees, ornaments, sun, and star | Batch 02 Blender renders at the existing `assets/mg/` paths | Replaced in place, provisional 4/5 |
| 2 | Fish body and fin craft layers | Registered Batch 04 body and fin art with the retained independent line layer | Replaced in place, provisional 4/5 |
| 2 | World leaf, grass, flowers, and beach ball inventory | Batch 04 painted replacements; the beach-ball runtime role uses a matte shader | Replaced or dormant, provisional 4/5 |
| 2 | Kart coral, seaweed, rocks, shells, sand dollar, crab, and decorative fish | Exact GEN2 role models; fish set is now clownfish, turtle, stingray, and dolphin | Re-routed, provisional 4/5 |
| 2 | Galaxy and kart butterflies | Complete paired-wing `butterfly_story.glb`, then GEN2 card fallback | Re-routed, provisional 4/5 |
| 2 | Procedural anemones and urchins | `anemone_story.glb` and `urchin_story.glb`, including efficient meadow MultiMeshes | Re-routed, provisional 4/5 |
| 2 | Procedural giant fish | `giant_fish_story.glb` with paired fins and horizontal flukes | Re-routed, provisional 4/5 |
| 2 | Generic monster truck | `monstertruck_story.glb` | Re-routed, provisional 4/5 |
| 2 | Static plush Huluu GLB | Protected Huluu illustrated cutout | Retired from normal play |
| 2 | Visible photo/HDR lagoon sky | Illustrated procedural day and dusk sky bands | Retired from normal play |

## Retained Low-Score Files

These files remain intentionally. They are not normal-path art defects.

| Family | Reason retained |
|---|---|
| Legacy `assets/aquatic/*.glb` | Missing-file fallback and migration source; no new direct consumer is allowed. |
| `assets/galaxy/butterfly1.glb`, `butterfly2.glb` | Missing-file fallback behind the complete butterfly and GEN2 cards. |
| `assets/vehicles/monstertruck.glb` and atlas | Missing-file fallback behind the story truck. |
| Legacy Roshan, Fairy, Huluu, and Chuck models | Character migration fallback or probe input. Character replacement is a separate owner-controlled project. |
| `assets/sky/lagoon_day_2k.hdr`, `lagoon_dusk_2k.hdr` | Licensed dormant inventory; no visible runtime consumer. |

## Reversal Archive

Original raster files from `origin/master` are mirrored under
`backups/art_pre_remediation_2026-07-15/`. The JSON manifest records the source
commit and SHA-256 values for both original and replacement files. To restore a
single disputed item, copy its mirrored file back to the same repository path
and run a Godot import. Legacy GLBs were not overwritten and therefore need no
duplicate backup.

## Next Audit Boundary

The next art pass should begin at 3/5, not revisit this list. The leading 3/5
families are galaxy crystals, fruit, beetles/ladybugs, and tropical plants.
They need gameplay-context review before generation because their silhouettes
and functional roles are already sound.

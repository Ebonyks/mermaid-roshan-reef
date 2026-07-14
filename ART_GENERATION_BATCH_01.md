# Mermaid Roshan Art Generation Review Batch 01

_Target: 36 first-pass review assets_

Ready-to-paste Google AI Studio prompts for every row (plus the Batch 02
texture sheets) live in `NB_AI_STUDIO_EXPORT.md`.

This is a calibration batch, not an automatic runtime replacement. Every image
must be reviewed beside its book pages and intended in-game size before import.
No existing runtime asset is overwritten by this batch.

## Batch rules

- Use the motif-specific rules in `ART_STYLE_GUIDE.md` before the general prompt.
- One generated image per named asset or animation pose.
- Use a flat removable key background for isolated art and retain complete anatomy.
- Use crisp cel value shapes. Reject gradients, painterly volume and inherited
  mascot faces where the book depicts an ordinary animal or object.
- Stay decisively cartoon-side: broad silhouettes, few interior marks and no
  specimen-level texture, even when the motif remains species-readable.
- Keep props modular: no ground island, neighboring species, particles or baked
  dressing unless the row explicitly asks for a composed reference.
- Normalize review files to a maximum 1024-pixel side. Approved assets require a
  separate alpha-matte and in-game integration pass.

## Planned assets

| # | Review asset | Book family/pages | Intended role |
|---:|---|---|---|
| 1 | Monarch butterfly - wings open | Butterflies, 18-20 | Complete dorsal animation frame |
| 2 | Monarch butterfly - wings half-folded | Butterflies, 18-20 | Matched animation frame |
| 3 | Blue butterfly - wings open | Butterflies, 19-20 | Complete dorsal animation frame |
| 4 | Blue butterfly - wings half-folded | Butterflies, 19-20 | Matched animation frame |
| 5 | Stag beetle | Beetles, 18 and 34 | Museum/garden creature card |
| 6 | Ladybird beetle | Beetles, 18 | Small readable creature card |
| 7 | Green jewel beetle | Beetles, 18 | Museum creature card |
| 8 | Pale mint border coral | Page-border reef, recurring | Quiet framing prop |
| 9 | Coral-blush border coral | Page-border reef, recurring | Quiet framing prop |
| 10 | Lavender branching scene coral | Immersive reef, 19-20 | Modular world prop |
| 11 | Coral-pink mound coral | Immersive reef, 19-20 | Modular world prop |
| 12 | Rounded leafy garden bush | Plants, 10 | `k_bush2` direction |
| 13 | Woody leafy shrub | Plants, 10 | `k_bush` direction |
| 14 | Orange flowering shrub | Plants, 10 | `k_flower1` direction |
| 15 | Coral-red flowering shrub | Plants, 10 | `k_flower2` direction |
| 16 | Rosette succulent | Plants, 10 and 34 | `flower` family direction |
| 17 | Paddle cactus with sparse buds | Plants, 10 and 34 | Garden variety |
| 18 | Aloe plant | Plants, 10 and 34 | `sprout`/leaf direction |
| 19 | Snake plant | Plants, 10 | `leaf` direction |
| 20 | Small broadleaf tree | Plants, 10 | `tree` direction |
| 21 | Small pine tree | Seasonal plants, 7-9 and 27 | `k_pine` direction |
| 22 | New seedling | Plants, 10 | `k_sprout` direction |
| 23 | Pink watering can | Garden prop, 10 | `wateringcan` replacement |
| 24 | Lamb plush calibration | Plush toys, 11 and 28 | Toy-family calibration only |
| 25 | Bear plush calibration | Plush toys, 11 and 28 | Toy-family calibration only |
| 26 | Child-made paper cat craft | Handmade crafts, 21 | Craft-family calibration only |
| 27 | Matte purple round ornament | Seasonal, 27-29 | `orn1` direction |
| 28 | Rose ribbed finial ornament | Seasonal, 27-29 | `orn2` direction |
| 29 | Pearl-blue round ornament | Seasonal, 27-29 | `orn3` direction |
| 30 | Warm-gold five-point star ornament | Seasonal, 27-29 | `orn4`/star direction |
| 31 | Lavender teardrop ornament | Seasonal, 27-29 | `orn5` direction |
| 32 | Snow-covered Christmas tree | Seasonal, 27-29 | `k_xmastree`/`xtree` direction |
| 33 | Friendly snowman coal piece | Seasonal, 8-9 | `coal` replacement |
| 34 | Glow-tip anemone | Immersive reef, 19-20 | Procedural anemone replacement |
| 35 | Rounded sea urchin | Immersive reef, 19-20 | Procedural urchin replacement |
| 36 | Giant gentle fish silhouette | Immersive reef, 6 and 32 | Procedural distant-fish replacement |

## Explicit exclusions

- `assets/mg/carrot.png` is direct source-book art and is not a replacement target.
- Existing protected characters, named family toys and book cutouts are not edited.
- Branded toys depicted in the book are not copied.
- Sky panoramas, terrain tiles, vehicles and track motifs wait for a later batch so
  this review can answer the motif-style question without mixing asset contracts.

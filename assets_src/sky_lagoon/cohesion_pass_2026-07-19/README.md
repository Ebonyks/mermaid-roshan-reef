# Sky Lagoon cohesion reference batch

Review-only model direction generated for the 2026-07-19 in-frame cohesion
audit. Nothing in this folder is a runtime replacement. `assets_src/.gdignore`
keeps the batch out of Godot imports and the APK.

## Layout

- `raw/`: untouched built-in image-generation outputs.
- `selected/`: high-quality bicubic review copies normalized to a maximum 1024
  px edge.
- `rejected/`: retained unsuccessful direction. The square-window castle is
  rejected because it cannot accept the existing tall protected book image.
- `contact_sheet.jpg`: overview only; inspect original selected sheets for
  modeling detail.
- `PROMPTS.md`: exact generation contracts and tool limitations.

## Selected review hashes

| File | Dimensions | SHA-256 |
|---|---:|---|
| `selected/alpine_chalet_family_v1.png` | 1024x683 | `4D543CE4F080799FD000964D6DDD87D83043D6D82EEECB955FC5800FFAE41E57` |
| `selected/alpine_mountain_cave_kit_v1.png` | 1024x683 | `79AA6C0B463A018FEAA023B6C9F7D9E7284A59BF78FCAA295B940FF2C3740805` |
| `selected/butterfly_world_gate_turnaround_v1.png` | 1024x683 | `CE3ED76B326F9C3DACB4DC5ACBE6AAEEE432FA2922B1FFFAFB5E9D1B175AF171` |
| `selected/courtyard_train_companion_cars_v1.png` | 1024x1024 | `74337761B1931F18A29C42331C37F9A24171A9D3B9CE04B4BA6F31B57D6D2E15` |
| `selected/path_bridge_water_edge_kit_v1.png` | 1024x683 | `582B687A2C253CFDFD58B90EC7BB38501BC6F954DD409A70BE7051770A7E1308` |
| `selected/pearl_castle_exterior_turnaround_v2.png` | 1024x683 | `00EED099CAE3ACD94725E8F80E6C48853B5FE5976DB03D3EC0CE5CB2633A6DC4` |
| `selected/protected_memory_frame_turnaround_v1.png` | 1024x683 | `249E9C99BE907F4866410A714ECC4D3B2F3850629C4FF36C14F8061D05A2E8AA` |
| `selected/storybook_path_lantern_turnaround_v1.png` | 1024x683 | `6AB03E2F1AE136CCA9B37BD06F0097CC393523CAA098D396589BECF67E2F57F9` |
| `contact_sheet.jpg` | 1066x1358 | `EDA2CB7B86BD42F14798BEAEDDFBC05A95BF217A1B18D979A7E08CCEC139A731` |

The untouched raw hashes are the generation-output hashes recorded during the
session. They can be recomputed with `Get-FileHash`; selected files are the only
copies intended for ordinary design review.

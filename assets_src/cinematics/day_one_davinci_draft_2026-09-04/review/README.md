# Resolve cut-boundary diagnostic boards

These thirteen boards are inspection-only derivatives of the rendered MP4 drafts. They are not generation inputs, delivery pixels, accepted keyframes, or evidence of full-speed playback. Each board samples every shot midpoint and both sides of every adjacent hard cut using the record ranges in `../RESOLVE_READBACK.json`; thumbnails are uniformly scaled to 320×180 and tiled without subject edits.

Extraction tool: project-bundled FFmpeg 8.1.2. Source: `../exports/D1-Cxx.mp4`. Role: `diagnostic_review_only`. `used_as_delivery_pixels: false`. `used_as_generation_pixels: false`.

| Board | SHA-256 |
|---|---|
| `D1-C00_CUT_BOARD.png` | `790a7f0b1d890abc3c50e9a91fa3ffda6eeb0d46037b25260fcbe8cf58767013` |
| `D1-C01_CUT_BOARD.png` | `7bfa16a8f167c7c38c5ee0d8bfe46b2e75f0524e2d2fb1901210850cd7c95e6e` |
| `D1-C02_CUT_BOARD.png` | `9d3303b0cd2d0047c8b283e509b810ccc89a4ac34a053abc74b851f3217fa1f5` |
| `D1-C03_CUT_BOARD.png` | `f2aa669636740c0254fb145b1974fa265008d54155691e69279e3b97e7d4314c` |
| `D1-C04_CUT_BOARD.png` | `c4ed711df6fe3ef83472ed9a82994ca95c45e6a3b76c4852983d6f3af0692e9c` |
| `D1-C05_CUT_BOARD.png` | `d157e0f7b1ac471ed480b9313654cc3b9913152ba0403bc6862d6aee2c616568` |
| `D1-C06_CUT_BOARD.png` | `12275489e4fa0c9e03eebda19653da248177fd934d71282182ea8100ab30fee7` |
| `D1-C07_CUT_BOARD.png` | `9d232f28d0a103674c10e2b7e272109e4e4495820e68f66e8a263c95f19e3484` |
| `D1-C09_CUT_BOARD.png` | `b77f1b1c8ce80d14e2456542ce8815f192f1bded50ac77541bd78f98cb8f4185` |
| `D1-C10_CUT_BOARD.png` | `ee0471e07ba545e359854e5b0ad71a7c304dc52160d40f32b7281233247d87ba` |
| `D1-C11_CUT_BOARD.png` | `27d74a78d5ea96bf345e916f7963a7b259d0834d900c1bebe0baf40abe047d08` |
| `D1-C12_CUT_BOARD.png` | `4962650c2e12729cbb8f26738d4579e00741f01cc58bf3d3be4a55f1da9b3862` |
| `D1-C13_CUT_BOARD.png` | `d946ca646519f003019b77e3b1ca60a3d76781472983cdf83ceb4dcd87422f70` |

Cut-specific findings are recorded in `../RENDER_REVIEW.md`.

## V02 replacement boards

The original thirteen `D1-Cxx_CUT_BOARD.png` files remain V01 history and were not overwritten. The original Resolve readback is archived at `../history/8243d88f004c/RESOLVE_READBACK.json`; the packet-root readback reflects the active V02 project.

| Board | SHA-256 | Result |
|---|---|---|
| `D1-C04_V02_CUT_BOARD.png` | `4a12637b08ff2dd877927b844f46a822b44f756cacda80861ed75cb2e7709985` | Flooded-floor shot absent; direct scrub → clean-room endpoint remains visibly provisional. |
| `D1-C12_V02_CUT_BOARD.png` | `d312bf27fc97713a8f378ae077159776d02bf9420ce0a8a058f9de02fbdc4d47` | Modern-bedroom/false Stuffie Room absent; five-shot recap ends on family hug. |

These V02 boards use the same diagnostic-only method and pixel restrictions as the V01 boards.

## V03 final recap board

`D1-C12_V03_CUT_BOARD.png` samples all four shot midpoints and both sides of all three hard cuts in the final eight-second recap. SHA-256: `6677dba09e8330bfe049fb3cf705e8718cd9f235e3a7f993632da84f28989a96`. The flooded Bathroom, modern bedroom, false Art room, and unverified friendship vignette are absent. The visible order is clean Bathroom endpoint → Pool/Rumi → room-correct Art desk wake → Main Hall family hug. It remains diagnostic-only and grants no acceptance.

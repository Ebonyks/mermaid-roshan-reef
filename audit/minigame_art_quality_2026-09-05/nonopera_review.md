# Non-Opera minigame art quality review

Date: 2026-09-05
Source worktree: `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/minigame-art-quality-20260905`
Scope: current non-Opera minigame source and directly inspected raster assets.
Runtime status: a 43-frame capture packet exists, but reviewed frames are invalid for minigame art scoring because the main menu/reward overlay dominates; no valid minigame canvas or device acceptance capture is claimed.

## Audit basis and evidence boundary

The binding medium criteria are `DL-MED-01` (true 2D authored medium and runtime structure), `DL-MED-04` (no `Node3D`/`Sprite3D`/3D staging as final language), and `DL-MED-05` (preserve drawn contours and identity colours). Visual and animation review uses `DL-VIS-07` (5/5 requires owner acceptance in runtime context), `DL-MOT-01` (identity, anatomy, topology, and stable contact), `DL-MOT-03` (coherent authored states, stable pivot, and return state), and `DL-MOT-04` (visual/audio feedback describe the same event).

Scores below are subjective isolated-image scores for assets actually viewed in this review. They are not runtime acceptance and do not inherit the historical whole-area scores in the master audit. An uncaptured family is recorded as unknown rather than scored.

## Directly viewed live assets

| Asset and exact live binding | SHA-256 | View finding | Isolated score | Priority |
|---|---|---|---:|---|
| `assets/mg/carrot.png`; `scripts/games/picture_games.gd:414` button at `(360,600)` size `150x110`, and `:430` face bit size `95x60` | `B4C35BEE6DE1A161F6891396A3B903D22893F772919BBBFE5832E5256E834A8F` | 128×128, 347-byte flat orange silhouette. It has a transparent canvas but almost no painterly volume, texture, or child-readable carrot detail. It is visibly weaker than the adjacent painted snowman, sun, star, and coal assets. | 3.0/5 | High |
| `assets/mg/wateringcan.png`; `scripts/games/picture_games.gd:596`, garden prop at `(1022,362)`, displayed `130x137`, rotated `0.32` radians | `DFCD93A98E83B7B0419602DB828E6895FD4884BF0DF800E9ECF4ED96C436F6E9` | 272×286 low-resolution crop. The viewed pixels include plant/background material and a hard rectangular source boundary. It is not a clean transparent prop, and the spout/angle needs a purpose-built replacement. | 2.5/5 | Critical |
| `assets/mg/k_flower1.png`, `assets/mg/flower.png`, `assets/mg/flower2.png`, `assets/mg/k_flower2.png`, `assets/mg/flower3.png`; `scripts/games/picture_games.gd:567,632` final growth states, each in a `228x228` rect | hashes below | Five live mature-state assets are a flat pastel/vector-like family: uniform fills, sparse shading, thin outline, and little texture. They are materially below the painted `seed`, `sun`, `butterfly`, and Roshan art used in the same garden surface. `flower4.png` is present on disk but is not proven live by the current runtime list. | 3.0/5 family | High |
| `assets/mg/k_sprout.png`; `scripts/games/picture_games.gd:623` intermediate state in a `148x148` rect | `D7542D8D812A28DDCE435C8ACF3A103DF85E5AF59178AD05C9BDB5FEF1ED0926` | Simple gradient-filled sprout and oval soil patch. It communicates the state, but lacks the painterly depth and contour specificity of the seed and the surrounding garden props. | 3.0/5 | High |
| `assets/mg/k_flower1.png`; `scripts/games/picture_games.gd:567,632` slot 0 (`k_flower1`) | `C4EDBD641F0CC13E96378B7468F56711B7DD79BB9F90013BFBE66588472FB35E` | Viewed pixels show the same simplified pastel family: six pale petals, flat purple center, low texture, and the shared minimal leaf/stem. Distinct silhouette/color is preserved, but finish is below the surrounding painted garden assets. | 3.0/5 | High |
| `assets/mg/k_flower2.png`; `scripts/games/picture_games.gd:567,632` slot 3 (`k_flower2`) | `522130AD5C354B1A80AA9734FEB025D23C4551AF6796CD89F9664D2C0750553D` | Viewed pixels show the same simplified family: eight pale yellow petals, flat pink center, low texture, and shared leaf/stem. It is a useful distinct role but below the 4.5 target in finish and material detail. | 3.0/5 | High |
| `assets/props/story/flower_lavender.png`; candidate only, no current PictureGames binding | `650FFBFE85CB93D9B42D12F9B291BA25F35285F641B5221A6300FE474554438B` | Clean transparent polished full plant with three lavender flowers, leaves, and roots. Stronger art quality, but its full-plant composition does not match the existing 228×228 flower-state layout without cropping or role changes. | 4.2/5 candidate | Do not force |
| `assets/props/story/flower_coral.png`; candidate only, no current PictureGames binding | `816C23A8A51E20FF9837CBBE7631375178B7BDA0F3ED9D0A807CBFD23403D724` | Clean transparent polished single coral flower with stem, leaves, and roots. Strong candidate for one mature state only, but it cannot supply all four distinct flower roles. | 4.2/5 candidate | Do not force |

The live flower hashes are: `k_flower1.png` `C4EDBD641F0CC13E96378B7468F56711B7DD79BB9F90013BFBE66588472FB35E`; `flower.png` `2753083D4E30F5F5E6B8B49949E0EB50497B5B03D37691DF7E3B6B6DEDDB79880D`; `flower2.png` `1AB22C71A550C94C71FCAB769C6F1B47F1D73C1FF792775FDC1F9C365AC77A09`; `k_flower2.png` `522130AD5C354B1A80AA9734FEB025D23C4551AF6796CD89F9664D2C0750553D`; `flower3.png` `46E05838998044AA1FB36738719FE769521D4B727D891C6062F5EC4CBBE56352`. `flower4.png` (`FED78117C484B52A69A1808E8AA19C0D3FA5A3F388EDC8B9EE9DF85384066D68`) is present but not proven live.

## Reuse decision for PictureGames

No `picture_games.gd` change is made. The two approved story flowers are higher quality, but they are not a complete four-state replacement set and have different full-plant geometry. Reusing one or two of them for all final states would erase the authored role distinctions recorded by the live code:

```gdscript
m.mg["flowers"] = ["k_flower1", "flower", "flower2", "k_flower2", "flower3"]
```

The correct next art work is a coordinated six-asset garden family: one sprout plus five distinct mature results, or an owner-approved mapping that preserves each plant's color, silhouette, visible height, stem-bottom anchor, and semantic progression. The story flowers remain reusable references or candidates for one final state only after a complete family is available. The farmer carrot concept was rejected because `assets_src/concepts/opera_jobs_flat_2026-07-21/cards/opera_job_farmer_gameplay_carrot.png` is a pig character on a dark scene card, not a clean carrot prop. `assets/art35/cards/mg/carrot_carrot.png` is the same weak carrot.

The watering can has no suitable approved clean equivalent in the current asset inventory. Leave it as an explicit replacement gap until a transparent, sufficiently large can with the correct spout direction and rotation is available.

## Unknown or uncaptured families

No score is assigned to Dolls, Melody, SlideRace runtime framing, Bathroom Cleanup composition, Fairy runtime staging, Fetch, Treasure, Shop, Brawl imp animation, DanceEngine procedural surface, SideScroll modes, or the inactive `k_*`, cat, and bird assets. Source tracing can identify their callers, but isolated source reading cannot establish the exact runtime composition, scale, contact, animation identity, or child-device legibility required by `DL-VIS-07` and `DL-MOT-*`. They require serialized 1280×720 and phone-ratio captures before any below-4.5 replacement decision.

Dust Boss is also excluded from a new commission decision here. A parallel rebuild is already active in `.worktrees/bunny-battle-rebuild`; coordinate its candidate and audit the resulting runtime rather than duplicating generation.

## Replacement-ready specifications

1. Carrot: transparent RGBA, clean silhouette, high-resolution source, painted Wind-Waker-inspired storybook shading matching `coal.png`/`sun.png`; preserve the existing button footprint and face-bit placement; no scene/background pixels.
2. Watering can: transparent RGBA at least 512px native, clearly readable handle/body/spout, spout aligned to the existing `0.32`-radian garden presentation or accompanied by an intentional new angle; preserve the `130x137` touch/display role while improving visible detail and alpha edges.
3. Garden family: replace as one coordinated set. Keep seed → sprout → mature flower progression and the existing bottom anchor (`GARDEN_ART_BOTTOM`); produce five distinct mature silhouettes/colors, with no reuse of two random flowers to fill four slots.

Each candidate must be inspected as a clean isolated image, checked for alpha contamination and source provenance, imported, captured in runtime context, and reaudited. A clean isolated image cannot claim 5/5 without owner acceptance in runtime context.

## Current capture packet review

The generated packet under `tmp/art-quality/picture-profile/appdata/Godot/app_userdata/Mermaid Roshan Reef of Light/minigame_art_quality_2026-09-05/` contains 43 PNGs, but the reviewed frames are not valid minigame art evidence: the 1280×720 images are dominated by the main menu and reward overlay rather than the active PictureGames canvas. Representative examples are `001_snowman_ready.png`, `005_snowman_face_ready.png`, `009_snowman_chase_ready.png`, `011_snowman_final.png`, `012_garden_ready_all_seeds.png`, `028_garden_all_five_mature.png`, `029_trampoline_ready.png`, `034_trampoline_final.png`, `035_xmas_ready_empty_tree.png`, `040_xmas_ornament_5_placed.png`, and `042_xmas_all_ornaments_no_flower_button.png`. These filenames document attempted state boundaries only; they do not support a runtime score for snowman, garden, trampoline, or xmas art. The visible reward/sticker overlays in some frames are evidence that a route or reward overlay was reached, but not evidence that the underlying minigame surface was captured.

The xmas filename `042_xmas_all_ornaments_no_flower_button.png` is an incomplete capture label, not a confirmed game defect. It may reflect the route closing before the flower button capture or harness teardown timing; it must be investigated with a route-ready capture before any completion claim. The harness also freezes main processing and manually ticks the minigame, so animation cadence and natural tween timing remain unqualified even where a future canvas capture is valid.

For that superseded packet, all four PictureGames runtime scores remain `UNCAPTURED`; the isolated asset scores above were the only valid scores at that stage.

That earlier packet is superseded for review purposes by the corrected final packet at `tmp/art-quality/picture-profile-final/appdata/Godot/app_userdata/Mermaid Roshan Reef of Light/minigame_art_quality_final_2026-09-05/`. The final packet has active canvases and is the evidence used below. It was driven by the corrected harness with manual ticking, so animation cadence remains a qualification gap.

## Corrected final runtime review

These are subjective visual scores for the observed 1280×720 frames only. They are not owner-accepted 5/5 claims under `DL-VIS-07`.

| Active card | Exact viewed frames | Runtime score | Observed weakness and priority |
|---|---|---:|---|
| Snowman | `001_snowman_ready.png`, `005_snowman_face_ready.png`, `008_snowman_face_3.png`, `009_snowman_chase_ready.png` | 3.5/5 | Snowman balls and Roshan are readable, but the orange carrot is visibly a tiny flat silhouette against polished coal and character art; the large instruction card and reward/sticker layers dominate later states. Replace carrot first; then capture natural chase/settle cadence. High. |
| Garden | `012_garden_ready_all_seeds.png`, `014_garden_seed_1_sprout_or_flower.png`, `028_garden_mature_1.png` through `032_garden_mature_5.png`, `033_garden_all_five_mature.png` | 3.0/5 | The garden reads clearly and all five mature states are reached. The pink watering can visibly contains a low-detail/cropped look and is weaker than the painted sun, butterflies, seed, and Roshan. The five flower states are distinct but flat and vector-like, with sparse texture; mature frames also place a large reward overlay over the field. Replace can and coordinated six-asset growth family. Critical/high. |
| Trampoline | `034_trampoline_ready.png`, `035_trampoline_bounce_1.png`, `039_trampoline_final.png` | 3.2/5 | Roshan and the star are readable, but the star is oversized and clips into the HUD/instruction card; the trampoline is a broad procedural blue bar and the repeated reward overlay obscures the action. Reframe the star/HUD and capture unblocked bounce contact at natural cadence. Medium/high. |
| Xmas | `040_xmas_ready_empty_tree.png`, `045_xmas_ornament_5_placed.png`, `047_xmas_post_button_sequence.png` | 4.1/5 | The tree and five ornaments are cohesive, polished, and child-readable. The final frame proves the reward sequence after five placements, but the reward card covers the tree center and no clean post-finale tree-only frame is present. Keep assets; capture the final unobscured composition and natural effect timing. Medium evidence gap. |

The garden captures visibly confirm the exact live five-state list and the weak runtime context: `k_flower1`, `flower`, `flower2`, `k_flower2`, and `flower3` appear across `028`–`032`; `flower4.png` remains inactive/unproven. The final packet's `047_xmas_post_button_sequence.png` is a reward/finale frame after five ornaments; it should not be interpreted as a missing flower-button defect.

## Garden after-repair reaudit — 2026-09-05

The corrected garden packet is at `tmp/art-quality/garden-profile/appdata/Godot/app_userdata/Mermaid Roshan Reef of Light/minigame_art_quality_garden_2026-09-05/`. Representative current captures are `001_garden_ready_all_seeds.png` (SHA-256 `27A4CBA2AA3730CE9A4D7EA47166EDE03A43A60A288EAF03ED6BE139B4D59CD5`), `003_garden_seed_1_sprout_or_flower.png` (`9F903BD8B9D61EBC67C98E9D8E20BDC3A7DA715BE5861F92A912DC6A0ED01B22`), and `022_garden_all_five_mature.png` (`881A71C10BCC1D5E72690D0E0CE69E4E70B146CC292A53401D387626FC2F2ADB`).

After-repair runtime score: **3.7/5**, up from the 3.0/5 baseline. The repair materially improves presentation: the banner is readable, the sun sits below the HUD, sprouts and all five mature flowers are grounded on their pots, the flower buttons no longer leave visible button panels around plants, and the full mature layout is spacious with no new plant crowding. The five states remain visibly distinct and the final capture proves the completion state.

The score remains below 4.5 because the source art itself is unchanged: the `k_sprout` and five mature flowers are still low-detail, flat pastel/vector-like assets beside the painted sun, butterflies, watering can, and Roshan. The watering can remains the most visible weak prop. The completion banner/reward card still occupies the upper center in `022_garden_all_five_mature.png`, so a clean owner-accepted final composition and natural animation cadence remain open. This is a presentation repair pass, not an art-quality replacement pass.

## Current non-Opera capture plan

This report does not run Godot. The parent integration pass should use the existing entrypoints and probes to capture each live surface at 1280×720 and a phone ratio, then attach the image and source hash to the ledger:

- PictureGames: `scripts/probe_mg2d.gd` for the five picture-game routes and state progression; capture snowman, garden seed/sprout/five mature slots, trampoline, slide GO, and xmas placement/finale.
- Dolls: `scripts/probe_dolls.gd` plus `scripts/probe_opera_nursery.gd` for the bounded catch surface and authored fall/contact states.
- Seek: `scripts/probe_seek.gd` and `scripts/probe_visual_audit.gd` for Evie/Lamb-a framing, four targets, reveal, and return state.
- Melody/Fetch/Fairy/Treasure/Shop/Brawl: use their named probes (`probe_melody.gd`, `probe_fetch.gd`, `probe_fairy_art.gd`, `probe_dungeon.gd`, `probe_collection.gd`, `probe_combat.gd`) and record the exact route; legacy spatial surfaces require an explicit `DL-MED-04` debt note.
- Day One pool/bathroom: `probe_day_one_pool_cleanup.gd`, `probe_day_one_bathroom_cleanup.gd`, and `probe_day_one_bathroom_integration.gd`; capture dirty, interaction, contact, clean/reveal, and teardown states.

For every capture, review identity, alpha edges, scale/anchor, action/contact/settle, visual/audio agreement, and phone-size readability. A source score remains provisional until the exact runtime image is reviewed; `DL-VIS-07` explicitly says a clean isolated render or green technical gate cannot grant 5/5.

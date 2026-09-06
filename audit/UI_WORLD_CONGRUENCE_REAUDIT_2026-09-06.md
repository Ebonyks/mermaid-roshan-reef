# UI/world congruence re-audit — 2026-09-06

Authority: `SUPPORTING_CURRENT`, bounded independent AI visual review by Astra. Source baseline `aad0d450d8b8f1381badeeb4bcb939181115ab00`, branch `codex/ui-opera-design-language-20260905`. Filename uses the requested review date; the task spans the September 5–6 local/UTC boundary.

**Result: Pearl Stage v1 is too ornate and reflective to establish the reusable game-wide UI default. Its picture readability and proposed target allocation remain useful.** This is a narrower, evidence-backed correction to the previous material/family verdict, not a claim that every shell, gold trim or decorative cluster is wrong.

## Question and authority

The user requested a comparison against the existing **game world**, explicitly reconsidering whether the newly proposed UI is over-the-top. This re-audit reopened non-UI paintings across Opera, Castle and Sky Lagoon alongside the actual unchanged pause/chooser images. It did not use the previous concept PASS as evidence of congruence. `AGENTS.md`, `SECURITY.md`, canonical `DL-VIS-01–05`, `DL-READ-01–03` and the acceptance boundary control this review; section 21 is being revised by root in response to the new direction.

The first review correctly identified large pictures and a dominant resume, but was too permissive about material and ornament consistency. It checked native Opera paintings, yet allowed the generated menus to validate one another as a coherent family and did not test portability against Castle and outdoor world art. Same-family consistency is not world congruence. Its static readability/provenance evidence survives; its global material/default-family PASS is **SUPERSEDED for this scope** by the findings below. The historical review remains intact.

## Inspected evidence and source roles

Every image below was opened through `view_image` in this re-audit. Hashes are SHA-256 of unchanged bytes. Paths are repository-relative. Existing menu phone proxies were reopened as an inspection aid only; they are not new generations or device evidence.

| ID / exact path | Dimensions | SHA-256 |
|---|---|---|
| W1 `assets/opera/worlds/backdrops/world_ballerina.png` | 1024×576 | `0011569b86b3c194cbcc8c6a2c7ad2e9278f3092640d0b55a771c02ddb9426a1` |
| W2 `assets/opera/worlds/backdrops/world_candymaker.png` | 1024×576 | `19ac984638fea33e0f0cb649b7d51b1364f13c36f0e5c5dd4e883dc283ef5d48` |
| W3 `assets/opera/worlds/backdrops/world_painter.png` | 1024×576 | `582276aa838559c392dcf64df6440e909e47d9aaafb38031f78b3208d0279d14` |
| W4 `assets/opera/worlds/backdrops/world_farmer.png` | 1024×576 | `947d0d2aa3b04677f1d0539acbed722252c05dcc687f0917c7b8fc569d0a803e` |
| W5 `assets/flats/castle/interactions_v4/backgrounds/room_kitchen_background.png` | 1024×576 | `b58bd03a394717ebff381d76e4cb7d03410a463b7b30d2a58065be5a4df8c065` |
| W6 `assets/flats/castle/interactions_v4/backgrounds/room_playroom_background.png` | 1024×576 | `bd0baef94bad5c9257c0ab20d239513bd42ef465584fec6f012d990993ce797b` |
| W7 `assets/flats/castle/interactions_v4/background_tiles/room_kitchen_background_r0_c2.png` | 1024×768 | `757c89aaf143d61d4d1e17f4f7c53ac23a2bc7c0fbf36c5bcd980568e1f7fb67` |
| W8 `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c1.png` | 1024×1024 | `ae962d17088df75e6f3db9fd632a1c2f105d91a902996cd5ac5aba184f82fc1d` |
| W9 `assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r1_c1.png` | 1024×1024 | `2fb96fa18f1e9ccec77ba4f1fd162223385fdfaa230f57647f0240de27ca1400` |
| C1 `assets_src/ui/pearl_stage_v1/concepts/pause_menu_pearl_stage_concept_v1.png` | 1672×941 | `cb3dd0824943562ffc4d2eb9729dbbaf42fbd71d508421066950d8ffed427b3f` |
| C2 `assets_src/ui/pearl_stage_v1/concepts/activity_chooser_pearl_stage_concept_v1.png` | 1672×941 | `28c8308a561b1088cc559fcb0cb9ae601a2d033f55d9cd7dd685823fd3fd6460` |

World roles were traced rather than inferred from filenames:

- W1–W4 belong to the career-world painting family. `scripts/opera_world_backdrop_2d.gd:81` constructs `world_%s.png`; `:163` loads corresponding world/stage tiles, and `:235` prefers the available tile set before `:240` falls back to the painting. These inspected 1024×576 images are useful world-art comparators, not proof that each exact PNG is today's visible background. The `sky_lagoon_farmer` variant explicitly clears the Farmer painting and loads Sky v5 columns 2–3 (`:72`, `:91`); W4 is retained world-family variety, not current Farmer-route authority. The Stuffie-room variant similarly overrides the generic painting. No deprecated venue is reintroduced by this review.
- W5/W6 are v4 logical room audit/background plates. The current Castle helper `scripts/arena/castle_fixture_rigs.gd:11` reads `assets/flats/castle/interactions_v4/castle_interactions_v4.json`; the manifest declares kitchen/playroom `generated_full_frame_pixel_ownership_tiles` routes under `interactions_v4/background_tiles`. `scripts/arena/castle_rooms_25d.gd:1472` loads those tiles and `:1492` chooses the validated native root. W7 directly samples that native runtime-tile family. The low-resolution plates are not described as the runtime's sole texture or as capture evidence.
- W8/W9 are two vertically adjacent actual Sky v5 runtime tiles. `scripts/arena/sky_lagoon_promenade.gd:420` constructs the 6×2 tile set and names its Canvas role `base_panorama`. They sample sky/distant mountain and foreground path/foliage respectively. Two tiles do not prove the entire panorama, exact viewport composition or night-state appearance.
- C1/C2 are review-only generated UI concepts, not current gameplay art. Their exact provenance and 640×360 whole-image proxies remain recorded in `UI_PEARL_STAGE_CONCEPT_REVIEW_2026-09-05.md`.

Additional older Castle composites were inspected only to check source-family continuity: `assets/flats/castle/rooms/room_kitchen.png` (1024×576, `ee2f05ce1eff483060ace90aee729a561b3ddf471d25d5a5c75eb9b9ba948104`), `room_kitchen_background.png` (same bytes/hash as W5), and `room_playroom.png` (1024×576, `5c7797c3be3586daca648f4fa4ab1161368f1c99fee719b42ba5efd27f5eaf6f`). These are supporting composites, not new assertions about live fixtures. Initial attempts to open the Castle main-hall master and another Sky tile failed in the image helper. A later whole-composition inspection resolved the master-image limitation as recorded below; the extra unopened Sky tile supplies no evidence.

### Full-composition follow-up for revision-2 references

The exact native Ballerina/Candymaker masters referenced in revised design 11 were also reopened through `view_image`: `assets_src/imagegen/opera_codex_2026-08-02/native/world_ballerina_native.png` (1672×941, SHA-256 `f28231f936b9e63e0697a14122a354ee4c0bad1864538fddbdf16147a311f544`) and `world_candymaker_native.png` in the same directory (1672×941, `e40eb603a6c1e8f2c57be2e704ae0017426f11366de847afad91d57fbd93b017`). These are authored source masters, not byte-identical versions of W1/W2 and not current runtime captures. Their broader shape/material findings agree; no source/rendering differences are concealed.

Direct `view_image` display of two larger PNGs failed. PIL could read them, so complete-canvas RGB/Lanczos inspection reductions were written under ignored `build/ui_world_congruence_review_2026-09-06/` and opened with `view_image`. No crop, subject isolation, retouching or original-file modification occurred; these are analytical display aids, not regenerated or delivered art.

| Source and role | Native binding | Inspected whole-canvas proxy |
|---|---|---|
| `assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png`: source panorama associated with the W8/W9 live tile family | 6144×2048; SHA-256 `017532ae864e534d9b356472e2e29150855ede6583a7f63f02f0401d28c7be41` | `build/ui_world_congruence_review_2026-09-06/sky_full_review_only.png`, 1536×512; `74bc5a0643901924675e32bb218f2c67bce28a7cb81c1d595b1ec1275ca944e5` |
| `assets/flats/castle/main_hall_2screen/main_hall_screen_a_room_led_master.png`: composed hall source, not asserted as the current sole runtime backing or acceptance authority | 2048×1153; SHA-256 `ae84f4f79a8183312b5ba26b6999f26b69c8a538424b5383a7d6623cc2f275e9` | `build/ui_world_congruence_review_2026-09-06/castle_hall_full_review_only.png`, 1024×576; `4975849002ff741e6647336f17b2de45e2590d55be7ab03a1485ac66e3b37b1f` |

The full Sky composition confirms that matte foliage clusters frame broad sky, meadow and an open path; the earlier two-tile inference was not a cherry-picked empty patch. The main-hall source genuinely contains gold architectural bands, pearl niches and an Opera doorway curtain. Its door pictures are comparatively simple and spaced within a broader room. It supports contextual grandeur, not imposing the same ornate surround on every ordinary control. The source shows composition joins and is not being newly accepted or used to infer current rendering quality. These additional observations preserve WG-01–05 and the limited prior hierarchy PASS.

## What matches and what does not

There is real shared vocabulary. W1 Ballerina has gold-rimmed pearl flower pads, ornate shell pavilions and repeated decorative rails. W2 Candymaker has brass collars, satin coral machinery and creamy highlights. W3 Painter has shell plaques on paint vats and warm metal brush ferrules. W5/W7 Kitchen contains shiny lamps and a pearl beside painted pots. The world's art is not uniformly matte or minimally decorated. Removing all trim or replacing it with bare flat rectangles would not follow this evidence.

The mismatch is the **distribution and strength** of those features. C1/C2 place a crown/pearl topper, layered bright metal contour and pearl/scroll pedestal on each control, then repeat the same vocabulary on the enclosing shell and full-screen stage. Every small control is dressed like a ceremonial focal object. In the world examples, richness is varied by object purpose and location; W1's ornate venue is not the material template for W4 farmland, W6 masonry or W8/W9 outdoor space.

| Finding | Concrete comparison | Disposition |
|---|---|---|
| WG-01 Repeated ceremonial trim | C1's three lower medallions and C2's five choice medallions each repeat top pearl, reflective ring and decorative base; the enclosing shell repeats those accents again. W1 supports ornate pads in a specific theatrical setting, but W3 paint vats and W5 cupboards use simpler local motifs. | **FAIL reusable default**, P2 `CONFIRMED_OPEN` concept defect. Keep a shared contour/material language; reduce repeated ornament layers. |
| WG-02 Reflective edge dominance | C1/C2 have multiple bright narrow gold bands and near-white specular rims around nearly every surface; their crown pearl and central action receive bloom/radiating light. W7 native masonry/pots use broad painted shading and modest local sheen; W9 foliage/path is textured and matte. | **FAIL reusable material balance**, P2 `CONFIRMED_OPEN`. Preserve painted depth; make sheen selective instead of the default perimeter signal. |
| WG-03 Imported theatrical backdrop | Both menus fill the outside world with deep violet curtains, crystal-like coral, pearls, bubbles and shafts of light. This is a separate invented stage around the UI. W8's broad airy aqua sky and W5/W6's readable room planes do not support imposing that atmosphere everywhere. | **FAIL portable world context**, P2 `CONFIRMED_OPEN`. Use actual current world context or a restrained situational overlay; theater dressing requires a venue reason. |
| WG-04 Motif/color vocabulary | Aqua, lilac, coral, cream, shell curves and occasional gold/pearls all appear in W1–W7. C1/C2 keep large cool/cream wells and distinct picture colors. | **PASS vocabulary**. No blanket desaturation, gold ban, shell ban or world-art recolor follows from this audit. |
| WG-05 Action readability | At the unchanged 640×360 proxies, resume remains dominant; chooser pictures and neutral close are distinguishable. Ornament consumes attention, but has not made these sampled controls illegible. | **PASS static proxy hierarchy**, with prior one-grid-target/route limits retained. Actual device/child evidence remains absent. |

## Canonical-rule re-evaluation

Results apply to C1 and C2 as proposed reusable defaults, not to the world's own acceptance status.

| Rule | C1 pause | C2 chooser | Reason / boundary |
|---|---|---|---|
| `DL-VIS-01` rounded shape / grouped detail | PASS rounded form; **FAIL global ornament distribution** | PASS rounded form; **FAIL global ornament distribution** | The first review counted outer clusters but underweighted a complete ornate mini-frame repeated at every control. |
| `DL-VIS-02` contour | **FAIL comparative contour restraint** | **FAIL comparative contour restraint** | Clean plum lines exist, but stacked bright metallic highlight rings become the dominant boundary treatment. Exact runtime 2–4 px measurement remains NOT TESTED; no unsupported numeric thickness claim is made. |
| `DL-VIS-03` high-key targets / colored shadows | PASS static image | PASS static image | Actual target wells remain light and readable with colored shade. A dark pause surround alone is not proof of a dark-target violation. |
| `DL-VIS-04` palette roles / selective saturation | PASS narrow hue-role test; WG-03 remains FAIL | PASS narrow hue-role test; WG-03 remains FAIL | Cool wells and warm accents are present and neither image is a full-screen neon field. The problem is imposing a saturated violet theatrical context across worlds, not a measured global palette percentage. |
| `DL-VIS-05` broad painted bands / selective wet accents | **FAIL reusable emphasis** | **FAIL reusable emphasis** | Both retain painted bands, but ubiquitous reflective edging, shine and jewel-like medallions overextend the limited wet/satin accents seen across the sampled worlds. No actual PBR pipeline is alleged. |
| `DL-READ-01` quiet support | PASS target separation; **FAIL restraint as portable surrounding world** | PASS target separation; **FAIL restraint as portable surrounding world** | Cream wells support pictures; high-detail decorative stage corners consume attention independently of any current world. |
| `DL-READ-02` phone identifiability | PASS existing proxy only | PASS existing proxy only | Required static symbols survive; V5 device/HUD composition is NOT TESTED. |
| `DL-READ-03` primary focus | PASS static default | PASS static default | Resume/book remain primary. Good focus does not independently excuse WG-01–03. |

**Updated art disposition: C1/C2 FAIL as game-wide reusable material/style anchors.** Retain them as over-ornate exploration and useful layout evidence. The initial packet's accurate hashes, target calculations and native/proxy observations remain valid. No new image has been generated or accepted; this document does not certify a quieter replacement that has not been made.

## Recommendations for the reusable language

1. Anchor the default to cross-world material behavior: broad painted body, one clear contour, colored contact shade and one restrained highlight. Use the actual world art as the comparator before looking at earlier UI studies.
2. Keep recognizable shell curves and selected pearl/rainbow accents. A simple secondary control does not need a crown, top pearl, gold ring, scroll base and bead train simultaneously. Make decoration vary with role; preserve one stronger focal accent where it helps the action.
3. Separate the portable component grammar from venue dressing. Pause may dim or soften the actual world; it should not invent an Opera-like stage as a mandatory backdrop. Dark curtains, gold railings and coronation crests need context.
4. Preserve picture scale, clear neutral return, quiet wells and generous target geometry. The repair is a reduction in repeated trim, shine and background spectacle, not a reduction in control size or a return to generic flat UI.
5. Future review should bind at least one ornate Opera world, one Castle interior and one outdoor runtime-art sample with explicit consumer/source roles. Assess contour, sheen, decoration distribution and contrast before cross-checking prior UI. A matching pause/chooser pair is not sufficient proof of game-world fit.

## Acceptance limits

This is V1 source/artifact evidence plus independent AI visual judgment, not a runtime capture or owner decision. The sampled world assets are not being globally graded, modified or newly accepted. Runtime layout, focus/press/cancel, voice, save, aspect/typography, device performance, observed child comprehension, owner visual acceptance and master closure remain separate. No game code, art bytes, protected original, git state or earlier audit file was changed by this reviewer.

## Review of the written revision

Reviewed root's revised `design/11_UI_PEARL_STAGE_LANGUAGE.md` in full and canonical section 21 (`DL-UI-VIS-01–11`). **PASS as a written corrective specification**, within the following scope:

- The repeated bevel/rim/medallion and routine-theater defects are directly constrained; simplification preserves painted depth, picture scale, bright identity colors and generous controls.
- Ornament counts are explicitly new revision-2 guardrails, not purported measurements derived from source art. The text recognizes ornate worlds and does not globally ban pearls, shells, gold accents, colored art or venue-specific richness.
- The world comparison is separate from inter-menu matching. New `DL-UI-VIS-11` binds host, other indoor/career and outdoor examples, exact roles/hashes, complete compositions and relevant object scale. It forbids using an elaborate crop or pixel-color average as a substitute.
- V1 images remain rejected style comparisons and useful layout/state evidence; no celebration/finale loophole auto-accepts them. Replacement images, focus/arrow art and runtime/device/child/owner evidence remain unproven.
- One wording refinement was requested and verified as repaired: section-21 rule 02 now says **at most one** modest panel accent, consistent with design 11's optional crest and ability to omit ornament in busy host contexts. The restriction caps adornment without requiring it.

This specification review does not close the confirmed v1 image defects: no replacement image exists. No new image generation, runtime integration, protected-art modification or git action was performed. Only this audit and ignored analytical display aids were written by this reviewer.

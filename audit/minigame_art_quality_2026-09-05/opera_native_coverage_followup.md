# Opera room native-coverage follow-up

Date: 2026-09-05
Scope: read-only metadata, hash, build-code, and provenance tracing in `.worktrees/minigame-art-dev-reconcile-20260905`. No image quality score was inferred from a filename or dimension. No image was edited, generated, imported, or run through Godot.

## Result

**No authored same-room source with native `>=2048×2048` detail was found for any of the 15 live Opera careers.** This records a provenance/2K-screen benchmark gap, not a blanket regeneration order: Opera is a fixed 1280×720 Canvas scene, so quality must be reviewed at the actual shipping scale before deciding whether any source needs replacement. Teacher is the important omission in the earlier wording: it does have a provenance-bound Library room source and live eight-tile route, but its current 3640×2048 master (`SHA-256 8c4dd2a82a8475a07d188565f9f93acce6a471b61e55cf868555b6661ea618a2`) is derived from the 1672×941 generated ownership source (`SHA-256 dea78951144fe242201fbbd0e4e01e5f9f53c20fc5b05777811f82223e7d7066`) by the recorded whole-canvas Lanczos normalization, so it does not prove native authored detail.

The repository does contain preserved, provenance-bound composition sources for 14 careers, including the Teacher Library route. They are useful authority references for actual-scale review. The 2048-square files and runtime tile sets do not by themselves prove native detail: several are deterministic presentation derivatives of smaller source frames. This is an audit limitation to resolve with 1280×720 visual review, not an automatic art-generation authorization.

## Preserved source inventory

The thirteen original Opera entries below are under `assets_src/imagegen/opera_codex_2026-08-02/native/` and are listed in `OPERA_CODEX_NATIVE_PROVENANCE_2026-08-02.json`; their recorded hashes were recalculated. Teacher is the separately traced Castle Library route documented in `audit/interactive_background_ownership_2026-08-29.json`.

| Career | Preserved same-room source | Decoded dimensions | Coverage disposition |
|---|---|---:|---|
| Astronaut | `world_astronaut_native.png` | 1672×941 RGB | Composition authority; below 2048×2048 |
| Ballerina | `world_ballerina_native.png` | 1672×941 RGB | Composition authority; below 2048×2048 |
| Boxer | `world_boxer_native.png` | 1672×941 RGB | Composition authority; below 2048×2048 |
| Candy Maker | `world_candymaker_native.png` | 1672×941 RGB | Composition authority; below 2048×2048 |
| Chef | `world_chef_native.png` | 1672×941 RGB | Composition authority; below 2048×2048 |
| Doctor | `world_doctor_native.png` | 1672×941 RGB | Composition authority; below 2048×2048 |
| Farmer | `world_farmer_native.png` | 1672×941 RGB | Composition authority; below 2048×2048 |
| Magician | `world_magician_native.png` | 1672×941 RGB | Composition authority; below 2048×2048 |
| Painter | `world_painter_native.png` | 1672×941 RGB | Composition authority; below 2048×2048 |
| Pop Star | `world_popstar_native.png` | 1672×941 RGB | Composition authority; below 2048×2048 |
| Racer | `world_racer_native.png` | 1672×941 RGB | Composition authority; below 2048×2048 |
| Detective | `world_detective_native.png` | 1254×1254 RGB | Complete square ownership edit; below 2048×2048 |
| Nursery | `world_nursery_native.png` | 1254×1254 RGB | Complete square ownership edit; below 2048×2048 |
| Geologist | No `world_geologist_native.png` or same-room approved 2K source found | — | No compliant room source; open |
| Teacher | `assets/flats/castle/rooms/room_library.png` plus `assets_src/castle/interactive_background_ownership_2026-08-29/generated_room_library_background_source.png` | 1024×576 logical plate; 1672×941 ownership source; current master 3640×2048 (SHA-256 `8c4dd2…618a2`); current v4 tile r0c0 SHA-256 `d42f48…4e74` | Live Library route exists; current master is whole-canvas Lanczos normalization, so native detail remains open |

Detective and Nursery have an additional traceable edit source under `assets_src/opera/interactive_background_ownership_2026-08-29/`:

- `generated_world_detective_missing_crown_source.png`, 1254×1254 RGB, removes the crown painted beneath the live missing-object card.
- `generated_world_nursery_empty_bottle_nook_source.png`, 1254×1254 RGB, removes the bottles painted beneath the live feeding-bottle card.

`audit/interactive_background_ownership_2026-08-29.json` binds those sources, prompts, dimensions, promoted natives, derived masters, and runtime tiles. It records `human_owner_review: pending`; these files solve pixel ownership, not native coverage or owner acceptance.

Geologist has a separately documented 1672×941 grotto composition candidate under `assets_src/geologist_rebuild_2026-09-05/`. `design/GEOLOGIST_REBUILD_2026-09-05.md` explicitly marks it reference-only because it is below 2048×2048. It is not an approved compliant room master. Teacher does have an equivalent live Library route, but its source/master chain is documented below as upscale-only.

## Why the 2048 files do not qualify

For the 13 original careers, `assets_src/concepts/opera_regeneration_2026-08-01/cards/opera_world_master_<career>.png` decodes at 2048×2048 and the runtime has four `world_<career>_c<column>r<row>.png` tiles. Dimensions alone are misleading.

`tools/build_opera_codex_art.py::native_master()` documents and implements the derivation:

- create a 2048×1152 blurred `ImageOps.fit` background from the smaller source;
- place the original source frame at its original pixel dimensions in the center, without enlarging it;
- feather only its outer edge;
- paste that active band into a 2048×2048 canvas at y=448;
- crop the result into four 1024×1024 runtime cards.

The source docstring says the accepted native subject-bearing frame is never enlarged. The master manifest records `active_crop=0,448,2048,1152` and “ImageGen native + non-subject edge continuation.” Thus these files are padded/continued delivery containers, not native 2048×2048 source paintings.

The later Detective/Nursery ownership builder uses a different `opera_master()` path: it fits/blurs each 1254-square edit to a 2048×1152 background and pastes the source over it, then pads to 2048 square and tiles. `audit/interactive_background_ownership_2026-08-29.json` calls this “established whole-canvas Opera 2048-square normalization.” It likewise adds no native source detail.

The legacy 1024×576 `assets/opera/worlds/backdrops/world_<career>.png` files are smaller logical/runtime views and cannot supply missing native detail. The 2048-square `opera_world_master_*` records in the older concept manifest carry historical `accepted` and `4.8` labels, but those labels predate or concern that delivery contract; they cannot override the current native-coverage rule or establish present art quality.

## Exact unresolved gaps and reuse path

- **Eleven 1672×941 careers:** Astronaut, Ballerina, Boxer, Candy Maker, Chef, Doctor, Farmer, Magician, Painter, Pop Star, and Racer have smaller source masters that should be compared at the fixed 1280×720 shipping scale against the 2K benchmark before any replacement decision. They remain the strongest composition/style authority and should be reused as references rather than redesigned for novelty.
- **Detective and Nursery:** each has a 1254-square ownership edit and derived delivery master. Review the corrected crown/bottle ownership at 1280×720 before deciding whether native-detail replacement is warranted; the edit source and prompt/hash record remain the continuity authority.
- **Geologist:** has a 1672×941 grotto candidate documented as reference-only. Review the fixed scene at shipping scale before opening a replacement brief.
- **Teacher:** has a live Library route whose native-detail status remains a benchmark/provenance gap, not an automatic replacement order. The existing `room_library.png` logical plate, the 1672×941 ownership source, and the eight `interactions_v4` tiles are valid continuity/provenance references and are live, but the current 3640×2048 master was built by whole-canvas Lanczos normalization of the 1672×941 ownership source. It supplies coverage geometry, not native authored detail.

Under the repository's reuse-first rule, do not commission or regenerate a room from this metadata alone. First capture and inspect each fixed 1280×720 route, then open a narrowly scoped replacement brief only for a demonstrated visible quality failure while preserving the approved composition, identity, and ownership corrections.

## Scope limits

- This inventory does not grade composition, style, contact, depth, occlusion, readability, or identity from metadata.
- It does not establish that a future 2048 image is acceptable; native dimensions are only one gate.
- It does not inspect stage masters, props, character atlases, cinematics, or multi-screen Castle rooms except where a record was necessary to trace an Opera derivative.
- It does not authorize generation or changes to protected originals. Any future candidate needs provenance, full pixel review, runtime integration review, Mobile/device performance, and the remaining master-audit gates.

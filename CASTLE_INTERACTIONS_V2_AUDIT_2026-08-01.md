# Pearl Castle object-first interaction audit v2 — 2026-08-01

## 2026-08-02 Mermaid Pool retirement addendum

The regenerated Mermaid Pool no longer loads its four v2 dry-fixture sheets.
Those sheets remain archived with their original provenance, but the active v2
manifest now covers 29 generated sheets and 34 instances across the other
seven rooms. Mermaid Pool uses four exact room-derived v1 atlases so the
rainbow waterfall remains continuously visible and the replacement seahorse
fountain, flower float, and star float match the regenerated room at rest.

## Outcome and review status

The v2 rollout replaces generic bounce, spin, squash, rotation, and detached
effect treatments with authored states of the fixtures themselves. It covers
33 unique generated object sheets and 38 physical fixture instances across all
eight destination rooms, an average of 4.75 interactions per room. Every room
has four to seven fixtures.

Each 4-by-2 sheet contains eight unique complete-object states. Runtime
sequences use eight, nine, or twelve steps, within the required 4–12 range. The
hardened timelines use symmetric return paths through authored states; they do
not interpolate, warp, or synthesize frames. Six Main Hall sconces share one
sheet but remain six independently stateful fixtures.

Codex visually reviewed the sheets for stable identity and topology, fixed
pivots, clean isolation, item-specific action, and absence of painted water or
generic overlays. This is not owner or other human approval. Provenance
correctly leaves explicit human review pending. Final normalization, the
fixed-canvas contact sheet, the manifest rebuild, and both castle static audits
now pass locally. Godot runtime probes, dev integration, Android packaging, and
release promotion remain CI-gated.

## Complete fixture inventory

Every item below has eight authored full-object states. “12” means a
12-step symmetric use/return path through those states.

| Room | Count | Full item list and authored mechanism | Timeline |
|---|---:|---|---:|
| Main Hall | 7 | Tapestry: real cloth rolls/unfurls from its fixed mount. Six shell sconces: attached shutters hinge around each pearl and each controls its own real light cluster. | Tapestry 12; sconces 8 forward/reverse |
| Opera Hall | 4 | Curtains gather at attached tiebacks; chandelier lamp cups open and crystals respond; six footlight covers hinge to expose bulbs; inlaid stage-star lights chase without spinning the prop. | Curtains 9; other fixtures 12 |
| Royal Kitchen | 7 | Sink control turns. Pan 1 flexes its hammered rim and center; pan 2 pitches in depth at its neck; pan 3 performs an oil-can center flex; pan 4 bows its spring-like handle while its bowl pitches. Oven door lowers to reveal an authored cavity, shelf, and cake tray. Fridge latch and attached door open to authored stocked shelves. | Sink/oven/fridge 9; pans 12 |
| Royal Library | 4 | Top book slides, opens, turns, closes, and returns; magic-book cover and paper leaf move; reading-table shell encloses/reopens around its pearl; lamp pearl depresses into its socket, rebounds, and lights. | 12 each |
| Stuffie Playroom | 4 | Real plush ears, paws, heads, and trunk wave; seven rings lift and reseat; three blocks topple and restack; tent flaps close over an authored interior and reopen. | Tent 9; other fixtures 12 |
| Craft Room | 4 | Pinned idea notes flex at their pins; paint-table brush stirs behind the jar rim; palette brush mixes inside paint wells with rim occlusion; ribbon roll turns while cloth unrolls and rewinds. | Ribbon rack 9; other fixtures 12 |
| Mermaid Pool | 4 | Waterfall control turns and its real gate retracts; fountain nozzle telescopes and unfolds; five flower petals fold to a bud and reopen; star float tips to reveal real side thickness. | Waterfall/fountain 9; floats 12 |
| Bubble Bath | 4 | Tub left tap rotates while the spout stays fixed; sink left handle turns; toilet rear lid stays upright while the separate seat ring flaps on its hinge; duck beak/body compress, dive, and pop up. | Tub/sink/toilet 9; duck 12 |

The refrigerator plays states 0 through 4 to open and hold before the recipe
menu is shown. Closing runs the authored reverse path 4, 3, 2, 1, 0 with its
dedicated close cue. A full-screen castle input blocker prevents fixture,
elevator, room, action, and exit input until the door reaches the closed rest
frame.

The four pans retain distinct art but
share one child-readable rack hotspot.

## Clean isolation and object-first contract

- Each delivered fixture is a complete object on transparent pixels. Prompts
  explicitly remove room fragments, floors, walls, counters, painted water,
  clipped debris, detached shadows, and effect marks.
- Runtime sheets are exact 4-by-2 grids, have eight occupied unique states, and
  are no larger than 1024 pixels on the longest edge.
- Normalization changes alpha only: a 5-by-5 interior matte and 1.35-times
  soft-edge alpha recovery prevent Roshan or room art showing through painted
  fixture interiors. It removed 107 sub-eight-pixel matte islands and 1,896
  low-alpha exact-chroma fringe pixels across all 264 states. Subject RGB is
  not repainted.
- Complete states may be translated to an audited fixed pivot. One uniform
  whole-sheet scale is allowed only to retain padding. Per-part warping,
  optical flow, interpolation, compositing, and frame synthesis are forbidden.
- The target is six pixels of cell padding; blocking thresholds are at least
  four pixels, no more than two pixels pivot spread, at least 0.80
  opaque/visible alpha, zero visible chroma, eight unique state hashes, and at
  least 5% visible-material change.
- V1 rest-cell bounds remain placement authority. Fridge, oven, and play tent
  are marked as authored hidden-surface interactions.
- The generated Sprite3D is the primary animation. Normal activation no longer
  creates a generic burst. Linear non-mipmapped atlas filtering and transparent
  borders prevent cross-cell alpha leakage.

These rules address the Roshan defect: fixture interiors remain opaque,
background pixels do not travel with interactive cards, the fridge has no
duplicate translucent glow card, and fluid never writes a broad foreground
depth silhouette.

## Measured water behavior

Jolt is used for rigid secondary solids, not fluid. Water uses a
Mobile-compatible spatial shader with the reef’s approved ripple-normal and
caustics textures, exact cached 96-by-96 polygon masks, and measured
object-local outlets.

| Fixture | Normalized geometry | Behavior |
|---|---|---|
| Kitchen sink | Outlet (0.6275, 0.3175); basin center (0.515, 0.600), radius (0.235, 0.060) | Stream grows from the faucet and terminates inside the basin. |
| Bath sink | Outlet (0.500, 0.145); basin center (0.500, 0.360), radius (0.220, 0.055) | Stream begins at the curved spout, not above the fixture. |
| Bathtub | Outlet (0.204, 0.155); fill center (0.515, 0.425), radius (0.325, 0.105) | Stream enters and fills only the tub cavity. |
| Toilet | Vortex center (0.500, 0.420), radius (0.180, 0.043) | One narrow vortex remains inside the bowl. |
| Flower/star/duck | Centers (0.340, 0.780), (0.500, 0.770), (0.500, 0.760) | Contact ripples render behind the objects. |
| Waterfall | Five outlet bands; splash center (0.535, 0.820), radius (0.275, 0.040) | Bands reveal from the opened gate; splash is delayed. |
| Fountain | x 0.625; y 0.160, 0.150, 0.130, 0.100, 0.075, 0.105, 0.140, 0.160 | Four bubbles follow all eight authored nozzle positions. |

Water is rendered by bounded Sprite3D nodes. Depth testing remains enabled so
the fixture can occlude its own water, while depth_draw_never and no
transparent depth prepass prevent fluid from erasing Roshan. Mask textures are
cached by geometry, avoiding repeated ImageTexture allocation when identical
layers are rebuilt. Water is tagged logic_authority=false.

## Capped Jolt secondary motion

Eight fixture types receive optional follow-through: hinge mode for the Opera
chandelier and four pans, and buoyant mode for the flower float, star float,
and duck. The authored sheet remains the primary action.

Bodies use collision layer/mask zero, lock depth, and have no gameplay
authority. Allocation is capped at 12 and awake bodies at eight. Activation
impulses and per-tick restoring forces are peak-bounded; sleeping bodies return
to their audited rest transform and freeze. Objectives, menus, touch
completion, and rewards never depend on body settling.

## Performance, export, audio, and provenance

- The static gate limits one live room’s interaction sheets to 24 MiB
  uncompressed RGBA. Textures are capped at 1024, masks at 96, water is
  unshaded, and Jolt allocation/awake/impulse peaks are bounded for the Lenovo
  Tab M11.
- The Mobile renderer path adds no OmniLights, broad water meshes, screen
  reads, depth prepass, or manual sRGB conversion.
- Android and desktop export presets explicitly package
  assets/flats/castle/interactions_v2/castle_interactions_v2.json.
- Audio paths and semantic cues are manifest-authoritative. The loader accepts
  res paths, assets/audio paths, and castle-relative paths without
  double-prefixing.
- fridge_open.ogg is a deterministic 720 ms cue with latch, door-open, and
  chime events. fridge_close.ogg is 520 ms with door-close and latch events.
  Castle interaction audio remains project-owned 24 kHz mono Ogg Vorbis.
- Every asset records its exact prompt/hash, generation method and attempt,
  native path/hash/dimensions, immutable chroma master, pre-normalization hash,
  alpha QA, rejected topology attempts where applicable, and Codex review.
- Runtime/source/shader/audio/provenance/review artifacts are registered in
  ASSET_LICENSES.md. No protected book, voice, or friend-character source was
  modified.

## Gate status at draft time

| Gate | Status |
|---|---|
| File roster | 33 unique sheets / 38 physical instances present |
| Codex visual review | Accepted; no human approval claimed |
| Final transactional normalization | Passed 33; min opacity ratio 0.8306, min material change 0.0783, visible exact chroma 0, max near-chroma ratio 0.0016, max pivot spread 1.5 px |
| Final normalization report/contact/manifest/static v2 audit | Passed: 33/38, 4.75 per room, nine water interactions, eight Jolt fixtures, 16.00 MiB max live-room RGBA |
| V1 interaction audit and 51-card alpha audit | Passed locally; zero invisible-depth failures |
| Parser and inference lint | Passed locally for every changed GDScript |
| Godot analyzer/probes and feature CI/Android | Pending pushed CI |
| Dev integration and protected promote workflow | Pending green gates |

## Full change list

1. Added 33 runtime sheets under assets/flats/castle/interactions_v2/ and
   matching chroma masters plus provenance under
   assets_src/imagegen/castle_object_animations_v2/.
2. Added tools/normalize_castle_interaction_v2_sheets.py,
   tools/build_castle_interaction_v2_manifest.py, and
   tools/audit_castle_interactions_v2.py for normalization, manifest/contact
   generation, and blocking validation.
3. Added scripts/arena/castle_fixture_rigs.gd and
   assets/shaders/castle_fixture_water.gdshader for cached exact-mask water,
   moving outlets, bounded Jolt garnish, and safe restoration.
4. Updated scripts/arena/castle_rooms_25d.gd for full-object playback,
   symmetric return timelines, manifest-authoritative audio, busy guards,
   independent sconces, grouped pans, gated fridge ordering, and a real
   castle-local close input blocker.
5. Updated scripts/main.gd with fixture state and physics-tick handoff.
6. Added fridge_open.ogg and fridge_close.ogg; updated the deterministic audio
   generator and castle SFX manifest.
7. Expanded scripts/probe_castle_pearl_art.gd for timeline, transform, water,
   Jolt-cap/peak/settling, audio, pan-group, light, and fridge-lifecycle checks;
   wired the v2 static audit into scripts/ci.sh.
8. Updated export_presets.cfg to package the v2 JSON in Android and desktop.
9. Updated ASSET_LICENSES.md and the 2026-08-01 runtime-correction shader hash
   in FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json while preserving historical
   evidence.
10. Added the fixed-canvas final contact board at
    audit/castle_interactions_v2/castle_interaction_frames_v2.png (SHA-256
    4ace63822e2d625312f8674196f67f909679e4cac3a8a6cd45a186f48ba5df70),
    plus this audit report.

# Codex Improvement Prototype Batch - 2026-07-18

Status: E1 review-only image prototypes integrated into `dev` for the Fable 5
co-constructor. Do not promote this batch to `master`, wire it into Godot, or
treat it as runtime art without the review and runtime gates below.

## Why this batch exists

The owner corrected the earlier workflow: make image-generation prototypes
before any Blender construction, repeat the art work under all project audit
instructions, and leave the result for the Fable 5 co-constructor. This batch
therefore contains raster design sheets only. It creates no GLB, `.blend`,
runtime replacement, scene edit, or master merge.

The prototype scope follows Queue 1 of the latest object-generation audit:

1. a bare coral direction without a shared pedestal;
2. a volumetric kelp direction rather than planar cards;
3. a locomotive identity plus a minimal straight/curve/station kit.

## Authority chain used

- `AGENTS.md`
- `assets/ART_GENERATION_CONTRACT.md`
- `CODEX_IMPROVEMENT_AUDIT_2026-07-18.md`
- `assets/OBJECT_GENERATION_AUDIT_LOG.md` v6 as inspected at commit
  `affb617d2323ef9ddb3d22c12d678efb9e02a35c`
- `ART_STYLE_GUIDE.md`
- `ART_GAP_WORKORDER_2026-07-18.md`
- `OBJECT_PLACEMENT_AUDIT_2026-07-17.md`
- `ART_SCORE3_REBUILD_AUDIT.md`
- `ART_RESIDUAL_LOW_SCORE_AUDIT.md`

The object log is not copied from the other branch into this worktree. Its v6
rules and its v4 packet schema are cited here so the source history stays
append-only.

## Evidence and promotion boundary

- Current evidence class: E1, design proposal / derivative synthesis.
- Maximum possible score from these sheets alone: 2/5.
- `runtime_pass`: not attempted and not claimable.
- Mobile renderer capture: not attempted.
- Interface dimensions, topology, overdraw, collision, and placement density:
  not proven by a raster turnaround.
- The raw 1254 px images are provenance files only. The 1024 px copies are the
  review set that obeys the repository texture-size rule.
- Gate 0 still blocks bulk generation and promotion. The owner's direction
  authorizes this review-only prototype pass, not runtime promotion.

## Selected review set

| Role | Review image | SHA-256 | Audit verdict |
|---|---|---|---|
| Bare branching coral | `generated/r003_coral_branch_bare/turnaround_v1_1024.png` | `2EE0D62498D54063B36988E5293F7E1918030924213CECB558104E6E136A621E` | Candidate reference. Bare growth and asymmetry read clearly; seabed embedding still requires proof. |
| Volumetric tall kelp | `generated/r004_volumetric_kelp_tall_canopy_a/turnaround_v2_1024.png` | `2044990D6D7E710C660A6A7D3B178FD0CB2E2A80D4083B06DDA10437046F9ED3` | Candidate with caution. Volumetric ribbons and direct-burial stem ends read; stem count and topology still need a constructor decision. |
| Locomotive identity | `generated/r021_locomotive_identity/turnaround_v1_repair_1024.png` | `632A3A4B07A65EACE3D6A4AF558E9F236357E7AC1E4B3B566460BBD867C1311D` | Candidate reference. Stack, cowcatcher, rail wheels, rods, cab, and coupling read; mechanical interfaces are unmeasured. |
| Straight track | `generated/r021_track_straight/turnaround_v1_1024.png` | `EE8AD99E5BD5D8CDF4F38A10FEA4611CDF0045B59741243156EB342A4B83ADC9` | Candidate kit piece. Gauge and end connector dimensions are illustrative only. |
| Quarter-curve track | `generated/r021_track_quarter_curve/turnaround_v1_1024.png` | `377A6DDDC07C441C0465C7DA34DE75D63BEAF16177568616020451152B6D27A5` | Candidate kit piece. Curve radius and straight-piece continuity are illustrative only. |
| Low station platform | `generated/r021_station_platform_low/turnaround_v1_1024.png` | `42693245C2D90B8AA23F9FFC22D99BA8413FE853EEA9796EB5E221E33801910F` | Candidate kit piece. Clear low boarding silhouette; train clearance is unproven. |
| Open station shelter | `generated/r021_station_shelter_open/turnaround_v1_1024.png` | `4DCCD64648F6E581B80E259DAFB773F04C8E95C52D08E34113824DBAD3943619` | Candidate kit piece. Open sightline reads; platform attachment is unproven. |

## Retained provenance and rejected directions

| File | Status | Reason |
|---|---|---|
| `generated/r003_coral_branch_bare/turnaround_v1.png` | Raw source for selected coral | 1254 px; keep for provenance, do not import. |
| `generated/r004_volumetric_kelp_tall_canopy_a/turnaround_v1.png` | Rejected direction | View-to-view stem topology and silhouette drift. |
| `generated/r004_volumetric_kelp_tall_canopy_a/turnaround_v1_repair_raw.png` | Superseded repair source | Removed labels but retained a bulbous base that conflicts with direct seabed insertion. |
| `generated/r004_volumetric_kelp_tall_canopy_a/turnaround_v1_repair_1024.png` | Superseded repair review | Same bulbous-base issue; retained so the v2 edit remains traceable. |
| `generated/r004_volumetric_kelp_tall_canopy_a/turnaround_v2_raw.png` | Raw source for selected kelp | 1254 px; direct-burial stem repair; keep for provenance, do not import. |
| `generated/r021_locomotive_identity/turnaround_v1.png` | Rejected direction | Too polished and detail-heavy; black silhouette inset was not clean enough. |
| `generated/r021_locomotive_identity/turnaround_v1_repair_raw.png` | Raw source for selected locomotive | 1254 px; keep for provenance, do not import. |
| `generated/r021_track_straight/turnaround_v1_raw.png` | Raw source for selected straight track | 1254 px; keep for provenance, do not import. |
| `generated/r021_track_quarter_curve/turnaround_v1_raw.png` | Raw source for selected curve | 1254 px; keep for provenance, do not import. |
| `generated/r021_station_platform_low/turnaround_v1_raw.png` | Raw source for selected platform | 1254 px; keep for provenance, do not import. |
| `generated/r021_station_shelter_open/turnaround_v1_raw.png` | Raw source for selected shelter | 1254 px; keep for provenance, do not import. |

One intermediate kelp edit added text labels. It was rejected before copying
into the project because text was explicitly forbidden.

## Output record and measurements

- Generator: OpenAI built-in image generation/editing tool. The tool did not
  expose a model build identifier or deterministic seed, so neither is claimed.
- Source/edit history: every copied `*_raw.png` or original `turnaround_v1.png`
  is the retained raster source. There is no layered editable source.
- Normalization: PowerShell `System.Drawing` resized review copies to 1024 px;
  the kelp v2 normalization explicitly used high-quality bicubic resampling.
- Isolated reviewer: Codex visual review, 2026-07-18. Review decisions are in
  the selected and rejected tables above.
- Placement status: `reference_only`; no runtime path has been replaced.
- Negative-control pipeline: not run. Gate 0 remains open.
- Runtime capture paths: none.
- Current evidence and score: E1; no score above 2/5 is supportable.

| File | Dimensions | SHA-256 |
|---|---:|---|
| `generated/r003_coral_branch_bare/turnaround_v1.png` | 1254x1254 | `96F07CBCC340A7B344A42F3BBCF1B9D0BDFBC81558100E92607BD7FCC4FD57CB` |
| `generated/r003_coral_branch_bare/turnaround_v1_1024.png` | 1024x1024 | `2EE0D62498D54063B36988E5293F7E1918030924213CECB558104E6E136A621E` |
| `generated/r004_volumetric_kelp_tall_canopy_a/turnaround_v1.png` | 1254x1254 | `37F48EDA647CFB5232D06C68805CB27B364320862B4339346D46572715AE0649` |
| `generated/r004_volumetric_kelp_tall_canopy_a/turnaround_v1_repair_raw.png` | 1254x1254 | `6A08B07A545189451E73833F24F099E9F36761C032F403A20F6C105B237FAEE5` |
| `generated/r004_volumetric_kelp_tall_canopy_a/turnaround_v1_repair_1024.png` | 1024x1024 | `BBB0868DA29F7ED1E552DB403C7573D3F4B47D619972B5ECCC52D6F2426CBEAD` |
| `generated/r004_volumetric_kelp_tall_canopy_a/turnaround_v2_raw.png` | 1254x1254 | `42B6E46A24C69C77A0BC52CF25C01E1036C71B963ED021B0D2B9DE271405E61B` |
| `generated/r004_volumetric_kelp_tall_canopy_a/turnaround_v2_1024.png` | 1024x1024 | `2044990D6D7E710C660A6A7D3B178FD0CB2E2A80D4083B06DDA10437046F9ED3` |
| `generated/r021_locomotive_identity/turnaround_v1.png` | 1254x1254 | `6140133A56F39B1ACBEF1E770B88F8E5F3CD75E6D231F31ADF8167DE84248DE6` |
| `generated/r021_locomotive_identity/turnaround_v1_repair_raw.png` | 1254x1254 | `722A2E6D49921630BF0BF93306EE2C1F26A5BEEAF466F2699B16B2E1613E4255` |
| `generated/r021_locomotive_identity/turnaround_v1_repair_1024.png` | 1024x1024 | `632A3A4B07A65EACE3D6A4AF558E9F236357E7AC1E4B3B566460BBD867C1311D` |
| `generated/r021_track_straight/turnaround_v1_raw.png` | 1254x1254 | `567105C8280123C26D3E38518291781DB5FAE237723C46BE6A8DDA475F416493` |
| `generated/r021_track_straight/turnaround_v1_1024.png` | 1024x1024 | `EE8AD99E5BD5D8CDF4F38A10FEA4611CDF0045B59741243156EB342A4B83ADC9` |
| `generated/r021_track_quarter_curve/turnaround_v1_raw.png` | 1254x1254 | `20F2CDD3145A9AAB10789E85D0D1838CFBF7E864EF0703856D127EF061492252` |
| `generated/r021_track_quarter_curve/turnaround_v1_1024.png` | 1024x1024 | `377A6DDDC07C441C0465C7DA34DE75D63BEAF16177568616020451152B6D27A5` |
| `generated/r021_station_platform_low/turnaround_v1_raw.png` | 1254x1254 | `C981AA19139F24D09A609CAF1AC735CDE18E446751235128278D0D565B92C3DA` |
| `generated/r021_station_platform_low/turnaround_v1_1024.png` | 1024x1024 | `42693245C2D90B8AA23F9FFC22D99BA8413FE853EEA9796EB5E221E33801910F` |
| `generated/r021_station_shelter_open/turnaround_v1_raw.png` | 1254x1254 | `4C4ECD7C8BD3856F05A8FF35542CF4E3F25FD49775CE4C93C9A493F5A185F0DC` |
| `generated/r021_station_shelter_open/turnaround_v1_1024.png` | 1024x1024 | `4DCCD64648F6E581B80E259DAFB773F04C8E95C52D08E34113824DBAD3943619` |

## Image-generation prompt contract

Every sheet asks for multiple consistent views of one named object on neutral
white, plus a pure black silhouette inset. No view labels or prose may appear
inside the image. The named object's construction, anatomy, functional parts,
and complete silhouette come before the pastel storybook finish.

Default exclusions used for all roles: no scene, habitat, pedestal, base rock,
face, eyes, mouth, character, wings, flowers, unrelated coral, bubbles, gems,
stars, swirls, confetti, sticker border, text, watermark, or baked dramatic
lighting. No Zelda assets, symbols, UI, vehicle designs, or other copied IP.

Art finish used for review: rounded toy-playset geometry, low-complexity
cel-shaded material grouping, navy/purple structural accents, aqua/lavender
shadow bias, oversized child-readable landmarks, and Mobile-friendly detail
density. These are design cues, not proof of a final material implementation.

## Required generation packets

The shared fields below and each role record together form the complete packet
required by the object-generation audit.

### Shared packet fields

- `audit_log_version`: `2026-07-18-v6`; required packet schema introduced in v4.
- `camera_and_distance`: four-view orthographic-style concept sheet plus black
  silhouette; final runtime review must use the actual child-height gameplay
  camera and representative near/mid/far distances.
- `source_motif_references`: shipped Mermaid Roshan book-derived world palette,
  `ART_STYLE_GUIDE.md`, active authored family comparators, rounded toy railway
  construction, and real coral/kelp anatomy. Wind Waker is rendering mood only.
- `material_list`: two to five broad matte material families per object; opaque
  unless a later measured role explicitly requires transparency.
- `palette_limits`: cool pastel world palette; high contrast reserved for
  silhouette landmarks and interaction edges; no candy striping or noisy
  rainbow distribution.
- `forbidden_motifs`: the default exclusion clause above, plus bases/pedestals
  on coral and kelp, planar leaf cards on kelp, and copied franchise motifs on
  railway objects.
- `repetition_test`: repeat at intended density from all field edges; fail on
  visible clones, shared rotation, tangencies, excessive silhouette noise, or
  transparent-overdraw buildup.
- `mobile_capture_plan`: Speedy tier, Mobile renderer, 1280x720, child-height
  player views, near/mid/far and oblique views; dense coral/kelp field stress;
  full train lap, station approach, boarding, occupied ride, and castle return.
- `license_and_provenance`: project-generated with OpenAI built-in image
  generation on 2026-07-18; no external source image; raw and normalized files
  retained; review-only and not APK-export-ready.
- `owner_decisions_affecting_role`: use image generation for prototypes before
  Blender; leave for Fable 5 co-constructor; do not merge to the main project;
  protect book art, family voices, and friend characters.
- `applicable_rule_ids`: R-ROLE1 through R-ROLE4, R-FUNC1 through R-FUNC4,
  R-MOT1 through R-MOT3, R-GEO1 through R-GEO4, R-MAT1 through R-MAT3,
  R-QA1 through R-QA8, Gate 0, Queue 1, and the repository Mobile/texture rules.

### R003 - bare branching coral

- `asset_id`: `r003_coral_branch_bare`
- `role_name`: bare branching reef coral reference
- `role_type`: prop
- `runtime_target`: planned future coral-family GLB under `assets/`; exact slot
  must be assigned after comparing the active `assets/props/gen2/coral*.glb`.
- `referencing_script_or_scene`: active reef/galaxy coral scatter paths,
  including `scripts/galaxy.gd`; verify all consumers before promotion.
- `gameplay_verb`: passive habitat landmark that reads as coral without a base.
- `states_and_separate_parts`: one static growth form; no baked seabed or FX.
- `world_scale_and_reference_dimensions`: oversized readable branches; buried
  foot sized for seabed insertion; final dimensions measured against Roshan.
- `placement_count_and_density`: mass placement; prototype one of three
  genuinely different growth-form references.
- `support_surface_or_attachment`: directly embedded into seabed terrain.
- `identity_and_anatomy_anchors`: fused trunk, irregular antler branching,
  tapered branch tips, plausible load-bearing forks, no rock-like pedestal.
- `silhouette_landmarks`: asymmetric crown, one high fork, one low lateral arm,
  clear negative spaces between branches.
- `family_variation_axes`: antler, plate/fan, and compact bush growth; height,
  fork rhythm, lean, crown width, and tip density.
- `active_asset_comparison`: existing coral family and the audited blue-grey
  pedestal failure; the new reference must remain recognizably bare.

### R004 - volumetric tall kelp

- `asset_id`: `r004_volumetric_kelp_tall_canopy_a`
- `role_name`: volumetric tall-canopy kelp reference
- `role_type`: prop
- `runtime_target`: future comparison/replacement candidate for
  `assets/art35/reef/kelp_0.glb`; not assigned for runtime here.
- `referencing_script_or_scene`: reef meadow and district foliage scatter in
  `scripts/main.gd` and the reef district builder; verify exact consumers.
- `gameplay_verb`: passive tall vegetation that frames swimming lanes without
  becoming an opaque wall.
- `states_and_separate_parts`: static clump reference; individual stems and
  blades remain constructible parts for later cheap sway.
- `world_scale_and_reference_dimensions`: tall enough to frame Roshan with an
  open lower third; final stalk/blade thickness measured in runtime.
- `placement_count_and_density`: sparse and dense field tests are mandatory.
- `support_surface_or_attachment`: narrow buried holdfast; no visible rock base.
- `identity_and_anatomy_anchors`: several round/tapered stems, thick ribbon
  blades with volume, alternating blade heights, coherent stem continuity.
- `silhouette_landmarks`: narrow root, open midsection, broad irregular canopy,
  two dominant outer sweeps, visible negative gaps.
- `family_variation_axes`: sparse/dense stem count, canopy width, lean, blade
  curl, height tiers, and open-space rhythm.
- `active_asset_comparison`: `kelp_0.glb`, `kelp_1.glb`, and the audited planar
  fan/card failure.

### R021A - locomotive identity

- `asset_id`: `r021_locomotive_identity`
- `role_name`: Sky Lagoon child-readable locomotive reference
- `role_type`: interactive
- `runtime_target`: planned future visual replacement inside
  `scripts/arena/courtyard_train.gd::_build_engine()`; retain ride logic.
- `referencing_script_or_scene`: `scripts/arena/courtyard_train.gd`,
  `scripts/arena/sky_lagoon.gd`, and `scripts/probe_train.gd`.
- `gameplay_verb`: carries Roshan around the castle and stops at the station.
- `states_and_separate_parts`: body, cab, boiler, stack, cowcatcher, rail-wheel
  sets, side rods, front/rear couplers, seat/boarding anchors; moving and parked
  states remain code-driven.
- `world_scale_and_reference_dimensions`: match current wheelbase, clearance,
  seat, collider, and ring constraints; raster proportions are not measurements.
- `placement_count_and_density`: one engine in a multi-car moving assembly.
- `support_surface_or_attachment`: wheels aligned to common rail gauge; coupler
  axis compatible with cars.
- `identity_and_anatomy_anchors`: unmistakable steam stack, boiler, enclosed
  cab, cowcatcher, rail wheels, rods, and functional couplings.
- `silhouette_landmarks`: tall stack, rounded boiler nose, peaked cab roof,
  forward triangular cowcatcher, large driver-wheel rhythm.
- `family_variation_axes`: stack height, roof curve, boiler length, cowcatcher
  width, wheel rhythm, and restrained accent placement.
- `active_asset_comparison`: current scripted primitive engine and current
  train clearances/ride anchors.

### R021B - straight track

- `asset_id`: `r021_track_straight`
- `role_name`: compatible straight rail segment
- `role_type`: kit_piece
- `runtime_target`: future authored visual segment for
  `scripts/arena/courtyard_train.gd::_build_track()`.
- `referencing_script_or_scene`: `scripts/arena/courtyard_train.gd` and
  `scripts/probe_train.gd`.
- `gameplay_verb`: visually supports and guides the moving train.
- `states_and_separate_parts`: two rails, four simplified ties, and matched end
  connectors; no ballast or terrain baked into the piece.
- `world_scale_and_reference_dimensions`: gauge, tie spacing, height, and end
  plane must be derived from the active train path before modeling.
- `placement_count_and_density`: repeated around a very large ring.
- `support_surface_or_attachment`: terrain/causeway support; flush end planes.
- `identity_and_anatomy_anchors`: parallel rails, perpendicular ties, readable
  rail head, consistent connector logic.
- `silhouette_landmarks`: long narrow paired lines and regular cross ties.
- `family_variation_axes`: restrained tie wear/tint only after a perfect modular
  reference; gauge and endpoints never vary.
- `active_asset_comparison`: current procedural rails/ties and ring path.

### R021C - quarter-curve track

- `asset_id`: `r021_track_quarter_curve`
- `role_name`: compatible quarter-curve rail segment
- `role_type`: kit_piece
- `runtime_target`: future authored curve visual for
  `scripts/arena/courtyard_train.gd::_build_track()`.
- `referencing_script_or_scene`: `scripts/arena/courtyard_train.gd` and
  `scripts/probe_train.gd`.
- `gameplay_verb`: continues the train path through a readable smooth turn.
- `states_and_separate_parts`: paired curved rails, simplified radial ties, and
  the same end connectors as the straight segment.
- `world_scale_and_reference_dimensions`: shared gauge and rail section; curve
  radius derived from the active ring, not from this raster.
- `placement_count_and_density`: repeated around the ring and transitions.
- `support_surface_or_attachment`: terrain/causeway support; tangent end planes.
- `identity_and_anatomy_anchors`: concentric rails, radial ties, matching gauge,
  tangent endpoints, no kink at joins.
- `silhouette_landmarks`: clean quarter arc with even paired-rail spacing.
- `family_variation_axes`: left/right mirror only until interfaces pass.
- `active_asset_comparison`: straight prototype, current ring curvature, and
  current procedural rail placement.

### R021D - low station platform

- `asset_id`: `r021_station_platform_low`
- `role_name`: low open boarding platform
- `role_type`: kit_piece
- `runtime_target`: future station visual for
  `scripts/arena/courtyard_train.gd::_build_station()`.
- `referencing_script_or_scene`: `scripts/arena/courtyard_train.gd`,
  `scripts/arena/sky_lagoon.gd`, and `scripts/probe_train.gd`.
- `gameplay_verb`: marks the train stop and gives a clear one-finger boarding
  location without blocking sightlines.
- `states_and_separate_parts`: platform deck and low edge/support structure;
  shelter remains a separate kit piece.
- `world_scale_and_reference_dimensions`: match car floor/step height, Roshan
  clearance, station bearing, and current stop envelope.
- `placement_count_and_density`: one station platform at the dwell point.
- `support_surface_or_attachment`: sits on the meadow beside the track; rail-side
  edge must clear the full moving train envelope.
- `identity_and_anatomy_anchors`: long low deck, obvious rail-side edge, broad
  open boarding surface, rounded child-safe corners.
- `silhouette_landmarks`: low horizontal slab with a shallow raised rim.
- `family_variation_axes`: length modules and mirrored entry side only after the
  reference clearance passes.
- `active_asset_comparison`: current procedural station and boarding anchors.

### R021E - open station shelter

- `asset_id`: `r021_station_shelter_open`
- `role_name`: open-sided station shelter
- `role_type`: kit_piece
- `runtime_target`: future separate station shelter visual for
  `scripts/arena/courtyard_train.gd::_build_station()`.
- `referencing_script_or_scene`: `scripts/arena/courtyard_train.gd` and player
  views from `scripts/arena/sky_lagoon.gd`.
- `gameplay_verb`: identifies the station while keeping the train and boarding
  location visible.
- `states_and_separate_parts`: roof, four posts, and optional rear low rail;
  platform is separate.
- `world_scale_and_reference_dimensions`: roof clearance above Roshan and the
  platform; posts outside the boarding/moving envelopes.
- `placement_count_and_density`: one shelter at the station.
- `support_surface_or_attachment`: keyed to platform attachment points, with no
  baked platform or track.
- `identity_and_anatomy_anchors`: simple weather roof, thin readable posts,
  completely open approach and train-facing side.
- `silhouette_landmarks`: broad shallow roof over four widely spaced supports.
- `family_variation_axes`: roof curve and mirrored open side only after the
  attachment interface passes.
- `active_asset_comparison`: current station roof/posts and the platform
  prototype above.

## Fable 5 co-constructor review gate

Review the seven 1024 px sheets first. Accept, amend, or reject one difficult
reference member per family before constructing geometry. For the railway kit,
define one measured interface sheet for gauge, rail section, endpoints, wheel
spacing, coupler axis, platform clearance, and shelter attachment before any
modeling.

If these references are accepted, the next image-only expansion may target a
40-sheet matrix, still without runtime claims:

- coral: three growth roles x four structural variants = 12;
- kelp/seagrass: two roles x four sparse/dense structural variants = 8;
- railway: five roles x four controlled variants = 20.

That matrix is a Codex continuation plan, not proof that forty assets are
currently required or approved. Queue 1 and R-MOT2 require reference acceptance
before the family expands. Only a later, separate constructor workstream may
translate approved sheets into geometry, run measured export checks, place the
assets in Godot, capture representative Mobile views, and request owner review.

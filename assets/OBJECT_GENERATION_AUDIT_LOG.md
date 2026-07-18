# Object Generation Audit Log

Last consolidated: 2026-07-18

Audience: any agent creating, regenerating, reviewing, or promoting world
objects, textures, sprites, environment kits, and interactive props.

This is the durable memory for the next generation pass. Read it after
`assets/ART_GENERATION_CONTRACT.md` and before writing prompts or Blender
generators. The contract defines mandatory policy. This log records why the
policy exists, evaluates new audits, and translates accepted findings into
generation rules.

Do not treat this log as permission to start another large batch. The current
full-texture-regeneration QA has unresolved P0 integrity defects. Close the P0
items in `CODEX_IMPROVEMENT_AUDIT_2026-07-18.md` before bulk generation.

## Evidence classes

Art scores and evidence classes are different things. A technically valid file
can have strong evidence about its validity and still be poor art.

| Class | Meaning | May establish |
|---|---|---|
| E0 | Claim without inspectable evidence | Question only |
| E1 | Design proposal, work order, or derivative synthesis | Candidate requirement |
| E2 | Independent source, file, render, or code inspection | Structural/static finding |
| E3 | Representative Mobile-renderer gameplay evidence | Runtime finding; 4/5 eligibility |
| E4 | Owner review of shipped runtime views | 5/5 eligibility |

When sources disagree, prefer the source with the more relevant evidence, not
the newest date. Runtime evidence outranks isolated renders for runtime quality.
Owner identity calls outrank generated similarity scores. A derivative work
order does not become independent evidence by repeating an earlier audit.

## Audit source register

### A01 - Claude GEN-2 image audit

- Source: `gen2/audit/claude_0.json` through `claude_9.json`,
  `gen2/generated/ANALYSIS.md`, `gen2/curation.json`, and
  `gen2/audit/round2.json`.
- Scope: 123 roles and 492 generated 2D variants.
- Evidence: E2 for isolated image defects; no runtime proof.
- Accepted: the flaw taxonomy is useful and the 635 recorded flaw incidents
  expose repeatable generator behavior.
- Limitation: KEEP means best available or salvageable, not 5/5. Eighteen of
  83 selected KEEP variants retained a recorded flaw or had usability below
  8/10.
- Carried forward: R-ID1 through R-ID4, R-REP1, R-QA1.

Most frequent failures:

| Failure | Count | Generation implication |
|---|---:|---|
| Face added to ordinary scenery | 133 | Ban invented faces unless the role is explicitly a character |
| Subject combined with another concept | 119 | One named subject per output |
| Cluster or miniature scene instead of object | 104 | No habitat, base vignette, or object bundle unless requested |
| Confetti/decal filler | 91 | Decoration must be specified, sparse, and functional |
| Category context hijacks subject | 91 | Put identity constraints before mood/style context |
| Baked bubbles/gems/droplets | 34 | Effects remain separate runtime layers |
| Palette bleed | 24 | Preserve local material identity, not only set palette |
| Visible texture repetition | 22 | Test tiled fields, not only edges |

### A02 - Human runtime and game-wide art audits

- Sources: `ART_HUMAN_REVIEW_AUDIT_2026-07-16.md`,
  `ART_GAME_WIDE_PASS35_AUDIT_2026-07-16.md`, `ART_AUDIT_2026-07-18.md`,
  and their runtime captures.
- Scope: active game roles in representative scenes.
- Evidence: E3 where Mobile captures exist; E2 where findings are inventory
  or routing checks only.
- Accepted: file replacement and routing are not visual completion. The jump
  from no reported low roles to 71 of 88 roles at 0-2 was an audit-method
  correction, not a one-day art regression.
- Carried forward: R-GOV1 through R-GOV4, R-QA2 through R-QA5.

### A03 - Ecosystem placement audit

- Source: `OBJECT_PLACEMENT_AUDIT_2026-07-17.md` and related placement
  ledgers/probes.
- Scope: habitat, support, density, reserved gameplay space, and continuity.
- Evidence: E2-E3 depending on area capture coverage.
- Accepted: object quality includes believable support and placement. A good
  isolated model can fail when it floats, grids, blocks a route, or carries a
  repeated pedestal that should come from terrain.
- Carried forward: R-GEO3, R-REP1 through R-REP3, R-FUNC3.

### A04 - Non-5 maximum-potential critique

- Source: `ART_NON5_MAX_POTENTIAL_CRITIQUE_2026-07-18.md`, commit `fa0f15d`
  on this branch (original commit `a755710`).
- Scope: cross-audit synthesis, Claude flaw totals, candidate-pack galleries,
  scoring contradictions, and recurring art-direction ceilings.
- Evidence: E2 synthesis. It does not replace runtime review.
- Accepted: the central failure is premature convergence on valid, attractive
  isolated candidates before motif truth, runtime composition, and owner
  acceptance are proved.
- Carried forward: all governance, motif, family, composition, and score rules
  below.

### A05 - Full texture regeneration implementation review

- Source: `FULL_TEXTURE_REGEN_IMPLEMENTATION_REVIEW_2026-07-18.md`, commit
  `4847ddb`.
- Scope: all 167 candidate files, galleries, hashes, manifests, and QA tools.
- Evidence: strong E2. The reviewer independently parsed files and inspected
  the review implementation, but candidates remain unwired.
- Accepted findings:
  - The finalize tool stamped every candidate as pass/4 without measurement.
  - A path-key mismatch discarded render results from the ledger.
  - Triangle, bound, and anatomy checks trusted generator-authored metadata.
  - R088 is a phantom role with no files.
  - Candidate entries lack runtime destinations.
  - Small props and 2D painted textures are the strongest pack areas.
  - World-scale roles represented by single miniatures are not deployable
    solutions.
- Accepted art calls: Northern candidates are regressions/reference-only;
  coral pedestals will repeat; kelp remains planar cards; the train reads as
  buses; meadow ground is too warm/dense; kitchen needs room-wide palette
  reconciliation.
- Carried forward: R-GOV1 through R-GOV4, R-ROLE1 through R-ROLE4,
  R-GEO1 through R-GEO4, R-QA1 through R-QA6.

### A06 - Codex improvement audit, iteration 2

- Source: `CODEX_IMPROVEMENT_AUDIT_2026-07-18.md`, commit `d001be4`.
- Scope: prioritized response to A04 and A05.
- Evidence: E1 derivative directive. Its acceptance tests are useful, but its
  repeated claims do not add independent confidence.
- Accepted: P0 QA repair blocks new bulk generation. Then promotion mapping,
  targeted rework, and missing-kit coverage proceed in that order.
- Carried forward: current queue and acceptance gates in this log.

### A07 - Art generation contract revision

- Source: `assets/ART_GENERATION_CONTRACT.md`, revised in commit `d001be4`.
- Scope: authoritative generation and promotion policy.
- Evidence: policy, not an audit.
- Accepted: generated candidates without runtime captures cap at 2/5; focal
  engine primitives cap at 1/5; every asset requires placement, source,
  license, QA, and Mobile evidence; Northern is complete and must not be
  regenerated.
- Carried forward: the contract always wins if this log drifts from it.

### A08 - Jolt physics and overworld feel audit

- Source: `JOLT_PHYSICS_AUDIT_2026-07-18.md`, commit `ccf934c`.
- Scope: physics usage, swim feel, camera behavior, and cheap animation wins.
- Evidence: E2 for current code behavior; E1 for proposed changes.
- Object-generation relevance: dynamic objects must be authored around their
  gameplay verb and motion envelope. Separate rest, active, hit, collected,
  and completed states where geometry changes. Do not bake wake, impact,
  sparkle, or bubble effects into the object texture.
- Not carried forward: physics-engine recommendations are outside object art.
- Carried forward: R-FUNC1 through R-FUNC4.

### A09 - Claude Fable dungeon difficulty audit

- Source: `DUNGEON_DIFFICULTY_AUDIT_2026-07-18.md`, commit `4b087a6`
  (original `ec84b24`, co-authored by Claude Fable 5).
- Scope: all ten dungeon rooms, age-four cognitive fit, sequencing, feedback,
  item moments, and lock/key grammar.
- Evidence: E2 for verified current behavior; E1 for redesign proposals.
- Accepted object-generation findings:
  - Clues must remain legible from the fixed gameplay camera.
  - Size-order objects need exaggerated adjacent differences.
  - Correct/complete state must remain visibly marked after interaction.
  - Elemental objects need shape and state differences, not color alone.
  - Collectible powers and keys need iconic silhouettes and a clear receiving
    lock or target.
  - Numerals and text cannot be the only state carrier.
- Qualification: its Zelda comparison is interaction grammar only. Do not use
  Zelda art, symbols, item designs, UI, music, architecture, or characters as
  generation references.
- Carried forward: R-FUNC1 through R-FUNC5, R-ROLE2, R-MOT3.

### A10 - Zelda-type gameplay expansion work order

- Source: `ZELDA_GAMEPLAY_WORKORDER_2026-07-18.md`, commit `ae2f7de`.
- Scope: proposed gameplay expansion and world-object needs.
- Evidence: E1 design proposal, not an art audit or owner-approved build.
- Accepted for generation planning: every proposed object must name its verb,
  readable state, placement, and one-finger interaction before modeling.
- Rejected as visual reference: all Zelda-specific appearance and iconography.
- Carried forward: R-ROLE1, R-FUNC1, R-FUNC2.

### A11 - Pearl Castle architecture and Royal Loo implementation audit

- Source and commit: `CASTLE_PEARL_ART_AUDIT_2026-07-18.md`; branch
  `codex/castle-rainbow-shell-5of5`.
- Scope: Grand Hall architecture, ceremonial motifs, visible upper gallery,
  Cloud Lounge seating, and toilet side-view construction.
- Evidence class: E2 export measurements plus isolated Blender renders and an
  E3 first-pass Mobile review that rejected four scene-level failures; the
  corrected pass still requires replacement Mobile evidence before promotion.
- Findings independently verified: generic cylinders, box rails, torus lights,
  flat banners, raw rainbow gate, and box cushions were still visible blockout
  language; the toilet lacked a continuous rear skirt and convincing S-trap.
- Findings accepted: shells should express joints, capitals, bowls, keystones,
  and water transitions; rainbows should mark ceremony and wayfinding rather
  than decorate every prop.
- First runtime rejects: the retained throne occluded protected character art,
  outdoor clouds failed as seating, fixtures read as column-mounted bulbs, and
  two nonblank review cameras did not actually frame their audit targets.
- Findings accepted as proposals only: all eighteen kit members are 5/5 targets,
  but remain structural/isolated candidates until fixed Mobile captures and
  owner review.
- Findings rejected: motif count, pastel harmony, or successful export alone
  cannot establish a 5/5 score.
- New rules: R-MOT4 and R-GEO5; the runtime rejects also reinforce R-QA2 and
  R-QA4.
- Required tests: one-mesh/triangle/static-node GLB audit, live placement count,
  eleven fixed hall/throne/entrance/gallery/room captures, route and light-budget
  preservation, and both isolated and runtime toilet side views.

### A12 - Pearl Castle contiguous-room evidence correction

- Source and commit: expanded `CASTLE_PEARL_ART_AUDIT_2026-07-18.md`; branch
  `codex/castle-rainbow-shell-5of5` after the green eleven-view runtime pass.
- Scope: every castle room adjoining or visible from the Grand Hall, including
  Toy Room, Royal Library, Star Chamber, Dreaming Floor, undercroft, basement
  rooms, music room, royal bedroom, Royal Loo, and back chamber.
- Evidence class: E3 Mobile runtime screenshots plus E2 Blender/export metrics.
- Findings independently verified: a structurally green focal audit still hid
  raw colored blocks, slab furniture, text glyphs, flat windows, primitive
  storage/craft/bath props, camera clipping, and a decorative gate with no
  destination read.
- Findings accepted: capture scope must follow contiguous player sightlines;
  motifs must identify function; coordinated room families outperform isolated
  one-off replacements; playable assemblies must preserve separate trigger
  nodes beneath a unified visual design.
- Findings accepted as proposals only: the expanded forty-nine-asset kit is a
  5/5 target but remains a runtime candidate until all seventeen fixed Mobile
  frames are inspected and the owner accepts it.
- Findings rejected or superseded: a green eleven-view probe, nonblank frame,
  or isolated render does not establish game-wide castle coverage.
- New rule: R-QA7. Reinforces R-GOV4, R-ROLE3, R-MOT4, R-GEO5, and R-QA4.
- Required test: seventeen fixed contiguous-area captures, measured import
  budgets for all forty-nine assets, and explicit preservation of exit,
  toilet, seven-key music, bed, wardrobe, craft, and moving-stand contracts.

## Consolidated generation rules

These rule IDs are stable. Reference them in manifests and review notes.

### Governance and evidence

- **R-GOV1 - Measure the export.** Parse triangles, materials, dimensions,
  bounds, mesh islands, and textures from the output file. Never accept the
  generator's own manifest as proof of those facts.
- **R-GOV2 - Keep stages distinct.** Use `generated`, `structural_pass`,
  `isolated_visual_pass`, `runtime_pass`, and `owner_accepted`. Numeric scores
  describe runtime art quality, not pipeline progress.
- **R-GOV3 - Prove the reviewer can fail.** Every review-tool revision must
  reject at least one known-bad negative-control asset before reviewing the
  real batch.
- **R-GOV4 - No self-awarded completion.** Runtime Mobile evidence is required
  for 4/5. Only owner acceptance of shipped views establishes 5/5.

### Role and identity

- **R-ROLE1 - Write the verb first.** State what the object does, where it is
  seen, how it is used, and what changes after interaction before generation.
- **R-ROLE2 - One role per output.** A train is not a station scene; coral is
  not a reef vignette; a fruit is not a winged mascot. Generate assemblies
  only when the role contract explicitly asks for an assembly.
- **R-ROLE3 - Name the runtime target.** Every candidate manifest entry needs
  `runtime_target`, referencing script/scene, scale, camera range, and expected
  placement count.
- **R-ROLE4 - Match solution scale to role scale.** A world, hall, arena, or
  biome is a kit plus layout and composition workstream, never one miniature
  GLB counted as coverage.
- **R-ID1 - Preserve the noun before the mood.** Identity, anatomy, and
  function constraints appear before storybook, magical, underwater, or cute
  styling in every prompt.
- **R-ID2 - No unsolicited characters.** No faces, eyes, mouths, expressions,
  invented creatures, or character poses on scenery and ordinary objects.
- **R-ID3 - No semantic contamination.** No habitat, flowers, coral, bubbles,
  gems, wings, stars, swirls, confetti, backing sticker, or display pedestal
  unless the role explicitly requires it.
- **R-ID4 - Protected sources remain exact.** Book characters, family voices,
  friend cutouts, child toys, carrot, watering can, and other protected source
  art are not regeneration targets. Presentation may be improved separately
  without redesigning identity.

### Motif, geometry, and materials

- **R-MOT1 - Use a family reference board.** Butterfly, beetle, coral, plant,
  toy, kitchen, snow, architecture, vehicle, and craft families each need
  their own source observations and forbidden substitutions.
- **R-MOT2 - Establish one reference member first.** Complete the full runtime
  loop on one difficult family member before generating more than 6-12
  variants from that family.
- **R-MOT3 - Encode meaning redundantly.** Important state uses silhouette,
  orientation, scale, motion, and value in addition to color. This is required
  for elemental objects, locks, keys, clues, and completed puzzle pieces.
- **R-MOT4 - Attach motifs to function.** Shells, rainbows, stars, and other
  branded forms belong at meaningful joints, thresholds, focal points, or
  state cues. Repeating them as stickers on every surface weakens place identity.
- **R-GEO1 - Read as a black silhouette.** Test at full frame and 112 px.
  Locomotives need unmistakable locomotive cues; butterflies need complete
  anatomy; plants need their actual growth habit.
- **R-GEO2 - Avoid primitive convergence.** Rounded boxes and cones are a
  blockout grammar, not a final identity. Add role-specific construction,
  asymmetry, joints, transitions, and structural landmarks.
- **R-GEO3 - Let the world provide support.** Do not attach the same base rock,
  soil disk, pedestal, or habitat slab to every scatter object. Floating roles
  are the exception and must be declared.
- **R-GEO4 - Plants are volumes.** Kelp and seagrass use overlapping, twisted,
  thickness-bearing clumps. Better-painted cards do not resolve a card-mass
  audit failure.
- **R-GEO5 - Audit functional assemblies from all useful views.** Plumbing,
  seating, hinges, vehicles, doors, and tools must preserve their structural
  connections in front, side, and gameplay views. A readable front icon does
  not excuse a missing rear body, support, joint, or mechanism.
- **R-MAT1 - Material identity precedes palette harmony.** Wood, metal, stone,
  leaf, snow, cloth, glass, and shell must remain distinguishable through
  value, roughness, shape transitions, and restrained local color.
- **R-MAT2 - Reconcile at room scale.** New floor, wall, counter, and prop
  colors are reviewed together. Do not promote a vivid texture into a muted
  room one file at a time.

### Repetition and composition

- **R-REP1 - Test the placement pattern.** Seam-safe edges are insufficient.
  Review 3x3 tiles, dense scatter, sparse scatter, path edges, and long camera
  pans for repeated centers, pedestals, diagonals, and color hotspots.
- **R-REP2 - Provide structural variants.** Rotation and hue shifts do not
  create a family. Change silhouette, branching, height, mass distribution,
  and negative space.
- **R-REP3 - Protect gameplay composition.** Stress with the player, HUD,
  pointer, touch controls, objectives, route sightlines, and reserved
  footprints visible.

### Function, animation, and age-four legibility

- **R-FUNC1 - Model the state machine.** List idle, active, hit, collected,
  locked, unlocked, complete, or broken states that the role uses. Separate
  files/meshes are required when pieces detach or geometry changes.
- **R-FUNC2 - Make the action obvious without text.** The target, receiving
  slot, direction, and current state must be readable by a non-reader with one
  finger.
- **R-FUNC3 - Exaggerate camera-critical differences.** Adjacent size steps,
  facing direction, active/inactive states, and attachment points must survive
  the fixed three-quarter gameplay camera and phone-scale display.
- **R-FUNC4 - Keep effects separate.** Wakes, bubbles, impact flashes, magic
  particles, pointers, and reward sparkles are runtime layers, not baked into
  object albedo or geometry.
- **R-FUNC5 - Persist success feedback.** A solved statue, lit lantern, opened
  lock, collected item, or completed assembly keeps an unmistakable visual
  state after the transient fanfare ends.

### QA and promotion

- **R-QA1 - Inspect all views.** Required isolated views are front, side,
  back, three-quarter, black silhouette, and phone-size thumbnail.
- **R-QA2 - Strengthen render checks.** Measure frame coverage, clipping,
  brightness, contrast, scale sanity, and silhouette occupancy. A nonblank
  render is not a visual pass.
- **R-QA3 - Test texture edges and fields.** Check all four edges plus 3x3 and
  larger fields. Include compressed in-engine output, not only source PNGs.
- **R-QA4 - Capture runtime distances.** Near, mid, gameplay, reverse, motion
  extreme, transition, bright, and shadowed Mobile-renderer views are required
  when relevant.
- **R-QA5 - Compare against the active asset.** Promotion requires a paired
  capture showing that the candidate improves the actual role without
  regressing function, frame time, readability, or neighboring art.
- **R-QA6 - Wire or quarantine.** Promote and reference the asset in the same
  workstream, with a byte-identical backup. Rejected, superseded, and
  reference-only candidates remain labeled and excluded from APK export.
- **R-QA7 - Follow contiguous sightlines.** A focal-area audit must enumerate
  every adjacent player-visible room and approach. A technically successful
  capture set fails when uncaptured neighboring art can remain at blockout
  quality.

## Family-specific directives for the next pass

These are current audit findings, not universal style rules.

1. **Coral:** remove the shared blue-grey pedestal. Generate bare growth forms
   with structural variation and test them embedded in the actual seabed.
2. **Kelp and seagrass:** replace planar fans with volumetric clumps. Test near
   and dense mass placement for overdraw and visual noise.
3. **Sky Lagoon train:** establish a locomotive reference with stack,
   cowcatcher, rods, rail wheels, and coupling logic. Generate a compatible
   rails/ties/curves/platform kit; cars without track do not solve the role.
4. **Butterfly meadow:** produce a cool, quiet base with low flower density.
   Use warmer high-density variants only as feature patches.
5. **Kitchen:** review textures and prop tints as one room. Avoid candy striping
   that overwhelms muted book-derived or shipped objects.
6. **World-scale roles:** reef hub, Sky Lagoon world, snow terrain, castle hall,
   Butterfly World, arenas, and alpine interiors require modular kits and
   runtime layout. Withdraw single-miniature substitutes from coverage counts.
7. **Northern Kingdom:** do not regenerate. The active authored kit is the
   reference. Existing pack candidates are reference-only unless an owner
   explicitly reopens a role.
8. **Dungeon items and locks:** use original Reef of Light designs with iconic
   silhouettes, matching receiver shapes, persistent solved states, and
   element differences beyond color. Do not imitate Zelda item art.
9. **Picture-game sprites and painted 2D textures:** use the strongest current
   pack examples as finish references, while preserving separate assembly
   pieces and testing them in the actual minigame camera.

## Gate and queue for the next generation run

### Gate 0 - Repair review integrity

Bulk generation is blocked until all are true:

- render metrics join to every model row;
- pass and score fields are measured, not hardcoded;
- GLB properties are parsed from exports;
- a renamed-blob anatomy negative control fails;
- R088 is removed or explicitly non-asset;
- each retained candidate has a runtime target or `reference_only` status;
- render framing and all-edge/field repetition checks are active.

### Queue 1 - Prove three family pilots

Run only three small pilots first:

1. one bare coral family with three genuinely different growth forms;
2. one volumetric kelp family with sparse and dense placement tests;
3. one locomotive plus a minimal straight/curve/station track kit.

Each pilot must reach `runtime_pass` before expanding its family. A failed
pilot updates this log before regeneration.

### Queue 2 - Promote proven low-risk work

Promotion is not new generation. Map and stage the strongest painted textures,
picture-game sprites, small dungeon props, and other independently reviewed
assets one area at a time. Capture Mobile comparisons after each area.

### Queue 3 - Build missing kits

After the pilots and promotions, open one kit workstream at a time for castle
architecture, kart spectator/pit dressing, reef walls and portal shell, Sky
Lagoon/fairy castle, Butterfly World, clutter/loot, and other gaps in
`ART_GAP_WORKORDER_2026-07-18.md`.

Newly developed areas, including the opera stage and dungeon redesign, must be
added to the audit inventory before their objects enter a bulk generation run.

## Required generation packet

Create this packet for every role before generating. Missing fields block the
role.

```text
audit_log_version: 2026-07-18-v1
asset_id:
role_name:
role_type: prop | kit_piece | texture | sprite | interactive | composition
runtime_target:
referencing_script_or_scene:
gameplay_verb:
states_and_separate_parts:
camera_and_distance:
world_scale_and_reference_dimensions:
placement_count_and_density:
support_surface_or_attachment:
source_motif_references:
identity_and_anatomy_anchors:
silhouette_landmarks:
material_list:
palette_limits:
forbidden_motifs:
family_variation_axes:
repetition_test:
mobile_capture_plan:
active_asset_comparison:
license_and_provenance:
owner_decisions_affecting_role:
applicable_rule_ids:
```

Default forbidden prompt clause for non-character objects:

```text
Generate exactly one named object with no scene, habitat, pedestal, base rock,
face, eyes, mouth, character, wings, flowers, coral, bubbles, gems, stars,
swirls, confetti, sticker border, text, watermark, or baked lighting unless a
listed role requirement explicitly asks for that element. Preserve the
object's real construction, functional parts, and complete silhouette before
applying the project palette or storybook finish.
```

## Required output record

Every generated file or family member records:

- generation packet and generator version;
- source image or deterministic seed;
- editable source path;
- exported-file measurements;
- isolated review state and reviewer;
- runtime target and placement status;
- negative-control pipeline version;
- runtime capture paths;
- current evidence class and art score;
- rejection, supersession, or owner-acceptance reason.

## Append-only intake template

When another audit arrives, append an entry before changing prompts:

```text
### Axx - Audit name
- Source and commit:
- Scope:
- Evidence class:
- Findings independently verified:
- Findings accepted as proposals only:
- Findings rejected or superseded:
- New or changed rule IDs:
- Roles/families affected:
- Required negative-control or runtime test:
```

Do not silently rewrite history. If a finding changes, keep the old entry and
add a dated correction identifying the stronger evidence or owner decision.

## Log history

- **2026-07-18-v3:** Added the Pearl Castle contiguous-room correction, expanded
  the generation kit from eighteen to forty-nine props, and established R-QA7
  after a green eleven-view pass still hid adjacent 0-2/5 blockouts.
- **2026-07-18-v2:** Added the Pearl Castle and Royal Loo implementation audit,
  role-based motif hierarchy, multi-view functional-assembly rule, measured
  export contracts, and the pending Mobile/owner acceptance boundary.
- **2026-07-18-v1:** Integrated the Claude GEN-2 corpus, human runtime audits,
  placement audit, non-5 critique, independent implementation review, Codex
  iteration-2 directives, revised generation contract, Jolt/feel audit,
  Claude Fable dungeon audit, and Zelda-type gameplay work order. Established
  evidence classes, stable rule IDs, Gate 0, three-family pilot queue, and the
  required generation packet.

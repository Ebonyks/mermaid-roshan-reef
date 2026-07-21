# Claude handoff — Opera House job assets and outfits

## Source of truth

Use `assets_src/concepts/opera_jobs_flat_2026-07-21/` as the visual source of
truth for the twelve non-boss jobs. Each job has three accepted sheets:

- `<job>_outfit_sheet_2026-07-21.png`
- `<job>_gameplay_sheet_2026-07-21.png`
- `<job>_stage_states_sheet_2026-07-21.png`

Use `audit/opera_job_flat_prototype_ledger_2026-07-21.csv` for the exact 576
card paths. Use `OPERA_JOB_FLAT_ART_AUDIT_2026-07-21.md` for scores and binding
continuity rules. The full set already passed a 4.5/5 gate.

Do not use earlier realistic or mesh-first experiments as style targets. Do
not modify protected book art, family voices, or friend cutouts. Do not create
Curtain Dragon, Shadow Phantom, or Midnight Maestro assets in this phase.

## Modeling boundary

The flat sheets are design/model references, not runtime sprite atlases. Build
original, efficient 3D interpretations with the accepted silhouette, palette,
and state logic. Do not trace every illustrated highlight into geometry.

Roshan's current act avatar is still a `Sprite3D` using
`assets/characters/roshan_sprite.png`. Until an approved outfit-aware 3D
character pipeline exists, build each outfit as a separate, reversible kit:

- headwear or hair-adjacent accessory;
- chest/shoulder garment shell;
- high tail sash/apron/belt attachment;
- primary hand prop;
- optional secondary prop;
- crest and wardrobe display.

Never replace Roshan's mermaid tail with legs. Outfit geometry must not clip
the tail silhouette or cover the face. Keep the cutout fallback unchanged.

## Live job map

`scripts/opera_house.gd` is the roster source of truth. The older asset request
that mentioned Opera Star was stale; the live Floor 2 slot is Boxer.

| Job | Runtime kind / builder | Critical live nodes or hook |
| --- | --- | --- |
| Pastry Chef | `order` / `_build_order()` | `OperaPad0..2`, `OperaGoal`, cake order, stir, toppings |
| Detective | `sleuth` / `_build_sleuth()` | `SearchProp0..5`, `TiaraChest`, three clue states |
| Ballerina | `echo` / `_build_echo()` | `OperaPad0..3`, demo/repeat tile glow |
| Candy Maker | `press` / `_build_press()` | `CandyPress`, gauge/slider, seven candies |
| Doctor | `doctor` / `_build_doctor()` | `PlushPatient`, `Stethoscope`, `Thermometer`, `BandageRoll` |
| Farmer | `scroll` / `_build_farm()` | CanvasLayer piggies, food target, toss feedback |
| Boxer | `box` / `_build_box()` | Ring, round waves, friendly imps, championship belt |
| Magician | `shuffle` / `_build_shuffle()` | `OperaHat*`, bunny-fish, shuffle/select/reveal |
| Painter | `order` / `_build_order()` | `OperaPad0..2`, `OperaGoal`, `PaintBrush`, canvas stripes |
| Astronaut Engineer | `fix` / `_build_fix()` | `PipePiece0..2`, ghost slots, valve, rocket launch |
| Racecar Driver | `race` / `_build_race()` | `RaceFlag`; existing KartGame is complete |
| Pop Star | `dance` / `_build_dance()` | `StarMicrophone`; existing DanceEngine is complete |

## Required continuity by job

- Chef: preserve the live layer order; bowl, stir, oven, topping targets, and
  final cake must be separate states.
- Detective: six boxes need different silhouettes. Only paw, feather, and
  ribbon are clues; fish/sock are friendly decoys; three clues open the tiara
  chest.
- Ballerina: four tiles differ by color and icon. Demonstration and pressed
  states must remain readable with emissive material swaps, not added lights.
- Candy Maker: the gauge has a broad green-teal center. Seven candies differ by
  body silhouette, not only by face decal.
- Doctor: every patient is the same coral five-armed starfish plush. Never swap
  to a bear, rabbit, axolotl, or ordinary fish.
- Farmer: keep three flat parallax layers and pose-swapped pig sprites/meshes.
  Do not turn the meadow into physics foliage.
- Boxer: all equipment is padded and toy-like. Imps are friendly targets;
  impact is a bubble puff, never injury.
- Magician: the bunny-fish is a pink fish with fins and tail plus long rabbit
  ears; it never gains rabbit legs.
- Painter: the order is plum, coral, cream wherever shown. Keep blank, first,
  second, and finished canvas states consistent.
- Astronaut Engineer: straight, elbow, and ring pipe pieces must only fit their
  matching sockets. Launch exhaust is bubbles, not flame.
- Racecar Driver: retain the existing kart engine. Add an Opera skin, tail-safe
  seat/channel, boost strip, flags, and reward props only.
- Pop Star: retain the existing dance engine. Use left/right/up/down arrows
  paired with coral/teal/plum/cream, a pearl microphone, and broad rhythm
  effects.

## Recommended asset architecture

Create one shared Opera job library plus small per-job scenes:

```text
assets/opera/jobs/shared/
assets/opera/jobs/pastry_chef/
assets/opera/jobs/detective/
...
assets/opera/jobs/pop_star/
assets_src/blender/opera_jobs_2026-07-21.blend
assets_src/blender/qa_opera_jobs_2026-07-21/
```

Shared pieces should include shell/pearl trim, low pedestals, curtain flats,
rounded brass frames, pointer glow, bubble puff, confetti, and bow marker. Job
folders should contain only distinct hero props and state variants.

Use one mesh with material/visibility states where practical:

- open/closed oven, chest, hat, press, and curtain;
- idle/active tile, gauge, boost strip, and progress lamps;
- blank/progressive/finished canvas;
- empty/filled shelves and boards;
- pipe loose/ghost/fitted states;
- before/after patient and reward tableaux.

Do not model the contact-sheet background or cell dividers.

## Modeling order

1. Shared palette/material library, trim, pedestals, pointers, and effects.
2. Floor 1 gameplay hero props and state swaps.
3. Floor 2 gameplay hero props, with Doctor species lock reviewed first.
4. Floor 3 gameplay hero props, with Painter order and pipe matching reviewed
   before integration.
5. Job stage modules and scenic flats.
6. Reversible Roshan outfit kits and wardrobe displays.
7. Optional secondary dressing only after all mechanic-critical props pass.

Review every family in fixed 0°, 45°, and 135° isolated renders plus at least
one Mobile-render gameplay camera. Reject any interpretation below 4.5/5 or
any version that loses the flat prototype's silhouette/state logic.

## Mobile constraints

- Godot Mobile renderer on every platform; Speedy is the default.
- No new OmniLights. Use existing scene lighting, matte materials, selective
  emission, and cheap unshaded effect cards.
- Shared palette materials; no unique 1024 texture per small prop.
- Keep primary props approximately 500–4,000 triangles, major stage modules
  under 10,000, and tiny dressing under 1,000 unless a measured exception is
  justified.
- Use simple static collision only on floors, large machines, ring edges,
  track barriers, and direct interaction surfaces.
- Farmer scenery and most scenic flats must never become physics bodies.
- Limit glass to the Engineer helmet, bubble tank, and one rocket window layer.
- Cap bubble/confetti/ribbon particles aggressively and provide a Speedy cull
  path.
- New textures remain at or below 1024 px; POT only if VRAM compressed.

## Integration discipline

- Preserve state on `ReefMain`; follow the existing extracted
  `scripts/opera_act.gd` architecture.
- Replace primitive builders mechanically, one job family per commit. Do not
  redesign gameplay and modeling in the same commit.
- Keep current node names or add an explicit adapter so probes and interaction
  logic remain stable.
- Outfit integration must retain the current cutout fallback and must not
  destructively edit `roshan_sprite.png`.
- Every new GLB, texture, and Blender source needs an `ASSET_LICENSES.md` line.

## Validation

For each job family:

1. Run the GDScript parser and inference lint on changed scripts.
2. Import under Godot 4.4 Mobile rendering.
3. Capture outfit/front, hero-prop, stage-wide, active-state, and completion
   views at the actual gameplay camera.
4. Verify the pointer, voice line, retry loop, and completion remain usable by
   a non-reader with one finger.
5. Run `scripts/ci.sh` and require every trusted probe to pass.

Do not begin boss work until the owner explicitly starts the boss phase.

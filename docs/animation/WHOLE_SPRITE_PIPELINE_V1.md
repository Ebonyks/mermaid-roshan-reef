# Whole-sprite adaptation pipeline — V1

Status: `PROPOSED / CANDIDATE`, owner-directed engine work, 2026-10-07.
Implementation: [sprite_pipeline.py](../../tools/sprite_pipeline.py). This is a
preparation/repair engine; its outputs do not accept art or integrate runtime
animation. The [wave fixture](../../assets_src/animation/whole_sprite_pipeline_20261007/README.md)
tests the format. The binding [production protocol](../../design/animation/ANIMATION_PRODUCTION_PROTOCOL.md)
and owner whole-figure, constant-size and single-unit decisions control.

The owner clarified the objective: develop a format for rapidly adapting
sprites, with the engine taking priority over fitting one image. The pink
outfit is the first fixture. Existing wardrobe code already composes its
choices into one texture; this change supplies authoring evidence and sparse
whole-figure correction requests without changing wardrobe saves or playback.

## Define once, adapt through data

One versioned catalog has five blocks. Every concrete job references the shared
definitions instead of embedding another character-specific script.

| Block | Responsibility | Change when adapting |
|---|---|---|
| `sources` | Exact paths/hashes, role, dimensions, license, acceptance scope, permitted input pixels and source/crop provenance | Add the actual approved artwork for the requested variant |
| `characters` | Identity locks and geometry calibration: landmarks, head region, segment lengths/conditions | Keep Roshan's contract across outfits; calibrate a different character explicitly |
| `outfits` | Character ID, approved references, garment description and invariant motifs | Add a named outfit definition; keep face, anatomy and motion authority |
| `actions` | Verb, count/rate, phases, entry/exit, tolerances, context, named key gaps and backend recipe reference | Add an action or tempo contract; chronological frames remain required |
| `jobs` | Character/outfit/action IDs, exact frame inventory, canvas mapping, pinned master, joint/review files and shared campaign ledger | Bind another sequence to the definitions; no code fork |

The complete executable catalog is [catalog.json](../../assets_src/animation/whole_sprite_pipeline_20261007/catalog.json).
The existing [animation card](../handoffs/codex_roshan_motion_language_2026-10-04/templates/ROSHAN_ANIMATION_CARD_V1.json)
continues to own scene/input/contact/runtime context. This catalog is its
batchable authoring companion, not a replacement scene planner.

All paths are project-relative. Native candidates, references and exports live
under `assets_src/`; disposable work uses `tmp/`. The engine refuses output in
runtime `assets/`, paths escaping the project and private/internal paths.

## Repeatable operator sequence

Run from the project root. `py -3.10` is the measured installed environment with
OpenCV 4.13.0, Pillow and NumPy on this Windows host. Elsewhere use a Python
environment with those dependencies. Missing OpenCV produces an explicit
pending geometry lane; it never silently skips into readiness. No dependency
installation or model download is performed by the engine.

```powershell
$catalog = 'assets_src/animation/whole_sprite_pipeline_20261007/catalog.json'
$out = 'tmp/sprite-adaptation'
py -3.10 -B tools/sprite_pipeline.py inspect $catalog --job pink_wave_native --out "$out/inspection.json"
py -3.10 -B tools/sprite_pipeline.py plan $catalog --job pink_wave_native --report "$out/inspection.json" --out "$out/repair_plan.json"
py -3.10 -B tools/sprite_pipeline.py export $catalog --job pink_wave_native --out "$out/aseprite-review"
```

`inspect` returns 0 only when its candidate checks pass, 1 for a truthful
blocked review and 2 for malformed/stale input. `plan` saves two named missing
keys in the wave fixture; it does not request a still for every failed frame.
Machine matte problems remain export problems, rather than 41 redraw jobs.

Before a generation call, reserve its budget slot. A reservation counts even
if the backend fails or the chat is interrupted:

```powershell
py -3.10 -B tools/sprite_pipeline.py reserve-key $catalog --job pink_wave_native --plan "$out/repair_plan.json" --key raise_key --out "$out/reservation.json"
```

Codex dispatches the saved prompt and its bound images through built-in
ImageGen. The CLI never invokes a paid endpoint. After the call, create a
receipt with `provider`, `request_id`, `provider_revision` (explicitly hidden
when unexposed), `elapsed_seconds`, `cleanup_minutes`, actual `usage`,
`disposition`, the exact `prompt_sha256` and ordered `binding_hashes`. Record it:

```powershell
py -3.10 -B tools/sprite_pipeline.py record-key $catalog --job pink_wave_native --plan "$out/repair_plan.json" --key raise_key --image '<native image path>' --receipt "$out/provider_receipt.json" --out 'assets_src/animation/my_action/key_attempt_1'
```

Use `FAILED` and omit `--image` for a failed backend call. Every native image is
copied without pixel changes; it can enter only as `CANDIDATE` or `REJECTED`.
Record time overruns honestly. They block further reservations. Repeated jobs,
new outfits and different backends share the campaign ledger; they cannot reset
the two-call action budget. Ledger mutations have an exclusive lock; a pending
reservation must be resolved rather than forgotten. New corrective commissions
retain their prior campaign evidence.

## Geometry and review evidence

The engine reuses the handoff's [unchanged numbers-only measurement implementation](../handoffs/codex_roshan_wave_whole_sprites_2026-10-07/tools/measure_wave.py),
configured from character data. It requires every declared landmark track and
finite per-frame measurement. Similarity/ECC estimates are diagnostic scale
measurements, not anatomical or artistic acceptance.

Joint annotations use this shape, in native canvas pixels:

```json
{"frames":[{"index":7,"sha256":"exact frame hash","points":{"shoulder":[0,0],"elbow":[0,0],"wrist":[0,0],"tip":[0,0]},"flags":{"hand_open":true}}]}
```

Coordinates above illustrate syntax, not valid Roshan measurements. Every
frame must have hash-bound annotations. Missing annotations, missing condition
flags, failed tracking and missing masters stay `PENDING`; proportion failures
stay `FAIL`. K0's relaxed hand is exempt only with explicit `hand_open: false`.
The waving upper arm/forearm still require their measurements.

Review records bind index and SHA-256, reviewer/date and `reviewer_kind`, `identity`, `outfit`,
`topology`, `motion`, notes and PASS/FAIL/PENDING states. Full-speed review is
separate and pins the entire ordered frame-hash list. Passing the required human lanes also needs `reviewer_kind: human` and an actual human review; a model must use `model_observation` and cannot declare itself human. Known negative observations may block a candidate. Static boards cannot
satisfy that lane. Any changed frame invalidates its old observations.

Adjacent defects become one contiguous repair span with clean context on both
sides. Expand the declared context where hair, bodice, shoulders or fin response
extends farther. Repair prompts request complete figures, keep independent
character/outfit/action locks and accept only approved identity/outfit/pose
inputs. Position guides, rejected studies, diagnostic boards and gameplay/HUD
captures are excluded from generation-pixel bindings.

## Aseprite bridge and next animation stage

[sprite_pipeline_bridge.lua](../../tools/sprite_pipeline_bridge.lua) imports each
complete native frame into one RGBA layer, distributes the integer-millisecond
clock, creates phase tags, saves and reopens the master, then exports every
frame. The Python engine compares dimensions, all decoded RGBA bytes and timing.
It never slices/replaces limbs, warps pieces, inserts holds, cross-fades copies,
changes the canvas or hides reference/reject layers in the delivery master.

`SOURCE_EXPORT_PASS` proves source transfer only. It can preserve an opaque,
rejected study for inspection; the alpha/readiness report continues to fail.
Native generated key dimensions and alpha are recorded without pretending they
already match the 256px delivery cell. Aseprite whole-canvas normalization must
be explicitly recorded and remeasured in the next job revision.

The saved backend block points to the previously executed local Union recipe.
The engine does **not** claim a parameterized LTX runner or a new transformer
take: corrected keys and W3 guide annotations must first pass their geometry
review. The later temporal take needs its own bounded recipe/card, native and
decoded measurements, whole-frame span mapping and all affected transitions.
Godot atlas sampling/runtime/device/child/owner checks follow when integration
is commissioned. `candidate_ready` is an authoring check, never
`DELIVERY_ACCEPTED`, release approval or master-audit satisfaction.

## Validation

```text
python -B -m unittest tools.tests.test_sprite_pipeline
python -B tools/audit_document_authority.py
python -B tools/audit_development.py --base auto
```

Focused tests cover source/review drift, missing joints/flags, proportions,
guide misuse, chronology, shared outfit budgets, reservations and failed calls,
protected/output paths and frame-clock rounding. Actual Aseprite and native
measurement evidence is in the fixture, separate from synthetic test geometry.

`normalize-key` performs only a declared Aseprite uniform whole-canvas resize to the action's `delivery_cell`; unequal aspect ratios fail before writing. Use a fresh output directory. Native source and normalized/master hashes are recorded, then bind the normalized samples in another data-defined job and rerun `inspect`. This operation cannot repair internal head/arm proportions or make a failed key accepted. The tested two-call wave campaign is exhausted; both keys remain rejected.

Every job also pins a `derivation` JSON. Each frame declares its index/hash, whole-frame production method, `pixel_assembly: "NONE"`, pinned parent files and all edits. Missing provenance remains pending; pasted-part/limb-deformation methods fail even in a one-layer master. This checks declared ancestry; exact human method/pixel review remains separate. CLI input errors return2 without treating malformed data as readiness.

Actions bind view slots such as `@rest` and `@raised`, resolved through the outfit's `source_aliases`. Another approved outfit binds its own full-figure rest/raised artwork while keeping the same wave action, timing and geometry contract. Character defaults and explicit job bindings can supply other view slots; unresolved or recursive aliases fail. The 24-test suite proves a blue reference and boundary use the same action without inheriting the pink appearance binding.

Native archive byte preservation: the packet has scoped Git attributes preventing line-ending conversion. New CLI JSON and prompt files use UTF-8 LF bytes. Existing Git metadata parents may declare `hash_normalization: git_text_lf` plus their original checkout checksum; this normalization is forbidden for images/native binaries. The manifest records immutable Git delivery checksums and any differing checkout checksum. Historical generation inputs retain their original bytes and hashes.

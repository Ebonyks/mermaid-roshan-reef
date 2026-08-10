# The game-wide visual design audit tool

`tools/audit_visual_design.py` turns the current design language's written promises into
checks that fail out loud. It is built to be **expanded and stress-tested by
Codex** — the expansion surface is a JSON file, and the tool refuses to pass
its own stress run if a check has never been proven capable of failing.

The final owner decision on 2026-08-09 makes the shipped game true Canvas 2D.
Every executable Godot `*3D` class, `WorldEnvironment`, `SideScrollStage`, and
active 3D model-resource load is migration debt, never acceptable evidence for
a passing visual check. Source art can still be
a flattened PNG; the runtime staging that presents it must also be 2D.

First findings from it: `VISUAL_DESIGN_AUDIT_2026-07-28.md`.

---

## Quick start

```bash
pip install Pillow numpy                        # same pins as probes.yml

python3 tools/audit_visual_design.py            # advisory run, every zone
python3 tools/audit_visual_design.py -v         # include INFO and SKIP
python3 tools/audit_visual_design.py --zone sky_lagoon
python3 tools/audit_visual_design.py --category layering
python3 tools/audit_visual_design.py --list-checks
python3 tools/audit_visual_design.py --strict   # saved-facts diagnostic; gaps block
python3 tools/audit_visual_design.py --fresh-runtime --godot "$GODOT" --strict
                                                # trusted complete-evidence gate
python3 tools/audit_visual_design.py --stress   # prove every check can fail
python3 -m unittest tools.tests.test_audit_visual_design

# Inspect an isolated saved capture (diagnostic only; it cannot report PASS):
python3 tools/audit_visual_design.py --runtime-facts C:/tmp/visual_facts.json --no-report
```

Every run writes `audit/visual_design_report.json` (machine-readable, for
Codex) and `audit/visual_design_report.md` (human-readable, for the owner).
`--no-report` suppresses that.

## The two halves

| Half | What it sees | Runs where |
|---|---|---|
| `tools/audit_visual_design.py` | source PNGs; declared Canvas-layer contract; the complete runtime dependency manifest; current clean Git HEAD/source revision; bound harness/spec/scene/project/builder hashes; flattened, target-hidden, temporal-stability, and source-projection evidence; ASSET_LICENSES.md; ci.sh | static checks and saved-evidence diagnostics run anywhere with Python; authoritative runtime PASS needs `--fresh-runtime` and trusted Godot |
| `scripts/probe_visual_audit.gd` | the assembled scene: tagged live Canvas instances, effective Camera2D movement, provenance-bound touch targets, live Canvas draw-order/occlusion samples, a frozen flattened viewport capture, and an asymmetric visible/hidden capture sequence for each exact bound Canvas target; legacy 3D counts are debt-only | needs exactly Godot 4.7.1-stable with the Mobile renderer at 1280×720 `canvas_items/expand`; writes `audit/visual_runtime_facts.json` by default |

The Python tool ingests the facts file when it exists. `--runtime-facts PATH`
selects an isolated evidence bundle for diagnostics only. Saved JSON and PNGs
never carry PASS authority, even when every recorded hash is self-consistent.
`--fresh-runtime` is the only authoritative runtime mode: the audit creates a
random one-use challenge, launches the bound probe itself, verifies the response
in that process, snapshots capture bytes into private memory, and deletes the
temporary response before evaluating checks. Checks that need runtime evidence
report `SKIP/COVERAGE_GAP` with a reason when it does not — **a check that
cannot run never reports a pass, and it blocks `--strict`.** A presentation
outside a rule's declared scope reports `INFO/NOT_APPLICABLE` explicitly.

## Severities

| | Meaning |
|---|---|
| `ERROR` | Violates a written rule. |
| `WARN` | A real cost or unresolved review finding. |
| `MANUAL` | The tool knows it cannot judge this; a human review remains open. |
| `INFO` | The check ran successfully or is explicitly not applicable. |
| `SKIP` | The check could not run; this is missing coverage, never a pass. |

Severity describes impact. Disposition describes whether the audit can close:

| Disposition | Meaning in strict mode |
|---|---|
| `PASS` | Check ran and accepted its evidence. |
| `FAIL` | Rule violation; blocks. |
| `REVIEW_OPEN` | Warning still needs disposition; blocks. |
| `MANUAL_OPEN` | Required human evidence is missing; blocks. |
| `COVERAGE_GAP` | Required check could not run; blocks. |
| `WAIVED` | Complete owner-approved disposition of a failure/review; visible, never rewritten as PASS. |
| `NOT_APPLICABLE` | Spec explicitly excludes this presentation from the rule. |

The audit-level result is `UNSATISFIED`, `SATISFIED_WITH_WAIVERS`, or
`SATISFIED`. `--strict` returns nonzero for every unresolved disposition, not
only for `ERROR` severity.

## Design contract

Four rules govern every check. Breaking any of them is how audit tools become
noise that everybody mutes.

1. **Every check names a rule in the spec.** `@check(..., rule="layering_rule")`
   must match a key in `spec["rules"]`, whose value quotes the document it
   comes from. A check with no document behind it is an opinion, and opinions
   do not gate. Enforced by `test_every_check_names_a_rule_in_the_spec`.
2. **Checks are pure.** `(zone, repo, runtime_facts) -> findings`. No check
   writes to the repo.
3. **Silence is never a pass.** Emit `SKIP/COVERAGE_GAP` with a reason, or an
   explicit `NOT_APPLICABLE`, instead of returning nothing. Enforced for every
   zone/check pair by `test_every_zone_check_pair_has_a_disposition`.
4. **Every check is provably falsifiable.** `--stress` builds a synthetic repo
   engineered to violate the check and asserts it fires — *and* asserts it
   stays quiet on a clean fixture. A check with no stress case fails the
   stress run as a `STRESS GAP`.

---

## Expanding it

### Add a zone — JSON only

Append to `zones` in `tools/visual_audit_spec.json`:

```json
{
  "id": "reef_promenade",
  "name": "Reef Promenade",
  "art_medium": "flattened_2d",
  "presentation": "panning_depth_cards",
  "lifecycle": "active_shipped",
  "builders": ["scripts/promenade.gd"],
  "probes": ["scripts/probe_promenade.gd"],
  "murals":   ["assets/flats/reef/main/flat_reef_main_L*.png"],
  "canvas_layers": [
    { "id": "L0", "role": "far",
      "assets": ["assets/flats/reef/main/flat_reef_main_L0_*.png"] },
    { "id": "L1", "role": "near",
      "assets": ["assets/flats/reef/main/flat_reef_main_L1_*.png"] }
  ],
  "standees": ["assets/flats/reef/main/standee_reef_*.png"],
  "characters": ["assets/sprites/reef/roshan_*.png"],
  "rendered_readability_states": [
    { "id": "promenade_idle",
      "capture_adapter": "probe_visual_audit:reef_promenade_promenade_idle",
      "required_targets": ["slide", "gate"] }
  ],
  "asset_roots": ["assets/flats/reef", "assets/sprites/reef"],
  "budgets": { "zone_runtime_texture_mb": 18.0 }
}
```

`presentation` decides which checks apply. It describes runtime staging, not
the authored art medium:

| presentation | Gets |
|---|---|
| `panning_depth_cards` | target contract for a Canvas promenade: declared/runtime layer identity, content, coverage and motion; Canvas draw order; palette, overdraw, texture, release evidence, hygiene. The name is retained for report compatibility, not permission to use 3D. |
| `fixed_depth_cards`, `overhead_canvas` | palette, overdraw, standee, texture, release evidence, hygiene; no promenade parallax requirement |
| `legacy_3d_debt` | honest current-state classification for an unconverted active surface. It emits an explicit `ERROR/FAIL`; source-art risk checks still run, but the label can never satisfy the 2D audit. |
| `free_swim`, `rail`, `canvas`, `ui`, `overlay` | common texture, release-evidence, readability, and hygiene checks; presentation-specific flat checks are explicitly `NOT_APPLICABLE` |

`budgets` on a zone overrides the global `budgets` block for that zone only.

### The Canvas-only builder gate is game-wide

Presentation labels select presentation-specific checks; they do not exempt a
zone from the shipped 2D medium. Every `active_shipped` zone receives the same
source/runtime builder gate. A live or source builder that uses any executable
Godot `*3D` class, `WorldEnvironment`, `SideScrollStage`, or an active 3D model
resource is an explicit
`ERROR/FAIL`, whether the zone is labelled `panning_depth_cards`, `free_swim`,
`ui`, or anything else. Labelling a zone `legacy_3d_debt` is also an explicit
failure until it is converted. Inactive or absent builders may be
`NOT_APPLICABLE` or `COVERAGE_GAP`, but active 3D debt never is.

Conversely, a true `Node2D`/`CanvasItem` implementation can pass when the
current probe proves its live instances and the relevant Canvas contracts.
Legacy 3D nodes can report debt counts for triage, but those counts can
never establish accepted build, layering, occlusion, or readability evidence.

### Canvas-layer evidence is identity-based, not filename-based

`layering.mural_is_a_stack` never infers a layer from `_L0_` or `_L1_` in a
filename. `canvas_layers` declares stable IDs and the complete source-asset set
for each layer. The runtime probe then has to find one visible Canvas instance
for every declaration (tagged with `visual_audit_layer_id`), and records its
instance path, Canvas type, exact asset set, content signature, viewport
coverage, explicit Canvas draw order, and screen displacement during a real
`Camera2D` sample. The sample distance is the effective change in the
viewport's Canvas transform, not the requested camera offset.

Content signatures are derived from canonical decoded RGBA, not filenames or
encoded PNG bytes; RGB is zeroed wherever alpha is zero before hashing. A
compression-level, metadata, filename, or invisible-RGB change therefore cannot
make identical visible pixels look like a distinct L1, and fully transparent
assets are omitted rather than allowed to distinguish an otherwise duplicate
layer. Each live layer also hashes its effective composited RGBA on the same
64×36 viewport grid, so different source files, crops, tiling, or transforms
that paint the same layer remain duplicates. Coverage is sampled
on a 64×36 viewport grid against effective Canvas alpha: decoded texture alpha
is multiplied by the visual's `self_modulate.a`, every ancestor CanvasItem's
`modulate.a`, and CanvasLayer opacity, and Control `clip_contents` ancestors are
applied in Canvas space. A broad bounding box around sparse corner art, or a
fully transparent/modulated layer, is not meaningful-coverage evidence.
CanvasGroup, material/shader, and unsupported generic `clip_children` effects
cannot be reconstructed faithfully from source alpha; their explicit count
makes the row `COVERAGE_GAP` until flattened evidence supports them.
The same applies to a divergent SubViewport/CanvasLayer custom viewport, a
`visibility_layer` excluded by the audited viewport's `canvas_cull_mask`, a
visible CanvasModulate or enabled Canvas light, y-sort/show-behind ordering, or a contributing visual
whose effective draw order differs from its tagged layer root.

Runtime Canvas rows also carry current probe/auditor/canonical game-wide 2D
taxonomy/spec/main-scene/project/main/player
and zone-builder hashes, a project-wide sorted path-and-byte-hash manifest of
runtime `.gd`/`.cs`/native-extension declarations, `.tscn`, `.tres`,
`.gdshader`, and runtime `.json` candidates (including Git-ignored/custom-root
files),
the current source revision, a nonce-derived per-run identity, and the exact
current clean whole Git worktree, HEAD, and tree. Whole-worktree cleanliness
prevents ordinary untracked changes from passing, while the project-wide
manifest independently invalidates an ignored autoload/helper under a custom
root. Those bindings are necessary stale-source checks, but
renewable hashes are not authorship. PASS additionally requires the private
same-process capability produced by a new random challenge. The audit snapshots
all challenged capture bytes, consumes and removes the temporary files, and
does not expose any command-line option for loading that capability. A saved
or replayed bundle therefore stays `COVERAGE_GAP`, even after someone renews
its JSON hashes against a later clean commit. Merely mentioning `Node2D` or
`CanvasItem` in a never-called source branch cannot pass
`layering.engine_layer_api`; the current bound probe must have observed the
tagged instances. The check rejects duplicate IDs,
shared source pixels, duplicate runtime
instances/signatures, uninstantiated declarations, extra undeclared layers,
asset mismatches, layers covering less than 50% of the viewport, insufficient
camera travel, less than 8px differential motion, and equal/insufficient draw
order. Missing or stale runtime capture is `COVERAGE_GAP`. Reachable source
classification imports the exact hash-bound `tools/audit_game_2d.py` canonical
Godot 4.7.1 taxonomy instead of maintaining a weaker visual-only class list.
Zone-transitive reachability follows direct loads, global `class_name`
dependencies, project autoload/main-scene bindings, scene transitions, and
current main/player sources. Resolved model loads and canonical spatial
classes/resources are hard structural failures. An unresolved dynamic call,
UID/user/absolute path, or opaque `.scn`/`.res`/`.mesh`/pack/archive is
`COVERAGE_GAP`, never Canvas proof. `SideScrollStage` is also rejected, even if
it has a Canvas-looking branch or happens to contain a `layers`
dictionary or assets named L0/L1. Low-level `RenderingServer`
scenario/instance/mesh/camera/environment/light and
related spatial RID families are also hard debt. Direct, aliased,
`Engine.get_singleton`, `Callable`, and resolved dynamic method forms share the
same classification; an escaped/unresolved server receiver or method gaps,
while explicit `canvas*` APIs and renderer observations remain clean controls.
Likewise, a bound, Callable, aliased, or escaped `ResourceLoader`/resource-pack
capability gaps instead of silently cutting off the dependency walk. Active
non-GDScript/native script dependencies are unsupported executable coverage,
not Canvas proof. Sky Lagoon
intentionally remains failing: it currently declares the one panorama it
actually has and still uses legacy
3D staging. A second declaration cannot close the finding until both distinct
Canvas layers are instantiated and measured.

### Canvas depth, occlusion, and touch evidence are live facts

Canvas hierarchy is established from observed Canvas draw order, not from
legacy spatial constants. `layering.depth_spread` consumes the current,
provenance-bound Canvas layer rows and requires distinct live draw-order values.
`layering.occlusion_band` consumes samples whose method is exactly
`live_canvas_alpha_overlap_samples_v2`: each sample binds the target and
occluder Canvas instance paths and measures alpha-weighted overlap on a 4px
screen grid after inverse-transforming samples into each Sprite2D/TextureRect's
decoded source alpha, applying the same effective opacity and Control clipping
chain as coverage. Rectangle intersections have no evidentiary value, so a
transparent hole around a target records zero overlap. A material, CanvasGroup,
or unsupported clipping effect makes the sample a `COVERAGE_GAP`; it is never
assumed painted. Contributing target and layer visuals must share the recorded
effective Canvas order; a tagged root z value cannot stand in for absolute-z
children. Overlap counts only where both effective alphas are at least 0.50,
across at least four 4px samples, and must cover at least 5% of the target's
painted sample area. One 1/255 pixel cannot certify occlusion. Each sample also records
that the target was actually observed behind and in front at the intended
interaction positions. Missing, stale, non-Canvas,
or unobserved samples are a `COVERAGE_GAP` or `FAIL`; source constants such as
`*_Z`, `HALF_D`, and `BAND_H` have no evidentiary value.

Runtime touch diameters use the same evidence contract. A numeric `screen_px`
value cannot pass by itself: the zone block must match the exact probe run,
root instance, current zone-builder hash, complete dependency manifest, source
revision, clean Git HEAD, engine/renderer, capture context, and current private
one-use challenge response. Changed source, copied facts, or a saved response
therefore become `COVERAGE_GAP`, not a stale pass.
The probe accepts only the still-live node from the actual promenade interaction
registry; a lingering highlight is never a hit-target fallback. `screen_px`
must equal `hit_diameter_px`, `meets_min_touch` must agree with the 110px
threshold, and visible Canvas art must measure at least 64×64px in the audited
root viewport. The registry radius is not trusted as the actual hit size: the
probe calls the production promenade resolver at the live node centre and at
all eight cardinal/diagonal points 55px away. Every point must remain inside
the root viewport and resolve to that same target, while the centre must lie
inside or near its decoded source-alpha-painted art. A centre-only hit cannot
claim a 110px diameter. Contradictory facts are a gap; genuinely undersized hit
or visual targets remain blocking review risks.

### Palette triage versus gameplay readability

`palette.background_recessive` and `palette.figure_ground_luminance` average
separate source files. That is useful risk triage, but it mixes mutually
exclusive frames and transparent decoration, ignores local placement, and can
never emit a hard gameplay `ERROR`. A risky source average is
`WARN/REVIEW_OPEN` while authoritative evidence is absent or failing; a quiet
average is not a substitute for rendered evidence. When every required current
rendered sample passes, that authoritative result automatically supersedes the
static heuristic to nonblocking `INFO/PASS`, so strict mode never demands an
art recolour merely to appease a source-average proxy.

`palette.rendered_composite_readability` is the hard gate. Every required state
must provide all of the following:

- a response created inside the current audit invocation to its unpredictable
  one-use challenge; saved/manual facts can inform diagnostics but cannot pass;
- a real flattened viewport PNG whose bytes match `capture_sha256`;
- exactly 1280×720 `canvas_items/expand` pixels rendered by Godot
  4.7.1-stable's Mobile renderer;
- exact hashes for the probe harness, PASS-producing auditor, canonical 2D
  taxonomy, visual spec, main scene, project settings, main/player scripts,
  every declared builder, and mural/foreground source,
  plus the complete `.gd`/`.tscn`/`.tres`/`.gdshader`/runtime-JSON dependency
  manifest, current clean whole Git worktree/HEAD/tree/source revision, and
  derived per-run identity,
  so any code, resource, shader, runtime-data, capture-configuration, or art
  change invalidates stale evidence;
- for each required target, hash-bound captures from one frozen scene with only
  its exact registered, visible Canvas visual instance paths hidden. The probe
  alternates visible and hidden states on the asymmetric `1,2,1,3,2,1` frame
  schedule and records two additional captures in each state; every visible
  capture must equal the baseline byte for byte and every hidden capture must
  equal the first hidden result byte for byte; and
- a full-viewport target mask whose pixels exactly equal the RGBA difference
  between the visible and target-hidden composites. The sample also records
target/visual instance paths, types, texture paths and hashes, Canvas
transforms, Sprite2D region/frame/flip data, and TextureRect stretch/crop
data. Within each state, required target IDs must own unique, non-overlapping
live target paths and disjoint visual-instance paths; one registered card cannot
satisfy several declared targets.

Python recomputes the mask from both captures byte for byte; it never trusts a
mask merely because its own hash and bounding box are self-consistent. It also
independently reloads every current source texture and inverse-projects its
source alpha through the recorded live Canvas transform. Instance paths must
be rooted beneath the captured zone/root and visual paths beneath their target;
transforms must be finite, invertible, and on-screen; boolean fields must be
actual booleans; frame coordinates, frame grids, regions, modes, and source
bounds must be integral and valid. The projection handles Sprite2D
hframes/regions/flips/centering/offset, rotation and nonuniform scale, and
TextureRect stretch, keep-aspect, cover/crop, tiling, flips, and clipping.

The exact visible-minus-hidden mask must agree with that independent
source-alpha silhouette: projected precision is at least the
`rendered_projection_precision_min` budget (0.90), and at least the
`rendered_projection_visible_fraction_min` share of projected source pixels
(0.35) must be visibly attributable to the target after occlusion. The visible
difference must also retain at least 0.20 precision and 0.20 recall against the
projected silhouette's real contour. This permits truthful partial occlusion
while rejecting a high-contrast interior rectangle that never shows the
target's identifying edge. A forged
self-consistent visible/hidden/mask triple, arbitrary `/root/Forged` path,
singular/off-screen transform, impossible frame/region, non-boolean flip, or
unrelated changed patch therefore remains `COVERAGE_GAP`. A hidden or fully
occluded visual changes no pixels and also remains a gap.

The asymmetric temporal sequence makes causality stable across time. Shader
`TIME`, particles, or any other periodic/two-frame drift cannot become target
pixels merely because visible and restored endpoints happen to match: both
the visible class and hidden class must remain byte-identical at their distinct
cadences before the difference is accepted.

The tool measures only pixels inside the resulting irregular target mask, background
pixels in an annulus outside that mask, and the mask's true inner/outer edge.
A bounding rectangle alone is a `COVERAGE_GAP`: transparent corners can make
rectangle averages lie. A sample passes if value separation, perceptual colour
distance, **or** outline/boundary contrast clears its threshold. It hard-fails
only when all approved separation channels fail in the same current,
state-local sample. Missing masks/channels, fake hashes, a dirty/mismatched Git
revision, stale dependency manifest/source revision/run identity, stale
harness/spec/scene/project/main/player/builder/shader/runtime-data/art,
malformed metadata or projection, temporal drift, or an unreadable capture
remain `COVERAGE_GAP`, never a fabricated pass or hard failure.

This contract does not claim that renewable file hashes cryptographically prove
Godot authorship. Its trust boundary is the configured Godot executable plus
the current clean, hash-bound probe source. The one-use challenge prevents an
old or hand-authored saved bundle from crossing that boundary: the CLI passes
the challenge only to the process it launches, accepts no stored attestation,
copies every returned capture into immutable memory, then removes the private
temporary directory. A missing executable, failed process, wrong echo, wrong
engine/renderer/source contract, escaped output path, or replay falls back to
diagnostic `COVERAGE_GAP`; the CLI never falls back to saved PASS facts.

A required state must name a real `capture_adapter`. Adapter-shaped strings are
not implementation: the verifier uses a closed zone/state dispatch and the
probe must execute its matching transition/assertions immediately before the
capture. The returned asserted-state object and signature must match that
dispatch, and two required states may not reuse one live-state signature or
flattened capture. The current generator has an adapter for Sky Lagoon's
entered and asserted promenade state only; it additionally requires no active
minigame, focus, playground animation, intro, pause, or disabled world controls
before it may label that capture `promenade_idle`. Fairy intro and boss
are both declared `not_implemented` with explicit reasons, so each remains an
honest adapter `COVERAGE_GAP`; running the current probe cannot pretend to
complete either state. Even a complete readable capture cannot suppress a
static palette risk unless current runtime facts also prove pure Canvas staging.

### Add a check — Python + a stress case

```python
@check("layering.foreground_sparse", "layering", "layering_rule",
       presentations=PARALLAX_PRESENTATIONS)
def _fore_sparse(zone: Zone):
    """L4 foreground vignettes stay under 15% painted pixels."""
    fore = [r for r in zone.murals if "_L4_" in r]
    if not fore:
        yield Finding("layering.foreground_sparse", zone.id, SKIP,
                      "zone declares no L4 layer")
        return
    for rel in fore:
        cov = zone.repo.image(rel)["coverage"]
        if cov > 0.15:
            yield Finding("layering.foreground_sparse", zone.id, ERROR,
                          f"{rel} paints {cov:.0%} — an L4 vignette must be "
                          f"sparse or it occludes Roshan and the tap targets",
                          evidence={"file": rel, "coverage": cov})
```

Then add one row to `STRESS_CASES`:

```python
("layering.foreground_sparse", {"murals": 1, "mural_layer_names": ("L4",)}, ERROR),
```

`--stress` now builds a fixture with a dense L4 and asserts your check fires,
then builds a clean fixture and asserts it stays quiet. Forget the row and the
stress run prints `STRESS GAP` and exits 1.

**Available to a check:** `zone.murals / standees / characters / foreground /
runtime_art` (resolved paths), `zone.budget(name, default)`,
`zone.runtime_facts()`, `zone.repo.image(rel)` (w, h, pot, coverage,
saturation, luminance, contrast, has_alpha, rgba_bytes),
`zone.repo.read(rel)`, `zone.repo.const_floats(gd_path)`,
`zone.repo.all_source()`, `zone.repo.license_patterns()`.

### Waive a finding — never silently

```json
"waivers": [
  { "check": "texture.import_sidecar", "zone": "fairy_pond",
    "rule": "texture_max_side_or_pot",
    "scope": "Fairy pond runtime PNG import sidecars",
    "reason": "accepted source-only review build",
    "owner": "project owner",
    "date": "2026-08-09",
    "review_trigger": "next Fairy art revision",
    "residual_risk": "device import settings remain unverified" }
]
```

A valid waiver preserves the original severity, changes only the disposition
to `WAIVED`, embeds the complete waiver in evidence, and stays visible in JSON,
Markdown, and console reports. A missing or mismatched rule, exact scope,
owner, date, review trigger, or residual risk creates an
`audit.waiver_contract` failure. A waiver cannot replace missing automated
coverage or a required human review: `COVERAGE_GAP` and `MANUAL_OPEN` remain
blocking until their evidence exists.

---

## The stress protocol

```
$ python3 tools/audit_visual_design.py --stress
VISUALAUDIT| stress: 18 cases, 18 stressable checks, 24 fuzz rounds
VISUALAUDIT| stress: ALL OK
```

Three things run:

1. **Mutation pass.** For each `STRESS_CASES` row: build a synthetic repo
   (PNGs written with the exact saturation/coverage/size needed, a synthetic
   GDScript builder, declared/runtime Canvas evidence, a clean synthetic Git
   revision and complete dependency manifest, real 1280×720 temporal
   visible/target-hidden PNGs, their exact difference mask, and an independent
   source-alpha projection contract, plus a synthetic ASSET_LICENSES.md and
   ci.sh), run only that check, assert the expected severity appears.
2. **Negative control.** Run the same check against a clean fixture — three
   distinct declared and instantiated Canvas layers with measured coverage and
   differential motion, plus a current flattened composite whose target clears
   at least one separation channel. Anything above `INFO` is reported as
   `STRESS FALSE-POSITIVE`. A check that cries wolf is worse than no check.
3. **Fuzz.** `--fuzz N` (default 24) builds randomised zones — random mural
   counts, colours, legacy/canvas builders, alpha coverage, and incomplete
   declarations — and asserts no check crashes. Crashes surface as
   `FUZZ CRASH seed <n>`, reproducible by seed.

Raise the fuzz count when you touch the `Repo` or `Zone` plumbing:

```bash
python3 tools/audit_visual_design.py --stress --fuzz 500
```

### The self-test suite

`tools/tests/test_audit_visual_design.py` additionally asserts the
contract itself: every check cites a real rule, every check has a docstring,
every stressable check has a case, no case names a removed check, zone ids are
unique, declared builders/probes exist, waivers satisfy their complete
contract, strict blocks every unresolved lifecycle state, no zone/check pair
is silent, no check crashes on the real repository, and reports round-trip.
Focused mutations also prove that filenames/`layers` keys and never-called
Canvas type tokens cannot fake live evidence; duplicate/uninstantiated,
low-coverage, static, or equal-draw-order layers fail; same-value strong-colour
targets pass; low-all-channel targets fail; forged self-hashed triples and
unrelated patches cannot replace a source-alpha-bound visible/hidden
difference; Sprite2D and TextureRect transform/crop families are independently
inverse-projected; non-boolean flags, impossible regions/frames, singular or
off-screen transforms, arbitrary instance roots, periodic temporal drift,
wrong engine/renderer/viewport, unproven touch sizes, dirty/mismatched Git HEAD,
or stale probe/spec/scene/project/main/player/builder/resource/shader/runtime
data/art become `COVERAGE_GAP`. It also proves that plausible clean-Git forged
saved captures, replayed challenges, post-capture committed source with renewed
JSON hashes, escaped output paths, and failed-probe fallback cannot gain PASS
authority, while a fresh CLI-orchestrated challenge is a positive control. The
suite also proves active 3D builder debt
fails across presentation labels and that accepted depth/occlusion uses live
Canvas facts rather than `*_Z`, `HALF_D`, or `BAND_H` constants.

---

## Wiring it into CI

`scripts/ci.sh` hard-gates the unit/stress contract and runs the repository
audit as advisory while current findings and coverage gaps remain open. The
GitHub workflow must preserve the same order when the owner enables the full
gate: unit contract, stress proof, then one same-process `--fresh-runtime`
strict audit. A separately saved runtime-facts step has no gate authority.

Advisory repository run — surfaces findings without claiming satisfaction:

```yaml
      - name: Visual design audit (advisory)
        continue-on-error: true
        run: |
          python3 tools/audit_visual_design.py

      - name: Upload visual design report
        if: always()
        continue-on-error: true
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4.6.2
        with:
          name: visual-design-report
          path: audit/visual_design_report.*
          if-no-files-found: warn
```

Gating is appropriate only after failures, reviews, manual evidence, and
coverage gaps have explicit dispositions. In `probes.yml` and `scripts/ci.sh`:

```bash
python3 -m unittest tools.tests.test_audit_visual_design \
	|| { echo "VISUAL AUDIT CONTRACT FAIL"; exit 1; }
python3 tools/audit_visual_design.py --stress \
	|| { echo "VISUAL AUDIT SELF-TEST FAIL"; exit 1; }
python3 tools/audit_visual_design.py --fresh-runtime --godot "$GODOT" --strict \
	|| { echo "VISUAL DESIGN FAIL"; exit 1; }
```

Run the unit contract and `--stress` before `--strict`, always. A green audit
from a tool whose lifecycle semantics or checks cannot fail is not evidence.

The trusted runtime half belongs in the xvfb visual-review block, not the
headless gate. The audit must launch the probe so its random challenge and
private in-memory attestation stay in one process:

```yaml
      - name: Trusted visual runtime audit
        env:
          LIBGL_ALWAYS_SOFTWARE: 1
          GODOT: godot
        run: timeout 6m xvfb-run -a python3 tools/audit_visual_design.py --fresh-runtime --strict
```

`scripts/probe_visual_audit.gd` is **not** in the trusted probe list: it is a
generator, and it needs a rendered viewport to capture the flattened and
target-hidden frames. For a trusted local audit, let the Python CLI create,
consume, and delete the private output:

```bash
python3 tools/audit_visual_design.py --fresh-runtime --godot "$GODOT" --no-report -v
```

Manual probe output can still be inspected with `--runtime-facts`, which also
relocates `visual_runtime_captures/` beside the selected JSON. That mode is
deliberately non-authoritative and remains `COVERAGE_GAP`. The default saved
path remains `audit/visual_runtime_facts.json` for diagnostics and review.

---

## Current state

Run `python3 tools/audit_visual_design.py -v --no-report` for the exact current
counts. They are intentionally not copied into this hand-maintained guide;
`audit/visual_design_report.json` is the machine-readable snapshot.

The remaining failures, reviews, manual items, and coverage gaps are current
work; none is represented as pass. In particular, every active presentation
is subject to the game-wide Canvas-only builder gate; Sky Lagoon's current
single-panorama 3D implementation remains a structural failure, Fairy is
classified honestly as an explicit failing `legacy_3d_debt` surface with
unimplemented intro/boss capture adapters, and static palette averages are open
review risks rather than fabricated gameplay errors. The high INFO count
includes explicit `NOT_APPLICABLE` rows because every zone/check pair receives
a disposition instead of disappearing behind a presentation filter.

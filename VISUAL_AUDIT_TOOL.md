# The game-wide visual design audit tool

`tools/audit_visual_design.py` turns the current design language's written promises into
checks that fail out loud. It is built to be **expanded and stress-tested by
Codex** — the expansion surface is a JSON file, and the tool refuses to pass
its own stress run if a check has never been proven capable of failing.

The final owner decision on 2026-08-09 makes Mermaid Roshan a 2D-authored
character. Godot may stage flattened art with `Sprite3D`, but the old
3D-migration order and dimensional rollback are not current audit rules.

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
python3 tools/audit_visual_design.py --strict   # complete-evidence gate
python3 tools/audit_visual_design.py --stress   # prove every check can fail
python3 -m unittest tools.tests.test_audit_visual_design
```

Every run writes `audit/visual_design_report.json` (machine-readable, for
Codex) and `audit/visual_design_report.md` (human-readable, for the owner).
`--no-report` suppresses that.

## The two halves

| Half | What it sees | Runs where |
|---|---|---|
| `tools/audit_visual_design.py` | every PNG, every builder constant, ASSET_LICENSES.md, ci.sh | anywhere with Python — **no Godot needed** |
| `scripts/probe_visual_audit.gd` | the assembled scene: real depths, real sprite counts, tap targets projected through the live lens | needs Godot; writes `audit/visual_runtime_facts.json` |

The Python tool ingests the facts file when it exists. Checks that need it
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
  "standees": ["assets/flats/reef/main/standee_reef_*.png"],
  "characters": ["assets/sprites/reef/roshan_*.png"],
  "asset_roots": ["assets/flats/reef", "assets/sprites/reef"],
  "budgets": { "zone_runtime_texture_mb": 18.0 }
}
```

`presentation` decides which checks apply. It describes runtime staging, not
the authored art medium:

| presentation | Gets |
|---|---|
| `panning_depth_cards` | parallax, occlusion, palette, overdraw, texture, release evidence, hygiene |
| `fixed_depth_cards`, `overhead_canvas` | palette, overdraw, standee, texture, release evidence, hygiene; no promenade parallax requirement |
| `free_swim`, `rail`, `canvas`, `ui`, `overlay` | common texture, release-evidence, readability, and hygiene checks; presentation-specific flat checks are explicitly `NOT_APPLICABLE` |

`budgets` on a zone overrides the global `budgets` block for that zone only.

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
VISUALAUDIT| stress: 16 cases, 16 stressable checks, 24 fuzz rounds
VISUALAUDIT| stress: ALL OK
```

Three things run:

1. **Mutation pass.** For each `STRESS_CASES` row: build a synthetic repo
   (PNGs written with the exact saturation/coverage/size needed, a synthetic
   GDScript builder with the exact depth constants, a synthetic
   ASSET_LICENSES.md and ci.sh), run only that check, assert the expected
   severity appears.
2. **Negative control.** Run the same check against a clean fixture — three
   L0/L1/L2 murals, well-separated depths, a saturated foreground on a muted
   background, the `layers` API in use. Anything above `INFO` is reported as
   `STRESS FALSE-POSITIVE`. A check that cries wolf is worse than no check.
3. **Fuzz.** `--fuzz N` (default 24) builds randomised zones — random mural
   counts, colours, depth sets, media, alpha coverage, some with no band, some
   with no depths at all — and asserts no check crashes. Crashes surface as
   `FUZZ CRASH seed <n>`, reproducible by seed.

Raise the fuzz count when you touch the `Repo` or `Zone` plumbing:

```bash
python3 tools/audit_visual_design.py --stress --fuzz 500
```

### The self-test suite

`tools/tests/test_audit_visual_design.py` (26 tests) additionally asserts the
contract itself: every check cites a real rule, every check has a docstring,
every stressable check has a case, no case names a removed check, zone ids are
unique, declared builders/probes exist, waivers satisfy their complete
contract, strict blocks every unresolved lifecycle state, no zone/check pair
is silent, no check crashes on the real repository, and reports round-trip.

---

## Wiring it into CI

`scripts/ci.sh` hard-gates the unit/stress contract and runs the repository
audit as advisory while current findings and coverage gaps remain open. The
GitHub workflow must preserve the same order when the owner enables the full
gate: unit contract, stress proof, runtime-fact capture, then strict audit.

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
python3 tools/audit_visual_design.py --strict \
	|| { echo "VISUAL DESIGN FAIL"; exit 1; }
```

Run the unit contract and `--stress` before `--strict`, always. A green audit
from a tool whose lifecycle semantics or checks cannot fail is not evidence.

The runtime half belongs in the xvfb visual-review block, not the headless
gate:

```yaml
      - name: Capture visual runtime facts
        continue-on-error: true
        env:
          LIBGL_ALWAYS_SOFTWARE: 1
        run: timeout 6m xvfb-run -a godot --rendering-method mobile -s scripts/probe_visual_audit.gd
```

`scripts/probe_visual_audit.gd` is **not** in the trusted probe list: it is a
generator, and it needs a real viewport to project tap targets. It passes the
static gates (`gdtoolkit` parse, `lint_inference`); it has not been run under
a Godot binary, because none is available in this container — the first real
execution will be its first full compile check.

---

## Current state

Run `python3 tools/audit_visual_design.py -v --no-report` for the exact current
counts. They are intentionally not copied into this hand-maintained guide;
`audit/visual_design_report.json` is the machine-readable snapshot.

There are 18 checks (16 stressable) across 7 categories and 12 declared zones. The obsolete dimensional
rollback error and migration-order warning are gone. The remaining failures,
reviews, manual items, and coverage gaps are current work; none is represented
as pass. The high INFO count includes explicit `NOT_APPLICABLE` rows because
every zone/check pair now receives a disposition instead of disappearing
behind a presentation filter.

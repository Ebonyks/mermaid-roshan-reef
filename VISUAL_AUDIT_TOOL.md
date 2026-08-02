# The game-wide visual design audit tool

`tools/audit_visual_design.py` turns the redesign's written promises into
checks that fail out loud. It is built to be **expanded and stress-tested by
Codex** — the expansion surface is a JSON file, and the tool refuses to pass
its own stress run if a check has never been proven capable of failing.

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
python3 tools/audit_visual_design.py --strict   # exit 1 on any ERROR
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
report `SKIP` with a reason when it does not — **a check that cannot run never
reports a pass.** That is the rule that keeps the tool from manufacturing
confidence, and it is the same discipline `probes.yml` applies to
`probe_human_art_audit`.

## Severities

| | Meaning |
|---|---|
| `ERROR` | Violates a written rule in the charter, the work order, or CLAUDE.md. Fails `--strict`. |
| `WARN` | Real cost — perf, APK size, process — but not a rule violation. |
| `MANUAL` | The tool knows it cannot judge this. Names the files a human must look at. |
| `INFO` | The check ran and found nothing wrong. Evidence that it ran. |
| `SKIP` | The check could not run, plus the reason. |

## Design contract

Four rules govern every check. Breaking any of them is how audit tools become
noise that everybody mutes.

1. **Every check names a rule in the spec.** `@check(..., rule="layering_rule")`
   must match a key in `spec["rules"]`, whose value quotes the document it
   comes from. A check with no document behind it is an opinion, and opinions
   do not gate. Enforced by `test_every_check_names_a_rule_in_the_spec`.
2. **Checks are pure.** `(zone, repo, runtime_facts) -> findings`. No check
   writes to the repo.
3. **Silence is never a pass.** Emit `SKIP` with a reason instead of returning
   nothing. Enforced by `test_every_zone_produces_at_least_one_finding`.
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
  "medium": "promenade_2p5d",
  "status": "shipped",
  "charter_order": 1,
  "supersedes": "scripts/reef_districts.gd",
  "reversibility_key": "world_style",
  "builders": ["scripts/promenade.gd"],
  "probes": ["scripts/probe_promenade.gd"],
  "murals":   ["assets/flats/reef/main/flat_reef_main_L*.png"],
  "standees": ["assets/flats/reef/main/standee_reef_*.png"],
  "characters": ["assets/sprites/reef/roshan_*.png"],
  "asset_roots": ["assets/flats/reef", "assets/sprites/reef"],
  "budgets": { "zone_runtime_texture_mb": 18.0 }
}
```

`medium` decides which checks apply:

| medium | Gets |
|---|---|
| `promenade_2p5d` | everything — parallax, occlusion, palette, overdraw, texture, charter, hygiene |
| `staged_2d`, `overhead_2d` | palette, overdraw, standee, texture, charter, hygiene (**no** parallax/occlusion — the charter declares fixed-camera stages compliant) |
| `free_swim_3d`, `rail_3d`, `canvas_2d`, `ui`, `screen_overlay` | texture, charter, hygiene |

`budgets` on a zone overrides the global `budgets` block for that zone only.

### Add a check — Python + a stress case

```python
@check("layering.foreground_sparse", "layering", "layering_rule",
       media=PARALLAX_MEDIA)
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
    "reason": "sidecars land with the batch-2 import pass; owner aware 2026-07-28" }
]
```

A waived finding drops to `INFO` with `[WAIVED: reason]` prepended — it stays
visible in every report. Waivers without a reason fail the test suite. A
silenced finding nobody can see is how a redesign rots.

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

`tools/tests/test_audit_visual_design.py` (14 tests) additionally asserts the
contract itself: every check cites a real rule, every check has a docstring,
every stressable check has a case, no case names a removed check, zone ids are
unique, waivers reference real checks and zones, no check crashes on the real
repository, every zone produces at least one finding, and reports round-trip.

---

## Wiring it into CI

The tool is deliberately **not** wired into `.github/workflows/` — workflow
changes are explicit-task-only under SECURITY.md, and this was not that task.
The additions below are ready to apply when the owner wants them.

Advisory (recommended first — surfaces findings without blocking the APK):

```yaml
      - name: Visual design audit (advisory)
        continue-on-error: true
        run: |
          python3 tools/audit_visual_design.py --stress
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

Gating (once the current `ERROR`s are fixed or waived), in the static-gates
step of `probes.yml` and in `scripts/ci.sh` beside the other `tools/audit_*`
gates:

```bash
python3 tools/audit_visual_design.py --stress \
	|| { echo "VISUAL AUDIT SELF-TEST FAIL"; exit 1; }
python3 tools/audit_visual_design.py --strict \
	|| { echo "VISUAL DESIGN FAIL"; exit 1; }
```

Run `--stress` before `--strict` in CI, always. A green audit from a tool
whose checks cannot fail is the failure mode this whole design exists to
prevent.

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

```
VISUALAUDIT| ERROR=6  WARN=17  MANUAL=2  INFO=23  SKIP=109
```

18 checks across 7 categories, 12 zones. All 6 `ERROR`s and the bulk of the
`WARN`s are the 48-hour findings written up in
`VISUAL_DESIGN_AUDIT_2026-07-28.md`; `--strict` will pass once they are fixed
or explicitly waived.

The 109 `SKIP`s are honest: most are unmigrated 3D zones that declare no flat
art yet, plus `readability.tap_target_size` waiting on runtime facts. As zones
migrate, SKIPs become INFOs — that count is itself a migration progress bar.

# .glb / .blend reachability audit

_2026-08-02. Sixteen-agent sweep: seven zone resolvers, an adversarial verify
stage per zone, a Blender-source auditor, and a completeness critic. Read-only;
all quarantine decisions below were made and executed afterwards, by hand._

## Question asked

Are there Blender items or `.glb` files in the project, and should they be
quarantined?

**Yes to both, and no to most of the quarantining.** 739 `.glb` and 32 `.blend`
exist. 221 `.glb` (97.5 MB) resolve as unreachable — but only 70 of them
(46.6 MB) are genuinely dead. The rest are deliberate fallbacks or
shipped-but-unwired art that one line of code would revive, and moving those
would be a mistake.

## Why a sweep was needed

Only **95 distinct literal `"res://….glb"` strings** exist in the codebase, for
739 files. Everything else loads through a constructed path:

```gdscript
load(LAGOON_KIT_ROOT + name + ".glb")                    // arena/sky_lagoon.gd:205
"res://assets/props/gen2/%s.glb" % name                  // kart.gd:1109
"res://assets/art35/cards/" + fname + ".glb"             // opera_act.gd:1313
"opera_candymaker_candy_%d.glb" % (candies_done % 7)     // opera_act.gd:5081
"res://assets/aquatic2/" + model + ".glb"                // main.gd:1780
```

Resolving reachability meant tracing each construction back to its vocabulary —
`const` arrays, `Dictionary` tables, `%d` loop ranges — and enumerating what
names it can actually produce. Coverage reconciled exactly: **639 files in
`assets/` across 45 directories + 96 already in `decommissioned/` + 4 in
`tools/out` = 739.** No gap, no double-count.

## Coverage

| Zone | `.glb` | Reachable | Unreachable |
| --- | ---: | ---: | ---: |
| art35 | 173 | 79 | 94 |
| zones_misc (13 dirs) | 155 | 130 | 25 |
| castle | 66 | 0 | 66 |
| opera | 65 | 47 | 17 |
| aquatic + aquatic2 + reef_regions | 62 | 50 | 12 |
| sky_lagoon | 61 | 60 | 1 |
| props (gen2, alpine) | 57 | 48 | 9 |
| **total** | **639** | **414** | **224** |

---

## Quarantined (70 files, 46.6 MB)

### `decommissioned/data/castle-3d-kit/` — 66 files, 9.6 MB

The entire castle 3D kit, including all 58 `pearl_kit` models. Its only
consumer was `scripts/arena/castle_hall.gd`, **deleted** in commit `d0732324`
("feat(castle): rebuild storybook hub in 2.5D"). The replacement,
`scripts/arena/castle_rooms_25d.gd`, contains **zero** `.glb` references — it
loads 2D cutouts from `res://assets/castle/dirty_cleanup_2d/` instead.

This satisfies CLAUDE.md's condition exactly: landed `.glb`s stay *until their
zone migrates*, and the castle has migrated. These 66 files were still shipping
in the APK with nothing able to load them.

Pre-move safety checks, all clean:
- No non-probe reference to any `assets/castle/*.glb` anywhere in
  `scripts/`, `scenes/`, `tools/`, `project.godot`.
- **No CI probe loads one.** `probe_castle_pearl_art`, `probe_kitchen_props`,
  `probe_bathroom_props`, `probe_bathroom_integration`, `probe_crown` and
  `probe_fable_kit` are all in the `scripts/ci.sh` trusted list and all have
  zero castle `.glb` references — they exercise the 2D rebuild.
- The `PEARL` hits in `probe_audit` / `probe_l2` / `probe_train` are
  `PEARL_TOTAL` / `pearl_count` game state, not `pearl_kit` assets.
- `const PEARL_KIT` does not exist in any live script; it died with
  `castle_hall.gd`.

`.glb.import` sidecars moved with their models.

### `decommissioned/data/rig-workbench-glb/` — 4 files, 37 MB

`birdie_rigged_full.glb`, `birdie_rigsrc.glb`, `craft_kitty_rigged_full.glb`,
`kitty_rigsrc.glb`. Git-tracked rig intermediates in `tools/out` with **zero
references anywhere** — not even from the build scripts that produced them.
No zone owned them; the critic caught them. They never shipped
(`tools/.gdignore` + `exclude_filter="tools/*"`), so this is pure repo weight —
but at 37 MB it is the largest single dead block in the sweep.

---

## Deliberately NOT quarantined

### `assets/aquatic2/` (11 files, 60.7 MB) — documented fallback, owner call

Every one of the 11 filenames is a `CREATURE_GEN2` key, and `_place_aq`
(`main.gd:1821`) tries `props/gen2` first, reaching `_aq()` only if
`_gen2_creature` returns null. All 12 gen2 creature models exist, so today
nothing gets there. Technically unreachable — but the code says why:

> `# rigged + textured gen2 rebuilds take priority; Riley pack is the fallback`
> `# the pack GLB remains the strangler-fig fallback if a file is ever missing`

This is an intentional three-tier safety net (`props/gen2` → `aquatic2` →
`aquatic`), not dead art. It is also the single largest reducible block in the
shipped game. **Removing it is an owner decision about whether the fallback
still earns 60.7 MB of APK**, not a cleanup call, so nothing was touched.

Note the sweep's own reasoning here was wrong before the critic fixed it: the
aquatic zone claimed `_aq()` had a single call site, but `slide_race.gd:181`
calls `m._aq(model)` through `_aq_game()` with a *different* gate (no `AQ_GEN2`
check). The conclusion survived — `_aq_game`'s three call sites all pass
`CREATURE_GEN2` keys — but on evidence the original report did not have.

### art35 (94), opera (17), zones_misc (25), props (9), sky_lagoon (1)

Left in place pending review. These are mostly the "shipped but never wired"
pattern — art built by `tools/build_*.py` and exported, but whose
`_lobby_prop(…)` / `_act_prop(…)` call was never added. `opera_crate.glb`,
`opera_crate_lid.glb` and `opera_tiara_chest.glb` are the clearest example:
named by nothing but their producer (`tools/build_opera_house_art.py:431/435/451`),
and revived by a single line. Several art35 card files sit in a documented
"runtime pool". Unlike the castle, no loader was deleted here — so absence of a
call site is likelier to mean unfinished than dead. Worth a pass, but it is
~27 MB across four zones and each needs a per-file judgement the owner should
make.

`assets/art35/kart/soft_barrier.glb` stays regardless: `kart.gd:164` documents
it as deliberately shipped-but-unwired, and kart is owner-protected.

---

## Blender sources — 32 files, nothing shipped

28 `.blend` under `assets_src/blender`, 4 under `tools/out`. Both trees carry a
`.gdignore`, and `export_presets.cfg` excludes `assets_src/*` and `tools/*`, so
**no `.blend` byte has ever reached the APK.** `.blend1` autosaves are
gitignored (`*.blend1`).

These are the only editable source for art that may need re-exporting, and the
2.5D redesign is explicitly reversible — so they were left alone. They cost the
phone nothing.

---

## Two live defects found (neither fixed here)

### 1. `opera_rival_nursery.glb` is referenced but does not exist

`opera_act.gd:2619` builds `"res://assets/opera/rivals/opera_rival_%s.glb" % costume`,
and `opera_house.gd:108` defines a 13th act with `"costume": "nursery"`. Disk
has 12 rivals. `opera_act.gd:2636` guards with `ResourceLoader.exists` and falls
back to a generic imp — so the Nursery act silently shows an imp instead of a
nurse rival. Not a crash; missing art. The opera zone counted 12 costumes and
missed the 13th.

### 2. Rebuilding art35 will turn the probe suite red

`tools/build_art_pass35.py:1195-1201` still registers and exports seven fairy
models into `assets/art35/arena/`:

```python
register("fairy_lily_cluster", …, "assets/art35/arena/fairy_lily_cluster.glb")
register("fairy_flower_gate",  …, "assets/art35/arena/fairy_flower_gate.glb")
for variant in range(2):
    register(f"fairy_bank_{variant}", …, f"assets/art35/arena/fairy_bank_{variant}.glb")
```

But `scripts/probe_fairy_art.gd:24-41` holds those exact paths in
`const RETIRED_MODELS` and **fails if the file exists** (`:78-81`) — a negative
assertion, and `probe_fairy_art` is in the `ci.sh` trusted list.
`tools/audit_fairy_art_v2.py` enforces the same rule in `probes.yml`. So anyone
re-running the art35 build resurrects exactly the files CI forbids.

Fairy is owner-protected, so I have not touched the builder. Flagging it: the
fix is to delete those `register(...)` lines, and it is the one finding here
that is actionable today.

The art35 zone agent read this backwards, reporting the seven paths as "stale
references, informational, no action". They are CI-enforced *absences*. Same for
`res://assets/characters/fairy.glb` and `fairy_v2.glb` at `probe_fairy_art.gd:96-101`.

---

## Verified clean

- **The earlier decommission introduced no broken references.** Grepping every
  `.gd`/`.tscn`/`.tres`/`.cfg`/`.godot`/`.py`/`.yml` outside the wing for
  `decommissioned` returns exactly two lines — the two `exclude_filter`
  entries. No live script points into the moved `gen2/` tree.
- 0 orphan `.glb.import` sidecars; 0 `.tscn`/`.tres` references any `.glb`.
- No runtime JSON vocabulary: no `.json` under `assets/` or `audit/` names a
  `.glb`, so there is no hidden data-driven loader.
- Guarded forward-hooks into PNG-only dirs are intentional and were left alone:
  `melody.gd:253` and `main.gd:2332` probe for
  `assets/characters/friends/*.glb` behind `ResourceLoader.exists`, falling
  back to the cutouts. This is *why* that directory contains no `.glb`.

## Reproducing

The zone reports, per-file verdicts and critic transcript are in the workflow
journal:
`.claude/projects/…/subagents/workflows/wf_9fd0a85a-628/journal.jsonl`.

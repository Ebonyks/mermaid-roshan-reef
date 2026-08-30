# Mermaid Roshan: Reef of Light — master audit, 2026-08-26 code-refinement round

- **Round ID:** `MA-2026-08-26`
- **Audited integration head:** `9a1754c1b1987dd2b9745fea8d8048f65f6d1ce2`
  (`origin/dev`, 2026-08-25) — 169 commits past the canonical audit's sealed
  evidence head `441adf35`
- **Round focus:** owner-directed comprehensive game analysis with the goal of
  refining the game **code**; criteria update; goal set; implementation
  handoff to Codex
- **Document authority:** `SUPPORTING_CURRENT` — the canonical audit ledger
  remains `MASTER_AUDIT_2026-08-09.md`, which carries this round's normative
  deltas in its sections 5, 12, 13, and 14; the citable rules live in
  `../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` section 18
  (`DL-CODE-01`–`DL-CODE-10`)
- **Findings register:** twelve new canonical records appended to
  `findings/ACTIVE_FINDINGS_2026-08-13.md`; three existing records
  (`MA-CODE-001`, `MA-CODE-002`, `MA-OPERA-012`) history-appended
- **Implementation handoff:**
  `../CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md`
- **Method and honesty bound:** static analysis, exact counts, workflow and
  probe reads, and git history at the audited head, produced in a remote
  container with no Godot binary and no target device. Every claim in this
  round is verification level V1 unless it cites an existing sealed record.
  Nothing here is device, child, owner, capture, or runtime evidence, and no
  existing sealed claim is altered.

---

## 1. Executive verdict

The game's content grew faster than its structure for a third straight cycle,
and this round names that as the current binding constraint on everything
else. Since the canonical audit's sealed head, dev landed a five-system burst
— the Canvas Melody rebuild, Castle Canvas2D baseline rooms, the entire Day
One fresh-save wing with start-menu routing, the Harper/Fiona slide canvas, a
game-wide audio remediation, and the owner's own true-2D three-floor Opera
House venue — while `scripts/main.gd` grew from 8,734 to **10,499 lines**
against a standing target below 2,500, and the dismantled `opera_act.gd` god
object (7,192 → 189 lines) re-accreted as `opera_gesture_surface.gd`
(**6,185 lines**). The mass moved; it did not dissolve.

The safety architecture, by contrast, held: the no-fail sweep found the
invariants intact in every new system, Day One state is properly serialized,
the opera neutral-exit leak recorded on the old master branch is already
fixed on dev, and the `probe_opera_pipe` CI hole is closed in both rosters.
The three most exposed edges today are the **gate**, not the game: the Day
One wing — the New Game path — has eight probes and none of them run in a
trusted roster (`MA-CI-004`); the central zero-input negative test cannot see
any reward surface newer than medals (`MA-CI-005`); and promotion accepts any
green run for a SHA rather than the newest (`MA-CI-006`).

**Binding constraint: `MA-CODE-001`.** At +1,765 coordinator lines in
thirteen days, every future wing — Chapter 2 explicitly plans to hook story
beats into these same files — pays compounding regression risk. The goal set
below therefore hardens the safety net first, then reverses the structural
trend mechanically, under the new `DL-CODE-*` criteria.

The audit program state is unchanged by this round: `IN_PROGRESS` /
`UNSATISFIED`, `REPAIRING` with concurrent focused `VERIFYING`.

---

## 2. What changed since the sealed evidence head

Groups, earliest → latest commit at `origin/dev`:

| Group | Content | Commits |
|---|---|---|
| Sky Lagoon true-Canvas completion and hardening | capture audit fail-closed, geography card locks, z-band binding, framing/contact repairs | `7391c53c` → `e9511e4f` |
| Melody rebuild | seven-note theater rebuilt as a Canvas rhythm stage with suspension-safe input; trusted `probe_melody` rebuilt with it | `4e692e91`, `7ef225f7` |
| Castle Canvas2D baseline | baseline rooms polished in Canvas2D, child navigation/room transitions hardened, redundant hall depth cards retired, chandelier placement preserved | `63f76d65` → `9e6616fb`, `b6e3d6b1`, `1680d45e` |
| Day One wing | dirty-pool rescue, art-studio attack customizer, pool cleanup games, start-menu New Game routing into Day One, Rumi identity fixes, canvas-only pool probes | `ea97da2f` → `d127db8c`, `7b6155d9`, `118492ab` |
| Harper/Fiona slide canvas | new canvas activity | `847537ca` |
| Audio remediation | game-wide sound-quality audit and repair | `ddf85a94`, `b17ed906` |
| Owner Opera House venue | true-2D three-floor venue as the Opera Hall room interior; portal decorations then removed | `0277071f`, `9a1754c1` |

The owner venue commits are recognized in the canonical audit's section 3.2
as the newest Opera navigation direction. Read against `MA-OPERA-012`: the
venue hosts only the Opera Hall room's three resident careers through
invisible painted portal regions over an accepted master painting — no card
grid, no all-career menu — so the no-central-lobby ruling is **preserved**,
not reversed.

None of these 169 commits carries updated canonical-audit bookkeeping; that
staleness is what this round repairs, and the repair path is recorded in the
canonical section 14.

## 3. Standing metrics at `9a1754c1`

Prior columns: the 2026-07-15 `AUDIT_UPGRADE.md` evidence table and the last
canonical measurements (2026-08-13 lineage, where one exists).

| Metric | 2026-07-15 | 2026-08-13 lineage | `9a1754c1` |
|---|---|---|---|
| `scripts/main.gd` lines | 8,239 | 8,734 (`51d0abc0`) | **10,499** |
| `main.gd` functions | — | — | 480 |
| Largest non-main script | `kart.gd` 2,950 | — | `opera_gesture_surface.gd` **6,185** |
| Next largest | — | — | `castle_rooms_25d.gd` 4,764; `kart.gd` 3,415; `opera_career_world_2d.gd` 3,433; `sky_lagoon.gd` 3,038 |
| `scripts/` non-probe lines | ~27,869 total repo | — | 78,689 |
| Probe scripts / lines | 49 | 96–110 on disk | **117** / 39,871 |
| Trusted roster (local/remote) | 19 | 64 / 63 | 64 / 63 (unchanged; `probe_opera_pipe` in both) |
| `.new(` in `main.gd` | 497 | — | 337 |
| `g[` accesses in `main.gd` | 140 | — | 82 |
| Distinct `g["…"]` keys repo-wide | — | 380 (at `e924d9ba`) | **409** |
| Probes defining private `_frames(` | — | — | 38 |
| Verbatim `▼` pointer blocks | — | 4 (at `e924d9ba`) | **8** |
| Authored `.tscn` scenes | 1 | 1 | 1 |
| Day One probes in trusted rosters | — | — | **0 of 8** |

Reading: the two metrics that measure *discipline* (`.new(` and `g[` on
main) kept improving even while the two that measure *load-bearing
structure* (coordinator size, second-largest file) regressed sharply. The
codebase is getting cleaner per line and heavier per owner — which is
exactly the profile of extraction debt, not of sloppiness. The typed-var
discipline remains complete (zero untyped declarations found on the prior
head's full sweep), and per-frame allocation is rare outside the named
findings. The foundation is good; the load path is wrong.

## 4. Scorecard movement

Only dimensions with material movement are re-scored; all others carry the
canonical audit's scores unchanged. Ratings use the canonical section 1.1
scale.

| System | Canonical | This round | Why |
|---|---|---|---|
| Child safety and no-fail behavior | 4/5 | 4/5 → | Held under five new systems: no-fail comments backed by code in every new mode, Day One serialized, opera neutral-exit repaired on dev. Residuals are bounded: dead loss-message code (`MA-CODE-005`), scratch-owned castle progress (`MA-SAVE-001`). |
| QA and release automation | 4/5 | **3/5 ↓** | The roster grew, but the fresh-save entry wing ships ungated (`MA-CI-004`), the central negative test is blind to every new reward surface (`MA-CI-005`), promotion accepts any green run (`MA-CI-006`), and harness duplication is the suite's dominant flake class (`MA-CI-007`). The gate's paper strength exceeds its real reach. |
| Architecture and maintainability | 2/5 | **2/5 →, worsening trend** | Coordinator +1,765 lines in thirteen days; god-object mass relocated to `opera_gesture_surface.gd`; clone families grew (pointer blocks 4 → 8); string-key surface 380 → 409. The score holds at 2 only because satellites, typing, and allocation discipline are genuinely good. |
| Performance and device fitness | 2/5 | 2/5 → | Same evidence gap as canonical (no device measurements); code-side risks now enumerated concretely (`MA-PERF-002`, `MA-PERF-003`) so the next device session has a target list. |
| Voice, music, and sound | 3/5 | 3/5 → | The audio remediation landed after the sealed head and is unaudited beyond machine gates; the Mic-bus layout gap remains (`MA-AUDIO-002`). Human listening gates unchanged. |
| Touch and non-reader access | 3/5 | 3/5 → | The 2026-08-03 audit's named repairs verified present; one residual unguarded path remains (`MA-TOUCH-002`). |

## 5. Findings opened, updated, and verified-moot this round

All records live in `findings/ACTIVE_FINDINGS_2026-08-13.md`; the compact
index is canonical section 5. Everything below is V1 static evidence at
`9a1754c1`.

Opened (twelve):

| Finding | Severity | One line |
|---|---|---|
| [`MA-CI-004`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-004) | P1 | Day One / start-menu wing: eight probes, zero gated |
| [`MA-CI-005`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-005) | P1 | Passive snapshot blind to all post-medal reward surfaces |
| [`MA-CODE-003`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-code-003) | P2 | Eight verbatim clone families |
| [`MA-CODE-004`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-code-004) | P2 | 409 distinct string state keys, growing |
| [`MA-CODE-005`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-code-005) | P3 | Wired-but-dead loss-message system |
| [`MA-PERF-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-perf-002) | P2 | `_sparkle_burst` allocates node+mesh+material per call, 141 sites, no tier gate |
| [`MA-PERF-003`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-perf-003) | P2 | Newest surfaces have zero quality-tier awareness |
| [`MA-SAVE-001`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-save-001) | P2 | Castle interaction progress lives in unpersisted scratch |
| [`MA-AUDIO-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-audio-002) | P2 | Mic bus absent from the bus layout |
| [`MA-TOUCH-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-touch-002) | P2 | Swim branch reads emulated mouse without the reserved-zone guard |
| [`MA-CI-006`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-006) | P2 | Promotion accepts any green run; roster not pinned |
| [`MA-CI-007`](findings/ACTIVE_FINDINGS_2026-08-13.md#ma-ci-007) | P2 | Probe harness copy-paste and wall-clock cadence |

Updated: `MA-CODE-001` (re-measured 10,499; trend reversed; named binding
constraint), `MA-CODE-002` (re-measured; five bounded sub-findings carved
out per its own fix plan), `MA-OPERA-012` (owner venue recognized,
premise-consistent).

Checked and **not** opened, with why:

- The opera neutral-exit leak and the missing `m.game = "kart"` handover
  from the 2026-08-05 release gate: repaired on dev
  (`pause_menu.gd` now has a dedicated opera branch; the venue/kart path was
  rebuilt in the Canvas Racer line).
- `probe_opera_pipe` absent from remote CI: present in both rosters at
  `9a1754c1`.
- Day One persistence: correctly serialized through
  `day_one_director.serialize_state()` into the save round-trip.
- Stale line-count claims in `design/03`: repaired by the 2026-08-09
  reconciliation; no current stale-claim hit found.
- The restored Opera House venue as a possible ruling reversal: verified
  premise-consistent (see section 2).

## 6. The goal set — G1 through G12

Every goal traces to findings, has a gate for its definition of done, and is
sized to one branch. "Suite green" means the full trusted local suite plus a
green remote probes run at the branch head, per the canonical section 9
protocol. No goal may weaken a child-rule invariant, and every refactor goal
is behavior-preserving under `DL-CODE-06` (probe fails → revert, never patch
the probe).

**Stage A — harden the net (do these first).**

| Goal | Trace | Definition of done |
|---|---|---|
| G1. Gate the Day One wing | `MA-CI-004` | The deterministic Day One / start-menu probes run in BOTH trusted rosters; an intentionally broken New Game route turns CI red in a demonstration branch; suite wall time stays inside the workflow ceiling |
| G2. Extend the passive negative test | `MA-CI-005` | `_progress_snapshot()` covers every save-backed reward surface; a hand-award mutation of each section fails the probe; documented rule: new modes extend the snapshot or carry an idle no-award leg |
| G3. Pin the promotion gate | `MA-CI-006` | `promote.yml` selects the newest completed run (push preferred) and fails on red; executed-roster count compared against a committed expected count; dry-run demonstrated |
| G4. Declare the Mic bus | `MA-AUDIO-002` | `default_bus_layout.tres` declares a muted Mic bus; `probe_audio` asserts it; runtime rename becomes a defensive assertion |
| G5. Guard the swim pointer path | `MA-TOUCH-002` | Swim branch honors `reserved_zone_hit()`; a touch-stress leg proves a held medallion no longer steers; remaining emulated-mouse reads audited as router-owned |
| G6. Persist castle interaction progress | `MA-SAVE-001` | Partial castle interaction state survives app kill via append-only keys with defaults; save probes cover the new keys |

**Stage B — spend the safety margin on structure.**

Owner direction (2026-08-26, after this round's first publication): shrink
goals alone are treatment, not cure — the architecture itself must change so
continued expansion no longer grows `main.gd`. That remodel is specified in
`../design/08_TARGET_ARCHITECTURE.md` (the Mode Platform: growth law
`DL-CODE-11`, GameMode/registry/director/services contracts, the CI
structure ratchet `DL-CODE-12`, migration plan M0–M6). **The structural
goals below execute through that plan**: G7 lands as migration step M6, G10
as M5, and G11's pooling half as M4's FxService; the handoff's Stage C
packages (WP-C0–C6) carry the step-by-step boundaries. G8, G9, G12 and
G11's tier-note half remain independent cleanups sequenced behind the
platform spine.

| Goal | Trace | Definition of done |
|---|---|---|
| G7. Reverse the coordinator regression | `MA-CODE-001` | Day One glue, venue delegation, and start-menu routing extracted from `main.gd` into their owning satellites/controllers mechanically; `main.gd` at or below 9,000 lines this round with each extraction suite-green; trajectory re-measured in the next round |
| G8. Decompose the gesture surface | `MA-CODE-001`, `MA-CODE-002` | `opera_gesture_surface.gd` split along its per-career/per-widget seams into modules at or below 3,000 lines each behind an unchanged dispatcher API; zero behavior delta under the opera probes |
| G9. Consolidate the clone families | `MA-CODE-003` | One shared implementation each for: action-press read, pointer glyph, cached material factory, AABB kit, avatar spawn, stage input map, mode start/end scaffold, act teardown list — one family per commit, suite green each step |
| G10. Freeze and shrink string state | `MA-CODE-004` | Distinct `g` key count at or below 409, recorded in the round metrics; two high-traffic modes migrated to typed accessors |
| G11. Pool the burst effects and tier the newest surfaces | `MA-PERF-002`, `MA-PERF-003` | `_sparkle_burst` pooled with cached mesh/materials and a Speedy reduction; each named tier-blind surface gains a Speedy path or a recorded budget note |
| G12. Remove safety-adjacent dead code and unify the probe harness | `MA-CODE-005`, `MA-CI-007` | `_fail_line` and the dead lose branch deleted; a shared probe harness exists and the top twenty trusted probes use it with no assertion weakened |

Stage A first is deliberate: G1–G3 make every Stage B refactor safer to
verify, and G4–G6 are small, child-facing, and independent. Inside Stage B,
G7 and G8 are the budget-setters; G9–G12 can interleave behind them.

## 7. Orchestration — how the handoff runs

Implementation belongs to Codex under
`../CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md`, which maps
G1–G12 onto work packages with scope boundaries, acceptance gates verbatim,
and non-goals. The contract highlights, binding on the implementer:

1. **Review first.** Before changing behavior for any package, re-verify its
   finding at the current head and file corrections back into the record's
   history if the code has moved. The audit may be wrong; the code is the
   truth.
2. **One package, one branch,** off fresh `origin/dev`, `codex/<topic>`
   named, merged to dev only with the suite green on CI for the branch head.
3. **Smallest truthful change** per the canonical section 9 protocol; no
   bundled redesign; extraction commits are mechanical and probe-gated.
4. **Escalate, don't decide,** on: anything touching `.github/workflows/`
   beyond G3's named scope, save-schema questions beyond additive keys,
   anything near protected content, any behavior change a probe would need
   rewriting for, and any conflict with an owner decision.
5. **Report per package:** commit refs, probe-run links, and the metric
   before/after (for G7/G10: the exact counts).

## 8. Criteria update — what changed and why

This round's owner request was to update the master-audit criteria and
analyze the game against them with a code-refinement goal. The update:

- **`DL-CODE-01`–`DL-CODE-10`** (design 06 section 18): the architecture
  dimension previously had a scorecard row but no citable rules — findings
  could not name what they violated. The new family turns the standing
  refactor contract, state-ownership mold, tier discipline, and probe-first
  practice into falsifiable criteria.
- **Section 12 code-refinement conditions** (canonical audit): satisfaction
  previously measured medium, evidence, device, child, and owner gates but
  would have accepted a 10,000-line coordinator. The gate now measures code
  health too.
- **The framework clause**, recorded in section 12: the criteria are a
  framework, not a ceiling — a material off-list defect is still a finding,
  and a recurring off-list class earns a rule in the same commit as the
  audit that justified it. This round used that clause: the promotion-gate
  and passive-blindness findings fit no prior criterion.

What was deliberately **not** changed: the rating scale, taxonomy, severity
definitions, verification ladder, section 9/10 protocol, and every sealed
evidence claim. The canonical ledger remains the lifecycle owner; this
round's normative deltas live there, and this document is the analysis
record.

## 9. What this round does not claim

- No runtime, capture, device, child, owner, or listening evidence — every
  new finding is V1 and says so in its record.
- No GAME2D re-measurement: the strict true-2D inventory needs the tool run
  under exact Godot, unavailable in this container; `MA-2D-002` counts are
  quoted from their sealed sources only.
- No claim that Stage B's targets are the end state: `main.gd` at 9,000 is a
  trend-reversal checkpoint, not the 2,500-line target, and the next round
  re-measures.
- No promotion readiness claim of any kind; the release gates in canonical
  section 12 stand untouched.

## 10. Round self-verification

`tools/audit_document_authority.py` passes `ALL OK` with this round's
documents in the inventory (46 active items / 48 records at time of
writing), and the twelve new records carry the exact section-10 field set.
The round changes documentation and criteria only: no runtime, asset,
workflow, save-schema, or protected-content file is touched by the audit
commit itself.

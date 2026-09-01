# Independent re-audit of the 2026-08-26 → 2026-08-31 governance line (2026-09-01)

_Owner instruction 2026-09-01: repeat the full audit and re-evaluate the
current results. This record is the Stage R the program prescribes for
itself, applied to this session's own output: every load-bearing claim in
the findings, rule families, evaluations, spec, and handoffs written
between 2026-08-26 and 2026-08-31 was re-verified against head `f5a2648b`
by four independent verification passes (refinement-round findings;
engine wing; pacing wing; spec and cross-document consistency), plus a
direct re-measurement of the metrics and a re-read of the runtime changes.
Verdict vocabulary: CONFIRMED (exactly true at head), ADJUSTED (true in
substance, numbers or anchors drifted or were imprecise), REFUTED (false
at head, or false when written). Every ADJUSTED and REFUTED item below was
corrected in place in the same commit as this record, with a dated
`history` line on the affected finding._

## 1. Headline

The program's structure survived intact: **zero dangling `DL-*` or `MA-*`
references across eight governance documents, every finding record's
mechanism reproduces, the doc-authority gate and CI are green, and no
document sends an agent to dev for governance.** What did not survive was
a layer of numbers and cross-references — about a fifth of the concrete
claims needed adjustment and **six were false**, four of them false when
written. Two of the six were the program failing its own rules: a fix
this session landed (`_sparkle_burst` caching) without updating the
finding it resolved (`MA-PERF-002`), and four wing documents registered
without the §3.2 authority row the wing protocol I wrote demands.

| Area | Claims checked | CONFIRMED | ADJUSTED | REFUTED |
|---|---|---|---|---|
| Refinement-round findings (14 records) | ~75 | ~52 | ~17 | 6 (`MA-PERF-002` alloc, `MA-PERF-003` galaxy, `MA-CODE-003` opera_house, `MA-CODE-004` two figures, `MA-CODE-002` builder count) |
| Engine wing (evaluation + 2 records) | ~35 | ~26 | 7 | 2 (`4.7.1` count method; test fixture `:473`) |
| Pacing wing (5 records + timeline) | ~60 | ~52 | 6 | 1 (post-boss door state) |
| Spec + cross-document consistency | 19 numeric premises + 20 consistency checks | 8 premises; DL/MA/branch/wing checks | 8 premises | 3 premises (private-call count, ceiling exemptions, ratchet baseline) + 20 contradictions/dangling refs |
| Runtime changes (animation wing) | 6 sites | all behave as documented; CI green ×2 | main.gd +20 lines vs `DL-CODE-01` | — |

## 2. Refuted claims and what replaced them

1. **`MA-PERF-002`** — "allocates a node, a mesh, and a material per call; helper
   unchanged": false at head because `ceb12271`/`f265ecc7` (this session's
   animation wing) cached the mesh and materials. Record moved to
   `IN_PROGRESS`; the remaining half is the missing Speedy-tier gate on
   burst amount/cadence. `MA-ANIM-002` now cross-references it as the fix.
2. **`MA-PERF-003`** — `scripts/galaxy.gd` "carries no quality-tier awareness":
   false when written — `_gate_light()` (`galaxy.gd:83-86`) has culled
   OmniLights by `_main.quality != "speedy"` since the 2026-08-05 alpha
   audit. Galaxy removed from the finding; the other named files stand.
3. **`MA-CODE-003`** — the `_mat` factory "recurs in `opera_house.gd`": that
   file is a Canvas career-lifecycle table with no such factory. The clone
   family is `dungeon_puzzle_room.gd`, `combat_arena.gd`, `hit_engine.gd`,
   `stuffie_battle.gd` (+ a static variant in `landmark_art.gd`).
4. **`MA-CODE-004`** — "380 at `e924d9ba`" (the record's own grep returns
   371 there) and "main holds 82 accesses" (92 occurrences on 78 lines at
   `9a1754c1`; 94/80 now). Corrected in place; the 409 → 413 trajectory
   holds.
5. **`ENGINE_ADOPTION` / `MA-ENGINE-001`** — "151 further `4.7.1` mentions":
   the count came from an unescaped-dot pattern (`4.7.1` matching hash
   fragments such as `43791`); the sound literal count is 172 lines / 175
   occurrences across 41 files. Also: 12 pinned files, not 13; the `:473`
   test is a negative fixture (a different dotted string asserted
   rejected), not a second lock; the capture gate is not in the CI path
   at all, so the impact lands on capture rounds, not CI greenness — a
   sharper, not weaker, finding.
6. **`MA-PACE-003`** — "all four doors go `BLOCKED` after the boss": false —
   completed Act One rooms resolve `OPEN` ("sparkly clean"); what stays
   `BLOCKED` is `__royal_hall` and the eight non-Act-One rooms, alongside
   locked jobs and opera. The conclusion (no close, nothing new opens,
   reef teardown, resume tax) is unchanged.

`MA-ENGINE-002`'s title also claimed *two* 4.4-attributed protocols; only
the exit-124 amnesty is attributed in text — the NPOT rule carries no
version or date anywhere, so its 4.4-era origin is a chronology inference.
Title and reproduction corrected; the remediation (empirical revalidation)
is unchanged.

## 3. Adjustments worth knowing about

- **`main.gd` is 10,927 lines** (10,499 at `9a1754c1`, +428; 503 functions,
  +23; 49 `day_one`-named functions on main, up from 26;
  `day_one_director.gd` 748 lines, up from 673). The trend `MA-CODE-001`
  named is still rising; 20 of the 428 are this session's animation
  exemplars (section 5).
- **Trusted rosters are 69 local / 68 remote**, not 64/63 — the same single
  intended difference (`probe_human_art_audit`). Day One probes: 13 files,
  3 gated, 10 not. Probe scripts on disk: 123.
- **design/08's quantitative premises**: the "~6,400 `m._` calls" figure
  counted every `m.` member access; the spec's own ratchet grep
  (`m\._[a-z_]+\(`) counts **846** private calls across 127 helpers. The
  six named builders total **422** calls (not ~280). `_process` is 386
  lines (not ~300); dispatch is ~530 lines (not ~400). Corrected in the
  spec with methods stated.
- **The ratchet as specified would have failed at M0**: four non-probe
  files already exceed the 3,000-line ceiling (`opera_gesture_surface.gd`
  6,185, `arena/castle_rooms_25d.gd` 4,881, `opera_career_world_2d.gd`
  3,433, `kart.gd` 3,324) and only the first was exempted; the budget JSON
  showed `9a1754c1`-era values as if they were the seed. design/08 §7 now
  states that budgets are measured at the M0 commit, scopes check 2 to
  non-probe scripts, and names the exemptions M0 must seed.
- **Sink instruction silence** is deterministic on every *fresh*
  playthrough; a resumed-supplies re-entry does voice it. **Nine**
  `dustboss_*` voice keys are in use, not five — the pacing handoff's
  script grew from 37 to 41 lines.
- Anchor drift: `scripts/ci.sh` amnesty at `:184-195` (+6 from this
  session's checker insertion), `combat_arena.gd:355`,
  `stuffie_battle.gd:274`, `main.gd:8597` (`_fail_line`), `main.gd:8976`
  (`g` overwrite), `dust_bunny_boss_sprite.gd:20-22`, `main.gd:7539-7542`.
- Mechanism precision: `mic_input.gd` appends a new bus at −80 dB
  (deliberately not muted — the analyzer effect needs signal) rather than
  renaming a spare one; `MA-CI-006`'s query does filter `head_branch ==
  'dev'`; the audit_visual_design NPOT checks are advisory WARN/INFO, the
  hard POT gate is separate.

## 4. Cross-document contradictions corrected

Twenty were found; all corrected: the master audit cited design/08 "§9,
four decisions" (it is §11, six); the handoff pointed Stage C at design/08
§7 (the step table is §10) and WP-C5 at §4.5 (typed state is §5.6);
`WP-B1`/`WP-B4` were referenced four times and defined nowhere (now
explicitly defined as absorbed cross-references); `MA-CI-004`'s promotion
was claimed by both WP-A1 and WP-P7 (now: whichever round runs first
executes it, the other verifies at Stage 0); two rounds shared the name
"Stage R" (the pacing round's WP-PR is now named as its counterpart); the
`DL-CODE-*` range read 01–10 in §12 (it is 01–12); "316-path inventory" stood as a
live obligation (now 1:1 parity, 340/340 today); §13 item 11 omitted Stage
E and the engine findings; the owner guide told the owner to run
`tools/audit_structure.py` today (it is an M0 deliverable — caveats added),
to "tell the integration lane" (the owner has no per-agent access), and
pointed the audit round at §6/§13 (§9, §12, §13); four wing documents
lacked their §3.2 authority rows (added); design/08 §8 and the guide's
pasteable blocks did not name the governance branch (added to the Stage R
lane row). "Eight probes, zero gated" stood in four documents against the
measured 13/3.

## 5. Self-findings — the program against its own rules

- **`DL-CODE-01` tension**: the animation wing's exemplar edits grew
  `main.gd` by +20 lines (10,907 → 10,927) with no same-branch net-out.
  The structure ratchet is not built yet, so this is governance-only
  today, and it is recorded here as the rule requires, with its netting
  plan: the burst cache cannot move to a new file without adding a
  production-3D file to the GAME2D manifest (forbidden), so the +20 nets
  out through the WP-C-era extractions (WP-C4 takes `_sparkle_burst` into
  `services.fx`) — a waiver-shaped note, expiring with WP-C4.
- **Duplicate-without-cross-reference**: `MA-ANIM-002` re-described
  `MA-PERF-002`'s allocation half as a new finding and fixed it without
  updating the original. Corrected; the lesson is a Stage-0 step the
  pacing handoff already mandates ("re-verify the finding at your head")
  applied to the audit's own writers.
- **Wing protocol non-compliance**: §3.4 step 2 requires a §3.2 authority
  row in the same commit as the ledger row; four documents shipped
  without one. Added.
- **Method hygiene**: two published counts (the `4.7.1` mentions, the
  "~6,400" calls) were never reproducible because the method was not
  stated or was wrong. Every count in this record states its grep.

## 6. Revised assessment

Nothing in the re-audit changes the four rounds' *direction*:

- The **code-refinement round and Mode Platform** are still the right
  answer to a `main.gd` that has grown another 428 lines since the round
  was measured; the ratchet needs the M0 seeding fixes above to be
  armable, and the six-builder inversion is larger (422 calls) than the
  spec assumed — which strengthens, not weakens, M4's case.
- The **engine adoption wing**'s findings stand with sharper mechanisms;
  the capture gate's stale pin is a capture-round failure waiting to
  happen rather than a CI defect.
- The **animation wing** delivered what it documented (CI green twice, the
  ratchet trip and rework recorded); its one debt is the +20 lines above.
- The **pacing review**'s verdicts and improvement guide stand; the boss
  door-state correction actually sharpens `MA-PACE-003` (eight rooms and
  the royal hall stay locked, not "the castle"), and the handoff's voice
  script is now complete for the boss.

Severities were re-examined and none changed. Lifecycles changed once:
`MA-PERF-002` `CONFIRMED_OPEN` → `IN_PROGRESS`.

## 7. Not independently re-verified (honest residue)

The picture-door ghost-hand loop and voiced prompt (timeline row 7); the
"+3 pearls" boss reward; "scene reload, no fade" at New Game; whether the
exit-124 hang has ever recurred on the 4.7 line (an absence claim WP-E1
exists to settle); device-side feel throughout (the tablet wing's domain).

## 8. Actions taken in this commit

Corrections applied in place to: the findings register (13 records with
dated history lines, one lifecycle change), the master audit (§3.2 rows
×4, §5 index rows ×7, §12/§13 standing statements, §13 item 11 scope), the
refinement handoff (three section pointers, WP-B1/B4 definitions, WP-A1
scope and deconfliction, WP-C4 gate), the pacing handoff (WP-P7
deconfliction, WP-PR naming, four boss voice lines), design/08 (seven
numeric premises, ratchet seeding, governance branch in the lane table),
design/06 (`DL-PACE-03` wording — a persistent pointer on the current
objective is the `DL-AGE-01` baseline, not a defect), the owner guide (six
stale instructions), the engine and animation evaluations (counts and
methods), and the Day One review (five wording corrections).

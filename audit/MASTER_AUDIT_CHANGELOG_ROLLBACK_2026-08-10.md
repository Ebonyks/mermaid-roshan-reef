# Mermaid Roshan master-audit change and rollback ledger

- **Ledger ID:** `MA-CHANGELOG-2026-08-10`
- **Change-ID namespace:** `CHG-001` through `CHG-023`; IDs are permanent and
  are never reassigned or renumbered
- **Audit branch:** `codex/master-audit-20260809`
- **Integration snapshot:**
  `ad36ee9ffe4eae4d5c4183d0546d775de0218213`
- **Integration parents:** audit parent
  `7b5d1209063a22002118c364767d537b34b3dc6f`; upstream parent
  `245c16137fae82271dabac456d5ab04d843463a8`; merge base
  `4ba20414a3fdbb771c3635a43cee66c850a49515`
- **Deprecated-resource archive:**
  `codex/deprecated-resources-roshan-20260809` at
  `9329d9a64b230908f6c77f1b17d8d231a29c5d38`
- **Document authority:** `SUPPORTING_CURRENT`, serving as operational/change-
  control authority below binding security, workflow, protected-asset, save,
  engine, [master-audit](MASTER_AUDIT_2026-08-09.md), and
  [comprehensive-design-language](../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md)
- **Program state:** `IN_PROGRESS / UNSATISFIED`

This is the durable answer to the fact that a long audit can produce both
improvements and regressions. It records what changed, why the change may be
good, how it may be bad, what has actually been proved, what remains unknown,
and how to undo one bounded group without pretending the rest of the branch is
independent. It is not authorization to restore 3D production content, weaken
a safety gate, alter protected originals, or ship an unverified rollback.

## 1. Machine-readable change index

`rollback_mode` values are defined in section 2. A source commit belongs to one
primary `CHG-*` record. A later group may name it only as a dependency.

```yaml
schema: mermaid-roshan/master-audit-change-log/v1
snapshot: ad36ee9ffe4eae4d5c4183d0546d775de0218213
changes:
  - {id: CHG-001, name: roshan-2d-contract-and-frame-repair, rollback_mode: owner_blocked_mixed}
  - {id: CHG-002, name: companion-no-fail-and-verification, rollback_mode: guarded_chain}
  - {id: CHG-003, name: child-access-route-snowman-and-playground, rollback_mode: guarded_mixed}
  - {id: CHG-004, name: voice-and-dialogue-integrity, rollback_mode: guarded_mixed}
  - {id: CHG-005, name: trusted-probe-parity-and-cross-platform-ci, rollback_mode: guarded_mixed}
  - {id: CHG-006, name: lagoon-and-visual-evidence-measurements, rollback_mode: guarded_mixed}
  - {id: CHG-007, name: canvas-2d-feedback, rollback_mode: guarded_mixed}
  - {id: CHG-008, name: game2d-gate-and-ci, rollback_mode: owner_blocked_mixed}
  - {id: CHG-009, name: source-and-model-retirement, rollback_mode: archive_recovery_only}
  - {id: CHG-010, name: canvas-racer-and-exact-cue, rollback_mode: guarded_chain}
  - {id: CHG-011, name: authority-and-master-documents, rollback_mode: documentation_migration}
  - {id: CHG-012, name: dolls-canvas-catcher, rollback_mode: guarded_single}
  - {id: CHG-013, name: seek-animated-kit-and-runtime, rollback_mode: owner_blocked_mixed}
  - {id: CHG-014, name: fresh-visual-attestation-and-cinematic-orientation, rollback_mode: owner_blocked_mixed}
  - {id: CHG-015, name: castle-provenance-newline-stability, rollback_mode: guarded_chain}
  - {id: CHG-016, name: opera-careers-atlases-and-minigame-art, rollback_mode: guarded_mixed}
  - {id: CHG-017, name: ballerina-specialist, rollback_mode: guarded_mixed}
  - {id: CHG-018, name: boxer-specialist, rollback_mode: guarded_single}
  - {id: CHG-019, name: candymaker-phone-fix, rollback_mode: guarded_single}
  - {id: CHG-020, name: deterministic-area-music, rollback_mode: guarded_mixed}
  - {id: CHG-021, name: castle-logo-personalization, rollback_mode: guarded_single}
  - {id: CHG-022, name: ad36-integration-reconciliation, rollback_mode: whole_merge_only}
  - {id: CHG-023, name: change-log-and-rollback-process, rollback_mode: documentation_migration}
```

## 2. Safe rollback protocol

### 2.1 Non-negotiable preparation

Every experiment starts from a clean, current branch. Replace `<change-id>`
with the lowercase ID, for example `chg-021`.

```powershell
git status --short
git fetch origin --prune
git switch -c codex/rollback-<change-id> ad36ee9ffe4eae4d5c4183d0546d775de0218213
git rev-parse HEAD
```

If `git status --short` was not empty, stop. Preserve the work under the
repository rescue workflow before creating a rollback branch. Never use
`reset --hard`, never work directly on `master` or `dev`, and never mix several
change IDs into one rollback commit.

Before editing, save the starting commit and inspect the exact source change:

```powershell
git show --stat --summary <exact-source-commit>
git diff <exact-source-commit>^ <exact-source-commit> -- <governed-paths>
```

### 2.2 Rollback modes

| Mode | Allowed method |
|---|---|
| `guarded_single` | On the clean rollback branch, run `git revert --no-commit <exact-commit>` only for the named logically independent commit. Stop on any conflict. |
| `guarded_chain` | Revert only the exact listed commits in reverse dependency order, one `--no-commit` operation at a time. Inspect after each operation; abort the experiment on an unexpected hunk. |
| `guarded_mixed` | A one-line revert is refused. Later work shares paths or semantics. Construct a reviewed inverse limited to the listed path family, leaf assets first, runtime second, probes/gates/docs last. Do not restore an old whole file over later work. |
| `owner_blocked_mixed` | Same mechanics as `guarded_mixed`, but the inverse conflicts with a direct owner/safety rule. It may be used only for diagnosis unless the owner explicitly changes that rule. |
| `archive_recovery_only` | Do not revert into production. Verify or recover exact historical bytes from the named archive with read-only `git show`/`git ls-tree`; never merge or cherry-pick the archive branch. |
| `documentation_migration` | Add a new superseding record and update ledgers/references together. Do not erase the prior decision or rewrite history. |
| `whole_merge_only` | Only the all-or-nothing recovery in section 7 applies. It is never an individual-change tool. |

The companion planner is read-only: it imports no Git/filesystem mutation API
and prints plans or guarded shell text to standard output. It never executes a
command. Use it from the repository root:

```powershell
python -B tools/plan_audit_rollback.py --list
python -B tools/plan_audit_rollback.py CHG-013
python -B tools/plan_audit_rollback.py CHG-021 --emit-script
```

Only CHG-020, CHG-021, and the all-or-nothing CHG-022 can emit a script. Every
other ID refuses automation even when its human ledger mode says
`guarded_single`: shared-path, product-policy, or not-yet-committed context
still requires a reviewed manual inverse. Emitted scripts create a dedicated
branch at exact `ad36ee9f`, run gates, and stop before commit.

For an allowed exact revert, the required form is:

```powershell
git revert --no-commit <exact-source-commit>
git status --short
git diff --stat
git diff --check
```

On a conflict, stop. Do not accept either side wholesale. Abort with
`git revert --abort` if Git created a revert sequence, then reclassify the
attempt as `guarded_mixed`. Before committing, compare the actual diff with the
path family in this ledger and prove no unrelated or protected path changed.

### 2.3 Protected assets and policy barriers

No rollback may modify, replace, recompress, or delete anything below:

```text
assets/book/
assets/audio/voices/
assets/characters/friends/
```

The voice changes below affect routing and cue selection, not protected voice
files. A rollback diff containing any protected path is invalid and must stop.
Likewise, restoration of retired GLB, Blend, model texture, 3D runtime, or 3D
probe content is not a normal product rollback: the direct final-2D decision
still controls. The deprecated-resource branch is evidence, not a fallback.

### 2.4 Gates after any candidate rollback

Run the focused group gates below first, then the repository gates. Commands
requiring Godot use exactly 4.7.1-stable.

```powershell
git diff --check
python -m gdtoolkit.parser <changed-gd-files>
python tools/lint_inference.py <changed-gd-files>
python -B tools/audit_game_2d.py
python -B tools/audit_probe_parity.py
& $env:GODOT --headless --import .
```

Then run the named focused probes and `scripts/ci.sh`. A rollback is not ready
to commit if it worsens the exact GAME2D inventory, makes the visual-evidence
contract less falsifiable, removes a no-fail/negative control, creates a save
incompatibility, changes a protected path, or relies on a probe-only/device
implementation split. Commit the rollback only after its focused and full
gates are green:

```powershell
git status --short
git add -- <reviewed-paths-only>
git diff --cached --check
git diff --cached --stat
git commit -m "revert(<change-id>): <bounded reason>"
```

Never use `git commit -a` for a rollback: a gate may have changed another
tracked file, and `-a` would stage it silently. Add every intended path
explicitly, then compare the staged set with this ledger. Never push, merge to
`dev`, or promote until the exact rollback commit is green in remote CI and all
applicable capture, device, child, audio-listening, and owner gates are
recorded. A local green run is not release authorization.

## 3. Evidence snapshot and common unknowns

At `ad36ee9f`, exact Godot 4.7.1-stable local `scripts/ci.sh` completed in
826.4 seconds with all 63 trusted local probes green. The focused Opera 2D,
Nursery, Detective, gesture-quality, audio, interaction, passive, voice, and
legacy-Opera probes were green. Deterministic checks reported 39 Opera
minigame-art outputs, 13 career atlases/208 frames, and 42 area-music cues as
matching their governed sources.

That does not make the audit satisfied. The game-wide inventory remains 509
model files, 68 production-3D files, 77 probe-3D files, one scene-3D file, and
one configuration-3D file. Strict fresh visual attestation remains
`UNSATISFIED` with 16 failures, 17 review-open items, two manual-open items,
and 86 coverage gaps. No remote exact-head, complete Mobile capture matrix,
Lenovo Tab M11 acceptance, intended-child session, complete audio listening
pass, protected-voice review, or owner visual/identity acceptance closes those
gaps. Every change record below inherits these common gaps unless it says
otherwise.

### 3.1 Merge scaffolding is topology, not source ownership

The following reachable commits join feature branches but do not own a
separate product behavior in this ledger. They are recorded so a future
reviewer does not mistake an unassigned merge for missing history:

| Merge commit | Topology role |
|---|---|
| `57225a2bc27993e2c5e83c25b9a5c90759eec03f` | Joined the Ballerina and Candymaker lines before the accepted Ballerina finish. |
| `18bbadd16923ee37b77d55449ffa654a455876ba` | Joined Boxer and Candymaker before the later Boxer/Ballerina merge. |
| `9b58c851dbdafede926b99c001f3bcb37c3b43c2` | Joined area music and Candymaker before the later music/Ballerina merge. |
| `053aaed584fcb2d15574ba62d9c1d9e41f280d36` | Joined Boxer/Candymaker with Ballerina; it is a diagnostic feature comparison, not an owned source commit. |
| `e38373c32e89fe9b197f1a27806c42a36c4898cb` | Joined music/Candymaker with Ballerina; it is topology only. |
| `ecad384e99c3f956e7559f9801c37f4a4a1a2111` | Joined general Opera-minigame work with the Castle-logo line. |

Likewise, upstream merge `245c16137fae82271dabac456d5ab04d843463a8`
is the exact parent-2 input to `ad36ee9f`, not an independently owned source
change. Its parent-1 comparison isolates CHG-020 for diagnosis; its opposing
parent-2 comparison isolates CHG-018. Those two comparisons are mutually
exclusive and must never be applied on the same rollback branch.

## 4. Detailed change records

### CHG-001 — Roshan 2D contract and frame repair

- **Sources:** `3be5b44bfa196df8d321ac0606472300c1c8d049`
  (2D-only Roshan contract and active model/pipeline retirement),
  and `a1be9a1ecf0a6fc65396a8dd78ee10c8fbe35fde` (replacement playground
  frames).
- **Paths:** Roshan model/tool families under `assets/characters/`,
  `gen2/meshy/roshan_*`, Roshan build/rig/pose tools and probes; playground
  sprites and provenance; narrow Roshan CI/audits.
- **Outcome / positive effect:** active Roshan no longer depends on the retired
  v2/v3/v4 model chain; clipped/debris playground frames were replaced.
- **Possible negative effect / unknown:** removal eliminates an emergency 3D
  visual fallback; replacement-frame identity, motion cadence, and cutoff still
  need supported-aspect capture, device, child, and owner review. The narrow
  Roshan pass does not prove the whole game is 2D.
- **Dependencies and evidence:** archive head `9329d9a6`; license/inventory
  ledgers; `audit_roshan_2d`, sprite-clipping tests, playground/Lagoon probes,
  full CI.
- **Rollback:** `owner_blocked_mixed`. Refuse a one-line revert: it would
  restore model code/assets and obsolete frames together. For a frame-only
  regression, inverse only `a1be9a1e`'s new runtime sprite references and
  corresponding provenance on `codex/rollback-chg-001`, while leaving the 2D
  contract intact; require clipping, Lagoon, Mobile capture, and owner identity
  review. Model recovery is archive inspection only and cannot be merged under
  the current owner decision.

### CHG-002 — Companion no-fail behavior and verification

- **Sources:** `0522d1faafa6e0ba13741b00187b8a873a1a7ab5` and follow-up
  verification `f8efeb0a1a55d6e203e25ef0ee4738ef12bc22be`.
- **Paths:** `scripts/companion.gd`, `scripts/stuffie_battle.gd`, save/main
  integration, companion/load/passive probes, `STUFFIE_COMPANIONS.md`.
- **Outcome / positive effect:** inactivity and imperfect care no longer create
  a fail state; progress and patient recovery remain available; negative and
  save/load paths are explicitly probed.
- **Possible negative effect / unknown:** a child may linger indefinitely if
  encouragement or exit affordances are unclear; a no-fail state can still be
  a soft comprehension trap. Child observation and device re-entry remain open.
- **Dependencies and evidence:** save compatibility, passive probe, companion/
  stuffie/load probes, full CI.
- **Rollback:** `guarded_chain`; the inverse would reintroduce a forbidden fail
  state and therefore is diagnostic only without a new owner decision. If
  required to reproduce a regression, attempt `git revert --no-commit
  f8efeb0a1a55d6e203e25ef0ee4738ef12bc22be` then `git revert --no-commit
  0522d1faafa6e0ba13741b00187b8a873a1a7ab5`; stop on the first
  conflict. Run passive, stuffie, load, save-recovery, and full CI before any
  commit.

### CHG-003 — Child-access route, snowman targets, and visible playground action

- **Sources:** `82f9828c5a478599668f2b019f53128ff084a73c`,
  `986010c0bb3c8a018e774e420c62cccc3737a333`, and
  `711879ecf10fa7c8871abb1544248a49f38d9078`, plus default-Hybrid portal
  coverage `e6e56f8b8c185b3efbc6583617eaad77c0b2108d`.
- **Paths:** picture-game touch geometry; Sky Lagoon promenade/main/pause route;
  Lagoon, interaction, boot-display, UI, and snowman probes.
- **Outcome / positive effect:** larger snowman face targets, a child-visible
  Reef route, and playground actions settling on visible Roshan improve one-
  finger reach and cause/effect legibility; the default Hybrid route is no
  longer hidden behind Classic-only probe setup.
- **Possible negative effect / unknown:** larger targets can overlap at unusual
  aspects; added route affordances can crowd the screen or trigger accidental
  navigation; visible settling still needs real touch and occlusion review.
- **Dependencies and evidence:** CHG-001 frame assets, CHG-006 measurement
  logic, `probe_mg2d`, Lagoon/interaction/UI probes, full CI.
- **Rollback:** `guarded_mixed`, because picture games and Lagoon files received
  later changes. Revert one user-visible subfeature at a time by inverse hunks
  limited to its source commit; never restore whole files. Verify touch-target
  non-overlap, route entry/exit, action completion, and child discoverability.

### CHG-004 — Voice and dialogue integrity

- **Sources:** `17813082951eefd8552c56cdda1bda61c8d1c87d` (duplicate objective
  suppression), `c86d3a7d024ecac59900b8b8348c305e3493c10d` (stop stale speech at
  transitions), `1c6e0c24799ab96a3e632f8202c8b6aa905185a4` (reject shadowed cue
  keys), `e8485d544c785548f855e55124af08dc4f15e277` (single Huluu brawl cues),
  and `8b5ca161a71f9bb7e709e4bc653d81be8445b077` (preserve Opera speaker on
  re-prompts).
- **Paths:** `scripts/audio_director.gd`, main/Brawl/Opera prompt routing,
  `tools/make_voices.py`, voice-generation tests, voice/Nursery probes. No
  protected recording was edited.
- **Outcome / positive effect:** one objective speaks once, stale lines do not
  bleed into the next dialogue, cue-key collisions fail, and Brawl/Opera
  re-prompts retain the intended family speaker and exact event.
- **Possible negative effect / unknown:** aggressive stopping can truncate a
  still-useful line; removing fallback behavior can expose a silent missing
  cue; machine probes do not prove intelligibility or mix balance on device.
- **Dependencies and evidence:** current cue registry, audio director, exact
  speaker/cue assertions in voice/audio/Nursery/Opera probes, full CI; human
  protected-voice and device listening remain open.
- **Rollback:** `guarded_mixed`; later music and Opera reconciliation share the
  same paths. Refuse a combined revert. Isolate the exact symptom's commit,
  inverse only its routing/test hunks, confirm the protected directories are
  absent from the diff, and run voice, audio, passive, Brawl, Nursery, Opera 2D,
  and full CI plus an audible transition test.

### CHG-005 — Trusted probe parity and cross-platform CI

- **Sources:** `7e6d699dcad4e8e37e0fd8e47583354d77cd1876`,
  Windows grade portability `5c4b34f0f50693ce79d12fb455936453c324ae0c`,
  and runner-temp archive containment
  `7b5d1209063a22002118c364767d537b34b3dc6f`.
- **Paths:** `scripts/ci.sh`, `.github/workflows/probes.yml`, and
  probe-parity and grade-headroom tools/tests.
- **Outcome / positive effect:** local and remote trusted-loop drift is detected
  rather than allowing CI to imply coverage it does not execute; Windows text
  encoding no longer creates a false grade failure; the downloaded Godot ZIP
  cannot be counted as active repository debt.
- **Possible negative effect / unknown:** legitimate display-only differences
  need explicit classification; loop expansion increases CI duration and a
  parser bug could block good work.
- **Dependencies and evidence:** parity unit/stress/default runs; current
  intended difference is the display-only human-art probe.
- **Rollback:** `guarded_mixed`: these are three CI protections, and the current
  CI/workflow files were later reconciled by CHG-022. Inverse only the proven
  faulty sub-change, preserve the other two, and stop on shared-file conflict.
  Run parity stress/default, grade tests, GAME2D, and full CI. Removing parity
  or moving the engine archive back into the workspace merely to make CI green
  is not acceptable.

### CHG-006 — Lagoon and visual-evidence measurements

- **Sources:** `219fe59384d3af5f2b0993fda13054bdf91f6b25`,
  `6e04706d686e1abdadd95c80195c5e2bf56c9c22`,
  `09027504f2da30897cf219f91728994d0392eb13`, and
  `76c30a6699de3a8bb2b9699f2ec9aaf89d5c00b6`.
- **Paths:** visual-audit spec/tool/tests, scene-congruency audit, Lagoon facts
  and touch/residency probes, `VISUAL_AUDIT_TOOL.md`.
- **Outcome / positive effect:** visual states are exhaustive, Lagoon touch
  regions are measured in the correct coordinate space, active 2D evidence is
  tracked, and texture residency is not inferred from misleading source data.
- **Possible negative effect / unknown:** stricter measurement exposes many
  review/coverage states and can lengthen investigations; a faulty runtime
  adapter can cause honest fail-closed gaps rather than useful captures.
- **Dependencies and evidence:** CHG-003 runtime surfaces and CHG-014 fresh-
  attestation rules; visual unit/stress/default/fresh-strict runs.
- **Rollback:** `guarded_mixed`. Do not revert measurements to convert an open
  state into PASS. If a formula is demonstrably wrong, inverse only that formula
  and its falsification test, then prove the old and new coordinate/residency
  cases, Lagoon probes, and fresh strict audit.

### CHG-007 — Canvas 2D feedback for picture games, wardrobe, and medals

- **Sources:** `21ae8391f019a00f740a2433e84532f300b6e109`,
  `be3fb490246f3dc21dd1f0246b8f72208e458e3a`,
  `fe3616b438b423600a840d5affa59baec8016880`, and
  `8ed978bec959140c0b100b8eb811ad648da589c1`.
- **Paths:** `scripts/games/picture_games.gd`, wardrobe and medal systems, and
  mg2d/UI/rank probes.
- **Outcome / positive effect:** reward/try-on/award feedback stays inside its
  owning Canvas stage or overlay; legacy spatial medal presentation is retired;
  teardown owns its transient tweens and nodes.
- **Possible negative effect / unknown:** Canvas layering can hide feedback at
  alternate aspect ratios; larger effects can increase transparent overdraw;
  picture-game music integration later changed the same lifecycle.
- **Dependencies and evidence:** CHG-008 manifest/gate, CHG-010's shared debt-
  shrink manifest commit, CHG-020 music routing, mg2d/UI/rank/passive/full CI.
- **Rollback:** `guarded_mixed`. Wardrobe's exact commit may be tested alone with
  `git revert --no-commit be3fb490246f3dc21dd1f0246b8f72208e458e3a`
  if it applies cleanly. Picture games and
  medals require reviewed inverse hunks; do not revert the shared manifest
  commit to undo medal presentation. Run the relevant focused probe, GAME2D
  default/stress, visual capture, and full CI.

### CHG-008 — Game-wide 2D gate and CI enforcement

- **Sources:** `e0877b65cf9e080e70117c995d53624ea3ab9910`,
  `d6240be828a841b70fba4742874ef28d34d47011`,
  `b3ad384228bda62d33af0e7cc9df099ad63326b8`,
  Opera/medal shrink `344d8d5c5d30d773dfc1da5868fa97fbdbf333b6`,
  and post-Seek/Dolls shrink `a3d3bce18dd73d0ac87f2fb4bac397e2b4396180`.
- **Paths:** `tools/audit_game_2d.py`, its manifest/tests, local CI, and remote
  workflow placement/import scope.
- **Outcome / positive effect:** disguised/model/archive/sidecar/runtime 3D debt
  is counted with falsification controls; the exact inventory may shrink but
  cannot be silently refreshed upward. Runner-temp archive containment belongs
  to CHG-005.
- **Possible negative effect / unknown:** the manifest is maintenance-heavy,
  default `UNSATISFIED` can be misunderstood as green, and a scanner defect can
  block unrelated work. The gate reports debt; it does not migrate it.
- **Dependencies and evidence:** 73 unit tests, 14 stress controls, default and
  regression runs, exact import, current 509/68 inventory, CHG-005 parity.
- **Rollback:** `owner_blocked_mixed`. Removing or weakening the gate conflicts
  with the final-2D decision. A scanner-bug rollback must preserve the manifest,
  falsification tests, after-import placement, and no-regression ceiling; patch
  only the proven faulty rule and add a failing fixture first. Full GAME2D tests,
  import, parity, and full CI are mandatory.

### CHG-009 — Source and unreachable-model retirement

- **Sources:** `86d0c2434579c1b0e226414a9601dcce4d5b9e22`
  (189 removals plus the migration-manifest update; 190 changed paths) and
  `0b75c60cdd16d670bc8366f7d3aeaaf426f682e9` (146 removals plus the
  manifest update; 147 changed paths). Roshan and Seek-specific retirements
  belong to CHG-001 and CHG-013, not this group.
- **Paths:** obsolete Blender sources, `assets/art35/`, Castle/galaxy/furniture/
  portal/ship model families, backups, and matching historical inventory.
- **Outcome / positive effect:** known non-runtime 3D payloads leave the active
  project while exact history remains recoverable on the archive branch.
- **Possible negative effect / unknown:** an incorrectly classified source may
  remove a future non-destructive derivation master; repository history is not
  as convenient as an active file tree; provenance links can become stale.
- **Dependencies and evidence:** reference/orphan audits, license ledger,
  GAME2D manifest history, archive branch/hash, full CI.
- **Rollback:** `archive_recovery_only`. Never revert these commits wholesale
  into production and never merge/cherry-pick the archive. For a claimed missing
  source, use `git ls-tree -r 9329d9a6 -- <exact-path>` and `git show
  9329d9a6:<exact-path>` to verify bytes/hash outside runtime. Restoration to an
  active branch requires a new owner decision, provenance review, reachability
  proof, and a fresh 2D plan.

### CHG-010 — True-Canvas Opera Racer and exact cue

- **Sources:** `82124b3a03426985afa9ff5d03447b8807d37f12`,
  and `e4528b27e2552f669de2b65c37da0243fb924eac`.
- **Paths:** Opera career world/2D probe and audio cue routing.
- **Outcome / positive effect:** Racer uses one Canvas implementation on device
  and headless, with `TUNE` → `TO THE LINE` → `RACE`, circle goal `0.9`, exact
  `op_racer_lap_two`, no external kart child, and no probe-only medium split.
- **Possible negative effect / unknown:** circle recognition may be too lenient
  or too difficult on the actual phone; removal of the 3D kart changes the
  spectacle and physical feel. The resulting measured debt shrink is owned by
  CHG-008 and cannot be blindly reversed with the runtime.
- **Dependencies and evidence:** CHG-004 cue integrity, CHG-016 current career
  table, CHG-022 conflict resolution; Opera 2D/passive/voice/teardown probes,
  GAME2D, full CI. Device touch, child comprehension, capture, and owner feel
  remain open.
- **Rollback:** `guarded_chain`, but only for a Canvas-to-Canvas replacement.
  Refuse any revert that restores the upstream nested 3D kart. Reverse exact
  cue and Racer commits only after a replacement owns the same save/lifecycle;
  update the CHG-008 manifest only from a fresh measured scan. Run Opera 2D,
  audio, voice, passive, GAME2D, full CI,
  Mobile capture, and device circle tests.

### CHG-011 — Authority and master-audit documents

- **Sources:** `806ffb95a4c36ca938235bc2e41d4491de2d019a`,
  `0e75f3838a439391ff999e2bee9131a81d212fa1`,
  `9289dd813439d16cc8178e57abcbd332a8e0fe9d`, and
  `d1f73a388ad9716a2abdfb6aca751f368abb2ff2`.
- **Paths:** master audit, design 00–06, `AGENTS.md`, `CLAUDE.md`, Roshan 2D
  README, documentation ledger/index.
- **Outcome / positive effect:** final game-wide 2D, security precedence,
  lifecycle/evidence vocabulary, and satisfaction criteria are stated in one
  traceable authority system.
- **Possible negative effect / unknown:** the ledger remains incomplete across
  hundreds of Markdown files; stale wording can acquire false authority; a
  documentation-only claim can outrun runtime reality.
- **Dependencies and evidence:** document ledger, resolvable links/IDs, current
  central audit and design language; CHG-022 integrates later Opera/music
  authority. Both central documents remain proposed until their own closure
  gates pass.
- **Rollback:** `documentation_migration`. Never delete history or restore stale
  3D authority. Add a dated superseding owner decision, update every authority
  index/ledger/reference in one bounded commit, and run UTF-8, link, ID, table,
  fence, forbidden-claim, and full CI checks.

### CHG-012 — Dolls true-Canvas catcher

- **Source:** `5df754279a358b475c3e088e9e54f6ad0c1f32dc`.
- **Paths:** Dolls game, main/player integration, audit/Dolls probes.
- **Outcome / positive effect:** the catcher and its interaction are true
  Canvas rather than spatial, while shared state and existing behavior remain
  owned by main.
- **Possible negative effect / unknown:** coordinate conversion may feel
  different at device stretch ratios; capture/occlusion, device touch, and child
  play remain open.
- **Dependencies and evidence:** CHG-008, Dolls/audit/passive/full CI.
- **Rollback:** `guarded_single`; attempt the exact revert only to diagnose a
  confirmed regression. Because it restores spatial behavior, it cannot be
  merged under current authority. Stop on main/player conflicts. Run parser,
  lint, Dolls/audit/passive, GAME2D, captures, and full CI.

### CHG-013 — Seek animated actor kit and 2D meadow

- **Sources:** `8fa90111fefddd114a7a9ad68f838ba2108ce00e` (animated Evie/Lamb-a'
  kit and provenance), `27bda85d3fc9a7842b05426e6ca846139160b043`
  (Canvas meadow/runtime and four meadow-GLB deletions).
- **Paths:** `assets/minigames/seek/`, governed ImageGen sources/build tool,
  Seek/main runtime, meadow GLBs, Seek/art/audit probes, `ASSET_LICENSES.md`.
- **Outcome / positive effect:** the low-quality vinyl pair/bush presentation is
  replaced by animated actors and a higher-grade true-Canvas meadow; protected
  originals are untouched. Default-Hybrid route coverage belongs to CHG-003.
- **Possible negative effect / unknown:** generated identity/motion and the new
  meadow may still diverge from the surrounding game's final art quality;
  animation decoding/overdraw and one-finger readability need device evidence;
  reverting runtime would revive expressly deprecated vinyl/3D presentation.
- **Dependencies and evidence:** deterministic build tests/provenance, Seek and
  audit probes, GAME2D shrink, full CI. Supported-aspect capture, target-device,
  child, and owner acceptance remain open.
- **Rollback:** `owner_blocked_mixed`. Refuse the two-commit one-line inverse:
  it would restore the vinyl runtime and four GLBs. If one generated asset is
  rejected, keep the Canvas engine and selectively replace only that derived
  asset at a new path with complete provenance; do not modify protected/reference
  originals. Run deterministic build, clipping/art/Seek/audit/passive, GAME2D,
  full CI, capture, device, child, and owner gates.

### CHG-014 — Fresh visual attestation and cinematic orientation

- **Sources:** wrong-orientation rejection
  `b50f2477f87b56ed16f1ca469fbf7b5848ead723`, ignored-review hygiene
  `96317f8b703f08f171a00a774b8dc546910f57e4`, fresh evidence
  `3b7a7e665323bed975b56635cbb6b7e99106c5e5`, and ignored-source binding
  `fea916a81d8ece3df36a568567016a59fecd46a0`; CHG-006 owns the earlier
  measurement corrections.
- **Paths:** visual-audit tool/spec/tests, runtime probe, methodology document,
  active ignored-source binding.
- **Outcome / positive effect:** equal-sized wrong-orientation cinematic inputs
  fail; saved/manual facts cannot grant PASS; a fresh,
  one-use, exact-engine Canvas capture must bind source, state transition,
  visibility, order, occlusion, and touch evidence. Missing adapters fail
  closed.
- **Possible negative effect / unknown:** the current environment produces 86
  coverage gaps and no authoritative Canvas captures; strict failure is honest
  but can slow delivery until capture infrastructure is available.
- **Dependencies and evidence:** CHG-006; visual unit/stress/default and exact
  `--fresh-runtime --strict`; current result remains unsatisfied.
- **Rollback:** `owner_blocked_mixed`. Never revert to saved evidence to obtain a
  green result. Repair the adapter/challenge/source binding while keeping every
  falsification test. Any proposed contract change requires old-vs-new negative
  controls and must not reduce failure observability.

### CHG-015 — Castle provenance newline stability

- **Sources:** `df5b4cf7f98cd1ce09468b2551cd3bd5bb8ddf4c` and dependency-light
  test follow-up `5961fd968066e4644e2b77f73c72e990c4bef4ac`.
- **Paths:** Castle interaction manifest/approval ledger, delivery/native build
  tools and tests.
- **Outcome / positive effect:** deterministic Castle provenance checks are
  stable across Windows/Linux newline conventions and do not require an
  unnecessary image dependency for the narrow test.
- **Possible negative effect / unknown:** over-normalization could conceal a
  meaningful byte change if applied beyond exact text outputs; runtime image
  bytes must remain strict.
- **Dependencies and evidence:** Castle provenance builders/tests and full CI.
- **Rollback:** `guarded_chain`; attempt `5961fd96` then `df5b4cf7` only for a
  reproduced false acceptance/rejection. Preserve binary/hash strictness and
  run both Castle builders/checks, interaction probe, cross-platform test, and
  full CI.

### CHG-016 — General Opera careers, 13 atlases, and minigame art

- **Sources:** `ebd75539f16546752dcea4cbcabd2fea1c9f9cb4` (pre-audit Chef
  animation source), `32e1a7e8c50123ec0abf83a291352fecee189ad0` (career/menu/
  atlas overhaul), and `2119ab399ae778530c1f944b4f7414a97d218608`
  (interaction/art overhaul). Specialist deltas belong to CHG-017–019.
- **Paths:** 13 runtime atlases and governed sources/reports, 17 crest/goal
  cards, Opera lobby/actor/career/gesture/backdrop code, minigame widgets,
  deterministic art/animation tools, probes, licenses, and domain audits.
- **Outcome / positive effect:** shipping Opera has 13 careers, 53 phases, 27
  modes, no generic `bop`, 208 reviewed atlas frames, clearer career identity,
  and 39 deterministically checked minigame-art outputs.
- **Possible negative effect / unknown:** large atlases and transparent art add
  APK/decode/overdraw costs; automated frame accounting does not prove identity,
  anatomy, cadence, stage composition, or child comprehension; some historical
  audit prose is superseded.
- **Dependencies and evidence:** CHG-017–020 and CHG-022; minigame-art check,
  animation audit, Opera 2D/gesture/Detective/Nursery/passive/teardown probes,
  full CI. Capture/device/child/owner gates remain open.
- **Rollback:** `guarded_mixed`. Refuse reverting `32e1a7e8` or `2119ab39` as a
  unit: later specialists and reconciliation depend on their files/assets.
  Select one career or widget family, remove runtime references first, preserve
  provenance/history, then remove only confirmed-orphan derived assets and
  update deterministic manifests/probes. Never fall back to a 3D career.

### CHG-017 — Ballerina specialist

- **Sources:** `dc48c91a047668dd90f7f794950e8402e0138e08`,
  `6ab63aa7c147be395d0d67945a527b5789ccf746`,
  `26305338d84791feb85b40927379a7c325947b63`,
  `86b6a5b693410c48c4fbcfdb83956ebca6100c44`,
  `6369a72adec388e1a4c751fc6a2d2a61458531fb`,
  `3dd98fbe5e63374615c64316f353665553d36fcd`,
  `7d9e6c5f121ef1245bff96388745fd85d54b16d3`, and
  `0447188f73b7ca7dadfe782384cc8d1c4da7828f`.
- **Paths:** Ballerina domain brief/surface, career/competition/actor/backdrop
  integration, 2D and gesture probes; accepted atlas itself is owned by
  CHG-016 and has SHA-256
  `c829784d4085e9cd9765cf0114a0f65bfe3f662ed8acc423223b726a0f003995`.
- **Outcome / positive effect:** the obsolete generic/looped Ballerina is
  superseded by Pearl Mirror, Ribbon Trail, and Grand Twirl, with held pose
  keys, explicit teaching/assists, and a one-shot curtain call. Earlier
  leg/feet-like candidates stay rejected.
- **Possible negative effect / unknown:** held poses reduce motion richness;
  silhouette discontinuities prevented looping; teaching timing, gesture
  tolerance, identity, and recital quality still require child/device/owner
  evidence.
- **Dependencies and evidence:** CHG-016 atlas/actor system and CHG-022 prompt
  reconciliation; animation hash/audit, Opera 2D and 271-check gesture probe,
  full CI.
- **Rollback:** `guarded_mixed`. Do not restore the old Ballerina atlas or
  chronological loop. Roll back one specialist behavior in reverse source order
  only after defining a Canvas replacement; keep the accepted atlas/provenance
  unless owner identity review rejects it. Re-run animation, gesture, 2D,
  voice/passive/full CI and capture/device/child/owner gates.

### CHG-018 — Boxer specialist

- **Source:** `8d67c2bd180b97a0bca6c473892d45aedbd00537`.
- **Paths:** Boxer project brief, `opera_boxing_surface.gd`, career integration,
  Opera 2D and gesture-quality probes.
- **Outcome / positive effect:** Boxer becomes a five-phase full-stage,
  two-glove, one/two-finger specialist with no misses/fail state and stable save
  bit 128.
- **Possible negative effect / unknown:** two-finger play may exceed the child's
  comfortable motor pattern despite one-finger compatibility; hit geometry,
  visual intensity, performance, and retained legacy Boxer GLB debt require
  device/child/owner review.
- **Dependencies and evidence:** CHG-016 base and CHG-022 integration; focused
  2D/gesture/passive/save/full CI.
- **Rollback:** `guarded_single` logically, but shared career/probe paths can
  conflict. Attempt `git revert --no-commit
  8d67c2bd180b97a0bca6c473892d45aedbd00537` only if the branch is
  intended to remove the entire specialist and preserves save bit semantics and
  a Canvas fallback. Never restore the three retained GLBs as dependencies.
  Run Opera 2D/gesture/passive/load/GAME2D/full CI and capture/device/child.

### CHG-019 — Candymaker phone-playability fix

- **Source:** `3974675629c45a8a95d41d597205f8110aaa0deb`.
- **Paths:** Opera gesture surface and 2D/gesture probes; base art/engine is
  owned by CHG-016.
- **Outcome / positive effect:** syrup play uses one complete phone-legible
  mold, a generous pitcher target, and shared painted spout/stream/hit geometry.
- **Possible negative effect / unknown:** the larger target may be overly
  permissive, obscure art, or reduce agency; phone capture and real touch are
  still needed.
- **Dependencies and evidence:** CHG-016/022; Candymaker assertions in Opera 2D
  and gesture-quality probes, full CI.
- **Rollback:** `guarded_single`; attempt the exact no-commit revert only if its
  hunks apply cleanly. Stop if it touches unrelated gesture engines. Verify
  mold completeness, painted/runtime hit alignment, passive non-completion,
  full CI, Mobile capture, and device touch before committing.

### CHG-020 — Deterministic area music

- **Sources:** `0da07e24c92c56a974635d7a3f3a4967f4695624`,
  `27c2c95d7711c5b5ddb36eb46fb5baf1a86e5f96`, and
  `ddac6b2e17246e6e7247692bc9c61af16d3adbeb`.
- **Paths:** 42 new OGG/import files and manifest, score source, deterministic
  builder, audio director and Castle/combat/picture/Opera/main routing,
  `probe_audio.gd`, licenses, music audit.
- **Outcome / positive effect:** formerly quiet areas receive deterministic,
  route-bound cues; source/render/import hashes, codec, loop, loudness, and
  routing are machine-checkable. Total music inventory is 57 files, including
  56 score files and legacy `banjo.ogg` as SFX.
- **Possible negative effect / unknown:** roughly 42 new compressed streams add
  APK size and memory/streaming pressure; continuous music may fatigue or mask
  family voices; stylistic similarity and loop seams require listening, not
  hashes.
- **Dependencies and evidence:** CHG-004 voice lifecycle, CHG-007 picture-game
  lifecycle, CHG-016 Opera routing, CHG-022 conflict resolution;
  `build_area_music.py --check`, audio/voice/interaction probes, full CI. Human
  two-wrap, voice/ducking, music-off, mono, and M11 listening remain open.
- **Rollback:** `guarded_mixed`. Refuse a one-line revert of `0da07e24`: later
  fixes and merge resolutions share its routing files. For one objectionable
  cue, first route that area to the prior valid state, prove voice/music-off
  behavior, then remove only the orphaned OGG/import/manifest/score entry and
  update licenses/audit. For the whole program, reverse docs follow-up, routing,
  generated delivery, and score source in that order on a dedicated branch;
  run builder check, import, audio/voice/picture/Opera probes, full CI, and the
  complete listening matrix. The planner's diagnostic whole-feature comparison
  is `git revert --no-commit -m 1
  245c16137fae82271dabac456d5ab04d843463a8`. It is mutually exclusive with
  CHG-018's opposing parent-2 comparison; never apply both on one branch. A
  read-only merge-tree check at `ad36ee9f` proves this CHG-020 comparison stops
  on `scripts/games/picture_games.gd`, where CHG-007 Canvas feedback and CHG-020
  music ownership were manually reconciled. Abort there or hand-author the
  inverse under both records; never auto-resolve the conflict.

### CHG-021 — Castle logo personalization

- **Source:** `9e75e8e392d34b784b9899e7434cdf954fb0e31d`.
- **Paths:** `scripts/castle_logo_studio.gd` and
  `scripts/probe_interaction.gd`.
- **Outcome / positive effect:** the saved logo replaces both painted purple
  shell banners in Craft and both in the Stuffie Playroom, keeps the Craft board
  badge, is input-transparent, and does not leak into unregistered rooms.
- **Possible negative effect / unknown:** overlay scale/alignment or z-order may
  be wrong at alternate aspects; user art can increase visual clutter; Castle
  remains spatial debt despite this Canvas overlay.
- **Dependencies and evidence:** interaction probe and full CI; two-aspect
  capture, save/re-entry, device touch, and owner review remain open.
- **Rollback:** `guarded_single` and the safest isolated material rollback in
  this ledger. Run `git revert --no-commit
  9e75e8e392d34b784b9899e7434cdf954fb0e31d`, stop on conflict, verify only the
  two named files changed, then run parser/lint, interaction/load/save,
  full CI, and before/after Castle captures.

### CHG-022 — `ad36ee9f` integration, conflict, workflow, and CRLF reconciliation

- **Source:** merge `ad36ee9ffe4eae4d5c4183d0546d775de0218213`
  with parents `7b5d1209063a22002118c364767d537b34b3dc6f` and
  `245c16137fae82271dabac456d5ab04d843463a8`.
- **Paths:** all 242 first-parent changed files; conflict authority centered on
  `.github/workflows/probes.yml`, `ASSET_LICENSES.md`, `scripts/ci.sh`, picture
  games, Opera career/2D/Nursery probes, and cross-platform
  `prepare_opera_minigame_art.py` plus its test; central audit/design docs.
- **Outcome / positive effect:** current upstream Opera, Ballerina, Boxer,
  Candymaker, Detective, Nursery, animation, music, and Castle-logo work is
  integrated without accepting the upstream device-only 3D kart. Local/remote
  static and trusted-probe coverage gains current Opera checks. Deterministic
  text comparison is CRLF/LF-stable while PNG bytes remain exact.
- **Possible negative effect / unknown:** this large merge can contain subtle
  behavioral or art regressions despite green probes; workflow changes are
  high-risk; 33,299 first-parent insertions make causal isolation difficult;
  remote exact-head and external acceptance gates remain open.
- **Dependencies and evidence:** every CHG-016–021 record, CHG-005/008/014,
  parser/lint/import/editor checks, deterministic art/music audits, focused
  Opera/audio probes, exact local full CI.
- **Rollback:** `whole_merge_only`. Never use the merge revert to undo one
  Ballerina pose, cue, widget, or workflow line. Use the owning CHG record for
  bounded rollback. The sole full-integration recovery is section 7.

### CHG-023 — Change-log and rollback process

- **Source:** pending introducing commit. A tracked file cannot contain its own
  Git object ID without a self-reference loop. After this file is committed,
  locate its immutable introduction anchor with `git log --diff-filter=A
  --format=%H -- audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md` and record
  that anchor in the next normal append-only audit synchronization. Until then,
  the planner deliberately refuses a CHG-023 inverse rather than guessing.
- **Paths:** this ledger, master audit, design index/architecture/open-work/
  ledger/design-language records, `.gitignore`, the read-only planner, and its
  tests.
- **Outcome / positive effect:** material work has stable IDs, explicit upside/
  downside, dependencies, evidence gaps, and bounded rollback paths; future
  regressions can be isolated without erasing audit history.
- **Possible negative effect / unknown:** the ledger can become stale or falsely
  imply reversibility if later commits change governed paths without adding a
  dependency entry. Commands are safeguards, not proof that an inverse remains
  clean.
- **Dependencies and evidence:** CHG-011 authority, current master audit/design
  language, clean UTF-8/table/fence/link/diff validation.
- **Rollback:** `documentation_migration`. Supersede with an additive dated
  ledger and update the document index. Never delete the historical mapping or
  reuse a `CHG-*` ID.

## 5. Per-group gate matrix

| Change IDs | Minimum focused gates before full CI | External gates that remain material |
|---|---|---|
| CHG-001, 003, 006, 013, 014 | Roshan/clipping, Lagoon/Seek/audit, visual unit+stress+fresh-strict | two-aspect Mobile capture, M11, child, owner art |
| CHG-002 | companion, stuffie, passive, load, save-recovery | child no-trap/re-entry |
| CHG-004 | voice, audio, Brawl, Nursery, Opera 2D, passive | protected-voice intelligibility and device mix |
| CHG-005, 008, 009 | parity stress/default, GAME2D unit+stress+default/regression, import | clean remote exact-head |
| CHG-007, 012 | mg2d/UI/rank/Dolls/passive, GAME2D | capture, device touch, child |
| CHG-010, 016–019 | Opera 2D, Nursery, Detective, gesture quality, passive, voice, teardown, animation/minigame-art audits | capture, device performance/touch, child, owner |
| CHG-015, 021 | Castle provenance builders/tests, interaction, load/save | Castle captures and owner review |
| CHG-020 | deterministic music check, audio, voice, picture games, Opera | two-wrap/ducking/off/mono/M11 listening |
| CHG-011, 023 | UTF-8, unique IDs, links, ledger coverage, table/fence and forbidden-claim checks | owner authority confirmation where changed |
| CHG-022 | every applicable gate above and exact `scripts/ci.sh` | remote exact-head plus all applicable external gates |

## 6. Required rollback record

Every attempted inverse appends a record; failed experiments remain evidence.

```yaml
rollback_attempt:
  change_id: CHG-000
  branch: codex/rollback-chg-000
  start_commit: <40-hex>
  source_commits: [<40-hex>]
  method: guarded_single | guarded_chain | guarded_mixed | archive_recovery_only
  reason: <falsifiable regression>
  expected_paths: []
  actual_paths: []
  protected_paths_changed: false
  conflicts: none | <exact paths>
  focused_gates: []
  full_ci: not_run | pass | fail
  remote_ci: not_run | pass | fail
  capture_device_child_owner: <explicit gaps>
  decision: abandon | keep_diagnostic | commit_candidate | accepted
  rollback_commit: null
```

## 7. Full-integration emergency fallback

The conventional all-or-nothing merge inverse is
`git revert -m 1 ad36ee9f`. It is **not** a per-change rollback tool. It discards
the entire second-parent integration relative to audit parent `7b5d1209`,
including positive Opera, art, music, Castle, probe, workflow, provenance, and
documentation changes.

Only use it for a confirmed integration-wide emergency on a clean
`codex/rollback-chg-022` branch. The inspection-first form is mandatory:

```powershell
git revert --no-commit -m 1 ad36ee9ffe4eae4d5c4183d0546d775de0218213
git status --short
git diff --stat
git diff --check
```

Stop on conflicts. Verify the diff is exactly the intended whole-integration
inverse, confirm protected paths remain unchanged, run every gate in section 5
and the complete exact-4.7.1 suite, then commit the recovery. Never push or
merge it until remote CI and every applicable external gate are green. If only
one change is objectionable, abort and use its `CHG-*` pathway instead.

## 8. Maintenance rule

Any later commit that materially changes one of these behaviors must append a
dated entry under the existing ID with its exact commit, path delta, new risks,
new evidence, and changed rollback dependency. It must not rewrite the original
record. A genuinely new behavior receives the next unused ID. This preserves a
reviewable history in which positive and negative outcomes can coexist without
either being hidden.

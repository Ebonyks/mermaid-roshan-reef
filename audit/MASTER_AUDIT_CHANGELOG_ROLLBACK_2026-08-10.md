# Mermaid Roshan master-audit change and rollback ledger

- **Ledger ID:** `MA-CHANGELOG-2026-08-10`
- **Change-ID namespace:** historical planner records `CHG-001` through `CHG-031`, with scoped review addition `CHG-032` below; IDs are permanent and
  are never reassigned or renumbered
- **Audit lineage:** `codex/master-audit-20260809`
- **Dedicated current audit branch:**
  `codex/sky-lagoon-canvas-repair-20260813`
- **Human scorecard and repository-version snapshot:**
  `a3d7580cbea2ba071364bae7dc3e727e3d1c1eb2`
- **Opera retirement and Canvas-lifecycle snapshot:**
  `e2c25878f6b9c64526d0686c426a9f29c5f1b3da`, with exact parent
  `41087f6634a416540b23a984d1f445b0bdab5f2f`
- **Castle-room Opera career-distribution snapshot:**
  `09e5e35665fd8d1bd782693e10fc0198f756d2c8`, with exact parent
  `f0b4f5e03fabbdcb3792f492f6cbd926afff0e2e`
- **Opera distribution probe-readiness repair snapshot:**
  `ff068db002202839f920a6f9fb78c942788a3034`, with exact parent
  `3fc151c8b3b6c054d0f6e6ab89f84a9f464f3f20`
- **Audit evidence and rollback-control synchronization snapshots:**
  `d991fdf3fbdb229de8685c3e52917b280942adb5`, with exact parent
  `ff068db002202839f920a6f9fb78c942788a3034`, followed by
  `9befc0f838f40eead2f42088a91206257fe217a8`
- **Fail-closed document-authority source chain:**
  `5ed0c75460c9afd5ab574ff2c4a907c1075964f0`, with exact parent
  `18b6150c01e1587100dca97c85ebad03f369825a`, followed by hardening source
  `7eb945957776ab3458a9de71c8be9937e2354720`, whose exact parent is
  `5ed0c75460c9afd5ab574ff2c4a907c1075964f0`. Exact official Godot 4.7.1
  local `scripts/ci.sh` is green at the first source in 1,359.8 seconds with all
  64 trusted probes; at that source checkpoint no direct full-local or remote
  result was recorded for hardening source `7eb94595`
- **Document-authority closure checkpoint:** CHG-023 maintenance
  commit `51887315bd537db2d16bdafcac1bbfa808352351`, exact parent `7eb94595`,
  passes official Godot 4.7.1 full local in 1,435.2 seconds/all 64 and exact-head
  Probe Suite run `31710377034`. That run's document static gate is 36 tests,
  six/six stress, 316/316 inventory/ledger, and then-current 36/36 active/
  records, all green. After `MA-DOC-002` and `MA-DOC-005` transition
  `VERIFIED_FIXED`, the current validator reports 34 active items and retains
  all 36 records
- **Sky Lagoon fail-closed capture-audit snapshot:**
  `7391c53cd6981a256bd8bfe40ccbb9f72fb723fe`, with exact parent and comparison
  baseline `e6edf559af219edd4e5ce38cab0c5094483be5c6`. Exact-source local
  `scripts/ci.sh` is green in 1,402.3 seconds/all 64 trusted probes; fresh local
  Mobile rendering is 20/20 PASS with 1,078/1,078 assertions. Exact-head Probe
  Suite run `31728755204` completes workflow-success at that SHA (probes 40m05s,
  63/63 trusted headings; music 3m38s, 42/42), but its non-blocking Sky step
  exits one after 20 PASS rows because the runner falls back to
  `gl_compatibility`; it is not a remote diagnostic PASS
- **Sky Lagoon true-Canvas promenade and touch-lifecycle snapshot:**
  `51d0abc0d32855a8ba32932599fedd8f59b398b7`, with exact single parent and
  comparison baseline `1b7d6bdaf89ebc7c9bdeae16fbde0e14079fd8a8`.
  Exact-source official-Godot local `scripts/ci.sh` is green in 1,404.5
  seconds/all 64 trusted probes. Separate local run-14 Mobile evidence is 20/20
  PASS at 1280x720 with no failed, skipped, or global row and unchanged save.
  Its manifest records `source_revision: unknown`; `AEAC7C72…DE34` binds the
  manifest and embedded PNG identities, while `B9EAF5E0…9C6C` binds the visual-
  probe script, not the full `51d0abc0` tree;
  no exact-source remote, matching APK, M11, child, owner, or release evidence
  is claimed
- **Sky Lagoon post-sealing integration-evidence checkpoint:** exact
  `441adf35f7dbdeb67d36fbf1a2217b87d3040d47` is a CHG-023 maintenance
  descendant, not a second CHG-031 source and not CHG-032. It passes exact-byte
  official-Godot local `scripts/ci.sh` in 1,391.5 seconds/all 64. Topic Probe
  Suite run `31760207048` succeeds at exact `441adf35` (probes 33m39s; music
  3m18s), and integrated-dev run `31762132976` succeeds at the same exact head
  (probes 33m39s; music 3m56s). Both retain 36 document-authority tests,
  six/six stress controls, 316/316 inventory/ledger, 34 active items and 36
  retained records, 63/63 remote trusted headings, 42/42 music checks, and zero
  hard workflow failures. Both raw Sky steps request Mobile but lack
  `VK_KHR_surface`, fall back through llvmpipe to `gl_compatibility`, record 20
  ordered PASS rows and `20/20/20/20` summary counts with zero failed and zero
  skipped, then emit
  `GLOBAL|FAIL|rendering_method|gl_compatibility` and `RESULT|FAIL` with exit
  one; the step is non-blocking, its artifact is PNG-only with no JSON, and it
  is not a remote Mobile diagnostic PASS. Android run `31763879294` records raw
  checkout and HEAD both at exact `441adf35`, then builds version 1414 for
  `dev`/`android-dev`; its
  596,033,220-byte APK has SHA-256
  `f04d0fef3b9bf097aa5b07e56e5726a1db9ff37e4be6ce35b495e31b9e4a72d8`,
  while the 82-byte sidecar has its own SHA-256
  `43e892cfb6c9a3847e1a8760d5cad4dd8fb36719d63db0625ec8b2fa3ba8e651`.
  M11 touch/performance, child play-test, owner acceptance, game-wide strict-2D
  closure, remote Mobile diagnostic PASS, and release acceptance remain open
- **Historical authority-head remote verification:** GitHub Actions run `31686380560`
  succeeds at exact `9befc0f838f40eead2f42088a91206257fe217a8`;
  machine-workflow success is not warning-clean or external/visual acceptance,
  and Sky Lagoon's uploaded diagnostic artifact internally fails
- **Current-dev reconciliation snapshot:**
  `f3b0de078898a8b4faddb2c738c4403180eff928`, with current-dev parent
  `ea6185fdb1a687a20a6d118bdc368400e2c30f60` and master-audit parent
  `5f58ef0a9db7aa9593f85131e1b855e51b84aea8`
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
- **Catalog inventory:** 31 permanent change IDs, 79 uniquely owned source-
  commit references, four guarded-script emitters, 27 manual/refusal groups,
  and 25 planner unit tests

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
snapshot: f3b0de078898a8b4faddb2c738c4403180eff928
evidence_snapshot: a3d7580cbea2ba071364bae7dc3e727e3d1c1eb2
opera_retirement_snapshot: e2c25878f6b9c64526d0686c426a9f29c5f1b3da
opera_distribution_snapshot: 09e5e35665fd8d1bd782693e10fc0198f756d2c8
opera_distribution_probe_fix_snapshot: ff068db002202839f920a6f9fb78c942788a3034
audit_evidence_rollback_sync_snapshot: d991fdf3fbdb229de8685c3e52917b280942adb5
audit_evidence_authority_sync_snapshot: 9befc0f838f40eead2f42088a91206257fe217a8
document_authority_snapshot: 5ed0c75460c9afd5ab574ff2c4a907c1075964f0
document_authority_hardening_snapshot: 7eb945957776ab3458a9de71c8be9937e2354720
document_authority_verification_checkpoint: 51887315bd537db2d16bdafcac1bbfa808352351
sky_lagoon_capture_audit_snapshot: 7391c53cd6981a256bd8bfe40ccbb9f72fb723fe
sky_lagoon_true_canvas_snapshot: 51d0abc0d32855a8ba32932599fedd8f59b398b7
sky_lagoon_true_canvas_integration_checkpoint: 441adf35f7dbdeb67d36fbf1a2217b87d3040d47
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
  - {id: CHG-015, name: cross-platform-generated-art-stability, rollback_mode: guarded_chain}
  - {id: CHG-016, name: opera-careers-atlases-and-minigame-art, rollback_mode: guarded_mixed}
  - {id: CHG-017, name: ballerina-specialist, rollback_mode: guarded_mixed}
  - {id: CHG-018, name: boxer-specialist, rollback_mode: guarded_single}
  - {id: CHG-019, name: candymaker-phone-fix, rollback_mode: guarded_single}
  - {id: CHG-020, name: deterministic-area-music, rollback_mode: guarded_mixed}
  - {id: CHG-021, name: castle-logo-personalization, rollback_mode: guarded_single}
  - {id: CHG-022, name: ad36-integration-reconciliation, rollback_mode: whole_merge_only}
  - {id: CHG-023, name: change-log-and-rollback-process, rollback_mode: documentation_migration}
  - {id: CHG-024, name: f3b0-current-dev-master-audit-reconciliation, rollback_mode: whole_merge_only}
  - {id: CHG-025, name: human-gamewide-scorecard-and-version-reconciliation, rollback_mode: documentation_migration}
  - {id: CHG-026, name: opera-boss-retirement-save-tombstones-and-canvas-lifecycle, rollback_mode: owner_blocked_mixed}
  - {id: CHG-027, name: castle-room-opera-career-distribution-and-direct-return, rollback_mode: owner_blocked_mixed}
  - {id: CHG-028, name: audit-evidence-and-rollback-control-synchronization, rollback_mode: documentation_migration}
  - {id: CHG-029, name: exhaustive-document-authority-and-canonical-finding-gate, rollback_mode: documentation_migration}
  - {id: CHG-030, name: fail-closed-sky-lagoon-promenade-capture-audit, rollback_mode: guarded_mixed}
  - {id: CHG-031, name: sky-lagoon-true-canvas-promenade-and-touch-lifecycle, rollback_mode: owner_blocked_mixed}
```

## 2. Safe rollback protocol

### 2.1 Non-negotiable preparation

Every experiment starts from a clean, catalog-pinned commit. Replace
`<change-id>` with the lowercase ID, for example `chg-021`, and replace
`<exact-start-from-plan>` with the exact start printed for that stable ID by
the planner. Do not assume one start SHA for every group.

```powershell
git status --short
git fetch origin --prune
python -B tools/plan_audit_rollback.py CHG-021
git switch -c codex/rollback-<change-id> <exact-start-from-plan>
git rev-parse HEAD
```

The current catalog pins CHG-024 to its exact two-parent reconciliation merge
`f3b0de078898a8b4faddb2c738c4403180eff928`. Its guarded script starts there
and recovers the exact current-dev parent tree. The catalog pins post-
integration CHG-005 and CHG-023 experiments to
`dacef1405b6a8cb470117e824aebac3a8ca500af`, which contains their recorded
follow-up commits. CHG-015 starts at its newer exact portability follow-up
`af4189a99cfd5a32d0df0f75185f6912d3889399`. Other groups remain pinned to
integration commit
`ad36ee9ffe4eae4d5c4183d0546d775de0218213`; in particular, the three emitted
CHG-020/021/022 scripts intentionally start there. CHG-025 starts at its exact
human-scorecard source commit `a3d7580cbea2ba071364bae7dc3e727e3d1c1eb2`.
CHG-026 starts at exact Opera product commit
`e2c25878f6b9c64526d0686c426a9f29c5f1b3da`; its planner entry records the
whole-commit diagnostic inverse but refuses to emit a script because save,
runtime, probes, the migration manifest, and authority documents are coupled.
CHG-027 starts at exact probe-repaired head
`ff068db002202839f920a6f9fb78c942788a3034`. It owns both the Castle-room
Opera distribution commit `09e5e35665fd8d1bd782693e10fc0198f756d2c8`
and the follow-up readiness repair. Its planner records a reverse-order,
two-commit diagnostic preview but refuses to emit a script because route,
save, reward, return, layer, probe, and migration-manifest ownership are
coupled.
CHG-028 starts at exact authority-sync commit
`9befc0f838f40eead2f42088a91206257fe217a8`. It owns the contiguous
rollback-control commit `d991fdf3fbdb229de8685c3e52917b280942adb5`
and authority-document follow-up `9befc0f838f40eead2f42088a91206257fe217a8`.
It is a manual documentation migration, not a raw two-commit revert or an
emitter.
CHG-029 starts at exact hardening head
`7eb945957776ab3458a9de71c8be9937e2354720`. It owns the contiguous first
document-authority source `5ed0c75460c9afd5ab574ff2c4a907c1075964f0`
and its hardening follow-up `7eb945957776ab3458a9de71c8be9937e2354720`.
It is a manual documentation migration over their exact 22-path union, not an
emitter.
CHG-030 starts at exact fail-closed capture source
`7391c53cd6981a256bd8bfe40ccbb9f72fb723fe`, whose exact parent and comparison
baseline is `e6edf559af219edd4e5ce38cab0c5094483be5c6`. It owns exactly the Sky
Lagoon capture probe and its synchronized GAME2D inventory entry. The planner
refuses an emitter because restoring the obsolete probe or only one of the two
paths would make evidence misleading or internally inconsistent.
CHG-031 starts at exact true-Canvas product source
`51d0abc0d32855a8ba32932599fedd8f59b398b7`, whose exact single parent and
comparison baseline is `1b7d6bdaf89ebc7c9bdeae16fbde0e14079fd8a8`.
It owns exactly the 19 catalogued runtime, touch, probe, and GAME2D paths. The
planner refuses an emitter because the Canvas route, one-finger touch and pause
lifecycle, return state, living-world layers, visual-evidence contract, and
strict-2D inventory must be repaired or reviewed as one safety-sensitive unit.
The planner output is the authority if a later append-only maintenance revision
changes this mapping.

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

Only CHG-020 and CHG-021, plus all-or-nothing CHG-022 and CHG-024, can emit a
script: four emitters across 31 stable IDs. The other 27 groups refuse
automation even when their human ledger mode says
`guarded_single`: shared-path, product-policy, or not-yet-committed context
still requires a reviewed manual inverse. Emitted scripts create a dedicated
branch at the exact start named by that record, run gates, and stop before
commit.

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
and 86 coverage gaps. Exact-head remote run `31457593351` is green, but no
complete Mobile acceptance matrix, Lenovo Tab M11 acceptance, intended-child
session, complete audio listening pass, protected-voice review, or owner
visual/identity acceptance closes those gaps. Every change record below
inherits these common gaps unless it says otherwise.

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
  `7b5d1209063a22002118c364767d537b34b3dc6f`; focused pinned music-verifier
  repair `dacef1405b6a8cb470117e824aebac3a8ca500af`.
- **Paths:** `scripts/ci.sh`, `.github/workflows/probes.yml`, probe-parity and
  grade-headroom tools/tests, plus the central audit/rollback checkpoint rows
  updated by the exact-head workflow repair.
- **Outcome / positive effect:** local and remote trusted-loop drift is detected
  rather than allowing CI to imply coverage it does not execute; Windows text
  encoding no longer creates a false grade failure; the downloaded Godot ZIP
  cannot be counted as active repository debt.
- **Possible negative effect / unknown:** legitimate display-only differences
  need explicit classification; loop expansion increases CI duration and a
  parser bug could block good work.
- **Dependencies and evidence:** parity unit/stress/default runs; current
  intended difference is the display-only human-art probe.
- **2026-08-10 follow-up checkpoint:** exact-head run `31456633826` at
  `fe10ffd2f36606eaad99e1e8881c1c84ffc5fa08` proves CHG-015's Opera
  repair green on Linux, then stops at the next static command because Ubuntu
  has no FFmpeg. The proposed CHG-005/020 repair moves only the deterministic
  music check to a parallel `windows-2025` job using pinned
  `actions/setup-python` commit `5fda3b95`, Python 3.13.14, NumPy 2.5.1,
  SciPy 1.18.0, and the existing checksum-pinned FFmpeg 8.1.2 installer. It
  removes no gate and changes no music or protected audio.
- **2026-08-10 verified follow-up:** introducing commit
  `dacef1405b6a8cb470117e824aebac3a8ca500af` completes exact-head GitHub run
  `31457593351` successfully in 34m19s. The Windows job passes 42/42 music
  deliveries; Ubuntu passes Opera 39/39, GAME2D 509/68/77
  `NO_REGRESSION`/`UNSATISFIED`, import, analyzer, all 62 trusted headless
  probes, boot, and balance. All capture/upload workflow steps complete and
  upload diagnostic artifacts; they are not visual passes. Parity default plus eight
  falsification cases are green and `PRB007` detects removal of either verifier.
- **Rollback:** `guarded_mixed`: these are coupled CI protections, and the current
  CI/workflow files were later reconciled by CHG-022. Inverse only the proven
  faulty sub-change, preserve the other two, and stop on shared-file conflict.
  For this focused verifier move, create a clean dedicated rollback branch at
  or after `dacef140`, run `git revert --no-commit
  dacef1405b6a8cb470117e824aebac3a8ca500af`, and inspect the four-file inverse
  before committing. A raw reversal deliberately restores the known
  Ubuntu-without-FFmpeg failure, so use it only to replace the verifier design,
  never to remove the 42-delivery gate.
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

### CHG-010 — Display/device Canvas Opera Racer and exact cue

- **Sources:** `82124b3a03426985afa9ff5d03447b8807d37f12`,
  and `e4528b27e2552f669de2b65c37da0243fb924eac`.
- **Paths:** Opera career world/2D probe and audio cue routing.
- **Outcome / positive effect:** normal display/device production UI and the
  forced-2D probe route use the Canvas Racer with `TUNE` → `TO THE LINE` →
  `RACE`, circle goal `0.9`, exact `op_racer_lap_two`, and no external kart
  child on that route. The display/device production selection cannot reach
  the legacy `_build_race` path.
- **Possible negative effect / unknown:** ordinary unforced headless startup
  still retains the legacy lobby/Racer route, and `opera_act.gd` can load
  `scripts/kart.gd` and attach its external kart child. This source/headless
  split remains open [MA-OPERA-010](MASTER_AUDIT_2026-08-09.md) and
  `MA-2D-002` debt; forced-2D probe success does not close it. On the Canvas
  route, circle recognition may also be too lenient or difficult on the phone.
- **Dependencies and evidence:** CHG-004 cue integrity, CHG-016 current career
  table, CHG-022 conflict resolution; Opera 2D/passive/voice/teardown probes,
  GAME2D, full CI. Ordinary-headless parity, device touch, child comprehension,
  capture, and owner feel remain open.
- **Rollback:** `guarded_chain`, but only for a Canvas-to-Canvas replacement.
  Refuse any revert that expands the retained legacy/external-kart path into
  display/device production UI. Reverse exact cue and Canvas-Racer commits only
  after a replacement owns the same save/lifecycle;
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

### CHG-015 — Castle and Opera cross-platform generated-art stability

- **Sources:** `df5b4cf7f98cd1ce09468b2551cd3bd5bb8ddf4c` and dependency-light
  test follow-up `5961fd968066e4644e2b77f73c72e990c4bef4ac`; Opera PNG portability
  follow-up `fe10ffd2f36606eaad99e1e8881c1c84ffc5fa08`; declared-text hashing
  follow-up `af4189a99cfd5a32d0df0f75185f6912d3889399`.
- **Paths:** Castle interaction manifest/approval ledger, delivery/native build
  tools and tests; Opera minigame-art generator/checker, focused tests, and its
  governed `PROVENANCE.json`/`REVIEW.md` evidence. The `af4189a9` inverse is
  exactly `assets_src/imagegen/opera_minigame_quality_2026-08-09/PROVENANCE.json`,
  `tools/prepare_opera_minigame_art.py`, and
  `tools/tests/test_prepare_opera_minigame_art.py`.
- **Outcome / positive effect:** deterministic Castle provenance checks are
  stable across Windows/Linux newline conventions. Opera's checker now accepts
  only a platform-dependent PNG `IDAT` recompression when CRC-checked PNG
  structure, non-`IDAT` chunks, color mode, dimensions, exact decompressed
  scanlines, and every decoded pixel are identical; provenance remains bound
  to the exact accepted delivery bytes.
- **Possible negative effect / unknown:** over-normalization could conceal a
  meaningful change. The relaxation is therefore limited to compression of an
  identical generated scanline stream; text meaning, metadata/chunks, color
  mode, dimensions, decoded pixels, and checked-in delivery hashes stay strict.
- **Dependencies and evidence:** Castle provenance builders/tests; Opera
  minigame-art unit/check-only gates with same-scanline/different-compression,
  pixel-drift, metadata-drift, mode-drift, invalid/trailing-payload PNG, CRLF,
  and semantic-text controls; full local and exact-head remote CI.
- **2026-08-10 follow-up checkpoint:** pushed process commit
  `57bc08d1220594fbabcab15362b5685a9f8514e6` exposed the defect in GitHub run
  `31455723446`: Linux stopped before import because valid PNG compression
  bytes differed from Windows for governed Opera outputs. The focused repair
  above passes locally for all 39 artifacts without rewriting any runtime PNG.
  Introducing commit `fe10ffd2f36606eaad99e1e8881c1c84ffc5fa08` then proves
  `CHECK OK: 39` on Linux in run `31456633826`; that run later fails at the
  separate missing-FFmpeg music gate recorded under CHG-005/020. This is exact
  focused evidence, not a green full-workflow or release claim.
- **2026-08-12 exact-head checkpoint and repair:** GitHub run `31648427712`
  passed all 42 deterministic music deliveries on Windows. Ubuntu static
  checking failed only because the checked-in Opera `PROVENANCE.json` retained
  the raw CRLF-checkout hash for the declared text input
  `assets_src/imagegen/opera_candymaker_syrup_2026-08-10/GENERATION.json`, while
  the Linux checkout supplied LF bytes. Commit `af4189a9` makes hashing
  LF-canonical only for that explicitly declared JSON text input; every binary
  input remains byte-exact. It refreshes the governed provenance and passes all
  10 focused `test_prepare_opera_minigame_art` tests plus a clean LF `git
  archive` check of all 42 deterministic Opera files. This repairs the isolated
  static false rejection; it does not turn failed run `31648427712` green or
  close any capture, device, child, audio-listening, or owner gate.
- **2026-08-12 replacement exact-head success:** GitHub run `31649113587` at
  exact commit `af4189a99cfd5a32d0df0f75185f6912d3889399` completed successfully.
  The Ubuntu probes job finished in 35m27s with static checks, import, analyzer,
  all 63 trusted probes, boot, balance, and the Opera manifest green. Five
  diagnostic capture/upload workflow steps completed and uploaded artifacts.
  The Windows music job finished in 3m55s with all 42 deliveries green. Those
  diagnostic captures prove that their CI
  collection/upload paths ran; they are not accepted visual evidence and do
  not close Mobile capture, device, child, audio-listening, protected-voice,
  identity/art, or owner-acceptance gates.
- **Rollback:** `guarded_chain`; attempt `5961fd96` then `df5b4cf7` only for a
  reproduced Castle false acceptance/rejection. Reverse Opera follow-up commit
  `fe10ffd2f36606eaad99e1e8881c1c84ffc5fa08` only on a dedicated rollback
  branch and only after reviewing conflicts from later workflow/log changes.
  To reverse the newer text-hash fix, start a clean dedicated branch at exact
  `af4189a99cfd5a32d0df0f75185f6912d3889399`, run `git revert --no-commit
  af4189a99cfd5a32d0df0f75185f6912d3889399`, and require the diff to contain
  exactly the three `af4189a9` paths named above. A raw inverse restores the
  known stale CRLF-sensitive provenance, so accept it only with a reviewed
  replacement that still keeps binaries byte-exact. Reverse the older
  checker's tests and generated review wording only when isolating its own
  defect; never regenerate or replace accepted delivery PNGs.
  Preserve delivery-hash strictness and run both Castle builders/checks, the
  focused `python -B -m unittest tools.tests.test_prepare_opera_minigame_art
  -v`, Opera 42-file check, interaction probe, cross-platform tests, and full CI.

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
- **Verifier environment:** the 42 deliveries remain provenance-bound to the
  original Windows render stack recorded in their manifest: Python 3.13.14,
  NumPy 2.5.1, SciPy 1.18.0, and FFmpeg 8.1.2. Remote verification therefore
  runs in the parallel checksum-pinned Windows job described in CHG-005 rather
  than falsely claiming an Ubuntu decoder reproduced the render toolchain.
  Exact-head run `31457593351` at `dacef140` proves this job green for all
  42 deliveries while the parallel Ubuntu gameplay/static job also succeeds.
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
  integrated without routing display/device production UI to the upstream
  device-only 3D kart. Local/remote static and trusted-probe coverage gains
  current Opera checks. Deterministic text comparison is CRLF/LF-stable while
  PNG bytes remain exact. Ordinary unforced headless retained a legacy
  lobby/Racer/kart source path, now explicitly open as `MA-OPERA-010`.
- **Possible negative effect / unknown:** this large merge can contain subtle
  behavioral or art regressions despite green probes; workflow changes are
  high-risk; 33,299 first-parent insertions make causal isolation difficult;
  external acceptance gates remain open.
- **Dependencies and evidence:** every CHG-016–021 record, CHG-005/008/014,
  parser/lint/import/editor checks, deterministic art/music audits, focused
  Opera/audio probes, exact local full CI.
- **Rollback:** `whole_merge_only`. Never use the merge revert to undo one
  Ballerina pose, cue, widget, or workflow line. Use the owning CHG record for
  bounded rollback. The sole full-integration recovery is section 7.

### CHG-023 — Change-log and rollback process

- **Source:** introduction commit
  `57bc08d1220594fbabcab15362b5685a9f8514e6`. Later append-only evidence
  synchronizations, self-hash updates, and count-only updates normally remain
  CHG-023 maintenance and do not create new product change IDs merely to
  record their own otherwise self-referential hashes. CHG-028 is the narrow
  material exception for its executable planner/test change and contiguous
  ten-path authority synchronization. CHG-029 separately owns the later
  contiguous two-source fail-closed document-authority/hardening chain. The
  post-`7eb94595` catalog/count update that records its exact second-source hash
  and boundary, exact verification checkpoint
  `51887315bd537db2d16bdafcac1bbfa808352351`, and this later terminal-lifecycle
  synchronization remain CHG-023 maintenance rather than a third CHG-029
  source or part of CHG-030. CHG-030 separately owns the later material
  executable-probe/GAME2D-manifest source `7391c53c`; this catalog/planner/prose
  update remains CHG-023 maintenance and does not recursively own itself.
  Routine future bookkeeping remains CHG-023 and does not recursively catalog
  its own prose-sync hash.
- **Paths:** this ledger, master audit, canonical findings register, design
  index/game-design/architecture/open-work/ledger/design-language records,
  `.gitignore`, the read-only planner, and its tests.
- **Outcome / positive effect:** material work has stable IDs, explicit upside/
  downside, dependencies, evidence gaps, and bounded rollback paths; future
  regressions can be isolated without erasing audit history.
- **Possible negative effect / unknown:** the ledger can become stale or falsely
  imply reversibility if later commits change governed paths without adding a
  dependency entry. Commands are safeguards, not proof that an inverse remains
  clean.
- **Dependencies and evidence:** CHG-011 authority, current master audit/design
  language, clean UTF-8/table/fence/link/diff validation. Exact maintenance
  checkpoint `51887315`, parent `7eb94595`, changes 11 documentation/planner
  paths with 298 insertions/213 deletions and no runtime or workflow path. It
  passes official Godot 4.7.1 full local in 1,435.2 seconds/all 64 and exact-head
  run `31710377034`: Ubuntu 41m12s, trusted loop 18m02s/63 headings, document
  gate 36 tests/six stress/316/316/36/36 ALL OK, and Windows 42/42 ALL OK in
  4m08s. After the two terminal transitions, the current validator reports 34
  active items and retains all 36 records. Raw Sky Lagoon remains 21 OK/44
  FAIL/one DONE and non-authoritative;
  runner warnings, legacy resource diagnostics, APK, and external gates remain.
- **Rollback:** `documentation_migration`. On a clean dedicated branch at or
  after the introduction anchor, preview `git revert --no-commit
  57bc08d1220594fbabcab15362b5685a9f8514e6`; stop on any overlap with later
  CHG-023 maintenance. Keep a copy of this ledger outside the worktree, preserve
  any still-required rollback evidence, and confirm the inverse does not alter
  runtime, protected assets, save schema, authority, or workflow security.
  Prefer superseding the ledger/tool over deleting the audit trail, and never
  reuse a `CHG-*` ID.

### CHG-024 — `f3b0de07` current-dev master-audit reconciliation

- **Source:** merge `f3b0de078898a8b4faddb2c738c4403180eff928` with
  current-dev parent `ea6185fdb1a687a20a6d118bdc368400e2c30f60` (mainline 1)
  and master-audit parent
  `5f58ef0a9db7aa9593f85131e1b855e51b84aea8` (parent 2).
- **Paths:** all 522 first-parent changed files. The merge imported the master
  audit documents, 2D audit/toolchain, generated evidence, provenance, and
  intentional archived-resource removals into current dev. It also reconciled
  current Opera, Castle, CI, and cross-platform tooling. The planner records
  the complete top-level path family; the exact first-parent Git delta is the
  file authority. No source delta exists below `assets/book/`,
  `assets/audio/voices/`, or `assets/characters/friends/`.
- **What changed, in plain English:** the old audit did not replace the newer
  game work. Newer borderless/diegetic Opera rooms, Candymaker, Ballerina, and
  Boxer revisions were preserved. Normal display/device production UI kept the
  Canvas three-phase Racer and exact cue, and cannot reach legacy
  `_build_race`. However, ordinary unforced headless still retains the legacy
  lobby/Racer route and can load `scripts/kart.gd`; CHG-024 did **not** remove
  that source/headless split, which remains open
  [MA-OPERA-010](MASTER_AUDIT_2026-08-09.md). The V2 Castle personalized-logo
  banners now render as Canvas `Control`/`TextureRect` content instead of
  `Node3D`/`Sprite3D`. Remote CI now runs the diegetic path probe and both
  borderless/diegetic static art gates. GAME2D text-sidecar fingerprints treat
  LF and CRLF checkouts identically while still detecting semantic edits.
  Nursery and Racer probes now sample their intended live states, so they prove
  the open-task idle reprompt and live Canvas-finale separation instead of
  relying on stale or post-close state.
- **Outcome / positive effect:** one exact merge now carries the central audit,
  retired-resource evidence, bounded Canvas conversions, current game work,
  and local/remote coverage forward together. It avoids silently regressing
  Candy/Ballerina/Boxer/diegetic Opera while preserving the display/device
  Canvas Racer and removing the V2 Castle banner 3D nodes. It does not certify
  ordinary-headless medium parity.
- **Possible negative effect / unknown:** this is a very broad change (522
  first-parent files, 44,758 insertions, and 15,377 deletions). It deliberately
  removes retired GLB/source/tool content from active repository paths, so a
  whole inverse would put that debt back. Green machine checks cannot prove
  child comprehension, owner art/identity acceptance, phone layout, touch,
  performance, audio mix, or every subtle behavior. The strict visual audit
  remains `UNSATISFIED`, and the ordinary-headless legacy Opera kart lifecycle
  remains open; this entry is reconciliation evidence, not a claim that the
  game-wide audit or final-2D migration is complete.
- **Evidence at the merge:** exact Godot
  `4.7.1.stable.official.a13da4feb` `scripts/ci.sh` exited 0 after 1,437.1
  seconds with all 64 trusted local probes green. Machine checks also passed
  74 GAME2D unit tests plus 14 falsification controls, 93 visual-contract
  tests, all 42 music deliveries, 42 deterministic Opera minigame files, and
  13 career atlases/208 frames. The local transcript was
  `tmp/audit_reconcile_full_ci_final.log` (ephemeral evidence, not a governed
  rollback path). Exact-head remote CI was still pending at this checkpoint.
- **Rollback:** `whole_merge_only`, and only for a confirmed integration-wide
  regression. On a clean, dedicated branch created at exact `f3b0de07`, use
  `git revert --no-commit -m 1
  f3b0de078898a8b4faddb2c738c4403180eff928`. This removes the **entire** audit
  reconciliation, including its useful Canvas/CI/tooling work, and reverses
  intentional archive removals. It cannot be combined with an individual
  CHG-001–023 inverse or mined for selected paths. Treat any restored retired
  resource as unapproved diagnostic content, not production art. The planner
  verifies the exact start, exact two parents, mainline 1, exact selected-parent
  tree, and absence of protected paths before and after the inverse. Stop on
  any mismatch or conflict, rerun every focused and exact-4.7.1 full gate, then
  require remote exact-head CI and applicable external acceptance before any
  rollback commit can move forward.

### CHG-025 — Human game-wide scorecard and repository-version reconciliation

- **Source:** `a3d7580cbea2ba071364bae7dc3e727e3d1c1eb2`.
- **Paths:** the master audit, this rollback ledger, design index/architecture/
  open-work/ledger/design-language documents, the read-only rollback planner,
  and its tests. These are the exact nine paths changed by the source commit;
  no runtime, save, workflow, protected source, generated art, or audio path is
  part of CHG-025.
- **What changed, in plain English:** the master audit gained a consistent 1–5
  rubric; human-readable scorecards for whole-game systems, worlds, every
  non-Opera activity, all 13 current Opera careers, and the three boss acts;
  and a repository-version comparison that separates integrated runtime,
  historical versions, docs-only proposals, dirty worktree candidates, shared-
  SHA aliases, and rescue refs. It explicitly explains that Seek/Lamb-a' was
  rebuilt as a bounded animated Canvas activity rather than importing the old
  3D game wholesale. It identifies the reconciled `f3b0de07` plus `af4189a9`
  line as the best audited base while quarantining the promising but
  pre-audit `20e9b1f2` animation-doubling branch from wholesale integration.
  The same commit also synchronized current local/remote evidence and the
  preceding CHG-024/CHG-015 control record.
- **Outcome / positive effect:** a human can now see what improved, what may
  have regressed, why no area is rated 5/5, which Opera version is actually
  implemented, and what should happen next without reconstructing dozens of
  branches or machine-only findings. Every material row points back to stable
  `CHG-*`, `MA-*`, commit, or branch evidence instead of presenting preference
  as release proof.
- **Possible negative effect / unknown:** 1–5 ratings contain bounded human
  judgment and can become stale when Painter, Arborist, animation-doubling, or
  another product branch advances. A reader could still mistake “best current
  base” for release approval if the explicit `UNSATISFIED` and external-gate
  warnings are removed. The scorecard does not itself test an APK, child,
  device, owner acceptance, listening quality, or visual identity.
- **Dependencies and evidence:** CHG-005, CHG-011, CHG-015, CHG-023, and
  CHG-024; exact `af4189a9` remote success run `31649113587`; exact f3 local
  64-probe evidence; GAME2D `509/68/77` `NO_REGRESSION / UNSATISFIED`;
  19 rollback-planner tests; Opera generated-art 10-test/42-file checks; probe
  parity; Markdown UTF-8/fence/table/link validation; and independent
  adversarial review of the ratings and branch facts.
- **Rollback:** `documentation_migration`. Start a clean branch at exact
  `a3d7580cbea2ba071364bae7dc3e727e3d1c1eb2`, run
  `python -B tools/plan_audit_rollback.py CHG-025`, and inspect
  `git show --stat --summary a3d7580cbea2ba071364bae7dc3e727e3d1c1eb2`.
  The planner intentionally refuses `--emit-script`. Do not erase the audit
  trail or raw-revert the whole commit over later evidence. Correct a disputed
  rating or branch fact with a superseding record, or construct a reviewed
  inverse limited to the exact documentation/control paths while preserving
  still-valid CHG-015/024 evidence. Rerun the full current planner suite (23 tests), document
  validation, probe parity, GAME2D regression, and `git diff --check` before
  recording any inverse.

### CHG-026 — Opera boss retirement, stable save tombstones, and unified Canvas lifecycle

- **Source and exact boundary:** product commit
  `e2c25878f6b9c64526d0686c426a9f29c5f1b3da`, whose single parent is
  `41087f6634a416540b23a984d1f445b0bdab5f2f`. Its first-parent delta is exactly
  32 files (1,648 insertions and 10,548 deletions). `git diff-tree` parity was
  checked against the planner path set; none of the 32 paths is under a
  protected-original directory.
- **Paths:** the exact 32-path scope is
  `audit/MASTER_AUDIT_2026-08-09.md`;
  `design/00_MASTER_INDEX.md`; `design/01_GAME_DESIGN.md`;
  `design/03_TECHNICAL_ARCHITECTURE.md`; `design/04_OPEN_WORK.md`;
  `design/05_DOC_LEDGER.md`; `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`;
  `scripts/hit_engine.gd`; `scripts/kart.gd`; `scripts/living_world.gd`;
  `scripts/living_world_catalog.gd`; `scripts/main.gd`;
  `scripts/opera_act.gd`; `scripts/opera_house.gd`;
  `scripts/opera_lobby_2d.gd`; `scripts/player.gd`;
  `scripts/probe_audio.gd`; `scripts/probe_castle_pearl_art.gd`;
  `scripts/probe_imp_animation_art.gd`; `scripts/probe_living_world.gd`;
  `scripts/probe_load.gd`; `scripts/probe_opera.gd`;
  `scripts/probe_opera_2d.gd`; `scripts/probe_opera_2d_balance.gd`;
  `scripts/probe_opera_art.gd`; `scripts/probe_opera_balance.gd`;
  `scripts/probe_opera_detective.gd`; `scripts/probe_opera_nursery.gd`;
  `scripts/probe_save_recovery.gd`; `scripts/probe_ui_system.gd`;
  `scripts/save_state.gd`; and `tools/game_2d_migration_manifest.json`.
- **What changed, in plain English:** owner authority cut Curtain Dragon,
  Shadow Phantom, and Midnight Maestro from the Opera. Their historical save
  positions were not deleted or reassigned: the 16-slot `ACTS` table remains
  stable, slots 4, 9, and 14 are permanent tombstones, and live careers remain
  at indices 0–3, 5–8, 10–13, and 15. The three retired bits form mask
  `0x4210`; the 13 live bits form `0xBDEF`. `opera_stars` preserves the complete
  raw 16-bit legacy mask, including old retired-only bits and `0xFFFF`, while
  effective `opera_progress` counts only live bits and caps at 13. Completion
  requires every bit in `0xBDEF`; neither old boss stars nor a sparse legacy
  progress value is allowed to shift or manufacture career credit.
- **Canvas and world lifecycle:** the production display route and ordinary
  unforced headless route now use the same Canvas lobby and Canvas career
  wrapper. The 13 live careers appear as picture cards on 4/4/5 pages with 13
  progress pearls; no boss card, finale gate, boss music, boss voice, or legacy
  kart route is reachable. Invalid/tombstone starts fail closed without taking
  visibility ownership. Earned results commit before a curtain-call leave or
  application pause, and teardown restores player, touch UI, and area music.
  Living-world boss entries were removed while the Nursery career at slot 15
  remains live. Ember's henchmen remain separately planned future story
  bosses; this change does not repurpose the three retired Opera slots for
  them.
- **Outcome / positive effect:** the owner-cut bosses can no longer leak back
  through headless behavior, a finale card, ambient routing, or a stale save.
  The much smaller lifecycle removes the duplicate legacy 3D lobby/boss/kart
  implementation while retaining all 13 approved career games and their
  existing art. Old saves keep their raw evidence and gain deterministic live
  progress instead of losing bits or crediting the wrong career. Focused probes
  now exercise real card taps, all 13 routes, no-idle-award behavior, first-win
  and replay rewards, completion exactly once, save migration, suspend/leave
  persistence, teardown, and re-entry.
- **Possible negative effect / unknown:** the intentionally preserved raw mask
  can look surprising because a save may contain retired bits that no longer
  count toward progress. A later editor must not compact the table, reuse
  slots 4/9/14, clear raw retired bits, or redefine `ALL_STARS` as `0xFFFF`.
  The current centralized three-page picker is still a transitional layout:
  owner direction ultimately distributes careers into Castle rooms and leaves
  only Ballerina, Pop Star, and Magician in the Opera Hall. That unresolved
  architecture remains P1 [MA-OPERA-012](MASTER_AUDIT_2026-08-09.md). Green
  machine checks do not prove M11 performance/touch, child comprehension,
  owner art acceptance, or release readiness; broad transitive 3D debt and the
  game-wide visual audit remain open.
- **Dependencies and coupling:** CHG-005, CHG-008, CHG-010, CHG-011, CHG-015,
  CHG-016, CHG-017, CHG-018, CHG-019, CHG-020, CHG-023, CHG-024, and CHG-025.
  In particular, this commit supersedes CHG-010's remaining ordinary-headless
  split, consumes the current 13-career/atlas/music work, updates the CHG-008
  shrink manifest, and synchronizes the master-audit authority built through
  CHG-024/025. It does not close MA-OPERA-012.
- **Evidence at the product commit:** exact Godot
  `4.7.1.stable.official.a13da4feb` `scripts/ci.sh` exited 0 after 1,428.6
  seconds with all 64 trusted local probes green. The current GAME2D inventory
  is 509 models, 66 production files, and 74 probe files; default remains
  `UNSATISFIED`, regression is `NO_REGRESSION`, and all 14 stress controls
  passed. Parser, inference lint, import/analyzer, focused Opera/load/recovery/
  living-world/audio/UI probes, 42 deterministic music deliveries, and the
  42-file Opera art gate passed. A Mobile-renderer 1280×720 run produced 17
  fresh diagnostic captures with zero capture stderr and no boss cards. The
  strict global visual result remains `UNSATISFIED` (`FAIL 16`, `REVIEW 17`,
  `MANUAL 2`, `GAP 86`, `PASS 32`, `NA 94`). Follow-up audit/rollback commit
  `e0677ae4c4f5e48258ff57c38f82e25f2dc3d9d0` then passes exact-head GitHub
  run `31661887863`: Ubuntu completes static gates, import, the full analyzer,
  all 63 remote trusted probes, boot, both balance advisories, the Opera
  manifest, and five diagnostic capture/upload pairs in 33m8s; pinned Windows
  music completes 42/42 in 6m52s. Those captures are review aids, not accepted
  visual evidence. MA-OPERA-010 and MA-OPERA-011 remain fixed pending device,
  child, owner, and authoritative visual verification; MA-OPERA-012 remains
  open.
- **Rollback:** `owner_blocked_mixed`; the planner is deliberately `MANUAL` and
  refuses `--emit-script`. For an isolated diagnostic only, begin with a clean
  tree and create `codex/rollback-chg-026` at exact
  `e2c25878f6b9c64526d0686c426a9f29c5f1b3da`. After confirming its parent and
  exact 32-path delta, preview only `git revert --no-commit
  e2c25878f6b9c64526d0686c426a9f29c5f1b3da`. Stop on any conflict, unexpected
  path, protected original, removed save key, tombstone reindexing, or mismatch
  with the exact parent tree. The inverse restores owner-cut boss routing and
  legacy lifecycle debt, so it is not production-approved. Inspect all coupled
  IDs and the entire staged inverse, then rerun every focused gate, GAME2D
  default/regression/stress, diagnostic captures, exact-4.7.1 full CI, and
  remote exact-head CI before any rollback commit is considered. Never apply
  this raw inverse over a later branch head or split the save/runtime/document
  portions into independent reversions.

### CHG-027 — Castle-room Opera career distribution and direct return lifecycle

- **Sources and exact boundary:** product commit
  `09e5e35665fd8d1bd782693e10fc0198f756d2c8`, whose single parent is
  `f0b4f5e03fabbdcb3792f492f6cbd926afff0e2e`. Its first-parent delta is
  exactly 15 paths (1,144 insertions and 1,333 deletions). Follow-up probe-
  readiness commit `ff068db002202839f920a6f9fb78c942788a3034`, whose single
  parent is `3fc151c8b3b6c054d0f6e6ab89f84a9f464f3f20`, changes only the already-
  owned `scripts/probe_opera.gd` (30 insertions and one deletion). The two
  owned deltas therefore retain an exact 15-path union. Both deltas and their
  union were checked with `git diff-tree`; none is below a protected-original
  directory.
- **Paths:** the exact 15-path scope is new
  `scripts/castle_career_routes.gd`; modified `scripts/living_world.gd`,
  `scripts/living_world_catalog.gd`, `scripts/main.gd`,
  `scripts/opera_career_world_2d.gd`, `scripts/opera_house.gd`,
  `scripts/pause_menu.gd`, `scripts/probe_castle_pearl_art.gd`,
  `scripts/probe_living_world.gd`, `scripts/probe_opera.gd`,
  `scripts/probe_opera_2d.gd`, `scripts/probe_opera_art.gd`,
  `scripts/probe_ui_system.gd`, and
  `tools/game_2d_migration_manifest.json`; plus deleted
  `scripts/opera_lobby_2d.gd`.
- **What changed, in plain English:** the three-page 4/4/5 all-career Opera
  picker was removed. There is no generic picker route or hidden direct-launch
  backdoor. Thirteen large picture cards now live in nine themed Castle rooms:
  Kitchen has Chef (slot 0) and Candymaker (3); Opera Hall has exactly
  Ballerina (2), Pop Star (13), and Magician (8); Library has Detective (1);
  Craft Room has Painter (10); Playroom has Doctor (5) and Boxer (7); Bubble
  Bath has Nursery Nurse (15); Mermaid Pool has Astronaut Engineer (11);
  Dining Room has Farmer (6); and Movie Lounge has Racer (12). The old Opera
  Hall stage action now only focuses the next room-owned picture; it cannot
  launch a second all-career surface.
- **Launch, return, and child-safety ownership:** a card can launch only while
  its recorded room is the current visible Castle owner. A mismatched room,
  retired slot, duplicate start, hidden room, or programmatic call fails
  closed. A valid card suspends that room, starts exactly one existing Canvas
  career, and records that same room for cancel, neutral pause exit, ordinary
  curtain completion, replay, application pause, teardown, and failed-start
  restoration. Each successful first play still owns its existing star bit
  and three-pearl reward; a replay still awards one pearl; all-live completion
  still awards its one-time 50-pearl/sticker result. Idle cards and rejected or
  cancelled starts cannot manufacture stars or pearls.
- **Save and retirement semantics:** this is a navigation/lifecycle change,
  not a save migration. `opera_stars` remains a raw 16-bit namespace. The 13
  live slots still form `0xBDEF`; retired slots 4, 9, and 14 still form
  `0x4210` and remain permanent raw-preserving tombstones. No bit, save key,
  completion condition, effective-progress rule, or reward identity was
  removed or reindexed. The room route is transient runtime state and is not
  allowed to rewrite historical star positions.
- **Layer, caption, pause, and living-world ownership:** the visible Castle
  cutaway remains opaque layer 14, its current-room living-world accents use
  layer 15, and the phone pause affordance stays reachable on layer 16. Inside
  a career, the opaque activity owns layer 10, living-world accents layer 11,
  the existing HUD/missing-voice caption layer 12, and pause layer 13. An open
  pause sheet rises to 29 below the transition fade at 30. HUD visibility and
  its previous layer, player visibility, objective-card visibility, camera,
  room music, and current room are captured and restored. Living-world stage
  identity now follows the visible `castle_room_id`, not the hidden legacy
  world-player coordinate; a live career reports only its stable act stage.
- **Outcome / positive effect:** navigation now matches the owner-directed
  storybook geography. A non-reader discovers a career beside a recognizable
  room and character picture, plays one activity, and returns to the place
  they touched. Opera Hall is a real three-career venue instead of a disguised
  menu for every job. Reusing the accepted 13 Canvas careers, sparse save bits,
  crests, actor art, and rewards avoided an unnecessary art or gameplay
  redesign. Exact route guards and teardown coverage also make wrong-room,
  passive, pause, and re-entry behavior more explicit than the removed hub.
- **Possible negative effect / residual issue:** the room routes are a shared
  overlay rather than individually composed diegetic props.
  **Residual P2 card overlap/occlusion:** the lower-center row of one to three
  154×154 cards visibly obscures Roshan's
  lower body or tail in reviewed room captures and can also cover, crowd, or
  compete with furniture, walk-space composition, or other affordances. The 22
  reviewed
  diagnostics show the current layouts and no blocking failure was found, but
  they do not turn this known composition risk into a visual pass. Fix it with
  bounded per-room card anchors/avoidance and renewed captures; do not restore
  the rejected hub. The Opera Hall's large stage action is now a guide to the
  pictures and may feel redundant. No new protected family voice was created;
  Racer still exercises the missing-recording fallback, so existing speech and
  the readable layer-12 caption carry accessibility where exact voice is absent.
  Neither machine checks nor screenshots establish M11 touch/
  performance, child comprehension, owner approval, or release readiness.
- **Dependencies and coupling:** CHG-005, CHG-008, CHG-010, CHG-011, CHG-015,
  CHG-016, CHG-017, CHG-018, CHG-019, CHG-020, CHG-023, CHG-024, CHG-025, and
  CHG-026. In particular, the distribution consumes CHG-026's 13-live-career
  Canvas/save baseline and closes the central-picker architecture it left open;
  it does not reopen or repurpose the three retired boss slots. Route code,
  shared main state, living-world catalog, pause/HUD layering, Opera lifecycle,
  probes, and the shrink-only GAME2D manifest therefore form one review unit.
- **Failed remote run and exact root cause:** GitHub Actions run `31678156887`
  at pre-fix head `3fc151c8b3b6c054d0f6e6ab89f84a9f464f3f20` passed import, static checks,
  the analyzer, and the surrounding career/lifecycle coverage, but the trusted
  Opera probe reported exactly
  `OPERA|detective starts only its stable Canvas career: FAIL` and
  `OPERA|nursery starts only its stable Canvas career: FAIL`, then
  `OPERA|result: 2 check(s) FAILED`. Raw viewport-touch launch, passive safety,
  save/reward, exact-room return, Opera 2D, all 2,247 diegetic-path checks, the
  Detective, Nursery, and Pipe probes, and all 273 gesture-quality checks were
  green. At that failed head, the compound stable-Canvas assertion was
  `scripts/probe_opera.gd:282–293`; its stale term at line 287 required living-
  world layer 11 after `_start_via_room_touch()` had waited only four frames
  at `scripts/probe_opera.gd:379–398` (the wait was line 390). Production starts
  the activity synchronously beneath the reveal, but `scripts/main.gd:3318`
  gives that reveal 0.25 seconds and `scripts/living_world.gd:269` deliberately
  suspends its layer change while fade alpha exceeds 0.02. Runner-dependent
  fast frames could therefore still observe the previous Castle layer 15.
  This was a probe-sampling defect, not evidence of a production launch,
  lifecycle, save, or return defect. Boot/capture work correctly remained
  skipped after the trusted-probe failure; the historical run remains red.
- **Probe-readiness repair and exact-head local evidence:** follow-up
  `ff068db002202839f920a6f9fb78c942788a3034` replaces the four-frame guess
  with bounded `_await_route_ready()` evidence. Its 120-frame limit waits for
  the Opera instance, completed and input-transparent reveal, exact
  `opera.act.NN` living-stage identity, and career living-world layer 11; a
  timeout prints the observed act, stage, layer, and fade instead of silently
  sampling too early. It changes no production runtime file or behavior. At
  this exact repaired head, official Godot `4.7.1.stable.official.a13da4feb`
  full local `scripts/ci.sh` exited 0 after 1,379.3 seconds with all 64 trusted
  local probes green. This local pass does not erase run `31678156887` or
  retroactively make it green. Later exact authority head `9befc0f8`, which
  preserves these runtime/probe bytes, passes remote run `31686380560`; that
  successor-head evidence is recorded under CHG-028.
- **Evidence at the product commit:** exact official Godot
  `4.7.1.stable.official.a13da4feb` full local `scripts/ci.sh` exited 0 after
  1,463.4 seconds with all 64 trusted local probes green. Parser, inference
  lint, import, full analyzer/check-only, focused Opera/Opera-2D/living-world/
  UI/load and surrounding lifecycle probes passed. A Mobile-renderer run
  produced 22 fresh 1280×720 diagnostic captures: nine Castle-room route views
  and thirteen direct career views. They are diagnostic/review aids, not
  target-device, child, owner, or authoritative visual acceptance. GAME2D is
  exactly 509 models, 66 production files, and 74 probe files; default remains
  `UNSATISFIED`, regression gate remains `NO_REGRESSION`, and stress is green.
  The residual P2 card overlap/occlusion above and the broader 2D/visual debt
  remain open despite the green local gate.
- **Rollback:** `owner_blocked_mixed`; the planner is deliberately `MANUAL` and
  refuses `--emit-script`. For diagnosis only, start a clean isolated
  `codex/rollback-chg-027` branch at exact
  `ff068db002202839f920a6f9fb78c942788a3034`, verify both owned commit-parent
  pairs and their exact 15-path union, then preview the owned commits in reverse
  order: first `git revert --no-commit
  ff068db002202839f920a6f9fb78c942788a3034`, then `git revert --no-commit
  09e5e35665fd8d1bd782693e10fc0198f756d2c8`. The intervening audit-document
  commits are not owned by CHG-027 and must not be swept into its inverse. Stop
  on any conflict, unexpected path, protected original, save-key change, bit
  reindexing, reward change, layer inversion, wrong-room return, lost bounded-
  readiness evidence, or parent-tree mismatch. Inspect the exact 15-path union
  together. The raw inverse restores the rejected all-career hub, deletes the
  owner-directed room routes, and removes the probe-readiness repair, so it is
  not production-approved and must never be automated or applied over a later
  head. Prefer a narrow fix to a specific P2 card anchor or lifecycle defect.
  Before any candidate inverse,
  rerun planner tests, parser/lint, probe parity, GAME2D default plus exact
  `python -B tools/audit_game_2d.py --regression-gate` and stress, the focused
  route/save/reward/layer probes, diagnostic captures, and exact Godot 4.7.1
  full CI; then obtain the still-missing device, child, owner, and authoritative
  visual decisions.

### CHG-028 — Audit evidence and rollback-control synchronization

- **Sources and exact boundary:** rollback-control synchronization commit
  `d991fdf3fbdb229de8685c3e52917b280942adb5` has exact parent
  `ff068db002202839f920a6f9fb78c942788a3034` and changes three paths with 112
  insertions and 27 deletions. Contiguous authority synchronization commit
  `9befc0f838f40eead2f42088a91206257fe217a8` has exact parent
  `d991fdf3fbdb229de8685c3e52917b280942adb5` and changes seven different paths
  with 223 insertions and 110 deletions. Their combined first-parent boundary is
  therefore an exact 10-path union with 335 insertions and 137 deletions.
- **Paths:** `audit/MASTER_AUDIT_2026-08-09.md`;
  `audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md`;
  `design/00_MASTER_INDEX.md`; `design/01_GAME_DESIGN.md`;
  `design/03_TECHNICAL_ARCHITECTURE.md`; `design/04_OPEN_WORK.md`;
  `design/05_DOC_LEDGER.md`;
  `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`;
  `tools/plan_audit_rollback.py`; and
  `tools/tests/test_plan_audit_rollback.py`. No runtime, scene, resource, save,
  workflow, asset, generated-art, audio, or protected-original path is present.
- **What changed, in plain English:** the first commit materially updated the
  executable read-only rollback planner and its tests so CHG-027 owns both the
  Opera distribution runtime and probe-readiness repair, starts diagnostic
  rollback review from the repaired head, retains the exact 15-path union, and
  continues to refuse automation. It also expanded the central ledger with the
  failed-run cause and fixed-head local evidence. The second commit propagated
  those facts through the current master audit and six design authorities:
  product runtime and probe/evidence head are distinguished; remote run
  `31678156887` remains genuinely red; the fixed four-frame probe sample and
  0.25-second reveal are named as the cause; the 1,379.3-second/all-64 local
  repaired-head result remains local. At the source boundary, replacement
  remote/APK, device, child, owner, voice, visual, listening, strict-2D, and P2
  card-composition gates were open. The later exact-head run below closes only
  the remote machine-workflow item; neither source changes the game.
- **CHG-023 policy boundary:** routine append-only self-hash, source-count, or
  catalog-count maintenance remains CHG-023 and does not earn a new stable ID.
  CHG-028 is a narrow exception because `d991fdf3` materially changed the
  executable planner/tests and `9befc0f8` synchronized the resulting authority
  state across ten governed paths. Recording CHG-028 and its future routine
  count/hash upkeep remains CHG-023 maintenance. The later `18b6150c`
  evidence-truthfulness synchronization is therefore CHG-023 maintenance, not
  a third CHG-028 source commit, and does not alter the historical
  two-commit/ten-path boundary above. CHG-029 is separately bounded to the
  still-later contiguous `5ed0c754`/`7eb94595` fail-closed document-authority
  chain.
- **Outcome / positive effect:** the human-facing audit, machine catalog, and
  refusal policy now tell the same story. Reviewers can distinguish a product
  defect from a runner-dependent probe sample, see which evidence is local or
  remote, and identify the exact documents and controls that would be lost by
  an inverse. The red run is preserved rather than rewritten, and no green
  documentation claim is promoted into device, child, owner, or release proof.
- **Possible negative effect / unknown:** evidence repeated across multiple
  authority documents can drift again when a new CI run, APK, product repair,
  or acceptance decision lands. This synchronization increases documentation
  volume and does not itself validate runtime behavior. Its accurate local/
  remote distinction could be damaged by a partial revert, while a whole
  inverse would remove useful rollback safeguards and leave the underlying
  runtime/probe commits reachable but under-documented.
- **Exact-head remote evidence:** GitHub Actions run `31686380560` succeeds at
  exact `9befc0f838f40eead2f42088a91206257fe217a8`. The Ubuntu `probes` job runs
  09:24:08–09:57:48 UTC (33m40s): static gates, import, the full
  analyzer, exactly 63 remote trusted probe headings, boot, Dust and Opera
  advisories, and the Opera manifest are green. The pinned Windows job runs
  09:24:08–09:27:55 UTC
  (3m47s) and ends
  `MUSIC|check 42/42|picture_xmas`. This is exact-head machine evidence. The run
  is not warning-clean: the logs retain the existing missing-Vulkan-surface
  fallback to OpenGL 3 plus ObjectDB/resource/texture-leak diagnostics. All five
  capture/upload pairs completed at the workflow level and uploaded diagnostic artifacts; they
  are not capture gates or visual passes. Raw Sky Lagoon `LAGOONSHOT` output has
  21 `OK`, 44 `FAIL`, and `DONE` (66 diagnostic lines), so the Sky Lagoon
  diagnostic internally fails. No matching APK,
  device, child, owner, exact-voice, human-listening, strict-2D satisfaction,
  or accepted-visual evidence follows from this run; all remain open.
- **Dependencies and evidence:** CHG-005, CHG-011, CHG-015, CHG-023, CHG-025,
  and CHG-027. Git parent checks, per-commit `diff-tree` checks, and the combined
  path union establish the exact boundary. At the CHG-028 checkpoint, its
  dedicated control brought the suite to 22 planner unit tests; the planner
  remained read-only, four groups could emit guarded scripts, and all 24
  then-manual groups refused automation. Probe parity, exact GAME2D regression-gate
  syntax, Python compilation, catalog/ledger source parity, and `git diff
  --check` remain required. The recorded 1,379.3-second/64-probe pass is
  inherited evidence from the repaired head, not a result produced by these
  documentation commits. Run `31686380560` supplies the later exact-head remote
  machine proof described above without turning workflow-completed diagnostic
  uploads—including the internally failed Sky Lagoon result—into acceptance.
- **Rollback:** `documentation_migration`; the planner is `MANUAL` and refuses
  `--emit-script`. Start any read-only investigation at exact
  `9befc0f838f40eead2f42088a91206257fe217a8`, verify both parent links and the
  exact 10-path union, and inspect the two owned diffs without mutating Git. Do
  not raw-revert either source: that would erase truthful failed-run evidence,
  CHG-027's second-commit ownership, and refusal safeguards while leaving the
  product/probe commits in history. Correct a disputed fact with a superseding
  append-only record. Only an owner-approved, reviewed ten-path documentation
  inverse that preserves every later truthful authority and control update may
  be considered, followed by all listed gates.

### CHG-029 — Exhaustive document authority and canonical-finding gate

- **Sources and exact boundaries:** first source
  `5ed0c75460c9afd5ab574ff2c4a907c1075964f0` has exact parent
  `18b6150c01e1587100dca97c85ebad03f369825a` and changes exactly 19 paths with
  2,645 insertions and 232 deletions. Contiguous hardening source
  `7eb945957776ab3458a9de71c8be9937e2354720` has exact parent
  `5ed0c75460c9afd5ab574ff2c4a907c1075964f0` and changes exactly 13 paths with
  479 insertions and 160 deletions. Ten of those paths overlap the first source;
  the three additions are this changelog, the rollback planner, and its tests.
  The exact combined union is 22 paths. Summed per-commit churn is 3,124
  insertions and 392 deletions; the exact baseline-to-head diff from `18b6150c`
  through `7eb94595` is 3,024 insertions and 292 deletions. These measurements
  are distinct and must not be conflated. The post-`7eb94595` metadata update,
  exact `51887315` verification checkpoint, and later terminal-lifecycle prose
  sync are CHG-023 maintenance, not a third CHG-029 source and not part of the
  separately bounded CHG-030 capture-audit source.
- **Exact 22-path union:** `.github/workflows/probes.yml`; `.gitignore`;
  `AUDIT_3_0.md`; `CODEX_OPERA_WIDGET_ART_HANDOFF_2026-08-02.md`;
  `MINIGAME_ENGINES.md`; `OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md`;
  `OPERA_WIDGET_INPUT_AUDIT_2026-08-02.md`;
  `audit/MASTER_AUDIT_2026-08-09.md`;
  `audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md`;
  `audit/castle_sprite3d/CASTLE_LIGHTING_CONTINUITY_AUDIT_2026-07-29.md`;
  `audit/findings/ACTIVE_FINDINGS_2026-08-13.md`; `design/00_MASTER_INDEX.md`;
  `design/01_GAME_DESIGN.md`; `design/03_TECHNICAL_ARCHITECTURE.md`;
  `design/04_OPEN_WORK.md`; `design/05_DOC_LEDGER.md`;
  `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`; `scripts/ci.sh`;
  `tools/audit_document_authority.py`; `tools/plan_audit_rollback.py`;
  `tools/tests/test_audit_document_authority.py`; and
  `tools/tests/test_plan_audit_rollback.py`.
- **What changed, in plain English:** the first source replaces an incomplete
  document inventory with one scoped authority-ledger row for every one of the
  316 Git-declared Markdown paths and adds a stable, section-5-linked canonical
  register for all 36 material P1/P2 records. Its fail-closed validator and 35
  focused unit tests reject inventory drift, missing or duplicate records,
  malformed/escaped table rows, wrong finding anchors, incomplete exact field
  sets, illegal lifecycle transitions, and unscoped current-vs-historical
  claims; six mutation controls are green. It wires focused tests, stress, and
  real-repository audit into local CI and the remote Probe Suite in that order,
  repairs malformed historical tables, scopes superseded spatial/3D passages,
  and synchronizes authority to `18b6150c` evidence. The hardening source adds
  fail-closed multiline regressions for pre-seal wording, predecessor-as-latest
  local evidence, cross-head release evidence, and stale change-group counts;
  synchronizes the master/index/design/finding evidence; and establishes the
  detailed CHG-029 record and planner refusal. Neither source changes runtime,
  scenes, save keys, protected originals, assets, audio, generated-art payloads,
  or gameplay behavior.
- **Outcome / positive effect:** document drift now fails visibly instead of
  silently omitting a tracked file, material finding, wrapped stale claim, or
  incorrect evidence head. Reviewers can trace current claims to declared rules
  and active P1/P2 items to complete stable records without treating historical
  passages as authority. The chain records 316/316 inventory/ledger parity and
  36/36 active-record parity while retaining terminal records for history.
- **Possible negative effect / unknown:** every future tracked Markdown path,
  material finding, or evidence-head update requires synchronized metadata,
  increasing maintenance cost and potential heuristic false positives. The
  first source changes `.github/workflows/probes.yml`, a high-risk workflow
  scope; its exact diff only adds three read-only Python commands under existing
  `contents: read` and adds no action, package, credential, secret, network,
  publication, or write permission. The hardening source changes no workflow
  path. Extra static checks add CI time. Structural green does not prove
  gameplay or external acceptance, and a partial inverse can desynchronize the
  validator, tests, ledger, findings, planner, and authority claims.
- **Dependencies and evidence:** CHG-005, CHG-008, CHG-011, CHG-023, CHG-025,
  and CHG-028. Exact official Godot 4.7.1 local `scripts/ci.sh` at first source
  `5ed0c754` is historically green after **1,359.8 seconds with all 64 trusted
  local probes**. At source head `7eb94595`, focused evidence is 36/36
  document-authority tests, six/six mutation controls, 316/316 inventory/ledger
  parity, 36/36 active-record parity, Python compilation, probe-parity
  stress/default, GAME2D stress/default/regression, planner tests, and `git diff
  --check`; no direct full-local or remote result was recorded at that source
  checkpoint. Exact CHG-023 maintenance head `51887315`, parent `7eb94595`,
  then passes official Godot 4.7.1 full local after **1,435.2 seconds with all
  64 trusted local probes** and exact-head Probe Suite run `31710377034`.
  Ubuntu runs 14:28:33–15:09:45 UTC (41m12s), including an 18m02s trusted loop
  with exactly 63 headings; its document static gate is 36 tests, six/six
  stress, 316/316 inventory/ledger, and then-current 36/36 active/records, all
  green. Windows completes in 4m08s with raw 42/42 ALL OK. `MA-DOC-002` and
  `MA-DOC-005` are therefore `VERIFIED_FIXED`; the current validator reports
  34 active items and retains all 36 records. The master audit and design 06 are
  `CANONICAL_CURRENT`, while the game-wide audit remains
  `IN_PROGRESS / UNSATISFIED`. Raw Sky Lagoon remains 21 OK/44 FAIL/one DONE,
  workflow-success/upload only; runner warnings, legacy resource diagnostics,
  runtime, device, child, owner, visual, voice, listening, strict-2D, APK, and
  release acceptance remain separate.
- **Rollback:** `documentation_migration`; the planner is
  `MANUAL_RECONSTRUCTION_REQUIRED` and refuses `--emit-script`. Do not raw-
  revert or selectively restore either source: a partial inverse can leave CI
  invoking deleted tooling, hide the canonical register while master links
  target it, remove required ledger rows/tests, or restore unscoped legacy-3D
  and stale evidence claims. Correct a disputed rule or fact with one reviewed
  superseding migration. Any owner-approved complete inverse must start at
  exact `7eb945957776ab3458a9de71c8be9937e2354720`, preserve every later truthful
  record, cover the exact 22-path union, and pass every focused gate plus exact
  official-Godot full CI.

#### CHG-029 maintenance — mandatory development integration, 2026-09-06

Owner explicitly commissioned the instruction/CI integration and preferred
better indexing to relocating the audit. Source baseline: the exact `baseline` SHA in the linked impact record.
Implementation source: the first commit adding `tools/audit_development.py`;
resolve its exact SHA with `git log --diff-filter=A --format=%H -- tools/audit_development.py`.
Before that commit exists this entry describes an uncommitted candidate.
Exact changed paths and verification are in
`design/audit_impacts/2026-09-06-audit-development-contract.json`.
This extends CHG-029's document-authority gate to operational entry points,
navigation and per-change traceability; historical source boundaries above stay
unchanged. Benefit: make applicable rules visible before development and expose
missing change coverage. Risks: incorrect routing or comparison-base selection
can block unrelated work; tests must reject missing references and exercise
Git additions, deletions, merges and stale records. No runtime/asset change or
master finding closure is claimed.
Rollback class: manual, policy-sensitive. Review the exact follow-up commit's
instruction/workflow/tool diff on a dedicated branch; preserve unrelated work
and all historical evidence. Do not emit an automatic rollback from the older
CHG-029 source pair. Re-run document, development and existing full gates after
any approved reversal. Machine evidence never supplies device/child/owner acceptance.

### CHG-030 — Fail-closed Sky Lagoon promenade capture audit

- **Source and exact boundary:** source
  `7391c53cd6981a256bd8bfe40ccbb9f72fb723fe` has exact parent and comparison
  baseline `e6edf559af219edd4e5ce38cab0c5094483be5c6`. It is a non-merge commit
  that changes exactly two paths with 1,029 insertions and 357 deletions:
  `scripts/probe_sky_lagoon_art.gd` has 1,025 insertions/348 deletions and
  `tools/game_2d_migration_manifest.json` has 4 insertions/9 deletions. The
  exact rollback start is the source itself, `7391c53c`.
- **Exact two-path set:** `scripts/probe_sky_lagoon_art.gd`; and
  `tools/game_2d_migration_manifest.json`. No workflow, production-runtime,
  scene, save-schema, protected-original, voice/audio, generated-art, or
  shipping-art path changes.
- **What changed, in plain English:** the prior screenshot script followed
  retired courtyard roles, created a second review `Camera3D`, used 1280×1024
  framing, and could report dozens of false failures while still writing 20
  pictures. The replacement audits the shipping promenade through the child's
  active production camera and writes 20 exact 1280×720 PNGs for arrival,
  Reef return, day/night overviews, all five live route/play targets, five
  animals, three focus/action pairs, Castle focus, and the raccoon startle. It
  fail-closes each row on current game/phase/route/focus/action state, active
  camera, live target/card/highlight ownership, subject visibility and screen
  position, animal texture/lighting, exact action frame, image dimensions and
  nonblank/luma sampling, exact output membership, official 4.7.1 Mobile
  renderer, and normal-save integrity. A root failure records a failed row and
  marks later IDs skipped instead of silently presenting a partial set as
  complete. The JSON manifest preserves capture IDs, expected/actual state,
  every assertion, image hashes/quality metrics, probe hash, renderer/version,
  source revision, save fingerprints, and the final result. The paired GAME2D
  manifest edit updates its inventory head/date and the rewritten probe's exact
  marker counts; it does not waive or close migration debt.
- **Outcome / positive effect:** local review now distinguishes a current,
  complete capture from a merely nonempty output directory. The fresh exact-
  source Mobile-render run produced 20 PASS / 0 FAIL / 0 SKIPPED rows, 20 exact
  PNGs, and 1,078/1,078 passing capture assertions; the normal save and all
  enumerated sidecars were unchanged, temporary save paths were clean, and
  in-memory plane/time state was restored. This is materially stronger,
  reproducible evidence for locating Sky Lagoon regressions and for human art
  review without changing the child's game.
- **Possible negative effect / unknown:** the larger probe is more coupled to
  current private promenade state, positions, atlas frames, and node names, so
  legitimate scene evolution must update the probe and GAME2D fingerprint
  together. Fixed-position and threshold checks can reject an intentional
  redesign, while nonblank/luma and state assertions can still pass unattractive
  composition. They do not prove layered depth, seam quality, target-device
  legibility, touch behavior, child comprehension, owner art approval, or
  runtime correctness outside the sampled moments. Fresh human review keeps
  four new visual concerns open: small animals lose child-readable presence at
  phone scale; overlapping silhouettes/props compete in some compositions; the
  seesaw action is ambiguous; and subtle focus feedback may not clearly signal
  the selected target. These are review findings, not machine-closed defects.
  `MA-VIS-002` (the one-mural/layer-stack defect) and `MA-VIS-006` (live visual
  review/manual/coverage gaps) remain open, as do applicable runtime, device,
  child, strict-2D, art, matching-APK, and release defects or gates.
- **Workflow limitation:** `.github/workflows/probes.yml` did not change. Its
  Sky Lagoon capture and upload steps both remain `continue-on-error`, and the
  artifact uses a PNG-only upload glob. The JSON manifest is not currently a
  remote artifact; a failed capture therefore cannot fail the workflow. A
  workflow-success badge, completed step, or uploaded PNG set is diagnostic
  availability only—not capture PASS, visual acceptance, or release evidence.
- **Dependencies and evidence:** CHG-005, CHG-006, CHG-008, CHG-011, CHG-023,
  CHG-025, and CHG-029. Exact-source local evidence under official Godot
  4.7.1 is green: parser, inference lint, full analyzer, two fresh rendered
  capture runs including pre-existing-output/save-state adversaries, focused
  `probe_l2`, `probe_l2_living_cards`, `probe_sky_lagoon_animals`,
  `probe_l2_reenter`, and `probe_train`, GAME2D stress/default/regression, and
  `git diff --check`. Exact `scripts/ci.sh` completed in **1,402.3 seconds with
  all 64 trusted probes**; the capture manifest records **1,078/1,078** passing
  assertions. Exact-head Probe Suite run `31728755204` for `7391c53c` completes
  workflow-success: the 40m05s probes job has 63/63 trusted headings and the
  3m38s music job is 42/42. Its Sky process is deliberately not accepted: all
  20 ordered rows and the `20/20/0/0` summary pass, then the binding renderer
  gate emits `GLOBAL|FAIL|rendering_method|gl_compatibility` and `RESULT|FAIL`
  with exit one after the runner lacks `VK_KHR_surface` and falls back to
  OpenGL. `continue-on-error` masks that process failure at workflow level and
  the PNG-only artifact omits the JSON result. Integrated predecessor
  `e6edf559` separately passes dev run `31722047536`; Android run `31724927769`
  publishes its 596,041,412-byte APK at SHA-256
  `66d16de5973dfe08947577b7cad59cfb40b0db87dde788d0d61d9c8b598ca17c`.
  No matching `7391c53c` APK, remote Mobile diagnostic PASS, or release gate is
  claimed.
- **Rollback:** `guarded_mixed`; the planner is
  `MANUAL_RECONSTRUCTION_REQUIRED` and refuses `--emit-script`. Do not raw-
  revert `7391c53c` or restore the old probe: that would restore obsolete
  courtyard-role assumptions, a second review camera, misleading framing and
  false-failure behavior. Do not reverse only one path, because the executable
  probe and GAME2D inventory fingerprint would disagree. An owner-approved
  inverse must start from a clean branch at exact
  `7391c53cd6981a256bd8bfe40ccbb9f72fb723fe`, hand-construct a reviewed
  two-path replacement that preserves the production camera, current-state,
  exact-output, provenance, fail-closed, and save-integrity guarantees, keeps
  the GAME2D inventory truthful, and passes every listed focused gate plus exact
  official-Godot full CI. No automatic inverse is authorized.

### CHG-031 — Sky Lagoon true-Canvas promenade and touch lifecycle

- **Source and exact boundary:** source
  `51d0abc0d32855a8ba32932599fedd8f59b398b7` has exact single parent and
  comparison baseline `1b7d6bdaf89ebc7c9bdeae16fbde0e14079fd8a8`.
  It is a non-merge commit that changes exactly 19 paths with 3,318 insertions
  and 3,517 deletions. The exact rollback start is the source itself,
  `51d0abc0`.
- **Paths:** `scripts/arena/sky_lagoon_promenade.gd`;
  `scripts/living_world.gd`; `scripts/main.gd`; `scripts/pause_menu.gd`;
  `scripts/probe_audit.gd`; `scripts/probe_boot_display.gd`;
  `scripts/probe_galaxy_state.gd`; `scripts/probe_interaction.gd`;
  `scripts/probe_l2.gd`; `scripts/probe_l2_living_cards.gd`;
  `scripts/probe_l2_reenter.gd`; `scripts/probe_northern.gd`;
  `scripts/probe_ocean_kingdoms.gd`;
  `scripts/probe_sky_lagoon_animals.gd`;
  `scripts/probe_sky_lagoon_art.gd`; `scripts/probe_touch_stress.gd`;
  `scripts/probe_train.gd`; `scripts/touch_ui.gd`; and
  `tools/game_2d_migration_manifest.json`. This boundary contains 18 GDScript
  paths and one static inventory path. It changes no workflow, scene,
  save-schema, protected-original, voice/audio, generated-art, or shipping-art
  path.
- **What changed, in plain English:** the Sky Lagoon promenade is now one true
  Canvas route over the approved continuous 6144x2048, twelve-tile panorama.
  `CanvasLayer -1`, `Node2D`/`Sprite2D`, and `Camera2D` own presentation and
  travel. Canvas Roshan owns master-space movement, camera following, touch
  navigation, focus, and the playground actions. Five live targets, five
  animals, day/night state, real parallax layers, route exits, and living-world
  cards follow the same master-space coordinates. The generic 3D Player stays
  hidden, inert, and camera-disabled only as compatibility state while this
  route is active. Reef, Castle, Galaxy, Ember, train, and northern transitions
  now restore the semantic Canvas destination instead of reading the hidden
  compatibility body.
- **Touch and lifecycle repair:** Classic short release remains jump outside
  the promenade and emits contextual world touch only inside it. A Classic
  drag starts manual movement, while manual input, keyboard movement, route
  transitions, overlays, and new goals clear stale hold/navigation/focus state.
  Opening pause first cancels every active touch before pausing the tree, so a
  held physical gear press cannot survive resume as movement or autowalk. The
  action hot path avoids repeated per-frame alpha scans, the seesaw derives
  rotation from its immutable rest pose, and invalid equipment input remains
  safe.
- **Outcome / positive effect:** Sky Lagoon no longer presents a 3D facade for
  this playable screen. Movement, camera, actions, animals, and child-facing
  one-finger input share one Canvas coordinate system, while the approved art,
  save keys, external-route semantics, no-fail behavior, and Mobile renderer
  contract are preserved. Probes now measure the visible master-space player
  and semantic destinations instead of accidentally passing or failing against
  the hidden 3D body.
- **Exact local machine evidence:** at the exact source bytes, official Godot
  4.7.1 `scripts/ci.sh` completed in **1,404.5 seconds with all 64 trusted
  probes**. Parser, inference lint, full analyzer, focused natural-timing
  Lagoon actions, living cards, re-entry, northern return, real Galaxy
  outbound/return, five animals, train, interaction, and physical touch/pause
  stress were green. Probe parity stress/default, `git diff --check`, and
  GAME2D stress/default/regression were green. The migration gate reports
  `NO_REGRESSION`; its default target remains `UNSATISFIED`.
- **Fresh visual evidence:** local run-14 has manifest SHA-256
  `AEAC7C72E0A3BFF992713127261DD00ED69049947DFB6723AA66365F5712DE34`
  and exact visual-probe source SHA-256
  `B9EAF5E0738CFB61CCD3E34ACFEA420AEADAB4E3ADE80B40A2CFD1F227569C6C`.
  The manifest records `source_revision: unknown`; the first hash binds the
  manifest and its embedded PNG identities, and the second binds only the
  visual-probe script. They do not bind the full runtime tree. The separate
  1,404.5-second local CI result above is the exact-`51d0abc0` source-byte proof.
  It records 20/20 ordered full-frame PNG rows PASS, zero failed, skipped, or
  global rows, exact 1280x720 output under official Godot 4.7.1 Mobile/Speedy,
  unchanged normal save state, zero probe writes, and successful cleanup. Two
  independent repository-side human reviewers approved all 20 frames. That
  review is not a Lenovo Tab M11, child, or owner-art acceptance substitute.
- **Remaining debt and unknowns:** GAME2D remains `UNSATISFIED` at 509
  active/export model files, 65 production-3D files, 70 probe-3D files, one
  scene dependency, one config dependency, and zero archive-now candidates.
  The change fixes the Sky route but does not close game-wide strict-2D debt.
  At sealing time there is no exact-source remote Probe Suite result, matching
  APK, M11 touch/performance result, child play-test, owner acceptance, or
  release evidence. Local machine success and independent frame review must
  not be promoted into any of those external gates.
- **Post-seal CHG-023 integration evidence:** exact integration head
  `441adf35f7dbdeb67d36fbf1a2217b87d3040d47` is a CHG-023 maintenance
  descendant of the sealed CHG-031 product source; CHG-031 still owns only
  `51d0abc0`, its exact 19 paths, and that exact rollback start, and this
  checkpoint does not create CHG-032. Exact-byte official-Godot local
  `scripts/ci.sh` passes in **1,391.5 seconds with all 64 trusted probes**.
  Topic run `31760207048` succeeds at exact `441adf35` with a 33m39s probes
  job and 3m18s music job; integrated-dev run `31762132976` succeeds at that
  same exact head with a 33m39s probes job and 3m56s music job. Both report 36
  document-authority tests, six/six mutation-stress controls, 316/316
  inventory/ledger, 34 active items and 36 retained records, 63/63 remote
  trusted headings, 42/42 music checks, and zero hard workflow failures.
  Neither raw Sky step is a Mobile diagnostic PASS: each requests Mobile,
  cannot acquire `VK_KHR_surface`, uses llvmpipe and falls back to
  `gl_compatibility`, records 20 ordered PASS rows and `20/20/20/20` summary
  counts with zero failed and zero skipped, then emits
  `GLOBAL|FAIL|rendering_method|gl_compatibility` and
  `RESULT|FAIL` with exit one. That step remains non-blocking and its artifact
  remains PNG-only with no JSON result. Android run `31763879294` records raw
  checkout and HEAD both at exact `441adf35`, then builds version 1414 on
  `dev` for `android-dev`; the
  596,033,220-byte APK is SHA-256
  `f04d0fef3b9bf097aa5b07e56e5726a1db9ff37e4be6ce35b495e31b9e4a72d8`,
  and its 82-byte sidecar has its own SHA-256
  `43e892cfb6c9a3847e1a8760d5cad4dd8fb36719d63db0625ec8b2fa3ba8e651`.
  This proves exact integrated repository, workflow, and APK identity; it does
  not close M11 touch/performance, child play-test, owner acceptance,
  game-wide strict-2D closure, remote Mobile diagnostic PASS, or release
  acceptance.
- **Dependencies:** CHG-001, CHG-003, CHG-005, CHG-006, CHG-008, CHG-011,
  CHG-014, CHG-023, CHG-025, CHG-029, and CHG-030. CHG-030 remains the
  historical fail-closed capture-audit source; CHG-031 owns the later product,
  touch, and synchronized probe/inventory change. Post-source count, hash,
  evidence, and authority synchronization is CHG-023 maintenance, not a second
  CHG-031 source and not CHG-032.
- **Possible negative effect / unknown:** the route, touch lifecycle, shared
  main/pause/living-world state, external transitions, probes, and GAME2D
  inventory are coupled. A raw revert restores the rejected 3D facade and
  stale Classic-touch/pause behavior. A partial inverse can strand camera or
  route ownership, leave a held touch alive, disagree about visible player
  coordinates, desynchronize probes from production, or make the inventory
  fingerprint dishonest.
- **Rollback:** `owner_blocked_mixed`; the planner is deliberately
  `MANUAL_RECONSTRUCTION_REQUIRED` and refuses `--emit-script`. Do not raw-
  revert `51d0abc0` or restore old whole files. Repair a defect forward. If the
  owner explicitly requires a complete inverse, create a clean isolated branch
  at exact `51d0abc0d32855a8ba32932599fedd8f59b398b7`, verify its exact parent,
  hand-construct and review the full 19-path inverse, preserve every save key,
  protected original, later truthful change, one-finger no-trap behavior, and
  evidence contract, then rerun every focused and full exact-4.7.1 gate plus
  remote, device, child, and owner review. No rollback script may be emitted.

## 5. Per-group gate matrix

| Change IDs | Minimum focused gates before full CI | External gates that remain material |
|---|---|---|
| CHG-001, 003, 006, 013, 014 | Roshan/clipping, Lagoon/Seek/audit, visual unit+stress+fresh-strict | two-aspect Mobile capture, M11, child, owner art |
| CHG-002 | companion, stuffie, passive, load, save-recovery | child no-trap/re-entry |
| CHG-004 | voice, audio, Brawl, Nursery, Opera 2D, passive | protected-voice intelligibility and device mix |
| CHG-005, 008, 009 | parity stress/default, GAME2D unit+stress+default/regression, import | clean remote exact-head |
| CHG-007, 012 | mg2d/UI/rank/Dolls/passive, GAME2D | capture, device touch, child |
| CHG-010, 016–019 | Opera 2D, Nursery, Detective, gesture quality, passive, voice, teardown, animation/minigame-art audits | capture, device performance/touch, child, owner |
| CHG-015, 021 | Castle provenance builders/tests, Opera generated-art gate, interaction, load/save | Cross-platform generated-art checks, Castle captures, and owner review |
| CHG-020 | deterministic music check, audio, voice, picture games, Opera | two-wrap/ducking/off/mono/M11 listening |
| CHG-011, 023 | UTF-8, unique IDs, links, ledger coverage, table/fence and forbidden-claim checks | owner authority confirmation where changed |
| CHG-022 | every applicable gate above and exact `scripts/ci.sh` | remote exact-head plus all applicable external gates |
| CHG-024 | exact parent/path guards, GAME2D/parity/generated-art checks, every applicable focused gate, and exact `scripts/ci.sh` | remote exact-head plus all applicable capture, M11, child, audio, and owner gates |
| CHG-025 | rollback catalog tests, document structure/links, probe parity, GAME2D regression, and diff check | re-audit ratings and branch facts whenever a candidate becomes committed or integrated |
| CHG-026 | exact commit-parent/path parity, parser/lint, Opera/load/recovery/living-world/audio/UI, GAME2D default+regression+stress, fresh Mobile captures, and exact `scripts/ci.sh` | remote exact-head, M11 touch/performance, child comprehension, owner art/authority, and MA-OPERA-012 Castle-room distribution |
| CHG-027 | exact two-commit/parent/15-path-union parity, parser/lint, bounded route-readiness, room-route/Opera/Opera-2D/load/living-world/UI, GAME2D default+regression-gate+stress, 22 fresh Mobile diagnostics, exact `scripts/ci.sh`, and successor authority-head remote run `31686380560` | repeat exact-head remote at the eventual integrated release candidate; bounded P2 card-overlap repair, M11 touch/performance, child comprehension, owner art/authority, and authoritative visual acceptance |
| CHG-028 | exact two-commit/parent/10-path-union parity, 22 planner tests, Python compilation, ledger/catalog source parity, probe parity, GAME2D regression gate, diff check, and exact-head run `31686380560` with warning diagnostics and internally failed Sky Lagoon diagnostic retained | matching APK and external evidence; supersede facts as CHG-023 maintenance after later product/evidence changes and never promote documentation synchronization into acceptance |
| CHG-029 | exact two-source parent/path parity, exact 22-path union, 23 planner tests, 36 document-authority tests, six mutation stress controls, 316/316 inventory/ledger and 36/36 active-record parity, Python compilation, probe parity, GAME2D stress/default/regression, diff check, first-source local `scripts/ci.sh` in 1,359.8 seconds/all 64, and exact CHG-023 maintenance-head local 1,435.2 seconds/all 64 plus Probe Suite run `31710377034` | repeat exact-head machine gates for any rollback candidate; all device, child, owner, voice, listening, strict-2D, visual, matching APK, and release acceptance |
| CHG-030 | exact source/parent/two-path parity, parser/lint/full analyzer, two fresh 20-frame Mobile capture runs with exact output/save/provenance checks, 1,078/1,078 assertions, five focused Lagoon probes, GAME2D stress/default/regression, diff check, and exact local `scripts/ci.sh` in 1,402.3 seconds/all 64; exact-source workflow run `31728755204` completes with 63/63 headings and 42/42 music | remote Sky internally ends `GLOBAL FAIL rendering_method=gl_compatibility` / `RESULT FAIL` after 20 PASS rows because the runner falls back from Mobile/Vulkan; workflow remains non-blocking and PNG-only, while MA-VIS-002/006, small-animal readability, overlap, seesaw/focus clarity, M11, child, owner-art, strict-2D, matching APK, and release acceptance remain open |
| CHG-031 | exact source/parent/19-path parity, parser/lint/full analyzer, natural-timing Lagoon actions, living cards, re-entry, northern/Galaxy/route return, five animals, interaction/train and physical touch/pause stress, separate run-14 20/20 Mobile evidence whose manifest/PNG identities and probe script are hashed while `source_revision` remains unknown, save integrity, probe parity, GAME2D stress/default/regression, diff check, exact local `scripts/ci.sh` source-byte proof in 1,404.5 seconds/all 64, and post-seal CHG-023 checkpoint `441adf35` with exact-byte local 1,391.5 seconds/all 64, successful topic/dev Probe runs `31760207048`/`31762132976`, and exact-head Android run `31763879294` version 1414/APK SHA `f04d0fef…72d8` | both remote Sky steps remain non-blocking PNG-only `gl_compatibility` failures after 20 PASS rows rather than Mobile diagnostic passes; M11 touch/performance, child play-test, owner acceptance, game-wide strict-2D closure, and release acceptance remain open |

## 6. Required rollback record

Every attempted inverse appends a record; failed experiments remain evidence.

```yaml
rollback_attempt:
  change_id: CHG-000
  branch: codex/rollback-chg-000
  start_commit: <40-hex>
  source_commits: [<40-hex>]
  method: guarded_single | guarded_chain | guarded_mixed | archive_recovery_only | whole_merge_only
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

## 7. Full-integration emergency fallbacks

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

### 7.1 Current-dev reconciliation fallback (`CHG-024`)

The newer all-or-nothing inverse is the exact `f3b0de07` merge back to its
current-dev parent `ea6185fd`. It removes the entire master-audit integration,
including beneficial current-dev reconciliation, Canvas conversions, CI gates,
and tool hardening. It also reverses intentional archive removals and can put
retired resources back into active repository paths. It is therefore an
integration-emergency mechanism, never a way to undo one career, art asset,
probe assertion, or older `CHG-*` group.

Start from the merge itself on a clean dedicated branch and keep mainline 1:

```powershell
git switch -c codex/rollback-chg-024 f3b0de078898a8b4faddb2c738c4403180eff928
git revert --no-commit -m 1 f3b0de078898a8b4faddb2c738c4403180eff928
git status --short
git diff --stat
git diff --check
```

Do not mix this branch with CHG-001–023, do not overwrite a protected original,
and do not treat restored archived content as approved runtime art. Prefer the
planner's guarded `--emit-script` form because it verifies the exact two-parent
topology, selected parent tree, and protected-path absence. Stop on any
conflict or mismatch. Run every applicable focused gate and the complete exact
Godot 4.7.1 suite; require green remote exact-head CI and every relevant
external acceptance gate before committing or integrating the recovery.

## 8. Maintenance rule

Any later commit that materially changes one of these behaviors must append a
dated entry under the existing ID with its exact commit, path delta, new risks,
new evidence, and changed rollback dependency. It must not rewrite the original
record. A genuinely new behavior receives the next unused ID. This preserves a
reviewable history in which positive and negative outcomes can coexist without
either being hidden.

### Day Two graphics review addition CHG-032

- Date: 2026-09-30. New review-tool/library behavior, distinct from historical CHG-023 maintenance.
- Exact integration baseline: `55032e88936b22723fd9af5282c61ba6696b3d43`. First exact source commit: `788e614eb1ebde47d3f9e5a87d5634638d5eb7bb`. Exact planned-contest extension and authority reconciliation commit: `2eae4ceb31b9274a53e4767c9845b6c6934260cc`. Publication metadata follows without changing those source records.
- Paths: `tools/build_day2_art_library.py`, `audit/day2_art_library_2026-09-30/REPORT.md`, `inventory.json`, `reviews.json`, `evaluations.json`, `index.html`, `priority_queue.csv`, `cover.jpg`, `preview_provenance.json`, `refresh_delta.json`, and `verification.log` in that same audit directory; `design/audit_impacts/day2-art-library-20260930.json`, `design/05_DOC_LEDGER.md`, `audit/MASTER_AUDIT_2026-08-09.md`, `ASSET_LICENSES.md`, and this changelog. The impact record enumerates exact repository paths, including all 660 adjacent source/historical preview images.
- Intended benefit: individually inspect 637 images and 190 current/planned phase or beat evaluations, prioritize the inclusive 4.5/5 threshold, and invalidate changed source reviews on a later manual refresh.
- Plausible negative effects: source opinions could be mistaken for runtime acceptance, historical screenshots for current captures, or inactive weak art for a generation order. The report, item records and UI explicitly retain those limits. The complete folder contains small HTML/JSON and separately hashed whole-source previews; source images remain unchanged.
- Dependencies and evidence: named baseline image/controller hashes, owner-corrected Arborist direction, design authority, historical capture manifests, individual authored reviews, browser inspection and audit gates recorded in `verification.log` and the impact record. Existing finding lifecycles are unchanged; no runtime, save, protected asset or release authority changes.
- Rollback class: `documentation_migration`. Start a clean dedicated `codex/rollback-chg-032` branch, inspect the exact source paths, preserve later review evidence, remove/migrate the tool and library together, and repair only these new navigation/license/ledger entries. The existing rollback planner has no emitter for this new scoped record; no raw inverse is authorized by this entry. Re-run authority/change coverage and applicable focused/full regression gates before publishing any rollback.

CHG-032 packaging correction: the first published large HTML exceeded the unchanged 4 MiB complete-text scan cap and failed run `36755706002` at `G2D101`. The same accepted-for-draft thumbnail pixels are now separate inspectable images; no migration-manifest, audit, runtime or original-art change is made. Exact packaging/source-link correction commit: `6757ea5e0c0bc4ddfbc1cd9615558df7b92ddec0`. Codex authorship replaces inaccurate human-authorship wording; human and owner acceptance remain outstanding.

CHG-032 live refresh: incoming integration `08acb0ce529660e79de6784aa4124352798bc4cd` changes one inventoried Rumi sheet. Its old source review is preserved in history, native re-review retains 4.5/5 for remaining fringe/scale work, and associated birthday Popstar/seam notes are updated. Upstream source-pixel edits remain owned by the separate Rumi repair impact; this task authors no new source-art change. Exact live-refresh source commit: `17ce3c9bf14f9140bd25a08b63eda1a61811b7cc`.


### Sky Lagoon animal boundaries CHG-033

- Date: 2026-10-07. Owner report: Sky Lagoon animals walk in the air and through bushes instead of staying on open ground.
- Exact integration baseline: `6238934447cf28834874396dfbaff65effafda46`. Source commit will be recorded in the verification follow-up after the exact focused/full gates; no published or green-source claim is made by this planning entry.
- Exact paths: `scripts/arena/sky_lagoon_promenade.gd`, `scripts/arena/sky_lagoon_layout.json`, `scripts/probe_sky_lagoon_animals.gd`, `design/audit_impacts/sky-lagoon-animal-boundaries-20261007.json`, `audit/sky_lagoon_animal_boundaries_20261007.json`, `audit/findings/ACTIVE_FINDINGS_2026-08-13.md`, `audit/MASTER_AUDIT_2026-08-09.md`, `design/05_DOC_LEDGER.md`, and this changelog.
- Intended benefit: place all five species on source-painted stone/grass with the whole footprint inside declared boundaries, keep all patrol/escape segments on those lanes, and align each unchanged source cell's feet and contact shadow with its floor coordinate.
- Plausible negative effects: smaller ambient ranges, endpoint disappearance, overlap/readability changes, or incorrect contact anchors. Complete-path negative/large-delta probes and real Mobile day/night scene captures are required. No new art, protected-original, family-voice, save schema, player route, objective/reward or release-policy change.
- Dependencies and evidence: unchanged native v5 plate and ten atlases, the existing pooled Canvas actor/shadow, main-owned transient state and current layout contract; exact hashes, baseline reproduction, gates and remaining acceptance are recorded in the linked impact. `MA-VIS-002` remains `FIXED_PENDING_VERIFICATION`; `MA-PLAY-003` remains `CONFIRMED_OPEN`; this repair does not close whole-game geometry.
- Rollback class: `manual_reconstruction`. Start clean on `codex/rollback-chg-033`; inspect the eventual exact source commit/path set and later layout changes. Keep contacts, floor envelopes, patrol/startle travel and regression coverage coherent; never restore unbounded motion as a claimed accepted fallback. The existing sealed rollback planner has no emitter for this newer scope. Re-run focused/full machine and applicable visual/device gates before publishing a rollback.

CHG-033 verification follow-up, 2026-10-07: exact source commit `13bc2ea36dd97572f64f6f5cc4a5f74f0270865c` passes official Godot 4.7.2 full local `scripts/ci.sh` with 82/82 trusted zero-exit probes and no trusted failure/script/parse/compile errors. The local log SHA-256 is `f7b015dc78265e6c5fb1bec4cf2cf8ab2ef6de71423404f1764eb949bcc46211`. The committed receipt binds unchanged runtime-source hashes and 45 paired Mobile day/night/patrol/startle cases; Codex reviewed ground placement on desktop. This follow-up only binds source/evidence metadata. Exact-head GitHub CI and dev integration are pending; target-device, child, owner, accepted-visual and game-wide geometry gates remain open. The manual reconstruction dependency now names this source commit.

## 2026-10-12 — R6 independent publication route

[R6 packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/README.md) is prepared on codex/flat-vector-r6-20261012 from dev e2b3c737,whose runtime bytes match6cde8aea. Prior R5 paths/reader stay untouched on their durable branch;no scanner/gate changes.884 new/1488 cumulative frames,68 partial/zero complete,13 classified/351 unresolved;20 independent congruency observations bound to20 native images and30 named records.0 replacement/acceptance;full weakness inventory remains incomplete. [Impact](../design/audit_impacts/flat-vector-r6-standalone-20261012.json) owns exact gates/publication evidence. Rollback removes this additive packet and its new license/ledger/index/history rows only;retain immutable R5 and all runtime/protected originals. This is evidence publication,not integration/release acceptance.

- R6 independent picture addendum:52retained nativeframes(44bounded diagnostics,8rejectedbootviews),24personallyviewed/17observations/15existingIDs;combined43existingnamedrecordswithpartialreview. Eightoverlappingpicture/gamealiases become partial(76/176;0complete;100without);356source scopes still unresolved. Exact workinglicense snapshot differs from historicalGit bytes and is explicitly preserved. No newunique design/removal or findingclosure;rollback reverts this R6-only evidence commit and retains immutable R5.

- Final R6 context reconciliation:980 new/1584 cumulative bounded frames;1686 retained including8 boot and94 failed-run diagnostics.76/176 entries partial,none complete;18/369 inventory-classified,351 unresolved. Three independent reviews bind44 existing records. Existing five picture scopes counted once. Prepared Garden pot job binds stable FVR-5A761C05C31C;zero generation. All82 trusted probes pass the permitted native/probe-by-probe lane,including4 same-source retries;original Bash exit1 preserved. No runtime/acceptance/finding-lifecycle change.

## 2026-10-12 — R7 Craft source-context and shared-caller audit

[R7 entry](../docs/handoffs/codex_flat_vector_art_2026-10-07/r7_craft_context/README.md) adds 80 bounded native captures and four findings: detached fins/duplicate eye, flat raster line, selected-red darkening, unconsumed preview detail. One whole fish supplements 224 frozen designs; three layers are component roles. 225 known/30 families, 1664 bounded/1766 retained, 77/176 partial, zero complete, 99 without. Frozen 369/18/351 scope counts are retained and two additional texture compositors remain incomplete. 5350 raw-identical files/1102 newline-only sidecars. No runtime/protected/save change, acceptance, MA lifecycle closure or known all-game denominator. [Impact](../design/audit_impacts/flat-vector-craft-context-20261012.json). Rollback removes only this additive subpacket/current pointer and its authority/license rows, restoring the R6 entry from 70879a91; preserve immutable R6/R5/runtime/protected sources.

## Teacher guide current-context evidence CHG-034

- Date:2026-10-14. One bounded full-game flat-vector mission audit; no runtime or source-art change. This is a scoped documentation/capture addition, separate from the sealed historical rollback planner catalog and prior R6/R7 evidence.
- Exact source baseline:`b5c061dfd5bc36b405bd38aa0ac141eba277a012`; origin/dev:`831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. Exact audit payload:`60a057c1dda25c34f308bf3e8e95c5e568d81710`. The final publication receipt binds required added metadata bytes independently; payload hashes remain immutable.
- Exact paths: every file under `docs/handoffs/codex_flat_vector_art_2026-10-07/r27_teacher_pointer_context/` is individually enumerated in `design/audit_impacts/flat-vector-teacher-pointer-context-20261014.json`; that record also lists `.gitattributes`, `ASSET_LICENSES.md`, `audit/MASTER_AUDIT_2026-08-09.md`, `design/05_DOC_LEDGER.md`, the handoff's root `CURRENT.json` and `README.md`, and this changelog. Frozen root registries/readers and production/protected paths are unchanged.
- Intended benefit: bind Teacher guide `FV-E1049E4945A3` to four actual tier0/sequence0 lesson kinds,84native frames at two aspects and20direct views. Document pale guide/card contrast and the moving addition counter's source-bound guide offset before a reuse trial. Reconcile one new partial record,51records/11families; zero newfamilies/removals,unknown whole-game totals preserved.
- Plausible negative effects: isolated debug entry can be confused with natural route closure; one tier/question with all four kind labels can be confused with all variants; a machine pass or agent source opinion can be confused with human acceptance; failed-frame volume or reused source images can inflate progress. The report and validators exclude79invalid first-run captures, retain failed union reconciliation, preserve status/history, and separate candidate/integration/runtime/device/child/owner lanes.
- Dependencies/evidence: unchanged actual Teacher surface/lesson generator,Castle Library caller,eight Library tiles and Teacher animator atlas bound in `SOURCES.json`; raw viewport private-profile native manifests,exact engine/parser/inference gates,ten-axis same-scene comparisons and `CAPTURE_CONTRACT.json`. Five payload gates pass (54document tests+6stress and strict2D NO_REGRESSION); exact R26receipt CI38499658027 passes. R27exact-head CI and all creative/device/child/owner acceptance remain separately tracked. Finding lifecycles and whole-game strict2D satisfaction remain open.
- Rollback class:`documentation_migration`. Start from a clean dedicated `codex/rollback-chg-034` branch. Inspect the exact payload and later receipt paths and preserve immutable historical evidence. Migrate this additive packet and only its associated navigation/license/ledger/impact rows together; do not revert inherited R14production behavior,erase owner history,restore 3D,or touch protected originals. The sealed rollback planner has no emitter for this newer scope; no one-line inverse is authorized. Conflicts stop the operation. Re-run source/capture/tally,authority/change coverage,applicable focused/full machine and remote byte gates before publishing rollback; machine evidence does not grant release or visual acceptance.

## Teacher whole-hand reuse trial CHG-035

- Date:2026-10-14. Exact baseline:`36b97a183c75ca897d7fd52fe9d54d4f44edda2a`; origin/dev:`831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. Exact source payload will be recorded in the final verification follow-up.
- Exact paths: individually enumerated in `design/audit_impacts/flat-vector-teacher-pointer-reuse-20261014.json`, including the additive `r28_teacher_pointer_reuse` packet and current routing/license/authority rows; this changelog. Production/protected/source-art bytes unchanged.
- Intended benefit: compare the existing whole R16painted hand against Teacher guide silhouette/contrast and source-bound moving-counter misalignment after published R27context; point to eligible join/counter/answer regions without hiding symbols. No new generation or artwork adoption.
- Plausible negative effects: hand overlap,incorrect cue timing/target,helpedanswer distraction,isolated entry mistaken for natural route or full tier/sequence coverage;machine/callback/static-source opinions mistaken forhuman/QA11/device acceptance. All such lanes stayexplicitly open.
- Dependencies/evidence: immutable R27context manifests/captures/actual Library/Teacher/currentsource hashes verified anonymously beforeprototypeedit;preserved R16PNG/Aseprite/derivation;current rawtouch/privateprofiles/official4.7.2MobileSpeedy captures;source/state/caller/capture,document/impact/medium gates andexact GitHub bytes. Existing findings unchanged.
- Rollback class:`documentation_migration`. Start a clean dedicated `codex/rollback-chg-035`;inspect exact payload/receipt paths andlaterdependent contextrequests. Migrate only this additive nonruntime trial and its associated authority/license/current-pointer rows,preserve immutable prior evidence andR16source masters. No rawone-line inverse is authorized;sealedrollback planner has no emitter for this scope. Stop on conflicts,re-run applicable focused/full machine/authority/remote byte gates,andnever restore3D oralter protected sources/saves.

CHG-035verification follow-up,2026-10-14: exactsource payload `da40a0457494bb3214847b03b67a196012907aec` binds40source references and51anonymous before-editcontext files. Sixscript gates/currentnative/independentcontract pass;84retainedevents/24uniquecontextcredits/60duplicatestaticviews excluded,20directinspections/18unique;rawTeacherinput snapshots equalR27,0phasecompletion,normal8savehashes unchanged. Fivepayload gates pass:source/capture/canonical,documentauthority,auditdevelopment,54tests+6stress,strict2D NO_REGRESSION/UNSATISFIED. No generation/sourcepixels/production/findingclosure/humanacceptance. Exactpublished dependencyverification andfinalmetadata remotechecks are required by the receipt; CI remains separatelytracked.

## Startup ambience current-route audit CHG-036

- Date:2026-10-14. Exact source baseline:`4c5ffcaf73b4b730b266d5bf415fd662bf6084f1`; origin/dev:`831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. Exact audit payload is recorded by the verification follow-up.
- Exact paths: individually enumerated in `design/audit_impacts/flat-vector-startup-ambience-context-20261014.json`, including additive `r29_startup_ambience_context` evidence, current routing/ledger/license/attribute rows and this changelog. Frozen registry bodies, runtime/protected/source-art bytes unchanged.
- Intended benefit: resolve the old retired IntroOverlay label against the current normal display StartMenu selector; bind actual bubble/sparkle/moon context and passive action states to stable IDs. Export current catalogue registrations and source slots without equating them with visible screens/pieces.
- Plausible negative effects: conflating IntroOverlay with the intro ambience stage, assuming registered stages are reachable or visible, inflating repeated motif/image counts, mistaking agent/source/machine evidence for QA11 or human acceptance. Current observations, exclusions and unknown denominators remain explicit.
- Dependencies/evidence: exact Main/StartMenu/LivingWorld catalogue/director/canvas and boot source hashes, official4.7.2 Mobile/Speedy normal startup with private SaveState beforeMain, raw captures/selector/layers/order/idle/input/teardown and normal save hashes. Source/capture/canonical/document/impact/tests/medium and anonymous exact GitHub byte gates. No owner review or finding closure inferred.
- Rollback class:`documentation_migration`. Use a clean dedicated `codex/rollback-chg-036`;inspect exact payload/receipts and later dependent records, migrate only this additive evidence and associated navigation/authority rows, preserve immutable historical evidence and protected originals. Sealed rollback planner has no emitter for this scope; no raw inverse is authorized. Stop on conflicts and rerun applicable source/capture/document/medium/remote-byte gates before publishing.

CHG-036verification follow-up,2026-10-14: exactpayload `774388254d0e7d93284dc621a2ce30af172ac696` binds10unchanged source files,16native/directview frames,2freshprivateprofiles/normal8savehashes/teardown. Normaldisplay intro.storybook ambience is live aboveStartMenu;flatmoon crossesOptions.100registeredstages/300sourceslots/29tokens/26existingdesigns are sourcecounts,notart/screen totals. Effective78partial/98without/0complete;54existingpartial/12families,2748bounded/3031retained. Fivepayload gates0,54tests+6stress,strict2D NO_REGRESSION/UNSATISFIED. Anonymous manifest/every2903dependency verification0;1270687779requiredbytes. No runtime/sourceart/generation/acceptance/findingclosure. Finalmetadata exactbytes follow separate receipt/proof.

## Startup procedural ambience retirement CHG-037

- Date:2026-10-14. Exactbaseline:`fdf41220b8cfe16f129741e364b2ea75f4e5e7f1`; origin/dev:`831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. Exactpayload follows verifiedpublication receipt.
- Exactpaths: individually enumerated in `design/audit_impacts/flat-vector-startup-ambience-retirement-20261014.json`,including `scripts/living_world.gd`,trusted `scripts/probe_living_world.gd`,additive R30packet andnavigation/authority/license rows. No source-art/protected/savekey changes.
- Intendedbenefit: retire redundant code-drawn bubble/sparkle/moon whileStartMenu ownsdisplay,keepingthe existingpainted background andunobscuredOptions. R29actualcurrentcontext is published/anonymousbyteverified beforeimplementation.
- Plausiblenegativeeffects: disabling ambience beyondmenu,staleevent orclock onexit/reentry,breakingheadlessprobeoverride/menu orContinue/save/voice/touch routing;miscounting3startuproles as3globallyaccepted removals. Exactbaseline/focused/headless/native/fullsuite andseparatecount/evidence lanes address these risks.
- Dependencies/evidence: current Main/StartMenu/LivingWorld/canvas/catalogue andbootart unchangedsourcebindings;published R29context;meaningful failingbaseline;official4.7.2MobileSpeedy privateprofiles,naturalmenu input/Continue anddeclaredreentry,normal8savehashes;parser/inference/analyzer/import/full82/document/medium/publication gates. QA11/device/child/owner/othercaller/globalzeroart remainopen.
- Rollbackclass:`behavior_repair_and_documentation`. Useclean dedicated `codex/rollback-chg-037`;inspect exactsourcepayload/receipts/dependencies,preserve allimmutableevidence. Restoreonlythismenucondition/proberegression and associatedtally/navigation/authorityrows;do notrestore3D,alterprotected originals orremove savekeys. No unsafeone-lineinverse;stoponconflicts,re-runfocused/full/machine/document/remote-byte gates beforepublishing.

CHG-037verification follow-up,2026-10-14: exactsource/evidencepayload `b6606504598fc0d32736918c9a23f7af102f7eb7` implements4lineLivingWorldmenuguard and36linetrustedregression after57publishedcontextfiles. Expectedbaseline3fails/fixed4menuchecks/full82trustednativezeroexit/import/parser/inference/analyzer/currentnative4profilespass.78nativeunique/18directviews,124failedfixtureframesexcluded,normal8savehashes unchanged/1998sidecars preserved1102restored. Threeboundedstartuprolesretiredincandidate,globalacceptedremoved0;allothershareddesigncallers/unknowninventory/QA11/device/child/owner open. Fivepayloadgates0,54tests+6stress/strict2D NO_REGRESSION/UNSATISFIED. Anonymousmanifest/every3284requireddependency verified,1519773950bytes. Finalmetadata separate receipt/proof;sourceart/protected/savekeys/mediumidentityunchanged.

## Startup UI current-context audit — CHG-038

- Planned at `849a7de5fa65270d354cb7973ded63b464668988`; origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. Payload/receipt/proof commits will be appended after publication.
- Scope: current StartMenu inset/sheen FV-276E68E0A9DA and decorative sparkle FV-619466CA433F plus existing music-off glyph observation and its mic-off sibling. Native context/source/reuse review only; production and artwork unchanged.
- Benefit: a named repair has current scene neighbors, real Options states and exact glyph/source evidence before choosing reusable art. Risks: treating diagnostic glyph coverage as packaged device coverage, double-counting repeated adornments, and overwriting frozen counters.
- Dependencies/evidence: [R31 plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r31_startup_ui_context/PLAN.json), [impact](../design/audit_impacts/flat-vector-startup-ui-context-20261014.json), complete changed-path coverage; all QA11/device/child/owner and full inventory remain open.
- Rollback class: additive audit/navigation metadata only. Plan read-only on clean dedicated `codex/rollback-chg-038`; inspect metadata diff and rerun source/document/impact checks. Preserve immutable historical packets; no production/save/protected-content inverse.

CHG-038 published payload `1b79269f78d53dda01c2d54c2e8aa36f8604b006`: manifest and every3430required file/1585534814bytes anonymously verified at `2026-10-14T08:22:12.679881+00:00`, manifestSHA `48043712642a10ebe3646528b443e81a7ad4e744b11705337e423bfb0ddd7117`, payloadSHA `97bf894ebadb174a0cef2d42bc0f7a83dfa811d3c17f02414531f0ee49aaedfc`.52currentnative/12views/5sourceviews,56existingpartial/12families,2878bounded/3285retained/407excluded;0acceptedremoved andwholeinventory/QA11/device/child/owner remainopen. Current doc/capture/source gates pass,54tests+6stress,2D NO_REGRESSION/UNSATISFIED. Unchanged R30 local82 and exact849a7de5 CI38524281207 green retained;R31CI/finalmetadata remainseparate.

## Startup redundant UI ornament retirement — CHG-039

- Planned at `a587e4ec5e82dbc86d52115ba41f3ae37e2e24f1`; fresh origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`; exact payload/receipt/proof commits appended after publication.
- Scope: inset/sheen FV-276E68E0A9DA and decorative sparkle FV-619466CA433F on StartMenu;sole helper caller closed. Preserve existing pearls/functional style/input/save/reset/semantic labels and splash;no new pixels or generation.
- Benefit: remove redundant flat coating/twinkling glyphs over current painted context. Risks: weakened target readability, unexpected dependent ornament lookup/tween, reset/save route regression.
- Required evidence: [R32 plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r32_startup_ui_retirement/PLAN.json), [impact](../design/audit_impacts/flat-vector-startup-ui-retirement-20261014.json); verified R31context beforeedit,meaningful failingbaseline/unchanged8control bounds/16pearls,full82/focused/import/currentnative/private-save and final anonymousbyte gates. Globalinventory/QA11/device/child/owner open;no acceptedremoval/lifecycleclosure.
- Rollback class: boundedsource retirement plusmeaningful regression; clean dedicated `codex/rollback-chg-039`,inspect smallestinverse/source callers andrerunfocused/full/document gates. Preserve immutableoldpackets andneverrestore unacceptedartasfallback/protected/save change.

CHG-039 published payload `2354ee4c5b62ee1adb80ae194f0e37a1ad459e2d`: manifest and every3707required file/1705054005bytes anonymously verified at `2026-10-14T09:36:07.799143+00:00`, manifestSHA `a83599c194f90fcb8753ade96ec1ab31516967edb9288f6819098ae33cdc4411`, payloadSHA `7afeab4692fc0b6fb0284664237965c1be7aad9b385bc9d481e6e782d2a008da`.94currentnative/70unique/24duplicateexcluded/12views11unique,56existingpartial/12families,2948bounded/3379retained/431excluded;0acceptedremoved andwholeinventory/QA11/device/child/owner remainopen. Current doc/capture/source gates pass,54tests+6stress,2D NO_REGRESSION/UNSATISFIED. Actual current R32 all82strictzeroexit/native/source gates pass;priorR31CIcancelled andcurrentR32CI/finalmetadata remainseparate.

## Menu painted-material fit — CHG-040

- Planned at `ecb9839a374d3260161a19d44039325d561a3509`; fresh origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. Exact publication commits appended after delivery.
- Scope: existing FV-2ABD73BAFFE0 StartMenu eight-button source reuse;nonruntime texture-region/nine-slice padding repair after30verifiedcurrentcontextfiles. Sourcepixels/production untouched;focuspaperrectangle localQCFAIL,notintegration-ready.
- Benefit: establish a real source-bound painted fit and named remaining state weakness without spending generationbudget. Risks: weak kind/disabled/focus contrast, double-counting diagnostic frames, expanding source/menu approval.
- Dependencies/evidence: [R33plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r33_menu_material_reuse/PLAN.json), [impact](../design/audit_impacts/flat-vector-menu-material-reuse-20261014.json), source/native/context/document gates. Wholegame/QA11/device/child/owner open.
- Rollback class: additive nonruntime candidate/audit/navigation. Plan read-only on clean dedicated `codex/rollback-chg-040`;inspectmetadata/candidate diff andrerunsource/document/impact gates. Preserve immutablefailures/history;no runtime/save/protectedsource inverse.

CHG-040 published payload `d3f55adf7ddc8319275ea0fc50fb6a136b8bc360`: manifest/every4058required file/2024712453bytes anonymously verified at `2026-10-14T10:30:52.859058+00:00`, manifestSHA `cdf2aa6be8cdc23675aeb49c835043c773cc2a8577091fe9d194384ed85842f1`, payloadSHA `b9b480be8125340f6fad6be408d0a8a64fd5825ea7a1d615b73955e8e133c88c`. Sourcepaddingfit partiallyrepaired/nonruntimefocuslocalQCFAIL;122current+122initialfailedretained,72newcredits/172excluded,3020bounded/3623retained/603excluded cumulative.16currentviews,56existingpartial/12families,78partial176routes/98without/0complete;0acceptedremoved/unknowninventory/QA11/device/child/owner open. Exactnative/source/doc/54tests6stress/2DNO_REGRESSION;R32full82retainedatunchangedproduction, no newfull82run. Finalmetadata/proof/CI remainseparate.

## Painted menu focus seam — CHG-041

- Planned at `4adea70d348b0650a1ef490a42dbcfc39407e689`; origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. Publication commits appended after delivery.
- Scope: FV-2ABD73BAFFE0 / FVO-R33-FOCUS-PAPER-RECT, nonruntime StartMenu eight-control focuscenter/press-state repair. Existing sourcePNG/production/input/save geometry unchanged;35publishedcontextfiles verifiedbeforeedit.
- Benefit: remove hard paperrectangle while preserving current buttonfeedback; advance sharedUIsource caller closure. Risks: focusfill overdraw/contrast, weak kind/disabled distinction, falsely accepting diagnostic/source eligibility.
- Dependencies/evidence: [R34plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r34_menu_focus_repair/PLAN.json), [impact](../design/audit_impacts/flat-vector-menu-focus-repair-20261014.json), exactnative/source/contrast/caller/doc gates;allglobalinventory/QA11/device/child/owner remainopen.
- Rollback class: additive nonruntime candidate/audit/navigation. Read-only plan on clean dedicated `codex/rollback-chg-041`;inspectmetadata/candidate diff andrerunsource/document/impact gates. Preserve immutableprior failures/history;no runtime/save/protectedsource inverse.

CHG-041 published payload `05475ac4f1ea951baeef4f7295a117ec23b814bf`: manifest/every4288required file/2200003740bytes anonymously verified at `2026-10-14T11:56:02.741919+00:00`, manifestSHA `dd256b6b3c16e72ed91547a8299fa56a1898c3fecc19070d12b7016126bb789e`, payloadSHA `553a6ae128fa17d9e8f679ddca91a8f3feb25c76d6021cb699cad23ad4962548`. Namedfocusseam repaired inisolatedcandidate,126currentnative/33newcredits/93excluded,3053bounded/3749retained/696excluded cumulative.16currentviews/fourcontrastcomparisons/33sourcecalls17files,56existingpartial/12families,78partial176routes/98without/0complete;0acceptedremoved/unknowninventory/QA11/device/child/owner open. Exactnative/source/doc/54tests6stress/2DNO_REGRESSION;R32full82retainedatunchangedproduction, no newfull82run. Finalmetadata/proof/CI remainseparate.

## Painted menu panel material reuse — CHG-042

- Planned at `d6b2a13ddf6991e4e96dab5fd70c4494e7f49121`; origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. Publication commits appended after delivery.
- Scope: FV-E9E82E0C6703,three named StartMenu Panel material reuse in nonruntime candidate. R34buttons/sourcePNG/production/hit/content/save geometry preserved;38publishedcontext/source files verified before edit.
- Benefit: replace namedflat fills/borders with reusedsame-neighborpainted paper/frame. Risks: flatcrest/bluepearlstyleconflict/duplicatecornerdecoration,opaque launchpaper,bottomcaptionfit,sourceapproval/phoneoverdraw/readability;allremainexplicit.
- Dependencies/evidence: [R35plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r35_menu_panel_reuse/PLAN.json), [impact](../design/audit_impacts/flat-vector-menu-panel-reuse-20261014.json), source/native/comparison/caller/doc/gates. Allglobalinventory/QA11/device/child/owner open.
- Rollback class:additive nonruntimecandidate/audit/navigation. Read-only planner on clean dedicated `codex/rollback-chg-042`; inspect exactcandidate/metadata diff andrerun source/document/impact gates. Preserveimmutablehistory;no runtime/save/protectedsourceinverse.

CHG-042 published payload `f70eec174599d971a1da9e5a94ed2b60bc804b66`: manifest/every4530required file/2382857879bytes anonymously verified at `2026-10-14T12:26:17.604720+00:00`, manifestSHA `ce627f16346d1b828acb6ada7907c9dabd550049647567ce312d07ab4d51e557`, payloadSHA `cefc95e0682197823ea7d153262d731882e63755d17ae2ae1aeb47fbf6498f63`. Threepanel materials repaired inisolatedcandidate;flatneighborcongruencyopen.126currentnative/72newcredits/54excluded,3125bounded/3875retained/750excluded cumulative.16currentviews/15uniqueviewhashes/12panelcomparisons/60sourcecalls29files,56existingpartial/12families,78partial176routes/98without/0complete;0acceptedremoved/unknowninventory/QA11/device/child/owner open. Exactnative/source/doc/54tests6stress/2DNO_REGRESSION;R32full82retainedatunchangedproduction, no newfull82run. Finalmetadata/proof/CI remainseparate.

## Painted menu ornament retirement — CHG-043

- Planned at `9730f40bbe725b71e2655653d04d5fea5d27bf34`; origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. Publication commits appended after delivery.
- Scope: FV-AB474EF3699E,31namedpuredecorative StartMenu nodes retired in nonruntime candidate. R35buttons/sourcePNG/production/hit/content/save geometry preserved;37publishedcontext/source files verified before edit.
- Benefit: remove31redundantflat decorative instances andrestorepaintedframe congruency. Risks: loss of visual grouping/cornercues,source/menuapproval,phoneperformance/nonreader readability;allremainexplicit.
- Dependencies/evidence: [R36plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r36_menu_ornament_retirement/PLAN.json), [impact](../design/audit_impacts/flat-vector-menu-ornament-retirement-20261014.json), source/native/comparison/caller/doc/gates. Allglobalinventory/QA11/device/child/owner open.
- Rollback class:additive nonruntimecandidate/audit/navigation. Read-only planner on clean dedicated `codex/rollback-chg-043`; inspect exactcandidate/metadata diff andrerun source/document/impact gates. Preserveimmutablehistory;no runtime/save/protectedsourceinverse.

CHG-043 published payload `5c03eda2735887995322b9f603dba0b135038622`: manifest/every4756required file/2569888003bytes anonymously verified at `2026-10-14T15:57:55.549891+00:00`, manifestSHA `53b810bb587f0149c12a1ef50534bd15b71b6a07b3ed7c2affc8afe3477fb17d`, payloadSHA `9368b022a47c4f87e0901762b9dd9197e692d02ac1ee4c5a49fe450c4ef19d05`. 31decorativenodeinstances (3crests28bluepearls) retiredonlyinpaintedcandidate;namedneighborcongruency addressed/allacceptanceopen.130currentnative/72newcredits/58excluded,3197bounded/4005retained/808excluded cumulative.16currentviews/16uniqueviewhashes/4beforeafterprofiles/17sourcecalls12files,56existingpartial/12families,78partial176routes/98without/0complete;0acceptedremoved/unknowninventory/QA11/device/child/owner open. Exactnative/source/doc/54tests6stress/2DNO_REGRESSION;R32full82retainedatunchangedproduction, no newfull82run. Finalmetadata/proof/CI remainseparate.

## Current source inventory reconciliation — CHG-044

- Planned at `01f670d7ab4933fe2c2e6605bbca4ef2105f200f`; reconciled origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. Publication commits appended after verified delivery.
- Scope: nonruntime source/resource/caller/glyph reconciliation; all369 frozen scope IDs and348 glyph IDs preserved. No production, protected original, save, art/generation, shared job writer or GPU changes.
- Benefit: identify source/caller and glyph-only audit gaps without inventing individual pieces or retirement evidence. Risks: lexical/AST candidates can be unreachable or typography; receiver/native/guard/font/runtime closure remains open.
- Rules: DL-AUTH-01/02/04/05/06/07,DL-VIS-07/08,DL-ASSET-01/03,DL-MED-02,DL-QA-11/14/15; MA-VIS-006/008 andMA-DOC-007 remain CONFIRMED_OPEN.
- Dependencies/evidence: [R37 plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r37_current_source_inventory/PLAN.json), [impact](../design/audit_impacts/flat-vector-current-source-inventory-20261014.json),source/canonical/stress/document/2D gates andretained actualR32full82/R35CI atunchangedproduction. No machine pass establishes visual/device/child/owner acceptance.
- Rollback: additive audit/navigation revision only. Use clean dedicated `codex/rollback-chg-044`, inspect exact payload/receipt/proof diffs and rerun source/document/coverage gates; preserve immutable history and prior runtime/save/protected sources.

CHG-044 published payload `efd1f89827ee1dc7d0531474b210c6d457c5a903`: manifest/every6337 required file/2675462383 bytes anonymously verified at `2026-10-14T17:25:12.576914+00:00`,manifestSHA `fc91293caf5fa2c26c33c73b916bf5f4a96e3e3259c236a208ab418af64159a0`,payloadSHA `21eef37b19a0311a05f41fc584c2353322d7ab15ed50285ca5d73c5bb80717f9`.312 parsed scripts/all369 frozen qualifiedfunction IDs rebound/348 glyph IDs preserved;814 broader syntax scopes536nonprobe278probe/90glyph-only scopes87nonprobe are candidates,not artpieces.302 exact glyph groups rebound/46 gaps.18 source stress cases,current source/canonical/docauthority740/impact/54tests6stress/2DNO_REGRESSION. No runtime/art/captures/dispositions/acceptance increment;225knownroles/30families,3197bounded/4005retained/808excluded,78partial176routes/98without/0complete.0acceptedremoved/unknownglobaldenominator/QA11/device/child/owner open. ActualR32full82/R35exactCI retainedatunchangedproduction,no new R37engine run. Finalmetadata/proof/CI separatelyrecorded.

## Frozen glyph-source reconciliation — CHG-045

- Planned at `8f48a0003a8a098658a3414414bd3da3c94f29c2`; historicalglyph source `92c9fe70319ef46bfaa8f61348a6f51512141ec3`,origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. Publication commits appended after verified delivery.
- Scope: all348 frozen glyph IDs/sourceorder/escaping/duplicates/scopedbinding in38 files/76revision pairs.347currentbindings/1priorR32source retirement;46group gaps resolved. No runtime/art/font/captures/generation/newretirement/sharedjob/save/protectedsource changes.
- Benefit: stop treating scanner grouping/category differences as missing source/art andretain the actualstillcurrent role backlog. Risk: source binding is notlive reach/font/semantic criticality/style/readability/acceptance. Allremainexplicit.
- Dependencies/evidence: [plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r38_glyph_reconciliation/PLAN.json), [impact](../design/audit_impacts/flat-vector-glyph-reconciliation-20261014.json), exacthistorical/currentsource/scopedretirement/14stress/canonical/doc/impact/tests/2D gates;retainedactualR32full82/R35CI atunchangedproduction. MA-VIS-006/008/MA-DOC-007 remain CONFIRMED_OPEN.
- Rollback: additive audit/navigation only; clean dedicated `codex/rollback-chg-045`,inspect exactpayload/receipt/proof diffs andrerun source/document/impact gates. Preserveimmutablehistory andruntime/save/protected sources.

CHG-045 scope extension: retain actual tracked post-R37 model-signature scan-limit failure (threeJSON/9findings). Split authored source/receipt metadata into bounded JSON text parts with exactlogical-byte/hash/immutable-original proof and reader compatibility;11roundtrip/negative cases andfresh18R37source cases supplement14glyph cases. Stage allnew evidence before2Ddiscovery;verify actual currenttracked state without auditor/manifest waiver. Future receipts bounded andallphysical parts included in delivery/finalproof. No runtime/root frozen arrays/protected source/art/acceptance changes.

CHG-045 published payload `4822680d134b522850d8772cef858908335e534d`: manifest/every 6572 required file/2876164523 bytes anonymously verified at `2026-10-14T18:40:38.033078+00:00`,manifestSHA `507e729f75937959e81569393606943b35a9d2a0f34c7e43f20d5c85be1c2ed1`,payloadSHA `fec4beb2caab5186b4db88bd84bff911f95cce9a3869deef5076359f37867642`. All348 frozen glyph IDs source-accounted:347current/1retained priorR32source retirement;45current+1prior retirement resolve46group gaps.14glyph/18source/11bounded cases; actual staged andpostcommit2D NO_REGRESSION with0models/0scancoverage;threeR37largeJSON logicallybytepreserved in84parts, unchanged auditor/manifest.54audit tests/6stress,docauthority741. No runtime/art/newretirement/capture/disposition/acceptance increment;225known/30families,3197bounded/4005retained/808excluded,78partial176routes/98without/0complete.0acceptedremoved/globaldenominator unknown; font/role/QA11/device/child/owner/fullcontext remainopen. ActualR32full82/R35CI retained; no new engine run. Finalreceipt/allparts/proof/CI separatelyrecorded.

## Craft compositor context audit — CHG-046

- Planned at `9d19fdc1f0ebdcac8c11d75adc56926bc43d136f`; reconciled origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. Published source/prerequisite31files anonymously verified before native work; final publication commits appended after verification.
- Scope: current Craft GUI body/accent/third/rainbow/finish/private save/re-entry,8 successful profiles/aspects/2 failed fixture attempts retained;420 files/300 bounded credits. Fish double eye/detached fin/tint and Detail preview gaps, same-scene ten axes,5 texture source scopes,Pass35 provenance and R7 caller exclusion correction.2 new stable shaded-plush design roles are not2 newly confirmed flat-art defects.
- Evidence: [plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r39_craft_compositor_context/PLAN.json), [impact](../design/audit_impacts/flat-vector-craft-compositor-context-20261014.json), capture/source/reuse/fixture/save/sidecar gates. Production/art/protected sources unchanged; no generation/new drawing/acceptance. Existing exact R32full82/R35CI retained at unchanged production.
- Benefit/risk: source-bound fish reuse can now proceed from current named context; sparse synthetic GUI evidence does not close natural downstream action, device, child, owner, QA11 or the unknown whole-game inventory.227 known roles/30 families,3497 bounded/4425 retained/928 excluded;78/176 partial/98 without/0 complete;0 accepted removed. Findings remain CONFIRMED_OPEN.
- Rollback: additive evidence/navigation only; inspect exact CHG-046 payload/receipt/proof diffs on dedicated `codex/rollback-chg-046`, preserve frozen histories/runtime/save/protected originals and rerun audit/document/impact/2D gates.

CHG-046 published payload `05159caa2bd1c7c338c38cc04d3772e86471a551`: all 7181 declared files/3038868333 bytes anonymously verified at `2026-10-14T20:32:30.139612+00:00`, manifestSHA `f3685e4de8351efc7f941795fc4b28df44077eb5adeff5c6c2903458231b12c2`, payloadSHA `bb558718479a49ca114e45ac6d9d019facbeab2924280bed09f804424f54780a`. R39 eight successful current GUI cases/420 retained/300 credits/120 excluded;227 known roles/30 families,3497 bounded/4425 retained/928 excluded;5 compositor source units,351 primitive scopes/98 missing route slices remain open. No runtime/new art/generation/accepted removal. Current diagnostic fixture/native and fresh audit gates separate from actual retained R32full82/R35CI; natural downstream/QA11/device/child/owner/global denominator remain open. Final metadata/allreceipt parts/proof independently verified.

## Craft whole fish source trial — CHG-047

- Baseline `69dfac241fb2bc3a51bbab138d4ddde952d60899`, reconciled origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`;27 source/context prerequisites remotely verified before one builtin generation call. Whole-unit owner contract and failed direct reuse gap documented before edit.
- One native complete painted fish source, one-layer Aseprite masters/exact native RGBA roundtrip/uniform1024 export; ignored one-TextureRect hue/fit prototype.607 native files/152 current credits/455 exclusions;13 invisible selector data PNGs kept separately.24 current/11 prior views and all8 current controls/private legacy-save cases pass; failed/partial attempts retained.
- [Plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r40_craft_whole_fish_trial/PLAN.json), [review](../docs/handoffs/codex_flat_vector_art_2026-10-07/r40_craft_whole_fish_trial/REVIEW.json), [impact](../design/audit_impacts/flat-vector-craft-whole-fish-trial-20261014.json), source/capture/functional geometry/sidecar/gates/manifest/receipt/proof. Production/protected/child saves unchanged; existing actual R32full82/R35CI retained only at identical production. Final publication revisions appended after exact byte verification.
- Candidate only: enlarged dorsal/anal pearl/color boundaries, Detail, full caller/fallback inventory,98 route gaps/351 primitive scopes and natural runtime/QA11/device/child/owner remain open. Two source samples pending;0 approved/integrated/accepted removed,global totals unknown; findings remain CONFIRMED_OPEN.
- Rollback: inspect CHG-047 additive source/evidence/navigation diffs on dedicated `codex/rollback-chg-047`; preserve native candidates/rejects/historical originals and child schema, rerun applicable audit/document/impact/2D gates. No release or dev promotion authorized by this trial.

CHG-047 published payload `0466a6e5300da701215010b6c072a167e2e00d0d`: all 8501 declared files/3353063431 bytes anonymously verified at `2026-10-14T22:24:55.004819+00:00`, manifestSHA `a9701c346ecbfa5dbaa9e02d25cf682d182cc2dc14d2b1401fed39ae3bc72cfa`, payloadSHA `1ef0fe80fee487cdb94a7faba61b77a8517764eef1f6a7382bcc2e69bda2b0e9`. R40 eight successful current GUI cases/607 retained/152 credits/455 excluded;227 known roles/30 families,3649 bounded/5032 retained/1383 excluded;5 compositor source units,351 primitive scopes/98 missing route slices remain open. One source-only fish drawing/call; no production integration/source retirement/accepted removal. Current diagnostic fixture/native and fresh audit gates separate from actual retained R32full82/R35CI; natural downstream/QA11/device/child/owner/global denominator remain open. Final metadata/allreceipt parts/proof independently verified.

## Companion consumer context audit — CHG-048

- Baseline `de44f9bb67ae7cb41a33d6eba25d56d9ed074f21`, reconciled origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`;31 published source/context prerequisites anonymously verified beforefixture.
- Original-source current Mewsha studio and Eagle/Lamb-a' swap/care/Canvascard contexts,6 supported native cases;167 files/56 credits/111 exclusions,14 current/10 prior direct views,6 source views. Initial missing-defaultCastle and four nonpaintable studio API diagnostic attempts retained/excluded. All pointer/identity/actualprivate save/reload checks pass;4039 sidecars/eightnormal save suffix hashes preserved.
- Direct TextureRect intrinsic-size clipping reproduced with8 current-order failures and8 corrected-order fits,usingreal official4.7.2 controls/textures/exact roster formula. Third-color token persists butall8 large-preview ROI hashes identical atboth aspects. Style/title/ambient/source/caller gaps recorded;no game fix/newart/generation/source retirement.
- [Plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r41_companion_context/PLAN.json), [review](../docs/handoffs/codex_flat_vector_art_2026-10-07/r41_companion_context/REVIEW.json), [impact](../design/audit_impacts/flat-vector-companion-context-20261014.json), [source diagnosis](../docs/handoffs/codex_flat_vector_art_2026-10-07/r41_companion_context/PREVIEW_SIZE_PROOF.json), manifests/parity/gates/receipt/proof.3 observed identity roles addone thematicfamily,not3 confirmedflatartworks:230roles/31families,3705bounded/5199retained/1494excluded.78partial/98without/0complete,351primitive scopes/5fullcompositorclosures open;0acceptedremoved/globalunknown.
- Risk/acceptance: Original/protected/child/save/production pixels unchanged. Source-preservingdirectpreviewfitrepair nextafterpublication;wholeunit/third/material/naturalaction/battle/follower/Studio/QA11/device/child/owner andfullinventory remainopen. Existingfinding lifecyclesCONFIRMED_OPEN.
- Rollback: inspect additive CHG-048 source/evidence/navigation diffs on dedicated `codex/rollback-chg-048`,preserveallfrozenhistory/originals/private diagnostic provenance andrerun document/impact/2D gates. No dev/master release authority added.

CHG-048 published payload `c4a81db15bcd3562d58455dd3bf9cdda6f65e7a2`: all 9597 declared files/3677815465 bytes anonymously verified at `2026-10-14T23:20:03.921654+00:00`, manifestSHA `d6caa814833bdc529eb8724202c38fdb6caf8a1fe17619690aa64ccb5631c8fb`, payloadSHA `7e07dc9c4bba64ab0c3015e98aa729e586dd36a50abcbb338ddfb88b2368075b`. R41 six supported current GUI cases/167 retained/56 credits/111 excluded;230 known roles/31 families,3705 bounded/5199 retained/1494 excluded;5 compositor source units,351 primitive scopes/98 missing route slices remain open. No new source drawing/generation; no production integration/source retirement/accepted removal. Current diagnostic fixture/native and fresh audit gates separate from actual retained R32full82/R35CI; natural downstream/QA11/device/child/owner/global denominator remain open. Final metadata/allreceipt parts/proof independently verified.

## Companion preview-fit trial — CHG-049

- Baseline `ef3b12fc456720bce2123876fe042ccd9e191505`, origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`;69 exact published source/context files anonymously verified before prototype.
- Ignored direct preview-fit subclass sets expand/stretch before original texture and requested size. Six supported Mobile/Speedy GUI cases/100native/56credits/44excluded,40 exact live boxes;12current+4prior direct views. Mewsha delegates unchanged;third-color pixel failure retained atboth aspects.4039 sidecars and8normal save suffix hashes unchanged.
- [Plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r42_companion_preview_fit/PLAN.json), [review](../docs/handoffs/codex_flat_vector_art_2026-10-07/r42_companion_preview_fit/REVIEW.json), [impact](../design/audit_impacts/flat-vector-companion-preview-fit-20261014.json), native/proof/parity/gates/manifest/receipts.230roles/31families,3761bounded/5299retained/1538excluded,78partial/98without/0complete routes;351primitive scopes/5fullcompositor closures open,0accepted/globalunknown. Frozen history preserved;stale R41 explanatory arithmetic corrected from its already-correct authoritative summary without changing past totals.
- Risk/acceptance: no production/art/generation/adoption/source retirement. Third/title/style/contact/ambient/callers/natural motion/QA11/device/child/owner and whole-game inventory remainopen;findings stayCONFIRMED_OPEN. Publication is mandatory and separately verified.
- Rollback: inspect additive CHG-049 evidence/navigation diffs on dedicated `codex/rollback-chg-049`;preserve all immutable history and later work. No dev/master promotion or production rollback involved.

CHG-049 published payload `d047c5b6d9f9297abd77bfddc7f5c928a3e1f294`: all 10081 declared files/3916026211 bytes anonymously verified at `2026-10-14T23:51:40.051656+00:00`, manifestSHA `510196674a13dc9fe1b1f19867d04641eedc308cc83edc37d595136a342633d5`, payloadSHA `9c3b26352430f3c62367da328e5c94805ed1c498879641a4f96107a5dcc5d365`. R42 six supported current GUI cases/100 retained/56 credits/44 excluded;230 known roles/31 families,3761 bounded/5299 retained/1538 excluded;5 compositor source units,351 primitive scopes/98 missing route slices remain open. No new source drawing/generation; no production integration/source retirement/accepted removal. Current diagnostic fixture/native and fresh audit gates separate from actual retained R32full82/R35CI; natural downstream/QA11/device/child/owner/global denominator remain open. Final metadata/allreceipt parts/proof independently verified.

## Whole Mewsha material/palette trial — CHG-050

- Baseline `1ca647a57943dc4b6a645f7cffb85a9be600f173`, origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`;97 exact published context/source files verified before one builtin imagegen edit. Ten reusable files/seven unique hashes fail the named identity/material/whole-unit gap; protected originals/child data remain untouched.
- One whole painted source candidate, native1254 RGBA/editable masters/exact decodedRGBA roundtrip/1024 bilinear export;one call cap used1/exhausted. No crop/recolor/redraw/part separation in technical normalization. Analytic invisible palette selectors drive body/horn/proposedheart slots ononeTextureRect,notartlayers.
- Actual6current GUI cases/100current+32prior visualguardfail files,60credits/72exclusions;3slotsx8distinctROI resultsx2aspects,privateSaveState/care/Castle/reload tokens match,124whole-image geometry observations/40nonpaintable fitcontrols.12current+3prior+2publishedbefore directviews. Initialpinkeyehalos/whiteheartclipping source/failure retained;currentguard fixes onlyfunctionaleligibility.4039sidecars/normal8save suffixes unchanged.
- [Plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r43_mewsha_whole_trial/PLAN.json), [review](../docs/handoffs/codex_flat_vector_art_2026-10-07/r43_mewsha_whole_trial/REVIEW.json), [impact](../design/audit_impacts/flat-vector-mewsha-whole-trial-20261015.json), proof/callerinventory/gates/manifest/receipts.230roles/31families,3821bounded/5431retained/1610excluded;3unaccepted samples,0acceptedremoved/globalunknown.78partial/98without/0complete routes,351primitive scopes/5fullcompositor closures remainopen. No runtime integration/fallback retirement.
- Risk/acceptance: Nativealpha boundary clearance/fullcontour,exactidentity/catchlights/whiskers/material density/contourwidth/contact/phone performance/readability remainopen;third-heart assignment is a candidateproposal. No creative/owner/child/device/QA11 acceptance or lifecyclechange. Existingfull82/CI evidence scoped to byte-identical production;newruns distinct. Publication mandatory andseparately verified.
- Rollback: inspect additive CHG-050 source/evidence/navigation diffs on dedicated `codex/rollback-chg-050`;preserve immutable history/later work/protected originals. No dev/master promotion or runtime rollback involved.

CHG-050 published payload `371daef9ec3402a7b8aa18c4eff147a9b9d5a3b5`: all 10565 declared files/4154762174 bytes anonymously verified at `2026-10-15T00:43:53.496934+00:00`, manifestSHA `2b88ad8cb83f90fd2ab2a9c955a5336dbe43e5e29f7e06b01404a2f99a1ae60c`, payloadSHA `a05183d82f381ac98a3ec76b6cdd38d27dbf6da461c18aa0b97082fe14634c04`. R43 six supported current GUI cases/132 retained/60 credits/72 excluded;230 known roles/31 families,3821 bounded/5431 retained/1610 excluded;5 compositor source units,351 primitive scopes/98 missing route slices remain open. One new wholeMewsha source drawing/1generationcallcap exhausted;localartQC remainsopen,3unaccepted samples. No productionintegration/source retirement/acceptedremoval. Current diagnostic fixture/native and fresh audit gates separate from actual retained R32full82/R35CI; natural downstream/QA11/device/child/owner/global denominator remain open. Final metadata/allreceipt parts/proof independently verified.

## Creature route and caller audit — CHG-051

- Baseline `ccbe6d60e4021977c520844797d4d36086ad6e73`, origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`;111 exact anonymous published prerequisites before ignored fixture creation. No production/art change or generation.
- [Plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r44_creature_route_caller_audit/PLAN.json), [review](../docs/handoffs/codex_flat_vector_art_2026-10-07/r44_creature_route_caller_audit/REVIEW.json), [impact](../design/audit_impacts/flat-vector-creature-route-caller-20261015.json):312scriptAST/49targetcalls(29non-test candidates,20probe/test);95unresolved non-testdynamic targets. Missing named sparring/roomtick callers do not prove global unreachability. Initial filename classification retained.
- Six exact official4.7.2 Mobile/Speedy private cases retain73native source/checkpoint/API views,all excluded from new context/route credit. Startup still constructs retained follower;promenade uses Canvas care;Hall doesn't create Studio. Forced battle HUD overlays courtyard while3D arena is hidden;forced Studio is hidden by Castle. Constructors/visibility flags are not normally reachable route or pixel evidence.
- Six Main fish/cat/bird constructor calls retain3Sprite3D resource layers/body/line tints;animated accent samples differ. Corrected initial equality assumption is archived with raw data;no native rerun. Fallback source omits third in callback;no accent/pixel invariance claim.
- Normal8save suffixes/4039sidecars/private identity/reload andbattlecancel/ownedStudio cleanup pass.230roles/31families,3821bounded/5504retained/1683excluded;3unaccepted samples,0accepted/globalunknown.78partial/98without/0complete routes,351primitive scopes/5fullcompositor closures andQA11/device/child/owner remainopen. PriorR32full82/R35CI retained only at unchanged production.
- Risk/acceptance: source absence/dynamic calls/node presence cannot establish route closure or accept art. R43 boundary/identity/material/contactQC remainsopen. No lifecycle change or source/3D retirement. Publication/all remote bytes and receipt parts are mandatory and separately verified.
- Rollback: inspect additive CHG-051 source/evidence/navigation diffs on dedicated `codex/rollback-chg-051`; preserve immutable history/later work/protected sources. No dev/master promotion or runtime rollback involved.

CHG-051 published payload `79ff8a0134b4cd58d96131d4d51aab12a4fa3d71`: all 11347 declared files/4460874152 bytes anonymously verified at `2026-10-15T01:55:59.169681+00:00`, manifestSHA `93f1399f325282b205eb974659cd7801e6f845634291b8b5c475883432d446c6`, payloadSHA `5406cfb0895e4a8617c597b8d536a5f62c00a44a026e2285b4a61b5ace44c645`. R44 six source-bound native cases/73retained diagnostic captures/all73excluded from newcontext orroute credit;230known roles/31families,3821bounded/5504retained/1683excluded.312scriptAST/49targetcalls/95non-testdynamic targets unresolved;5fullcompositor closures/351primitive scopes/98route gaps remainopen.0newart/generation,3prior samples unaccepted. No productionintegration/source retirement/acceptedremoval. Current diagnostic fixture/native and fresh audit gates separate from actual retained R32full82/R35CI; natural downstream/QA11/device/child/owner/global denominator remain open. Final metadata/allreceipt parts/proof independently verified.

## Dispatch semantics and callback ports — CHG-052

- Baseline `e17c929d22fdf749fffb1ad2acdaeff7059c21a1`, origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`;331 exact published source/graph/context prerequisites before classifier. No runtime/art/source-retirement or generation change.
- [Plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r45_dispatch_semantics_audit/PLAN.json), [review](../docs/handoffs/codex_flat_vector_art_2026-10-07/r45_dispatch_semantics_audit/REVIEW.json), [impact](../design/audit_impacts/flat-vector-dispatch-semantics-20261015.json): all493 raw IDs retained at312 exact source files.257 non-test candidates =100 constructors/defaults/bindings +157 invocations;100 known selectors/57 callback target gaps in39 scoped declaration groups. R44 raw95 reconciled;two empty cancellation payloads correctly classified as callback data. Two standard Main callback bindings are examples, not global target closure.
- Exact official4.7.2 headless semantics13 checks and20 adversarial source tests pass. Current97 Native ClassDB records use hashed filenames;first passing source/output is preserved in a verified105-member ZIP. All97 metadata bytes match;no class-query loop instantiation. Fixture uses2 RefCounted targets and its SceneTree, no game scene/world/camera/light. Normal8 save hashes/4039sidecars unchanged. Actual full staged/committed2D gates and exact remote publication remain required.
- Frozen arrays/stable IDs/history preserved.230roles/31families,3821bounded/5504retained/1683excluded,3unaccepted samples/0accepted/global unknown.0 new rendered/art/route credits;78partial/98without/0complete routes;351primitive scopes/5fullcompositor closures andallnatural/QA11/device/child/owner acceptance remain open.
- Risk/acceptance: a known method selector or scoped declaration does not prove navigation, runtime implementation, full write/caller domains, visible art or human acceptance. R43 boundary/identity/material/contact QC remains open. No finding lifecycle changes. Prior full82/CI applies only to unchanged production;current source/language evidence is separate.
- Rollback: inspect additive CHG-052 audit/evidence/navigation diffs on dedicated `codex/rollback-chg-052`;preserve immutable history/later work/protected originals. No dev/master promotion or runtime rollback involved.

CHG-052 published payload `57f6e1b07e1cb5ad3087b30caf53851e3d4f657a`: all 11965 declared files/4615420796 bytes anonymously verified at `2026-10-15T03:26:57.927144+00:00`, manifestSHA `0a6101cef73e7b9918dd49a014265e1e1ce98627679e2104f904a4c03e6e306f`, payloadSHA `10a37f47601766e4c435f3cdcea7bbecc2f6e5e6577838de8d3cf8ea097d1695`. R45 preserves493 raw expressions/312 exact scripts;257 non-test candidates separate100 bindings/defaults from157 invocations,100 known selectors/57 callback target gaps in39 declaration groups.13 actual headless checks/97 native metadata records/20 source-boundary tests;0 new game renders/art/route credit.230roles/31families,3821bounded/5504retained/1683excluded,3unaccepted samples/0accepted/global unknown;5fullcompositor closures/351primitive scopes/98route gaps andallacceptance remain open. No productionintegration/source retirement/acceptedremoval. Current diagnostic fixture/native and fresh audit gates separate from actual retained R32full82/R35CI; natural downstream/QA11/device/child/owner/global denominator remain open. Final metadata/allreceipt parts/proof independently verified.

## Melody current-source context — CHG-053

- Baseline `7cdb9bf63bd8f3846b34b17cce74b065747aae92`,origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. [Plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r46_melody_context/PLAN.json), [review](../docs/handoffs/codex_flat_vector_art_2026-10-07/r46_melody_context/REVIEW.json), [impact](../design/audit_impacts/flat-vector-melody-context-20261015.json).23 published source/context prerequisites before fixture;initial workspace CRLF comparison stopped and exact Git blob verification corrected before capture.
- Actual official4.7.2 Mobile/Speedy GUI at1280/1600x720;58native/48bounded/10excluded,real seven-note touch progression,re-entry/neutral exit. Normal8save suffix hashes and4039sidecar bytes unchanged. Direct API entry only,natural route unverified;no production/art changes.
- Eleven frozen Melody role IDs retained;ten visibly flat roles gain partial same-scene context. Initial candidate inventory was reconciled against all11 IDs before adding records;no duplicate roles.8actual native frame views,2painted-source views,six hashed reuse leads. No generation/fit/replacement/owner acceptance.
-230roles/31families,3869bounded/5562retained/1693excluded;80partial catalogue aliases/96without/0complete,not distinct screens. Global denominators,351primitive scopes,fivefull compositor closures andallnatural/device/child/owner/QA11 gates stay open.
- Rollback: inspect additive CHG-053 evidence/navigation on dedicated `codex/rollback-chg-053`,preserve frozen records/immutable history/later work/protected art. No dev/master integration or runtime rollback.

CHG-053 published payload `ac874448d128b09e21e9a3511bc883ff0f0799bb`:all12238 requiredfiles/4705880740 bytes anonymously verified at `2026-10-15T04:17:02.613014+00:00`. ManifestSHA `db27d300ab2e9bb2ae65f6e9502824868e7cefc5c6121bccd28dc844dfcedce8`,payloadSHA `840ab4a5de25df690c8be58ebc4eccc139cb1526f69e73da441297cee252b6fc`.58native/48bounded/10excluded;11frozenMelody IDs/10visible andsixreuse leads.230roles/31families,3869bounded/5562retained/1693excluded,80partialcataloguealiases/96without/0complete;naturalentry/globaltotal/allacceptance open. No runtime/art change/generation/accepted removal.

## Day One Playroom and Art Room context — CHG-054

- Baseline `dca7e7ce8d712b2b16ab004b7fcd070d3133b8b7`,origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. [Plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r47_day_one_room_context/PLAN.json), [review](../docs/handoffs/codex_flat_vector_art_2026-10-07/r47_day_one_room_context/REVIEW.json), [impact](../design/audit_impacts/flat-vector-day-one-room-context-20261015.json).35exact published prerequisites beforefixture;83current source/image references bind selected actual renderers/consumers.
- Four actual official4.7.2 Mobile/Speedy GUI cases at1280/1600x720:declared private checkpoints toHall,real door/pin-or7cleanup/desk input,private save/reload andactual room re-entry. Normal8save hashes/4039sidecars exact,no runtime/art/protected-source edits.
- First fixed-frame picker check failed;12PNGs/exact executed source/wrapper/report/log retained. Current control-ready wait passed both rescue cases after468/451ms extra wait;toy-nook recovery notexecuted. No production defect/fix or fabricated natural full journey.
- Five newly named caller/visual roles plusseven additional frozen-role partial contexts;235knownroles/31families. Rescue pointer/burst shareone existing star asset;these are notfive newdrawings. Four grime roles bind current functions;historical separate interior-edge role remainsunbound. Child-authored mark variants/keys remainprotected andunreviewed. Existing PNG format orroom use doesnot establishpainted/zero-flat acceptance.
-108native/78bounded/30excluded;13actually viewedframes(3prior diagnostics).3947bounded/5670retained/1723excluded;82partialcatalogueentries/94without/0complete,not distinctscreen totals.73existing partial IDs/15families and11supplemental partialroles;3unaccepted drawings/0accepted/global unknown.351primitive scopes/fivefull compositor closures andallnatural/QA11/device/child/owner evidence open.
- Rollback:inspect additive CHG-054 evidence/navigation on dedicated `codex/rollback-chg-054`;preserve immutable source/history/laterwork/protectedart. No dev/master integration orruntime rollback.

CHG-054 published payload `9bed85ed191d85e7b563abf324ca8e42755e664e`:all12614 requiredfiles/4949120555 bytes anonymously verified at `2026-10-15T05:13:50.019430+00:00`. ManifestSHA `124d5d312b8230a943efbcfa613c7e0b8244d9e1e803c3d3c9d6214858764d97`,payloadSHA `9d8349783458f599b6dbe5a298d8c036a68392bec6b5bccc8e68e3fc807af480`.108native/78bounded/30excluded;four current DayOne door/action/reload cases,five newcaller roles.235roles/31families,3947bounded/5670retained/1723excluded,82partialcatalogueentries/94without/0complete;fullnaturaljourney/globaltotal/allacceptance open. No runtime/art change/generation/accepted removal.

## Grand Puff current encounter context — CHG-055

- Baseline `677ee7b734c9c58dc2464c99f021715d347835db`, origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. [Plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r48_grand_puff_context/PLAN.json), [review](../docs/handoffs/codex_flat_vector_art_2026-10-07/r48_grand_puff_context/REVIEW.json), [impact](../design/audit_impacts/flat-vector-grand-puff-context-20261015.json).24 exact published prerequisites before fixture; domain authority rechecked at caller review.
- Two unmodified official4.7.2 Mobile/Speedy actual portal/encounter cases at1280/1600x720. Source geometry is a declared bot oracle; all-room/clip/companion checkpoints synthetic.60native/56bounded/4excluded,12native/3source direct views. Normal8save hashes/4039sidecars unchanged.
- Five caller roles in new GrandPuff family, not five unique drawings/confirmed defects. Current landing/lane warnings retain painted source pixels and invisible geometry. Veil may be functional compositing, disposition pending. Splash identity frames clip the body at both widths; preserve source and fix layout in later authorized repair. Hidden splash rehearsal follows current caller-specific owner direction. No score fabricated.
-240knownroles/32families;4003bounded/5730retained/1727excluded.83partial catalogue entries/93without/0complete;73existing partial IDs plus16supplemental roles. Global denominators,351primitive scopes,fivefull compositor runtime closures andallnatural/strictCanvas/QA11/device/child/owner gates open. No new runtime/art/generation/acceptedremoval.
- Rollback: inspect additive CHG-055 evidence/navigation on dedicated `codex/rollback-chg-055`; preserve immutable history, later work and protected sources. No dev/master integration or runtime rollback.

CHG-055 published payload `769b777a802a7c38500d0b7a9a2e2dd40673ac5b`:all12939 requiredfiles/5180085026 bytes anonymously verified at `2026-10-15T05:55:55.571168+00:00`. ManifestSHA `87d67d4f68407405ef6668bfa04db3bf547d93ad6589af5582a53f5bef06ae2b`,payloadSHA `193cb6a18c90c4fdb49fd8ee47da5785c1a1dcdcfc2863100ceead44d3b43e97`.60 native/56 bounded/4 excluded; two source-assisted Grand Puff portal/encounter cases,five new caller roles.240 roles/32 families,4003 bounded/5730 retained/1727 excluded,83 partial catalogue entries/93 without/0 complete;fullnaturaljourney/globaltotal/allacceptance open. No runtime/art change/generation/accepted removal.

## Callback source-path domains — CHG-056

- Baseline `61d12c5b7d29cd106a817d8d0064aa60f48f3ed2`, origin/dev `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`. [Plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r49_callback_value_domains/PLAN.json), [review](../docs/handoffs/codex_flat_vector_art_2026-10-07/r49_callback_value_domains/REVIEW.json), [impact](../design/audit_impacts/flat-vector-callback-value-domains-20261015.json).330 exact public prerequisites before source classification/component fixture.
-312 unchanged active-folder scripts yield922 AST rows;338 invocation IDs match preserved R45 expressions. Nine standard source-path chains cover14 sites;43 outside subset andall57 full runtime/native/alias/resource domains stay open. Keep12 probe callers andcomputed mutation risks separate.
- Actual official4.7.2 headless TouchUI component checks21/21;8normal save suffixes and4039sidecars unchanged. No Main/game render/Royal Hall runtime, artwork/source alteration, generation, new capture/route or acceptance credit. Counts remain240known/32families,4003bounded/5730retained/1727excluded,83partial/93without/0complete,0accepted/globalunknown.
- Rollback: inspect additive CHG-056 evidence/navigation on dedicated `codex/rollback-chg-056`; preserve immutable history, protected sources and later work. No dev/master integration or runtime rollback.

CHG-056 published payload `3f191462fddfa7052587eb1e2a16fba8e0722708`:all13419 required files/5276583739 bytes anonymously verified at `2026-10-15T07:13:31.050635+00:00`. ManifestSHA `6abc58ec4a22c3fff333b30cdb3ba99649b8742aa46ad31b20c15c30d69fcfa7`,payloadSHA `5ef37493a93aeb0c070be7cafac93e5b9c12d815cdbc2cae994ce6bf068d20f7`.312 source scripts/922 AST rows;9 named source paths/14 invocation sites,all57 full runtime domains still open.21 headless component checks;no new art/capture/route credit.240 roles/32families,0 accepted/globalunknown/allacceptance open.

CHG-056 freshness amendment: origin/dev advanced from831d0bbb to `5120b6d59885dd057937aaf284e73681d8eac9f5` during finalization (665 changed paths,23 product paths:20 scripts/3 objective-audio files). R49 receipt `b9e61c8c886e0e2683d8be9a68ec9545c6041ffa` and all13419 payload dependencies remain published/verified.312 source hashes compared;18 selected callback/owner/binding method bodies exact at both sources. Fresh full inventory/caller/runtime-context review of incoming changes remains required; no merge, artwork credit, accepted removal or regression count inferred. New exact anonymous source/authority/product proof is UPSTREAM_RECONCILIATION.json; final amended metadata receipt follows.

## Upstream source inventory refresh — CHG-057

- Topic baseline `4c5c026fd4a3c1ffaded5f13a123a28a2e13f677`; immutable audited origin/dev `5120b6d59885dd057937aaf284e73681d8eac9f5`. [Plan](../docs/handoffs/codex_flat_vector_art_2026-10-07/r50_upstream_source_refresh/PLAN.json), [review](../docs/handoffs/codex_flat_vector_art_2026-10-07/r50_upstream_source_refresh/REVIEW.json), [impact](../design/audit_impacts/flat-vector-upstream-source-refresh-20261015.json).330 public immutable prerequisites before collection. No source merge/runtime change.
-312 scripts parsed;369 frozen functions/348 glyph IDs preserved,825 additional source candidates.25 script differences/137 qualified function changes/9 top-level delta files;13 additional candidate scopes and2 absent probe scopes versusR37.4420 runtime-root paths/18JSON catalogues parsed. Counts remain source units,not artworks or accepted removals.
-506 dispatch expressions separate102 non-test constructors from157 invocations/57 unresolved.927 mutation/caller risk rows preserve historical evidence and qualify changed excerpts. No new engine/game/scene run,art generation,capture/route credit,disposition or acceptance.240known roles/32families,0accepted/globalunknown; all historical totals retained and current-upstream context transfer pending.
- Rollback: inspect additive CHG-057 evidence/navigation on dedicated `codex/rollback-chg-057`; preserve immutable history,protected sources and later work. No dev/master integration or runtime rollback.

CHG-057 published payload `f83bd2028f343e4bb6ddf30e0008c40429aca059`:all15282 required files/5432876919 bytes anonymously verified at `2026-10-15T08:13:58.603532+00:00`. ManifestSHA `57afb6cb42ab3362add0bf28bc1d0fb92ad075a9c649d8b3c2643f39d4c1f489`,payloadSHA `ce37f4716fa88fc979759bb9363fbe9f7a56ad1ace669682c0beea69623e87ed`.312 source scripts/1510inputs/369frozen functions rebound/825additional source candidates.25 changed scripts/137 qualified function changes/9top-level delta files;506dispatch/927mutation records,57callback runtime domains open.4420runtime-root paths/18JSON catalogues;no engine/game/scene runs,new art/capture/route credit.240 roles/32families,0 accepted/globalunknown/allacceptance open.

<a id="farmer-current-context-chg-058"></a>
## CHG-058 — Farmer current-context audit (2026-10-15)

- Scope: [R51 plan/review/manifest](../docs/handoffs/codex_flat_vector_art_2026-10-07/r51_farmer_context/README.md); [impact](../design/audit_impacts/flat-vector-farmer-context-20261015.json). Audit branch801b36a5 remains production-source unchanged;runtime native source5120b6d5 uses separate clean managed checkout.
- Two continuous original viewport cases complete gather5/fill5/drag delivery;private synthetic post-boss/startup room seams are explicit. Original private reload case fails after gathering:disk completion64 precedes fill/delivery;this is not fixed by continuous success. Normal saves andall4420source/4041initialized sidecar bytes unchanged.
-120native files add96bounded/24excluded;totals4099bounded/5850retained/1751excluded. Stable240role records/32families retained;83partial catalogue entries/93without/0complete;global artwork/screens/regressions unknown,0accepted. Six point-by-point observations attach exact sources andsame-scene comparison;no new generation orruntime code/adoption.
- Machine/document/2D signatures andpublication receipts remain separately evidenced;they do not accept art,natural journey,QA11 ordevice/child/owner lanes. Existing finding lifecycles remain unchanged.
- Rollback: inspect additive CHG-058 audit/navigation on a dedicated codex rollback branch,preserving frozen history andlater changes. No runtime rollback orrelease authority.

CHG-058 payload `8cdf8df7373615d827357e9cfa8ecce4aa373e05`: all 257 direct R51/source/canonical files (218477317 bytes) anonymously verified at `2026-10-15T09:22:52.966440+00:00`. ManifestSHA `eddfd9ce98718d4e543892aa4632ac0e456c03141d5fbc6a64ff56544fae7d97`, payloadSHA `7595ed8a2c8eae0bcf6e1c616633e336cdd0c20814396f291ab1086645b874df`. Historical R50 transitive verification retains its immutable receipt/time. Two continuous cases pass; harvest-only cold resume fails; 120 native/96 bounded/24 excluded, 0 replacements accepted and global totals unknown.

<a id="farmer-panorama-reuse-chg-059"></a>
## CHG-059 — Farmer panorama reuse fit (2026-10-15)

- [R52 plan/review/native/manifest](../docs/handoffs/codex_flat_vector_art_2026-10-07/r52_farmer_panorama_reuse/README.md); [impact](../design/audit_impacts/flat-vector-farmer-panorama-reuse-20261015.json). Topicbaseline65adbc4a,actualruntime5120b6d5;allproduction/protected bytesunchanged. CurrentR51context59selectedreferencesverifiedpublicbeforefixturework.
- Twoactual Mobile/Speedy cases useoriginal gather/fill/deliverycontrols. Ignoredvisual-onlyclasscomparesoriginal,center448,lower672andrestore;40story/phase/progress/root/surfacechecks unchanged. Center448losespathandisrejected. Lower672closes448rowgapandpreservesall460800lowercomponentpixels;retainedforfurtherreview,notadopted/approved.
-81native=30unchangedsourcecontrols+44nonruntimecandidatecaptures+7diagnostics;74bounded. Totals4173bounded/5931retained/1758excluded;240roles/32families,83partial/93without/0complete,0accepted/globalunknown. No newdrawings/generation;source reuse/candidate andcurrentproductionlanesseparate. Nativecoverage,upperhierarchy,allcallers/fullmotion/QA11/device/child/owner remainopen;R51otherweaknessesandsavefailureunrepaired.
- Allnewphysicalfiles needimpactcoverage,documentauthority/development gatesandactualstaged/committed2D beforepushes;publicationreceiptsbindexactremote bytes separatelyfromacceptance.
- Rollback: inspect additiveCHG-059 audit/navigation on dedicatedcodexrollbackbranch,preserving frozenhistoryandlaterchanges. No productionrollbackorreleaseauthority.

CHG-059 payload `88711cc99993a69dabbfa9ffd3d61a3c40a56266`: all 205 direct R52/source/canonical files (162713292 bytes) anonymously verified at `2026-10-15T10:01:08.195288+00:00`. ManifestSHA `6a5a10641b9ae3146e03dd9dc9e704e13c0aeb352fac911c196fb7ea20671be5`, payloadSHA `a2bcce7a86ef98f751f9d596e4715ea871ac52be08569a074cd18a44b7ec3229`. Historical R51/R50 transitive verification retains its immutable receipts/times. Two visual-only reuse cases pass; 40unchanged-state checks and460800exactlowerpixels.81native/74bounded/7excluded separate30currentcontrols/44candidatecaptures;noadoption/newdrawing/generation,0accepted/globalunknown. HistoricalR51savefailure remainsunrepaired.

<a id="castle-logo-context-chg-060"></a>
## Castle crest studio context (CHG-060)

2026-10-15: [R53](../docs/handoffs/codex_flat_vector_art_2026-10-07/r53_castle_logo_context/README.md) audits source5120b6d5 original paint-table/crest controls at both widths. Preserve all140 initial numeric-type fixture diagnostics; two corrected native cases pass136 checks. Twelve native/three source views bind flat backing, selector/preview identity mismatch and scoped title/toast overlap. Saved choices/room copies survive private same-engine reload; no pending write existed at background. Runtime/protected bytes unchanged. 240 roles/32 families;4313 bounded/6211 retained/1898 excluded;84 partial catalogue aliases/92 without/0 complete,0 accepted/global unknown. Applicable findings and acceptance remain open. Rollback removes only this audit delta; never revert child content or runtime source.

CHG-060 payload `03dfe4b482c8052753749b5e63b5309c45aed267`: all 431 direct files (153392806 bytes) anonymously verified at `2026-10-15T10:51:48.538045+00:00`; manifestSHA `c170b34cbd40f5538988e6d949d4878582a33219b398e47c64c1505408b0f4a0`, payloadSHA `81ea3683356df27cbf483b679e8c63caa2412078de60ced8e364423167179616`. Two current native cases pass136 checks;280 native/140 bounded/140 excluded initial fixture diagnostics. 12 native/3 source views,240 roles/32 families;0 accepted/global unknown. Historical R52/R51 retain original verification and acceptance limits.

<a id="castle-logo-motif-reuse-chg-061"></a>
## Castle crest motif reuse (CHG-061)

2026-10-15: [R54](../docs/handoffs/codex_flat_vector_art_2026-10-07/r54_castle_logo_motif_reuse/README.md) tests exact eight-source motif reuse for selector/status identity after published R53 context. Two original-control native cases pass252 checks/116 local-layout/state mode comparisons;15 native/8 source views.372 retained/118 bounded/254 excluded comparison frames,4431 bounded/6583 retained/2152 excluded overall. No art generation, production change, new role/family/review request or acceptance.240 roles/32 families,74 existing partial IDs/15 families,84 partial catalogue aliases/92 without/0 complete. Whole-game denominator unknown. Rollback only this audit delta; never change saved child content.

CHG-061 payload `c8235022c5b327f5cfbe8a1f464663c0d1229a45`: all 523 direct files (173801410 bytes) anonymously verified at `2026-10-15T11:26:42.673756+00:00`; manifestSHA `3800bc3006dba2d3f65d1cb267fd040c76fa3acbff944175384e1d4e1bc54b80`, payloadSHA `9c23db61a1fd7d47955773635f7d9b8a6ef2239e9166fba76fc7aa4f875a73c0`. Two current native reuse cases pass252 checks/116 state-local-layout comparisons;372 native/118 bounded/254 excluded comparisons.15 native/8 source views,240 roles/32 families;0 accepted/global unknown. Historical R53/R51 retain original verification and acceptance limits.

<a id="comfy-room-context-chg-062"></a>
## Original Comfy room context (CHG-062)

2026-10-15: [R55](../docs/handoffs/codex_flat_vector_art_2026-10-07/r55_comfy_room_context/README.md) binds original room controls, passive, hunt, supper, movie counts, bedtime, repeat and private mid/final reload at two aspects;88 checks. Two fixture failures/62 frames retained, plus4 current boot diagnostics.184native118bounded66excluded;4549bounded6767retained2218excluded overall.15 native9 source views;12 consumer occurrences9 textures do not add art roles. Pot full-stove reuse, blank movie/duplicate frame, duplicate identity staging, ingredient congruency and flat room/UI scopes remain open.85partial aliases91without0complete;240roles32families,74existing partial IDs15families;0accepted/globalunknown. Rollback this audit delta only; preserve originals/child save identities.

CHG-062 payload `02ebffa85fe2b1cd1fb01ad6382cfe27397e3038`: all 411 direct files (299518934 bytes) anonymously verified at `2026-10-15T12:19:52.120084+00:00`; manifestSHA `1807c634744d13614ba2abae6ad399219bfb748f15093b7d465daaa8f2152aa9`, payloadSHA `9fc221b0febdf5df0aa6a921e42e7ffc115725dd455d2b2d6635e7795725bd6a`. Two current native cases pass88 checks;184 native/118 bounded/66 excluded fixture and boot diagnostics.15 native/9 source views,240 roles/32 families;0 accepted/global unknown. Historical R54/R51 retain original verification and acceptance limits.

<a id="comfy-pot-ownership-chg-063"></a>
## Current pot ownership and scoped reuse fit (CHG-063)

2026-10-15: [R56](../docs/handoffs/codex_flat_vector_art_2026-10-07/r56_comfy_pot_ownership/README.md) binds current healed Kitchen/V2 oven without a stove-pot body under Comfy. Static first-cell retained-reject new-purpose fit removes duplicate stove/actor occlusion in ignored fixture; historical rejection remains.24 source ownership/32 refined-fit checks,12native5source views.38 first-fit contact rejects and zero-frame parse failure retained.104native34bounded70excluded;4583bounded6871retained2288excluded. No new art/role/family/sample/production/acceptance;240roles32families,85partial aliases91without0complete/global unknown. Rollback audit delta only, preserve protected originals/save identities and old rejects.

CHG-063 payload `21eb18b6f3d20633a7162f1b7ad961dfb26a7709`: all 405 direct files (265750754 bytes) anonymously verified at `2026-10-15T13:12:50.712880+00:00`; manifestSHA `9f4e69da670ac1d0b1845c3c5cb4c9b297c3f048eb7b3eccf02aa732eb22ad41`, payloadSHA `85421066a32099bb491d091d2e1a7c9f030d97b3d06bff7e198581dc9c97b051`. Two original cases24checks andtwo refined cases32checks;104native34bounded70excluded.12native5source views;first-fit visual rejects preserved,240 roles/32 families;0 accepted/global unknown. Historical R54/R51 retain original verification and acceptance limits.

## CHG-064 — catalogue and selector source crosswalk (2026-10-15)

Baseline `1e0589b3a99c0d4c0911d3e56304fa7a27a7f664`; runtime source `5120b6d59885dd057937aaf284e73681d8eac9f5`. [Impact](../design/audit_impacts/flat-vector-catalogue-selector-crosswalk-20261015.json) and [R57 evidence](../docs/handoffs/codex_flat_vector_art_2026-10-07/r57_catalogue_selector_crosswalk/README.md).176stable catalogue labels crosswalked100ambient/60game/12UI/4standalone;312AST/99game candidates14literal values;22adversarial tests; unchanged component144queries87assertions. No natural route/render/art credit.85partial91without0complete,240roles32families,global unknown/accepted0. Runtime/protected originals/save hashes unchanged; historical arrays/readers/rejects/caps retained. Findings remain open. Rollback only this non-runtime evidence/navigation change; do not restore obsolete runtime/assets or erase historical published packet.

CHG-064 payload `7707a032e7e0ea6c2a656f87ccfbaed88bc4977c`: all 396 direct files (17683454 bytes) anonymously verified at `2026-10-15T14:04:13.938628+00:00`; manifestSHA `25504cfa1b54fa29ecdf847cd879f7b8fe6016f46703e61fda89d4c747626e57`, payloadSHA `d33792aaea2085c996da7149127ee3abcd4f3dd9d5988d52a81e8f19a50d2dda`. 312script AST99candidate writes14literalvalues;22adversarial tests;144component queries87assertions;0new captures/art,240 roles/32 families;0 accepted/global unknown. Historical R54/R51 retain original verification and acceptance limits.

## CHG-065 — current Critter Book context (2026-10-15)

Baseline `5459a484f9f1a5d11c9b4c8b2f9279af87905a0a`; runtime source `5120b6d59885dd057937aaf284e73681d8eac9f5`. [Impact](../design/audit_impacts/flat-vector-critter-book-context-20261015.json), [current context](../docs/handoffs/codex_flat_vector_art_2026-10-07/r58_critter_book_context/README.md). Original Menu/Critters/tabs/Back/private reload2Mobile widths plus passive10s:59passing checks,110native71bounded39excluded; failed numeric-comparison fixture preserved. Assistant9native2source views;1px title/help, flat materials and transient caption overlap remain.240roles32families/85partial91without0complete/global unknown0accepted. No alias merging, art/runtime/protected/save changes. Rollback only this nonruntime evidence/navigation change; retain immutable historical packet and source acceptance/reject/cap history.

CHG-065 payload `022c49f55e02b2b8a2080f615b38ce008446b5b8`: all 553 direct files (117295847 bytes) anonymously verified at `2026-10-15T14:49:55.602761+00:00`; manifestSHA `f9ded1489695b0157f292e89cb574ec6ba025dbf7c9facb01ab2b17aa1e31a8e`, payloadSHA `4a6692e84441159e617883648e6a84f0e34fe11f7d1acab2c4d0cb34e59bb04d`. Two main native cases52checks plus passive7checks;110native71bounded39excluded.9native2source views;0new art/alias credit,240 roles/32 families;0 accepted/global unknown. Historical R54/R51 retain original verification and acceptance limits.

## CHG-066 — Critter Book layout/reuse candidate (2026-10-15)

Baseline `431c165647f4dcca4aec0e4ccada517534ead513`; source `5120b6d59885dd057937aaf284e73681d8eac9f5`. [Impact](../design/audit_impacts/flat-vector-critter-book-reuse-20261015.json), [candidate packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r59_critter_book_reuse/README.md). Isolated layout/painted trial at2Mobile widths104checks/340native128bounded212excluded;68book204button observations and exact source recipe. Main text/card layout repaired in fixture; original callbacks/sizes/input owner preserved with declared tab move, book layer reorder; source-script/rect binding fixes code ornaments surviving auto-renamed redraw. Existing source UI and new use unapproved; no source pixels/generated art/production changes or accepted removal.240roles32families85partial91without0complete/global unknown. Rollback only this nonruntime evidence/navigation overlay; preserve immutable historical files, source acceptance/reject/cap history.

CHG-066 payload `e23dd6a74c000780482207ab141a6da12df3f84a`: all 863 direct files (359263166 bytes) anonymously verified at `2026-10-15T16:01:56.706575+00:00`; manifestSHA `9a2285cabe70e81110d1c3a7a247682829b6fb7c01791936426ccfec13cf9311`, payloadSHA `8f4f723c5c611b4cc4459264499074ecf85ca963b68b09aa3bef583a71fa5e88`. Final4layout/painted native cases104checks;340native128bounded212excluded;68book204button observations.0new art/alias/adoption credit,240 roles/32 families;0 accepted/global unknown. Historical R54/R51 retain original verification and acceptance limits.

## CHG-067 — original Critter Book saved-state context (2026-10-15)

Baseline `2e2464a742885d0d0803870ffea9dfdd51b49889`; source `5120b6d59885dd057937aaf284e73681d8eac9f5`. [Impact](../design/audit_impacts/flat-vector-critter-saved-context-20261015.json), [packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r60_critter_saved_context/README.md). Original partial6/full18private saved profiles at2Mobile widths140checks148native140bounded8excluded;80book480card1440label observations.16pure queries/312script35call16symbol26function facts; source/reuse/provenance/phone/child/owner gaps retained. CURRENT pointer corrected fromR56 toR60 without frozen-array/schema/history changes. No measured UI/layout/art/protected/save-key changes or manufactured acquisition;240roles32families85partial91without0complete/global unknown0accepted. Rollback only this nonruntime evidence/navigation metadata overlay; preserve immutable packets/source/caps/reject history and reopen routing facts as appropriate.

CHG-067 payload `b378b6e06e256679cf19e11a7dc1abc0dd030e67`: all 678 direct files (174207444 bytes) anonymously verified at `2026-10-15T16:50:13.920002+00:00`; manifestSHA `3aa7b75d71f9193d0ba30789b4176d49c30481267552cc1d4737385133c4e0f7`, payloadSHA `dbe820c511ac069d48433758438d230f9f2bc8e0292b9270e4fdfaa23bf65b5b`. Four original partial/full saved native cases140checks;148native140bounded8excluded;80book480card1440label observations.16pure queries312scripts;0new art/alias/adoption credit,240 roles/32 families;0 accepted/global unknown. Historical R54/R51 retain original verification and acceptance limits.

## CHG-068 — caught-role and painted insect category candidate (2026-10-15)

Baseline `2db770402f9ec00c332b8def6a83aada9ccc6bd9`; source `5120b6d59885dd057937aaf284e73681d8eac9f5`. [Impact](../design/audit_impacts/flat-vector-critter-saved-reuse-20261015.json), [packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r61_critter_saved_reuse/README.md). Ignored structural source-role layout fix and current unchanged painted butterfly CATEGORY reuse, preserving original IDs/text/Button callbacks/sizes/counts and unknown status. Four final partial/full2aspects172checks, fixed control43, excluded negative36/120collisions;222native175bounded47excluded. No generation/source PNG/protected/runtime/save-key changes, no adoption/creative/device/child/owner acceptance.240roles32families85partial91without0complete/global unknown/0accepted. Rollback only this nonruntime overlay/navigation metadata; preserve immutable packets, source/caps/reject history.

CHG-068 payload `27071494a36b401e304cf5d15d3f29282639bc6e`: all 809 direct files (308992779 bytes) anonymously verified at `2026-10-15T17:41:18.939939+00:00`; manifestSHA `b8216db81d6df8a9ae0425b22816c7640097dd0ce5c9f5c5cdddf0ba4b119f84`, payloadSHA `45109c415dc3833601d85484d7360788abaa38726c95bf4de8081851cd9d1cbe`. Four final insect category candidate cases172checks,control43,excluded negative36;222native175bounded47excluded;0new art/alias/adoption credit,240 roles/32 families;0 accepted/global unknown. Historical R54/R51 retain original verification and acceptance limits.

## CHG-069 — catalogue origins and explicit Critter Book partial binding (2026-10-15)

Baseline `d0f2e17433557d5775463f44576fe7ebf03cf3df`; current source `5120b6d59885dd057937aaf284e73681d8eac9f5`. [Impact](../design/audit_impacts/flat-vector-catalogue-origin-20261015.json), [packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r62_catalogue_origin/README.md). Reconstruct176original ID origins without executing historical scripts;60game-prefixed reference labels are not a Main.game contract. Source/current original callback and existing R60saved-book4cases140checks80states bind only a book subset of game.critters;86partial90without0complete,0newnative/art/accepted removal. Wrong alias binding could over-credit coverage: exact construction/current preload/callback/navigation/source/native predicates and12targeted negative/positive tests constrain it. Full acquisition/route/native/resource/state/QA11/device/child/owner remain open. Rollback only this nonruntime overlay/navigation/current catalogue union, preserving all176IDs, frozen5/readers, immutable packets, original R60/R61candidates and caps/history.

CHG-069 payload `a3ddc9e595abe553f8401b63cf83ecd773509b45`: all 205 direct files (21508991 bytes) anonymously verified at `2026-10-15T18:19:01.301728+00:00`; manifestSHA `dc2ba6393e02b970928a09e54469442564927068dde5c7f5b98b64c2de131db5`, payloadSHA `6b6f462949b9e1ffba163b2e26352af1ed5a4813b339606f4965189d8886645c`. Original176catalogue origins/60reference labels;105source-host/108all-evidence paths and209hash refs67current142different. One existing-book partial binding86partial90without0complete;0newnative/art/adoption credit,240 roles/32 families;0 accepted/global unknown. Historical R54/R51 retain original verification and acceptance limits.

## CHG-070 — original Royal Bedroom wardrobe context (2026-10-15)

Baseline `db43af9e46f0b7f718225ffc03dd40206b8cc2de`; audited source `5120b6d59885dd057937aaf284e73681d8eac9f5`. [Impact](../design/audit_impacts/flat-vector-wardrobe-context-20261015.json), [packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r63_wardrobe_context/README.md).5passing native cases147checks;294events231bounded63excluded; cumulative5328bounded2657excluded7985native. Explicit original catalogue/current caller/native subset bindings add game.wardrobe/interior game.pearl_castle partial IDs only;88partial88without0complete, all176incomplete. Preserve failed fixture reader history54excludedframes/3failed checks. Actual Back/Done kills live14instance feedback; current title/caption/toast/material/portrait-use/action/raster weaknesses remain open. Wrong route/acceptance inference is the main evidence risk: no bootstrap-as-normal-route,14instances-as14designs or machine-as-owner credit.0newart/production/adoption/removal/global unknown. Rollback only this nonruntime overlay/routing/current union; retain frozen5/readers/immutable history/caps/protected sources/normal saves.

CHG-070 payload `0e44a79149362f342e27bc956c33d238c2452ce1`: all 459 direct files (191031710 bytes) anonymously verified at `2026-10-15T19:28:57.523095+00:00`; manifestSHA `ca839327b79e5c90cfad3799c5b057827df61de9396ef2b8ae3532d55644bc4b`, payloadSHA `33b5c44049c4fb6d649970ea95b6b94787780d84658231e55f740b50d8abb980`. Original Wardrobe5cases147checks with locked/unlocked1280/1600matrix and live Back/Done cancellation;294native231bounded63excluded;88partial88without0complete;0art/adoption/removal credit,240 roles/32 families;0 accepted/global unknown. Historical R54/R51 retain original verification and acceptance limits.

## CHG-071 — painted Wardrobe material and heading reuse candidate (2026-10-15)

Baseline `d7703fef32f32c4e2727f43eaecef5ff73d8cdce`; source `5120b6d59885dd057937aaf284e73681d8eac9f5`. [Impact](../design/audit_impacts/flat-vector-wardrobe-material-reuse-20261015.json), [packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r64_wardrobe_material_reuse/README.md). Ignored source-inheriting candidate only: unchanged Fashion panel/card source samples, original input/save/feedback/close methods;5duplicate ornament nodes detached and one source-text heading initialized beforetree.4candidate cases196checks+liveclose23/control49;402native231bounded171excluded;5559bounded2828excluded8387cumulative. Preserve failed observer/control and v1fit54frames each. Plausible negative effects are ornate corner/thumbnail/label padding, altered frame sampling/state modulation and inherited portrait/caption problems; actual candidate fit/source-use/QA11/device/child/owner acceptance remain open. No production/identity/sourcePNG/save-key changes, newart or acceptedremoval;88partial88without0complete unchanged/globalunknown. Rollback only this nonruntime candidate/evidence/routing overlay; retain frozen5/readers/immutable failures/source controls/caps/protected originals/normal saves.

CHG-071 payload `c8604d31e8d739c3b5d30559df9547fcbec73c27`: all 588 direct files (349738301 bytes) anonymously verified at `2026-10-15T20:37:26.271909+00:00`; manifestSHA `f553fa789f466afe70412bb3d34f1fd1dce448b02cfdd17d2918fc8b61d77dbd`, payloadSHA `a68ba8d7f14aed80f2913183344188e2ba59ca68ff8609b33ccbc70c6d99f3e0`. Ignored painted Wardrobe candidate219checks plus sourcecontrol49;402native231bounded171excluded;88partial88without0complete unchanged;0newart/production/adoption/removal credit,240 roles/32 families;0 accepted/global unknown. Historical R54/R51 retain original verification and acceptance limits.

## CHG-072 — Wardrobe cached frame and fit refinement (2026-10-15)

Baseline `6647c56cb0c05f0130557f022abf5d421b4cc871`; source `5120b6d59885dd057937aaf284e73681d8eac9f5`. [Impact](../design/audit_impacts/flat-vector-wardrobe-cached-fit-20261015.json), [packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r65_wardrobe_cached_fit/README.md). Ignoredrefinement uses unchanged paintedframe, originaltargets/portraits, rightinset36/5cachedstyles; source refresh semantics/helper typography/meta effects retained. Fourcandidate200checks/liveclose25/R64control50;304native239bounded65excluded;5798bounded2893excluded8691cumulative. Thincontour differs from thickneighbors, focus/disabledunexercised/inheritedmobilecostunprofiled.0production/sourcePNG/identity/savekeys/newart/partialcredit/removal. Rollback newnonruntimeoverlay/evidence/routing only; retainfrozen5/readers/parenthistory/failures/caps/protectedoriginals/normalsaves.

CHG-072 payload `0e974a72e3e455f01c0448aeac678c1bb543380a`: all 477 direct files (296401427 bytes) anonymously verified at `2026-10-15T21:36:29.051938+00:00`; manifestSHA `576eea2f4e491801614fd78f5b06ce3e50d031fe81b651f881180e3e2b9ea3e9`, payloadSHA `946c26eb616aac25d5c9ff1b12346da5a7972d9e59df33505420d257701afadb`. Ignored painted Wardrobe candidate225checks plus R64control50;304native239bounded65excluded;88partial88without0complete unchanged;0newart/production/adoption/removal credit,240 roles/32 families;0 accepted/global unknown. Historical R54/R51 retain original verification and acceptance limits.

## CHG-073 — original display entry and castle-gate mask inventory (2026-10-15)

Baseline `0ff29db519e81bb98c69669fffe79de1d68db065`; source `5120b6d59885dd057937aaf284e73681d8eac9f5`. [Impact](../design/audit_impacts/flat-vector-display-entry-20261015.json), [packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r66_display_entry_context/README.md). OriginaldisplayMain/privatepreReadySaveState/Options/Continue andactualsourceNewGame archive/reload, no authoredworldbootstrap.6cases60checks/preflight3pass;2legacycases retain24checks/2sourcepolicyfailures.126native70bounded56excluded(legacy42,preflight2,Sparkly12);5868bounded2949excluded8817cumulative. Newvisibleflatmaskrole FVR-42846B2A5A82 familySkyLagoonAffordances addsknown241/33, rootexistingholdfillpartial75/15+17supplemental;89partial87without0complete. Risks/limits: sourcelegacycomment mismatchnotfixed, viewport/cliponset/source default and currentnode metadata not fullQA11/freshOS/nativeclosure/device/child/owner.0runtime/sourcepixel/identity/savekey/newart/removal. Rollback newnonruntime evidence/canonicalrouting overlay only; preservefrozen5/readers/history/failures/protectedoriginals/normaldata; do not revert source/progress to hidefailure.

CHG-073 payload `6f836230c3badcf734d33446b628e56d0c692a89`: all 307 direct files (192706134 bytes) anonymously verified at `2026-10-15T22:34:25.171190+00:00`; manifestSHA `6b21780ff13f34ca208b1efb87f9eb334f47fa7abd981e786b8e280e27994bbe`, payloadSHA `6a7b1473b3b755f3a69b8e10cc20a42a9b052de2d74e9456414d8ed0c8f7c939`. Sixsourcecases60checks/preflight3pass;2legacycases retain24checks/2policyFAILs, notfixed.126native70bounded56excluded;241roles33families,75existingpartial15families+17supplemental/89partial87without0complete;0newart/production/acceptedremoval/globalunknown. Historicalparent receipts/times retain scope.

### CHG-074 — R67 painted castle-gate cue reuse candidate

Baseline `858436a8697b06ba1dc8cfa012d5879a218afc20`; current source `5120b6d59885dd057937aaf284e73681d8eac9f5`. [Packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r67_painted_gate_cue/README.md), [impact](../design/audit_impacts/flat-vector-painted-gate-cue-20261015.json). Existing gold star is trialed at the original invisible door anchor. Four native cases pass54 checks;20 raw frames. Production and protected sources are unchanged; acceptance/removal credit remains0. Missing-art early-return could remove the functional target and blocks adoption; new-use material/readability, return/callers, QA11/device/child/owner and global inventory remain open. R66 routing failure retained. Rollback is metadata routing to immutable R66; do not roll back runtime or overwrite another editor.

CHG-074 payload `ceda23cfb6a65d8685906b3599f97ddb28044e68`: all 174 required files (85775245 bytes) matched anonymous immutable HTTPS at `2026-10-15T23:12:50.346601+00:00`. Manifest SHA-256 `a22a905f09807bbf7b95880b0770f5938c370c2a379d282638c8519c8ab937c5`. Source/candidate4 cases54 checks20 frames;241 known roles33 families;89 partial87 without current context0 complete.0 production changes and accepted removals; new-use/missing-art/caller/device/child/owner/global gaps remain open.

### CHG-075 — R68 gate missing-art direct interaction and scope correction

Baseline `348116d6dc82c5a4f9e0a6a0b856de0ff6416349`; native source `5120b6d59885dd057937aaf284e73681d8eac9f5`. [Packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r68_gate_missing_art/README.md), [impact](../design/audit_impacts/flat-vector-gate-missing-art-20261015.json). Nonproduction constructor retains target/focus with missing artwork; source walking entry already survived and is not newly repaired. Four repaired cases88 checks;52 native32 bounded20 excluded. Two premature8s baseline entry assertions are retracted and retained with exact versions; two corrected baselines confirm source walking entry while direct interaction remains absent. Source/normal save guards unchanged;0 accepted removals or production changes. Missing artwork/style/QA11/device/child/owner and comprehensive inventory remain open. Rollback is metadata routing to immutable R67, preserving R68 correction/history; no runtime rollback or other editor changes.

CHG-075 payload `05ad9e5fb60f16d1cffd95f8a164d634632fb2ae`: all 273 required files (139366371 bytes) matched anonymous immutable HTTPS at `2026-10-16T00:00:12.676910+00:00`. Manifest SHA-256 `26cd510f59f155187d06050582aca66d1d4c5b0334ac0333058859340414676c`. Repaired4 cases88 checks52 native32 bounded20 excluded;source walking access already survived;premature8s assertion retracted;241 known roles33 families;89 partial87 without current context0 complete.0 production changes and accepted removals; new-use/missing-art/caller/device/child/owner/global gaps remain open.

### CHG-076 — R69 Fairy route context and unrepaired source failures

- Scope: [R69](../docs/handoffs/codex_flat_vector_art_2026-10-07/r69_fairy_route_context/README.md), [impact](../design/audit_impacts/flat-vector-fairy-route-20261015.json), baseline `fe7ad2cb55205dd21035cc59beca0d2d918b3920`, runtime source `5120b6d59885dd057937aaf284e73681d8eac9f5`.4 source observer cases55 checks62PNG40 bounded22 excluded. Source purple occlusion and Back return contracts FAIL.2 new named roles/1 family/3 partial aliases;243 roles34 families;92 partial84 without0complete.0 accepted removals.
- Verification: exact Godot4.7.2 Mobile/Speedy, original controls, private fresh-Main saved-load,4420 source/4041 sidecar/11 normal hashes. Document/evidence/parser/inference/2D and exact anonymous remote delivery recorded separately. Machine results grant no visual/device/child/owner acceptance.
- Rollback: retire only new nonruntime R69 evidence/routing changes with history-preserving follow-up; do not alter frozen registries, protected sources, production runtime, normal saves or owner decisions. No defect lifecycle changed.

CHG-076 payload `5166c0e92dbe6c1804fafe19201cc857f7a5db26`: all 263 required files (134729845 bytes) matched anonymous immutable HTTPS at `2026-10-16T01:11:42.777124+00:00`. Manifest SHA-256 `716d298e34865193c1fe546167dcca366d11a5ae79e26a4aa585c05b58bae294`. Four observer cases55 checks62 native40 bounded22 excluded;source art and Back contracts FAIL;243 roles34 families;92 partial84 without0 complete.0 production changes and accepted removals;caller/device/child/owner/global gaps remain open.

### CHG-077 — R70 existing-art Skyway reuse candidate

- Scope: [R70](../docs/handoffs/codex_flat_vector_art_2026-10-07/r70_skyway_art_reuse/README.md), [impact](../design/audit_impacts/flat-vector-skyway-art-reuse-20261015.json); topicbaseline `dccb444efd0277bbcea62af1384a78b535d5b569`, source `5120b6d59885dd057937aaf284e73681d8eac9f5`.2 final cases52 checks89 raw36 bounded53 excluded. Source controller/state/control/world/foreground signature equality retained; source art and gardenBack remain failed. No generation/runtime/accepted-removal credit.
- Verification: original inputs/private dependency beforeReady, natural hall camera convergence/directBack/re-entry/House caller; exact4.7.2 Mobile/Speedy and4420/4041/11 guards. Native pixels/coverage and document/2D/remote gates retained separately. Widecrop/nativequality/hand/contact/fallback/voice/caller/QA11/device/child/owner/global inventory remain open.
- Rollback: retire only nonruntime R70 candidate/evidence/routing through a history-preserving follow-up. Do not edit frozen registries, runtime/protected sources or normal saves. No master finding lifecycle changes.

CHG-077 payload `12b4823566d55799a798c999334c5a47b04e2686`: all 289 required files (198912343 bytes) matched anonymous immutable HTTPS at `2026-10-16T02:02:24.074552+00:00`. Manifest SHA-256 `18f46f04548d268d77225fdf253dc896cc98ff79aea5e951e8330d5fe4be2166`. Two final reuse cases52checks89native36bounded53excluded;4 exact source/control/foreground signatures;source art/Back FAIL.243roles34families92partial84without0complete;0 production changes/acceptedremovals. Crop/nativequality/hand/fallback/caller/device/child/owner/global gaps open.

### CHG-078 — R71 Skyway pointer registration and blocked art export

- Scope: [R71](../docs/handoffs/codex_flat_vector_art_2026-10-07/r71_skyway_pointer/README.md), [impact](../design/audit_impacts/flat-vector-skyway-pointer-20261015.json); baseline `872b45515e27df6b833ea4b697755186563ed904`, source `5120b6d59885dd057937aaf284e73681d8eac9f5`. Source misses reproduced; local offset-only preview fixes measured tip reach while flat art remains. Centre trial failed hero visibility, not silently accepted. Art export automatically rejected before call; public review request needs destination-specific owner authorization.
- Verification and risks: 163raw/86bounded/77excluded; exact engine/source/private profile guards and source input/bob measurement. Unexplained aborted exit, source gardenBack/HUD, crop/nativequality/hand/fallback/caller/QA11/device/child/owner/global inventory remain open. No production, paid generation, accepted removal or lifecycle change.
- Rollback class: history-preserving retirement of nonruntime R71 evidence/candidate/routing only from a clean dedicated rollback branch. Do not edit frozen registries, source/protected pixels, normal saves or prior records. A mixed evidence/policy diff is reviewed before any reversal; no automatic one-line revert.

CHG-078 reuse correction before publication: approved combined gesture atlas includes an existing painted pointing pose. New-art request is deferred until a source-bound reuse trial; no immediate owner approval needed for that safe path. The rejected external export remains denied and no generation call ran. [Follow-up](../docs/handoffs/codex_flat_vector_art_2026-10-07/r71_skyway_pointer/REUSE_FOLLOWUP.json).

CHG-078 payload `69688371157886eb544c23fb331f1669c9cb84aa`: all 387 required files (306520733 bytes) matched anonymous immutable HTTPS at `2026-10-16T03:31:16.288029+00:00`. Manifest SHA-256 `b7e6543946208e8be49a80fb6f524ec0fa5109fc355c1f61bc56e96b1e88a35c`. Four final cue cases; existing source hand misses all three waypoint tips. Offset-only preview remains inside measured targets; art export blocked, no new art or removal.243 roles34families92partial84without0complete; all acceptance gaps open.

### CHG-079 — R72 painted pointing-hand reuse audit

- Scope: [R72](../docs/handoffs/codex_flat_vector_art_2026-10-07/r72_skyway_hand_reuse/README.md), [impact](../design/audit_impacts/flat-vector-skyway-hand-reuse-20261015.json); baseline `63b842887eb14d6b51bedb0b676afbe17b6453a7`, source `5120b6d59885dd057937aaf284e73681d8eac9f5`. Two literal approved source crops fail new-use quality; native source/provenance, real inputs and exact rejected captures retained. No pixel editing/generation/export or production change.
- Evidence/risks:7native cases/322checks,28bobcycles,142raw40bounded102excluded. Original state/controls/world/otherforeground preserved; source gardenBack/HUD fails. Prebinding observer metadata corrected without rewriting prior raw facts. Caller census finite, and all prior fallback/QA11/device/child/owner/strict2D/global inventory gaps remain open. New-art export request awaits destination-specific owner authorization.
- Delivery: exact payload then one final receipt commit, anonymous all-file checks and actual staged/committed no-regression gates for each push. Final receipt own bytes/head verified after push, without recursive self-hash commits; no gate waived.
- Rollback class: history-preserving retirement of nonruntime R72 candidate/evidence/current routing from a clean dedicated rollback branch. Review actual mixed diff before any revert; preserve frozen registries, source/protected originals, normal saves and earlier records. No lifecycle/authority change or automatic one-line reversal.

CHG-079 decode follow-up: same28px crop from original PNG improves color/contour over lossyVRAM import, yet retains a cut wrist/limited standalone detail and is rejected. SourcePNG export warning separately blocks integration-ready proof. Exact tracked-versus-initialized import content differs only LF/CRLF; PNG/sidecar bytes unchanged throughout.7runtime cases/322checks/28cycles plus2source-only inspections,142raw40bounded102excluded;6122bounded3223excluded9345retained. No generation or production changes.

CHG-079 published payload `1b771fafcc68506eed8212a1cc9b5981bc25b0a2`: 355 required files/243198540 bytes anonymously verified at 2026-10-16T05:07:48.051991+00:00; manifest SHA-256 `1e5a53b480e68b6e4204429c202a310bf01184dabb59752d603c32035d22dc67`. The separate final receipt binds the exact two-image request without sending it to ImageGen. Its own bytes/head are verified after push; source gardenBack/HUD/global inventory and required acceptance remain open.

### CHG-080 — R73 current shared-hand source consumers

- Scope: [R73](../docs/handoffs/codex_flat_vector_art_2026-10-07/r73_hand_consumer_audit/README.md), [impact](../design/audit_impacts/flat-vector-hand-consumers-20261015.json). Baseline `e4ff0ae20c0edfc567221396d4613b1fc4b1d067`, source `5120b6d59885dd057937aaf284e73681d8eac9f5`. Preserve16R17 candidate file paths;2additional references are probe requirements. Bind current loading/field/source-entry candidate functions and4reviewed retirement dependencies without new pixel/role/acceptance credit.
- Benefit/risk: prevents treating bitmap deletion, a test filename or one Skyway fit as global removal. Source/static candidate graphs are incomplete for dynamic/native/state dataflow and cannot establish execution or visible art quality. Conditional primitive fallbacks, saved tree-book and safe-menu behavior must close separately. No runtime, art, import, save, policy or frozen-root changes.
- Evidence:318text inputs/312ASTs,127function bindings,12directly reviewed source functions. Existing6122bounded/3223excluded/9345retained and243roles/34families remain unchanged; whole-game denominator/allcaller/QA11/device/child/owner/strict2D open. R72ImageGen request remains unapproved,0calls.
- Delivery/rollback: same durable GitHub topic, exact payload and final receipt with anonymous all-file checks and actual staged/committed2D gates perpush. Rollback is a reviewed history-preserving retirement of this nonruntime audit/routing from a clean dedicated rollback branch; preserve prior namespaces, frozen registries/protected originals and save/acceptance histories. No automatic one-line revert or finding closure.

CHG-080 final reproduction correction: initial payload scanner emitted raw rows before source-ID enrichment. The current reproducer includes that deterministic enrichment and a scratch output directory; a fresh run reproduces all four authoritative source-analysis JSON files exactly. Payload evidence/source bytes and all art/context/removal totals remain unchanged. The final receipt separately verifies corrected audit tooling and its reproduction report.

CHG-080 published payload `5a46e06c26be03099967e665d7407b507f9cf010`: 398 required files/19262880 bytes anonymously verified at 2026-10-16T05:40:16.530760+00:00; manifest SHA-256 `39a41206d8906457d00fd8551b155caca8e0bc2175b6f8fdfced41871b093596`. The final receipt binds the current source audit without sending any inputs to ImageGen. Its own bytes/head are verified after push; source gardenBack/HUD/global inventory and required acceptance remain open.

CHG-081 R74 embedded tree-book current context at source `5120b6d59885dd057937aaf284e73681d8eac9f5`: original stage-star/practice-book input, all6source stages/help/partialhold/cancel/Back/reopen/newMain reload/completion/Replay.2healthy aspects96checks; source tip misses8states and caption occlusion remain unrepaired.123raw=78bounded+45excluded; failed fixture JSON int/float assertion preserved/excluded.11new named partial roles/1family =>254/35; cumulative6200bounded3268excluded9468retained. Catalogue92/84/0 unchanged, global totals unknown,0accepted removal. No production/code/art/save change, no new generation/export, no finding closure. Rollback: revert this documentation/evidence change only; frozen R6 registries/prior namespaces unchanged. Exact payload/final delivery evidence follows.

CHG-081 published payload `23ace33abc1d74b938dbaead53a0b4e421c22e1a`: 237 required files/113177561 bytes anonymously verified at 2026-10-16T06:35:37.174832+00:00; manifest SHA-256 `0c100cf1dba21d22b1ce6728edf404c9ca9a6a9003ca0e56aa462fb5f0f9c561`. Final receipt binds pinned-source tree-book context, all excluded failures and unchanged acceptance limits. Integration doorframe delta is separately disclosed; no new-head native or accepted-removal claim. Final receipt own bytes/head checked after push.

CHG-082 R75 source-bound book hand registration at `dd799b2d43871b29d1d6e0503646308a194dad1e`:2fresh controls preserve8tipmisses;2first-preview cases input-pass but treatmentbadge placement rejected;2final-preview cases8actualtipadvances/primaryleaf projection,114checks.6cases324checks/230raw=78sourcebounded+152excluded; cumulative6278/3420/9698.0newroles/families,254/35known,92/84/0catalogue unchanged,0acceptedremoval/globalunknown. Source callbacks/targets/state/clocks/synthetic private persistence retained; only declared nonproduction handvisual substitute. Initial import rawguard failed on1102EOL-only changes; losslessbackup/exact restoration preservesold4041sidecars,47newgeneratedsidecars recorded,4425runtime/4088sidecars guarded. No runtime source/art changes, generation/export, finding or finalQA11/device/child/owner closure. Rollback: revert new documentation/evidence/routing only, prior namespaces/frozen root bytes preserved.

CHG-082 published payload `063b7b6131df443fbed3972873b0f7a3478e9146`: 389 required files/204697650bytes anonymously verified at 2026-10-16T07:51:26.003231+00:00; manifest SHA-256 `94ce51a816c033b49f7d934bb8172f4bd6bfa063d30f08d38ad8ea2ee0205e90`. All230rawframes, rejected first semantic placement, exact import EOL recovery and source guards retained. Final receipt owns a separate byte/head check; painted hand, global denominator/caller/QA11/device/child/owner acceptance remain open.

## Stuffie care current context (CHG-083)

2026-10-16 R76: [care pictogram/status audit](../docs/handoffs/codex_flat_vector_art_2026-10-07/r76_stuffie_care_context/README.md), [impact](../design/audit_impacts/flat-vector-stuffie-care-context-20261016.json). Source dd799b2d, original Main/private-beforeReady save and declared promenade startup seam, then original Menu/Stuffie/Back/care inputs;86healthy checks at1280/1600. Seven new semantic care roles in existing shared_ui family,261known/35families;32new bounded+56excluded=88retained;6310bounded/9786total. Glossy glyph material, nested need-label acknowledgement lookup and1280title-heart occlusion remain open. Zero runtime/art/acceptance changes;0accepted/globalunknown,92partial84without0complete catalogue aliases. Preserve failed10/26frame observers, frozen root5 and prior histories. Rollback routing may return to R75 only as historical evidence; no retired runtime fallback or approved artwork is supplied.

CHG-083 payload `c641283bba1c1bb2dfe56faa2341f474f45543bd`: 193required files/88760995bytes anonymously verified at 2026-10-16T08:41:35.351584+00:00; manifest SHA-256 `892c3f398101c4e35bada5b8e5b10e907979e965d8a6e25aadaf521cce188fdc`. All88native images,36failed-observer diagnostics,86healthy checks and source/import/save guards retained. No production/art/acceptance change; final receipt owns a separate byte/head check.

## Intro entry ownership and Keep Game hand (CHG-084)

2026-10-16 R77: [current entry/hand audit](../docs/handoffs/codex_flat_vector_art_2026-10-07/r77_intro_entry_ownership/README.md), [impact](../design/audit_impacts/flat-vector-intro-entry-20261016.json).313current scripts parse; named legacy intro startup is headless-guarded, while actual display StartMenu shares intro_active/ambient label without an IntroOverlay. Original private-userdir NewGame/reload/opening/Continue and source hand-tip cancel pass50checks/64bob samples at2aspects. New semantic hand FVR-67E362D1DE53;262known/35families,0accepted/globalunknown,92partial84without0complete. Retain18cache-error frames and0frame prelaunch containment stop;32bounded+22excluded=54raw,6342bounded/9840total. Source4425/import4088/normal11hashes unchanged. R66legacyContinue mismatch and existing gate-mask role remain open; no forced legacy display, global unreachability, production/art/QA11/device/child/owner or cinematic acceptance. Rollback is routing/evidence comparison to R76 only; no production/runtime change to undo.

CHG-084 payload `d2eaff753986d8dcf25fc4f15a7ef5fff50f5929`: 470required files/90878887bytes anonymously verified at 2026-10-16T09:52:06.423322+00:00; manifest SHA-256 `3e16ae058417f024743ca3e81213a55894790dd3d0060b955fc23b5f395d4b8f`. All54native images,18cache-error diagnostics/0frame prelaunch stop,50healthy checks and313-script source guard and source/import/save guards retained. No production/art/acceptance change; final receipt owns a separate byte/head check.

## Named game payload boundaries (CHG-085)

2026-10-16, baseline `d3d5124c2373d17bb835ae85f63044b6fd2dfbdc`, current runtime source `dd799b2d43871b29d1d6e0503646308a194dad1e`. [R78 packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r78_game_payload_closure/README.md) and [impact](../design/audit_impacts/flat-vector-game-payload-20261016.json) record changed paths and publication receipts.

Benefit:4named producer bindings and3guarded slide callers narrow opaque `fr["game"]` input provenance. Separate p_slide race redirect, synchronous fade callback and Fairy defer; retain mutable alias limitations.313current scripts,15adversarial extraction tests/13official4.7.2no-Main checks; no screenshots or production/art edits.262/35,92partial84without0complete,0accepted removals and unknown totals preserved. Dynamic/native/caller, scene/style, QA11/device/child/owner remain open.

Possible negative effects/dependencies: source initializers can be mistaken for immutable runtime tags or exhaustive normal routes. Explicit open edges/validators prohibit that credit. Prior approvals/rejections/protected originals unchanged. No integration/release authority. Payload/final commits follow publication and anonymous exact verification.

Rollback class: audit/document metadata only. Use a clean dedicated `codex/rollback-chg-085` branch and inspect the bounded packet/routing/impact diff. Never revert runtime, frozen root5 or prior packets here. Re-run document/development/2D regression and anonymous delivery checks for any published rollback.

CHG-085 payload `f163d46b146ec94deb5fd3bf478a59713831eb45`: 383required files/18569260bytes anonymously verified at 2026-10-16T10:24:02.101779+00:00; manifest SHA-256 `0046ff01df9ceac739d32e476129087f3c03397cac786a790b9c40f4212cc632`.313script exact-source graph,4named producers/3slide callers,15extraction tests/13no-Main language checks and4425rawsource/11save guards. No art/production/native-frame/acceptance increment. Final metadata owns separate byte/head verification.

## Current promenade ownership and focus cue (CHG-086)

2026-10-16, topic baseline `ce4a454f65fc5b61f915ce41176af866fdf633ab`, runtime source `dd799b2d43871b29d1d6e0503646308a194dad1e`. [R79 packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r79_promenade_slide_ownership/README.md) and [impact](../design/audit_impacts/flat-vector-promenade-slide-20261016.json) list exact changed files and publication evidence.

Benefit: current world/touch ownership and actual private original-input slide/swing/seesaw states distinguish live Canvas play from retained portrait/race routes. 313-script named audit, four native cases / 100 checks, 78 frames (70 bounded / eight bootstrap excluded); one shared procedural ring/pointer role adds no family. 263 roles / 35 families; 6,412 bounded / 9,918 retained history; zero accepted removals. Ten-axis same-scene review keeps flat cue material and action/contact/motion gaps explicit. No production/art/source/normal child-data changes or new generation.

Dependencies/possible negative effects: confusing a shared cue with three new pieces, current animation with a legacy game alias, source selection with global unreachability, or machine/native observation with acceptance. Validators retain the exact units and unknown denominator; prior packets/rejections/protected sources remain unchanged. Full dynamic/native/caller, motion, QA11/device/child/owner and zero-art evidence remain blocking. Payload/final receipt commits follow publication and exact anonymous verification.

Rollback class: audit/context documents only. Start a clean `codex/rollback-chg-086` branch and inspect the bounded packet/routing/impact diff; never revert production, frozen root5 or prior evidence for this change. Re-run source/evidence/document and actual staged/committed 2D regression plus delivery gates for a published rollback.

CHG-086 payload `9d25c779ee3ea5b0780f7dea9661121a28554a5b`: 534required files/214998233bytes anonymously verified at 2026-10-16T11:08:09.682600+00:00; manifest SHA-256 `a7cc79f11d09d00f6739a44e0ff654a84d71ad808fe708471ef947c6a044b89a`.313script owner graph/8wall-array refs,10source tests,4native cases/100checks,78frames70bounded8bootstrapexcluded; one shared cue role/3consumers;263roles35families.4425rawsource/4088sidecars/11save guards unchanged. No generation/production change or accepted replacement. Final metadata corrects the generic hit-radius caption to118/110/110px; source glow-center geometry is not a direct gesture test. Native inputs/counts unchanged. Final metadata owns separate byte/head verification.

## CHG-087 — playground cue input and approved-source reuse audit (2026-10-16)

Owner mission continuation, source `dd799b2d43871b29d1d6e0503646308a194dad1e`, topic baseline `fab29b2b25db8bfc732cda623190f32c5edd9d41`. R80 confirms actual glow-center/tip input for the three playground toys and records a separate whole-source painted-star prototype. Two official 4.7.2 Mobile/Speedy cases / 84 checks / 61 frames: 39 original-source context and 22 excluded candidate/bootstrap views. Known 263 roles / 35 families unchanged; one shared-role reuse sample pending new-use semantics/occlusion review, zero production changes or accepted removals. All 4,425 runtime files, 4,088 sidecars and 11 normal save-name hashes unchanged. Whole-game denominator, full motion/contact/caller/QA11/device/child/owner acceptance remain open. Frozen root5, protected sources and R72 rejection preserved. Rollback: revert only the R80 evidence/routing commits; retain immutable published history, no production rollback required. [Packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r80_playground_cue_reuse/README.md); [impact](../design/audit_impacts/flat-vector-playground-cue-reuse-20261016.json). Publication receipt follows exact remote verification.

CHG-087 payload `ab78b3c3ca7547b8c5514838bc1f87e1f115f295`: all 521 required files / 186153327 bytes anonymously verified at 2026-10-16T12:08:21.608493+00:00; manifest SHA-256 `a0cf6d269bdd0f27bc57623ae87a31a2fd689ba3aabd13235ce59029befa0597`. Two native cases / 84 checks / 61 raw frames; 39 bounded source + 22 excluded. Twelve source and six candidate input trials, one shared-role approved-source reuse sample awaiting new-use/occlusion review. Known 263 roles / 35 families unchanged; zero production integration or accepted removal. Exact-source, protected and save guards unchanged; full acceptance and global inventory remain open. Final metadata owns separate byte/head verification.

## CHG-088 — source-owned TouchUI flash audit (2026-10-16)

Source `dd799b2d43871b29d1d6e0503646308a194dad1e`; topic baseline `89bca453942eb91a2fd23a486373aafde2f33658`. Original source flash creation/material/alpha/freed-state binds R80 observation FVS-38151AC2830B to existing FV-7976FC8C2881 subpart.313 AST scripts /16 named calls /10 local flash calls; two exact4.7.2Mobile/Speedy native cases /52 checks /23 frames /four selected lifecycles.19 bounded contexts +four excluded bootstrap views. Known263/35 unchanged;76 existing partial roles /15 families plus39 supplemental partial. Whole-game totals and acceptance open; no production, new art, generation or accepted removals. Rollback: revert only R81 evidence/routing commits, retaining immutable history; no production rollback. [Packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r81_touch_flash_ownership/README.md); [impact](../design/audit_impacts/flat-vector-touch-flash-ownership-20261016.json). Publication receipt follows exact verification.

CHG-088 payload `85727a455f82e0d54450b6938f8af395732c4899`: 487 required files / 111504472 bytes anonymously verified at 2026-10-16T12:38:52.787004+00:00; manifest SHA-256 `8a493250670451639d006602a0b468a106c148c6cf384fe4413a4e21b5feb0d9`.313 AST scripts /16 named calls /10 local flash calls;52 native checks /23 frames /four selected source flash lifecycles. Existing partial roles76/15families plus39supplemental; known263/35 unchanged. No production/source edits, new art or accepted removals. Whole-game and full parent/caller/QA11/device/child/owner remain open. Final metadata verified separately.

## CHG-089 — local painted-ring touch-feedback reuse (2026-10-16)

Source `dd799b2d43871b29d1d6e0503646308a194dad1e`; baseline `2acd2c969faeb3fb61d3ff5bcf1540aadba6735b`. Existing accepted ground-telegraph ring reused as one declared nonruntime touch-feedback sample after11source fit inspections.4original4candidate lifecycles/two exact4.7.2Mobile/Speedy cases/84checks/39frames:19original context,16candidate+4bootstrap excluded. Original Panel/input/fade/free and whole source bitmap retained; peak opacity/new-use/alarm semantics remain open.263roles35families/76existingpartial unchanged; zero production integration/generation/accepted removals.39audit framebuffer license rows appended; protected originals/runtime assets unchanged. Full caller/inventory/QA11/device/child/owner open. Rollback: revert only R82 evidence/license/routing commits; preserve immutable history, no production rollback. [Packet](../docs/handoffs/codex_flat_vector_art_2026-10-07/r82_touch_flash_reuse/README.md); [impact](../design/audit_impacts/flat-vector-touch-flash-reuse-20261016.json). Publication receipt follows exact remote verification.

CHG-089 payload `f90b69eec617018691a8c62ffb1c22a2f6acf799`: 514 required files / 150703839 bytes anonymously verified at 2026-10-16T13:20:49.255019+00:00; manifest SHA-256 `80e7849c0a066a957c4984989b2bb3f397267a8c22d8eec51afd6cb725aa7936`.Four source and four separate candidate lifecycles /84checks /39frames; one whole painted-ring reuse sample pending new-use review. Existing partial roles76/15families plus39supplemental; known263/35 unchanged. No production/source edits, new art or accepted removals. Whole-game and full parent/caller/QA11/device/child/owner remain open. Final metadata verified separately.

## Painted touch-feedback trial reconciliation (CHG-090)

R83 [canonical tally](../docs/handoffs/codex_flat_vector_art_2026-10-07/r83_touch_flash_runtime/README.md) references exact runtime trial 06dbe47f52837a08cf39bbb2e604a372fcab46cc / [PR34](https://github.com/Ebonyks/mermaid-roshan-reef/pull/34).82/82clean local exits and60nativechecks are separate from new-use/QA11/device/child/owner acceptance. No runtime changes on this audit branch; no accepted-removal/devintegration/family/role/alias credit. All23newframes excluded from current-dev coverage. Prior failures, rawEOL/transport handling, shutdown warnings and unknown global totals preserved. [Impact](../design/audit_impacts/flat-vector-runtime-tally-20261016.json). Roll back only this evidence routing if incorrect; never restore frozen historical representations or unrelated runtime/save/art sources.

## Global Menu and Back source context (CHG-091)

[R84 context](../docs/handoffs/codex_flat_vector_art_2026-10-07/r84_navigation_context/README.md) binds exact source dd799b2d to original touch pause/resume, the same 112px layer-29 button, two native widths and 38 passing checks. Fourteen raw frames comprise ten bounded source views and four excluded bootstrap views. Only normal material is visibly observed; other styles/routes and exact packaged glyph/device/child/owner acceptance remain open. Existing FV-2ABD73BAFFE0 gets no new role/family/alias/sample credit; unknown denominators and zero accepted removals persist. No runtime or source-art changes. [Impact](../design/audit_impacts/flat-vector-navigation-context-20261017.json). Rollback only this evidence routing if inaccurate; preserve immutable historical records, frozen root files, original art and saves.

## Runtime trial remote CI blocker record (CHG-092)

[R84-CI01](../docs/handoffs/codex_flat_vector_art_2026-10-07/r84_navigation_context/ci_status_20261017/CI_STATUS.json) records exact trial head 06dbe47f: both remote probe jobs cancelled near the configured 55-minute limit; PR logs retain Opera advisory CAPPED and Sky Lagoon gl_compatibility rejection. No newer run was present at observation time. Local machine/source-context results are separate; no integration, acceptance, new art/count credit or inferred regression total. No blind rerun, workflow/gate change or fallback acceptance. [Impact](../design/audit_impacts/flat-vector-navigation-context-20261017.json). Roll back only inaccurate status/routing; preserve original logs, source captures and historical local results.

## Painted global navigation material sample (CHG-093)

[R85](../docs/handoffs/codex_flat_vector_art_2026-10-07/r85_navigation_reuse/README.md) follows anonymously verified R84 context with the existing painted wardrobe card on only the actual112px Menu/Back control. Final cases pass92engine checks/pixel guards; earlier metadata-only render false positives, diagnostic toggle correction and invalid cross-mode pixel assertion stay retained. All96new raw frames excluded from current-dev coverage; one new material-use sample for existing FV-2ABD73BAFFE0, no new role/family/alias or approval/integration/removal credit. Source/glyph/font/save bytes unchanged; no new generation. [Impact](../design/audit_impacts/flat-vector-navigation-reuse-20261017.json). Runtime implementation must apply in the actual constructor/mode-sync path before draw; formalQA11/device/child/owner, other callers and unknown totals remain open. Roll back only inaccurate evidence/routing; preserve raw attempts, sources, frozen root records and all protected originals.

## Painted global navigation runtime reconciliation (CHG-094)

[R86 canonical tally](../docs/handoffs/codex_flat_vector_art_2026-10-07/r86_navigation_runtime/README.md) binds separately published runtime 684e34f06ebce6a70065847b5ecb69547ea8a128 /[PR35](https://github.com/Ebonyks/mermaid-roshan-reef/pull/35).82/82local/64native checks and full anonymous payload/final-metadata verification are separate from exact-head remoteCI, integration and all creative/QA11/device/child/owner acceptance.30new frame events are excluded from current-dev coverage;26source route labels are not screens. Stable IDs, root snapshots/history, unknown global totals and0accepted/devintegrated persist. [Impact](../design/audit_impacts/flat-vector-navigation-runtime-tally-20261017.json). Roll back only inaccurate evidence/routing; preserve immutable history, root representations/readers and every source/protected asset. No runtime rollback, integration or release is authorized by this evidence change.

## Critter Book source caller and persistent text bounds (CHG-095)

[R87 audit](../docs/handoffs/codex_flat_vector_art_2026-10-07/r87_critter_navigation_context/README.md) binds actual published-source Menu/Critters/fish/insect/Back/reentry at1280/1600 Mobile/Speedy:74native/18material checks,22excludedframes,1px title/help widths and help bottom743 on720viewport. Eight raw frames received partial ten-axis agent review. No artwork/runtime repair or acceptance credit. ExactPR35push workflow green; optional Sky renderer fails and formalQA11/device/child/owner remain separate. [Impact](../design/audit_impacts/flat-vector-critter-navigation-context-20261017.json). Roll back only inaccurate R87evidence/routing, preserving raw captures, parent history, stable IDs, root five representations/readers and all runtime/protected assets. Unknown whole-game scope and0accepted/devintegrated persist.

## Canonical painted Critter Book candidate reconciliation (CHG-096)

[R88](../docs/handoffs/codex_flat_vector_art_2026-10-07/r88_critter_book_runtime/README.md) records the separately published source-bound book frame/layout implementation and verbatim R86navigation dependency.606native/82local machine checks,349excluded raw frames; frozen roots and all historical acceptance boundaries retained. No runtime code or source artwork changed on this audit branch. [Impact](../design/audit_impacts/flat-vector-critter-book-runtime-tally-20261017.json). Roll back only this namespace/routing metadata if required, preserving immutable runtime/history evidence. Unknown whole-game scope, critical glyphs, shared consumers and formalQA11/device/child/owner remain open.

CHG-096 canonical payload publication: `d7f12689400673795555cfc121f7b78495d2f2c2`, manifest SHA-256 `93f7b08e9afaa8482ff28c8c4ef7544fa540fe0bfcd483f013e65c3ac5f927f5`; 2325 required files / 1006675416 bytes anonymously verified at 2026-10-17T13:25:56.184373+00:00. Final own receipt metadata separately checked; acceptance and integration remain distinct.

## Critter Book glyph source and consumer context (CHG-097)

[R89](../docs/handoffs/codex_flat_vector_art_2026-10-07/r89_critter_glyph_context/README.md) binds existing category/habitat consumers and later source bytes before a bounded insect-tab replacement. Historical source approvals, R40 whole-unit rejects, all raw frame/history totals and zero acceptance/dev-integration remain preserved. No runtime or source image changes. [Impact](../design/audit_impacts/flat-vector-critter-glyph-context-20261017.json). Rollback may remove only this namespace/routing delta while preserving immutable prior evidence.

CHG-097 canonical payload publication: `9791fc08dcf8129bed220f5a105b910c76b4da2c`, manifest SHA-256 `0ccc88ff0cf02276a0e29542d9e2dec9174b86b65d09b2bceb2e3f588fe07170`; 2388 required files / 1023023629 bytes anonymously verified at 2026-10-17T14:04:59.714491+00:00. Final own receipt metadata separately checked; acceptance and integration remain distinct.

## Exact green book/navigation Dev integration evidence (CHG-098)

[R90](../docs/handoffs/codex_flat_vector_art_2026-10-07/r90_dev_integration/README.md) records exact sourceF normal Dev integration, terminal required CI, retained advisory failures, pre-push source/gates and anonymous public ref/four-source proof. Two partial code artifacts differ from zero complete artwork-role/family/removal acceptance. [Impact](../design/audit_impacts/flat-vector-book-dev-integration-20261017.json). No runtime code changed on this canonical branch. Rollback only this metadata/routing delta if needed; any runtime correction uses the normal separate green Dev workflow and preserves source art, saves and history.

CHG-098 canonical payload publication: `22069487bf303d4682df389c9dc786b9bbed8955`, manifest SHA-256 `f7e0835957c75ff1d96cefa8a50dae8db02180cfdefcaf43b467f37d3501c1a0`; 2444 required files / 1035060761 bytes anonymously verified at 2026-10-17T15:18:05.405369+00:00. Final own receipt metadata separately checked; acceptance and integration remain distinct.


## Dev CI timeout reconciliation (CHG-100)

[R92](../docs/handoffs/codex_flat_vector_art_2026-10-07/r92_dev_ci_timeout/README.md) records exactDevF timeout, one failed-job retry and absent exactFAPK verification. Prior green sourcebranch runs, partial code integrations and historical totals retain scope. [Impact](../design/audit_impacts/flat-vector-dev-ci-timeout-20261017.json). No runtime/workflow changes. Rollback current routing only; retain immutable timeout history and zero acceptance.

CHG-100 canonical payload publication: `deffd85ef593e9690aaba0da64f4338aa7577eb6`, manifest SHA-256 `ae2eeb053e29029b5a9e720f30ff2aa71a5a7b1cc82403c6042c8602ec1d6fec`; 2485 required files / 1044525007 bytes anonymously verified at 2026-10-17T15:45:53.246265+00:00. Final own receipt metadata separately checked; acceptance and integration remain distinct.


## Restore item-by-item Phase2 production (CHG-101)

[Workflow](../docs/handoffs/codex_flat_vector_art_2026-10-07/PRODUCTION_WORKFLOW.md), [queue](../docs/handoffs/codex_flat_vector_art_2026-10-07/PRODUCTION_QUEUE.json), [impact](../design/audit_impacts/flat-vector-phase2-workflow-20261017.json). Correct the audit-heavy loop using existing October13 authority and October17 owner steering. Verify the same automation is replacement-first, preserve the specific ImageGen block and in-flight CI. No runtime/art/count change. Rollback operational routing only after reconciling owner direction; preserve immutable history.

CHG-101 delivery: `41b5d9b67e37922aac97f6989418fe5d95da1bc3`, 34 direct required files / 8557156 bytes anonymously exact at 2026-10-17T16:13:26.633968+00:00. No recursive archive, generation or acceptance credit.

## First painted Skyway hand candidate (CHG-102)

[R93](../docs/handoffs/codex_flat_vector_art_2026-10-07/r93_painted_hand_candidate/README.md), [impact](../design/audit_impacts/flat-vector-painted-hand-candidate-20261017.json). Owner authorized exactly two public inputs after the prior automatic rejection; one actual ImageGen take now preserved. Existing stable role only; no runtime, protected-source, acceptance or removal changes. Rollback restores routing and retains the unmodified candidate/provenance in history; do not rewrite the historical rejection.

CHG-102 delivery: `88ff2a795a5796a44b1b2857874808534fcf0391`, 38 direct required files / 12409883 bytes anonymously exact at 2026-10-17T17:26:16.672269+00:00. One actual generated candidate; no runtime/acceptance/removal credit.

## Native painted-hand fit and insect-tab Dev integration (CHG-103)

[R94](../docs/handoffs/codex_flat_vector_art_2026-10-07/r94_painted_hand_native/README.md), [impact](../design/audit_impacts/flat-vector-painted-hand-native-20261017.json). Advance the existing one-take hand through actual-controller preview, retain unselected49pxfit, select36pxfit beside separately declaredR70painted neighbors.36frames/138checks, no new artwork generation, source-pixel edits or hand integration. R91partialtab code integratedDev39b from green exactsourcepush; redundantPR55minute cancellation remains distinct. Rollback requires normal tested Dev reconciliation for the source leaf; retain exact candidate/native/CI history. No complete role, family, owner/device/child or accepted-removal claim.

CHG-103 delivery: `194647a398f89fc52c3efbb32ff1f1c0e3e3cbca`, 143 direct required files / 51161118 bytes anonymously exact at 2026-10-17T18:55:07.549536+00:00. Same one-take hand, actual native fit/context and partial Dev integration only; no new generation, acceptance or removal credit.

## Painted Geologist washing pan — CHG-104

[R95](../docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/README.md) publishes the implemented source patch and current native context:106checks,16validframes,20excluded setupframes, sevenpartialagentviews, zero new generation. One whole painted pan replaces flat ellipses/arcs; original controls/progression/source preserved. FullCI is running on the frozen actual producer; no Dev/formal/device/child/owner acceptance inferred. Current workflow/heartbeat adopts owner2026-10-17 quality-first ImageGen direction and removes failed-reuse prerequisites. [Impact](../design/audit_impacts/flat-vector-geologist-pan-publication-20261017.json).

CHG-104 delivery: `1e0c4c2b7e93541c29f1148319482b5bbb2e4a3b`, 118 direct required files / 47239185bytes anonymously exact at 2026-10-17T21:15:00.699512+00:00. Runtime fullCI/sourceCI/Dev integration and visual/device/child/owner acceptance remain separate.

## Geologist painted mineral source samples and pan recovery — CHG-105

[R96](../docs/handoffs/codex_flat_vector_art_2026-10-07/r96_geologist_mineral_candidate/README.md) retains2actual built-in ImageGen PNGs for1existing mint mineral role, exact prompts/reference hashes, partial10-axis comparison and unresolved halo/reframing. No runtime or accepted-removal credit. R95fullCI59912finishedFAIL; normal saves/source stayed unchanged. CurrentDev has independently evidenced throne/verbs test-precondition repairs; same pan is reconciled and all82 unchanged trusted probes run through the documented probe-by-probe route in session1292. Preserve the original failure and current live handle. [Impact](../design/audit_impacts/flat-vector-geologist-mineral-candidate-20261017.json).

CHG-105 delivery: `7f5292785b331ee42a460eeba5ec612a687e2b0e`; 36 direct required files / 14860297 bytes anonymously exact at 2026-10-17T23:11:32.721329+00:00. Samples still alpha/context pending; original pan failure preserved and recovery1292 separate.

## Painted mineral Aseprite matte — CHG-106

[R97](../docs/handoffs/codex_flat_vector_art_2026-10-07/r97_geologist_mineral_matte/README.md) supplies a970x1015source cutout and editable two-layer master from generated take02. Aseprite clears6,210alpha1..15pixels and crops with16pxmargin; all584,044body RGBApixels remain exact. RGB under alpha0 explained part of the earlier visible-preview impression; historical raw states stay preserved, no raw take is relabeled approved. Opaque proof at44/64/128px is source-only, not actual-game runtime/QA11. Zero generation/drawing/runtime/removal increments; pan existingoperations continue unchanged. [Impact](../design/audit_impacts/flat-vector-geologist-mineral-matte-20261017.json).

CHG-106 delivery: `f6ffa4c54340818c88366cec2763a74beadaf30c`; 31 direct required files / 18344330 bytes anonymously exact at 2026-10-17T23:24:50.817308+00:00. Technical alpha/body proof passes; actual scene/acceptance and pan operations remain separate.

## Painted pan actual source publication — CHG-107

[R98](../docs/handoffs/codex_flat_vector_art_2026-10-07/r98_geologist_pan_source_ci/README.md) reconciles current registry/scene/tally to actual runtimecommit`ce05d4d38636fefc82af1172153c7f4d6119b562`. Current82probe-by-probe PASS, source/import/normal-save guards unchanged; original fullCI failure preserved.181required source files/40949356bytes anonymously exact. SourceCI39079175770running; no restart, Dev/formalQA11/device/child/owner pending. Existing artifact, frame and unknown-denominator totals unchanged;0new generation/removals. [Impact](../design/audit_impacts/flat-vector-geologist-pan-source-publication-20261017.json).

CHG-107 delivery: `b304633d55619568a844371493c102a929f3f90f`; 27 direct required files / 6698570 bytes anonymously exact at 2026-10-17T23:34:35.115823+00:00. Actual runtime source/local82/181file receipt verified; sourceCI and Dev/formal/physical acceptance remain separate.

## Painted pan current-Dev revalidation — CHG-108

The same painted-pan source is reconciled and published at `4918dc910b2f922a85f458cc0cdc710e8059c187`, with82unique trusted checks and two-aspect native context. [R99](../docs/handoffs/codex_flat_vector_art_2026-10-07/r99_geologist_pan_merge_revalidation/README.md) preserves initial console -1/no-verdict failure and native continuation, exact source/save guards and anonymous source delivery. Eight frame events; zero new artwork/artifacts/generation/accepted removal. New exact-sourceCI and Dev/formalQA11/device/child/owner remain separate. Rollback: preserve existing source/archive and revert only this current metadata delta, never restore flat pan as an accepted production fallback.

CHG-108 delivery: `6ea9f9d3d6b7fd353f8518d0e4b5c0d7caa9cb4c`; 29 direct required files / 5473836 bytes anonymously exact at 2026-10-18T02:20:42.422697+00:00. Actual runtime source/local82/current-source manifest receipt verified; sourceCI and Dev/formal/physical acceptance remain separate.

CHG-108 recovery continuation: [R100 same-pan actual source](../docs/handoffs/codex_flat_vector_art_2026-10-07/r100_geologist_pan_ci_recovery/README.md) publishes `2d91d85f20271d109c5a8dc90390de15925a4b24` with82trusted/static gates and anonymous source-byte receipt. Cancelled39089515223/55minutejobtimeout remains explicit; exact currentDev90minute workflow is inherited from existing owner-authorized1549c377. Existing R99 target context reused by hash; counts unchanged. Exact newCI/Dev/formalQA11/device/child/owner remain open. Rollback only this current metadata delta while preserving all previous evidence.

CHG-108 delivery: `ff891ffc0c9f6a2dfec9733bdc067bfb2f8cdcf8`; 28 direct required files / 5449499 bytes anonymously exact at 2026-10-18T04:40:12.640715+00:00. Actual runtime source/local82/current-source manifest receipt verified; sourceCI and Dev/formal/physical acceptance remain separate.

### R101 Geologist painted pan continuation — original pan CHG-104

Same artifact/sourcee69b50b5 reconciles Dev4d098375; current82/static/import and54native checks/8direct views pass. Source47files anonymously exact. Original failures retained, exactCI/Dev/formal/device/child/owner pending; no art/generation/artifact/removal credit. Current registry adds8bounded frame events only. This canonical change edits documentation and structured production evidence only; no repeated engine suite. Original pan rollback remains manual_reconstruction after later-caller review, preserving independent newer work, source art and saves; exact focused/full gates apply to any runtime rollback.

### Painted Geologist pan exactgreen Dev integration — original pan CHG-104

2026-10-29: sourceCI40824815737 is overallgreen at `e69b50b5e74d02f55985c7b87cf1f2271b91d452`, including trustedprobes. Dev fast-forwards4d098375 to that exact source, preserving fullsource/context47file delivery. Three changedruntimefiles anonymously match immutablebytes/SHA256; [receipt](../docs/handoffs/codex_flat_vector_art_2026-10-07/r101_geologist_pan_current_dev/dev_integration_20261029/DEV_INTEGRATION.json). Fourth partialDev artifact; fiveboundedsourceartifacts and allrole/frame/removal totals unchanged. NewDevAPK/formalQA11/device/child/owner remain pending; lifecycle/master satisfaction unchanged. Rollback remains originalpan CHG-104 manual_reconstruction after laterconsumer review; preserve allindependent changes, protectedoriginals, provenance andsavekeys. No runtime/engine rerun for this canonical bookkeeping delta.

### R102 first painted mint source production

2026-10-29 actualsource `8f86192be96dcdfc59b9f1c87899c4df015548a8`: [current production/evidence](../docs/handoffs/codex_flat_vector_art_2026-10-07/r102_geologist_mint_runtime/README.md). Existingpaintedsource preserved, one512-square technicalexport, firstmint dispatch only. Localcurrentstatic/import/82trusted and66configurednativechecks/8actualframes reviewed; fullsourcedelivery anonymous exact. Originalignored-fixture failure retained with byte-preserved oldtestfiles, no gate/probe/manifest relaxation. Sixboundedsourceartifacts,4partialDevartifacts, no newrole/family/removal. SourceCI/Dev/formal/external andothercolour/sharedcaller gaps remain. Actualruntime rollback is sourcepacketCHG-109 manual_reconstruction afterlaterconsumer review, preserving paintedpan, all source/reject/master/protectedbytes andsavekeys; this canonical bookkeeping does not modify runtime or repeat healthy engine checks.

### R103 remaining mineral source production

2026-10-29: [Production record](../docs/handoffs/codex_flat_vector_art_2026-10-07/r103_geologist_remaining_minerals/README.md). Two painted blue/lavender sources and native masters/512exports produced against exact8f scene and painted mint family. Original/reject sources preserved. Mint exact-green Dev integration credited once,4to5partial artifacts; source6 and frame6665/4134/10799 totals unchanged. Source-only outputs are unconsumed; rollback requires no runtime repair, preserve sources/history and supersede candidates explicitly. Formal/device/child/owner and global gaps remain.

### R104 two painted PAN mineral runtime variants

2026-10-29 actualsource `8df4757e6f2e399d1c4e3d7f352f0a38bef13b55`: [production/evidence](../docs/handoffs/codex_flat_vector_art_2026-10-07/r104_geologist_mineral_variants_runtime/README.md). Two whole painted sprites replace only the remaining blue/lavender PAN drawings; pure flat helper retired, census48to45,54otherfunctions unchanged. Actualcurrentstatic/import/all82trusted and90configurednativechecks/8reviewedframes pass. Source delivery anonymously exact.7boundedsource/5partialDev artifacts; eightnewframeevents, no newrole/family/removal. ExactCI/Dev/formal/external/global gaps remain. Actualruntime rollback is sourceCHG-110 manual_reconstruction afterlaterconsumer review; canonical bookkeeping changes no runtime and repeats no healthy engine suite.

### R104 painted PAN mineral Dev integration

2026-10-29: [verified integration](../docs/handoffs/codex_flat_vector_art_2026-10-07/r104_geologist_mineral_variants_runtime/dev_integration_20261029/README.md), exactsource `8df4757e6f2e399d1c4e3d7f352f0a38bef13b55`, sourceCI40855569210success and trustedstepsuccess, ordinary guarded Dev fastforward,5changedruntimefiles anonymous exact. Source7 unchanged, partialDev5to6 exactly once; no newroles/families/frameevents/removal or generation. Runtime is unchanged from the published reviewed candidate, so no repeat engine suite. Formal/external/otherGeologist/globalgaps and exactnewDevAPK remain open. Actualruntime rollback remains sourceCHG-110 manual_reconstruction afterlaterconsumer review; this bookkeeping changes no runtime.

### R105 painted PAN sediment runtime

2026-10-29 actualsource `0e2cf1c4a1840bc33dd288fc92428fd198880fa5`: [production/evidence](../docs/handoffs/codex_flat_vector_art_2026-10-07/r105_geologist_pan_sediment_runtime/README.md). One existing wholepaintedgrain replaces only flat PAN sediment dots; census45to44,56otherfunctions unchanged. Actualcurrentstatic/import/all82trusted and102configurednativechecks/8reviewedframes pass. Source delivery anonymously exact.8boundedsource/6partialDev artifacts; eightnewframeevents, no newrole/family/removal. ExactCI/Dev/formal/external/global gaps remain. Actualruntime rollback is sourceCHG-111 manual_reconstruction afterlaterconsumer review; canonical bookkeeping changes no runtime and repeats no healthy engine suite.

### R105 painted sediment Dev integration

2026-10-29: [verified integration](../docs/handoffs/codex_flat_vector_art_2026-10-07/r105_geologist_pan_sediment_runtime/dev_integration_20261029/README.md), exactsource `0e2cf1c4a1840bc33dd288fc92428fd198880fa5`, exactsourceCI success and trustedstepsuccess, ordinary guarded Dev fastforward,3changedruntimefiles anonymous exact. Source8 unchanged, partialDev6to7 exactly once; no newroles/families/frameevents/removal or generation. Runtime is unchanged from the published reviewed candidate, so no repeat engine suite. Formal/external/otherGeologist/globalgaps and exactnewDevAPK remain open. Actualruntime rollback remains sourceCHG-110 manual_reconstruction afterlaterconsumer review; this bookkeeping changes no runtime.

### R106 painted shared Geology workbench

Actualsource `44da99ba5c68153fa247e0794425b5f6d7d3cc79`: [production/evidence](../docs/handoffs/codex_flat_vector_art_2026-10-07/r106_geologist_workbench_runtime/README.md). Two-take named overhead view, first aspect reject retained; whole1024 candidate replaces three flat layers/helper. Currentstatic/import/local82/native220 and24reviewedcandidateframes pass. Anonymous source exact;9boundedsource/7partialDev artifacts,35events split32bounded/3excluded. Otherart/global/sourceCI/Dev/formal/external gates open, zero removal. Runtime rollback uses sourceCHG-112 manual reconstruction after laterconsumer review. Canonical bookkeeping changes no runtime and repeats no healthy engine suite.

### R106 painted workbench Dev integration

2026-10-29: [verified integration](../docs/handoffs/codex_flat_vector_art_2026-10-07/r106_geologist_workbench_runtime/dev_integration_20261029/README.md), exactsource `44da99ba5c68153fa247e0794425b5f6d7d3cc79`, exactsourceCI success and trustedstepsuccess, ordinary guarded Dev fastforward,3changedruntimefiles anonymous exact. Source9 unchanged, partialDev7to8 exactly once; no newroles/families/frameevents/removal or generation. Runtime is unchanged from the published reviewed candidate, so no repeat engine suite. Formal/external/otherGeologist/globalgaps and exactnewDevAPK remain open. Actualruntime rollback remains sourceCHG-112 manual_reconstruction afterlaterconsumer review; this bookkeeping changes no runtime.

### R107 painted fossil and exact matching fragments

Actualsource `f02aec12181b28706cae1f79705ff95df9aac7b9`: [production/evidence](../docs/handoffs/codex_flat_vector_art_2026-10-07/r107_geologist_fossil_runtime/README.md), one static wide backing and four technical exports, one coherent implementation. Currentstatic/import/all82trusted/native114/16reviewedframes and exactsourceCIgreen, normalDev integration verified.10source/9partialDev artifacts and16newbounded frameevents;6old sourceframes reused without credit. Allformal/external/global acceptance remains open, acceptedremoved0. Canonical bookkeeping repeats no engine suite; runtime rollback uses sourceCHG-113 with laterconsumer review.

### R108 painted soil material

Actualsource `97cfaa0bd90e47c33dfcae790417d3a1b2d5299a`: [production/evidence](../docs/handoffs/codex_flat_vector_art_2026-10-07/r108_geologist_soil_runtime/README.md), two static takes, one aspect reject, one whole material export, one coherent implementation. Currentstatic/import/all82trusted/native126/16reviewedframes and exactsourceCIgreen, normalDev integration verified.11source/10partialDev artifacts and16newbounded frameevents;8old sourceframes reused without credit. Allformal/external/global acceptance remains open, acceptedremoved0. Canonical bookkeeping repeats no engine suite; runtime rollback uses sourceCHG-114 with laterconsumer review.

### R109 painted crystal gallery

Actualsource `0f4fad1901967b8cc536c6d894dd255f4a9bb786`: [production/evidence](../docs/handoffs/codex_flat_vector_art_2026-10-07/r109_geologist_gallery_runtime/README.md), one static take/whole512export/implementation. Currentstatic/import/all82trusted/native88/16reviewedframes and exactsourceCIgreen/normalDev verified;8excluded nativeframes retain unchanged119terminal defect.12source/11partialDev artifacts,16newbounded/8excluded events;6prior frames reused without credit. Remaining geode/formal/external/global acceptance open, acceptedremoved0. Runtime rollback uses sourceCHG-115 after laterconsumer review; canonical bookkeeping runs no engine suite.

### R110 painted river source and receiving pools

Actualsource `51b2e1ef7b32d155786277871fc3f5e941145ea6`: [production/evidence](../docs/handoffs/codex_flat_vector_art_2026-10-07/r110_geologist_river_pools_runtime/README.md), one static take/3whole512exports/onecoherentimplementation. Currentstatic/import/all82trusted/native98/12reviewedframes and exactsourceCIgreen/normalDev verified,6excluded fixturefailureframes retained.13source/12partialDev artifacts,12newbounded/6excluded events;6oldsourceframes reused withoutcredit. Remainingformal/external/otherart/globalacceptanceopen, acceptedremoved0. Runtime rollback uses sourceCHG-116 after laterconsumerreview; canonicalmetadata runsnoengine suite.

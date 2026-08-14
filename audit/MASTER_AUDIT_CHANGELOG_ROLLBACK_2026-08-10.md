# Mermaid Roshan master-audit change and rollback ledger

- **Ledger ID:** `MA-CHANGELOG-2026-08-10`
- **Change-ID namespace:** `CHG-001` through `CHG-031`; IDs are permanent and
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

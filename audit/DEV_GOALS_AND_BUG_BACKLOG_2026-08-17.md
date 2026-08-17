# Mermaid Roshan: Reef of Light — branch review, bug-fix backlog, and development goals

- **Document ID:** `GOALS-2026-08-17`
- **Document authority:** `PROPOSED_CANDIDATE` — a planning proposal under the
  master-audit category. It is **not** canonical, it closes nothing, and it
  changes no `MA-*` lifecycle. Only
  [`audit/MASTER_AUDIT_2026-08-09.md`](MASTER_AUDIT_2026-08-09.md) and
  [`audit/findings/ACTIVE_FINDINGS_2026-08-13.md`](findings/ACTIVE_FINDINGS_2026-08-13.md)
  own audit state.
- **Review date:** 2026-08-17
- **Exact review head:** `origin/dev` `ac8ce9180760d7b848969ce43cece3963e675213`
  (2026-08-13, "audit: record integrated Sky Lagoon delivery")
- **Release branch at review time:** `origin/master`
  `e924d9ba14217e0b9b8de38b480b51a41e3aa183` (2026-08-05), 113 commits behind
  `dev`, 0 ahead
- **Branch estate reviewed:** all 313 remote branches at 2026-08-17
- **Change and rollback ledger:**
  [`audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md`](MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md)
- **Implementation status:** none. Every item below is a proposal. No runtime,
  asset, save, workflow, or authority file is changed by this document.

This document does three things and nothing else:

1. reviews the current master audit and states, in plain terms, what is
   actually blocking it;
2. reviews every remote branch and gives each unmerged branch a proposed
   disposition;
3. proposes a bug-fix backlog (`BF-*`) and a development-goal set (`G-*`),
   each with its evidence, its child-facing reason, and how it would be
   verified.

It does not promote diagnostic output into acceptance, does not assert a
runtime defect it did not observe, and does not treat a branch's existence as
proof that its content is either valuable or dead.

---

## 1. Scope, method, and evidence boundaries

### 1.1 What was reviewed

| Input | Exact scope |
|---|---|
| Master audit | `audit/MASTER_AUDIT_2026-08-09.md` at `ac8ce918` (1,832 lines, sections 1–14) |
| Canonical records | `audit/findings/ACTIVE_FINDINGS_2026-08-13.md` at `ac8ce918` (36 records) |
| Change ledger | `audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md` at `ac8ce918` |
| Branches | 313 remote branches, unshallowed clone, exact ahead/behind and merge-base per branch against `origin/dev` |
| Pull requests | All open pull requests (1) |
| Workflow runs | The 15 most recent `probes.yml` runs |
| Repository state | `scripts/`, `tools/`, `.github/workflows/`, `.gitignore`, `project.godot` at `ac8ce918` |
| Tools actually run here | `tools/audit_document_authority.py`, `tools/audit_probe_parity.py`, `tools/audit_game_2d.py` |

### 1.2 Evidence boundaries — read these before trusting any number below

- **No Godot binary exists in this review container**, and release downloads
  are proxy-blocked. No probe, no import, no capture, and no runtime
  observation was performed here. Every runtime claim in this document is
  quoted from the master audit or from a named GitHub run, never observed.
- **`tools/audit_game_2d.py` was run here and reported
  `FAIL - manifest drift (352 finding(s))`.** That result is an artefact of
  this container, not a product regression: the 352 findings are exactly the
  352 generated `*.glb.import` sidecars that only exist after a Godot import,
  which cannot run here. It is recorded as a tooling-ergonomics item
  (`BF-06`), explicitly **not** as a 2D-contract regression.
- `tools/audit_document_authority.py` and `tools/audit_probe_parity.py` are
  pure-Python and did run clean at `ac8ce918`:
  `DOCAUTH|INVENTORY=316|LEDGER=316|ACTIVE=34|RECORDS=36 … ALL OK` and
  `PROBE_PARITY|result: ALL OK`.
- Branch counts, merge-bases, file deltas, line counts, and workflow-run
  outcomes are directly measured and reproducible from the commands named in
  each item.
- Nothing here constitutes device, child, owner, exact-voice, human-listening,
  strict-2D, or accepted-visual evidence.

---

## 2. Master-audit review

### 2.1 Current state

The master audit round `MA-2026-08-09` is `IN_PROGRESS` / `UNSATISFIED`, cycle
state `REPAIRING` with concurrent focused `VERIFYING`. At `ac8ce918` the
canonical register holds 36 complete records — 22 P1 and 14 P2 — distributed
as:

| Lifecycle | Count | Reading |
|---|---|---|
| `FIXED_PENDING_VERIFICATION` | 11 | Repaired in code; waiting on evidence the machine cannot produce |
| `CONFIRMED_OPEN` | 11 | Real, reproduced, unrepaired |
| `BLOCKED_EXTERNAL` | 6 | Needs the owner, the child, or a physical device |
| `REPORTED_UNCONFIRMED` | 2 | Metric flagged it; no state-local evidence confirms a defect |
| `OWNER_DECISION_REQUIRED` | 2 | Not an engineering question |
| `VERIFIED_FIXED` | 2 | Retained in the register for anti-regression history |
| `IN_PROGRESS` | 1 | `MA-2D-002`, the game-wide true-2D conversion |
| `DEFERRED_WITH_REASON` | 1 | Optional optimisation |

### 2.2 The honest shape of the blockage

The audit's own satisfaction gate (section 12) has 16 conditions. Two are
checked. The remaining fourteen sort into exactly three buckets, and the
project's forward plan should be organised around that split rather than
around the finding list:

**Bucket A — engineering work that is genuinely unfinished (5 conditions).**
The zero-category `GAME2D` strict gate, the archive/preservation record, the
visual-stress green result with every gap dispositioned, the full runtime
capture matrix, and the clean second audit pass. These are the only items
where more code and more art actually move the needle. `MA-2D-002`,
`MA-VIS-006`, `MA-VIS-002`, `MA-VIS-003`, `MA-VIS-004`, `MA-OPERA-004`, and
`MA-ASSET-001` live here.

**Bucket B — evidence the CI machine structurally cannot produce (6
conditions).** Target-phone and Lenovo Tab M11 frame time, hitches, memory,
thermals and touch latency; the observed five-minute child golden path; owner
identity/style acceptance; human audio listening; exact protected voice; and
on-device touch/pause/save/re-entry. `MA-PERF-001`, `MA-CHILD-001`,
`MA-TOUCH-001`, `MA-ACCESS-001/002/003`, `MA-AUDIO-001`, `MA-COMBAT-001`, and
`MA-RELEASE-001` are all waiting here. **Eleven of the twenty-two P1/P2
non-terminal records are blocked on a human sitting down with a phone, not on
more code.** No amount of further repair work closes them.

**Bucket C — decisions only the owner can make (2 conditions plus 2
records).** `MA-PLAY-002` (the standalone fire arena's truthful home or
retirement) and `MA-OPERA-007` (Farmer/Doctor above-water backdrop
convention), plus the residual P2 route-card composition that obscures
Roshan's lower body and tail.

The single most useful thing that can happen next is **not** another repair
branch. It is one owner session with the phone that clears part of Bucket B
and answers Bucket C — because Bucket B is what the satisfaction gate is
actually waiting on, and every extra repair branch adds another
`FIXED_PENDING_VERIFICATION` record to the same queue. That observation drives
`G-01` below.

### 2.3 Where the repair order still holds

Section 13's order remains sound and this document does not propose replacing
it. The proposals below slot into it as follows: `BF-01`/`BF-02`/`G-02` serve
step 1 (preserve document control while authorising later repair); `BF-08` and
`G-04` serve step 3 (continue shrink-only true-2D conversion); `BF-09` serves
steps 2 and 4 (repair the harness so its assertions observe the intended
states); `G-01` serves step 9 (device matrix, listening matrix, child golden
path); and `G-06` serves step 8 (classify all probes).

---

## 3. Branch review — all 313 remote branches

### 3.1 Estate shape

| Measure | Value |
|---|---|
| Remote branches | 313 |
| Fully merged into `dev` (tip is an ancestor, 0 ahead) | 228 |
| Not merged into `dev` (1 or more unique commits) | 85 |
| `codex/*` | 169 |
| `claude/*` | 101 |
| `rescue/*` | 31 |
| `archive/*` | 5 |
| `auto/*`, `backup/*`, `integration/*`, `ww-lighting-wind` | 5 |
| `dev`, `master` | 2 |
| Distinct commits shared by two or more branch tips | 8 groups |
| Open pull requests | 1 (`#1`, opened 2026-07-09, base `master`) |
| Last commit anywhere in the estate | 2026-08-16, `claude/emperor-king-character-dev-3mmtoy` |

**228 of 313 branches are fully merged and have never been deleted.** They
carry no unique content; they only make the estate expensive to review and
make it easy to mistake a merged branch for live work. That is the single
largest hygiene problem in the repository, and it is cheap to fix.

`dev` history was re-founded on 2026-07-26/27 at the 2.5D redesign. Forty-seven
of the eighty-five unmerged branches fork from before that point — thirty of
them authored `claude/*` or `codex/*` branches and the rest `rescue/*` or
`archive/*` snapshots — so much of their "unique" commit count is pre-redesign
history rather than unlanded work.

### 3.2 The two master-audit branches

`codex/master-audit-20260809` and `codex/master-audit-docctrl-20260813` are
both **fully merged into `dev`** — 0 commits ahead, 32 and 5 behind
respectively. `dev` therefore already
carries the canonical master audit, the findings register, the change/rollback
ledger, `tools/audit_document_authority.py`, and the blocking document gate in
`.github/workflows/probes.yml`, and it is five commits ahead of the audit
branch with the Sky Lagoon true-Canvas conversion (`51d0abc0`, `441adf35`).
**`dev` — not either audit branch — is the current audit-control head.** This
document is therefore based on `dev` so it does not restate superseded Sky
Lagoon state; `MA-VIS-002` moved `CONFIRMED_OPEN` → `FIXED_PENDING_VERIFICATION`
in those five commits.

### 3.3 Proposed dispositions for the 85 unmerged branches

Disposition classes:

| Class | Count | Meaning and proposed action |
|---|---|---|
| `SALVAGE_REVIEW` | 18 | Forked at or after the redesign and carries runtime, tool, or workflow deltas. Diff its content against `dev` before deciding; land, rewrite, or retire deliberately. |
| `PRE_REDESIGN` | 30 | Forks before the 2026-07-27 redesign re-founding. Presumed superseded by the true-2D direction. Delete after confirming no unique asset or licence line is lost. |
| `EVIDENCE_SNAPSHOT` | 29 | `rescue/*` workspace preservation commits, not authored features. Keep as tags, not branches, or delete once their content is confirmed present or irrelevant. |
| `DUPLICATE_TIP` | 5 | `archive/*` branches whose tip commit is byte-identical to a `claude/*` branch tip. Keep exactly one name per tip. |
| `DOCS_REVIEW` | 3 | Recent, documentation-only, and the most likely to still matter. Review and land or reject explicitly. |

The `code/art/docs` column counts files changed against `dev` in
`scripts`+`tools`+`.github`+`project.godot` / `assets`+`assets_src` / `*.md`.

| Branch | Ahead | Fork base | Last commit | code/art/docs | Disposition |
|---|---|---|---|---|---|
| `claude/emperor-king-character-dev-3mmtoy` | 2 | 2026-08-05 | 2026-08-16 | 0/0/2 | DOCS_REVIEW |
| `codex/boxing-v2-design-20260812` | 1 | 2026-08-10 | 2026-08-12 | 0/0/1 | DOCS_REVIEW |
| `claude/opera-house-games-redesign-e3y590` | 3 | 2026-08-05 | 2026-08-11 | 0/0/2 | DOCS_REVIEW |
| `rescue/peter-20260809-opera-ballet-party-inflight` | 1 | 2026-08-09 | 2026-08-09 | 4/0/0 | EVIDENCE_SNAPSHOT |
| `rescue/desktop-ibimu2e-20260809-diegetic-inflight-on-ballet` | 1 | 2026-08-09 | 2026-08-09 | 2/0/0 | EVIDENCE_SNAPSHOT |
| `rescue/desktop-ibimu2e-20260809-diegetic-inflight-2` | 1 | 2026-08-09 | 2026-08-09 | 1/0/0 | EVIDENCE_SNAPSHOT |
| `rescue/desktop-ibimu2e-20260809-detective-start` | 1 | 2026-08-09 | 2026-08-09 | 0/0/0 | EVIDENCE_SNAPSHOT |
| `rescue/desktop-ibimu2e-20260809-boxing-start` | 2 | 2026-08-09 | 2026-08-09 | 6/0/1 | EVIDENCE_SNAPSHOT |
| `rescue/desktop-ibimu2e-20260809-ballet-start` | 1 | 2026-08-09 | 2026-08-09 | 4/0/1 | EVIDENCE_SNAPSHOT |
| `codex/deprecated-resources-roshan-20260809` | 11 | 2026-08-09 | 2026-08-09 | 8/115/96 | SALVAGE_REVIEW |
| `rescue/peter-2026-08-09-opera-takeover-start` | 1 | 2026-08-05 | 2026-08-09 | 0/117/2 | EVIDENCE_SNAPSHOT |
| `rescue/desktop-ibimu2e-20260809` | 1 | 2026-08-05 | 2026-08-09 | 1/4/0 | EVIDENCE_SNAPSHOT |
| `codex/castle-hall-polish` | 1 | 2026-08-04 | 2026-08-04 | 8/5/1 | SALVAGE_REVIEW |
| `claude/dust-bunny-boss-ai-qdbf48` | 1 | 2026-08-03 | 2026-08-04 | 1/0/2 | SALVAGE_REVIEW |
| `codex/nonlighting-integration-20260803` | 9 | 2026-08-03 | 2026-08-03 | 24/1/8 | SALVAGE_REVIEW |
| `claude/day-one-castle-intro-u77vnf` | 4 | 2026-08-02 | 2026-08-03 | 13/147/5 | SALVAGE_REVIEW |
| `codex/last48-integration-20260802` | 14 | 2026-08-02 | 2026-08-02 | 89/1750/128 | SALVAGE_REVIEW |
| `rescue/peter-20260802-pool-room-start` | 1 | 2026-08-01 | 2026-08-02 | 0/0/0 | EVIDENCE_SNAPSHOT |
| `claude/project-decommission-cleanup-w0gvn4` | 4 | 2026-08-01 | 2026-08-02 | 5/115/95 | SALVAGE_REVIEW |
| `claude/dust-bunny-ai-keszd0` | 1 | 2026-08-01 | 2026-08-02 | 3/0/2 | SALVAGE_REVIEW |
| `rescue/peter-2026-08-01-combat-assets-start` | 1 | 2026-08-01 | 2026-08-01 | 0/0/0 | EVIDENCE_SNAPSHOT |
| `rescue/peter-2026-08-01-combat-assets-handoff` | 2 | 2026-08-01 | 2026-08-01 | 1/12/1 | EVIDENCE_SNAPSHOT |
| `rescue/desktop-ibimu2e-2026-08-01-opera-start` | 1 | 2026-08-01 | 2026-08-01 | 0/9/0 | EVIDENCE_SNAPSHOT |
| `rescue/desktop-ibimu2e-2026-08-01-nursery-start` | 1 | 2026-08-01 | 2026-08-01 | 1/22/0 | EVIDENCE_SNAPSHOT |
| `rescue/desktop-ibimu2e-2026-08-01-dream-house-start` | 1 | 2026-08-01 | 2026-08-01 | 12/13/9 | EVIDENCE_SNAPSHOT |
| `codex/sky-lagoon-animal-support` | 3 | 2026-08-01 | 2026-08-01 | 6/1/4 | SALVAGE_REVIEW |
| `rescue/desktop-ibimu2e-2026-08-01-castle-start` | 1 | 2026-08-01 | 2026-08-01 | 28/78/8 | EVIDENCE_SNAPSHOT |
| `codex/redesign-promenade-swing` | 1 | 2026-07-30 | 2026-08-01 | 2/1/0 | SALVAGE_REVIEW |
| `codex/daddy-mermaid-animations` | 1 | 2026-07-30 | 2026-08-01 | 7/18/3 | SALVAGE_REVIEW |
| `rescue/desktop-ibimu2e-2026-08-01` | 1 | 2026-07-29 | 2026-08-01 | 21/29/11 | EVIDENCE_SNAPSHOT |
| `codex/roshan-25d-sprites` | 1 | 2026-07-29 | 2026-07-29 | 18/19/5 | SALVAGE_REVIEW |
| `rescue/desktop-2026-07-29-castle-prep` | 4 | 2026-07-29 | 2026-07-29 | 41/525/38 | EVIDENCE_SNAPSHOT |
| `codex/pearl-castle-interactivity` | 7 | 2026-07-29 | 2026-07-29 | 5/0/2 | SALVAGE_REVIEW |
| `codex/minigame-graphical-audit` | 1 | 2026-07-27 | 2026-07-28 | 35/340/3 | SALVAGE_REVIEW |
| `claude/3d-2d-game-audit-oj3v9p` | 2 | 2026-07-27 | 2026-07-28 | 1/0/1 | SALVAGE_REVIEW |
| `rescue/peter-2026-07-28-local-cartoon-video` | 1 | 2026-07-25 | 2026-07-28 | 6/0/4 | EVIDENCE_SNAPSHOT |
| `claude/game-redesign-2-5d-7nhkbw` | 3 | 2026-07-27 | 2026-07-27 | 1/0/4 | SALVAGE_REVIEW |
| `codex/day-one-opening-final` | 2 | 2026-07-26 | 2026-07-27 | 11/58/12 | PRE_REDESIGN |
| `claude/texture-codex-assets-dzfbij` | 4 | 2026-07-26 | 2026-07-27 | 7/33/7 | PRE_REDESIGN |
| `codex/day-one-opening` | 5 | 2026-07-26 | 2026-07-27 | 12/53/11 | PRE_REDESIGN |
| `codex/pointer-navigation` | 1 | 2026-07-27 | 2026-07-26 | 18/0/0 | SALVAGE_REVIEW |
| `claude/craft-layer-canvases` | 1 | 2026-07-27 | 2026-07-26 | 3/7/1 | SALVAGE_REVIEW |
| `claude/castle-camera-audit` | 1 | 2026-07-26 | 2026-07-26 | 5/0/0 | PRE_REDESIGN |
| `claude/storybook-ui-dev` | 1 | 2026-07-26 | 2026-07-26 | 1/0/1 | PRE_REDESIGN |
| `codex/roshan-pool-pnw` | 10 | 2026-07-25 | 2026-07-26 | 8/12/2 | PRE_REDESIGN |
| `claude/codex-audit-design-items-11ooie` | 2 | 2026-07-25 | 2026-07-26 | 5/24/2 | PRE_REDESIGN |
| `integration/opera-return-fix` | 1 | 2026-07-25 | 2026-07-26 | 1/0/0 | PRE_REDESIGN |
| `claude/mermaid-character-audit-nqx5ix` | 5 | 2026-07-21 | 2026-07-26 | 21/58/9 | PRE_REDESIGN |
| `claude/navigation-audit-world-castle-lzezdx` | 9 | 2026-07-21 | 2026-07-25 | 12/38/8 | PRE_REDESIGN |
| `claude/mermaid-roshan-combo-system-ctiokp` | 4 | 2026-07-21 | 2026-07-25 | 2/40/7 | PRE_REDESIGN |
| `claude/toca-boca-design-analysis-m61udu` | 10 | 2026-07-21 | 2026-07-25 | 9/38/9 | PRE_REDESIGN |
| `claude/mermaid-roshan-spells-mdinxn` | 3 | 2026-07-21 | 2026-07-25 | 9/40/8 | PRE_REDESIGN |
| `claude/game-analysis-reflection-nnv3bj` | 1 | 2026-07-21 | 2026-07-25 | 11/0/1 | PRE_REDESIGN |
| `claude/game-art-audit-impl-j6p6ly` | 34 | 2026-07-25 | 2026-07-25 | 38/518/42 | SALVAGE_REVIEW |
| `codex/dirty-castle-2d` | 4 | 2026-07-22 | 2026-07-23 | 2/325/4 | PRE_REDESIGN |
| `claude/opera-house-stage-kp3oq3` | 1 | 2026-07-22 | 2026-07-23 | 2/0/0 | PRE_REDESIGN |
| `claude/todo-implementation-i4hkmh` | 1 | 2026-07-21 | 2026-07-23 | 1/0/0 | PRE_REDESIGN |
| `rescue/peter-2026-07-22-fairy-background-preflight` | 1 | 2026-07-21 | 2026-07-22 | 5/1/0 | EVIDENCE_SNAPSHOT |
| `claude/remove-cc0-assets-regen-sieh6e` | 4 | 2026-07-21 | 2026-07-22 | 4/48/4 | PRE_REDESIGN |
| `claude/game-narrative-day-structure-v2k7w4` | 5 | 2026-07-21 | 2026-07-22 | 0/0/4 | PRE_REDESIGN |
| `codex/sky-lagoon-pnw-trees` | 1 | 2026-07-21 | 2026-07-21 | 9/117/3 | PRE_REDESIGN |
| `rescue/peter-2026-07-29-dev-camera-p0-codex` | 1 | 2026-07-19 | 2026-07-19 | 4/0/1 | EVIDENCE_SNAPSHOT |
| `claude/android-apk-upload-6yzxxv` | 1 | 2026-07-18 | 2026-07-18 | 1/0/0 | PRE_REDESIGN |
| `rescue/peter-2026-07-18-claude-art-start` | 1 | 2026-07-18 | 2026-07-18 | 0/66/0 | EVIDENCE_SNAPSHOT |
| `rescue/desktop-ibimu2e-2026-07-16-art-audit-start` | 1 | 2026-07-16 | 2026-07-16 | 1/32/0 | EVIDENCE_SNAPSHOT |
| `codex/gabby-stage` | 6 | 2026-07-16 | 2026-07-16 | 3/0/0 | PRE_REDESIGN |
| `codex/fairy-art-rebuild` | 1 | 2026-07-16 | 2026-07-16 | 9/33/3 | PRE_REDESIGN |
| `rescue/peter-2026-07-15-landmark-start` | 1 | 2026-07-15 | 2026-07-15 | 9/28/0 | EVIDENCE_SNAPSHOT |
| `rescue/desktop-ibimu2e-2026-07-15-collection-start` | 1 | 2026-07-15 | 2026-07-15 | 0/2/0 | EVIDENCE_SNAPSHOT |
| `rescue/peter-2026-07-15-art-remediation` | 3 | 2026-07-15 | 2026-07-15 | 14/611/28 | EVIDENCE_SNAPSHOT |
| `rescue/peter-2026-07-14-combat-start` | 1 | 2026-07-14 | 2026-07-14 | 7/582/25 | EVIDENCE_SNAPSHOT |
| `rescue/peter-2026-07-14-art-batch-02` | 3 | 2026-07-14 | 2026-07-14 | 13/604/28 | EVIDENCE_SNAPSHOT |
| `rescue/desktop-master-work-2` | 1 | 2026-07-13 | 2026-07-13 | 1/0/0 | EVIDENCE_SNAPSHOT |
| `claude/physics-engine-improvements-pdfz5r` | 4 | 2026-07-13 | 2026-07-13 | 7/0/1 | PRE_REDESIGN |
| `archive/physics-jolt-cove` | 4 | 2026-07-13 | 2026-07-13 | 7/0/1 | DUPLICATE_TIP |
| `claude/roshan-codebase-audit-ufn9cs` | 2 | 2026-07-11 | 2026-07-11 | 2/0/1 | PRE_REDESIGN |
| `claude/game-dev-mode-tools-lhqs7l` | 1 | 2026-07-11 | 2026-07-11 | 3/0/0 | PRE_REDESIGN |
| `archive/roshan-codebase-audit` | 2 | 2026-07-11 | 2026-07-11 | 2/0/1 | DUPLICATE_TIP |
| `archive/game-dev-mode-tools` | 1 | 2026-07-11 | 2026-07-11 | 3/0/0 | DUPLICATE_TIP |
| `rescue/desktop-master-work` | 1 | 2026-07-09 | 2026-07-09 | 1/8/0 | EVIDENCE_SNAPSHOT |
| `claude/replace-assets-free-sources-z3jp2y` | 1 | 2026-07-09 | 2026-07-09 | 1/8/0 | PRE_REDESIGN |
| `claude/replace-assets-free-sources-lnplz7` | 1 | 2026-07-09 | 2026-07-09 | 1/8/0 | PRE_REDESIGN |
| `archive/replace-assets-voices` | 1 | 2026-07-09 | 2026-07-09 | 1/8/0 | DUPLICATE_TIP |
| `claude/first-level-texture-audit-gl8xyq` | 5 | 2026-06-25 | 2026-06-25 | 1/27/0 | PRE_REDESIGN |
| `archive/first-level-texture-audit` | 5 | 2026-06-25 | 2026-06-25 | 1/27/0 | DUPLICATE_TIP |

### 3.4 The five branches that actually matter

Ranked by how much unlanded value they hold against the audit's own priorities:

1. **`codex/deprecated-resources-roshan-20260809`** (11 commits) — the
   decommission programme: tranche-1 quarantine of superseded docs and dead
   working data, an audio-usage audit that resolves runtime-composed paths and
   labels all 186 audio files, quarantine of the orphaned castle 3D kit and
   rig-workbench models, archival of the retired Roshan 3D pipeline, Meshy
   source bundles and importer sidecars, and a shrinking game-wide 2D
   contract. **`decommissioned/` does not exist on `dev` at `ac8ce918`** — none
   of it landed. This is the largest single lever on `MA-2D-002` and
   `MA-ASSET-001` sitting outside the integration branch. See `BF-08`.
2. **`claude/project-decommission-cleanup-w0gvn4`** (4 commits) — the first
   four commits of the same programme, superseded by the branch above; review
   the two together, land once.
3. **`claude/day-one-castle-intro-u77vnf`** (4 commits) — a Days system driven
   from the pause menu with no day selected by default, the Huluu opener cut,
   and movement plus interaction taught in the Sky Lagoon. Nothing matching
   `story_day`/`day_one` exists in `scripts/` on `dev`. This is onboarding
   work that bears directly on `MA-PLAY-001` and `MA-CHILD-001`; it should be
   reviewed on its merits and either landed or explicitly rejected.
4. **`codex/last48-integration-20260802`** (14 commits, 89 code files) and
   **`codex/nonlighting-integration-20260803`** (9 commits, 24 code files) —
   integration branches that merged several topic branches and were then
   abandoned. Their constituents may have landed individually; each needs a
   content diff, not a merge.
5. **`claude/emperor-king-character-dev-3mmtoy`** — the newest commit in the
   repository (2026-08-16) and the only branch carrying an owner decision that
   the integration branch does not have. See `BF-01`.

### 3.5 Branches that are already fine

The 228 merged branches include every branch named in the master audit's
evidence chain — `codex/master-audit-*`, `codex/opera-career-distribution-20260812`,
`codex/sky-lagoon-canvas-repair-20260813`, `codex/castle-royal-hall`,
`codex/opera-art-regeneration`, `claude/combat-wing-20260804` — so the audit's
commit references all resolve inside `dev`. No audit-cited work is stranded.

---

## 4. New observations from this review

These are observations, not audit findings. Each names exactly how it was
measured. None changes any `MA-*` lifecycle.

| ID | Observation | How it was measured |
|---|---|---|
| `BR-01` | `master` is 113 commits behind `dev` and has not moved since 2026-08-05, while `dev` is green at `ac8ce918` (run `31768445745`, 2026-08-14). | `git rev-list --left-right --count origin/master...origin/dev`; workflow-run list |
| `BR-02` | `claude/emperor-king-character-dev-3mmtoy` adds a binding music-direction decision to `CLAUDE.md` dated 2026-08-16 plus a new `MUSIC_DIRECTION.md`, and that path has no row in `design/05_DOC_LEDGER.md` on any branch. | `git diff origin/dev...` on that branch; `grep MUSIC_DIRECTION.md` in its ledger returns 0 |
| `BR-03` | The decommission programme is entirely unlanded; `dev` still carries 509 `.glb` files and 157 tracked `.glb.import` sidecars. | `git ls-tree -d origin/dev decommissioned` is empty; `git ls-tree -r --name-only origin/dev` counts |
| `BR-04` | 228 of 313 branches are fully merged and undeleted; 8 commits are each the tip of two or more branches. | `git rev-list --left-right --count` per branch; `git for-each-ref` tip grouping |
| `BR-05` | Pull request `#1` has been open since 2026-07-09 and targets `master`, which by owner rule moves only by promotion. | Open-PR listing |
| `BR-06` | 107 probe scripts exist; `scripts/ci.sh` names 64 in one hardcoded trusted list; 43 have no declared classification. | `ls scripts/probe*.gd`; `scripts/ci.sh` line 127 |
| `BR-07` | `scripts/main.gd` is 8,734 lines at `ac8ce918`, up from the 8,647 recorded at `09e5e356`, against an extraction-only target below 2,500. | `wc -l scripts/main.gd`; master audit `MA-CODE-001` |
| `BR-08` | `.github/workflows/android.yml` binds to the probe workflow by its literal `name:` string, and its own comment records that renaming the probe workflow silently stops all APK builds with no error. | Reading `.github/workflows/android.yml` lines 6–12 |
| `BR-09` | Remote capture steps do request `--rendering-method mobile` under `xvfb-run`, yet the register records that both current remote Sky subprocesses fail requested-Mobile renderer identity — so remote visual output cannot be authoritative regardless of workflow success. | `.github/workflows/probes.yml`; `MA-VIS-002` verification field at `ac8ce918` |
| `BR-10` | The latest dev APK is 596,041,412 bytes. | Master audit section 1, Android run `31695675866` |

---

## 5. Proposed bug-fix backlog

Each item states its confidence honestly. `CONFIRMED` means measured in this
review from repository state. `CANDIDATE` means it needs runtime confirmation
before anyone changes code.

### BF-01 — Merging the music-direction branch as-is would break the document gate

- **Confidence:** `CONFIRMED`
- **Related:** `MA-DOC-002`, `MA-DOC-005` (both `VERIFIED_FIXED`)
- **Statement:** `claude/emperor-king-character-dev-3mmtoy` adds
  `MUSIC_DIRECTION.md` with no matching row in `design/05_DOC_LEDGER.md`. It
  passes its own CI only because it forks from 2026-08-05, before the document
  gate landed. Merged into `dev` unchanged, `tools/audit_document_authority.py`
  would see a 317-path inventory against 316 ledger rows and fail closed,
  regressing two terminal P1 findings.
- **Fix:** in the same merge, add one scoped ledger row for `MUSIC_DIRECTION.md`,
  index it in `design/00_MASTER_INDEX.md`, and re-run the document gate before
  pushing. The `CLAUDE.md` edit is a high-risk authority change and must be
  called out in its commit message.
- **Verification:** `python3 -B tools/audit_document_authority.py` reports
  `INVENTORY=317|LEDGER=317` with `ALL OK`, plus its focused unit suite and
  `--stress` controls.
- **Child impact:** none directly; it protects the authority chain that keeps
  repairs pointed at the right art and mechanics.

### BF-02 — The 2026-08-16 owner music decision is not in the integration branch

- **Confidence:** `CONFIRMED`
- **Related:** `MA-DOC-002`
- **Statement:** the newest owner decision in the repository — Condard-inspired
  chiptune direction, four voices, ≤112 BPM, no sampling, music never signals
  failure — exists only on an unmerged branch. Any agent reading `dev` will not
  see it, and `MUSIC_AUDIT_2026-08-09.md` on `dev` predates it.
- **Fix:** land it under `BF-01`'s conditions, or record explicitly that it is
  a proposal the owner has not finalised. Either is fine; silence is not.
- **Verification:** the decision appears exactly once in the authority chain
  with a date and a named spec, and the ledger states its scope.

### BF-03 — A stale pull request targets the release branch

- **Confidence:** `CONFIRMED`
- **Statement:** PR `#1` (2026-07-09, "Asset licensing audit; flag
  non-redistributable aquatic pack for CC0 swap") is still open against
  `master`. Under the owner rule, `master` moves only by fast-forward
  promotion from `dev`, so this PR can never merge as targeted, and its
  licensing content is 5 weeks stale.
- **Fix:** close it with a note, or reopen its still-valid licensing points as
  a fresh change against `dev`.
- **Verification:** zero open PRs targeting `master`.

### BF-04 — The APK build is bound to a workflow display name

- **Confidence:** `CONFIRMED` (latent; the failure mode is documented in-file)
- **Statement:** `.github/workflows/android.yml` triggers on `workflow_run`
  matched by the probe workflow's literal `name:`. Renaming that workflow stops
  every APK build silently — no error, no build, and the phone's stable
  bookmark quietly stops updating.
- **Fix:** add a guard step that fails loudly when no matching upstream run is
  found, and a scheduled canary that asserts an APK newer than the last green
  `dev` push exists. Changes to `.github/workflows/` are high-risk and
  explicit-task-only.
- **Verification:** deliberately renaming the probe workflow in a scratch
  branch produces a red guard rather than silence.
- **Child impact:** direct — a silent break means she keeps playing an old
  build while everyone believes she has the new one.

### BF-05 — 43 of 107 probe scripts have no declared classification

- **Confidence:** `CONFIRMED`
- **Related:** `MA-CI-003`
- **Statement:** `scripts/ci.sh` line 127 is a single hardcoded 64-name list.
  The other 43 probe scripts are neither trusted, nor declared advisory,
  diagnostic, obsolete, or quarantined. A probe can rot for weeks without
  anyone noticing, and a new probe joins the gate only if someone remembers to
  edit that line.
- **Fix:** move the roster to a declarative data file with exactly one class
  per probe, have `scripts/ci.sh` and `.github/workflows/probes.yml` read it,
  and extend `tools/audit_probe_parity.py` to fail closed on any probe script
  with zero or more than one classification.
- **Verification:** parity tool reports 107 scripts, 107 classifications, and
  the existing 64-local/63-remote trusted split unchanged.

### BF-06 — The 2D audit reports manifest drift on a checkout that has not been imported

- **Confidence:** `CONFIRMED` (tooling ergonomics, not a product defect)
- **Related:** `MA-2D-002`
- **Statement:** on a clean checkout with no Godot import,
  `python3 -B tools/audit_game_2d.py` emits 352 `G2D201` "stale active
  untracked model import sidecar manifest entry" findings and
  `RESULT| FAIL - manifest drift (352 finding(s))`. Those 352 paths are exactly
  the generated sidecars that only exist post-import. The tool is right to fail
  closed, but the message invites a reader to believe the manifest drifted when
  the import simply has not run.
- **Fix:** detect the "import has not run" state and emit a distinct code and
  message — still fail-closed, but naming the real cause and the remedy
  (`--headless --import .`).
- **Verification:** the same clean checkout produces the distinct code; a
  genuinely drifted manifest still produces `G2D201`; existing unit and stress
  controls stay green.

### BF-07 — `main.gd` grew instead of shrinking

- **Confidence:** `CONFIRMED`
- **Related:** `MA-CODE-001`, `MA-CODE-002`
- **Statement:** 8,647 lines at `09e5e356` → 8,734 at `ac8ce918`. The target is
  extraction-only, below 2,500. Nothing currently prevents the next feature
  from adding another 200.
- **Fix:** add a ratchet to the static gate — a recorded ceiling that may only
  be lowered, failing any change that raises it. Then resume mechanical
  extraction one builder or one minigame tick per commit, probe-gated before
  and after, exactly as the refactor rules require.
- **Verification:** the ratchet fails a deliberate +1-line test commit; the
  full trusted probe suite stays green across each extraction.

### BF-08 — The decommission tranche is unlanded and the install is 596 MB

- **Confidence:** `CONFIRMED` (branch content and counts); `CANDIDATE` (that
  landing it materially reduces the APK — that needs a build to prove)
- **Related:** `MA-2D-002`, `MA-ASSET-001`, `MA-ASSET-004`, `MA-PERF-001`
- **Statement:** `dev` carries 509 model files and 157 tracked sidecars, the
  orphan PNG reports total roughly 222 MB across Castle, Galaxy, Opera and
  Lagoon, and the current dev APK is 596,041,412 bytes. The branch that
  quarantines the orphaned castle 3D kit, archives the retired Roshan 3D
  pipeline and Meshy bundles, and labels all 186 audio files has never been
  merged.
- **Fix:** review `codex/deprecated-resources-roshan-20260809` against `dev`,
  then land it in bounded, individually probe-gated slices — archive and record
  provenance before any active deletion, keep protected book art, family
  voices, and friend cutouts untouched, and hold save compatibility.
- **Verification:** per slice — `GAME2D` category counts fall with exact
  `NO_REGRESSION`, import is clean, focused plus surrounding plus full trusted
  probes are green, the archive record is complete, and no archived resource is
  still an active fallback. Then measure the APK.
- **Child impact:** direct — a 568 MiB install on a three-to-four-year-old
  Android phone is slow to download, slow to update, and competes for storage
  she does not have.

### BF-09 — Remote captures cannot prove they ran on the Mobile renderer

- **Confidence:** `CONFIRMED` (from the register's own verification text)
- **Related:** `MA-VIS-002`, `MA-VIS-006`, `MA-OPERA-004`
- **Statement:** capture steps request `--rendering-method mobile` under
  `xvfb-run`, but both current remote Sky subprocesses fail requested-Mobile
  renderer identity, and the raw Sky output has stood at 21 `OK` / 44 `FAIL` /
  one `DONE` across several runs. This is *the* structural reason 86 visual
  checks sit in `COVERAGE_GAP` and cannot leave it: the machine cannot produce
  evidence the contract will accept.
- **Fix:** give the runner a Vulkan implementation that reports the Mobile
  renderer (a software ICD such as lavapipe, or a self-hosted runner with a
  GPU); assert renderer identity in-process at capture start and fail closed on
  mismatch. If that proves impossible on hosted runners, then say so in the
  contract and move the visual gate to a device-only gate rather than leaving
  86 gaps permanently open.
- **Verification:** a capture run prints the requested renderer identity and
  the Sky diagnostic reaches an internally consistent result; `MA-VIS-006`
  totals move for the first time.

### BF-10 — Branch-tip ambiguity between `archive/*` and `claude/*`

- **Confidence:** `CONFIRMED`
- **Statement:** five `archive/*` branches point at commits that are also the
  tips of `claude/*` branches, and `archive/replace-assets-voices` shares its
  tip with three other names. Nothing states which name is authoritative.
- **Fix:** keep one name per tip, delete the rest, and record the deletions in
  a short branch ledger so the history is recoverable by SHA.
- **Verification:** no commit is the tip of more than one branch.

### BF-11 — Unreviewed in-flight Opera scripts sit only on rescue snapshots

- **Confidence:** `CANDIDATE`
- **Related:** `MA-OPERA-004`, `MA-OPERA-005`, `MA-OPERA-009`
- **Statement:** five `rescue/*` branches from 2026-08-09 carry unique versions
  of `scripts/opera_ballet_surface.gd`, `scripts/opera_career_world_2d.gd`,
  `scripts/opera_stage_paths.gd`, `scripts/opera_world_hotspot_2d.gd`, and
  `scripts/probe_opera_2d.gd`. Whether any of it is a fix that never landed or
  simply a mid-edit snapshot is unknown without diffing each against `dev`.
- **Fix:** diff each of the five files against `ac8ce918`; land anything that is
  a genuine repair through the normal probe gate; delete the snapshots
  otherwise.
- **Verification:** each file is either identical to `dev`, or its delta is
  landed with focused probes green, or the branch is deleted with its SHA
  recorded.

### BF-12 — Route cards obscure Roshan's lower body and tail

- **Confidence:** `CONFIRMED` by the audit (residual P2, all nine room captures)
- **Related:** `MA-OPERA-012`
- **Statement:** the 154×154 lower-centre career cards clear the controls but
  cover Roshan's tail in every Castle room-route capture.
- **Fix:** restage the cards without shrinking the touch target below the
  child-safe minimum and without reintroducing the deleted all-career hub.
- **Verification:** new captures at 1280×720 and a wide-phone aspect show the
  full character silhouette; target size is unchanged or larger; room-route
  probes stay green.

---

## 6. Proposed development goals

### G-01 — One owner-and-child evidence session, run as a first-class deliverable

**This is the highest-leverage item in the document.** Eleven of the
twenty-two non-terminal P1/P2 records — `MA-PERF-001`, `MA-CHILD-001`,
`MA-TOUCH-001`, `MA-AUDIO-001`, `MA-COMBAT-001`, `MA-RELEASE-001`,
`MA-OPERA-001`, `MA-OPERA-005`, `MA-OPERA-009`, `MA-OPERA-010`,
`MA-OPERA-011` — plus most of `MA-OPERA-012` are waiting on evidence that only
a phone, an adult, and the child can produce. Every further repair branch adds
to that queue rather than draining it.

Build the session as tooling, not as an event: a printed one-page checklist
generated from the register, a capture protocol for the target phone and the
Lenovo Tab M11, a 30-minute soak with frame-time and thermal logging, an audio
listening pass in the room where she actually plays, and a five-minute
observed golden path with no adult verbal instruction. Store the results as
evidence records under the existing protocol.

**Definition of done:** at least six `FIXED_PENDING_VERIFICATION` records have
either device evidence attached or a named reason they still cannot close.

### G-02 — Keep document control green while everything else moves

`MA-DOC-002` and `MA-DOC-005` are the only two `VERIFIED_FIXED` records, and
both regress on drift. Every change that adds or removes a Markdown path, or
that edits `CLAUDE.md`, `AGENTS.md`, `SECURITY.md`, `.claude/`, `.codex/`, or
`.github/workflows/`, must carry its ledger row in the same commit. `BF-01` is
the immediate instance; the goal is that this never becomes an instance again.

**Definition of done:** the document gate is green at every head for a full
month, including at least one merge that adds a new Markdown path.

### G-03 — Ship what is already green

`dev` is green at `ac8ce918`; `master` has not moved since 2026-08-05. The
child's stable bookmark predates the entire thirteen-career Castle-room
distribution, the boss retirement, the 42-cue music programme, the Royal Hall,
and the Sky Lagoon true-Canvas conversion. Either promote — the workflow
refuses unless the probe suite is green for `dev`'s exact head — or record the
owner's explicit decision to hold, with the reason. A twelve-day silent gap
between a green integration branch and the release branch is itself the
finding.

**Definition of done:** `master` matches a green `dev` head and the stable APK
URL serves a build containing the current Castle-room routing, or a dated
owner hold is recorded.

### G-04 — Drive the true-2D contract to zero, family by family

`MA-2D-002` is the only `IN_PROGRESS` record and the largest remaining
engineering arc: 509 model files, 157 tracked plus 352 generated sidecars, 65
production 3D files, 70 probe 3D files, one 3D scene, one 3D configuration.
Sequence it as: land the decommission tranche (`BF-08`), then take one gameplay
family per bounded slice — the kart racer is the largest single remaining
consumer of 3D code and is still referenced from the living-world catalogue and
three probes — archiving exact resources before any active deletion and holding
`NO_REGRESSION` at every step.

**Definition of done:** all eleven `GAME2D` categories are zero, strict exits
zero, and import plus the full trusted probe suite are green at the same
commit.

### G-05 — Close the visual evidence loop

`MA-VIS-006` is stuck at 16 FAIL / 17 REVIEW_OPEN / 2 MANUAL_OPEN / 86
COVERAGE_GAP / 32 PASS / 94 NOT_APPLICABLE, and it will stay stuck until
`BF-09` gives captures a renderer identity worth trusting. After that, build
the live state adapters for converted surfaces and Fairy, then work the failure
list down. Resolve `MA-VIS-003` and `MA-VIS-004` from state-local evidence
only — approved art must not be recoloured to satisfy a source-average
heuristic.

**Definition of done:** every applicable visual item has current accepted live
evidence, and each remaining gap has an explicit named disposition.

### G-06 — Make the test estate self-describing

Combine `BF-05` with a documented meaning for each probe class, so a
newcomer — human or agent — can tell in one file which probes gate a release,
which are advisory, and which are dead. Retire probes proved obsolete rather
than leaving them to rot.

**Definition of done:** every probe script carries exactly one classification,
enforced fail-closed, with the trusted split unchanged.

### G-07 — Consolidate the branch estate

Delete the 228 merged branches after recording their tips, resolve the five
duplicate `archive/*` tips, convert `rescue/*` snapshots to tags, decide the
30 pre-redesign branches as a batch, and work the 18 `SALVAGE_REVIEW` branches
one at a time. Then adopt a rule: a branch is deleted when merged, and a
work branch that goes 30 days without a commit is either landed or explicitly
retired.

**Definition of done:** fewer than 40 remote branches, each with a named owner
and purpose, and a short ledger recording every deleted tip by SHA.

### G-08 — Answer the open owner questions

`MA-PLAY-002` (the standalone fire arena's home or retirement) and
`MA-OPERA-007` (Farmer and Doctor's above-water backdrop convention) are
`OWNER_DECISION_REQUIRED` and block the P2 half of the satisfaction gate. Add
the `BF-12` route-card composition question and the `BF-02` music-direction
status to the same queue. Batch them into one short decision list rather than
raising them one at a time.

**Definition of done:** every `OWNER_DECISION_REQUIRED` record carries a dated
decision.

### G-09 — Reduce install size to something a small phone can hold

Set an explicit budget for the shipped APK, measure against it in CI, and treat
`BF-08` and `MA-ASSET-001` as the first two levers. The point is not
tidiness — it is that update friction on the family phone is a real obstacle to
her playing the current build.

**Definition of done:** a stated budget, a CI measurement against it, and a
measured reduction from 596,041,412 bytes.

### G-10 — Onboarding and reachability as one piece of work

`MA-PLAY-001` needs a fresh-save, no-cheat, child-visible route through every
destination. `claude/day-one-castle-intro-u77vnf` proposes exactly the
onboarding this needs — a Days system with no day selected by default, the
Huluu opener cut, movement and interaction taught in the Sky Lagoon — and none
of it is on `dev`. Review it on its merits first, then build the complete route
matrix around whatever onboarding the owner accepts, with a visible pointer and
a spoken cue for every objective.

**Definition of done:** an automated route matrix covers every visible
destination for entry, exit, and re-entry from a fresh save, and a device
session confirms it without adult verbal instruction.

---

## 7. Proposed sequence

| Wave | Items | Why this order |
|---|---|---|
| 1 — cheap and unblocking | `BF-01`, `BF-02`, `BF-03`, `BF-10`, `G-02` | Hours of work; protects the two terminal document findings and clears estate noise before anyone reviews branches again |
| 2 — get value to the child | `G-03`, `BF-04`, `G-01` | The build she plays is twelve days and 113 commits stale, the APK pipeline can break silently, and device evidence is what the audit is actually waiting on |
| 3 — structural debt | `BF-08`, `G-04`, `BF-07`, `G-09` | The true-2D arc and the install size are the same problem seen from two sides |
| 4 — evidence machinery | `BF-09`, `G-05`, `BF-05`, `G-06` | Without a trustworthy renderer identity the visual gate cannot close no matter how much art changes |
| 5 — content and decisions | `BF-11`, `BF-12`, `G-08`, `G-10`, `G-07` | Needs owner input and per-branch review; safe to run in parallel with wave 4 |

---

## 8. What this document does not claim

- It does not close, reopen, or re-severity any `MA-*` finding.
- It does not claim any runtime, device, child, owner, exact-voice,
  human-listening, strict-2D, or accepted-visual evidence. None was produced.
- It does not assert that any unmerged branch's content is safe to merge. Every
  `SALVAGE_REVIEW` disposition explicitly requires a content diff first.
- It does not assert that the branches marked `PRE_REDESIGN` are worthless —
  only that they fork before the redesign re-founding and need a batch decision
  before deletion.
- It does not treat the `GAME2D` result measured in this container as a
  product regression; see section 1.2.
- It proposes no change to protected book art, family voices, or friend
  cutouts, and no change to save-file keys.

---

## 9. Review log

| Date | Author | Change |
|---|---|---|
| 2026-08-17 | Branch and goals review | Created at `origin/dev` `ac8ce918`: master-audit review, 313-branch review with dispositions for all 85 unmerged branches, ten observations, twelve proposed bug fixes, ten development goals, and a five-wave sequence. No implementation. |

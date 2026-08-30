# Active master-audit findings register — 2026-08-13

This is the stable canonical-record companion to section 5 of
`audit/MASTER_AUDIT_2026-08-09.md`. It contains the 36 material P1/P2 items
that were non-terminal when this register was created. Stable records remain
here through later lifecycle transitions so their history is not erased.
Missing and externally blocked evidence is stated explicitly; no record below
promotes diagnostic output into acceptance or changes the lifecycle indexed by
the master audit.

Current Sky authority is sealed source
`51d0abc0d32855a8ba32932599fedd8f59b398b7`, exact parent
`1b7d6bdaf89ebc7c9bdeae16fbde0e14079fd8a8`. It changes exactly 19 paths
with 3,318 insertions and 3,517 deletions, without changing art, assets,
protected originals, audio, workflows, or the save schema. Its exact source
bytes pass local official-Godot 4.7.1 CI in 1,404.5 seconds/all 64 trusted
probes. Run-14 supplies 20/20 local 1280×720 Mobile/Speedy frames, manifest
SHA-256 `AEAC7C72E0A3BFF992713127261DD00ED69049947DFB6723AA66365F5712DE34`,
and visual-probe SHA-256
`B9EAF5E0738CFB61CCD3E34ACFEA420AEADAB4E3ADE80B40A2CFD1F227569C6C`.
Its manifest's `source_revision` is unknown; these exact hashes bind the
manifest, embedded PNG identities, and visual-probe script, not the full source
revision. Governance-only integrated evidence head
`441adf35f7dbdeb67d36fbf1a2217b87d3040d47` preserves unchanged product source
`51d0abc0`. Exact local CI over `441adf35` exits 0 in 1,391.5 seconds/all 64;
topic Probe `31760207048` and dev Probe `31762132976` both succeed at that
exact head, and Android `31763879294` publishes its matching dev APK. Each
remote Sky subprocess still fails requested-Mobile renderer identity after 20
PASS rows, uploads PNGs only, and supplies no remote JSON/Mobile PASS. No
target-device, child, owner, or accepted-visual result is claimed.

## MA-2D-002

| Field | Value |
|---|---|
| id | `MA-2D-002` |
| title | The active project and export inventory still contain nonzero 3D migration categories. |
| rule_ids | `DL-MED-01`, `DL-MED-03`, `DL-MED-09`, `DL-QA-09` |
| domain / zone | Runtime medium and export inventory / game-wide |
| source | Game-wide audit plus the shrinking-baseline GAME2D tool and stress controls. |
| severity | P1 |
| lifecycle | `IN_PROGRESS` |
| verification | V2/V3 partial: exact inventory and no-regression controls are green, while the strict zero-debt gate is unsatisfied. |
| reproduction | At exact Sky source `51d0abc0`, run `python -B tools/audit_game_2d.py --strict` and inspect the active project/export inventory; this is a repository/runtime-structure check, so no device or aspect ratio can substitute for it. |
| child_impact | Mixed 2D/3D implementation keeps visual inconsistency, load cost, and older-device performance risk in the game used by this child. |
| evidence | Master audit sections 1 and 5.1; `tools/audit_game_2d.py`; source `51d0abc0` records 509 model/export files, 157 tracked and 352 active-untracked sidecars, 65 production-3D files, 70 probe-3D files, one 3D scene, and one 3D configuration. Regression is exact `NO_REGRESSION`, all 14 stress controls pass, and strict remains `UNSATISFIED`. |
| owner_decision | Owner decision 2026-08-09: the game-wide final authored and runtime medium is true 2D; relabeling spatial content does not satisfy it. |
| fix | Continue shrink-only conversion or retirement of active 3D sources, preserving approved 2D art, save compatibility, and protected originals. |
| surrounding_tests | GAME2D default, regression, strict, and stress; import/analyzer; relevant positive, passive, sibling, save/re-entry, teardown, and full trusted probes after each bounded conversion. |
| acceptance | All eleven GAME2D categories are zero and strict, import, focused, surrounding, and full probes pass at the same candidate. |
| closure | Open as of 2026-08-13; no zero-category result, strict pass, closure commit, device result, or acceptance date exists. |
| relationships | Parent game-wide debt for resolved `MA-DOLLS-001` and `MA-SEEK-001`; overlaps active `MA-VIS-002`, `MA-VIS-006`, and `MA-CODE-002`; documentation premise fixed by `MA-DOC-001`. |
| history | 2026-08-09: indexed from the full game-wide audit. 2026-08-12: Dolls, Seek, and bounded Opera sources reduced the baseline. 2026-08-13: true-Canvas Sky source `51d0abc0` reduces current production/probe 3D-file counts to 65/70 while the model count stays 509; lifecycle remains `IN_PROGRESS` because strict is unsatisfied. |

## MA-DOC-002

| Field | Value |
|---|---|
| id | `MA-DOC-002` |
| title | The sealed exhaustive document ledger required exact-head full-local and remote verification before closure. |
| rule_ids | `DL-AUTH-01`, `DL-AUTH-02`, `DL-AUTH-04`, `DL-MED-10` |
| domain / zone | Documentation authority / repository-wide Markdown |
| source | Repository documentation audit and comparison of tracked Markdown paths with `design/05_DOC_LEDGER.md`. |
| severity | P1 |
| lifecycle | `VERIFIED_FIXED` |
| verification | V2/V3 verified at exact CHG-023 maintenance head `51887315`: the Git-declared inventory, one-row-per-path ledger, 36 focused tests, six mutation controls, exact official-Godot full-local suite, and exact-head remote Probe Suite are green. |
| reproduction | From exact verification checkpoint `51887315`, run `python -B tools/audit_document_authority.py`, its focused unit suite, and stress mode; independently enumerate the Git-declared `*.md` inventory and compare each path with `design/05_DOC_LEDGER.md`. Device and aspect ratio are not applicable. |
| child_impact | Conflicting or stale instructions can steer repairs toward the wrong art, mechanics, or engine baseline and indirectly degrade the child's game. |
| evidence | Contiguous CHG-029 sources `5ed0c75460c9afd5ab574ff2c4a907c1075964f0` (parent `18b6150c01e1587100dca97c85ebad03f369825a`) and `7eb945957776ab3458a9de71c8be9937e2354720` (parent `5ed0c754`) establish and harden the exact 316 paths/316 rows. Exact CHG-023 verification checkpoint `51887315bd537db2d16bdafcac1bbfa808352351`, parent `7eb94595`, passes official Godot 4.7.1 `scripts/ci.sh` in 1,435.2 seconds with all 64 trusted local probes and exact-head Probe Suite run `31710377034`; its static document gate reports 36 tests, six/six stress, 316/316 inventory/ledger, and then-current 36/36 active-record parity, all green. After the two verified document findings transition terminal, the current validator reports 34 active items and retains all 36 records. |
| owner_decision | Direct owner decisions through 2026-08-09 remain controlling; no decision permits an incomplete ledger to imply authority. |
| fix | Implemented at first source `5ed0c754` and hardened at `7eb94595`: one unique ledger row per Git-declared Markdown path with exact current, historical, superseded, partial, or candidate scope, enforced by a fail-closed validator including wrapped stale-claim controls. |
| surrounding_tests | Unique-path and duplicate-row checks; relative-link and anchor checks; stale 3D/Godot-baseline rejection; Markdown table/fence validation; diff check. |
| acceptance | Every Git-declared Markdown path has exactly one resolvable row, mixed documents state exact partial-supersession scope without contradicting binding decisions, and the exact sealed commit passes local and remote authority gates. |
| closure | Verified 2026-08-13 at exact `51887315`: official Godot 4.7.1 full local exits zero after 1,435.2 seconds/all 64, and remote run `31710377034` succeeds at the same SHA after executing the document gate, exact import/analyzer, and all 63 remote trusted probe headings. |
| relationships | Supports `MA-DOC-005`; follows the authority reconciliation closed under `MA-DOC-001` and tracking repair closed under `MA-DOC-004`. |
| history | 2026-08-09: confirmed incomplete by the master audit. 2026-08-13: source `5ed0c754` expands the ledger and passes full local CI in 1,359.8 seconds/all 64; contiguous `7eb94595` hardens multiline stale-claim detection and leaves the source checkpoint `FIXED_PENDING_VERIFICATION`. Later CHG-023 maintenance head `51887315` passes exact local and remote V3 gates, moving the item to `VERIFIED_FIXED` without changing the CHG-029 source boundary. |

## MA-DOC-003

| Field | Value |
|---|---|
| id | `MA-DOC-003` |
| title | The reported off-repository journal of 36 findings cannot be verified or reconciled from repository evidence. |
| rule_ids | `DL-AUTH-02`, `DL-AUTH-03`, `DL-QA-07` |
| domain / zone | Documentation provenance / off-repository journal |
| source | Owner report recorded by the master audit; the underlying journal is unavailable in the repository. |
| severity | P1 |
| lifecycle | `BLOCKED_EXTERNAL` |
| verification | V1: the report exists, but names, contents, dates, and current applicability of the 36 entries are blocked. |
| reproduction | At current repository state, search tracked audit/design records for the asserted journal and its 36 named entries; the source cannot be reproduced because it is external, and device/aspect are not applicable. |
| child_impact | Unknown external findings may include unresolved child-safety, usability, or quality defects, while guessing their content risks unnecessary regressions. |
| evidence | Master audit section 5.1 records the claim; source file, stable IDs, entry text, provenance, and reconciliation evidence are explicitly missing. |
| owner_decision | No item-specific owner disposition exists; the report must be imported or replaced by a fresh equal-scope audit rather than assumed current. |
| fix | Obtain the original journal with provenance and reconcile each entry, or perform and retain a fresh equal-scope audit. |
| surrounding_tests | Provenance/hash review; unique-ID and lifecycle mapping; duplicate/supersession analysis; links; full relevant audit gates for any actionable imported finding. |
| acceptance | A preserved source or equal-scope replacement accounts for all 36 asserted entries and maps each to a current stable record, terminal history, or explicit non-applicability. |
| closure | Blocked as of 2026-08-13; external source, equal-scope replacement, acceptance result, commit, and date are missing. |
| relationships | May overlap any `MA-*` item; must be reconciled with `MA-DOC-002` and `MA-DOC-005` without inventing duplicates. |
| history | 2026-08-09: recorded as an external report. 2026-08-13: remains `BLOCKED_EXTERNAL`; no source evidence was supplied. |

## MA-DOC-005

| Field | Value |
|---|---|
| id | `MA-DOC-005` |
| title | The sealed complete linked finding register required exact-head full-local and remote verification before closure. |
| rule_ids | `DL-AUTH-02`, `DL-AUTH-03`, `DL-QA-07`, `DL-QA-10` |
| domain / zone | Audit governance / active master-audit findings |
| source | Master audit sections 5 and 10; section 5 rows are explicitly non-canonical indexes. |
| severity | P1 |
| lifecycle | `VERIFIED_FIXED` |
| verification | V2/V3 verified at exact CHG-023 maintenance head `51887315`: all 36 material records, exact required fields, index links, lifecycle/severity parity, rule resolution, 36 focused tests, six mutation controls, exact official-Godot full-local, and exact-head remote Probe Suite are green. |
| reproduction | From exact verification checkpoint `51887315`, run `python -B tools/audit_document_authority.py`, its focused unit suite, and stress mode; compare every material section-5 ID with this stable record path and its required fields. Device and aspect ratio are not applicable. |
| child_impact | Repairs can start from abbreviated or ambiguous evidence, increasing the chance of changing the wrong feature in a child-specific game. |
| evidence | Contiguous CHG-029 sources `5ed0c75460c9afd5ab574ff2c4a907c1075964f0` (parent `18b6150c01e1587100dca97c85ebad03f369825a`) and `7eb945957776ab3458a9de71c8be9937e2354720` (parent `5ed0c754`) establish and harden 36 linked complete stable records. Exact CHG-023 verification checkpoint `51887315bd537db2d16bdafcac1bbfa808352351`, parent `7eb94595`, passes official Godot 4.7.1 `scripts/ci.sh` in 1,435.2 seconds/all 64 and exact-head Probe Suite run `31710377034`; its static document gate reports 36 tests, six/six stress, 316/316 inventory/ledger, and then-current 36/36 active-record parity, all green. After the two verified document findings transition terminal, the current validator reports 34 active items and retains all 36 records. |
| owner_decision | No waiver permits abbreviated index rows to serve as canonical findings; unknown evidence must be explicit. |
| fix | Implemented at first source `5ed0c754` and hardened at `7eb94595`: maintain one stable complete record for every material item, link it from the authoritative section-5 matrix/ledger, and enforce parity plus wrapped stale-claim checks with a fail-closed validator. |
| surrounding_tests | Exact 36-ID set; unique headings and IDs; exact 18 field keys; severity/lifecycle parity; resolvable `DL-*` rules; Markdown tables/fences/links; diff check. |
| acceptance | Every material section-5 item resolves to exactly one complete stable record, validators pass locally and remotely at the exact sealed commit, and the master index/ledger records the canonical path without lifecycle drift. |
| closure | Verified 2026-08-13 at exact `51887315`: official Godot 4.7.1 full local exits zero after 1,435.2 seconds/all 64, and remote run `31710377034` succeeds at the same SHA after executing the canonical-record gate, exact import/analyzer, and all 63 remote trusted probe headings. |
| relationships | Depends on `MA-DOC-002`; complements external-source reconciliation `MA-DOC-003`; does not reopen terminal index items. |
| history | 2026-08-09: gap identified. 2026-08-13: source `5ed0c754` adds 36 complete stable records and passes full local CI in 1,359.8 seconds/all 64; contiguous `7eb94595` hardens stale-claim enforcement and leaves the source checkpoint `FIXED_PENDING_VERIFICATION`. Later CHG-023 maintenance head `51887315` passes exact local and remote V3 gates, moving the item to `VERIFIED_FIXED` without changing the CHG-029 source boundary. |

## MA-VIS-002

| Field | Value |
|---|---|
| id | `MA-VIS-002` |
| title | Sky Lagoon's true-Canvas repair has exact machine integration but still lacks requested-Mobile remote visual proof, device, and accepted-visual verification. |
| rule_ids | `DL-MED-01`, `DL-LAY-01`, `DL-LAY-02`, `DL-QA-11` |
| domain / zone | Visual medium and staging / Sky Lagoon |
| source | Game-wide visual/source audit and Sky Lagoon runtime structure review. |
| severity | P1 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3/V4 local source and visual evidence plus exact integrated machine/build evidence: the promenade is an owned true-Canvas stage, local source-byte suites, topic/dev Probe runs, and matching APK are green. Both current remote Sky subprocesses fail requested-Mobile renderer identity; target-device, child, owner, and accepted-visual verification are missing. |
| reproduction | From exact source `51d0abc0`, run the Sky focused/surrounding probes and `scripts/probe_sky_lagoon_art.gd` under official Godot 4.7.1 Mobile/Speedy at 1280×720. Inspect the live `CanvasLayer` -1, `Node2D`/`Sprite2D` layer stack, `Camera2D`, 6144×2048 master coordinates, 6×2 backdrop tiles, real rear/foreground parallax, and the ordered arrival/route/animal/playground/action/castle/day/night frames. Target-phone and M11 captures are missing. |
| child_impact | Flat staging weakens depth, route readability, and visual quality in a major area of the child's game. |
| evidence | Master audit sections 1.4, 4, and 5.1. Source `51d0abc0`, exact parent `1b7d6bda`, changes 19 paths with +3,318/-3,517 and introduces no art/asset/workflow/save-schema change. The exact source bytes pass official-Godot full local CI in 1,404.5 seconds/all 64. Run-14 is 20/20 PASS under local official Godot 4.7.1 Mobile/Speedy at 1280×720, with manifest SHA-256 `AEAC7C72E0A3BFF992713127261DD00ED69049947DFB6723AA66365F5712DE34` and current visual-probe SHA-256 `B9EAF5E0738CFB61CCD3E34ACFEA420AEADAB4E3ADE80B40A2CFD1F227569C6C`; those hashes bind the manifest/PNGs and visual-probe script, not the full source revision, which remains `unknown`. Human adversarial review accepts the local evidence as an approval candidate, not owner/device/art acceptance. Governance-only head `441adf35` preserves the product source, passes exact local CI in 1,391.5 seconds/all 64, topic/dev Probe runs `31760207048`/`31762132976` with 63/63 remote loops and zero hard failures, and Android `31763879294`. Each remote Sky diagnostic requests Mobile, misses `VK_KHR_surface`, falls back through llvmpipe to `gl_compatibility`, prints 20 PASS rows plus summary `20/20/20/20` with zero failed/skipped rows, then exits 1 on `GLOBAL`/`RESULT`; only PNGs upload, with no remote JSON/Mobile PASS. Historical `7391c53c`/`31728755204` remains earlier failed-renderer evidence. |
| owner_decision | Owner decision 2026-08-09 requires game-wide true 2D; `Sprite3D`, `SideScrollStage`, or filename-only relabeling cannot close the finding. |
| fix | Preserve the owned Canvas implementation and close only the missing requested-Mobile remote Sky proof, target-device, child, owner, and accepted-visual gates; repair any concrete failure without restoring spatial fallback or changing protected/approved art. |
| surrounding_tests | Seam and per-screen coverage; unique pixel ownership; per-card occlusion; touch/world alignment; overdraw and Speedy budget; entry/exit/re-entry; sibling Lagoon routes; Mobile captures and device run. |
| acceptance | True Canvas differential layers pass seams, ownership, overdraw, touch, runtime visual review, and target-device review with no spatial fallback. |
| closure | Pending as of 2026-08-13. The layered implementation, local candidate, exact integrated machine runs, and matching APK exist through `441adf35`, but requested-Mobile remote Sky proof, target-device result, owner/accepted-visual review, closure commit, and date are missing. |
| relationships | Contributes to `MA-2D-002` and `MA-VIS-006`; evidence quality is constrained by `MA-VIS-003` and `MA-VIS-004`. |
| history | 2026-08-09: confirmed as a mural-layer defect. 2026-08-13: predecessor runs through `e6edf559` retain 21 OK/44 FAIL history, and source `7391c53c` plus run `31728755204` retain the earlier failed remote `gl_compatibility` diagnostic. Sealed source `51d0abc0` replaces the spatial promenade with true Canvas and passes the exact local source-byte and run-14 gates; integrated `441adf35` adds exact local/topic/dev machine and APK evidence while retaining a failed remote renderer proof. Lifecycle moves from `CONFIRMED_OPEN` to `FIXED_PENDING_VERIFICATION`, not closed. |

## MA-VIS-003

| Field | Value |
|---|---|
| id | `MA-VIS-003` |
| title | Source-average saturation flags for Fairy and Lagoon do not yet establish a rendered-state art defect. |
| rule_ids | `DL-VIS-08`, `DL-QA-03`, `DL-QA-07`, `DL-QA-11` |
| domain / zone | Visual hierarchy / Fairy and Sky Lagoon |
| source | Reproduced source-average visual diagnostics plus audit interpretation. |
| severity | P1 |
| lifecycle | `REPORTED_UNCONFIRMED` |
| verification | V1 with `REVIEW_OPEN`: numeric source averages reproduce, but state-local Canvas/HUD/runtime/device evidence is absent. |
| reproduction | Run the current visual diagnostic on audited sources, then compare a true state-local Mobile 1280×720 composite for Fairy and Lagoon; the second step and target-device confirmation are missing. |
| child_impact | A real hierarchy problem could hide objectives, but acting on this weak metric could unnecessarily recolor approved child-recognizable art. |
| evidence | Master audit sections 4 and 5.1; source-average flags reproduce; Fairy is likely a false positive or coverage gap and Lagoon remains only a plausible hierarchy risk. |
| owner_decision | Approved art must not be regenerated or recolored merely to satisfy a global average; owner acceptance controls visual identity. |
| fix | Capture and assess true local Canvas composites with HUD/viewport context; change art only if that evidence confirms a named defect. |
| surrounding_tests | Visual-audit stress controls; decoded-alpha/occlusion; focus/objective visibility; sibling states; Mobile aspect variants; target-device and owner review. |
| acceptance | Each flagged zone receives authoritative state-local evidence that either confirms a bounded repair and passes review or documents the diagnostic as non-defective. |
| closure | Open/unconfirmed as of 2026-08-13; authoritative composites, device/owner decision, result, commit, and date are missing. |
| relationships | Shares missing live evidence with `MA-VIS-006`; Lagoon interpretation relates to `MA-VIS-002` and `MA-VIS-004`. |
| history | 2026-08-09: source metric reproduced and finding kept unconfirmed. 2026-08-13: no accepted runtime evidence; lifecycle remains `REPORTED_UNCONFIRMED`. |

## MA-VIS-006

| Field | Value |
|---|---|
| id | `MA-VIS-006` |
| title | The fail-closed visual audit lacks accepted live evidence for every applicable player-visible state. |
| rule_ids | `DL-QA-03`, `DL-QA-07`, `DL-QA-10`, `DL-QA-11` |
| domain / zone | Visual verification / game-wide player-visible states |
| source | Fresh-runtime visual-contract audit and current visual report. |
| severity | P1 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V2/V3 contract plus V4 local Sky candidate and exact integrated machine/build evidence: contract/stress behavior is approved and run-14 verifies the repaired Sky stage locally, but the current remote Sky renderer proof fails and the game-wide report, missing live adapters, and external/accepted-visual evidence remain unresolved. |
| reproduction | Run the fresh-runtime visual audit at current source and the exact `51d0abc0` Sky probe under Godot 4.7.1 Mobile 1280×720. Inspect every applicable adapter and all twenty ordered Sky frames; missing live adapters/captures remain unresolved, and device/owner acceptance is absent. |
| child_impact | Unseen cutoff, occlusion, hierarchy, or stale-art defects may reach the child despite green logic probes. |
| evidence | `audit/visual_design_report.json` and `.md`; global totals remain 16 FAIL, 17 REVIEW_OPEN, two MANUAL_OPEN, 86 COVERAGE_GAP, 32 PASS, and 94 NOT_APPLICABLE. Exact source bytes at `51d0abc0` pass full local in 1,404.5 seconds/all 64. Run-14 produces 20/20 ordered 1280×720 Mobile/Speedy captures with zero failures/skips/global failures, manifest SHA-256 `AEAC7C72E0A3BFF992713127261DD00ED69049947DFB6723AA66365F5712DE34`, visual-probe SHA-256 `B9EAF5E0738CFB61CCD3E34ACFEA420AEADAB4E3ADE80B40A2CFD1F227569C6C`, isolated save restoration, and two independent human approvals of the local candidate. Integrated `441adf35` passes exact local/topic/dev machine gates and has Android `31763879294`, but each remote Sky subprocess falls back to `gl_compatibility`, exits 1 after its 20 PASS rows, and uploads PNGs only with no JSON/Mobile PASS. This does not close game-wide gaps or grant remote/device/owner/accepted-visual authority. Historical source `7391c53c` retains the earlier remote renderer failure. |
| owner_decision | The accepted fail-closed contract from `3b7a7e66` and `fea916a8` must remain; missing evidence cannot be converted to PASS. |
| fix | Implement closed live-state adapters and same-process captures, then resolve every applicable failure, review, manual item, and coverage gap. |
| surrounding_tests | Visual stress-first suite; source/Git closure; immutable capture checks; per-target occlusion and touch; positive/negative/passive/sibling states; teardown/re-entry; Mobile aspects and device review. |
| acceptance | Every applicable item has accepted current live evidence and no unresolved FAIL, REVIEW_OPEN, MANUAL_OPEN, or COVERAGE_GAP remains. |
| closure | Open as of 2026-08-13. The Sky product slice now has a locally approved candidate plus exact machine/build integration, but global unresolved totals are nonzero and no requested-Mobile remote Sky PASS, all-applicable-pass result, device/owner acceptance, or closure date exists. |
| relationships | Contract mechanics closed under `MA-VIS-005`; active evidence gaps affect `MA-VIS-002`, `MA-VIS-003`, `MA-VIS-004`, and Opera visual findings. |
| history | 2026-08-09: indexed as the fail-closed evidence gap. 2026-08-13: report remains 16/17/2/86/32/94. Historical source `7391c53c` exposed bounded Sky defects and a failed remote renderer step; source `51d0abc0` repairs that product slice locally, while the broader finding remains `CONFIRMED_OPEN`. |

## MA-VIS-007

| Field | Value |
|---|---|
| id | `MA-VIS-007` |
| title | Interactive foreground sprites can duplicate baked background objects or expose blurred placeholder holes left by the extraction pipeline. |
| rule_ids | `DL-LAY-03`, `DL-LAY-04`, `DL-LAY-05`, `DL-QA-01`, `DL-QA-03`, `DL-QA-07`, `DL-QA-11` |
| domain / zone | Visual ownership and restoration / game-wide backgrounds with interactive cards |
| source | Owner's repeated two-bathtub report, current Bubble Bath runtime/source reproduction, Castle V4 source-ownership manifests, background builders, and parallel game-wide scrub begun 2026-08-29. |
| severity | P1 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3/V4 exact local plus human multi-review; external and integration evidence open. The game-wide ownership inventory is dispositioned, seven Castle and two Opera backgrounds are regenerated as complete full frames, the fail-closed ownership/generator/frame gates pass, all 96 retained V4 frames have been reviewed against the exact runtime underlay, exact Godot 4.7.2 Mobile dirty/clean bathroom captures each show one bathtub, and the complete local CI suite exits zero. Exact integrated `dev`, target-device, child, and owner acceptance remain open. |
| reproduction | In Bubble Bath, compare the retired lower-left and lower-right shell-basket card footprints with the former background tiles and generator inputs, then enter the Day One dirty and clean states. For the systemic variant, run each extracted Castle V4 object through every authored frame and inspect the uncovered ownership mask against its healed room plate; scanline interpolation plus Gaussian blur leaves a smeared hole even though the existing numeric duplicate threshold passes. Repeat the pairing audit for every non-Castle environment and overlay. |
| child_impact | A four-year-old sees extra fixtures, ghost silhouettes, or obvious smeared holes and cannot reliably tell which object is real or tappable; repeated topic-only fixes also leave the production build unchanged. |
| evidence | The bathroom branch was eight commits ahead of `dev` while `dev` had advanced independently, proving the earlier fix was not production-visible. The current repair retires both false shell-basket cards from runtime and deterministic generation, heals both baked footprints, preserves originals and provenance, and produces passing exact-4.7.2 Mobile screenshots with one bathtub in dirty and clean states. Castle scrub identifies 39 active interactive sprites and 12 static foreground cards over seven blur-filled room plates; all seven room builders use `_clean_plate` scanline interpolation plus `GaussianBlur(2.5)`, and multiple authored frames expose the placeholder fills. The non-Castle scrub confirms the painted Detective crown and identifies Nursery's painted bottle row beneath its live FEED bottle overlay; the remaining inspected environments are clean or intentional. |
| owner_decision | Owner direction 2026-08-29 makes this a high-priority master-audit sub-branch and requires a series of subagents to scrub and repair every incidence using the same background-regeneration protocol. Approved/protected originals remain immutable, existing suitable art is reused first, and human visual acceptance cannot be inferred from a machine check. |
| fix | Maintain one exhaustive ownership register. For every confirmed pairing, preserve the original, remove the foreground object from one full clean background plate, regenerate only the irreducible missing pixels when reuse cannot meet quality, derive runtime tiles by whole-canvas normalization, retain the interactive object once as an owned Canvas card, and remove every stale builder/manifest/runtime fallback that can recreate the duplicate or blur hole. |
| surrounding_tests | Registry completeness and hash drift; generator check mode; duplicate-card negatives; source-mask/background residual and placeholder-texture negatives; every authored frame's exposed mask; tile seams and per-screen coverage; runtime dirty/clean/sibling states; passive, touch, save/re-entry, teardown; exact Godot 4.7.2 import/analyzer/focused/full probes; Mobile capture; device, child, owner, and exact-`dev` integration evidence. |
| acceptance | Every runtime background/interactive-card pairing is dispositioned; no confirmed or latent pairing retains duplicate pixels or an exposed procedural placeholder; all generated repairs have complete source/prompt/hash/license provenance; the detector proves its negative controls; exact 4.7.2 Mobile captures and focused/full gates pass at one integrated `dev` head; required device, child, and owner visual gates are explicitly recorded rather than implied. |
| closure | Fixed pending verification as of 2026-08-29. The seven Castle clean plates and two Opera repairs are source/hash bound, deterministic build checks and the fail-closed ownership detector are green, 96 retained interaction frames pass exact-underlay review, and the complete exact-4.7.2 local suite exits zero. Integration to `dev` plus target-device, child, and owner visual acceptance remain explicitly open; no machine or agent review is recorded as owner acceptance. |
| relationships | Subordinate workstream of `MA-VIS-006`; enforces the unique-pixel ownership and per-card occlusion rules implicated by `MA-VIS-002`; includes the product repair already indexed as `MA-OPERA-002`; exact production visibility also depends on `MA-RELEASE-001`. |
| history | 2026-08-29: repeated owner report reproduced. Root causes include an abandoned topic branch, removal of only one of two false foreground cards, two baked/blurred background footprints, regeneration tooling that could restore the defect, node-only probes, a runtime route allow-list that rejected the repaired route, and cwd-relative review tooling that could inspect stale branches or composite against an obsolete plate. Both bathroom footprints were repaired and exact 4.7.2 dirty/clean captures passed. Three parallel scrubs dispositioned the game, drove full-frame regeneration of seven Castle plates plus Opera Detective and Nursery, retired the incomplete duplicate tent-flap card, repaired the cupboard's incomplete rest frame, and independently reviewed all 96 retained V4 frames against exact worktree/runtime paths. The complete exact-4.7.2 local suite exits zero; lifecycle advances to `FIXED_PENDING_VERIFICATION` while exact `dev` and external acceptance remain open. |

## MA-PLAY-001

| Field | Value |
|---|---|
| id | `MA-PLAY-001` |
| title | No fresh-save child-visible route has proved entry, exit, and re-entry for every visible destination without debug shortcuts. |
| rule_ids | `DL-AGE-01`, `DL-AGE-06`, `DL-SAVE-04`, `DL-QA-05` |
| domain / zone | Progression and navigation / whole playable world |
| source | Game-wide reachability audit and absence of an end-to-end golden-path artifact. |
| severity | P1 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1/V3 partial: bounded routes and probes exist, but complete visible-world proof is missing. |
| reproduction | Start a genuinely fresh save on the exact candidate, use only visible one-finger routes and spoken/visual cues at phone aspect, enter/leave/re-enter every visible destination, and restart from save; no complete device session exists. |
| child_impact | The child may become trapped, miss content, or require adult/debug navigation. |
| evidence | Master audit sections 5.1 and 12. Source `51d0abc0` strengthens real Sky Reef/Castle/Northern/Galaxy/Ember/kart route, return, re-entry, save-state, and teardown probes, but a complete no-cheat world traversal, device video, voice/touch trace, and save replay are still missing. |
| owner_decision | The game is for a non-reader using one finger, with no lost progress or fail states; visible and spoken navigation is binding. |
| fix | Repair only routes that fail the end-to-end traversal, adding visible pointers and exact spoken cues without hidden debug calls. |
| surrounding_tests | Positive route traversal; proximity/passive negatives; sibling destinations; back/pause/focus loss; save/restart/re-entry; touch and voice; teardown; full probes. |
| acceptance | A fresh-save exact-candidate device session reaches and re-enters every visible destination without cheats, reading, traps, or progress loss. |
| closure | Open as of 2026-08-13; full route matrix, target-device recording, child observation, closure commit, and date are missing. |
| relationships | External comprehension closure overlaps `MA-CHILD-001`; exact voice gaps overlap `MA-ACCESS-001` and `MA-ACCESS-003`; release gate under `MA-RELEASE-001`. |
| history | 2026-08-09: confirmed missing game-wide proof. 2026-08-13: bounded route evidence improved, but lifecycle remains `CONFIRMED_OPEN`. |

## MA-ACCESS-001

| Field | Value |
|---|---|
| id | `MA-ACCESS-001` |
| title | Some required objectives still lack an authorized exact spoken cue or an independently sufficient diegetic alternative. |
| rule_ids | `DL-AGE-01`, `DL-SND-01`, `DL-SND-03`, `DL-QA-07` |
| domain / zone | Accessibility and voice / game-wide objectives |
| source | Objective-to-voice audit and protected-recording inventory. |
| severity | P1 |
| lifecycle | `BLOCKED_EXTERNAL` |
| verification | V1: missing exact cue coverage is identified; recording, listening, and child evidence are external. |
| reproduction | On the audited candidate, enter each flagged objective with captions unread and audio enabled on the target phone; observe that the exact action is not spoken. Exact device matrix is missing. |
| child_impact | A non-reading four-year-old may not know what to do without adult help. |
| evidence | Master audit section 5.1 and design voice rules; exact authorized recordings and complete device/child playback evidence are missing. |
| owner_decision | Protected family voices may not be modified or substituted without owner authorization. |
| fix | Obtain authorized exact recordings, or implement an independently sufficient spoken/diegetic cue approved by the owner. |
| surrounding_tests | Exact key/file routing; queue order; voice ducking; captions as supplemental only; music-off/mono; passive no-progress; sibling objectives; device listening and child comprehension. |
| acceptance | Every required objective communicates the exact action without reading, with authorized identity, correct playback, device intelligibility, and observed child comprehension. |
| closure | Blocked as of 2026-08-13; recordings/approved alternative, device/child evidence, commit, and closure date are missing. |
| relationships | Includes specific unresolved cases `MA-ACCESS-002` and `MA-ACCESS-003`; audio mix evidence also relates to `MA-AUDIO-001`. |
| history | 2026-08-09: blocked exact-voice coverage indexed. 2026-08-13: no authorization or substitute evidence supplied; lifecycle unchanged. |

## MA-ACCESS-002

| Field | Value |
|---|---|
| id | `MA-ACCESS-002` |
| title | Lamba's current semantic role still plays protected recordings that call the character a bunny-fish. |
| rule_ids | `DL-SND-03`, `DL-SND-05`, `DL-VIS-06`, `DL-QA-06` |
| domain / zone | Character identity and voice / Lamba interactions |
| source | Semantic-role and protected-audio key audit. |
| severity | P1 |
| lifecycle | `BLOCKED_EXTERNAL` |
| verification | V1: the role-to-recording mismatch is confirmed; authorized replacement and listening evidence are absent. |
| reproduction | Trigger Lamba's current objective/interaction on the audited build with voices enabled and compare the spoken noun with the current visual/semantic role; target-device listening is not yet recorded. |
| child_impact | Conflicting name and appearance can confuse the child about the character and objective. |
| evidence | Master audit section 5.1; current semantic mapping and legacy “bunny-fish” protected recordings; owner-approved replacement file, exact key proof, and device capture are missing. |
| owner_decision | Protected voice originals must not be edited, recompressed, or substituted; owner-approved re-record/re-render is required. |
| fix | Add an authorized new recording and route the exact key to it, preserving originals and provenance. |
| surrounding_tests | Exact voice-key routing; protected-original hashes; queue/ducking; captions; old-key negative; sibling character voices; mono/device listening; child comprehension. |
| acceptance | Current Lamba visuals and semantics match an owner-approved exact recording on device, with no legacy mismatch reachable. |
| closure | Blocked as of 2026-08-13; owner-approved recording, implementation, device listening, commit, and date are missing. |
| relationships | Specific child of `MA-ACCESS-001`; identity authority also relates to visual rules and `MA-AUDIO-001`. |
| history | 2026-08-09: mismatch confirmed and externally blocked. 2026-08-13: protected audio remains unchanged and finding remains `BLOCKED_EXTERNAL`. |

## MA-ACCESS-003

| Field | Value |
|---|---|
| id | `MA-ACCESS-003` |
| title | Seek lacks an exact protected Evie recording that tells the child to tap the wiggly tree. |
| rule_ids | `DL-AGE-01`, `DL-SND-01`, `DL-SND-05`, `DL-QA-05` |
| domain / zone | Objective voice and comprehension / Seek |
| source | Seek repair audit, protected Evie voice inventory, and current visual cue review. |
| severity | P1 |
| lifecycle | `BLOCKED_EXTERNAL` |
| verification | V1/V3 partial: visual wiggle/U-cue/peek and a generic Evie hide-and-seek line exist; exact objective speech and external comprehension evidence do not. |
| reproduction | Enter Seek on the current runtime at phone aspect with no adult instruction, wait for the target tree cue, and listen for the exact action; no recording says “tap the wiggly tree.” |
| child_impact | The child may see motion but still not understand the required tap without adult explanation. |
| evidence | `scripts/games/seek.gd`, Seek art/runtime repair evidence, protected Evie voice inventory, and master audit section 5.1; exact authorized line, device listening, and child session are missing. |
| owner_decision | Protected Evie recordings cannot be altered or synthesized without owner authorization. |
| fix | Record and add an authorized exact Evie objective cue, then route it through the current visual prompt without changing protected originals. |
| surrounding_tests | Exact key/file/hash; queue and ducking; visual-pointer synchronization; passive no-win; wrong-tree recovery; replay/re-entry; mono/device listening; child comprehension. |
| acceptance | The exact Evie cue plays at the actionable tree, remains intelligible on device, and an observed child acts without reading or adult instruction. |
| closure | Blocked as of 2026-08-13; authorized exact line, device/child evidence, closure commit, and date are missing. |
| relationships | Specific child of `MA-ACCESS-001`; Seek runtime medium is closed under `MA-SEEK-001`, which this voice gap does not reopen. |
| history | 2026-08-09: exact speech gap retained separately from the Seek visual repair. 2026-08-13: remains `BLOCKED_EXTERNAL`. |

## MA-TOUCH-001

| Field | Value |
|---|---|
| id | `MA-TOUCH-001` |
| title | Held travel and medallion input lacks recorded real-phone hold, drag, multitouch, and focus-loss verification. |
| rule_ids | `DL-UI-01`, `DL-UI-04`, `DL-UI-05`, `DL-QA-04` |
| domain / zone | Touch input / held travel and medallion path |
| source | Touch-path implementation/probe audit and missing target-phone evidence. |
| severity | P1 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3 reported: implementation-level repair is reported green; target-phone V5 evidence is missing. |
| reproduction | On the exact candidate installed on the intended three-to-four-year-old Android phone, hold to travel, drag through direction changes, introduce a second finger, background/focus-loss, pause, release, and resume at native aspect; no recorded run exists. |
| child_impact | Stuck ownership or lost release can make Roshan move incorrectly or trap the child in an interaction. |
| evidence | Master audit section 5.1 and source `51d0abc0`: Classic short-release behavior is scoped to the active Sky promenade, manual/keyboard/touch movement cancels stale Canvas goals and focus, pause/focus/overlay transitions clear touch ownership, and the real gear/resume signals plus 240-event churn pass focused stress. Target-phone video/input trace, native focus-loss result, and child-handed evidence are missing. |
| owner_decision | Primary play is one finger on an older Android phone; input ownership and focus-loss cleanup are binding. |
| fix | If device evidence fails, make the smallest bounded input-ownership/release cleanup repair without changing the visible one-finger grammar. |
| surrounding_tests | Press/hold/drag/release positive; second-finger negative; focus loss/pause/back; target disappearance; sibling touch routes; passive; teardown/re-entry; save unaffected. |
| acceptance | A recorded target-phone matrix passes hold, drag, multitouch rejection, focus loss, pause, release, and re-entry without stuck motion or duplicate actions. |
| closure | Pending as of 2026-08-13; target-phone result, device identifier, recording, acceptance commit, and date are missing. |
| relationships | Device gate contributes to `MA-PERF-001`, `MA-CHILD-001`, and `MA-RELEASE-001`. |
| history | 2026-08-09: implementation repair indexed as reported. 2026-08-13: `51d0abc0` strengthens the Canvas/Classic/pause input lifecycle and automated stress evidence; it remains `FIXED_PENDING_VERIFICATION` for lack of real-phone evidence. |

## MA-OPERA-001

| Field | Value |
|---|---|
| id | `MA-OPERA-001` |
| title | Chef's repaired cooking sequence lacks accepted two-aspect, target-device, and owner art verification. |
| rule_ids | `DL-INT-02`, `DL-READ-02`, `DL-QA-06`, `DL-QA-12` |
| domain / zone | Art, interaction, and acceptance / Opera Chef and Castle Kitchen entry |
| source | Chef source/runtime audit, deterministic art checks, and current valid configuration probes. |
| severity | P1 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3 partial: accepted-source pitcher, stream/fill, mitt gate, cake, and toppings are implemented and probed; V4/V5/owner evidence is incomplete. |
| reproduction | Launch Chef from its current Castle Kitchen route on runtime `09e5e356`; complete pour, mix, oven, and topping actions at 1280×720 and a second phone/tablet aspect. Target-device and owner-reviewed captures are missing. |
| child_impact | Cutoff, misleading object state, or poor touch alignment could make the cooking actions unclear despite green logic. |
| evidence | Current Chef config and deterministic art/runtime probes; master audit section 5.1. The prior cutoff/fallback/wrong-object report is not a current premise. Accepted two-aspect captures, device evidence, and owner review are missing. |
| owner_decision | The batter pitcher and current source-true cooking fiction are accepted; speculative invalid-config recovery in the sealed Castle Kitchen controller requires renewed owner visual approval. |
| fix | Preserve the current implementation and collect acceptance evidence; repair only a reproduced bounded visual/device defect. Treat speculative Castle caller hardening separately under `MA-CODE-002`. |
| surrounding_tests | Correct and wrong action; passive no-win; mitt gating; visual/touch alignment; sibling career route; voice; save/reward/replay; close/teardown/re-entry; two aspects and target device. |
| acceptance | Two accepted aspects and target-device play show complete, legible, correctly aligned cooking states, followed by owner art acceptance. |
| closure | Pending as of 2026-08-13; accepted aspect/device/owner evidence, final result, closure commit, and date are missing. |
| relationships | Invalid-config hardening is excluded and tracked by `MA-CODE-002`; release acceptance contributes to `MA-RELEASE-001`. |
| history | 2026-08-09: old Chef defect indexed. 2026-08-12: current source-true sequence and valid config confirmed. 2026-08-13: remains `FIXED_PENDING_VERIFICATION`. |

## MA-OPERA-002

| Field | Value |
|---|---|
| id | `MA-OPERA-002` |
| title | Detective's supposedly missing crown is still visibly painted into the scene source. |
| rule_ids | `DL-VIS-06`, `DL-ASSET-01`, `DL-ASSET-03`, `DL-QA-03` |
| domain / zone | Visual narrative and owned source / Opera Detective |
| source | Human review of current Detective scene evidence and source audit. |
| severity | P1 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V4 partial: the painted crown is visible in review evidence; an accepted healed source and runtime narrative capture do not exist. |
| reproduction | Enter Detective's crown-missing state on the current runtime and inspect the full Mobile 1280×720 scene; the crown remains in the painted background. Device/owner acceptance is missing. |
| child_impact | The mystery asks the child to find something that is already visible, breaking the story logic and objective comprehension. |
| evidence | Master audit section 5.1 and current Detective scene evidence; owned source provenance, healed derivative, accepted runtime capture, and owner review are missing. |
| owner_decision | Protected originals cannot be destructively modified; healing must use an owned source/derived path and retain provenance. |
| fix | Verify source ownership, create a non-destructive healed scene without the crown in the missing state, and retain the crown only in truthful reveal/payoff states. |
| surrounding_tests | Missing-state negative; reveal positive; pointer and touch alignment; passive no-win; sibling Detective phases; save/reward/replay; two-aspect capture; teardown/re-entry. |
| acceptance | Accepted source and runtime captures show the crown absent before discovery and present only at the truthful payoff, with owner/narrative approval. |
| closure | Open as of 2026-08-13; healed source, provenance, accepted captures, owner result, closure commit, and date are missing. |
| relationships | Capture completeness depends on `MA-OPERA-004` and game-wide visual evidence `MA-VIS-006`. |
| history | 2026-08-09: crown contradiction confirmed. 2026-08-13: remains `CONFIRMED_OPEN`; no accepted source repair recorded. |

## MA-OPERA-004

| Field | Value |
|---|---|
| id | `MA-OPERA-004` |
| title | The Opera capture harness has not produced accepted evidence for every career, widget, scuffle, and stress state. |
| rule_ids | `DL-QA-03`, `DL-QA-07`, `DL-QA-11`, `DL-QA-12` |
| domain / zone | Visual verification tooling / all Opera careers |
| source | Opera capture-harness audit and current diagnostic artifact review. |
| severity | P1 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: harness coverage and acceptance are incomplete; existing local and remote captures are diagnostic. |
| reproduction | Run the Opera visual capture workflow for all 13 careers and required state variants at Mobile 1280×720 plus the required second aspect; compare emitted files with the complete matrix. Accepted full-matrix output is absent. |
| child_impact | Visual cutoff, overlap, wrong state, or unreadable actions may escape review and reach the child. |
| evidence | Master audit section 5.1; 22 current local route/career captures are diagnostic, remote uploads are non-authoritative, and no accepted all-career/widget/scuffle/stress matrix exists. Historical dev-head run `31693492735` is workflow-green while its obsolete Sky diagnostic records 21 OK/44 FAIL, proving step success is not capture acceptance. The later 20/20 Sky diagnostic at `7391c53c` does not expand or accept the Opera matrix. |
| owner_decision | Diagnostic artifacts never grant authoritative visual, device, child, or owner acceptance. |
| fix | Repair the harness and state adapters so every required state produces immutable, correctly labeled, reviewable output without swallowing internal failures. |
| surrounding_tests | Expected-file manifest; missing/duplicate/stale-output negatives; exact state identity; stress/scuffle states; two aspects; touch/HUD composition; deterministic rerun; artifact provenance; teardown. |
| acceptance | The complete required matrix is freshly generated, machine-validated, human-reviewed, and explicitly accepted at required aspects without internal capture failures. |
| closure | Open as of 2026-08-13; complete accepted matrix, validator result, owner review, closure commit, and date are missing. |
| relationships | Blocks visual closure for `MA-OPERA-002`, `MA-OPERA-003`, `MA-OPERA-005`, `MA-OPERA-006`, `MA-OPERA-009`, and `MA-OPERA-012`; overlaps `MA-VIS-006`. |
| history | 2026-08-09: harness gap confirmed. 2026-08-13: exact `18b6150c` CI uploads complete as workflow steps, but its Sky output is 21 OK/44 FAIL and diagnostic. Sky source `7391c53c` later repairs only the separate Lagoon harness; the Opera matrix remains incomplete and lifecycle is unchanged. |

## MA-OPERA-009

| Field | Value |
|---|---|
| id | `MA-OPERA-009` |
| title | Boxer's five-phase Canvas implementation lacks two-aspect, target-device, child, and owner acceptance. |
| rule_ids | `DL-INT-09`, `DL-UI-04`, `DL-AGE-03`, `DL-QA-12` |
| domain / zone | Career gameplay and touch / Opera Boxer |
| source | Boxer specialist implementation, focused probes, and current authority audit. |
| severity | P1 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3 partial: five phases, two gloves, one-finger sequence, no-loss behavior, passive rejection, cleanup, and save bit are probed; external evidence is missing. |
| reproduction | Launch Boxer from Stuffie Playroom on runtime `09e5e356`; complete all five phases with one finger, then test optional multitouch, passive play, close, and re-entry at 1280×720 and a second target aspect. Device/child/owner runs are absent. |
| child_impact | Touch ambiguity, poor framing, or unclear gestures could make the repaired activity frustrating on the child's actual device. |
| evidence | Current Boxer specialist and focused/full-local/exact-head machine evidence; master audit section 5.1. Remote captures remain diagnostic. Two-aspect, device, child, and owner evidence is missing. |
| owner_decision | Friendly no-loss one-finger play and current integrated Boxer remain authority; Boxer V2 is an unmerged documentation proposal and cannot silently supersede runtime. |
| fix | Preserve the integrated specialist, collect external evidence, and make only bounded defects found by that review; evaluate V2 separately before changing authority. |
| surrounding_tests | One-finger positive; optional second finger; wrong/passive no-win; touch ownership; focus/pause/close; save/reward/replay; sibling careers; teardown/re-entry; performance and two aspects. |
| acceptance | Both aspects and target device pass touch/performance, an observed child understands the sequence, and the owner accepts identity/style. |
| closure | Pending as of 2026-08-13; two-aspect/device/child/owner evidence, accepted result, closure commit, and date are missing. |
| relationships | Visual capture depends on `MA-OPERA-004`; release gate under `MA-RELEASE-001`; Boxer V2 remains non-authoritative. |
| history | 2026-08-09: specialist repair recorded. 2026-08-13: current runtime is machine-green, but lifecycle remains `FIXED_PENDING_VERIFICATION`. |

## MA-OPERA-010

| Field | Value |
|---|---|
| id | `MA-OPERA-010` |
| title | Opera's unified Canvas lifecycle lacks authoritative Mobile, device, child, and owner acceptance. |
| rule_ids | `DL-INT-07`, `DL-INT-10`, `DL-SAVE-03`, `DL-QA-12` |
| domain / zone | Runtime lifecycle / Opera entry, Racer, close, suspend, and re-entry |
| source | Commit `e2c25878`, focused lifecycle probes, full local CI, and exact-head remote runs. |
| severity | P1 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3 full local plus exact-head remote: machine lifecycle evidence is green; visual/device/child/owner acceptance is incomplete. |
| reproduction | From ordinary unforced and display entry on the audited runtime, start Opera and Racer, idle, act, win, close, suspend/resume, leave, and re-enter; verify the same Canvas controller and no external kart. Required device/child review is absent. |
| child_impact | A hidden alternate engine or broken cleanup could cause inconsistent play, stuck overlays, or lost reward state. |
| evidence | `e2c25878`; exact local Godot 4.7.1 lifecycle suite; run `31661887863` at `e0677ae4`; successor run `31686380560` at `9befc0f8`; captures are diagnostic and external acceptance remains missing. |
| owner_decision | Ordinary unforced, display, and device entry must converge on the true-Canvas Opera implementation; real/external kart routing is not accepted. |
| fix | Preserve the unified lifecycle and obtain authoritative acceptance; repair only a reproduced lifecycle or presentation defect without restoring an alternate engine. |
| surrounding_tests | Startup variants; Racer; idle/passive; reward; pause/focus/suspend; close; save/restart; teardown weakrefs; re-entry; sibling careers; Mobile/device/child review. |
| acceptance | Authoritative Mobile captures plus device, child, and owner sessions confirm one Canvas lifecycle with correct cleanup, rewards, and re-entry. |
| closure | Pending as of 2026-08-13; machine gates are green, but authoritative visual/device/child/owner evidence, closure commit, and date are missing. |
| relationships | Implemented with boss retirement `MA-OPERA-011`; current room distribution is `MA-OPERA-012`; rollback is `CHG-026`. |
| history | 2026-08-12: unified lifecycle committed and local/remote machine-verified. 2026-08-13: successor exact-head remote remains green; lifecycle stays `FIXED_PENDING_VERIFICATION`. |

## MA-OPERA-011

| Field | Value |
|---|---|
| id | `MA-OPERA-011` |
| title | The retired Opera bosses and stable save tombstones lack authoritative visual, device, child, and owner acceptance. |
| rule_ids | `DL-INT-13`, `DL-SAVE-01`, `DL-SAVE-06`, `DL-QA-12` |
| domain / zone | Content retirement and save compatibility / Opera bosses |
| source | Commit `e2c25878`, migration/reward/passive probes, save inspection, and exact-head CI. |
| severity | P1 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3 full local plus exact-head remote: removal and compatibility are machine-green; external acceptance is missing. |
| reproduction | Load fresh and legacy saves on the audited runtime; inspect Opera cards, gates, completion, voice/music routing, and slots 4/9/14 through win, suspend, leave, restart, and re-entry. Device/owner review is absent. |
| child_impact | A reachable cut boss could reintroduce unwanted content, while incorrect migration could lose or miscount the child's progress. |
| evidence | `e2c25878`; raw-preserving tombstones `0x4210`; live completion mask `0xBDEF`; effective progress 0–13; focused/full-local/exact-head evidence. External acceptance remains missing. |
| owner_decision | Curtain Dragon, Shadow Phantom, and Midnight Maestro are cut from reachable product; stable 16-slot save compatibility must remain. |
| fix | Preserve removal and tombstones; obtain external acceptance and repair only a reproduced route/migration defect without deleting save keys or reintroducing bosses. |
| surrounding_tests | Fresh/legacy/future saves; raw-bit preservation; reward counts; passive; voice/music negative; cards/routes negative; suspend/leave/restart/re-entry; sibling careers; device/owner review. |
| acceptance | No cut boss is reachable or required, legacy progress is preserved exactly, and authoritative visual/device/child/owner evidence accepts the result. |
| closure | Pending as of 2026-08-13; machine evidence is green, but external acceptance, closure commit, and date are missing. |
| relationships | Coupled with `MA-OPERA-010`; distribution `MA-OPERA-012` must not recreate a hidden route; rollback is `CHG-026`. |
| history | 2026-08-12: bosses retired with tombstones and machine verification. 2026-08-13: exact-head successor evidence green; lifecycle unchanged. |

## MA-OPERA-012

| Field | Value |
|---|---|
| id | `MA-OPERA-012` |
| title | The thirteen Castle-room career routes pass current machine/build gates but still lack external acceptance, and route cards obscure Roshan. |
| rule_ids | `DL-INT-12`, `DL-READ-05`, `DL-UI-03`, `DL-QA-12` |
| domain / zone | Navigation, composition, and release evidence / Castle rooms and all Opera careers |
| source | Runtime commit `09e5e356`, probe repair `ff068db`, local suites, diagnostic captures, historical Probe Suite runs, exact `441adf35` topic/dev Probe runs `31760207048`/`31762132976`, and exact-head Android dev run `31763879294`. |
| severity | P1 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3 full local plus exact-head remote and V4 diagnostic; external open. Runtime and readiness gates are green, while captures and external acceptance are not. |
| reproduction | Install the exact `441adf35` APK from Android run `31763879294` before device testing. Launch each of 13 careers only from its assigned Castle room, return to that room, test save/reward/pause/re-entry, and inspect nine route screens at native Mobile aspect. The prior 154×154 lower-center-card diagnostics obscure Roshan's lower body/tail; accepted device review is still missing. |
| child_impact | The new routes remove a reading-heavy hub, but card occlusion can hide Roshan and external gaps leave child discovery and phone usability unproved. |
| evidence | Runtime full local: 1463.4 seconds/64 probes; `ff068db` full local: 1379.3 seconds/64; pre-fix run `31678156887` remains red from four-frame reveal sampling. Historical e6 and `7391c53c` preserve bounded remote evidence, including the latter's failed Sky renderer subprocess. Product source `51d0abc0` changes no Opera behavior and passes full local in 1,404.5 seconds/all 64. Governance-only integrated head `441adf35` preserves it and passes exact local CI in 1,391.5 seconds/all 64 plus topic/dev runs `31760207048`/`31762132976` with 63/63 remote loop, zero hard failures, and music 42/42. Android `31763879294` publishes the exact raw-checkout/package-source `441adf35` APK (596,033,220 bytes; SHA-256 `f04d0fef3b9bf097aa5b07e56e5726a1db9ff37e4be6ce35b495e31b9e4a72d8`). |
| owner_decision | Owner direction 2026-08-02 assigns all thirteen careers to exact thematic Castle rooms, makes Movie Lounge Racer's sole home, and forbids a central or hidden all-career lobby. |
| fix | Preserve exact room ownership and direct return; reposition/compose route cards without shrinking child-safe targets; complete external review on the matching current APK. |
| surrounding_tests | Exact room mapping; hidden/off-room negatives; launch/return; save/reward/tombstones; voice/pointer; passive; pause/layers/focus; teardown/re-entry; sibling rooms; two aspects; APK/device/child/owner. |
| acceptance | A matching current APK and machine gates are green; route cards keep large targets without obscuring Roshan; phone/M11, child, owner, voice/listening, strict-2D, and authoritative visual gates pass. |
| closure | Pending as of 2026-08-13; exact integrated machine runs and matching APK exist at `441adf35`. Phone/M11, child, owner, voice/listening, strict-2D, and accepted-visual evidence are missing, remote Sky renderer diagnostics remain failed, and P2 card composition is unresolved. |
| relationships | Builds on `MA-OPERA-010` and `MA-OPERA-011`; visual capture gap `MA-OPERA-004`; release gate `MA-RELEASE-001`; rollback `CHG-027`. |
| history | 2026-08-12: `09e5e356` implemented exact room routes and local evidence. 2026-08-13: `ff068db` repaired readiness sampling; e6 and `7391c53c` preserve predecessor machine/build history. Current integrated head `441adf35` preserves unchanged `51d0abc0` Opera behavior and adds local/topic/dev machine plus APK evidence; all external/visual gates remain open. 2026-08-26: owner commits `0277071f` and `9a1754c1` (2026-08-25) add `scripts/opera_house_venue_2d.gd`, a true-2D three-floor Opera House venue serving as the Opera Hall room interior that hosts only its three resident careers through invisible painted portal regions with no card grid or all-career menu; the no-central-lobby premise is preserved, the venue is recognized as the newest owner direction, and the lifecycle is unchanged pending the same external verification. |

## MA-PERF-001

| Field | Value |
|---|---|
| id | `MA-PERF-001` |
| title | No exact-release target-device matrix establishes frame time, hitches, memory, thermal behavior, load time, or touch latency. |
| rule_ids | `DL-PERF-01`, `DL-PERF-02`, `DL-PERF-07`, `DL-QA-04` |
| domain / zone | Performance / whole game on older Android phone and Lenovo Tab M11 |
| source | Performance audit and absence of U0 device measurements for the current candidate. |
| severity | P1 |
| lifecycle | `BLOCKED_EXTERNAL` |
| verification | V0: no current exact-candidate target-device performance matrix exists. |
| reproduction | Install and verify the exact `441adf35` APK from Android run `31763879294` on the intended older Android phone and Lenovo Tab M11, then run representative cold load, traversal, Castle/Opera, Lagoon, combat, particles, pause/re-entry, and touch-latency traces at native aspect. Current measurements are missing. |
| child_impact | Hitches, heat, memory pressure, slow loads, or delayed touch can make the game unusable for its only intended player. |
| evidence | Source `51d0abc0` passes exact local official-Godot CI in 1,404.5 seconds/all 64 and run-14 local Mobile/Speedy visual capture. Governance-only head `441adf35` passes exact local/topic/dev machine gates. Android run `31763879294` publishes its exact raw-checkout/package-source APK (596,033,220 bytes; SHA-256 `f04d0fef3b9bf097aa5b07e56e5726a1db9ff37e4be6ce35b495e31b9e4a72d8`). Speedy action-loop samples stay below the local 1 ms probe ceiling, but P50/P95/P99 device frame time, hitches, memory, thermal, load, and touch-latency data are missing. |
| owner_decision | Mobile renderer is authoritative; Speedy is default; stable 30 fps and transparent-overdraw limits are binding for the target hardware. |
| fix | Produce and measure a matching current APK, then optimize only the bounded hotspots demonstrated by traces while preserving art and behavior. |
| surrounding_tests | Cold/warm load; long session; representative high-cost zones; frame-time percentiles; hitches; RAM/VRAM; thermal; touch latency; focus/pause/re-entry; save integrity; visual comparison. |
| acceptance | The exact release candidate meets documented design thresholds on required devices with retained touch, save, visual, and gameplay behavior. |
| closure | Blocked as of 2026-08-13; the matching `441adf35` APK exists, but no device matrix, measurements, accepted result, closure commit, or date exists. |
| relationships | Blocks `MA-RELEASE-001`; device touch overlaps `MA-TOUCH-001`; asset/performance risks include `MA-ASSET-004` and `MA-2D-002`. |
| history | 2026-08-09: V0 device gap indexed. 2026-08-13: integrated predecessor `e6edf559` gained a matching dev APK; historical source `7391c53c` preserved its failed remote renderer diagnostic. Integrated head `441adf35` adds exact machine and matching-APK evidence over unchanged source `51d0abc0`, but no target-device matrix, so the item remains `BLOCKED_EXTERNAL`. |

## MA-CHILD-001

| Field | Value |
|---|---|
| id | `MA-CHILD-001` |
| title | No current observed five-minute child golden-path session proves comprehension and independent play. |
| rule_ids | `DL-AGE-01`, `DL-AGE-06`, `DL-QA-05`, `DL-SAVE-04` |
| domain / zone | Child usability / whole-game golden path |
| source | Child-evidence audit and absence of a current private observed session. |
| severity | P1 |
| lifecycle | `BLOCKED_EXTERNAL` |
| verification | V0: no current observed child session exists for the exact candidate. |
| reproduction | Install and verify the exact `441adf35` APK from Android run `31763879294` on the target device, and start a private fresh-save five-minute session; give no reading or route instructions and record only safe, consented observations of discovery, touch, recovery, exit, and progress. Session evidence is missing. |
| child_impact | Machine-green mechanics may still be undiscoverable, confusing, tiring, or dependent on adult help for the intended child. |
| evidence | Current source `51d0abc0` passes local official-Godot CI in 1,404.5 seconds/all 64 and strengthens Sky's no-reading focus, touch, route, return, and re-entry mechanics. Integrated head `441adf35` passes local/topic/dev machine gates and Android `31763879294` publishes its matching APK. No current observed session, behavior log, comprehension result, or installed-device record exists. |
| owner_decision | The game is designed for one specific non-reading four-year-old, one finger, short sessions, no fail states, and no lost progress. |
| fix | After machine/device readiness, conduct the smallest safe private observation and repair only concrete comprehension or trapping defects it reveals. |
| surrounding_tests | Fresh save; visible/spoken objective; passive no-win; wrong-action recovery; one-finger navigation; reward; pause/exit; save/re-entry; sibling route; no adult/debug intervention. |
| acceptance | The observed child independently discovers, acts, recovers, receives feedback, exits, and retains progress during the defined session without distress or reading. |
| closure | Blocked as of 2026-08-13; the matching `441adf35` APK exists, but no consented session, observation record, accepted result, closure commit, or date exists. |
| relationships | Depends on `MA-PLAY-001`, `MA-ACCESS-001`, `MA-TOUCH-001`, and `MA-PERF-001`; blocks `MA-RELEASE-001`. |
| history | 2026-08-09: V0 child-evidence gap indexed. 2026-08-13: no observed exact-candidate session; lifecycle remains `BLOCKED_EXTERNAL`. |

## MA-RELEASE-001

| Field | Value |
|---|---|
| id | `MA-RELEASE-001` |
| title | The current integrated head is machine-green with a matching APK but lacks remote Mobile-renderer proof and external release evidence. |
| rule_ids | `DL-SAVE-05`, `DL-QA-04`, `DL-QA-05`, `DL-QA-10` |
| domain / zone | Release readiness / whole game |
| source | Full local CI, GitHub Actions history, exact-head Android dev build, audit scorecard, and missing external-gate inventory. |
| severity | P1 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3 exact local/topic/dev machine/build plus V4 local visual evidence. Integrated head `441adf35` preserves source `51d0abc0`, is machine-green, and has a matching APK; requested-Mobile remote Sky proof and release acceptance remain open. |
| reproduction | Preserve the exact `441adf35` local/topic/dev logs, Android package/hash, and the separate run-14 manifest/PNG/probe-hash evidence with its unknown source revision. Obtain a remote Sky run that actually remains on Mobile and emits accepted JSON rather than treating PNG upload as visual acceptance, then execute device, child, owner, voice/listening, visual, strict-2D, and re-audit gates. Historical `18b6150c`, e6, and `7391c53c` results remain time-scoped predecessor evidence. |
| child_impact | Shipping without these gates risks performance, comprehension, identity, audio, visual, or save defects on the child's actual device. |
| evidence | Runtime `09e5e356` full local 1463.4 seconds/64; `ff068db` full local 1379.3 seconds/64; failed run `31678156887` retained. Historical `51887315`, e6, and `7391c53c` preserve time-scoped machine/build evidence, including the latter's failed Sky renderer. Product source `51d0abc0`, parent `1b7d6bda`, changes exactly 19 paths (+3,318/-3,517) and passes official Godot 4.7.1 local CI in 1,404.5 seconds/all 64. Run-14 has 20/20 local Mobile/Speedy frames, manifest SHA-256 `AEAC7C72E0A3BFF992713127261DD00ED69049947DFB6723AA66365F5712DE34`, and visual-probe SHA-256 `B9EAF5E0738CFB61CCD3E34ACFEA420AEADAB4E3ADE80B40A2CFD1F227569C6C`; these bind its manifest/PNGs and probe script, while `source_revision` remains unknown. Governance-only `441adf35` preserves those product bytes, passes exact local CI in 1,391.5 seconds/all 64 and topic/dev Probe runs `31760207048`/`31762132976` with 63/63 headings, zero hard failures, document 36/six/316/316/34/36, and music 42/42. Both Sky subprocesses still fail requested-Mobile renderer identity after 20 PASS rows and upload PNGs only. Android `31763879294` publishes the exact-head 596,033,220-byte APK at SHA-256 `f04d0fef3b9bf097aa5b07e56e5726a1db9ff37e4be6ce35b495e31b9e4a72d8`. GAME2D is `NO_REGRESSION` at 509 models/65 production/70 probe files but strict remains `UNSATISFIED`. No device, child, owner, accepted-visual, or release acceptance exists. |
| owner_decision | Release requires exact Godot 4.7.2-stable, green integration, save compatibility, protected-asset compliance, and applicable external acceptance; diagnostic captures do not authorize release. |
| fix | Preserve exact-head build provenance, resolve the remote renderer/capture diagnostics, complete all external gates with the matching APK, and repair only concrete failures before promotion. |
| surrounding_tests | Exact local/remote CI; import/analyzer; all trusted probes; GAME2D; visual audit; APK install/upgrade/save; device matrix; child session; owner art/authority; exact voice/listening; clean status and re-audit. |
| acceptance | One exact candidate has green required machine gates, matching APK, resolved diagnostic classification, target-device performance/touch, child comprehension, owner/visual/audio acceptance, strict-2D satisfaction, and clean re-audit. |
| closure | Pending as of 2026-08-13: exact `441adf35` local/topic/dev machine and matching-APK evidence plus the `51d0abc0` run-14 candidate are green, but requested-Mobile remote Sky proof and device/child/owner/listening/strict-2D/accepted-visual evidence are missing. No release closure commit/date is recorded. |
| relationships | Aggregate blocker for `MA-2D-002`, `MA-VIS-006`, `MA-PLAY-001`, `MA-ACCESS-001`, `MA-TOUCH-001`, `MA-OPERA-012`, `MA-PERF-001`, `MA-CHILD-001`, and `MA-AUDIO-001`. |
| history | 2026-08-12: runtime and predecessor local/remote evidence improved. 2026-08-13: e6 supplied predecessor evidence; historical `7391c53c` preserved a failed remote Sky renderer diagnostic. Sealed true-Canvas source `51d0abc0` passes local/run-14 gates, and integrated `441adf35` adds exact local/topic/dev machine plus APK evidence while its remote Sky renderer proof remains failed. Release stays `FIXED_PENDING_VERIFICATION`. |

## MA-VIS-004

| Field | Value |
|---|---|
| id | `MA-VIS-004` |
| title | Current source-average figure/ground values cannot confirm a rendered Fairy or Lagoon separation defect. |
| rule_ids | `DL-VIS-08`, `DL-READ-01`, `DL-QA-03`, `DL-QA-07` |
| domain / zone | Figure/ground readability / Fairy and Sky Lagoon |
| source | Source-average visual diagnostic and game-wide audit interpretation. |
| severity | P2 |
| lifecycle | `REPORTED_UNCONFIRMED` |
| verification | V1 with `COVERAGE_GAP`: source values exist, but rendered local-state evidence is missing. |
| reproduction | Recompute source averages, then capture the true local Canvas scene, HUD, and viewport at Mobile 1280×720 and target-device aspect; only the first step is available. |
| child_impact | A real separation issue could hide actionable figures, but repairing an unconfirmed average could damage approved art and recognition. |
| evidence | Fairy source-average figure/ground values are 0.039 versus 0.040; Lagoon is about 0.004. The metric does not measure rendered local state, and authoritative capture/device evidence is missing. |
| owner_decision | Do not recolor or regenerate approved art merely to satisfy a global average; local runtime evidence and owner identity review control. |
| fix | Obtain state-local Canvas/HUD/viewport/device evidence and apply no art change unless it confirms a specific bounded readability defect. |
| surrounding_tests | Visual-audit stress; focus/objective visibility; decoded alpha and occlusion; sibling states; two aspects; device and owner review; source-hash preservation. |
| acceptance | Authoritative local evidence either disproves the report or identifies and verifies a bounded repair without using the source average as closure. |
| closure | Unconfirmed as of 2026-08-13; local captures, device/owner decision, accepted result, commit, and date are missing. |
| relationships | Related to `MA-VIS-003`; live evidence is tracked by `MA-VIS-006`; Lagoon structure is `MA-VIS-002`. |
| history | 2026-08-09: metric recorded as a coverage gap rather than a confirmed defect. 2026-08-13: lifecycle remains `REPORTED_UNCONFIRMED`. |

## MA-ASSET-001

| Field | Value |
|---|---|
| id | `MA-ASSET-001` |
| title | Large sets of PNGs are reported orphaned without sufficient reachability and provenance proof for safe retention or deletion. |
| rule_ids | `DL-ASSET-01`, `DL-ASSET-04`, `DL-PERF-06`, `DL-QA-01` |
| domain / zone | Asset reachability and export size / Castle, Galaxy, Opera, and Lagoon |
| source | Repository asset/reference inventory summarized by the master audit. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: candidate orphan counts and sizes are measured; deletion safety and provenance classification are incomplete. |
| reproduction | At current audited source, enumerate PNGs in each zone and trace every scene, script, manifest, dynamic load, source-master, and export reference; this static check has no device/aspect substitute. |
| child_impact | Orphans inflate install/import cost on old hardware, while unsafe deletion could remove visible or irreplaceable art. |
| evidence | Castle 9/15 at 2.1 MB; Galaxy 32/32 at 11.7 MB; Opera 453/548 at 166.5 MB; Lagoon 48/90 at 41.9 MB. Per-file reachability/provenance and safe-delete evidence is missing. |
| owner_decision | Inventory and reuse approved assets before generation; never modify/delete protected originals or discard provenance. |
| fix | Classify each candidate as reachable, source-only, historical, protected, licensed reusable, or safely removable; remove only proved export orphans in bounded batches. |
| surrounding_tests | Reference/dynamic-load scan; import/export diff; license/provenance; negative missing-resource scan; boot and zone probes; sibling routes; captures; APK size; clean re-import. |
| acceptance | Every reported file has a reviewable classification, reachable art remains intact, proved orphans are removed from export, and import/runtime/probes/captures are green. |
| closure | Open as of 2026-08-13; per-file disposition, safe-delete proof, post-change APK/import result, closure commit, and date are missing. |
| relationships | Export/medium debt overlaps `MA-2D-002`; size/performance gate overlaps `MA-PERF-001`; Lagoon texture debt includes `MA-ASSET-004`. |
| history | 2026-08-09: current zone counts recorded. 2026-08-13: no safe per-file disposition completed; lifecycle remains `CONFIRMED_OPEN`. |

## MA-ASSET-004

| Field | Value |
|---|---|
| id | `MA-ASSET-004` |
| title | Sky Lagoon retains ten NPOT textures with approximately 11.6 MB of uncompressed simultaneous residency cost. |
| rule_ids | `DL-PERF-03`, `DL-PERF-04`, `DL-PERF-07`, `DL-QA-04` |
| domain / zone | Texture memory and mobile fitness / Sky Lagoon |
| source | Lagoon texture-dimension and residency audit. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: 10/41 NPOT count and estimated decoded residency are recorded; target-device impact is unmeasured. |
| reproduction | Inventory the 41 current Lagoon textures at audited source, identify the ten NPOT dimensions/import modes, then profile simultaneous residency during a full Lagoon traversal on Speedy Mobile; device trace is missing. |
| child_impact | Excess decoded memory may cause load delays, hitches, eviction, or instability on the child's older device. |
| evidence | Master audit section 5.2 records 10/41 NPOT and about 11.6 MB uncompressed residency; per-texture need, optimized variants, and device memory trace are missing. |
| owner_decision | New textures must be at most 1024 px longest side or power-of-two; approved art must not be destructively recompressed merely for convenience. |
| fix | Reuse or derive non-destructive compliant variants only where measured residency requires it, preserving source masters, composition, provenance, and visual quality. |
| surrounding_tests | Dimensions/import modes; lossless visual comparison; seams; references; import deadlock guard; full Lagoon traversal; memory/hitch trace; sibling zones; device capture. |
| acceptance | Required textures meet policy or have justified exceptions, simultaneous residency meets target-device budget, and Lagoon visuals/seams/runtime remain accepted. |
| closure | Open as of 2026-08-13; bounded variant plan, device memory proof, accepted comparison, commit, and closure date are missing. |
| relationships | Contributes to `MA-PERF-001`; Lagoon staging remains `MA-VIS-002`; asset disposition overlaps `MA-ASSET-001`. |
| history | 2026-08-09: 10/41 and 11.6 MB recorded. 2026-08-13: no device proof or accepted optimization; lifecycle unchanged. |

## MA-CI-003

| Field | Value |
|---|---|
| id | `MA-CI-003` |
| title | The 106 probe scripts do not each have exactly one declared trust and execution classification. |
| rule_ids | `DL-QA-01`, `DL-QA-02`, `DL-QA-07`, `DL-SAVE-05` |
| domain / zone | CI governance / all probe scripts |
| source | Probe inventory audit and current local/remote workflow review. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: 106 scripts are inventoried; exhaustive one-class-per-script mapping is absent. |
| reproduction | Enumerate all current `scripts/probe*.gd` and related probe scripts, then compare them with a unique classification manifest covering trusted, runtime-visual, advisory, diagnostic, obsolete, or quarantined states; device/aspect are not applicable. |
| child_impact | An obsolete or weak probe can look authoritative, while an unexecuted critical probe can let regressions reach the child. |
| evidence | Master audit sections 5.2 and 11.2; blocking-loop parity is separately verified under `MA-CI-002`, but the full 106-script classification artifact is missing. |
| owner_decision | Red trusted probes remain real failures; diagnostic/advisory output cannot silently become acceptance, and obsolete probes must not be trusted. |
| fix | Assign every script exactly one declared class, reason, owner/workflow location, and retirement/quarantine rule; validate coverage and uniqueness. |
| surrounding_tests | Complete-set and duplicate-class negatives; local/remote roster parity; workflow reference checks; known-obsolete rejection; quarantine reasons; trusted-probe execution and failure controls. |
| acceptance | All 106 scripts resolve to exactly one valid class, every blocking script executes where declared, and no diagnostic/obsolete/quarantined script can grant a false pass. |
| closure | Open as of 2026-08-13; classification manifest, uniqueness validator, passing result, closure commit, and date are missing. |
| relationships | `MA-CI-002` is terminal for blocking-loop parity only; release implications belong to `MA-RELEASE-001`. |
| history | 2026-08-09: exhaustive classification separated from parity. 2026-08-13: 64/63 execution is green, but 106-script classification remains `CONFIRMED_OPEN`. |

## MA-ROSHAN-003

| Field | Value |
|---|---|
| id | `MA-ROSHAN-003` |
| title | Roshan atlas repacking is optional optimization because current owned-pixel windows and engine sampling are green. |
| rule_ids | `DL-MOT-02`, `DL-PERF-03`, `DL-PERF-07`, `DL-QA-01` |
| domain / zone | Character atlas optimization / Mermaid Roshan |
| source | Roshan 2D pixel-window and engine-sampling probes plus optimization review. |
| severity | P2 |
| lifecycle | `DEFERRED_WITH_REASON` |
| verification | V1/V3 reported: current sampling contract is machine-green; no measured need justifies repacking. |
| reproduction | Run current Roshan pixel/import/runtime sampling probes at audited source and inspect representative animations at Mobile aspect; they pass. A target-device profile showing repack benefit is missing. |
| child_impact | Unnecessary repacking risks clipping or changing the child's central character, while deferral has no demonstrated current gameplay harm. |
| evidence | Current owned-pixel windows and engine sampling probes are green; no atlas-overflow defect, device bottleneck, or accepted repacked candidate exists. |
| owner_decision | Preserve approved Roshan identity and art; do not regenerate or reorganize approved assets for novelty or unmeasured optimization. |
| fix | No current change. Reopen only with a measured device/performance or correctness defect, then create a non-destructive derived atlas with exact anchors. |
| surrounding_tests | Pixel bounds; transparent borders; import filters; UV/cell sampling; all poses/animations; clipping negatives; Mobile captures; device memory/performance; source hash/provenance. |
| acceptance | Deferral remains valid while probes and device behavior are green; any future repack must demonstrate measured benefit and exact visual/runtime equivalence. |
| closure | Deferred as of 2026-08-13; no repair is authorized, and no closure commit/date is required unless new evidence reopens the item. |
| relationships | Roshan clipping repairs are terminal elsewhere; device motivation would relate to `MA-PERF-001`; visual identity review relates to `MA-VIS-006`. |
| history | 2026-08-09: repacking classified as optimization. 2026-08-13: current sampling remains green and lifecycle remains `DEFERRED_WITH_REASON`. |

## MA-PLAY-002

| Field | Value |
|---|---|
| id | `MA-PLAY-002` |
| title | The standalone fire arena has no owner-approved truthful home or retirement for its reward, flag, and medal. |
| rule_ids | `DL-AUTH-01`, `DL-AGE-03`, `DL-MOT-05`, `DL-QA-06` |
| domain / zone | Progression and narrative ownership / standalone fire arena |
| source | Game-wide route/reward audit and unresolved product-role question. |
| severity | P2 |
| lifecycle | `OWNER_DECISION_REQUIRED` |
| verification | V1: the standalone surface and ambiguous reward role are identified; intended product disposition is unknown. |
| reproduction | At current source, trace every visible route, flag, reward callback, medal display, and save key for the standalone fire arena; no authoritative narrative home or retirement decision resolves them. |
| child_impact | The child may encounter a reward with no understandable place in progression, or lose a meaningful activity if it is removed without intent. |
| evidence | Master audit section 5.2; current route/reward/flag/medal ownership is ambiguous. Owner disposition and consequent acceptance evidence are missing. |
| owner_decision | Required: choose a truthful named world/home and reward meaning, or retire the standalone arena while preserving save compatibility. |
| fix | After the owner chooses, implement the smallest route/reward integration or safe retirement; do not invent narrative authority. |
| surrounding_tests | Visible route positive/negative; no hidden route; objective voice/pointer; passive/no-fail; reward exactly once; save migration/re-entry; sibling combat; teardown; child comprehension. |
| acceptance | The owner-approved disposition is implemented, reachable behavior and rewards match it truthfully, saves remain compatible, and applicable device/child/visual gates pass. |
| closure | Waiting for owner decision as of 2026-08-13; disposition, implementation, acceptance result, commit, and date are missing. |
| relationships | Combat presentation may overlap `MA-COMBAT-001`; release remains gated by `MA-RELEASE-001`. |
| history | 2026-08-09: ambiguous standalone role indexed. 2026-08-13: no owner disposition; lifecycle remains `OWNER_DECISION_REQUIRED`. |

## MA-COMBAT-001

| Field | Value |
|---|---|
| id | `MA-COMBAT-001` |
| title | Combat's repaired wave count, slash-band scale, and tutorial discoverability lack phone verification. |
| rule_ids | `DL-AGE-01`, `DL-AGE-07`, `DL-UI-03`, `DL-QA-04` |
| domain / zone | Touch combat and tutorial / phone-only review scope |
| source | Combat implementation/probe report and remaining device-review checklist. |
| severity | P2 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3 reported: bounded repairs are reported green; exact phone visual/touch evidence is absent. |
| reproduction | On the matching APK on the intended phone at native aspect, enter the combat tutorial, discover and use the slash band, complete the configured waves, miss/recover, pause, and re-enter. No current device recording exists. |
| child_impact | Too many waves, a small/misaligned slash area, or an unclear tutorial can cause fatigue or confusion. |
| evidence | Master audit section 5.2 and focused reported repair evidence; phone capture, touch trace, observed discoverability, and performance result are missing. |
| owner_decision | Combat must remain child-appropriate, non-punitive, readable, and one-finger discoverable. |
| fix | Preserve current repair until device evidence; if it fails, adjust only the measured wave/scale/tutorial defect without adding fail states. |
| surrounding_tests | Tutorial positive; passive no-win; miss/recovery; exact wave count; touch bounds; second finger; pause/focus; save/reward/replay; sibling combat; teardown; device performance. |
| acceptance | Target-phone evidence shows legible slash scale, correct bounded waves, independent tutorial discovery, responsive touch, and no punitive state. |
| closure | Pending as of 2026-08-13; target-phone evidence, accepted result, closure commit, and date are missing. |
| relationships | Device performance overlaps `MA-PERF-001`; child comprehension overlaps `MA-CHILD-001`; possible fire-arena scope overlaps `MA-PLAY-002`. |
| history | 2026-08-09: reported repair retained pending device proof. 2026-08-13: lifecycle remains `FIXED_PENDING_VERIFICATION`. |

## MA-OPERA-003

| Field | Value |
|---|---|
| id | `MA-OPERA-003` |
| title | The historical grouped pipe, echo, and Nursery fallback claim has unresolved subclaims that are not individually re-audited. |
| rule_ids | `DL-AUTH-04`, `DL-INT-02`, `DL-QA-03`, `DL-QA-12` |
| domain / zone | Art-fiction and interaction / Opera pipe, echo, and Nursery phases |
| source | Historical Opera audit compared with current authored pipe, echo, bottle, pat, and blanket behavior. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1/V4 partial: several current behaviors repair parts of the grouped report, but accepted per-subclaim evidence is incomplete. |
| reproduction | Launch each named current Opera phase at Mobile aspect, exercise the truthful object/action, and compare against the original grouped claims and accepted captures; the complete split matrix is missing. |
| child_impact | A remaining wrong object or fallback can make an action nonsensical, while treating the whole old claim as current can trigger unnecessary changes. |
| evidence | Current authored pipe, echo, bottle, pat, and blanket behavior; master audit section 5.2. Original claim decomposition, per-subclaim lifecycle, and accepted captures are missing. |
| owner_decision | Later narrower accepted implementations supersede only the conflicting part of a broad historical report; history must remain. |
| fix | Split the grouped report into falsifiable subclaims, retire repaired parts with evidence, and fix only confirmed current defects. |
| surrounding_tests | Each phase positive/negative/passive; truthful object state; voice/pointer; touch alignment; sibling phases; save/reward/replay; teardown/re-entry; accepted two-aspect captures. |
| acceptance | Every historical subclaim has an explicit current lifecycle and evidence; any surviving defect is repaired and accepted without erasing history. |
| closure | Open as of 2026-08-13; split records, complete accepted captures, closure result, commit, and date are missing. |
| relationships | Capture matrix depends on `MA-OPERA-004`; grouped-art re-audit parallels `MA-OPERA-006`. |
| history | 2026-08-09: grouped claim retained as partially repaired. 2026-08-13: current behaviors remain, but unresolved subclaims are unsplit; lifecycle unchanged. |

## MA-OPERA-005

| Field | Value |
|---|---|
| id | `MA-OPERA-005` |
| title | The current three-act mermaid Ballerina lacks accepted two-aspect, M11, child, and owner identity/style evidence. |
| rule_ids | `DL-INT-08`, `DL-MOT-09`, `DL-VIS-06`, `DL-QA-12` |
| domain / zone | Character art and career gameplay / Opera Ballerina |
| source | Current Ballerina atlas/specialist authority, focused probes, full local CI, and exact-head remote gates. |
| severity | P2 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3 partial: accepted 1024×1024 4×4 mermaid atlas and three-act runtime are machine-green; V4/V5/V6/owner evidence is missing. |
| reproduction | Launch Ballerina from Opera Hall on runtime `09e5e356`; complete Pearl Mirror, Ribbon Trail, and Grand Twirl, including assists, held poses, and curtain call at 1280×720 and a second aspect. M11/child/owner sessions are absent. |
| child_impact | The old human-leg art/mechanics are retired, but unverified framing, touch, or identity could still confuse or disappoint the child. |
| evidence | `BALLERINA_PARTY_REBUILD_2026-08-09.md`; current atlas/specialist; focused/full-local/exact-head remote machine evidence. Remote captures are diagnostic and do not supply accepted identity/style review. |
| owner_decision | The one-tail mermaid atlas and three-act full-stage recital supersede older Ballerina art, generic phases, and looped playback. |
| fix | Preserve current Ballerina, gather two-aspect/M11/child/owner evidence, and repair only a demonstrated bounded presentation or interaction defect. |
| surrounding_tests | Three acts; pose keys and one-shot curtain call; monotonic assists; one-finger input; passive no-win; voice/music; reward/save/replay; teardown/re-entry; two aspects/device. |
| acceptance | Accepted two-aspect captures, M11 play, observed child comprehension, and owner identity/style approval pass for the current authority. |
| closure | Pending as of 2026-08-13; external/accepted visual evidence, closure commit, and date are missing. |
| relationships | Supersedes old Ballerina versions; capture gap `MA-OPERA-004`; release gate `MA-RELEASE-001`. |
| history | 2026-08-09: newer mermaid atlas and three-act authority adopted. 2026-08-13: machine evidence remains green; lifecycle remains `FIXED_PENDING_VERIFICATION`. |

## MA-OPERA-006

| Field | Value |
|---|---|
| id | `MA-OPERA-006` |
| title | The grouped Nursery, Farmer, and Racer art-fiction report remains unsplit after partial repairs and retains unresolved voice mismatches. |
| rule_ids | `DL-AUTH-04`, `DL-SND-01`, `DL-SND-05`, `DL-QA-03` |
| domain / zone | Art-fiction and protected voice / Opera Nursery, Farmer, and Racer |
| source | Historical grouped Opera report compared with current repaired runtime and voice inventory. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1/V3 partial: material art-fiction repairs exist, but per-subclaim and protected-voice closure is incomplete. |
| reproduction | Exercise every affected Nursery, Farmer, and Racer phase on current runtime, compare visuals/actions/voice keys with the grouped report, and record each subclaim separately; complete accepted captures/listening are missing. |
| child_impact | Remaining mismatched narration or art-fiction can tell the child to do or expect the wrong thing. |
| evidence | Current repaired Nursery/Farmer/Racer behavior and master audit section 5.2; split subclaim inventory, accepted captures, authorized exact voice, device listening, and owner review are missing. |
| owner_decision | Protected voice originals cannot be modified; later repairs supersede only their exact conflicting historical subclaims. |
| fix | Split and re-audit all subclaims, preserve completed repairs, and address only confirmed residual visual/voice defects with authorization. |
| surrounding_tests | Per-phase positive/negative/passive; exact voice keys; visual/touch alignment; sibling careers; reward/save/replay; teardown/re-entry; two-aspect capture; mono/device listening. |
| acceptance | Every grouped subclaim has an explicit lifecycle; surviving defects have accepted visual/device/voice/owner evidence and protected originals remain intact. |
| closure | Open as of 2026-08-13; split records, authorized voice evidence, accepted captures/listening, closure commit, and date are missing. |
| relationships | Parallels grouped finding `MA-OPERA-003`; exact voice gap relates to `MA-ACCESS-001`; capture gap `MA-OPERA-004`. |
| history | 2026-08-09: grouped claim marked partially repaired. 2026-08-13: residual subclaims/voices remain open; lifecycle unchanged. |

## MA-OPERA-007

| Field | Value |
|---|---|
| id | `MA-OPERA-007` |
| title | Farmer and Doctor use above-water settings while other Opera careers use a different backdrop convention, with no owner disposition. |
| rule_ids | `DL-AUTH-01`, `DL-VIS-04`, `DL-QA-03`, `DL-QA-06` |
| domain / zone | Narrative art direction / Opera Farmer and Doctor |
| source | Cross-career backdrop comparison and master audit owner-decision index. |
| severity | P2 |
| lifecycle | `OWNER_DECISION_REQUIRED` |
| verification | V1: the setting difference is observed; whether it is intentional or defective is unknown. |
| reproduction | Compare current Farmer and Doctor full-stage backdrops with the other Opera careers at Mobile 1280×720, including narrative entry and objective context; no owner ruling defines the desired convention. |
| child_impact | An unintended setting shift can weaken story coherence, but changing an intentional contrast could remove variety the child enjoys. |
| evidence | Master audit section 5.2 and current career backdrop comparison; owner intent, accepted reference, and runtime/device acceptance are missing. |
| owner_decision | Required: explicitly accept the above-water exception or select the intended replacement setting and continuity scope. |
| fix | Make no art change until the owner decides; then preserve the accepted exception or apply a bounded, provenance-safe backdrop correction. |
| surrounding_tests | Narrative entry/objective consistency; figure/ground; touch alignment; sibling-career comparison; seams; voice; two-aspect/device capture; owner review. |
| acceptance | The owner records the intended setting, and the resulting current or repaired scenes pass narrative, visual, device, and child-readability review. |
| closure | Waiting for owner decision as of 2026-08-13; disposition, accepted reference/evidence, implementation commit if needed, and date are missing. |
| relationships | Visual evidence depends on `MA-OPERA-004`; grouped Farmer issues also appear in `MA-OPERA-006`. |
| history | 2026-08-09: setting difference indexed for owner decision. 2026-08-13: no disposition recorded; lifecycle unchanged. |

## MA-AUDIO-001

| Field | Value |
|---|---|
| id | `MA-AUDIO-001` |
| title | Complete runtime audio has measured delivery and bounded repairs but lacks required human, voice-identity, mono, transition, child, and device acceptance. |
| rule_ids | `DL-SND-06` through `DL-SND-17`, `DL-QA-04`, `DL-QA-13`, `DL-QA-16` |
| domain / zone | Voice, music, ambience, UI, SFX, fallbacks, and mix / game-wide |
| source | Deterministic score/render/manifest audit, routing probes, local CI, and pinned Windows jobs. |
| severity | P2 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3 partial: hashes, codec, loop/import, loudness, peak, seam, routing, and 42/42 machine delivery pass; listening/device evidence is open. |
| reproduction | On the exact candidate with matching APK, listen to two wraps of every cue, transitions, speech ducking, music-off restoration, and mono fold-down on headphones/speaker and Lenovo Tab M11. The human/device matrix is missing. |
| child_impact | A technically valid loop can still be tiring, mask family voices, click at transitions, disappear in mono, or play poorly on the child's hardware. |
| evidence | `assets_src/audio/music/area_music_scores.json`; `assets/audio/music/area_music_manifest.json`; `AUDIO_QUALITY_AUDIT_2026-08-24.txt`; `audit/audio_quality_ledger_2026-08-24.csv`; and `audit/audio_quality_summary_2026-08-24.json`. Current topic/dev runs `31760207048`/`31762132976` at exact `441adf35` finish music 42/42 in 3m18s/3m56s. The 2026-08-24 extension measures and grades all 303 final audio files, removes the clipping UI tap, adds two exact Racer voices, true-peak repairs three unprotected voices, and preserves six protected files byte-identically. Human identity/listening, 31 legacy candidates, 126 bounded voice-peak candidates, mono, child, and device evidence remain open. |
| owner_decision | Machine evidence never substitutes for human listening; protected voices remain authoritative and must stay intelligible. |
| fix | Complete the all-audio listening matrix and make only bounded voice/score/SFX/mix repairs demonstrated by it, preserving deterministic sources, manifests, speaker identity, and protected originals. |
| surrounding_tests | 42/42 deterministic rebuild; source/render/import hashes; codec/loop/seam/loudness/peak; named routing; hard cuts; voice ducking; music-off/on; mono; two wraps; M11 start/loop/performance. |
| acceptance | Every ledger row has a final disposition; required voices pass exact semantics, identity, intelligibility, child comprehension, and teardown; all 42 new scores pass two-wrap/style review; the full mix passes mono, transitions, music-off, M11, older-phone, and performance review while machine evidence remains exact. |
| closure | Pending as of 2026-08-13; human/device listening evidence, accepted result, closure commit, and date are missing. |
| relationships | Exact objective voice gaps are `MA-ACCESS-001` through `003`; aggregate release gate is `MA-RELEASE-001`. |
| history | 2026-08-12: deterministic 42/42 repair and remote Windows verification completed. 2026-08-13: exact-head Windows remains 42/42; lifecycle stays `FIXED_PENDING_VERIFICATION` for listening/device evidence. 2026-08-24: Luna-led 301-file baseline and 303-file final ledger extend the finding game-wide; six bounded repairs land without altering protected bytes, while subjective/device/child gates and documented candidates remain open. |

## MA-CODE-001

| Field | Value |
|---|---|
| id | `MA-CODE-001` |
| title | `scripts/main.gd` is 10,499 lines at integration head `9a1754c1`, far above the extraction-only target below 2,500 lines, and the trend has reversed. |
| rule_ids | `DL-SAVE-03`, `DL-QA-01`, `DL-QA-02` |
| domain / zone | Architecture and maintainability / `ReefMain` |
| source | Static line-count and architecture audit at runtime commit `09e5e356`. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: exact line count and target are confirmed; remaining extraction boundaries are not completed. |
| reproduction | At current source `51d0abc0`, count `scripts/main.gd` lines and inspect state ownership; it is 8,734 lines versus the documented extraction-only target below 2,500. Device/aspect are not applicable to the count. Historical runtime `09e5e356` was 8,647 lines. |
| child_impact | Large coupled code raises regression risk for saves, touch, navigation, and activities when the child's game changes. |
| evidence | `scripts/main.gd`; master audit sections 1.3, 4.7, and 5.2; satellite scripts exist, but HUD/environment/aquatic/galaxy/kart/level-2 glue remains. |
| owner_decision | Refactor by mechanical extraction only: shared state stays on main, one bounded owner/tick per commit, and failed probes require revert rather than probe weakening. |
| fix | Continue small behavior-preserving extractions into typed satellites until the target is met, with no opportunistic rewrite. |
| surrounding_tests | Parser and inference lint; exact before/after focused probes; passive; save/load/recovery/re-entry; UI/touch; sibling systems; full trusted probes and exact CI for each extraction. |
| acceptance | `main.gd` is below 2,500 lines through reviewed mechanical extractions, behavior/save contracts are unchanged, and all required gates remain green. |
| closure | Open as of 2026-08-26; current line count is 10,499 and no complete extraction sequence, final gate result, closure commit, or date exists. |
| relationships | Coupled structural risks are `MA-CODE-002`; broad medium migration is `MA-2D-002`; release risk aggregates under `MA-RELEASE-001`; the 2026-08-26 round decomposes bounded sub-risks into `MA-CODE-003`, `MA-CODE-004`, `MA-PERF-002`, and `MA-SAVE-001`. |
| history | 2026-07-18: extraction-only target documented. 2026-08-13: `09e5e356` measured 8,647 lines; `51d0abc0` measured 8,734; lifecycle `CONFIRMED_OPEN`. 2026-08-26: integration head `9a1754c1` measures 10,499 lines (+1,765 in thirteen days) with 480 functions — the Day One glue (about thirty `day_one_*` functions), start-menu routing, and venue delegation landed on main while `scripts/day_one_director.gd` exists as a 673-line satellite; the shrink trajectory is reversed and `DL-CODE-01` now names the criterion; lifecycle remains `CONFIRMED_OPEN`. |

## MA-CODE-002

| Field | Value |
|---|---|
| id | `MA-CODE-002` |
| title | String-owned state, duplicated input, save frequency, material churn, and remaining 3D glue create unresolved structural risk. |
| rule_ids | `DL-SAVE-01`, `DL-SAVE-02`, `DL-SAVE-03`, `DL-QA-02` |
| domain / zone | Architecture, state, input, save, and rendering glue / game-wide |
| source | Static code and lifecycle audit across main, activities, save paths, input ownership, and rendering helpers. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: risk patterns are confirmed; each requires a separately bounded reproduction before repair. |
| reproduction | At current runtime source, trace string states, duplicate input routes, save calls, per-frame material creation, retained 3D glue, and lifecycle cleanup across representative enter/act/pause/leave/re-enter flows; no single broad runtime reproduction closes the grouped risk. |
| child_impact | These patterns increase chances of stuck touch, excessive writes, lost/restored-wrong progress, hitches, or cross-activity state leaks. |
| evidence | Master audit sections 4.7 and 5.2; current code inspection. The sealed Castle Kitchen caller's speculative invalid-Chef recovery is deliberately unimplemented because current config is valid/probed and owner approval would be required. |
| owner_decision | Preserve save keys/defaults/backups, keep one-touch ownership, extract rather than rewrite, and do not alter sealed Castle visual callers without renewed owner approval. |
| fix | Split this grouped risk into bounded changes with concrete reproductions; remove duplication/churn/glue mechanically while preserving state ownership and save compatibility. |
| surrounding_tests | Parser/lint/analyzer; positive and invalid-state negatives; passive; duplicate-touch/focus/pause; save/write cadence/load/recovery; materials/performance; sibling systems; teardown/re-entry; full CI. |
| acceptance | Each confirmed sub-risk has a bounded repair and regression evidence, no speculative caller change is smuggled in, and state/input/save/render contracts remain green. |
| closure | Open as of 2026-08-13; sub-risk decomposition and repairs are incomplete, with no aggregate acceptance result, closure commit, or date. |
| relationships | Companion to size finding `MA-CODE-001`; save/release risk affects `MA-RELEASE-001`; remaining 3D glue contributes to `MA-2D-002`; Chef caller exclusion relates to `MA-OPERA-001`. |
| history | 2026-08-09: grouped structural risks confirmed. 2026-08-12: speculative Chef caller hardening explicitly excluded. 2026-08-13: lifecycle remains `CONFIRMED_OPEN`. 2026-08-26: the code-refinement round re-measures the group at `9a1754c1` — 409 distinct string state keys, eight verbatim pointer-glyph copies, three `_action_pressed` copies, roughly 280 cross-module calls into main-side private builder helpers, and 38 probe-private `_frames` helpers — and carves bounded sub-findings `MA-CODE-003`, `MA-CODE-004`, `MA-PERF-002`, `MA-SAVE-001`, and `MA-CI-007` out of this group per its own fix plan; the residual group stays `CONFIRMED_OPEN` for what remains. |

## MA-CI-004

| Field | Value |
|---|---|
| id | `MA-CI-004` |
| title | The Day One wing and start-menu routing ship with eight dedicated probes, none of which runs in either trusted roster. |
| rule_ids | `DL-CODE-10`, `DL-QA-02`, `DL-QA-07`, `DL-SAVE-05` |
| domain / zone | CI and release evidence / Day One wing, start menu, mermaid pool, art studio |
| source | 2026-08-26 code-refinement round roster cross-check at integration head `9a1754c1`. |
| severity | P1 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: roster absence is exact; the ungated probes' own health is unassessed. |
| reproduction | At `9a1754c1`, list `scripts/probe_day_one_*.gd` plus `scripts/probe_start_menu_routing.gd` (eight files), then search the trusted loops in `scripts/ci.sh` and `.github/workflows/probes.yml`; zero of the eight appear in either roster, so no push can fail on a Day One or fresh-save-routing regression. |
| child_impact | Day One is the fresh-save entry arc — the first thing the child meets after New Game. A routing, cleanup, or reward regression there ships without any gate noticing. |
| evidence | `scripts/probe_day_one_art_attack_state.gd`, `probe_day_one_art_studio_shots.gd`, `probe_day_one_castle_dressing.gd`, `probe_day_one_director.gd`, `probe_day_one_integration.gd`, `probe_day_one_pool_cleanup.gd`, `probe_day_one_pool_shots.gd`, `probe_start_menu_routing.gd`; trusted rosters in `scripts/ci.sh` and `.github/workflows/probes.yml` contain none of them; `scripts/main.gd:3763` `_launch_from_start_menu` routes New Game into Day One. |
| owner_decision | Not required: gating an existing wing's probes implements the standing probe-first contract. |
| fix | Classify the eight probes per master audit section 11.2; promote the deterministic non-capture ones (at minimum `probe_day_one_director`, `probe_day_one_integration`, `probe_day_one_pool_cleanup`, `probe_start_menu_routing`) into both trusted rosters; capture-style probes become `ADVISORY_CAPTURE`. |
| surrounding_tests | Each promoted probe runs green three consecutive times locally before promotion; full suite before/after; roster parity check between `ci.sh` and `probes.yml`. |
| acceptance | Both rosters carry the promoted probes, a deliberately injected Day One routing break turns the gate red, and suite wall time stays inside the workflow ceiling. |
| closure | Open as of 2026-08-26; no roster change exists. |
| relationships | Decomposes release risk from `MA-RELEASE-001`; complements `MA-CI-003` classification and `MA-CI-005` passive coverage. |
| history | 2026-08-26: confirmed by roster cross-check; opened `CONFIRMED_OPEN`. |

## MA-CI-005

| Field | Value |
|---|---|
| id | `MA-CI-005` |
| title | The central zero-input negative probe snapshots only pearls, trophies, stickers, and medals, so a passive award in Opera, combat, castle interactions, or Day One is invisible to it. |
| rule_ids | `DL-AGE-04`, `DL-CODE-10`, `DL-QA-02` |
| domain / zone | CI negative coverage / `scripts/probe_passive.gd` game-wide |
| source | 2026-08-26 code-refinement round probe-content audit at integration head `9a1754c1`. |
| severity | P1 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: snapshot field list and per-mode idle checks are read exactly; no runtime demonstration of a slipped award exists. |
| reproduction | At `9a1754c1`, read `scripts/probe_passive.gd` `_progress_snapshot()` — it reads `pearl_count`, `trophies`, `stickers`, `medals` (with shop/animal ownership) and never `opera_stars`, `opera_progress`, combat completion fields, `stuffie_wins`, castle interaction milestones, or Day One state; the file's mode coverage is the five friend games, shop, slide, fairy, and brawl. Newer modes carry their own opt-in idle assertions inside their own probes, which a brand-new mode does not inherit. |
| child_impact | The no-fail promise's enforcement arm is the passive probe; a future mercy or assist feature that quietly awards progress for watching would ship ungated in every mode the snapshot does not cover. |
| evidence | `scripts/probe_passive.gd` (snapshot function and mode list; three total references matching opera/combat/dungeon/stuffie/castle); distributed idle checks exist in `probe_opera.gd`, `probe_opera_2d.gd`, `probe_combat.gd`, `probe_stuffie.gd`, `probe_living_world.gd` but are opt-in per probe. |
| owner_decision | Not required: extending the negative test implements `DL-AGE-04` as already decided. |
| fix | Extend `_progress_snapshot()` to a complete reward-surface dictionary (opera stars/progress/pantry, combat and tutorial completion, dungeon checkpoints, `stuffie_wins`, care points, Day One serialized state, castle milestone fields), and add passive legs for the reward-bearing modes it can cheaply enter; document that a new mode must either extend the snapshot or carry its own idle no-award leg. |
| surrounding_tests | Deliberate mutation test: hand-award one field of each new snapshot section under idle input and confirm the probe fails; full suite green after. |
| acceptance | The snapshot covers every save-backed reward surface at the audited commit, the mutation test fails closed for each section, and the rule is recorded in the probe header. |
| closure | Open as of 2026-08-26; snapshot unchanged. |
| relationships | Enforces the same invariant family as `MA-CI-004`; classification context is `MA-CI-003`. |
| history | 2026-08-26: confirmed by probe-content read; opened `CONFIRMED_OPEN`. |

## MA-CODE-003

| Field | Value |
|---|---|
| id | `MA-CODE-003` |
| title | At least eight shared behaviors exist as verbatim multi-copy clones — pointer glyphs, action-press reads, cached material factories, AABB kits, avatar spawns, mode start/end scaffolds, stage input maps, and act teardown lists. |
| rule_ids | `DL-CODE-05`, `DL-CODE-06`, `DL-QA-02` |
| domain / zone | Architecture and maintainability / cross-cutting gameplay scripts |
| source | 2026-08-26 code-refinement round duplication sweep at integration head `9a1754c1`, decomposed from `MA-CODE-002`. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: copies located and counted by exact text search; behavioral equivalence of each family is asserted from reading, not runtime diffing. |
| reproduction | At `9a1754c1`: the `pointer.text = "▼"` Label3D block appears eight times; `func _action_pressed()` is verbatim in `scripts/dungeon_puzzle_room.gd:312`, `scripts/combat_arena.gd:354`, `scripts/stuffie_battle.gd:285`; the keyed cached-material factory `_mat(col, glow)` with primitive trio recurs across `dungeon_puzzle_room.gd` and `opera_house.gd`; `_gather_aabbs`-style kits recur in `ember_fortress.gd`, `kart.gd`, `galaxy.gd`, and main; a thirty-line Roshan avatar spawn is cloned between `ember_fortress.gd` and `galaxy.gd`; the eight-branch keyboard-to-stage input map is cloned between `games/side_scroll.gd` and `games/octagon_stage.gd`; main's `_start_X_now`/`_end_X` scaffolds repeat per standalone mode. |
| child_impact | Clone drift is how one mode's fix misses its siblings — the child meets the stale copy. |
| evidence | Paths and line anchors above; count check `grep -rn 'pointer.text = "▼"' scripts` returns eight. |
| owner_decision | Not required: consolidation under exact-behavior extraction is the standing refactor contract. |
| fix | One clone family per commit: extract a shared helper (satellite or static), point every copy at it mechanically, and prove exact behavior with the owning probes; start with the action-press read and the pointer widget, which have the smallest surfaces. |
| surrounding_tests | Full trusted suite before/after each family; the owning mode probes for every touched file; parser/lint/analyzer. |
| acceptance | Each named family has one implementation with all call sites migrated, suite green at each step, and no behavior delta reported by the owning probes. |
| closure | Open as of 2026-08-26; no consolidation commit exists. |
| relationships | Decomposed from `MA-CODE-002`; probe-side boilerplate is `MA-CI-007`; size pressure feeds `MA-CODE-001`. |
| history | 2026-08-26: copies re-verified at `9a1754c1` after the Opera dismantle relocated several; opened `CONFIRMED_OPEN`. |

## MA-CODE-004

| Field | Value |
|---|---|
| id | `MA-CODE-004` |
| title | Cross-system state is keyed by 409 distinct raw string literals in the `g` scratch dictionary, where a typo fails silently at runtime. |
| rule_ids | `DL-CODE-04`, `DL-CODE-03`, `DL-QA-01` |
| domain / zone | Architecture and state / `ReefMain.g` and all satellites |
| source | 2026-08-26 code-refinement round state-surface count at integration head `9a1754c1`, decomposed from `MA-CODE-002`. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: distinct-key count is exact; no specific live typo defect is currently reproduced. |
| reproduction | At `9a1754c1`, `grep -rhoE 'g\["[a-z0-9_]+"\]' scripts --include='*.gd' \| sort -u \| wc -l` reports 409 distinct keys (380 at `e924d9ba` thirteen days earlier); main itself holds 82 accesses while satellites hold the rest as `m.g["…"]`. |
| child_impact | A misspelled state key reads as a default instead of erroring, producing wrong-but-quiet behavior in whatever mode the child is in. |
| evidence | Count command above; the historical shrink of `g` on main relocated rather than reduced the surface. |
| owner_decision | Not required: `DL-CODE-04` states the direction; no schema or save change is involved. |
| fix | Freeze the surface (no new keys — reviewed against the baseline count), introduce typed accessor helpers or per-mode typed state objects for the top-traffic key families (phase/timer/position groups), and migrate one mode per commit mechanically. |
| surrounding_tests | Full suite per migration; a lint count of distinct keys recorded in the round metrics so growth is visible at the next audit. |
| acceptance | Distinct-key count is at or below 409 at the next audit round and at least two high-traffic modes read state through typed accessors with suite green. |
| closure | Open as of 2026-08-26; count is 409 and growing. |
| relationships | Decomposed from `MA-CODE-002`; interacts with `MA-CODE-001` extraction boundaries. |
| history | 2026-08-26: counted 409 distinct keys (up from 380 on 2026-08-13's parent head); opened `CONFIRMED_OPEN`. |

## MA-CODE-005

| Field | Value |
|---|---|
| id | `MA-CODE-005` |
| title | A fully wired but unreachable loss-message system (`_fail_line()` and the unused lose branch of `_end_game`) sits one call away from violating the no-fail rule. |
| rule_ids | `DL-CODE-09`, `DL-AGE-03` |
| domain / zone | Child-safety adjacent dead code / `scripts/main.gd` |
| source | 2026-08-26 code-refinement round dead-code sweep at integration head `9a1754c1`. |
| severity | P3 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: zero call sites confirmed by exact search. |
| reproduction | At `9a1754c1`, `scripts/main.gd:8143` defines `_fail_line()` returning in-character loss lines ("Aww... now Chuck is all wet!"); repo-wide search finds no caller, and no `_end_game(false` call exists, so the lose path of `_end_game(win: bool)` is also unreachable. |
| child_impact | None today; the risk is a future wiring mistake resurrecting a loss message against the no-fail promise. |
| evidence | `scripts/main.gd:8143` and caller search; `_end_game(false` returns zero hits. |
| owner_decision | Not required: removing dead code that cannot ship a behavior change. |
| fix | Delete `_fail_line()` and the dead lose branch; keep `_end_game`'s signature only if a caller needs it, otherwise simplify mechanically. |
| surrounding_tests | Parser/lint/analyzer; full suite; passive probe unchanged. |
| acceptance | The symbols are gone, the suite is green, and no probe output changes. |
| closure | Open as of 2026-08-26; code present. |
| relationships | Child-safety context is `DL-AGE-03` enforcement; grouped origin is `MA-CODE-002`. |
| history | 2026-08-26: confirmed dead at `9a1754c1`; opened `CONFIRMED_OPEN`. |

## MA-PERF-002

| Field | Value |
|---|---|
| id | `MA-PERF-002` |
| title | `_sparkle_burst` allocates a particle node, a mesh, and a material on every call from 141 sites with no quality-tier gate, including a permanent wayfinder cadence. |
| rule_ids | `DL-CODE-07`, `DL-CODE-08`, `DL-PERF-03` |
| domain / zone | Runtime performance / `scripts/main.gd` effect helper, game-wide callers |
| source | 2026-08-26 code-refinement round allocation sweep at integration head `9a1754c1`, decomposed from `MA-CODE-002`. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: allocation pattern and call count are exact; no target-device frame-time measurement isolates its cost yet. |
| reproduction | At `9a1754c1`, `scripts/main.gd:8001` constructs `CPUParticles3D.new()` + `BoxMesh.new()` + `StandardMaterial3D.new()` per call and frees via a tween 1.6 seconds later; 141 call references exist across scripts; the wayfinder emits bursts on a repeating cadence during free roam; no `speedy`/quality check appears in the function. |
| child_impact | Steady allocation and node churn on a weak phone GPU/CPU is a plausible hitch source exactly while the child follows the sparkle trail. |
| evidence | `scripts/main.gd:8001` function body; call-reference count; absence of tier checks in the function. |
| owner_decision | Not required: pooling and caching preserve identical visuals. |
| fix | Cache one shared `BoxMesh` and per-color materials, pool a small ring of particle nodes, and add the Speedy-tier reduction (fewer simultaneous bursts) per `DL-CODE-08`; keep visual output otherwise identical. |
| surrounding_tests | Full suite; visual spot-check of a celebration and the wayfinder trail; later target-device frame capture under `MA-PERF-001`'s protocol. |
| acceptance | No per-call allocation of mesh/material remains, pooled nodes are bounded, tier reduction exists, and the suite is green with unchanged probe output. |
| closure | Open as of 2026-08-26; helper unchanged. |
| relationships | Decomposed from `MA-CODE-002`; device evidence rolls up to `MA-PERF-001`; tier-coverage context is `MA-PERF-003`. |
| history | 2026-08-26: re-verified at `9a1754c1` (141 sites; body allocates all three resources); opened `CONFIRMED_OPEN`. |

## MA-PERF-003

| Field | Value |
|---|---|
| id | `MA-PERF-003` |
| title | The newest child-facing surfaces — the Canvas Melody theater, the Day One director, the side-scroll stage, and the remaining spatial Galaxy/companion layers — contain no quality-tier awareness at all. |
| rule_ids | `DL-CODE-08`, `DL-PERF-02`, `DL-PERF-03` |
| domain / zone | Runtime performance / newest gameplay surfaces game-wide |
| source | 2026-08-26 code-refinement round tier-coverage sweep at integration head `9a1754c1`. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: zero-reference counts are exact per file; actual per-surface frame cost on the target device is unmeasured. |
| reproduction | At `9a1754c1`, searching `speedy`/`quality` reports zero hits in `scripts/games/melody.gd` (1,295 lines, new Canvas rhythm stage), `scripts/day_one_director.gd` (673 lines), and `scripts/games/side_scroll.gd` (930 lines); `scripts/opera_gesture_surface.gd` (6,185 lines) matches only an unrelated gesture-quality signal; legacy spatial `scripts/galaxy.gd` and `scripts/companion.gd` also carry none while creating lights, labels, and transparent cards. The Speedy tier itself defaults on for mobile. |
| child_impact | The tier exists to keep the weakest phone at a stable frame rate; surfaces that ignore it spend the same budget on the M11 as on a desktop, and the newest surfaces are where she now plays most. |
| evidence | Per-file zero counts above; `scripts/main.gd` `_apply_quality` implements the tier for the legacy reef systems only. |
| owner_decision | Not required for reductions that do not change what the child sees at Sparkly tier. |
| fix | Per surface, identify the dominant cost (redraw cadence, canvas particle counts, ambient loop counts, decoded texture residency, remaining 3D lights/cards) and either implement a Speedy reduction or record a measured budget note stating why none is needed, per `DL-CODE-08`. |
| surrounding_tests | Full suite; before/after screenshots at both tiers for one touched surface; later device capture under `MA-PERF-001`. |
| acceptance | Every named surface has either a tier path or a recorded budget note, and the suite is green. |
| closure | Open as of 2026-08-26; no tier work exists in the named files. |
| relationships | Effect churn is `MA-PERF-002`; device evidence is `MA-PERF-001`; spatial remainder overlaps `MA-2D-002`. |
| history | 2026-08-26: swept at `9a1754c1`; opened `CONFIRMED_OPEN`. |

## MA-SAVE-001

| Field | Value |
|---|---|
| id | `MA-SAVE-001` |
| title | Castle interaction progress the child can see accumulates only in the unpersisted `m.g` scratch dictionary and is lost on app kill. |
| rule_ids | `DL-CODE-03`, `DL-SAVE-01`, `DL-SAVE-04` |
| domain / zone | Save and persistence / `scripts/arena/castle_rooms_25d.gd` interaction state |
| source | 2026-08-26 code-refinement round persistence sweep at integration head `9a1754c1`, decomposed from `MA-CODE-002`. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: the scratch writes and the absence of any save path for them are exact; the child-visible loss is reasoned, not observed. |
| reproduction | At `9a1754c1`, `scripts/arena/castle_rooms_25d.gd` writes `m.g["castle_dust_bunnies_cleared"]` at lines 919, 3968, and 4060 and `m.g["crown_won"]` at 4729; `ReefMain.g` is per-activity scratch cleared by `_clear_game()` and never serialized. Milestones are laundered into real save fields (`stuffie_wins`, `level2_done_once`) only at completion, so partial clearing progress (for example one of two cleared pins) resets on kill or leave. Day One state is, correctly, serialized through `day_one_director.serialize_state()` — the gap is the castle interaction layer. |
| child_impact | A child who clears half a room's dust bunnies, gets interrupted, and returns finds her work undone — a small but real broken promise against zero tolerance for lost progress. |
| evidence | Write sites above; `save_state.gd` has no castle interaction fields; `main.gd` `_clear_game()` resets `g = {}`. |
| owner_decision | Not required: adding append-only keys with defaults is the standing save contract. |
| fix | Promote durable child-visible castle interaction progress into append-only save fields with defaults (per-room cleared maps), written through the existing `_queue_save` cadence; leave true per-session scratch in `g`. |
| surrounding_tests | Save round-trip probe extension covering the new keys; kill-and-relaunch restore; passive probe unchanged; full suite. |
| acceptance | Partial castle interaction progress survives an app kill, the new keys are append-only with defaults, and save probes cover them. |
| closure | Open as of 2026-08-26; state remains scratch-only. |
| relationships | Decomposed from `MA-CODE-002`; save-contract kin `MA-RELEASE-001`. |
| history | 2026-08-26: verified write sites and missing serialization at `9a1754c1`; opened `CONFIRMED_OPEN`. |

## MA-AUDIO-002

| Field | Value |
|---|---|
| id | `MA-AUDIO-002` |
| title | The microphone capture player routes to a "Mic" bus that does not exist in the bus layout and depends on a runtime bus rename to avoid audible self-capture. |
| rule_ids | `DL-SND-04`, `DL-SND-14`, `DL-AGE-08` |
| domain / zone | Audio routing / `scripts/mic_input.gd`, `default_bus_layout.tres` |
| source | 2026-08-26 code-refinement round audio-routing sweep at integration head `9a1754c1`. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: the missing bus and the runtime-rename fallback are exact; the failure mode (mic audible through speakers) is reasoned, not reproduced on device. |
| reproduction | At `9a1754c1`, `default_bus_layout.tres` declares Master, Music, Voice, SFX, Ambience, and UI — no Mic; `scripts/mic_input.gd:244` assigns `bus = "Mic"`, relying on the self-heal at lines 217–223 that renames a spare bus at runtime. If that path fails or races player creation, Godot falls back to Master and the spoken-spell microphone becomes audible through the phone speaker. |
| child_impact | A mic-to-speaker loop during a stuffie battle would be a loud, confusing, potentially frightening noise — exactly the class `DL-AGE-08` exists to prevent. |
| evidence | Bus list in `default_bus_layout.tres`; assignment and self-heal sites in `mic_input.gd`. |
| owner_decision | Not required: declaring a muted bus in the layout resource changes no audible behavior when the current rename path succeeds. |
| fix | Declare a seventh, muted `Mic` bus in `default_bus_layout.tres`; keep the runtime check as a defensive assertion rather than the creation path; extend `probe_audio.gd` to assert the Mic bus exists and is muted. |
| surrounding_tests | `probe_audio` extension; mic probe (`probe_mic`) unchanged and green; full suite. |
| acceptance | The layout declares the muted Mic bus, `probe_audio` asserts it, and the rename fallback becomes unreachable in normal boot. |
| closure | Open as of 2026-08-26; layout unchanged. |
| relationships | Mix-review context is `MA-AUDIO-001`. |
| history | 2026-08-26: verified layout and assignment at `9a1754c1`; opened `CONFIRMED_OPEN`. |

## MA-TOUCH-002

| Field | Value |
|---|---|
| id | `MA-TOUCH-002` |
| title | The side-scroll swim branch reads the emulated mouse without the reserved-zone guard, so holding a UI medallion drags Roshan toward it. |
| rule_ids | `DL-UI-02`, `DL-UI-04`, `DL-QA-02` |
| domain / zone | Touch routing / `scripts/games/side_scroll.gd` swim tick |
| source | 2026-08-26 code-refinement round touch-guard sweep at integration head `9a1754c1`; residual of the 2026-08-03 touch audit's third finding. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: the unguarded read is exact in source; the drag symptom is reasoned from the same mechanism the fixed sibling paths had. |
| reproduction | At `9a1754c1`, `scripts/games/side_scroll.gd` around line 158 maps `Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT)` plus `get_mouse_position().x` directly to stage x in the swim branch with no `reserved_zone_hit()` check, unlike its own `walk_tick` hold path (guarded at about line 277). A held action medallion or pause-corner press in a swim stage therefore steers continuously. |
| child_impact | Pressing the big action bubble while swimming pulls her toward screen-right instead of acting — the exact "held button becomes movement" confusion the touch audit repaired elsewhere. |
| evidence | Unguarded read at `games/side_scroll.gd:158` area versus the guarded sibling at `:277`; guard contract in `touch_ui.gd` `reserved_zone_hit()`. |
| owner_decision | Not required: applying the existing guard to the remaining path implements the already-accepted repair. |
| fix | Route the swim-branch press through the same `reserved_zone_hit()` guard, then sweep the remaining direct emulated-mouse reads in gesture-owned code to confirm each is inside a router-owned drag context. |
| surrounding_tests | `probe_touch_stress` and `probe_touch_router` legs extended to a swim stage; full suite. |
| acceptance | The swim branch ignores presses that begin in reserved zones, a touch-stress leg proves it, and no other unguarded read remains outside router-owned drags. |
| closure | Open as of 2026-08-26; guard absent on the swim branch. |
| relationships | Sibling of the repaired `MA-TOUCH-001` surface. |
| history | 2026-08-26: verified at `9a1754c1`; opened `CONFIRMED_OPEN`. |

## MA-CI-006

| Field | Value |
|---|---|
| id | `MA-CI-006` |
| title | Promotion accepts any successful probe run for dev's SHA — not the latest, not push-only — and nothing verifies that the run executed the expected trusted roster. |
| rule_ids | `DL-SAVE-05`, `DL-QA-07` |
| domain / zone | Release workflow / `.github/workflows/promote.yml` |
| source | 2026-08-26 code-refinement round workflow read at integration head `9a1754c1`. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: workflow logic is read exactly; no exploiting sequence has occurred. |
| reproduction | At `9a1754c1`, `promote.yml` queries workflow runs by `head_sha` and accepts success if any of up to twenty runs concluded green, regardless of event type or recency — a green `workflow_dispatch` re-run can therefore satisfy the gate even when a later push-triggered run at the same SHA went red; separately, nothing compares the run's executed probe list against the repository's trusted roster at that SHA, so a commit that shortens the roster gates itself. |
| child_impact | Indirect: a weaker gate raises the chance a regression reaches the stable APK bookmark on her phone. |
| evidence | `promote.yml` run-query and filter logic; roster lives only in `probes.yml`/`ci.sh` with no cross-check. |
| owner_decision | Not required for tightening run selection; owner awareness recommended since `.github/workflows/` is explicit-task-only territory — this finding authorizes exactly that task. |
| fix | Select the latest completed run for the SHA (prefer push events) and fail on red; emit the executed probe-heading count in the run and have `promote.yml` compare it to a committed expected-roster count so silent shrinkage fails closed. |
| surrounding_tests | Dry-run promotion against a known SHA; deliberately shortened-roster branch test proving the guard trips; workflow lint. |
| acceptance | Promotion refuses a SHA whose newest run is red and refuses a roster-count mismatch; a normal green promotion still passes. |
| closure | Open as of 2026-08-26; workflow unchanged. |
| relationships | Release aggregation is `MA-RELEASE-001`; roster hygiene is `MA-CI-004`. |
| history | 2026-08-26: confirmed by workflow read; opened `CONFIRMED_OPEN`. |

## MA-CI-007

| Field | Value |
|---|---|
| id | `MA-CI-007` |
| title | Probe infrastructure is copy-paste — 38 probes define a private frame-wait helper, most re-implement boot/skip-intro scaffolding, and wall-clock waits mix inconsistently with scaled engine time. |
| rule_ids | `DL-CODE-05`, `DL-QA-02` |
| domain / zone | Test fidelity / `scripts/probe_*.gd` suite-wide |
| source | 2026-08-26 code-refinement round probe-infrastructure sweep at integration head `9a1754c1`, decomposed from `MA-CODE-002`. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: counts exact; flake incidence is not quantified from run history in this round. |
| reproduction | At `9a1754c1`, 38 probe files define their own `func _frames(`; no probe shares a helper class (zero `class_name`/`preload` of a probe base); many trusted probes combine `Time.get_ticks_msec()` wall-clock windows with `Engine.time_scale` overrides and hundreds of `await process_frame` loops whose real duration varies with runner speed — the release gate's own history includes a red run caused by a fixed-frame sample of a timed reveal. |
| child_impact | Indirect: flaky or duplicated probes slow every repair cycle and erode trust in the gate that protects her build. |
| evidence | `grep -l "func _frames(" scripts/probe_*.gd \| wc -l` = 38; the 2026-08-05 release-gate history (fixed-four-frame `probe_opera` sample) as precedent; wall-clock sites across trusted probes. |
| owner_decision | Not required: probe-side refactor with unchanged assertions. |
| fix | Introduce one shared probe harness (boot, intro skip, frame/sim-time waits, isolated user-dir setup, snapshot helpers) and migrate probes mechanically a few per commit; prefer bounded semantic waits over wall-clock windows, following the `ff068db` repair pattern. |
| surrounding_tests | Suite green after each migration batch; migrated probes' transcripts byte-compared where deterministic. |
| acceptance | A shared harness exists, at least the trusted roster's top-twenty probes use it, no assertion weakened, and no fixed-frame timing sample remains in trusted probes. |
| closure | Open as of 2026-08-26; no shared harness exists. |
| relationships | Decomposed from `MA-CODE-002`; classification context `MA-CI-003`; roster context `MA-CI-004`. |
| history | 2026-08-26: counted at `9a1754c1`; opened `CONFIRMED_OPEN`. |

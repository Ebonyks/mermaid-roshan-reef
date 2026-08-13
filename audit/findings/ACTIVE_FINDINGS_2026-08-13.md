# Active master-audit findings register — 2026-08-13

This is the stable canonical-record companion to section 5 of
`audit/MASTER_AUDIT_2026-08-09.md`. It contains the 36 material P1/P2 items
that were non-terminal when this register was created. Stable records remain
here through later lifecycle transitions so their history is not erased.
Missing and externally blocked evidence is stated explicitly; no record below
promotes diagnostic output into acceptance or changes the lifecycle indexed by
the master audit.

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
| reproduction | At exact integrated dev/audit head `18b6150c`, run `python -B tools/audit_game_2d.py --strict` and inspect the active project/export inventory; this is a repository/runtime-structure check, so no device or aspect ratio can substitute for it. |
| child_impact | Mixed 2D/3D implementation keeps visual inconsistency, load cost, and older-device performance risk in the game used by this child. |
| evidence | Master audit sections 1 and 5.1; `tools/audit_game_2d.py`; 509 model/export files, 157 tracked and 352 active-untracked sidecars, 66 production-3D files, 74 probe-3D files, one 3D scene, and one 3D configuration; 14 stress controls pass and strict remains unsatisfied. |
| owner_decision | Owner decision 2026-08-09: the game-wide final authored and runtime medium is true 2D; relabeling spatial content does not satisfy it. |
| fix | Continue shrink-only conversion or retirement of active 3D sources, preserving approved 2D art, save compatibility, and protected originals. |
| surrounding_tests | GAME2D default, regression, strict, and stress; import/analyzer; relevant positive, passive, sibling, save/re-entry, teardown, and full trusted probes after each bounded conversion. |
| acceptance | All eleven GAME2D categories are zero and strict, import, focused, surrounding, and full probes pass at the same candidate. |
| closure | Open as of 2026-08-13; no zero-category result, strict pass, closure commit, device result, or acceptance date exists. |
| relationships | Parent game-wide debt for resolved `MA-DOLLS-001` and `MA-SEEK-001`; overlaps active `MA-VIS-002`, `MA-VIS-006`, and `MA-CODE-002`; documentation premise fixed by `MA-DOC-001`. |
| history | 2026-08-09: indexed from the full game-wide audit. 2026-08-12: Dolls, Seek, and bounded Opera sources reduced the baseline. 2026-08-13: retained `IN_PROGRESS` at 509/66/74 with strict unsatisfied. |

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
| title | Sky Lagoon still renders as one mural layer instead of independently staged true-Canvas depth layers. |
| rule_ids | `DL-MED-01`, `DL-LAY-01`, `DL-LAY-02`, `DL-QA-11` |
| domain / zone | Visual medium and staging / Sky Lagoon |
| source | Game-wide visual/source audit and Sky Lagoon runtime structure review. |
| severity | P1 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1 source/runtime plus V4 local diagnostic: one mural/spatial spread across twelve tiles remains; the new harness reliably observes it but does not repair it. Runtime/device acceptance is missing. |
| reproduction | From exact source `7391c53c`, run `scripts/probe_sky_lagoon_art.gd` under official Godot 4.7.1 Mobile/Speedy at 1280×720, then inspect the ordered arrival/route/animal/playground/action/castle/day/night frames and the live runtime ownership. The one mural/spatial treatment remains. Target-phone and M11 captures are missing. |
| child_impact | Flat staging weakens depth, route readability, and visual quality in a major area of the child's game. |
| evidence | Master audit sections 1.4, 4, and 5.1; current twelve-tile Lagoon source/runtime. Historical runs through exact parent `e6edf559` retain the predecessor 21-OK/44-FAIL/one-DONE result. Two-file diagnostic source `7391c53c` passes exact official-Godot full local CI in 1,402.3 seconds/all 64 and locally emits 20/20 ordered 1280×720 Mobile captures with 1,078 assertions, source SHA-256 `f28413263c0bedeed421fae6e9de4626095f03b6010bade8380ad7fb5aa07db9`, and GAME2D manifest SHA-256 `8c70b9aeaba5302322bdd44ca84d8a2b76fca053a091753e0e04676ee407fb00`. The frames still show the mural/spatial runtime. Exact-source run `31728755204` is overall green, but raw Sky output has 20 PASS rows followed by `GLOBAL|FAIL|rendering_method|gl_compatibility` and exit 1; continue-on-error masks the failed renderer proof and only PNGs upload. |
| owner_decision | Owner decision 2026-08-09 requires game-wide true 2D; `Sprite3D`, `SideScrollStage`, or filename-only relabeling cannot close the finding. |
| fix | Rebuild the promenade as owned `Sprite2D`/Canvas background, midground, interactive, character, and sparse foreground layers using approved art non-destructively. |
| surrounding_tests | Seam and per-screen coverage; unique pixel ownership; per-card occlusion; touch/world alignment; overdraw and Speedy budget; entry/exit/re-entry; sibling Lagoon routes; Mobile captures and device run. |
| acceptance | True Canvas differential layers pass seams, ownership, overdraw, touch, runtime visual review, and target-device review with no spatial fallback. |
| closure | Open as of 2026-08-13; source `7391c53c` fixes only diagnostic observation. An accepted layered implementation, authoritative capture, device result, closure commit, and date are missing. |
| relationships | Contributes to `MA-2D-002` and `MA-VIS-006`; evidence quality is constrained by `MA-VIS-003` and `MA-VIS-004`. |
| history | 2026-08-09: confirmed as a mural-layer defect. 2026-08-13: predecessor runs through `e6edf559` retain the obsolete 21 OK/44 FAIL diagnostic as history. Source `7391c53c` makes the current local diagnostic fail closed at 20/20 ordered captures and 1,078 assertions, but the frames still reproduce the one-mural/spatial product defect; lifecycle unchanged. |

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
| verification | V2/V3 contract plus V4 local Sky diagnostic: contract/stress behavior is approved, and the repaired Sky harness is deterministic, but the current report and observed product defects remain unresolved. |
| reproduction | Run the fresh-runtime visual audit at current source and the exact `7391c53c` Sky probe under Godot 4.7.1 Mobile 1280×720. Inspect every applicable adapter and all twenty ordered Sky frames; missing live adapters/captures and the observed readability/composition defects stay unresolved. Device acceptance is absent. |
| child_impact | Unseen cutoff, occlusion, hierarchy, or stale-art defects may reach the child despite green logic probes. |
| evidence | `audit/visual_design_report.json` and `.md`; current totals remain 16 FAIL, 17 REVIEW_OPEN, two MANUAL_OPEN, 86 COVERAGE_GAP, 32 PASS, and 94 NOT_APPLICABLE. Exact Sky source `7391c53c` passes full local in 1,402.3 seconds/all 64 and locally produces 20/20 ordered 1280×720 Mobile captures with 1,078 assertions and isolated-save restoration. Review exposes P1 preschool-readability risks (especially tiny frog/otter and subtle non-castle focus cues) plus P2 hare/squirrel/raccoon overlap or weak grounding and poor seesaw contact. Overall remote run `31728755204` succeeds, but its Sky step internally fails required-Mobile renderer identity after 20 PASS rows; the continue-on-error/PNG-only workflow grants no remote JSON or visual acceptance. |
| owner_decision | The accepted fail-closed contract from `3b7a7e66` and `fea916a8` must remain; missing evidence cannot be converted to PASS. |
| fix | Implement closed live-state adapters and same-process captures, then resolve every applicable failure, review, manual item, and coverage gap. |
| surrounding_tests | Visual stress-first suite; source/Git closure; immutable capture checks; per-target occlusion and touch; positive/negative/passive/sibling states; teardown/re-entry; Mobile aspects and device review. |
| acceptance | Every applicable item has accepted current live evidence and no unresolved FAIL, REVIEW_OPEN, MANUAL_OPEN, or COVERAGE_GAP remains. |
| closure | Open as of 2026-08-13; the repaired Sky diagnostic does not make its captured product pass. Current unresolved totals and named Sky defects are nonzero, and no all-applicable-pass result, device/owner acceptance, product-fix commit, or closure date exists. |
| relationships | Contract mechanics closed under `MA-VIS-005`; active evidence gaps affect `MA-VIS-002`, `MA-VIS-003`, `MA-VIS-004`, and Opera visual findings. |
| history | 2026-08-09: indexed as the fail-closed evidence gap. 2026-08-13: report remains 16/17/2/86/32/94. Source `7391c53c` repairs one diagnostic and exposes bounded current Sky defects without accepting them; lifecycle remains `CONFIRMED_OPEN`. |

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
| evidence | Master audit sections 5.1 and 12; focused Lagoon→Reef and route probes exist; complete no-cheat world traversal, device video, voice/touch trace, and save replay are missing. |
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
| evidence | Master audit section 5.1 and current touch probes; target-phone video/input trace, focus-loss result, and child-handed evidence are missing. |
| owner_decision | Primary play is one finger on an older Android phone; input ownership and focus-loss cleanup are binding. |
| fix | If device evidence fails, make the smallest bounded input-ownership/release cleanup repair without changing the visible one-finger grammar. |
| surrounding_tests | Press/hold/drag/release positive; second-finger negative; focus loss/pause/back; target disappearance; sibling touch routes; passive; teardown/re-entry; save unaffected. |
| acceptance | A recorded target-phone matrix passes hold, drag, multitouch rejection, focus loss, pause, release, and re-entry without stuck motion or duplicate actions. |
| closure | Pending as of 2026-08-13; target-phone result, device identifier, recording, acceptance commit, and date are missing. |
| relationships | Device gate contributes to `MA-PERF-001`, `MA-CHILD-001`, and `MA-RELEASE-001`. |
| history | 2026-08-09: implementation repair indexed as reported. 2026-08-13: remains `FIXED_PENDING_VERIFICATION` for lack of real-phone evidence. |

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
| title | The thirteen Castle-room career routes pass current machine gates but lack a matching current APK and external acceptance, and route cards obscure Roshan. |
| rule_ids | `DL-INT-12`, `DL-READ-05`, `DL-UI-03`, `DL-QA-12` |
| domain / zone | Navigation, composition, and release evidence / Castle rooms and all Opera careers |
| source | Runtime commit `09e5e356`, probe repair `ff068db`, local suites, diagnostic captures, historical Probe Suite runs, exact-parent dev Probe Suite `31722047536`, current local diagnostic-source suite, and integrated-predecessor Android dev run `31724927769`. |
| severity | P1 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3 full local plus exact-head remote and V4 diagnostic; external open. Runtime and readiness gates are green, while captures and external acceptance are not. |
| reproduction | From current audit source `7391c53c`, build and hash a matching APK before device testing; integrated-predecessor e6 APK run `31724927769` may be used only to reproduce prior route-card diagnostics, not current-source acceptance. Launch each of 13 careers only from its assigned Castle room, return to that room, test save/reward/pause/re-entry, and inspect nine route screens at native Mobile aspect. The prior 154×154 lower-center-card diagnostics obscure Roshan's lower body/tail; accepted device review is still missing. |
| child_impact | The new routes remove a reading-heavy hub, but card occlusion can hide Roshan and external gaps leave child discovery and phone usability unproved. |
| evidence | Runtime full local: 1463.4 seconds/64 probes; `ff068db` full local: 1379.3 seconds/64; pre-fix run `31678156887` remains red from four-frame reveal sampling. Historical CHG-023 head `51887315` passes local/remote machine gates. Exact parent `e6edf559` passes latest integrated dev Probe Suite `31722047536` (34m25s/63-of-63; document 36/six/316/34 active/36 retained; music 3m33s/42-of-42); earlier branch run `31719143975` is corroborating e6 history. Current two-file Sky source `7391c53c` changes no Opera/runtime behavior, passes full local in 1,402.3 seconds/all 64, and passes overall remote run `31728755204`; that run's Sky step internally fails renderer identity after 20 PASS rows. Workflow-run Android `31724927769` publishes the exact raw-checkout/package-source e6 APK (596,041,412 bytes; SHA-256 `66d16de5973dfe08947577b7cad59cfb40b0db87dde788d0d61d9c8b598ca17c`); no matching `7391c53c` APK is claimed. Historical Sky 21/44/DONE output remains predecessor-only. |
| owner_decision | Owner direction 2026-08-02 assigns all thirteen careers to exact thematic Castle rooms, makes Movie Lounge Racer's sole home, and forbids a central or hidden all-career lobby. |
| fix | Preserve exact room ownership and direct return; reposition/compose route cards without shrinking child-safe targets; build a matching current APK and complete external review. |
| surrounding_tests | Exact room mapping; hidden/off-room negatives; launch/return; save/reward/tombstones; voice/pointer; passive; pause/layers/focus; teardown/re-entry; sibling rooms; two aspects; APK/device/child/owner. |
| acceptance | A matching current APK and machine gates are green; route cards keep large targets without obscuring Roshan; phone/M11, child, owner, voice/listening, strict-2D, and authoritative visual gates pass. |
| closure | Pending as of 2026-08-13; current `7391c53c` is local- and overall-remote-machine green, but its remote Sky step fails renderer identity and no matching APK exists. Phone/M11, child, owner, voice/listening, strict-2D, and accepted-visual evidence are missing, warning/capture diagnostics remain, and P2 card composition is unresolved. |
| relationships | Builds on `MA-OPERA-010` and `MA-OPERA-011`; visual capture gap `MA-OPERA-004`; release gate `MA-RELEASE-001`; rollback `CHG-027`. |
| history | 2026-08-12: `09e5e356` implemented exact room routes and local evidence. 2026-08-13: `ff068db` repaired readiness sampling; historical heads passed bounded remote machine gates, and e6 dev run `31722047536` plus Android run `31724927769` provide the latest integrated-predecessor machine/build pair. Current Sky diagnostic source `7391c53c` passes local CI without changing Opera and completes overall remote run `31728755204`, whose Sky subprocess fails required-Mobile renderer identity; its matching APK and all external/visual gates remain open. |

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
| reproduction | Build and hash an APK from current audit source `7391c53c`, then install it on the intended older Android phone and Lenovo Tab M11 and run representative cold load, traversal, Castle/Opera, Lagoon, combat, particles, pause/re-entry, and touch-latency traces at native aspect. The available e6 APK is integrated-predecessor-only; current matching build and measurements are missing. |
| child_impact | Hitches, heat, memory pressure, slow loads, or delayed touch can make the game unusable for its only intended player. |
| evidence | Exact parent `e6edf559` passes latest integrated dev Probe Suite `31722047536`; current `7391c53c` passes exact official-Godot local CI in 1,402.3 seconds/all 64 and overall remote run `31728755204`, although the remote Sky step fails required-Mobile renderer identity. No matching APK exists. Android run `31724927769` publishes only the exact raw-checkout/package-source e6 APK (596,041,412 bytes; SHA-256 `66d16de5…ca17c`). Speedy/mobile budgets exist, but P50/P95/P99 frame time, hitch, memory, thermal, load, and touch-latency data are missing. |
| owner_decision | Mobile renderer is authoritative; Speedy is default; stable 30 fps and transparent-overdraw limits are binding for the target hardware. |
| fix | Produce and measure a matching current APK, then optimize only the bounded hotspots demonstrated by traces while preserving art and behavior. |
| surrounding_tests | Cold/warm load; long session; representative high-cost zones; frame-time percentiles; hitches; RAM/VRAM; thermal; touch latency; focus/pause/re-entry; save integrity; visual comparison. |
| acceptance | The exact release candidate meets documented design thresholds on required devices with retained touch, save, visual, and gameplay behavior. |
| closure | Blocked as of 2026-08-13; no matching `7391c53c` APK, device matrix, measurements, accepted result, closure commit, or date exists. |
| relationships | Blocks `MA-RELEASE-001`; device touch overlaps `MA-TOUCH-001`; asset/performance risks include `MA-ASSET-004` and `MA-2D-002`. |
| history | 2026-08-09: V0 device gap indexed. 2026-08-13: integrated predecessor `e6edf559` gained a matching dev APK; current `7391c53c` is local- and overall-remote-machine green but has a failed remote renderer diagnostic and no matching APK or target-device matrix, so the item remains `BLOCKED_EXTERNAL`. |

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
| reproduction | Build and hash a matching APK from current audit source `7391c53c`, install it on the target device, and start a private fresh-save five-minute session; give no reading or route instructions and record only safe, consented observations of discovery, touch, recovery, exit, and progress. The available e6 APK is integrated-predecessor-only; current build and session evidence are missing. |
| child_impact | Machine-green mechanics may still be undiscoverable, confusing, tiring, or dependent on adult help for the intended child. |
| evidence | Exact parent `e6edf559` passes latest integrated dev Probe Suite `31722047536`; current `7391c53c` passes local official-Godot CI and overall remote run `31728755204`, although the remote Sky step fails renderer identity, and no matching APK exists. Android run `31724927769` publishes only the exact raw-checkout/package-source e6 APK. No current observed session, behavior log, comprehension result, or installed-device record exists. |
| owner_decision | The game is designed for one specific non-reading four-year-old, one finger, short sessions, no fail states, and no lost progress. |
| fix | After machine/device readiness, conduct the smallest safe private observation and repair only concrete comprehension or trapping defects it reveals. |
| surrounding_tests | Fresh save; visible/spoken objective; passive no-win; wrong-action recovery; one-finger navigation; reward; pause/exit; save/re-entry; sibling route; no adult/debug intervention. |
| acceptance | The observed child independently discovers, acts, recovers, receives feedback, exits, and retains progress during the defined session without distress or reading. |
| closure | Blocked as of 2026-08-13; no matching `7391c53c` APK, consented session, observation record, accepted result, closure commit, or date exists. |
| relationships | Depends on `MA-PLAY-001`, `MA-ACCESS-001`, `MA-TOUCH-001`, and `MA-PERF-001`; blocks `MA-RELEASE-001`. |
| history | 2026-08-09: V0 child-evidence gap indexed. 2026-08-13: no observed exact-candidate session; lifecycle remains `BLOCKED_EXTERNAL`. |

## MA-RELEASE-001

| Field | Value |
|---|---|
| id | `MA-RELEASE-001` |
| title | The current audited source is exact-local and overall-remote-machine green but has a masked remote Sky renderer failure, no matching APK, and no external release evidence. |
| rule_ids | `DL-SAVE-05`, `DL-QA-04`, `DL-QA-05`, `DL-QA-10` |
| domain / zone | Release readiness / whole game |
| source | Full local CI, GitHub Actions history, exact-head Android dev build, audit scorecard, and missing external-gate inventory. |
| severity | P1 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3 predecessor exact local/remote/build plus V4 current exact-local/remote machine evidence. Source `7391c53c` is local- and overall-remote-machine green; its nonblocking Sky step internally fails required-Mobile renderer identity, while a matching APK and release acceptance remain open. |
| reproduction | From exact source `7391c53c`, preserve the completed local/remote logs, repair the protected runner/renderer and blocking JSON Sky gate, build and hash a matching APK, then execute device, child, owner, voice/listening, visual, strict-2D, and re-audit gates. Historical `18b6150c` evidence plus exact-parent e6 Probe Suite/Android evidence remain predecessor evidence, not a matching current build. |
| child_impact | Shipping without these gates risks performance, comprehension, identity, audio, visual, or save defects on the child's actual device. |
| evidence | Runtime `09e5e356` full local 1463.4 seconds/64; `ff068db` full local 1379.3 seconds/64; failed run `31678156887` retained. Historical `51887315` and parent `e6edf559` pass their exact remote machine gates; latest integrated e6 dev run `31722047536` has probes 34m25s/63-of-63, document authority 36 tests/six stress/316 parity/34 active and 36 retained records, and music 3m33s/42-of-42. Earlier branch run `31719143975` is corroborating e6 history. Current two-file source `7391c53c` passes exact official Godot 4.7.1 full local in 1,402.3 seconds/all 64 and locally emits 20/20 ordered 1280×720 Sky diagnostic frames spanning all five live animals with 1,078 assertions, isolated save/restoration, probe SHA-256 `f28413263c0bedeed421fae6e9de4626095f03b6010bade8380ad7fb5aa07db9`, and GAME2D manifest SHA-256 `8c70b9aeaba5302322bdd44ca84d8a2b76fca053a091753e0e04676ee407fb00`. Source-head run `31728755204` completes overall SUCCESS (probes 40m05s, trusted 17m50s/63 headings; music 3m38s/42-of-42), but raw Sky output has 20 PASS rows then `GLOBAL|FAIL|rendering_method|gl_compatibility`/exit 1; continue-on-error masks it and only PNGs upload. Android run `31724927769` publishes only the exact raw-checkout/package-source e6 APK (596,041,412 bytes; SHA-256 `66d16de5973dfe08947577b7cad59cfb40b0db87dde788d0d61d9c8b598ca17c`); no matching `7391c53c` APK or external acceptance exists. |
| owner_decision | Release requires exact Godot 4.7.1-stable, green integration, save compatibility, protected-asset compliance, and applicable external acceptance; diagnostic captures do not authorize release. |
| fix | Preserve exact-head build provenance, resolve warning/capture diagnostics, build/hash/publish an APK for the current candidate, then complete all external gates with that matching APK and repair only concrete failures before promotion. |
| surrounding_tests | Exact local/remote CI; import/analyzer; all trusted probes; GAME2D; visual audit; APK install/upgrade/save; device matrix; child session; owner art/authority; exact voice/listening; clean status and re-audit. |
| acceptance | One exact candidate has green required machine gates, matching APK, resolved diagnostic classification, target-device performance/touch, child comprehension, owner/visual/audio acceptance, strict-2D satisfaction, and clean re-audit. |
| closure | Pending as of 2026-08-13: exact `7391c53c` full local and overall remote machine suite are green, but the remote Sky renderer diagnostic fails and matching APK plus device/child/owner/listening/strict-2D/accepted-visual evidence are missing. Sky product/capture-workflow debt remains, and no release closure commit/date is recorded. |
| relationships | Aggregate blocker for `MA-2D-002`, `MA-VIS-006`, `MA-PLAY-001`, `MA-ACCESS-001`, `MA-TOUCH-001`, `MA-OPERA-012`, `MA-PERF-001`, `MA-CHILD-001`, and `MA-AUDIO-001`. |
| history | 2026-08-12: runtime and predecessor local/remote evidence improved. 2026-08-13: historical `18b6150c` passed Probe Suite/Android dev; CHG-029 and later CHG-023 maintenance established/verified document controls through parent `e6edf559`; e6 dev Probe Suite `31722047536` and Android `31724927769` then supplied the latest integrated-predecessor machine/build pair. Sky diagnostic source `7391c53c` passed exact local CI and overall remote machine gates, while its nonblocking remote Sky renderer diagnostic failed and source-head APK/external acceptance remained open. Release stays `FIXED_PENDING_VERIFICATION`. |

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
| title | Forty-two deterministic area cues lack required human listening, voice-mix, mono, transition, and M11 acceptance. |
| rule_ids | `DL-SND-06`, `DL-SND-07`, `DL-SND-09`, `DL-QA-04` |
| domain / zone | Music and mix / 42 game-wide area cues |
| source | Deterministic score/render/manifest audit, routing probes, local CI, and pinned Windows jobs. |
| severity | P2 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
| verification | V3 partial: hashes, codec, loop/import, loudness, peak, seam, routing, and 42/42 machine delivery pass; listening/device evidence is open. |
| reproduction | On the exact candidate with matching APK, listen to two wraps of every cue, transitions, speech ducking, music-off restoration, and mono fold-down on headphones/speaker and Lenovo Tab M11. The human/device matrix is missing. |
| child_impact | A technically valid loop can still be tiring, mask family voices, click at transitions, disappear in mono, or play poorly on the child's hardware. |
| evidence | `assets_src/audio/music/area_music_scores.json`; `assets/audio/music/area_music_manifest.json`; 48 kHz stereo OGG and measured manifests; historical runs through `31710377034` preserve music 42/42. Integrated-predecessor dev run `31722047536` at exact `e6edf559` finishes music 42/42 in 3m33s; current source-head run `31728755204` finishes music 42/42 in 3m38s. Earlier branch run `31719143975` is corroborating history. Human two-wrap/style, intelligibility/ducking, mono, music-off, and M11 evidence is missing. |
| owner_decision | Machine evidence never substitutes for human listening; protected voices remain authoritative and must stay intelligible. |
| fix | Complete the listening matrix and make only bounded score/mix/transition repairs demonstrated by it, preserving deterministic sources and manifests. |
| surrounding_tests | 42/42 deterministic rebuild; source/render/import hashes; codec/loop/seam/loudness/peak; named routing; hard cuts; voice ducking; music-off/on; mono; two wraps; M11 start/loop/performance. |
| acceptance | All 42 pass human style/two-wrap listening, voice intelligibility/ducking, mono, music-off transitions, and M11 playback/performance while machine evidence remains exact. |
| closure | Pending as of 2026-08-13; human/device listening evidence, accepted result, closure commit, and date are missing. |
| relationships | Exact objective voice gaps are `MA-ACCESS-001` through `003`; aggregate release gate is `MA-RELEASE-001`. |
| history | 2026-08-12: deterministic 42/42 repair and remote Windows verification completed. 2026-08-13: exact-head Windows remains 42/42; lifecycle stays `FIXED_PENDING_VERIFICATION` for listening/device evidence. |

## MA-CODE-001

| Field | Value |
|---|---|
| id | `MA-CODE-001` |
| title | `scripts/main.gd` remains 8,647 lines, far above the extraction-only target below 2,500 lines. |
| rule_ids | `DL-SAVE-03`, `DL-QA-01`, `DL-QA-02` |
| domain / zone | Architecture and maintainability / `ReefMain` |
| source | Static line-count and architecture audit at runtime commit `09e5e356`. |
| severity | P2 |
| lifecycle | `CONFIRMED_OPEN` |
| verification | V1: exact line count and target are confirmed; remaining extraction boundaries are not completed. |
| reproduction | At runtime commit `09e5e356`, count `scripts/main.gd` lines and inspect state ownership; it is 8,647 lines versus the documented extraction-only target below 2,500. Device/aspect are not applicable to the count. |
| child_impact | Large coupled code raises regression risk for saves, touch, navigation, and activities when the child's game changes. |
| evidence | `scripts/main.gd`; master audit sections 1.3, 4.7, and 5.2; satellite scripts exist, but HUD/environment/aquatic/galaxy/kart/level-2 glue remains. |
| owner_decision | Refactor by mechanical extraction only: shared state stays on main, one bounded owner/tick per commit, and failed probes require revert rather than probe weakening. |
| fix | Continue small behavior-preserving extractions into typed satellites until the target is met, with no opportunistic rewrite. |
| surrounding_tests | Parser and inference lint; exact before/after focused probes; passive; save/load/recovery/re-entry; UI/touch; sibling systems; full trusted probes and exact CI for each extraction. |
| acceptance | `main.gd` is below 2,500 lines through reviewed mechanical extractions, behavior/save contracts are unchanged, and all required gates remain green. |
| closure | Open as of 2026-08-13; line count remains 8,647 and no complete extraction sequence, final gate result, closure commit, or date exists. |
| relationships | Coupled structural risks are `MA-CODE-002`; broad medium migration is `MA-2D-002`; release risk aggregates under `MA-RELEASE-001`. |
| history | 2026-07-18: extraction-only target documented. 2026-08-13: current audited count remains 8,647; lifecycle `CONFIRMED_OPEN`. |

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
| history | 2026-08-09: grouped structural risks confirmed. 2026-08-12: speculative Chef caller hardening explicitly excluded. 2026-08-13: lifecycle remains `CONFIRMED_OPEN`. |

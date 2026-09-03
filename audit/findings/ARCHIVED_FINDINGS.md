# Archived canonical findings

_Archive tier of the findings register (opened 2026-09-01). A canonical
record moves here verbatim — same heading, same eighteen fields — in the
commit that makes its lifecycle terminal (`VERIFIED_FIXED`,
`DISMISSED_NOT_A_DEFECT`, `DISMISSED_NOT_IN_PROJECT`, `SUPERSEDED`,
`DUPLICATE`), and its section-5 link in `audit/MASTER_AUDIT_2026-08-09.md`
follows it here. `tools/audit_document_authority.py` fails a terminal record
left in the active register (DOC082), an open record placed here (DOC081), a
record present in both files (DOC080), and a section-5 link that points at the
wrong register (DOC083). Archived records are never edited except to append a
dated `history` line; a regression reopens the item as a NEW finding with its
own ID rather than resurrecting the archived record._

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

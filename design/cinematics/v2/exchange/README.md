# Exchange — append-only requests and receipts

Actual images/clips live in the established private videos repository.
This folder stores metadata only. Historical attempts retain their original
schema, contents and limitations; they are not retroactively valid new requests.

New attempts: `attempts/<SHOT_ID>/A00N/{REQUEST,RETURN,REVIEW}.json`.
Use the revised templates. Before dispatch, publish immutable request/card/prompt
and image hashes, exact owner opening approval, recipient ACCESS_ACK and any
attempt-cap exception. A RETURN echoes request ID/hash. REVIEW records exact
frame index, seconds, measured fps, observed defect, expected state and one repair.

Coverage is COV-* and never fulfills an acted SHOT-* automatically. Attempt numbers
continue existing lineage; a revision does not reset the cap. Do not overwrite
rejected bytes or fabricate missing historical receipts. Planning receipt !=
still authorization != motion readiness != delivery acceptance.

Cold-start construction (2026-09-19): each REQUEST is self-contained
(`construction: cold_start`, 2–3 files, verbatim identity, stop after return).
Do not batch shots or carry prompt memory. See
[../SHOT_CONSTRUCTION.md](../SHOT_CONSTRUCTION.md) and
[COLD-START-20260919/START_HERE.txt](COLD-START-20260919/START_HERE.txt).


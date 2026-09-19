# V2 planning schema and canonical export

CARD.json uses `reef.grok.shot-plan.v2`, not an Imagine packet. A draft can
record missing inputs but cannot claim motion readiness.

| Field | Meaning |
|---|---|
| exact_cast / cast_instances | Registered identities, instance IDs, start/end visibility; proposed staging until approved. |
| room_state / end_room_state | Concrete fixture maps, not generic set-later notes. |
| camera / causal_chain / end_state | Physical address, one verb, contact, consequence and endpoint. |
| preparation_references | Immutable source URLs/full hashes, not I2V bindings. |
| binds | Proposed IMAGE_1..IMAGE_4 slots; missing inputs are null with missing_reason. |
| opening_candidate / approval_receipt | Exact candidate/owner record or null; empty coverage stays separate. |
| blocking_findings / hold / attempts_used | Explicit cumulative blockers and caps. |
| canon_sha256 / prompt_sha256 | Current fingerprints; stale records invalidate readiness. |
| request | Path/hash of newly published execution request, or null for a plan. |

Planning PASS is distinct from `--require-ready`. Missing approval never passes
the latter. `tools/compile_v2.py` exports one ready card into canonical
`imagine-shot-packet-v2`; its output still needs the canonical Imagine audit.

Separate `preparation/*/REQUEST.json` records may authorize ONE candidate still
after recipient ACCESS_ACK. They bind the plan, brief, still prompt and 2–4
source images; respect cumulative caps/HOLD; explicitly forbid motion and stop
for owner approval. These are not the motion plan's `still_attempt_allowed` flag.

New REQUEST hashing uses sorted compact UTF-8 JSON excluding request_sha256.
It binds the plan fingerprint, prompt, all image hashes, attempt and immutable URL.
RETURN echoes request ID/hash. Owner receipt identifies actor, timestamp, source
URL, accepted opening hash and plan fingerprint. Historical schema/receipts are
preserved but cannot authorize new execution.

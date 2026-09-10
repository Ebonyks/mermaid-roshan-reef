# Day One Grok Handoff 2

This is the 2026-09-09 continuity repair commission, separate from the historical third-pass archive. Start with the [footage audit](../../../audit/GROK_HANDOFF_2_FOOTAGE_AUDIT_2026-09-09.md) and [protocol](../../../design/GROK_HANDOFF_2_CONTINUITY_PROTOCOL_2026-09-09.md).

**47 repair jobs; 23 retain candidates needing review; four obsolete events remain omitted.** The archive includes actual approved references, all-scene narrative boards, selected-edit cut boards, six fresh native-sample sheets, exact source hashes and the old decisions. Boards and rejected footage are review-only, never generator pixels.

- [Major findings and evidence](FINDINGS.json)
- [Every shot and its repair card](SHOT_REPAIR_QUEUE.json)
- [Shared room/identity/state locks](CONTINUITY_LOCKS.json)
- [Approved source reference index](REFERENCE_INDEX.json)
- [73-file native footage inventory](FOOTAGE_INVENTORY.json)
- [Fresh sample timecodes and hashes](NATIVE_SAMPLE_EVIDENCE.json)
- [Archive manifest and payload digest](HANDOFF_PACKET.json)

## Operator order

1. Pilot C07-S01, S02 and S06 using the same approved playroom. Empty-room S01 binds no characters. Keep exactly two rescue pins for S06; no swing, basket search or wing trail.
2. Pilot C05-S05, C06-S01 and S02 with the same blue-lavender seahorse and coral pedestal. Discovery keeps the obstruction lodged. The player-caused pull removes it once; the next shot inherits that accepted endpoint.
3. Repair remaining Bathroom/Pool/Art/arena sequences, comparing incoming and outgoing cuts as well as the local clip. Update dependent endpoints when a parent changes.
4. Build recaps from accepted clean room endpoints only. Keep C13's unresolved event/owner decisions explicit.

Each `shots/<id>/SHOT_PACKET.json` is a **draft repair specification** based on the V1 card fields, with a separate draft `PROMPT.txt`. Do not paste a draft prompt into Grok until it has an approved complete opening, two to four reviewed image bindings, and passes the existing Imagine execution gate. Null IMAGE_1 is intentional: a room plate is not a completed shot opening. No generated board or rejected frame is promoted by this archive.

## Three separate claims

ARCHIVE_COMPLETE is established only by the subsequent immutable remote-verification record. GENERATION_READY is **false**. DELIVERY_ACCEPTED is **false**. No new footage is generated or accepted here. The full-frame cinematic rule remains unchanged; Grok output is motion/editorial reference.

Run `python -B tools/audit_grok_handoff_2.py assets_src/cinematics/day_one_grok_handoff_2_2026-09-09` from the repository root. `--require-ready` intentionally rejects this draft queue. A finished V1/V2 execution packet must pass `tools/audit_imagine_handoff.py --require-ready`; final delivery must independently pass `tools/audit_cinematic.py` and human/device gates.

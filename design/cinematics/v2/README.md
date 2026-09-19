# Grok cinematic handoff v2

Docs-only protocol. **No media in this tree.** Bytes stay in [Ebonyks/mermaid-roshan-grok-videos](https://github.com/Ebonyks/mermaid-roshan-grok-videos).

v2 exists because Revision 4’s builder packet (`grok_builder_2026-09-14`) is a **library**, and Grok was handed the library. Extra cast, unicorn-horn tiaras, bearded Daddys, and clean rooms are what you get when 306 references and 36 prompts share one window, and when IMAGE_1 stills already contain people.

Parent: Revision 4 Codex packet + `design/templates/IMAGINE_SHOT_CARD_V2.md` + `design/GROK_MASTER_HANDOFF_FORMULA_2026-08-30.md` + A001/A002 audits.

## Two layers (do not mix)

| Layer | Lives here | Grok may see it? |
|---|---|---|
| **Canon** — identity, empty plates, fixture dirty/clean, knockouts, data gaps | `canon/` | Only the rows named on the current CARD |
| **Execution** — one shot, 2–4 binds, one prompt | `shots/<id>/CARD.json` + `PROMPT.txt` | **Yes — this is the job** |
| **Library** — DATABASE.json, 332 clips, 90 job proposals, boards | private archive / Revision 4 packet | **Never** |

`START_GROK.txt` is the only builder brief. It is short on purpose.

## Round trip

```text
Codex compiles CARD.json from canon + queue
        ↓
Owner approves first frame (opening_approved=true, hash locked)
        ↓
Grok animates THAT still with PROMPT.txt (action only)
        ↓
Grok returns hashes in exchange/attempts/<id>/A00N/RETURN.json
        ↓
Codex/owner REVIEW.json (t0, contact span, t_end)
        ↓
REGENERATE | HOLD | ROUGH_REFERENCE_CANDIDATE
```

Three attempts then stop. Missing plates become a Codex ticket (`canon/DATA_GAPS.json`), not another Grok roll.

## Status

`ARCHIVE_COMPLETE` for this protocol: this folder.
`GENERATION_READY`: false (no owner-approved first frames).
`DELIVERY_ACCEPTED`: false.

A002 bathroom-sink is a **motion sketch**, not a lock. Late extra-cast at t55 revoked the earlier rough hold.

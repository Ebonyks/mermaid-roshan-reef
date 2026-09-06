# Day One V4 + C14 — 3-set stage (awaiting first-frame approval)

**Status:** `STAGED_AWAITING_FIRST_FRAME_APPROVAL`  
**GENERATION_READY:** false · **DELIVERY_ACCEPTED:** false

Publication: [GROK_HANDOFF_PUBLICATION_2026-09-05.md](https://github.com/Ebonyks/mermaid-roshan-reef/blob/d9e44a12761f76c910779eb5803721e8aedabae7/design/GROK_HANDOFF_PUBLICATION_2026-09-05.md)  
Content commit: `1ec777f76fcdd76cbb4e31cce6a59dfb7d1ddfc0`

## Policy (do not skip)

> Approve exact first-frame **filename + SHA-256** per shot. Sol `RECOMMEND_APPROVAL` never authorizes generation.  
> After approval: bind 2–4 named images, one role each; one job = one shot; ≤1 camera move.  
> Never bind boards, endpoint candidates, contact sheets, or HUD captures as generation pixels.

## 3 sets (22 jobs)

| Set | Scope | Jobs |
|-----|--------|-----:|
| **SET1** | P0 hall route + arena + suds/rainbow-friend finale | 6 |
| **SET2** | P1 rooms, pool, rescue wingbeat, art desk | 10 |
| **SET3** | C14 team cleanup coda (31s) | 6 |

### SET1
`D1-C11-S01` `D1-C11-S02` `D1-C11-S03` `D1-C11-S04` `D1-C13-S04` `D1-C13-S05`

### SET2
`D1-C01-S04` `D1-C03-S02` `D1-C03-S03` `D1-C03-S04` `D1-C05-S01` `D1-C05-S03` `D1-C06-S05` `D1-C08-S06` `D1-C09-S03` `D1-C10-S05`

### SET3
`C14-S01` … `C14-S06`

## Staged artifacts

- `THREE_SETS/SET*/<shot_id>/` — SHOT_PACKET, PROMPT, README, FRAME_*, OPENING_CANDIDATE.png, CARD_STATUS.json
- `first_frames/` — 22 Sol-recommended openings (SHA verified)
- `V4_C14_THREE_SETS_WORKPLAN.json` — machine-readable plan + approval checklist

## How to approve (then generate)

Reply with one of:

1. `approve all SET1` / `approve all SET2` / `approve all SET3` / `approve all`
2. Or per shot: `approve D1-C11-S01` (uses staged candidate filename+hash)
3. Or reject with alternate filename

On approval, Grok will run image-to-video from the approved opening, then upload clips to GitHub.

## C13-S05 hard constraints (when approved)

- Giant dust body/face/ears **fully gone** by final hold
- Cast: Roshan + Daddy + Baby Eagle + Rumi + **one** tiny rainbow friend only
- Arena keeps **two shell-topped side windows**

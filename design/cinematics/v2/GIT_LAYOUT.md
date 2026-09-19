# Git layout

## This branch (`codex/grok-handoff-v2`)

Long-lived cinematic protocol. Do not cut a new branch per night of generation.

```text
design/cinematics/v2/          protocol + execution cards (this)
design/handoffs/2026-09-18-grok-handoff-v2/   pointer for Codex
design/audit_impacts/grok-handoff-v2.json
```

No MP4, no PNG, no JPG here.

## Other repos / branches

| What | Where |
|---|---|
| Revision 4 library (DATABASE, 139 media refs, boards) | private `mermaid-roshan-grok-videos` folder `grok_builder_2026-09-14/` |
| A001 / A002 motion sketches | private repo `videos/queue-a00N-*` + releases `grok-queue-a00N-*` |
| A001/A002 audit notes | `design/handoffs/2026-09-16-grok-queue-a00N/` on this history |
| Game runtime flats | `assets/flats/...` — source art, **not** a Grok bind unless listed on a CARD |
| Forbidden | `assets_src/cinematics/grok_*` binaries in the game tree |

## Exchange records

```text
design/cinematics/v2/exchange/attempts/<SHOT_ID>/A00N/
  REQUEST.json     hashes of CARD + binds (no pixels)
  RETURN.json      clip/still sha256 + private release URL
  REVIEW.json      knockout / regenerate / hold
```

If a still must be shown to the owner, host it on the private repo or a release. Commit only `sha256` and URL.

## Stale policy

Changing `canon/IDENTITY.json` or a location plate hash marks every CARD that binds it `opening_approved=false` and `generation_allowed=false` until the first frame is re-reviewed.

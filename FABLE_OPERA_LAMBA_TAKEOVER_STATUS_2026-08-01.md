# Fable status — Lamba takeover (2026-08-01)

Companion to FABLE_OPERA_LAMBA_TAKEOVER_HANDOFF_2026-08-01.md. Fable verified
the Codex delivery on `codex/opera-art-regeneration` (probe_opera_2d: ALL OK,
twelve careers including the Lamba magician act; on-screen copy says
"Lamba" / "LAMBA CHASE"; vo keys `op_magician_vanish` /
`op_magician_bunny_chase` retained as compatibility aliases) and executed the
completable portion of the four takeover tasks. Tasks 1 and 2 are
owner-gated; everything the owner needs to unblock them is below.

## Task 1 — voice recordings: READY FOR OWNER, audio untouched

`assets/audio/voices/` was not modified. The two live clips still say
"bunny-fish" while the screen says Lamba. To close the gap the owner picks
either path:

**Path A — family recordings (handoff-preferred).** Record the two lines and
drop them at these exact paths (OGG Vorbis; the pipeline standard is
-16 LUFS / -1.5 dBTP, but any clean phone recording is fine — the game
plays whatever is at the path):

| Path | Line to record |
|---|---|
| `assets/audio/voices/roshan_op_magician_vanish.ogg` | "Hold the wand to make Lamba vanish!" |
| `assets/audio/voices/roshan_op_magician_bunny_chase.ogg` | "The imp captain hid Lamba! Bop the crew to the stage!" |

No code change is needed; the runtime already loads these paths.

**Path B — approved TTS re-render.** Say the word and Fable runs the house
pipeline (the two LINES entries are already staged in
`tools/make_voices.py` with the old text; they will be updated to the Lamba
wording first):

```bash
python tools/make_voices.py --only roshan_op_magician_
```

## Task 2 — legacy 3D swap: INVENTORIED, awaiting the approved Lamba model

No owner-approved Lamba 3D model or fallback exists yet, so nothing was
replaced. The complete reference inventory for the one-commit swap:

- `assets/opera/jobs/magician/opera_magician_bunnyfish.glb` — the actor
  itself (headless-probe-only path; normal play never builds it).
- `scripts/opera_act.gd` — 11 sites: loader at :4084
  (`_job_art("magician/opera_magician_bunnyfish.glb", ...)`), spoken lines
  :4102/:4201, HUD objective strings :6948/:6952, comments :7/:215/:222/
  :4091/:4131/:4305.
- `scripts/opera_house.gd` — :70, the ACTS intro voice line.
- `scripts/probe_opera.gd` — :516/:517/:531, legacy regression wording.
- `scripts/probe_art_manifest.gd` — :82/:85, manifest object names
  (`bunny_fish`, `giant_bunny_fish`) — update ONLY after the new resource
  exists; the probe must never be weakened to accept a missing actor.

Swap plan (single commit when the model is approved): place the Lamba GLB at
a new `opera_magician_lamba.glb` path, point :4084 at it with the old path
as load-fallback, update the strings/comments above, then the two probe
files, run `probe_opera` + `probe_art_manifest` + `probe_opera_2d`. Save
keys and act timing are untouched by any of this (the swap is art + text).
Note: the 2026-07-26 "2D sprites only" owner decision means the owner may
instead choose to retire the GLB with a flat Lamba standee — both options
preserve the probe contract.

## Tasks 3 and 4 — sequenced, not started

Alias renames (`bunny_fish_*` asset IDs, `op_magician_bunny_chase` vo key →
`lamba` names with compatibility shims) and the art-manifest probe update
happen together in one commit only after Task 1's audio and Task 2's model
both land, per the handoff.

## Validation on this branch

- `probe_opera_2d`: ALL OK (re-verified by Fable in this worktree).
- `ci.sh`: fails only on upstream `dev` issues outside opera scope (fairy
  pond / sky lagoon visual design, stale castle interaction hashes) —
  matches the Codex audit note and Fable's earlier run on the rebuild
  branch. Opera-scoped probes are green.

# Mermaid Roshan Luna editorial recut

This package contains the completed DaVinci Resolve recut of the Mermaid Roshan
opening. The final picture is a 39.125-second, 1280×720, 24 fps H.264 sequence
with a bespoke 48 kHz stereo mix. Downloaded source clips were read in place and
were not altered.

## Primary deliverables

- `mermaid_roshan_luna_recut_v1_resolve.mp4` — final Resolve render.
- `Mermaid_Roshan_Luna_Editorial_Recut_2026-08-23.drp` — portable Resolve project.
- `luna_recut_v1_final.fcpxml/Info.fcpxml` — editable final timeline exchange.
- `luna_recut_audio_mix.ogg` — standalone compressed mix.
- `luna_recut_audio_mix_resolve.wav` — 24-bit PCM timeline master.
- `final_contact_sheet.png` — visual continuity overview.
- `editorial_report.md` — arrangement, reasoning, and improvement notes.
- `stress_test.json` — machine-readable final validation.

The live Resolve library project is named
`Mermaid Roshan - Luna Editorial Recut 2026-08-23 v5`; the suffix records the
conform iterations that were stress-tested. Its final timeline is
`MERMAID_ROSHAN_LUNA_RECUT_V1_24FPS`.

## Editorial policy

The cut uses three one-second Cross Dissolves only for story/geography changes.
Action, reaction, and eyeline edits remain hard cuts. Original clip audio is not
used. The A1 mix contains the accepted `home.ogg` music plus the eight bespoke,
nonvoice stems authored in the companion sound-design package. No voice was
generated, altered, or substituted.

## Rebuild order

With Resolve open and its installed loopback bridge running:

1. `python edit_plan.py`
2. `python build_resolve_timeline_native.py`
3. `python render_recut_audio.py`
4. `python import_recut_audio.py`
5. Apply the three marked transitions in Resolve.
6. `python render_resolve_recut.py`

`build_resolve_timeline_native.py` intentionally interprets Resolve's
`endFrame` as exclusive. The preflight stress test proved that subtracting one
frame creates gaps and black flashes at transitions.

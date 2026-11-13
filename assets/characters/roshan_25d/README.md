# Mermaid Roshan 2D atlas contract

**Mermaid Roshan 3.0 identity sources.** This approved RGBA family supplies
existing Canvas atlas playback and source artwork for the Rigby2D authoring
workflow. Keep source pixels and provenance. Use derived, versioned cutouts
and export data under `DL-MED-02` and `DL-MOT-17`. Review the assembled
actor as one figure at play scale. Existing spatial player staging remains
migration debt.

Retired 3D **resource blobs** live only on archive branch
`codex/deprecated-resources-roshan-20260809` (verified archive head
`9329d9a6`). Ledger-classified textual pipeline, work-order, audit, and
decision history remains tracked on the active branch as non-executable
`HISTORICAL_EVIDENCE`; it preserves provenance and explains retired work but
cannot authorize a model pipeline or runtime dependency. The archive branch is
preservation evidence, not a runtime fallback, rollback target, merge source,
or alternate production authority.

All runtime textures are RGBA PNGs with power-of-two dimensions and 256x256
cells. `scripts/player.gd` is the source of truth for frame selection.

## Runtime atlases

- `roshan_directional.png` (4x2): front, front-left, left, back-left,
  back, back-right, right, front-right.
- `roshan_swim_front.png` and `roshan_swim_back.png` (4x4 each): sixteen
  chronological frames per view for one seamless reach/sweep/glide cycle.
- `roshan_gesture_a.png` (4x4): wave, cheer, clap, twirl. Each row is one
  animation with four chronological keyframes.
- `roshan_gesture_b.png` (4x4): look, giggle, sleep, point/reach.
- `roshan_gesture_c.png` (4x4): collect, boing, hair-twirl, hum.
- `roshan_gesture_d.png` (4x2): flop and carry.
- `roshan_play_a.png` (4x4): swing, climb, ride, land.
- `roshan_play_b.png` (4x4): dig-left, dig-right, seated ride, hop.
- `roshan_base.png` (1x1): the front frame derived from the directional
  atlas for portraits and isolated cutout call sites.

Every verb and playground action now has four authored keyframes. Swimming
has sixteen front and sixteen back keyframes, quadrupling the original
four-phase loop in each view. The original `roshan_swim.png`,
`roshan_gestures.png`, and `roshan_play.png` sheets are retained as generation
provenance/source references but are not preloaded by the player.

Current implementation note, not final authority: the primary player still
uses a legacy `Sprite3D` billboard, although no Roshan GLB or character
skeleton is loaded. Convert that staging to `Node2D`/`Sprite2D` while
preserving direction selection, movement clock, verb timing, playground
choreography, touch behavior, saves, and surrounding probes.

Opera costume ids remain gameplay state while the animated base sprite stays
visible. Dedicated 2D outfit layers are optional future design, not an audit
requirement; they must never restore a model path.

# Mermaid Roshan 2.5D sprite contract

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
provenance and rollback references but are not preloaded by the player.

The primary player is a `Sprite3D` billboard and no Roshan GLB or character
skeleton is loaded. Direction is selected relative to the active camera, swim
phase follows the established movement clock, verb frames advance across each
verb's existing duration, and playground frames follow their choreography
parameters. Opera costume ids remain gameplay state while the animated base
sprite stays visible; dedicated 2D outfit layers can be added without restoring
the retired model path.

# Day One bathroom finale movie contract

The runtime hook expects:

- `res://assets/cinematics/day_one_bathroom_finale.ogv`
- Ogg Theora in the project's native 1280x720 composition.
- A complete flattened 2D storybook frame at every timeline index, following
  the repository's mandatory cinematic generation and provenance rules.
- Frame 0 must match the final clean Bubble Bath room composition exactly:
  camera, crop, fixtures, Roshan placement, lighting, and colour. This creates
  an invisible content-matched cut from gameplay into the movie without a
  forbidden cross-dissolve, overlay animation, or subject translation.
- No black leader, logo card, debug frame, letterbox, or resolution jump.
- The clean gameplay scene remains underneath the `VideoStreamPlayer`; when
  playback ends, removing the movie reveals that same clean composition.

Completion and pool unlock are saved before the hook is invoked. Missing or
invalid media must remain a harmless clean-scene fallback and may never replay
the Day One rescue on Continue.

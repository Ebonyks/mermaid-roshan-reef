# Pearl navigation/tutorial component board v1 provenance

- Status: review-only adult component study; not a runtime texture or accepted
  child-facing UI.
- Generation method: built-in Codex `image_gen` (default built-in mode).
- Generated native output: `C:\Users\Peter\.codex\generated_images\01a074c0-ddea-7a71-a7e0-24747b063df9\exec-76016573-183b-4803-bb0b-5e0cd661365b.png`
- Workspace copy: `assets_src/ui/pearl_stage_v1/concepts/pearl_navigation_tutorial_component_board_v1.png`
- Workspace SHA-256: `1E0A1018149917AB5F6F3B6EDD187C2DA8A1297F2585D287DCC4FF50D8008F7A`
- Native/default SHA-256: `1E0A1018149917AB5F6F3B6EDD187C2DA8A1297F2585D287DCC4FF50D8008F7A`
- Native/default and workspace copies are byte-identical (matching SHA-256);
  the workspace copy is the packet artifact.
- Executed prompt transcript: `assets_src/ui/pearl_stage_v1/concepts/pearl_navigation_tutorial_component_board_v1.prompt.txt`
- Executed prompt transcript SHA-256: `0E5C08C42A2BF13CB45AF989247971CAA4102161D093FF48E84AD03661204EB5`
- Native/review dimensions: 1672x941 (wide review board).

## Bound references

1. `assets_src/ui/pearl_stage_v1/concepts/pause_menu_pearl_stage_concept_v1.png` — Pearl Stage pause style/material anchor; SHA-256 `CB3DD0824943562FFC4D2EB9729DBBAF42FBD71D508421066950D8FFED427B3F`.
2. `assets_src/ui/pearl_stage_v1/concepts/activity_chooser_pearl_stage_concept_v1.png` — Pearl Stage chooser style/material anchor; SHA-256 `28C8308A561B1088CC559FCB0CB9AE601A2D033F55D9CD7DD685823FD3FD6460`.

References provide style, material, and grouped ornament continuity only. No
reference pixels are runtime delivery pixels.

## Prompt intent

Create one matching Pearl Stage navigation/tutorial study with three separated
adult-review samples labeled `REST`, `PRESSED`, and `SELECTED`; one picture-only
illustrative target with one clear helping pointer; and large `REPLAY` and `BACK`
medallions. Rest uses standard aqua-pearl shell; pressed uses inset/darker
value, reduced shadow, and contact ring; selected uses a double gold contour,
raised pearl crown, and applied check seal. Keep all controls generous,
picture-first, one-finger, and visually distinct beyond color. Preserve the
cream-aqua scallop panel, violet underwater opera surround, pearl/gold contour,
rainbow ribbon, and grouped perimeter dressing from the two bound references.

Negatives requested: tiny controls, competing arrows, multiple pointers, red X,
warning/loss language, confirmation trap, generic flat mobile-game candy UI,
unrelated characters, Zelda/Wind Waker symbols, logos, watermark, photorealism,
3D render, wireframe, fake HUD, and illegible microtext.

## Proposed base-canvas placement (implementation study, not runtime proof)

These rectangles are bounded 1280x720 layout proposals for a future native
reconstruction. They are separate from the native 1672x941 art-study estimates
and do not assert that the generated board itself contains these coordinates.

| Component | Proposed base-canvas visual rectangle | Notes |
| --- | --- | --- |
| Safe area | `Rect2(48, 32, 1184, 656)` | Keeps shell/perimeter art and controls away from the viewport edge. |
| Teaching target | `Rect2(184, 174, 300, 300)` | Picture-first target; pointer anchors to the target's lower-right book region. Preserve at least a 110x110 projected hit region within the target owner. |
| Replay | `Rect2(500, 496, 170, 170)` | Large medallion on the lower rail; 22 px vertical gap / 27.203 px nearest-corner separation from teaching target, and 68 px from Back. |
| Neutral Back | `Rect2(738, 496, 170, 170)` | Large doorway medallion; one neutral route, no warning or loss semantics. |

The three proposed action rectangles do not overlap and remain inside the safe
area. They are adult-review layout allocations; final hit envelopes, focus
order, phone projection, and neighboring-world occlusion require runtime
measurement.

## Visual review notes

- Labels rendered legibly: `REST`, `PRESSED`, `SELECTED`, `REPLAY`, `BACK`.
- Pointer fingertip visibly contacts the storybook card's lower-right region;
  there is one pointer. This is an illustrative relationship on a static board,
  not a live runtime target binding.
- Rest/pressed/selected samples differ by inset/outline/value/contact/seal
  treatment, giving Astra a direct state-comparison board.
- Replay is a large speaker/wave medallion; Back is a large open shell-door
  medallion. Both are supplemental component examples, not wired controls.
- Coverage gaps are explicit: this board has no dedicated arrow-tip component
  study and no dedicated focus-state sample. The helping hand is a pointer
  illustration only; arrow routing and focus semantics require separate review.
- The board has no child-required objective text and no runtime target proof.
- Follow-up acceptance still requires Godot-native reconstruction, 110x110 base
  target/hit evidence, Mobile 1280x720 and wide-phone captures, typography and
  glyph evidence, performance checks, and owner/child review.

The generated board is project-original review art. Root must add its
`ASSET_LICENSES.md` entry with the generation source and this provenance path
before any commit that carries the PNG.

# Castle non-congruency audit — 2026-08-21

## Scope and result

The active Pearl Castle room registry, runtime cards, source masters, room
controls, Dream House furniture, banner replacement, Stuffie Playroom, and
library route were inspected against the 1280x720 child-facing frame and the
project's per-screen art rules.

The runtime alpha audit covered 51 castle cards and found no invisible-depth
failures. The new rear-facing movie couch has a complete alpha silhouette with
clear padding on every edge. Several room-level issues remain source-art work,
not safe code-only repairs.

## Repaired in this pass

- Cloud Movie Lounge: both couches now use a complete rear-facing cutout so
  they face the TV rather than the player. The original couch is untouched.
- Stuffie Playroom: the fixed couch/nook route now uses the existing approved
  shell-mermaid six-cubby shelf, fills it from the unlocked roster, highlights
  the active friend, and opens the established no-fail swap picker.
- Single-screen rooms: live camera drift is disabled. The Main Hall retains
  only the horizontal camera travel required by its two-screen layout.
- Castle chrome: the generic room-action and corner elevator controls no
  longer render or accept child input. Direct prop touches, physical doors,
  and contextual Back remain.
- Personalized banners: all four active baked purple-shell locations (two in
  Craft Room and two in Stuffie Playroom) are covered immediately by the saved
  user-designed banner components. No other active room contains that banner.

## Artwork findings requiring a separate art-production pass

Seven active V4 room backgrounds contain baked soft-focus/parallax-like edge
artifacts in both their source masters and runtime tiles:

- Stuffie Playroom
- Craft/Painting Room
- Royal Library
- Bubble Bath
- Kitchen
- Opera Hall
- Mermaid Pool

The affected 3640x2048 masters are under
`assets_src/castle/room_backgrounds_2k/`. Runtime camera motion was removed,
but deleting or masking painted pixels would damage complete authored frames.
These backgrounds need individually reviewed full-frame healing/regeneration,
followed by rebuilding their 2x4 tile grids.

The five Dream House rooms (gallery, dining room, royal bedroom, sleepover
bedroom, movie lounge) still use legacy 2x2 runtime coverage reconstructed as
2048x1152. That is below the current 2048x2048-per-playable-screen rule and
requires higher-resolution source masters before it can be marked complete.

`dream_house/movie_screen_frame.png` touches its left alpha edge and should be
re-audited with the next Dream House art batch. The active castle card-alpha
contact sheet is `audit/castle_sprite3d/castle_card_alpha_contact.png`.

## Library blocker

The owner PDF exists locally and matches the documented 34-page source hash,
but it is 192,566,311 bytes. The repository has no Git LFS configuration, and
there is no owner-approved hosted PDF URL in project documentation. Bundling
the file would exceed GitHub's normal per-file limit and add roughly 193 MB to
the Android build; opening an exported `res://` file URI is not a reliable
phone link. The correct final repair needs an owner-approved HTTPS PDF URL or
an explicitly approved separate distribution mechanism. The local source was
not modified, recompressed, or published.

## Validation state

- Godot 4.7.1 import: passed.
- Godot 4.7.1 analyzer for `castle_rooms_25d.gd`: passed.
- `gdtoolkit.parser`: passed.
- `tools/lint_inference.py`: passed.
- `probe_interaction.gd`: `INTERACTION|ALL OK`.
- `tools/audit_castle_card_alpha.py`: 51 cards, zero invisible-depth failures.
- `probe_castle_pearl_art.gd`: remaining failures are recorded, including the
  new cubbie's deliberate non-atlas interaction contract and unrelated
  concurrently added Main Hall content; this probe needs its inventory rules
  updated before the full suite can be green.

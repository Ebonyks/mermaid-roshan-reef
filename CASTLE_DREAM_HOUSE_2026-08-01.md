# Pearl Castle Dream House Wing

The castle now has a constructed Dream House Wing: one physical gallery plus
four casual role-play rooms designed for one-finger, non-reading play.

The first bay of Main Hall now contains a house-crest arch that opens the wing.
It is an unshaded depth-card insert over the existing decorative bay, so the
approved two-screen hall master remains unchanged. Main Hall therefore has
eight room doors, plus Huluu's throne.

Inside the gallery, four large picture doors are always visible in one screen,
left to right:

| Picture door | Room | Casual play |
| --- | --- | --- |
| plate and fork | Family Dining Room | serve six places and eat a meal one bite at a time |
| moon | Royal Bedroom | sleep, use the pearl light, pretend dress-up, and relax with a story |
| three stars and pillow | Sleepover Bedroom | choose any of three distinct dream beds and sleep |
| movie play symbol | Cloud Movie Lounge | cycle family home movies, sit on cloud couches, and play on the pouf |

The doors are world-space Sprite3D cards with invisible touch hotspots. There
are no floating room buttons. Back from any role-play room returns to the
gallery; Back from the gallery returns to Main Hall. Every activity has no
failure or resource cost and can be repeated forever.

## Art and runtime contract

- The gallery and four role-play rooms each have a deterministic 2048 x 2048
  native master. Each centered 2048 x 1152 gameplay band is split into four
  exact 1024 x 576 Sprite3D cards.
- The wing entrance and its four doors reuse the approved Pearl Castle
  playroom portal non-destructively. New project-authored crests distinguish
  the routes without requiring words or new generated art.
- Readable furniture remains on separate unshaded Sprite3D cards. No readable
  object is painted across a background-tile boundary.
- The ImageGen dining-room result remains a composition reference only and is
  never loaded at runtime.
- Protected family book images are loaded directly into the movie-screen card.
  No book image is modified, recompressed, or copied into a derivative asset.

tools/build_castle_dream_house_rooms.py reproduces the art package.
tools/audit_castle_dream_house.py blocks missing sources, changed hashes,
undersized masters, oversized runtime textures, tile reconstruction drift,
floating-route regressions, ImageGen-reference leakage, or loss of the
physical-door and role-play contracts.

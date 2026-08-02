# Pearl Castle Dream House

The picture-first Pearl Castle now has four additional casual role-play rooms.
They are deliberately nested behind existing rooms so the Main Hall keeps its
seven clear physical doorways and remains easy for a four-year-old to remember.

| Existing room | Picture-first doorway | New room | Play |
| --- | --- | --- | --- |
| Royal Kitchen | plate | Family Dining Room | serve six places and eat a meal one bite at a time |
| Royal Library | moon | Royal Bedroom | sleep, use the pearl light, pretend dress-up, relax with a story |
| Royal Bedroom | bed | Sleepover Bedroom | choose any of three distinct dream beds and sleep |
| Stuffie Playroom | movie camera | Cloud Movie Lounge | cycle family home movies, sit on cloud couches, play on the pouf |

Back always returns to the immediately preceding room. Every activity accepts
one touch, has no failure or resource cost, and can be repeated forever.
Picture icons carry navigation; labels are accessibility hints rather than
required reading.

## Art and runtime contract

- Each room has a deterministic 2048 x 2048 native master. The centered
  2048 x 1152 gameplay band is split into four exact 1024 x 576 Sprite3D
  cards, satisfying native per-screen coverage and Mobile texture limits.
- Readable furniture is kept on separate unshaded Sprite3D cards. No room
  object is painted across a background-tile boundary.
- Approved Pearl Castle/art-pass-35 furniture was reused non-destructively.
  The only new shared components are a simple pearl meal plate and movie
  frame.
- The ImageGen dining-room result is composition reference only and is never
  loaded at runtime. Its 1254-pixel output is intentionally not promoted.
- Protected family book images are loaded directly into the movie-screen card.
  No book image is modified, recompressed, or copied into a derivative runtime
  asset.

tools/build_castle_dream_house_rooms.py reproduces the art package.
tools/audit_castle_dream_house.py blocks missing sources, changed hashes,
undersized masters, oversized runtime textures, tile reconstruction drift,
ImageGen-reference leakage, or loss of the role-play contracts.

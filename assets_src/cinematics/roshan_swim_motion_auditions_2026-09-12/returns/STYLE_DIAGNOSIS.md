# Style diagnosis — 2026-09-13 (session 2)

The first Imagine return proved the video tool and lost the character.

## What was ignored

- `ART_STYLE_GUIDE.md` — modern flat-color anime with soft storybook painting.
- `AGENTS.md` cinematic rule — 2D storybook medium; do not switch to 3D.
- `VIDEO_OPERATOR.txt` — painted character is design authority (loose rainbow hair, gold crown with one gem, pink/lilac, pearlescent tail).
- Packet README — openings are existing 8-view cutouts on navy. **No character is redrawn.**
- Day One handoff 2 and overnight recut — do not make a new look; approved masters are appearance authority.
- Shot card — IMAGE_1 is a pinned first frame, not a license to invent a scene.

## What take-01 actually did

1. Bound GitHub `openings/front-right.png` / `right.png` as IMAGE_1. Those files are a 3D CGI redraw (bun, silver multi-gem crown, different face), not the 8-view cutouts.
2. Attached `approved-front.png` as IMAGE_2 but treated it as a weak hint.
3. Called `imagine_reference_to_video`, which builds a new scene from references. That is restyle, not emulation.
4. Scored identity as “held” because costume colors were nearby.
5. Shortlisted the wrong mermaid.

The unused painted 8-view family (`references/front-right.png`, `right.png`, …) already had alpha cutouts. Those are the existing art.

## Repair (purposed and executed)

1. Composite the 8-view cutouts onto navy RGB(17,37,54), 1280×720. No redraw.
   - `openings/locked-front-right.png`
     SHA-256 `6b0918967e5b1703e4b04a67b27798b7a733a6ab79c44314ebcf6f12bf1be685`
   - `openings/locked-right.png`
     SHA-256 `042c2e052ad6bdcead67731282c6e7a8059c788a75cbc8bc687a63b7848859b7`
2. Animate the locked front-right still with `imagine_image_to_video` (pin the still).
3. RSW-01 take-02: `fabb219b99df6ecfd0fd6f3b8578ecb204ce019541e3e0088b74d787529ecbf5`
   Identity holds. End pose still camera-facing. Native 10.04s / 24 fps / AAC.
4. Mark all eight take-01 clips `rejected` for STYLE_REWRITE.
5. Quota 9 / 10. One replacement left. Layout approval of the locked openings is still pending.

`DELIVERY_ACCEPTED` remains false. No Aseprite conversion. No cinematic claim.

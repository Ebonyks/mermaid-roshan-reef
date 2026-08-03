# Animated dust bunny source

This is the second enemy art project after the animated mischief imp. It uses
only 2D sprite cards. The approved project-memory anchors were recovered
losslessly from commit `32eba2ea` on `origin/codex/dirty-castle-2d`:

- `references/dust_bunny_curl_ears.png`
- `references/dust_bunny_hop.png`

Their SHA-256 hashes remain:

- curl ears: `D88F667724D2C06FC591B00EA91B018430BAD1A359E7527124A6E25B0CC6DA0F`
- hop: `677CDA8C5DE1D3AAF1D8960B089D48FAB27106429BC221B4C26C14775B382752`

OpenAI built-in image generation produced six-frame idle, hop, and
cleaning-poof atlases using the approved art as identity references. The exact
prompts are in `PROMPTS.md`. The accepted defeat sequence sharply squashes the
bunny into a large lavender poof, expands into a hollow dust ring, and finishes
on an aqua-white clean sparkle. It contains no injury imagery. The rejected
soft-dissolve source is retained under `rejected/` for audit history.
`tools/process_dust_bunny_animation.py` resizes generated 3-by-2 sources to
mobile-safe 768x512 chroma masters. The installed ImageGen chroma helper
converts those masters into the three runtime RGBA atlases under
`assets/sprites/dust_bunnies/`.

Runtime cells are 256x256 in reading order. `scripts/dust_bunny_sprite.gd`
loads the atlas regions directly; it never creates or consumes a 3D model.

The live integration uses the Pearl Castle dungeon's fourth room as the second
enemy-family encounter. `CombatArena` spawns five `DustBunnySprite` cards,
drives their seeded hop brains, accepts the forgiving CLEAN action, and keeps
each card present until the accepted cleaning-poof animation reaches its final
sparkle. The CLEAN projectile reuses the exact project-memory soap bubbles from
the Dirty Castle 2D pack.

`rainbow_dust_bunny_concept.png` is a non-runtime color-variant design derived
from the approved curl-ear identity. It keeps the original silhouette and face,
uses a soft curl-to-curl pastel rainbow instead of flag-like stripes, and adds
one small prismatic forehead sparkle. It remains concept art until a dedicated
runtime animation set is approved.

`dust_bunny_first_boss_concept.png` develops the same species into Mermaid
Roshan's proposed first boss. Its boss read comes from a much wider three-tier
storm-cloud body, enormous spiral ears, smoky grey-to-deep-plum values, and a
natural curl crest with one lavender sparkle. The expression stays confident
and playful for the no-fail preschool experience. It remains non-runtime
concept art until its dedicated boss animations and encounter are approved.

`dust_bunny_first_boss_concept_v2_teeth.png` is the revised preferred boss
design. It preserves the body and palette from the first concept while replacing
only the tiny closed smile with a compact plum grin and two short pointed pearl
teeth. The visible points strengthen the boss read without introducing a snarl,
large jaw, or frightening expression.

The first-boss animation pass adds five four-frame 2x2 sheets: dust-plume
jump, vulnerable laugh, flinch, angry recovery, and inward implosion to wisps.
The generated sheets are normalized to 1024x1024 chroma masters under
`boss_chroma/`; the transparent runtime derivatives use four 512x512 cells
under `assets/sprites/dust_bunnies/boss/`. Exact prompts, state timing, and the
later octagonal-arena interaction contract are in `BOSS_ANIMATION_DESIGN.md`.

`scripts/dust_bunny_boss_sprite.gd` exposes the sheets as one unshaded
`AnimatedSprite3D` card. Laugh frame 2 opens a 0.75-second vulnerability window.
Each of three accepted taps plays a distinct two-frame flinch and a different
project-original sound (`ui_tap`, `hop_boing`, then `chime`); the third removes
one of three health rounds. After round two, action playback rises to 1.25x and
the final window tightens to 0.65 seconds. The final-round `angry_jump_final`
animation reuses approved peak-angry, crouch, lift-off, and landing atlas regions;
no new image was generated and no additional texture is loaded. A timeout resets
only the current three taps through the phase-appropriate anger animation. The
third completed round automatically plays the readable implosion. Encounter
movement, normal-hit immunity, three-pip health/tap feedback, and arena placement
remain for dedicated stage integration.

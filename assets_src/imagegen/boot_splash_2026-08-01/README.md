# Mermaid Roshan boot splash - 2026-08-01

## Purpose

Replace the default Godot boot image with a Mermaid Roshan opening image at
the earliest engine-controlled point, then hand the same image to the first
game frame for a seamless fade into the existing story intro or live world.

## Reuse and gap audit

Relevant existing art was inventoried before generation:

- The five shipped friend groups are defined by `FRIEND_DEFS` in
  `scripts/main.gd`: Harper and Fiona, Evie and Lamb-a', Faron and the baby,
  Daddy Mermaid, and Wacky with Chuck. Princess Huluu is the story companion.
  Gabby remains excluded by the IP hold.
- `assets/characters/roshan_25d/roshan_base.png`,
  `assets_src/daddy_master.png`, and the character sticker derivatives are
  the identity authorities. None of those originals was modified.
- `assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png`
  supplies the approved outdoor mountain, lagoon, path, and low-clutter tone.
- The recent castle-room master and Fairy Pond dawn art supply the current
  pearl, shell, rainbow, navy-outline, aqua/lavender-shadow finish.
- `gen2/ui_prototypes_2026-07-19/intro_story_v1_1024x576.png` is a useful
  layout precedent, but its figures are explicit placeholders and it is not a
  title or boot image.

No reusable image contained the title, full current cast, outdoor world, and
the requested Roshan/Daddy celebration. A new full-frame image was therefore
the narrow gap. Generation was limited to three candidates plus one rejected
pose-correction attempt.

## Brief in-game tone audit

The selected direction uses the game's existing visual vocabulary:

- polished 2D storybook rendering with soft cel shading and navy-purple ink;
- pastel aqua, lavender, coral, pearl, and gold, with rainbow color reserved
  for celebration and route readability;
- Caribbean reef coral and shells, the Pearl Castle, and Sky Lagoon mountains;
- large, separated character silhouettes and low detail behind faces for the
  target child's phone-scale readability;
- a single exact title and no loading instruction, progress bar, fail language,
  or reading-dependent action.

## Candidates

| Candidate | Native source | SHA-256 | Review |
|---|---|---|---|
| A - Rainbow Reef Reunion | `candidates/candidate_a_rainbow_reef_reunion_raw.png` | `627d6a5667333cb27f8527a94fcc09a8b5277bface24a27c90bc99998f0654ad` | Complete cast and richest reef foreground; more visual density than needed at phone scale. |
| B - Rainbow Bridge Celebration | `candidates/candidate_b_rainbow_bridge_celebration_raw.png` | `4e56cb12b67d50318bc3383308138e399faa16f3803a6696f4dfa45708b1311e` | **Selected.** Best hierarchy, exact title, complete cast, strongest rainbow theme, clearest silhouettes, and safest central pair. |
| C - Pearl-Shell Storybook Festival | `candidates/candidate_c_pearl_shell_storybook_festival_raw.png` | `0362336176b158f213ef5929b0083b2bbd05c743849503829c331b25da7a0d4d` | Strong shell/title-page framing and intimacy; foreground is busier than B. |

The contact sheet is `candidates/contact_sheet.jpg`
(`fe6f7d20cd2eec8dc48c2b14f775e46188ef82779d9a82a9c77d4c674b332bae`).

## Selection audit

Candidate B passes the requested content gates:

- exact text: `MERMAID ROSHAN`, once;
- outdoor daytime setting;
- Roshan and Daddy are the largest central figures, touching, leaning together,
  and raising their free arms in celebration;
- all five shipped friend groups plus Princess Huluu are visible;
- rainbow arch and bridge dominate, with reef, castle, lagoon, and mountain
  landmarks subordinate to the cast;
- no Godot logo, loading bar, watermark, villain, weapon, or added character;
- critical title and faces are inside the center-safe field.

The requested mutual shoulder pose was treated as a preference, not ignored.
A targeted edit was generated after the three candidates. It still left
Daddy's inside hand at Roshan's waist and introduced mild identity/style drift,
so it was rejected. The selected candidate keeps the stronger identities and
readability rather than weakening the review gate to accept the attempted edit.

## Runtime derivative

`assets/ui/boot_splash_mermaid_roshan.png`

- 1024x576 opaque PNG, within the runtime texture limit;
- whole-canvas high-quality bicubic normalization from selected native
  candidate B (1672x941);
- no crop, mask, subject move, compositing, retouch, or protected-source
  overwrite;
- runtime SHA-256:
  `d5127c4a6227baab05343dc10692e2f76f1dd59f22ca24a22329de402dbb8044`.

The native generated master remains unchanged under `candidates/`.

## Earliest-load wiring and transition

`project.godot` now sets the custom PNG as
`application/boot_splash/image`, leaves
`application/boot_splash/minimum_display_time` at zero, enables filtering,
and uses aspect-preserving `stretch_mode=1`. This replaces the default Godot
image without adding an artificial delay. The matching sky-blue background
fills any aspect bars rather than cropping the title or outer friends.

`scripts/boot_splash_overlay.gd` draws the same asset before
`ReefMain._ready()` builds the heavy world. It remains opaque while that
synchronous work runs, then fades over 0.45 seconds on the first rendered
frames. Headless probes skip the overlay.

## Generator and prompts

All candidates used the OpenAI built-in image-generation tool. The complete
request specs and input roles are recorded in `PROMPTS.md`.

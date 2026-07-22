# Opera House Job Prototype Plan — 2026-07-21

## Scope lock

- Source of truth: `scripts/opera_house.gd`.
- Twelve playable jobs, three flat prototype sheets per job (36 accepted sheets total).
- Boss encounters are explicitly deferred: Curtain Dragon, Shadow Phantom, and Midnight Maestro.
- Every sheet is a strict 4 x 4 grid of sixteen isolated, modelable concepts.
- Every individual concept is delivered as a 1024 x 1024 PNG card derived
  deterministically from its accepted sheet cell. Do not reduce these cards.
- The three-sheet package for every job is:
  1. Roshan outfit and silhouette sheet.
  2. Core one-touch subgame props and mechanical states.
  3. Stage dressing, guidance, celebration, and before/after states.
- Generated sheets are concept sources only. They do not replace protected runtime character art.

## Shared visual contract

- Flat storybook concept art for a pastel theatrical toy diorama; never a Blender render or photoreal object study.
- Rounded, low-complexity forms that can become efficient Godot Mobile meshes.
- Navy/purple outlines, aqua/lavender shadows, warm coral, teal, cream, plum, and brushed-gold accents.
- Shell-and-pearl ornament is used as a controlled Opera House family resemblance, not repeated on every surface.
- Roshan keeps her recognizable warm brown eyes, long wavy brown hair with a rainbow streak, joyful childlike expression, and rainbow-scaled mermaid tail.
- Job clothing must read clearly at phone size and must not obscure Roshan's face or replace her tail with human legs.
- Do not reproduce the backpack or any third-party characters visible in the identity reference.
- No written labels, numerals, logos, copyrighted character motifs, Zelda iconography, realistic skin rendering, tiny filigree, or fragile geometry.
- Guidance is nonverbal: strong silhouettes, color matching, glow, arrows, paths, and before/after poses.
- Failure is never punitive. Retry states are gentle, inviting, and visually distinct from completion states.

## Acceptance gate

Each sheet is graded with a computer maximum of 4.9/5. Any sheet below 4.5 is rejected and regenerated.

| Dimension | Weight | Passing requirement |
| --- | ---: | --- |
| Style and palette consistency | 25% | Clearly belongs beside the accepted Opera House pack |
| Child-readable silhouette | 20% | Main function readable at phone scale |
| Job/mechanic continuity | 20% | Every concept supports the shipped activity |
| Roshan identity or prop-set cohesion | 15% | Outfit preserves identity; props share one material language |
| Modelability and mobile practicality | 10% | Rounded construction, limited transparent layers, no micro-detail traps |
| Grid completeness and uniqueness | 10% | Sixteen distinct, uncropped concepts; no filler or near-duplicates |

Automatic rejection: wrong job, boss content, realistic rendering, human legs on Roshan, copied third-party imagery, text-heavy signage, malformed character anatomy, clipped cells, repeated filler, or a dominant off-palette treatment.

## Three-sheet inventory by job

### Floor 1

| Job | Outfit sheet focus | Gameplay sheet focus | Stage/state sheet focus |
| --- | --- | --- | --- |
| Pastry Chef | Puff toque, coral apron, shell buttons, whisk and piping tools | Three cake layers, recipe pictograms, bowl states, oven, toppings and completed cake | Pastry counter, ingredient shelves, topping pedestals, stir/frosting effects, reveal table |
| Detective | Plum capelet, deerstalker-inspired shell cap, magnifier, clue satchel | Six distinct mystery boxes, paw/feather/ribbon clues, decoys, chest and tiara reveal | Moonlit prop-library set, search pools, clue trail, reveal pedestal and case-complete effects |
| Ballerina | Layered shell-petal tutu over tail, pearl tiara, fin ribbons | Four dance tiles, demonstration/press states, barre, music box and twirl cues | Recital stage, mirror panels, spotlights, gentle retry and completed-bow states |
| Candy Maker | Teal/coral confectioner jacket, wrapped-candy cap, press mitts | Press machine, timing gauge, molds, seven readable candies and wrapping tools | Toy candy workshop, conveyor, hopper, parade cart, success squish and shelf-fill states |

### Floor 2

| Job | Outfit sheet focus | Gameplay sheet focus | Stage/state sheet focus |
| --- | --- | --- | --- |
| Doctor | Friendly cream clinic coat adapted around tail, shell badge, stethoscope | Plush starfish before/after, thermometer, kiss hearts, bandages, checkup tray | Cozy toy clinic, exam platform, tool trolley, guidance sparkles and recovery celebration |
| Farmer | Coral plaid kerchief, teal work vest, straw shell hat, produce basket | Piggy trot/hop/munch poses, vegetables, toss arcs, basket, hay and mud effects | Meadow layers, barn, fence, picnic blanket, toss lane and happy piggy finale |
| Boxer | Padded coral gloves, navy training vest, safe shell belt, headband | Ring pieces, mitt, bell, round lights, soft imp-bop effects, championship belt | Toy boxing ring, corner stool, training bag, pennants, victory podium and confetti |
| Magician | Plum tailcoat/capelet, tall shell-trim hat, wand, pearl bow | Three hats, bunny-fish states, selector glow, swap trails, decoy puff and reveal | Vaudeville trick stage, table, cabinet, hat pedestals, shuffle and celebration states |

### Floor 3

| Job | Outfit sheet focus | Gameplay sheet focus | Stage/state sheet focus |
| --- | --- | --- | --- |
| Painter | Coral beret, teal smock around tail, palette cuff, broad brush | Three paint pots, brushes, easel/canvas progression, palette, rinse cup and splats | Sunrise studio set, color pedestals, swipe ribbons, gallery reveal and finished painting |
| Astronaut Engineer | Rounded cream/teal bubble suit around mermaid tail, helmet ring, tool belt | Bubble tank, rocket, three pipe types, ghost slots, valve, wrench and bubble stream | Retro-future launch set, gantry, workbench, pipe wall, launch states and bubble exhaust |
| Racecar Driver | Coral/navy racing jacket, open-face shell helmet, gloves, tail guard | Opera kart views, steering/turbo controls, boost strips, flags, trophy and pit tools | Curved track set, starting arch, barriers, pit cart, progress lights and finish podium |
| Pop Star | Iridescent coral/plum stage jacket, shell glasses, pearl microphone | Microphone states, directional dance cues, speakers, rhythm pulses and rainbow effects | Concert frame, catwalk, light panels, arrow lanes, audience glow props and finale state |

## Runtime continuity note

`OPERA_ASSET_REQUESTS_2026-07-19.md` still describes an older “Opera Star / Moonlight Aria” slot. The current playable slot in `scripts/opera_house.gd` is Boxer / “The Championship Bout.” This package follows the live implementation; the stale request section should be corrected in the delivery commit.

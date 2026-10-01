# Roshan appearance analysis (2026-09-30)

**Status:** `SUPPORTING_CURRENT` analysis prepared by Claude for revision 2
of this handoff (analysis only; no image created or changed). Measured at
`dev` `b65c21fdddd79f272a6854f241faa1441abe6616`. Tracking finding:
[`MA-DOC-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-008).
The plan that uses it is [README.md](README.md), work package VL2.

**Owner direction (2026-09-30):** *"Lavender tail is cannon. Atlases are
primary approved, but there's some variance in appearances, if a more
comprehensive analysis is effective, it should be given as part of a codex
handoff in making this"*, then: *"Technically, both tails are right, the tail
is both rainbow and iredescent pink/purple, depending how light hits it"*.

## 1. Answer in brief

- **Her tail is consistent once light is taken into account.** Every
  approved image shows one iridescent tail: lavender-pink-purple in the
  base-world atlases, rainbow in most career art, a mix in the playground.
- **Two designs of Roshan are in the game, and the difference is not light.**
  Images generated from `assets/characters/roshan_25d/roshan_base.png` and
  the base-world atlases show the canonical young child. Images generated
  from the older `assets/characters/roshan_sprite.png` (13 career cards, the
  13 career atlases built from them, the Sky Lagoon playground sprites) show
  an older, slimmer girl with a loose rainbow lock instead of a tied
  ponytail, no tiara, warm brown outlines and a muted painted finish.
- **The cause is the identity reference, not the generator.** The two
  career sheets made later from `roshan_base.png` (Geologist, Teacher) came
  out close to canon. Binding the approved atlas as the identity reference
  for every future job removes most of the drift without repainting
  anything.
- **A defect list is independent of design:** the Geologist's idle frames
  have no fins, Pop Star's ribbon reads as a second tail, three career cards
  crop her tail, the Magician frames bake in spell effects, the Astronaut's
  hair passes through her helmet, one gesture frame flips the tail, and three
  unused images carry a third-party cartoon backpack.

## 2. Decisions this analysis applies

- The approved atlases are Roshan's primary identity authority. The
  protected book image is a likeness reference only.
- The tail is iridescent: pink, purple and lavender scales that show rainbow
  colours where light hits them. Lavender and rainbow renderings are both
  correct.
- Everything else that differs between images is variance, sorted below into
  light, costume, second design and defect.

## 3. Every Roshan image the game shows

| Surface | Images | Used by |
|---|---|---|
| Base-world atlases | 9 runtime atlases (256 px frames) and `roshan_base.png` in `assets/characters/roshan_25d/` | The player, castle rooms, Sky Lagoon, portraits, cinematic identity binding |
| Career atlases | 15 `roshan_<career>_sheet_a.png` (4×4, 256 px frames) in `assets/opera/worlds/actors/animation/` | `scripts/opera_roshan_actor.gd`, the ballet surface, the faerie prototype |
| Career portrait cards | 14 `roshan_<career>.png` (512 px) in `assets/opera/worlds/actors/` | Castle career route cards, the Opera player fallback, Melody (Pop Star), the Racer driver |
| Sky Lagoon playground | 12 sprites (512 px) in `assets/sprites/sky_lagoon/roshan_playground/` | Swing, slide and seesaw in `scripts/arena/sky_lagoon_promenade.gd` |
| Boot splash | `assets/ui/boot_splash_mermaid_roshan.png` | Start-up |
| Tree Book test | `assets/opera/tree_book_test/roshan_book.png` | The Arborist practice scene |
| Not loaded by game code | `assets/characters/roshan_sprite.png`, `assets/sprites/sky_lagoon/sky_lagoon_roshan.png` and `..._runtime_audited.png`, three older provenance sheets in `roshan_25d` | Reference, history and two preview tools |

## 4. Method

- **Measured** with the `cells` mode of
  [`tools/measure_visual_profile.py`](tools/measure_visual_profile.py): every
  frame of 24 atlases (368 frames) and 31 single images. Per frame: silhouette
  size and position, shares of the measured identity colours, lavender,
  periwinkle and pink-purple hue bands, saturation, lightness and the colour
  of the dark silhouette edge. Data:
  [`data/roshan_atlas_frames.json`](data/roshan_atlas_frames.json) and
  [`data/roshan_single_images.json`](data/roshan_single_images.json).
- **Reviewed by eye**, image by image, against the canonical directional
  atlas (Claude plus two read-only review passes): tail light state, fins,
  hair, headwear, top or costume, face and age, line, rendering, proportions,
  frame defects.
- **Traced** each family to the identity reference named in its provenance
  record.
- Source-file indicators only (`DL-VIS-08`): no number here justifies
  recolouring approved art. No image was created, cropped or edited.

## 5. Results by family

### 5.1 Measured profiles

Medians per frame (range in brackets).

| Family | Frames | Lavender band | Pink top colour | Hair colours | Saturation | Lightness | Dark edge |
|---|---:|---|---|---|---|---|---|
| Base-world atlases and `roshan_base` | 129 | 0.23 (0.19–0.29) | 0.07 (0.03–0.11) | 0.17 (0.14–0.24) | 0.70 (0.64–0.73) | 0.65 (0.63–0.68) | Brown on hair, plum on body |
| Career atlases | 240 | 0.01 (0.00–0.15) | 0.00 | 0.27 (0.16–0.39) | 0.53 (0.43–0.61) | 0.54 (0.47–0.62) | Warm brown (213 of 240) |
| Career cards | 14 | 0.00 (0.00–0.13) | 0.00 | 0.26 (0.18–0.35) | 0.47 (0.38–0.60) | 0.53 (0.50–0.61) | Mixed |
| Playground sprites | 12 | 0.03 (0.02–0.21) | 0.00 (0.00–0.11) | 0.27 (0.16–0.30) | 0.60 (0.58–0.63) | 0.63 (0.61–0.69) | Pink-plum (11 of 12) |

Read with section 5.2: the low lavender figures for career art are the
rainbow light state, not drift. The higher hair share (longer, looser hair),
lower saturation and lower lightness are the second design.

### 5.2 Base-world atlases (canon)

All nine runtime atlases and `roshan_base.png` show the same character as the
directional atlas: a girl of about four or five with a round face and large
brown eyes, brown wavy hair with a tied rainbow ponytail, a small gold tiara
with a blue gem, a pink top with lilac ruffle sleeves, an iridescent tail in
its lavender state, rainbow fins, thin dark lines and soft pastel cel shading.

Small issues:

- **Ponytail side.** All 32 swim frames, `roshan_play_b` frames 4–7 (dig-right)
  and `roshan_gesture_a` frame 14 put the rainbow on her right; the rest put it
  on her left, so it can jump sides when animations switch.
- **Tail flip.** `roshan_gesture_b` frame 2 curls the tail the opposite way
  from frames 0, 1 and 3 of the same "look" row.
- **Possible specks** above `roshan_play_a` frames 2–3 and `roshan_gesture_c`
  frame 2, where the 2026-09-26 repack erased pixels bleeding in from
  neighbouring frames; the committed clipping audit reports none, so confirm
  in a transparency-aware viewer before acting.

### 5.3 Career atlases

- **Tail:** thirteen sheets show the rainbow state, Geologist and Teacher the
  lavender state. Each sheet keeps one state across its sixteen frames.
- **Second design in thirteen sheets** (all but Geologist and Teacher), each
  generated from its career card: waist-length loose chestnut hair with an
  untied red-to-violet rainbow lock; career headwear and never the tiara; a
  longer face with almond eyes, heavier lashes, a pointed chin and open grins,
  reading about seven to nine; warm dark-brown lines of medium weight;
  textured, higher-contrast painted shading in a warmer, deeper palette;
  smooth rainbow fins without the canon's white bands.
- **Geologist and Teacher**, generated from `roshan_base.png`, keep the
  canonical face, thin lines and pastel cel shading. Both still have long
  loose hair (their layout references were career sheets); Geologist alone,
  whose prompt asked for a "rainbow ponytail", gathers the rainbow into a
  bunch.
- **Scale:** idle height is about 200–224 px in a 256 px frame against about
  220 for canon; Nursery is about 76% of canon (166–171 px).
- **The 2026-08-09 acceptance review** passed "identity" for the thirteen
  sheets against their own career cards, so the second design was never
  compared with the base atlas.
- **Frame defects** (frame numbers read left to right, top to bottom, from 0):

| Sheet | Frames | Defect |
|---|---|---|
| Geologist | 0–1 (idle) | Tail ends in a point with no fins |
| Geologist | 12, 14; 10 | White leftover background inside the tail loop; a sand patch baked in |
| Pop Star | Most | A dark ribbon from the waist reads as a second thin tail |
| Astronaut | All | Long hair hangs outside the sealed helmet |
| Magician | 8–11 | Spell rings and portals baked into the sprite, floating apart from her |
| Farmer | 3; 9 | The apron turns coral and loses its pocket; a soil patch baked in |
| Candy Maker | 14 | Rainbow lock and sash bow on the opposite side |
| Nursery | All | About 76% of canon height |
| Teacher | 4 | Small pale patch at the hip, probably leftover background (check) |

- **Closest to canon:** Teacher, then Geologist once its fins and background
  are repaired. **Furthest:** Pop Star, then Racer, Astronaut and Magician.

### 5.4 Career portrait cards

- **13 cards** (Astronaut, Ballerina, Boxer, Candy Maker, Chef, Detective,
  Doctor, Farmer, Magician, Nursery, Painter, Pop Star, Racer) follow the
  second design: rainbow tail, a loose rainbow lock, career headwear and no
  tiara, an older and slimmer girl (about seven to nine), thin warm brown
  lines, a muted painted finish, and most look soft as if enlarged.
- **Teacher** is the exception: lavender tail, younger round face, close to
  canon, generated from `roshan_base.png` (its provenance says so), but
  blurry.
- **Defects:** Boxer, Chef and Candy Maker cut off the tail and fin at the
  bottom edge; Astronaut and Ballerina touch it. Pop Star's trailing plum
  ribbon reads like a second tail. Racer has a thin white glow along inner
  outlines and is much sharper and more saturated than the other cards.
  Magician has a stray speck at the left edge. The imp-contest handoff
  already forbids drawing the tail-cropping cards as full-body actors.

### 5.5 Sky Lagoon playground sprites

All twelve follow the second design with the tail in its mixed state (paler,
bluer lavender with a pastel rainbow belly band): a rainbow streak from the
parting, no tiara, a pale pink sleeveless top with ruffle straps, an older and
slimmer build (about eight to ten). `roshan_slide_3_v2.png` and
`roshan_swing_3_v2.png` are noticeably pinker and more saturated than the
other ten. Their provenance names only "the project Mermaid Roshan" reference.

### 5.6 Other images

- **Boot splash:** canon look (tiara, pink top, lavender tail), but the
  rainbow hair is not visible.
- **Tree Book test (`roshan_book.png`):** a costume variant close to canon
  (lavender tail with a diamond scale pattern), with a heavy near-black line
  and a bright green patch in the hair.
- **Not loaded by game code:** `roshan_sprite.png`, `sky_lagoon_roshan.png`
  and `sky_lagoon_roshan_runtime_audited.png` show the second design and a
  backpack printed with third-party cartoon characters and their name. Two
  tools (`tools/audit_sky_lagoon_kit.py`, `tools/build_sky_lagoon_preview.py`)
  and one test still read the audited copy.

## 6. Why the designs differ: identity reference lineage

| Generated from | Date | Produced | Result |
|---|---|---|---|
| Five multi-view references kept outside the repository | 2026-07-26 | Base-world atlases, `roshan_base.png` | Canon |
| `assets/characters/roshan_sprite.png` (named the binding identity in `assets_src/concepts/opera_jobs_flat_2026-07-21/PROMPTS.md`) | 2026-07-21 | 13 career cards | Second design |
| Each career card (`assets_src/imagegen/opera_roshan_animation_2026-08-09/PROMPTS.md`) | 2026-08-09 | 13 career atlases | Second design |
| `roshan_sprite.png` (per `ASSET_LICENSES.md`) | 2026-07 | `sky_lagoon_roshan.png` | Second design |
| "The project Mermaid Roshan" (not specific) | 2026-07 | 12 playground sprites | Second design |
| `roshan_base.png` (Geologist also used the Farmer sheet for layout) | 2026-08-30, 2026-09-03 | Geologist and Teacher atlases, Teacher card | Close to canon |

The lesson for the visual language: **a style card's identity anchor must be
an approved base-world atlas or `roshan_base.png`.** Career art may be bound
only as a costume or pose anchor, and `roshan_sprite.png` never.

## 7. Variance register

Light and costume are accepted by the owner's decisions. Everything else is
listed for the owner; nothing changes without approval.

| ID | Variance | Where | Kind | Suggested handling |
|---|---|---|---|---|
| RV-01 | Tail light state differs | All families | Light (accepted) | Record the state on every card; pick it from the scene light |
| RV-02 | Career costume replaces top and headwear | Career art | Costume (accepted) | Keep face, hair colour, tail and fins as canon |
| RV-03 | Older, slimmer girl with a longer face, almond eyes and a pointed chin | 13 career cards, 13 career atlases, playground | Second design | Owner question; new art follows the canon age and build |
| RV-04 | Loose rainbow lock or front streak instead of a tied ponytail | Same, plus Geologist and Teacher | Second design | Owner question; new base-outfit art uses the ponytail |
| RV-05 | No tiara outside career costume | Playground | Second design | New base-outfit art wears the tiara |
| RV-06 | Muted, darker painted finish (saturation about 0.5 against 0.7), warm brown lines, fins without white bands | Career cards and the 13 career atlases | Second design | Owner question; new Opera art matches whichever finish the owner keeps |
| RV-07 | Ponytail side jumps between frames | Swim pair, `play_b` 4–7, `gesture_a` 14; Candy Maker 14 | Continuity | Accept, or match the side when a sheet is regenerated |
| RV-08 | Tail curls the wrong way for one frame | `roshan_gesture_b` frame 2 | Defect | Repair candidate |
| RV-09 | No fins on two idle frames; white leftover background; baked sand | Geologist atlas 0–1; 12 and 14; 10 | Defect | Repair candidate (the idle row is the most-seen state) |
| RV-10 | A ribbon reads as a second tail | Pop Star card and atlas | Defect (identity) | Repair candidate |
| RV-11 | Long hair outside a sealed helmet | Astronaut atlas | Defect | Repair candidate |
| RV-12 | Spell effects baked into the character frames | Magician atlas 8–11 | Defect | Move effects to overlays (family F-FX) |
| RV-13 | Apron changes; baked soil | Farmer atlas 3; 9 | Defect | Repair candidate |
| RV-14 | Sheet drawn at about 76% scale | Nursery atlas | Scale | Check the runtime scale; regenerate only if it shows |
| RV-15 | Tail and fin cut off, or touching the edge | Boxer, Chef, Candy Maker (cut); Astronaut, Ballerina (touching) cards | Defect | Never use as full-body actors; recrop from the atlas if needed |
| RV-16 | White glow along inner outlines; much sharper than siblings | Racer card | Defect | Repair candidate |
| RV-17 | Specks or pale patches to verify | Magician card; `play_a` 2–3, `gesture_c` 2; Teacher atlas 4 | Check | Verify in a transparency-aware viewer |
| RV-18 | Heavy near-black line; green hair patch | `roshan_book.png` | Drift | Repair if the Tree Book test ships |
| RV-19 | Rainbow hair not visible | Boot splash | Drift | Accept or recompose |
| RV-20 | Within-set colour jump | Playground `slide_3_v2`, `swing_3_v2` | Drift | Accept or match the set |
| RV-21 | Third-party cartoon characters on a backpack | `roshan_sprite.png`, both `sky_lagoon_roshan` files (not loaded by game code) | IP | Owner decision: quarantine like the Gabby assets; never bind as a reference |

## 8. Proposed identity rules for `ID-ROSHAN`

1. Identity anchor for every new Roshan job: `roshan_base.png` or a base-world
   runtime atlas, by hash.
2. Tail: iridescent; the card names the light state (lavender for soft or
   ambient light, rainbow for bright or stage light, mixed for outdoor light,
   pending `OQ-VIS-LIGHT-STATE`); one state per sheet and per scene; fins
   always rainbow.
3. Base outfit: pink ruffled top, small gold tiara with a blue gem, tied
   rainbow ponytail. A career costume may replace the top and the headwear
   only.
4. Age and build: the base-world child (about four or five, round face, large
   brown eyes), whatever the costume.
5. Line and finish: thin dark lines (plum on the body and tail, warm brown on
   the hair) and soft pastel cel shading, within the measured base-world
   ranges in section 5.1, unless the owner keeps the career finish (RV-06).
6. Forbidden: legs, feet or shoes; a second tail or tail-like ribbon; a flat
   or split two-tone tail; adult proportions; third-party characters, brands
   or logos.

## 9. What Codex should do with this

- Build `ID-ROSHAN` from section 8 and the measured ranges, and add the
  identity check (`tools/visual_language.py check --identity ID-ROSHAN`) that
  reports light state, age-and-build drift indicators and line colour against
  the base-world profile.
- Register exemplars by role: base-world atlases as identity exemplars;
  career atlases as costume and pose exemplars only; `roshan_sprite.png` and
  the 13 older career cards as "never bind as identity" anti-exemplars with
  reason code `RC-IDENTITY-SOURCE`.
- Put RV-03 to RV-21 to the owner as one review list with the suggested
  handling; prepare (but do not run) repair cards for the defects the owner
  approves.
- Change no approved image in this handoff.

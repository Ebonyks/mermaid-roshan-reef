# Mermaid Roshan visual design language (draft)

**Status:** `PROPOSED / CANDIDATE` draft prepared by Claude on 2026-09-30 for
Codex to land as `design/reference/VISUAL_LANGUAGE.md` (work packages VL1 to
VL4 in [README.md](README.md)). It is not authority until it lands and the
owner answers the open questions in section 12. It restates no rule: it links
to `DL-*` IDs and adds measured values, families, identity sheets, a
generation card, a review card and a learning loop. Values marked *measured*
come from [`tools/measure_visual_profile.py`](tools/measure_visual_profile.py)
at `dev` `b65c21fd`; values marked *proposed* are new and need acceptance.

## 0. How to use it

To make or change any picture in the game:

1. Find the family of the thing you are making (section 3).
2. Read that family's traits, tokens and exemplar images.
3. For every character shown, open its identity sheet (section 4).
4. Write one art style card (`ART_STYLE_CARD_V1`) that binds two to four
   exemplar images by ID and copies the family's tokens.
5. Codex generates or edits, post-processes and runs the checks (section 8).
6. Review with one art review card (`ART_REVIEW_CARD_V1`, section 10).
7. Record the outcome: an accepted image becomes an exemplar, a rejected one
   an anti-exemplar with reason codes (section 11).

Claude writes cards and reviews in words; Codex builds every image
(`CLAUDE.md`, owner decision 2026-09-30). Reuse comes first (`DL-ASSET-01`,
`DL-ASSET-02`); protected art is never edited (`DL-ASSET-08` for the picture
book).

## 1. The look in one paragraph

Mermaid Roshan's illustrated storybook presented as a pastel toy playset:
rounded toy-like forms with slight handmade asymmetry, broad painted value
bands, clean indigo-to-plum contours, aqua and lavender shadows, warm pearl
highlights, graphic readable water, coral and gold accents and restrained
magical sparkle. Cool colour fills the world; warm rainbow colour marks
characters, rewards and the thing to touch. Every subject reads as one
silhouette at phone size. Wind Waker is a rendering reference only.

Sources: design 06 section 4; the cinematic shared style guide
(`assets_src/cinematics/*/written_guide/SHARED_STYLE_AND_CHARACTER_GUIDE.txt`);
`CLAUDE.md` art direction.

## 2. Pillars

| ID | Pillar | Rules and sources |
|---|---|---|
| VL-P1 | **One readable silhouette.** Big rounded masses, detail in two or three calm clusters, readable when squinted and at 112 px | `DL-VIS-01`, `DL-READ-02`; phone silhouette test in `assets/OBJECT_GENERATION_AUDIT_LOG.md` |
| VL-P2 | **Drawn, not rendered.** Clean contours, a few painted value bands, matte-to-satin; no PBR noise, no mesh imitation | `DL-VIS-02`, `DL-VIS-05`, `DL-MED-05` |
| VL-P3 | **Cool world, warm heroes.** About two thirds cool colour; warm rainbow for characters, rewards, targets | `DL-VIS-04`; design 02 section 2 |
| VL-P4 | **High-key and safe.** No dark masses on faces, hands or targets; shadows aqua or lavender, never neutral black | `DL-VIS-03`, `DL-AGE-08` |
| VL-P5 | **The real subject first.** Faithful species and objects, complete anatomy, no invented faces on props or scenery | `ART_STYLE_GUIDE.md` motif families; flaw codes F1 and F2 |
| VL-P6 | **Painted once.** Approved art keeps its authored light; the engine adds motion, contact shadow and sparkle, never relighting | `DL-MED-05`; lighting headroom spec |
| VL-P7 | **Identity is fixed.** Every character matches its identity sheet in every frame and costume | `DL-VIS-06`, `DL-MED-02`, `DL-MOT-*` |

## 3. Families

Every picture belongs to one family. A family has a style line (pasted into
style cards), tokens, exemplars and anti-exemplars.

| ID | Family | Style line | Measured now | Open question |
|---|---|---|---|---|
| F-HERO | Roshan atlases (base world and careers) | Polished children's storybook sprite, clean dark plum outline, soft cel shading; iridescent tail in the scene's light state | Body contour indigo-plum; hair contour brown; base world saturation about 0.70, careers about 0.53 | Identity settled 2026-09-30; `OQ-VIS-LIGHT-STATE` |
| F-CAST | Family and friends from the book and the cinematic guide | Match the identity sheet exactly; never restyle protected art | Not measured (protected) | — |
| F-RIVAL | Opera imps and rivals | As drawn today: chunky cartoon imp, heavy dark outline, saturated purple skin | Contour near-neutral `#101314` | `OQ-VIS-RIVAL-LINE` |
| F-CREATURE | Dust bunnies, Grand Puff, Baby Eagle | Friendly round storybook creatures; Grand Puff per its identity lock | Dust bunnies `#353b4e` (slate) | — |
| F-ROOM | Castle room backgrounds | Fully painted pearl-castle interior: lavender stone, cream and gold trim, plum contours | 8 of 12 rooms cool-shadowed; 4 flat-shell rooms | `OQ-VIS-FLAT-ROOMS`, `OQ-VIS-WARM-ROOMS` |
| F-WORLD | Sky Lagoon and outdoor worlds | Painted panorama with aqua shadows; matches the Sky Lagoon reference images | Sky Lagoon sprites near-neutral `#2c272d` | — |
| F-STAGE | Opera stages and backdrops | Painted stage panels at native resolution | Not measured | — |
| F-PROP | Interactive props and state sheets | Oversized, rounded, five to eight colour shapes, indigo-violet contour, four to twelve authored states | Story props `#241d63`, minigame `#3a236c`, pool `#4b2772` | — |
| F-FX | Bubbles, caustics, sparkles | Separate overlays; four-point sparkles; never baked into props | Water effects `#161f56` | — |
| F-UI | Interface | Storybook UI tokens; picture first | Tokens in `scripts/storybook_ui.gd` | — |
| F-BOOK | Picture-book pages | Existing book and Grok frames only; crop, isolate, local in/outpaint | Protected | — |
| F-CINE | Cinematic frames | Full-frame rule; shared cinematic guide | Not measured | — |

## 4. Character identity

Each recurring character gets one identity sheet in the format of Grand
Puff's lock (`assets_src/characters/grand_puff_2026-09-13/IDENTITY_LOCK.json`):
identity authority, traits, part counts, forbidden changes, sampled colours,
and scale against Roshan.

### Roshan (`ID-ROSHAN`)

**Settled by the owner on 2026-09-30:** the approved atlases are her primary
identity authority, and her tail is iridescent: pink, purple and lavender
scales that show rainbow colours depending on how the light hits them. The
lavender rendering and the rainbow rendering are both correct. Evidence:
[ROSHAN_APPEARANCE_ANALYSIS.md](ROSHAN_APPEARANCE_ANALYSIS.md).

- **Approved images** (`DL-MED-02`): `assets/characters/roshan_25d/` (nine
  runtime atlases and `roshan_base.png`) and the fifteen career atlases in
  `assets/opera/worlds/actors/animation/`.
- **Invariants in every image:** one young child mermaid with the same soft
  round face, large brown eyes and age; brown wavy hair with a rainbow section;
  one continuous iridescent tail with rainbow fins; child-sized, distinct arms
  and hands; no legs, feet or shoes.
- **Tail light states:**

| State | Looks like | Seen in | Proposed use |
|---|---|---|---|
| Lavender | Lavender and periwinkle sequins with pink and sky-blue sheen | All base-world atlases; Teacher and Geologist lean this way | Soft or ambient light: exploring the castle and Sky Lagoon |
| Rainbow | Continuous rainbow-gradient scales | Thirteen career atlases and their portrait cards | Bright or stage light: Opera careers |
| Mixed | Paler, bluer lavender with a pastel rainbow belly band | Sky Lagoon playground sprites | Outdoor light |

  Proposed rule (`OQ-VIS-LIGHT-STATE`): choose the state from the scene's
  light, keep one state within a sheet and a scene, and keep the fins rainbow.
- **Base outfit (measured on the runtime atlases):** pink ruffled top
  `#eeb2e8`; small gold tiara with a blue gem `#f4d74b`; rainbow ponytail;
  brown hair `#ae743e`, `#7e492a`, `#e29455`; skin `#f9ddc2` with blush
  `#d49e99`; lavender-state tail `#b9a1f2`, `#8e7adc` (shade `#757094`) with
  sheen `#aad3f9`, `#64a8db`.
- **Career outfits:** a costume may replace the top and the headwear; her
  face, hair colour, tail and fins stay hers.
- **Recorded variance:** hair style and where the rainbow sits, headwear,
  outline colour, rendering and scale differ between atlas families
  (analysis section 5). Each item goes to the owner; no art changes without
  approval.
- **Forbidden:** adult proportions; legs, feet or shoes; a second tail; a flat
  single-colour or left/right two-tone tail; different hair or eye colour;
  third-party characters, brands or logos (the old sprite
  `assets/characters/roshan_sprite.png` carries one and is never bound).
- **Retired wording:** "lavender clothing, green-right / pink-left tail"
  (design 01, design 02, scoring governance, generation contract) is
  superseded by the owner decision.

### The rest of the cast

Starting text for each sheet is in the cinematic shared guide; approved images
are in its reference map.

| ID | Character | Key traits from the guide |
|---|---|---|
| `ID-DADDY` | Daddy Mermaid | Small crown, dark rectangular glasses, long brown/deep-green hair, navy coat with gold trim, teal cape, rainbow tail |
| `ID-RUMI` | Rumi (Violet) | Large sculpted violet braid, pointed ears, star-shell earrings, navy/lavender jacket, aqua-to-violet-to-pink tail |
| `ID-BABY-EAGLE` | Baby Eagle | One young turquoise, yellow and pink bird; two dust bunnies pin it, never a blanket |
| `ID-DUST-BUNNY` | Dust bunnies | Friendly round storybook creatures; no legs on the swimmer |
| `ID-GRAND-PUFF` | Grand Puff | Existing identity lock: three-tier grey-lavender body, spiral ears, pearl paws, two pearl teeth |
| `ID-PEARL-PLANE` | Pearl plane | Exact approved silhouette, windows and scale |

## 5. Line, shape, colour, value and light

| Token | Value | Strength | Source |
|---|---|---|---|
| `TOK-VIS-CONTOUR-MAJOR` | 2–4 screen px at 1280×720 | Rule | `DL-VIS-02` |
| `TOK-VIS-CONTOUR-INTERIOR` | 1–2 screen px | Rule | `DL-VIS-02` |
| `TOK-VIS-CONTOUR-COLOUR` | World and props: dark indigo to plum (hue about 220–300°, luma below 90); hair and skin may be warm brown; no white rims | Proposed from measurement | `DL-VIS-02`; contour profile |
| `TOK-VIS-SHADOW-HUE` | Lavender about 300° in castle interiors; aqua about 200° in Sky Lagoon; one per zone; never neutral | Proposed from historical spec | `DL-VIS-03`; `LIGHTING_2P5D_AUDIT_2026-08-02.md` C2 |
| `TOK-VIS-VALUE-BANDS` | Three painted value bands per material | Proposed (sources say 3, 2–3, "a few") | `DL-VIS-05`; design 02 |
| `TOK-VIS-COOL-SHARE` | About two thirds of an environment cool | Rule wording | `DL-VIS-04`; design 02 |
| `TOK-VIS-HEADROOM` | Top 1% luminance at most 0.88, bottom 1% at least 0.05, blown and crushed pixels each under 0.5%; painted highlights about 0.85 | Proposed from historical spec | lighting headroom spec C2; `tools/check_grade_headroom.py` budgets differ |
| `TOK-VIS-PROP-SHAPES` | Five to eight colour shapes per prop | Source | `ART_STYLE_GUIDE.md` environment section |
| `TOK-VIS-PALETTE` | One palette file: named anchors (the style guide's 20) plus measured family palettes, each with a colour-difference tolerance | Proposed | Section 4.1 of the audit |
| `TOK-UI-INK` and the other interface colours | `scripts/storybook_ui.gd:8-23` | Code | `DL-UI-06` |

Interface ink is defined nine times with eight values in code; the palette
file becomes the one source and code reads it later (refinement handoff
WP-13, owner-gated).

## 6. Composition and readability

- One focal action per view; the target is the most contrasted shape
  (`DL-READ-01` to `DL-READ-06`).
- The child reads it at phone size: the silhouette test at 112 px and the
  touch target at least 110 px (`DL-UI-03`).
- No words in world art; Roshan's lower body and tail stay visible.
- Highlights follow the painted object, not the touch box (door handoff,
  pattern `PAT-GUIDE-02` in the refinement handoff).

## 7. Layers, motion and effects

- At least two layers, aiming for four or five; at least 2048 px native
  coverage per playable screen (`DL-LAY-02`, `DL-LAY-07`).
- Overdraw: at most eight cards each over 10% of the screen, at most 150%
  cumulative overlap (`LIVING_CARD_DESIGN_LANGUAGE_2026-07-29.md`).
- One dominant moving landmark plus three quiet loops (design 02).
- Idle drift at most about 1% of body height; response within two frames at
  30 fps (`design/animation/ROSHAN_MOVEMENT_LANGUAGE.md`).
- Effects are overlays that never hide the action (`DL-MOT-*`); about 40
  particles on the Speedy tier (aesthetics plan).

## 8. Technical

- Textures at most 1024 px on the longest side or power-of-two
  (`DL-PERF-04`); character cells 256 px.
- Cutouts: flat `#00ff00` chroma generation, border-sampled soft matte
  (12/220) with despill; one spill definition and one "visible alpha"
  threshold for every tool (*proposed*; today there are four and six).
- No painted checkerboard, no fake alpha, no halo or black matte rim, no
  neighbour-frame bleed; sheet gutters at least 8 px.
- Every new asset: provenance record and an `ASSET_LICENSES.md` row in the
  same commit.

## 9. Making new art

1. Name the gap and show why existing art cannot be reused.
2. Pick the family and bind exemplars: identity anchor, style anchor, and
   optionally a neighbour and a previous state. For Roshan the identity anchor
   is always `roshan_base.png` or a base-world atlas; career art is bound only
   for costume or pose (appearance analysis, section 6).
3. Fill `ART_STYLE_CARD_V1` in the proven order: use case, inputs, request,
   invariants, backdrop, style line, framing, constraints, avoid.
4. Codex generates, post-processes and checks. New frames for an existing
   sheet follow the answer to `OQ-VIS-SPRITE-CHANNEL`.
5. Never bind an anti-exemplar, a runtime capture with interface on it, a
   generated board or third-party art.

## 10. Reviewing art

One review card replaces the nine rubrics (*proposed*):

- **Vetoes** (any one rejects): identity drift from the sheet; anatomy or
  part-count errors; fake alpha or checkerboard; words in world art;
  third-party characters, brands or game assets; wrong family contour or a
  neutral-black shadow without an approved exception.
- **Six axes, scored 0–5, weakest axis decides:** silhouette and readability;
  line; colour and value; material and finish; identity; fit in the scene.
- **Pass for runtime:** every axis at least 4.5 in a phone-size runtime
  capture of the real state (`DL-VIS-08`). Only the owner gives 5/5
  (`DL-VIS-07`).
- **Evidence levels:** isolated file, sheet, in-scene capture, device,
  owner. A score names its level.

## 11. Learning loop

| Registry | Holds | Grows when |
|---|---|---|
| `EX-*` exemplars | Path, SHA-256, family, what it teaches, approval evidence | An image is accepted |
| `AX-*` anti-exemplars | Path or description, reason codes, source | An image is rejected |
| `RC-*` reason codes | Merged from flaw codes F1–F10, transparency classes, minigame trials, design 02 rejected approaches, animation hard failures | A new kind of failure appears |
| `ID-*` identity sheets | Section 4 | A character is added or the owner settles a question |
| Family profiles | Measured contour, palette and value statistics of each family's exemplars | Exemplars change; never typed by hand |

The profile tool recomputes each family's numbers from its exemplars and
reports how far a new image sits from them. The report advises; it never
recolours approved art (`DL-VIS-08`).

## 12. Open questions for the owner

| ID | Question | Default until answered |
|---|---|---|
| `OQ-VIS-ROSHAN` | Which Roshan do new pictures continue? | **Answered 2026-09-30:** her tail is iridescent; lavender and rainbow renderings are both correct |
| `OQ-VIS-LIGHT-STATE` | Does the tail's light state follow the scene light (lavender in soft or ambient light, rainbow in bright or stage light, mixed outdoors), one state per sheet and scene? | Yes |
| `OQ-VIS-SECOND-DESIGN` | Keep the older, slimmer career and playground Roshan (loose rainbow lock, muted finish), or regenerate it from the base-world identity over time? | Keep existing art; all new art follows the base-world child |
| `OQ-VIS-TIARA` | Does Roshan wear the tiara whenever she is not in a career costume? | Yes, for new art |
| `OQ-VIS-AUTHORITY` | Is the identity authority the book (`DL-VIS-06`) or the approved atlas family (`DL-MED-02`)? | **Answered 2026-09-30:** the approved atlases are primary; the book is a likeness reference |
| `OQ-VIS-RIVAL-LINE` | Keep the imps' heavy near-black line as their deliberate look, or move them to the plum line? | Keep, and record it as the rival family trait |
| `OQ-VIS-FLAT-ROOMS` | Are the four flat-shell rooms placeholders to repaint? | Yes, as backlog; not part of this handoff |
| `OQ-VIS-WARM-ROOMS` | May rooms with warm floors (Craft Room, Movie Lounge, Playroom) keep warm dark local colour? | Yes for local colour; shading stays cool |
| `OQ-VIS-SPRITE-CHANNEL` | New frames: image generation from bound exemplars, or Aseprite cel authoring? | Generation for new sheets; Aseprite for corrections and in-betweens |
| `OQ-VIS-PALETTE` | Replace the 20 typed swatches with measured family palettes plus named anchors? | Yes |
| `OQ-BAKED-LIGHT` | May painted flats show lit lamps and a vignette? | Lit practical lamps yes; no global vignette |
| `OQ-COLOUR` | What gold, red, blue, coral and ruby mean | Refinement handoff default |

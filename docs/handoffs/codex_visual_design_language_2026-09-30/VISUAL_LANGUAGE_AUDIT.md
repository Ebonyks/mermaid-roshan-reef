# Visual design language audit (2026-09-30)

**Status:** `SUPPORTING_CURRENT` audit evidence prepared by Claude (analysis
only; no game change). Measured at `dev`
`b65c21fdddd79f272a6854f241faa1441abe6616`. Tracking finding:
[`MA-DOC-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-doc-008).
The plan is [README.md](README.md); the proposed reference text is
[VISUAL_LANGUAGE_DRAFT.md](VISUAL_LANGUAGE_DRAFT.md).

**Update (2026-09-30, revision 2):** the owner settled the identity questions
raised in sections 4.1 and 5. The approved atlases are Roshan's primary identity
authority, and her tail is iridescent, lavender-pink-purple or rainbow
depending on the light, so both renderings are correct. The frame-by-frame
follow-up, which traces the remaining variance to the identity reference
each batch was generated from, is
[ROSHAN_APPEARANCE_ANALYSIS.md](ROSHAN_APPEARANCE_ANALYSIS.md). The evidence
below is unchanged.

**Owner request (2026-09-30):** *"Is the visual design language of the mermaid
roshan articulated in the master audit in a way that it is easy for the game to
reference and learn from itself how to develop future art? If not, implement a
plan to refine it."*

## 1. The answer

**No.** The pieces exist, but they are scattered, partly contradictory, mostly
adjectives, and not tied to the game's own approved art.

- **The master audit routes; it holds no visual language.** Its "Art" task
  row leads to the ten `DL-VIS-*` rules in design 06. Only one of them gives
  numbers (contour width), none gives a colour value, and none names an image.
  The working palette, the generation prompt block and the review checklist
  sit in documents the Art row never links.
- **The approved art disagrees about Roshan.** The base-world atlas gives her
  a lavender sequin tail and a rainbow ponytail. The fifteen career atlases
  and the cinematic character guide give her a rainbow tail. The written
  anchors in design 01 and 02 say "lavender clothing, green-right / pink-left
  tail". They match none of the approved images. A generator following the
  documents would draw a Roshan the child has never seen.
- **No example images back the words.** The only image any rule names is
  the Ballerina atlas. No approved "finish board" was ever built, and the book
  PDF that design 02 calls the primary visual authority is not in the
  repository.
- **There is no current recipe for new still art.** Ten partial protocols
  exist. The best structured is a per-asset prompt record
  (`assets/characters/roshan_25d/PROMPTS.md`), not a reusable card.
- **Nine scoring rubrics disagree** on averaging versus weakest-link and on
  the pass line.
- **Measured rules live in tools and archived audits, not in the rules.**
  Examples are the light-headroom spec, the overdraw budgets and the
  audit-tool thresholds. No tool checks contour colour, shadow hue or the
  cool/warm balance.
- **Nothing learns.** Accepted and rejected art do not feed any registry.
  The Day Two library holds 637 reviewed, hashed images that no rule or
  generator reads.

| Criterion | Verdict | Evidence |
|---|---|---|
| Reachable from the master audit in two links | Partly | Art row reaches design 06 sections 4–6 only; design 02, the style guide and the scoring rubric are unlinked |
| Covers every visual aspect | No | No visual spec for effects, interface art or any character but Roshan in the governed documents |
| Measurable | No | One of ten `DL-VIS-*` rules has numbers; design 06, design 02 and the master audit contain no colour values |
| Consistent | No | Section 5: Roshan's appearance, outline colour, palettes, colour meanings, rubrics |
| Current | Partly | Style guide and generation contract mix 3D-era pipelines with live rules |
| Backed by example images | No | One rule names one image; no exemplar or rejection registry |
| Ready to generate new art | No | No style card; the only coded style prompt asks for black outlines |
| Checkable by tools | Partly | Tools check alpha, headroom, layout and one Sky Lagoon palette match; none checks `DL-VIS-01` to `DL-VIS-05` |
| Learns from accepted and rejected art | No | Review results stay in dated files |

## 2. What the master audit routes to

- **Art row:** design 06 section 4 (visual promise), 5 (composition), 6 (2D
  canvas construction), 14 (reuse and provenance) and 3 (medium). It does not
  link `design/02_ART_DIRECTION.md`, `ART_STYLE_GUIDE.md`,
  `design/BOSS_SPLASH_DESIGN_LANGUAGE.md` or `design/07_CASTLE_DOOR_LANGUAGE.md`,
  although the ledger marks the last two binding.
- **Section 3 authority map** lists no art-direction document at all.
- **Hops to concrete guidance:** contour widths and shadow hues, 1;
  Roshan's anchors, 2 and not through the Art row; the 20-colour palette,
  prompt block and checklist, no link path (named in plain text only).
- **Rules by family in design 06:** `DL-VIS-*` 10, `DL-MED-*` 10, `DL-ASSET-*` 8,
  `DL-READ-*` 6, `DL-LAY-*` 9, `DL-MOT-*` 13, `DL-UI-*` 7, `DL-TYPE-*` 12. Art has
  no rule family of its own beyond `DL-VIS-*`; motion rules are `DL-MOT-*`.

## 3. Where the visual language actually lives

| Source | Status | What it holds | Problem |
|---|---|---|---|
| design 06 sections 4–6, 9, 14 | Rules | Shape, contour, value, cool/warm balance, layers, motion, provenance | Mostly adjectives; no colour values; no images |
| `design/02_ART_DIRECTION.md` | Current | Two-thirds cool, three value families, technical gates, score caps, rejected approaches, seven-step review | Roshan anchors wrong; claims seven hard CI gates where three are not |
| `ART_STYLE_GUIDE.md` (2026-07-13) | Partly superseded | 20-colour palette, motif families, castle grammar, identity, effects, composition, prompt block, checklist | Never revised for true 2D; ranks itself above owner briefs |
| `assets/ART_GENERATION_CONTRACT.md` | Partly superseded | A second palette, motif fidelity, ground-plant rule | Written for Blender; wrong Roshan anchors |
| `ART_SCORING_GOVERNANCE_2026-07-18.md`, `ART_HUMAN_REVIEW_AUDIT_2026-07-16.md` | Partly binding | 0–5 rubric and seven hard caps | Unlinked; wrong Roshan anchors |
| `LIGHTING_2P5D_AUDIT_2026-08-02.md` | Historical | Headroom spec: top 1% at most 0.88, bottom 1% at least 0.05, one shadow hue per zone (lavender about 300° castle, aqua about 200° Sky Lagoon) | The only measurable light rule; marked for archive |
| `LIVING_CARD_DESIGN_LANGUAGE_2026-07-29.md` | Partly superseded | Overdraw budgets, one dominant moving landmark plus three quiet loops | Mixed with Sprite3D structure |
| Cinematic `SHARED_STYLE_AND_CHARACTER_GUIDE.txt` (42 copies, one text) | Unledgered | The clearest one-paragraph statement of the look; identity text for Roshan, Daddy, Rumi, Baby Eagle, dust bunnies, Grand Puff and the pearl plane | Lives inside cinematic packets; not referenced by any rule |
| `assets_src/characters/grand_puff_2026-09-13/IDENTITY_LOCK.json` | Proposed | Machine-readable identity: traits, part counts, forbidden changes, seven sampled colours, scale against Roshan | The right format, used for one character |
| `assets/characters/roshan_25d/PROMPTS.md` | Provenance | The proven prompt order and chroma-key recipe | Per asset, not a template |
| `docs/handoffs/codex_visual_polish_2026-09-25/AESTHETICS_PLAN.md` | Proposed | Painted versus flat rooms; style-matching protocol | Says Claude may build reference packs (now forbidden) |
| `design/VISUAL_REPAIR_PLAN_2026-09-26.md` | Supporting | Aseprite cel authoring for new sprite frames | Its requested protocol "was not found"; conflicts with image generation for new frames |
| `scripts/storybook_ui.gd` | Code | 15 interface colour tokens, type roles, panel and button styles | The only centralised visual tokens; interface only |

## 4. Measured against the game's own art

Every number below comes from
[`tools/measure_visual_profile.py`](tools/measure_visual_profile.py) (read-only;
writes numbers, never images) and is stored under [`data/`](data/). These are
source-file indicators. Under `DL-VIS-08` they never justify recolouring
approved art; they show where the written language is silent or wrong.

### 4.1 Roshan

- **Measured palette** of six runtime base-world atlases (directional, swim
  front and back, gestures a to c;
  [`data/roshan_identity_palette.json`](data/roshan_identity_palette.json)):
  lavender-periwinkle tail (`#b9a1f2`, `#8e7adc`, 23% of opaque pixels, with
  shade `#757094`), brown hair (`#ae743e`, `#7e492a`, `#e29455`, 29%), pink
  top (`#eeb2e8`), skin (`#f9ddc2`, blush `#d49e99`), sky-blue sheen
  (`#aad3f9`, `#64a8db`), gold tiara and fins (`#f4d74b`).
- **Identity presence across the approved family**
  ([`data/roshan_identity_presence.json`](data/roshan_identity_presence.json)):
  hair and skin colours persist in every atlas, but the tail colours that
  make up 16–21% of all nine runtime base-world atlases make up 0.0–0.4% of
  thirteen career atlases (Geologist and Teacher about 8%). Opening the Chef
  atlas shows why: a rainbow-gradient tail, warmer brown contours and longer
  hair.
- **Four descriptions of one character:**

| Source | Hair | Top | Tail |
|---|---|---|---|
| Base-world atlas (`roshan_25d`, approved by `DL-MED-02`) | Brown, rainbow ponytail, tiara | Pink ruffled | Lavender sequin, rainbow fins |
| Career atlases (approved by `DL-MED-02`), cinematic guide, style-guide palette | Brown, rainbow section | Pink or costume | Continuous rainbow |
| Protected book image `assets/book/hall/glass_mermaid.png` | Brown, rainbow front lock, crown | Pink puffed | Green into purple scales, rainbow fin |
| Written anchors (design 01:490, design 02:286–287, scoring governance, generation contract) | Chestnut, front-left rainbow forelock | "Lavender clothing" | "Green-right / pink-left" |

`DL-VIS-06` names the book as the identity authority, but no book image of
the game's Roshan design is in the repository, and the older reference sprite
`assets/characters/roshan_sprite.png` (not loaded by runtime code) carries a
branded third-party backpack.

### 4.2 Contours by art family

[`data/contour_profile.json`](data/contour_profile.json), up to eight files per
family. The rule says contours are deep-indigo, plum or warm-brown.

- **Indigo to violet, as the rule says:** story props `#241d63`, minigame
  art `#3a236c`, Day One pool `#4b2772`, Day One art studio `#531d62`,
  dirty-castle cleanup `#4f336c`, birthday props `#552f6e`, water effects
  `#161f56`, stuffie studio `#232255`, terrain, training props.
- **Near-neutral dark, which the rule does not describe:** Opera actors and
  rivals `#101314` (the rival imps have a heavy near-black line, unlike
  Roshan's thin plum line), Sky Lagoon sprites `#2c272d`, castle room buttons
  `#2a2625`, companions `#222427`.
- **Warm brown:** Roshan's hair contours and the career atlases.

The prompts themselves drift: 427 prompt files describe contours as
"navy-purple" (70), "violet" (54), "plum" (22), "navy" (7), "indigo" (6),
"purple" (5) and "warm-brown" (1), and the one coded style prompt
(`tools/gen2_batch.py`) asks for "crisp thin black outlines".

### 4.3 Shadows in castle rooms

[`data/castle_room_shadow_profile.json`](data/castle_room_shadow_profile.json)
classifies the darkest 15% of each room's background. Eight of twelve rooms
are 72–100% cool (aqua or lavender), as `DL-VIS-03` asks. The Craft Room (76%
warm), Movie Lounge (95% warm, median brightness 76 of 255) and Playroom (58%
warm, 29% neutral) are not. In the Movie Lounge the dark tones are its red
carpet, so this is local colour rather than shading. The language does not
say whether warm-floored rooms are allowed exceptions to `DL-VIS-04`.

### 4.4 Two background treatments

The Playroom is a fully painted illustration. The Royal Bedroom, Movie
Lounge, Dining Room and Family Gallery use flat-shape shells (flat ceiling
band, flat window, flat floor). The 2026-09-25 aesthetics plan already judged
those four "read as placeholders beside the painted family". No rule says
which treatment is the standard.

## 5. Contradictions on visual matters

| Topic | Positions | Suggested resolution |
|---|---|---|
| Roshan's appearance | Section 4.1 (four versions) | Owner question; meanwhile record both approved image variants and retire the prose anchors |
| Identity authority | Book (`DL-VIS-06`) versus approved atlas family (`DL-MED-02`); the book of the game design is absent | Owner question |
| Contour colour | Deep-indigo, plum or warm-brown (design 06); navy/purple (design 02, `CLAUDE.md`); ink indigo `#222E44` (style guide); near-black (generation contract, coded prompt) | Measured bands per family, with the owner deciding whether rivals keep a black line |
| Working palette | Style guide 20 colours versus generation contract (for example lavender `#9A77C8` versus `#a87dd6`) versus code: `INK` is defined nine times with eight values, none equal to the style guide | One palette file with tolerances, derived from approved art |
| Colour meanings | Gold means animation (`scripts/interaction_affordance.gd`), plot (`scripts/castle_door_cue.gd`), or plot with ruby for bonus (door handoff) | Owner question (`OQ-COLOUR`) |
| Opera career palettes | `tools/build_opera_codex_art.py` and `scripts/opera_world_backdrop_2d.gd` disagree for 10 of 13 careers | Code that ships, then one source |
| Scoring | Nine rubrics: averaging versus weakest-link; pass at 4/5, 4.5 per dimension, or 4.5 counted as needing work | One review card |
| Value bands | "Three value families" (design 02) versus "two or three" (style guide) versus "a few" (design 06) | One token |
| Baked light | Never bake light or vignettes (style guide) versus flats with lit lamps and a planned vignette | Owner question (`OQ-BAKED-LIGHT`) |
| New sprite frames | Image generation (aesthetics plan) versus Aseprite cel authoring (repair plan) | Owner question |
| Reference packs | Claude may build them (aesthetics plan) versus Claude builds no images (`CLAUDE.md`, 2026-09-30) | `CLAUDE.md` |
| Hard CI gates | design 02 lists seven; three do not run in the remote suite | Correct design 02 |
| Interface panel shadow | Violet-tinted (`storybook_ui.gd`) versus neutral black (`scripts/games/picture_games.gd:109`) | Tokens |

## 6. What the game cannot learn today

- **No exemplar registry.** The nearest are the Roshan atlases
  (`roshan_base.png` is the identity anchor in 28 of 35 cinematic handoff
  packets), the castle interaction approval ledger (owner acceptance pending),
  the 28 castle touch items that pass the subjective 4.5 gate in
  `FABLE_CASTLE_ITEM_STYLE_AUDIT_2026-07-28.md` (scores typed into a tool, not
  measured), and the Day Two library (637 hashed reviews, none
  owner-accepted).
- **No rejection registry.** Reasons are spread over the image-generator
  flaw codes F1–F10 (`gen2/generated/ANALYSIS.md`), the transparency defect
  classes, the boss-splash and design 02 rejected approaches, the minigame
  trials and the animation hard failures.
- **No identity data for Roshan.** Only her frame geometry is
  machine-readable; Grand Puff alone has an identity lock.
- **No style card.** Every prompt is written per batch.
- **Tool thresholds disagree.** Green-screen spill has four definitions,
  "visible" alpha six (8 to 128), and plausible coverage three ranges. Two
  blocking gates (`tools/audit_castle_card_alpha.py`,
  `tools/audit_fairy_art_v2.py`) write contact-sheet images, which matters
  for the 2026-09-30 rule that Claude runs no image-producing script.

## 7. What already works and should be kept

- The cinematic guide's paragraph of visual language and its character
  identity blocks: the best words the project has.
- Grand Puff's identity lock: the right shape for every character sheet.
- The Roshan prompt order and chroma-key recipe.
- The light-headroom spec, overdraw and motion budgets, design 02's
  technical gates and rejected approaches.
- The image-generator flaw codes, transparency defect classes and minigame
  trial rejections: the start of a rejection taxonomy.
- The Day Two library and the castle approval ledger: hashed review data
  ready to become exemplar candidates.
- `audit_scene_congruency.py`: a working palette-match gate to generalise.
- `scripts/storybook_ui.gd`: centralised interface tokens to copy for art.

## 8. Method and limits

Three read-only sweeps (governance documents; other art documents; code,
data and tools) plus direct inspection of six approved images and the
measurements in section 4, all at the head named above. The measurements
sample source files with fixed seeds; they are not state-local runtime
evidence (`DL-VIS-08`) and grant no visual acceptance. No image was created
or edited, and no image-producing script was run.

# Codex handoff: job-game art, from flat vector shapes to painted ImageGen art (2026-10-17)

**Owner request to Claude (2026-10-17):** "Identify weak artwork currently in
the game, particularly in the jobs, a lot of artwork doesn't use image-gen.
Identify where image-gen versions have been made, and are not properly
implemented, and where they are still needed, we are trying to eliminate flat
vector art. Then, make a handoff for codex to be able to revise these"

**Owner direction to Codex the same day** (quoted in Codex's
`OWNER_PRIORITY.json` on `codex/flat-vector-r6-20261012`): "Insure that all
job games have high quality artwork all around, use image-gen 2.5 when art is
sub optimal to retain quality."

**Roles.**
- **From:** Claude: written audit, specifications and briefs. No game change,
  no images.
- **To:** Codex: every code change, every image and every capture.
- **Owner:** answers Q1-Q5 below and accepts the look.

**Status:** `PROPOSED / CANDIDATE`, revision 3.
- Revision 3 records the owner's answers of 2026-10-18 to Q1-Q5 (see
  [Owner answers](#owner-answers-2026-10-18)).
- Revision 2 corrected three
counts from revision 1:
- every career, not nine, has at least one code-drawn object the child acts on;
- four code paths, not three, request art that was never made;
- the shared gesture surface serves eleven careers, not nine.

It also records that none of the stranded images is named in Codex's
flat-vector packet.
- Baseline: `dev` `7a65b9f0abacddeee70230f220955f4d18d551b5`.
- Finding: [`MA-VIS-010`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-010)
  (P1, `CONFIRMED_OPEN`).
- Delivery states:
  - `ARCHIVE_COMPLETE` after the remote verification below.
  - `GENERATION_READY` for Codex's own ImageGen. Every input is a repository
    file named by path and SHA-256, and no generated board is bound.
  - `DELIVERY_ACCEPTED` false.

| Read | For |
|---|---|
| [AUDIT.md](AUDIT.md) | The evidence: what the child sees in every job, the painted art that exists but is not in the game, what is drawn badly, and why it keeps not landing |
| [BRIEFS.md](BRIEFS.md) | The written ImageGen briefs, rules C1-C10 and the style anchors |
| [data/job_art_register.json](data/job_art_register.json) | All 108 items, each with its code location, class, severity, available art (path, branch, SHA-256), action, brief and package |
| [data/measure_baseline.json](data/measure_baseline.json) | The numbers at the baseline, from the tool |
| [tools/measure_job_art.py](tools/measure_job_art.py) | Numbers-only measurement: code drawing per job, phase art, SVGs, asset wiring, stranded art with alpha checks, and the program's runtime-change ratio. Rerun after every package. |

## What is wrong, in one screen

- **The careers are mostly code-drawn.** The Opera career code makes 972
  primitive draw calls against 107 texture draws.
  - 28 of the 61 career phases draw their own picture in code.
  - Geologist has no painted room or work object at all, and its gold-star
    authored-art score is 0.
  - Teacher loads no texture.
  - In every other career at least one object the child acts on is
    code-drawn:
    - Chef: the oven and cake.
    - Boxer: the gloves.
    - Candymaker: the candies.
    - Doctor: the sink and the patient.
    - Farmer: the seed bed and the gate.
    - Magician: the rope and the portal.
    - Painter: the cover.
    - Nursery: the crib, the blanket and the hand.
    - Pop Star: the stars.
    - Ballerina: the shell frames and the ribbon.
    - Racer: the steering wheel and the turbo button.
    - Detective: the clues.
  - Five SVG files are live.
- **Painted art was made and not used.**
  - 74 painted job images are stranded on unmerged branches. They include the
    whole Geologist set, the Nursery wash and care frames, the Boxer gloves
    and kart views.
  - A complete painted Geologist grotto has sat in `assets_src` since
    2026-09-05.
  - Four code paths ask for art that was never made: pipe tiles, star notes,
    portal rings and success images for six careers.
  - Two Geologist texture paths are empty strings.
  - Painted art is loaded and not drawn, or drawn stretched, ghosted or
    covered (AUDIT section 6).
- **ImageGen is still needed** for 57 of the 108 register items. The other 51
  are wiring, drawing fixes, deletions or work already in flight.

## Packages, in order

Owner answer Q1 ("all the above"): every package below is first priority.
- Run packages in parallel where they do not edit the same files.
- Packages that edit `scripts/opera_gesture_surface.gd` (P4, P6, P7 and P8)
  take turns in that file, in the order listed.

Each package is one branch from current `dev`, carrying:
- one impact record;
- the register items and briefs named below;
- before and after numbers from the tool;
- captures at 1280×720 and 1600×720 with the HUD (BRIEFS C8);
- green CI, then a merge to `dev`.

Close each register item by setting its outcome in the package's impact
record. Do not open a new evidence round per item.

### P0 Governance and process (small; do first)

1. **Land the owner's 2026-10-17 text on `dev`.** "Art quality and ImageGen"
   replaces "Art reuse and generation budget".
   - Today it exists only as an uncommitted edit to `CLAUDE.md` and
     `AGENTS.md` in the main checkout, and in rescue snapshot `e3aefde2`.
   - These are high-risk files. The owner decision is explicit; commit the
     owner's text as written and say so in the commit message.
2. **Revise `DL-ASSET-01`, `DL-ASSET-02` and `DL-ASSET-06`** in
   `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` to match:
   - reuse is an option, not a prerequisite;
   - ImageGen is chosen for quality;
   - the provenance and licence duties are unchanged.
   - Record the decision with `tools/record_owner_decision.py`.
3. **Remove the comments that tell code to avoid painted art**, as each job
   is repaired: `opera_boxing_surface.gd:776-777` and
   `opera_geology_surface.gd:40-41`.

### P1 Geologist (items JA-GEO-01 to -08; briefs JB-GEO-01, -02)

- **Wire the stranded set** from `codex/job-art-review-v2-20261001`
  (`cfcadc96`). Cherry-pick only the image files and their provenance; do not
  merge the branch, which is 139 commits behind `dev`.
- **Set the two empty paths** `PAN_PATH` and `GEODE_PATH`.
- **Delete** the three SVG uses and the code tray, river, dirt grid, pan and
  geode.
- **Generate** the grotto backdrop and the crest.
- **The pan:** decide the pan together with Codex's in-flight
  `codex/flat-vector-geologist-pan-runtime-20261017`; ship one design.
- **The mineral:** stop the separate mineral generation (`r96`/`r97`), because
  `painted_work_v1/mineral.png` exists.

**Done when:**
- no Geologist file draws its objects in code;
- no SVG remains;
- the vector-room fallback is gone;
- the curtain call uses the shared finale stage.

### P2 Teacher (JA-TEA-01 to -07; JB-TEA-01 to -05)

**Generate:** the lesson board, shape tiles, pearls and trays, answer cards
and crest.

**Wire:** the guide hand A6 for hints.

**Done when:**
- `opera_teacher_surface.gd` draws only textures;
- the lesson geometry and voice cues are unchanged;
- the trusted Opera probes pass (`probe_opera`, `probe_opera_2d`,
  `probe_opera_gesture_quality`). There is no Teacher-specific probe, so add
  one that fails if a lesson texture is missing.

### P3 Astronaut (JA-AST-01 to -06; JB-AST-01 to -04)

**Generate:** the pipe set at the exact file names the code already requests,
plus the tank, intake, napping imp, painted patches and launch flame.

**Do not wire:** the stranded brass gear or the neon fluid (AUDIT 3.1).

**Done when:** the PIPES board draws no primitive except functional hit
geometry, and `probe_opera_pipe` passes with the textures required.

### P4 Chef (`MA-OPERA-001`; JA-CHF-01 to -09; JB-CHF-01 to -03)

**Wire:**
- the Chapter Two bowl, batter and cakes;
- the painted cake that is loaded but never drawn.

**Fix:**
- the jug aspect, and make the jug empty as it pours;
- the whisk pivot;
- the stack cap.

**Generate:** the oven states, the frosting stroke and a new chocolate
topping.

**Done when:** BAKE, MIX, STIR and FROST show painted objects only, and the
owner looks again at the Chef (the owner rejected its look on 2026-10-03).

### P5 Nursery and Boxer (stranded art; JA-NUR-01 to -06, JA-BOX-01 to -05)

**Wire:**
- the stranded cradle hands and pillows;
- the wash frames (WASH HANDS currently shows nothing);
- the care frames, as they are (owner answer Q3: "use them");
- the crib mobile;
- the painted gloves.

**Generate:** the bottle states, crib and quilt, patting hand, invitation
ring and pearl lamps.

**Probe:** `probe_opera_nursery` must pass.

### P6 Doctor, Farmer, Magician, Painter (JA-DOC-*, JA-FRM-*, JA-MAG-*, JA-PNT-*)

**Wire:**
- the painted rope;
- the existing soap bubbles;
- cut-outs from the retired cards: Doctor sink, cast and cushion (AUDIT 3.6).

**Fix:**
- move the painted Magician hats in TRACK;
- remove the gold slabs over the painted knob and lock;
- remove the Farmer face and basket duplicates;
- remove the Painter frame slab;
- restore the banner aspect.

**Generate:** the briefs JB-DOC-01 to -03, JB-FRM-01 to -03, JB-MAG-01 and
JB-PNT-01.

### P7 Ballerina, Racer, Pop Star, Detective, Candymaker (JA-BAL-*, JA-RAC-*, JA-POP-*, JA-DET-*, JA-CDY-*)

**Generate:** the shell frame, ribbon, twirl ring, race controls, singing
stars, music notes and wrapper twist. For the SHARE recipients, use stuffies
(owner answer Q4, brief JB-CDY-02).

**Fix:** the crops, the 60% ghosting and the tilted mic.

**Coordinate:** Detective, Pop Star rhythm and Candymaker SORT are in flight
(see below). Verify them against this register when they land.

### P8 Shared career layers (JA-SHR-01 to -10)

**Remove:**
- the spotlight wedges over the 13 painted rooms;
- the causal-backdrop and playfield stripes;
- the ambient doodles in jobs (owner answer Q2: "yes" to the default).

**Replace** with painted families:
- the invitation ring;
- pearl progress;
- confetti and sparkle;
- Hall HUD medals, panels and bars;
- storybook frames.

**Fix:** draw the lanes at full opacity and use the painted guide hand for
every demo.

### P9 Chapter Two, Day One, Fashion, Arborist (JA-CH2-*, JA-D1-*, JA-FSH-*, JA-ARB-*)

**Chapter Two:**
- generate the strawberry candy station and the storybook spread;
- wire the cake's first stage;
- fix the banner;
- generate party hats as separate layers. The protected portraits stay
  untouched (`DL-ASSET-03`).

**Day One:**
- remove the code dirt wash, cracks and bands (owner answer of 2026-10-05,
  `ODR-POOL-DIRT-LOOK-20261005`);
- show the painted bathroom guides;
- replace the craft-room emoji and glyphs with the guide hand and sparkle;
- generate the paint pots;
- generate painted danger marks for Grand Puff;
- replace the 3D cube "sparkles" with `fx_stolen_sparkle.png`.

**Fashion:** generate painted lock, check and arrow icons (`MA-TYPE-004`).

### P10 Census gate and clean-up (JA-CLN-01)

**The gate.** Promote this packet's tool to `tools/audit_job_art.py --check`,
with a committed baseline at the first repaired package:
- the job scripts' primitive draw count may only fall;
- runtime SVG files are zero;
- any new primitive drawing call in a job script needs an allowlist entry
  marked `FUNCTIONAL` (hit area, debug).

Add it to the static gates in `scripts/ci.sh`. The workflow file needs no
change.

**Clean-up.** Delete the dormant code fallbacks of each repaired job and make
missing textures fail its probe (BRIEFS C9).

## Working with what is in flight (checked 2026-10-18)

| Codex work | State | Overlap |
|---|---|---|
| `codex/flat-vector-r6-20261012` (R6 to R100) and `codex/flat-vector-geologist-pan-runtime-20261017` | pushed; pan CI running | P1. Use this register as the job worklist and record its closures in the flat-vector tally as a by-product. None of the 74 stranded images appears by name anywhere in that program's packet. The grotto appears there only in source hash lists, and `codex/job-art-review-v2-20261001` only in CI checkout logs. |
| `codex/flat-vector-touch-runtime-20261016`, `codex/flat-vector-navigation-runtime-20261017` | pushed, unmerged | none (shared UI outside jobs) |
| local `candymaker-boxes-friends-20261017` | uncommitted | JA-CDY-01; that work's new `candymaker_sort_boxes_v2.png` |
| local `detective-scene-investigation-20261017` | uncommitted | JA-DET-01 to -03; re-check after it lands |
| local `popstar-rhythm-20261017` | uncommitted | JA-POP-01 (close it if the stars go) |
| `codex/studio-scene-integration`, local `studio-room-repair-20261017` | in progress | Day One craft room; studio furniture images |
| local `pool-visual-repair-20261017` | committed locally, pushed | Day One Pool; not in this packet |
| `codex/arborist-spray-20261015` | pushed, unmerged | JA-ARB-01 |

## Questions for the owner

The owner answered these on 2026-10-18; the answers and what they change are
in [Owner answers](#owner-answers-2026-10-18).

| # | Question | Default if unanswered |
|---|---|---|
| Q1 | Which jobs first? | Geologist and Teacher (the two that are almost all code), then Astronaut and Chef, then the stranded-art wins (Nursery, Boxer), then the rest |
| Q2 | Ambient doodles, spotlights and sparkle rings drawn over the jobs: remove them, or repaint them as painted effects? | Remove the spotlights, backdrop stripes and ambient doodles from job scenes; replace the invitation halo and sparkles with one painted ring and sparkle family |
| Q3 | The stranded Nursery frames show Roshan in the older career design (loose rainbow lock, headband, no tiara), which matches the Nursery atlas the child sees in the same scene. Use them, or regenerate them following the base-world child (`ODR-ROSHAN-Q13`)? | Use them in the Nursery so the scene stays consistent; new Roshan art elsewhere follows the base-world child |
| Q4 | Candymaker SHARE needs six friends. New painted sea friends (seahorse, pufferfish, crab, turtle, octopus, starfish), or the protected family friend portraits? | New painted sea friends; the protected portraits stay untouched |
| Q5 | May Codex work in one branch per package, with one impact record and green CI before merging, and stop publishing per-step receipts for internal work? | Yes. External handoffs (Grok and others) keep the full GitHub delivery rule. |

## Owner answers (2026-10-18)

The owner answered in the session, quoted verbatim below. The answers are
recorded in the owner decision register (`design/reference/OWNER_DECISIONS.md`).

| # | Owner answer | Decision ID | What it means for Codex |
|---|---|---|---|
| Q1 | "all the above" | `ODR-JOBART-ORDER-20261018` | Every job package is first priority; no job waits for another. Packages run in parallel where their files do not overlap. Where they share a file, they go in the listed order. |
| Q2 | "yes" | `ODR-JOBART-DECORATION-20261018` | The stated default is accepted. Remove the spotlight wedges, the causal-backdrop and playfield stripes, and the ambient doodles from job scenes (JA-SHR-01, -04, -07). Replace the invitation halo and the sparkles with one painted ring and sparkle family (JB-SHR-02, JB-SHR-04). No ambient motif atlas is needed (JB-SHR-01 closed). |
| Q3 | "use them" | `ODR-JOBART-NURSERY-FRAMES-20261018` | Wire the stranded Nursery care and wash frames as they are, in the older career design, in the Nursery (JA-NUR-02, JA-NUR-03). New Roshan art elsewhere still follows the base-world child (`ODR-ROSHAN-Q13`). |
| Q4 | "use extra stuffies" | `ODR-JOBART-SHARE-STUFFIES-20261018` | The Candymaker SHARE recipients are stuffies, not new sea creatures and not the protected friend portraits. Codex's in-flight Candymaker work carries an earlier direction of 2026-10-17 (`ODR-CANDY-BOXES-FAMILY-20261017`, not on `dev` at revision 3) naming Baby Eagle, Rumi and Daddy Mermaid, with voiced thanks. Any further recipients are extra stuffies, Lamb-a' and Mewsha first (brief JB-CDY-02). |
| Q5 | "yes" | `ODR-JOBART-PROCESS-20261018` | Codex works one branch per package, with one impact record, green CI, then a merge to `dev`. It stops publishing per-step receipts for internal work. External handoffs (Grok and others) keep the full GitHub delivery rule. |

## Delivery

This packet is committed and pushed to `Ebonyks/mermaid-roshan-reef` on
branch `claude/job-art-imagegen-audit-20261017`.

- Revision 1 (`569dbf04`) passed anonymous verification: the manifest and
  all 7 files matched bytes and SHA-256.
- Each revision's immutable tree link, manifest link and receipt are in
  [REMOTE_VERIFICATION.json](REMOTE_VERIFICATION.json).

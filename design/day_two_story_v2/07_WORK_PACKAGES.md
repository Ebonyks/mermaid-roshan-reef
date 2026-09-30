# 07 — Work packages for Astra

Part of the [Day Two story draft v2](README.md). Status: `CANDIDATE`,
2026-09-30. This breaks the whole draft into self-contained packages. The
story each package builds is in the [plotline](00_DAY_TWO_PLOTLINE.md); its
[section 13](00_DAY_TWO_PLOTLINE.md#13-for-astra-from-the-built-levels-to-this-day)
maps each built level to its completed scene. Each
package names its inputs, outputs, dependencies and acceptance, so it can be
picked up without reading the rest of the conversation that produced it.

## Rules every package follows

- Read `CLAUDE.md`, `AGENTS.md`, the master audit planning entry and the
  document ledger first. Every change needs a `design/audit_impacts/*.json`
  record and passing `tools/audit_document_authority.py` and
  `tools/audit_development.py --base auto`.
- Godot 4.7.2 exactly; true 2D Canvas; Mobile renderer; no 3D, no new lights.
- Never alter `assets/book/`, `assets/audio/voices/` family recordings, or
  `assets/characters/friends/`. New textures ≤1024 px or power-of-two; every
  new asset gets an `ASSET_LICENSES.md` line in the same commit.
- Non-reader rules: every objective has an exact spoken line and a moving
  picture cue; no fail states; passive input never wins; one finger.
- Saves: never remove keys; add with defaults; every milestone saves and
  restores the same picture after an app restart.
- Keep new logic out of `scripts/main.gd`: satellites and thin delegation
  only (`DL-CODE-01`).
- Report implementation, machine checks, and outstanding visual, device,
  child and owner acceptance separately.

## Dependency order

```text
WP-00 owner decisions
  └─► WP-01 authority updates ─► WP-02 save model
        ├─► WP-03 opening + party plan ─┐
        ├─► WP-04 practise→for-real routine ─┬─► WP-06 cameo system
        │                               └─► WP-05 in-world level host
        │                                         └─► WP-07…WP-14 jobs J1–J8
        ├─► WP-15 Lamma (Day One inserts can start after WP-02)
        └─► WP-16 finale ◄── WP-07…WP-14 results, WP-15
WP-17 voice ◄── lines from 03/04 (can start after WP-00)
WP-18 graphics fixes ◄── 06 (most can start immediately)
WP-19 Book Two rough, WP-20 cinematic cards ◄── WP-00
WP-21 probes and acceptance runs alongside every package
```

## Packages

### WP-00 — Owner decisions (blocking)

- **Goal:** answers to the thirteen decisions in the
  [README](README.md#owner-decisions).
- **Output:** a dated owner-decision note appended to the README.
- **Acceptance:** each decision recorded verbatim with its date.

### WP-01 — Update the binding documents

- **Depends on:** WP-00.
- **Inputs:** 01, 03, 04 of this package; the current spine and cake
  contract.
- **Outputs:**
  - `design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md`: Arborist
    replaces Candy Maker; new sequence and masks (Arborist-first:
    `[18, 6, 0, 10, 2, 13, 11, 1]`, chapter mask `0x42C47`); the
    practise-then-for-real routine; Chef's strawberry-topping step.
  - `design/CHAPTER2_CAKE_VISUAL_PROGRESSION_2026-08-31.md`: Chef owns bits 5
    and 6.
  - `DL-INT-12`/`DL-INT-07` only if WP-00 chose Opera Hall launches or a
    freeplay Arborist.
  - The lawn finale draft marked superseded by `04`.
  - Ledger rows and an impact record.
- **Acceptance:** the document audit's mask and sequence checks pass against
  `scripts/chapter_two_party_plan.gd` after WP-02.

### WP-02 — Save model and migration

- **Depends on:** WP-01.
- **Outputs:** additive keys with defaults:
  - `chapter2_party_tree_phase` (0–4);
  - `lamma_moments_seen` (bitmask of LAMMA-1…3);
  - `lamma_joined` (mirrors the existing `friend_lamma` unlock);
  - `chapter2_lawn_tour` (bitmask);
  - `chapter2_cameo_seed`;
  - per-job `chapter2_job_levels` (bit 0 practice done, bit 1 world level
    done).

  Migration:
  - A legacy Candy Maker bit in `chapter2_party_piece_mask` credits the
    Arborist and sets the tree to blooming.
  - A save mid-chapter under the old order gets the Arborist as its next job
    without losing any finished job.
  - Saves past Day One mark LAMMA-1 and LAMMA-2 seen.
- **Acceptance:** `probe_chapter2.gd` covers every migration case, including
  malformed values, and restores the same visuals after restart.

### WP-03 — Opening and Daddy's Party Plan (D2-OPEN-1…3)

- **Depends on:** WP-02.
- **Outputs:**
  - Lamma's Episode One peeks can wait for WP-15; this package covers Day
    Two's start.
  - The birthday wake-up in the attic's bubble pile (`D2-OPEN-1`).
  - The Day Two card rewritten: night to dawn, the attic window glowing, a
    birthday picture, Daddy's whisper; no job medallions.
  - **Daddy's Party Plan:** a picture scroll on an easel in the Main Hall,
    eight frames, the next one glowing, filled frames showing the real party
    pieces; and the **R-beat** after every job, where Daddy arrives with the
    scroll wherever Roshan finished.
  - **The guest row and the function beat** (the party-preparation script,
    [plotline](00_DAY_TWO_PLOTLINE.md#what-each-job-gives-the-party)): the
    seven invited friends along the bottom of the scroll, as small runtime
    views of the protected portraits, plus one empty "one more" frame; in
    each R-beat the friend the piece is for hops into its frame while Roshan
    says the job's function line (`Jn-FN`). No new save: the pictures follow
    the party bits, and the empty frame follows `lamma_joined`.
  - The Main Hall's party dressing as the day goes on (bunting, balloons,
    the glowing doors), world-locked ([GFX-HALL-12](06_GRAPHICS_AUDIT.md)).
  - Every opening line voiced.
  - The caption-only chapter-start message removed.
- **Acceptance:** a non-reader can reach the first job from the Main Hall
  using only voice and pictures; captures of the board at 0, 4 and 8 pieces,
  with the guest row, and after R5 with Lamma in the one-more frame; protected
  portraits byte-identical.

### WP-04 — The practise-then-for-real routine

- **Depends on:** WP-02.
- **Outputs:**
  - For each job, its room card launches the Opera practice (level 1),
    cut to the steps named in the plotline through the dormant
    `chapter2_tutorial` path: no rival race, a short bow. The bow hands
    Roshan the costume piece and routes her to level 2.
  - The imp apprentice at every practice: arrive, copy, grab the prop, get
    booped, drop it and scurry off, using the existing `imp_op_*`
    recordings (new lines for the Arborist).
  - A one-phase warm-up for children who already hold the career star.
  - Grand Puff as the travel guide between places, including the Sky Lagoon,
    and the next job's door lit in the Day One golden-door language
    ([GFX-ROOM-06](06_GRAPHICS_AUDIT.md)).
- **Acceptance:** each job's two levels play in order; leaving mid-way
  resumes at the right level; no central all-career picker unless WP-00
  changed `DL-INT-12`.

### WP-05 — In-world level host

- **Depends on:** WP-04.
- **Outputs:** a reusable room-mounted activity host, following the Day One
  pool pattern (`scripts/games/day_one_pool_cleanup.gd` mounting
  `pool_skimmer_activity.gd`, `pool_waterfall_activity.gd` and
  `pool_seahorse_rescue_activity.gd`). It:
  - mounts the Opera gesture surfaces (pour, circle, oven, tap, swipe, hold,
    choice, lens, pipe, echo, ballet) inside the room's own art;
  - makes Roshan travel to each object and visibly do the action
    (`MA-PLAY-004`);
  - exposes phase callbacks to the Chapter 2 director.
- **Acceptance:** one job (recommend J3, Kitchen) fully playable in the
  Kitchen room art with passive, held, off-target, focus-loss and re-entry
  probes.

### WP-06 — Mixing Day One friends into challenges

- **Depends on:** WP-05.
- **Outputs:**
  - The four challenge roles (Mischief, Helper, Coach, Hint), seeded
    selection, per-level slots and quotas, and every job's deck of cards, as
    specified in the [plotline](00_DAY_TWO_PLOTLINE.md#5-the-challenge-mix)
    (section 5 and each job in section 8).
  - Art and motion for: Daddy's demonstration, Baby Eagle carrying and
    spotting (also on the Sky Lagoon), dust bunny mischief (hide, puff,
    roll, tangle), and the rainbow friend hopping to a target (he has no
    wings).
- **Acceptance:** fixed-seed probes prove determinism; the quota and
  no-repeat rules hold over a full playthrough; no role can block or undo
  progress.

### WP-07 … WP-14 — The eight jobs

One package per job, each covering level 1 (the Opera practice) and level 2
(the in-world level) exactly as told in the plotline's
[Act II](00_DAY_TWO_PLOTLINE.md#8-act-ii-one-little-job-at-a-time), with the
steps and gesture modes in [03](03_LEVEL_DESIGN.md): its voice lines, visual
cues, challenge deck, R-beat, saves and assets:

| Package | Job | Level 2 place | Notes |
|---|---|---|---|
| WP-07 | J1 Arborist | Sky Lagoon lawn, party tree | Needs the Arborist art committed first; new career (Arborist handoff); the petal nest in the shade; Baby Eagle's lookout perch on the mended branch |
| WP-08 | J2 Farmer | Sky Lagoon strawberry grove | Reuse Chapter 2 Farmer phases in-world; R2 gives the dust bunnies one more berry, and they fill a tiny berry basket for every friend (shown, no input) |
| WP-09 | J3 Chef | Royal Kitchen | Adds the strawberry-topping phase; the finished cake shows the empty shell candle holder from then on; the cut-cake state for F7; LAMMA-3 at the end |
| WP-10 | J4 Painter | Craft Room | Banner goes to the party tree via Baby Eagle; the paint reveals Roshan's own picture in the medallion; R4 hangs it on the mended branch ("On the branch we mended!") |
| WP-11 | J5 Ballerina | Stuffie Playroom | Starts with LAMMA-JOIN (WP-15); the grand twirl spins as fast as the child draws (the wild half); R5 fills the one-more frame with Lamma |
| WP-12 | J6 Pop Star | Opera Hall stage | Rumi has no voice: her memory is shown as a picture and said by Roshan |
| WP-13 | J7 Astronaut | Mermaid Pool | Rainbow waterfall fuels the rocket; seahorse helps; the rocket's three-blink countdown is built with WP-16 |
| WP-14 | J8 Detective | Royal Library | The unlit candle; completes the party |

- **Acceptance for each:** strict order; passive, held and off-target input
  earn nothing; save at every phase; persistent piece visible in the room,
  on the Party Plan (with the friend it is for) and on the lawn; the job's
  function line voiced in its R-beat; captures at two aspects.

### WP-15 — Lamma

- **Depends on:** WP-00 (decision 9: her name, and whose lamb she is), WP-02
  (Day One inserts), WP-05 (LAMMA-3, LAMMA-JOIN), and
  [GFX-LAMMA-01](06_GRAPHICS_AUDIT.md#gfx-lamma-01) (one canonical design).
- **Starting point:** she cannot be unlocked in real play today. The
  `boss_lamma` battle has no authored caller and the Seek game has no live
  entry, so this package builds her first reachable path. She has no Day One
  moment and no sound of her own.
- **Outputs:**
  - LAMMA-1 (Playroom tent, Day One) and LAMMA-2 (Craft Room jars, Day One)
    as in-room gameplay peeks, never inside story clips (`DL-CIN-16`);
  - LAMMA-3 in the Kitchen, leaving floury bounce marks and her dropped egg;
  - LAMMA-JOIN as a four-find game built on `scripts/games/seek.gd` (wool,
    bounce marks, her egg, then Lamma in the tent), given a live entry in the
    Playroom;
  - the `friend_lamma` unlock on joining;
  - her presence in the stuffie ballet and the finale, staged so only one
    Lamma is ever on screen (Evie's portrait already holds her; see
    [GFX-LAMMA-02](06_GRAPHICS_AUDIT.md#gfx-lamma-02));
  - poses in the canonical egg-carrying design: peek, hide, bounce away,
    sniff, hug the egg, dance, hat offer;
  - a soft lamb bleat sound effect (new, licensed and listed in
    `ASSET_LICENSES.md`);
  - the legacy lines that speak for her through Evie's voice (the roster
    hello and the capture plea) revised or retired with the owner.
- **Acceptance:** the join game is completable without having seen every
  sighting; saves at each clue; the companion roster shows Lamma afterwards;
  a capture of every Lamma moment shows the same design.

### WP-16 — The party chapter (F1–F8)

- **Depends on:** WP-07…WP-15.
- **Outputs:** everything in plotline sections 9 and 10, with the production
  detail in [04](04_FINALE_PARTY_CHAPTER.md):
  - the party map (each guest beside the piece made for them, a tiny berry
    basket beside each, the petal nest by Faron), the candle set in its
    holder, and the payoff tour with each piece's friend reacting as a whole
    picture (existing guest clips optional, unaltered);
  - every party need met in the scenes: Baby Eagle's hello from the mended
    branch (F1), the countdown and Kareem watching Rumi's show (F3), the
    Prince reading Roshan's picture on the banner (F4), the lawn falling into
    dusk without the candle and the cake shared after the wish (F7), and the
    friends going home with their berry baskets (F8);
  - ignition with Rumi's song, and the imp scout;
  - the royal entrance, with the King's "MY birthday party!";
  - three rounds with friend shelter layers and painted warnings;
  - the King's motion set;
  - the Prince's acting;
  - the theft composition;
  - Lamma's comfort and the wish;
  - the evening walk and the sky-door reveal;
  - the birthday evening (supper with the cake, the movie of the day, the
    sleepover), reskinning the existing comfy games.

  Also removes the stale scout and "north-star clue" lines and objective from
  `scripts/main.gd`.
- **Acceptance:** existing lawn probe cases still pass; the new beats save
  and resume; the reassurance can never be skipped after the theft; captures
  of every beat.

### WP-17 — Voice production

- **Depends on:** WP-00 (voice decision).
- **Outputs:**
  - Every line in the [voice lines](03_LEVEL_DESIGN.md#voice-lines) produced
    through the Parler candidate/selector/master pipeline as provisional
    filler, with new presets for the King and the Prince.
  - Distinct keys for new Daddy lines; no Rumi voice; nothing trained or
    conditioned on family recordings.
  - Caption text matches each voice line exactly.
- **Acceptance:** exact-word ASR gate passes for every line; owner listening
  session recorded.

### WP-18 — Graphics fixes

- **Depends on:** nothing for the first three groups; WP-00 for the
  owner-gated items.
- **Outputs:** the GFX-* fixes in [06](06_GRAPHICS_AUDIT.md), in the order of
  its [fix table](06_GRAPHICS_AUDIT.md#10-fix-order-and-work-packages):
  1. Can the child finish, and does it look broken: GFX-DET-03 (the candle
     touch area), GFX-SYS-13 (steps with no pointer, with the 05 B1 repair),
     GFX-HALL-07 (the party table glued to the screen) and GFX-HALL-08 (the
     cake hiding the candle).
  2. Fixes with no new art: the career-world framing (GFX-SYS-01, -02),
     spotlights, wide-phone side panels, honest scene tags, Detective
     targets, the cherry-cake invitation, stray work and cheer cells, dead
     ember actors, the shipped superseded cake.
  3. Derivative repairs: the costume tail alpha, the cake ledge and berry
     size, the banner states, the berry trays.
  4. Owner-gated: costume identity (decision 10), protected-art
     re-isolations (decision 11).
  5. The venue plaques and done states.

  The in-world, Lamma, finale and opening fixes ride with WP-05 and WP-07 to
  WP-16, as the fix table lists.
- **Acceptance:** before/after captures at 16:9 and 20:9 for every fix;
  protected files byte-identical; every derivative has a hash, provenance
  and an `ASSET_LICENSES.md` line; owner art review.

### WP-19 — Book Two rough

- **Depends on:** WP-00.
- **Outputs:** a Book Two rough on the book branch
  (`codex/mermaid-roshan-picture-book`, new `books/chapter_two/`) from the
  [manuscript](02_PICTURE_BOOK_MANUSCRIPT.md), sourcing art under
  `DL-ASSET-08` and recording every gap.
- **Acceptance:** 34-page proof; gap list; owner read-through.

### WP-20 — Cinematic cards

- **Depends on:** WP-00, WP-16 staging.
- **Outputs:** revised Grok shot cards replacing C2-01…C2-09 for the new
  finale beats, using `design/templates/IMAGINE_SHOT_CARD_V1.md`, published
  and verified on GitHub per the handoff rules.
- **Acceptance:** `ARCHIVE_COMPLETE` / `GENERATION_READY` /
  `DELIVERY_ACCEPTED` reported separately.

### WP-21 — Probes and acceptance

- **Runs with:** every package.
- **Outputs:**
  - Probe updates: `probe_chapter2.gd`, `probe_chapter2_lawn.gd`,
    `probe_chapter2_farmer_resume.gd`, new `probe_arborist.gd`,
    `probe_lamma.gd` and `probe_chapter2_cameo.gd`.
  - A Day Two playtest protocol modelled on
    `audit/day_one_playthroughs_2026-09-02/`.
- **Acceptance:** green CI on each package's head; device 30 fps; a recorded
  child session; owner review.

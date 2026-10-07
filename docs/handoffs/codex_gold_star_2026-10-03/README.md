# Codex handoff: gold-star audit, Pool five-star proposal and the work that follows (2026-10-03)

Status: `PROPOSED / CANDIDATE`. Written by Claude. Claude writes specifications and audits and did the Pool's coding at the owner's explicit request; Codex builds every image, board and capture, and takes the repairs below. Nothing here grants acceptance or release.

| Start here | What it is |
|---|---|
| [AUDIT.md](AUDIT.md) | The game-wide audit at dev `87f99268`: strongest and weakest games, what a child can reach, new findings, why the Mermaid Pool is the reference |
| [POOL_FIVE_STAR.md](POOL_FIVE_STAR.md) | The Pool's proposed five-star implementation (Claude's code), its verification, the three human checks for a gold star, and the art and voice handoff GS2 |
| [Gold-star scorecard](../../../design/reference/GOLD_STAR.md) | Live ranking, rubric and reference patterns, rendered by `tools/gold_star.py` |
| [Recipe](../../../design/reference/recipes/gold_star.md) | How to raise a game to the gold star; say "bring fetch up to the gold star" |

## The tasks, in order

### GS0. Repair the P0: Chapter 2 story careers cannot start ([`MA-PLAY-005`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-005))

**Effect today.** After Grand Puff, the first party job (Farmer, Dining Room) opens a broken scene. The party can never finish, so the following never appear on a fresh save:

- the lawn finale;
- the Galaxy and Fairy route;
- every free-play Opera career card.

**Two causes, both confirmed:**

1. **Empty phase override.**
   - `OperaCareerWorld2D.setup` copies a missing `phase_overrides` key as an empty list (`scripts/opera_career_world_2d.gd`, the `override_config["phase_overrides"] = config.get("phase_overrides", [])` line).
   - The run context marks Chapter 2, so `ChapterTwoAdapter.validate_config_overrides` rejects the empty list (`validate_phase_overrides`: `phases.is_empty()` returns false).
   - Setup then returns early. The world has no phases, stations or surface, and `_process` raises script errors every frame.
2. **Unmapped story steps.**
   - Even with phases, `_assign_stations` maps by phase name through `PHASE_STATIONS`, which lists only free-play names.
   - So 19 of the 29 story steps of the eight party careers never arm a room object:
     - every Farmer, Candy Maker, Ballerina and Detective step;
     - Chef STACK;
     - Painter STAMP and HANG;
     - Astronaut BUILD ROCKET and READY PARK;
     - Pop Star STAGE RUMI.

**Specification.**

1. Pass only real overrides: copy `phase_overrides` into `override_config` only when the key exists and is non-empty, and let `ChapterTwoAdapter.resolve` supply the story phases.
2. Give every story step an authored opening:
   - Either add a `station` to each story phase in `ChapterTwoAdapter.PHASE_SETS`, and have `_assign_stations` prefer `phase.station` over the free-play name map;
   - or open the task directly where the story owns its own targets. The Farmer's five strawberries are such targets: they appear only once the task is open.
   - Choose stations from each career's existing `StagePaths` landmarks, following the scene's canon. Invent no new room object.
3. Add a trusted probe that launches each of the eight party careers through the real room route with the director's config (`_start_opera_from_room` and `OperaHouse.start`). It must assert:
   - no rejection error;
   - a non-empty phase list;
   - an armed opening for every step;
   - completion of every step with real touch events;
   - for the whole party: lawn finale and free-play cards appear.

**Done when** the finding's acceptance holds on a phone too. Re-assessment: Claude then re-scores the 21 blocked games (`python -B tools/gold_star.py --check` lists them as stale once their code changes).

### GS1. Repair the Astronaut two-finger soft-lock ([`MA-OPERA-013`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-013))

**Specification.**

1. Give `scripts/opera_gesture_surface.gd` per-touch ownership (gold-star pattern GS-10, from `opera_boxing_surface.gd`):
   - ignore presses and drags from another index while one is held;
   - cancel on focus loss and close.
2. Make `_pipe_press` refuse a new tray pick while `pipe_drag_tile` is set.
3. Extend `probe_opera_pipe` with a two-finger leg that proves round one can always finish.

The ownership change also helps every other generic-surface career.

### GS2. Pool art and voice

> **Status, 2026-10-04 (revision 5):** GS2-A carries forward as P2, GS2-B is replaced by reuse of the approved water-ripple atlas (done in code) and GS2-C carries forward as P7 in the [Pool five-star packet](../codex_pool_five_star_2026-10-04/README.md).

See [POOL_FIVE_STAR.md section 5](POOL_FIVE_STAR.md#5-codex-handoff-gs2-art-and-voice-for-the-pool):

- **GS2-A:** Roshan's scoop, scrub and tug actions under the owner's 2026-10-03 animation workflow: one job card per action, an editable Aseprite master with per-frame hand sockets, at least four drawn keys each, from the `roshan_base` identity. Pilot the scoop first; the owner reviews it before scrub and tug are made.
- **GS2-B:** an optional water ripple.
- **GS2-C:** six per-object skimmer lines through the Day One voice pipeline. The code already prefers them once their catalogue rows are READY.

Codex builds every board and capture.

### GS3. Gate the tool in the remote Probe Suite (needs the owner's explicit authority)

`scripts/ci.sh` already runs:

- `python3 -m unittest tools.tests.test_gold_star`
- `python3 tools/gold_star.py --check`

The protected workflow `.github/workflows/probes.yml` does not. It is a high-risk file, so these two lines wait for the owner's yes:

- append `tools.tests.test_gold_star` to its loop-tool `unittest` line;
- add `python3 tools/gold_star.py --check` after `python3 tools/audit_document_authority.py`.

### GS4. Keep the scorecard honest in every change

- `python -B tools/gold_star.py --check` fails when a new game file is not catalogued, and reports stale scores when judged code changes.
- Re-assess the criteria the change touched. Claude does this in review, or Codex proposes notes for Claude to confirm.
- Then run `--rebind GAME` and `--render`.
- Record phone, child and owner results in the game's `acceptance` lanes. Never raise C12 without that evidence.

### GS5. Fix the measured overdraw ([`MA-VIS-008`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-008))

> **Status, 2026-10-04 (revision 5):** the Pool's items are done by Claude and carved out as [`MA-VIS-009`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-vis-009) (fixed pending verification). That covers items 1 and 3 for the Pool, item 2 and the Pool's ripple arcs; see the [framework](../codex_pool_five_star_2026-10-04/FRAMEWORK.md). Item 4 needs no repair: the "255-layer burst" was a meter artifact, now corrected in `scripts/probe_overdraw.gd`. Everything below still applies to the other Day One rooms and the Opera careers.

The owner asked on 2026-10-04 for overdraw to be analysed specifically. The gold-star criteria now include six overdraw checks (OD1-OD6 under C7), measured on the real routes by `tools/measure_overdraw.py`. The method is GPU layer counts plus the live Canvas tree, numbers only. The [scorecard](../../../design/reference/GOLD_STAR.md) lists every result. `python -B tools/gold_star.py --compare GAME` ends with the ordered list for each game.

**What the measurement found** ([data](../../../design/reference/overdraw.json), dev `f07c1a48`):

- **Every dirty Day One room.** `scripts/arena/day_one_castle_dressing.gd` draws, in code, above the room art, the fixtures and Roshan:
  - a 12% purple-grey wash over the whole screen;
  - grime bands along the four edges;
  - drips and cracks.
- **The Pool:**
  - two identical cleanup baskets (`CleanupBasket`, `RescueCleanupBasket`) are drawn over each other during the skimmer;
  - `CastleLetterboxBackdrop`, a full-screen fill, is drawn 98% hidden under the room tiles;
  - Rumi's reveal briefly stacks 255 layers in one spot;
  - the swimming dust bunny's ripples are code arcs;
  - play states average 3.2-3.4 layers per pixel against a budget of 2.5.
- **Every Opera career:**
  - `opera_world_backdrop_2d.gd` draws props and stage spotlights in code over the painted backdrop;
  - `opera_world_hotspot_2d.gd` draws halos and sparkles in code;
  - the work surfaces draw objects as code shapes (`opera_gesture_surface.gd` for nine careers, plus the specialist surfaces);
  - `living_world_canvas.gd` draws ambient motifs in code above the career.
  - Codex's Chef repair already removed the room-sized focus lens.
- **Over the fill budget:**
  - Geologist's task: mean 5.75 layers, 61% of the screen with four or more, max 13.
  - Teacher's task: mean 3.5.

**Specification.**

1. Remove the castle dressing's code-drawn wash, grime, drips and cracks. A dirty room reads through authored dirt art, or through a declared tint with Roshan counter-tinted (pattern GS-17), per the owner's answer to question 5.
2. Draw one cleanup basket during the skimmer.
3. Crop or drop full-screen fills that sit hidden under opaque art (`CastleLetterboxBackdrop`, and `OperaStageBleed` where the backdrop covers it).
4. Find and cap the burst at Rumi's reveal (peak budget 32 layers).
5. Replace the code-drawn props, halos, spotlights, ripples and ambient motifs with approved art, or remove them. Codex builds any new art from Claude's written description.
6. Bring the Geologist and Teacher task frames inside the fill budget.
7. After each repair, run `python -B tools/measure_overdraw.py` and have Claude re-score. Record the painted-copy (OD1) and look-alike (OD2) reviews in each game's `overdraw_review`.

**Done when** OD1-OD6 pass for the game on the scorecard. Device frame time and the owner's look remain separate gates.

## Questions for the owner

1. **Who takes GS0?** Default: Codex repairs `MA-PLAY-005` first, before any other work; Claude re-scores afterwards.
2. **Dolls, Seek, Melody and the fish slide** are strong Canvas games with no way in since the reef was retired. Should each get a castle-room home, or be retired? Default: give Dolls and Seek a home first.
3. **GS3 workflow lines.** May the two gold-star lines be added to the protected Probe Suite workflow? Default: yes, exactly the two lines above.
4. **Opera Hall elevator.** It opens the "Job playtesting / DEV MODE" menu to any child who taps it. Should it stay until release, or be gated now? Default: keep it for your testing and gate it before the next release.
5. **Dirty-room look.** May a dirty Day One room keep any wash at all (as a declared tint with Roshan kept in her colours), or must dirt be authored art only? Default: authored dirt only; the room tint stays, the code-drawn wash goes.
6. **Overdraw budgets.** Are the starting budgets right (2.5 layers per pixel on average, at most 10% of the screen with four or more, max 8, peak 32)? Default: keep them until the phone session shows whether they predict stutter.

## Delivery

This packet is published on GitHub with a manifest and an anonymous fetch receipt. The links and hashes are given in the session report and in the [impact record](../../../design/audit_impacts/gold-star-pool-five-star-20261003.json).

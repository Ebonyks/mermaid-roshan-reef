# Codex handoff: visual polish, sprite audit and approved work (2026-09-25)

**From:** Claude (analysis and recommendations only; no game changes).
**To:** Codex (implementation, including any image generation).
**Owner:** approves anything that changes the game's look, in context on the phone.

**Status:**
- `PROPOSED / CANDIDATE`. Publication is not creative acceptance.
- No visual, device, child or owner acceptance is claimed.
- Every change still follows `CLAUDE.md`, `AGENTS.md` and the master-audit development
  contract: impact records, gates, CI, then integration into `dev`.

**Evidence baseline:** `dev` at `f76a8ba5` (2026-09-24), exact Godot 4.7.2 display
captures on isolated test saves.

## What is in this folder

| Path | What it is |
|---|---|
| [AESTHETICS_PLAN.md](AESTHETICS_PLAN.md) | Ten engine-side interventions on the existing art, the art that needs image generation, a style-matching protocol, and a suggested order |
| [TRANSPARENCY_AUDIT.md](TRANSPARENCY_AUDIT.md) | Castle sprite errors (neighbouring-frame bleed, cut-off crops, see-through fabric, objects hidden behind opaque art), a cut-off analysis of every image touching its edge, evidence and fixes |
| `media/before/` | Full-frame captures of every castle room, the Sky Lagoon and the Grand Puff backdrop |
| `media/prototypes/` | Before/after clips of two prototypes (living pool water, warm bathroom light) |
| `media/evidence/`, `media/sheets/` | Evidence for each confirmed audit finding; every image is shown in the documents |
| `data/` | Capture inventories (every drawn object and its sampled region), analyzer findings, the sheet sweep and the visibility pass |
| `tools/` | The capture, analysis, sheet-sweep and visibility scripts, plus the prototype scripts and their masks, so every result can be rerun |
| [MANIFEST.json](MANIFEST.json) | SHA-256 of every file in this folder |

Nothing in this folder is loaded by the game; a `.gdignore` keeps Godot from importing
it.

## Owner-approved work queue

The owner approved these on 2026-09-24. Claude prepared the specifications but did not
build them: the owner clarified that Claude recommends and Codex implements.

### 1. Baby Eagle: backpack-free cutout everywhere

Replace every runtime appearance of Baby Eagle:
- the castle companion card beside Roshan;
- the adoption picker;
- the care sheet;
- the pinned-rescue display;
- the follower.

Use the approved backpack-free cutout, and remove the eagle's colour-painting step,
because protected art cannot be recoloured.

- **Source:** `books/chapter_one/landscape/art/stress_revision/eagle_original_isolated.png`
  on `origin/codex/mermaid-roshan-picture-book` (944×1666 RGBA, SHA-256 starts
  `166461427017b262`). Cite its provenance record on that branch.
- **Runtime copy:**
  - at most 1024 px on the long side, Lanczos, alpha kept, no recolour;
  - stored outside `assets/book/`, e.g. `assets/characters/companions/`;
  - built by a small tool with a `--check` mode, modelled on
    `tools/build_rainbow_friend_cutout.py`;
  - with an `ASSET_LICENSES.md` row noting a private derivative of protected book art,
    owner-approved on 2026-09-24.
- **Code:**
  - the eagle roster entry in `scripts/companion.gd` gets the sprite and becomes
    non-paintable;
  - the picker skips the part and colour steps for non-paintable friends, so the gold
    frame goes straight to the heart;
  - the castle card (`scripts/arena/castle_rooms_25d.gd`) and the rescue display use the
    same art.
- **Gates:** editing `castle_rooms_25d.gd` requires rebuilding the v3 castle
  manifest (`python tools/build_castle_interaction_v3_manifest.py`). Update
  `probe_stuffie` (card path, palette steps) and `probe_audit` (it expects 3 part buttons
  and 8 swatches on the eagle). Keep negative coverage for paintable stuffies.
- **Never** modify `assets/book/baby_eagle.png`, and never use the rejected redraws
  (SHA-256 prefixes `90c54412aa59`, `dab2d2cd9c89`).
- This also resolves audit finding T2.

### 2. The library's magic book opens "repeat the days"

Owner direction: *"The main book in the middle of the library should open a menu to
repeat the days."*

- **Entry:** the Royal Library's `magic_book` fixture (`library:magic_book` in
  `castle_rooms_25d.gd`) opens a picture-first menu:
  - big cards (at least 110 px);
  - a spoken prompt through `_say`;
  - a close control;
  - no reading dependency.
- **Day One replay:**
  - Add save keys with defaults:
    - `day_one_completed_once`: only goes false→true, backfilled when Grand Puff is
      defeated, cleared only by New Game;
    - `day_one_replay_active`;
    - `day_one_replay_clips_seen`.
  - Reset the director's 26 Day One keys, the rescue flags (set false, not deleted),
    `dustboss_pending_*` and the replay clip list.
  - Reload through New Game's route (`DAY_ONE_AFTER_RESET_META`) without wiping the
    save.
- **Keep:**
  - companion and care;
  - pearls and medals;
  - attack colour;
  - castle logo, stickers, crafts and critters;
  - all `chapter2_*`, opera and comfy progress;
  - the permanent story-clip history.
- **Hazards:**
  - `chapter2_active` is recalculated from "Grand Puff defeated", so it must read
    "defeated or completed once", and Chapter 2 plot items must hide while Day One is
    active.
  - The rainbow bunny hides until Grand Puff is beaten again.
  - The companion eagle card hides in the playroom until the eagle is rescued again.
  - Story clips replay once per replay, using the replay list.
- **Way back:** Day One mode routes every exit back to the Day One room, and the library
  is closed during Day One. Add a picture-first "back to today" button, for example in
  the pause menu during a replay only, that restores the finished Day One state.
- **Day Two:** add a card only if the post-boss Day Two/Chapter 2 flow has a clean
  replayable start; otherwise report what it would need.
- **Tests:** a new trusted `probe_day_one_replay.gd` covering the full loop, added to
  both `scripts/ci.sh` and `.github/workflows/probes.yml` (a high-risk file, so append
  only). Also update the director, story-clip, start-menu, load, passive and
  save-recovery probes.

### 3. The four-floor Opera House

Owner direction (2026-09-24): put the four-floor, 16-door venue into the game and retire
rule `DL-INT-12`.

- **Source:** `origin/rescue/opera-four-floors-20260906-worktree` at `d664da18` (parent
  `aad0d450`). This is a verbatim rescue of work that was never committed:
  - 88 files added and 19 modified;
  - the rewritten `scripts/opera_house_venue_2d.gd`, `opera_venue_navigation.gd`,
    `opera_venue_foreground.gd`;
  - the `assets/flats/castle/opera_house_four_floors/` art;
  - the jazz foyer ambience and music rebuild;
  - probe updates.
- **Port onto current `dev`:**
  - Take the files unchanged since `aad0d450` as they are.
  - Three-way merge `scripts/main.gd` (the non-Chapter-2 opera branch),
    `export_presets.cfg` and `scripts/probe_opera_2d.gd`. Add
    `assets/flats/castle/opera_house_four_floors/physical/parts.json` to every export
    preset's include list, or Android breaks.
  - Leave out `.import` churn and the snapshot's unrelated master-audit text.
- **Governance:**
  - amend `DL-INT-12` with the owner decision;
  - update the master-audit decision and the superseded-ideas table;
  - add document-ledger rows;
  - write an impact record.
- **Open gate:** the venue background is 1672×941, below the 2048-px native-height rule.
  Record an owner-approved exception rather than upscaling or redrawing.
- **Music:** include the jazz foyer if `tools/build_area_music.py --check` and the audio
  ledger pass reproducibly; otherwise land the venue first and report the blocker.
- **Keep:** the Opera Hall "resting" during Day One, and the Chapter 2 opera flows.

### Audit errors to fix

[TRANSPARENCY_AUDIT.md](TRANSPARENCY_AUDIT.md) lists 15 sprite errors, one item to
confirm (T14) and one interface overlap (O1). The four P1 errors show in normal play:

| ID | Error | Fix |
|---|---|---|
| T1 | Pieces of neighbouring Rumi poses float beside her in the pool | Re-pack her sheet with gutters; never regenerate Rumi |
| T2 | Baby Eagle's book crop is cut off at the left edge | Resolved by work item 1 |
| T15 | The Movie Lounge screen is opaque and hides the family home movie | Clear the screen's alpha, or draw the picture above the frame |
| T16 | The Day One rescue star over Baby Eagle draws behind the stuffie nook | Give it the effects z-index; create it only while the rescue is pending |

These fixes move, clear or reorder existing pixels; none needs new art. Anything
that changes how the game looks still goes to the owner in context.

### Not approved

- Promoting `dev` to the phone's stable build. The owner said "not yet".
- The Rumi single reveal and voice, and the Grand Puff fight direction (`OD-1`), are
  still waiting on owner answers.

## How to rerun the audit

1. Copy `tools/inventory.gd` into scratch space and set its `OUT` path.
2. Run each scenario (`free`, `d1_bath`, `d1_pool`, `d1_playroom`, `d1_craft`) in a real
   window with isolated app data:

   ```bash
   APPDATA=<temp> LOCALAPPDATA=<temp> godot --windowed --resolution 1280x720 -s inventory.gd -- free
   ```

3. Run `python analyze.py`, then `python sweep_sheets.py` (set `REPO` to your checkout),
   then `python occlusion.py` and `python occlusion_evidence.py`.
4. Review every flag by eye before reporting it. The heuristics find candidates; they do
   not decide.

The prototype scripts `tools/proto_pool.gd` and `tools/proto_bath.gd` run the same way.
They inject effects into the running game and record frames; they change nothing in the
project.

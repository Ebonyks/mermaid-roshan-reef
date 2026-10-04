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

## Questions for the owner

1. **Who takes GS0?** Default: Codex repairs `MA-PLAY-005` first, before any other work; Claude re-scores afterwards.
2. **Dolls, Seek, Melody and the fish slide** are strong Canvas games with no way in since the reef was retired. Should each get a castle-room home, or be retired? Default: give Dolls and Seek a home first.
3. **GS3 workflow lines.** May the two gold-star lines be added to the protected Probe Suite workflow? Default: yes, exactly the two lines above.
4. **Opera Hall elevator.** It opens the "Job playtesting / DEV MODE" menu to any child who taps it. Should it stay until release, or be gated now? Default: keep it for your testing and gate it before the next release.

## Delivery

This packet is published on GitHub with a manifest and an anonymous fetch receipt. The links and hashes are given in the session report and in the [impact record](../../../design/audit_impacts/gold-star-pool-five-star-20261003.json).

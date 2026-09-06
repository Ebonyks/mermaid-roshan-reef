# C14 — proposed playback seam, not implemented

This packet changes no runtime scripts, save keys, game art or movie playback.

## Evidence

`scripts/arena/day_one_castle_dressing.gd:273–280` returns for Main Hall after the exterior edge wash. Other-room tint/cracks are not a localized Main Hall litter/web system. `scripts/arena/castle_rooms_25d.gd:198–227` contains living proximity-only dust-bunny dressing, not this cleanup event.

`scripts/main.gd` clears Day One dressing at boss completion via `_day_one_clear_castle_dressing` around 7884–7895 / 8320–8321 in the inspected worktree. The teardown also affects draft-movie cancellation. Gameplay therefore currently exposes clean hall art after completion. C14 is an authored coda, not a recording of a five-person cleanup minigame.

## Preferred later implementation

Keep the game architecture and correct the animation to it.

1. Complete C13's friendship reveal and preserve boss-complete progress. Queue C14 only after the rainbow friend visibly joins.
2. Play this editorial coda before returning camera/input to the clean Main Hall. Never show clean gameplay, then re-dirty the hall to play a movie.
3. Add separate pending/seen cinematic state with defaults if needed. Completion or skipping never erases/replays the boss victory or forces the child to clean completed rooms again.
4. Save/relaunch during the coda must safely resume a supported checkpoint or return to clean gameplay without stranded input or duplicate rewards. Choose that behavior explicitly during implementation.
5. Delay Chapter 2/Opera prompts and competing movie/voice queues until exit. Verify dressing teardown cannot accidentally cancel the queued coda.
6. Restore clean Main Hall camera, touch UI and input exactly once on completion, safe skip, playback error or unsupported media; persist the consumed cinematic state.

Re-read the live code before selecting hooks: other agents may change it. Proposed pending/seen names are not claims of existing APIs. No new mandatory objective is introduced.

## Later acceptance tests

- New game: C13 reveal → C14 → clean hall, no premature rainbow reveal.
- Existing completed save: no lost progress, boss repeat or dirty-state reset.
- Skip at every shot boundary and mid-S05: one correct camera/input/UI restoration.
- Reload/media failure: completion retained, no duplicated rewards or blocked next chapter.
- Target tablet, Mobile/Speedy: decode performance, framing, sound and gameplay seam.
- Human first-frame and film review; final cinematic evidence remains separate from rough-draft authorization.

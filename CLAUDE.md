# CLAUDE.md — Mermaid Roshan: Reef of Light

## What this is
A Godot 4.4 game for one specific 4-year-old, playable on a 3–4-year-old
Android phone by touch. Every decision is weighed against: non-reader,
one finger, short sessions, zero tolerance for lost progress or fail states.
The book art and recorded family voices are irreplaceable — never modify,
recompress destructively, or substitute anything in assets/book/,
assets/audio/voices/, or assets/characters/friends/ without being asked.

## Layout
- scenes/main.tscn → scripts/main.gd (~8.9k lines as of 2026-07-18; still
  the state owner — see Refactor rules. Target <2.5k; remaining bulk is the
  intro, HUD, craft studio, wardrobe, galaxy/kart glue, arena builders, and
  several half-finished extractions whose builder bodies still live here)
- Phase 7 satellites (RefCounted, receive `main` by reference, own logic
  only — ALL state stays on main):
  scripts/save_state.gd, scripts/audio_director.gd,
  scripts/arena/castle_hall.gd, scripts/arena/sky_lagoon.gd,
  scripts/arena/courtyard_train.gd,
  scripts/games/{fetch,dolls,seek,melody,slide_race,treasure,shop,fairy,
  picture_games,side_scroll,brawl}.gd (side_scroll = the shared 2.5D stage
  engine, brawl = the co-op toy-castle brawler on it — see
  MINIGAME_ENGINES.md)
- scripts/player.gd (swim controller), scripts/touch_ui.gd (virtual stick)
- scripts/probe*.gd — headless bots. probe_audit.gd is the source of truth;
  probe_passive.gd is the zero-input negative test (Phase 6).
- assets/ — aquatic GLBs, terrain PBR (ambientCG), book art, voices, music
- disabled_addons/tessarakkt.oceanfft — DISABLED (dead code removed Phase 0)

## Build & test (headless, no display needed)
GODOT=./Godot_v4.4.1-stable_linux.x86_64   # or `godot` on PATH
1. Import (required after any asset change):
   $GODOT --headless --import .
   ⚠ KNOWN DEADLOCK: NPOT textures with compress/mode=2 hang the headless
   importer at 0% CPU. If import hangs >3 min, find the offender in the
   last "Importing file:" verbose line and fix its size/import mode.
2. Full validation (must print all-OK before any commit) — one command:
   GODOT=$GODOT scripts/ci.sh        # import + all trusted probes,
                                     # exits nonzero on any FAIL line
   Or probe-by-probe:
   $GODOT --headless -s scripts/probe_audit.gd     # full-game bot
   $GODOT --headless -s scripts/probe_passive.gd   # zero-input: nothing may be won
   $GODOT --headless -s scripts/probe_load.gd      # save restore
   $GODOT --headless -s scripts/probe_mg2d.gd      # 5 picture games
   $GODOT --headless -s scripts/probe_l2.gd        # sky lagoon
   $GODOT --headless -s scripts/probe_train.gd     # courtyard train: no-clip lap, ride, hide
3. Never trust probe_games.gd / probe_trial.gd / probe_race.gd until
   Phase 1 replaces them — they reference removed APIs. (Deleted Phase 0.)

NOTE (this environment): no Godot binary is available inside the remote
session container and GitHub release downloads are proxy-blocked, so the
probe suite runs in CI instead — .github/workflows/probes.yml executes
import + all trusted probes on every push to the graphics fork and fails
on any FAIL line. Treat a red probes run exactly like a local red probe.

## Getting the game onto the phone
Every push to `master` auto-builds the debug APK
(.github/workflows/android.yml) and refreshes the stable download URL
https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/android-test/roshan-reef.apk
— bookmark that on the phone; tapping it always grabs the newest build.
From a computer, `./pull-apk.sh` downloads it and, if a phone is on adb,
installs it in place (save data kept).

## Hard rules
- Renderer: "mobile" on EVERY platform (owner decision 2026-07-11:
  desktop and phone must look identical — mobile is the dominant
  interface; supersedes the 2026-07-09 forward_plus split). Base
  1280×720 canvas_items/expand. Anything new must run under the Mobile
  renderer; Forward+-only effects (the cel post grade) are dormant
  behind a rendering-method guard.
- No new OmniLights beyond current counts without a Speedy-tier cull path.
- All new textures: ≤1024px longest side OR power-of-two; VRAM compress ok
  only if POT. New audio: OGG, music ≥64kbps, loop-tagged.
- Every new asset gets a line in ASSET_LICENSES.md (source, license, URL,
  modifications) in the same commit that adds it.
- No fail states, no reading-dependent objectives: any new objective must
  also fire a voice line via _say() and a visual pointer.
- Save compatibility: never remove keys from reef_save.json; add with defaults.
- GDScript: tabs, typed vars where present, match surrounding style.

## Git workflow
- Owner rule (2026-07-13): when a task is COMPLETE (probes green on CI),
  merge the work branch into `master` and push it — master is the branch
  the owner pulls and plays, so finished work parked only on a feature
  branch is invisible to him. Develop on the session's designated work
  branch as usual, and never merge unprobed or red work into master.

## Refactor rules for main.gd
Extract, don't rewrite. Moves must be mechanical: one arena builder or one
minigame tick per commit, preserving exact behavior, gated by the probe
suite before/after. Shared state stays on main; extracted files receive
`main` by reference. If a probe fails after an extraction, revert — do not
patch the probe to match new behavior unless the behavior change was the
explicit goal of the task.

## Art direction (graphics fork)
Static Mermaid Roshan storybook characters in a cel-shaded, Wind
Waker-inspired diorama world. Characters are illustrated cutouts —
unshaded, pre-drawn outlines, idle bob, contact shadows, sparkle/bubble
overlays; never re-lit, never redesigned. The world is a pastel toy
playset: rounded geometry, toon materials, navy/purple outlines,
aqua/lavender shadows, graphic water, oversized child-readable props.
CC0 sources only for the world (Tiny Treats, KayKit, Quaternius, Kenney,
curated OpenGameArt); every import is restyled through the _toonify
pastel pipeline. Wind Waker is a rendering reference only — no Zelda
assets, symbols, UI, music, or character designs.

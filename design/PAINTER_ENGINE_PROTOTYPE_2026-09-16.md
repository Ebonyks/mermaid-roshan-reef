# Painter engine prototype — 2026-09-16

Status: `PROPOSED / CANDIDATE`. One owner-commissioned standalone game prototype,
not a new chapter or an accepted replacement for the current Painter career.
[Impact record](audit_impacts/painter-engine-prototype-20260916.json).

## Selection and import

Painter has the strongest audited opportunity for bounded code reuse: a mature
Godot drawing subsystem can replace the current reveal-grid limitation with
guided, closed-region colouring and exact picture persistence. Hurry Curry's recipes and Librerama's touch activities
remain useful later candidates; no cooking engine, second activity, chapter,
unlock route, or donor art is included here.

The imported component is Pixelorama's scanline flood-fill implementation,
MIT, pinned to `da7b68f97806c461abde615d1d847af91921c37b`.
Its [original source](https://github.com/Orama-Interactive/Pixelorama/blob/da7b68f97806c461abde615d1d847af91921c37b/src/Classes/FloodFillObject.gd),
attribution to Shawn Hargreaves/Allegro, full license, preserved source sample,
and modifications are recorded under `scripts/painter/vendor/`. The adapter
removes editor Project/selection dependencies and uses exact RGBA regions.
This is a selective subsystem import; the Pixelorama editor is not embedded.
Both export presets explicitly carry its full MIT notice and exclude the
prototype test helpers.
Roshan-specific drawing, history, persistence and UI are new prototype code.

## Playable scope

Run `scenes/painter_prototype.tscn` with exactly Godot 4.7.2-stable, using
the project's Mobile renderer. From the project directory:

```text
godot --path . --windowed --resolution 1280x720 scenes/painter_prototype.tscn
```

On the configured Windows workstation, `powershell -File tools/run_painter_prototype.ps1` checks the installed official engine and opens the scene.

The owner's review corrected the initial free-paint emphasis: a minigame must
have blanks and a coloured layout to follow. The default is now one guided
sunrise postcard with five closed regions, a coloured reference, five palette
choices and a cue that moves between the matching colour and the unresolved
region. Contact immediately shows a hold-progress ring. Hold the correct region
for 0.22 seconds to request its fill. The exact
existing voice says, “Hold to fill the glowing shape!” Wrong colours, a short
tap, passive waiting and repeated completed regions earn no progress. Five
picture dots reflect actual completed regions; the finished picture remains
visible and survives leave/re-entry. Undo/redo remain recoverable.

The page is engine-native region data, not a new generated background or a
replacement Roshan image. Its shell region follows the existing shell motif's
alpha silhouette. The reference and blanks derive from identical region data;
completion must match the reference pixel-for-pixel. This single page tests the
engine; it does not add a sequence of levels or another game section.

Free paint remains available only with launcher `-FreePaint` (or Godot `-- --free-paint`), for future Craft Room
integration. It shares the brush/fill/history/persistence engine and offers a
shell stamp and six colours. Its tools are absent from the default minigame.
There is no claim of a later story payoff for free painting and it has no career
reward. Neither variant changes existing birthday or career consumers.

Both variants use shared StorybookUI paper/violet controls with 110px palette
and navigation targets. There is one neutral exit and a picture resume control
following focus loss. No timer pressure, lives, destructive reset or required
reading is introduced. Roshan hosts the child's direct creative surface; this
prototype does not claim to close the embodied-job finding. Future in-world
integration still needs the appropriate navigation and save-service contracts.

## Existing art remains unchanged

The scene reuses the Painter panorama, the accepted painter atlas's held
brush/celebration poses, the shell motif and two existing spoken invitations.
The impact record stores SHA-256 for all five. No PNG, audio source, import setting, character
design or source master is changed. No new generated art or donor graphics are
imported. The shell is copied into scratch memory when stamped; the original
texture remains immutable. Holding an authored pose is not a claim of newly
accepted character animation.

## Engine boundaries and budget

`PainterDocument` owns a 512×256 RGBA8 scratch canvas (0.5 MiB). Sixteen undo
snapshots cost at most 8 MiB of pixel data; redo transfers those snapshots
rather than duplicating the whole history. A live stroke and a fill need bounded
additional scratch buffers. The imported scanline fill runs on a worker thread;
cancelled results are discarded and teardown joins the worker. GPU texture
updates occur on changed input/results, not each idle frame. Device latency,
overdraw and whole-process memory still require measurement.

`PainterStudio` owns scene layout, single-pointer lifetime, controls, voice and
the invitation. It uses the same stage transform for input and drawing. A second
finger cannot take a held route, dragging a control cannot become painting,
focus loss drops queued fills, and release cannot initiate another action.
Already painted pixels survive cancellation. The resume overlay requires a
fresh intentional tap. Source art, background and host do not become paintable.

The guided page saves `user://painter_sunrise_v1.png`; optional free paint uses
`user://painter_prototype.png`. Each uses a
validated temporary PNG and a last-good `.bak`. It never opens `reef_save.json`.
It saves on stroke release, undo/redo, focus/exit and periodically during a long
stroke. Undo history is session-local; the actual painting persists. Future page/region
changes must use a new versioned save name and retain earlier artwork. A save
failure leaves the in-memory picture intact and displays an adult diagnostic.
Integration into the full game would move the artifact reference into the
existing append-only save service rather than create a second career-progress
authority.

## Verification and acceptance

Run the focused engine/input probe with:

```text
godot --headless --path . -s scripts/probe_painter.gd
```

It checks enclosed fills and exact undo/redo, compares the imported fill with an
independent BFS over 32 deterministic random maps, tests history bounds and
cancelled fills, saves/reloads and recovers a damaged primary, then drives actual
ScreenTouch/ScreenDrag through the studio. Passive play, second-finger ownership,
pause/stale events, picture resume, controls, stamping and neutral exit are
covered. Test PNG paths are isolated from the child's painting.

The guided leg additionally checks wrong-colour and short-hold negatives, pause
cancellation, each intentional region, exact final reference equality, partial
save and completed re-entry.

The same helper runs at the start of `probe_mg2d`, already in both trusted
local/remote rosters; no workflow changes are needed. For diagnostic desktop
captures add `-- --capture` to the focused probe and use a windowed Mobile run
at each desired aspect. Capture pixels come from the live viewport. These are
review evidence, not the stricter master-audit fresh-runtime acceptance claim.

Current test outcomes and exact evidence are recorded in the impact JSON.
Target-device performance, observed non-reader comprehension, audio listening,
and owner UI/art acceptance remain open. No existing MA finding is closed and
the master audit remains UNSATISFIED.

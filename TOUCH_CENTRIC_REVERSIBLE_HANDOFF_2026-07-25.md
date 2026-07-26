# Mermaid Roshan — Reversible Touch-Centric Handoff

Date: 2026-07-25
Branch: `codex/touch-centric-reversible`
Base: `origin/dev` at `d5ef00957fa5f6d37870552baebe437381008e79`

## Outcome

This fork keeps the 3D world and adds a touch-first interaction layer without
deleting the shipped controller. The pause menu contains a saved
**Hybrid Touch / Classic Touch** tile:

- **Hybrid Touch (default):** fixed lower-left analog movement, a real
  lower-right pictogram-plus-word action target, tap-to-select/tap-to-approach,
  proximity glow, explicit second tap/action to enter activities, and
  manual-stick override.
- **Classic Touch (rollback):** the prior drag-anywhere floating stick,
  tap-to-action, second-finger hold, and second-finger camera implementation.

The save key is additive (`touch_mode`) and defaults to `hybrid`. Selecting
Classic is the normal child-facing rollback. Reverting this branch is the
code-level rollback. No protected book, voice, or friend art was modified.

## Interaction language

Every registered world interaction follows:

1. **Discover:** within a generous range, an aqua ground ring appears.
2. **Acknowledge:** the first target tap produces a gold ring and sparkle.
3. **Approach:** the existing player controller receives steering intention;
   no teleport or second physics controller is used.
4. **Ready:** the action bubble changes to the object's verb.
5. **Act:** a second target tap or the pink action button activates.
6. **Recover:** moving the left stick cancels assisted movement immediately.

Open-space taps request assisted travel. Two stalled steering recoveries try
opposite side steps; persistent blockage cancels safely and asks for a small
manual wiggle. Proximity can still discover friends and collect forgiving
collectibles, but it cannot start a game or change worlds in Hybrid.

Action presses are frame-bounded edges: pressing and releasing before choosing
an object cannot activate the next object later. Full-screen overlays suspend
both world controls and clear every owned finger. Synchronous world rebuilds
clear focus/assisted travel and make the fade cover claim taps until reveal.

## Zone coverage

### Reef and ocean kingdoms

- Five friend activities
- Manta Pearl Shop
- Shipwreck Secret Cave
- Penguin Slide
- Toy Castle brawler
- Ocean Race
- Rainbow Portal / castle hub
- Ocean-kingdom return gate

### Sky Lagoon and long northern route

- Caribbean/Norway kingdom gates
- Alpine magic-cave route and northern return
- Pearl Opera entrance
- Both Rainbow Race directions
- Butterfly World and Ember Fortress gates
- Dream Stars as assisted-travel landmarks
- Castle front and secret back entries
- Optional wall-picture activities

### Pearl Castle, lower and upper floors

- Front exit, bed, wardrobe, craft easel
- Golden stand / basement stair reveal
- Royal loo encounter, dungeon, opera
- Explicit Music Star, music bells, and touch-and-delight props
- Daddy's treasure chest
- Crown Star

The glow is emissive mesh geometry. It adds no OmniLights and is pooled as one
discovery ring plus one focus ring, preserving the Speedy-tier light and
transparent-overdraw budget.

## Code map

- `scripts/touch_ui.gd` — reversible router and the preserved Classic path
- `scripts/tap_move_director.gd` — steering intention, bounds, arrival/stall
- `scripts/interaction_director.gd` — screen selection and interaction states
- `scripts/main.gd` — all mutable state, registry, dispatch, feature toggle
- `scripts/player.gd` — assisted intention enters the existing movement stack
- `scripts/save_state.gd` — additive `touch_mode` normalization/persistence
- `scripts/pause_menu.gd` — accessible Hybrid/Classic toggle
- `scripts/arena/{sky_lagoon,castle_hall,northern_kingdom}.gd` — Hybrid-only
  suppression of automatic activity/portal entry; Classic behavior retained

## Automated adversarial cycle

The trusted gate now includes:

- `probe_touch_router.gd` — touch ownership, simultaneous stick/world input,
  real pictorial action target, action-edge expiry, overlay-held-finger
  clearing, lifecycle clearing, and Classic rollback
- `probe_interaction.gd` — advertise/select/approach/act behavior and zone
  registry completeness, explicit Music Star start, picture-game control
  suspension (including nested overlays), same-frame stale action rejection,
  playback bell suppression, and rapid transition taps
- `probe_touch_adversary.gd` — 25 fresh-instance adversarial touch scenarios;
  every run prints its own feedback and covers routed first taps, randomized
  child-finger jitter, screen-space misses/control occlusion, real-time
  physical player travel in all headings, blocked-route recovery, manual
  override, the reef, courtyard, castle floors, northern return, and both
  toggle directions
- updated `probe_passive.gd` — explicitly rejects Hybrid proximity auto-start
- updated full-game/ranking bots — perform the new explicit activation verb
- `probe_touch_look.gd` — now explicitly verifies the Classic rollback path
- `probe_save_recovery.gd` — serializes, reloads, backs up, repairs, and
  defaults the additive `touch_mode` preference without rolling back progress

The adversarial gate is not complete until it prints:

`TOUCH_ADVERSARY|ALL 25 SCENARIO RUNS CLEAR`

Any run printing `FAIL`, any parser/analyzer error, or any trusted probe failure
blocks acceptance and requires another code/audit cycle.

These are deliberately called *scenario runs*, not complete playthroughs. They
instantiate the full game 25 times and physically exercise navigation and
route transitions, but they do not impersonate 25 independent multi-hour child
sessions. The mandatory human/device pass below owns that claim.

### Iteration record (2026-07-25)

1. The original automated cycle reached 25/25 after fixing transition routing,
   Opera return placement, and proximity bounce.
2. Independent adversarial code review rejected that result for stale action
   edges, proximity-started bells, swallowed overlay releases, action-button
   overlay occlusion, non-failing probes, and stale transition taps.
3. The strengthened 25-run cycle rejected undersized castle-prop approach
   radii; every prop was raised to the child-safe minimum.
4. The next cycles rejected slow reverse-direction tap movement. The
   assisted-only turn curve was made more responsive; Classic and analog
   steering were not changed.
5. The strengthened cycle reached 25/25, but a second independent review
   rejected same-frame pre-focus actions, second-finger activation dropping a
   held stick, direct transitions keeping old targets, nested overlays
   re-enabling controls, and bell targets that did nothing during playback.
6. Input edges are now focus-bound, non-transition actions preserve the stick,
   all world rebuild paths clear/repopulate targets, overlay blocks are
   reason-keyed, and bells disappear during authored playback. Dedicated
   regressions passed and the strengthened cycle again reached 25/25.
7. A third review rejected modal sleep/hug ownership and delayed bell-state
   registry refresh. Both cutscenes now own and release a named input block,
   cannot restart while active, and every bell play/echo/idle transition
   updates targets in the same frame. Their exact regressions pass, and a
   fresh isolated strengthened cycle again reports 25/25 clear.
8. Final independent adversarial re-review found no remaining high- or
   medium-severity touch defect in the diff. Human tablet/child sign-off
   remains outstanding by design.

Local desktop validation uses the owner's installed
`Godot_v4.7-dev2_win64_console.exe`. CI remains the compatibility authority for
the project's declared Godot 4.4 runtime.

## Mandatory human stress test

Automation cannot judge whether the diorama composition *looks good* on the
Lenovo Tab M11 or whether a four-year-old understands a glow. Do not promote
this branch solely from green probes. Test a fresh install and an upgraded save
in both day and night:

1. Make 30 rapid alternating left-stick and world taps. Confirm no ownership
   swap, surprise jump, or unwanted activity.
2. Hold movement while pressing the pink action button with a second finger.
3. Tap friends partly hidden by coral, the wreck, the manta, and each portal.
   Confirm the intended target wins and the gold ring is not visually noisy.
4. Walk away during auto-approach, hit walls deliberately, and take over with
   the stick. Confirm cancellation feels instant and never snaps position.
5. Traverse spawn → Sky Lagoon → northern castle → return without reading.
6. Traverse the castle front hall, balcony, upper galleries, Dreaming Floor,
   basement, bedroom, music room, dungeon and exit. Check ring visibility when
   ceilings, stairs, walls, chandeliers, or the upper floor cross the camera.
7. Open and close every 2D overlay/minigame. Confirm no hidden world tap leaks
   through and no held action survives resume.
8. Toggle Classic, fully quit, relaunch, and verify it persists. Repeat back to
   Hybrid. Confirm save progress, medals, cosmetics, and pearls are unchanged.
9. Repeat at Speedy quality while watching for ring overdraw, frame pacing,
   camera boom shortening, and excessive sparkle.
10. Let the intended child play unprompted. Record first-tap comprehension,
    accidental activations, missed targets, two-hand use, requests for help,
    and any place she becomes visually lost.

Log human findings by zone and attach screenshots/video before promotion. A
human visual sign-off remains intentionally outstanding until that device test
is performed.

## Rollback

Immediate runtime rollback:

1. Pause.
2. Tap **Hybrid Touch**.
3. The tile changes to **Classic Touch** and saves immediately.

Code rollback:

- Do not merge `codex/touch-centric-reversible`, or revert its merge commit.
- The original input implementation is retained in
  `TouchUI._classic_unhandled_input()`; it is not reconstructed from history.
- Existing save files remain compatible because old keys were not removed and
  `touch_mode` has a default.

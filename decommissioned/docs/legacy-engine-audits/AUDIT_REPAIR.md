# Mermaid Roshan: Reef of Light — Audit / Repair

Date: 2026-07-15

Validated branch: `codex/game-polish`

Validated commit: `f3c0a46`
Authoritative CI: [Probe suite run 29462126174](https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/29462126174)

## Purpose

This record closes the repair phase of the full-game audit. The work focused on
player agency, no-fail progression, touch reliability, save safety, replay and
return paths, runtime correctness, and release gates. It did not rewrite the
book plot or replace protected book art, family voices, or friend art.

Roshan chasing the snowman and eating his carrot nose remains the canonical end
of the snowman picture game. The complete sequence—roll three snowballs, chase
the snowman, eat the carrot—is now driven through the real touch path by the
trusted picture-game probe.

## Confirmed repair findings

1. Several activities could award progress without a meaningful player action.
   Passive motion or proximity could complete slide, kart, fairy, shop, and
   other activity paths.
2. Some activities had no neutral exit. A child could be trapped in an activity
   or forced through a result to return to free play.
3. The old save path was vulnerable to interruption during overwrite and did
   not preserve unknown fields or future-schema data safely.
4. Galaxy, Sky Lagoon, custom fish, custom friends, and some reward milestones
   had incomplete round-trip persistence.
5. Touch state could remain held through focus, pause, and back-navigation
   transitions.
6. The snowball-roll instruction advertised circular touch-stick input, but the
   implementation only read a physical gamepad or mouse gesture. This made the
   canonical snowman sequence impossible through the primary Android control.
7. Multiple 3D nodes were animated through nonexistent `modulate` properties,
   causing runtime errors during crown, combat-popcorn, and dungeon-gate beats.
8. Historical terrain textures no longer present in the repository were still
   loaded at runtime.
9. Several trusted probes had drifted from production state: obsolete toy
   counts, synthetic castle state, frame-cadence-dependent travel, and bots that
   did not perform newly required deliberate actions.
10. Android publishing could rotate the debug signing identity or publish a
    commit that had not passed the exact probe workflow.

## Repairs completed

### Agency and no-fail behavior

- Progress and rewards now require a real player verb where the activity claims
  to test one. Passive runs remain valid negative tests and cannot fabricate
  trophies, stickers, pearls, or finale progress.
- Slide rewards require deliberate steering; kart payout requires real steering,
  braking, turbo, or rocket-start participation; fairy and shop rewards require
  fresh deliberate input.
- Penguin Slide restarts gently when no steering occurred instead of converting
  passive travel into success or loss.
- A neutral **Leave Activity** path is available from pause for friend games,
  wardrobe, craft, Sky Lagoon, Galaxy, kart, combat, and dungeon. Leaving is not
  recorded as a win or failure.
- The ten-room dungeon uses four combat rooms and six visual puzzle rooms, keeps
  checkpoints, and distinguishes neutral exit, earned exit, and final completion.

### Touch and interaction reliability

- Touch state clears on focus loss, pause, back-navigation, and save-related
  transitions.
- Snowball rolling now accepts circular movement from the Android virtual stick.
- The picture-game bot performs the actual roll, chase, and carrot-eating verbs.
- The carrot is removed from active state immediately after the bite, preventing
  repeated access to a queued-free UI node during the victory close.
- Explicit gestures reset the idle clock, so a completed `look` animation cannot
  instantly auto-start another idle `look` and appear stuck.

### Persistence and progression

- Saves are versioned and transactional, with temporary and backup files,
  validation, recovery, additive defaults, unknown-field preservation, and
  read-only handling for future schemas.
- Permanent portal progress uses the five-friend milestone plus the recorded
  lifetime pearl peak rather than volatile current inventory.
- Galaxy completion, partial butterfly checkpoints, return origin, Sky Lagoon
  stars, custom fish colors, and custom friend colors survive round trips.
- Save-recovery and load probes use isolated user-data directories so one test
  cannot hide another test's failure.

### Runtime and presentation correctness

- Crown and landmark replay state supports the new layered 3D stars.
- Crown celebration, dungeon veil, and combat popcorn animate valid 3D
  properties/materials and no longer emit property errors.
- Missing `Ground054` and `Rock061` dependencies were replaced with the existing
  painted `up_sand` and `up_cliff` material families.
- Castle front-door, level re-entry, combat return, picture-game cleanup, and
  gesture probes now exercise valid production states rather than synthetic or
  frame-rate-dependent approximations.

### Build and release safety

- Every push and pull request runs parser and inference lint gates, a guarded
  Linux import, Godot's analyzer against every script, and 19 trusted probes.
- Every probe receives isolated save/config data; missing trusted probes fail.
- Android publishing is permitted only after a successful push-triggered probe
  run for the exact commit.
- Publishing requires a persistent signing identity and refuses to rotate it
  silently. The APK and SHA-256 file use a stable release URL.

## Validation result

The authoritative Linux workflow passed:

- GDScript parser and Variant-inference lint
- deadlock-guarded asset import
- Godot analyzer for every `.gd` file
- full-game audit and finale
- zero-input negative progression audit
- load and transactional save recovery
- Galaxy, picture games, dance, Sky Lagoon and re-entry
- crown and castle exit
- train, gestures, skins, touch-look, and voice
- kart feel, combat, and ten-room dungeon

Targeted local evidence also passed:

- all five picture games; snowman completed in 28.8 simulated seconds
- all five friend trophies and finale
- combat completion and return
- crown completion and front-door return
- Sky Lagoon re-entry with stable node/toy counts
- wave, cheer, clap, twirl, look, giggle, and sleep animations

## Deliberately unresolved

- Plot revision is deferred. The snowman/carrot scene is not a defect.
- A full visual capture matrix and sustained performance trace on the actual
  target phone/tablet remain necessary; headless probes cannot certify art,
  frame pacing, audio mix, thermal behavior, or touch ergonomics.
- The stable Android keystore exists locally but has not been transferred to
  GitHub because credential transfer requires explicit owner authorization.
  Therefore this repair branch has not yet been merged to `master` or published
  as the next stable APK.
- New exact family voice lines require owner recordings. Generic recorded voice
  fallbacks and visual pointers remain in use where no exact clip exists.

## Repair verdict

The repair phase achieved its intended outcome: progress is safer, rewards are
earned, every major activity has a neutral return path, the canonical snowman
scene works through the target touch control, saves are recoverable, and the
trusted full-game suite is green. The next phase should improve production
quality and measured presentation rather than add plot or more disconnected
features.

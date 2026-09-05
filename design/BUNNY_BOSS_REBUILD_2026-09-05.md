# Grand Puff: movement and counterattack rebuild

Scope: the owner's September 5 request replaces the previous timing-only fight.
The approved jump, laugh, flinch, angry and implosion atlases and flashing-head
weakness remain. Earlier triple-tap, random roaming-contact and optional twirl
mechanics are superseded for this encounter. No new art is commissioned.

## References and design inference

Official Google Play listings reviewed September 5, 2026:

- [Sonic Dash](https://play.google.com/store/apps/details?id=com.sega.sonicdash)
  combines accessible avoidance controls and boss encounters. Adaptation: evade
  a clearly announced attack, then take a distinct counterattack opportunity.
- [Archero](https://play.google.com/store/apps/details?id=com.habby.archero) and
  [Survivor.io](https://play.google.com/store/apps/details?id=com.dxx.firenow)
  emphasize one-hand combat and movement through escalating encounters.
  Adaptation: positioning creates the challenge without extra action buttons.
- [Guardian Tales](https://play.google.com/store/apps/details?id=com.kakaogames.gdts)
  describes dodging attacks and exploiting weaknesses. Adaptation: preserve
  Grand Puff's gold head tell as the reward for understanding the attack.

These are broad control/encounter references, not claims that any source uses
the exact patterns below. Adult roguelike death, restart, grinding and monetized
progression are unsuitable for this child's game and are not adopted.

## Encounter

| Phase | Spatial challenge | Counter |
| --- | --- | --- |
| Puffy | One landing circle locks where Roshan was when the warning began. | Move clear, then tap the flashing head once. |
| Dizzy | Two landings, each with its own newly locked warning. | Move twice, then counter once. |
| Angry | A landing followed by a broad, separately warned dust lane. | Leave the landing, move out of the lane, then counter once. |

Peach shapes show the exact dangerous footprint; a cyan destination points
toward safety. Gold is reserved for the head weakness. The target stays fixed
after its warning starts. Damage is resolved at the visible impact, never from
unannounced idle contact. No attack requires two simultaneous finger actions.
Tap the arena floor to send Roshan toward that point; tapping the cyan safe
destination snaps to the exact safe target. After movement ends, tap Grand
Puff's generously projected head while its gold marker flashes. The retired
corner `WAIT`/`BONK!` control does not teach or bypass this world action.
Keyboard and controller fallbacks remain available through the host adapter.

Taking a hit costs the current counter opportunity and repeats the current
phase after a short recovery. Completed phases remain earned. Clean movement
therefore beats stationary tap spam, while no health depletion can end play.
Repeated bumps or missed openings lengthen warnings/openings; assistance never
inserts damage or awards a win without input. The live HUD shows completed
encounter rounds consistently. Replay mastery and pearl rewards remain optional
result/return incentives rather than a competing in-battle star display.

Checkpoints include all three earned counters. An interruption during the final
celebration resumes the friendship ending without another attack. The reward and
checkpoint reset are committed together, preventing duplicate pearl grants.

The single counter plays all three existing flinch reactions as an authored
sequence. The standalone animation kit's older three-tap API stays supported
for its independent contract tests, but is not the battle's input requirement.

## Evaluation contract

Blocking behavioral checks cover target immutability; safe escape from edges
at actual movement speed; distinct three-phase patterns; no victory from idle,
stationary tapping, or held input; deliberate movement plus one counter per
phase; slow reactions with assistance; collision at visual impact; interruption
and save checkpoints; unchanged friendship/Day Two/reward completion seams.
Engine validation uses exactly Godot 4.7.2-stable.

The new attack math and warning renderer are Vector2/Canvas code. The shared
OctagonStage and existing sprite presentation remain measured 3D migration
debt; this mechanics change does not claim completion of the game-wide 2D audit.
Automated bots do not establish preschooler comprehension or Lenovo Tab M11
frame rate. Those require a real child/device playtest.

## Shared encounter architecture

The rebuild now provides content-neutral shared classes instead of keeping the
rules inside Grand Puff:

- `EncounterAttack2D` and `EncounterPhase2D` describe ordered attack geometry.
- `EncounterProfile2D` owns phase order and assistance timing. Its shipped
  factories are `grand_puff()` and `pepper(7)`.
- `EncounterPatterns2D` locks target geometry and computes valid safe points.
- `BossEncounter2D` owns the no-death state machine, monotonic completed rounds,
  hit/recovery, avoids, opening misses and counter eligibility.
- `EncounterNavigation2D` maps direct screen taps to 2D play coordinates and
  advances tap-to-go movement.
- `EncounterTelegraph2D` renders the projected danger/safety contract and
  supports a variable `total`, a floor pass behind actors and an overlay pass
  for hand/progress UI; `DustBossTelegraph2D` is a compatibility name.
- `EncounterGestureGuide2D` supplies the shared downward hand and optional
  TAP/HOLD picture chip at a host-projected live target.
- `EncounterContractChecks` exercises both profiles. Pepper is a real seven-
  round consumer in `combat_arena.gd`, including its ICE-shell then FIRE-head
  host interaction, checkpoint, reward and teardown seams.

To add another boss without changing `main.gd`, create an
`EncounterProfile2D` from phases and attacks, construct `BossEncounter2D` in
the owning activity, call `configure(profile, saved_rounds, saved_damage,
saved_misses)`, and bind the activity's existing entry/tick/close callbacks.
At tell start call `begin_attack`; advance the warning with `tick_tell`; call
`begin_strike` when the host starts its authored attack animation; call
`resolve_impact` only on the visible animation contact frame. After
`COUNTER_READY`, start the host's visible weakness animation, call
`open_counter`, and pass a fresh edge, live target hit and actual visual-open
state to `try_counter`. The host alone persists checkpoints, plays character
animation and voice, grants rewards, and clears its checkpoint atomically on
real completion. It also owns world/screen projection, input routing and
teardown. The shared engine must never infer animation contact from a timer,
write save data, or award progress.

For presentation, instantiate `EncounterTelegraph2D`, call
`configure_quality(quality)`, and pass the existing readout plus projected
`points`, `player_point`, optional `safe_point`, `puffs` and `total`. Keep
danger, movement and counter sequential, and keep the visual marker attached
to the live actionable target. A mixed retained stage may call `draw_floor`
behind its actors and `draw_overlay` above them; visibility and discrete
progress changes must request redraw even when the Speedy continuous cap has
not elapsed. Teardown hides and queues owned Canvas layers without detaching a
busy parent manually.

## Measured evaluation

### Background authority audit

The owner's correction identifies the recent dusty room, not the procedural
purple octagon. Two independent agents checked asset history and imagery.
The production match is `assets/flats/castle/boss/dusty_attic_arena_2048.png`
from commit `0243d929f29cb95df2c870db58895c31c87377c5` (August 30), on the
unintegrated `codex/dust-bunny-arena-2d` branch. The exact PNG, original native
source, provenance and license entries are restored; no image was regenerated.
Runtime SHA-256: `a6f4bb59df43e63cedbf9a164526475b91985c85c73cac7e061f830d60ef4122`.
The Canvas background replaces the mesh floor, walls, posts and decorative
primitives. The September 2 cinematic `DUSTY_ATTIC_OCTAGON_ARENA_MASTER.png`
is a separate topology candidate whose sidecar explicitly denies appearance
authority; it is not the runtime background.

### Battle behavior

Godot 4.7.2-stable, fixed 60 FPS simulation, shared live scene/animation clock:

| Input persona | Fight seconds | Bumps | Missed openings | Outcome |
| --- | ---: | ---: | ---: | --- |
| Attentive | 44.50 | 0 | 0 | Three counters, complete |
| Learning | 44.50 | 1 | 0 | Recovers, complete |
| Slow movement | 59.35 | 4 | 0 | Recovers, complete |
| Slow counter response | 61.30 | 0 | 2 | Wider openings, complete |
| Moving and repeatedly tapping | 43.50 | 0 | 0 | Movement still required, complete |

Idle, stationary tap spam, and held-action controls each scored zero rounds in
60 seconds. Movement-only scored zero rounds despite seven avoided attacks and
six expired openings. The integration probe additionally sweeps 16 edge
positions across every phase/step and exercises the live door, checkpoint,
performance retention, head tap, friendship, reward and Day Two seams.

The current shared-engine balance evaluation ran once per required roster at
fixed 60 FPS under exact Godot 4.7.2-stable. Normal and control runs both ended
`ALL OK` with exit code 0. Logs are
`audit/boss_encounter_2026-09-05/balance-normal.log` (SHA-256
`5ef825bb0ce2402620258717153beb9f093303446abfc10ed66588549a5bb89f`)
and `audit/boss_encounter_2026-09-05/balance-controls.log` (SHA-256
`c4e0183bd0c5cb7009a62a61f0e679d87835b6f5bd42551601769508080131cf`).
These tracked simulation logs normalize only CRLF to LF; original capture
hashes remain in the packet manifest. They do not establish device performance
or child acceptance.

```csv
persona,seconds,rounds,damage,avoids,opening_misses,taps,result
attentive,44.50,3,0,5,0,3,OK
learning,44.50,3,1,6,0,3,OK
slow,59.35,3,4,5,0,3,OK
slow_counter,61.30,3,0,7,2,3,OK
moving_masher,43.50,3,0,5,0,145,OK
idle,60.05,0,12,0,0,0,OK
stationary_masher,60.05,0,12,0,0,200,OK
held_action,60.05,0,12,0,0,0,OK
movement_only,60.05,0,0,7,6,0,OK
```

The tracked local packet `audit/boss_encounter_2026-09-05/manifest.json` binds
LF-normalized SHA-256 hashes for 17 runtime/probe sources and 13 unmodified
Mobile viewport PNGs: four selected final Dust states at both 1280×720 and
1560×720 plus five final tutorial states at 1280×720. Independent hash recheck
passes. The final Dust logs finish 23-state runs with `DONE`; tutorial root3
finishes `ALL OK`; their error logs are empty. Agent review confirms the floor
warning behind actors, overlay safety/hand/progress cues above, the corrected
tutorial bunny frame and floor placement, suppressed unrelated action control,
and partner hand above its portrait. This is source-bound local V4 evidence;
the immutable remote commit, Android/device, child and owner acceptance remain
pending.

The scoped graphics and tutorial evidence is recorded in
`audit/BOSS_ENCOUNTER_VISUAL_AUDIT_2026-09-05.md`. The bounded tutorial repair
now uses the approved grotto as a Canvas background, the normal framed bunny,
one shared downward gesture guide with approved TAP/HOLD chips, suppressed
unrelated action chrome and a compact restoring caption. Roshan, imp, camera,
HitEngine staging and floor projection remain spatial transition debt, and the
lesson captions still lack exact contextual voice-ledger coverage. Current
diagnostic frames do not establish device, child or owner acceptance.

Combined-scope local validation uses exact Godot 4.7.2-stable. The full
`scripts/ci.sh` run passed static/art/metadata/import gates, 95 visual-audit
contract tests and the unchanged gameplay probes. Four probes still assumed
the retired boss timing; their interaction drivers were updated to earn the
real warning/avoidance/counter openings, preserving completion assertions.
The subsequent complete 78-probe roster passed all gameplay checks. Its
`probe_castle_pearl_art` process exited before emitting a verdict; an isolated
retry exited 0 with `CASTLE2D|done failures=0`. Thus all 78 trusted probes have
passing current-source results, although the aggregate runner itself exited
nonzero for that startup failure. Logs are `tmp/bunny-rebuild/full-ci-shared.log`,
`final-probe-roster.log` and `pearl-final-retry.log` under the same directory.

Parser/inference checks, document authority, typography classification and
source/capture hash verification pass. Game-wide migration remains
`NO_REGRESSION`, not zero debt; the advisory visual audit remains
`UNSATISFIED` for its existing open items. Remote exact-head CI and dev/APK
integration are the remaining delivery gates for this combined candidate.

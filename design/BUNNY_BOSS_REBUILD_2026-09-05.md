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
Drag anywhere in unclaimed arena space to move, release, then tap to counter.
Keyboard/controller action and existing touch action remain accessible.

Taking a hit costs the current counter opportunity and repeats the current
phase after a short recovery. Completed phases remain earned. Clean movement
therefore beats stationary tap spam, while no health depletion can end play.
Repeated bumps or missed openings lengthen warnings/openings; assistance never
inserts damage or awards a win without input. Existing mastery and pearl rewards
remain an optional replay incentive.

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
| Learning | 44.50 | 0 | 0 | Three counters, complete |
| Slow movement | 59.35 | 4 | 0 | Recovers, complete |
| Slow counter response | 61.80 | 0 | 2 | Wider openings, complete |
| Moving and repeatedly tapping | 43.50 | 0 | 0 | Movement still required, complete |

Idle, stationary tap spam, and held-action controls each scored zero rounds in
60 seconds. Movement-only scored zero rounds despite seven avoided attacks and
six expired openings. The integration probe additionally sweeps 16 edge
positions across every phase/step and exercises the live door, checkpoint,
performance retention, head tap, friendship, reward and Day Two seams.

The Mobile-rendered shot run captured tells, impacts, recovery, counters and
friendship. Inspection found and corrected a hidden warning layer and foreground
scenery/caption occlusion. The warning renderer ignores input, the camera reserves
the HUD/caption bands, and lowered walls expose the playable floor. These desktop
captures are visual evidence only; they do not establish Android frame rate.

Full local validation completed on Godot 4.7.2-stable: static/art/metadata gates,
95 visual-audit contract tests, and all 78 trusted probes. The full command's
initial exit was nonzero because the final `probe_props` process ended before
its verdict; its isolated rerun exited 0 with `PROPS|result: ALL OK`. The boss
and animation probes both passed inside the full run, including the final-round
interruption case. Game-wide migration remains `NO_REGRESSION`, not zero debt;
the advisory visual audit remains `UNSATISFIED` for its existing open items.

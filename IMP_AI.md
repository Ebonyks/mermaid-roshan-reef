# IMP_AI.md — the mischief-imp brain (2026-08-02)

One decision layer, shared by every imp fight in the game.
Code: `scripts/imp_ai.gd` (class `ImpAI`). Probe: `scripts/probe_imp_ai.gd`.

## Why

Owner report, 2026-08-02: *"imp combat behavior seems extremely weak."* It
was. Every fight had its own two-line loop and none of them made a single
decision:

| fight | old behaviour |
|---|---|
| opera stage scuffles (`opera_career_world_2d.gd`) | ping-pong along the painted walkway, wait to be tapped |
| toy-castle brawl (`games/brawl.gd`) | beeline at the nearer hero, bump, repeat |
| dungeon / Ember arena (`combat_arena.gd`) | drift to 7 m, stop, lob one slow orb every ~3 s |
| stuffie battle (`stuffie_battle.gd`) | hold a fixed ring; the QTE did all the acting |

Imps read as props, not characters. The brain gives them a repertoire, a
crew that coordinates, and a mood that answers how the fight is going —
without ever breaking the no-fail rules.

## The loop, per imp

```
prowl ─ stalk ─ flank      hold the crew's spacing ring, close the gap, circle
   │
   └─► windup              TELEGRAPH: crouch, freeze, gold ring + "!"
          │                never shorter than ImpAI.MIN_WINDUP (0.55 s)
          ▼
        charge             COMMITTED: dashes at the spot she was standing on
          │                when the crouch started. It does not re-home.
          ▼
        slash              the swipe. Lands → "contact"; misses → "whiff"
          │
          ▼
        recover            THE COUNTER WINDOW: slumped, slow, and a bigger
                           tap target (×1.45 reach) than an imp on its feet

guard    captains only, after being hit — always drops on its own clock
stagger  reeling from a hit or a stun; decides nothing until it wears off
taunt    she has not played for 3.5 s: come into view and show off
rally    the captain calls a thinned crew back together
flee     the last of the crew loses its nerve — briefly, and always catchable
bopped   retired
```

Every state is a **pose** string the renderer plays (`ImpAI.POSES`). No art
is required: each site plays the pose procedurally (squash, tilt, lift,
tint) and swaps in state sprites the moment they exist —
see `CODEX_IMP_ANIMATION_HANDOFF_2026-08-02.md`.

## The crew brain, per tick

* **attack tokens** — only `attackers_allowed()` imps may be winding up or
  charging at once (hard ceiling `max_attackers`, normally 2). The crew
  picks who: closest, boldest, off cooldown.
* **flank slots** — alive imps are handed evenly spaced angles around the
  hero and *orbit* to them (radius + angle, never a straight line through
  her), so they surround instead of forming a conga line and never end up
  standing inside Roshan.
* **morale** = alive / crew size. Below 0.4 the crew stops swarming; below
  0.34 the survivors start scampering. A fight visibly winds down.
* **aggression** rises while the child is *not* landing hits (the imps come
  to her — nothing can stall) and drops 0.22 on every landed bop (a
  breather after every win). It shortens cooldowns, never the telegraph
  below the floor.
* **mercy** — after `mercy_delay` (45 s) everything slows, telegraphs
  lengthen, and the fight becomes strictly one-attacker-at-a-time.
* **contact gap** — a crew-wide floor (5 s) between landed bumps. Being
  bumped is an event, never a drizzle.

## No-fail contract (binding — CLAUDE.md)

The brain deals no damage and scores nothing. A landed slash emits one
`contact` event; the caller turns that into a bubble-shield bump, a
sparkle and a shove. Consequences may only ever *add*: on the opera stage
a bump lets the imp run off with a sparkle, and popping that imp wins it
back (+0.5 progress). Nothing is ever taken away, and no imp action can
end a beat. A zero-input run still wins nothing — the brain cannot pop an
imp, only the child's tap can (`probe_passive`, `probe_imp_ai`).

## Wiring (all state stays on the caller)

`ImpAI` is a RefCounted satellite: pure logic, no nodes, plane-agnostic. It
thinks in a 2D plane using **the caller's own units** — screen pixels on
the opera stage, metres on a 3D floor — so each site passes its own tuning
dict.

```gdscript
brain = ImpAI.new(TUNE, seed)          # seeded: same fight every run
brain.begin_crew(count)
mind = brain.spawn_mind(index, captain)  # store it in your enemy record
...
mind["pos"] = <where the imp is>; mind["alive"] = true
brain.tick(delta, minds, hero_pos)
<read mind["pos"], mind["pose"], mind["face"]; clamp to your world>
for ev in brain.drain_events(): ...    # telegraph/charge/contact/whiff/…
brain.on_player_swing(landed)          # every swing, hit or miss
brain.on_hit(mind, popped)             # bops, freezes
brain.on_stun(mind, seconds)           # Huluu's stun bubble
```

| site | plane | notes |
|---|---|---|
| `opera_career_world_2d.gd` | 1280×720 px | positions snap back onto the painted walkway (`_stage_feet_at_x`); poses drive sprite swap + squash/tilt; telegraph draws a gold ring + "!" |
| `games/brawl.gd` | courtyard metres (x, z) | clamped to the open segment; Huluu's stun feeds `on_stun`; one brain per wave |
| `combat_arena.gd` | arena metres | clamped inside the octagon; imps too far to reach throw instead of standing about |
| `stuffie_battle.gd` | arena metres | `"lunges": false` — the brain owns spacing and mood, the DODGE QTE keeps owning attacks |

`opera_act.gd`'s legacy 3D scuffles are deliberately untouched: those acts
are being replaced by the 2D career worlds (GAME_REDESIGN_2P5D_2026-07-27).

## Tuning

Defaults live in `ImpAI.DEFAULTS`; each site overrides. The knobs that
matter most: `strike_range` (when a lunge is even considered), `stand_off`
(the spacing ring), `contact` (slash reach), `windup` (telegraph),
`recover` (counter window), `cool_min`/`cool_max`, `max_attackers`,
`contact_gap`.

Raising boldness can never break readability: `windup_time()` is clamped
at `MIN_WINDUP` and the probe asserts it.

## What the probe guards

`scripts/probe_imp_ai.gd` (in `scripts/ci.sh` and the CI probe list) runs
whole fights headless and asserts on the decision stream: no unannounced
charge, the telegraph floor, the attacker ceiling, the contact gap, the
full pose repertoire, a committed charge being dodgeable and never
re-homing, thinned-crew flee/rally, the captain's stagger→guard→drop,
mercy, the QTE mode's silence, that nothing pops itself, and that the same
seed replays the same fight while a different seed does not.

# Pearl Castle dust-bunny AI — 2026-08-02

Supersedes the behaviour half of `CASTLE_DUST_BUNNY_SPAWN_GUIDE_2026-07-29.md`
(the three founder spawns, their coordinates and the one-touch clear contract
are unchanged; what follows replaces "one static, one static, one patrol").

## Outcome

The Main Hall no longer ships a fixed cast of three dust bunnies. It grows a
**colony**: the three authored founders plus generated bunnies, and it keeps
passively making new ones while Roshan plays. Every bunny has exactly one hit
point, hops at a toy pace, and cannot hurt her — there is still no fail state,
no timer, no score and no reading anywhere in the interaction.

## The critter contract

| Property | Value |
| --- | --- |
| Hit points | `1` (`HALL_BUNNY_HP`), decremented by `_damage_dust_bunny()` |
| Damage to Roshan | none — a bunny has no attack, no push and no block |
| Clear condition | one contact between her live foot and the bunny's ellipse |
| Travel speed | ~46 logical px per hop, ~1.1 s per hop-and-rest cycle (≈40 px/s) |
| Roshan's speed | ≈680 logical px/s — she outruns every bunny by ~17× |
| Live cap | `HALL_BUNNY_LIVE_CAP = 5` cards (mobile visible-card budget) |

## Versions the game generates

`HALL_BUNNY_VARIANTS` is the generator's palette. Weights bias the mix; the
three founders always cover the sleeping and shell-hiding versions.

| Role | Art | Motion | Behaviour |
| --- | --- | --- | --- |
| `sleeping_static` | `dust_bunny_sleepy.png` | none while asleep | breathes in place; wakes when a shell sconce near it is switched **on** (or a prop startles it), then hops; curls back up after ~5 s of resting in the dark |
| `shell_static` | `dust_bunny_shell_hide.png` | none | peeks out of its shell in the dark when Roshan is far; tucks back under when a sconce lights it or she comes within 340 px |
| `runner` (founder) | `dust_bunny_hop.png` | hop patrol | keeps the guide's `1850 → 2550` patrol, now as hops instead of a slide |
| `hopper` | `dust_bunny_hop.png` | hop patrol | wanders its own ±420 px patch, drifts toward the darker side of the hall, hops away from Roshan |
| `shy_hopper` | `dust_bunny_hop.png` | hop patrol | smaller and further forward; same rules with a tighter ±300 px patch |
| `family_nursery` | `dust_bunny_family.png` | none | a huddle that sits and breathes — and while it is alive the hall spawns pups next to it on the faster clock |

Every generated bunny is unshaded, depth-tested, `proximity_only` (no Button
hotspot), and gets a small pitch/scale/depth jitter so no two read as clones.

## What the Codex art dictates

The behaviour inputs are the props already painted into this hall — no new
artwork was generated for this task and no existing pixel was modified.

| Codex asset | Effect on the AI |
| --- | --- |
| `main_hall_sconce_atlas.png` shell sconces (7 fixtures, `castle_room_light_states`) | light level per x drives sleep/wake, hide/peek and the direction bias — bunnies always hop toward the darker side |
| `main_hall_tapestry_atlas.png` royal shell tapestry | unfurling it startles every bunny within 560 px: sleepers wake, hoppers flee away from it for 2.4 s |
| `HALL_PORTALS` painted doorways | generated bunnies never spawn within 90 px of a door approach foot, and their cards sit low enough that no card can reach a door approach band even at the top of a hop |
| Roshan's arrival mark `(380, 835)` | nothing spawns within 260 px of it |
| `dust_bunny_family.png` | the nursery variant: while a family huddle lives, the passive spawn clock drops from 13 s to 9 s and pups appear beside it |

## Passive generation

- One colony per castle visit, seeded from `castle_visit_serial`, so a later
  visit brings a different mix without touching `reef_save.json`.
- The founders are always spawn 1–3; the generator adds 1–2 more at open.
- `_update_dust_bunny_spawner()` refills: whenever live bunnies are under the
  cap, a new one puffs in (star burst + boing) every `HALL_BUNNY_DRIFT_INTERVAL`
  (13 s), or every `HALL_BUNNY_NURSERY_INTERVAL` (9 s) with a nursery alive.
- Spawn x comes from `_hall_bunny_free_spans()`: the hall floor minus door
  approaches, minus Roshan's arrival mark, minus 150 px around every live
  bunny. A cleared bunny gives its patch back.
- Cleared IDs are never reused, so clearing is permanent for the visit while
  the hall still keeps producing fresh bunnies to find.

## Runtime state

All of it is visit-scoped on `main` (nothing is added to the save file):

`castle_visit_serial`, `castle_dust_bunny_colony`,
`castle_dust_bunny_spawn_clock`, `castle_dust_bunny_spawn_serial`,
`castle_dust_bunnies_cleared`, `castle_dust_bunny_runner_time`.

Per-bunny AI state lives on its `castle_room_item_sprites` record
(`bunny_role`, `bunny_state`, `bunny_center`, `bunny_bounds`, `hp`, …) and is
mirrored onto the Sprite3D as `dust_bunny_state` / `dust_bunny_hp` metadata for
probes. Leaving and re-entering the Main Hall rebuilds the cards and resets the
poses; the colony roster and the cleared list survive until the castle closes.

## Probe coverage

`scripts/probe_castle_pearl_art.gd`

- `main_hall_generates_several_dust_bunny_versions` — more than the three
  founders, all within the live cap, every card unshaded/depth-tested/1 HP;
- `main_hall_colony_includes_sleeper_and_shell_hider`;
- `main_hall_dust_bunny_colony_size_within_budget`;
- `main_hall_two_static_dust_bunnies` / `main_hall_third_dust_bunny_runs` —
  unchanged founder contract;
- `main_hall_dust_bunnies_hop_slowly` — ≤120 logical px travelled per second;
- `main_hall_shell_bunny_hides_and_peeks`;
- `main_hall_sconce_light_wakes_sleeping_dust_bunny`;
- `main_hall_dark_settles_woken_dust_bunny_back_to_sleep`;
- `main_hall_one_touch_dust_bunny_explosions` and
  `main_hall_dust_bunny_explosions_exactly_once` — the one-hit-point rule;
- `main_hall_cleared_dust_bunnies_do_not_respawn_this_visit`;
- `main_hall_passively_generates_more_dust_bunnies` — refills after clears,
  never past the cap, never reusing a cleared ID.

`scripts/probe_crown.gd` counts the hall as seven authored props plus the live
colony (3…cap) instead of a hard ten.

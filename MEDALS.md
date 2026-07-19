# MEDALS.md — bronze / silver / gold rankings

Owner decision 2026-07-18: every game ranks each completed run
bronze / silver / gold. The game is growing with its player — bronze keeps
the no-fail promise for the 4-year-old of today, gold is a genuine
skill-and-precision target sized for the 6-8-year-old she'll become.

## Rules (enforced by MedalSystem + probe_rank + probe_passive)

- **Bronze = completion.** Every finished game earns at least bronze.
  There is still NO fail state anywhere — a medal is always added, never
  denied, and a game never ends early because of performance.
- **Upgrade-only.** `m.medals` (game id → best tier) only ever goes up.
  A slower replay keeps the old medal. Persisted in `reef_save.json`
  under `"medals"` (NOT in `KNOWN_KEYS`, same pattern as `"critters"`,
  so pre-medal saves stay schema-complete).
- **Win-path only.** Awards fire exclusively from win/completion code.
  probe_passive asserts zero-input play can never touch `m.medals`.
- **Non-reader display.** Tiers are pure glyphs: 🥉 🥈 🥇 — award banner +
  tier-colored sparkles + rising chime on every finish, a floating medal
  under each friend's won-star, and a 🥇/🥈/🥉 tally on the HUD stars line.
  The surrounding win flow still plays the family `*_win` voice lines.

## Where the code lives

- `scripts/medal_system.gd` — Phase-7-style satellite (state on main:
  `m.medals`; logic here). `evaluate()` is pure; `award_stats()` is the
  single award entry point.
- Central hooks: `main._end_game` (all 8 arena games via `m.g`),
  `PictureGames._mg2d_win`, `main._kart_completion_committed`, the bell
  song win, `CombatArena._win` (standalone only), `DungeonLevel.
  _complete_dungeon`, `GalaxyLevel._win`, `DanceEngine._finish_round`.
- Gate: `scripts/probe_rank.gd` (tier table, purity, upgrade-only, a real
  fetch win, save round trip), registered in `ci.sh` + `probes.yml`.

## Tier table (tuning knobs — `MedalSystem.TIERS`)

Times are real seconds of the run; "≤/≥" bounds are inclusive.

| Game id | Signal | 🥇 Gold | 🥈 Silver | 🥉 Bronze |
| --- | --- | --- | --- | --- |
| fetch | lake splashes `g.miss` | 0 | ≤ 2 | finish |
| dolls | dropped babies `g.missed` | 0 | ≤ 2 | finish |
| seek | slowest single find (s) | ≤ 12 | ≤ 25 | finish |
| melody | full rainbow time (s) | ≤ 75 | ≤ 150 | finish |
| slide | fish caught `g.got` | 5 / 5 | ≥ 3 | finish |
| penguin (chase) | caught him / cornered him | caught | ≥ 1 panic burst | finish |
| race | play-place course time (s) | ≤ 80 | ≤ 160 | finish |
| treasure | cavern dive time (s) | ≤ 100 | ≤ 200 | finish |
| fairy | shield losses + bugs zapped | 0 fails, 10 hits | ≤ 1 fail | finish |
| snowman | build+chase time (s) | ≤ 80 | ≤ 160 | finish |
| garden | five flowers time (s) | ≤ 25 | ≤ 60 | finish |
| trampoline | reach the star time (s) | ≤ 10 | ≤ 25 | finish |
| xmas | tree decorated time (s) | ≤ 35 | ≤ 80 | finish |
| kart | podium place | 1st | ≤ 3rd | finish |
| galaxy | butterfly rescue time (s) | ≤ 360 | ≤ 720 | finish |
| combat_ice | swarm cleared time (s) | ≤ 60 | ≤ 120 | finish |
| combat_fire | boss tamed time (s) | ≤ 75 | ≤ 150 | finish |
| dungeon | rooms cleared in ONE visit | 10 | ≥ 5 | finish |
| bells | echo mistakes | 0 | ≤ 2 | finish |
| dance | best combo streak in a round | ≥ 10 | ≥ 5 | any hit |

Unranked on purpose: shop (a store, not a game), the 2D "slide" screen
(reroutes to the 3D play place = `race`), dungeon combat rooms (they roll
into the one `dungeon` medal), sleep/hug/craft cutscene stickers.

Replayable golds everywhere: galaxy re-awards on replay after `bwdone`
(the pearl/skin grand prize stays once-per-save), dance re-ranks every
round, and `_end_game` ranks every win — not just the first trophy.

## Tuning notes

The time thresholds are first-pass estimates from course sizes and tick
speeds, not from on-device play. When she starts collecting silvers,
re-time real sessions on the phone and tighten/loosen `TIERS` in one
place; probe_rank's table test pins whatever the values are, so update
the probe's expected cases in the same commit.

# Quiet medals (package QM)

Part of the [learning-sessions work order](README.md). Owner choices:
`ODR-MEDALS-QUIET-20261018` (soften the medals, all three ways) and
`ODR-GUIDE-VOICE-20261019` (new narrator voice). Written by Claude; Codex
implements, paints the keepsake and generates the voice lines.

## 1. The owner decision, and what stays the same

On 2026-10-18 the owner answered "Yes, all three" to softening the medals,
approving: **surprise medals instead of a banner on every finish, speed
tiers hidden from her, and new synthetic lines praising what she did ("You
kept trying!"); tiers are still computed and saved, upgrade-only.** This
amends the display and celebration parts of the 2026-07-18 decision in
`MEDALS.md`.

Unchanged:

- Bronze is completion; every finished game still earns a tier.
- Tier maths (`MedalSystem.evaluate()`, `TIERS`, `OperaMastery.evaluate()`,
  `RULES`) and its probe tests.
- Upgrade-only saving in `m.medals` (save key `medals`) and in the Opera
  mastery ledger. No save key is removed (`DL-SAVE-01`).
- Awards fire only from win paths; a zero-input session changes nothing
  (`DL-AGE-04`, `DL-MOT-05`).

Why: the learning-value review found that the medals grade speed and
accuracy with a banner, sparkles and a chime on every finish, the reward
type most linked to losing interest later. Unexpected rewards, and feedback
about what the child did, do not carry that risk (sources in the
[README](README.md#3-evidence-copied-from-the-review)).

## 2. What she sees today (dev `e1dc3e21f67afeacf48a3609ac520468d6fecc28`)

| Surface | File (blob SHA-256) | Today |
|---|---|---|
| Finish ceremony | `scripts/medal_system.gd` (`585959372cbe4bf2e98d0830097b3b98c9519b52645516857a61ce22b489d36d`) | `award_stats()` calls `_celebrate()` on **every** ranked finish: a centred card with an emoji medal (🥉 🥈 🥇), a row of filled and empty stars by tier, 8, 10 or 12 sparkles in the tier colour, and the chime pitched higher for better tiers, for 2.2 seconds. Grand Puff's card adds a 💎 gem for a run with no bumps. Only then are upgrades saved. |
| HUD tally | `scripts/main.gd` (`hud_stars.text`) and `MedalSystem.hud_suffix()` | A line "🥇 n 🥈 n 🥉 n" under the star line, all the time. |
| Opera careers | `scripts/opera_mastery.gd` (`1a5c6f89f2cd0effea2b22e85a29c3dcfcebb0298fb6d582b81a9bb427518bf3`), `scripts/opera_act.gd` (`9e2fa238b904db3b0548f3b76ddd647f6e27934f4a3148da3c893b04ccf135a3`), `scripts/opera_performance_overlay.gd` (`16c7a17ed901750764481e7077ac2e60d4cf5bfc1a3b41970066e4a633545ddb`) | Fifteen careers are ranked by active seconds, misses and assists. The best tier is written to `m.medals["opera_<career>"]`, and `show_result(tier, token_delta, token_balance)` draws the tier result with "+N" encore tokens (worth 1, 3 and 6 in total by tier). |
| Grand Puff captions | `scripts/games/dust_boss.gd` (dev `05f9174e05c0c00ee09cf21c8e70e251c3afbed8e35b9f9526e200de65869a0d`; care branch `226016e382a8956fcf5ca9a4eddfc4e591be8d4c446d9bb0d2e644558d9f706c`) | The victory caption names the tier ("Three gold stars…", "Two silver stars…", "A bronze star…"); a run with no bumps adds two bonus pearls. |
| Documentation | `MEDALS.md` (`715f32fe2a5715ceea6de2a003882016d2099c4ec73459a90df908a72b024962`) | Still describes a floating medal under each friend's won-star; the code retired it (`refresh_friend_glyphs()` is now only a compatibility hook). |

The emoji medals and the gem carry reward meaning on their own, which
`DL-TYPE-07` does not allow (finding `MA-TYPE-004`). This package removes
them from the child's screen; it does not close that finding, which covers
the whole game.

## 3. Target behaviour

### QM1: hide the tiers

- No child-facing surface shows or sounds a tier: no 🥉 🥈 🥇 or 💎, no
  bronze, silver or gold colour, no star row that counts a tier, no chime
  pitched by tier, and no caption that names a tier.
- Remove the HUD medal tally. A standing tally is a persistent report card,
  which `DL-UI-07` keeps off the play surface. `hud_suffix()` returns an
  empty string, or the call is removed with its probe.
- Grand Puff's victory caption becomes one tier-neutral line for every run:
  "All clean! Grand Puff feels better!" (already the care branch's wording
  for a run with no bumps).
- The Opera result overlay draws no tier-specific medal or colour. Its token
  numbers stay as they are (see OQ1).
- Tiers are still computed, saved and probed, so a later owner decision can
  show them again (for example when she is older). Remove the old ceremony
  code rather than parking it behind a switch.

### QM2: a surprise keepsake, not a banner

- **When:** only the first time a ranked game is completed on a save,
  meaning its stored best tier was 0 before this award. That covers every
  `MedalSystem` game id and every `opera_<career>` medal. Later completions
  of the same game show no medal moment at all.
- **Never:** random, announced in advance, tied to speed or score, counted
  in a streak, daily, or used to ask her to keep playing (the review's
  guardrails, ICO standard 13).
- **The moment** (one shared helper in `MedalSystem`, used by both the
  minigame and Opera paths, `DL-CODE-05`): after the friend's existing win
  line, a painted keepsake rises to the centre; one soft burst in a single
  warm palette, the same for every game; one gentle chime at one fixed
  pitch; the narrator says "A little surprise for you!" About 2.5 seconds,
  and a touch skips it.
- **Keepsake art (new, Codex):** a small round rosette of pearl and shell
  with a short rainbow ribbon, in the game's pastel storybook style (navy or
  purple outline, lavender shadow). No number, letter or star count, and no
  colour that could read as bronze, silver or gold. It is an authored
  texture, never an emoji (`DL-TYPE-07`). Check existing art first
  (`DL-ASSET-01`); if nothing fits, generate one 512 × 512 picture for this
  gap (`DL-ASSET-02`) and add its `ASSET_LICENSES.md` line in the same
  change.
- **Her current save:** games that already hold a medal have had their
  first moment, so on her save surprises will be rare: new or rebuilt games
  only. Her saved medals and tiers stay untouched.

### QM3: praise what she did

- After every ranked completion, following the friend's win line and any
  surprise, the narrator says one line about what she did. Never speed,
  score, rank, comparison, or who she is ("clever", "smart", "good girl").
- **Which line:** if the run's internal tier is bronze, a "kept trying"
  line; otherwise the line for the game's category (section 5). Each
  category has two lines, alternated by a counter that is not saved.
- The line waits for the win line to finish, never overlaps it, can be
  skipped with a touch, is cleared on teardown, and ducks the music
  (`DL-SND-03`, `DL-SND-04`, `DL-SND-14`).
- No praise for practice or developer play-test runs, or anything that
  earns no tier (the shop, tutorials).
- Protected and existing win lines are untouched (`DL-SND-05`,
  `DL-SND-11`); praise is added after them.

### QM4: documents

- Rewrite the display section of `MEDALS.md`: the tier table stays as
  internal tuning; the display rules become QM1 to QM3; cite
  `ODR-MEDALS-QUIET-20261018`; drop the stale floating-medal text.
- Update the `MEDALS.md` ledger row note when the display changes ship.

## 4. Voice lines (new narrator voice, package VG)

| Key | Exact line |
|---|---|
| `surprise_keepsake` | A little surprise for you! |
| `praise_kept_trying_a` | You kept trying, and you did it! |
| `praise_kept_trying_b` | You did it, one little step at a time! |
| `praise_looked_a` | You looked so carefully! |
| `praise_looked_b` | You looked carefully and found it! |
| `praise_gentle_a` | You were so gentle! |
| `praise_gentle_b` | You took such gentle care! |
| `praise_listened_a` | You listened so well! |
| `praise_listened_b` | You listened and followed the music! |
| `praise_kept_going_a` | You kept going all the way! |
| `praise_kept_going_b` | You kept going to the very end! |
| `praise_made_a` | You made it yourself! |
| `praise_made_b` | You made that with your own hands! |
| `praise_thought_a` | You thought it through! |
| `praise_thought_b` | You had an idea, and it worked! |

"One little step at a time" echoes the picture book's refrain ("One little
job at a time"). Each line has an adult caption with the same words.

## 5. Praise category for each ranked game (default mapping)

| Category | Minigames (`MedalSystem` ids) | Opera careers |
|---|---|---|
| gentle | `dolls`, `dustboss` | `doctor`, `nursery`, `farmer` |
| looked | `seek`, `treasure` | `detective`, `magician`, `geologist` |
| listened | `melody`, `bells`, `dance` | `ballerina`, `popstar` |
| kept going | `fetch`, `slide`, `penguin`, `race`, `trampoline`, `kart`, `galaxy`, `fairy`, `combat_ice`, `combat_fire`, `dungeon` | `boxer`, `racer` |
| made | `snowman`, `garden`, `xmas` | `chef`, `candymaker`, `painter` |
| thought | none | `teacher`, `astronaut` |

Each line must be true of what the game asked her to do. If a rebuilt game
changes its verb (for example the Pop Star, Ballerina and Racer rebuilds in
`MA-OPERA-014`), update its row in the same change.

## 6. Files that change

- `scripts/medal_system.gd`: the shared surprise ceremony replaces
  `_celebrate()` (first award only); tier glyph, colour and star display
  removed; `hud_suffix()` empty or removed; praise choice. `award_stats()`
  still returns the tier.
- `scripts/main.gd`: the HUD star line no longer appends a medal tally.
- `scripts/opera_act.gd`, `scripts/opera_performance_overlay.gd`: no tier
  drawing; the first Opera medal uses the shared ceremony; praise after the
  win line.
- `scripts/games/dust_boss.gd`: the tier-neutral victory caption. This file
  is also changed by FP: do it after the care branch is integrated, and not
  in parallel with FP.
- `scripts/audio_director.gd`: the 15 new keys and a route that queues after
  the win line.
- Probes: `scripts/probe_rank.gd` (keep the tier table, purity, upgrade-only,
  real fetch win and save round-trip cases; replace the display asserts),
  `scripts/probe_passive.gd`, `scripts/probe_opera_performance.gd`, and any
  other probe that asserts the old ceremony node names
  (`MedalCelebration…`), `hud_suffix()` or tier wording. Find them by
  searching.
- `MEDALS.md`; new keepsake art and its `ASSET_LICENSES.md` line; new audio
  (package VG); an impact record.

## 7. Probes and checks

1. Unchanged tier maths: every existing tier, purity, upgrade-only and save
   case in `probe_rank.gd` passes untouched.
2. The first completion of a game with no stored medal plays one ceremony
   with the neutral keepsake and no tier glyph, colour or star row; the
   saved tier equals `evaluate()`.
3. A second completion, including one that upgrades the tier, plays no
   ceremony; the saved tier still upgrades.
4. The HUD shows no medal line in any state.
5. Opera: the first completion of a career plays the shared ceremony, later
   ones do not; the overlay draws no tier medal; token numbers are unchanged.
6. Praise: a bronze run gets a "kept trying" line, a silver or gold run its
   category line; variants alternate; nothing for practice, developer
   play-test or unranked runs; the line follows the win line, is skippable
   and stops on teardown.
7. Zero input: no ceremony, praise or medal change (`probe_passive.gd`;
   `MA-CI-005`).
8. A code search finds no child-facing node or caption that shows 🥉, 🥈,
   🥇, 💎, a tier star row or the words gold, silver or bronze as a result.
9. Full `scripts/ci.sh` at exact Godot 4.7.2-stable, then green branch CI
   before integration.

## 8. Acceptance

Report implemented, machine-verified and still-open claims separately.

- **Machine:** section 7 passes; document, development and 2D gates pass.
- **Visual:** Mobile captures at 1280×720 and a wide phone of a first and a
  repeat finish in an arena game, a picture game and an Opera career.
- **Audio:** human review of all 15 lines at 4/5 or better (`DL-SND-15`);
  device timing (`DL-SND-16`).
- **Owner:** approves the keepsake and the lines (`DL-QA-06`).
- **Child, two weeks** (log in [PARENT_LOG.md](PARENT_LOG.md)):
  - Off-screen use: she uses the praise words about herself or someone else
    ("I kept trying!").
  - Chooses it again: she still picks her favourite games, without asking
    for medals or trying to "get gold".
  - Frustration: she asks where her medals went, or looks let down at a
    finish with no ceremony. If that happens twice, tell the owner; a small
    finish moment can come back by a new decision.

## 9. Open owner questions (defaults apply until answered)

| # | Question | Default |
|---|---|---|
| OQ1 | Opera encore tokens (1, 3 and 6 in total by tier) and Grand Puff's two bonus pearls for a run with no bumps still pay more for faster or cleaner play. Make them tier-neutral too? | No change in this work: they are separate currencies outside the medal decision. |
| OQ2 | Surprises come only on a game's first completion, so they will be rare on her current save. Add another trigger? | No other trigger. |
| OQ3 | Should a grown-up be able to see the hidden tiers somewhere? | No screen for it; tiers stay in the save for a later decision. |

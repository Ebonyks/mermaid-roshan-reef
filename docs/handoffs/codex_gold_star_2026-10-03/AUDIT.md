# Game-wide audit: strongest and weakest games (2026-10-03)

Status: `SUPPORTING_CURRENT` audit evidence, written by Claude at the owner's request. Audited head: dev `87f99268` (game code identical to `e9915f44`, where CI run [37170079511](https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/37170079511) ran 81 trusted probes clean). This is code reading and machine evidence only: no game was played on a phone, no child was observed and no owner acceptance is claimed. The live scores are in [the catalogue](../../../design/reference/games.json) and the rendered [scorecard](../../../design/reference/GOLD_STAR.md); this page explains them at the audited commit.

## 1. The answer

**Strongest games a child can reach today** (all rated 3 of 5; points out of 24):

1. Grand Puff in the Dusty Attic, 19. The best-built encounter in the game: exact cues, mercy that cannot be mashed, checkpoints and a persona balance probe. It fails the true-2D rule, because the fight itself is built from 3D nodes.
2. Pearl Castle rooms, 18. The hub: every objective has an exact recorded line and a gold door cue, and Roshan walks to each object before it animates.
3. Castle banner maker and the Royal Bedroom wardrobe, 18 each. Small customisation screens with a diegetic entry and a lasting change.
4. **Mermaid Pool cleanup (Day One), 17: the chosen gold-star reference.** It contains the strongest single activity in the game, the waterfall.
5. Comfy castle games and Free Baby Eagle, 17 each.

**Weakest:** everything a child cannot reach rates 1. That covers 21 live games behind one blocker plus 26 dormant, retired or prototype-only entries. Among the games a child can reach, the weakest are:

- Chapter 2's party preparation (2/5, a P0 blocker);
- stuffie adoption and care (15 points; the care loop hides behind a menu);
- the Sky Lagoon and the Bubble Bathroom (16 each). The bathroom's sponge and brush still float while Roshan stands still.

**The most important finding is a P0 blocker, [`MA-PLAY-005`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-005).** Chapter 2's story careers cannot start:

- The career world rejects the empty phase override it gives itself and runs half-built, raising script errors every frame.
- 19 of the 29 story steps of the eight party careers have no room object to open them.

So the first party job, the Farmer in the Dining Room, is a dead end. All 15 Opera careers, the lawn finale, the Galaxy and the Fairy Pond are unreachable from a fresh save, because each is unlocked only by finishing Chapter 2. Trusted probes stay green because each one calls internal functions instead of the real route.

## 2. What a child can reach from a fresh save

- **Reachable:**
  - Start menu, Sky Lagoon, Pearl Castle.
  - The Day One rooms: Bubble Bathroom, Mermaid Pool, Playroom (Baby Eagle) and Craft Room, then Grand Puff.
  - The Day Two card.
  - Castle extras after Day One: the banner maker, the wardrobe, the comfy castle games and the Royal Hall sparring class.
  - Stuffie adoption.
  - The first Chapter 2 job card, which then fails.
- **Live but blocked by `MA-PLAY-005`:** all 15 Opera careers, the lawn finale, the moonflower door and Butterfly House, the Galaxy, the Fairy Pond, the dance, and the Galaxy ice battle.
- **Dormant (no route at this head):** the five picture games, Dolls, Seek, Melody, the fish slide, Fetch, the Pearl Shop, Treasure, the penguin chase, the play-place course, the brawler, the dungeons, the kart race, the stuffie ladder, the Critter Book and the craft studio.
  - Most lost their route when the reef was retired (2026-09-09 to 2026-09-23). The friend launchers and picture frames lived only in the old 3D courtyard.
- **Retired:** the Reef (owner decision) and the courtyard train.
- **Prototype only:** the painter studio and the Faerie Garden restoration.

## 3. How it was scored

- **Rubric.** Twelve criteria from the design-language rules, each scored 0, 1 or 2; the full text is in [gold_star.json](../../../design/reference/gold_star.json).
  - C1–C10 were assessed by Claude: reachability, true 2D, non-reader objectives, one-finger input, no-fail agency, truthful action, authored art, feedback and reward, lifecycle and save, and machine verification.
  - C11 (open defects) is computed from the finding register, counting only game-specific defects.
  - C12 (device, child and owner acceptance) is computed from recorded acceptance. It is 0 for every game, and the owner's Chef verdict is recorded as "not accepted".
- **Rating.** A fixed rule turns the twelve scores into the master audit's 1–5 scale. A game a child cannot reach rates 1; a game-specific P0 blocker caps the rating at 2; a 5 needs every criterion at 2, including acceptance.
- **Who read what.** Six read-only agents read one family each and reported function- and line-level evidence. Claude then checked the decisive claims in code:
  - the Chapter 2 rejection and its unmapped stations, also reproduced at runtime;
  - the Astronaut tray soft-lock;
  - the Teacher help line;
  - the Opera playtest elevator;
  - the Galaxy idle payouts;
  - the Sky Lagoon castle line;
  - `DayOneContactAction2D` sharing.
- **Calibration.** Claude adjusted agent scores where the rubric required it. For example, the Pool's C10 is 1 because its waterfall completion uses a probe helper and its idle leg lasts 0.12 s, and Galaxy's C5 is 1 because of its idle pearl payouts.
- **Evidence binding.** Each score is bound to hashes of the functions or files it judged (`tools/gold_star.py --check` reports any that change). Agent line citations without a file were not copied into the catalogue.

## 4. Ranking of the games a child can reach, and of the blocked live games

| Rank | Game | Family | Rating | Points | C1-C12 | Why not higher |
|---:|---|---|---:|---:|---|---|
| 1 | Grand Puff in the Dusty Attic (Day One boss) | Day One | 3 | 19 | `202222122220` | Workable: fails C2 |
| 2 | Castle banner maker | System | 3 | 18 | `221212122120` | Workable: 4 criteria only partly met |
| 3 | Royal Bedroom wardrobe | System | 3 | 18 | `221221122120` | Workable: 4 criteria only partly met |
| 4 | Pearl Castle rooms | World | 3 | 18 | `222222121110` | Workable: 3 criteria only partly met |
| 5 | Comfy castle games (Day Two) | Minigame | 3 | 17 | `221221112120` | Workable: 5 criteria only partly met |
| 6 | Mermaid Pool cleanup (Day One) | Day One | 3 | 17 | `221212112120` | Workable: 5 criteria only partly met |
| 7 | Free Baby Eagle (Day One) | Day One | 3 | 17 | `221221222100` | Workable: an open P0/P1 defect; 3 criteria only partly met |
| 8 | Royal Hall sparring class | Action | 3 | 16 | `201221112220` | Workable: fails C2; 4 criteria only partly met |
| 9 | Craft Room tidy (Day One) | Day One | 3 | 16 | `221212111120` | Workable: 6 criteria only partly met |
| 10 | Bubble Bathroom cleanup (Day One) | Day One | 3 | 16 | `221220222100` | Workable: fails C6; an open P0/P1 defect |
| 11 | Sky Lagoon promenade | World | 3 | 16 | `221221112110` | Workable: 5 criteria only partly met |
| 12 | Stuffie adoption and care | System | 3 | 15 | `111221112120` | Workable: 7 criteria only partly met |
| 13 | Birthday party preparation (Chapter 2) | Chapter 2 | 2 | 13 | `220221111100` | An open P0 blocker; fails C3 |
| 14 | Boxer | Opera career | 1 | 18 | `022221122220` | A child cannot reach it in normal play |
| 15 | Teacher | Opera career | 1 | 17 | `022121122220` | A child cannot reach it in normal play |
| 16 | Magician | Opera career | 1 | 16 | `022122122110` | A child cannot reach it in normal play |
| 17 | Racecar Driver | Opera career | 1 | 16 | `022211122210` | A child cannot reach it in normal play |
| 18 | Nursery Nurse | Opera career | 1 | 16 | `022121221210` | A child cannot reach it in normal play |
| 19 | Birthday lawn and Ember King (Chapter 2 finale) | Chapter 2 | 1 | 15 | `021121222200` | A child cannot reach it in normal play |
| 20 | Moonflower door and Butterfly House | World | 1 | 14 | `021221112020` | A child cannot reach it in normal play |
| 21 | Ballerina | Opera career | 1 | 14 | `021212122100` | A child cannot reach it in normal play |
| 22 | Dance with Daddy (rhythm) | Minigame | 1 | 13 | `022211011120` | A child cannot reach it in normal play |
| 23 | Geologist | Opera career | 1 | 13 | `020211012220` | A child cannot reach it in normal play |
| 24 | Pop Star | Opera career | 1 | 13 | `022121112100` | A child cannot reach it in normal play |
| 25 | Stuffie Doctor | Opera career | 1 | 12 | `022111111110` | A child cannot reach it in normal play |
| 26 | Painter | Opera career | 1 | 11 | `022111111100` | A child cannot reach it in normal play |
| 27 | Farmer | Opera career | 1 | 11 | `022111111100` | A child cannot reach it in normal play |
| 28 | Galaxy ice battle | Action | 1 | 10 | `001121011120` | A child cannot reach it in normal play |
| 29 | Candy Maker | Opera career | 1 | 10 | `021111111100` | A child cannot reach it in normal play |
| 30 | Astronaut Engineer | Opera career | 1 | 10 | `022101111100` | A child cannot reach it in normal play |
| 31 | Pastry Chef | Opera career | 1 | 9 | `021111101100` | A child cannot reach it in normal play |
| 32 | Detective | Opera career | 1 | 9 | `021101111100` | A child cannot reach it in normal play |
| 33 | Fairy Pond flight | Minigame | 1 | 8 | `000111111110` | A child cannot reach it in normal play |
| 34 | Butterfly World (Galaxy) | World | 1 | 8 | `001011011120` | A child cannot reach it in normal play |

## 5. Games with no live route

| Game | Family | State | Points | C1-C12 | Main reason |
|---|---|---|---:|---|---|
| Faron's Sleepy Dolls | Minigame | `dormant` | 18 | `021222122220` | No route since the reef removal: the friend launchers are data only and _start_game has no caller for it. |
| Painter studio prototype | Minigame | `debug_only` | 17 | `021222112220` | Standalone prototype scene. |
| Harper and Fiona fish slide | Minigame | `dormant` | 17 | `022212112220` | No route since the reef removal: the friend launchers are data only and _start_game has no caller for it. |
| Faerie Garden restoration prototype | Minigame | `debug_only` | 16 | `022222112020` | Standalone prototype scene. |
| Hide and Seek with Evie and Lamb-a' | Minigame | `dormant` | 16 | `021212212210` | No route since the reef removal: the friend launchers are data only and _start_game has no caller for it. |
| Daddy's Rainbow Theater (melody) | Minigame | `dormant` | 15 | `022211112210` | No route since the reef removal: the friend launchers are data only and _start_game has no caller for it. |
| Christmas Tree (picture game) | Picture game | `dormant` | 15 | `020212212120` | No route: the picture frames were only built by the retired 3D lagoon courtyard. |
| Color-a-Friend craft studio | System | `dormant` | 14 | `020221112120` | No live route. |
| Flower Garden (picture game) | Picture game | `dormant` | 14 | `020211122120` | No route: the picture frames were only built by the retired 3D lagoon courtyard. |
| Snow Roller (picture game) | Picture game | `dormant` | 13 | `020112022120` | No route: the picture frames were only built by the retired 3D lagoon courtyard. |
| Trampoline (picture game) | Picture game | `dormant` | 12 | `020211012120` | No route: the picture frames were only built by the retired 3D lagoon courtyard. |
| Rainbow and Ocean kart race | Action | `dormant` | 11 | `001121012120` | No live route. |
| Stuffie sparring ladder | Action | `dormant` | 11 | `001211012120` | No live route. |
| Fetch with Chuck | Minigame | `dormant` | 10 | `001220011120` | No route since the reef removal: the friend launchers are data only and _start_game has no caller for it. |
| Northern kingdom | World | `dormant` | 10 | `001121011120` | Entries only in the retired courtyard phase. |
| Critter Book collection | System | `dormant` | 9 | `000021012120` | Critters never spawn in live play. |
| Castle and Ember dungeons | Action | `dormant` | 9 | `001020012120` | No live route. |
| Rainbow Slide play-place course | Minigame | `dormant` | 9 | `001111011120` | Only through the retired slide portrait. |
| Toy Castle brawler | Minigame | `dormant` | 8 | `001111011110` | No route since the reef removal: the friend launchers are data only and _start_game has no caller for it. |
| Ember Fortress | World | `dormant` | 8 | `001021011110` | No live route. |
| Pearl Shop | Minigame | `dormant` | 7 | `000110011120` | No route since the reef removal: the friend launchers are data only and _start_game has no caller for it. |
| Penguin chase | Minigame | `dormant` | 7 | `000110011120` | No route since the reef removal: the friend launchers are data only and _start_game has no caller for it. |
| Secret Treasure cave | Minigame | `dormant` | 7 | `001110011020` | No route since the reef removal: the friend launchers are data only and _start_game has no caller for it. |
| Courtyard and train | World | `retired` | 2 | `000000000020` | Retired; replaced by the Sky Lagoon promenade. |
| Slide launcher (picture game) | Picture game | `dormant` | 2 | `000000000020` | No route: the picture frames were only built by the retired 3D lagoon courtyard. |
| Reef and home ocean | World | `retired` | 2 | `000000000020` | Retired by owner decision. |

## 6. By family

- **Day One:**
  - Strong, consistent and true 2D. The Pool's waterfall and the bathroom's toilet scrub are the best activities in the game: Roshan travels, her hand makes contact, and only then does the authored dirt clear.
  - The bathroom's sink, drain and tub still move a free-floating sponge and brush while Roshan stands still (the owner's 2026-09-06 job rule, [`MA-PLAY-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-004)).
  - All Day One voices are synthetic placeholders awaiting owner listening.
  - Idle re-prompts are often silenced by a once-per-session filter.
  - Pointers are emoji text glyphs whose font coverage is unresolved.
- **Chapter 2:** The party cannot finish (`MA-PLAY-005`). Even before that, nothing guides a non-reader to the next job: the route lines speak of a glowing door that is never lit, the picture objective card sits on a hidden layer, and prompts use the silent caption path.
- **Opera careers:**
  - Excellent engineering in places:
    - Boxer: per-finger ownership and an end-to-end real-touch probe.
    - Teacher: speaks every counted pearl, and help never inflates mastery.
    - Ballerina: one geometry for paint, demo and hits.
    - Candy Maker: a pour registered to the art.
  - Recurring weaknesses:
    - a navy focus bloom and a completion puff over finished work;
    - code-drawn duplicates of painted objects;
    - no touch ownership in the shared gesture surface;
    - no action sounds;
    - probes that finish careers with a fake gesture.
  - Chef pours backwards and is owner-rejected ([`MA-OPERA-001`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-001)).
  - Geologist speaks unrelated lines over placeholder shapes.
  - A second finger soft-locks the Astronaut's first pipe round ([`MA-OPERA-013`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-013)).
  - Detective sends a slow child back to zero after about 40 seconds.
- **Picture games and minigames:**
  - Several strong Canvas games have simply lost their way in: Dolls, Seek, Melody and the fish slide each score 15–18 points.
  - The rest are 3D legacy with invisible actors after the model retirement: Fetch's Chuck, the penguin and Treasure's chest are all missing.
  - Wherever an instruction is spoken through the generic `talk` fallback, the child hears "This is so much fun!" instead of the instruction.
- **Worlds:** Pearl Castle is the strongest space. The Sky Lagoon is generous but its only objective plays a generic cheer: the key `roshan_day1_castle` has no recording, although "Let's walk to the castle!" exists. The castle's per-frame tick still runs through the old 3D lagoon code.
- **Action and systems:** The combat tutorial teaches well but is 3D with unspoken instructions. Most other action games are unreachable. The banner maker and the wardrobe are the best small systems.

## 7. New defects found

- [`MA-PLAY-005`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-005), **P0**: the Chapter 2 story careers cannot start or progress (above).
- [`MA-OPERA-013`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-013), **P1**: a second finger on the Astronaut tray loses the carried tile; round one can never finish.
- Observations recorded in the catalogue rather than as findings:
  - Galaxy pays a pearl every 9 seconds for standing at a fruit tray, and 2 pearls every 20 seconds at the fountain (`scripts/galaxy.gd`, rewards for zero input).
  - The Pool skimmer's spoken line follows the item index, so it can name the wrong object.
  - The Teacher's idle help line is queued and immediately cleared.
  - The Sky Lagoon castle line falls back to a generic cheer.
  - Detective's timed reset to zero.
  - The Opera Hall elevator opens the owner-requested "Job playtesting / DEV MODE" text menu to any child who taps the painted elevator. It was added on purpose on 2026-09-30, but must be gated before release.
- **A systemic weakness.** Most trusted probes call internal functions rather than the child's real route, so the suite stays green while routes are broken (`MA-PLAY-005`, the dormant minigames). The gold-star C10 criterion now asks for real input through every step.

## 8. Why the Mermaid Pool is the reference

The Pool is the strongest game that already meets the true-2D rule, and the clearest model of the owner's job rule:

- Roshan travels to each part of the job.
- Her hand stays in contact for the work time before credit counts (`DayOneContactAction2D`, shared with the seahorse and the craft room).
- Authored dirt clears from the approved clean fixture.
- Each part has its own line, and every change saves.

Alternatives considered:

- **Grand Puff** has more points but fails C2; a reference cannot break the medium rule.
- **Pearl Castle** is the hub rather than a game, and it lacks focus-loss handling.
- **The banner maker and the wardrobe** are customisation screens.
- **Boxer** has the best Opera engineering, but no child can reach it, and Codex was refining its art in parallel.
- **Teacher and Dolls** are also unreachable.

The Pool's gaps to a gold star are specific:

- C3: the skimmer's lines and the pointers;
- C5: the seahorse's eight identical taps and the dropped taps;
- C7: code-drawn effects and the room tint on Roshan;
- C8: wrong-object lines and silent drops;
- C10: helper completion and a trivial idle leg;
- C12: device, child and owner acceptance.

The proposed five-star implementation follows in the next commit of this change, with the art generation handed to Codex.

## 9. Recommended order

1. **Repair `MA-PLAY-005` first.** It returns Chapter 2, the lawn finale, all fifteen careers and the Galaxy route to the child. The fix and its probe are specified in [the finding](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-play-005).
2. **Finish the Mermaid Pool five-star proposal** and record a phone session, a child session and the owner's verdict, so the game has its first real gold star.
3. **Owner decision for the dormant Canvas games:** give Dolls, Seek, Melody and the fish slide a castle-room home, or retire them. They are strong and cheap to restore.
4. **Repair `MA-OPERA-013`,** and give the shared gesture surface per-finger ownership (pattern GS-10).
5. **Make the trusted probes use real routes.** New games then cannot pass while unreachable, because C10 and `gold_star.py --check` keep every new game file catalogued.

## 10. Limits

- No runtime was played except the one scratch check for `MA-PLAY-005`.
- No capture, phone, child or owner evidence was created.
- Agent reports are code readings with cited lines; Claude verified only the claims listed in section 3.
- Scores describe this commit and go stale when the bound code changes.
- The audit grants no acceptance, closes no finding and changes no game file.

# Every racing build, and which one the final game should use

- **Status:** the inventory and comparison (sections 2 to 5) are
  `SUPPORTING_CURRENT` analysis. The recommendation (sections 1, 6 and 7) is
  `PROPOSED / CANDIDATE` until the owner answers README Q2 to Q4. It changes no
  owner decision by itself.
- **Baseline:** dev `a0bb2cf4691631a534e210a5fb60fd227213322f`; branch commits
  as named. No game was run and no image was opened or made; captures are cited
  by name only.
- **Method:** every `origin/*` branch name and commit message was searched for
  race, racer, kart, track, lap, rainbow road, slide, rally, circuit and grand
  prix. Each candidate was read from its own commit. The owner's words below
  were checked in the files named (some exist only on branches).

## 1. The answer

There are ten racing builds in four families: the Opera Racer career in its
forms (V1, V6, V7, V8), the go-kart engine and its true-2D ports (V3, V4, V5,
V9), the slide games (V10) and the unbuilt Reef Grand Prix specification (V2).

**Recommended for the final game: a combination, R1 ("Castle-room Grand
Prix").**

- **Engine, course and view from V3**, the restored castle-room Canvas racer
  on `codex/racer-castle-integration-20261022` (`96d6ef9e`). This is the
  owner's latest explicit direction (2026-10-22: "Integrate thei superior game
  into mermaid roshan ... Use the tracks that were generated from the various
  rooms in the castle"), and it matches his 2026-10-03 priority ("Converting
  this engine to our racing engine, versus any others, is a priority"). It is
  built, true Canvas, idle-safe and green on remote CI.
- **The child rules from V2**, the Reef Grand Prix specification: three broad
  lanes chosen by a tap, so steering is a choice rather than a skill she cannot
  yet do; holding drives but cannot change lane, which makes it the slowest way
  to race; and a pit stop (pick a colour, fit the wheels with Roshan's hand)
  instead of the TUNE and TO THE LINE chores.
- **The contest from V6**, the imp-contest branch: the imp's kart can finish
  first, which restarts the race at once with everything kept, as the owner
  ruled for every competitive career (`DL-INT-14`). Its mercy is retuned to the
  owner's words, "after two failures, imp should radically slow down".
- **Head-to-head**: Roshan and the imp only. V3's eight-kart pack, which races
  a protected friend portrait and the book dolls and renames Baby Eagle
  "Sparkle", leaves the track (README Q3).

**Why not V2 alone.** The owner's own trail points at the existing game. On
2026-10-17 he wrote "the racer (there are several games build in this minigame
that are superior)"; generation 1 read "this minigame" as the Opera career set
(`audit/cycles/minigame-rebuild-20261017/owner_request.json`) and compared no
racing builds. His 2026-10-03 and 2026-10-22 words both name the existing
engine. The 2026-10-18 question that produced `ODR-RACER-VIEW-20261018` offered
only two options, a side-scroller or "a following camera over the existing
painted circuit", and neither was the existing engine. V2 is also unbuilt and
needs the most new art: three scenes in four parallax layers, a side-view
driver set and an imp kart.

**Why not V3 as it is.** It keeps the reasons the owner rejected V1: a held
finger drives (`scripts/racer_game_2d.gd:1063-1064`, `:1141` on the branch),
the imp cannot win (its own record: "Earlier first-to-two-laps Imp/rematch
behavior is not supplied by this source recovery"), and TUNE and TO THE LINE
stay. It adds continuous steering inside an eight-kart pack, which the
research behind generation 1 says children of four and five handle poorly, and
its record marks the art "NOT_ACCEPTED; existing flat room shells, large empty
framing and untextured road fail the owner visual standard".

**If the owner keeps the side-scroller (2026-10-18):** build V2 as specified,
taking the donor parts listed in section 8 (R2).

**For the demo:** leave V1 as it is. The freeze (`ODR-DEMO-FREEZE-20261031`)
parks every Racer change until the demo build is promoted. V1 appears only
after the Part 2 story ends.

## 2. The owner's words on racing

| Date | Exact words or recorded ruling | Where | On dev |
|---|---|---|---|
| 2026-07-12 | Penguin slide: "NO catch without beans" | `scripts/games/slide_race.gd:1471-1475` (comment) | Yes |
| 2026-07-13 | "track design at this point is repetitive. neither track has any interesting hazards." | commit `49b150a2`; `scripts/kart.gd:69` | Yes |
| 2026-07-13 | Playtest: "still feels bad, items don't work" | `KART_FEEL.md:96` | Yes |
| 2026-07-14 | "it doesn't make sense that the star is the hazard" | `scripts/kart.gd:90-91`; commit `1f9727fe` | Yes |
| 2026-07-18 | "the pink and blue orbs should be gone" | `scripts/kart.gd:992-994`; commit `9d74d517` | Yes |
| 2026-07-25 | Claude's note of an owner remark: "the Racecar and Pop Star acts already HAVE finished games behind them" | commit `acb51322` message | History |
| 2026-08-02 | Shows move into castle rooms; the Racer's home is "Cloud Movie Lounge or courtyard" | `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md:260`; `scripts/castle_career_routes.gd:29-31` | Yes |
| 2026-08-09 | Final medium: true 2D game-wide | `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` (`DL-MED-01`) | Yes |
| 2026-08-12 | "real/external kart routing is not accepted" | [`MA-OPERA-010`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-010) | Yes |
| 2026-09-30 | OD-A: "imp comes in during the final act, there should be a contest at the end that reflects part of the skill of the job that's a challenge against the imp"; OD-B: "If imp wins, the game restarts immediately afterwards." | [contest design](../codex_opera_imp_contest_2026-09-30/CONTEST_DESIGN.md) lines 29-31 | Yes |
| 2026-10-04 | OD-E: "Imp just restarts contest at end, after two failures, imp should radically slow down." `DL-INT-14` applies it to the Racer: "the imp's kart finishing two laps first is his win and restarts the race" | contest design lines 37-41; `DL-INT-10` and `DL-INT-14` | Yes |
| 2026-10-03 | "Racer specifically has a problem. There's a racing game that's 3d and has already been developed in this game. Converting this engine to our racing engine, versus any others, is a priority" | `fcee911c:design/audit_impacts/job-game-racer-refinement-20261003.json` (`owner_verbatim`) | **Branch only** |
| 2026-10-17 | "The weakest of the minigames so far are the pop star, the ballerina, and the racer (there are several games build in this minigame that are superior) ... These need to be completely rebuilt, current version are very weak." | `audit/cycles/minigame-rebuild-20261017/owner_request.json`; `ODR-MINIGAME-REBUILD-20261017` | Yes |
| 2026-10-18 | "Use the defaults for Q1-Q5, and merge the handoff into dev once its CI passes." Recorded as `ODR-RACER-VIEW-20261018`: "Rebuild the Racer as the side-scrolling three-lane race (Reef Grand Prix) rather than a following camera over the existing painted circuit." | `audit/cycles/minigame-rebuild-20261017/owner_reply_20261018.json`; [decision register](../../../design/reference/OWNER_DECISIONS.md) | Yes |
| 2026-10-22 | "Integrate thei superior game into mermaid roshan, then launch godot to ai with a demo of this game in action. Use the tracks that were generated from the various rooms in the castle" | `96d6ef9e:design/RACER_CASTLE_INTEGRATION_2026-10-22.json` (`owner_request_quote`). The row `ODR-RACER-EXISTING-INTEGRATION-20261022` exists only in that branch's generated `OWNER_DECISIONS.md`, not in `owner_decisions.json`, so a regeneration would drop it | **Branch only** |
| 2026-10-31 | Feature freeze until the demo build is promoted | `ODR-DEMO-FREEZE-20261031`; [demo handoff](../codex_demo_readiness_2026-10-31/README.md) section 3 | Yes |

Not owner decisions, though often cited as if they were: the whole Reef Grand
Prix design (Claude's; the owner accepted its direction by default); every
1-to-5 rating of a racing build; V3's precedence note ("The October18
side-scroll handoff remains an unimplemented alternate proposal"), which is
Codex's.

## 3. Lineage

- **Opera Racer career:** a 3D Opera act that launched the go-kart game
  (2026-07-18 to 07-25) → a 2D five-beat Racer (2026-08-01) → "Build F", a 2D
  world with a nested 3D kart lap (2026-08-05, `e924d9ba`) → the Canvas
  one-circle Racer (2026-08-09 to 08-12; still on stable `master` `ff68f955`,
  V7) → the painted-circuit Racer (2026-09-05, `f4a5de33`, current dev, V1) →
  the imp-contest version (2026-09-30, V6) → the castle-room Canvas racer
  (2026-10-22, V3); plus the Reef Grand Prix specification (2026-10-17/18, V2).
- **Go-kart engine:** 3D Rainbow Road (2026-06-27, `da6806a4`) → merged
  2026-07-20 → dormant on dev after the 3D models were retired (V5). Side
  branches: Go-Kart Cove (Jolt physics, 2026-07-13, V9); a Canvas port
  (2026-10-03) → a castle and Sky Lagoon chase rally (2026-10-04, V4) → the
  castle-room racer (V3).
- **Slides:** the play-place course (the original 2026-06-24 "race" game), the
  penguin chase and the fish slide (V10).

## 4. The versions

### V1. Painted-circuit Racer (current dev)

- **Where:** `scripts/opera_racer_surface.gd` (476 lines),
  `scripts/kart_driving.gd` (141), phases at
  `scripts/opera_career_world_2d.gd:331-335`; built 2026-09-05 (`f4a5de33`);
  report `design/OPERA_RACER_ENGINE_INTEGRATION_2026-09-05.md`. Movie Lounge
  card after the Part 2 story; also the developer elevator, hidden for the demo.
- **Play:** TUNE (circle the wrench), TO THE LINE (swipe the kart to the arch),
  RACE: two laps of about 24 s over the still painting; a finger on the bar
  drives and steers by its x position; a turbo disc also fires by itself when
  its meter is full; walls rebound softly; the rival paces at 0.94 with
  catch-up and only Roshan's finish ends the race. Idle: nothing advances.
- **Evidence:** real-touch legs in `probe_opera_2d` (second-finger turbo,
  cancel, re-entry); gold star 15 of 24 (stale); art re-audit 3.9 of 5,
  review open (`audit/minigame_art_quality_2026-09-05/racer_reaudit.md`).
- **Defects:** JW-RACE-1 to JW-RACE-5 in the
  [register](WEAKNESS_REGISTER.md#31-racecar-driver-bit-12).
- **Keep:** the touch-ownership and focus-loss code, the probe legs, the
  native-painting draw path, the wheel-fitting art.

### V2. Reef Grand Prix (specification only)

- **Where:** [RACER.md](../codex_minigame_rebuilds_2026-10-17/RACER.md) and its
  shared systems; on dev since `fa0ee524` (2026-10-18). Nothing is built (no
  lane model, no `probe_racer_lanes`).
- **Play:** a paddock (pick one of three kart colours; tap two glowing wheel
  spots and Roshan fits each wheel), then about 45 s of side-scrolling through
  reef, kelp forest and castle bridge to the `world_racer` stadium. Three
  full-width lane bands of at least 150 px; a tap swerves in about 0.4 s; the
  kart drives while she has touched in the last 3 s; holding drives but cannot
  steer. Rings boost; ramps launch with an air-tap trick; gentle bumps slow for
  0.8 s and never stop her; pearls are never lost; everything is visible 2 s
  ahead. The imp paces off her so an engaged child wins the first try about
  three times in four; if he wins, the race restarts within 2 s with nothing
  lost; after two of his wins he drives at half speed; ties go to her. Photo
  finish, podium, trophy; medals from honest play.
- **Evidence:** published-game and child-development references
  ([REFERENCES.md](../codex_minigame_rebuilds_2026-10-17/REFERENCES.md)
  section 4), which admit that no study compares continuous steering with lane
  choice at four or five. No runtime evidence.
- **Weak points:** unbuilt; the largest new-art volume; parallax overdraw risk;
  whether she understands lanes is unproven.

### V3. Castle-room Canvas racer (`codex/racer-castle-integration-20261022`)

- **Where:** tip `96d6ef9e` (2026-10-22), base `9c78f6aa`. Adds
  `scripts/racer_game_2d.gd` (1,905 lines), `scripts/kart_canvas_2d.gd` (653),
  `scripts/kart_course_worlds.gd` (45) and `scripts/probe_racer_integration.gd`
  (143); rewrites `scripts/opera_racer_surface.gd`. Records
  `design/RACER_CASTLE_INTEGRATION_2026-10-22.json` and its impact record, both
  on the branch. It recovers V4's engine (`recovered_source: fcee911c`).
- **Play:** TUNE and TO THE LINE unchanged from V1; RACE embeds the engine
  full-screen in the career world. A road view from behind the kart, drawn on
  Canvas, through Movie Lounge, Family Gallery, Royal Bedroom, Family Gallery
  and back. Eight racers: Roshan (`roshan_base.png`), "Sparkle" (the Baby Eagle
  art), "Princess Huluu" (`assets/characters/friends/huluu.png`, a protected
  friend portrait) and five book dolls from `assets/book/`
  (`scripts/racer_game_2d.gd:200-213` on the branch). A 1.5 s countdown;
  relative one-finger steering anywhere (180 px for full lock); an optional
  turbo button with auto-fire; pickups, zoom strips, ramps, drift, drafting and
  soft furniture that pays nothing on contact. Two laps take about 34 s, then a
  0.9 s seated coast and the career's curtain call; the career world owns
  rewards, save and Back. A held finger counts as driving; after a 2 s grace an
  idle kart stops ("sixty seconds unattended earns no distance, pearl or
  finish").
- **Evidence:** remote Probe Suite run 39913994741 succeeded at `96d6ef9e`
  (2026-10-23); the record lists 81 assertive local probes and a native demo of
  two laps with 28 pearls.
- **Defects (its own record):** final art not accepted; no second-lap voice
  line; the imp rematch not supplied; device, child and owner checks pending.
  Also: the voice still says "coral gates" on a castle course; protected art
  races; the decision row is missing from the JSON register.

### V4. Canvas port and chase rally (`codex/racer-existing-engine-2d-20261003`)

- **Where:** `4f718145` (the flat Canvas port, 2026-10-03), `892fc87e` (the
  chase rally, 2026-10-04), tip `fcee911c`; open pull request #21. Rewrites
  `scripts/kart.gd` as a 2D node and adds the Canvas presenter, course table and
  `probe_kart_canvas_2d.gd`. Records `design/RACER_EXISTING_ENGINE_2D_PORT_2026-10-03.md`
  and `design/RACER_WORLD_RALLY_2026-10-03.md` (branch only).
- **Play:** ride (moto, kart or truck) and eight paints chosen on picture
  cards with a 5 s auto-pick; 3-2-1; a road view with a visible steering band
  and turbo; two laps over eleven sectors (Movie Lounge, Family Gallery, Main
  Hall, Mermaid Pool, Main Hall, bridge, Sky Lagoon and back); all 17 engine
  features, including hazards and a shortcut. Idle: the kart drives itself to
  the finish in about 59 s and earns nothing.
- **Evidence:** remote CI succeeded at `fcee911c` (runs 37186624403 and
  37186622267).
- **Weak points:** no child route; dense (pack, items, hazards, shortcut);
  reused hall art below native resolution. Superseded for integration by V3.

### V5. 3D go-kart (the "galaxy kart", dormant on dev)

- **Where:** `scripts/kart.gd` (3,232 lines, 3D nodes), entered from
  `scripts/main.gd:2024-2140` and `scripts/arena/sky_lagoon.gd`; history on
  `claude/go-kart-mobile-rainbow-track-8gyatx`. Docs `RACE_ENGINE.md`,
  `KART_FEEL.md` (their 3D parts superseded).
- **Play:** vehicle and paint choice, a joystick drag to steer and tap-anywhere
  turbo, seven AI rivals with a gentle rubber band, pickups, ramps, hazards,
  drift, a shortcut, a podium at any place; rewards only after a deliberate
  input. Races of 42 to 61 s. The HUD teaches with text.
- **Status:** 3D migration debt; on dev its vehicles draw as boxes and it has
  no route. Its floating rainbow race still unlocks Galaxy and Butterfly World
  (`scripts/main.gd:2068-2070`, `:2117-2129`), so retiring it needs another
  unlock. The master audit: "Too control-dense and fully spatial for this
  target". It holds the only recorded owner playtests of a racer (July).

### V6. Imp-contest Grand Prix (`codex/opera-imp-contests-20260930`)

- **Where:** tip `66420ae7`; open pull request #17; `scripts/opera_imp_contest.gd`
  (315 lines) implements twelve job contests. Remote CI succeeded at
  `66420ae7` (runs 36815277212 and 36815346523). Its commit also changed
  `.github/workflows/probes.yml`, a high-risk path.
- **Play:** V1 plus a contest rule: the rival's two-lap finish is his win and
  starts a contest-only rematch; one spin at 1.1 laps; he waits while she is
  idle. Its mercy, `maxf(0.75, pow(0.9, rematches))`
  (`scripts/opera_imp_contest.gd:206` on the branch), never drops below three
  quarters of his pace, short of "radically slow down".

### V7. One-circle Racer (stable `master` `ff68f955`, on her device today)

RACE is one finger circle, goal 0.9, "Loop the loop! Draw big racing circles!"
(`ff68f955:scripts/opera_career_world_2d.gd:296`). The master audit called it
the best Opera Racer (2026-08-09); the 2026-09-05 mechanics re-audit rated it
2.3 of 5 ("The finale has no live driving decisions or laps"). Replaced by V1
when the demo build is promoted.

### V8. Earlier Opera racers (history)

The 3D Opera "Racecar" act (2026-07-18 to 07-25), the 2D five-beat Racer
(2026-08-01; "Worst logic mean in the set (2.5)") and "Build F" (2026-08-05),
whose nested 3D lap was praised as "the biggest single wow" and ended by the
true-2D decision and `MA-OPERA-010`.

### V9. Go-Kart Cove (`archive/physics-jolt-cove`, `be6d30e8`)

A Jolt-physics kart racing a turtle on a walled oval; the player holds UP to
drive. Never merged ("duplicates the merged kart game"). 3D.

### V10. The slides (`scripts/games/slide_race.gd`)

(a) The Harper and Fiona fish slide: an 11.5 s Canvas ride with touch-half
steering and five fish; dormant, with no room; gold star 17 of 24 ("One steer
touch with zero fish still completes as a win"). (b) The penguin chase (3D;
beans-only catch). (c) The play-place checkpoint course (3D). None is a kart
race.

## 5. Comparison

| | V1 | V2 | V3 | V4 | V5 | V6 | V7 |
|---|---|---|---|---|---|---|---|
| True 2D | Yes | Planned | Yes | Yes | No | Yes | Yes |
| Built and green | Yes, dev | No | Yes, CI green | Yes, CI green | Dormant | Yes, CI green | Yes, master |
| Steering a child can see | No (19 px) | Lanes | Yes, continuous | Yes, continuous | Joystick | No | No race |
| Holding alone finishes | Yes | Slowest way; the imp beats it | Yes | Drives itself | Drives itself | Yes, but the imp may win | No |
| The imp can win (`DL-INT-14`) | No | Yes | No | No | No | Yes (mild mercy) | No |
| Rivals | One pacer | Imp only | Pack of 8 | Pack of 8 | Pack of 8 | Imp | None |
| Length | About 48 s | About 45 s | About 34 s | 55 to 59 s | 42 to 61 s | About 48 s | One circle |
| Owner record | Rejected 10-17 | Chosen 10-18 | Directed 10-22 (branch) | Commissioned 10-03/04 (branch) | Prioritised for conversion 10-03 | Implements OD-A/B | None |
| New art needed | Already painted | Most | Race-facing room art | Room art | n/a | None | None |

Judgement (Claude's view, not an owner decision), weighed in this order:
owner direction, then child fit, then what is already built:

1. **Owner direction** favours the existing engine: three October statements
   (10-03, 10-17, 10-22) against one default answer (10-18) to a question that
   left it out.
2. **Child fit** favours V2's rules: lanes, holding as the slowest way, a real
   imp who slows right down after two wins, and one rival to watch.
3. **What exists** favours V3: a true-Canvas engine inside the career host, a
   castle-room course, green CI, an idle stop and a probe.

R1 takes each axis's winner. The lane rule is a control layer on V3's road,
not a new engine: published runners such as Subway Surfers and Temple Run use
three lanes behind the runner, and Mario Kart's Smart Steering keeps a young
player's kart on the road ([REFERENCES.md](../codex_minigame_rebuilds_2026-10-17/REFERENCES.md)
section 4).

## 6. The recommended combination R1

| Part | Comes from | What changes | Why |
|---|---|---|---|
| Engine, road view, castle-room course (Movie Lounge, Family Gallery, Royal Bedroom), pickups, zoom strips, ramps, drafting, soft furniture, the 0.9 s seated finish, the career-world ownership of rewards, save and Back | V3 | Merged onto current dev after the demo; nothing else | Owner 2026-10-22 and 2026-10-03; built, true Canvas, CI green |
| Control | V2 | Three lane positions across the road. A tap on the left or right half of the road moves one lane; a drag also works; the kart glides there in about 0.4 s and holds the lane through every curve. The turbo button goes: boosts come from zoom strips, pickups, ramps and the slipstream | Four- and five-year-olds steer poorly; one finger, one decision |
| Driving rule | V2 and V3 | The kart drives while she has touched in the last 3 s (V3 already holds 3 s); a held finger drives but cannot change lane, so it is the slowest way; idle stops after the grace, and 60 s idle earns nothing | Holding must never be the best way (`DL-AGE-05`) |
| Pit stop | V2, with V4's picture cards | Replaces TUNE and TO THE LINE: pick one of three kart colours (remembered); tap two glowing wheel spots and Roshan fits each wheel, counted only after her hand's contact | The chores were the owner's complaint; the job's own act (`MA-PLAY-004`) |
| Rival | V6 logic, V2 tuning | Roshan and the imp only, head to head. If his kart finishes two laps first, a beat of at most 2 s, then the race restarts with every star, pearl and save kept; the first restart keeps his pace; after two of his wins he drives at half speed for the rest of the visit; ties go to her; he moves only while she plays | `DL-INT-14`; OD-E "radically slow down" |
| Finish | V2 | Photo flash, podium, trophy; medals from honest play: bronze for winning, silver without the mercy, gold on the first attempt with at least half the pearls | A job payoff (JL5); gold-star pattern GS-13 |
| Voice | New, after the freeze | Exact lines for the lane instruction, the pit stop, the imp's challenge, lap two, his win and rematch, and her win; "coral gates" retired | `DL-SND-01`; [`MA-ACCESS-004`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-access-004) |
| Art | New, after the freeze, by Codex | Painted race-facing room art for the course (V3's own remaining gap), whole-frame Roshan driving sprites (lean left, lean right, boost, a wave at the finish), the imp's kart and three kart colours from `assets/kart/chase/*`; one room first, then the rest | Owner 2026-10-07: sprites drawn whole; one branch per package (`ODR-JOBART-PROCESS-20261018`) |
| Rules and records | – | Rewrite `DL-INT-10` for R1; record the owner's answer in `owner_decisions.json` with `tools/record_owner_decision.py`, including the 2026-10-22 direction that is today branch-only | One authority |

## 7. R1 acceptance

Machine legs (a new or extended trusted probe, real input, exact Godot 4.7.2):

1. Sixty seconds with no input earns no distance, pearl, finish or star.
2. One tap on either half of the road moves exactly one lane within 0.5 s, and
   the kart holds that lane through every curve of both laps.
3. A held finger without taps: the imp wins attempts one and two; each restart
   begins within 2 s and keeps every star, pearl and save key; on attempt three
   he drives at half speed and she wins.
4. A seeded lane-tapping persona wins the first attempt in at least three of
   four runs.
5. A second finger cannot change lane while the first owns the touch; focus
   loss and Back cancel held input; re-entry restores the pit-stop checkpoint
   and the kart colour (new save keys only, with defaults).
6. No 3D node on the route (gold star C2); no generic fallback line; every
   spoken line true of the scene.
7. Overdraw checks OD1 to OD6 measured on the real route.

Outstanding after the machine legs: frame pacing on the Lenovo Tab M11, one
observed child session, and the owner's verdict. Machine success grants none of
these.

## 8. The alternative R2 (if the owner keeps the side-scroller)

Build V2 as specified in
[RACER.md](../codex_minigame_rebuilds_2026-10-17/RACER.md), and take from the
built versions: V3 and V4's boost, ramp-landing and slipstream behaviour, the
data-driven course-sector table, the epoch-guarded input handling and the
60-second idle probe; the existing side-view kart and moto art
(`widget_crank_racer_kart.png`, `assets/kart/canvas/*` on V4); V6's contest
logic with half-speed mercy; V1's lifecycle code and probe legs.

## 9. What to retire

- V1 when R1 (or R2) lands; keep `scripts/kart_driving.gd` only if R1 uses it.
- V5 as a runtime path, once Galaxy and Butterfly World have another unlock
  (an owner decision outside this packet); keep `KART_FEEL.md` and
  `RACE_ENGINE.md` as feel references.
- V8, V9, V10b and V10c as runtime paths. V10a, the fish slide, is not a race;
  whether it gets a room is a separate question.
- V7 leaves her device when the demo build is promoted.

## 10. Owner questions for the Racer

README Q2 (which direction: R1, R2, or V3 as built with only the contest
added), Q3 (head-to-head, or keep the eight-kart pack with the friend portrait
and book dolls) and Q4 (replace TUNE and TO THE LINE with the pit stop). The
defaults are R1, head-to-head and the pit stop.

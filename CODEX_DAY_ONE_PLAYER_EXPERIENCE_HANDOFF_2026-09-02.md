# Codex handoff — Day One player-experience round (2026-09-02)

Audience: the implementing Codex agent. Authority: this document is
`SUPPORTING_CURRENT` and subordinate to `CLAUDE.md` / `AGENTS.md`,
`design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` (the `DL-*` rules, especially
`DL-AGE-01` through `DL-AGE-08`), and `audit/MASTER_AUDIT_2026-08-09.md`
(canonical audit ledger). Owner decisions win over anything here. The
evidence behind every package is the sixteen-run playthrough bundle in
`audit/day_one_playthroughs_2026-09-02/`.

All line numbers are pinned to integration head `ff68f955` (2026-08-30).
Re-verify at your head before changing anything (Stage 0 below).

## Mission

Make Day One — the fresh-save entry arc (Sky Lagoon → dirty castle →
Bubble Bath → Mermaid Pool → Stuffie Playroom → Craft Room → Grand Puff →
Day Two) — fit a four-year-old's attention, one finger, and non-reading, and
make it impossible to lose. The room activities are already good. What fails
today is everything *between* the rooms: the first pointer of the game leads
out of Day One, no instruction is ever actually spoken, three room
completions end in silence with the next door off-screen, the boss is paced
above her reaction time and cannot be interrupted safely, and the arc ends by
dropping her into the retired 3D reef. Every package below is a bounded,
probe-gated repair of one of those seams; none redesigns a room.

## Method — what this analysis is and is not

- Sixteen independent code-traced playthroughs, one persona each (golden
  path, tap-everything toddler, passive watcher, impatient skipper, door
  explorer, quit-and-resume, sloppy gestures, speedrunner, repeat visitor,
  ears-first, non-reader with no adult, the family phone, boss struggler,
  stuffie lover, little artist, three short sessions). Each run followed the
  shared protocol (`audit/day_one_playthroughs_2026-09-02/PROTOCOL.md`),
  traced the actual input handlers and state machines, and produced a
  beat log, time budget, pros/cons, hazard table and numeric proposals.
- No Godot binary exists in the analysis container, so nothing was executed
  on a device. Every duration is derived from constants, tweens, timers and
  gesture thresholds in the code plus a stated child model (reaction
  1.5–3 s to a new prompt, 0.9–1.6 s to a timed flash, taps 1.0–1.5 s apart,
  50–120 px accuracy, passive spans read as "restless" after 4 s and "taps
  away" after 8–10 s, silence after a prompt tolerated ~5 s). Treat the
  numbers as a model to be confirmed on the Lenovo Tab M11, not as
  measurements.
- Convergence is the evidence of weight: a finding reported independently by
  many runs from different angles is marked with its run count below.
  Proven-by-code claims were re-verified by the author at `ff68f955`; the
  per-run reports separate proven from inferred in their own Confidence
  sections.

## Read before any package

1. `CLAUDE.md` / `AGENTS.md` — no fail states, non-reader objectives must
   fire a voice line *and* a pointer, save keys additive only, protected
   voices, true-2D rule, workflow and branch law.
2. `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` sections on `DL-AGE-*`,
   `DL-SAVE-01`, `DL-QA-02`, `DL-CODE-06`.
3. `audit/MASTER_AUDIT_2026-08-26.md` — the standing findings this round
   leans on: `MA-CI-004` (Day One probes ungated), `MA-CI-005` (passive
   negative test blind to Day One), `MA-SAVE-001` (scratch-owned castle
   progress), `MA-TOUCH-002`.
4. `CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md` — WP-A1 (gate
   the Day One wing) is a prerequisite for every acceptance gate below.
5. `DUST_BUNNY_BOSS_2026-08-02.md`, `BOSS_CONVERGENCE_DECISION_2026-08-02.md`,
   `COMBAT_DIFFICULTY_AUDIT_2026-08-04.md` — the owner's boss contract
   (three rounds of three quick taps, 0.75 s window) that WP-D5 must not
   silently rewrite.
6. `assets/audio/voices/VOICE_MANIFEST.md` and `tools/make_voices.py` — the
   established Roshan voice pipeline WP-D2 extends; `daddy1-3.ogg`,
   `chuck*.ogg` and `voice_yay.mp3` are sacred family recordings.
7. `audit/day_one_playthroughs_2026-09-02/README.md` — the persona matrix
   and the per-finding convergence table, then the individual run whose
   package you are executing.

## Stage 0 — review first (mandatory, per package)

The runs are evidence, not gospel; the code is the truth.

- Re-verify each finding you touch at your current head with the cited
  lines. `dev` may have moved past `ff68f955`.
- If a cited path no longer reproduces, stop, record why in your package
  report, and do not manufacture a change.
- Where a run marks a claim "inferred" (device timings, what the 3D world
  looks like at the post-boss anchor, GUI hit-test ordering), confirm it
  with a headless probe or a device capture before relying on it.

## Day One as she experiences it (typical path, golden run)

| # | Beat | What carries the objective today | Typical s | Attention |
|---|---|---|---|---|
| 1 | Start menu, NEW GAME, scene reload | gold button; no voice | 4 + 3 | G |
| 2 | Sky Lagoon arrival | pulsing ring **on the pearl plane** + "Come on! Let's go!" under "Tap the pearl plane to visit the Reef!"; castle off-screen | 4 | G→R |
| 3 | (likely) reef detour and return | none; the return replays the same plane prompt | 0–90 | R |
| 4 | Walk east to the castle | nothing points at the castle (gate glow idle alpha 0.10) | 30 | G/Y |
| 5 | Main Hall | golden door off-screen right (view 0–1672 of 3344; door at 2540); only moving thing is the elevator ▼; captions hidden | 2 + 13 | Y |
| 6 | Bubble Bath: basket, sink circle, tub tap, tub brush | ghost hand, demos, tool follows finger; voice = "This is so much fun!" | ~30 | G |
| 7 | Pool picture route | framed picture + bobbing ghost hand | 3 | G |
| 8 | Mermaid Pool: skimmer 6, waterfall 3, seahorse 8, Rumi | ☝ rover, chevrons, beads; Rumi's line = pitched "yay" | ~40 | G |
| 9 | Leave the pool | **nothing**; ▼ pointer gone after first elevator use | 12 | Y/R |
| 10 | Playroom: two pins, eagle, picker | star pointer, gold tutorial frame; eagle = chirp | ~20 | G |
| 11 | Leave the playroom | **nothing** | 12 | Y/R |
| 12 | Craft Room: 4 supplies, 3 grime, desk | 👇 pointer, sparkles; 7 × "This is so much fun!" | 18 | G |
| 13 | Attack customizer | **no voice, no pointer**; exit is an unlabeled ✦ | 12 | Y |
| 14 | Find the boss door | **nothing**; Royal Hall off-screen and absent from the elevator | 30–90+ | R |
| 15 | Boss splash + showing | input blocked/ignored 9.6 s; two pitched "yay"s | 10 | Y/R |
| 16 | Three rounds | 0.75 s windows vs 0.9–1.6 s reaction; two guaranteed misses per round; 9.6 s and 8.5 s holds | 65 | G→R |
| 17 | Friends, win, Day Two card | 3.4 s + 4.18 s; then the 3D reef at the castle anchor | 8 | G→R |

Time budget across the runs (New Game tap → Day Two banner):

| Model | min | typical | max | Source |
|---|---|---|---|---|
| Golden path, attentive | 2.6 min | 5.7 min | 15.7 min | run 01 |
| Content only (rooms + boss, no navigation, no boot) | 150 s | 215 s | 380 s | run 16 |
| Realistic with navigation and dawdle | 4.5 min | 7 min | 15 min | run 16 |
| Hard floor, perfect inputs | 80 s (boss 44.8 s = 59 %) | 153 s | 235 s | run 08 |
| Forced wait vs agency, typical | 79 s forced / 120 s agency; pre-boss 15 s forced of 132 s; boss 64 s forced of 67 s | | | run 04 |
| Re-entry tax per Continue | 15 s | 30 s | 60 s | runs 06, 16 |
| Boss, tired child (1.5–3 s reaction) | 45 s | 78 s | 125 s | run 13 |

The fit verdict (run 16): two sittings are comfortable, three are right
only because every Continue costs 25–45 s of unguided re-entry and the boss
must not be interrupted; four are never needed. Inside the rooms the
agency-to-passive ratio is 3–12 : 1; in the boss it is 1.2 : 1, and about
20 of the boss's 44 "agency" seconds are windows she physically cannot hit.

## Pros — what already works for a four-year-old (keep it)

- **Every room activity is a wordless, one-finger, no-fail loop with a
  pointer and a demo.** Basket ghost hand, sponge/brush travelling demos,
  ☝ rover, lane chevrons, seahorse beads, playroom star, art 👇, picker gold
  frame stepping part → colour → heart. The stuffie picker is the
  best-taught screen in the game (`scripts/companion.gd:830-872`).
- **Targets are child-sized where it matters.** Basket 220², pool picture
  205×190, elevator 136², bunny cards ≈166 px, TAKE ALONG 330×150, seahorse
  accepts a tap anywhere on screen, skimmer catch radius 118 px.
- **Nothing punishes her.** Blocked doors answer with swish + flutter,
  boss taps outside the window poof and giggle, wrong lanes and random taps
  still progress, bumps only tune replay stars. Zero input never wins
  (bathroom counters need live motion, boss free taps ≤ 2 of 3).
- **Room progress is honest.** Bathroom, pool, playroom and art restore to
  the exact step with voice and pointer re-fired within 2–3 s; pins are
  written synchronously; `normalise_save_patch` heals partial saves in her
  favour; backgrounding flushes the 1.5 s debounce.
- **Immediate cause and effect everywhere she touches**: pops, catches,
  tugs, sparkles, a room that visibly brightens, a bunny that shouts "NO!",
  Rumi rising, the eagle flying free, Grand Puff's dizzy orbit.
- **The elevator picture map with one gold card** is a real non-reader
  route and a legal two-tap shortcut through the first three rooms.
- **Music marks every place** and the two genuine celebrations (stuffie
  confirm, boss win) have a real fanfare.
- **Grand Puff is genuinely unlosable**, the tell is picture-first (gold
  strobe + halo + 👆 + button flip), and the tap ladder gives a wordless
  1-2-3.

## Cons — what works against her (grouped, with run convergence)

1. **The first pointer of the game leads out of Day One** (13 of 16 runs).
   `first_session` is forced false before the promenade builds
   (`scripts/main.gd:3975`), so `build()` skips the pending branch and calls
   `_show_reef_route_guidance()` (`scripts/arena/sky_lagoon_promenade.gd:266-269`,
   `1077-1083`): the only focused object is the pearl plane, the only spoken
   line is "Come on! Let's go!", kind `"reef"` activates on the *first* tap
   (`:333-336`) and `_exit_level2` has no Day One guard (`main.gd:8440-8452`).
   The castle is off-screen at spawn x 610 and its gate glow idles at alpha
   0.10. Every return through the reef portal, and every Continue, replays
   the same prompt. From the reef, the Dusty Attic portal is not gated on
   Day One either, and a win there calls `day_one_complete_boss_and_begin_day_two()`
   with zero rooms cleaned (`main.gd:5373-5374`, `10004-10007`;
   `scripts/day_one_director.gd:439-447`).
2. **No Day One instruction is ever spoken** (16 of 16). `_say` resolves
   `<speaker>_<event>.ogg` → `<speaker>.ogg` → pitched `voice_yay.mp3`
   (`scripts/audio_director.gd:13-47`). Every objective passes `"talk"`, which
   is `roshan_talk.ogg` = "This is so much fun!" (`tools/make_voices.py:47`,
   1.05 s); `"win"` = "Yay! I did it!". No `roshan.ogg`, `daddy.ogg`,
   `rumi.ogg`, `roshan_home/hint/intro`, `roshan_dustboss_*` or
   `roshan_day_two_begins` exists, so every Pearl Castle, Daddy Mermaid,
   Rumi, boss and Day Two line is a wordless "yay". The blocked-door answer
   is "yay" followed by "This is so much fun!". The tub-drain success plays
   `wacky_fail` "Ho ho! Chuck got all wet! Try again!" (2.85 s). The sink
   instruction's voice is eaten by the 0.5/0.8 s `min_gap` because the
   sponge travel is 0.38 s (`scripts/games/day_one_bathroom_cleaning.gd:583,
   599, 811-816`).
3. **Captions are invisible for the whole castle** (7 of 16). `hud_msg` is a
   child of `hud_layer` (`main.gd:3590, 3617`); the castle hides that layer
   on open and resume and restores it only on close
   (`scripts/arena/castle_rooms_25d.gd:967-968, 993, 1116`). Text was never a
   carrier for the child, but it was the adult's fallback and it is gone
   too. Run 11's inventory: 51 text carriers in Day One, 13 fully backed by
   a non-text channel, 22 partial, 12 text-only, 4 inert.
4. **Three silent hand-offs and an off-screen door** (14 of 16). After the
   pool (`main.gd:7304-7320`), the playroom (`7322-7333`) and the art room
   (`7273-7284`) nothing speaks, glows in reach or points. The authored line
   "All four rooms are clean! The big back door is glowing!" lives only in
   the placeholder branch (`main.gd:7180-7190`) that the four real rooms
   return before (`7150-7170`). On every hall entry Roshan spawns at foot
   x 380 with the view at 0–1672 while the Day One doors sit at 1940–2700
   and the Royal Hall at 2870–3220 (`castle_rooms_25d.gd:2318-2323`,
   `152-191`); the Royal Hall has no elevator card (`:296-305`); the
   elevator's bobbing ▼ is hidden the first time the menu opens and never
   restored (`:1732-1736`). Run 16's attention reservoir hits zero at
   roughly +20 s in each of these lulls.
5. **The bathroom gestures are a motor-skill wall for a finger-lifter**
   (4 of 16). Sink and tub need ≥ 2.0 s of *moving frames inside one
   touch*; `probe_begin_gesture` zeroes `_valid_motion_seconds` on every
   touch-down (`day_one_bathroom_cleaning.gd:299`, gates `:494-496`,
   `:511-513`, accrual `:356-357`). Arc, distance and reversals bank across
   lifts; time does not. The grime alpha is `0.72 × (1 − min(arc, dist,
   time))` (`:834-857`), so the fixture visibly re-dirties on every re-touch;
   the `_progress` bar is declared but never built (`:110, 819-831`); the
   5.0 s maximums are never enforced. A press that lands during the three
   busy windows (0.38 / 0.70 / 1.04 s) is dropped and every drag after it is
   ignored until she lifts (`:285-287, 305-307, 449-450`).
6. **Grand Puff is paced above her and cannot be interrupted safely**
   (11 of 16 for the strand, 9 for the pacing). The trigger writes
   `giant_dust_bunny_boss_triggered = true`
   *before* the fight (`main.gd:7794-7798`); restore keeps it
   (`day_one_director.gd:612-613`); `day_one_boss_door_ready()` and
   `_day_one_arm_boss_door()` then refuse forever (`main.gd:7069-7072,
   7761-7766`); the Royal Hall resolves BLOCKED. A phone call, a low-memory
   kill or pause → Leave during the 45–125 s fight strands Day One with
   jobs and Opera locked; the only exit is the unpointed reef attic. Inside
   the fight: 0.75 s / 0.65 s three-tap windows against a 0.9–1.6 s reaction
   mean two guaranteed misses per round; the gentle assist (window +4.0 s)
   arrives at streak 2 and is thrown away each round because
   `_on_round_done` zeroes the streak it derives from
   (`scripts/games/dust_boss.gd:92, 1176-1177`); after each landed round she
   sits 9.6 s / 8.5 s (`STRUCK 1.8 + DIZZY 3.2/ANGRY 2.1 + PHASE_BEAT 2.8 +
   CELEBRATION 1.8`, `:61-66, 573-574`) with taps answered only by sparkles;
   splash + showing is 9.64 s of blocked input; every expired window plays
   the kit's ANGRY puff (`scripts/dust_bunny_boss_sprite.gd:239-243`); the
   mastery card removes stars live on bumps she cannot avoid while rooted
   (`dust_boss.gd:1017-1034`); the 💜 round pips never render because
   `hud_game` is forced hidden every frame (`main.gd:9741-9744`); shielded
   taps get a cheerful "yay" every 2.6 s (`:718-722`).
7. **Day One ends in the wrong world** (9 of 16). `_end_game` has no Dusty
   Attic branch, so `_leave_arena_now` puts her at `return_pos`
   (`main.gd:9003-9046, 11066-11073`), captured by `_enter_arena`
   (`:10944`) as the castle-interior anchor `CASTLE_POS + (0, 6, 24)`
   (`:6840`) in reef mode with `game == ""`, the castle closed and the
   promenade torn down; a fresh save has no portal back
   (`:5632-5637`). Only an app restart → Continue (now the legacy route)
   recovers. The Day Two banner is overwritten in-frame and the medal card
   sits under the 4.18 s transition.
8. **Save and start-menu routing** (runs 06, 12, 16). Any real on-disk
   save is normalised at load with `day_one_active` defaulting to true and
   the primary file is rewritten before the first tap
   (`scripts/save_state.gd:426-441, 526-531, 80-87`;
   `day_one_director.gd:597-598`), so an old family save enters Day One
   with jobs and Opera locked, contrary to the comments at
   `scripts/start_menu.gd:241-242` and `main.gd:3967-3969`;
   `probe_start_menu_routing.gd` cannot see it because it feeds a raw dict.
   NEW GAME is a gold button, its confirm is a same-style gold button 168 px
   above it with focus pre-placed on it and no voice or pointer
   (`start_menu.gd:201-235, 256-264`); the `.before_new_game` archive has
   no restore path in-game, in `backup.sh` or `BACKUP.md`. Every Continue
   lands at the lagoon plane, never the room she left. Two 0.58 s windows
   in the pool can save the skimmer/seahorse mask complete with the old
   step; both activities then restore as `_completed` without emitting
   `completed` (only the waterfall re-emits: `pool_waterfall_activity.gd:86-87`
   vs `pool_skimmer_activity.gd:92-100`, `pool_seahorse_rescue_activity.gd:100-106`).
9. **Stuffie room and art room payoffs vanish** (runs 09, 14, 15). Closing
   the picker (its ↩ is the glyph she has used all day) or an app kill
   before the heart makes the adoption unreachable until Day Two because
   `day_one_activate_castle_room` answers "sparkly clean" before the
   `"stuffies"` branch (`main.gd:7145-7148`; `castle_rooms_25d.gd:4763-4786`);
   the adopted eagle is invisible in the castle (`companion.gd:192-196,
   242-246`). In the art room, collecting the brushes or blue paint calls
   `_activate_room_item("paint_table")` whose `launch_activity: "castle_logo"`
   opens the full-screen Castle Logo Studio 1.44 s later, twice, with no
   Day One gate (`scripts/day_one_art_studio.gd:291-297`;
   `castle_rooms_25d.gd:498-501, 3672-3680`). The attack customizer is a
   layer-18 modal with no voice, no pointer and only an unlabeled ✦ exit
   (`scripts/attack_customizer.gd:99-121, 182-193, 257-261`), and the
   chosen colour/effect is never used by the boss that follows (zero
   references in `dust_boss.gd`, `dust_bunny_boss_sprite.gd`,
   `boss_splash_2d.gd`, `octagon_stage.gd`; only `combat_arena.gd:478-500`
   consumes it).
10. **Revisit friction** (runs 05, 09). The completed-room action button
    fires "This room is sparkly clean!" plus two overlapping Roshan clips on
    every tap (`main.gd:7145-7148`); the completed bathroom hides back and
    elevator on every re-entry and re-fires the pool picture line
    (`main.gd:7385-7396, 7640-7675, 7704-7726`); Rumi is freed on room
    change and `day_one_pool_rumi_met` is read by nothing; blocked room
    doors have no SFX cooldown (only the Royal Hall has 2.8 s); the pause
    sheet's "🌊 REEF" tile drops her into the ocean from anywhere in the
    castle.

## Findings register

Severity follows the canonical scale (P1 = strands, misroutes or silences
a required objective for the child; P2 = confuses or costs attention; P3 =
polish). "Runs" is the number of independent runs that reported it.

| ID | Sev | Finding | Runs | Rule | Evidence |
|---|---|---|---|---|---|
| DO-01 | P1 | Arrival guidance focuses the reef plane; one tap exits Day One; return and Continue replay it; castle has no pointer | 13 | `DL-AGE-01` | `main.gd:3975`; `sky_lagoon_promenade.gd:261-269, 333-336, 801-804, 1077-1083`; `main.gd:8440-8452` |
| DO-02 | P1 | Reef Dusty Attic portal ungated; win ends Day One with rooms incomplete | 3 | `DL-AGE-03` | `main.gd:5373-5374, 5491-5493, 10004-10007`; `day_one_director.gd:439-447` |
| DO-03 | P1 | No objective clip exists; every `_say` is "This is so much fun!", "Yay! I did it!" or a pitched "yay" | 16 | `DL-AGE-01` | `audio_director.gd:13-47`; `tools/make_voices.py:47, 58`; `assets/audio/voices/` |
| DO-04 | P1 | Castle hides `hud_layer`, so every banner in the hall, four rooms and picker is invisible | 7 | `DL-AGE-01` | `castle_rooms_25d.gd:967-968, 993, 1116`; `main.gd:3590, 3617` |
| DO-05 | P1 | Pool, playroom and art completions fire no voice/pointer; boss-door line unreachable; Royal Hall not on the elevator | 14 | `DL-AGE-01` | `main.gd:7150-7190, 7273-7284, 7304-7333, 7792-7793`; `castle_rooms_25d.gd:296-305` |
| DO-06 | P1 | Golden door off-screen on every hall entry; elevator ▼ hidden forever after first open | 12 | `DL-AGE-01` | `castle_rooms_25d.gd:152-191, 1732-1736, 2318-2323` |
| DO-07 | P1 | Boss-triggered flag saved before the fight; interruption strands Day One | 11 | `DL-AGE-03`, `DL-AGE-06` | `main.gd:7069-7072, 7761-7766, 7794-7798`; `day_one_director.gd:612-613`; `castle_door_language.gd:47-48` |
| DO-08 | P1 | Sink/tub motion clock resets per touch; grime re-dirties; no progress bar; busy windows drop presses | 4 | `DL-AGE-02`, `DL-AGE-05` | `day_one_bathroom_cleaning.gd:285-307, 356-357, 449-450, 494-513, 834-857` |
| DO-09 | P1 | Post-boss landing is the 3D reef at the castle anchor with no way back on a fresh save | 9 | `DL-AGE-06` | `main.gd:9003-9046, 10944, 11066-11073, 6840, 5632-5637` |
| DO-10 | P1 | Legacy saves are normalised into Day One at load and rewritten on disk | 1 (12) | `DL-SAVE-01` | `save_state.gd:426-441, 526-531, 80-87`; `day_one_director.gd:597-598`; `start_menu.gd:19-21, 243` |
| DO-11 | P1 | NEW GAME is a two-tap, text-only, gold-then-gold wipe with no in-game restore | 5 | `DL-AGE-01`, `DL-AGE-03` | `start_menu.gd:201-235, 256-275`; `save_state.gd:285-316`; `backup.sh:64-68` |
| DO-12 | P2 | Boss windows 0.75/0.65 s vs child reaction; assist reset per round; 9.6/8.5 s holds; angry puff on expiry; live star loss; hidden pips; "yay" on shielded taps | 9 | `DL-AGE-04`, `DL-AGE-05` | `dust_boss.gd:61-68, 92, 573-574, 718-722, 1017-1034, 1176-1177`; `dust_bunny_boss_sprite.gd:20-22, 239-243`; `main.gd:9741-9744` |
| DO-13 | P2 | Continue always lands at the lagoon plane; 25–45 s re-entry tax per sitting | 3 | `DL-AGE-06` | `main.gd:3966-3972, 5748` |
| DO-14 | P2 | Stuffie picker unreachable after close/kill in Day One; adopted companion invisible in the castle | 4 | `DL-AGE-03` | `main.gd:7145-7148`; `castle_rooms_25d.gd:4763-4786`; `companion.gd:192-196, 242-246` |
| DO-15 | P2 | Art tutorial taps launch the Castle Logo Studio twice, unprobed | 2 | `DL-AGE-02` | `day_one_art_studio.gd:291-297`; `castle_rooms_25d.gd:498-501, 3672-3680` |
| DO-16 | P2 | Attack customizer: no voice, no pointer, modal above castle controls, ✦-only exit; choice unused by the boss | 6 | `DL-AGE-01` | `attack_customizer.gd:99-121, 182-193, 257-261`; `main.gd:6994-7003` |
| DO-17 | P2 | Tub-drain success voiced by `wacky_fail` "…Try again!"; sink line silenced by `min_gap`; eight clip collisions | 9 | `DL-AGE-01` | `day_one_bathroom_cleaning.gd:583, 599, 669-670, 811-816`; `audio_director.gd:15-19, 37-47, 169-173` |
| DO-18 | P2 | Skimmer/seahorse restore as complete without emitting `completed` (0.58 s save windows) | 1 (16) | `DL-AGE-03` | `pool_skimmer_activity.gd:92-100`; `pool_seahorse_rescue_activity.gd:100-106`; `day_one_pool_cleanup.gd:320-325, 354-360` |
| DO-19 | P2 | Completed-room button spams banner + two clips; completed bathroom is a one-way room; Rumi is a one-shot | 3 | `DL-AGE-06` | `main.gd:7145-7148, 7385-7396, 7640-7675, 7704-7726`; `day_one_pool_cleanup.gd:83-100` |
| DO-20 | P2 | Pause "🌊 REEF" tile exits the castle to the ocean during Day One | 3 | `DL-AGE-06` | `pause_menu.gd:141-143, 261-262` |
| DO-21 | P3 | Blocked room doors have no SFX cooldown; two banners collide on hall entry; "Tap the loose loose brushes!" | 6 | — | `castle_rooms_25d.gd:1695-1718`; `main.gd:6845-6860, 7784-7785`; `day_one_art_studio.gd:8, 380` |
| DO-22 | P3 | Debounce starvation: rapid taps keep resetting the 1.5 s save timer | 2 | `DL-SAVE-01` | `main.gd:3983-3988, 9727-9734` |
| DO-23 | P3 | Leftover 3D magnitudes in 2D tweens (pointer bob 0.28 px, eagle lift +1.25 px); companion still `Node3D`/`Sprite3D` | 1 (14) | true-2D rule | `castle_rooms_25d.gd:4186-4193, 4228-4229`; `companion.gd:128-187` |

## The attention-budget contract (targets every package is measured against)

| Target | Value | Why |
|---|---|---|
| Objective → voice that *says it* → pointer | within 1.0 s of the objective appearing, every time, including after room completion | `DL-AGE-01`; today the pointer exists in rooms but the voice never does |
| Longest span with input blocked or ignored | ≤ 6 s (boss ceremonies included) | passive >8–10 s = she taps away; today 9.64, 9.6, 8.5 s |
| Silence after a prompt while input is expected | ≤ 5 s, then a re-prompt (voice + pointer pulse), repeated at 12 s, cap 3 | the passive watcher sits 10–20 s before acting |
| Re-orientation on Continue | the current room's own prompt within 10 s of tapping CONTINUE | today 25–45 s and the wrong prompt |
| Any stop, anywhere | loses at most the current gesture; never a story gate | `DL-AGE-06`; today the boss is a one-way door |
| Boss fight, typical child | 45–90 s from splash to friends, no forced hold > 6 s, first landed hit by the second window | run 13 measured 78 s with two certain misses per round |
| Per-room content | 30–120 s of agency; ≥ 3 : 1 agency-to-passive | the rooms already meet this; keep it |
| Whole arc, realistic | fits two sittings of ≤ 8 min with a safe stop after every room | run 16 |

## Work packages

Branch law: one package per branch, `codex/<topic>` off fresh `origin/dev`,
merge to dev only with the full probe suite green on CI for the exact head,
never touch `master`. Smallest truthful change per package; no bundled
redesign; save keys additive with defaults; if a trusted probe fails after a
step, revert the step, never patch the probe (`DL-CODE-06`, `DL-QA-02`).
Every package that adds a child-facing objective adds a voice key from
WP-D2's list and a pointer, and extends or adds a probe leg (WP-D9).

### WP-D1 — Entry and re-entry routing (DO-01, DO-02, DO-06, DO-13, DO-20)

Scope: `scripts/arena/sky_lagoon_promenade.gd` `build()` / guidance /
`handle_touch` / `_activate`; `scripts/main.gd` `_launch_from_start_menu`,
`_exit_level2*`, the reef attic item and proximity start;
`scripts/arena/castle_rooms_25d.gd` hall spawn and elevator pointer;
`scripts/pause_menu.gd` tiles; `scripts/day_one_director.gd` one additive
key.

Do:
1. While `m.day_one_is_active()`, `build()` must not call
   `_show_reef_route_guidance()`. Focus `castle_gate` instead, raise its idle
   cue alpha from 0.10 to ≥ 0.45 with the standard pulse, and speak
   `roshan_day1_castle` ("Let's go to the castle!"). Spawn New Game at
   master x 4520 (the existing from-castle spawn) so the gate is on-screen;
   keep the plane card but let it read as scenery.
2. During Day One a tap on any `"reef"` target (plane, marker, FLY bubble)
   answers with the blocked-door language (cue pulse + swish +
   `roshan_day1_castle`) and does not call `_exit_level2()`. Gate
   `_exit_level2_now`, the Dusty Attic reef item, its proximity start and
   the pause "🌊 REEF" tile on `not day_one_is_active()`. Make
   `complete_day_one_after_boss()` require `boss_door_glow` as well as
   `day_one_active` so no side entrance can end Day One early.
3. Continue re-enters where she was: add additive key
   `day_one_resume_castle_room` (default `""`), written by `show_room()` while
   Day One is active and cleared on Day Two. `_launch_from_start_menu(true)`
   routes to `_enter_castle_interior_now()` + `show_room(resume_room)` when
   `dirty_castle_discovered` is true; otherwise to the WP-D1 lagoon spawn.
4. Hall entry during Day One places the hall view so the active PLOT door is
   on-screen: set the spawn foot to `active_door_foot.x − 600` (clamped) and
   the initial `_hall_view_left_art` accordingly, instead of the fixed
   `(380, 835)`. Re-show `ElevatorPointer` whenever the elevator closes and
   whenever `day_one_current_room_id` changes; retarget its bob to sit over
   the elevator only while no PLOT door is on-screen.

Don't: remove the plane, change Sky Lagoon outside Day One, or touch the
arrival-plane media hook (cinematic pipeline territory).

Gate: `probe_start_menu_routing` gains a leg that boots the promenade with a
fresh Day One save and asserts the focused target is `castle_gate`, a
simulated tap on the plane does not change `m.game`, and the reef attic item
refuses while Day One is active; `probe_day_one_integration` asserts Continue
with `day_one_resume_castle_room = "mermaid_pool"` opens the pool; a hall
probe asserts the PLOT door rect intersects the view rect on entry for each
of the four rooms and the Royal Hall. Suite green.

### WP-D2 — Say the instruction (DO-03, DO-04, DO-17)

Scope: `tools/make_voices.py` LINES table and its bounded `--line`
regeneration; new `assets/audio/voices/roshan_day1_*.ogg` (Kokoro, the
existing Roshan voice, same loudness pipeline); the Day One call sites;
`scripts/audio_director.gd` voice arbitration; a castle caption mirror.

Do:
1. Add the clips in Appendix B with exact keys, generate them with
   `tools/make_voices.py --line <key>` only, add each to
   `ASSET_LICENSES.md` and rebuild `audit/audio_quality_ledger_2026-08-24.csv`
   with `tools/audit_audio_quality.py`. Never regenerate an existing clip.
2. Replace every Day One `show_msg(..., "talk")` / `_say("roshan","talk")`
   objective call with its bespoke key (Appendix B lists every site). Drop the
   trailing generic `_say("roshan","talk", 0.8)` calls that today only add
   collisions.
3. Route lines whose speaker has no recorded voice through Roshan with a
   Roshan clip: Pearl Castle room names → no voice (music already marks the
   room) or `roshan_day1_room_<id>`; Daddy Mermaid hints → `roshan_day1_resting`
   ("That door is resting. Follow the golden door!"); Rumi's thank-you →
   `roshan_day1_rumi` ("You saved the pool! This is Rumi!"); Baby Eagle keeps
   its chirp but the objective is spoken by Roshan (`roshan_day1_bump_bunnies`).
   **Do not synthesize a Daddy voice**: `daddy*.ogg` are sacred family
   recordings and a synthetic Daddy is an owner decision (see Escalation).
4. Fix the two audio bugs: the sink announce must use a distinct key with
   `min_gap 0` (it fires 0.38 s after the basket line); the tub-drain reaction
   must not play `wacky_fail` — use the new `roshan_day1_bunny_no` or a short
   bunny SFX, and delay the "brush the tub" line until the reaction clip ends.
5. Serialize voice: `show_msg`'s fallback "yay" must not start while any pool
   player is audible, and `talk`/`win` share one Roshan cooldown ≥ 1.2 s
   (`audio_director.gd:37-47, 169-173`), so the one line she gets is heard.
6. Mirror the caption inside the castle: give `castle_room_stage` a
   `HudVoiceCaption`-styled label on the castle layer that shows the current
   `show_msg` text while `hud_layer` is hidden (an adult fallback, never the
   child's only channel).

Gate: a new `probe_day_one_voice.gd` walks every Day One objective site,
resolves the key the way `_say` does, and fails if any objective resolves to
`roshan_talk.ogg`, `roshan_win.ogg` or the `voice_yay.mp3` fallback; asserts
no two Roshan clips start in the same frame at the basket, desk and win
sites; `probe_day_one_bathroom_cleanup` asserts the sink announce is not
suppressed. Suite green; the audio ledger regenerates clean.

### WP-D3 — Hand-offs between rooms and to the boss door (DO-05, DO-06)

Scope: `scripts/main.gd` `day_one_complete_pool_scene`,
`day_one_complete_stuffie_rescue`, `day_one_complete_art_scene`,
`_on_day_one_hook_event` (`EVENT_BOSS_DOOR_GLOW`), `_show_day_one_pool_route`
generalised; `scripts/arena/castle_rooms_25d.gd` elevator cards and
`refresh_door_states`.

Do:
1. On every room completion fire `_fanfare()`, the next-step line
   (`roshan_day1_next_door`, or `roshan_day1_back_door` after art — the text
   already exists at `main.gd:7182-7186`, move it out of the placeholder
   branch) and a route picture button for the next PLOT door, reusing the
   bathroom's `_show_day_one_pool_route` pattern with the target room and
   preview texture parameterised (pool → playroom, playroom → craft room,
   craft room → Royal Hall). The picture is the pointer; keep the ghost hand.
2. Add a Royal Hall card to the elevator book that appears only while
   `day_one_boss_door_ready()` and wears the PLOT cue; keep the ▼ pointer
   alive (WP-D1 item 4).
3. Keep `castle_room_action_button` visible after art completion with a
   single "next door" answer instead of the hidden button.

Gate: a probe leg completes each room through the director and asserts,
within one frame, that a voice key from Appendix B fired, a node with meta
`visual_pointer` exists on the castle stage, and the next PLOT door or its
route button intersects the view rect; `probe_passive` gains the Day One
snapshot legs so the new rewards cannot be awarded idle (`MA-CI-005`).
Suite green.

### WP-D4 — Bathroom gesture forgiveness (DO-08, DO-17)

Scope: `scripts/games/day_one_bathroom_cleaning.gd` only (plus its probe).

Do:
1. Bank the motion clock across lifts: stop zeroing `_valid_motion_seconds`
   in `probe_begin_gesture`; decay it only after ≥ 3.0 s with no touch; keep
   the live-motion requirement so a still finger or passive time still
   cannot win. Lower `SINK_MIN_GESTURE_SECONDS` and `TUB_MIN_GESTURE_SECONDS`
   from 2.0 to 1.5. Count tub motion on any move > 1 px, not only when
   accumulated |Δx| crosses 2 px.
2. Make progress monotonic and visible: drive the grime alpha from
   `max_so_far(min(arc, dist))` (drop the time term from the visual), build
   the declared `_progress` bar or delete its dead code.
3. Buffer a press that arrives during a busy window (sponge travel 0.38 s,
   sponge-return + brush 0.70 s, drain 1.04 s) and start the gesture when
   busy clears; shorten tool travel 0.38 → 0.22 s and the post-drain timer
   0.36 → 0.20 s.
4. Add a 12 s idle re-prompt per stage: replay the stage's voice key and
   pulse the ghost hand (cap 3).
5. Fire child-facing Buttons on press (`ACTION_MODE_BUTTON_PRESS`) for the
   basket, the pool picture and — in WP-D7 — the art targets and the
   customizer, so a 120 px drag that starts on the target counts.

Gate: `probe_day_one_bathroom_cleanup` gains legs proving (a) three 0.8 s
touches with 0.5 s lifts complete the sink where one continuous touch was
required before, (b) grime alpha never increases between two samples, (c) a
press during a busy window starts the gesture on release of busy, (d) a
zero-input wait still never completes (existing negative leg unchanged).
Suite green.

### WP-D5 — Grand Puff pacing and resumability (DO-07, DO-09, DO-12)

Scope: `scripts/main.gd` `_on_day_one_hook_event`, `day_one_boss_door_ready`,
`_day_one_arm_boss_door`, `_end_game`/`_leave_arena_now` Dusty Attic branch,
`_show_day_two_transition`; `scripts/day_one_director.gd`
`normalise_save_patch`; `scripts/games/dust_boss.gd` constants and assist
bookkeeping; `scripts/dust_bunny_boss_sprite.gd` expiry animation;
`scripts/medal_system.gd` presentation only.

Do:
1. Never strand the door: do not persist `giant_dust_bunny_boss_triggered`
   before the fight (write it from `complete_day_one_after_boss()`), and
   treat a restored `triggered` flag as untriggered while `day_one_active`
   is still true so `_day_one_arm_boss_door` re-arms; pause → Leave during
   the fight returns to the castle hall with the door glowing.
2. End Day One in the castle: in `_end_game` for `fname == "Dusty Attic"`
   when `g["day_two_started"]` was just set, return via `_enter_level2(true)`
   then `_enter_castle_interior()` (the Rainbow Slide / Fairy Pond pattern),
   play the Day Two transition over the hall, and speak
   `roshan_day1_day_two` after the transition, not under it. Show the medal
   card after the transition.
3. Pace the opening and the holds within the owner's contract: keep the
   three-tap 0.75/0.65 s windows, but set `PREASSIST_TRIGGER_STREAK 2 → 1`,
   persist the pre-assist tier for the rest of the encounter (store
   `db_preassist_tier = max(...)` instead of deriving it from a streak that
   `_on_round_done` zeroes), and give the first window of round 1 the tier-1
   window (+2.0 s) so a first landed hit is possible by window two.
   `DIZZY_T 3.2 → 1.6`, `ANGRY_T 2.1 → 1.4`, `PHASE_BEAT_T 2.8 → 1.2`,
   `CELEBRATION_BEAT_T 1.8 → 1.0` (holds 9.6/8.5 s → 5.6/4.4 s). Let a tap
   end the showing once the demo flash has played (`st ≥ 5.2`). Set
   `POSITIVE_PACING_FLOOR 38 → 26` or anchor it at the first accepted input.
4. Stop it reading as losing: play `play_jump()` instead of `play_angry()` on
   an expired window; keep the mastery stars static during the fight and
   reveal the bump tier only on the medal card; render three tap pips for
   the current window on a castle/boss layer that `main.gd` does not hide;
   silence the "yay" on shielded taps (banner only, cooldown 2.6 → 6.0 s,
   soft poof SFX).
5. Record the boss and Day Two lines (Appendix B) so the tell is spoken.

Don't: change `VULNERABILITY_WINDOW` / `FINAL_WINDOW` or the three-taps rule
without the owner decision flagged below; touch the boss art.

Gate: `probe_day_one_director` asserts a save with all rooms complete,
`day_one_active` true and `triggered` true restores with the door armed;
`probe_dust_boss_balance` re-run shows the fight band 45–120 s for its
slow-bot with no forced hold > 6 s and a first hit no later than window 2 in
≥ 90 % of runs; `probe_dust_boss` asserts the post-win state is the castle
hall with `day_one_active` false; `probe_passive` boss leg unchanged (zero
input never wins). Suite green.

### WP-D6 — Save and start-menu safety (DO-10, DO-11, DO-18, DO-22)

Scope: `scripts/save_state.gd` candidate read; `scripts/start_menu.gd`
confirm sheet and options; `scripts/day_one_director.gd`
`normalise_save_patch` default; `scripts/games/pool_skimmer_activity.gd`,
`pool_seahorse_rescue_activity.gd` `start()`; `scripts/main.gd` debounce;
`backup.sh`, `BACKUP.md` (documentation only).

Do:
1. Legacy decision made explicit: capture `raw.has("day_one_active")` in
   `_read_save_candidate` (`result["day_one_declared"]`) and have
   `continue_day_one_mode` use the declared value; a save that carries
   progress (`plays ≥ 1` or `level2` true) without the namespace defaults
   `day_one_active` to false. Add a probe fixture that round-trips a legacy
   dict through `SaveState`, not the static helper. **Confirm the intended
   policy with the owner first (Escalation).**
2. Child-proof NEW GAME: when a save exists style CONTINUE gold and NEW GAME
   secondary; in the confirm sheet focus and gold-style KEEP GAME, style
   START NEW secondary, disable START NEW for 1.5 s after the sheet opens and
   require a 0.8 s press-and-hold; speak `roshan_day1_keep_game` with a ghost
   hand on KEEP GAME. Add a grown-up restore (long-press OPTIONS 3 s → swap
   `reef_save.json.before_new_game` back through `_commit_save`); pull the
   archive in `backup.sh`; document both in `BACKUP.md`.
3. `start()` in the skimmer and seahorse activities emits `completed` once
   when `_completed` is already true, mirroring the waterfall.
4. Cap debounce starvation: keep the 1.5 s idle write but force a write once
   `save_pending` has been true for > 4.0 s.

Gate: `probe_start_menu_routing` legacy leg goes through `SaveState` and
asserts the direct route; `probe_save_recovery` asserts the `.before_new_game`
restore; `probe_day_one_pool_cleanup` asserts a restored complete mask emits
`completed` and the pool can finish; `probe_load` asserts the > 4.0 s forced
write. Suite green.

### WP-D7 — Stuffie room and art room payoffs (DO-14, DO-15, DO-16, DO-23)

Scope: `scripts/main.gd` `day_one_activate_castle_room` stuffie/art
branches; `scripts/arena/castle_rooms_25d.gd` `_restore_playroom_rescue_clears`,
`_activate_room_item` launch gate, playroom tweens; `scripts/companion.gd`
castle presence (2D only); `scripts/day_one_art_studio.gd` station
animation and hit boxes; `scripts/attack_customizer.gd` cue and pointer;
`scripts/games/dust_boss.gd` hit feedback.

Do:
1. Re-arm the adoption while Day One is active: before the "sparkly clean"
   reply, if `logical_room == "stuffie"` and `companion_id == ""`, open
   `_open_playroom_stuffie_tutorial()`; also call it from
   `_restore_playroom_rescue_clears` on re-entry. Hide the picker's ↩ during
   the rescue tutorial and shrink the dim-close to nothing.
2. Show the friend she just adopted: stage a `Sprite2D` cutout of the
   companion on `castle_room_item_visual_layer` beside Roshan (positioned in
   `_position_player_at_foot`) and keep the 🧸 badge on the castle stage. This
   is new true-2D work; do not extend the `Node3D`/`Sprite3D` follower.
3. Art room: `_animate_storage_station` must not call `_activate_room_item`;
   play the station atlas via the fixture rig without `launch_activity`, and
   gate `launch_activity == "castle_logo"` on `not day_one_jobs_locked()`.
   Grow the hit boxes: bottles 92×104 → 128×128, brushes/cups 124×104 →
   150×128, grime → 150×110 (art px). Fire the art Buttons on press.
4. Customizer: on `open()` speak `roshan_day1_pick_colour` and show a
   pulsing 👇 over the ✦ (park it there after 4 s idle at the latest); tween
   the ✦ 1.0↔1.08 every 0.6 s; let a dim tap after ≥ 1 choice equal confirm.
   Show the choice in the fight: tint the boss hit burst with `attack_color`
   and pick the bubble/splash frames by `attack_effect` on each landed tap
   (the helper `HitEngine.show_attack_feedback_2d` already exists).
5. Convert the leftover 3D magnitudes: pointer bob `+0.28 → +12.0` px; eagle
   farewell `position.y + 1.25 → position.y − 80.0` over 0.72 s.

Don't: relocate the customizer or change the art room's fantasy (owner
decision below); touch `attic/gabby/`.

Gate: `probe_stuffie` asserts the picker reopens after a close during Day
One and that a 2D companion card exists on the castle stage after confirm;
`probe_day_one_art_attack_state` asserts no `castle_logo_layer` is created
by the seven tutorial taps and that the customizer opens with a
`visual_pointer` node; `probe_dust_boss` asserts the hit burst colour equals
`attack_color`. Suite green.

### WP-D8 — Revisit and small-friction polish (DO-19, DO-20, DO-21)

Scope: `scripts/main.gd` completed-room answer and bathroom control
suspension; `scripts/arena/castle_rooms_25d.gd` blocked feedback, Rumi idle;
`scripts/pause_menu.gd`; `scripts/day_one_art_studio.gd` label.

Do:
1. Completed-room button: one line (`roshan_day1_room_clean`) rate-limited to
   ≥ 6 s, plus a small diegetic response (re-run the room's fixture surge);
   never two clips.
2. Keep back and elevator visible on completed-bathroom revisits; suspend
   controls only while the bathroom is the current, unfinished room.
3. Persist Rumi: when `day_one_pool_rumi_met` and the room is the pool,
   mount the two-frame idle Rumi at (650, 350) with a tap line
   `roshan_day1_rumi_hi` (min_gap 4.0).
4. Blocked room doors: 1.2 s SFX cooldown; on the second blocked tap within
   6 s pulse the PLOT cue and pan the hall to it.
5. Sequence the two hall-entry banners with `say_sequence`; fix "Tap the
   loose loose brushes!".

Gate: `probe_day_one_castle_dressing` / `probe_castle_door_language` legs
assert the cooldown, the pan, and that the completed bathroom exposes the
back button; suite green.

### WP-D9 — Probe coverage is the gate

Every package above names its probe legs. All of them are worthless while
the Day One probes stay outside the trusted rosters (`MA-CI-004`). Execute
WP-A1 from the 2026-08-26 handoff first, or as the first package of this
round on its own branch, and add each new Day One probe to BOTH
`scripts/ci.sh` and `.github/workflows/probes.yml` in the same package that
introduces it (workflow edits are explicit-task-only; this handoff is the
explicit task for those roster lines and nothing else). Extend
`probe_passive._progress_snapshot()` with the Day One serialized state and
the new route buttons (`MA-CI-005`) so no reward added by WP-D3/D5/D7 can be
earned idle.

## Order and parallelism

1. WP-D9 (roster) → then everything else is gated.
2. WP-D1, WP-D2, WP-D5 item 1 (the three P1 seams: exit, voice, boss
   strand) — parallel-safe, independent files.
3. WP-D3, WP-D4, WP-D6 — parallel-safe after WP-D2's keys exist (WP-D3 and
   WP-D6 reference Appendix B keys; land the keys first or stub them with a
   TODO that WP-D2 removes).
4. WP-D5 items 2–5, WP-D7, WP-D8 — after the above; WP-D5 item 3 needs the
   balance probe re-baselined.

## Escalation triggers — stop and surface to the owner

- **Legacy saves into Day One (DO-10).** The code comments say the old
  family save takes the direct route; the runtime sends it into Day One and
  rewrites the file. Which is intended? Do not ship WP-D6 item 1 without the
  answer.
- **A Daddy Mermaid voice.** Daddy's hint lines have no clip. `daddy1-3.ogg`
  are protected family recordings; generating a synthetic Daddy is a
  family-voice decision. Default in WP-D2 is to route the hints through
  Roshan; the owner may prefer to record `daddy_hint.ogg`.
- **A Rumi voice.** No Rumi voice exists in `make_voices.py`; assigning one
  is an identity decision (Rumi identity fixes were an owner item). Default
  is Roshan speaking for her.
- **The boss window.** The 0.75 s / three-taps contract is the owner's
  (2026-07-29). WP-D5 stays inside the assist/mercy system; widening the
  window itself (`VULNERABILITY_WINDOW 0.75 → 1.6 s`, proposed by runs 08 and
  11) needs the owner.
- **Where Day Two starts.** WP-D5 item 2 returns her to the castle hall;
  the owner may prefer the courtyard.
- **The art room's fantasy and the customizer's place.** Run 15 proposes
  making the Castle Logo Studio the art-room reward and moving the attack
  customizer to the Royal Hall door beat, where "attack" first means
  something. That is a design change, not a repair; not in scope unless
  approved.
- Anything touching `assets/book/`, `assets/audio/voices/` beyond adding
  new Kokoro Roshan clips, `assets/characters/friends/`, or `attic/gabby/`.
- Any workflow edit beyond the WP-D9 roster lines; any save-schema change
  beyond additive keys with defaults; any package that seems to need a
  probe rewritten to pass.
- The Sky Lagoon arrival-plane media hook and the Day One cinematic slate
  are out of scope (cinematic rule in `AGENTS.md`); WP-D1 changes only the
  in-engine guidance.

## Reporting format (per package)

```
Package: WP-Dn — <title>
Branch / head: codex/<topic> @ <sha>
Stage 0: <which findings reproduced at this head; what had moved>
Change: <files, one line each; constants old → new>
Probes: <legs added/extended; local run result; CI run id, green>
Findings closed: DO-xx → FIXED_PENDING_VERIFICATION (evidence)
Attention contract: <which targets now met, measured how>
Not done / deferred: <with reason>
Owner questions raised: <if any>
```

Closure claims stay `FIXED_PENDING_VERIFICATION` until a target-device
session confirms the modelled timings; this round produced no device or
child evidence.

## Appendix A — persona matrix and convergence

| Run | Persona | What it stressed | Total (min/typ/max) |
|---|---|---|---|
| 01 | Golden path, attentive | baseline beat log, every timer | 2.6 / 5.7 / 15.7 min |
| 02 | Tap-everything toddler | input routing, spam, sequence breaks | 2.8 / 6.4 / 22 min |
| 03 | Passive, distracted watcher | idle nudges, silence, phone-down | 8 / 13 / 23 min |
| 04 | Impatient skipper | forced wait vs agency, skippability | 2.0 / 3.3 / 5.5 min |
| 05 | Door explorer | blocked doors, elevator, leaving mid-room | 4.0 / 8.7 / 18.7 min |
| 06 | Quit-and-resume | 19 kill points, save/restore | 14 / 22 / 35 min to the boss strand |
| 07 | Sloppy gestures | every recognizer's tolerance | 3.2 / 5.6 / 12.5 min |
| 08 | Speedrunner | hard floor, ceremony, fast-input breakage | 1.3 / 2.6 / 3.9 min |
| 09 | Repeat visitor | revisits, replays, post-boss | 4.4 / 9.3 / 21.7 min |
| 10 | Ears first | voice resolution per beat, collisions | 3 / 7 / 20 min |
| 11 | Non-reader, no adult | 51-string text-carrier inventory | 2.8 / 9.6 / 35 min |
| 12 | The family phone | four save openings, New Game wipe | per opening 20–120 s |
| 13 | Boss struggler | fight second by second, mercy ramp | boss 45 / 78 / 125 s |
| 14 | Stuffie lover | playroom rescue, picker, companion | stuffie slice 21 / 84 / 357 s |
| 15 | Little artist | art studio, customizer, logo hijack | art room 21 / 90 / 335 s |
| 16 | Three short sessions | reservoir model, safe stops, session fit | 4.5 / 7 / 15 min |

The per-finding convergence table and each run's full beat log, hazard
table and proposals are in `audit/day_one_playthroughs_2026-09-02/`.

## Appendix B — voice keys to add (Kokoro Roshan voice, `tools/make_voices.py`)

| Key | Text | Fired from |
|---|---|---|
| `roshan_day1_castle` | "Let's go to the castle!" | promenade Day One guidance; reef refusal (WP-D1) |
| `roshan_day1_golden_door` | "Follow the one golden rainbow door!" | `main.gd:6847-6859` hall entry |
| `roshan_day1_dust_bunnies` | "Dust bunnies! This castle needs our help!" | `main.gd:7783-7786` |
| `roshan_day1_resting` | "That door is resting. Follow the golden door!" | `main.gd:7125-7132`; `castle_rooms_25d.gd:1712-1718` |
| `roshan_day1_basket` | "Tap the cleaning basket!" | `day_one_bathroom_cleanup.gd:712-716` |
| `roshan_day1_supplies` | "We found the sponge and the brush!" | `day_one_bathroom_cleanup.gd:677-709` (replace the two colliding lines) |
| `roshan_day1_sink` | "Scrub the sink in little circles!" | `day_one_bathroom_cleaning.gd:807-816` (min_gap 0) |
| `roshan_day1_tub_tap` | "Tap the tub to let the water out!" | same |
| `roshan_day1_bunny_no` | "No! Splash!" (short, comic) | `day_one_bathroom_cleaning.gd:669-670` (replaces `wacky_fail`) |
| `roshan_day1_tub_brush` | "Brush the tub back and forth!" | same |
| `roshan_day1_bathroom_done` | "The bathroom is sparkling!" | `day_one_bathroom_cleaning.gd:745` |
| `roshan_day1_pool_picture` | "Tap the pool picture!" | `main.gd:7636-7637` |
| `roshan_day1_skimmer` | "Sweep the skimmer through the trash!" | `day_one_pool_cleanup.gd:384-385` |
| `roshan_day1_waterfall` | "Pull the trash down the waterfall!" | `:387-388` |
| `roshan_day1_seahorse` | "Tap tap tap! Tug the trash out!" | `:390-391` |
| `roshan_day1_rumi` | "You saved the pool! This is Rumi!" | `:593-595` |
| `roshan_day1_next_door` | "A new picture door is glowing!" | WP-D3 room completions |
| `roshan_day1_bump_bunnies` | "Bump both dust bunnies away!" | `castle_rooms_25d.gd:1859-1862` (after the chirp) |
| `roshan_day1_eagle_free` | "You saved Baby Eagle!" | `:4218-4220` |
| `roshan_day1_pick_friend` | "Tap your friend, then a colour, then the heart!" | `companion.gd:610` |
| `roshan_day1_art_supplies` | "Tap the loose paints and brushes!" | `day_one_art_studio.gd:376-386` |
| `roshan_day1_art_scrub` | "Now scrub the counter!" | same |
| `roshan_day1_art_desk` | "The paint desk is glowing! Tap it!" | `:387-388` |
| `roshan_day1_pick_colour` | "Pick a colour, then tap the star!" | `attack_customizer.gd` open (WP-D7) |
| `roshan_day1_back_door` | "All four rooms are clean! The big back door is glowing!" | `main.gd:7182-7186` (moved, WP-D3) |
| `roshan_day1_boss_show` | "The great dust bunny wakes up! He is too puffy to bonk." | `dust_boss.gd:333-334` |
| `roshan_day1_boss_tell` | "When he jumps and his star flashes, tap him three times!" | `:429-430` |
| `roshan_day1_boss_wait` | "Wait for the big gold star!" | `:521-546` (miss reminders) |
| `roshan_day1_boss_dizzy` | "Bonk! He is all dizzy!" | `:1187-1197` |
| `roshan_day1_boss_cross` | "He is cross now! Watch the star!" | `:1199-1202` |
| `roshan_day1_boss_friends` | "Poof! Grand Puff is our friend!" | `:596-597` |
| `roshan_day1_day_two` | "A new day! The castle is awake!" | `main.gd:7100-7102` (after the transition) |
| `roshan_day1_room_clean` | "This room is sparkly clean!" | `main.gd:7147-7148` |
| `roshan_day1_keep_game` | "Keep our game!" | `start_menu.gd` confirm sheet (WP-D6) |
| `roshan_day1_rumi_hi` | "Hi Roshan!" (Roshan voice until a Rumi voice is decided) | WP-D8 persistent Rumi |

Keep each clip under 2.5 s, one sentence, present tense, no reading words
("button", "menu"). Add every file to `ASSET_LICENSES.md` in the same
commit.

## Appendix C — constants and values (current → proposed)

| File:line | Constant / value | Current | Proposed | Package |
|---|---|---|---|---|
| `sky_lagoon_promenade.gd:261` | Day One spawn x | 610 | 4520 | D1 |
| `sky_lagoon_promenade.gd:695-697` | castle gate idle cue alpha | 0.10 | ≥ 0.45 | D1 |
| `castle_rooms_25d.gd:2323` | hall spawn foot | (380, 835) | active door foot x − 600 | D1 |
| `day_one_bathroom_cleaning.gd:25, 27` | `*_MIN_GESTURE_SECONDS` | 2.0 | 1.5, banked across lifts | D4 |
| `day_one_bathroom_cleaning.gd:299` | motion clock reset per touch | yes | no (decay after 3 s idle) | D4 |
| `day_one_bathroom_cleaning.gd:583, 617` | tool travel | 0.38 s | 0.22 s | D4 |
| `day_one_bathroom_cleaning.gd:690` | post-drain timer | 0.36 s | 0.20 s | D4 |
| `dust_boss.gd:92` | `PREASSIST_TRIGGER_STREAK` | 2 | 1, tier persisted | D5 |
| `dust_boss.gd:63` | `DIZZY_T` | 3.2 | 1.6 | D5 |
| `dust_boss.gd:64` | `ANGRY_T` | 2.1 | 1.4 | D5 |
| `dust_boss.gd:65` | `PHASE_BEAT_T` | 2.8 | 1.2 | D5 |
| `dust_boss.gd:66` | `CELEBRATION_BEAT_T` | 1.8 | 1.0 | D5 |
| `dust_boss.gd:60` | `SHOW_T` | 6.4 fixed | tap-skippable after 5.2 | D5 |
| `dust_boss.gd:68` | `POSITIVE_PACING_FLOOR` | 38.0 | 26.0 | D5 |
| `dust_boss.gd:101` | `FEEDBACK_COOLDOWN` (shielded taps) | 2.6 s + "yay" | 6.0 s, no voice | D5 |
| `main.gd:7794-7798` | boss flag persisted | before fight | on win; re-arm while active | D5 |
| `main.gd:3983-3988` | debounce | reset to 1.5 s per queue | forced write after 4.0 s pending | D6 |
| `start_menu.gd:230-235, 262-264` | confirm sheet | START NEW gold + focused | KEEP GAME gold + focused; START NEW hold 0.8 s, 1.5 s delay | D6 |
| `day_one_art_studio.gd:8-24` | art hit boxes (art px) | 92×104 / 124×104 / 132×76 | 128×128 / 150×128 / 150×110 | D7 |
| `castle_rooms_25d.gd:4187, 4228` | pointer bob / eagle lift | +0.28 px / +1.25 px | +12 px / −80 px | D7 |
| `main.gd:7145-7148` | completed-room answer | 0.5/0.6 s gap, two clips | ≥ 6 s, one clip | D8 |
| `castle_rooms_25d.gd:1710-1718` | blocked-door SFX cooldown | none | 1.2 s | D8 |
| `audio_director.gd:169-173` | Roshan `talk`/`win` cooldown | separate keys | shared ≥ 1.2 s | D2 |

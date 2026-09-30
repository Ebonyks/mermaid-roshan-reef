# 05 — Build audit: Day Two as it stands

Part of the [Day Two story draft v2](README.md). Status: `CANDIDATE` audit,
2026-09-30, at `dev` `e7899cc0` (work branch head `4febc33b`). Method: source
reading, the repository's recorded captures and audits, and the Chapter One
book. There is no Godot binary in the authoring container, so nothing was
run. Items marked **SOURCE-DERIVED** need a real-touch runtime check before
they count as confirmed.

## The verdict in brief

Day Two has a strong skeleton:

- a real eight-step causal chain;
- a persistent cake that grows across three jobs;
- careful additive saves;
- a playable lawn finale.

But the child does not experience a story. Every job is the same
full-screen Opera template wearing a new label. The birthday is never said
out loud. Guidance mostly never reaches her. None of the Day One friends take
part, and the rooms never change as the party gets made.

| # | Finding | Severity |
|---|---|---|
| B1 | 19 of the 29 story phases have no room object, so with real touch the activity may never open (SOURCE-DERIVED; probes bypass it) | P0 suspected |
| B2 | Ballerina story goals (6 and 2) exceed the ballet surface's 1.0 cap, so two phases cannot complete (audit-recorded) | P0 |
| B3 | Six of eight story scenes draw the freeplay painting, and the widgets draw freeplay objects (pigs, the kart, the sunrise, a topping cake, the crown) | P1 |
| B4 | The birthday is never spoken; each job's result line is invisible and silent; the next-job guidance is overwritten in the same frame | P1 |
| B5 | 16 of 29 story phases have no voice; several bound clips say the wrong thing | P1 |
| B6 | The guidance picture (objective card) is hidden in castle rooms and cleared on the Sky Lagoon, and no castle door is lit for the next job: after Day One, `door_state()` uses the free-play resolver and only the Royal Hall event is ever highlighted (`scripts/arena/castle_rooms_25d.gd:1686-1702`) | P0 for wayfinding |
| B7 | Day One friends are absent from every job: Daddy, the dust bunnies and Baby Eagle have no role; the rainbow friend and Baby Eagle are static cards; Lamma is missing | P1 (theme) |
| B8 | No job leaves its result in its own room; the party table appears only after job 5 | P1 (theme) |
| B9 | The lawn finale: three drifting script versions; every line in Roshan's synthetic voice; stale "silhouette" lines; no exit route | P1 |
| B10 | Day Two locks every freeplay career and runs an unrelated "Family Evening" story in the same rooms | P2 |
| B11 | The Detective's candle touch area overlaps only about 42×22 px of the drawn candle, so a tap on the candle's centre misses ([GFX-DET-03](06_GRAPHICS_AUDIT.md#gfx-det-03); source and pixel arithmetic) | P0 |
| B12 | Lamma cannot be unlocked in real play: the `boss_lamma` battle has no authored caller and the Seek game has no live entry | P1 (theme) |

## A. From Day One into Day Two

| Step | What happens | Problem |
|---|---|---|
| Boss win | `day_one_complete_boss_and_begin_day_two` (`scripts/main.gd:6575-6589`) saves, starts Chapter 2 (first wave `0x0449`), queues the transformation clip, then the epilogue | — |
| Where Roshan lands | `_end_game` → `_exit_level2_now()` puts her on the **Sky Lagoon promenade**, not in the castle (`main.gd:8665-8668`); the objective card is cleared (`main.gd:5108`) | The first Day Two job starts from the wrong place with no picture |
| Chapter start line | Caption only: "The castle is clean! The Opera House is open. Farmer Roshan can gather strawberries first!" (`main.gd:7590-7596`), immediately replaced by "Next party sparkle: Farmer in the Sky Lagoon strawberry grove! Enter through the Dining Room berry doorway!" | Unvoiced; fired under the story clips; no berry doorway art exists |
| Day Two card | 4.18 s, eats taps; "✦ A NEW DAY ✦ / DAY TWO! / NEW ADVENTURES"; Opera, Craft and Kitchen medallions (`scripts/day_two_transition_2d.gd`); voiced "The second day is here! Visit castle jobs and the Opera House!" | No birthday; medallions don't match the first job (Dining Room); a sad tragedy mask on a celebration card |
| Unused asset | `roshan_day_two_begins.ogg` exists but nothing plays it | — |

## B. How every job is played today

All job play happens in full-screen `OperaCareerWorld2D` layers
(`scripts/opera_career_world_2d.gd`). The template:

1. Room card, then a fade.
2. A painted career world. Roshan walks to a glowing station and a floating
   widget opens.
3. A 2.2 s result hold, then a rival imp race with bars.
4. A proscenium curtain call.
5. Back to the castle with "This birthday job is ready! Back to our party!"
   and "Yay! I did it!".

### B1 — Unmapped phases (suspected P0)

- `_assign_stations` maps a phase to a room object only through
  `PHASE_STATIONS[career][phase name]` (`opera_career_world_2d.gd:407-423`,
  `1872-1889`). That table is keyed by the freeplay phase names. There is no
  alias for the Chapter 2 names.
- An unmapped phase gets `armed_station = -1`. The code comment says the
  activity "stays closed until the corresponding room object has been selected
  and reached". The 20 s auto-walk only fires when `armed_station >= 0`
  (`4573-4579`).
- Unmapped Chapter 2 names:

  | Career | Unmapped phases | Expected stall point |
  |---|---|---|
  | Chef | STACK | STACK |
  | Farmer | all 3 | Phase 0 |
  | Candy Maker | all 4 | Phase 0 |
  | Painter | STAMP, HANG | Phase 1 |
  | Ballerina | all 3 (the custom stuffie stations reuse the freeplay IDs but the phase names differ) | Phase 0 |
  | Pop Star | STAGE RUMI | Phase 1 |
  | Astronaut | BUILD ROCKET, READY PARK | Phase 0 |
  | Detective | all 3 | Phase 0 |

- Some phases may have side paths that still work: Farmer's five berry
  buttons, and the Detective lens layer.
- `probe_chapter2.gd` never builds a world, and
  `probe_chapter2_farmer_resume.gd` calls `_open_task()` directly, so no probe
  would notice.
- **Action:** a touch-driven probe for every story phase, then add the
  Chapter 2 names to the station table (or a station key on each phase).

### B2 — Ballerina goals (P0, audit-recorded)

STUFFIES TWIRL has goal 6.0 and STUFFIES BOW 2.0
(`scripts/chapter_two_career_scene_adapter.gd:35-36`). The ballet surface
caps at 1.0 and then blocks input (`scripts/opera_ballet_surface.gd:282-290`,
`461-468`, `533-544`). Recorded in `audit/OPERA_MECHANICS_REAUDIT_2026-09-05.md`
(lines 267-272, 908-917): "Chapter 2 implementation is 1/5 until the blocker
is repaired."

### B3 — Scenes and widgets that contradict the story

- Only the stuffie room and the Sky Lagoon farmer have scene art
  (`scripts/opera_world_backdrop_2d.gd:65-80`). The other six labels draw the
  freeplay painting.
- The widgets never read the Chapter 2 asset settings (`chapter2_*` keys set
  at `opera_career_world_2d.gd:2523-2556` are never read by
  `opera_gesture_surface.gd`).

| Job | What the story says | What the child actually sees |
|---|---|---|
| Farmer | Deliver the basket to the kitchen | Three pigs pushed to a barn gate (`widget_push_farmer_mover.png`) |
| Chef | Stack the six rainbow tiers | Toppings placed on a plain sponge cake, in a bakery that already has a painted celebration cake |
| Candy Maker | Candy the five strawberries | A transparent input surface over code-drawn panels in a candy factory with no strawberries |
| Painter | Paint the birthday banner | The sunrise painting (`goal_painter.png`) revealed; two easels; a gallery choice |
| Astronaut | Park the rocket, unlaunched | The kart pushed to a starting arch |
| Detective | Find the candle in the magic storybook | The imp's crown-theft intro ("The sparkly crown! Now everyone will look at ME!"), a night market with the crown painted in its chest, and no storybook |
| Pop Star | Sound-check with Rumi | Freeplay stage; Rumi is one static frame |

The rival imp still races Roshan with bars and a bow in birthday jobs
(`opera_career_world_2d.gd:3196-3233`, `3778-3792`).

## C. Job by job

| Job | Launch | Phases (story) | Voice | Result shown | Thematic gap |
|---|---|---|---|---|---|
| Farmer | Dining Room card (Main Hall → Dream House Wing → Dining Room) | GATHER, FILL, DELIVER | All caption-only | Nowhere in the Dining Room | Never on the real Sky Lagoon; pigs; the dust bunnies and Baby Eagle absent |
| Chef | Kitchen card | MIX, STIR, BAKE, STACK, FROST | STACK caption-only; MIX, BAKE and FROST play old clips ("Tap when the oven marker is green!") while exact `_stage` clips go unused | Cake hold 2.2 s; later on the Main Hall table | Daddy absent; the bakery already has a cake |
| Candy Maker | Kitchen card (second Kitchen job) | COAT, SORT, GLAZE, PLACE | All caption-only | Cake tray, then final cake | Replaced by the Arborist in this draft |
| Painter | Craft Room card | PAINT, STAMP, HANG | All caption-only | A blank banner, only after job 5; the child's strokes are never kept | Paints a sunrise; not the table she cleaned on Day One |
| Ballerina | Playroom stuffie nook (plot prop) | MIRROR, TWIRL, BOW | MIRROR caption; the others partial | Party table appears in the Main Hall | Lamma absent; B2 blocker |
| Pop Star | Opera Hall stage star → foyer → balcony portal | SOUND CHECK, STAGE RUMI, RHYTHM, ENCORE | RHYTHM caption-only (exact clip unbound); STAGE RUMI generic | Icon on the table | Rumi static; her castle history unused |
| Astronaut | Mermaid Pool card | BUILD, PATCH, VALVE, PARK | BUILD and PARK caption-only; VALVE's clip implies launching | Rocket on the table | The kart; the pool's rainbow waterfall and seahorse unused |
| Detective | Library magic book (plot prop) | LENS, BOARD, CANDLE | CANDLE caption-only; the crown intro plays | Candle in the Library until the party | Crown intro; the storybook board is free taps on a transparent surface |

Pacing: 29 story phases in total (freeplay has 61). Every job adds 2.2 s
holds, a 3.2 s curtain call, fades and castle walking.

## D. The castle on Day Two

- **Rooms never change.** No berries in the Dining Room, no cake in the
  Kitchen, no rocket at the pool. Only the Library shows the unlit candle
  after Detective.
- **The party table appears only after job 5** (`chapter_two_director.gd:538-540`):
  - a blank rainbow banner;
  - the stateful cake;
  - the candle;
  - the rocket;
  - icons for four jobs, dimmed until earned;
  - no icons for Chef, Detective, Candy Maker or Farmer.
- **The Opera foyer "story index":**
  - The foyer portals are invisible buttons with no pointer; the pulse
    animates an invisible button.
  - The caption says "Four glowing career doors…", which is wrong after
    Painter.
  - Its clip invites a choice ("Which job should I play?") when only one door
    works (`main.gd:2757-2760`; `opera_house_venue_2d.gd:359-379`).
- **Room entries:** most room-entry voice files are missing, so the child
  hears a pitched "yay" (`castle_rooms_25d.gd:1799-1814`).
- **The party hotspot:** "Tap the rainbow to visit the party!" but the touch
  area is the table (`chapter_two_room_plot.gd:92-102`, `125-127`).
- **Freeplay is locked.** While Chapter 2 is active, room cards show only
  party jobs and launch only the story version (`castle_career_routes.gd`,
  `chapter_two_director.gd:604-616`). Doctor, Boxer, Magician, Racer,
  Nursery, Geologist and Teacher return only at lawn beat 8.
- **A parallel story:** the optional Comfy Games run a Day Two hide-and-seek
  and a "Family Evening" (dinner, movie, bedtime) in the same rooms on the
  birthday (`scripts/comfy_games.gd:8-17`, `271-331`).

## E. Who is (not) in Day Two

| Character | Day Two today | Gap against Book One |
|---|---|---|
| Daddy Mermaid | Lawn guest portrait only; speaker of two locked-room captions | The book's guide ("One little job at a time") has no job role |
| Baby Eagle | Static companion card beside Roshan in castle rooms; not on the Sky Lagoon | No role in any job |
| Rainbow friend (Grand Puff) | Static card in castle rooms (`scripts/rainbow_friend_follower.gd`); not on the Sky Lagoon | No role; "Your rainbow was there all along!" never pays off |
| Playful dust bunnies | Absent | The book's gentle-play thread is dropped |
| Rumi | Static frame 0 of `assets/characters/rumi/rumi_eight_pose_runtime.png` in Pop Star; a lawn guest | Her hundreds of years in the castle are unused; no voice (by rule) |
| Lamma | Absent from the story; exists only in the companion roster, a battle round and Seek, none of which a child can reach today (B12). Her only Day Two appearance is in Evie's arms in Evie's portrait at the party | The owner's new thread: three hiding moments and a joining game |
| Mewsha | A roster starter whose art the owner rejected; to be rebuilt only from photos of the real toy | Not used in this draft until rebuilt |
| Friends | Lawn portraits with procedural hats | Present only at the very end |
| Imps | Race Roshan in every job | Unused recorded lines would tie them to a rival grey party (`tools/make_voices.py:376-427`), e.g. "I was sent to learn the DECORATING. Ours is very grey." |

## F. The lawn finale (implemented alpha)

- Nine beats with voiced `chapter2_lawn_*` lines, rocket ignition with real
  walk-and-press, three protection rounds, theft and reassurance
  (`scripts/chapter_two_lawn_finale_2d.gd`).
- Three script versions disagree:
  - the design script (`design/CHAPTER2_LAWN_FINALE_DRAFT_2026-09-06.md`);
  - the captions (`DIALOGUE`);
  - the recorded lines (`assets_src/chapter2_lawn_audio_2026-09-06/LINES.json`,
    Roshan narrating everything). The captions and recordings dropped
    "Father, it's her birthday" and "He took our light".
- Every line plays in the synthetic Roshan voice, including the King's and
  Prince's; captions carry "King:" and "Prince:" labels.
- Stale lines still fire from `main.gd`: "A little ember silhouette is
  watching the party!" and "…His little son's silhouette points to the bright
  north-star clue!", plus a `chapter3_north_fire_mountain` objective.
- The end returns straight to the Main Hall. The Chapter 3 sky-door reveal
  runs only when entering the castle from outside, so Day Two ends with no
  visible next route.
- Presentation problems are itemised in the [graphics audit](06_GRAPHICS_AUDIT.md#6-the-lawn-finale)
  (GFX-LAWN-01 to -16): hats that cover faces, a tiny banner, the headline
  text, the flat ellipse warning, the static King and Prince, a candle
  lighting too small to see, and no change after the theft.

## G. Voice and captions

Rule in force (`scripts/audio_director.gd:475-516`): inside a career world
only an exact recording plays, otherwise the caption shows silently. In the
castle, `show_msg("", …)` is a silent caption.

| Job | Caption-only phases | Wrong clip | Exact clip that exists but is unbound |
|---|---|---|---|
| Farmer | GATHER, FILL, DELIVER | — | — |
| Chef | STACK | MIX, BAKE, FROST | `op_chef_pour/stir/bake/pipe_stage` |
| Candy Maker | all 4 | — | — |
| Painter | all 3 | — | — |
| Ballerina | MIRROR | TWIRL, BOW (partial) | `op_ballerina_ribbon/twirl_stage` |
| Pop Star | RHYTHM | STAGE RUMI (generic) | `op_popstar_rhythm_stage`, `op_popstar_encore_stage` |
| Astronaut | BUILD, PARK | VALVE implies launch | `op_astronaut_pipes_stage` |
| Detective | CANDLE | LENS, BOARD, the crown intro | `op_detective_lens_stage` |
| Castle | Every route line, foyer redirect and plot announcement | — | none |

- Every job's result line, the candle-found line, the ballet-done line and
  the "I learned my … sparkle!" line are sent while the Opera world is still
  up, so they are neither shown nor spoken (`main.gd:2906-2909`, `7486-7541`).
- The Opera ACTS intro lines and the Chapter 2 override intros are dead data:
  nothing reads them.
- This is `MA-ACCESS-001` (required objectives lack exact spoken cues) and
  `DL-AGE-01` / `DL-SND-01`.
- Kareem's voice route (`_speaker_key` maps "kareem" to "shop",
  `audio_director.gd:470`) plays the adult shopkeeper preset ("Shop, Jon,
  welcoming adult voice" in `assets/audio/voices/VOICE_MANIFEST.md`), but his
  protected portrait (`kareem.png`) shows a boy in a shell armchair. No Day
  Two scene uses his voice today; any new line for him needs his own preset
  first ([decision 13](README.md#owner-decisions)).

## H. Saves, probes and document drift

- **Saves** are careful and additive: berry mask, cake mask, job phase masks,
  party piece mask, event phase, lawn beats and protection rounds, with
  healing for malformed values. Keep this.
- **Probes** check the director and saves, not real touch. B1 would pass
  every current probe.
- **Drift:**
  - The spine promises Farmer washing and Rumi animation; neither exists.
  - `DL-INT-07` still says 13 careers and 53 phases; the code has 15 and 61.
  - `DL-INT-12` lists 13 careers.

## I. Where the theme is thin

1. **The birthday lives only in captions.** It is never said in the castle,
   never on the card, and every job ends with the same "Yay! I did it!".
2. **One template for eight jobs.** Nothing tells the child why this job,
   for whom, or what it adds to the party. The draft answers with the
   party-preparation script
   ([plotline](00_DAY_TWO_PLOTLINE.md#what-each-job-gives-the-party)).
3. **Nobody helps.** Book One's heart is helping friends; Day Two has Roshan
   working alone against a rival.
4. **The world does not remember.** Rooms stay the same; the party appears
   late; the banner is not her own.
5. **Settings contradict the plot:** the bakery's cake, the candy factory,
   the sunrise, the crown, the kart, the pigs.
6. **The Day One threads are dropped:** gentle play, Rumi's castle, Baby
   Eagle's rescue, the hidden rainbow.
7. **The finale arrives without set-up:** the King and Prince appear only at
   the end; nothing foreshadows them. The unused imp "grey party" lines could
   plant it.
8. **A parallel family evening** competes with the birthday in the same rooms.
9. **Nobody invited the guests.** Eight friend portraits, Daddy's among them,
   wait on the lawn (`GUEST_FILES`, `chapter_two_lawn_finale_2d.gd:34-35`),
   but no scene invites them and no job is for any of them. The August party-function
   script (`CHAPTER2_PARTY_ROLES_2026-08-03.md`) made "Somebody has to tell
   me" a guest's first need and gave every job a named guest. The draft
   answers with Daddy's invitations at dawn and a named friend for each job
   (`D2-OPEN-2`; [01, section 11](01_STORY_BIBLE.md#11-the-party-preparation-script-what-day-two-keeps)).

## J. What is strong and should be kept

- The causal chain and additive save model (berries → cake → candle → rocket
  → party).
- The persistent cake with its seven honest picture states.
- The Day One in-room activity pattern (pool, bath, toilet), the right engine
  for in-world levels.
- The stuffie ballet idea: Roshan leading the stuffies on the playroom's own
  tiles (its stations and doll crops need the repairs in
  [06](06_GRAPHICS_AUDIT.md#ballerina-scene-255)).
- The lawn's walk-and-press rocket ignition with real hand contact.
- The Opera freeplay careers as finished teaching levels, with exact
  `_stage` recordings for every job.
- The Teacher lesson plan as the model for the Arborist's Tree Book.
- The King V4 and Prince identity locks and the corrected 80% scale.

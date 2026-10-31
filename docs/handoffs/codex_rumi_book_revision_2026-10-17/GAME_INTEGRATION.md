# Bringing the under-pool book into the game

**Status:** `PROPOSED / CANDIDATE`, written by Claude on 2026-10-17 at dev
`7a65b9f0abacddeee70230f220955f4d18d551b5`. The playable chapter is **not
commissioned**: under `DL-PLAN-01` the owner first approves a chapter's premise
and boundaries (owner question Q6 in the [README](README.md#5-owner-questions)).
Until then Codex may prepare the brief and the book, not runtime work.
Facts about existing code were checked at the dev commit above; scores come
from `python -B tools/gold_star.py --rank` on that tree.

**Revision 2 (2026-10-18).** After this packet was written, the owner ordered
the Pop Star rebuilt from the ground up (`ODR-MINIGAME-REBUILD-20261017`,
`ODR-POPSTAR-CORE-20261018`, finding `MA-OPERA-014`): its note-memory echo
becomes a music-timed call and answer in the
[Rainbow Band handoff](../codex_minigame_rebuilds_2026-10-17/POP_STAR.md).
The call-and-response activities below now take that engine, and the quiet
hold takes the shared hold gesture rather than the old Pop Star phase list.

## 1. Options and the recommended method

| Option | What it is | For | Against |
|---|---|---|---|
| A. Book only | Revise and print the book; no game change | No runtime risk | The owner asked for smooth integration; nothing to play |
| B. In-game storybook | Show the pages in the castle with recorded narration | Reuses the pages | No book reader exists today (closest: the Movie Lounge still-picture advance and the Library's opening-book animation in `scripts/arena/castle_rooms_25d.gd`); watching is not playing; book rendering differs from the game's |
| C. Story clips | Animate chosen pages as short clips between activities, like Day One | A proven pattern (`scripts/day_one_story_clips.gd`, [story-clip recipe](../../../design/reference/recipes/story_clip.md)) | New footage goes through the full animation workflow and its gates; clips never perform the child's action |
| D. Book-led chapter | Each book chapter becomes a playable segment in Pearl Hollow, reached from the Mermaid Pool room; book and game share one world bible, one script and one asset family | Deepest fit; reuses the game's best verbs; leaves persistent results in the castle | Largest scope; needs the owner's commission; art gaps |
| **E. Hybrid (recommended)** | D as the spine; B as the reward (finishing each segment unlocks that book chapter, narrated, in the castle library); C only for the two spreads (arrival and lantern release) once their art exists | The book becomes the chapter's recap and bedtime reading; play stays first | Needs D's commission first |

**Method: one world, two media.** The [world bible](WORLD_BIBLE.md) and
[`data/page_plan.json`](data/page_plan.json) are the single source. Book
pages and game scenes are built from the same reference boards, so a place,
prop or character looks the same in both. The book shows what the game lets
the child do; the game never needs the book to be read (`DL-AGE-01`).

**Order:** story first (owner read-aloud approval), then reference boards,
then the chapter brief, then one representative activity, then the rest — the
sequence the [chapter guide](../../../design/09_CHAPTER_DEVELOPMENT_GUIDE.md)
requires (build one activity early and fix its pattern before repeating it).

## 2. What the game already has

| System | Where | The child's verb | Gold-star score | Use in Pearl Hollow |
|---|---|---|---|---|
| Mermaid Pool room (Rumi's pool) | Room built in code in `scripts/arena/castle_rooms_25d.gd`; Day One jobs in `scripts/games/day_one_pool_cleanup.gd`, `pool_skimmer_activity.gd`, `pool_waterfall_activity.gd`, `pool_seahorse_rescue_activity.gd` | Drag a net, stroke clogged lanes, tug trash free | 3/5, 21/24 — rank 1 and the reference model ([GOLD_STAR](../../../design/reference/GOLD_STAR.md)) | Entry (the glint door) and return; follow its patterns |
| Bathroom cleanup (Day One) | `scripts/games/day_one_bathroom_cleanup.gd`, `day_one_bathroom_cleaning.gd`, `day_one_bathroom_toilet.gd`; tools in `assets/castle/dirty_cleanup_2d/` | Scrub in circles with a star sponge, drain, brush | 3/5, 15/24 | Cleaning Station scrub of Duri's shell |
| Detective career | `detective` phases in `scripts/opera_career_world_2d.gd` | "Sweep the magnifying glass ... glitter footprints!" (`lens` mode) | Not reachable in normal play | Magnifier clues (pages 3, 13, 15) |
| Pop Star career | `popstar` phases in `scripts/opera_career_world_2d.gd`; modes in `scripts/opera_gesture_surface.gd` | Bop the imps; **hold** the microphone; choose the dance arrow; bop the band; **echo**: "Listen to the stars sing — then tap their song back, as slow as you like!"; draw an encore circle | 1/5, 13/24 — not reachable in normal play (`MA-PLAY-005`); being rebuilt (`MA-OPERA-014`) | Prototype stand-in only. The rebuild's call and answer replaces this echo for the Echo Dome and the finale; the hold gesture lives in the shared gesture surface |
| Pop Star rebuild, "Roshan's Rainbow Band" (owner-approved design, not yet built) | [POP_STAR.md](../codex_minigame_rebuilds_2026-10-17/POP_STAR.md) in the career-rebuild handoff | The band plays a one-bar call and the child answers it on drums in the next bar; ribbons demonstrate; a crowd break where her lead makes the crowd answer | — | **The call-and-answer engine for Pearl Hollow:** its help levels, its "the band waits" mercy floor and its anti-mash damper suit a four-year-old, and its crowd break is the Lantern Night circle |
| Wardrobe and Fashion Designer | `scripts/fashion_designer.gd`; the pre-party dress gate in `scripts/chapter_two_director.gd` ([brief](../../../design/FASHION_DESIGNER_ROSHAN_2026-10-06.md)) | Dress up; a required outfit before an event | Wardrobe 3/5, 18/24 | Detective hat, bathhouse robe, show outfit |
| Comfy castle games | `scripts/comfy_games.gd` | Find hidden friends (Rumi already hides in the pool room), cook and serve dinner, bedtime | 3/5, 17/24 | Finding lanterns; serving the feast |
| Discovery and return | `scripts/arena/fairy_conservatory_door_2d.gd`, `fairy_conservatory_handoff_2d.gd`, `scripts/probe_fairy_conservatory_route.gd` | Touch a landmark, travel, come back to the exact room | — | The glint door route ([Fairy route](../../../design/FAIRY_CONSERVATORY_CHAPTER3_2026-08-30.md)) |
| Swim navigation | `scripts/stage_navigation_2d.gd`, `scripts/roshan_sprite_loop.gd` | Touch to swim along authored lanes | — | Bridge gully, bubble maze |
| Water effects | `assets/sprites/fx_water/`, `scripts/fx_water.gd` | — | Approved project-original art | Bubbles, foam, vent plumes, whirlpool |
| Imp behaviour | `scripts/imp_ai.gd` | Bop crews, no-fail | — | Comic stage imps only |
| Microphone words | `scripts/mic_input.gd`, [MIC_SPELLS](../../../MIC_SPELLS.md) | Say a taught word as an extra to a tap | Prototype; owner sign-off on the microphone permission is still outstanding | Optional "Here I am!" (Q5) |
| Dormant engines | `scripts/games/melody.gd`; `scripts/collection_system.gd` | Tap notes in a window; catalogue screen | — | Possible lantern collection page |

## 3. Chapter-to-activity map

Activity ids match `game_link` in the page plan. Each row gives the chapter
guide's causal sentence: by doing X, Roshan changes Y, so Z becomes possible.

| Book pages | Activity id | Verb and engine | Causal sentence | Persistent result |
|---|---|---|---|---|
| 2–3 | `pool_room_glint`, `wardrobe_detective_hat` | Dress (wardrobe); sweep the magnifier (Detective `lens`) | By putting on her detective hat and looking under the bench, Roshan finds light rising from below, so the glint door opens | The door stays open in the pool room |
| 4–5 | `pearl_hollow_arrival` | Transition: swim down, or a clip (option C) | Establishes the town; no prize | — |
| 7 | `answer_circle_practice` | A short story beat: Rumi calls, the BOOM swallows the answer | Shows the problem; no prize | — |
| 8–11 | `bridge_whirlpool_rescue` | Touch Hana to stop her; swim into the calm eye; drag the strap off the knot; touch Rumi's hand | By swimming into the calm middle and loosening the knot, Roshan frees Duri, so his lanterns can be found | Duri is free |
| 12–13 | `collect_lantern_shells` | Find and drag lanterns into Duri's satchel (comfy find plus `lens` for hidden ones) | By finding the scattered lanterns, Roshan refills the satchel, so every home will have one | Lantern count; Pip appears |
| 14 | `bathhouse_robe_dressup` | Dress: robe, sheep towel on the hat | Arrival ritual; no prize | Outfit worn in the bathhouse |
| 15 | `cleaning_station_scrub` | Scrub circles with a sponge (Day One bathroom engine) | By scrubbing Duri's shell clean, Roshan uncovers the imps' glitter logo, so she knows who is booming | Clue found |
| 16 | `echo_dome_call` | Call and answer (Rainbow Band engine): Grandma whistles a two-note call, the child answers on glowing shells in the next bar, with the band-waits mercy | By answering in the Echo Dome, Roshan proves the BOOM swallows small voices | Test done |
| 18 | `lounge_feast` | Serve: drag dishes to each friend (comfy dinner) | A quiet reward and a natural stopping point before the dark-out | Feast eaten |
| 21 | `show_costume_change` | Dress gate, like the party dress | By choosing a show outfit, Roshan is ready for the stage | Show outfit worn |
| 22–23 | `bubble_maze_swim` | Swim through soft bouncing bubbles | By swimming the maze, Roshan reaches the Boom Shell | — |
| 25–27 | `boom_shell_quiet_hold` | **Hold** (the shared hold gesture in `scripts/opera_gesture_surface.gd`): a calm, steady hold whistles; fast tapping only makes the shell rumble louder (feedback, never failure) | By holding a calm whistle instead of tapping, Roshan starves the shell, so every lost voice comes back | The Boom Shell turned upward |
| 29–31 | `lantern_answer_song` | **Crowd lead** (Rainbow Band crowd break): the child calls "Here I am!" with a tap (or, optionally, her voice) and the circle answers "Here you are!" on the next beat; each answer lights a ring of lanterns | By calling first, Roshan wakes every lantern, so Lantern Night happens | Lanterns float in Rumi's pool |
| 32 | `pool_room_return` | Return to the exact pool-room context | The pool glows with lanterns; Roshan asks to look for the candle | Pool-room dressing changed |

The quiet hold is the activity where the story's rule and the game's rule are
the same: mindless tapping is never the best strategy (`DL-AGE-04`,
`DL-AGE-05`), and here it visibly feeds the BOOM, while intentional calm play
wins. Build the call-and-answer activities on the Rainbow Band engine once it
lands, keeping its anti-mash damper. If a prototype uses today's untimed echo
mode as a stand-in, remember the 2026-08-05 playability audit found that stray
taps earned progress there (`OPERA_QUALITY_PLAYABILITY_AUDIT_2026-08-05.md`,
item A2).

**Recommended representative activity:** `cleaning_station_scrub`. It reuses
the game's core verb and an existing engine, it is short, it has a visible
truthful result (the shell's real pattern and the clue appear,
`DL-INT-02`), and it exercises enter → understand → act → result → save →
leave → return inside the new bathhouse art.

## 4. Navigation and save

- **Entry.** The glint appears under the Mermaid Pool room's bench only after
  Chapter 2 ends with the candle taken — the same two conditions the Fairy
  route checks (`chapter2_story_complete` and `chapter2_candle_taken`) — so the
  candle is canonically missing. While `MA-PLAY-005` keeps Chapter 2 from
  completing on a fresh save, this chapter is equally unreachable; the brief
  must say so or choose a reviewed alternative.
- **Route.** Pool room → glint door → rainbow shaft → Pearl Hollow hub
  (bridge, park, bathhouse, plaza) → back to the exact pool-room context, with
  one Back that always works (`DL-AGE-06`).
- **Save.** Add keys with defaults; never remove or rename existing keys. One
  phase number for the chapter, a lantern count and a completion flag cover
  the plan; Codex sets final names and reconstruction with the
  [save rules](../../../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md#13-save-lifecycle-and-release-safety).
  Every activity boundary is a resume point; no lantern is ever lost.
- **Persistent consequence at home.** After the finale, the pool room keeps
  its floating lanterns and brighter rainbow; Rumi's line there changes.

## 5. Asset shortlist

Decisions follow `DL-PLAN-03`; inspect each file and its consumers again at
the implementation head.

| Asset or family | Path | Authority as found | Proposed role | Gaps | Decision |
|---|---|---|---|---|---|
| Mermaid Pool room art and fixtures | `assets/flats/castle/rooms/room_mermaid_pool*.png`, `assets/castle/day_one_pool/` | Approved runtime art | Start and return | A bench-glint state and an open-door state at new paths | Use |
| Roshan atlases | `assets/characters/roshan_25d/`; Pop Star career atlases | Identity authority | Roshan throughout | Pop Star ribbon defect (`MA-ROSHAN-005`) | Use |
| Rumi atlases | `assets/characters/rumi/rumi_eight_pose_runtime.png`, `rumi_pool_idle_swim_atlas.png`; outfits in `assets/fashion/outfits/` | Runtime art | Rumi in Pearl Hollow | Swim-down and chain poses | Use |
| Imps | `assets/opera/worlds/actors/rival_popstar*.png`, `rival_magician*.png` | Project-owned Opera art | Stage imps | Swallowed and shell-turning states | Use, with named gaps |
| Detective magnifier mode | `lens` mode in `scripts/opera_gesture_surface.gd` | Runtime code | Clue sweeps | Underwater dressing | Use |
| Bathroom cleanup tools | `assets/castle/dirty_cleanup_2d/` | Runtime Day One art | Sponge and bubbles | A sea-sponge variant | Use |
| Water effects | `assets/sprites/fx_water/` | Approved | Bubbles, foam, vents | — | Use |
| Kelp, seagrass, sea star, clownfish | `assets/props/gen2/kelp.png`, `seagrass.png`, `starfish_decal.png`, `clownfish_side.png` | 2D props; recheck authority | Kelp Park dressing | Style match | Candidate |
| Turtle concept | `gen2/generated/aquatic_turtle/v3.webp` (turnarounds in `gen2/turnarounds/aquatic_turtle/`) | Concept only: no `ASSET_LICENSES.md` row; the art inventory marks the family not approved | Duri's identity source | Provenance row, approval, cutout and states | Reserve; needs approval |
| Book pages, all editions | Rescue branch, see the [README](README.md#2-sources) | Owner-commissioned draft art | Reference for Hana, Nari and Duri likeness only | Different rendering | Reference only |
| Friend portraits | `assets/characters/friends/` | Protected originals (`DL-ASSET-03`) | — | — | Reject as anonymous crowd art |

**Named new-art gaps:** Pearl Hollow hub and district backdrops; the five
bathhouse rooms; Grandma Gobuk; the citizens set; glow-jelly lanterns (dark and
lit); clam-shell lanterns; the Boom Shell (idle, booming, swallowing,
hiccuping, turned upward); Duri; game atlases for Hana and Nari if they appear
in play. Art follows the project's art rules at the implementation head
(`DL-ASSET-01`, `DL-ASSET-02`); a 2026-10-17 owner art-quality direction exists
as uncommitted work in another checkout and is not on `dev` at this packet's
baseline, so apply whichever text is current when the work starts.

## 6. Voices

Every objective needs an exact spoken cue and a moving pointer (`DL-AGE-01`,
`DL-SND-01`, `DL-SND-13`). Existing Rumi lines are provisional synthetic
filler (`assets/audio/voices/filler_v1/rumi_*.ogg`), and the birthday chapter's
scope says "no invented Rumi voice". Protected recordings stay untouched
(`DL-SND-05`). Who voices Hana, Nari, Duri, Grandma Gobuk, the imps and any new
Roshan or Rumi line is the owner's choice (Q5).

| Activity | Cue (exact) | Speaker | Pointer |
|---|---|---|---|
| `pool_room_glint` | "Something is glinting under the bench!" | Roshan | The bench |
| `wardrobe_detective_hat` | "My detective hat!" | Roshan | The wardrobe |
| `bridge_whirlpool_rescue` | "Help! My strap is stuck!" / "Stop, Hana!" / "Swim into the calm middle!" / "Reach for Rumi!" | Duri / Roshan / Roshan / Rumi | Hana; the eye; Rumi's hand |
| `collect_lantern_shells` | "Find Duri's lanterns!" | Rumi | Next lantern |
| `cleaning_station_scrub` | "Scrub Duri's shell — gently!" | Grandma Gobuk | The shell |
| `echo_dome_call` | "Listen... now whistle it back!" | Grandma Gobuk | The dome |
| `lounge_feast` | "Give everyone a treat!" | Nari | The next friend |
| `show_costume_change` | "Pick your show outfit!" | Rumi | The rack |
| `bubble_maze_swim` | "Swim to the Boom Shell!" | Nari | The shell |
| `boom_shell_quiet_hold` | "Hold still and whistle softly." | Grandma Gobuk (remembered) | Roshan |
| `lantern_answer_song` | "Call it, Roshan: Here I am!" / "Here you are!" | Rumi / Everyone | The centre spot |

## 7. Dependencies and risks

| Item | Effect | Next step |
|---|---|---|
| `MA-PLAY-005` (Chapter 2 careers cannot complete on a fresh save) | The entry condition cannot be met in normal play | Track it; decide the gate in the brief |
| Pop Star rebuild (`MA-OPERA-014`) | The Echo Dome and finale need the Rainbow Band call and answer, which is designed but not built | Build those two activities after it lands; a stand-in on the old echo mode must not reward mashing (2026-08-05 audit, A2) |
| Microphone permission | Voice input needs owner sign-off; the tap must always work alone | Q5 |
| Turtle art authority | Duri has no approved, licensed source | Provenance row and approval |
| Rendering style | Book art cannot double as game art unless the style matches | Q4 |
| Book sources stranded | Editions exist only on rescue branches | RB0 in the [README](README.md#4-work-packages) |
| Child evidence | No observed child session exists for the game (`MA-CHILD-001`) | Plan a read-aloud and a play observation |

## 8. Draft chapter-brief values

For `design/templates/CHAPTER_BRIEF_V1.md` section 1, as proposals:

| Field | Proposed value |
|---|---|
| Chapter ID/title | Lantern Night beneath the Pool |
| Owner authorization | Proposed only; Q6 |
| One-sentence child desire | Help the hidden town under Rumi's pool light its lanterns — and sing the very first line |
| Entry state and ending | After Chapter 2's candle is taken; ends with lanterns floating in Rumi's pool and Roshan ready to look for the candle |
| Canon and authorities | [Chapter 2 spine](../../../design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md); [Fairy route](../../../design/FAIRY_CONSERVATORY_CHAPTER3_2026-08-30.md); [reference library](../../../design/10_CHAPTER_REFERENCE_LIBRARY.md); approved Roshan and Rumi identities |
| Delegated minor additions | Pearl Hollow, its citizens, Lantern Night, the Boom Shell, Pip, the bathhouse rooms |
| Reserved decisions | Q1 candle, Q2 Grandma Gobuk's relation, Q4 style, Q5 voices and microphone, Q6 commission |
| Scope | Eleven activities in section 3, two optional clips, the named art gaps, the voice cues in section 6 |
| Out of scope | Recovering the candle, the Ember King, any 3D, a required microphone, changes to Day One clips |

# Day One pacing review — chapter one, rough draft (2026-08-31)

_First evaluation of the **Pacing and session flow wing** (master audit
section 3.4; rules `DL-PACE-01`–`DL-PACE-06`, design 06 section 21). Owner
mandate: play through the completed chapter-one rough draft as a game
designer focused on timing, spacing, and pacing for a four-year-old's
tablet play, and deliver pros/cons, weaknesses, and an improvement guide
grounded in this branch's principles._

**Method and honesty note.** No Godot binary runs in the review
environment, so this is a **code-traced playthrough**: every timer,
message, tween, travel distance, spawn count, gesture threshold, and save
edge in the Day One path was read at the current head, voice-clip
durations were measured from the OGG files themselves, and the child's
experienced timeline was reconstructed from those constants. Where the
verdict depends on device feel (touch latency, load hitches, real finger
travel) the item says so and defers to the tablet performance wing. Claims
carry file:line anchors; the two P1 mechanisms (caption overwrite at
castle entry, post-boss teardown) were independently re-verified.

## 1. The played timeline (fresh save, cooperative four-year-old)

| Beat | What happens | Time (est.) | Pacing verdict |
|---|---|---|---|
| Boot → menu → NEW GAME | 0.45 s splash; menu; no confirm on fresh device; scene reload, **no fade, no intro** | ~5 s | Excellent — control almost immediately |
| Arrival at promenade | Focus ring + "Tap the pearl plane to visit the Reef!" (`sky_lagoon_promenade.gd:1077-1083`); the Grok arrival media is a request key only — nothing renders | — | **Misdirection**: the chapter's only opening guidance points away from the castle; the plane departs on a 7 s timer |
| Walk to castle | 4,702 master px at 790 px/s ≈ 5.95 s of held travel; auto-enter at 62 px | 15–30 s real | Long neutral hold for the age; no story pull toward the door |
| Castle entry | Discovery line "Dust bunnies! This castle needs our help!" fires and is **overwritten in the same frame** by the golden-door line (`main.gd:6647` before `6652`); voices: generic `roshan_talk` + a pitched **yay** (`roshan_home.ogg`/`roshan.ogg` don't exist) | ~5 s | The inciting story beat is unreadable and unvoiced |
| Hall → Bubble Bath | Tap-to-walk clamps at a flat 1.05 s per hall crossing; golden door pulses (3.2 s period); 3 poppable hall bunnies | ~10 s | Good macro signpost; snappy travel |
| Bathroom | One-tap "supply hunt" (both tools pre-placed) → 3 captions inside 0.4 s → sink scrub (arc + 520 px + 2 s) whose instruction is **always caption-only** (0.38 s machine-timed cooldown collision, `day_one_bathroom_cleaning.gd:599` + `audio_director.gd:16-19`) → tub tap, comic "NO!" (0.68 s) → brush scrub → win line, 0.34 s reveal, 0.92 s teardown | 30–50 s | Core gesture play is the chapter's best; entry beat is fake, first instruction silent, sink gets no reward beat |
| Picture door → Pool | Ghost-hand loop on the pool picture; voiced prompt | ~5 s | Good |
| Pool | 6 sweep + 3 pull + 8 tap = 17 actions; one spaced instruction per phase; room brightens on a 17-step lerp; Rumi rises 1.15 s, waves, line at ~1.73 s after the last tap — **voiced as a pitched yay** (no `rumi_*` clip exists) | 60–100 s | Best-designed room; climax emotionally under-delivered; afterwards **nothing says where to go next** |
| Playroom (stuffie) | Eagle chirp announce; bump 2 pinning bunnies (contact or tap) | 10–20 s | Good palate-cleanser; completion has the eagle's win line only |
| Craft room (art) | 7 taps, **8 captions fired back-to-back** with an uncooled `roshan_talk` on every tap (`day_one_art_studio.gd:393`, min_gap 0.0); "Tap the loose loose brushes!" (duplicated word); "scrub the grime" is voiced while input is a single tap; desk → attack customizer (5 colors × 2 effects — the chapter's one agency beat) | 30–60 s | Machine-gun pacing; verb/gesture mismatch; the customizer is a genuinely good payoff |
| Boss door arms | `EVENT_BOSS_DOOR_GLOW` fires on art completion — **with no message, no celebration, on the real path** (`day_one_complete_art_scene` `main.gd:7030-7040` shows nothing; the "All four rooms are clean! The big back door is glowing!" banner lives only in the unused generic path `main.gd:6939`) | — | The chapter's biggest state change is silent |
| Boss | 6.4 s intro (auto-advances); telegraph "When he JUMPS and his star FLASHES — TAP him!" — `dustboss_*` voice keys **don't exist** → yay + caption; 3 rounds × 3 taps in 0.75 s vulnerability windows (0.65 s at 1.25× speed final); mercy ladder from 5 misses (+5.5 s window, +4 reach, slower) | 40–90 s | The only skill-gated mechanic in the chapter is taught by text a non-reader cannot read, at an adult-grade first-encounter window |
| Chapter "end" | Boss win banner (+3 pearls) → `_clear_game` wipes `g` (`main.gd:8583-8584`) → `_leave_arena_now` teleports to `return_pos` in the **reef free-roam** (`main.gd:10827-10834`); `day_one_active` never clears, so all four doors go `BLOCKED`, jobs/opera stay locked | — | **The chapter has no ending**: the climax exits to an unrelated space and the castle locks behind her |
| Resume (any later session) | Continue → promenade x 610 → the same 4,702 px walk, castle re-entry, hall re-walk; the 3 hall bunnies respawn | 20–40 s tax | Mid-room progress restores beautifully; the retraversal tax fights the short-session pillar |

Total content: **roughly 4–7 minutes** of engaged play — a genuinely good
chapter length for the audience and the short-session rule (`DL-AGE-06`).

## 2. Pros — what the rough draft already does right

1. **Interruption safety is exemplary.** Immediate `_write_save()` on
   every completion edge, debounced saves on every step, derived-on-restore
   keys (`art_desk_unlocked`, `boss_door_glow` recomputed from parts —
   `day_one_director.gd:574-598`) so no mid-frame save can lose a reward.
   A nap, a battery death, or a grabbed tablet never costs progress.
2. **No-fail integrity holds everywhere.** `passive_progress: false` is
   real (valid-motion seconds, capped free taps, one-shot drain guard);
   the boss's mercy ladder is a textbook kindness curve; zero timers
   pressure the child anywhere outside the boss window.
3. **A real gesture curriculum.** Tap → circular scrub → tap → horizontal
   scrub → sweep → pull-down → rapid tap → bump-by-swimming, each taught by
   a continuous, non-feeding demonstration ghost (the bathroom demo hand
   is best-in-class; `day_one_bathroom_cleaning.gd:370-393`). This is a
   motor-skill ramp, not filler.
4. **Nonverbal storytelling through transformation.** Dirty→clean is told
   by the space itself: the pool's 17-step lighting lerp, grime alpha
   fades, castle dressing, the sick seahorse visible from phase 0 as a
   promise. This is the strongest channel in the chapter and it is
   perfectly non-reader-native.
5. **Clear macro structure.** One golden door at a time, blocked doors
   that flutter and redirect kindly, a linear room order a four-year-old
   can hold in her head, and picture-door handoffs.
6. **Right-sized chapter with an agency payoff** — 4–7 minutes ending in
   the attack customizer, the child's first owned choice.

## 3. Weaknesses — organized, with mechanisms

**A. The spoken layer is generic or absent (P1, `MA-PACE-001`).** Not one
day-one objective has an exact spoken cue (`DL-SND-01`/`DL-SND-13`
require it; `DL-AGE-01` forbids text as the only route). Every
instruction voices generic `roshan_talk` (1.05 s); several speakers have
no playable clip at all — `rumi_*` (the chapter's climax), bare
`roshan.ogg`, `daddy.ogg` (all Daddy Mermaid hints), `dustboss_*` (the
boss telegraph) — and fall to a pitched yay. One instruction is
*structurally* silent: "Scrub the sink in little circles!" always lands
inside a 0.38 s cooldown collision. The chapter currently works for a
non-reader only because the pointers and demos are strong; story,
wayfinding, and the boss's timing lesson are text-locked.

**B. Beats stack, overwrite, and skip their breaths (P2, `MA-PACE-002`).**
One caption slot + same-frame bursts: the inciting line at castle entry is
never readable; the bathroom opens on three captions in 0.4 s; the art
studio fires eight in a row with a voice repeat per tap. Missing
micro-wins: the sink completion goes straight to the next instruction in a
0.70 s busy-lock with no reward beat; the art room — the beat that arms
the boss door — completes in total silence; after Rumi's thank-you nothing
directs the child onward.

**C. The chapter has no ending and every session pays a travel tax (P1,
`MA-PACE-003`).** Winning the boss tears down to reef free-roam with the
castle closed behind her; `day_one_active` never clears, so the castle
becomes four `BLOCKED` doors and locked jobs with no narrative close.
Continue always respawns at the promenade for the full walk again.

**D. Assistance and difficulty ignore the house ladder (P2,
`MA-PACE-004`).** The repo already codified escalation (`DL-INT-08`'s
five- and ten-second assistance) — Day One uses none of it: no idle-gated
voice re-prompt exists anywhere in the castle (`_tick_roshan_reactions`
early-returns for `game != ""`), pointers are permanent rather than
earned, `SINK/TUB_MAX_GESTURE_SECONDS` are declared and never read, and
the boss opens at a 0.75 s reaction window (0.65 s final) — adult-grade —
with mercy arriving only after five misses, against `DL-INT-09`'s
no-required-reaction precedent.

**E. Beat honesty and polish debt (P3, folded into the findings above).**
The one-tap "supply hunt" celebrates a find the child didn't perform
(both tools pre-placed; the cabinet/drag route is dead code); "scrub" is
voiced where the input is a tap (the same verb IS a real gesture one room
earlier — a grammar inconsistency); "Tap the loose loose brushes!";
dead `_progress`/`_target`/`_swoosh` code; the phantom
`_clear_day_one_art_studio` call that refreshes a queue-freed node; a
step-4 pool save replays the whole Rumi reveal.

## 4. Improvement guide — prioritized, cheapest-first

1. **Voice the chapter (one TTS batch).** Add ~35 semantic lines to
   `tools/make_voices.py` LINES + a Rumi voice row (voice+pitch), and
   regenerate per-line: every instruction in section 5 of this document's
   flow list, Rumi's introduction, Daddy Mermaid's redirect, the four
   room-complete lines, next-destination lines, and the five `dustboss_*`
   keys. This single batch converts the chapter's whole communication
   layer from text-locked to spoken. (`MA-PACE-001`.)
2. **One voice channel.** `show_msg` is already the voice+caption entry;
   delete the dead trailing `_say` calls that its 0.5 s gap suppresses,
   and fix the two real defects: the art studio's uncooled repeat
   (min_gap 0.0 → drop the call) and the sink line's collision (announce
   after the tool travel *plus* the remaining cooldown, or voice it via
   its own semantic key which has no colliding cooldown entry).
3. **The one-breath rule at every beat.** Payoff (0.5–1 s, on the object,
   Juice vocabulary) → breath (~0.5 s) → one instruction. Concretely:
   queue castle entry's two lines through `say_sequence` (built, unused
   in Day One, touch-skippable); merge the bathroom's three openers into
   one honest line; announce art phases at boundaries only (3 lines, not
   8) with per-tap chime+pop instead of caption churn; give the sink its
   "Sparkly sink!" micro-win inside the existing 0.70 s busy window.
4. **Announce the macro transitions.** After each bespoke room completes:
   one next-destination line + the golden-door pointer ("Baby Eagle needs
   us! Follow the golden door!"). On the fourth room: the celebration the
   generic path already owns — "All four rooms are clean! The big back
   door is glowing!" — moved onto the real path, with a hall pointer at
   the royal mist. Silent arming is forbidden (`DL-PACE-04`).
5. **Give the chapter an ending (owner decision required).** Post-boss:
   return INTO the hall (not the reef), a short two-line close over the
   restored castle, and an explicit day-one-complete state — either
   `day_one_active` clears (jobs unlock as "day two") or a bedtime close
   with the next chapter gated. Any of these beats the current reef dump;
   which one is the owner's story call. (`MA-PACE-003`.)
6. **Kill the resume tax.** Once the dirty castle is discovered, Continue
   resumes at the castle door (or the hall) instead of promenade x 610;
   keep the full walk for the first arrival only. Suppress the pearl-plane
   guidance while Day One is active and undiscovered — point the opening
   at the castle instead ("Our castle needs us!").
7. **Install the assistance ladder chapter-wide (`DL-PACE-03`).** One
   helper on the announce system: idle ~8 s → re-speak the current
   instruction; ~16 s → refresh pointer/demo. The bathroom demo ghost and
   skimmer pointer already exist — this only adds the voice tier and
   idle-gates what is currently permanent.
8. **Retune the boss for first contact (`DL-PACE-05`).** Baseline
   vulnerability 1.2 s (final 1.0 s), narrowing toward today's 0.75/0.65
   on demonstrated success — invisible ramp instead of visible rescue;
   mercy stays as the floor. Voice the telegraph (item 1) and let the
   existing demo-flash window carry the lesson.
9. **Make the supply hunt true or shrink it.** Either two real finds
   (each tool a tap target, then the basket — the `MAX_SUPPLIES = 2`
   machinery already exists) or collapse to one honest beat ("Got the
   sponge and brush — let's clean!"). Fix "scrub the grime" by wording
   ("Tap the grime away!") or by reusing the bathroom's arc-gesture
   machinery on the counters. Fix "loose loose".
10. **Debt sweep (small, mechanical).** Remove dead `_progress`/`_target`/
    `_swoosh` and the phantom `_clear_day_one_art_studio` call; collapse
    the art path's double `_write_save`; guard the step-4 pool save
    against a second full Rumi reveal; append the register history for
    `MA-CI-004` (13 day-one probe files now exist; 3 run trusted — the
    other 10, including pool, director, art, and start-menu routing,
    still gate nothing).

Items 1–4 and 6–7 are documentation-light, engine-light, and reuse
machinery that already exists (`say_sequence`, the TTS pipeline, the
Juice vocabulary, the golden-door system) — least investment, highest
child-facing return, in the same spirit as the animation wing.

## 5. What enters the framework

- The **Pacing and session flow wing** (master audit section 3.4,
  Standing) with rules `DL-PACE-01`–`DL-PACE-06` (design 06 section 21):
  the one-breath beat template, session shape and resume-tax bounds, the
  idle assistance ladder, announced macro transitions, first-encounter
  reaction-window floors, and truthful beats.
- This is a prose-and-exemplar wing for now (taste and timing rule);
  its accepted exemplars are the pool's one-instruction-per-phase
  announcements and the bathroom's continuous non-feeding demonstration.
  A deterministic beat-lint (static scan for same-frame `show_msg`
  bursts) is a candidate follow-up checker, not yet claimed.
- **Findings** `MA-PACE-001` (voiceless semantic layer), `MA-PACE-002`
  (stacked captions, missing micro-beats, silent transitions),
  `MA-PACE-003` (no chapter close; resume retraversal tax), `MA-PACE-004`
  (assistance ladder absent; boss window vs. age), plus a history append
  to `MA-CI-004`.

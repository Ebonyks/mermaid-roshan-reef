# CHAPTER 2 — "Roshan Makes Her Own Birthday": review for discussion

**Status: DESIGN ONLY. Nothing below is implemented.** This is the review
document requested before any build. Full working papers (the chapter bible,
four floors of act scripts, the systems build plan — ~175k words) are in the
session analysis archive; this is the decision surface.

The one thing already built is the plumbing the story needs: `say_sequence`
(timer-advanced, touch-skippable, non-blocking spoken exchanges) shipped at
`a0fbdf33` because the game previously had ONE caption slot that overwrote
itself — two characters could never trade lines.

---

## 1. THE CHAPTER IN ONE PARAGRAPH

The castle is clean (Chapter 1) and it is Roshan's birthday. Princess Huluu
offers to have the whole party *made for her*; Roshan says no thank you — she
wants to make her own. So the thirteen Pearl Opera career shows become the
thirteen things her party needs, and she makes each one herself with a friend
who knows that job. The mischief imps — who have never been invited to
anything — sabotage each preparation, and the Imp Captain snatches each
finished piece and runs for the stage, where Roshan wins it back by
out-performing him. Every piece lands on a party table in the lobby. When the
table is full the party happens and she invites the imps. Then the **Ember
King** arrives, blows out her five birthday candles, takes them home to his
fire mountain, and dares her to come get them — which sends everyone north
(Chapter 3) and ultimately to the lava planet (Chapter 4).

## 2. THE SPINE, BEAT BY BEAT

**Chapter open (7 spoken lines, over the existing lobby).** Roshan announces
her birthday; Huluu offers to have it all made; Roshan refuses — *making it is
the joy she chose, not a chore*; the Maestro welcomes her ("thirteen shows,
thirteen party things"); she sees her empty party table; the Imp Captain
giggles offstage: "a party? WE love parties…" — the villains are planted
before act one.

**The loop, thirteen times.** Costume on -> into the painted world with a
helper -> make the piece at the painted stations -> the Captain steals it ->
win it back on stage -> it drops onto the party table.

**Imp escalation, one posture per floor** (this is what stops thirteen acts
feeling identical):
- **Floor 1 — PLAYING.** They just want to touch the party things. *"Is that
  for the PARTY? Let me hold it!"*
- **Floor 2 — COPYING.** They're building a rival party backstage out of a
  crate and a paper tablecloth; every steal now goes on *their* table.
  *"We're having our OWN party! You weren't invited either!"*
- **Floor 3 — FRANTIC.** They can hear the real party being laid out and hold
  pieces like a ticket. *"If we HOLD it, you have to let us come… right?"*

**The three bosses are the three things a party needs that aren't objects:**
the Curtain Dragon is **the place** (asleep in the curtains; he isn't evicted,
he's cast as doorman), the Shadow Phantom is **the light** (lighting his five
lanterns lights the whole floor), the Midnight Maestro is **the music** (he
has hosted every act since the chapter open; at his own act he finally stops
announcing and conducts). All three keep their shipped kind win-lines.

**The party (climax).** The shelf ripples to full colour, the Maestro
announces "Roshan's birthday party!", Huluu notes the whole reef came, Evie
says Lamba wants to sit next to the cake — and from the doorway, small: *"…Are
we invited?"* Roshan: **"Imps — you're invited."** The lesson is enacted,
never stated.

**The crash (cliffhanger).** The Ember King **is never seen** — a huge rumble,
one long puff, every light goes out. *"Nobody ever invited ME to a party. So I
shall take the candles."* He takes only the candles, hurts nobody, and dares
her to come to the fire mountain. The Imp Captain: *"We know him — our cousins
live at his gate."* Rosalina: the old folk in the far north know the way.
Roshan's last line of the chapter: *"Then we're going north — and I'm getting
my candles back."*

## 3. THE FIVE-CANDLE RHYME (the best find in the whole pass)

Three fives already exist in the shipped codebase and nobody connected them:
the Shadow Phantom act carries `"lanterns": 5`, the Ember Fortress objective
is `const LANTERNS := 5`, and the birthday wants candles. Wire them and the
chapter's spine becomes literal and childproof: **five lanterns lit here ->
five candles on the table -> five candles taken -> five lanterns to relight at
the fire mountain.** It costs no new mechanic, gives the shy phantom a reason
to exist ("the one who made the candles"), and gives Chapter 3 a second owner
— Roshan wants her candles back, the phantom wants his light back.

*Owner call:* if Roshan is turning four rather than five, the fifth candle can
be the King's own. The scripts are written agnostic, so either ruling stands
without a rewrite.

## 4. WHO DOES WHAT — the thirteen helpers

| Act | Piece made | Helper | The hook |
|---|---|---|---|
| Chef | the cake | **Kareem** (shopkeeper) | She walks into his cake shop on her birthday and tells him she does NOT want to buy one — then bakes hers beside his. A boxed shop cake sits on the cart all show as the road not taken. |
| Detective | the tiara crown | **Princess Huluu** | Huluu lends her own tiara as a birthday crown; it vanishes the moment it leaves her head. |
| Ballerina | the music box | **Rosalina** | A music box that only plays while somebody is dancing — she teaches Roshan the dance she'll dance at her own party. |
| Candymaker | the party bags | **Sparkle** (baby eagle, chirps only) | Sparkle keeps eating the party bags; the reveal is that nobody had given *her* one yet. |
| Doctor | the mended plushy guest | **Evie** | Evie's beloved starfish is torn; her posture on the sideline is the tension meter. |
| Farmer | the picnic | **Chuck** (real family recordings only) | A herding dog performance built entirely from his existing bark/whimper clips. One piggy, "Pudding", wears a party hat so a non-reader can find her among twelve. |
| Boxer | the champion's sash | **Wacky** | Grandpa corner-coach with a threaded needle — the belt gets *re-tailored* into a birthday sash. |
| Magician | the entertainment | **Evie + Lamba** ⭐ | The owner's own bar: Lamba is the vanishing subject, Evie watches from the stage lip with her hands over her mouth. |
| Painter | the decorations | **Flower Friend** | Silent muse — she poses, and the finished sunrise is *her* portrait. |
| Astronaut | the fireworks | **Mewsha** (meows only) | The cat in a fishbowl helmet. |
| Racer | the invitations | **Harper & Fiona** | The speed sisters as pit crew; `harper_win.ogg` already exists for the finish line. |
| Nursery | the star ceiling | **Nurse Faron** (shipped) | The one thing Roshan has never been good at: being quiet. |
| Pop Star | the microphone | **Daddy Mermaid** (existing clips only) | She finds out what a microphone is *for* when the imps unplug it. |

Sacred audio is honoured throughout: Daddy and Chuck appear using **existing
recordings only**, never new lines.

## 5. WHAT IT COSTS

**Voice — ~120 new Kokoro clips**, all in already-configured voices except
three new speaker slots. Generation is ~20-30 minutes on CPU, ~3 MB total.
- New speaking roles needing a voice assignment: **Ember King** (recommend
  `am_santa` — big, warm, theatrical), **Shadow Phantom** (recommend `af_sky`
  — soft and unmistakably *small*), **Imp Captain** as a distinct routing from
  the generic imp.
- Three `_speaker_key` branches are missing today, so those characters would
  silently speak in **Roshan's voice**: phantom, captain, and (already fixed
  by me) maestro/kareem.

**Graphics — 13 blocking + ~10 optional.** The whole floor-2 arc leans on
**one shared asset**: `dressing_imp_crate_table.png`, a packing crate with a
paper tablecloth parked in every floor-2 world, re-dressed four times
(bandage bunting -> muddy hoofprint -> paper crown -> taped curtain). One
asset, four acts, and the child reads the imps' entire motive without a word.
- **Highest value single card:** `lamba_partyhat.png` — Lamba in a tiny imp
  party hat, which proves the imps' motive at a glance five acts before the
  invitation pays off.
- Helper stage actors needed: Kareem, Rosalina, Evie (two poses — scrubs and
  stage), Wacky, Mewsha, Flower Friend, Sparkle; plus small story props
  (empty tiara cushion, torn starfish "before", party bag, five candles,
  Pudding's party hat, the boxed shop cake).
- **Reused, no new art:** every career backdrop, stage, actor, rival 13-frame
  set, all 13 goal props, the dragon GLB, `imp_captain_bow.png`.

**Engine — no new save keys.** The party table derives entirely from the
existing `opera_stars` bitmask; the thirteen shelf textures are the goal props
that already ship.

## 6. THREE DEFECTS FOUND (all would block or embarrass the story)

1. **Captions are invisible over the Opera lobby.** `hud_msg` sits on a
   CanvasLayer at layer 0; `OperaLobby2D` is layer 35 with an opaque
   backdrop. Every spoken line in the lobby — the entire chapter open, the
   party, the crash — currently plays audio behind an opaque panel. Fix is a
   mirrored caption label inside the lobby (~8 lines), not a global z-order
   change.
2. **The Shadow Phantom speaks in Roshan's voice** (no `_speaker_key`
   branch). Same class of bug would hit the Ember King and the Captain.
3. **Boxer, racer and pop star never visit their final station** — 6 phases,
   4 non-bop, 5 stations, so the last landmark is orphaned. In all three the
   orphan is *the pedestal holding that act's goal prop* — the birthday piece
   the painting was built around. One-line fix in `_assign_stations()`.

## 7. CHAPTER 5 IMPLICATIONS (decided now, cheaply)

Chapter 5 remixes these same stages harder and settles into a cozy,
revisitable endgame. Three consequences to honour while building Chapter 2:
- **Parameterize difficulty** rather than hard-coding goals, so the remix is
  a data pass and not a rewrite.
- **No one-shot-only story.** Beats must be replayable and shortenable (an act
  that already has its star plays a trimmed version).
- **Build the party venue as a place, not a cutscene** — the party table and
  the party scene should be a persistent space the child can return to, since
  Chapter 5 moves in there.

---

## 9. DAYS ARE THE CONTENT GATE (owner canon, 2026-08-03)

**Days are the narrative device that locks content behaviour walls.** Chapters
ARE days:

| Day | Chapter | Content |
|---|---|---|
| Day 1 | 1 | Clean the castle. Ends: the dust bunnies are shooed, the giant one is beaten, **everyone goes to bed.** |
| Day 2 | 2 | **Getting ready for the party** — the thirteen career shows — then the party itself, then the Ember King's crash. |
| Day 3 | 3 | North, for information on how to stop them. |
| Day 4 | 4 | The lava planet. |
| Day 5 | 5 | The ultimate party; settles into the cozy endgame. |

### What already exists (better than expected)

**The chapter transition is already built.** `main.gd:_begin_sleep()` is a
complete tuck-in cutscene: Roshan snuggles onto the castle bed, "z"s float up
with descending lullaby chimes, the screen dream-fades to indigo, the
"Sleepyhead" sticker is awarded, and *A Place I Call Home* plays. Chapter 1's
"everyone goes to bed" is therefore not new work — it is the existing bed
interaction, and **sleep is the chapter boundary**.

The dust-bunny cleaning and the giant dust-bunny boss also already exist
(`combat_arena.gd`, `dust_bunny_boss_sprite.gd`).

### What does NOT exist — the one foundational gap

**There is no day counter.** `is_night` today is cosmetic only: it flips on
every launch (`plays % 2`) and again on each sleep, driving music and lighting.
Nothing persists "which day/chapter am I on", and there is no castle-clean
completion key in `KNOWN_KEYS`.

So the foundational build item for Chapter 2 — before any story content — is:

1. **A `story_day` save key** (int, default 1). Adding a key with a default is
   explicitly permitted; no existing key is touched, and old saves migrate by
   defaulting to day 1 (or by inferring day 2+ from existing progress flags so
   current players aren't demoted).
2. **Sleep advances the day** *only when the day's objective is complete* —
   Day 1 advances once the giant dust bunny is beaten. Sleeping early stays the
   existing cosy nap (it already awards its sticker), so nothing is lost.
3. **Content gates read `story_day`.** The Opera career shows become available
   on Day 2; the north opens on Day 3; and so on. This is the "behaviour wall"
   the owner describes, and it gives every chapter a clean, testable condition.

### A free win this unlocks

Chapter 2 spans one day — morning preparation, evening party. The existing
`is_night` / `_apply_time_of_day()` machinery can carry that arc: **the Opera
lobby warms toward evening as the party table fills.** Thirteen pieces made =
sundown = the party. No new system, and the child feels the day passing.

### Consequence for the Chapter-1 handoff (my question 5, answered)

Chapter 1 should end on the beaten giant and the tuck-in, with the party named
in the last lines before sleep ("tomorrow is my birthday — tomorrow we get
ready"). Day 2 then opens on waking, which is where this chapter's seven-line
open begins. The two chapters lock together through the bed, not through a
menu.

---

## 10. WHERE THE SHOWS LIVE — distribute them through the castle (owner direction)

**Problem with the current gating:** all thirteen shows sit behind one Opera
House menu, three floors of cards, unlocked in floor order. That is a menu, not
a home, and it wastes the castle the child just spent Chapter 1 learning.

**Direction:** mix the shows through the castle so each room promotes the jobs
that belong to it — the Opera Hall hosting the ballerina and pop star makes
sense; the kitchen should promote the baker and the candy maker.

### The castle already has exactly the rooms this needs

Thirteen rooms are shipped (`castle_rooms_25d.gd` ROOMS): main hall, opera
hall, royal kitchen, royal library, stuffie playroom, craft room, mermaid
pool, bubble bath, family dining room, royal bedroom, sleepover bedroom, cloud
movie lounge, dream house wing — plus the courtyard outside. Thirteen careers,
and the thematic fit is close to one-to-one:

| Room | Shows it promotes | Why |
|---|---|---|
| **Royal Kitchen** | **Pastry Chef, Candy Maker** | the cake and the sweets are literally made here |
| **Opera Hall** | **Ballerina, Pop Star, Magician** | the three performances; also the boss stage |
| **Royal Library** | **Detective** | clue archives, evidence shelves, quiet searching |
| **Craft Room** | **Painter** | the decorations, made where crafts are made |
| **Stuffie Playroom** | **Stuffie Surgeon (doctor), Boxer** | the patients ARE stuffies; the toy ring is play-fighting |
| **Bubble Bath** | **Nursery Nurse** | bath-time, babies, Faron's own domain |
| **Mermaid Pool** | **Astronaut Engineer** | the bubble rocket launches through water |
| **Family Dining Room** | **Farmer** | the picnic food for the party table |
| **Cloud Movie Lounge** *or courtyard* | **Racer** | the big-screen grand prix / the outdoor track |
| **Main Hall** | *(no show)* | **the party venue itself** — where the table fills and the party happens |
| Bedrooms | *(no show)* | **the day boundary** — sleep, per section 9 |

That is 2+3+1+1+2+1+1+1+1 = **thirteen shows**, every room with a job earning
its place, and the two bedrooms and main hall carrying the story instead.

### What this changes

- **The Opera House stops being the hub and becomes one venue among many** —
  the Opera Hall room, hosting its three stage careers plus the boss stage.
  The existing 2D lobby stays useful there (three performance cards + the
  finale card) rather than being the front door to all thirteen.
- **Gating becomes spatial and thematic, not a floor ladder.** She wanders her
  home on her birthday and each room offers what it can contribute. A room's
  card can be marked done once its piece is on the party table.
- **The party table moves to the Main Hall**, which is where the party
  happens, where the Ember King crashes it, and — per Chapter 5 — the cozy
  endgame lives. It becomes a place she returns to, not a menu strip.
- **Progression** keys off the party table (thirteen pieces) rather than floor
  stars; the three bosses can gate on counts (e.g. the Curtain Dragon wakes
  once the first four pieces are home) instead of floor completion.

### What it costs and what it does NOT cost

- **Save compatibility is intact.** `opera_stars` remains the thirteen-bit
  record of which pieces are made; only the *presentation* moves. No key is
  removed or repurposed.
- **No new career content.** All thirteen painted worlds, stages, widgets,
  actors and props are already built and unchanged — this is a navigation and
  framing change.
- **Rooms need a job affordance:** each participating room needs its show
  entry point (a themed hotspot/card in the room's existing 2.5D card stage)
  and one line of dialogue. That is the main build cost.
- **Open question:** the racer is the one awkward fit (movie lounge vs
  courtyard). The courtyard is outdoors and already exists as the castle's
  exterior — it may be the better home for both racer and farmer if we would
  rather keep the dining room purely for the party feast.

### Why this is better for the child

She is not choosing "act 7 of 13" from a menu. She is walking around her own
home on her birthday, and every room has something to make. It also makes the
imps' floor-2 "copying" arc physical — their crate table can appear in the
rooms they have raided.

---

## 8. DECISIONS I NEED FROM YOU

1. **Is Roshan turning four or five?** (Decides whether the fifth candle is
   hers or the Ember King's; scripts work either way.)
2. **Ember King as the party crasher** — confirm. He is existing canon (all
   growl, zero bite; his shipped ending is friendship), needs no new art
   because he is never seen, and his imps already guard his gate.
3. **The Maestro as house host from act one** — confirm. It makes his own
   act land ("the one staff member never allowed on stage") and mirrors the
   imps exactly.
4. **Art budget:** approve the 13 blocking cards, or approve the minimum set
   (crate table + Lamba party hat + the seven helper actors) and defer props.
   Note the room-distribution change (section 10) adds a small per-room job
   affordance but removes nothing.
6. **Room mapping (section 10):** confirm the thirteen-show placement, and
   rule on the racer — cloud movie lounge, or the outdoor courtyard alongside
   the farmer?
5. ~~Chapter-1 handoff~~ — **ANSWERED (see section 9):** chapter 1 ends with
   the giant dust bunny beaten and everyone going to bed; the party is named
   in the last lines before sleep. Days are the content gate, so the real
   question is now: **approve adding the `story_day` save key** (default 1,
   no existing key touched) as the foundational build item, and confirm that
   current saves should be inferred forward rather than demoted to day 1.

Once these are settled the build order is: defect fixes -> `opera_story.gd`
data + hooks -> TTS generation -> party table -> codex art handoff.

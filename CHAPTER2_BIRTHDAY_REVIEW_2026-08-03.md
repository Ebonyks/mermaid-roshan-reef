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

## 11. NO FORCED FITS — jobs may serve the game in other ways (owner direction)

**Rule: do not force a job into the party-prep frame just to complete the set.**
If a career does not have an honest reason to be birthday preparation, it is
better used elsewhere — or excused from this chapter entirely. Not every job
has to be represented in every phase of the game.

**The worked example — the RACECAR DRIVER is a transition, not a party job.**
"Roshan makes a shell trophy for her party" is a weak reason to exist. What
the racer is genuinely good at is *movement*: getting from one place to the
next. So the driver becomes the chapter's **transport character** — the
interstitial that carries her between stages — rather than a thirteenth
contribution. This also gives the chapter a rhythm device it currently lacks
(a short, fast, low-stakes beat between two long careers) and it scales
naturally into Chapter 3's journey north.

Supporting tech already exists: the legacy race path delegates to `KartGame`,
`slide_race.gd` ships, and the Fable kit includes train and station models
used by the northern kingdom.

**The three candidate categories for any weak-fitting job:**
1. **Party contribution** — it meets a real guest need (the core set).
2. **Structural role** — transitions, traversal, interstitials, or the hub
   itself (the racer; potentially the astronaut, whose rocket may serve
   Chapter 4's departure better than a birthday firework).
3. **Excused from Chapter 2** — it keeps existing as playable content without
   being load-bearing in this chapter's plot, and may headline a later day.

**How this changes the review:** the party-function pass (in flight) was asked
to flag every weak or redundant contribution and rank all thirteen by how
legible they are to a four-year-old. Those flags are now *permission slips*,
not problems to solve — anything at the bottom of that ranking gets reassigned
to category 2 or 3 rather than being argued into the party.

**Consequence for the party table:** it no longer needs exactly thirteen
slots. The table holds however many pieces the honest set produces, and the
remaining rooms/careers stay available as play without pretending to be
preparation. This is also healthier for Chapter 5, which revisits the stages
as cozy content rather than as a checklist.

---

## 12. THE CAREER ROSTER IS A DESIGN VARIABLE (owner direction)

Two further permissions change how section 11 resolves:

**Chapter 5's extended universe is the home for excused careers.** New
characters and environments arrive there, so a career that has no honest place
in a birthday party is not orphaned by being excused — it is *deferred*. A job
that makes no sense as party preparation can make excellent sense once the
extended universe supplies the context for it. "Excused from Chapter 2" is
therefore a scheduling decision, not a deletion.

**Careers may be added or removed.** The thirteen are not fixed. This inverts
the design question in the most useful way:

> Stop asking "how do these thirteen careers serve a birthday party?" and start
> asking "what does Roshan's birthday party actually need — and which careers
> serve it?" Then keep, defer, repurpose, or *invent* accordingly.

### How this resolves the party-function pass

The taxonomy work (in flight) derives party needs from the guest's point of
view and was already asked to flag (a) needs with no job covering them and
(b) jobs whose contribution is weak or redundant. Under this direction both
outputs become actionable rather than awkward:

| Finding | Old response | New response |
|---|---|---|
| A job's party role is weak | argue it into the party | **repurpose** (structural, like the racer) or **defer to Chapter 5** |
| A real party need has no job | ignore it, or stretch a job to cover it | **add a career** that owns it honestly |
| Two jobs serve the same need | keep both, blur them | **keep the stronger**, defer or differentiate the other |

### What this is likely to produce (to be confirmed by the taxonomy)

- A **smaller, tighter Chapter 2 set** where every career has an unarguable
  reason to exist, rather than thirteen of varying strength.
- **Possibly no new careers at all.** Before inventing, check the existing
  roster and the boss-staff — the obvious "missing" party jobs are already
  owned:
  - *Decorating the hall* -> **the PAINTER**. This is his real party role
    (owner ruling): not "a framed sunrise on the wall" but **making the room
    look like a party** — banners, colour, the space transformed. That is an
    unarguable contribution a four-year-old reads instantly, and it upgrades
    the painter from a weak prop-maker to one of the strongest jobs in the
    chapter.
  - *Greeting and seating the guests* -> **the CURTAIN DRAGON**, already cast
    as the party's doorman in the bible.
  - *Lighting the room* -> **the SHADOW PHANTOM**, already the lantern-lighter
    (and the origin of the five candles).
  - *Wrapping and handing out favours* -> **the CANDY MAKER**, whose piece is
    literally wrapped sweets in party bags.
  So an addition must clear a high bar: a real guest need that no career and
  no boss-staff role already covers.
- **A deferral list for Chapter 5**, which arrives with the new characters and
  environments that give those careers their proper context.

### Cost note

Removing or deferring a career costs nothing — the built content stays in the
repo and stays playable; only its plot role changes. **Adding** a career is the
expensive direction (painted world, stage, actor, rival set, widgets, voice),
so any addition should be justified by a party need that no existing career
can honestly meet, and should be weighed against simply re-skinning an
existing career's framing.

---

## 13. THE CAREERS RUN ACROSS CHAPTERS 2-5 (owner clarification)

**The jobs are not Chapter 2 content.** They exist through chapters 2, 3, 4
and 5, and the design is revisited each time. Chapters **2 and 5 both take
place at the castle**, so those two are the same place seen twice — which is
exactly why Chapter 5 works as a remix.

| Chapter | Place | What the careers mean there |
|---|---|---|
| 2 | **Castle** | **Preparation** — each job makes something the birthday party needs. |
| 3 | North | **Journey and investigation** — the same skills used to travel and to learn how to stop the enemies. |
| 4 | Lava planet | **The confrontation / the rescue** — the same skills under pressure, to win the candles back. |
| 5 | **Castle** | **Celebration** — the ultimate party; the jobs return to their party roles, harder, and settle into the cozy endgame. |

### What this corrects in sections 11-12

"Excused from Chapter 2" does **not** mean "shelved until Chapter 5." A career
with a weak party role may well be a *strong* Chapter 3 or Chapter 4 job — so
the right question per career is not "does it fit the party?" but:

> **What is this career's arc across the four chapters, and which chapter is
> its home?**

The racer illustrates it: as party preparation he is weak, but as *movement*
he is load-bearing in Chapter 3's journey north, useful as Chapter 2's
transition between stages, and a natural race event in Chapter 5's cozy
castle. His home is the journey; Chapter 2 borrows him.

Likewise the astronaut's rocket probably belongs to the departure in Chapter 4
rather than to a birthday firework — though a firework is an honest party need,
so he may legitimately serve both, with the launch meaning something different
each time.

### The design consequence

Each career wants a **one-line arc** across the four chapters before Chapter 2
is finalised, so that its Chapter 2 framing is chosen to *set up* its later
role rather than to close it off. That is cheap to write now and expensive to
retrofit later.

It also means Chapter 2 does not have to carry all thirteen at full weight. A
career can appear in Chapter 2 in a **light** form (a cameo, a transition, a
single beat) and take its full form in the chapter where it belongs — which is
a better use of the same built content than thirteen equal-weight party jobs.

### And it makes Chapter 5 concrete

Chapter 5 is the same castle, the same rooms, the same jobs — the party that
finally happens without being ruined. That is why the party venue must be
built as a **place** (section 7): Chapter 5 moves back into it. The remix is
"everything you learned, in the home you know, with everyone invited."

---

## 14. THE ASTRONAUT ENGINEER SENDS THE INVITATIONS (owner ruling)

**Her party role: she designs the invitations and launches them to her friends
by bubble-rocket — early in the process.**

This is the strongest single fit in the chapter, and it settles several open
questions at once:

- **It is an honest job, not a forced one.** A rocket's whole purpose is
  *sending something far away*. Invitations are the one party item that must
  travel. A four-year-old joins those two ideas instantly.
- **It replaces the weak "birthday firework" framing** and frees the rocket's
  *departure* meaning for Chapter 4, where the same launch means leaving for
  the fire mountain. Same skill, different stakes — exactly the cross-chapter
  arc section 13 asks for.
- **It removes the racer from invitation duty.** The racer stays the
  transition character (section 11); the astronaut owns invitations. No job
  does double duty and neither is forced.
- **The room already fits:** the Mermaid Pool, where bubbles rise and carry
  things up and away.

### It is the chapter's FIRST act (an ordering constraint)

Invitations go out before anything else — that is simply how a party works,
and a child knows it. So the astronaut act should be the chapter's opening
job, either as the only one available at first or as the strongly-guided
first choice. The rooms stay freely visitable afterwards.

### It creates the chapter's central interlock: THE GUEST COUNT

Sending the invitations **establishes how many friends are coming**, and that
number then drives the other jobs:

- the **candy maker** fills a party bag for every guest,
- the **farmer** packs that many picnic portions,
- the **pastry chef** bakes a cake big enough to share out,
- the **nursery nurse** knows how many little ones need settling,
- the **painter** knows how big the hall must be dressed,
- and the **detective** notices when an invitation comes *back* — a guest who
  did not reply is a guest who might be missing.

That is the dependency web the interlock pass was asked to design, and it now
has a natural source: one number, established in act one, felt everywhere
after. It also gives the imps a motive with teeth on floor 1 — an invitation is
the one party item that is literally *a ticket*, and they never got one.

### Phase mapping (existing beats, no mechanical change)

The shipped astronaut phases carry it as-is: **PIPES** routes the bubble
tubes, **PATCH** seals the leaks, **VALVE** pressurises, **BOOST** builds
thrust, **LAUNCH** sends them off — the invitations fly to every friend. The
goal prop (`goal_astronaut`, the rocket) stays; what changes is what the child
understands it is *for*.

**Open sub-question:** should the child see *who* the invitations go to — i.e.
does the launch beat name the guests as they fly out (Huluu, Evie, Wacky,
Harper and Fiona...)? That would make the guest list explicit, set up every
later callback, and cost only voice lines. Recommended.

---

## 15. THE RECONCILED PARTY-ROLE MAP (the answer to "why does each job make the party better?")

Derived from first principles by walking one guest through one party, then
reconciled with the owner rulings in sections 11-14. Working papers:
`CHAPTER2_PARTY_ROLES_2026-08-03.md`.

**The governing rule this establishes:** a job does not earn its place by
producing an object. It earns its place by **meeting a need a guest would
otherwise feel**. So every act gains one extra spoken line — the *function
line* — delivered right after the piece lands on the table.

### 15.1 The fifteen things a party needs, in a guest's own words

| # | The felt need | Owned by |
|---|---|---|
| 1 | "Somebody has to come and TELL me." | **Astronaut** (owner ruling: invitations by rocket) |
| 2 | "Somebody has to open the door and be GLAD it's me." | Curtain Dragon *(staff)* |
| 3 | "I have to be able to SEE." | Shadow Phantom *(staff)* |
| 4 | "Somebody has to say when it's time." | Midnight Maestro *(staff)* |
| 5 | "Everybody has to HEAR — even me at the back." | Pop Star |
| 6 | "The second I walk in it has to LOOK like a party, not a room." | **Painter** (owner ruling: decorates the hall) |
| 7 | "I have to know WHOSE birthday it is." | Detective |
| 8 | "Nobody goes hungry — not even the animals." | Farmer |
| 9 | "There has to be CAKE." | Pastry Chef |
| 10 | "There has to be something to DO." | Ballerina (dancing) + Boxer (the wild half) |
| 11 | "There has to be something to WATCH if I don't join in." | Magician |
| 12 | "If I'm little or sleepy I need somewhere soft — and still to be AT the party." | Nursery Nurse |
| 13 | "If I'm torn or hurt or broken, I still get to come." | Stuffie Surgeon |
| 14 | "I go home with something in my hand." | Candy Maker |
| 15 | "Somebody has to get me there." | **Racer** — *structural, not a table piece* (section 11) |

**SUPERSEDED BY SECTION 16:** needs 2, 3 and 4 were assigned to the three
floor bosses. That assignment was a retrofit, the bosses are cut, and those
three "needs" turn out not to be real gaps — the Main Hall is the place, the
lights are on, and the timing belongs to Roshan and her friends.

### 15.2 Two needs no job can meet — and that is the point

- **"The one moment we all share"** — the candles, the wish, the song. No job
  makes it; it only happens when everything else is in place. **This is
  exactly what the Ember King takes.** He does not steal an object; he steals
  the only thing nobody could make.
- **"Being wanted when nobody ever invited you"** — the imps' whole arc, paid
  off by the invitation at the climax, and the Ember King's own motive
  ("nobody ever invited ME").

### 15.3 Per job: role, who it serves BY NAME, what breaks

The specificity is the point — a named guest with a concrete problem, not
"everyone."

| Job | The role | Serves | Breaks without it |
|---|---|---|---|
| **Astronaut** | the one who tells everybody it's happening | **Wacky** (lives furthest out, slowest) | half the chairs are empty; Wacky knocks the next morning asking when the party is |
| **Pastry Chef** | makes the thing that turns a day into a birthday | **Evie** ("Lamba wants to sit next to the cake!") | nowhere to put the candles — no wish, no song, a table with nothing in the middle |
| **Candy Maker** | makes sure nobody goes home empty-handed | **Sparkle** (she kept eating the bags because nobody made her one) | guests leave with nothing and Sparkle eats the tablecloth |
| **Painter** | makes the hall LOOK like a party before anyone speaks | **the Flower Friend** (silent — the decorations are how she is present) | it is just the main hall with food in it |
| **Ballerina** | makes sure there's something to DO | **Princess Huluu** (a princess with nothing to do stands politely all evening) | music plays and everyone stands in a ring looking at their feet |
| **Magician** | gives the non-dancers somewhere to look | **Kareem** (the grown-up at the edge with a cup) | the shy and the grown-ups drift to the walls and leave before cake |
| **Detective** | makes sure everyone can tell whose birthday it is | **the imps** (they arrive last, having never met her) | guests wish the wrong mermaid; Roshan is a guest at her own party |
| **Farmer** | makes sure nobody goes hungry, animals included | **Chuck** (a dog with no dinner goes for the cake) | Chuck reaches the cake first |
| **Boxer** | the wild half of "something to do" — the party games | the big kids who won't dance | the energy has nowhere to go and ends in tears |
| **Nursery Nurse** | keeps the littlest guests happy AND present | the babies (and every grown-up holding one) | the little ones cry and their grown-ups take them home early |
| **Stuffie Surgeon** | makes sure the broken ones still get to come | **Lamba** (torn) | a guest is left on a shelf |
| **Pop Star** | makes sure everyone can hear | the guests at the back | the song happens for the front row only |
| **Racer** | **structural** — movement between stages; his home is Ch3 | — | (not a table piece) |

### 15.4 The interlock: one number, established first, felt everywhere

The astronaut sending invitations **fixes the guest count**, and that number
drives the rest — party bags, picnic portions, cake size, how many little ones
to settle, how big the hall must be dressed. It also gives the detective a
thread (an invitation that comes *back* is a guest who might be missing) and
gives the imps a motive with teeth on floor 1: an invitation is literally a
ticket, and they never got one.

**Order-independence rule** (rooms are freely visitable): a callback line only
fires if the referenced piece is already on the table — read straight from the
`opera_stars` bitmask — otherwise a neutral variant plays. No sequencing is
enforced beyond the astronaut going first.

### 15.5 Two framing fixes the analysis surfaced

- **The magician's piece is an event, not an object.** What lands on the table
  should be the magician's hat **with Lamba coming out of it in a party hat** —
  which is the already-approved `lamba_partyhat.png`, doing double duty as the
  imps' motive plant.
- **Pudding must never read as food.** The farmer's fed piggy comes to the
  party as a *guest* in a party hat. That also cleanly separates the farmer's
  "everybody eats" from the chef's "the one cake we share."

### 15.6 Recommendation on the roster

**No new careers.** Every honest party need is owned by an existing career or a
reformed boss. The only career without a table piece is the racer, and he has
a better job (section 11). Chapter 2 therefore carries **twelve party
contributions plus one structural career**, with each career's full
cross-chapter arc (section 13) still to be written in one line apiece.

---

## 16. CUT THE THREE FLOOR BOSSES (owner ruling) — and my error in section 15

**Ruling: the Curtain Dragon, Shadow Phantom and Midnight Maestro are cut.
They serve no role in the greater narrative.**

**I got this wrong in section 15 and the correction matters.** I wrote that the
three bosses owning "the place, the light, and the time" was "the elegant
part" — the former enemies holding the party together. That was not a finding;
it was me **retrofitting a justification onto legacy content**, which is
precisely the forced fit section 11 forbids. The tell was there in plain sight:
their needs were the only ones I had to *invent a category* for. A real party
need is felt by a guest ("I go home with something in my hand"); "someone must
own the concept of time" is an adult abstraction I reverse-engineered.

### Why cutting is correct

- **They are artifacts of the abandoned hub.** They exist to gate *floors* of
  an Opera House lobby. With the shows distributed through castle rooms
  (section 10) there are no floors to gate, so their only structural job is
  gone.
- **They connect to nothing.** The chapter's antagonist is the Ember King and
  his imps. The dragon, phantom and maestro belong to no chapter's plot, set
  up nothing, and pay nothing off across chapters 2-5.
- **They are the last live 3D content in the opera.** Every career show is 2D;
  `kind == "boss"` is the *only* remaining path that builds the 3D proscenium,
  avatar, camera and HUD. Cutting them retires that entire branch.

### What cutting frees

The largest simplification available in this system: the boss engine plus the
3D theatre scaffolding it alone keeps alive (roughly the `_build_theatre`,
`_build_avatar`, `_build_camera`, `_build_hud`, boss engine and dressing
regions of `opera_act.gd`). Three acts removed, one whole rendering path
retired, and `opera_act.gd` collapses toward the 2D router it effectively
already is.

### What it costs — the one real risk

**Save compatibility.** `opera_stars` is a 16-bit mask where bit *i* is
`ACTS[i]`, `ALL_STARS = (1 << 16) - 1`, and floor unlocks hardcode bits 4 and
9. Removing three entries **renumbers every act after them**, so an existing
save would credit the wrong shows. This is the "never break saves" rule, so it
needs a deliberate migration: keep the mask's meaning stable by either
retiring the three bits in place (leave gaps, so surviving acts keep their
indices) or writing a one-time remap. **Retiring in place is the safer of the
two and costs nothing at runtime** — the bits simply go unused and
`ALL_STARS` becomes the mask of the thirteen live acts.

Probe updates follow from that: `probe_opera.gd` asserts sixteen acts, one
boss per floor, bosses at 5/10/15, and `opera_progress == 16`; those
assertions describe the structure being removed and would be rewritten, not
patched.

### What needs rehoming (small)

- **The five-candle rhyme** loses one leg — the Shadow Phantom's `"lanterns": 5`.
  It survives intact and arguably cleaner: **five birthday candles (Ch2) → five
  ember lanterns to relight (Ch4)**, a direct chapter-to-chapter rhyme with no
  middleman.
- **The three "needs"** they owned are not real gaps: the Main Hall *is* the
  place, the lights are simply on, and the party's timing belongs to Roshan and
  her friends. No replacement content is required.

### Open question

**Cut or defer?** Deleting the acts is free (section 12: built content can stay
in the repo unused), and the dragon/phantom/maestro art and GLBs already exist.
If the extended universe of Chapter 5 could use a theatrical dragon or a shy
phantom as *characters* rather than boss fights, they cost nothing to leave on
the shelf. My recommendation: **cut them from the chapter structure now**
(remove the acts, retire the bits, delete the 3D boss path) and keep the art in
the repo for later reuse as characters.

---

## 17. THE ANTAGONIST STRUCTURE: EMBER KING + EMBER PRINCE (owner ruling)

**Primary antagonists: the EMBER KING and the EMBER PRINCE. Boss fights are
their henchmen.**

This supersedes section 16's "cut the bosses and have no boss fights." Boss
fights *stay* — they simply belong to the real villains instead of to three
characters imported from an opera that no longer exists.

### On the dragon, phantom and maestro

No objection to them existing in the story **if** they can be introduced
elegantly — but they are not part of the standard Mermaid Roshan story and
integrating them takes effort that buys little. So the ruling stands: **they
are not boss fights.** They stay in the repo as art. If a later chapter finds a
graceful use for a theatrical dragon or a shy phantom as *characters*, the
assets are there; nothing is spent keeping that door open.

### The Ember Prince is the key addition

A **child-scale antagonist** is exactly what Chapter 2 was missing, and he
solves a problem the Ember King alone could not:

- **The King is an endgame threat** — a mountain that talks, saved for Chapter
  4. Using him as the party-crasher spends the final boss in act one of the
  story.
- **The Prince is Roshan's counterpart.** A kid who wasn't invited to another
  kid's birthday and wrecks it is the most legible villain motive a
  four-year-old will ever meet — she has *lived* that feeling from both sides.
- It also gives the imps a boss they plausibly report to, and it lets the
  King's own line ("nobody ever invited ME to a party") land in Chapter 4 as
  the *father's* version of the son's grievance. The two antagonists rhyme.

**Recommended split:** the **Prince crashes the birthday party** (Chapter 2
climax) and takes the candles; the **King** is the power behind it, met in
Chapter 4 when she goes to get them back. Chapter 3's journey north is where
she learns who the Prince's father actually is.

### Henchmen as boss fights — the content already exists

The Ember Fortress ships with exactly this cast and structure: **"Cinder Gate
Imps"** (4 enemies), **"Ash Imp Ambush"** (6 enemies), and **"The Molten
Throne"** (a dual fire/ice boss with `boss_hp`, peek/shell phases) — plus
`ember_imp.glb`, `ember_boss.glb` and a full arena kit. So henchman bosses are
not new content to invent; they are existing ember content promoted into the
role the opera bosses were wrongly filling.

**For Chapter 2 specifically:** one or two ember henchmen appearing at the
castle would (a) prove the threat is real before the party, (b) explain how
the mischief imps got organised, and (c) make the Prince's arrival at the
climax feel prepared rather than sudden. That is a genuine narrative role —
unlike the floor bosses, these earn their place.

### What this changes in the plan

- **Sections 15-16 stand corrected:** boss fights exist; they are ember
  henchmen, not opera characters. The three "needs" the opera bosses held
  remain non-gaps (the Main Hall is the place, the lights are on, timing
  belongs to Roshan).
- **The crash script (bible §5) is re-cast** from Ember King to Ember Prince,
  with the King named but unseen — which *strengthens* the existing "never
  seen, never frightening" design and saves his reveal for Chapter 4.
- **The five-candle rhyme survives** and gets better: the Prince takes the
  five candles to his father's mountain, where five ember lanterns must be
  relit.
- **Save/probe migration is unchanged** — the three opera boss acts still
  retire in place (bits kept, indices stable); henchman encounters slot in as
  new content rather than renumbering anything.

### Open questions

1. **How many henchman bosses in Chapter 2, and where?** My recommendation:
   two — one mid-chapter (the imps get organised) and one just before the
   party — staged in castle rooms rather than a separate venue.
2. **Does the Ember Prince appear before the climax?** A brief early sighting
   (watching from a window, unimpressed) would plant him cheaply. My
   recommendation: yes, once, wordless.
3. **Art needed:** the Prince has no assets. He needs a design — the one
   genuinely new character this chapter requires, and worth commissioning
   properly since he carries Chapters 2-4.

---

## 18. THE MIRROR IMPS ARE THE SPINE (owner ruling) — already built, barely used

**There is an imp in an identical costume matching Mermaid Roshan for every
single career. This must be a key part of every one of these processes.**

Verified in the repo: **156 rival files** — all twelve careers, each with a
full thirteen-state set (`rival_chef.png` plus `_bopped, _bow, _charge, _flee,
_guard, _hop_a, _hop_b, _recover, _slash, _stagger, _taunt, _windup`) against
Roshan's 13 costumed actors. Chef imp in a toque, detective imp in a
deerstalker, ballerina imp in a tutu — a complete shadow cast, fully animated,
**already delivered**. The game currently spends it on "a rival appears at the
finale."

### What the mirror actually means (the story it was always telling)

The imps are not random thieves. **They are copying her, job for job, costume
for costume.** Everything she makes, an identical imp is making beside her.
That single image explains the whole chapter without a word of exposition:

- **Why they steal each piece** — not mischief, *procurement*. They are
  assembling a duplicate party, one stolen piece at a time.
- **Why there is a rival in every act** — because the copy needs a chef, a
  painter, a magician too. The finale isn't a random duel; it is her catching
  the imp doing her job.
- **Why the invitation resolves it** — a copy exists because someone wanted the
  real thing and could not have it. Inviting them makes the copy unnecessary.
  The lesson is enacted by the *structure*, never spoken.

### This promotes the bible's floor-2 "COPYING" posture to the whole spine

The bible staged copying as one floor's escalation with a crate-table prop.
That is now the chapter's **through-line from act one**, and the escalation
becomes how *good* the copy gets:

| Stage | The copy | What the child sees |
|---|---|---|
| Early | clumsy imitation — wrong hats, upside-down tools | funny |
| Middle | a working duplicate — their crate table has real pieces on it | uh-oh |
| Late | nearly as good as hers, and *nearly convincing* | genuinely tense |
| Party | the copy is abandoned the moment they are invited | the payoff |

### It hands the Ember Prince his entire characterisation for free

If the imps copy Roshan job-for-job, then **the Prince is the copy of Roshan
herself** — a child throwing his own party because he was not invited to hers.
The costumed imps are *his* court doing what he ordered. His crash at the
climax is the copy's final act: if he cannot have a party, nobody can. And it
sets his Chapter 4 father as the origin of the grievance.

That is a complete antagonist arc derived entirely from art that already
exists — no new character logic required, only the Prince's own design.

### Consequences for the plan

- **Every act should show the mirror early**, not just at the finale. The
  costumed imp should be visible doing her job badly somewhere in the act
  before he steals the piece — the shipped `_taunt`, `_hop`, `_windup` and
  `_flee` states are exactly the vocabulary for that, and the roaming stage
  combat already places imps in the painted world.
- **The party table gains a shadow.** The imps' crate table can hold *their*
  version of each piece taken — visible, wrong, sad. It is the strongest
  single image available for the invitation payoff, and it costs one prop.
- **The stolen piece is never destroyed**, which the design already assumes —
  it is *displayed* on their table, so winning it back reads as reclaiming
  rather than repairing.
- **Chapter 5 inherits it:** at the ultimate party the imps are guests, and
  their thirteen costumes become fancy dress rather than counterfeit — the
  same 156 files, re-read.

### Recommendation

Make the mirror explicit in the chapter's opening minute (the child should see
one costumed imp copying her *before* the first theft), and let it carry the
imp arc end to end. It is the highest-value narrative change available,
because the art is already finished and currently underused.

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
6. **Room mapping (section 10):** confirm the placement, noting the racer is
   now proposed as the chapter's transition character (section 11) rather
   than a room-bound party job.
7. **Which jobs get excused, and does the roster change?** Once the
   party-function ranking lands: confirm which careers stay as party
   contributions, which become structural (racer = transition), and which
   defer to Chapter 5's extended universe. Then rule on whether to ADD a
   career for any uncovered party need — the only expensive option, since
   additions need a painted world, stage, actor, rival set, widgets and
   voice, whereas deferrals cost nothing.
5. ~~Chapter-1 handoff~~ — **ANSWERED (see section 9):** chapter 1 ends with
   the giant dust bunny beaten and everyone going to bed; the party is named
   in the last lines before sleep. Days are the content gate, so the real
   question is now: **approve adding the `story_day` save key** (default 1,
   no existing key touched) as the foundational build item, and confirm that
   current saves should be inferred forward rather than demoted to day 1.

Once these are settled the build order is: defect fixes -> `opera_story.gd`
data + hooks -> TTS generation -> party table -> codex art handoff.

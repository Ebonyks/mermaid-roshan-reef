# 01 — Day Two story bible

Part of the [Day Two story draft v2](README.md). Status: `CANDIDATE`,
2026-09-30. This bible holds the canon and the rules; the whole story, scene
by scene, is in the [plotline](00_DAY_TWO_PLOTLINE.md), which wins where the
two differ. Owner direction for this draft (2026-09-30):

- Anchor Day Two to the Chapter One picture book: every room has a story.
- Mix Daddy Mermaid, the dust bunnies (including the rainbow one) and Baby
  Eagle into the challenges, randomly.
- Add Lamma: three hiding moments across Days One and Two, and a game where
  she joins the stuffie team.
- The Opera House is the routine that introduces each minigame mechanic; each
  job's second level is in the game world, mostly reskinned to fit the plot.
- Replace the Candy Maker's Day Two job with Arborist Roshan
  ([handoff](../ARBORIST_TREE_DOCTOR_HANDOFF_2026-09-30.md)), as the owner
  corrected the Tree Book on 2026-09-29
  (`design/ARBORIST_TREE_BOOK_HANDOFF_2026-09-29.md` on `dev`).
- Fit each job to what is on record (2026-09-30): the Pop Star has the Iko
  Iko material; the Detective finds the candle; the Ballerina is a
  performance with no star until Lamma, who unlocks it; the Astronaut sends
  the birthday invitations ([section 12](#12-the-job-canon-on-record)).

## 1. What Book One established

*Mermaid Roshan and the Hidden Rainbow* (32 pages, branch
`codex/mermaid-roshan-picture-book`, `books/chapter_one/landscape/book.json`):

- Roshan and Daddy fly to the Sky Lagoon and find Pearl Castle full of dust
  (p1–3). Daddy hands her a brush and a sponge: "One little job at a time."
  (p4)
- **Bubble Bath:** a playful dust bunny splashes in the dirty bath; Roshan
  wipes the sink, drains and scrubs the tub; clean water, and the playful pest
  splashes again (p5–8).
- **Mermaid Pool:** Rumi, whose home the castle has been for hundreds of
  years, is stuck under gunk. Roshan scoops the pool, clears three streams
  (the waterfall turns rainbow) and the fountain; Rumi is free and hugs her:
  "You helped me!" (p9–15)
- **Stuffie Playroom:** "Chirp, chirp! Someone needs help!" Two dust bunnies
  tumbled onto Baby Eagle while playing. Roshan frees him one bunny at a time;
  the bunnies say sorry, "we were just playing". "Let's play gently… Come with
  me, Baby Eagle!" (p16–20)
- **Craft Room:** sort the brushes and paints, scrub the table, "I choose
  purple!" (p21–23)
- **The glowing door:** Grand Puff, dusty and unwell. Roshan's shell sparkles
  make him dizzy; Daddy, Rumi and Baby Eagle help scrub; POP, he springs out
  rainbow bright and lands soft and small. "Your rainbow was there all
  along! We helped it shine." (p24–31)
- Everyone falls asleep together in the bubbles: "There was room for
  everyone." (p32)

The game follows the same order, with story clips between rooms. After the
transformation, the rainbow dust bunny follows Roshan through the castle, as
Baby Eagle does.

**Where the Day One game differs from the book, and how Day Two answers:**

| Book One | Day One game today | Day Two picks it up |
|---|---|---|
| The dust bunnies say sorry and learn to play gently | Every dust bunny is popped into sparkles, even the two on Baby Eagle | The bunnies come back clean, play tricks, say "We were just playing!", get a strawberry of their own and end up helping (J3) |
| Daddy hands out the tools and says "One little job at a time." | Daddy appears only in the story clips; the refrain is never said | Daddy's Party Plan and his refrain after every job (D2-OPEN, the routine) |
| "I choose purple!" is self-expression | The colour choice became the Grand Puff attack colour | The banner is painted in the colour she chose (J5) |
| Roshan's shell makes Grand Puff dizzy | The magic brush and a gold star | Day Two's contest is a song, not a fight: the battle of the bands (F5) |
| Rumi's castle home for hundreds of years | Never mentioned; Rumi has no voice | The castle's long memory: its magic storybook has kept the candle for hundreds of years (J8) |
| Everyone sleeps in the bubbles | No nap; the day ends with Daddy's hug and the Day Two card | Day Two wakes in the bubble pile (D2-OPEN-1) and ends at a birthday sleepover (E3) |
| The rainbow friend is Grand Puff himself | A nameless static card in castle rooms, no voice | Named, the day's guide and hint |

## 2. Book Two in one paragraph

On the morning after the bubble nap, it is Roshan's birthday. Daddy draws a
party plan: invitations, a tree, a cake, a banner, a show, a band and a
candle. One little job at a time, Roshan practises each job on the Opera stage
and then does it for real around the castle and the Sky Lagoon. First she
sends a rocket full of invitations to all her friends. Then she heals Baby
Eagle's sick tree so it can be the party tree, picks strawberries, bakes a
rainbow cake, paints a banner, finds a shy hidden lamb called Lamma to be the
star of the stuffies' show, practises Iko Iko with her family band and finds a
long-lost rainbow candle. At the party the Ember King arrives with his kind son
and demands the light: whose band is best? Roshan's band plays its song all
the way to the end. The King cheats and takes only the candle. Everything else
they made together is still there, and so is everyone she loves. That night,
a secret door in the castle begins to glow.

## 3. Themes (for grown-ups; never spoken as a lesson)

- **We make it together.** Every piece of the party is made by Roshan with a
  friend's help.
- **There's room for everyone.** Book Two's echo of Book One's last line,
  "There was room for everyone." Daddy's plan keeps one empty star ("There's
  always room for one more"); the shy lamb fills it and becomes the star; the
  Prince is invited.
- **Everything is for someone.** The party is for the friends she invites
  herself, and each piece is for the party they come to (the
  party-preparation script, [section 11](#11-the-party-preparation-script-what-day-two-keeps)).
- **Kind is strong.** Roshan doesn't fight the King: she plays her song, all
  the way through.
- **What we make together can't be taken.** He takes one light; he cannot
  take the tree, the cake, the show, the band, or the friends.

## 4. The shape of the day

| ID | Where | What happens | Book One friend in it | Party piece | What it gives the party |
|---|---|---|---|---|---|
| D2-OPEN | Bubble pile → Main Hall | Birthday wake-up; Daddy's Party Plan, with empty frames for the friends to invite and a show with an empty star; "practise first, then for real" | — | Party Plan board appears | — |
| J1 Astronaut | Mermaid Pool | Fill the little bubble rocket with rainbow water; one picture invitation per friend; launch | The seahorse | The invitations, sent | Every friend is told, even Wacky and Chuck |
| J2 Arborist | Sky Lagoon middle meadow | Baby Eagle's tree has orange spots; Tree Book: which tree, which leaf, which medicine; spray | Baby Eagle | The blooming party tree | Shade for everyone, even Faron's baby |
| J3 Farmer | Sky Lagoon strawberry grove | Five strawberries; a playful dust bunny rolls one away | The dust bunnies (they learn to help) | Five strawberries | Five for the cake, and one for the dust bunnies |
| J4 Chef | Royal Kitchen | Daddy's apron; rainbow batter; bake, stack, frost, top | Daddy | The rainbow cake | The cake, with a place for the candle; Evie beside it |
| LAMMA-3 | Royal Kitchen | Lamma sniffs the cake, hides, bounces away leaving floury bounce marks and drops her egg | Lamma | — | — |
| J5 Painter | Craft Room | The birthday banner on the table Roshan cleaned yesterday | The rainbow friend (Grand Puff) | The banner | It looks like a party, in colours for Flower Friend |
| LAMMA-JOIN, J6 Ballerina | Stuffie Playroom | The show has no star; hide-and-seek to find Lamma; she says yes and the Ballerina job wakes; the dress rehearsal | Lamma and the stuffies | The stuffies' show | A show to watch, with Lamma as its star |
| J7 Pop Star | Opera Hall | The family band practises Iko Iko: Roshan on drums, Daddy on ukulele, Baby Eagle on bass | Daddy and Baby Eagle | The band's song | Music for everyone, and the band that plays at the party |
| J8 Detective | Royal Library | The magic storybook's clues; the unlit rainbow candle | The castle's long memory | The rainbow candle | A light to wish on |
| F1–F8 | Sky Lagoon middle meadow → Main Hall | The party and Lamma's show, the candle lit, the Ember King and Prince, the battle of the bands, the theft, comfort, the wish, the glowing door | Everyone | — | — |
| E1–E3 | Kitchen, Dining Room, Movie Lounge, Sleepover Bedroom | Birthday supper with the cake; the movie of the day; the birthday sleepover | Everyone | — | — |

**Recommended job order change.** The binding production spine orders the
jobs Farmer, Chef, Candy Maker, Painter, Ballerina, Pop Star, Astronaut,
Detective. This draft replaces the Candy Maker with the Arborist and puts the
Astronaut first:

- The Astronaut sends the invitations, and "Invitations go out before
  anything else — that is simply how a party works, and a child knows it" (the
  August review, section 14).
- The Arborist comes next: the party's place, and Baby Eagle's cry for help,
  a direct echo of Book One. The strawberry grove is beside the meadow, so
  jobs 2 and 3 are one outdoor trip before the castle.
- The Ballerina comes after the Chef, because Lamma must join first and her
  egg drops in the Kitchen (LAMMA-3).
- The Detective finds the candle last, as the spine has it.

This needs owner approval and a spine update (sequence
`[11, 18, 6, 0, 10, 2, 13, 1]`, masks, migration). Keeping the Astronaut at
slot 7 also works if the owner prefers; the story then sends the invitations
late, and the plan's guest row fills later.

## 5. The routine: practise, then do it for real

Every job follows the same four steps, so a four-year-old learns the day's
rhythm:

1. **Daddy's Party Plan.** The next empty picture on Daddy's picture scroll
   glows and Daddy names it: "Next, the cake!" Grand Puff hops to the right
   door and it lights up.
2. **Level 1, the Opera practice.** The job's Opera House career show teaches
   the mechanic on the stage, short and forgiving, with a short bow. Roshan
   comes out wearing the job's costume. No imp appears: Chapter 2 story and
   tutorial runs get no imp and no contest (rule C13 of the imp-contest
   handoff on `dev`, and the design language's new Opera-contest rule there).
3. **Level 2, for real.** Roshan goes to the real place in the castle or the
   Sky Lagoon (the rainbow friend hops ahead as the guide) and uses the same
   mechanic, reskinned into the room's story, with a friend who needs it.
4. **Back on the plan.** The finished piece appears where it lives in the
   world, and Daddy arrives with the scroll: its picture frame fills. Whoever
   it is for joins the frame (after the invitations, the whole guest row), and
   Roshan says what the party has now (the job's function line,
   [section 11](#11-the-party-preparation-script-what-day-two-keeps)).
   Daddy: "One little job at a time!"

Rules:

- The Opera practice launches from the job's existing room card, so it keeps
  the owner's room-distribution rule (`DL-INT-12`: no central all-career
  picker). If the owner wants every practice to start from the Opera Hall
  stage instead, `DL-INT-12` must change first.
- If the child already has that career's star from freeplay, the practice
  shrinks to a one-phase warm-up. It is never skipped silently.
- Level 2 always happens in the room's own art with Roshan there, visibly
  doing the job (`MA-PLAY-004`). It is not another full-screen stage.
- This replaces the production spine's "no tutorial prelude" rule and must be
  recorded there as owner direction.

## 6. Who is in Day Two

| Character | Day Two role | Where | Challenge roles (see §8) |
|---|---|---|---|
| **Roshan** | Birthday girl; does every job | Everywhere | — |
| **Daddy Mermaid** | Party planner and coach; the Party Plan board; the apron; the ukulele in the family band; lights the candle (decision 14); the hug after the theft | Main Hall, Kitchen, every job start, the band, finale | Coach |
| **Baby Eagle** | His tree is the party tree; spots things from above; carries the banner to the tree; plays bass in the family band | Sky Lagoon, following Roshan in the castle, the band | Helper |
| **Rainbow friend (Grand Puff)** | Guide between places; the sparkle that shows the right answer when she hesitates | Everywhere | Hint (always available) |
| **Playful dust bunnies** | Still playful, now learning to help; one mess per level at most; party hats at the stage's edge | Everywhere | Mischief |
| **Rumi** | A guest at the party (existing frames only); her castle's long memory is the Library's seed | Finale | — (story anchor) |
| **The seahorse** | Fills the invitation rocket with rainbow water | Mermaid Pool | — (story anchor) |
| **Lamma** | The shy lamb who has been hiding since Day One; asked to be the star of the stuffies' show, and her yes unlocks the Ballerina job; dances the star part; brings Roshan her hat | Three hiding places, then the Playroom and the finale | — (authored only) |
| **Stuffie team** (Kitty and Bunny, the book dolls from the Ballerina job, then Lamma as the star) | Put on the ballet show at the party | Playroom, finale | — |
| **Party guests** (protected friend portraits) | Invited by Roshan's rocket first thing; three jobs are made for one friend each; they wait in the meadow, wear hats, react and comfort | The Party Plan's guest row; the finale | — |
| **The Ember King** | Demands the light, starts a battle of the bands, loses it, cheats | Finale | — |
| **The Prince** | Kind, conflicted; plays drums in his father's band, speaks up for Roshan, objects to the cheat, apologises | Finale | — |

## 7. Lamma's arc

**Who she is.** Lamma is a small, soft, egg-shaped stuffed lamb who carries
a lavender egg: the look of her protected identity source
(`assets/characters/lamb_0.png`) and her companion card
(`assets/sprites/stuffie_studio/lamma.png`). She is Evie's lamb in the Seek
game, and Evie's protected portrait shows Evie hugging her. She is shy: the
dusty castle and the tumbling dust bunnies frightened her on Day One, so she
hides. She is also curious and follows the fun from a safe distance. She has
no words of her own, only soft bleats (a new sound effect: no lamb sound
exists yet). She bounces rather than walks, which matches her roster attack,
BOUNCE.

**Names.** The owner and the files say "Lamma"; the roster, battle and Seek
display "Lamb-a'"; the Opera magician says "Lamba". This draft uses Lamma
everywhere and asks the owner to confirm one spoken name
([decision 9](README.md#owner-decisions)).

**What already exists.** A companion roster entry locked behind
`stuffie_wins["friend_lamma"]` (`scripts/companion.gd`), a stuffie-battle
capture round (`boss_lamma`, `scripts/stuffie_battle.gd`) that draws a
generic boss rather than Lamma, the Seek game with its animation atlas (hide,
peek, reveal and celebrate: `assets/minigames/seek/lamma_animation.png`), and
the Opera magician's "Hold the wand to hide Lamba under a hat!".

**What does not exist yet.** She cannot be unlocked in real play today: the
battle has no authored caller and the Seek game has no live entry. She has no
Day One moment at all, so LAMMA-1 and LAMMA-2 are new Day One room content.
Her two designs disagree (the Seek atlas has feet and no egg), which
[GFX-LAMMA-01](06_GRAPHICS_AUDIT.md#gfx-lamma-01) resolves before she is
staged anywhere.

| Moment | When | Where | What the child sees and does | Keepsake |
|---|---|---|---|---|
| LAMMA-1 | Day One, right after Baby Eagle is freed | Stuffie Playroom, the play tent | A lamb ear and nose peek out of the tent flap. Touch it: a tiny "Baa?" and she ducks inside; the flap wiggles. Roshan: "Hello? Someone is shy." | — |
| LAMMA-2 | Day One, during the craft-table sorting | Craft Room, between the paint jars | A jar wobbles; Lamma peeks between two jars, then scampers off the table. Roshan: "A little lamb! She ran away." | A tuft of white wool on the table |
| LAMMA-3 | Day Two, after the cake is frosted | Royal Kitchen, behind the flour sack | A floury nose sniffs the cake; touch it and she bounces away, leaving round floury bounce marks toward the door and dropping her lavender egg as she goes. Roshan: "Someone small wants cake!" Roshan picks up the egg: "Her egg! We'll keep it safe for her." | Floury bounce marks; the egg, carried by Roshan |
| LAMMA-JOIN | Day Two, before the Ballerina job, which it unlocks | Stuffie Playroom | See below | Lamma joins as the star of the show |

**LAMMA-JOIN: the joining game.** Kitty and Bunny have a show and no star.
"Our show needs a star!" says Roshan. Then a tiny bleat: the little lamb! The
owner's direction (2026-09-30) is that the Ballerina is a performance and
"there's no one to be the star of the show until Lamma unlocks her", so the
Ballerina job's card sleeps until she joins. The game uses the Seek engine's
four-find structure in the Playroom's own art, and every find plays back one
of her earlier moments, so the child's memory is the clue:

1. **The toy chest:** a tuft of wool pokes out of the lid (from LAMMA-2).
2. **The block tower:** round floury bounce marks lead there (from LAMMA-3).
   *Bounce, bounce!*
3. **The play tent:** its flap wiggles with a tiny "Baa!", just like
   yesterday (LAMMA-1).
4. **The stuffie nook:** Kitty and Bunny point their paws; she is hiding
   among them, and this time she stays, shy.

Each time she is found she giggles and bounces to the next hiding place: she
is playing, gently. At the end Roshan kneels and holds out the lavender egg:
"Here's your egg. Will you be our star? There's room for everyone." Lamma
hugs her egg and nods (atlas `celebrate`), hops onto the empty star, and the
Ballerina card wakes: the show has its star. She dances the star part in the
rehearsal and at the party. The full scene is in the
[plotline](00_DAY_TWO_PLOTLINE.md#lamma-join-and-j6--ballerina-the-star-of-the-show).

Rules:

- The three sightings are story beats, not optional collectibles. They play
  automatically when their room beat happens, and nothing is locked if one was
  missed.
- Saves already past Day One count LAMMA-1 and LAMMA-2 as seen, so the
  joining game's clues still make sense.
- Joining sets the existing `friend_lamma` unlock, so she also becomes
  available in the companion roster. In story mode the gentle hide-and-seek
  is the way she joins; the unreachable 3D-era `boss_lamma` battle is not
  revived for her.
- Her joining sets `lamma_joined`, which the Ballerina card follows: the show
  cannot start without its star.
- She dances the star part in the stuffies' show at the party (F2), and brings
  Roshan her fallen party hat after the theft (F7).

## 8. Mixing Day One friends into the challenges

Each real level has two or three **challenge slots**, filled from each job's
deck of cards. The full rules and all eight decks are in the plotline
([section 5](00_DAY_TWO_PLOTLINE.md#5-the-challenge-mix) and each job in
section 8); this is the summary. Story anchors (the invitations, Baby
Eagle's tree, Lamma, the band) are authored, never random.

| Role | Who | What it does | How it resolves |
|---|---|---|---|
| **Mischief** | A playful dust bunny; sometimes Grand Puff, whose mischief is always a lucky accident | One gentle, fixable complication using the level's own gesture: rolls a strawberry away, puffs flour, leaves paw prints in wet paint | The child fixes it with the same gesture. The bunny says sorry ("We were just playing!") and Roshan says "Let's play gently." It never undoes finished work |
| **Helper** | Baby Eagle | Spots or carries one thing ("Chirp, chirp!" over the hidden strawberry) | The child still makes the final touch |
| **Coach** | Daddy Mermaid | Shows the gesture once, holds something, or counts along: "Watch me: round and round!" | A demonstration never scores or completes (`DL-INT-06`) |
| **Hint** | Grand Puff | Only when she hesitates: he hops beside the right target and it shimmers with rainbow light | Assistance only; never answers |

The rules, in short:

- **First play is the book.** Each job's first play uses its book card, the
  one Book Two prints.
- **Replays are random,** seeded per save file, never the same card twice in
  a row for a job.
- **Everyone gets a turn:** across one Day Two, Daddy, Baby Eagle, the dust
  bunnies and Grand Puff each appear in at least three jobs, with never two
  Mischief cards in one job.
- **Gentle and short:** one child action, at most about ten seconds, nothing
  lost, nothing failed, nothing stalled (after 8 seconds the Helper or Coach
  resolves it).
- **Never** in Lamma's moments or the battle of the bands.

## 9. Continuity locks

- **One cake:** six tiers, red to violet from top to bottom, exactly five
  strawberries, no baked candle. It persists from the Kitchen to the meadow and
  survives the theft.
- **One candle:** found unlit in the storybook; lit only at the party (by
  Daddy, in the recommended answer to decision 14); taken lit by the King's
  royal magic; the cake keeps its empty candle place.
- **The party tree** heals once and stays in bloom from then on, at the edge
  of the middle meadow, and is still there after the King takes the candle.
- **One stage:** the party's single broad stage in the middle meadow, with the
  cake on a visible pedestal, never floating (the bands commission).
- **One song:** the published Iko Iko v89 master, never edited or retimed,
  with no invented lyrics or replacement voices.
- **The King and the Prince** keep their locked looks and the 80% height
  ratio.
- **Protected art and voices** (`assets/book/`, `assets/audio/voices/`,
  `assets/characters/friends/`) are never altered; friend portraits get
  separate hat cutouts, never paint-overs.
- **Saves:** every milestone saves; new keys are additive with defaults; old
  completed saves stay complete.

## 10. Writing rules for every line

- One idea per line; four to eight words is the target.
- Every instruction the child needs is voiced and has a moving picture cue;
  captions are for the grown-up.
- The speaker is the character on screen, in their own voice.
- Sound pairs for actions; the refrains from §1 and §3 recur.
- No lessons spoken aloud, no threats, no mocking, and nothing that makes
  the King's theft the child's fault.

## 11. The party-preparation script: what Day Two keeps

The owner pointed this draft back to the existing script about how each job
contributes to preparing the party. That script is the August party-function
work:

- `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md`, sections 11-20: the owner's
  rulings (no forced fits; the roster can change; the careers run across
  Chapters 2 to 5; the Astronaut sends the invitations; the three stage
  bosses are cut; the Ember King and Prince; the mirror imps), and section 15,
  the reconciled party-role map built around them.
- `CHAPTER2_PARTY_ROLES_2026-08-03.md`, its working papers: the fifteen things
  a party needs, in a guest's own words; each job's role, named guest, stake,
  imp motive, played beats, function line and links to other jobs; the party
  map; the "and one more" count motif.
- `CHAPTER2_BIBLE_ACT_SCRIPTS_2026-08-03.md`: complete per-act scripts for the
  old all-Opera programme.

The document ledger keeps all three as `PROPOSAL_DEFERRED` or historical
evidence, and says their dialogue needs a current owner decision and the
voice gate. This draft adopts parts of them for Day Two, as a `CANDIDATE` for
owner review ([decision 12](README.md#owner-decisions)). The result is in the
plotline: [what each job gives the party](00_DAY_TWO_PLOTLINE.md#what-each-job-gives-the-party).

| From the August script | In this draft | Why |
|---|---|---|
| A job earns its place by meeting a need a guest would feel, not by making an object | **Kept**, as the rule for all eight jobs | It is the clearest answer to "why does this job make the party better?" |
| One function line right after each piece lands ("[Piece], on the table!") | **Kept, moved:** the function line (`Jn-FN`) follows Daddy's "Look what you made!" in each R-beat, said by Roshan as whoever it is for joins the frame | The Opera party table became Daddy's Party Plan, and Roshan's is the one voice every job already has |
| A named guest with a concrete problem for each job | **Kept where one fits, re-cast from the portraits** (below); the show, the band and the candle are for everyone | Specific beats general, and a non-reader reads a face, not a list; no guest is forced onto a job |
| The fifteen needs | **Kept** for the eight jobs, each giving the party the one thing on record for it; the rest wait for their own careers | Review section 11 (no forced fits) and section 13 (careers across Chapters 2 to 5). The owner said on 2026-09-30 that some fits were bad, so no job is given a second need to fill a table |
| Every piece has a named place beside the guest it serves (the party map) | **Kept** in the middle meadow: each guest stands nearest their piece where there is one | The party moved from the Main Hall to the Sky Lagoon (owner direction, 2026-09-05), and the owner placed the contest in the middle meadow (2026-09-20) |
| Show the need before the job and the need met at the party | **Kept:** the empty frames, the empty star, the spotty tree, the empty shell on the cake | It is how a four-year-old sees why a job matters |
| Invitations by the Astronaut's rocket, fixing a guest count that the bags, picnic and cake follow | **Kept:** the Astronaut sends the invitations by bubble rocket, first thing (J1), and the guest row they fill is the party's guest list. Nothing else is counted | The owner restated the August ruling on 2026-09-30: "The astronaut sends birthday invitations." It replaces this draft's earlier dawn invitations from Daddy. The binding spine's candle-lighting rocket changes only with the owner's approval (decisions 1 and 14) |
| "And one more": a spare bag, plate, invitation and chair | **Kept as one thread:** the dust bunnies' extra berry, and the empty star that Lamma fills when she agrees to be the star | It is Book One's "There was room for everyone.", and Lamma is the one more |
| "There has to be something to DO" (the Ballerina and the Boxer) and "something to WATCH" (the Magician) | **Changed:** the Ballerina puts on a show to watch, with Lamma as its star, and the show cannot start until she joins | The owner, 2026-09-30: "Ballerina is going to be a performance but there's no one to be the star of the show until Lamma unlocks her" |
| "Everybody has to HEAR, even me at the back" (the Pop Star) | **Kept, as the band:** the family band plays Iko Iko for everyone, and its song is the finale's contest | The owner, 2026-09-30: "The pop star already has the iko iko material", after choosing the battle of the bands on 2026-09-20 |
| "I have to know WHOSE birthday it is" (the Detective) | **Changed:** the Detective finds the candle | The owner, 2026-09-30: "Detective finds the relevant candle", as the production spine has it |
| The shared moment (candles, wish, song) is made by no job, and is what the villain steals | **Turned the right way up:** the King takes the candle and cannot take the moment; the wish survives (F7) | Canon: he takes only the candle, and what we make together can't be taken |
| The imps ask "Are we invited?", and the Imp Captain is let in at the climax | **Not used:** Day Two has no imps; the Prince is the one offered a place ("You can join us") | Chapter 2 story and tutorial runs get no imp and no contest (rule C13 of the imp-contest handoff on `dev`, and the design language's new Opera-contest rule there); the 2026-08-30 canon makes the Ember King the antagonist, and the Prince is kind and conflicted |
| The Curtain Dragon, Shadow Phantom and Midnight Maestro own the door, the light and the time | **Not used** | They are cut (`DL-INT-13`), and review section 16 finds those needs were never real gaps |
| The Candy Maker's party bags, the Racer's delivery run, the Magician, Boxer, Nursery Nurse and Stuffie Surgeon | **Left for later days** | Not Day Two careers; the Candy Maker is reserved for a later part of the game and is not placed in the Kitchen (owner, 2026-09-29) |
| Guests as the August papers imagined them: Kareem the grown-up shopkeeper, a Flower Friend who cannot speak, Huluu as the Ballerina's guest, Harper and Fiona as the Boxer's | **Re-cast from the protected portraits** | The portraits show Kareem as a boy in a big shell armchair, Flower Friend with rainbow hair holding a smiling rainbow flower, Princess Huluu in a bubble space helmet with her arms folded, and Harper and Fiona as sisters hugging |
| Function lines in the guests' own voices | **Not in this draft:** Roshan says every function line; existing guest clips may play unaltered | New guest lines are an owner choice ([decision 13](README.md#owner-decisions)); Faron's recordings are protected |

**The named guests, and why each one.**

| Job | Guest | Why this guest, from the portrait and the record |
|---|---|---|
| J1 Astronaut | Every friend, and most of all Wacky and Chuck | They live furthest out; the August map says the Astronaut serves "Wacky (lives furthest out, slowest)", and without an invitation "Wacky knocks the next morning asking when the party is" |
| J2 Arborist | Faron and her baby | A baby needs shade to nap; Faron's own clip is "Shhh... the babies are getting sleepy." |
| J3 Farmer | The dust bunnies | They grabbed a berry because they wanted one too; one of their own stops the grabbing |
| J4 Chef | Evie | The best seat at a party is the one beside the cake, and Evie brings her lamb (the August map: "Lamba wants to sit next to the cake!") |
| J5 Painter | Flower Friend | Rainbow hair and a rainbow flower: she loves colour more than anyone; the August map gives the Painter "the Flower Friend" |
| J6 Ballerina | Lamma, the star; everyone watching | The owner: no one is the star of the show until Lamma |
| J7 Pop Star | Everyone, all the way to the back | The August map's Pop Star serves "the guests at the back" |
| J8 Detective | Roshan | The candle is the light for her birthday wish, and everyone wishes with her |

## 12. The job canon on record

On 2026-09-30 the owner corrected this draft's job fits and pointed to the
records: "No, bad fits for some. The pop star already has the iko iko
material. Detective finds the relevant candle. Balarina is going to be a
performance but there's no one to be the star of the show until lamma, unlocks
her. The astronaut sends birthday invitations. Check rep more carefully, this
information should be on record." This section puts each fact beside the
record that holds it, so the next draft starts from them.

| Job | What the job does | The record | Where it is kept, and its status |
|---|---|---|---|
| Astronaut | Sends the birthday invitations, by bubble rocket, as the chapter's first act | "The Astronaut Engineer sends the invitations (owner ruling)": "she designs the invitations and launches them to her friends by bubble-rocket — early in the process"; "the astronaut act should be the chapter's opening job"; "The shipped astronaut phases carry it as-is: PIPES routes the bubble tubes, PATCH seals the leaks, VALVE pressurises, BOOST builds thrust, LAUNCH sends them off" | `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md` section 14 and section 15.1 ("Astronaut (owner ruling: invitations by rocket)"). The master index and the ledger adopt only the review's sections 10, 16 and 17 as owner authority, so section 14, although it calls itself an owner ruling, sits with the review's `PROPOSAL_DEFERRED` remainder. The August 30 options record ranked "Build the little rocket that lights the candle" above "Launch picture invitations across the kingdom", and the binding production spine gives the rocket to the candle ("post-Detective rocket ignition"). The owner restated the invitation ruling on 2026-09-30; the spine changes only when the owner approves this draft |
| Pop Star | The Iko Iko material: Roshan drums in her Pop Star outfit, with Daddy on ukulele and Baby Eagle on bass, in a battle of the bands against the Ember King (lead guitar) and the Prince (drums); the same drumming serves the Pop Star's rehearsal and the finale | "The owner now selects a battle of the bands to the recorded Iko Iko" (the "September 20 contest revision"); "Roshan drums in her Pop Star outfit to the recorded Iko Iko"; "Owner-commissioned isolated playable Pop Star drumming and cheating-theft prototype"; "Extract a bounded reusable drumming component for Pop Star rehearsal and this finale" | `design/CHAPTER2_LAWN_FINALE_DRAFT_2026-09-06.md`, `design/BATTLE_OF_BANDS_2026-09-20.md` (`CANDIDATE`), `design/audit_impacts/battle-of-bands-20260920.json`, the review packet `assets_src/cinematics/battle_of_bands_2026-09-20/` and `scripts/battle_of_bands_prototype.gd`, all on branch `codex/battle-of-bands-20260920` (commits `c141a63e` and `841510be`), not yet merged to `dev`. On `dev` the Pop Star's Day Two job is still "sound-check the birthday song with Rumi", and the question `OQ-BANDS-VS-LAWN` stays open. The Iko Iko v89 archive says it "is not a runtime game cue or approval to reuse the composition in the game", and its workflow says the song's rights "would need a separate decision before any reuse in the game" (branch `codex/reaper-music-workflow-20260920`) |
| Ballerina | A performance, the stuffies' show, whose star is Lamma; her joining unlocks it | The owner, 2026-09-30, quoted above. The review's adopted section 10 already files the Ballerina with the Pop Star and the Magician as "the three performances", and the Ballerina's three acts are "a recital, not a race or combat encounter" | Lamma as the star is recorded here for the first time: a search of every branch's history found no earlier record. `BALLERINA_PARTY_REBUILD_2026-08-09.md` is `BINDING_DOMAIN` for the Ballerina's acts. Two older owner decisions place her elsewhere and stay as they are: Lamba is the Magician's hat-trick subject (`FABLE_OPERA_LAMBA_TAKEOVER_HANDOFF_2026-08-01.md`, owner 2026-08-01), and Lamb-a' is the first stuffie a battle can capture (`STUFFIE_COMPANIONS.md`, owner 2026-07-20), through a `boss_lamma` round that uses the retired `lamb.glb` body (decision 4) |
| Detective | Finds the rainbow candle in the magic storybook | The owner's direction of 2026-08-30, as the options record summarises it: "the Detective candle reveal as the last required career beat". The spine's Detective: "final missing unlit rainbow candle revealed in the magic storybook". The alpha's spoken route line: "Tap the glowing Library door. Find the unlit rainbow candle in the magic storybook!" | `design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md` (`BINDING_DOMAIN`), `design/CHAPTER2_EIGHT_CAREER_STORY_OPTIONS_2026-08-30.md` (its header note), and `scripts/chapter_two_voice_catalog.gd` on `dev`. The August review's older Detective jobs (the tiara crown; "whose birthday it is") are superseded |

Related records the correction also follows:

- **The Arborist.** The owner corrected the Tree Book on 2026-09-29: every
  patient has a visibly diseased leaf, "the previous fixed Thirsty → Broken
  branch two-problem event is superseded", each patient has three decisions
  with four choices, "Roshan visibly gives the medicine to the tree. The same
  tree becomes healthy. A tree sticker is the payoff", and "A healed tree
  remains visible at the lawn finale and after the King takes the candle"
  (`design/ARBORIST_TREE_BOOK_HANDOFF_2026-09-29.md` on `dev`). The practice
  is built as `design/OPERA_TREE_BOOK_TEST_2026-09-30.md` on `dev`.
- **The Candy Maker.** "Candy Maker is reserved for a later section of the
  game. Do not place it in the Kitchen." (the same handoff, 2026-09-29).
- **No imps in Chapter 2's story.** "Chapter 2 story runs (`reward_policy
  chapter2_story`), tutorial runs, and configs with `phase_overrides` or
  `scene_adapter` get no imp and no contest" (rule C13,
  `docs/handoffs/codex_opera_imp_contest_2026-09-30/CONTEST_DESIGN.md` on
  `dev`, `PROPOSED / CANDIDATE`), and the design language's new Opera-contest
  rule on `dev` (2026-09-30): "Chapter 2 story
  and tutorial runs opt out."

**What this changed in the draft.** The Astronaut moves to the front and
sends the invitations (Daddy no longer does); the Pop Star's job is the family
band, and the battle of the bands replaces the stomp-and-dodge protection
rounds; the Ballerina's show waits for Lamma, its star; the Detective's job is
unchanged, with the extra "light to see by" removed; the Arborist follows the
leaf-based Tree Book; the imps leave Day Two; and the extra needs the previous
round invented to fill a checklist (the petal nest, the berry baskets, cake
for everyone after the wish, Roshan's picture on the banner, the countdown,
Kareem's show, the wild twirl and the light at dusk) are gone. Who lights the
candle now that the rocket carries the invitations is a new owner decision
([decision 14](README.md#owner-decisions)).

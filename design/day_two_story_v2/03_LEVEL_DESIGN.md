# 03 — Level design: every Day Two event

Part of the [Day Two story draft v2](README.md). Status: `CANDIDATE`,
2026-09-30. Rules and cast are in the [story bible](01_STORY_BIBLE.md); the
finale is in [04](04_FINALE_PARTY_CHAPTER.md).

## How to read a job

Every job has the same parts:

- **Room story:** the friend who needs it, the problem, the refrain.
- **Level 1 (Opera practice):** a short cut of the job's existing Opera career
  show, using only the verbs level 2 needs, then the curtain call. The full
  show stays in freeplay. A child who already holds the career star gets a
  one-phase warm-up instead.
- **Level 2 (for real):** in the room's own art, with Roshan there doing it.
  The mechanics are the same modes as level 1, reskinned to the plot object.
  This is where today's Chapter 2 story phases move to; today they run inside
  full-screen Opera career worlds.
- **Challenge slots:** which roles from the story bible (§8) may appear.
- **Result:** the persistent party piece and where it shows up afterwards.

Mode names are the existing gesture modes in
`scripts/opera_career_world_2d.gd` and
`scripts/chapter_two_career_scene_adapter.gd`.

## D2-OPEN — Birthday morning

### D2-OPEN-1 — Wake-up

| | |
|---|---|
| Follows | The Day One epilogue clip and a revised Day Two card |
| Scene | Morning light through the attic's shell windows on the bubble pile from Book One's last page (the calm attic where Grand Puff was freed); Daddy, Roshan, Rumi, Baby Eagle and the small rainbow friend waking |
| Child | Touches Roshan to wake her (a moving hand on her) |
| Voice | Daddy: "Wake up, birthday girl!" Roshan: "It's my birthday! Can we have a party?" |
| Save | New `day2_wakeup_seen` |
| Art source | The attic is not a castle room in the game (it is the Grand Puff arena), and the calm bubble pile exists only as Book One art (`books/chapter_one/landscape/art/personality_v20/bubble_nap.png`, non-runtime). Options: import that illustration as a runtime still with a morning-light derivative (owner approval, since book art is non-runtime today), or stage the wake-up in the calm Grand Puff arena with existing cutouts |

**Day Two card fix:** keep the dawn animation, but show Roshan's birthday
(the rainbow cake silhouette or balloons, no words needed) and point at the
first place (the lawn), not the Opera, Craft and Kitchen medallions. Change
its voice line from "The second day is here! Visit castle jobs and the Opera
House!" to "It's Roshan's birthday!"

### D2-OPEN-2 — Daddy's Party Plan

| | |
|---|---|
| Scene | Main Hall. Daddy unrolls a big picture board: eight empty frames (tree, strawberries, cake, banner, stuffies, microphone, rocket, candle) |
| Child | Touches the board |
| Voice | Daddy: "The best party ever. Let's make it together. A place, a cake, a banner, a dance, a song and a light. One little job at a time." |
| After | The board lives in the Main Hall all day. The next frame glows; filled frames show the real piece. It replaces the late-appearing party table as the day's progress picture |
| Art | Frame pictures can reuse existing art: strawberries (`assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png`), cake (`chapter2_grand_five_strawberry_cake.png`), banner (`assets/flats/castle/logo_studio_v2/castle_banner_rainbow.png`), stuffies (`assets/book/doll_cat.png`, used unchanged), microphone (`assets/opera/worlds/props/goal_popstar.png`), rocket (`goal_astronaut.png`), candle (`rainbow_candle_unlit.png`); the tree comes from the Arborist art. **GAP:** the board itself (a shell-framed picture board in the castle style) and a greyed "not yet" frame state |

### D2-OPEN-3 — Practise first

| | |
|---|---|
| Voice | Daddy: "First we practise on the Opera stage. Then we do it for real!" |
| Picture | The board's first frame (the tree) glows; the rainbow friend hops to the job's door (he has no wings) |

## J1 — Arborist: Baby Eagle's tree

**Room story.** Baby Eagle's favourite tree on the Sky Lagoon lawn is sick:
drooping grey leaves and a broken branch. He circles and cries. "Chirp,
chirp! Someone needs help!" (the Book One echo). Healing it makes it the
party tree.

**Level 1: Tree Doctor Training** (new Opera career; see the
[Arborist handoff](../ARBORIST_TREE_DOCTOR_HANDOFF_2026-09-30.md)). Three
potted patients, two cards per page, sicknesses Thirsty, Spotty leaves and Bug
tickles. It teaches the Tree Book: which tree, what's wrong, which medicine,
then pour, spray and tap.

**Level 2: The party tree** (Sky Lagoon lawn).

| Beat | Mode | What the child does | Voice | Picture cue |
|---|---|---|---|---|
| 1 Arrive | travel | Roshan swims to the tree after Baby Eagle | Baby Eagle: "Chirp, chirp!" Roshan: "Baby Eagle's tree is sick. I'll help!" | Baby Eagle circling the tree |
| 2 TREE | book match | Match the tree's leaf in the Tree Book (3 cards) | Roshan: "Which tree? Find the same leaf!" | The leaf floats into the book |
| 3 THIRSTY | book match + pour | Match "Thirsty" and the watering can, then pour on the roots | Roshan: "It's thirsty! Pour, pour!" | Blue-drop badge; roots darken as they drink |
| 4 BRANCH | book match + circle | Match "Broken branch" and the bark bandage, then circle to wrap | Roshan: "Wrap, wrap!" | Zigzag badge; the bandage wraps round |
| 5 BLOOM | tap | Touch the tree: blossoms open, Baby Eagle hops home | Roshan: "This is our party tree!" | Blossoms burst in a ring |

- **Challenge slots:** Mischief (a dust bunny sits on the bark bandage; tap to
  bounce it off), Hint (always).
- **Result:** the blooming party tree, saved in `chapter2_party_tree_phase`;
  it stays in bloom on the lawn and in the finale; the board's tree frame
  fills.

## J2 — Farmer: five strawberries

**Room story.** The strawberry grove on the Sky Lagoon, next to the lawn.
The playful dust bunnies are here too; they still love to play, and now they
want to help.

**Level 1: The Piggy Picnic Challenge, practice cut.** HERD (`swipe`) and
PICNIC (`tap`). It teaches tapping each thing once and sweeping something
along a path.

**Level 2: The strawberry grove** (reuses Chapter 2 Farmer phases in-world).

| Beat | Mode | What the child does | Voice | Picture cue |
|---|---|---|---|---|
| 1 GATHER | tap | Touch five ripe strawberries on the plants | Roshan: "One! Two! Three! Four! Five!" | Each ripe berry sparkles; a counter of five berry pictures fills |
| 2 FILL BASKET | tap | Touch each picked berry to put it in the basket | Roshan: "In the basket!" | The berry hops in |
| 3 DELIVER | swipe | Push the basket along the path to the castle door | Roshan: "To the kitchen!" | A glowing path arrow |

- **Challenge slots:** Mischief (a dust bunny rolls the fifth berry under a
  leaf; "We were just playing!"), Helper (Baby Eagle spots it: "Chirp,
  chirp!").
- **Result:** five strawberries (`chapter2_strawberry_mask`), carried to the
  Kitchen; the board's strawberry frame fills.

## J3 — Chef: the rainbow cake

**Room story.** The Royal Kitchen. Daddy ties Roshan's apron. The cake's six
rainbow colours come from the rainbow friend's sparkle: he shakes, and six
colours of batter swirl in the bowl.

**Level 1: The Castle Bake-Off, practice cut.** MIX (`pourt`), STIR
(`circle`), BAKE (`oven`), FROST (`swipe`), TOP (`tap`). Chef already
teaches every verb level 2 uses.

**Level 2: The birthday cake** (Kitchen room art: oven, counter and sink are
already room items).

| Beat | Mode | What the child does | Voice | Picture cue |
|---|---|---|---|---|
| 1 MIX | pourt | Tip the batter into the shell bowl; six colours | Daddy: "Apron on, birthday chef!" Roshan: "Mix, mix!" | The rainbow friend's sparkle colours the batter |
| 2 STIR | circle | Big circles; the ribbons swirl into one spiral | Roshan: "Stir, stir!" | Spiral guide |
| 3 BAKE | oven | Roshan swims to the room's oven; wait for golden; mitt out | Roshan: "Into the oven!" | Oven glow turns gold |
| 4 STACK | tap | Touch the six tiers, biggest first | Roshan: "Stack them up!" | The next tier pulses |
| 5 FROST | swipe | Trace the frosting ribbon | Roshan: "Frosting!" | Glowing ribbon path |
| 6 TOP (new) | tap | Place the five strawberries on the upper tiers | Roshan: "Five strawberries on top! A rainbow cake!" | Five sparkling places |

- The TOP beat takes over the Candy Maker's placement: Chef now owns cake bits
  5 and 6, and the cake reaches its final art.
- **Challenge slots:** Coach (Daddy demonstrates the first tip of the bowl),
  Mischief (a dust bunny sneezes flour over the counter: "Achoo!", swipe it
  away).
- **After the result: LAMMA-3** (see Lamma below).
- **Result:** the rainbow cake (`chapter2_cake_piece_mask` `0x7F`), shown on
  the Kitchen counter, the party table and the lawn; the board's cake frame
  fills.

## J4 — Painter: the birthday banner

**Room story.** The Craft Room table Roshan cleaned in Book One ("Now there
was room to make art"). The rainbow friend wants his colours on the banner.

**Level 1: The Sunrise Paint-Off, practice cut.** PAINT (`paint_reveal`),
STAMPS (`tap`), GALLERY (`choice`).

**Level 2: The banner.**

| Beat | Mode | What the child does | Voice | Picture cue |
|---|---|---|---|---|
| 1 PAINT | paint_reveal | Paint across the long banner to reveal rainbow stripes and a cake-and-candle picture in its middle, in the colour she chose in the Craft Room on Day One (the saved `attack_color`) | Roshan: "A banner for my party! Paint, paint!" | Stripes appear under her brush |
| 2 STAMP | tap | Stamp five birthday stars | Roshan: "Stamp, stamp! Five stars!" | Five star outlines to fill |
| 3 SEND | choice | Choose the party tree picture (not the other two) to send it | Roshan: "To the party tree!" | Baby Eagle takes the rolled banner and flies out the window |

- **Challenge slots:** Mischief (a dust bunny walks across the wet paint
  leaving paw prints; stamp stars over them), Helper (Baby Eagle carries the
  banner).
- **Result:** the banner, strung in the party tree on the lawn; the board's
  banner frame fills.
- **Art:** the banner's painted, stamped and hung states are derivatives of
  the approved banner ([GFX-PROP-BANNER-01](06_GRAPHICS_AUDIT.md#gfx-prop-banner-01)).

## LAMMA-JOIN and J5 — Ballerina: the stuffie team

**Room story.** The Stuffie Playroom, where Roshan freed Baby Eagle in Book
One. The stuffies want to dance at the party, but they need one more dancer,
and someone has been hiding all along.

**Level 1: The Mermaid Pearl Ballet Party, practice cut.** PEARL MIRROR
(`ballet_pose`), RIBBON TRAIL (`ballet_ribbon`), GRAND TWIRL
(`ballet_twirl`).

**Level 2a: LAMMA-JOIN** (four-find, built on `scripts/games/seek.gd`):

| Find | What the child does | Voice | Picture cue |
|---|---|---|---|
| 1 Wool | Touch the tuft of wool on a shelf (from LAMMA-2) | Roshan: "Wool!" | A soft glow |
| 2 Bounce marks | Touch the round floury bounce marks on the floor (from LAMMA-3) | Roshan: "Bounce, bounce! She went this way!" | The marks light up one by one toward the toy chest |
| 3 Egg | Touch the lavender egg peeking out of the toy chest (she dropped it in the kitchen) | Roshan: "Her egg! Let's give it back." | The chest lid bounces; the egg glows, then rides in Roshan's hand |
| 4 Lamma | Touch the play tent; she peeks; Roshan holds out the egg; Lamma bounces out and hugs it | Roshan: "There you are! Here's your egg. Will you dance with us? There's room for everyone." Lamma: a happy bleat (sound effect) | Seek atlas peek → reveal → celebrate |

**Level 2b: The stuffie dance** (the existing plot-owned Ballerina job, now
in the Playroom's own art, with Lamma added).

| Beat | Mode | What the child does | Voice |
|---|---|---|---|
| 1 MIRROR | ballet_pose | Match poses; Kitty, Bunny and Lamma copy | Roshan: "Point!" |
| 2 TWIRL | ballet_ribbon | Guide the ribbon; the stuffies twirl | Roshan: "Twirl!" |
| 3 BOW | ballet_twirl | One grand twirl, then everyone bows | Roshan: "Bow! The stuffie team can dance!" |

- **Challenge slots:** Helper (Baby Eagle points at a clue during the
  search), Hint (always). No Mischief: this is Lamma's shy moment.
- **Result:** Lamma joins (`lamma_joined`, `friend_lamma`); the stuffie
  team's dance; the board's stuffie frame fills.

## J6 — Pop Star: the birthday song with Rumi

**Room story.** The Opera Hall stage. Rumi has lived in the castle for
hundreds of years and knows its oldest songs. When the song is ready, she
remembers the castle's lost rainbow candle.

**Level 1: The Starlight Sound-Off, practice cut.** SOUND CHECK (`hold`),
RHYTHM (`echo`), ENCORE (`circle`).

**Level 2: The birthday song.**

| Beat | Mode | What the child does | Voice | Picture cue |
|---|---|---|---|---|
| 1 SOUND CHECK | hold | Hold the microphone while Rumi's rainbow note grows | Roshan: "Testing, testing!" | Note grows |
| 2 STAGE RUMI | choice | Tap the arrow that puts Rumi beside the band | Roshan: "Rumi, over here!" | Glowing arrow |
| 3 RHYTHM | echo | Listen to three stars, then tap them back | Roshan: "La, la, la!" | Stars light in order |
| 4 ENCORE | circle | One big spin | Roshan: "Encore!" | Spin guide |
| 5 MEMORY | watch | A thought bubble above Rumi shows a rainbow candle inside a glowing book | Roshan: "Rumi remembers a rainbow candle!" | The bubble; the board's last two frames (rocket, candle) sparkle |

- **Rumi has no voice** (spine rule: approved animation and notes only). Her
  memory is a picture, said aloud by Roshan.
- **Challenge slots:** Mischief (the dust bunnies, as the audience, bang the
  drum too early; tap in time to calm them), Coach (Daddy claps the rhythm
  first).
- **Result:** the party song (`party_song`), which plays at the party; the
  board's microphone frame fills.

## J7 — Astronaut: the candle-lighting rocket

**Room story.** The Mermaid Pool, where the waterfall turned rainbow in Book
One. A rainbow candle needs a rainbow spark, and the rainbow waterfall
can fill the little rocket. The seahorse Roshan freed helps connect the
pipe.

**Level 1: The Rocket Repair Race, practice cut.** PIPES (`pipe`), PATCH
(`tap`), VALVE (`circle`). LAUNCH is not practised: this rocket must not
launch.

**Level 2: The little rocket.**

| Beat | Mode | What the child does | Voice | Picture cue |
|---|---|---|---|---|
| 1 BUILD | pipe | Connect the waterfall to the rocket through the pipe boards | Roshan: "Click, click!" | The seahorse holds the end of the pipe |
| 2 PATCH | tap | Patch the sparkling leaks | Roshan: "Patch, patch!" | Leaks sparkle |
| 3 FILL | circle | Turn the valve; rainbow water fills the rocket | Roshan: "Rainbow water!" | Rocket window fills with colour |
| 4 PARK | swipe | Push the rocket onto its little cart, ready but parked | Roshan: "Ready… but not yet!" | Parking spot outline |

- **Challenge slots:** Helper (the seahorse, fixed), Mischief (a dust bunny
  bounces on the valve; tap to lift it off), Hint (always).
- **Result:** the parked rocket, which rolls to the lawn for the party; the
  board's rocket frame fills.

## J8 — Detective: the rainbow candle

**Room story.** The Royal Library and its magic storybook, the one from
Rumi's memory. The rainbow candle has been hidden in it for hundreds of
years, waiting for the right party.

**Level 1: The Two-Detective Mystery, practice cut.** SEARCH (`lens`) and
CASE BOARD (`clue_board`).

**Level 2: The storybook** (the existing plot-owned Detective job, in the
Library's own art).

| Beat | Mode | What the child does | Voice | Picture cue |
|---|---|---|---|---|
| 1 LENS | lens | Sweep the magnifier over the glowing storybook | Roshan: "Rainbow drips!" | Rainbow wax clues appear under the lens |
| 2 BOARD | tap | Touch each rainbow clue on the storybook board | Roshan: "Red, orange, yellow…" | Clues glow in rainbow order |
| 3 CANDLE | tap | Touch the page; the unlit rainbow candle rises out | Roshan: "The rainbow candle! It's not lit yet." | The candle floats up |

- **Challenge slots:** Mischief (a dust bunny hides between the books; the
  lens finds it, it giggles and helps), Helper (Baby Eagle spots the right
  shelf), Hint (always).
- **Result:** the unlit candle on the cake (`chapter2_party_event_phase` 1);
  all eight board frames full; the Main Hall doors glow for the party (F1).

## Lamma's sightings

| ID | Day | Room and trigger | Child | Voice | Save |
|---|---|---|---|---|---|
| LAMMA-1 | One | Stuffie Playroom, right after Baby Eagle is freed | Touch the ear peeking from the play tent; she ducks in | Lamma: a questioning bleat (sound effect). Roshan: "Hello? Someone is shy." | `lamma_moments_seen` bit 0 |
| LAMMA-2 | One | Craft Room, during sorting | Touch the wobbling jar; she peeks and scampers off | Roshan: "A little lamb! She ran away." | bit 1; wool tuft stays on the table |
| LAMMA-3 | Two | Kitchen, right after the cake is finished | Touch the floury nose behind the flour sack; she bounces away and drops her egg | Roshan: "Someone small wants cake!" | bit 2; bounce marks stay on the floor |

All three are in-room gameplay moments, never edits to the Day One story
clips (`DL-CIN-16`).

## Voice script

Speaker and voice source for every new line. "Filler" means the provisional
Parler synthetic pipeline (`assets/audio/voices/VOICE_MANIFEST.md`), never
trained on family recordings; new Daddy lines use the manifest's Daddy-only
"Will" filler preset. The sacred family recordings (`daddy1.ogg` to
`daddy3.ogg`, `chuck.ogg`, `chuck_bark.ogg`, `chuck_whimper.ogg`) and Faron's
protected voice stay untouched. Rumi has no voice. Lamma's legacy lines that
play through Evie's voice (the roster hello and the capture plea) are revised
in [WP-15](07_WORK_PACKAGES.md).

| ID | Speaker | Line | Source |
|---|---|---|---|
| OPEN-1a | Daddy | "Wake up, birthday girl!" | Filler, new Daddy key |
| OPEN-1b | Roshan | "It's my birthday! Can we have a party?" | Synthetic Roshan |
| OPEN-2 | Daddy | "The best party ever. Let's make it together." | Filler |
| OPEN-2b | Daddy | "A place, a cake, a banner, a dance, a song and a light." | Filler |
| OPEN-2c | Daddy | "One little job at a time." | Filler |
| OPEN-3 | Daddy | "First we practise on the Opera stage. Then we do it for real!" | Filler |
| PLAN-next-* | Daddy | "Next, Baby Eagle's tree!" / "Next, strawberries!" / "Next, the cake!" / "Next, the banner!" / "Next, the dance!" / "Next, the song!" / "Next, the rocket!" / "Next, the light!" | Filler |
| PLAN-done | Daddy | "Look what you made!" | Filler |
| GUIDE | Roshan | "Follow Grand Puff!" | Synthetic Roshan |
| J1-* | Roshan, Baby Eagle | As in J1 above, plus the Tree Book lines in the Arborist handoff | Synthetic Roshan; Baby Eagle existing chirp |
| J2-* | Roshan, dust bunny | "One! Two! Three! Four! Five!", "In the basket!", "To the kitchen!", dust bunny: "We were just playing!", Roshan: "Let's play gently." | Synthetic; dust bunny filler |
| J3-* | Daddy, Roshan, dust bunny | "Apron on, birthday chef!", "Mix, mix!", "Stir, stir!", "Into the oven!", "Stack them up!", "Frosting!", "Five strawberries on top! A rainbow cake!", "Achoo!", "Swish it away!" | Filler / synthetic |
| J4-* | Roshan | "A banner for my party! Paint, paint!", "Stamp, stamp! Five stars!", "To the party tree!" | Synthetic |
| LAMMA-* | Roshan, Lamma | "Hello? Someone is shy.", "A little lamb! She ran away.", "Someone small wants cake!", "Wool!", "Bounce, bounce! She went this way!", "Her egg! Let's give it back.", "There you are! Here's your egg. Will you dance with us? There's room for everyone." Lamma has no words: questioning and happy bleats | Synthetic Roshan; new lamb bleat sound effect (none exists) |
| J5-* | Roshan | "Point!", "Twirl!", "Bow! The stuffie team can dance!" | Synthetic |
| J6-* | Roshan | "Testing, testing!", "Rumi, over here!", "La, la, la!", "Encore!", "Rumi remembers a rainbow candle!" | Synthetic |
| J7-* | Roshan | "Click, click!", "Patch, patch!", "Rainbow water!", "Ready… but not yet!" | Synthetic |
| J8-* | Roshan | "Rainbow drips!", "Red, orange, yellow…", "The rainbow candle! It's not lit yet." | Synthetic |
| F-* | All | Every line in [04](04_FINALE_PARTY_CHAPTER.md) | Roshan synthetic; King and Prince new filler presets; Daddy filler; dust bunnies filler; Lamma sound |

Every line needs its exact caption text, and its picture cue must be on
screen while it plays.

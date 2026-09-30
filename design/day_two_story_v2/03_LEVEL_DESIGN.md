# 03 — Level mechanics and voice lines

Part of the [Day Two story draft v2](README.md). Status: `CANDIDATE`,
2026-09-30.

The story is told in full in [00, the plotline](00_DAY_TWO_PLOTLINE.md). This
file is its compact build sheet: every scene's steps with the existing gesture
mode each one reuses, the save each step writes, and every voice line and
sound the day needs. If this file and the plotline disagree, the plotline
wins.

## How to read it

- **Gesture modes** are the existing modes in
  `scripts/opera_career_world_2d.gd` and
  `scripts/chapter_two_career_scene_adapter.gd`. "New" means no mode exists.
- **Practice (L1)** runs in the job's existing Opera career world, cut short
  through the dormant `chapter2_tutorial` path: no rival race, no imp, a short
  bow. A child who already holds that career's star plays only the first step.
  Two practices come from elsewhere: the Arborist's is the Tree Book test level
  on `dev`, and the Pop Star's drum part is the bands commission's reusable
  drumming component.
- **Real (L2)** runs in the room's own art on the Day One in-room activity
  pattern, with Roshan there doing the job. Its gestures are the practice's
  gestures, reskinned to the story's objects.
- **Decks** list each job's challenge cards by role (plotline section 5): D a
  dust bunny, P Grand Puff, E Baby Eagle, M Daddy. The book card plays first.
- **R-beats** (after every job) are watched, then touched to continue.
  Whoever the piece is for joins its Party Plan frame while Roshan says the
  job's function line (`Jn-FN`, plotline
  [what each job gives the party](00_DAY_TWO_PLOTLINE.md#what-each-job-gives-the-party)).
  Only R3 adds a step: one `tap`.

## Act I

| Scene | Step | Gesture | Object | Save |
|---|---|---|---|---|
| D2-OPEN-1 | Wake Roshan | tap | Roshan in the bubble pile | — |
| D2-OPEN-1 | Leave the attic | tap | The attic door | `day2_wakeup_seen` |
| D2-OPEN-2 | Open the plan | tap | Daddy's rolled scroll | — |
| D2-OPEN-2 | Ask about the empty star | tap (Roshan asks anyway after 6 s) | The empty star in the plan's stage picture | `chapter2_party_plan_seen` |

## The jobs

### J1 — Astronaut (Mermaid Pool)

| Part | Step | Gesture | Object |
|---|---|---|---|
| Practice | PIPES, PATCH, VALVE, LAUNCH | `pipe`, `tap`, `circle`, `hold` | The Astronaut world |
| Real | B2 Pipes | `pipe` (3 pieces) | Waterfall spout to the tank |
| Real | B3 Patch | `tap` | The leaks |
| Real | B4 Fill | `circle` | The seahorse fountain's valve |
| Real | B5 The invitations | `tap` ×7 | One picture invitation per friend, into the hatch |
| Real | B6 Launch | `hold` | The launch button; the existing "Hold through the countdown and launch!" |

Deck: E1 (book), D1, M1, P1. Save: `chapter2_invitations_mask`, one bit per
friend; then the party bit, which the plan's guest row follows. The rocket is
launched here; it no longer waits to light the candle (decision 14).

### J2 — Arborist (practice in the Opera House foyer; real in the meadow)

| Part | Step | Gesture | Object |
|---|---|---|---|
| Practice | The built Tree Book test level: tree, leaf, medicine, then spray | `choice` ×3 (four pictures each); `hold` to spray | One orange-spotted patient in the Opera House foyer (`scripts/opera_tree_book_test.gd` on `dev`) |
| Real | B2 Which tree? | `choice` (4) | The book on the left; the tree in the upper right |
| Real | B3 What is wrong? | `choice` (4) | The big spotty leaf beside the tree |
| Real | B4 Which medicine? | `choice` (4) | The picture sum in the book; four medicines on the right |
| Real | B5 Spray | `hold` | The big spotty leaf, after Roshan carries the bottle over |

Deck: E1 (book), D1, D2, P1, M1, M2. Save: `chapter2_party_tree_phase` 0-4
(after each right choice and after the treatment), then the party bit; the
tree sticker stays in her Tree Book.

### J3 — Farmer (card in the Dining Room; real in the grove)

| Part | Step | Gesture | Object |
|---|---|---|---|
| Practice | PLANT, TOSS, HERD | `garden_plant`, `farm_lob`, `swipe` | The Farmer world |
| Real | B2 Gather | `tap` ×5 (the built berry pickups, seated on plants) | Ripe berries; green ones wiggle |
| Real | B5 Into the basket | `farm_lob` ×5 | Each berry toward the basket |
| Real | B6 Home | `swipe` | The basket's cart along the path |
| R3 | One more berry, for the dust bunnies | `tap` (Roshan picks it after 6 s) | The glowing berry on the nearest plant |

Deck: D1 and E1 (book), D2, D3, P1, E2, M1, M2. Save:
`chapter2_strawberry_mask` `0x1F`, then the party bit.

### J4 — Chef (Kitchen) and LAMMA-3

| Part | Step | Gesture | Object |
|---|---|---|---|
| Practice | MIX, STIR, BAKE, FROST | `pourt`, `circle`, `oven`, `swipe` | The Chef world |
| Real | B1 Mix | `pourt` | The rainbow pitcher into the shell bowl |
| Real | B2 Stir | `circle` | The bowl |
| Real | B3 Bake | `oven` | Six tins; the gold window; the mitt |
| Real | B4 Stack | `tap` ×6, biggest first | The baked rounds |
| Real | B5 Frost | `swipe` | The frosting ribbon |
| Real | B6 Strawberries | `tap` ×5 | Five spots on the tiers; the empty shell candle holder shows on the top tier from now on |
| LAMMA-3 | Egg | `tap` (auto after 6 s) | Lamma's lavender egg |

Deck: M1 (book), D1, D2, P1, E1, M2. Save: `chapter2_cake_piece_mask` `0x7F`
(the Chef now owns bits 5 and 6), `lamma_moments_seen` bit 2,
`lamma_egg_carried`.

### J5 — Painter (Craft Room)

| Part | Step | Gesture | Object |
|---|---|---|---|
| Practice | PAINT, STAMPS, GALLERY | `paint_reveal`, `tap`, `choice` | The Painter world |
| Real | B1 Paint | `paint_reveal` | The long banner, in her `attack_color` first |
| Real | B2 Stamp | `tap` ×5 | Five star outlines |
| Real | B3 Send | `choice` (3) | The party tree picture |

Deck: P1 (book), D1, D2, M1, E1. Baby Eagle always carries the banner.

### LAMMA-JOIN and J6 — Ballerina (Playroom)

| Part | Step | Gesture | Object |
|---|---|---|---|
| LAMMA-JOIN | Four finds | Seek's four-find `tap` (`scripts/games/seek.gd`) | Toy chest (wool), block tower (bounce marks), play tent (a bleat), stuffie nook (the stuffies point) |
| LAMMA-JOIN | The egg | `tap` | Roshan's egg; Lamma's yes wakes the Ballerina card |
| Practice | PEARL MIRROR, RIBBON TRAIL, GRAND TWIRL | `ballet_pose`, `ballet_ribbon`, `ballet_twirl` | The Ballerina world |
| Real | B2-B4 Mirror, ribbon, the star's twirl and the bow | The same three modes, with goals the surface can reach (build audit B2) | Kitty, Lamma and Bunny on the little stage, Lamma on the star; the music box |

Deck (the rehearsal only): M1 (book), D1, E1, P1. Save: `lamma_moments_seen`
bit 3, `lamma_joined` (which the Ballerina card follows), `friend_lamma`,
`chapter2_stuffie_ballet_done`.

### J7 — Pop Star (Opera Hall stage)

| Part | Step | Gesture | Object |
|---|---|---|---|
| Practice | The drum part | The bands commission's drumming component (new); until it exists, the show's RHYTHM `echo` | The Pop Star world |
| Real | B2 Tune up | `tap` ×2 | Daddy, then Baby Eagle |
| Real | B3 The groove | The drumming component: six forgiving taps on the glowing drum | Roshan's pastel shell drums, over the song's opening (up to 25.3 s) |

Deck: E1 (book), D1, M1, P1. Save: the party bit.

### J8 — Detective (Royal Library)

| Part | Step | Gesture | Object |
|---|---|---|---|
| Practice | SEARCH, CLUE BOARD | `lens`, `tap` | The Detective world (after its framing fix), without its crown introduction |
| Real | B2 Rainbow drips | `lens` | The storybook's pages |
| Real | B3 The rainbow page | `tap` ×6 in colour order | The drips into the rainbow's bands |
| Real | B4 The candle | `tap`, on a touch area at least 120×160 around the drawn candle | The page |

Deck: M1 (book), D1, E1, P1. Save: `rainbow_candle_found`,
`chapter2_party_event_phase` 1.

## The party and the evening

| Scene | Step | Gesture | Save |
|---|---|---|---|
| F1 | Open the doors; set the candle in its holder | `tap`, `tap` | `chapter2_lawn_started` |
| F2 | The payoff tour, four pieces; Lamma's show plays on its touch | `tap` each (auto-advance after 8 s) | `chapter2_lawn_tour` |
| F3 | Light the candle | `tap` the candle; Daddy lights it (decision 14) | `chapter2_lawn_beat` 1 |
| F4 | Dialogue | `tap` the forward picture, or wait for the voice | Beats 2-3 |
| F5 | The battle of the bands | Twelve forgiving `tap`s on the glowing drum across the whole song (the bands prototype); the taps and the song must both finish | `chapter2_band_taps`, `chapter2_band_song_position`, `chapter2_band_song_done`, then beat 5 |
| F6 | The theft | `tap` to advance | Beat 6, `chapter2_candle_taken` |
| F7 | Comfort; the wish | `tap` Lamma; `hold` on Roshan | Beat 8, `chapter2_story_complete`, `chapter2_wish_made` |
| F8 | The door | `tap` the pearl | The existing Chapter 3 reveal keys |
| E1-E3 | Supper, the movie, the sleepover | The existing comfy games | Their existing keys |

## Voice lines

**Voice sources.**

| Speaker | Source |
|---|---|
| Roshan | The existing synthetic Roshan configuration |
| Daddy | The manifest's Daddy-only "Will" filler preset. His real recordings (`daddy1.ogg` to `daddy3.ogg`) are never edited |
| The Ember King, the Prince | Two new synthetic presets, a low theatrical King and a young soft Prince, pending owner listening (decision 5) |
| The dust bunnies (Splash included) | A new small synthetic voice, used for a handful of lines |
| Lamma, Grand Puff | Sound effects only: bleats; a happy boing |
| Rumi | None, by rule |
| Baby Eagle | His existing chirp (`sparkle.ogg`) |
| Chuck | His real bark (`chuck_bark.ogg`), unaltered |
| The party guests | No new lines (decision 13); their existing clips only, unaltered |
| The band's song | The published Iko Iko v89 master, never edited or retimed, with no invented lyrics or replacement voices; whether it may ship is decision 15 |

Nothing is trained or conditioned on family recordings. Every line needs its
exact caption text, and its picture cue must be on screen while it plays.

**Existing recordings the day reuses.**

- Each practice step's exact `_stage` recording (`op_<career>_<step>_stage`),
  including the Astronaut's "Hold through the countdown and launch!", which
  the real launch reuses.
- The Tree Book test level's generated Roshan cues
  (`scripts/opera_tree_book_test.gd` on `dev`): "Which tree? Find the same
  tree.", "What is wrong? Find the orange spots.", "Orange spots need leaf
  spray. Find its bottle.", "Let's take the spray to our tree.", "Hold this
  leaf. Spray, spray!" and "Our tree feels better!", used in both the practice
  and the real level. The owner-corrected handoff's fuller cue script
  (`design/ARBORIST_TREE_BOOK_HANDOFF_2026-09-29.md` on `dev`) covers the
  other three sicknesses.
- The lawn's "Ready? Let's light our rainbow!" and "Look! Our rainbow candle
  is shining!", and "The castle found a secret sky door!".
- The comfy bedtime lines ("Goodnight, Rumi. Snuggle in!" and the others).
- The party guests' existing clips, each optional and unaltered: Wacky's
  "Ho ho! Hello there, little mermaid!" (`wacky.ogg`, F1), Faron's "Shhh...
  the babies are getting sleepy." (`faron.ogg`, protected, F2), Harper's
  "Wheee! That was amazing!" (`harper_win.ogg`, F2, after the show's bow) and
  Princess Huluu's "Thank you, Mermaid Roshan! You did a great job!"
  (`huluu_thanks.ogg`, F3).
- The Iko Iko v89 master, through the bands commission's non-destructive Ogg
  derivative (`assets/prototypes/bands/iko_iko_v89.ogg` on branch
  `codex/battle-of-bands-20260920`).

**New lines, in story order** (generated from every line the plotline marks
new):

| Scene | Speaker | Line | Voice source |
|---|---|---|---|
| Bubble Bath (optional) | Roshan | "Bubbles for the party!" | Synthetic Roshan |
| P-1 | Roshan | "Hello? Someone is shy." | Synthetic Roshan |
| P-2 | Roshan | "A little lamb! She ran away." | Synthetic Roshan |
| Day Two card | Daddy | "It's Roshan's birthday today." | Daddy filler (Will) |
| D2-OPEN-1 | Daddy | "Wake up, birthday girl!" | Daddy filler (Will) |
| D2-OPEN-1 | Roshan | "It's my birthday! Can we have a party?" | Synthetic Roshan |
| D2-OPEN-1 | Daddy | "The best party ever." | Daddy filler (Will) |
| D2-OPEN-2 | Daddy | "Invitations, a tree, a cake, a banner, a show, a band and a candle!" | Daddy filler (Will) |
| D2-OPEN-2 | Daddy | "And a place for every friend you invite!" | Daddy filler (Will) |
| D2-OPEN-2 | Roshan | "Who's the star?" | Synthetic Roshan |
| D2-OPEN-2 | Daddy | "We'll find one. There's always room for one more." | Daddy filler (Will) |
| D2-OPEN-2 | Daddy | "Let's make it together. One little job at a time." | Daddy filler (Will) |
| D2-OPEN-2 | Roshan | "One little job at a time!" | Synthetic Roshan |
| D2-OPEN-3 | Daddy | "First we practise on the Opera stage. Then we do it for real!" | Daddy filler (Will) |
| R-beats | Daddy | "Look what you made!" | Daddy filler (Will) |
| R-beats | Daddy | "One little job at a time." | Daddy filler (Will) |
| J1 | Daddy | "First, the invitations! A rocket can take them far away." | Daddy filler (Will) |
| J1 | Roshan | "A rocket for my invitations!" | Synthetic Roshan |
| J1 | Roshan | "Rainbow water for my rocket!" | Synthetic Roshan |
| J1 | Roshan | "Click, click!" | Synthetic Roshan |
| J1 | Roshan | "Patch, patch!" | Synthetic Roshan |
| J1 | Roshan | "Rainbow water!" | Synthetic Roshan |
| J1 | Roshan | "For Evie!", "For Harper and Fiona!", "For Wacky and Chuck!", "For Faron and her baby!", "For Kareem!", "For Princess Huluu!", "For Flower Friend!" | Synthetic Roshan |
| J1 | Roshan | "Fly to every friend!" | Synthetic Roshan |
| J1 | Splash | "Sorry! I love splashing!" | New dust bunny voice |
| J1 | Roshan | "Splash, splash!" | Synthetic Roshan |
| J1 | Daddy | "Righty tighty!" | Daddy filler (Will) |
| J1 | Roshan | "Fizzy rainbow!" | Synthetic Roshan |
| R1 | Roshan | "Everyone's invited, even Wacky and Chuck!" | Synthetic Roshan |
| R1 | Daddy | "Next, the party tree!" | Daddy filler (Will) |
| J2 | Roshan | "Chirp, chirp! Someone needs help!" | Synthetic Roshan |
| J2 | Roshan | "Your tree is sick?" | Synthetic Roshan |
| J2 | Daddy | "A tree doctor can help. Let's practise first!" | Daddy filler (Will) |
| J2 | Roshan | "Baby Eagle's tree needs help!" | Synthetic Roshan |
| J2 | Roshan | "Our party tree!" | Synthetic Roshan |
| J2 | Roshan | "Thank you, Baby Eagle!" | Synthetic Roshan |
| J2 | Dust bunny | "We were just napping!" | New dust bunny voice |
| J2 | Roshan | "Oops! Sorry, bunny!" | Synthetic Roshan |
| J2 | Roshan | "That's the tree's leaf!" | Synthetic Roshan |
| J2 | Roshan | "Grand Puff, you're all sparkly!" | Synthetic Roshan |
| J2 | Daddy | "Hold it down, like this!" | Daddy filler (Will) |
| J2 | Daddy | "Which one has orange spots?" | Daddy filler (Will) |
| R2 | Roshan | "Now there's shade for everyone, even Faron's baby!" | Synthetic Roshan |
| R2 | Daddy | "Next, strawberries!" | Daddy filler (Will) |
| J3 | Roshan | "Strawberries for my cake!" | Synthetic Roshan |
| J3 | Roshan | "Five red strawberries!" | Synthetic Roshan |
| J3 | Roshan | "One!" "Two!" "Three!" "Four!" | Synthetic Roshan |
| J3 | Roshan | "Not yet! Still green." | Synthetic Roshan |
| J3 | Roshan | "Where did it go?" | Synthetic Roshan |
| J3 | Roshan | "Five!" | Synthetic Roshan |
| J3 | Roshan | "Five in the basket!" | Synthetic Roshan |
| J3 | Roshan | "To the kitchen!" | Synthetic Roshan |
| J3 | Roshan | "Hey! Come back, strawberry!" | Synthetic Roshan |
| J3 | Dust bunny | "We were just playing!" | New dust bunny voice |
| J3 | Roshan | "Let's play gently." | Synthetic Roshan |
| J3 | Dust bunny | "Sorry!" | New dust bunny voice |
| J3 | Dust bunny | "Sorry! It was tickly!" | New dust bunny voice |
| J3 | Roshan | "Rainbow strawberries!" | Synthetic Roshan |
| J3 | Daddy | "One... two... three..." | Daddy filler (Will) |
| J3 | Daddy | "Heave-ho!" | Daddy filler (Will) |
| R3 | Roshan | "Five for the cake, and one for you, bunnies!" | Synthetic Roshan |
| R3 | Daddy | "Next, the cake!" | Daddy filler (Will) |
| J4 | Daddy | "Apron on, birthday chef!" | Daddy filler (Will) |
| J4 | Roshan | "Let's learn the cake!" | Synthetic Roshan |
| J4 | Roshan | "Pour, pour!" | Synthetic Roshan |
| J4 | Roshan | "Round and round! Stir, stir!" | Synthetic Roshan |
| J4 | Roshan | "Golden!" | Synthetic Roshan |
| J4 | Roshan | "Biggest first! Stack them up!" | Synthetic Roshan |
| J4 | Roshan | "Frosting!" | Synthetic Roshan |
| J4 | Roshan | "Five strawberries on top! A rainbow cake!" | Synthetic Roshan |
| J4 | Daddy | "Watch me: round and round!" | Daddy filler (Will) |
| J4 | Dust bunny | "Sorry! It was tickly!" | New dust bunny voice |
| J4 | Roshan | "Swish it away!" | Synthetic Roshan |
| J4 | Dust bunny | "Sorry! It smelled so yummy!" | New dust bunny voice |
| J4 | Roshan | "Rainbow sprinkles!" | Synthetic Roshan |
| J4 | Daddy | "Careful, it's warm. You take them out!" | Daddy filler (Will) |
| LAMMA-3 | Roshan | "Someone small wants cake!" | Synthetic Roshan |
| LAMMA-3 | Roshan | "Her egg! We'll keep it safe for her." | Synthetic Roshan |
| R4 | Roshan | "Cake for everyone, and a place for the candle!" | Synthetic Roshan |
| R4 | Daddy | "Next, the banner!" | Daddy filler (Will) |
| J5 | Roshan | "The little lamb's wool!" | Synthetic Roshan |
| J5 | Roshan | "A banner for my party! Paint, paint!" | Synthetic Roshan |
| J5 | Roshan | "Stamp, stamp! Five stars!" | Synthetic Roshan |
| J5 | Roshan | "To the party tree!" | Synthetic Roshan |
| J5 | Roshan | "Grand Puff's rainbow!" | Synthetic Roshan |
| J5 | Roshan | "Sparkly paw prints! They look pretty!" | Synthetic Roshan |
| J5 | Roshan | "Pop, pop!" | Synthetic Roshan |
| J5 | Daddy | "I've got this end!" | Daddy filler (Will) |
| R5 | Roshan | "Now everyone can see it's a party!" | Synthetic Roshan |
| R5 | Daddy | "Next, the show!" | Daddy filler (Will) |
| LAMMA-JOIN, J6 | Roshan | "Our show needs a star!" | Synthetic Roshan |
| LAMMA-JOIN, J6 | Roshan | "The little lamb! Let's find her. Gently!" | Synthetic Roshan |
| LAMMA-JOIN, J6 | Roshan | "Wool! There she is!" | Synthetic Roshan |
| LAMMA-JOIN, J6 | Roshan | "Bounce, bounce! She's playing!" | Synthetic Roshan |
| LAMMA-JOIN, J6 | Roshan | "The tent! Just like before!" | Synthetic Roshan |
| LAMMA-JOIN, J6 | Roshan | "Here's your egg. Will you be our star? There's room for everyone." | Synthetic Roshan |
| LAMMA-JOIN, J6 | Roshan | "Now we can have our show!" | Synthetic Roshan |
| LAMMA-JOIN, J6 | Roshan | "Let's learn the show!" | Synthetic Roshan |
| LAMMA-JOIN, J6 | Roshan | "Point!" | Synthetic Roshan |
| LAMMA-JOIN, J6 | Roshan | "Twirl!" | Synthetic Roshan |
| LAMMA-JOIN, J6 | Roshan | "Bow! Our show is ready!" | Synthetic Roshan |
| LAMMA-JOIN, J6 | Daddy | "One, two, three, twirl!" | Daddy filler (Will) |
| LAMMA-JOIN, J6 | Dust bunny | "Whee! Sorry!" | New dust bunny voice |
| LAMMA-JOIN, J6 | Roshan | "A rainbow spotlight!" | Synthetic Roshan |
| R6 | Roshan | "Our show has a star: Lamma!" | Synthetic Roshan |
| R6 | Daddy | "Next, the band!" | Daddy filler (Will) |
| J7 | Roshan | "Our band! Let's practise our song!" | Synthetic Roshan |
| J7 | Roshan | "Ready, band?" | Synthetic Roshan |
| J7 | Roshan | "Ukulele! Bass!" | Synthetic Roshan |
| J7 | Roshan | "Boom, boom!" | Synthetic Roshan |
| J7 | Roshan | "What a band!" | Synthetic Roshan |
| J7 | Roshan | "Bounce with the music!" | Synthetic Roshan |
| J7 | Daddy | "Tap, tap, with me!" | Daddy filler (Will) |
| J7 | Roshan | "A rainbow spotlight for our band!" | Synthetic Roshan |
| R7 | Roshan | "Our band can play for everyone!" | Synthetic Roshan |
| R7 | Daddy | "The last one! The candle!" | Daddy filler (Will) |
| J8 | Roshan | "The magic storybook!" | Synthetic Roshan |
| J8 | Roshan | "Rainbow drips!" | Synthetic Roshan |
| J8 | Roshan | "Red! Orange! Yellow!..." | Synthetic Roshan |
| J8 | Roshan | "The rainbow candle! It's not lit yet." | Synthetic Roshan |
| J8 | Daddy | "Every job is done!" | Daddy filler (Will) |
| J8 | Daddy | "This book is heavy! I'll hold it." | Daddy filler (Will) |
| J8 | Dust bunny | "Achoo! Sorry!" | New dust bunny voice |
| J8 | Roshan | "Grand Puff found it!" | Synthetic Roshan |
| R8 | Daddy | "Look what you made! Everything for the party!" | Daddy filler (Will) |
| R8 | Roshan | "A candle for my birthday wish!" | Synthetic Roshan |
| R8 | Daddy | "Everyone is waiting in the meadow!" | Daddy filler (Will) |
| F1 | Daddy | "A hat for the birthday girl!" | Daddy filler (Will) |
| F1 | Daddy | "Everyone is here, birthday girl!" | Daddy filler (Will) |
| F1 | Roshan | "Our candle goes on top!" | Synthetic Roshan |
| F2 | Roshan | "Baby Eagle's tree is all better!" | Synthetic Roshan |
| F2 | Roshan | "Our rainbow cake!" | Synthetic Roshan |
| F2 | Roshan | "My banner!" | Synthetic Roshan |
| F2 | Roshan | "Lamma is our star!" | Synthetic Roshan |
| F2 | Roshan | "We made all of this together!" | Synthetic Roshan |
| F4 | King | "Make way! Make way for the King!" | New King preset |
| F4 | Prince | "You made that?" | New Prince preset |
| F4 | Roshan | "All of us did. You can join us." | Synthetic Roshan |
| F4 | King | "A rainbow light! That belongs at a KING'S party. MY birthday party!" | New King preset |
| F4 | Prince | "Father, it's HER birthday." | New Prince preset |
| F4 | King | "Then let's see whose band is best!" | New King preset |
| F4 | Roshan | "He's so big..." | Synthetic Roshan |
| F4 | Roshan | "...but we can play our song!" | Synthetic Roshan |
| F5 | Roshan | "We played our song!" | Synthetic Roshan |
| F5 | Prince | "She did it, Father." | New Prince preset |
| F6 | King | "Enough games. I am taking the light." | New King preset |
| F6 | Prince | "You said the best band wins!" | New Prince preset |
| F6 | King | "Come, son." | New King preset |
| F6 | Prince | "I'm sorry." | New Prince preset |
| F7 | Roshan | "He took our light." | Synthetic Roshan |
| F7 | Daddy | "I'm proud of you." | Daddy filler (Will) |
| F7 | Roshan | "But you're all still here." | Synthetic Roshan |
| F7 | Daddy | "And you can still make a wish." | Daddy filler (Will) |
| F7 | Roshan | "We'll find our light together." | Synthetic Roshan |
| F8 | Daddy | "An adventure for tomorrow, birthday girl." | Daddy filler (Will) |
| F8 | Roshan | "Tomorrow!" | Synthetic Roshan |
| E1 | Roshan | "He took the candle. But not the cake!" | Synthetic Roshan |
| E2 | Roshan | "That was my birthday!" | Synthetic Roshan |
| E3 | Roshan | "Goodnight, Grand Puff. Sweet rainbow dreams!" | Synthetic Roshan |
| E3 | Roshan | "Goodnight, Kitty, Bunny and Lamma!" | Synthetic Roshan |
| E3 | Roshan | "Goodnight, Mermaid Roshan. What a birthday!" | Synthetic Roshan |

**New sound effects:** Lamma's bleats (questioning, startled, happy, soft);
Grand Puff's hop "boing"; a crowd cheer and a crowd "Oooh!"; a faint chime for
the moonflower's answer; a soft pop for each bubble; one ukulele strum and one
bass pluck for the band's tune-up (J7); a few soft ukulele strums for the wish
(F7).

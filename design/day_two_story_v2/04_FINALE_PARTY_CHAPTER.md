# 04 — The party chapter: the Ember King and the Prince

Part of the [Day Two story draft v2](README.md). Status: `CANDIDATE` story and
staging draft, 2026-09-30. It revises the implemented alpha described in
[`design/CHAPTER2_LAWN_FINALE_DRAFT_2026-09-06.md`](../CHAPTER2_LAWN_FINALE_DRAFT_2026-09-06.md)
(also `CANDIDATE`), and it follows the owner's later choice for the contest:
a battle of the bands to the recorded Iko Iko (2026-09-20), developed as a
playable prototype and fourteen scene candidates on branch
`codex/battle-of-bands-20260920` (`design/BATTLE_OF_BANDS_2026-09-20.md`, not
yet on `dev`). It keeps the owner-approved premise both share: the party in
the middle of the Sky Lagoon, Roshan's success followed by the King's cheating
theft of the candle only, and a sincerely kind Prince who is conflicted about
his father. Nothing here is implemented or accepted yet.

The story version of this chapter is section 9 of the
[plotline](00_DAY_TWO_PLOTLINE.md#9-act-iii-the-party). This file holds its
production detail. Where the two differ, the plotline wins.

## What this chapter must make a four-year-old feel

1. **Pride:** "We made all of this." Every piece at the party is something she
   made that day, every friend there came because she invited them, and she
   gets to see the show she rehearsed.
2. **Wonder:** the candle lights and the whole party glows.
3. **Brave:** someone big and loud arrives with a louder band. She feels
   small, plays her song all the way to the end anyway, and wins.
4. **Sad, but not alone:** the King cheats and takes the one light. It is his
   choice, never her failure.
5. **Held:** her friends, her Daddy and the newest, shyest friend (Lamma, the
   star of the show) close in around her. Everything else they made is still
   there.
6. **Ready:** she knows there is somewhere to go next.

No health bar, no losing, no scary faces, no lesson spoken aloud. The King is
theatrical and a bit silly; his choices still hurt.

## The stage

Location: the middle screen of the approved 6144×2048 Sky Lagoon panorama:
the "middle Sky Lagoon meadow, formerly the playground" of the bands
commission, which is the same screen the lawn alpha already uses with its
playground equipment removed. The bands prototype reconstructs the literal v5
crop (native `[1536,320,4608,2048]` from eight existing 1024 px tiles) and
forbids invented water, islands, waterfalls or mountains. Remove the
playground equipment only while the party is staged, and bring it back on
teardown (the bands work order).

| Band | Contents |
|---|---|
| Back | The castle on the horizon; the path from the far northern mountains |
| Middle | One broad wooden stage. On its left, the family band's places: Roshan's pastel shell drums (two sticks, no microphone), Daddy's four-string ukulele, Baby Eagle's turquoise bass with exactly four strings, four posts and four pegs. In its middle, the one six-tier cake on a visible pedestal, never floating, with its empty shell candle holder until F1. Its right side stays open for the royals, who bring the lead guitar and the drum kit with exactly one kick. The healed party tree stands at the stage's side with the banner in its branches (Arborist, Painter) |
| Front | The stuffies' little curtain and the music box, for Lamma's show (Ballerina); the friends in a shallow arc, each in a painted party hat; the dust bunnies at the stage's edge |

All five musicians, the kit's feet and the cake's pedestal rest on the one
shared stage (the bands work order). Keep the cake visible between the two
bands for touch, rather than copying the storyboard's wide shot blindly.
Where the party tree stands in the literal panorama is an owner staging
question ([decision 15](README.md#owner-decisions)).

**The party map.** Three jobs were made for one friend each, so those friends
stand nearest their piece; everyone else fills the arc:

| Guest (protected portrait) | Stands | Their piece |
|---|---|---|
| Faron and her baby (`mama_baby.png`) | In the party tree's shade | The tree's shade (J2) |
| Flower Friend (`flower_friend.png`) | Beneath the banner | The banner's colours (J5) |
| Evie (`pearl_friend.png`) | Right in front of the cake | The cake (J4) |
| Wacky and Chuck (`wacky_chuck.png`) | The arc's end nearest the path | They came furthest, because the invitations reached them (J1) |
| Harper and Fiona (`two_friends.png`), Kareem (`kareem.png`), Princess Huluu (`huluu.png`) and Rumi (existing frames) | Between them | The show, the band and the candle are for everyone |

The dust bunnies (J3) bounce at the stage's edge in party hats. The arc stays
shallow and never covers the stage.

Replace these current placeholders (see the [graphics audit](06_GRAPHICS_AUDIT.md)
for the detailed fixes):

- the procedural triangle party hats → painted hat cutouts fitted per guest;
- the 90×145 px banner in the top-left corner → the full banner in the tree;
- the "Happy Birthday, Roshan!" headline text → no text; the scene says it;
- the flat orange ellipse and thin white ring of the old protection rounds →
  nothing: the battle of the bands has no attacks to warn about;
- the stacked two-speaker text captions → one short caption line for the
  grown-up, with every line voiced by its own speaker.

## Beat sheet

Timings are targets for an unhurried first play; nothing is timed against the
child. "Touch" means one intentional tap on a visible object. Every scene ends
at a natural stopping point with a save.

### F1 — To the party (about 20 s)

| | |
|---|---|
| Where it starts | Main Hall, after the Detective job. Daddy's Party Plan has all eight pictures filled and its guest row full; the big doors glow; Roshan holds the unlit candle |
| Child | Touches the glowing doors (the current "party hotspot"); then, in the meadow, touches the cake's empty holder to set the candle in it |
| On screen | Daddy puts a painted party hat on Roshan (it matters in F5 and F7). Roshan swims out of the castle and along the Sky Lagoon path; the rainbow friend hops ahead as the guide (he has no wings); Baby Eagle flies ahead to his branch. The first thing she sees is the pink tree with her banner in it; then the meadow comes into view: the stage, and every friend who got an invitation, waving |
| Voice | Daddy: "A hat for the birthday girl!" A crowd cheer (sound effect); Wacky's existing "Ho ho! Hello there, little mermaid!" may follow as he and Chuck wave from the end nearest the path. Daddy: "Everyone is here, birthday girl!" Roshan: "Our candle goes on top!" |
| Save | Existing `chapter2_lawn_started` |

### F2 — Everything we made, and Lamma's show (about 60–90 s)

The payoff tour. Each piece glows once, in the order it was made: the tree,
the cake (with the strawberries on it), the banner and the show. The friends
themselves are the invitations' piece, and the band plays in F5. The child
touches each piece to hear who helped and see it come alive.

| Touch | What happens | Its friend | Voice |
|---|---|---|---|
| Party tree | Blossoms drift down; Baby Eagle chirps on his branch | Faron rocks her baby in the shade (her whole picture sways) | Roshan: "Baby Eagle's tree is all better!" Faron's existing "Shhh... the babies are getting sleepy." may follow |
| Cake | The five strawberries twinkle | Evie leans in | Roshan: "Our rainbow cake!" |
| Banner | It ripples in the breeze; the five stars twinkle | Flower Friend sways beneath its colours | Roshan: "My banner!" |
| The show | The music box plays and the little curtain opens: Kitty and Bunny dance either side, Lamma on the star twirls the star's twirl, and all three bow. Then Lamma bounces to Evie, who hugs her (Evie staged with her Seek sheet so only one Lamma is on screen) | Every friend watches; Harper and Fiona bounce | Roshan: "Lamma is our star!" A crowd cheer; Harper's existing "Wheee! That was amazing!" may follow |

Guest reactions are whole-picture moves only (sway, lean, bob, bounce); the
protected portraits are never re-posed or edited. The optional clips are the
guests' existing recordings, unaltered, and never delay the next touch.

Then Roshan turns to everyone: **"We made all of this together!"** A friend
straightens a crooked hat.

- Touches are optional after the first: a gentle pointer moves on after about
  8 s of no input. Passive waiting never lights the candle.
- The show needs one touch and plays for about 20 s: the child danced it in
  the rehearsal, and here she watches her star.
- Save: `chapter2_lawn_tour` bitmask (new, additive), one bit per piece shown.

### F3 — Light our rainbow (about 15 s)

| | |
|---|---|
| Child | Touches the candle (moving hand pointer on it) |
| On screen | Daddy leans in beside the cake (his whole picture leans), a small rainbow spark hops to the wick, and the rainbow flame opens; a soft crowd "Oooh!" plays (a crowd sound effect, never family voices); the candle's glow tints the whole scene warm |
| Voice | Roshan: "Ready? Let's light our rainbow!" … "Look! Our rainbow candle is shining!" Princess Huluu, arms folded all party, bounces, helmet and all; her existing "Thank you, Mermaid Roshan! You did a great job!" may follow. Chuck's real bark, once |
| Hidden hook | For one second, far away on the castle, a moonflower shape glows in answer (sets up the Chapter 3 door; see F8) |
| Save | Existing ignition milestone: `chapter2_lawn_beat = 1`, party/candle keys |

Hold the lit candle on screen for at least 2.4 s before anything else moves.
Who lights it is decision 14: this draft follows the recommended answer,
Daddy, because the Astronaut's rocket now carries the invitations. The
alternative keeps the built walk-and-press rocket ignition (`OQ-LAWN-ROCKET`
on `dev`), with the rocket back from delivering the invitations.

### F4 — Two unexpected guests (about 40 s)

Heavy footsteps come up the path from the north:

- **The Ember King:** broad, slow, heavy steps; cape sweeping; chest out; a
  big lead electric guitar on his back. No fire, no damage, and nothing
  shakes: the footsteps are sound only.
- **The Prince:** four-fifths of the King's height, quick and quiet, with his
  drumsticks. He looks at the **people** first, not the candle.

They climb onto the open side of the stage: the King swings his guitar round,
and the Prince sits behind his enormous drum kit.

| # | Speaker | Line | Acting |
|---|---|---|---|
| 1 | King | "Make way! Make way for the King!" | Arms wide on the stage |
| 2 | Prince, quietly | "You made that?" | Looks at the cake, then at Roshan |
| 3 | Roshan | "All of us did. You can join us." | Open hands toward the party |
| 4 | — | — | The Prince nearly smiles. The King steps between them |
| 5 | King | "A rainbow light! That belongs at a KING'S party. MY birthday party!" | Points at the candle with a big claw |
| 6 | Prince | "Father, it's HER birthday." | A small step forward, hand half-raised |
| 7 | King | "Then let's see whose band is best!" | Strikes one loud chord |
| 8 | Roshan, softly | "He's so big…" | Looks up at him, then back at her friends |
| 9 | Roshan | "…but we can play our song!" | Picks up her two sticks; Daddy takes his ukulele and Baby Eagle flies down to his bass |

- Each line advances when the child touches the big forward picture (current
  control), or automatically after its voice finishes plus 1 s, whichever is
  later. Never faster than the voice.
- Save: existing beats 2 and 3.

### F5 — The battle of the bands (about 100 s)

The bands commission's prototype, joined to the production route: twelve
forgiving intentional taps on the glowing drum across the published Iko Iko
v89 master (91 s, unedited). No timing deadline or failure state applies.
Both the taps and the song must finish before the story moves on; finished
taps never skip unfinished music, and finished music never replays as a debt.
Passive, wrong, repeated and second-finger input earn nothing; focus loss
pauses and keeps the song's position (all covered by the prototype's focused
probe on its branch).

| Time | Scene | On stage |
|---|---|---|
| 0.000–3.583 s | `BAND-01` | Ready: Roshan raises her two sticks and looks to her bandmates; the single candle glows on the supported cake |
| 3.583–25.303 s | `BAND-02` to `BAND-04` | Roshan starts the groove on the upper tom heads; Daddy answers on ukulele; Baby Eagle plucks the bass line |
| 25.303–31.062 s | `BAND-05` | The King's first break: a theatrical lead-guitar flourish with an open-mouthed growl; the candle does not move |
| 31.062–48.268 s | `BAND-06`, `BAND-07` | Roshan answers without fear (two toms, one light cymbal); she cues Daddy and Baby Eagle for a call and response |
| 48.268–54.027 s | `BAND-08` | The Prince's break: a two-stick fill round his many toms, then one cymbal tap; the single kick and the crest stay unchanged |
| 54.027–83.060 s | `BAND-09`, `BAND-10` | Everyone finds the groove again; Roshan lands her last big beat and raises both sticks in delight |
| 83.060–91.000 s | `BAND-11` | The final interruption: the King's last flourish with the Prince's fill. The last loud chord blows Roshan's party hat off; it tumbles off the stage behind the stuffies' curtain (the set-up for F7) |

- The break times are the recording's measured arrangement (the bands audio
  cue sheet); which royal each break belongs to is editorial and awaits the
  owner's local listening review.
- The hat's tumble is this draft's addition to `BAND-11`: a comic beat, never
  a push.
- **The payoff.** The song ends. The friends wave their hats; the Prince, behind
  his drums, claps once before he can stop himself.

| Speaker | Line |
|---|---|
| Roshan | "We played our song!" |
| Prince, quietly | "She did it, Father." |

Saves: the band's taps, song position and completion as they happen (new and
additive), then the existing beat 5. A save that already won the old contest
(`chapter2_protection_rounds` 3) counts the battle as won.

### F6 — The King cheats (about 20 s)

This is a new choice by the King after Roshan's band won, not something she
could have stopped (`BAND-12`, `BAND-13`, 91–103 s of the scene plan). The
child only watches (touch to advance).

| # | Speaker | Line | Acting |
|---|---|---|---|
| 1 | King | "Enough games. I am taking the light." | Straightens up; lifts one hand toward the cake, his guitar still strapped on |
| 2 | — | — | His royal magic lifts **only the candle**, still lit, from the intact cake into his free palm |
| 3 | — | — | Hold one composition that shows all three together: the King holding the lit candle, the intact cake with its **empty candle place**, and Roshan |
| 4 | Prince | "You said the best band wins!" | Steps toward his father with one empty open hand |
| 5 | King | "Come, son." | Turns away with the candle; does not look back |
| 6 | — | — | The Prince looks at his father, then at Roshan. He starts to speak and can't |
| 7 | Prince, to Roshan | "I'm sorry." | Hands open, eyes down |
| 8 | — | — | They leave the stage together and walk down the path. Halfway, the Prince looks back once. The rainbow glow of the candle grows smaller and disappears |

- The candle keeps the same display size on the cake and in the King's hand
  (existing rule, 90 px frame).
- The Prince leaves with his father. He is not left behind as a guest, and
  nothing implies his objection made Roshan responsible.
- Save: existing beat 6 (theft) and the candle keys.

### F7 — What he couldn't take (about 60 s)

| # | Speaker | Line | Acting |
|---|---|---|---|
| 1 | — | — | Quiet. The music has stopped. The warm candle tint drains from the scene. Daddy and Baby Eagle move close to Roshan (`BAND-14`) |
| 2 | Roshan | "He took our light." | Looks at the empty candle holder; her tail droops; the approved self-hug gesture |
| 3 | — | — | **Lamma**, the shyest friend and the star of the show, bounces out from behind the stuffies' curtain with Roshan's party hat, which tumbled there in F5, and holds it up |
| 4 | Lamma | (a soft bleat: a new lamb sound effect; she has no words) | |
| 5 | — | — | Roshan puts the hat back on. The friends close in around her. Daddy hugs her (a callback to the Day One epilogue hug) |
| 6 | Daddy | "I'm proud of you." | |
| 7 | — | — | Roshan looks around: the tree, the cake, the banner, the show, her band, the friends; each bobs as she sees it |
| 8 | Roshan | "But you're all still here." | Stands tall |
| 9 | Daddy | "And you can still make a wish." | |
| 10 | Roshan, whispering | "We'll find our light together." | Eyes closed, hands together (the approved clasped-hands gesture); sparkles gather in her hands while the child holds; Daddy strums his ukulele softly (a few new strum sounds, not the song); everyone sways |
| 11 | — | — | She opens her hands; the sparkles float up into the evening sky, over the castle |

- **Child:** two acts, neither of which can fail. A glowing hand on Lamma
  holding the hat: touching her puts the hat back on Roshan, the child's own
  act of accepting comfort. Then a hold on Roshan: her wish.
- **Save:** existing beat 8 and `chapter2_story_complete`, plus
  `chapter2_wish_made` (new, additive). The reassurance checkpoint stays
  separate from the theft, so restarting after the theft can never skip the
  kind ending (existing rule).
- **Why a wish:** everything the jobs made is still here. Only the candle, the
  light to wish on, is gone, and the wish shows the child it was never the
  candle's ([plotline: what no job makes](00_DAY_TWO_PLOTLINE.md#what-each-job-gives-the-party)).

### F8 — The door wakes (about 30 s)

The sun sets over the cloud sea. The friends wave goodbye. Everyone else walks
back to the castle together, the stuffies riding on the cake's cart, Baby
Eagle overhead, Grand Puff hopping ahead, the dust bunnies rolling behind.

In the Main Hall, the moonflower relief on the wall is glowing: it woke when
the rainbow candle was lit (F3), just as Roshan wished.

| Speaker | Line |
|---|---|
| Roshan | "The castle found a secret sky door!" (existing voiced line) |
| Daddy, yawning | "An adventure for tomorrow, birthday girl." |
| Roshan | "Tomorrow!" |

- One large moving pointer on the pearl; a touch opens it and saves (the
  existing Fairy Conservatory reveal). Today it only runs on entering the
  castle from outside, so it must also run here, at the end of the party.
- Then the birthday evening, section 10 of the
  [plotline](00_DAY_TWO_PLOTLINE.md#10-epilogue-birthday-evening): supper
  with the cake, the movie of the day, and the birthday sleepover, built from
  the existing comfy games.
- Which next adventure the door opens is an owner decision; see
  [open decisions](README.md#owner-decisions).

## The two royals

### The Ember King — the loud one

- **Wants:** to be the centre of the brightest party, and to be admired.
- **Believes:** being a king means everything bright is his.
- **Speaks:** short declarations: "Make way!", "Then let's see whose band is
  best!", "Come, son." Loud and theatrical; his indignation can be funny.
- **Plays:** lead electric guitar, with a big flourish and an open-mouthed
  growl on his breaks. The growls are the recording's own; he gets no
  invented lyrics.
- **Moves:** slow, heavy and square. Chest leads.
- **Never:** threatens to hurt, taunts Roshan about being small or weak, or is
  shown as justified because he felt left out.
- **Look (locked, V4):** stocky red-scaled turtle-dragon, cream muzzle, amber
  eyes (both visible), obsidian crown and shell with glowing orange seams,
  black spiky mane, charcoal armour with chain belt, enormous aubergine cape.
  Height 288 px on the shared ground plane (1.34× Roshan).

### The Prince — the kind one

- **Wants:** to be included; he notices people before things.
- **Believes:** he should obey his father, and is starting to doubt it.
- **Speaks:** quietly, in few words, always about fairness or other people.
- **Plays:** a comically elaborate metal drum kit, many toms and cymbals but
  exactly one kick; the crowned-flame family emblem on it is a trial, not
  established canon.
- **Moves:** narrow, diagonal, quick and soft ("Cinderstep"); his gaze returns
  to Roshan while his body follows the King.
- **Arc in this chapter:** notices → invites himself a little ("You made
  that?") → objects ("It's her birthday") → plays for his father's band →
  admires ("She did it") → objects to the cheat → apologises → leaves ashamed,
  looking back once.
- **Never in Chapter 2:** named romance, hearts, a kiss, or being rewarded for
  helping. Later affection must come from his own repeated choices.
- **Look (locked, recovered identity):** slender red/coral turtle-dragon,
  cream muzzle, amber eyes, asymmetrical black fringe, short obsidian horns,
  sleeveless charcoal jacket with an ember-heart clasp, long split coat tails,
  a compact shell with exposed red skin around it and no centre-back coat
  panel. Always about 80% of the King's height (230 px), never miniature.
- **Name:** the Prince has no name in canon. Giving him one is an owner
  decision.

## Voice and caption plan

Today every lawn line plays in the synthetic Roshan voice, including the
King's and Prince's, and the captions read like a script ("King: … Prince: …").
A four-year-old cannot tell who is talking.

- Give the King and the Prince their own speaking voices. The recommended
  alpha is two new synthetic voices in the existing pipeline (a low,
  theatrical King; a young, soft Prince), pending owner listening. No family
  voice is cloned.
- Every line is voiced by its speaker, and the speaker visibly acts while it
  plays (mouth or body movement, never a still card).
- The battle's objective needs an exact spoken cue with a visual pointer: the
  bands work order names the missing key `bands_tap_glowing_drum`, and a
  caption or an unrelated cheer does not count.
- Captions: one short line for the adult, no speaker labels, never over a
  face, hidden during the song except the one-word cue.
- Full line list for recording: see the [voice lines](03_LEVEL_DESIGN.md#voice-lines).

## Animation needs

| Character | Needed | Exists today |
|---|---|---|
| Ember King | Walk in; point; strum and flourish on the guitar; lift the candle by royal magic; hold it; turn and walk away | One static V4 cutout (`assets/chapter2/ember_alpha/king_v4_cutout.png`); on the bands branch, guitar-playing scene candidates and bounded new instrument poses awaiting approval. The owner reference sheet's side, back and expression views can be isolated first ([GFX-CHAR-KING-01](06_GRAPHICS_AUDIT.md#gfx-char-king-01)) |
| Prince | Walk (sleek), idle glance, drum fill, clap once, apologise, look back while walking away | One idle frame at runtime; on the bands branch, kit-playing candidates awaiting approval. The V2 motion package (`idle_glance`, a 16-frame `sleek_walk`, `cinderstep`; motion in REVIEW) is recorded but its atlas is not in the current tree and must be recovered from history ([GFX-CHAR-PRINCE-01](06_GRAPHICS_AUDIT.md#gfx-char-prince-01)) |
| Roshan | Swim, set the candle, drum strike, contact and rebound, raise both sticks, sad droop, hat on, stand tall | Swim and reach atlases, the approved 16-pose gesture sheet (`roshan_gestures.png`: surprise, clasped hands, pointing, self-hug, hope, cheers, holding) and her Pop Star outfit. Readable drum strike, contact and rebound poses are still needed (the bands work order: contact on the upper heads, not the shell fronts). A sad droop is an art gap |
| Daddy | Strum the ukulele; lean in to light the candle; hug | Book portrait (whole-picture moves only); ukulele candidates on the bands branch awaiting approval |
| Baby Eagle | Chirp on his branch, pluck the bass, step closer | Book Baby Eagle art; bass candidates on the bands branch, whose four strings, posts and pegs must survive every frame |
| Friends | Hat wobble, lean in, bob to the band, wave hats, wave goodbye | Protected static portraits: motion only as whole-card squash, bob or tilt; never repaint them |
| Stuffies (Kitty, Bunny, Lamma) | The show's twirls and bow; Lamma hops out and holds up the hat | Book dolls (damaged crops, [GFX-CHAR-DOLLS-01](06_GRAPHICS_AUDIT.md#gfx-char-dolls-01)); Seek atlas for Lamma, which is off-model ([GFX-LAMMA-01](06_GRAPHICS_AUDIT.md#gfx-lamma-01)); star-twirl and hat-offer poses needed in the canonical egg-carrying design |
| Rainbow friend | Hop and bounce in the front row | Static rainbow friend card; hop motion needed |
| Rumi | Idle sway, wave | Existing eight-pose atlas only. She is on IP hold: no new frames, no regeneration, no voice |
| Props | The shared stage and the cake pedestal; the stuffies' little curtain; the instruments | The bands commission's stage (a transparent full-canvas generation, with a runtime version of at most 1024 px) and pedestal; the curtain is new small art |

## Cinematics

The lawn alpha's nine Grok shot cards (C2-01 to C2-09) are
`GENERATION_READY: false`, blocked on clean approved first frames. For the
contest, the bands commission's packet replaces them: 14 full-frame scene
candidates and 19 short V1 shot cards (`BAND-01` to `BAND-14`), with 91
seconds of song and an 18-second story coda, published and remotely verified
on its branch. Its generation readiness is blocked by first-frame, continuity
and topology approval, and its delivery acceptance is false. The other beats
(arrival, tour and show, candle, comfort, door) need revised cards. Until
full-frame cinematic delivery is accepted under `AGENTS.md`, every beat above
plays as gameplay staging.

## What changes from the implemented alpha

| Area | Implemented alpha (2026-09-06) | This draft |
|---|---|---|
| Party payoff | Static collage; one line | Touch-to-thank tour of the tree, cake, banner and Lamma's show (F2), each with the friend it was made for |
| Guests | Eight portraits in a generic arc | Invited by Roshan's rocket in J1; the three friends a job was made for stand beside their piece |
| Party tree | None | Healed Arborist tree at the stage's side |
| Banner | Tiny 90×145 px card, top-left | Full banner strung in the tree |
| Hats | Procedural triangles | Painted hat cutouts per guest |
| Headline | "Happy Birthday, Roshan!" text on screen throughout, even during the theft | Removed |
| Stage | Lawn staging with the playground removed | One shared stage in the same middle meadow, with the cake on a pedestal (the bands commission) |
| Candle | The Astronaut's rocket, walk-and-press | Lit by Daddy (decision 14); the rocket carried the invitations |
| Contest | Three stomp-and-dodge protection rounds | The battle of the bands to the unedited Iko Iko: twelve forgiving drum taps, no failure |
| Voices | All lines in synthetic Roshan's voice | Each speaker voiced; King and Prince get their own voices |
| King motion | None | Guitar, royal magic, walk away |
| Comfort | Roshan's line only | Lamma, the star, brings the hat; Daddy's hug; Daddy's soft ukulele |
| The King's motive | Said once, in text | Spoken: "MY birthday party!", as the production spine's canon has it |
| The wish | None | Daddy: "You can still make a wish"; the child holds; the door answers |
| After the party | Back to the Main Hall; an unrelated Family Evening | The door wakes; then supper with the cake, the movie of the day and the sleepover |
| Ending | Returns to Main Hall with a stale "north-star clue" objective | Evening walk home; the sky door opens in the Main Hall |
| Stale lines | "A little ember silhouette is watching the party!" and "His little son's silhouette points to the bright north-star clue!" fire from `scripts/main.gd`. On `dev` the alpha repair of 2026-09-30 replaced the second with the voiced "The Ember King took our glowing candle. Follow the north star!" | Removed: after the theft the day goes on to the wish and the door |

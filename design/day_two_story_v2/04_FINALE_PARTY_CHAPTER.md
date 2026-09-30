# 04 — The party chapter: the Ember King and the Prince

Part of the [Day Two story draft v2](README.md). Status: `CANDIDATE` story and
staging draft, 2026-09-30. It revises the implemented alpha described in
[`design/CHAPTER2_LAWN_FINALE_DRAFT_2026-09-06.md`](../CHAPTER2_LAWN_FINALE_DRAFT_2026-09-06.md)
(also `CANDIDATE`). It keeps that draft's owner-approved premise: the Sky
Lagoon lawn, a protection victory followed by the King's cheating theft of
the candle only, and a sincerely kind Prince who is conflicted about his
father. Nothing here is implemented or accepted yet.

The story version of this chapter is section 9 of the
[plotline](00_DAY_TWO_PLOTLINE.md#9-act-iii-the-party). This file holds its
production detail. Where the two differ, the plotline wins.

## What this chapter must make a four-year-old feel

1. **Pride:** "We made all of this." Every piece on the lawn is something she
   made that day, and she gets to touch each one and see who helped.
2. **Wonder:** her rocket lights the candle and the whole party glows.
3. **Brave:** someone big and loud arrives. She feels small, and protects her
   friends anyway, and wins.
4. **Sad, but not alone:** the King cheats and takes the one light. It is his
   choice, never her failure.
5. **Held:** her friends, her Daddy and the newest, shyest friend (Lamma) close
   in around her. Everything else they made is still there.
6. **Ready:** she knows there is somewhere to go next.

No health bar, no losing, no scary faces, no lesson spoken aloud. The King is
theatrical and a bit silly; his choices still hurt.

## The stage

Location: the central screen of the approved 6144×2048 Sky Lagoon panorama
(the current lawn crop), with the healed **party tree** from the Arborist job
standing left of centre. Three depth bands:

| Band | Contents |
|---|---|
| Back | The blooming party tree; the birthday banner strung between two of its branches (Painter); Baby Eagle on a branch; the castle on the horizon |
| Middle | The shell table with the one six-tier cake and its empty shell candle holder, waiting for the candle Roshan brings (Farmer, Chef, Detective); the parked rocket beside it (Astronaut); Rumi on a small shell stage with the microphone (Pop Star); guests in a shallow arc, each in a painted party hat and each nearest the piece made for them (the party map below) |
| Front | A picnic blanket with the stuffie team (Kitty, Bunny and Lamma) and the music box (Ballerina); dust bunnies bouncing at the edges; the path in from the right |

The **right third of the lawn stays open**: the royals enter there and the
protection rounds happen there, so the child never has to find Roshan among
the guests. Roshan starts centre-right, the rainbow friend at her feet.

**The party map.** Every job made its piece for someone
([plotline: what each job gives the party](00_DAY_TWO_PLOTLINE.md#what-each-job-gives-the-party)),
so each guest stands in the arc nearest their piece and the eight pieces read
as one party:

| Guest (protected portrait) | Stands | Their piece |
|---|---|---|
| Faron and her baby (`mama_baby.png`) | The arc's left end, in the tree's deepest shade | The party tree's shade (J1) |
| Flower Friend (`flower_friend.png`) | Under the banner | The banner's colours (J4) |
| Evie (`pearl_friend.png`) | At the table, beside the cake | The cake (J3) |
| Harper and Fiona (`two_friends.png`) | At the stuffie blanket's edge | The stuffie dance (J5) |
| Kareem (`kareem.png`) | Furthest back, his big chair facing Rumi's stage | The song (J6) |
| Princess Huluu (`huluu.png`) | By the rocket | The rocket's spark (J7) |
| Wacky and Chuck (`wacky_chuck.png`) | The arc's right end, nearest the path | The invitations: they came furthest |

The dust bunnies (J2) bounce at the blanket's edges in party hats. The arc
stays shallow and never enters the open right third.

Replace these current placeholders (see the [graphics audit](06_GRAPHICS_AUDIT.md)
for the detailed fixes):

- the procedural triangle party hats → painted hat cutouts fitted per guest;
- the 90×145 px banner in the top-left corner → the full banner in the tree;
- the "Happy Birthday, Roshan!" headline text → no text; the scene says it;
- the flat orange ellipse and thin white ring used in battle → painted ember
  warnings and a sparkling safe spot. Existing house-style effects can be
  reused first: `assets/opera/worlds/props/fx_telegraph_ring.png` (gold
  spiked ring with navy outline; an ember-tinted derivative, flattened onto
  the ground plane, as the stomp warning), `fx_dust_puff.png` (stomp dust)
  and `fx_dizzy_stars.png` (the King's dizzy spin);
- the stacked two-speaker text captions → one short caption line for the
  grown-up, with every line voiced by its own speaker.

## Beat sheet

Timings are targets for an unhurried first play; nothing is timed against the
child. "Touch" means one intentional tap on a visible object. Every scene ends
at a natural stopping point with a save.

### F1 — To the party (about 20 s)

| | |
|---|---|
| Where it starts | Main Hall, after the Detective job. Daddy's Party Plan has all eight pictures filled; the big doors glow; Roshan holds the unlit candle |
| Child | Touches the glowing doors (the current "party hotspot"); then, on the lawn, touches the cake's empty holder to set the candle in it |
| On screen | Daddy puts a painted party hat on Roshan (it matters in F4 and F7). Roshan swims out of the castle and along the Sky Lagoon path; the rainbow friend hops ahead as the guide (he has no wings); Baby Eagle flies above; the lawn comes into view with everyone waiting |
| Voice | Daddy: "A hat for the birthday girl!" A crowd cheer (sound effect); Wacky's existing "Ho ho! Hello there, little mermaid!" may follow as he and Chuck wave from the end nearest the path. Daddy: "Everyone is here, birthday girl!" Roshan: "Our candle goes on top!" |
| Save | Existing `chapter2_lawn_started` |

### F2 — Everything we made (about 60–90 s)

The payoff tour. Each piece glows once, in the order it was made: six stops,
because the strawberries ride on the cake and the candle was set in F1. The
child touches it to hear who helped, see it come alive and see the friend it
was made for. This replaces a checklist with the child's own work.

| Touch | What happens | Its friend | Voice |
|---|---|---|---|
| Party tree | Blossoms drift down; Baby Eagle chirps from his branch | Faron rocks her baby in the shade (her whole picture sways) | Roshan: "Baby Eagle's tree is all better!" Faron's existing "Shhh... the babies are getting sleepy." may follow |
| Cake | The five strawberries twinkle | Evie leans in beside it | Roshan: "Our rainbow cake!" |
| Banner | It ripples in the breeze; the five stars shine | Flower Friend sways beneath its colours | Roshan: "My banner!" |
| Stuffies | Kitty, Bunny and Lamma do their little bow; then Lamma bounces to Evie, who hugs her (Evie staged with her Seek sheet so only one Lamma is on screen) | Harper and Fiona bounce at the blanket's edge | Roshan: "Our stuffie team!" Harper's existing "Wheee! That was amazing!" may follow |
| Rumi | Rumi waves from her shell stage (existing wave frames); the microphone plays a two-note chime | Kareem, furthest back, leans toward the music | Roshan: "Rumi's song!" (Rumi herself has no voice; the chime is music) |
| Rocket | It wiggles, ready | Princess Huluu leans in, arms still folded | Roshan: "Our little rocket!" |

Guest reactions are whole-picture moves only (sway, lean, bob, bounce); the
protected portraits are never re-posed or edited. The optional clips are the
guests' existing recordings, unaltered, and never delay the next touch.

Then Roshan turns to everyone: **"We made all of this together!"** A friend
straightens a crooked hat; the dust bunnies bounce.

- Touches are optional after the first: a gentle pointer moves on to the
  rocket after about 8 s of no input. Passive waiting never lights the candle.
- Save: `chapter2_lawn_tour` bitmask (new, additive), one bit per piece shown.

### F3 — Light our rainbow (about 20 s)

| | |
|---|---|
| Child | Touches the rocket (moving hand pointer on it) |
| On screen | Roshan swims to the rocket, reaches up and presses its brass button (the implemented approach and hand-contact behaviour); one small spark travels up to the candle; the rainbow flame opens; a soft crowd "Oooh!" plays (a crowd sound effect, never family voices); the candle's glow tints the whole scene warm |
| Voice | Roshan: "Ready? Let's light our rainbow!" … "Look! Our rainbow candle is shining!" Princess Huluu, arms folded all party, bounces, helmet and all; her existing "Thank you, Mermaid Roshan! You did a great job!" may follow |
| Music | "Happy Birthday" begins as an instrumental score from Rumi's shell stage (existing Pop Star performance score). Rumi sways in her existing idle frames: she is on IP hold, so she gets no new frames and no voice |
| Hidden hook | For one second, far away on the castle, a moonflower shape glows in answer (sets up the Chapter 3 door; see F8) |
| The scout | In the hedge beside the path, an ember imp (the same kind as the imp apprentices at every Opera practice) peeks out, stares at the candle, gasps and scurries down the hill. Imp: "The rainbow light! The King must see this!" Roshan: "The little imp from the Opera?" The song keeps playing |
| Save | Existing ignition milestone: `chapter2_lawn_beat = 1`, party/candle keys |

Hold the lit candle on screen for at least 2.4 s before anything else moves.
Leaving or switching apps before the button press cancels the unfinished walk
(already implemented).

### F4 — Two unexpected guests (about 40 s)

The song is cut off by three heavy **stomps** that make the cake plates
rattle. The guests' hats wobble, and Roshan's own hat tumbles off and rolls
under the stuffie blanket (the set-up for F7). From the right, up the path:

- **The Ember King:** broad, slow, heavy steps; cape sweeping; chest out.
  Every step puffs a little ember dust from the grass (no fire, no damage).
  His imp scout rides on his shoulder, pointing at the candle.
- **The Prince:** four-fifths of the King's height, quick and quiet, stepping
  around his father's dust. He looks at the **people** first, not the candle.

| # | Speaker | Line | Acting |
|---|---|---|---|
| 1 | King | "Make way! Make way for the King!" | Arms wide; stops on the open grass |
| 2 | Prince, quietly | "You made that?" | Looks at the cake, then at Roshan |
| 3 | Roshan | "All of us did. You can join us." | Open hands toward the party |
| 4 | — | — | The Prince nearly smiles. The King steps between them |
| 5 | King | "A rainbow light! That belongs at a KING'S party. MY birthday party!" | Points at the candle with a big claw |
| 6 | Prince | "Father, it's HER birthday." | Small step forward, hand half-raised |
| 7 | King | "Then show me how strong you are!" | Stamps a heavy foot; a glowing ember ring marks the open grass |
| 8 | Roshan, softly | "He's so big…" | Looks up at him, then back at her friends |
| 9 | Roshan | "…but I can keep my friends safe." | Moves in front of the friends |

- Each line advances when the child touches the big forward picture (current
  control), or automatically after its voice finishes plus 1 s, whichever is
  later. Never faster than the voice.
- The composition settles into the playable arena before any attack. No
  impact crosses from the talking into the play (existing rule).
- Save: existing beats 2 and 3.

### F5 — Protect the party (about 90–150 s)

The rounds reuse the Grand Puff boss rules already configured in
`scripts/chapter_two_ember_encounter.gd`: a fixed painted warning, one-finger
movement out of it, then a large glowing target to tap during the opening.
It is the move the child already learned against Grand Puff in the Day One
game: wait for the big gold star, tap it, and Roshan's magic brush sends
sparkles in the colour she chose in the Craft Room. (Book One says "Sparkles
flew from Roshan's shell"; the game uses the brush, and Day Two keeps the
brush so the prop stays consistent.)

**The one cycle every round uses:**

1. **Warning.** The King lifts a foot high (anticipation). A glowing ember
   crack spreads on the grass where it will land: painted, pulsing, with a
   rim. A sparkling lily-pad **safe spot** appears clear of it, with a moving
   hand on it.
2. **Move.** The child touches the safe spot (or drags); Roshan swims there.
3. **Stomp.** The foot lands. A soft puff of ember dust and a small screen
   bounce. Friends flinch but are safe behind the shelter.
4. **Opening.** The King wobbles off balance ("Whoa!") and the big gold
   star from Day One appears on his crown crest.
5. **Counter.** The child taps the gold star. Sparkles in her chosen colour
   fly from Roshan's magic brush, the King spins dizzy for a moment (comic,
   never hurt), and a
   **friend adds a layer to the shelter**.

**The three rounds, each paying off a Day One friendship:**

| Round | King's pattern (existing engine phase) | Friend who helps | Shelter layer | Voice |
|---|---|---|---|---|
| 1 "Royal stomp" | One stomp on Roshan's last position (`royal_stomp`) | The playful **dust bunnies** | They roll together into a soft pink wall in front of the guests | Dust bunnies: "We play gently — and we help!" |
| 2 "Double demand" | Two stomps, each with its own full warning (`double_demand`) | The **Prince**, then **Baby Eagle** | Before the second stomp the Prince points to clear grass: "Over here!" (his help is real). After the counter, Baby Eagle carries the banner down as a canopy over the guests | Prince: "Over here!" Baby Eagle: "Chirp, chirp!" |
| 3 "Make way" | One stomp, then a clearly marked straight sweep of the cape (`make_way`) | The **rainbow friend** (Grand Puff) | He puffs his rainbow into a dome over everyone and the cake | Roshan: "Your rainbow keeps us safe!" |

- The King never changes a marked attack to chase her (existing rule).
- **Bump:** if Roshan is still in the warning when the foot lands, she bounces
  gently like a popped bubble, the King pauses ("Hmph!"), and the next warning
  is longer. Nothing is lost.
- **Missed opening:** the opening repeats and gets more forgiving (existing
  assist: up to +2 s warning, +5 s opening).
- Waiting, holding, or tapping off-target never completes a round (existing).
- Finished rounds save immediately and never reset (existing
  `chapter2_protection_rounds`).

**The payoff.** The King tries one last huff against the finished dome
("Mine!"); it holds with a soft boing. The guests wave their hats. The Prince,
behind his father, claps once before he can stop himself.

| Speaker | Line |
|---|---|
| Roshan | "You're safe!" |
| Prince, quietly | "She did it, Father." |

Save: existing beat 5 plus protection rounds 3.

### F6 — The King cheats (about 30 s)

This is a new choice by the King after he lost, not an attack she could have
dodged. The child only watches (touch to advance).

| # | Speaker | Line | Acting |
|---|---|---|---|
| 1 | King | "Enough games. I am taking the light." | Straightens up, smooths his cape, steps to the dome |
| 2 | — | — | He reaches up and over the rainbow dome with one long arm; a thin ember glow on his claws; he plucks **only the candle**, flame still lit |
| 3 | — | — | Hold one composition that shows all three together: the King holding the lit candle, the intact cake with its **empty candle place**, and Roshan |
| 4 | Prince | "You promised a fair challenge!" | Steps toward his father |
| 5 | King | "Come, son." | Turns away; does not look back |
| 6 | — | — | The Prince looks at his father, then at Roshan. He starts to speak and can't |
| 7 | Prince, to Roshan | "I'm sorry." | Hands open, eyes down |
| 8 | — | — | Both walk down the path together. Halfway, the Prince looks back once. The rainbow glow of the candle grows smaller and disappears |

- The candle keeps the same display size on the cake and in the King's hand
  (existing rule, 90 px frame).
- The Prince leaves with his father. He is not left behind as a guest, and
  nothing implies his warning made Roshan responsible.
- Save: existing beat 6 (theft) and the candle keys.

### F7 — What he couldn't take (about 60 s)

| # | Speaker | Line | Acting |
|---|---|---|---|
| 1 | — | — | Quiet. The music has stopped. The warm candle tint drains from the scene. The rainbow dome pops softly into sparkles; the bunny wall unrolls; Baby Eagle lays the banner back in the tree |
| 2 | Roshan | "He took our light." | Looks at the empty candle holder; her tail droops; the approved self-hug gesture |
| 3 | — | — | **Lamma**, the shyest friend, bounces out from under the stuffie blanket with Roshan's party hat, which rolled there in F4, and holds it up |
| 4 | Lamma | (a soft bleat: a new lamb sound effect; she has no words) | |
| 5 | — | — | Roshan puts the hat back on. The friends close in around her. Daddy hugs her (a callback to the Day One epilogue hug) |
| 6 | Daddy | "I'm proud of you." | |
| 7 | — | — | Roshan looks around: the tree, the cake, the banner, the stuffie team, Rumi, the friends, each still beside the thing made for them; each bobs as she sees it |
| 8 | Roshan | "But you're all still here." | Stands tall |
| 9 | Daddy | "And you can still make a wish." | |
| 10 | Roshan, whispering | "We'll find our light together." | Eyes closed, hands together (the approved clasped-hands gesture); sparkles gather in her hands while the child holds; the birthday song returns softly from Rumi's stage; everyone sways |
| 11 | — | — | She opens her hands; the sparkles float up into the evening sky, over the castle |

- **Child:** two acts, neither of which can fail. A glowing hand on Lamma
  holding the hat: touching her puts the hat back on Roshan, the child's own
  act of accepting comfort. Then a hold on Roshan: her wish.
- **Save:** existing beat 8 and `chapter2_story_complete`, plus
  `chapter2_wish_made` (new, additive). The reassurance checkpoint stays
  separate from the theft, so restarting after the theft can never skip the
  kind ending (existing rule).
- **Why a wish:** everything the jobs made for someone is still here. Only the
  candle, the light to wish on, is gone, and the wish shows the child it was
  never the candle's ([plotline: what no job makes](00_DAY_TWO_PLOTLINE.md#what-each-job-gives-the-party)).

### F8 — The door wakes (about 30 s)

The sun sets over the cloud sea. Everyone walks back to the castle together,
the stuffie team riding on the cake's cart, Baby Eagle overhead, Grand Puff
hopping ahead, the dust bunnies rolling behind.

In the Main Hall, the moonflower relief on the wall is glowing: it woke when
the rainbow candle was lit (F3), just as Roshan wished.

| Speaker | Line |
|---|---|
| Roshan | "The castle found a secret sky door!" (existing voiced line) |
| Daddy, yawning | "An adventure for tomorrow, birthday girl." |
| Roshan | "Tomorrow!" |

- One large moving pointer on the pearl; a touch opens it and saves (the
  existing Fairy Conservatory reveal). Today it only runs on entering the
  castle from outside, so it must also run here, at the end of the lawn.
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
- **Speaks:** short declarations: "Make way!", "Mine!", "Come, son." Loud,
  theatrical, sometimes funny ("Hmph!").
- **Moves:** slow, heavy and square. Chest leads. Stomps have a big
  anticipation (foot up), a pause, and a heavy landing.
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
- **Moves:** narrow, diagonal, quick and soft ("Cinderstep"); his gaze returns
  to Roshan while his body follows the King.
- **Arc in this chapter:** notices → invites himself a little ("You made
  that?") → objects ("It's her birthday") → helps for real ("Over here!") →
  admires ("She did it") → objects to the cheat → apologises → leaves ashamed,
  looking back once.
- **Never in Chapter 2:** named romance, hearts, a kiss, or being rewarded for
  helping. Later affection must come from his own repeated choices.
- **Look (locked, recovered identity):** slender red/coral turtle-dragon,
  cream muzzle, amber eyes, asymmetrical black fringe, short obsidian horns,
  sleeveless charcoal jacket with an ember-heart clasp, long split coat tails,
  a compact shell with exposed red skin around it and no centre-back coat
  panel. Always exactly 80% of the King's height (230 px).
- **Name:** the Prince has no name in canon. Giving him one is an owner
  decision.

## Voice and caption plan

Today every lawn line plays in the synthetic Roshan voice, including the
King's and Prince's, and the captions read like a script ("King: … Prince: …").
A four-year-old cannot tell who is talking.

- Give the King and the Prince their own voices. The recommended alpha is two
  new synthetic voices in the existing pipeline (a low, theatrical King; a
  young, soft Prince), pending owner listening. No family voice is cloned.
- Every line is voiced by its speaker, and the speaker visibly acts while it
  plays (mouth or body movement, never a still card).
- Captions: one short line for the adult, no speaker labels, never over a
  face, hidden during the rounds except the one-word cue.
- Full line list for recording: see the [voice lines](03_LEVEL_DESIGN.md#voice-lines).

## Animation needs

| Character | Needed | Exists today |
|---|---|---|
| Ember King | Walk in; point; stomp (foot up, land); wobble off-balance; dizzy spin; reach over the dome; hold candle; turn and walk away | One static V4 cutout (`assets/chapter2/ember_alpha/king_v4_cutout.png`); no motion. The owner reference sheet's side, back and expression views can be isolated first ([GFX-CHAR-KING-01](06_GRAPHICS_AUDIT.md#gfx-char-king-01)) |
| Prince | Walk (sleek), idle glance, point "over here", clap once, apologise, look back while walking away | One idle frame at runtime. The V2 motion package (`idle_glance`, a 16-frame `sleek_walk`, `cinderstep`; motion in REVIEW) is recorded but its atlas is not in the current tree and must be recovered from history; the identity sheet's side, back and sad-face views can be isolated ([GFX-CHAR-PRINCE-01](06_GRAPHICS_AUDIT.md#gfx-char-prince-01)) |
| Roshan | Swim, reach/press, protect pose, dodge swim, brush-sparkle counter, sad droop, hat on, stand tall | Swim and reach atlases (used for ignition), and the approved 16-pose gesture sheet (`roshan_gestures.png`), unused on the lawn today: surprise, clasped hands, pointing, self-hug, hope, cheers, holding. A sad droop is an art gap |
| Friends | Hat wobble, flinch, wave hats, lean in | Protected static portraits: motion only as whole-card squash, bob or tilt; never repaint them |
| Dust bunnies | Bounce, roll into a wall | Day One dust bunny art and animations |
| Baby Eagle | Chirp on branch, carry banner down | Book Baby Eagle art; carrying pose needed |
| Rainbow friend | Puff rainbow dome | Static rainbow friend card; puff motion needed |
| Lamma | Hop out, hold up hat | Seek atlas (hide, peek, reveal, celebrate), which is off-model (see [GFX-LAMMA-01](06_GRAPHICS_AUDIT.md#gfx-lamma-01)); hat-offer pose needed in the canonical egg-carrying design |
| Imp scout | Peek from the hedge, gasp, run, ride on the King's shoulder | An existing Opera rival imp cutout; whole-card motion |
| Rumi | Idle sway, wave | Existing eight-pose atlas only. She is on IP hold: no new frames, no regeneration, no voice |

## Cinematics

The earlier plan has nine Grok shot cards (C2-01 to C2-09) with
`GENERATION_READY: false`, blocked on clean approved first frames. This draft
changes several beats (payoff tour, friend shelter layers, Lamma's comfort,
evening door), so the cards must be revised before any generation. Until
full-frame cinematic delivery is accepted under `AGENTS.md`, every beat above
plays as gameplay staging.

## What changes from the implemented alpha

| Area | Implemented alpha (2026-09-06) | This draft |
|---|---|---|
| Party payoff | Static collage; one line | Touch-to-thank tour of every piece (F2), each with the friend it was made for |
| Guests | Eight portraits in a generic arc | The party map: each guest beside the piece made for them, invited by Daddy at dawn |
| Party tree | None | Healed Arborist tree frames the scene |
| Banner | Tiny 90×145 px card, top-left | Full banner strung in the tree |
| Hats | Procedural triangles | Painted hat cutouts per guest |
| Headline | "Happy Birthday, Roshan!" text on screen throughout, even during the theft | Removed |
| Song | None on the lawn | Rumi's song starts at ignition, is cut off by the stomps, and returns softly at the end |
| Voices | All lines in synthetic Roshan's voice | Each speaker voiced; King and Prince get their own voices |
| Warnings | Flat orange ellipse and thin white ring | Painted ember cracks and a sparkling safe spot |
| Shelter | Thin pastel arcs | Three friend layers: dust bunny wall, banner canopy, rainbow dome |
| Counter | Tap the King | Tap the gold star on the crown crest; brush sparkles in her chosen colour, as in Day One |
| King motion | None | Stomp, wobble, dizzy, reach, walk away |
| Comfort | Roshan's line only | Lamma brings the hat; Daddy's hug; the song returns |
| Foreshadowing | None | An imp apprentice at every Opera practice, and the imp scout who runs to fetch the King |
| The King's motive | Said once, in text | Spoken: "MY birthday party!", as the production spine's canon has it |
| The wish | None | Daddy: "You can still make a wish"; the child holds; the door answers |
| After the party | Back to the Main Hall; an unrelated Family Evening | The door wakes; then supper with the cake, the movie of the day and the sleepover |
| Ending | Returns to Main Hall with a stale "north-star clue" objective | Evening walk home; the sky door opens in the Main Hall |
| Stale lines | "A little ember silhouette is watching the party!" and "His little son's silhouette points to the bright north-star clue!" still fire from `scripts/main.gd` | Removed |

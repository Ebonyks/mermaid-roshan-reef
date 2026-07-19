# Pearl Opera House — asset & mechanics request lists (per act)

Owner request 2026-07-19: each act is a 1–2 minute Showtime-style performance
(backstage gremlin brawl → curtain → puzzle beat → bow). Everything below is
currently a rough primitive demo; each item names the placeholder node it
replaces so art drops in one-for-one without touching game logic. World art
follows the house rules: CC0 sources or original, restyled through the
_toonify pastel pipeline, ≤1024px / POT textures, one ASSET_LICENSES.md line
per asset. Book art, family voices and friend cutouts are never modified.

## Shared theatre (used by all acts)
Assets
- Proscenium arch + stage deck kit (replaces `_build_theatre` boxes)
- Curtain set: back drape, side gathers, and the sliding gate curtain
  (`gate_curtain`) with an authored open animation
- Backstage corridor kit: wooden boards, prop crates, rope pulleys, string
  lights (replaces `_build_backstage` primitives)
- STAGE GREMLIN character (replaces the recast dungeon `mischief_imp` GLB):
  a giggly theatre gremlin — plus a "pop into confetti" burst sprite
- Audience seat bench + a curtain-call confetti burst
- SFX: curtain whoosh, gremlin giggle/pop, applause loop, ta-daa sting
- Voice lines (family recordings): backstage intro, curtain-open, act win
  lines per act (scripts already pass distinct `voice`/`win_line` strings)

Mechanics wishlist
- Gremlins occasionally juggle a stolen act prop (pure flavor)
- Curtain-call bow pose for Roshan's cutout (verb clip)

## Act 1 — Pastry Chef, "The Great Cake Show" (order + stir finale)
Assets: cake layer models ×3 (`PadProp` on `OperaPad0..2`), mixing bowl with
swirl lid (`OperaGoal`), recipe board art, chef-hat costume prop, oven glow
backdrop. SFX: plop, whisk-whoosh ×3 rising, cake fanfare.
Mechanics wishlist: frosting squiggle free-draw during the bow (touch-drag).

## Act 2 — Detective, "The Missing Tiara" (hidden-clue search)
Assets: pawprint / feather / ribbon clue props (`PadProp`), treasure chest
with tiara reveal (`OperaGoal`), magnifier costume prop, dim "searchlight"
stage dressing. SFX: pop-out "boing", chest creak, twinkle.
Mechanics wishlist: clues squeak & wiggle when the magnifier passes near.

## Act 3 — Ballerina, "The Dance Recital" (echo tiles)
Assets: glowing dance tile set ×4 (`OperaPad*`), tutu costume, mirror-ball.
SFX: four-note tile scale (authored, replacing pitched chime).
Mechanics wishlist: Roshan twirl verb on every correct step.

## Act 4 — Candy Maker, "The Candy Parade" (press timing, 4 candies)
Assets: candy press machine (`CandyPress`), gauge track + star slider art,
candy bodies with 4 authored face decals (dot / starry / hearts / sleepy),
shelf. SFX: press *thunk*, squish-giggle, parade kazoo.
Mechanics wishlist: a wrapped-candy toss to the audience at the bow.

## Act 5 — Doctor, "The Plushy Checkup" (5 one-touch steps)
Assets: plush starfish patient (`PlushPatient`) with sad→happy faces,
stethoscope (`Stethoscope`), thermometer, bandage roll, band wrap, heart
puffs. SFX: thump-thump heartbeat, pop-kiss, better-now chirp.
Mechanics wishlist: patient blinks and giggles when tickled between steps.

## Act 6 — Farmer, "The Piggy Picnic" (2D side-scroller, 7 piggies)
Assets (2D): meadow parallax layers, PIGGY sprite with trot/hop/munch frames
(replaces the circle-panel piggies), snack icons (carrot/apple/corn/berry/
pumpkin), veggie toss arc sprite, barn backdrop for the finale.
SFX: oink ×7 pitched, munch, toss-whoosh.
Mechanics wishlist: a mud puddle piggies hop over (pure animation beat).

## Act 7 boss — "The Curtain Dragon" (roaming peek boss, 4 stars)
Assets: dragon puppet on a stick (head + curtain slot ×3 spots), sparkle
star projectile, bubble-puff. SFX: grumble, puff, tamed-purr.
Mechanics wishlist: dragon sneezes confetti when popped the final time.

## Act 8 — Opera Star, "The Moonlight Aria" (echo bells)
Assets: golden bell trio (`OperaPad*` bells), conductor seahorse cutout on a
podium, moon backdrop. SFX: authored three-bell chord scale, crowd "la-la"
echo after each round.
Mechanics wishlist: audience sways in rhythm during the demo.

## Act 9 — Magician, "The Magic Hat Trick" (shuffle, 3 rounds)
Assets: magic hats ×3 (`OperaHat*`), BUNNY-FISH character (`BunnyFish`),
wand costume prop, star-swirl swap trail. SFX: whoosh-swap, ta-da, giggle.
Mechanics wishlist: round 3 hats do one fake-out feint mid-swap.

## Act 10 — Painter, "Paint the Sunrise" (dip & swipe)
Assets: paint pots ×3, brush (replaces `PaintBrush`), canvas easel with 3
authored stripe reveals (`stripes`), beret costume. SFX: dip-sploosh,
swipe-shhh, masterpiece sting.
Mechanics wishlist: free-paint splatter taps on the finished canvas.

## Act 11 — Astronaut Engineer, "The Bubble Rocket" (pipe fix)
Assets: bubble tank (`BubbleTank`), star rocket with window glow
(`StarRocket`), pipe pieces — straight/elbow/ring (`PipePiece*`), ghost-slot
frames, valve wheel (`BubbleValve`), bubble stream. SFX: clank-fit ×3,
valve squeak, bubbling launch.
Mechanics wishlist: rocket does a tiny hop-launch behind the bow.

## Act 12 — Racecar Driver, "The Opera Grand Prix" (KartGame)
Assets: opera-liveried kart skin, checkered stage flag (`RaceFlag`),
grandstand banner. (Kart engine content otherwise complete.)
Mechanics wishlist: none — engine already at 5/5.

## Act 13 — Pop Star, "The Starlight Concert" (DanceEngine)
Assets: sparkling microphone (`StarMicrophone`), stage-light frame for the
dance overlay, star glasses costume. (Dance engine content complete.)
Mechanics wishlist: an encore verse if the first round is all-perfect.

## Act 14 boss — "The Shadow Phantom" (lantern dual boss)
Assets: shy phantom puppet, stage lanterns ×3 (`OperaLantern*`), spotlight
beam cone, friendship-bow finale pose. SFX: shy "oooo", lantern fwoom,
happy squeak.
Mechanics wishlist: phantom peeks from behind the lantern glass itself.

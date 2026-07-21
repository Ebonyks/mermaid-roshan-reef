# Codex custom-asset request — Pearl Opera House visual overhaul

Owner 2026-07-21: gameplay engines are locked and unique per act; this list is
the full custom-asset order for Codex to replace every primitive with
high-quality authored art and texturing. House rules apply to every item:
cel-shaded pastel toy-playset look (Wind Waker as rendering reference only),
navy/purple ink outlines, aqua/lavender shadows, Mobile-renderer safe,
textures ≤1024px or power-of-two (VRAM compress only if POT), OGG audio,
one ASSET_LICENSES.md line per asset. Book art, family voices and friend
cutouts are never modified. Every placeholder below names the node it
replaces so art drops in one-for-one without touching game logic.

## 1. Shared material & texture kit (used everywhere)
- Toon material set: theatre-red velvet (curtains, benches), gilded gold
  (frames, trim, ropes), lacquered plum wood (floors, panels), backstage
  pine boards, stage-canvas cream. Each as tileable POT albedo + flat
  cel ramp; no PBR noise — big readable value shapes
- Sparkle/confetti particle sprite sheet (star, dot, streamer) — replaces
  every `_sparkle_burst` default
- Golden usher-sparkle pointer model (replaces pointer sphere + ★ label)
- Roshan verb clips for the cutout: twirl (win), bow (curtain call),
  punch jab (boxer), peek lean (sleuth)

## 2. The Lobby (three floors)
- Grand carpet runner texture with gold fringe (`_build_lobby` carpet boxes)
- Wainscot + wall panel set with poster frames; three authored SHOW POSTERS
  per floor (12 total, one per career door — doubles as door signage)
- Chandelier model ×2 (crystal drops, glow bulb) at y36
- Audience bench model (tufted velvet) ×4
- Mezzanine railing kit: turned gold balusters, deck fascia, corner caps
- Bubble lift: glass column with rising bubble particles, brass base +
  landing pad ring, lift chime SFX
- Centre-stage medallion ×3: dark inlaid marquetry disc → ignited gold
  state with boss crest reveal + light pillar (replaces disc/halo/crest)
- Career door kit: gold frame, recessed curtain (per-act tint mask),
  glowing walk-in veil plane, crest plate (the 12 career crest logos from
  the approved sheet), gold completion star
- Theatre crest: 🎭 masks + star sculpture over the top gallery
- Lobby ambience: murmur loop, door twinkle, transformation chime,
  star-stamp ta-daa, all-stars fanfare

## 3. Backstage brawl shell (Chef, Detective, Doctor, Magician, Painter, Astronaut)
- Backstage corridor kit: plank walls, prop crates, rope pulleys, string
  lights, sandbag counterweights (replaces `_build_backstage` boxes)
- Sliding gate curtain with authored open animation (`gate_curtain`)
- Mischief imp reuse (`mischief_imp.glb`) + CAPTAIN accessory pass:
  1.45× scale variant with gold bow + tiny champion belt; giggle-dash
  dust-puff sprite; pop-into-confetti burst
- SFX: imp giggle, pop, captain "nuh-uh!" raspberry, curtain whoosh

## 4. Per-act unique packs (one distinct engine each — assets must not repeat)
1. **Pastry Chef — order/stir/toppings**: cake layer models ×3 (`PadProp`),
   mixing bowl with swirl lid (`OperaGoal`), recipe board, topping pedestals
   ×3 + cherry/berry/star toppings, oven-glow backdrop. SFX plop, whisk ×3
   rising, cherry squish, fanfare.
2. **Detective — sleuth peek-in-props**: search crate/vase/hatbox set ×6
   with pop-open lids (`SearchProp*`), clue props (pawprint, feather,
   ribbon), SILLY FISH jack-in-the-box character, tiara treasure chest with
   burst-open reveal (`TiaraChest`), dim searchlight dressing. SFX lid
   creak, fish boing-giggle, clue twinkle, chest fanfare.
3. **Ballerina — echo tiles**: glowing dance tile set ×4 (`OperaPad*`),
   mirror-ball, tutu prop. Authored four-note tile scale.
4. **Candy Maker — press timing**: candy press machine (`CandyPress`),
   gauge track + star slider, candy bodies + 4 face decals, parade shelf.
   SFX press thunk, squish-giggle, kazoo.
5. **Doctor — one-touch checkup**: plush starfish with sad→happy faces
   (`PlushPatient`), stethoscope, thermometer, bandage roll + wrap, heart
   puffs. SFX heartbeat, pop-kiss, better-chirp.
6. **Farmer — 2D scroller**: meadow parallax layers, piggy sprite with
   trot/hop/munch frames, snack icons ×5, toss arc sprite, barn finale
   backdrop. SFX oink ×9 pitched, munch, toss-whoosh.
7. **Boxer — ring combat (NEW)**: toy boxing ring kit — canvas deck with
   printed star logo, corner posts, gold ropes (`_build_box` boxes), round
   bell on post, boxing glove costume pair + championship belt prop,
   round card "1/2/3" placards (picture, not text-dependent), corner stool.
   SFX bell ding-ding, bop, crowd "oooh", belt fanfare.
8. **Magician — hat shuffle**: magic hats ×3 (`OperaHat*`), BUNNY-FISH
   character, wand, star-swirl swap trail. SFX whoosh, ta-da, giggle.
9. **Painter — dip/swipe/splat**: paint pots ×3, brush (`PaintBrush`),
   canvas easel with 4 stripe reveals (`stripes`) + splat decal set ×3
   (replaces the flattened spheres), beret. SFX dip-sploosh, swipe-shhh,
   SPLAT, masterpiece sting.
10. **Astronaut — pipe fix**: bubble tank (`BubbleTank`), star rocket with
    window glow (`StarRocket`), pipe pieces straight/elbow/ring
    (`PipePiece*`), ghost slots, valve wheel (`BubbleValve`), bubble
    stream. SFX clank ×3, valve squeak, bubbling launch.
11. **Racecar — kart**: opera-liveried kart skin, checkered stage flag
    (`RaceFlag`), grandstand banner.
12. **Pop Star — dance**: sparkling microphone (`StarMicrophone`),
    stage-light frame for the overlay, star glasses.

## 5. Boss packs (medallion showdowns)
- **Curtain Dragon**: dragon puppet-on-stick with 5 curtain slots (outer
  two for bold phase), sparkle star projectile, bubble puff, confetti
  sneeze for the final pop. SFX grumble, puff, tamed purr.
- **Shadow Phantom**: shy phantom puppet, stage lanterns ×3
  (`OperaLantern*`) with lit/flicker glass states, spotlight cone,
  friendship-bow pose. SFX shy oooo, lantern fwoom, happy squeak.
- **Midnight Maestro (grand finale)**: conductor silhouette with gold
  baton (replaces primitive gown/baton), music-stand podium, swirling
  sheet-music particles, grand confetti curtain, curtain-call cameo
  sprites of all 12 careers. SFX dramatic hum, baton swish, full-company
  fanfare.

## 6. UI & wardrobe
- 12 career crest icons (from the approved crest sheet) as POT textures:
  door plates, wardrobe entries, sticker-book stamps
- Gold star stamp (door/medallion completion) + ★ n/15 HUD chip art
- Objective banner frame + per-act trim tint mask
- Boxer costume entry for the wardrobe (gloves + belt)

## 7. Voice lines (family recordings — never synthesized)
- Lobby welcome, medallion light-up, star praise, all-stars celebration
- Per-act: intro line, win line (scripts already pass distinct strings)
- New: boxer round calls ("Round one!", "Ding ding!"), sleuth clue/fish
  reactions, splatter cheer, captain chase line

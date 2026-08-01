# Mermaid Roshan Pearl Opera career audit and runtime system

Date: 2026-07-29

Scope: all twelve Mermaid Roshan career jobs, their artwork packages,
competition rules, nested minigames, and the three major Opera boss games.

## Executive finding and correction

The accepted job art described twelve 2D/2.5D worlds, but career play still
entered a generic 3D theatre and treated much of that art as reference. That
was an engine-integration error, not a missing-polish issue.

The shipping path is now corrected:

1. Opera entry opens a native 1280x720 `OperaLobby2D` Canvas menu; no 3D
   lobby, avatar, camera, doors, lifts, lighting, or spatial navigation are
   created in normal desktop or Android play.
2. Three large direct floor tabs expose four picture-first Mermaid Roshan job
   cards per floor. The picker never presents imps as floor cards.
3. Selecting a job instantiates `OperaCareerWorld2D`, backed by a scalable
   code-native 2D set for that profession rather than a stretched concept key.
4. The early phases are Roshan's own short job minigames. Rival movement,
   timer, score bars, and the dressed imp remain hidden and paused.
5. Each job's configured final level then introduces its dressed imp and turns
   the relevant last phase(s) into a competition in front of the family crowd.
6. Detective includes magnifier practice before its 40-second shared-mystery
   finale and guided reveal/rematch; boxing introduces the boxer at round one.
7. Completing the final performance produces Warm Cheers, Big Cheers, or a
   Standing Ovation according to pace, accuracy, and guided retries.

No 3D lobby or career stage, job camera, avatar rig, physics body, or decorative
job set is built during normal Android/windowed play. The three separate floor
bosses still use the 3D proscenium; the detailed legacy 3D lobby/job path is
headless-only while its historical mechanical regression probes are retained.

## Reusable system

The system is deliberately data-driven so it can be reused elsewhere.

| Component | Responsibility |
| --- | --- |
| `scripts/opera_lobby_2d.gd` | 2D floor tabs, Roshan-only job cards, finale locks, star progress, spoken hints |
| `scripts/opera_world_backdrop_2d.gd` | Twelve scalable code-native job sets and lightweight living motion |
| `scripts/opera_career_world_2d.gd` | 2D actors, early minigames, final-level reveal, audience, score display, curtain call |
| `scripts/opera_gesture_surface.gd` | One-finger tap, hold, swipe, circle, highlighted choice, and broad timing-window input |
| `scripts/opera_competition.gd` | Rival pace, player/rival scores, audience energy, cheer tier, Detective retry policy |
| `scripts/opera_act.gd` | Picker-to-world lifecycle, save-safe completion, boss/legacy routing, touch-layer handoff |
| `tools/prepare_opera_2d_worlds.py` | Deterministic non-destructive preparation of Roshan/finale-imp actor sprites |

Each career supplies a Roshan actor, finale-rival actor, code-native palette, accent,
competition pace, and a list of phase dictionaries. A phase contains a
pictogram, gesture mode, progress goal, and spoken prompt. The same framework
therefore supports a short tactile job sequence without reading, precision
failure, or lost progress.

Incorrect choices and off-beat taps lower performance quality but still move
the phase slightly. This keeps the competition legible without trapping a
four-year-old. Every completed career still earns its star.

## Artwork packages actually used

### A. Runtime 2D career-world package

`scripts/opera_world_backdrop_2d.gd` draws twelve distinct scalable sets: a
pastry kitchen, clue archive, recital stage, candy workshop, plushy clinic,
meadow/barn, boxing ring, illusion portal stage, sunrise gallery, bubble-rocket
bay, grand-prix circuit, and pop concert. These are Godot-native vector worlds,
not raster placeholders, so they remain crisp without violating the required
2048px native raster coverage per playable screen.

`assets/opera/worlds/actors/roshan_<career>.png` contains twelve 512x512
transparent actor sprites derived from the accepted outfit hero cards. Only
the edge-connected navy presentation field and card border are removed.

`assets/opera/worlds/actors/rival_<career>.png` contains twelve final-level
competition actors. Eleven are deterministic 512x512 slices of one consolidated
identity-locked costume sheet. Boxer uses the dedicated 1024x1024 two-glove
match sprite. These actors are hidden during the earlier minigames and enter
only for the configured finale segment.

### B. Accepted flat job package

`assets_src/concepts/opera_jobs_flat_2026-07-21/` contains:

- 36 accepted 1024×1024 sheets: outfit, gameplay, and stage/guidance art for
  each career; and
- 576 deterministic sliced cards.

The outfit hero cards are runtime actor sources. The remaining gameplay and
stage cards remain the detailed palette, prop-state, pictogram, and
interaction reference package.

### C. Accepted 2.5D environment package

`assets_src/concepts/opera_jobs_2p5d_2026-07-24/` contains:

- twelve 1024x576 composition keys, retained as source references only; and
- twelve environment/module texture kits, retained as source masters and
  expansion references.

The scene keys are 1024x576. Although they meet the single-texture size limit,
they do not meet the 2048px-per-playable-screen background rule and are not
loaded or stretched at runtime.

### D. Rival source and provenance package

`assets_src/concepts/opera_rivals_2026-07-29/` contains:

- the untouched owner-supplied imp identity reference;
- the accepted match-ready boxer master;
- the accepted eleven-costume sheet;
- rejected identity/shell-motif iterations; and
- a prompt/derivation ledger.

The rival identity is the purple humanoid imp with curled striped horns,
amber eyes, pointed ears, friendly fangs, small hair tuft, and curled tail.
Profession is communicated by clothing and tools. No imp uses a shell, pearl,
scallop, marine badge, ocean emblem, target, medallion, crest, logo, or
jewelry motif.

### E. Family audience package

Six existing family/friend cutouts from `assets/characters/friends/` are
loaded unchanged along the front of every career world. They bob during play
and hop more strongly for higher cheer tiers. Protected originals were not
edited, relit, regenerated, or recompressed.

### F. Opera lobby and boss package

`scripts/opera_lobby_2d.gd` is the shipping hub package. It uses opaque native
Controls, three 150x112 floor tabs, four large Roshan-only job cards, one gated
floor-finale card, star persistence, and spoken lock/selection hints. No lobby
raster background is required.

`assets/art35/opera/*.glb` is retained for the three 3D floor-boss
prosceniums and the headless legacy navigation regression only. Normal lobby
entry never builds its doors, medallions, lifts, railings, chandeliers, camera,
lights, or swimming avatar.

### G. Legacy job GLB package

`assets/opera/jobs/` contains 53 project-authored GLBs for outfits and props.
They remain licensed, preserved source/runtime fallback material and support
the legacy mechanical regression probes, but normal career-job play no
longer constructs those 3D sets. They are not evidence that a career is a 3D
game.

### H. Hybrid finale package

`assets_src/concepts/opera_jobs_hybrid_finales_2026-07-24/` contains twelve
1024×576 composition keys. They remain art-direction references for spectacle,
boss-family continuity, and possible future finale extensions; they are not
silently presented as implemented gameplay screens.

## Career-by-career game and artwork audit

### Floor 1: Lagoon Lights

#### 1. Pastry Chef — The Reef Bake-Off

- World art: code-native pastry kitchen set with giant ovens, bowls,
  counters, frosting color, and celebratory architecture.
- Roshan art: chef toque, coral apron, whisk, rainbow tail.
- Rival art: the same authoritative imp in a cream toque and coral apron with
  a whisk; no marine insignia.
- Nested minigames: scrub/swipe the sieve; hold to pour; circle to stir;
  broad-window oven timing; swipe the frosting pipe; tap five toppings.
- Final competition level: the imp enters for piping and topping; the two
  finished cakes are scored before the crowd.

#### 2. Detective — The Two-Detective Mystery

- World art: moonlit archive/detective district with clue shelves, paths,
  pedestals, and a shared-case atmosphere.
- Roshan art: detective cap, coat, magnifying glass.
- Rival art: matching purple imp identity in navy deerstalker and coat with
  magnifier.
- Nested minigames: identify five highlighted clues; trace the footprint
  trail; make four board matches; select the final highlighted answer.
- Competition: both detectives solve the same case. The rival clock is 40
  seconds. If the imp finishes first, play pauses for a 3.6-second answer
  demonstration; the same mystery restarts with sparkle memory and a
  12-second-slower rival. It is a guided recognition rematch, not lost
  progress or a blind reset.

#### 3. Ballerina — The Twin-Ribbon Recital

- World art: code-native recital garden/stage with arches, ribbon pathways, and
  soft performance lighting.
- Roshan art: lavender recital outfit and ribbon styling.
- Rival art: same imp face and horns in lavender tutu with coral ribbon wand.
- Nested minigames: hold/watch the opening phrase; repeat six highlighted
  steps; swipe-trace the ribbon; draw circles for the final twirl.
- Final competition level: after the watch/practice opening, the ribbon imp
  enters for recital steps, ribbon tracing, and the final twirl.

#### 4. Candy Maker — The Candy Workshop Cup

- World art: bright candy workshop/district with oversized confection
  machinery, parade lanes, jars, and wrapper color.
- Roshan art: candy-maker cap, apron, sweets/tool styling.
- Rival art: same imp in striped cap and coral apron holding one wrapped
  candy.
- Nested minigames: hold syrup; sort seven highlighted candies; twist wrappers
  with circles; time five parade-cart loads.
- Final competition level: the candy imp enters for the parade load and
  shared reveal.

### Floor 2: Starlight Balcony

#### 5. Doctor — The Plushy Care Relay

- World art: friendly plushy clinic with large care stations, X-ray language,
  basins, bandage shapes, and calm teal lighting.
- Roshan art: doctor coat and child-readable medical tools.
- Rival art: same imp in teal coat with head mirror, stethoscope, and bandage
  roll; the mirror is functional equipment, not a marine badge.
- Nested minigames: hold to wash; find three highlighted patients; choose
  three X-ray cracks; circle-wrap the cast; swipe the outer bandage.
- Final competition level: the doctor imp enters for casts and bandages.
  Mistakes affect applause only; no plushy or career progress can be lost.

#### 6. Farmer — The Piggy Picnic Challenge

- World art: meadow/farm district with planting beds, picnic props, mud route,
  and barn destination.
- Roshan art: straw hat, overalls, crop and piggy-care cues.
- Rival art: same imp in straw hat and teal overalls holding a carrot.
- Nested minigames: swipe seeds into furrows; time five piggy feeds; swipe up
  through mud hops; sweep back and forth to guide the herd home.
- Final competition level: the farmer imp enters for the mud-hop and
  barn-herding finish.

#### 7. Boxer — The Friendly Championship

- World art: the accepted underwater boxing/training district is now the
  actual ring world, including padded platforms, hanging bags, bell tower,
  ropes, banners, and crowd space.
- Roshan art: two coral gloves, teal headband, padded vest, rainbow tail.
- Rival art: the corrected owner-supplied imp identity with the exact face,
  curled horns, ears, fangs, body, tail, and boots; exactly two coral boxing
  gloves; plain quilted vest and teal waistband; no focus mitt, target, pearl
  belt, shell, badge, crest, or ocean emblem.
- Nested minigames: five-tap warm-up; four timed punches in round one; swipe
  down to duck; five timed punches in round two; second duck; six timed
  punches in round three; tap the championship belt.
- Final competition level: after Roshan's bag warm-up, this becomes a direct,
  friendly boxing match against one padded imp
  in front of the crowd. The imp advances, guards, counters, and bows at the
  result; it is not a punching-gallery prop.

#### 8. Magician — The Grand Illusion Duel

- World art: code-native illusion district with stage-scale architecture, hat
  stations, lights, and portal-ready central space.
- Roshan art: magician coat/cape, hat, wand, rainbow-tail silhouette.
- Rival art: same imp in navy top hat and short cape with a star wand.
- Nested minigames: hold to vanish the bunny-fish; follow six highlighted hat
  moves; swipe the magic rope; hit four cabinet timing flashes; hold to charge
  the giant star portal.
- Final competition level: the magician imp enters for cabinet timing and
  the star-portal spectacle, after Roshan practices vanish, tracking, and rope.

### Floor 3: Grand Gallery

#### 9. Painter — The Sunrise Paint-Off

- World art: code-native sunrise painting district with giant paint pots,
  elevated walkways, easel space, and gallery architecture.
- Roshan art: beret, brush, palette, apron, rainbow tail.
- Rival art: same imp in purple beret and paint-marked teal apron with brush
  and palette.
- Nested minigames: swipe the sketch; hold to fill the highlighted form;
  broad paint strokes; five splatter taps; gallery-hang tap.
- Final competition level: the painter imp enters when the two sunrise
  canvases are painted, splattered, and revealed to the gallery crowd.

#### 10. Astronaut Engineer — The Rocket Repair Race

- World art: rocket/engineering district with bubble conduits, launch
  platforms, repair stations, and child-readable machinery.
- Roshan art: open-faced space/engineering suit and tool cues.
- Rival art: same imp in an open cream-and-teal helmet and suit with wrench;
  face and horns remain readable.
- Nested minigames: six highlighted pipe choices; hold a leak patch; circle
  the valve; hold through countdown and launch.
- Final competition level: the astronaut imp enters for the valve-and-launch
  race after Roshan practices pipes and patching.
  Propulsion remains playful bubbles rather than realistic exhaust.

#### 11. Racecar Driver — The Opera Grand Prix

- World art: code-native underwater track-city with grandstands,
  elevated roadways, corner language, and finish architecture.
- Roshan art: driver suit, headgear, gloves, rainbow racing tail.
- Rival art: same imp in coral-and-teal racing suit, carrying the helmet so
  the face and horns remain visible.
- Nested minigames: swipe steering through the first lap; five broad turbo
  timing hits; faster second-lap steering; three finish timing hits.
- Final competition level: the driver imp enters for lap two and the finish
  sprint on the same 2D circuit.

#### 12. Pop Star — The Starlight Sound-Off

- World art: concert district with stage lighting, audience space, rhythm
  color, and a large finale platform.
- Roshan art: pop-star performance outfit, microphone, rainbow accents.
- Rival art: same imp in glittery purple jacket with handheld microphone.
- Nested minigames: hold for sound check; seven highlighted dance choices;
  six rhythm-window hits; circle for the encore spin.
- Final competition level: the pop-star imp enters for the rhythm phrase and
  encore; score bars appear only then.

## Major-game boss minigames

The three floor bosses remain friendly 3D Opera finales. They are separate from
the dressed-imp final levels nested inside each career job:

1. **Curtain Dragon:** readable hide/peek/roar cycles; tap SPARKLE during a
   peek. The dragon joins the show instead of being defeated.
2. **Shadow Phantom:** hold SHINE at the twinkling lantern, then use SPARKLE
   during the peek. The phantom becomes a curtain-call performer.
3. **Midnight Maestro:** finale remix of lantern charging and wider/faster
   curtain peeks. The Maestro ends by conducting the whole cast.

## Validation and safety

- Godot importer: completed under Godot 4.7.1, Forward Mobile.
- `probe_opera_2d.gd`: forces the shipping path under headless Godot; verifies
  the 2D lobby has zero 3D children, three floor tabs, four Roshan-only cards,
  no imp cards, finale locks, scalable code-native career worlds, hidden/paused
  rivals before the finale, final-level imp entry, all one-finger phase
  completions, Detective's guided clock reset, cheer tiers, and touch restore.
- Existing detailed Opera probe remains green for the preserved mechanical
  engines.
- Static GDScript parse and inference lint pass.
- No undersized raster is used as a playable background. Actor sprites are
  512x512 except the 1024x1024 boxer; all meet the mobile texture rule.
- Normal career play creates no physics bodies or lights.
- No save key was removed. Completion still routes through the existing
  Opera-star write path.
- Nothing in `assets/book/`, `assets/audio/voices/`, or
  `assets/characters/friends/` was modified.

## Honest remaining work

The system is now integrated and playable, not concept-only. Remaining work is
focused polish rather than an engine rewrite:

1. phone playtest gesture thresholds with the intended four-year-old;
2. record three distinct family crowd-cheer intensities if the family wants
   voiced applause;
3. add small frame animations only where playtest evidence justifies the art
   cost; and
4. profile the full-screen alpha actors on the Lenovo Tab M11 Speedy tier.

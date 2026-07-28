# Minigame graphical audit — 2D-sprite transition

Audit date: 2026-07-27
Audited revision: `origin/dev` at `aed444a6b8aabbf6dbe769d96a010cce976b382d`
Scope: every player-facing minigame family, its runtime background, focal
characters/props, and immediately adjacent selection or lobby surface.

Production amendment, owner direction 2026-07-27: use a
**regeneration-first** reconstruction. Do not search the repository for a
merely similar prop, background, or decorative family and promote it into a
different game. Questionable art is regenerated for the exact game and state.
Faron's three baby-doll sprites are the protected gameplay exception and remain
byte-for-byte unchanged.

## Reconstruction status

Status below records the implementation pass on this branch; the evidence and
original verdict later in this document intentionally describe the audited
`origin/dev` baseline.

| Family | Branch status | Verification |
|---|---|---|
| Dolls, Fetch, Seek, Treasure, Melody, Toy Castle, Shop | Reconstructed with separate tailored plates and 2D focal sprites | Full audit green; Treasure and passive probes green |
| Play-place, Penguin Slide, Rainbow Slide | Reconstructed as three distinct course families | Race-feel and passive probes green |
| Snowman, Garden, Trampoline, Christmas, Dance | Reconstructed with tailored 2D stage plates | Picture-game and dance probes green |
| Fairy Pond | Reconstructed overhead with regenerated bugs, hazards, flower growth and effects | Fairy passive gate green |
| Combat, Castle Dungeon, Ember Dungeon | Reconstructed with separate crystal/Ember room and actor families | Combat and all ten Dungeon rooms green |
| Stuffie Battle, picker, castle room, reef den | Reconstructed as one nursery/stuffed-toy family; direct Lamb GLB removed | Full Stuffie suite all-OK |
| Critter collection and book | Eighteen regenerated cutouts, 2D net/markers, illustrated silhouette cards | Passive collection gate green |
| Echo Bells | Reconstructed local music-room plate, seven colored 2D bars and song-star | Full audit music-room checks green |
| Kart | Reconstructed as separate Ocean and Butterfly World families with regenerated vehicles, hazards, pickups, finish gates and boost cues | Kart feel all-OK; 66 live sprites, zero renderable legacy mesh layers |
| Butterfly Galaxy | Reconstructed as a celestial butterfly nursery with a tailored plate and sixteen regenerated actors/landmarks | Galaxy state all-OK; 40 live sprites, zero renderable legacy mesh layers |
| Ember Fortress overworld | Reconstructed as an obsidian-coral kingdom with a tailored plate and sixteen regenerated route/landmark sprites | Ember suite all-OK; zero renderable legacy mesh layers |
| Opera lobby, twelve careers, three bosses | Reconstructed with Opera-local lobby, career and boss-stage plates; no Opera treatment exported to other games | All fifteen acts all-OK; legacy act meshes cannot render |
| Entry/selection surfaces | Reconstructed with theme-specific Ocean race, Rainbow race, Opera and crystal-dungeon gates plus 2D selection markers | Passive and full-audit entry checks green |

## Completion verification

- Runtime minigame art contains 144 PNGs and 61 project-original SVGs.
  Every PNG is either at most 1024 px on its longest side or uses a valid
  power-of-two 2048x1024 plate. The inventory contains no size-policy
  violations.
- The core minigame, collection, companion, combat, dungeon, and stuffie
  scripts contain no `.glb` references or `MeshInstance3D`,
  `MultiMeshInstance3D`, or primitive-mesh constructors.
- Galaxy, Kart, Ember, and Opera retain some historical non-rendering
  scene/state scaffolding so their large gameplay engines remain mechanically
  stable. Current probes assert that every legacy mesh layer in those
  reconstructed surfaces is zero while the tailored Sprite3D art is live.
- Faron's protected originals remain byte-for-byte unchanged:
  `baby_doll.png` SHA-256
  `00BF49B8E76CEC939B2C3908654B5BC25BEE02D1907CA034D347F3FFAA386472`;
  `baby_doll2.png`
  `10D8153696B2BCCC6B878E000862C42CFB4C5E23002B8975E2E83418878B4652`;
  `baby_doll3.png`
  `0617BF861B63EF92B396F979CB4894948AD9517157B5DD820001E0131FBE1A6A`.

## Executive verdict

The owner's concern is confirmed. No minigame family is fully at the new target
of custom 2D background art plus 2D sprite gameplay art.

- Most minigames still build their visible world from GLBs, `MeshInstance3D`
  primitives, or both. A static scan of the 21 runtime files in scope found
  **122 unique quoted `.glb` path literals** and **161 primitive-mesh
  constructor sites**. The GLB count includes fallback paths and format
  strings, so it is a dependency indicator rather than a live-node count.
  The separately inventoried Ember overworld adds 27 quoted GLB literals and
  four primitive-mesh constructor sites.
- Only the picture-game suite and dance engine are 2D-first. They still use
  generated gradients, panels, labels, and UI geometry in place of tailored
  stage art.
- Across the core arena games, only four authored raster files currently act as
  backgrounds: the protected `nursery_bg.jpg` and the three Fairy Pond plates.
  Every other space relies on a solid environment color, material texture, or
  3D geometry to fill the frame.
- The picture games literally stretch a **64×64 generated gradient** across the
  1280×720 stage. Their focal sprites are mixed in quality and resolution:
  `carrot.png` is 128×128, `wateringcan.png` is 272×286, and the snowman is
  291×520, while the newer generated tree, ornaments, butterfly, sun, and star
  reach 804–1024 px. The inconsistent source families are visible together.
- The Dolls nursery displays the protected 796×1100, 118.6 KB portrait book
  page as a large stage plate. It is not a defective source file; it is simply
  the wrong aspect, composition, and role for a wide interactive background.
  It must remain untouched in `assets/book/`.
- Fairy Pond is the closest background success: three purpose-made 1024×1024
  plates already exist. The plates can remain as visual references, but the
  game still places twelve named GLB families plus primitive bullets, gates,
  fireflies, and fallback creatures over them.
- A major identity-reference opportunity is being missed. The repository
  already
  contains **833 custom Opera 2D images** across the Opera house flat set,
  job-flat set, 2.5D scene keys/environment kits, and hybrid finale keys. The
  runtime does not reference any of those collections. It instead instantiates
  Opera GLBs and procedural colored set panels. These images can anchor
  Opera-specific identity, but the amendment above means they are not
  automatically promoted when a clean runtime layer or state is questionable.

This audit now recommends a regeneration-first 2D conversion. Preserve Faron's
babies exactly. An existing asset may survive only when it is exact to the
game/state, original and licensed, already technically compliant, and passes
current Mobile review. Otherwise regenerate it from a theme-local brief. Never
turn any source into a GLB.

## Rules used for this audit

The following are hard gates, not scoring preferences:

1. All visible game art is a 2D sprite or flat. No GLBs, authored meshes,
   procedural focal meshes, 3D character models, or Blender work.
2. Existing game logic may continue to use 3D coordinates and cameras.
   `Sprite3D` cards and CanvasItems are valid; models are not.
3. Protected originals in `assets/book/`, `assets/audio/voices/`, and
   `assets/characters/friends/` are never overwritten, resized, recompressed,
   or restyled. A new derivative or companion background lands elsewhere.
4. A background contains no words, letters, or digits. Gameplay is explained by
   a voice line, pictograms, animation, and the golden pointer.
5. The Mobile renderer and Lenovo Tab M11 are the review target. New textures
   follow the project's power-of-two and overdraw budgets.
6. A visual family cannot score 5/5 without current near, mid, and
   gameplay-distance Mobile captures plus explicit owner acceptance.
7. The 2D transition changes the **medium**, not every game's theme. Shared
   layer code, import settings, sprite anchors, and performance budgets are a
   technical grammar only. They are not permission to share Opera's shell-gold
   palette, proscenium, curtains, footlights, or theatrical dressing with other
   games.

The existing contact sheets under
`audit/runtime_shots_2026-07-16/pass_35/contact_sheets/` are useful historical
evidence of composition and inconsistency. They predate the 2026-07-27 2D-only
decision and are not current acceptance captures.

## Runtime-wide evidence

| Runtime family | Current frame filler | Focal art | 2D transition status |
|---|---|---|---|
| Friend/arena games | Geometry, materials, occasional GLB room shell | GLBs and primitives, with a few protected cutouts | Fail |
| SideScrollStage clients | One portrait plate or no background | Real 3D player plus procedural props; one cutout companion | Fail |
| Picture games | 64×64 generated gradient | Mixed PNGs plus panels and labels | Partial |
| Dance | UI panels and lane shapes | Labels/buttons/effects | Partial |
| Fairy Pond | Three custom 1024² overhead plates | GLB bugs, gates, hazards, and boss states | Fail, background salvageable |
| Kart | Solid sky, 3D track/world | 3D vehicles, props, obstacles | Fail |
| Galaxy | Solid sky, spherical 3D world | 3D landmarks, creatures, avatar fallbacks | Fail |
| Ember Fortress overworld | Shader sky, spherical 3D planet | At least sixteen named GLB families plus procedural planet/atmosphere | Fail |
| Combat / Dungeon / Stuffie | Solid environment color, 3D arena | GLB or primitive enemies/props; sprite avatar in two engines | Fail |
| Opera | Solid environment color and procedural set shell | Opera/job GLBs plus procedural props | Fail, extensive 2D source ready |
| Ambient collection / companion systems | Host world's 3D space or procedural room | Eighteen collectible GLBs, catch-net GLB, creature models, primitive den/room | Fail |

The issue is not merely “low-resolution backgrounds.” In many games there is
no authored background at all. A flat material, colored box, or 3D floor
texture is doing the compositional job that the new art direction assigns to
purpose-built 2D illustration.

## Theme separation audit

### Reuse boundary

The production hierarchy is:

1. preserve Faron's protected `baby_doll.png`, `baby_doll2.png`, and
   `baby_doll3.png` exactly;
2. retain an exact current asset only after explicit technical and Mobile
   acceptance;
3. use protected or historical art as an identity reference without modifying
   the original;
4. regenerate a new theme-local asset for every questionable or incomplete
   case.

Opera source art is **Opera-only**. Its 833 images are a reuse opportunity for
the lobby, twelve career shows, and three Opera bosses only when a specific
image passes the exact-state acceptance gate; otherwise it is a direct
reference for regeneration, not a universal skin. Likewise, Fairy Pond masters
remain Fairy Pond references, Ember concepts remain Ember references, and
picture-game pieces remain picture-game references.

It is appropriate to share code for `SideScrollStage`, parallax math, sprite
anchors, alpha scissor, pointer behavior, import presets, hit regions, and
animation timing. It is not appropriate to share a finished background,
decorative motif, generic “magic” prop pack, arena plate, enemy silhouette, or
palette merely because two games use the same camera or interaction.

### Current cross-theme contamination

These are active runtime risks that must be split during conversion:

- `scripts/opera_act.gd:605-629` uses generic `assets/art35/cards/mg/*`
  picture-game sun, star, flower, ornament, Christmas-tree, and rainbow cards,
  plus `style3/*` fruit, crystal, shipwood, and leaf cards, as dress across
  unrelated careers. Replace those with the matching career's existing Opera
  cards; do not promote the generic dress table into the 2D pipeline.
- `scripts/opera_act.gd:1379`, `scripts/games/brawl.gd:164`, and
  `scripts/stuffie_battle.gd:228` all spawn the same `DungeonArt` imp.
  Opera mischief performers, toy-castle troublemakers, and soft stuffie
  opponents need three distinct silhouette/costume families.
- `scripts/stuffie_battle.gd:152` imports the Dungeon arena and line 245 can
  import its boss. A tint does not turn an icy stone dungeon into a bedroom
  play mat.
- Fetch and Slide both use `assets/art35/arena/winter_tree_*.glb`. Their new
  sprites must split: quiet rounded lakeshore trees for Chuck's fetch space;
  swept, speed-readable alpine markers for the downhill race.
- Fairy Pond already has nine bespoke 1024² top-down sprite masters, but the
  runtime embeds them into GLBs and does not reference the PNG masters. The 2D
  conversion should promote copies of those exact masters into runtime sprite
  assets, not replace them with dungeon hazards, generic garden icons, or new
  Opera-style flora.
- Combat, Castle Dungeon, Ember Dungeon, and Stuffie Battle may share an
  overhead engine schema. They must not share a room plate or a recolored enemy
  pack. Their setting, silhouettes, edge dressing, and effect language are
  different.
- The picture games share a generated gradient because they are placeholders.
  That is not evidence that Snowman, Garden, Trampoline, and Christmas should
  share one finished room or one decorative kit.

### Per-game visual DNA and prohibited borrowing

| Game / surface | Identity that must survive the 2D shift | Reserved motifs and composition | Do not borrow |
|---|---|---|---|
| Fetch — Chuck | Quiet winter lakeshore play with Chuck | Powder-blue snow, rounded shore pines, open throw lane, warm dog focal | Slide speed stripes, race gates, Opera curtains |
| Dolls — nursery | Dreamy, intimate nursery memory | Wide companion to the protected nursery page, quilt softness, cradle and pillow shapes | Trampoline carnival energy, Opera gold, dungeon geometry |
| Toy-castle brawl | Friendly cardboard/foam castle adventure | Chunky toy crenellations, fabric flags, visible stage progression, harmless toy foes | Stone dungeon plate, Opera proscenium, real fortress severity |
| Seek — Lamb-a' | Close-to-ground secret meadow | Soft hide clusters, peek gaps, clover/flower landmarks, Lamb as the value focal | Opera Farmer footlights, Garden pot sockets, Butterfly Galaxy stars |
| Treasure cavern | Quiet luminous discovery | Geodes, pearl glints, rounded safe cave pockets, chest reveal | Dungeon combat octagon, Opera Magician parlour, Ember lava |
| Melody — rainbow theater | Modern family concert with Daddy | Rainbow crown/sound towers, aqua-neon pulses, seven clear orb stations | Shell-gold Opera house, Pop Star job set, generic nightclub UI |
| Kareem's shop | Lived-in reef market/cabin | Practical shelves, tanks, handmade wares, pearl pictograms, Kareem's protected cutout | Opera Pastry/Candy machinery, formal theatre dressing |
| Play-place | Sunny child-scale climbing course | Rounded playground modules, safe rails, checkpoint sockets, open sky | Slide snow, toy-castle walls, Opera scenery |
| Penguin / rainbow slide | Fast, celebratory downhill snow ride | Swept alpine silhouettes, rainbow track accents, readable turns and finish arch | Fetch's quiet lakeshore layout, Opera Racecar track |
| Fairy Pond | Botanical enchanted pond seen from above | Aqua/lavender water, lily margins, indigo contours, jewel bugs, flower-growth boss | Galaxy celestial grids, Garden UI pots, dungeon hazards |
| Snowman picture game | Simple snowy play-yard craft | Three clear snowball sockets, mitten-soft props, quiet roll lane | Fetch traversal scenery, Christmas interior, Opera icons |
| Garden picture game | Airy book/craft garden | Five pot sockets, sunny greenhouse or garden edge, retained flower family | Seek hide clusters, Opera Farmer stage, Fairy boss flora |
| Trampoline picture game | Bright safe toy-yard or cloud playroom | One dominant trampoline, open bounce arc, stars as feedback only | Dolls' sleepy nursery mood, Opera recital hall |
| Christmas picture game | Cozy winter room/window scene | Central empty-tree socket, warm window light, five ornament homes | Opera Candy Maker ornament dressing, generic star field |
| Dance | Mermaid Roshan performance space | Four wordless lane medallions, audience silhouettes, beat pulse, character-first staging | Opera career sets, Melody's seven-orb concert layout |
| Kart — ocean | Storybook ocean race | Reef roadway, nautical barriers, fish/pearl pickups, ocean vehicles | Opera Grand Prix footlights, Galaxy planet road |
| Kart — butterfly/rainbow | Airy Butterfly World race | Rainbow bridges, crystal-butterfly landmarks, lighter celestial color rhythm | Ocean nautical props, Fairy Pond botany, Opera race set |
| Butterfly Galaxy | Large celestial dream-world journey | Distinct destination panoramas, crystal landmarks, butterfly realm scale | Fairy Pond's overhead garden language, Opera Magician stars |
| Ember Fortress overworld | Volcanic pilgrimage around five lantern landmarks | Long ash path, black paper-cut skyline, five unmistakable lantern stations, Great Gate destination | Galaxy crystal world, a generic red planet, Opera Dragon spectacle |
| Combat arena | Elemental training/play arena | Clean telegraph zones, element-specific plates and effects, readable enemy rings | Dungeon narrative rooms, Stuffie fabric mat, Opera boss stage |
| Castle dungeon | Icy pearl-castle puzzle adventure | Graphic octagonal rooms, frosted pearl trim, door/puzzle landmarks | Combat recolors, Ember black/lava kit, Stuffie toys |
| Ember dungeon | Volcanic paper-cut fortress | Obsidian shapes, ember orange, cooled-lava paths, ash flora, heat devices | Castle ice palette, generic red tint, Opera dragon scenery |
| Stuffie battle | Bedroom/den make-believe sparring | Stitched play mat, cushion boundaries, soft toy silhouettes, friendly impacts | Dungeon stone arena/imps, Castle boss, hard weapon language |
| Stuffie companion wing | Cozy care, choosing, painting, and home shelves | Quilted den, soft shelf cubbies, stitched wants, each stuffie's own silhouette | Battle arena, hard dungeon materials, Opera wardrobe |
| Critter collection | Gentle field-guide discovery across existing habitats | Habitat-specific cards, naturalist-book page, eighteen crisp animal silhouettes | Fairy bug enemies, Opera decoration, one generic recolor family |
| Castle echo bells | Pearl Castle music-room listening game | Seven large rainbow bars, shell-room acoustics, note pulses traveling in order | Melody's concert orbs, Opera Pop Star stage, generic piano UI |
| Opera lobby | Formal shell palace and show-selection space | Shell-gold architecture, crimson curtains, velvet/pearl lighting | Exporting this identity to any non-Opera game |
| Opera bosses | Spectacle inside the established Opera house | Curtain Dragon, Shadow Phantom, Midnight Maestro each get a distinct stage state family | Dungeon enemies, Galaxy star kit, generic purple “magic” |

Shared characters may recur without a redesign when the story says they are
the same person. Their protected source files remain untouched. Reusing a
character identity does not imply reusing the host game's environment, palette,
costume, or prop family.

## Full minigame ledger

Priority meanings:

- **P0** — directly violates the 2D-only owner rule.
- **P1** — already 2D, but visibly placeholder-like or missing custom stage art.
- **P2** — cleanup, inactive legacy path, or secondary polish after the main
  conversion.

| Game / surface | Current implementation | Main graphical finding | Reuse or generate | Priority |
|---|---|---|---|---:|
| Fetch — Chuck | `games/fetch.gd`: winter-shore/tree GLBs, Chuck GLB, eight primitive sites | Bright but sparse 3D snow lane; no authored wide background; focal character is banned | Generate a winter lakeshore flat stack and new Chuck action sprites from his protected identity reference without modifying it | P0 |
| Dolls — nursery | `games/dolls.gd`: `nursery_bg.jpg`, real 3D Roshan, procedural babies/pillows/cradle | Portrait book page floats behind a wide stage; every interactive object except the page is 3D | Preserve the book page; generate a new wide nursery inspired by it, plus sleeping-baby, pillow, cradle, and Roshan action sprites | P0 |
| Toy-castle brawl | `games/brawl.gd`: no backdrop; primitive wall, towers, roofs, banners, gates; DungeonArt enemies | Side-scroll engine is ready, but the “set” is a row of pastel primitives against raw environment space | Generate a 3–4 screen toy-castle courtyard stack and standees; reuse protected Huluu unchanged | P0 |
| Seek — Lamb-a' | `games/seek.gd`: Lamb and meadow-bush GLBs, primitive hill | Attractive color family, but still an open 3D bowl with no authored stage composition | Generate meadow hide-and-seek stack; create Lamb hide/peek/celebrate sprites from identity reference | P0 |
| Treasure cavern | `games/treasure.gd`: chest/dais/cluster GLBs and primitive gems/coins | Dark empty 3D floor with isolated loot; no layered cavern storytelling | Generate a luminous child-safe cavern stack and separate chest, gem, coin, dais, and checkpoint sprites | P0 |
| Melody — rainbow theater | `games/melody.gd`: procedural 3D theater, Daddy GLB preference, 14 primitive sites | Visually busy construction, inconsistent scale, and no painted theater plate | Generate a custom rainbow concert/theater stack; reuse Daddy's protected cutout rather than the GLB; generate seven orb sprites | P0 |
| Kareem's shop | `games/shop.gd`: shop GLB, primitive wares/tanks/door, two OmniLights, protected Kareem cutout | Kareem fits; everything around him is 3D. Labels and numeric prices make the shop reading-dependent | Generate an open-front shop interior stack and individual merchandise/tank/door standees; replace prices with repeated pearl pictograms | P0 |
| Play-place course | `games/slide_race.gd`: procedural 3D platforms/rails | Geometry carries all visual identity; no tailored background | Generate a side-on playground climb stack with clear checkpoint sockets and sprite platforms/rails | P0 |
| Penguin / rainbow slide | Same file: snowbank/tree/finish GLBs and procedural rail | Long bright track, but washed-out empty sky and 3D roadside objects dominate | Generate scrolling downhill background layers, road/skirt tiles, penguin poses, pickups, snowbanks, trees, and finish arch sprites | P0 |
| Fairy Pond | `games/fairy.gd`: three 1024² plates plus twelve named GLB families and primitives | Best current background, but the strong paintings are covered by incompatible modeled focal art | Keep plates as reference or approved floor plates; promote the nine existing top-down PNG masters for three bugs, leaf, and five flower-growth states; generate only missing gates, hazards, projectiles, reticle, and effects | P0 |
| Snowman picture game | `games/picture_games.gd`: 64×64 gradient, circles/panels, 128² carrot, 804×755 coal | Mostly blank screen with giant UI circles; text carries the verb; focal asset quality is uneven | Generate a snowy play-yard plate with quiet roll lane and three sprite snowball states; regenerate the tiny carrot as a crisp 512² derivative | P1 |
| Garden picture game | Same file: gradient, panel mound/pots, mixed generated/book-derived sprites | Strong newer flower art sits over generic circles; background has no sense of place | Generate a sunny garden/greenhouse plate with five empty pot sockets; retain accepted flowers, butterfly, watering can, and seed where they survive phone review | P1 |
| Trampoline picture game | Same file: gradient, one panel trampoline, star and Roshan cutout | Extremely sparse and UI-like; button text is the main instruction | Generate a safe toy-yard or cloud-playroom plate, trampoline sprite states, bounce trail, and wordless hand/tap pictogram | P1 |
| Christmas picture game | Same file: gradient plus strong tree/ornament PNGs | Focal art is the best of this suite, but it floats on a dark gradient with no scene | Generate a cozy winter room/window plate with a clean central tree socket; retain accepted empty tree and five ornament sprites | P1 |
| Legacy picture slide | `_mg_build_slide()` remains, but `_mg2d_open("slide")` routes to the 3D play-place | Inactive duplicate uses plain colored bands and a text GO button | Delete or keep unreachable until the real slide becomes 2D; do not spend art budget on both paths | P2 |
| Dance engine | `games/dance_engine.gd`: Canvas UI only | Medium is compliant, presentation is generic rhythm UI rather than a Mermaid Roshan stage | Generate a reusable 2D performance plate, four wordless lane medallions, beat pulse, success burst, and audience silhouettes | P1 |
| Kart — ocean and rainbow | `kart.gd`: 21 unique quoted GLB literals and 31 primitive constructor sites | Complete 3D dependency: vehicles, track, world, selection plinths, props, and hazards | Build a sprite-based rail presentation: rear/turn vehicle sheets, opaque road/skirt tiles, background layers, sprite obstacles, sprite selection carousel | P0 |
| Butterfly Galaxy | `galaxy.gd`: 23 unique quoted GLB literals and 22 primitive constructor sites | Complete 3D spherical world; washed wide compositions and tiny focal targets | Reframe as connected 2.5D storybook stages using custom Butterfly World panoramas, landmark standees, and sprite avatar/creatures | P0 |
| Ember Fortress — five lanterns and Great Gate | `ember_fortress.gd`: spherical procedural planet, shader sky, at least sixteen named GLB families, model-first avatar | A full playable collection journey omitted by any dungeon-only fix; text-heavy HUD compensates for small targets on a globe | Reframe as connected volcanic promenade stages; use Ember concepts for theme anchors and separate lantern, gate, King, hazard, avatar, and home-ring sprites | P0 |
| Combat arena | `combat_arena.gd`: solid background, primitive floor/enemies, Sprite3D Roshan | Simple readable loop, but the arena is a colored primitive diagram rather than storybook art | Generate one overhead arena plate per element family and sprite sheets for enemies, shots, telegraphs, and reward states | P0 |
| Castle dungeon | `dungeon_level.gd`, `dungeon_art.gd`, `dungeon_puzzle_room.gd`: 28 GLB tokens in art map | Current layout is readable, but all ten rooms are variations on a modeled octagon with GLB props | Keep deterministic room logic; replace the art loader with 2D room plates and separate top-down sprite props/characters | P0 |
| Ember dungeon variant | Reuses the same dungeon engine with Ember GLB art map | Same structural failure, recolored darker; cannot be left behind when the shared loader changes | Produce an Ember-only plate/standee family in the shared sprite schema; evaluate the existing 40 isolated Ember concept pieces; reuse no Castle or 3D fallback | P0 |
| Stuffie battle | `stuffie_battle.gd`: solid background, primitive arena/effects, Lamb GLB boss | No authored setting; controlled stuffie and enemies are model-driven | Generate a friendly overhead play-mat plate, active-stuffie pose sprites, imp sprites, Lamb boss sprites, dodge/bruise pictograms | P0 |
| Opera lobby | `opera_house.gd`: Opera GLBs, primitives, solid background | Runtime ignores the excellent 2D Opera house source collection | Rebuild from the existing 2D master scene key and isolated cards; generate only missing layer repairs/states | P0 |
| Opera — 12 career shows | `opera_act.gd`: procedural sets, job GLBs, solid backgrounds | Every career has custom 2D concepts and/or scene keys, but none are wired as runtime art; the current dress table also mixes generic picture-game and style-kit cards across jobs | Promote each career's own scene key/environment kit/cards into production flats and standees; remove generic cross-job dressing | P0 |
| Opera — 3 bosses | Curtain Dragon, Shadow Phantom, Midnight Maestro use Opera GLBs | Bosses repeat the same 3D stage language | Use the existing dragon, phantom, and maestro 2D cards as identity anchors; generate three full stage-state layer sets | P0 |
| Castle echo-bell game | `main.gd` plus `arena/castle_hall.gd`: seven Pearl Castle GLB bars, GLB song star, modeled room, labels | Genuine no-fail listening minigame was outside the extracted game-file scan; the notes are readable, but presentation remains model-driven and the objective lives partly in text | Keep it a Pearl Castle music room; create seven distinct 2D bell/bar sprites, note-pulse sequence, song-star sprite, and a music-room plate or local flat stack | P0 |
| Critter collection and Critter Book | `collection_system.gd`: eighteen collectible GLBs, catch-net GLB, generic UI panels, emoji and names | Ambient catching is a playable collection mode and violates 2D-only; the book depends heavily on text and generic panels | Replace each critter and net with habitat-correct sprites; give the book illustrated habitat tabs/cards and silhouette progress while retaining names only as adult supplement | P0 |
| Stuffie companion wing / den | `companion.gd`: direct Lamb GLB, modeled/generated creatures, primitive gift, room, shelves, tournament den; procedural picker | Adjacent care/selection mode is visually tied to Stuffie Battle but currently mixes hard geometry, labels, and model-first roster paths | Build a soft 2D den/room family, shelf and gift standees, 2D stuffie pose layers, and pictorial care/picker cards; share character identities with battle, not its arena | P0 |

### Entry and selection surfaces

The launch landmark is part of each minigame's graphical contract. A child
sees it more often than some win screens, so converting only the loaded arena
would leave a highly visible 3D seam.

| Entry surface | Current evidence | Required 2D treatment |
|---|---|---|
| Friend-started arena games | World friend plus generic focus ring/action prompt | Keep the exact friend identity; add a small game-local prop cluster or medallion that previews the verb |
| Ocean Kart | Procedural torus, shader rainbow, OmniLight, `Label3D` instructions | Ocean-race arch sprite and vehicle/flag pictogram; no Opera race dressing |
| Penguin Slide | Primitive ice floe, Penguin model path, `Label3D` title | Penguin standee, illustrated floe/slide vista, downward-motion pictogram |
| Toy-castle brawl | Primitive keep/towers plus protected Huluu cutout | Preserve Huluu; replace the model castle with a foam/cardboard castle vignette |
| Treasure / Shop / Stuffie den | Host-world object or primitive ring plus text/action prompt | Theme-local cave, market, and stitched-den vignettes; no universal portal |
| Picture games | Castle wall pictures and generic `PLAY` prompt | Use the actual picture's visual subject as the large tap target; never use Opera frames on all pictures |
| Rainbow Kart / Butterfly World / Ember | Shared gateway code, labels, modeled destination props | Three distinct destination silhouettes: race arch, butterfly/crystal gate, ember-black gate |
| Castle Dungeon | Modeled Pearl Castle door | Icy pearl puzzle-door flat/standees, visually separate from Ember |
| Pearl Opera | Modeled marquee/threshold | This is the correct place for Opera shell-gold and curtain language |
| Castle echo bells | Music Star GLB and shell-room objects | Song-star sprite plus seven-color sound ripple leading toward the room |

The Hybrid action button already pairs a pictogram with its word
(`PLAY`, `RACE`, `ENTER`, and similar). Keep the pictogram as the primary
signal and treat the word as optional adult support. World `Label3D` sentences
must not be the only way to distinguish two entrances.

## Existing tailored 2D art: reference, verify, or regenerate

### Opera house

`assets_src/concepts/opera_house_flat/` contains:

- 13 full 1024-wide source sheets, including 1024×576 lobby and stage scene
  keys;
- 172 isolated 2D cards;
- 185 PNGs total.

Notable production anchors:

- `opera_house_master_scene_key_2026-07-21.png`
- `opera_house_stage_scene_key_2026-07-21.png`
- `cards/opera_stage_scenic_backdrop.png`
- `cards/opera_floor1_curtain_dragon.png`
- `cards/opera_floor2_phantom_puppet.png`
- `cards/opera_floor3_maestro_puppet.png`

The runtime's `assets/art35/opera/*.glb` and `assets/art35/cards/*.glb`
represent the retired 3D conversion path. The correct source direction is the
PNG library, not another conversion of those PNGs into models.

This collection's shell-gold, curtain, velvet, pearl, and proscenium language
is reserved for the Opera house. It must not become the default treatment for
arena, picture, Kart, Fairy, Galaxy, or dungeon backgrounds.

### Opera career shows

`assets_src/concepts/opera_jobs_flat_2026-07-21/` contains:

- 36 source sheets at 1024×1024;
- 576 isolated cards;
- 612 PNGs total.

`assets_src/concepts/opera_jobs_2p5d_2026-07-24/` adds twelve 1024×576 scene
keys and twelve 1024×1024 environment kits.
`assets_src/concepts/opera_jobs_hybrid_finales_2026-07-24/` adds twelve
1024×576 finale keys.

| Career | Existing primary scene key | Production action |
|---|---|---|
| Pastry Chef | `pastry_chef_2p5d_scene_key_2026-07-24.png` | Separate/heal background layers; use existing gameplay cards for cake states |
| Detective | `detective_2p5d_scene_key_2026-07-24.png` | Separate library backdrop, boxes, clues, and tiara standees |
| Ballerina | `ballerina_2p5d_scene_key_2026-07-24.png` | Separate recital hall and four dance-tile states |
| Candy Maker | `candy_maker_2p5d_scene_key_2026-07-24.png` | Separate workshop, press, candies, belt, and gauge sprites |
| Doctor | `doctor_2p5d_scene_key_2026-07-24.png` | Separate clinic, patient, scan, cast, and recovery states |
| Farmer | `farmer_2p5d_scene_key_2026-07-24.png` | Separate meadow parallax, barn, piggies, food, mud, and picnic sprites |
| Boxer | `boxer_2p5d_scene_key_2026-07-24.png` | Separate ring backdrop, bag, gloves, belt, crowd, and imp poses |
| Magician | `magician_2p5d_scene_key_2026-07-24.png` | Separate parlour, three hats, bunny-fish, swap trails, and reveal states |
| Painter | `painter_2p5d_scene_key_2026-07-24.png` | Separate gallery, easel, paint pots, brush states, splats, and finished canvas |
| Astronaut Engineer | `astronaut_engineer_2p5d_scene_key_2026-07-24.png` | Separate launch pad, rocket, pipes, slots, valve, and launch states |
| Racecar Driver | `racecar_driver_2p5d_scene_key_2026-07-24.png` | Use sprite-rail Kart presentation; separate Opera track and vehicle poses |
| Pop Star | `pop_star_2p5d_scene_key_2026-07-24.png` | Separate concert plate, microphone states, rhythm icons, and finale effects |

These source keys are identity references and concept composites, not drop-in
runtime backgrounds.
Interactive objects painted at play depth must become separate standees, and
the background must be healed behind them. Cropping a key into one big mural
would recreate the layering bug the promenade work order explicitly forbids.

The common proscenium is an Opera continuity device, not a reason to collapse
the twelve careers into one look:

| Career | Theme-local identity | Exclude |
|---|---|---|
| Pastry Chef | Warm bakery workbench, cake build, flour and icing shapes | Kareem's market shelves; Candy Maker machinery |
| Detective | Cozy library mystery, clue boxes, tiara reveal | Magician occult shorthand; generic crystal/star scatter |
| Ballerina | Airy recital hall, floor marks, ribbon movement | Pop Star concert lighting; Dance minigame lane UI |
| Candy Maker | Playful candy workshop, press, conveyor, bright sweets | Christmas ornaments as filler; Pastry kitchen props |
| Doctor | Reassuring toy-like clinic, scan and recovery sequence | Laboratory menace; Astronaut pipes |
| Farmer | Constructed meadow show with barn, piggies, mud, picnic | Seek's natural hide clusters; Garden's pot-board layout |
| Boxer | Friendly exhibition ring, gloves, belt, readable crowd | Dungeon combat arena; threatening weapon motifs |
| Magician | Intimate parlour, hats, bunny-fish reveal, swap trails | Galaxy stars as scenery; Detective clues |
| Painter | Bright gallery/studio, easel and controlled splat shapes | Garden flower pack; generic rainbow dressing |
| Astronaut Engineer | Storybook launch pad, pipes, slots, valve, rocket | Galaxy destination panoramas; Doctor clinic equipment |
| Racecar Driver | Indoor theatrical Grand Prix with audience and footlights | Ocean Kart or Butterfly Kart tracks and vehicles |
| Pop Star | Career-specific concert stage, microphone and finale lights | Melody's Daddy-centered seven-orb theater |

### Fairy Pond

The active 1024×1024 plates are properly sized and purpose-built:

- `assets/fairy/pond_dawn.png`
- `assets/fairy/pond_twilight.png`
- `assets/fairy/pond_boss_clearing.png`

They are the strongest current minigame background reference family, but they
still require fresh Mobile review. Their long-track seams and repeated square
composition need testing. Regenerate any plate that does not pass rather than
searching for another pond image elsewhere in the project.

The export-excluded `assets_src/fairy_v2/runtime_textures/` also contains nine
finished 1024×1024 transparent masters:

- `bug_jewel.png`, `bug_moth.png`, and `bug_firefly.png`;
- `boss_leaf.png`;
- `boss_seed.png`, `boss_sprout.png`, `boss_bud.png`,
  `boss_opening.png`, and `boss_bloom.png`.

They already follow a coherent top-down Fairy contract: rounded phone-readable
silhouettes, thin indigo contours, two or three cel-value bands, and
aqua/lavender lighting. They are presently embedded into runtime GLBs. Copy
them into an importable runtime sprite location and use the PNGs directly;
preserve the source masters. New generation is limited to uncovered gate,
shadow-hazard, projectile, reticle, and feedback states after a state-by-state
runtime check.

### Ember Fortress

`assets_src/concepts/ember_fortress_claude_2026-07-22/` contains 51 PNGs:
six 1024×683 overview boards, five contact sheets, and forty isolated 1024²
expansion pieces. The isolated set includes architecture, terrain, devices,
flora, and effects such as the basalt archway, cooled-lava flow, ember cave
mouth, magma lever, heat plate, ember bloom, ash fern, and spark trail.

These are candidates and theme anchors, not automatic drop-ins: verify alpha,
viewpoint, ground line, phone silhouette, and texture rules before promotion.
Even if only part of the set survives review, it makes a generic recolor of the
Castle Dungeon unnecessary and visually incorrect.

### Kart and Butterfly World

The non-rejected concept boards in
`assets_src/concepts/cc0_ocean_replacements_2026-07-22/` include original 2D
vehicle, butterfly, crystal, castle, reef, and furniture directions. In
particular, `regen_02_03_vehicles.png`, `regen_04_06_crystal_family.png`,
`regen_07_crystal_castle.png`, and `regen_09_10_butterflies.png` can anchor
new sprite extraction or generation. Files under that collection's
`rejected/` folder are excluded.

Ocean Kart, Butterfly/Rainbow Kart, and Butterfly Galaxy may share a canonical
vehicle, butterfly, or landmark only when it depicts the exact same story
object. They still require independent background compositions and must not
inherit Opera Racecar's indoor theatrical track.

### Picture-game focal pieces

The newer ImageGen-derived assets in `assets/mg/` are materially better than
the old generated UI shapes. Strong candidates to retain after current Mobile
capture are:

- butterfly, coal, fish body/fins;
- tree and empty Christmas tree;
- five ornaments;
- sun and star;
- generated flower and plant family.

Do not automatically retain the older tiny or near-empty assets merely because
they are already PNGs. Medium compliance is not quality acceptance.

## Required background and standee briefs

### Fixed-screen Canvas games

Snowman, Garden, Trampoline, Christmas, and Dance each need:

- one opaque 2048×1024 POT background with a center-safe 16:9 gameplay crop;
- a quiet lower third and clear sockets for every live target;
- no baked interactive objects;
- individual 512×512 or 512×1024 alpha sprites for live pieces;
- one wordless “tap/drag/turn” pictogram animation or two-state card;
- no text embedded in the art.

The existing text labels may remain temporarily for adult debugging, but the
child-facing composition must communicate the objective without them.

### Side-on arena games

Fetch, Dolls, Brawl, Seek, Treasure, Melody, Shop, Play-place, and Slide should
use the already-implemented `SideScrollStage.layers` and `flat()` paths.
Each stage follows the promenade format:

| Layer | Runtime role | Size |
|---|---|---:|
| L0 sky | Opaque, rides camera | 1024×512 |
| L1 far | Opaque, distant silhouettes, seamless | 2048×1024 |
| L2 mid | Alpha, identity dressing, ≤40% transparent pixels | 2048×1024 |
| L3 skirt | Opaque play-plane strip | 2048×512 |
| L4 fore | Optional sparse alpha vignette, ≤15% painted pixels | 2048×512 |

All interactive props and anything the player can pass in front of or behind
are separate POT standees with their ground line at the painted bottom edge.
The L0–L4 table is a file and performance contract, not a shared art pack.
Every game receives a separate palette strip, motif list, silhouette sheet, and
“do not borrow” list from the theme matrix above before art production begins.

### Overhead games

Fairy, Combat, Dungeon, Ember Dungeon, and Stuffie Battle need:

- 1024×1024 opaque floor/room plates;
- optional sparse 1024×1024 edge-overlay plate;
- separate top-down or three-quarter sprite states for every moving target;
- alpha-scissor edges for focal sprites;
- scale and anchor registration shared across every animation state;
- no textured 3D floor hidden under the plate as a visual fallback.

### Kart

The game can retain its deterministic rail math, but the presentation must
become sprite-based:

- rear, rear-left, rear-right, celebration, and selection poses per vehicle;
- opaque 2048×1024 road/skirt tiles;
- L0–L2 background layers per theme;
- separate barrier, pickup, ramp, hazard, finish, and audience sprites;
- a 2D selection carousel with pictorial handling cues instead of 3D plinths;
- no GLB vehicle fallback.

### Galaxy

Do not attempt to “flatten” the existing spherical model world by rendering it
through Blender. Recompose Butterfly World as authored promenade stages:

1. meadow/home gate;
2. crystal approach;
3. castle hall;
4. ice gate/boss approach.

Each needs its own painted layer stack and landmark standees. The current
planet-wide view makes targets tiny even before considering the medium change.

### Ember Fortress overworld

Do not reduce the five-lantern journey to one red Galaxy reskin. Retain the
analytic progression but present it as connected 2.5D volcanic stages:

1. ash-moon arrival and first lantern;
2. obsidian bridge / cooled-lava crossing;
3. ember settlement and device landmarks;
4. fortress approach with the remaining lanterns;
5. Great Gate, Ember King, and home-ring junction.

Each lantern needs a unique surrounding landmark so the objective can be
remembered spatially without reading a `5 / 5` counter. The Ember concept set
provides relevant architecture, terrain, devices, flora, and effects; the
Galaxy crystal/butterfly kit and Opera dragon set do not.

### Ambient playable systems

Critter collection inherits the host world's background, so it does not need
one universal minigame plate. It does need eighteen 2D critter sprites,
habitat-aware scale/contrast, a 2D catch-net sweep, and an illustrated Critter
Book whose empty/caught state reads by silhouette. Reef, meadow, river, and
alpine cards should preserve their local habitat colors rather than recoloring
one card four ways.

The Stuffie companion wing and its battle can share the exact same stuffie
character sprites and care-state poses. They should not share a room
background: the wing is a quilted home/shelf/picker space; the battle is a
separate play-mat arena. Lamb-a's protected identity reference stays intact,
and her GLB path is removed when this surface is converted.

## Production order

### Batch A — fast visible correction

1. Picture-game backgrounds and wordless verb cards.
2. Dance stage plate and lane medallions.
3. Dolls nursery, because the engine already supports layered flats and the
   protected page provides a strong identity reference.
4. Toy-castle brawl, because the engine already supports wide layers,
   standees, and a cutout companion.

This batch removes the most obvious “prototype UI” presentation with the least
gameplay risk.

### Batch B — high-value existing, theme-local art

1. Opera lobby.
2. The twelve Opera career stage sets using each career's own 2.5D keys and
   cards.
3. The three Opera boss stages.
4. Fairy focal sprite conversion using the nine existing PNG masters while
   retaining/reviewing its plates.
5. Ember asset triage using the isolated Ember concept set, without importing
   Castle or Opera visual language.

This batch should emphasize asset integration and layer repair, not broad new
generation.

### Batch C — arena conversion

1. Fetch and Seek.
2. Treasure and Shop.
3. Melody.
4. Castle echo bells.
5. Play-place and Penguin/Rainbow Slide.
6. Combat, Dungeon, Ember Dungeon, and Stuffie Battle.
7. Companion wing / den and Critter collection sprites and book.

Convert one mechanically isolated game per commit and keep shared state and
gameplay behavior unchanged.

### Batch D — structural presentation conversions

1. Kart sprite-rail presentation.
2. Butterfly Galaxy promenade rebuild.
3. Ember Fortress five-lantern promenade rebuild.

These retain the largest amount of bespoke simulation while replacing nearly
their entire visual layer. They need their own device-tested milestones.

Every batch converts each game's entry landmark in the same game-specific
change. Entry surfaces are not deferred to one generic portal pass.

## Per-game acceptance gate

A conversion is not complete when PNGs merely load. Every game must pass all
of the following:

1. **Dependency gate:** no runtime `.glb` load, model fallback, or
   `MeshInstance3D` focal-art construction remains in the touched game.
2. **Composition gate:** at 1280×720, the objective is identifiable after a
   one-second squint test; focal sprites win the value/saturation hierarchy.
3. **Non-reader gate:** an idle child receives a voice line and visible pointer;
   text is not required to identify the next action.
4. **Touch gate:** the visual target and forgiving touch region agree; the
   target does not hide behind L2/L4 alpha art.
5. **Layer gate:** no object at play depth is baked into a mural; standee ground
   lines and depth sorting remain stable throughout the route.
6. **Theme gate:** a side-by-side contact sheet does not make two different
   games look like reskins. Each frame preserves its row in the visual-DNA
   matrix; Opera-specific shell-gold, curtain, and footlight motifs stay inside
   Opera, and each Opera career remains distinct inside that frame.
7. **Mobile gate:** current Mobile-renderer screenshots at selection/start,
   active play, mercy/help, and win states; no alpha-overdraw regression on
   Speedy.
8. **Asset gate:** POT/import limits, license line, correct naming, and no
   modification of protected originals.
9. **Behavior gate:** trusted probes remain green. Visual conversion does not
   rewrite objectives, rewards, save keys, or no-fail behavior.
10. **Review gate:** owner accepts the current M11 views before the family can be
   called 5/5.

## Definition of done for the whole audit program

The graphical transition is complete only when:

- every row marked P0 has no 3D visual dependency;
- every minigame has a purpose-built background plate or layer stack;
- every active target, prop, character, vehicle, and effect is a 2D sprite;
- every minigame has a recorded theme-local palette, motif, silhouette, and
  prohibited-borrowing check; shared technical schemas do not collapse the
  settings into one visual treatment;
- every existing high-quality custom 2D collection is either wired into the
  runtime or explicitly rejected with a recorded visual reason;
- the old GLB and primitive visual fallbacks are removed from touched runtime
  paths rather than left as silent regressions;
- current Mobile contact sheets cover the complete roster, including all
  fifteen Opera acts, both Kart themes, both dungeon palettes, all picture
  games, the Ember overworld, echo bells, Critter Book/catching, Stuffie
  selection/care/battle, entry landmarks, active play, mercy/help, and win
  states.

## Audit coverage appendix

The 122-GLB / 161-primitive indicator in the executive verdict was collected
from these 21 core visual runtime files:

- `scripts/games/fetch.gd`
- `scripts/games/dolls.gd`
- `scripts/games/brawl.gd`
- `scripts/games/seek.gd`
- `scripts/games/treasure.gd`
- `scripts/games/melody.gd`
- `scripts/games/shop.gd`
- `scripts/games/slide_race.gd`
- `scripts/games/fairy.gd`
- `scripts/games/picture_games.gd`
- `scripts/games/dance_engine.gd`
- `scripts/games/side_scroll.gd`
- `scripts/kart.gd`
- `scripts/galaxy.gd`
- `scripts/combat_arena.gd`
- `scripts/dungeon_level.gd`
- `scripts/dungeon_art.gd`
- `scripts/dungeon_puzzle_room.gd`
- `scripts/stuffie_battle.gd`
- `scripts/opera_house.gd`
- `scripts/opera_act.gd`

The completeness extension also traced launch landmarks and embedded/ambient
activities through `scripts/main.gd`, `scripts/arena/castle_hall.gd`,
`scripts/arena/sky_lagoon.gd`, `scripts/collection_system.gd`,
`scripts/companion.gd`, `scripts/ember_fortress.gd`, and
`scripts/touch_ui.gd`. Craft Studio, Wardrobe, pause/settings, sleep, and
passive touch-delight props were reviewed as adjacent UI or world activities
but are outside this minigame-background production ledger.

# Minigame 2D reconstruction — generated art record

Generation date: 2026-07-27
Tool: built-in OpenAI image generation
Processing: `tools/process_generated_minigame_asset.py`; transparent sources
also pass through the installed ImageGen `remove_chroma_key.py` helper.

## Production contract

- Every game receives its own environment and prop family.
- Opera motifs remain inside Opera.
- Backgrounds contain no characters, text, UI, or interactive objects.
- Moving or interactive objects remain separate sprites.
- Runtime backgrounds are opaque 2048×1024 PNGs.
- Runtime sprites are transparent power-of-two PNGs.
- Faron's protected babies remain the untouched originals:
  `assets/book/baby_doll.png`, `baby_doll2.png`, and `baby_doll3.png`.

## Shared Roshan catch sprite

Source: `shared/roshan_catch_chroma.png`
Runtime: `assets/minigames/shared/roshan_catch.png`

Prompt:

> Preserve Roshan's warm-brown hair, rainbow hair streak, lavender top,
> rainbow-scaled mermaid tail, cheerful identity, and child-friendly
> proportions. Create one full-body 2D side-on three-quarter gameplay cutout,
> facing right with both arms open in a ready-to-catch pose. Remove the
> backpack and all brands or copyrighted symbols. Use a dark-indigo storybook
> contour and soft painted cel bands on a flat magenta chroma background. No
> text, props, shadow, floor, watermark, or human legs.

The generated rainbow subject conflicted with a broad soft chroma matte. The
accepted runtime sprite uses a strict hard key plus a two-pixel edge contract;
the rejected broad-matte intermediates remain source-only for provenance and
must not be promoted.

## Faron's nursery

### Background

Source: `dolls/dolls_nursery_background_raw.png`
Runtime: `assets/minigames/dolls/background.png`

Prompt:

> Create a polished original wide 2D storybook background for Faron's dreamy
> underwater nursery: rounded shell alcoves, quilt-like wall panels, bubble
> garlands, coral night-lights, a pale floor skirt, and one aqua-water window.
> Use a very wide side-on composition with a quiet center and lower third.
> No characters, babies, dolls, cradle, pillows, interactive objects, text,
> UI, Opera treatment, 3D rendering, logos, or watermark.

### Three-slot cradle

Source: `dolls/dolls_cradle_chroma.png`
Runtime: `assets/minigames/dolls/cradle.png`

Prompt:

> Create one wide low shell-shaped nursery cradle with a pearl-cream rim,
> lavender quilted interior, rounded rocker base, and three visibly open
> resting slots. Orthographic side view, dark-indigo storybook contour, no
> babies or dolls, on a uniform green chroma background.

### Pillow bank

Source: `dolls/dolls_pillow_bank_chroma.png`
Runtime: `assets/minigames/dolls/pillow_bank.png`

Prompt:

> Create one continuous ground-level bank of seven oversized soft nursery
> landing pillows in lavender, dusty rose, pale aqua-blue, and warm cream,
> with stitched scallop and wave patterns. Orthographic side view,
> dark-indigo storybook contour, no characters or cradle, on a uniform green
> chroma background.

## Fixed-screen picture games

The four plates below are independent designs. Their sockets are environmental
landmarks only; every changing or touchable object remains a separate runtime
node.

### Snowman play-yard

Source: `picture/snowman_background_raw.png`
Runtime: `assets/minigames/picture/snowman_background.png`

Prompt:

> Create a wide snowy storybook play-yard with a quiet circular rolling lane
> across the left and lower center, an open stacking area at the right, distant
> rounded pines, a low fence, powder-blue snow, lavender shadows, and an
> uncluttered HUD area. No characters, snowman, snowballs, carrot, coal, text,
> UI, Opera treatment, 3D rendering, logos, or watermark.

### Garden workshop

Source: `picture/garden_background_raw.png`
Runtime: `assets/minigames/picture/garden_background.png`

Prompt:

> Create a sunny underwater storybook garden with exactly five separated empty
> planting sockets across the lower third, plus a light shell greenhouse edge,
> coral hedges, and quiet aqua water. No characters, seeds, sprouts, flowers,
> butterfly, watering can, text, UI, Opera treatment, 3D rendering, logos, or
> watermark.

### Trampoline cloud-playroom

Source: `picture/trampoline_background_raw.png`
Runtime: `assets/minigames/picture/trampoline_background.png`

Prompt:

> Create a safe underwater cloud-playroom with one large padded trampoline in
> the lower center and an empty glowing star-shaped destination halo high above
> it. Preserve a clear vertical bounce arc. No characters, star object, text,
> UI, Opera treatment, 3D rendering, logos, or watermark.

### Christmas room

Source: `picture/xmas_background_raw.png`
Runtime: `assets/minigames/picture/xmas_background.png`

Prompt:

> Create a cozy underwater winter room with a central empty tree-shaped alcove,
> five empty ornament dishes on a low shelf, a frosted round window, shell
> fireplace glow, and quilted rug. No tree, ornaments, friendship-flower object,
> characters, text, UI, Opera treatment, 3D rendering, logos, or watermark.

## Dance playground

Source: `dance/background_raw.png`
Runtime: `assets/minigames/dance/background.png`

Prompt:

> Create an informal open-air reef dance celebration with a broad center floor,
> four empty shell-medallion sockets along the bottom, soft audience silhouettes
> behind side rails, bubble-light garlands, and distant beat ripples. Explicitly
> exclude a proscenium, curtains, Opera-gold motifs, characters, arrows, text,
> UI, 3D rendering, logos, and watermark.

## Toy Castle

### Three-chapter courtyard

Source: `brawl/background_raw.png`
Runtime: `assets/minigames/brawl/background.png`

Prompt:

> Create a very wide side-on toy-castle courtyard that progresses through a
> quilted foam training yard, cardboard drawbridge court, and pillow-throne
> court. Use stitched flags, scalloped cardboard, and a continuous walk band.
> No characters, enemies, live gates, text, Opera treatment, real medieval
> weapons, 3D rendering, logos, or watermark.

### Mischief imp, padded gate, and Roshan bop pose

Sources: `brawl/imp_chroma.png`, `brawl/gate_chroma.png`,
`brawl/roshan_bop_chroma.png`
Runtime: `assets/minigames/brawl/imp.png`, `assets/minigames/brawl/gate.png`,
`assets/minigames/brawl/roshan_bop.png`

Prompts:

> Create a harmless tiny lavender stuffed prankster with teal floppy ears,
> mitten hands, springy feet, visible stitches, and a playful grin. No demon,
> weapons, fire, or threatening features.

> Create a tall padded gate of five rounded foam bars in a scalloped stitched
> frame, isolated for a vertical opening animation.

> Preserve Roshan's established identity and create a three-quarter right-facing
> action pose releasing one soft sparkle pop. No weapon, enemy, castle, human
> legs, or unrelated props.

All three were generated on uniform chroma fields, locally alpha-extracted,
and visually inspected. Huluu continues to use her existing protected cutout
unchanged; it was not regenerated or modified.

## Chuck's winter fetch

### Lakeshore plate

Source: `fetch/background_raw.png`
Runtime: `assets/minigames/fetch/background.png`

Prompt:

> Create a wide oblique-overhead winter lakeshore plate. The left side is a
> powder-blue safe snow field with a clear throw lane; the right side is a
> graphic aqua lake; a scalloped shore makes their boundary unmistakable.
> Include only far-edge pines and a small distant dock. No characters, dog,
> ball, arrow, text, UI, Opera treatment, 3D rendering, logos, or watermark.

### Chuck fetch pose

Source: `fetch/chuck_chroma.png`
Runtime: `assets/minigames/fetch/chuck.png`

Prompt:

> Use the family illustration only as Chuck's identity reference. Create Chuck
> alone as the same friendly black standard poodle with curly coat, floppy ears,
> red collar, and warm eyes in a playful fetch stance. Exclude the adult
> mer-person, ball, ground, and all unrelated content.

The ball and safe/wet aim arrow are new project-original SVG sprites created
for this minigame; they do not reuse or trace another project asset.

## Lamb-a's secret meadow

Sources: `seek/background_raw.png`, `seek/bush_chroma.png`,
`seek/lamb_chroma.png`
Runtime: `assets/minigames/seek/background.png`,
`assets/minigames/seek/bush.png`, `assets/minigames/seek/lamb.png`

Prompts:

> Create a wide oblique-overhead clover meadow with exactly four empty hide
> patches around a clear play circle. Frame it with low habitat flora and
> bubbles, while excluding characters, lamb, live bushes, garden pots, text,
> UI, Opera treatment, 3D rendering, logos, and watermark.

> Create one soft clover hide bush with a roomy lower hollow, mint foliage,
> small butter-yellow and coral flowers, and lavender fronds. No character,
> eyes, face, pot, or background.

> Preserve Lamb-a's round white body, wide ears, navy eyes with lashes, blush,
> tiny pink nose, wool curls, and gentle personality. Remove the printed egg,
> all wording, brands, and handheld objects; show empty little hooves.

The existing Lamb image was used only as an identity reference and remains
unchanged. The new background is opaque; bush and Lamb were generated on
uniform chroma and locally alpha-extracted.

## Secret Cave treasure

Sources: `treasure/background_raw.png`, `treasure/chest_chroma.png`
Runtime: `assets/minigames/treasure/background.png`,
`assets/minigames/treasure/chest.png`

Prompts:

> Create a safe luminous cave route through five rounded open pockets, ending
> at an empty pearl dais. Use indigo rock, aqua/lavender geodes, and soft coral,
> while excluding characters, chest, live path gems, checkpoint stars, dungeon
> or Ember motifs, text, UI, 3D rendering, logos, and watermark.

> Create one open lavender shell treasure chest on a low pearl dais with a
> coral cushion, tidy rainbow pearls, rounded toy-like gems, and a
> friendship-flower clasp. No danger, weapons, room background, text, or UI.

The checkpoint is a new project-original SVG sprite created for this
minigame. It does not reuse another project asset.

## Daddy Mermaid's rainbow pavilion

Source: `melody/background_raw.png`
Runtime: `assets/minigames/melody/background.png`

Prompt:

> Create a modern open-air underwater rainbow music pavilion with a broad
> uncluttered catch area, pearl-shell canopy, seven-color light ribbons, coral
> speaker flowers, and a distant friendly audience suggested only as soft
> silhouettes. No characters, live rainbow orbs, text, UI, proscenium,
> curtains, Opera-gold treatment, 3D rendering, logos, or watermark.

The seven live color targets use a new project-original SVG orb. Daddy
Mermaid continues to use his existing identity cutout unchanged.

## Kareem's Pearl Shop

### Shell-market plate

Source: `shop/background_raw.png`
Runtime: `assets/minigames/shop/background.png`

Prompt:

> Create a warm open-front underwater shell market for a preschool storybook
> game. Place exactly four large empty glass display windows across the back
> wall, a clear central shell pedestal for one live item, a roomy shopkeeper
> area on the right, and a shell-shaped open doorway on the left. Use coral,
> aqua, lavender, honey light, painted paper texture, and thick navy-purple
> contours. No people, mermaids, animals, merchandise, price numbers, labels,
> text, UI, Opera stage, proscenium, curtains, 3D rendering, logos, or
> watermark.

### Four reef-friend offers

Source: `shop/animals_sheet_raw.png`
Runtime: `assets/minigames/shop/turtle.png`,
`assets/minigames/shop/dolphin.png`,
`assets/minigames/shop/stingray.png`, and
`assets/minigames/shop/squid.png`

Prompt:

> Create a clean 2-by-2 sprite sheet with exactly four separate full-body
> aquatic toy sprites: a friendly small green sea turtle, blue dolphin,
> lavender stingray, and coral-pink squid. Use consistent 2D paper-cutout
> illustration, thick hand-inked navy-purple outline, softly painted pastel
> fills, gentle faces, and fully visible silhouettes. Isolate them on a uniform
> bright-green chroma field. No scenery, bubbles, water, plants, frames,
> dividers, labels, letters, numbers, logos, shadows, or extra objects.

The sheet was split by quadrant, locally alpha-extracted, and each sprite was
normalized to transparent 1024×1024 PNG. Kareem's existing friend cutout is
loaded unchanged. Beans, pearl markers, and the exit arrow are new
project-original SVG gameplay sprites.

## Play-place and downhill slides

### Indoor play-place

Source: `slide_race/playplace_raw.png`
Runtime: `assets/minigames/slide_race/playplace.png`

Prompt:

> Create a wide, slightly oblique side-on cutaway of a three-story underwater
> padded play place. Include a lower ball-pit basin and trampoline, middle
> rainbow finger curtain and mint hoop, upper finger curtain, and a large
> yellow spiral slide. Keep a clear climb route with six roomy glowing
> shell-shaped sockets. Use quilted coral, aqua, butter yellow, mint and
> lavender foam with painted-paper texture. No characters, live stars, text,
> UI, theater/Opera treatment, logos, watermark, or 3D render.

### Baby-penguin winter run

Source: `slide_race/penguin_slide_raw.png`
Runtime: `assets/minigames/slide_race/penguin_slide.png`

Prompt:

> Create a behind-and-above downhill view along a broad powder-blue ice chute
> sweeping through a magical Antarctic cove. Frame the open steering lane with
> rounded snowbanks, paper-cut firs, lavender mountains, mint ice caves and
> turquoise sea, with a star-and-shell finish arch ahead. No characters,
> penguins, fish, rider, snowball, text, UI, Opera/castle motifs, logos,
> watermark, or 3D render.

### Sky Lagoon rainbow run

Source: `slide_race/rainbow_slide_raw.png`
Runtime: `assets/minigames/slide_race/rainbow_slide.png`

Prompt:

> Create a behind-and-above downhill view of a broad seven-band padded rainbow
> chute in the open Sky Lagoon, with cloud banks, floating flower meadows,
> lavender waterfalls and a shell-and-kite finish arch. Keep the steering lane
> clear. No characters, fish, penguins, rider, vehicle, text, UI, Opera,
> winter or kart motifs, logos, watermark, or 3D render.

### Racing baby penguin

Source: `slide_race/penguin_chroma.png`
Runtime: `assets/minigames/slide_race/penguin.png`

Prompt:

> Create one full-body baby penguin sliding belly-first toward the lower right,
> with flippers balancing, tiny orange feet, a mischievous smile, round
> navy-and-white body, ice-blue highlights and coral scarf. Use a crisp
> paper-cutout silhouette on a uniform bright-green chroma field. No scenery,
> fish, text, UI, logos, watermark, or 3D render.

The checkpoint shell, hoop, fish, snowball, ice-track and rainbow-track art
are new project-original SVG gameplay sprites. The three backgrounds remain
theme-local and are not shared with Opera, Kart, or one another.

## Fairy Pond overhead flight

Sources: `fairy/pond_dawn_raw.png`, `fairy/pond_twilight_raw.png`,
`fairy/boss_clearing_raw.png`
Runtime: `assets/minigames/fairy/pond_dawn.png`,
`assets/minigames/fairy/pond_twilight.png`,
`assets/minigames/fairy/boss_clearing.png`

Prompts:

> Create an exact top-down long vertical aqua pond corridor for a preschool
> Fairy Pond flight. Keep a broad quiet central lane; frame only the edges with
> giant lily pads, mint leaves, pond flowers, curled reeds, shell bridges and
> warm dawn reflections. No characters, bugs, monsters, boss, rings,
> projectiles, text, UI, Opera/castle/dungeon motifs, or 3D render.

> Create the same exact top-down Fairy Pond corridor at gentle twilight, with
> lavender lily pads, moonlit reeds, coral mushrooms, curled ferns, pearl
> pebbles and soft edge lights. Keep the center open. No characters, bugs,
> monsters, boss, rings, projectiles, text, UI, Opera/castle/dungeon motifs, or
> 3D render.

> Create an exact top-down circular moonlit Fairy Pond clearing with a broad
> empty center and a short water approach from the bottom. Frame it with lily
> pads, blossoms, reeds, pearl stones and six golden petal niches. No
> characters, bugs, boss flower, loose leaves, projectiles, text, UI,
> theater/coliseum motifs, or 3D render.

The first two plates were normalized to 512×1024 portrait textures and the
clearing to a 1024×1024 square texture.

### Pond creatures and flower growth

Sources: `fairy/creatures_sheet_raw.png`, `fairy/flower_sheet_raw.png`
Runtime: `assets/minigames/fairy/bug_*.png`,
`assets/minigames/fairy/hazard_*.png`,
`assets/minigames/fairy/boss_*.png`

Prompts:

> Create a 3-by-2 sheet of six exact-top-down shadow toys: jewel beetle, moth,
> firefly bug, ribbon jellyfish, blunt felt urchin and curled eel. Give each a
> friendly mischievous face, painted-paper texture and clear silhouette on a
> uniform green chroma field. No scenery, frames, text, UI or 3D render.

> Create a 3-by-2 sheet of six exact-top-down growth assets for one Fairy
> Flower: cracked seed, mint sprout, closed bud, opening bud, full flower and
> one orbiting shield leaf. Keep one coherent coral/lavender/mint progression
> on a uniform green chroma field. No scenery, characters, frames, text, UI or
> 3D render.

Both sheets were locally alpha-extracted, split by cell, and normalized to
transparent 1024×1024 PNGs. Flower ring, firefly glow, reticle, shadow orb and
wand bolt are new project-original SVG gameplay sprites.

## Crystal Dungeon and Ember puzzle forge

Sources: `dungeon/crystal_arena_raw.png`,
`dungeon/ember_arena_raw.png`
Runtime: `assets/minigames/dungeon/crystal/arena.png`,
`assets/minigames/dungeon/ember/arena.png`

Prompts:

> Create an exact-top-down square crystal puzzle arena with an open octagonal
> aqua/lavender pearl-stone floor, crystal alcoves, shell lamps, blue banners,
> an empty doorway niche and subtle live-prop sockets. Bright magical training
> hall, not a prison, toy castle, Opera stage or Ember recolor. No characters,
> props, projectiles, text, UI or 3D render.

> Create an exact-top-down square Ember Fortress puzzle arena with an open
> charcoal-purple basalt mosaic, soft coral/magenta glow seams, lantern
> alcoves, safe glass ember gardens, a rounded empty doorway and live-prop
> sockets. Warm volcanic observatory, not a crystal recolor or real fire
> hazard. No characters, props, projectiles, text, UI or 3D render.

Both were normalized to opaque 1024×1024 floor plates.

### Dungeon actors

Sources: `dungeon/actors_sheet_raw.png`,
`dungeon/boss_parts_sheet_raw.png`
Runtime: `assets/minigames/dungeon/crystal/imp.png`,
`assets/minigames/dungeon/ember/imp.png`,
`assets/minigames/dungeon/{crystal,ember}/boss_{shell,head}.png`

Prompts:

> Create a 2-by-2 sheet with a crystal plush imp, friendly crystal
> dragon-turtle, distinct Ember felt imp, and friendly Ember dragon-turtle.
> Use three-quarter-overhead painted-paper/felt style, safe rounded silhouettes
> and uniform green chroma. No scenery, weapons, text, UI or 3D render.

> Create a 2-by-2 modular sheet with crystal shell-only, matching crystal
> head/front-paws-only, Ember shell-only and matching Ember head/front-paws
> only. Make the parts layer cleanly in an overhead arena. Uniform green
> chroma; no scenery, weapons, text, UI or 3D render.

The sheets were locally alpha-extracted and split into transparent 1024×1024
runtime sprites. All doors, pedestals, baskets, lanterns, statues, elemental
shots, pointer, completion spark, pearl target, and the 4×3 semantic pictogram
atlas are new project-original SVG sprites. Crystal and Ember architecture
remain separate; only gameplay-semantic icons are shared.

## Stuffie nursery gym

Sources: `stuffie/arena_raw.png`, `stuffie/characters_sheet_raw.png`
Runtime: `assets/minigames/stuffie/arena.png`,
`assets/minigames/stuffie/{imp,eagle,mewsha,lamma}.png`

Prompts:

> Create an exact-top-down square round quilted nursery play-battle arena.
> Build a broad cream stitched center, coral/lavender/mint/yellow quilt lanes,
> pillow bleachers, four cozy friendship niches and toy baskets at the outer
> corners. Keep the center empty for live actors. Preschool storybook fabric
> texture, navy ink outline, warm and safe. No characters, enemies, text, UI,
> dungeon, Opera, crystal, lava, castle, or 3D render.

> Create a clean 2-by-2 character sheet on one uniform bright green chroma
> background: a unique coral/lavender felt nursery-gym mischief imp; Baby
> Eagle as a cream-and-golden stitched plush; Mewsha as a pink/lavender
> stitched plush cat; Lamb-a' as a cream-and-pink stitched plush lamb. One
> complete centered character per quadrant, consistent three-quarter-overhead
> storybook cutout, navy ink outline, no scenery, text, UI, shadows crossing
> cells, or 3D render.

The arena was normalized to an opaque 1024×1024 plate. The character sheet
was locally alpha-extracted, split by quadrant, and normalized to four
transparent 1024×1024 cutouts. The gift, castle room, shelves, den posts,
pointer, friendship icons, claw/peck flashes, and enemy orb are new
project-original SVG sprites for this family.

## Critter collection

Sources: `critters/{fish,insect,bird}_sheet_raw.png`
Runtime: `assets/minigames/critters/*.png`

Prompts:

> Create a clean 3-by-2 chroma sprite sheet of six distinct preschool
> storybook fish: Coral Clownfish, Pearl Seahorse, Rainbow Angelfish, Sky Koi,
> Cloud Minnow, and Frostfin. Give every animal a crisp friendly silhouette,
> painted-paper texture and navy-purple contour. No scenery, labels, frames,
> photorealism, 3D models, or 3D render.

> Create the matching 3-by-2 chroma sheet for Coral Ladybug, Blue Dragonfly,
> Moon Moth, Honeybee, Snow Beetle, and Crystal Butterfly. Use overhead or
> three-quarter-overhead cutout poses. No scenery, labels, frames,
> photorealism, 3D models, or 3D render.

> Create the matching 3-by-2 chroma sheet for Lagoon Bluebird, Ruby
> Hummingbird, River Kingfisher, Cloud Puffin, Snowy Owl, and Aurora Tern.
> Keep every whole bird inside its cell. No scenery, branches, labels, frames,
> photorealism, 3D models, or 3D render.

The three sheets were locally alpha-extracted, split by cell, and normalized
to eighteen transparent 1024×1024 sprites. The catch net and
discovered/caught markers are new project-original SVG sprites.

## Kart races

Sources: `kart/ocean_background_raw.png`,
`kart/rainbow_background_raw.png`, `kart/vehicles_sheet_raw.png`,
`kart/hazards_sheet_raw.png`, and `kart/pickups_sheet_raw.png`
Runtime: `assets/minigames/kart/ocean_background.png`,
`assets/minigames/kart/rainbow_background.png`,
`assets/minigames/kart/{moto,kart,truck}.png`,
`assets/minigames/kart/hazard_*.png`, and
`assets/minigames/kart/pickup_*.png`

Prompts:

> Create a wide preschool storybook Ocean Kart background with a broad aqua
> reef roadway, coral-and-shell guard edges, rounded kelp hills, friendly fish
> silhouettes, pearl markers and a clear finish horizon. Leave the road center
> open for live vehicles and the upper corners quiet for HUD. Outdoor reef
> race, not Opera, Butterfly World or dungeon. No characters, vehicles, UI,
> photorealism, 3D models, or 3D render.

> Create a separate Butterfly World Rainbow Kart background with a broad
> luminous rainbow bridge over clouds, crystal-butterfly landmarks, celestial
> meadow islands, ribbon winds and a crystal destination. Not Ocean Kart,
> Fairy Pond or Opera. No characters, vehicles, UI, photorealism, 3D models,
> or 3D render.

> Create a 3-by-1 chroma sprite sheet of a rear-view Zoom Cycle, Rainbow
> Go-Kart and friendly Monster Truck. Painted-paper toy texture, navy-purple
> contour, no drivers, scenery, labels, logos, 3D models, or 3D render.

> Create a clean 4-by-2 chroma sprite sheet of eight readable kart hazards:
> crab, kelp patch, bubbly geyser, grumpy comet, soft spike pendulum, water
> whirl, jelly bounce dome, and sleepy cloud. One complete centered object per
> cell, thick navy-purple outline, no scenery, words, UI, 3D models, or 3D
> render.

> Create a clean 4-by-1 chroma sprite sheet of four friendly race pickups:
> shell turbo, bubble zip, golden star, and rainbow full-power star. One
> complete centered icon per cell, painted-paper storybook texture and strong
> silhouette. No scenery, labels, UI, 3D models, or 3D render.

Both race plates were normalized to opaque 2048×1024 textures. The vehicle
and gameplay sheets were locally alpha-extracted, split, and normalized to
transparent 1024×1024 sprites. The two finish-gate identities, boost chevrons,
and shared race landmark cards are new project-original SVG sprites.

## Butterfly Galaxy

Sources: `galaxy/background_raw.png`, `galaxy/objects_sheet_raw.png`
Runtime: `assets/minigames/galaxy/*.png`

Prompts:

> Create a wide Butterfly Galaxy storybook plate: a luminous flower-meadow
> planet suspended in lavender space, crystal palace silhouette, gentle orbit
> trails, oversized flowers and quiet HUD-safe corners. Keep the center open
> for live butterfly play. This is a celestial nursery-garden, not Opera,
> Ember, Kart, or a generic nebula. No characters, text, UI, 3D models, or 3D
> render.

> Create a clean 4-by-4 chroma sheet containing seven distinct baby butterfly
> cutouts, their grand butterfly, palace gate, fruit tray, beetle, ladybug,
> bounce flower, crystal, home ring, and star bell. One complete centered
> object per cell with a crisp navy-purple contour. No scenery, labels, UI,
> 3D models, or 3D render.

The wide plate was normalized to opaque 2048×1024. The object sheet was
locally alpha-extracted and split into sixteen transparent 1024×1024 runtime
sprites. These butterfly babies are newly generated Galaxy actors; they are
not Faron's protected baby-doll files.

## Ember Fortress

Sources: `ember/background_raw.png`, `ember/objects_sheet_raw.png`
Runtime: `assets/minigames/ember/*.png`

Prompts:

> Create a wide Ember Fortress overworld plate as a warm obsidian-and-coral
> storybook kingdom under an ash moon: broad safe causeway, distant rounded
> citadel, five lantern routes, friendly lava light, and quiet HUD corners.
> Keep it magical rather than frightening and distinct from the crystal
> dungeon, Opera, Kart, and Butterfly Galaxy. No characters, text, UI, 3D
> models, or 3D render.

> Create a clean 4-by-4 chroma sheet containing five distinct route lanterns,
> the Great Gate, friendly Ember King, home ring, three rounded crags, two
> crystals, a geyser, beacon, and ash moon. One complete centered object per
> cell with painted-paper texture and navy-purple contour. No scenery, labels,
> UI, 3D models, or 3D render.

The wide plate was normalized to opaque 2048×1024. The object sheet was
locally alpha-extracted and split into sixteen transparent 1024×1024 runtime
sprites.

## Pearl Opera House

Sources: `opera/lobby_raw.png`, `opera/careers_sheet_raw.png`,
`opera/racecar_driver_raw.png`, and `opera/bosses_sheet_raw.png`
Runtime: `assets/minigames/opera/lobby.png`,
`assets/minigames/opera/careers/*.png`, and
`assets/minigames/opera/bosses/*.png`

Prompts:

> Create a wide Pearl Opera House lobby plate: coral-and-lavender
> proscenium architecture, shell chandeliers, balcony doors, plush carpet and
> a clear central promenade. It is a theatrical selection lobby, not a
> template for other minigames. No characters, text, UI, 3D models, or 3D
> render.

> Create a clean 4-by-3 contact sheet of twelve distinct career stages:
> pastry chef, farmer, painter, ballerina, magician, detective, animal doctor,
> boxer, astronaut, candy maker, plumber, and pop star. Each cell must retain
> its career-specific props while sharing only Pearl Opera House stage
> language. No characters, labels, UI, 3D models, or 3D render.

> Create one complete racecar-driver career stage matching the contact
> sheet's Pearl Opera House language: toy grand-prix circuit scenery, pit
> pennants, shell trophy and open center for live play. No characters, text,
> UI, 3D models, or 3D render.

> Create three separate wide Pearl Opera boss-stage plates: Curtain Dragon,
> Shadow Phantom, and Midnight Maestro. Keep each boss identity unmistakable
> while preserving the theatre's shared proscenium vocabulary. No live
> characters, text, UI, 3D models, or 3D render.

The lobby and boss plates were normalized to opaque runtime images. The
career contact sheet was split into twelve 1024×1024 stages; the Racecar
Driver stage was generated separately to complete the playable twelve-career
roster without reusing another game's race art.

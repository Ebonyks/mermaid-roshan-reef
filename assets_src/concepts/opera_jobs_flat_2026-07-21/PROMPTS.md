# Opera House job flat-prototype prompt record

Generation mode: OpenAI built-in image generation with local project images as
visual references. Each accepted image used one built-in generation call. Raw
outputs remain in the external Codex generated-image cache; accepted project
copies were normalized to 1024 x 1024. The accepted 4 x 4 cells are exported
as deterministic 1024 x 1024 individual modeling references by
`tools/slice_opera_job_prototypes.py`. The individual exports preserve the
accepted sheet art; they are not independent generative reinterpretations.

## Binding reference set

- Roshan identity: `assets/characters/roshan_sprite.png`.
- Outfit finish anchor after the pilot:
  `pastry_chef_outfit_sheet_2026-07-21.png`.
- Opera House finish and mechanic anchors:
  `assets_src/concepts/opera_house_flat/opera_house_master_scene_key_2026-07-21.png`,
  `opera_house_stage_scene_key_2026-07-21.png`, and the relevant floor act-prop
  sheet.
- The backpack in the Roshan identity image was explicitly excluded from every
  outfit prompt; it and its printed imagery are not part of these designs.

## Exact shared prompt contracts

Every outfit call bound the following requirements, with the job-specific
sixteen-cell list below appended:

> Create a production-quality FLAT 2D CONCEPT ART SHEET, not a 3D render.
> Strict square 4-by-4 grid, exactly sixteen equal cells with thin dark navy
> dividers and a deep navy presentation background. Every concept is centered,
> fully visible, uncropped, and separated by generous margin. Preserve Roshan's
> joyful young face, warm brown eyes, long wavy brown hair with a vivid rainbow
> streak, continuous rainbow-scaled mermaid tail, and split tail fin. Omit the
> backpack and everything printed on it. Roshan remains a mermaid in every
> pose: no human legs, shoes, or boots. Match the accepted Opera House finish:
> polished storybook cel illustration, rounded toy-like modelable forms,
> confident navy-purple outlines, aqua/lavender shadows, coral, teal, cream,
> and plum with restrained brushed gold, pearl, and shell accents. Keep hands,
> anatomy, tools, and tail attachments clean and child-readable at phone size.
> No words, letters, numbers, logos, watermarks, generic star icons, bosses,
> photorealism, Blender rendering, copied franchise designs, or duplicate
> filler.

Every gameplay call used this binding contract:

> Create a production-quality FLAT 2D GAME ASSET CONCEPT SHEET, not a 3D
> render. Strict square 4-by-4 grid, exactly sixteen equal cells with thin dark
> navy dividers on a deep navy field. Every asset is isolated, centered,
> uncropped, and immediately readable by a non-reader using one finger. Use
> rounded toy-diorama storybook cel forms, navy-purple outlines, aqua/lavender
> shadows, coral/teal/cream/plum, and restrained gold/pearl/shell accents. Show
> mechanically distinct props and states, including gentle retry rather than a
> punitive fail state. No Roshan, people, words, letters, numbers, logos,
> watermarks, generic stars, bosses, photorealism, Blender rendering, scary
> imagery, or repeated filler.

Every stage/state call used this binding contract:

> Create a production-quality FLAT 2D ENVIRONMENT AND STATE CONCEPT SHEET, not
> a 3D render. Strict square 4-by-4 grid, exactly sixteen equal cells with dark
> navy dividers/background. Build a child-friendly early-20th-century live-show
> set inside the accepted Opera House: rounded Mobile-modelable storybook cel
> forms, navy-purple outlines, aqua/lavender shadows, coral/teal/cream/plum,
> and restrained brushed gold, pearls, and shells. Communicate guidance,
> progress, retry, and completion nonverbally with strong silhouettes, matching
> colors/shapes, glow, paths, arrows, bubbles, and broad effects. No Roshan,
> people, words, letters, numbers, logos, watermarks, generic star mascots,
> bosses, photorealism, Blender rendering, fragile micro-detail, or repeated
> filler.

## Accepted job-specific prompt sets and raw provenance

The lists below are the exact requested cell order, left-to-right and
top-to-bottom, appended to the shared contracts.

| Job / sheet | Exact job-specific content | Raw generation |
| --- | --- | --- |
| Pastry Chef / outfit | Cream puff toque with pearl-shell clasp; coral double-breasted jacket; teal piping; plum neckerchief; scalloped tail apron; whisk, piping bag, shell mitts; crest, swatches, idle/action silhouettes, cake bow, wardrobe display. | `exec-de5fe4ce-45d6-4490-bc72-33516f727c1d.png` |
| Pastry Chef / gameplay | Vanilla, coral, plum cake layers; layer-order board; empty/calm/stirring bowls; whisk; closed/open oven; cherry, cream, chocolate toppings; targets; finished cake; piping ribbon. | `exec-0008f2b5-3c68-44f4-a65a-7f5b88098758.png` |
| Pastry Chef / stage | Pastry proscenium; counter; ingredient shelf; cake cart; topping pedestals; recipe stand; oven alcove; reveal table; frosting pointer; stir/frosting/placement effects; retry; oven success; cake reveal; curtain call. | `exec-0367afc3-006a-4a03-88c0-e3192f2b9e2c.png` |
| Detective / outfit | Plum capelet; teal vest; cream blouse; coral bow; rounded shell detective cap; magnifier, clue satchel, pointer lantern; crest, swatches, silhouettes, tiara reveal, wardrobe display. | `exec-51f4a647-72d1-4c6c-809b-b51d6b2c6b30.png` |
| Detective / gameplay | Six structurally distinct mystery containers; paw, feather, ribbon clues; magnifier; fish and sock decoys; closed/open chest; tiara; three-clue medallion. | `exec-c55c8503-ba2a-4d36-851c-c21eb8cd9f42.png` |
| Detective / stage | Moonlit prop-library set; archive shelf; three- and six-box displays; search pool; pointer; clue glows; empty/complete case board; wiggle and fish surprise; chest pedestal; retry; tiara reveal; completed case; curtain call. | `exec-19db0305-4a54-4820-a50a-c3a4899ca100.png` |
| Ballerina / outfit | Pearl tiara; coral-cream bodice; teal ribbons; layered shell-petal tail tutu; fin and wrist ribbons; music-box accessory; crest, swatches, silhouettes, recital bow, wardrobe display. | `exec-ed687a4f-d6e9-4ee9-b4a9-733b535b976c.png` |
| Ballerina / gameplay | Coral shell, teal wave, plum ribbon, cream pearl tiles; four matching demo glows; pressed ripple; four-tile arrangement; example sequence; barre; music box; mirror ball; twirl ribbon; completion bloom. | `exec-184dbcfc-d7ab-4c57-ac7c-e9ef368971f0.png` |
| Ballerina / stage | Recital proscenium; dance floor; barre; mirrors; mirror-ball rig; coral/teal wing curtains; spotlight; watch/repeat/correct/retry states; twirl; floor bloom; recital reveal; bouquet curtain call. | `exec-cf7e40cd-922d-4dcc-89f1-a813e6dd2ecd.png` |
| Candy Maker / outfit | Teal parade jacket with coral lapels; cream sleeves; plum sash; wrapped-candy cap; press mitts; tongs and scoop; crest, swatches, silhouettes, candy-tray bow, wardrobe display. | `exec-4aaf43ea-f08a-440e-9ce6-d8876c0ac076.png` |
| Candy Maker / gameplay | Press idle/open/squish; red-green-red gauge; approach/center slider; seven distinct candies; four molds; scoop/tongs; wrapped reward. | `exec-6c4af66e-674a-4faa-964e-6e7f6bd7f2a3.png` |
| Candy Maker / stage | Workshop; conveyor; hopper; press platform; wrapping station; seven-slot shelf; parade cart and arch; timing pointer; squish/retry/wrapping effects; partial/full shelf; parade tableau; curtain call. | `exec-efb00942-c13d-484e-943b-3a0002fefeea.png` |
| Doctor / outfit | Cream clinic coat; coral trim; teal blouse; plum tail band; headband; stethoscope, thermometer, bandage pouch; shell-heart crest; silhouettes and interaction only with the coral five-armed starfish plush. | `exec-65018d58-1192-4e73-914a-c22a51ee25f9.png` |
| Doctor / gameplay | Coral five-armed starfish worried/calm/happy; stethoscope and listening pad; cool/warm thermometer; kiss puff; bandage roll/sheet/wrap; tool tray; heartbeat; pointer; care medallion; recovered patient. | `exec-fa55e228-c303-4b50-a739-eef9ee9b8d87.png` |
| Doctor / stage | Toy clinic; exam platform; trolley; privacy curtain; pictogram cabinet; basin; starfish waiting bench; four-step board; pointer; listen/warmth/kiss/bandage states; before/after; recovered starfish tableau; curtain call. | `exec-e1556c6c-e99b-4474-9df5-041165293489.png` |
| Farmer / outfit | Woven shell hat; teal vest; cream blouse; large coral-plum checked kerchief; scalloped tail tool apron; produce basket and scoop; crest, swatches, silhouettes, piggy picnic, wardrobe display. | `exec-30f7b698-2591-4fa4-bb22-505826e71d9c.png` |
| Farmer / gameplay | Piggy trot A/B, hop, munch, fed; carrot, apple, corn, berries, pumpkin; basket; toss arc; mud splash; hay; hungry/happy target; happy group. | `exec-1a6b99fe-b78d-4cdb-bdbe-6dd56fe5632a.png` |
| Farmer / stage | Meadow proscenium; distant/orchard/flower parallax; barn; fence; picnic; puddle; hay; toss pointer; approach/in-flight/fed states; picnic group; piggy finale; sunset curtain call. | `exec-35ba82dc-ac10-4703-af28-207b53a9e361.png` |
| Boxer / outfit | Navy training vest; cream top; coral trim; plum waistband; teal headband; soft coral gloves; focus mitt; high shell belt; crest, swatches, guard/punch silhouettes, belt victory, wardrobe display. | `exec-72801104-d960-4740-91f9-d854ae3d1830.png` |
| Boxer / gameplay | Gloves; focus mitt; padded post/ropes; ring corner; bell; three round lamps; soft training bag; belt; friendly imp peek/bop/bow; bubble-puff impact; recoil; glove medallion; towel/flask; belt pedestal. | `exec-ff2c7fac-194a-4c94-8628-9b24cd00207a.png` |
| Boxer / stage | Toy ring set; ring platform; coral/teal stools; bell; bag; pictogram pennants; round lights; glove pointer; peek/bop/round/retry states; belt reward; podium; curtain call. | `exec-798aac00-28e6-4dfd-b225-b6e006b13a88.png` |
| Magician / outfit | Plum tailcoat/capelet with teal lining; cream blouse; coral cummerbund; soft top hat; pearl bow; pearl-tip wand; trick satchel; crest, swatches, silhouettes, bunny-fish reveal, wardrobe display. | `exec-3ee9f3e7-8e39-49d3-a662-4be8a8f46347.png` |
| Magician / gameplay | Three banded hats; open hat; pink rabbit-eared finned bunny-fish swim/peek/reveal; wand; swap/crossed/feint trails; bubble decoy; selector; start/shuffle lineups; reveal. | `exec-5d675c8d-acc1-4434-8ba4-676b3bb67996.png` |
| Magician / stage | Magic proscenium; table; cabinet; three-hat rail; mirror; curtains; spotlight; watch/swap/select/decoy/reveal/retry/complete states; final bunny-fish reveal; curtain call. | `exec-e52e86fd-6ff1-4dbe-883a-9b576a84e6ed.png` |
| Painter / outfit | Coral beret; teal smock; cream sleeves; plum sash; drop-cloth tail apron; palette cuff; broad brush; three-pot carrier; sunrise crest; swatches, silhouettes, canvas bow, wardrobe display. | `exec-89ed8a11-75e9-4bb4-8ee5-a2421aa8b86e.png` |
| Painter / gameplay | Coral/cream/plum pots and loaded brushes; blank, plum, plum-coral, finished sunrise canvases; plum-coral-cream order board; palette; rinse cup; swipe; splat set; framed sunrise. | `exec-35bdb4e4-3fb6-47ca-90f7-374862e24167.png` |
| Painter / stage | Proscenium; easel platform; pots and board locked to plum-coral-cream; cart; cloth; gallery wall; rinse station; pointer; carry/swipe/retry/splat states; before/after; gallery reveal; curtain call. | `exec-13673417-cbd9-4a18-bbad-7fdd864ed3cb.png` |
| Astronaut Engineer / outfit | Original cream/teal mermaid bubble suit; coral shoulders; open bubble helmet ring; plum tool belt; visible tail guard; wrench, bubble tank, communicator; rocket/pipe crest; swatches, silhouettes, launch pose, wardrobe display. | `exec-c4eb44a9-65de-4f9c-a502-ec5a4473d785.png` |
| Astronaut Engineer / gameplay | Bubble tank; rocket side/front; straight/elbow/ring pipes; three matching ghost slots; wrong hover; three fitted states; valve; valve bubbles; bubble-only launch. | `exec-c83d3cf6-af33-47e9-9724-ab8badf44b53.png` |
| Astronaut Engineer / stage | Launch proscenium; pad; gantry; workbench; three-shape pipe wall; tank and valve pedestals; pressure lamps; match/return/complete/valve/prelaunch/launch/reveal states; curtain call. | `exec-8c64e5bd-9f3a-4625-8f58-e8d5cb246f56.png` |
| Racecar Driver / outfit | Coral/navy jacket; cream layer; plum high tail belt; open shell helmet; raised pearl goggles; gloves; steering wheel; mermaid-tail-safe Opera kart pose; crest, swatches, silhouettes, trophy victory, wardrobe display. | `exec-8e8a19ab-f379-4a74-a8d2-38ddaf93f10d.png` |
| Racecar Driver / gameplay | Opera kart front/side/rear with open tail channel and bubble exhaust; steering wheel; turbo button; inactive/active strips; finish/course flags; trophy; pit kit; barrier; turbo trail; steering arrow; finish ribbon; pedestal. | `exec-6a407ac5-ec3b-4c0e-8d76-9834bb356d92.png` |
| Racecar Driver / stage | Race proscenium; start arch; straight/curve modules; barrier; pit cart; grandstand; progress lamps; steering/strip/turbo/finish/lap states; trophy podium; curtain call. | `exec-b568469a-e7b4-40ac-bb44-714232e60b53.png` |
| Pop Star / outfit | Iridescent coral jacket; plum lapels; teal lining; cream top; high tail sash; translucent cape ribbons; winged shell glasses; pearl microphone and stand; cuffs/earpiece; crest, swatches, silhouettes, finale bow, wardrobe display. | `exec-df1b67bc-fa99-4a60-8a02-be81190169c8.png` |
| Pop Star / gameplay | Microphone idle/active; stand; coral left, teal right, plum up, cream down arrow tiles; four-step sequence; pressed ripple; rainbow ribbon; beat pulse; speaker; monitor; tambourine; completion bloom; finale. | `exec-798b9a4d-310b-4f83-bf7d-d8fe66c76337.png` |
| Pop Star / stage | Concert proscenium; pearl light arch; speakers; catwalk; rainbow panels; four-arrow floor; mic pedestal; glow-stick rail; pointer; arrow lane; press/retry/rainbow/complete states; encore reveal; curtain call. | `exec-b52191a3-37e3-46c4-b431-8e96af3ffda0.png` |

## Rejected generations and exact corrections

- Doctor outfit `exec-ce9d683d-501a-4986-b87b-e062fbec590f.png` and Doctor
  stage `exec-d92eee36-2ca9-4cca-97c8-f52cf0cc84e0.png` were rejected because
  the interaction patient drifted to an axolotl and teddy bears. Correction:

  > Every patient in every interaction and state must be the same simple coral
  > FIVE-ARMED STARFISH PLUSH shown in the accepted gameplay reference. Never
  > use a bear, rabbit, axolotl, ordinary fish, or four-limbed creature.

- Painter stage `exec-8972a69f-27d5-4577-af1d-14a351963aba.png` was rejected
  because the color board contradicted the shipped order. Correction:

  > Every color-order display must show exactly PLUM PURPLE FIRST, CORAL PINK
  > SECOND, CREAM GOLD THIRD, left-to-right, matching the accepted gameplay
  > reference. Do not show any other order.

Rejected sources remain outside the repository in the generation provenance
cache. Bosses were excluded from generation by scope: Curtain Dragon, Shadow
Phantom, and Midnight Maestro.

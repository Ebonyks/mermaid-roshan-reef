# FLOOR 1 — LAGOON LIGHTS STAGE — complete story scripts
### Chef · Detective · Ballerina · Candymaker · Curtain Dragon
Written against the shipped code. Every landmark named below is a real `OperaStagePaths.PATHS` entry; every quoted instruction is the shipped `PHASES` `voice`; every win_line is the shipped `ACTS` `win_line`, unchanged.

---

## 0. VERIFIED RUNTIME FACTS THAT SHAPED THESE SCRIPTS

Read before writing any line for any floor — three of these change what a writer is allowed to say.

**(a) Which landmark Roshan is actually standing at.** `_assign_stations()` (`opera_career_world_2d.gd:521-532`) skips every `mode == "bop"` phase and assigns the remaining phases to `stations[]` **in index order**. There is no per-phase station key. Floor 1 therefore resolves to:

| Career | station 1 | station 2 | station 3 | station 4 (finale) | station 5 (finale) |
|---|---|---|---|---|---|
| chef | POUR @ `mixing_bowl` | STIR @ `hearth_oven` | BAKE @ `cake_tower` | PIPE @ `macaron_cart` | TOP @ `grand_cake_stage` |
| detective | LENS @ `evidence_shelves` | TRAIL @ `pedestal_display` | SEARCH @ `magnifier_tower` | MATCH @ `mirror_gallery` | NAME @ `treasure_dais` |
| ballerina | WATCH @ `curtain_alcove` | STEPS @ `wave_tuffets` | RIBBON @ `shell_bandstand` | DUET @ `trifold_mirror` | TWIRL @ `rose_finale_stage` |
| candymaker | SYRUP @ `gumball_vat` | SORT @ `taffy_press` | WRAP @ `candy_bag_cottage` | PARADE @ `sweet_display_shop` | SHARE @ `candy_cart` |

**(b) BLOCKING FOR ALL FINALE LINES — the painting is replaced at the steal.** `_show_phase()` computes `stage_from = steal_index` (phase 4 on all four shows) and calls `backdrop_node.set_stage(true)` (`:664-668`). `set_stage` swaps the whole backdrop to the `stage_<career>_c*r*.png` tile set (`opera_world_backdrop_2d.gd:78-101`). **Roshan still glides to stations 4 and 5, but those landmarks are no longer on screen.** Consequence, and I have obeyed it throughout: **FINALE_OPEN and FINALE_MID lines must name the stage — curtain, footlights, crowd — never a world landmark.** The two exceptions where the world station *is* a stage (`grand_cake_stage`, `rose_finale_stage`) are still written stage-generically so they are safe either way.

**(c) `_speaker_key` has no dragon branch — the Curtain Dragon currently speaks in Roshan's voice.** `audio_director.gd:95-113`: `"Curtain Dragon"` matches nothing and falls through to `return "roshan"` (:113). This is the identical defect the Bible §8 found for the Ember King. Fix, above the `"imp"` branch:
```gdscript
if "dragon" in w: return "dragon"
```

**(d) There is no helper slot on stage.** `_build_world()` (`:376-384`) creates exactly two actors: `player_actor` and `rival_actor` (= `rival_<career>.png`; nursery alone swaps it to `faron_nursery.png`). On floor 1 the rival imp must stay — it is the finale duet partner — so **Kareem, Huluu, Rosalina and Sparkle cannot appear until a third actor exists.** Ask: a `helper_actor` TextureRect loading `assets/opera/worlds/actors/helper_<career>.png`, hidden when the file is missing, placed by `_place_on_stage()` at the current station. ~12 lines, mirrors the existing `_actor()` + `_place_on_stage()` calls, zero risk. Until it lands, all four helpers are voice-only and the scripts still play.

**(e) Good news — per-phase speakers already ship.** `_show_phase()` passes `String(phase.get("speaker", "Roshan"))` into `m.show_msg` (`:727`). The key is used only by nursery today. Adding `"speaker": "Kareem"` to a chef phase routes that phase's instruction line through Kareem's voice with **zero new plumbing**.

**(f) Minor, written around, optional fix.** Chef's BAKE lands at `cake_tower`, not `hearth_oven` — an artefact of (a). I have written the beat so the tower is where the *baked layer goes*, which is true on screen and needs no code. If you ever want it exact, honour an optional `"station": "<id>"` key inside `_assign_stations` (~4 lines).

---

# ACT 1 · PASTRY CHEF — "The Castle Bake-Off"
`ACTS[0]` · costume `chef` · goal prop `goal_chef.png` · steal at phase 4 · finale from phase 5

**LOGLINE** — Roshan walks into the reef's cake shop on her own birthday, tells the shopkeeper she does *not* want to buy a cake, and bakes her own next to his — which is the one the imps decide is worth stealing.

**HELPER — Kareem (`shop` → `bm_george`, already routed at `audio_director.gd:111`).**
What he wants: to **give** her a cake. He has already boxed one with her name piped on it.
The clever hook: **he is the reef's cake seller, and the birthday girl refuses his cake to his face — kindly.** He is not demoted by that; he is promoted. He becomes her ingredient supplier and her taste judge, and his own boxed cake sits on the `macaron_cart` for the entire act as a silent, untouched *"you could have just taken this."* The shipped `cake_tower` — "gold etagere tower displaying yellow, pink, and purple cakes" — is **his shop stock**, so when her layer goes up onto it, it is standing beside professional work. The button: **the imp captain steals hers, not his**, because hers is the one that was *made*. Kareem's last line asks to buy the recipe. Chapter 2's entire thesis (offered → refused → joy of making) is dramatised in act 1 with one shopkeeper and one cardboard box.

**BEAT SCRIPT** — 9 lines
| # | Line | Tag |
|---|---|---|
| 1 | "One more thing for my party! Tonight we bake my birthday cake!" | `[Roshan \| ACT_OPEN]` |
| 2 | "But I already boxed you one, Roshan! With your name in icing!" | `[Kareem \| ACT_OPEN]` |
| 3 | "Teehee! Cake smell! We want to hold the sparkly spoons too!" | `[Imp Captain \| SCUFFLE]` |
| 4 | "No thank you, Kareem — mine goes in the big pink bowl!" | `[Roshan \| STATION_1 — mixing_bowl]` |
| 5 | "Ding! Straight from the golden oven onto the cake tower — beside mine!" | `[Kareem \| STATION_3 — hearth_oven → cake_tower]` |
| 6 | "Teehee! Is that for the PARTY? Let me hold it! Are we invited?" | `[Imp Captain \| STEAL]` |
| 7 | "Places, please! The Pearl Opera presents… Roshan icing her own birthday cake!" | `[Maestro \| FINALE_OPEN]` |
| 8 | "Imps! Grab a sprinkle each — everybody tops the birthday cake!" | `[Roshan \| FINALE_MID]` |
| 9 | "Birthday cake — on the table!" | `[Roshan \| CURTAIN_CALL]` |

*Optional button (strongly recommended, 1 clip):* "Roshan — will you sell ME that recipe?" `[Kareem | CURTAIN_CALL]` — the shop's surrender, and the funniest possible proof that made beats bought.

**Instruction layer, unchanged and quoted where it works.** STATION_2 (STIR) is **deliberately silent** — the audit's "never talk over the doing" rule; a circle gesture wants music, not a voice. Beat 3 sets up the shipped `"Mischief imps grabbed the spoons! Tap each imp to shoo them off!"` so the imps' *want* arrives before the imps' *nuisance*. Beat 9 runs immediately before the shipped win_line `"Roshan's celebration cake wins the Castle Bake-Off!"`, spoken via the win_vo slot.

**BIRTHDAY LINK** — line 1: *"One more thing for my party! Tonight we bake my birthday cake!"*

**ESCALATION — the imps want your HANDS ON IT.** F1 posture at its purest: they take **tools, never the food** (the shipped scuffle is literally "grabbed the spoons"). Nothing is consumed, nothing is hidden, nothing is imitated. This is the floor's baseline against which the other three read as escalations, and the steal is the first moment in the whole chapter that the Captain touches a *finished* party piece.

**ASSET WISHES**
- **NEW `actors/helper_chef.png`** — Kareem in shop apron and paper hat, arms folded, behind the `mixing_bowl`. *Why:* he must read as a person standing in the world, not a menu portrait. (Audit already names this as `kareem_chef.png`; use the `helper_<career>` convention so the loader stays one line.)
- **NEW `props/prop_boxed_shop_cake.png`** — a ribboned bakery box, lid open, "ROSHAN" piped on the cake inside. Parked on the `macaron_cart` from ACT_OPEN to curtain call, never interacted with. *Why:* it is the thesis, stated in an object, with no dialogue. A non-reader sees the easy cake sitting there all show and sees her choose the hard one.
- **REUSE** `props/goal_chef.png`, `actors/roshan_chef.png`, `actors/rival_chef*.png` (12 poses, all shipped), `backdrops/world_chef*.png`, `backdrops/stage_chef*.png`.

---

# ACT 2 · DETECTIVE — "The Two-Detective Mystery"
`ACTS[1]` · costume `detective` · goal prop `goal_detective.png` · steal at phase 4

**LOGLINE** — Princess Huluu lends Roshan her own tiara to wear as a birthday crown, it vanishes the instant it leaves her head, and the only witness solves the case by remembering her own fourth birthday.

**HELPER — Princess Huluu (`huluu` → `bf_emma`, shipped).**
What she wants: to give Roshan something on her birthday that is not new — something that has been to birthdays before.
The clever hook: **she is the victim, the client and the gift-giver in one breath, and she detects by remembering being four.** She does not know facts; she knows *where a small girl hides a crown*, because she was one. Every clue she offers is a memory of her own party — "I hid mine in the lockbox shelves when I was four", "mine turned up under the big magnifying glass" — so the helper's method is *being little*, which is the exact expertise the player has. The shipped final station seals it: `treasure_dais`, "giant open treasure chest with pearl tiara under the domed pavilion" — the crown was in the treasure chest the whole time, where a four-year-old would have put it. Huluu then crowns her.

**BEAT SCRIPT** — 9 lines
| # | Line | Tag |
|---|---|---|
| 1 | "One more thing for my party! Tonight we find my birthday crown!" | `[Roshan \| ACT_OPEN]` |
| 2 | "It is my own tiara, Roshan. Yours for the whole birthday." | `[Princess Huluu \| ACT_OPEN]` |
| 3 | "Teehee! Sparkly, sparkly! We only wanted to try it on!" | `[Imp Captain \| SCUFFLE]` |
| 4 | "Peek in the lockbox shelves. I hid mine there when I was four." | `[Princess Huluu \| STATION_1 — evidence_shelves]` |
| 5 | "Now the big golden magnifying glass tower! Mine turned up underneath." | `[Princess Huluu \| STATION_3 — magnifier_tower]` |
| 6 | "Teehee! Is that for the PARTY? Let me wear it! Are we invited?" | `[Imp Captain \| STEAL]` |
| 7 | "Places, please! The Pearl Opera presents… Detective Roshan tells us who took it!" | `[Maestro \| FINALE_OPEN]` |
| 8 | "You just wanted a turn! Everybody wears the crown at the bow." | `[Roshan \| FINALE_MID]` |
| 9 | "Birthday crown — on the table!" | `[Roshan \| CURTAIN_CALL]` |

*Optional button (recommended — it is a Chapter-2 continuity plant):* "Happy birthday, Detective. Keep it until your candles are lit." `[Princess Huluu | CURTAIN_CALL]` — **flag for the climax/crash writer:** this is the only floor-1 line that reaches forward to the Ember King blowing the candles out. It costs one clip and makes the crash rhyme all the way back to act 2.

**Instruction layer.** STATION_2 (TRAIL @ `pedestal_display`) is silent — the swipe is continuous and the shipped `"Swipe along the footprint trail!"` already carries it. Beat 3 quietly makes those footprints **imp** footprints, which is why the trail exists at all. Beat 9 precedes the shipped `"Case closed! Roshan solved the Two-Detective Mystery!"`

**BIRTHDAY LINK** — line 1: *"One more thing for my party! Tonight we find my birthday crown!"*

**ESCALATION — the imps HIDE, and their mischief becomes the puzzle.** Chef's imps grabbed in the open; these ones conceal, and the consequence is that **for the first time in the chapter the imps' trouble IS the gameplay content** — the trail she follows and the clues she lenses are theirs. It is also the first imp who wants to *wear* a party piece rather than hold it: dress-up, a step past touching, and the exact impulse the Captain repeats at the steal.

**ASSET WISHES**
- **REUSE `huluu.png` as-is** for the voice/portrait — audit-approved, no new art required to ship the act.
- **NEW `props/prop_tiara_cushion.png`** — a small purple velvet cushion with a crown-shaped dent, **empty**. Sits on the `pedestal_display` from the steal onward. *Why:* the cheapest possible card in the whole floor and it states "it is gone" without a word, which is the one thing a non-reader needs to understand a detective story.
- **NEW (optional) `actors/helper_detective.png`** — Huluu seated beside the `pedestal_display`, hands empty, tiara already off. *Why:* the act is about an absence on her head; her bare hair is the story.
- **REUSE** `props/goal_detective.png`, `actors/roshan_detective.png`, `actors/rival_detective*.png`, `backdrops/world_detective*.png`, `backdrops/stage_detective*.png`.

---

# ACT 3 · BALLERINA — "The Twin-Ribbon Recital"
`ACTS[2]` · costume `ballerina` · goal prop `goal_ballerina.png` · steal at phase 4 · `ACTS[2]` carries `"pitch": 0.6`

**LOGLINE** — Rosalina lends Roshan a music box that only plays while somebody is dancing, and teaches her the exact dance she will dance at her own party — until the imps tangle the ribbons and the tune starts running down.

**HELPER — Rosalina (`rosalina` → `bf_lily`, shipped).**
What she wants: for the dance to be *learned*, not watched.
The clever hook: **Rosalina never explains a step. She winds the box, and the steps appear as light** — which is not a metaphor, it is the shipped `WATCH` phase, `"Hold still and watch the glowing dance!"` **The helper's entire teaching method is the game's existing mechanic**, so a four-year-old learns the same way the character does. Second hook, and this is the one that makes the act *sound* different from everything else on the floor: **the box winds down.** `ACTS[2]` already ships `"pitch": 0.6`. When the imps tangle the ribbons the music sags and slows — the child **hears** the problem before she sees it — and the only way to wind it back up is to keep dancing. Third: this is the dance Roshan performs at the climax. The act is a rehearsal for a scene the child will later watch pay off, which is why Rosalina's button line is worth a clip.

**BEAT SCRIPT** — 9 lines
| # | Line | Tag |
|---|---|---|
| 1 | "One more thing for my party! Tonight we make the dancing music!" | `[Roshan \| ACT_OPEN]` |
| 2 | "My little music box, Roshan. It plays while you keep dancing." | `[Rosalina \| ACT_OPEN]` |
| 3 | "Teehee! Bouncy tiles! We want to dance at a party too!" | `[Imp Captain \| SCUFFLE]` |
| 4 | "Watch from the gold dressing alcove. The steps will glow for you." | `[Rosalina \| STATION_1 — curtain_alcove]` |
| 5 | "Around the pearl bandstand, dreamer — your ribbon is winding the music." | `[Rosalina \| STATION_3 — shell_bandstand]` |
| 6 | "Teehee! Is that for the PARTY? WE want music! Are we invited?" | `[Imp Captain \| STEAL]` |
| 7 | "Places, please! The Pearl Opera presents… Roshan's birthday dance, both ribbons!" | `[Maestro \| FINALE_OPEN]` |
| 8 | "Twirl with me, imps! Nobody dances alone at a birthday party." | `[Roshan \| FINALE_MID]` |
| 9 | "Dancing music — on the table!" | `[Roshan \| CURTAIN_CALL]` |

*Optional button (recommended):* "Save that last twirl, Roshan. Dance it at your party." `[Rosalina | CURTAIN_CALL]` — the climax callback.

**Instruction layer.** STATION_2 (STEPS @ `wave_tuffets`) silent — it is the act's only choice-tapping beat and it needs the child's full attention. Beat 8 is the inclusion beat granting beat 3's want verbatim. Beat 9 precedes the shipped `"Roshan wins the Twin-Ribbon Recital with a beautiful final twirl!"`

**BIRTHDAY LINK** — line 1: *"One more thing for my party! Tonight we make the dancing music!"*

**ESCALATION — the imps COPY.** They take nothing at first; they join in, badly, on the other half of the stage (the shipped `rival_ballerina`). This is the floor's only *imitative* mischief and it is **the seed of the entire floor-2 posture** — "fine, we'll make our own party" starts here as "we can dance too." It is also the first steal in the chapter with a stated **motive** rather than a want ("WE want music"), which is the F2 crack showing through F1 by one act. And it is the only act on the floor where the trouble is **audible, not visual** — the shipped pitch sag does the work no caption could.

**ASSET WISHES**
- **NEW `actors/helper_ballerina.png`** — Rosalina in a soft practice wrap at the `curtain_alcove`, **the music box in both hands, lid open.** *Why:* the hook only reads if her hands are on the box; a portrait without it is a stranger.
- **NEW `props/fx_music_wilt.png`** — a single drooping, dimmed music note. Drawn over the `shell_bandstand` while the tune sags, cleared when she dances. *Why:* one small card gives the pitch-drop a picture, and it is reusable in the popstar act and in the crash.
- **REUSE** `props/goal_ballerina.png` (**it is already the music box** — no new prop needed), `actors/roshan_ballerina.png`, `actors/rival_ballerina*.png`, `backdrops/world_ballerina*.png`, `backdrops/stage_ballerina*.png`.

---

# ACT 4 · CANDY MAKER — "The Candy Workshop Cup"
`ACTS[3]` · costume `candymaker` · goal prop `goal_candymaker.png` · steal at phase 4

**LOGLINE** — Roshan fills a party bag for every guest while a baby eagle who cannot count and cannot talk keeps eating them, until Roshan works out that Sparkle was only ever hungry because nobody had given her one yet.

**HELPER — Sparkle the baby eagle (chirps only — `sparkle` = `af_bella` 1.55; recommend **SFX chirps, no TTS lines at all**).**
What she wants: a bag. She cannot say so.
The clever hook, and this is the floor's Lamba-and-Evie beat: **Sparkle is not naughty — she is the guest list.** She eats one bag, so Roshan has to make one more; she eats another, one more again. The counting game *is* the helper's appetite. Then at the finale Roshan gives Sparkle **hers first**, and Sparkle stops eating everyone else's. A four-year-old reads that in one frame — *she was hungry because she hadn't been given one* — and it is the imp arc's whole thesis, rehearsed in miniature, one act before the Curtain Dragon and sixteen acts before the Captain is finally invited. The shipped final phase does the landing for free: `SHARE`, *"Tap a candy for every friend in the crowd!"* at the `candy_cart`. The party-bag beat is already built; it just needed a reason.

**BEAT SCRIPT** — 9 spoken + 1 SFX
| # | Line | Tag |
|---|---|---|
| 1 | "One more thing for my party! Tonight we fill the party bags!" | `[Roshan \| ACT_OPEN]` |
| — | *(bright chirp — she swallows a gumdrop whole)* | `[Sparkle \| ACT_OPEN — SFX, no TTS]` |
| 2 | "Sparkle! That was somebody's party bag. Now we need one more!" | `[Roshan \| ACT_OPEN]` |
| 3 | "Teehee! Juggly gumdrops! We are SO hungry — just one each?" | `[Imp Captain \| SCUFFLE]` |
| 4 | "Pink syrup from the big glass gumball boiler — enough for everybody!" | `[Roshan \| STATION_1 — gumball_vat]` |
| 5 | "Bags from the cottage with the big red bow! Sparkle, count them!" | `[Roshan \| STATION_3 — candy_bag_cottage]` |
| 6 | "Teehee! Is that for the PARTY? A bag for us? Are we invited?" | `[Imp Captain \| STEAL]` |
| 7 | "Places, please! The Pearl Opera presents… Roshan's party-bag parade!" | `[Maestro \| FINALE_OPEN]` |
| 8 | "Sparkle gets hers first! Then one bag for every single friend." | `[Roshan \| FINALE_MID]` |
| 9 | "Party bags — on the table!" | `[Roshan \| CURTAIN_CALL]` |

**Instruction layer.** STATION_2 (SORT @ `taffy_press`) silent — put a second Sparkle chirp there instead, from the lever she is perched on. Beat 5's *"Sparkle, count them!"* is an invitation for the child to count out loud with a bird who cannot. Beat 9 precedes the shipped `"Roshan's smiling sweets win the Candy Workshop Cup!"`

**BIRTHDAY LINK** — line 1: *"One more thing for my party! Tonight we fill the party bags!"*

**ESCALATION — the imps EAT.** The only act on the floor where what they take is **gone** — and the act's answer is a shrug, because it is candy and you simply make more. That is the floor's most generous piece of mischief and its largest appetite. Critically, it is also **the only act where the helper does exactly the same thing the imps do.** Sparkle steals candy; the imps steal candy; the child cannot tell them apart, and nobody is scolded. That moral flattening is deliberate and load-bearing: it is what makes *"the dragon isn't grumbly anymore — he just wanted to be in the show!"* land as the obvious truth one act later instead of as a twist.

**ASSET WISHES**
- **NEW `actors/helper_candymaker.png`** — Sparkle perched on the `taffy_press` ball-topped lever, **one cheek visibly bulging with a gumdrop**, eyes innocent. *Why:* the cheek is the entire joke, the entire hook and the entire explanation of the counting game. If only one new card is funded on floor 1, fund this one.
- **NEW `props/prop_party_bag.png`** — a single striped, ribbon-tied party bag. Used for the counting row, for Sparkle's bag at beat 8, and reusable on the party table at the climax. *Why:* `goal_candymaker.png` is *wrapped candy*; the **bag** is the thing that reads as a birthday to a four-year-old.
- **REUSE** `props/goal_candymaker.png`, `actors/roshan_candymaker.png`, `actors/rival_candymaker*.png`, `backdrops/world_candymaker*.png`, `backdrops/stage_candymaker*.png`, existing eagle chirp SFX.

---

# FLOOR 1 BOSS · THE CURTAIN DRAGON
`ACTS[4]` · `type: boss`, `boss_hp: 15`, `peek_time 5.0`, `hide_time 5.0` · 3D `OperaAct` boss engine (`opera_act.gd:6035-6089`), puppet `assets/art35/opera/opera_dragon.glb` — **shipped**

**ROLE IN THE BIRTHDAY PREPARATION — HE IS THE PLACE.**
Four pieces are made and there is nowhere to put them. The party is going to be at the Pearl Opera House, and the Pearl Opera House has exactly one room big enough — the big stage. The curtain will not open. Something heavy is in it.

The reveal is that **he is not blocking the curtain. He is holding it.** He has been holding it for years, in the dark, on the far side, and he has never once been told when to let go, because nobody gives the curtain a cue — they just expect it to open. He is "grumbly" the way anyone is grumbly at the end of a long shift nobody thanked them for. Roshan's sparkles are not an attack; they are the first light anyone has pointed at him.

**KIND RESOLUTION — she does not evict him, she casts him.** She gives him a cue. *"Pull the curtain when I say places."* He is not removed from the doorway of the party; he is put in charge of it. He becomes **the party's curtain-puller and doorman — Guest 1** — which means the creature who was in the way of the party is now the one who lets everybody into it. This is exactly the shipped win_line, `"The dragon isn't grumbly anymore — he just wanted to be in the show!"`, with a job attached.

**BEAT SCRIPT** — 7 lines
| # | Line | Tag |
|---|---|---|
| 1 | "My party needs the big stage — but the curtain will not open!" | `[Roshan \| ACT_OPEN]` |
| 2 | *(a small grumble)* "Nobody ever tells me when to pull it." | `[Curtain Dragon \| FIRST_PEEK — boss phase "peek"]` |
| 3 | "You are not grumbly — you are stuck! Hold on, big fellow." | `[Roshan \| ROAR — boss phase "roar", tier 2]` |
| 4 | "I have held this curtain for years. Nobody ever clapped." | `[Curtain Dragon \| LAST_HIT — hp reaches 0]` |
| 5 | "Then you are my doorman! Pull the curtain when I say places." | `[Roshan \| CURTAIN_CALL]` |
| 6 | "Places… **please!**" *(the curtain sweeps open; he beams)* | `[Curtain Dragon \| CURTAIN_CALL]` |
| 7 | "Dragon is coming to my party! Look — a whole new floor!" | `[Roshan \| LOBBY_RETURN]` (Bible §7 boss variant) |

Beat 5 runs immediately before the shipped win_line, spoken. **Beat 6 is the best line on the floor and it is free:** the dragon steals the Maestro's own house call, four acts after the child first heard it. It is a laugh now, and it is a setup — Bible §3 makes the Maestro the one member of staff never allowed on stage, so act 14's *"wants to steal the whole show"* lands harder because a **dragon** got his catchphrase first, on floor 1, and nobody minded.

**Nothing is defeated.** House law holds: fifteen sparkle hits are fifteen moments of somebody finally being looked at. No line contains a threat, no line contains "hurry", and the roar phase is answered with concern (*"you are stuck!"*), never with fear.

**HANDOFF TO THE CLIMAX/CRASH WRITER (one line, no obligation):** the dragon opens the curtain on the party at the climax — and at the crash he is the one who cannot get it closed in time when the Ember King puffs. His shipped stage business already exists for both beats.

**ASSET WISHES**
- **REUSE `assets/art35/opera/opera_dragon.glb`** — verified present; the puppet-on-a-stick with a primitive fallback at `opera_act.gd:6078-6088`. **No new dragon art is needed for this act.**
- **NEW (optional, small) `props/prop_curtain_rope.png`** — a frayed gold pull-rope, wrapped around one dragon claw, visible from the first peek. *Why:* it converts "monster in the curtain" into "worker holding a rope" **before** the dialogue says so, which is the difference between a reveal and a relief for a four-year-old.
- **NEW (optional) `actors/dragon_doorman_bow.png`** — the dragon in a small doorman's cap, bowing, for the curtain call and for reuse as Guest 1 at the climax. Mirrors the shipped `imp_captain_bow.png` pattern.

---

# CROSS-ACT SUMMARY

**Escalation ladder — five distinct shapes, no repeats.**
| Act | The imps' verb | What is at risk | First-in-chapter |
|---|---|---|---|
| Chef | **grab** — tools, never food | nothing | the Captain's first touch of a finished piece |
| Detective | **hide** | one crown | imp mischief becomes the puzzle content |
| Ballerina | **copy** | the tune slows | a stated motive at the steal (F2 posture, early) |
| Candymaker | **eat** | bags, genuinely gone | helper and imp mischief become indistinguishable |
| Dragon | **none** | nothing was ever wrong | the obstacle turns out to be an employee |

**Refrain compliance (Bible §7).** Refrain 1 opens every act (line 1, carrying the piece name — also the birthday link). Refrain 2 closes every act (`"[Piece] — on the table!"`, timed to the shelf-pop tween). Refrain 3 (`"Are we invited?"`) closes every Captain steal line; implementers may split it into a single shared clip appended after the per-act steal line if they prefer one recording over four. Refrain 4 (`"Places, please! The Pearl Opera presents…"`) opens every finale — and is hijacked once, by a dragon.

**Line budget for floor 1:** 42 new Kokoro clips (chef 9, detective 9, ballerina 9, candymaker 9, dragon 6) + 3 optional buttons + 2 Sparkle chirp SFX + 1 shared lobby-return clip (`"On the table! What shall we make next?"`). Every line is 8-14 words, one idea, ear-first; every gesture beat that is a continuous drag or circle is left silent on purpose.

**Voice asks specific to floor 1** (beyond the Bible §8 `captain` and `maestro` slots):
- **`"dragon": ("am_puck", 0.86, 0.90)`** — the imp actor pitched **down**, so the floor-1 boss is audibly **a giant imp**. This is canon-true (Bible §3: the imps and the dragon share one want — to be in the show), costs **zero new models**, and leaves `af_sky` free for the Ember King fallback. Fallback if it muddies against the crew at 1.38 and the Captain at 1.16: `("af_sky", 0.82, 0.94)`.
- Requires the `_speaker_key` dragon branch from §0(c) or he speaks as Roshan.
- Kareem, Huluu, Rosalina and Sparkle all route correctly today (`shop`/`huluu`/`rosalina`/`sparkle`); **no new voice models needed for any of the four helpers.**

**Two engineering asks, both small, in priority order:**
1. **`helper_actor` slot** (§0(d)) — without it Kareem, Huluu, Rosalina and Sparkle are voices with no bodies. ~12 lines. The scripts play without it; they just play thinner.
2. **`"dragon"` branch in `_speaker_key`** (§0(c)) — one line, and without it the boss speaks in the player's voice.# FLOOR 2 — THE STARLIGHT BALCONY

**Act writer deliverable: doctor, farmer, boxer, magician + Shadow Phantom.**
Floor theme (derived, not invented): **floor 2 is about loneliness handled kindly.** The imps stop playing and start *copying* — they are building a rival party backstage — and the floor ends with the Shadow Phantom, someone who expresses the identical wound by going dark instead of loud. Roshan's answer both times is the same: be seen, be invited.

---

## 0. GROUND TRUTH I VERIFIED FIRST (read this before the scripts)

### 0.1 Station-to-phase mapping is mechanical — I computed it, I did not guess
`_assign_stations()` (`scripts/opera_career_world_2d.gd:521-532`) walks phases in order, **skips every `"mode": "bop"` phase**, and hands the rest the painted stations left-to-right. So the landmark each line fires at is fully determined:

| Career | STATION_1 | STATION_2 | STATION_3 | STEAL | FINALE_OPEN | FINALE_MID |
|---|---|---|---|---|---|---|
| **doctor** | WASH @ `starfish_triage` | FIND @ `stethoscope_clinic` | X-RAY @ `thermometer_garden` | PLUSHY CHASE | CAST @ `exam_booth` | BANDAGE @ `recovery_bed` |
| **farmer** | PLANT @ `flower_urn` | FEED @ `barn_door` | MUD HOP @ `hay_steps` | PIGGY CHASE | HERD @ `mud_pen` | PICNIC @ `harvest_picnic` |
| **boxer** | JAB @ `target_pads` | DUCK @ `punching_bags` | *(none)* | BELL CHASE | ROUND @ `sparring_mats` | BELT @ `victory_bell` |
| **magician** | VANISH @ `stage_curtain` | TRACK @ `purple_hat_door` | ROPE @ `red_hat_den` | LAMBA CHASE | CABINET @ `magic_door_gallery` | PORTAL @ `moon_pool` |

Two happy accidents I wrote *into* the fiction rather than around:
- **doctor `starfish_triage`** is painted as "smiling starfish patient waiting on a purple cushion **under the golden shell archway at the left entry**." The party piece is a starfish plushy and it is sitting **at the front door, where a guest arrives**. Act 5's whole premise was already painted.
- **farmer MUD HOP lands at `hay_steps`, not `mud_pen`.** Read as a mismatch it's a bug; read as staging it's the joke — you climb the hay-bale staircase, wind up at the top, and hop *down* into the mud. I wrote the line that way, so no code change is needed.

### 0.2 DEFECT — the Shadow Phantom currently speaks in Roshan's voice
`audio_director.gd:95-113`. `_speaker_key("Shadow Phantom")` matches no branch and falls through to `return "roshan"` at `:113`. This is the same class of bug the bible flagged for the Ember King, but it is on **my** floor and blocks the boss entirely. Fix, alongside the two the bible already names:

```gdscript
if "phantom" in w or "shadow" in w: return "phantom"
if "captain" in w: return "captain"        # MUST sit above the "imp" branch at :112
```
Confirmed good news: `chuck` `:104`, `wacky` `:105`, `maestro` `:110` all already route correctly, so three of my four helpers need no plumbing.

**Voice slot for the phantom:** the bible assigns `am_santa` to the Ember King and lists `af_sky` only as a fallback. If the King takes Santa (recommended there), **`af_sky` is free** and is close to ideal for a shy little phantom: `"phantom": ("af_sky", 1.08, 1.02)` — soft, slightly lifted, unmistakably *small*. That spends the last unused Kokoro model on the one floor-2 character who has no voice at all.

**Harmless but worth knowing:** `:100` is `if "evie" in w or "lamb" in w: return "evie"` — a speaker labelled "Lamba" would speak *in Evie's voice*. Lamba is silent by design so this never fires, but do not "fix" it: it is a graceful failure mode.

### 0.3 DEFECT — the boxer never reaches the pedestal holding his own party piece
Boxer has **6 phases, only 4 non-bop**, against **5 stations**. `station_index` runs 0,1,2,3 and stops. Station 4 — `champion_belt`, *"giant championship belt with golden scallop-shell buckle displayed on the tiered pedestal"* — **is never visited in the entire act.** The one landmark the painting built for this career is the one the child never walks to, and it is the birthday sash.

This generalises: the same arithmetic orphans `trophy_shell` in **racer** and `encore_balcony` in **popstar** (both 6 phases / 4 non-bop / 5 stations). In all three the orphan is the *final destination landmark holding the goal prop*. Floor 3's writer needs this.

Cheapest fix, one line in `_assign_stations()` — pin the last non-bop phase to the last station:
```gdscript
# after the loop: make the final job beat land on the destination landmark
var last := station_for_phase.keys().max()
if last != null: station_for_phase[last] = station_list.size() - 1
```
I wrote the boxer script assuming this fix lands. If it does not, boxer's FINALE_MID line fires at `victory_bell` instead — which still works, because the bell is what the captain rang. Both readings are safe.

### 0.4 Helper lines are a data-only change
`opera_career_world_2d.gd:727` reads `phase.get("speaker", "Roshan")` and passes it straight to `m.show_msg(...)`. Nursery already uses this (`"speaker": "Faron"`, `:137-141`). **Every helper cheer below can ship as a string in the PHASES dict — no new code.** Only the ACT_OPEN / STEAL / CURTAIN_CALL beats need `say_sequence`.

### 0.5 Bible §6 supersedes the audit's casting table
The audit (`OPERA_NARRATIVE_AUDIT_2026-08-02.md:108-111`) casts Harper on doctor and Mewsha on magician. **The bible overrides both**: doctor = Evie, magician = Evie + Lamba, Mewsha moves to astronaut. I wrote to the bible. This means **Evie carries two of my four acts**, which is the bible's stated intent ("Evie deliberately doubles") and is the spine of my floor.

### 0.6 Two continuity fixes in shipped text
- ACTS magician `voice` (`opera_house.gd:71`) still says *"hide and track the **bunny-fish**"* while PHASES `:101,:104` already say **Lamba**. One-word fix; without it the child hears two names for one character.
- Two proper nouns I am **proposing, not assuming** — flag for owner ratification: the starfish plushy is **Starry**, the guest-of-honour piggy is **Pudding**. A 4-year-old needs a name to hold onto; both acts are "find the one specific one" games and are much weaker with "the starfish" / "the piggy."

---

# ACT 5 — STUFFIE SURGEON (`doctor`) · party piece: **the mended starfish plushy**

**LOGLINE**
Evie brings Roshan her birthday present and it arrives with its arm torn off — so the birthday girl puts on a white coat and mends her own present while the giver watches, terrified, from the end of the bed.

**HELPER — Evie** *(little kid + giggles; voice `evie` 1.30)*
**What she wants:** for her present to be *good*. She chose it herself, it broke on the way, and she is convinced she has ruined the birthday.
**The clever hook:** this is the only act where **the party piece is a gift being given to Roshan, not made by her** — and it's broken before we meet it. The child watches a four-year-old logic problem resolve perfectly: *you can't be sad about a broken present if you're a doctor.* Evie's anxiety is the act's difficulty meter — she's on screen the whole time, hands over her mouth. And the payoff is three acts long: **because Roshan is gentle with Starry here, Evie hands her Lamba in act 8.** The trust is *earned on screen*, not asserted.
Station 1 of the painting is literally a smiling starfish on a cushion at the front door. The set already knew.

**BEAT SCRIPT** *(existing phase `voice` strings stay as the instruction layer underneath)*

| # | Line | Tag |
|---|---|---|
| 1 | "One more thing for my party! Tonight we mend Starry, my birthday present!" | `[Roshan \| ACT_OPEN]` |
| 2 | "I brought your present, Roshan… but Starry's arm came undone." | `[Evie \| ACT_OPEN]` |
| 3 | "Teehee! Bandages! Stripy things look GREAT on our party table!" | `[Imp Captain \| SCUFFLE]` |
| 4 | "You found her ouch so gently. Starry isn't even wriggling!" | `[Evie \| STATION_2 — the teal-domed clinic pavilion with the giant stethoscope]` |
| 5 | "Her temperature says… HAPPY! Is happy a temperature?" *(giggles)* | `[Evie \| STATION_3 — the giant red-bulb thermometer in the scalloped flower planter]` |
| 6 | "Our party needs a patient! Are we invited? No? Then borrowing!" | `[Imp Captain \| STEAL]` |
| 7 | "Places, please! The Pearl Opera presents… the gentlest doctor in the sea!" | `[Maestro \| FINALE_OPEN — the heart-crowned curtained exam booth]` |
| 8 | "Soft cast on — and a bandage for your pretend ouch, imp." | `[Roshan \| FINALE_MID — the shell-backed recovery plaza with the sunken bed-basin]` |
| 9 | "Starry is all mended — and ON THE TABLE!" | `[Roshan \| CURTAIN_CALL]` → then shipped `win_line` verbatim: *"Every stuffie is wiggling again — Roshan wins the surgeon relay!"* |

**Plus one per-act LOBBY_RETURN override** — the only one I am asking for on this floor, because it carries three acts of setup in ten words:
> "You kept Starry safe. I trust you with Lamba too." `[Evie | LOBBY_RETURN]`

Line 3 exists to explain the shipped instruction *"Imps are hiding the bandages!"* — they are not vandals, they want bunting. Line 6 exists to set up the shipped word **"borrowed"** in *"The imp captain **borrowed** the plushy patient!"* Line 8 is the inclusion beat: the imps faked ouches to get bandages, and Roshan treats the fake one anyway, without comment.

**BIRTHDAY LINK** — line 1: *"One more thing for my party! Tonight we mend Starry, my birthday present!"*

**ESCALATION — the imps FAKE NEEDING HER.**
Unique on the floor: this is the only steal disguised as *asking for help*. The imps queue up with invented ouches because bandages are stripy and stripy things look like party bunting. Where farmer's imps lure her guests away, boxer's announce themselves with a bell, and magician's take a person — doctor's imps **pretend to be patients**. It is the floor's gentlest opening move and it makes the captain's "borrowing" read as a fib rather than a threat.

**ASSET WISHES**
- **NEW `evie_scrubs.png`** — Evie in a too-big nurse apron, clutching the torn starfish. She must be visible on the sidelines for the whole act; her posture is the tension meter and there is no substitute.
- **NEW `prop_starry_torn.png`** — the *before* state. Genuinely required: for a non-reader the entire arc is "broken → fixed," and that only reads if she sees broken first. The *after* is **REUSE `goal_doctor.png`** (already shipped, already the shelf slot).
- **NEW `dressing_imp_crate_table.png`** ⭐ — **my strongest ask, and it serves all four acts.** A packing crate with a paper tablecloth, parked at the far right of every floor-2 painted world. It is the single visual proof of the floor's COPYING posture, and it grows across the four acts: bandage-bunting here → a muddy hoofprint in farmer → a paper crown in boxer → a taped-on stage curtain in magician. One asset, four dressings, and the child reads the imps' whole motive without a word.
- REUSE `roshan_doctor.png`, the full `rival_doctor_*` 13-frame set, `imp_mischief.png` + `imp_mischief_taunt.png` (the fake-ouch gag is just imps holding their arms).

---

# ACT 6 — FARMER · party piece: **the fed piggy (the guest of honour)**

**LOGLINE**
Roshan has to pick one piggy out of twelve to be her party's guest of honour, she cannot tell them apart, and the only one who can is a dog who cannot talk.

**HELPER — Chuck** *(real family recording; `chuck.ogg`, `chuck_bark.ogg`, `chuck_whimper.ogg` — **EXISTING CLIPS ONLY, SACRED, NEVER REGENERATE**)*
**What he wants:** to do his job properly. He is a herding dog and he knows exactly which piggy is hungriest.
**The clever hook:** Chuck cannot say a single word, so **the act turns his silence into the mechanic**. Roshan asks yes/no questions and Chuck answers in barks — one bark yes, one whimper no. A 4-year-old can play twenty-questions with a dog. Then the captain throws the gate open, twelve identical piggies scatter, and finding Pudding again is *only* possible by listening for Chuck. **This is the most wordless act in the chapter and the one that leans hardest on a real recording of the family's real dog.**

Implementation note: **play Chuck's beats as direct SFX, not through `show_msg`/`say_sequence`.** Routing them as dialogue risks a future TTS pass touching sacred audio. `_speaker_key` has a `chuck` branch at `:104` — do not rely on it here.

**BEAT SCRIPT** — 9 spoken lines + 3 sacred-clip SFX beats (the SFX are not lines and add nothing to the voice budget)

| # | Line | Tag |
|---|---|---|
| 1 | "One more thing for my party! Tonight we make Pudding the guest of honour!" | `[Roshan \| ACT_OPEN]` |
| 2 | "Chuck — which piggy is hungriest? One bark for yes!" | `[Roshan \| ACT_OPEN]` |
| — | *one bark* — `chuck_bark.ogg`, EXISTING | `[Chuck \| STATION_1 — the stone pedestal urn overflowing with pink flowers]` |
| 3 | "Teehee! Muddy! Our party needs a mud pool, splishy-splashy!" | `[Imp Captain \| SCUFFLE]` |
| 4 | "Good throw! Pudding caught it — look at that happy wiggle." | `[Roshan \| STATION_2 — the red barn with the open arched wooden door]` |
| 5 | "Up the hay steps… wind up… and SPLAT in the mud!" | `[Roshan \| STATION_3 — the staircase of stacked golden hay bales]` |
| 6 | "Piggies! Come to OUR party! Are we invited? Piggies are!" | `[Imp Captain \| STEAL]` |
| — | *one whimper* — `chuck_whimper.ogg`, EXISTING | `[Chuck \| STEAL]` |
| 7 | "Places, please! The Pearl Opera presents… the fastest herding dog alive!" | `[Maestro \| FINALE_OPEN — the round log-post fenced mud pen]` |
| 8 | "Snacks for every piggy — and a corn cob for you, imp." | `[Roshan \| FINALE_MID — the red gingham picnic blanket with baskets of corn and grapes]` |
| 9 | "Pudding, you're the guest of honour — ON THE TABLE!" | `[Roshan \| CURTAIN_CALL]` → then shipped `win_line`: *"Roshan's happy herd wins the Piggy Picnic Challenge!"* |
| — | *happy bark* — `chuck.ogg`, EXISTING | `[Chuck \| CURTAIN_CALL]` |

Line 7 announces **Chuck**, not Roshan — the one time in sixteen acts the Maestro's house call points at somebody else, and it costs one word. Line 9's joke is that a live piggy goes "on the table" as a guest; that is exactly four-year-old funny and `goal_farmer.png` already shows a piggy on the shelf.

**BIRTHDAY LINK** — line 1: *"One more thing for my party! Tonight we make Pudding the guest of honour!"*

**ESCALATION — the imps steal the GUESTS, not the goods.**
This is the only floor-2 steal where the captain ends up **holding nothing**. He doesn't snatch a prop; he opens the gate and *invites her guest list to his party instead* — and the piggies go willingly, which is worse and funnier. It is also the only act on the floor with zero helper dialogue, so the theft has to land purely on one whimper from a real dog. Deliberately placed second: after doctor's small fib, this is the first steal that costs Roshan something she cannot simply pick back up.

**ASSET WISHES**
- **NEW `prop_pudding_ribbon.png`** — one piggy in a birthday party hat. **This is required, not decorative.** The act is "find Pudding" and twelve identical piggies makes it unplayable for a non-reader. Cheapest possible form: a single hat overlay sprite composited onto one existing piggy.
- **REUSE — crop of `wacky_chuck.png`** for Chuck's sideline portrait (the audit already proposes this at `:109`; it needs no new generation).
- **REUSE `dressing_imp_crate_table.png`** (shared floor-2 asset) — dressed here with a muddy hoofprint across the tablecloth.
- REUSE `goal_farmer.png`, `roshan_farmer.png`, the `rival_farmer_*` set, `imp_mischief_flee.png` for the gate-opening gag.

---

# ACT 7 — BOXER · party piece: **the championship belt = the birthday sash**

**LOGLINE**
Roshan fights three friendly rounds for a championship belt that turns out to be about six sizes too big — so her corner man spends the whole match sewing it into a birthday sash.

**HELPER — Wacky** *(grandpa chuckle; voice `wacky` 0.98)*
**What he wants:** to finally give the belt away. He won it a very long time ago and it has been on a shelf ever since.
**The clever hook:** **Wacky is coaching and tailoring at the same time.** A championship belt on a four-year-old mermaid goes round three times — it is a comedy prop, not a wearable — so between rounds Wacky is on one knee with a needle and a tape measure, hemming it into a sash while bellowing encouragement. It explains in one image why the party piece is a *sash*, it keeps a boxing match unmistakably silly (the bible's stated reason for casting him), and it quietly rhymes with the imps: **nobody ever threw Wacky a party either.** He never says that. He just gives the belt away, which is what people who were never celebrated do.

**BEAT SCRIPT**

| # | Line | Tag |
|---|---|---|
| 1 | "One more thing for my party! Tonight we win my birthday sash!" | `[Roshan \| ACT_OPEN]` |
| 2 | *(chuckle)* "That belt's mine, little champ. Won it before you had a tail!" | `[Wacky \| ACT_OPEN]` |
| 3 | "Teehee! Padded gloves! Bouncy! Our party needs a bouncy castle!" | `[Imp Captain \| SCUFFLE]` |
| 4 | "Ho ho! Straight little jab! Hold still, I'm hemming your sash." | `[Wacky \| STATION_1 — the red X-stitched target shields on the domed training tunnel]` |
| 5 | *(giggling, clanging the bell)* "DING DING! Our party starts NOW! Are we invited? Don't care!" | `[Imp Captain \| STEAL]` |
| 6 | "Places, please! The Pearl Opera presents… the friendliest title bout ever!" | `[Maestro \| FINALE_OPEN — the red circular sparring mat]` |
| 7 | "Left, middle, right — and YOU ring the bell with me, imp!" | `[Roshan \| FINALE_MID — the bell tower with the golden victory bell]` |
| 8 | "One birthday sash, won fair and square — ON THE TABLE!" | `[Roshan \| CURTAIN_CALL]` → then shipped `win_line`: *"And the winner of the friendly championship is... ROSHAN!"* |
| 9 | "Ho ho — it's yours now, champ. Happy birthday, little sash-wearer." | `[Wacky \| CURTAIN_CALL]` |

**Optional 10th if the budget allows** — Wacky at `STATION_2` (the rack of hanging punching bags): *"Duck low! Ducking's how I kept this handsome nose, ho ho!"*

Line 5 is the floor's turning point and it is a **deliberate escalation *inside* the refrain**: it is the first and only time in sixteen acts the captain asks "Are we invited?" and then answers it himself. That bravado is what makes his climax line — *(small, from the doorway)* "…Are we invited?" — land like a release. He is giggling when he says "Don't care," and he is lying.

Line 7 is the best inclusion beat on the floor: **the bell he stole to announce his own party, she hands back so he can ring it for hers.** No lesson is stated.

**BIRTHDAY LINK** — line 1: *"One more thing for my party! Tonight we win my birthday sash!"*

**ESCALATION — the imps go PUBLIC.**
Doctor's imps fibbed, farmer's imps lured. Boxer's imps **announce**. The captain rings the great bell over the entire opera house to declare that his party has begun — the loudest act on the floor and the moment the rival party stops being a backstage rumour and becomes a public claim. It is the only steal the whole building hears.

**ASSET WISHES**
- **NEW `wacky_corner.png`** — Wacky with a corner-man's towel, a tape measure round his neck and **a threaded needle in his hand**. The needle *is* the gag; without it the sewing beat is invisible and lines 4 and 9 stop making sense.
- **NEW `prop_belt_sash.png`** — the belt re-tailored, worn diagonally. Wanted because `goal_boxer.png` is a belt on a pedestal and the party piece is a sash; the child should see the transformation. **Acceptable zero-cost fallback:** REUSE `goal_boxer.png` and simply pose Roshan wearing it diagonally in the curtain-call frame.
- **REUSE `dressing_imp_crate_table.png`** (shared) — dressed here with a paper crown, since this is the imps' "we're the champions" beat.
- REUSE `roshan_boxer.png`, the full `rival_boxer_*` 13-frame set, `goal_boxer.png`.
- **FLAG, not art:** see §0.3 — `champion_belt` is currently an unreachable station. This act's party piece has a painted pedestal the child never walks to.

---

# ACT 8 — MAGICIAN · party piece: **Lamba's reveal (the party's big trick)**

**LOGLINE**
Evie lends Roshan her Lamba to be vanished in front of a full house, the imp captain hides her for real, and the trick only works when Evie is brave enough to call her back.

**HELPER — Evie + Lamba** *(the owner's own quality bar)*
**What Evie wants:** to be brave enough to watch.
**The clever hook, in two moves beyond the brief:**
1. **Evie says the magic word, not Roshan.** Roshan does every piece of magic in the act and it isn't enough — the portal at the moon pool opens on *Evie's* voice, because Lamba only comes back for her own person. The child watches a smaller kid do the hardest thing in the show, which is trust somebody.
2. **Lamba comes back wearing a tiny imp party hat.** ⭐ The captain didn't steal a hostage — he *cast her in his show*, and he tucked her in. One small sprite delivers the imps' entire motive with zero words, three acts before the invitation pays it off. This is the single most valuable image on floor 2.

And act 5 is why any of it is allowed: Roshan mended Starry, so Evie hands over Lamba. The trust is stated out loud in line 2 and the child has seen it earned.

**BEAT SCRIPT**

| # | Line | Tag |
|---|---|---|
| 1 | "One more thing for my party! Tonight we make the big trick!" | `[Roshan \| ACT_OPEN]` |
| 2 | "You mended Starry… so you can hold Lamba. Be gentle." | `[Evie \| ACT_OPEN]` |
| 3 | "Teehee! Hats! Our party needs hats! Everybody wears hats!" | `[Imp Captain \| SCUFFLE]` |
| 4 | "She's gone! …She's really gone. Do it AGAIN!" *(giggles)* | `[Evie \| STATION_1 — the golden scallop-shell proscenium arch with red velvet curtains]` |
| 5 | "Our show needs a star! Are we invited? Then she's coming instead!" | `[Imp Captain \| STEAL]` |
| 6 | *(small)* "Bring her back, Roshan. She doesn't know those imps yet." | `[Evie \| STEAL]` |
| 7 | "Places, please! The Pearl Opera presents… the greatest reveal in the sea!" | `[Maestro \| FINALE_OPEN — the row of freestanding enchanted doors and potion-shelf wardrobes]` |
| 8 | "LAMBA! Come back!" | `[Evie \| FINALE_MID — the round scrying pool reflecting the crescent moon]` |
| 9 | "Lamba's back — in a party hat! ON THE TABLE!" | `[Roshan \| CURTAIN_CALL]` → then shipped `win_line`: *"Roshan's star portal wins the Grand Illusion Duel!"* |

**Optional 10th** — Evie at `STATION_3` (the red top-hat building with the arched rabbit-den doorway): *"Lamba likes the little red door best. She told me."*

Line 8 is **deliberately three words** — it is a shout, not a line, and it is the only intentional break from the 8-14 word budget in this whole deliverable. It should be short enough that a four-year-old shouts it at the screen with her. Line 3 plants the hats that pay off in line 9; the shipped instruction *"Imps popped out of the magic hats!"* is already doing that work for free. Line 6's *"yet"* is load-bearing — by the climax she will know them.

**BIRTHDAY LINK** — line 1: *"One more thing for my party! Tonight we make the big trick!"*

**ESCALATION — the imps take a SOMEONE, and it turns out to be the kindest thing they do.**
The only floor-2 steal of a person rather than a thing, and the only one the captain performs *tenderly*. It is placed last on the floor because it needs act 5's trust to exist first, and because it is the floor's emotional turn: the moment that looks like it might genuinely hurt resolves into proof the imps were only ever playing dress-up. **That turn is what hands off to the Shadow Phantom** — magician ends on "the lonely ones weren't dangerous," the phantom opens on "here is an actually lonely one."

**ASSET WISHES**
- **NEW `lamba_partyhat.png`** ⭐ — Lamba in a tiny imp party hat. **The highest-value new asset on floor 2.** It is the whole proof-of-motive for the imps' arc, delivered in one glance, and it makes the climax invitation (bible §4 beat 6) something the child has already understood for five acts.
- **NEW `evie_stage.png`** — Evie at the lip of the stage, hands over her mouth, watching. Distinct pose and costume from `evie_scrubs.png`; she is on screen the entire act and her posture is the tension meter.
- **REUSE `dressing_imp_crate_table.png`** (shared) — dressed here with a scrap of stage curtain taped to the front, because by act 8 the imps have built themselves a theatre.
- REUSE `goal_magician.png`, `roshan_magician.png`, the `rival_magician_*` set, `imp_captain.png` / `imp_captain_taunt.png` (the tuck-in beat needs no new frame — the captain simply holds her).
- **FLAG, not art:** `opera_house.gd:71` still says "bunny-fish" where PHASES says "Lamba." One-word fix, or the child hears two names for the same friend.

---

# FLOOR-2 BOSS — THE SHADOW PHANTOM *(act 9)*

**ROLE IN THE BIRTHDAY PREPARATION — he makes the candles.**

The bible casts him as THE LIGHT: the Starlight Balcony is dark and lighting his lantern lights the whole floor. **Shipped data lets me push that considerably further at zero cost.**

### ⭐ THE FIVE-CANDLE RHYME — already shipped, three ways, nobody wired it up
- `opera_house.gd:75` — the Shadow Phantom act carries **`"lanterns": 5`**
- `ember_fortress.gd:33` — the Ember Fortress objective is **`const LANTERNS := 5`**
- Bible §5 — the Ember King blows out and steals **Roshan's five birthday candles**

Three fives, already in the codebase, never connected. Wire them and the phantom stops being "the lantern guy" and becomes **the one who made the candles**: the shy one finally shone, and then the Ember King blew it out. Chapter 3's journey north gains a second owner — Roshan wants her candles back, and the phantom wants his light back. The chapter's spine becomes literal: *five lanterns lit here → five candles on the table → five candles taken → five lanterns to relight at the fire mountain.* Not one new asset, not one new mechanic.

**Owner call to flag:** the bible notes that if Roshan is turning four, the fifth lantern should be the King's own. My line 5 below is written to stay agnostic — it says "a birthday candle," never "my fifth" — so either ruling works without a rewrite.

### The kind resolution
`boss_hp: 12` must **not** read as twelve hits. It reads as **twelve times he lets himself be seen.** Each SHINE doesn't damage him, it reveals a little more of him, and on the last one he stops hiding on purpose. He is never driven off, never beaten, never made sad — he is *found*. That is fully consistent with the shipped `win_line`, which I do not touch: *"The shadow was a lonely little phantom — now he's the star of the curtain call!"*

He and the imps share one wound and split it: **the imps got loud, the phantom went dark.** Roshan's answer is identical both times, and she gives it here first — which is exactly why the climax invitation works. He becomes **Guest 2: the party's lantern-lighter.**

**BEAT SCRIPT** *(7 lines; the existing act `voice` string stays as the instruction layer)*

| # | Line | Tag |
|---|---|---|
| 1 | "The balcony is dark! My party needs candles — five of them." | `[Roshan \| ACT_OPEN]` |
| 2 | "Places, please! Something shy is hiding in the Pearl Opera's shadows." | `[Maestro \| ACT_OPEN]` |
| 3 | "There you are! Don't hide — I'm just looking for you." | `[Roshan \| STATION_1 — first lantern lit]` |
| 4 | *(tiny, echoey)* "Nobody ever shines a light on ME. They all walk past." | `[Shadow Phantom \| FINALE_MID — third lantern]` |
| 5 | "Then hold this one yourself — it's a birthday candle." | `[Roshan \| FINALE_OPEN — fifth lantern]` |
| 6 | *(no echo now)* "I'm not a shadow. I'm the lantern boy!" | `[Shadow Phantom \| CURTAIN_CALL]` → then shipped `win_line` verbatim |
| 7 | "All five candles are lit — ON THE TABLE!" | `[Roshan \| CURTAIN_CALL]` |

**LOBBY_RETURN** uses the bible §7 shared boss line unchanged: *"The phantom is coming to my party! Look — a whole new floor!"*

Line 3 states the entire boss in ten words — **looking, not fighting** — before the child has swiped once. Line 4 is his one wound line, written to rhyme with the captain's "Are we invited?" without repeating it, so the two never blur. Line 5 is the act: **she gives him the fifth lantern instead of lighting it.** Line 6 is him naming himself, which is the kindest available resolution and needs no new proper noun. Drop the echo processing on line 6 and the child hears him stop hiding.

**BLOCKING DEFECT** — see §0.2. `_speaker_key` has no phantom branch, so **every line above currently plays in Roshan's voice.** Add `if "phantom" in w or "shadow" in w: return "phantom"` and the voice slot `"phantom": ("af_sky", 1.08, 1.02)`.

**ASSET WISHES**
- **REUSE — everything.** The phantom is *defined* by not being seen; the shipped peek/hide cycle (`peek_time: 5.0`, `hide_time: 4.0`) is the character. Do not commission a phantom portrait for the fight.
- **NEW `prop_five_candles.png`** — the five lit lanterns re-read as five birthday candles, for the curtain call and for the party-table shelf. This is the asset that makes the three-way rhyme *visible*, and it is later the thing the Ember King blows out in bible §5 — so it is spent twice.
- **REUSE `dressing_imp_crate_table.png`** (shared) — one last floor-2 appearance, now with a single unlit stub of candle on it. The imps tried to make their own light too.

---

## FLOOR-2 SUMMARY OF ASKS

**Code (all small, all verified against shipped source):**
1. `audio_director.gd:112` — add `captain` branch **above** the `imp` branch *(bible-flagged)*
2. `audio_director.gd:113` — add `phantom`/`shadow` branch **(new — I found this; it silently breaks the entire floor-2 boss)**
3. `opera_career_world_2d.gd:521-532` — pin the final non-bop phase to the last station **(new — orphans `champion_belt`, and also `trophy_shell` and `encore_balcony` on floor 3)**
4. `opera_house.gd:71` — "bunny-fish" → "Lamba"
5. `make_voices.py` `CHARS` — add `"phantom": ("af_sky", 1.08, 1.02)`

**Art, ranked by value per unit of work:**
1. `lamba_partyhat.png` — the imps' whole motive in one glance
2. `dressing_imp_crate_table.png` — one asset, four acts, four dressings; the floor's thesis made visible
3. `prop_pudding_ribbon.png` — without it act 6 is unplayable for a non-reader
4. `evie_scrubs.png`, `evie_stage.png`, `wacky_corner.png` — the three costumed helper portraits
5. `prop_starry_torn.png`, `prop_five_candles.png`, `prop_belt_sash.png` — the before/after states

**Line count:** 36 new spoken lines across the four acts + 7 for the phantom = **43**, of which the four bible refrains are recorded once and reused, and **three of Chuck's four beats use existing sacred clips and cost nothing.**

**Sacred audio honoured:** Chuck performs act 6 entirely on `chuck.ogg` / `chuck_bark.ogg` / `chuck_whimper.ogg`, played as direct SFX rather than routed through the dialogue system, so no future TTS pass can touch them.FLOOR 3a ACT SCRIPTS — Painter (act 10), Astronaut (act 11), Racer (act 12)
Written inside the approved Chapter 2 Bible. Grounded in the shipped code read below.

SOURCE FILES READ
- C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/scripts/opera_career_world_2d.gd (PHASES :100-160, GOAL_PROPS :173-187, FINALE_START :159-172, _assign_stations :521-533, phase speaker hook :727, celebrate :1185-1225)
- .../scripts/opera_house.gd (ACTS :20-133 — painter/astronaut/racer entries)
- .../scripts/opera_stage_paths.gd (PATHS :20-190 — painter/astronaut/racer stations)
- .../OPERA_NARRATIVE_AUDIT_2026-08-02.md (helper casting §5, 7-beat spine §4, rules appendix)
- .../scripts/audio_director.gd (_speaker_key :95-113), .../scripts/main.gd (_build_hud :3004-3041)

===============================================================================
VERIFIED STAGE GEOGRAPHY — which phase docks at which painted landmark
===============================================================================
_assign_stations() walks non-"bop" phases left-to-right through the station list.
Derived mapping (this is what the child actually walks):

PAINTER  (FINALE_START = 5, all 5 stations used)
  1 SKETCH  -> purple_pot      "giant purple paint pot with brush on its stepped pedestal"
  2 FILL    -> coral_pot       "giant coral-pink paint pot with brush, pink spill running down its steps"
  3 SPLAT   -> cream_pot       "giant cream/gold paint pot with brush at the deck's right end before the bridge"
  4 (SUNRISE CHASE — combat, no station)
  5 STROKES -> splat_garden    "rock-ringed garden bed of paint-splat topiaries" (ON STAGE)
  6 REVEAL  -> arch_gallery    "balustraded stone terrace beneath the grand scallop-shell archway" (ON STAGE)

ASTRONAUT (FINALE_START = 5, all 5 stations used)
  1 PIPES   -> observation_scope "giant brass-and-glass telescope tube mounted on a stone stand"
  2 PATCH   -> zero_g_ring       "giant upright glass ring (torus) with gold crown fitting"
  3 VALVE   -> valve_tower       "mint control tower with pink hand-wheel valve and shell emblem"
  4 (ROCKET CHASE — combat)
  5 BOOST   -> oxygen_tanks      "row of linked glass bubble tanks resting on arched bridge supports" (ON STAGE)
  6 LAUNCH  -> rocket_pad        "teal-and-pink rocket ship standing on the pier launch pad" (ON STAGE)

RACER (FINALE_START = 4, only 4 non-bop phases)
  1 STEER   -> start_curtain "giant scallop-shell archway with purple velvet stage curtains (starting gate)"
  2 TURBO   -> pit_garage    "blue arched pit-garage bays stocked with tool racks, crates, and stacked tires"
  3 (TROPHY CHASE — combat)
  4 LAP TWO -> tire_depot    "stacks of purple and teal race tires piled at the base of the track wall" (ON STAGE)
  5 FINISH  -> grandstand    "purple-seated spectator grandstand with scalloped white canopy" (ON STAGE)
  ** DEFECT FOUND: station index 4, `trophy_shell` ("giant scallop-shell trophy stage holding a huge
  pearl on a golden pedestal at the ramp summit") is NEVER assigned to any phase — racer has only four
  non-bop phases, so the act's own title landmark is unreachable. Fix options: (a) anchor the curtain
  call there, (b) move FINISH's station to index 4. My script assumes (a). **

===============================================================================
BINDING RULE I APPLIED (implementer must not undo it)
===============================================================================
The audit's per-act spine beat 6 ("Roshan invites the imps on stage") is SUPERSEDED by Bible §7
refrain 3: "Are we invited?" is asked once per act and NEVER answered for sixteen acts, so the
climax invitation (§4 beat 6) lands as a release. To keep each act warm without answering it,
every floor-3a act instead gives the imps a JOB, not an invitation:
  painter   -> she paints a gold frame around their handprints (they stay in the picture)
  astronaut -> they do the countdown
  racer     -> the Captain gets the checkered flag to wave
No line anywhere states the lesson (audit trap 1).

===============================================================================
ACT 10 — PAINTER — "The Sunrise Paint-Off"
===============================================================================
LOGLINE
Roshan paints the banner that will hang over her birthday cake, using her silent flower friend as
the live model — and the imps paint themselves into the corner so they'll be at the party too.

HELPER — the Flower Friend (silent by design; `assets/characters/friends/flower_friend.png` exists,
referenced by no script today)
WHAT SHE WANTS: nothing she can say. She wants to be in the picture, and she is the only one who
never asks.
THE CLEVER HOOK (Lamba-tier): she is not decoration, she is the COLOUR CHART. She poses on the
arch-gallery terrace and turns one petal to whichever colour comes next — so the child watches the
FLOWER, not the canvas, to know which giant paint pot Roshan walks to. Her silence becomes a
mechanic. Then the imps splat her with coral pink and she does not flinch — she blooms, and Roshan
paints the splat into the banner as a flower. The party banner ends up being a portrait of a friend
inside a sunrise. She never speaks and never needs to; every line about her is spoken BY Roshan.

BEAT SCRIPT (9 new lines + 2 shared ritual lines)
1 [Roshan | ACT_OPEN]        "One more thing for my party! Tonight we paint the party banner!"
2 [Imp Captain | SCUFFLE]    "Teehee! Squishy paint! We want to be IN the picture!"
3 [Roshan | STATION_1 — the giant purple paint pot]
                             "Purple first. Hold still, flower friend — you're going in my sunrise!"
4 [Imp Captain | STATION_2 — the giant coral-pink paint pot]
                             "Oops! Teehee! We splatted the flower friend — pink all over!"
5 [Roshan | STATION_3 — the cream-and-gold paint pot]
                             "Look — her splat turned into a flower. Five happy splatters!"
6 [Imp Captain | STEAL]      "Our handprints are on it now! It's our ticket — are we invited?"
7 [Maestro | FINALE_OPEN]    "Places, please! The Pearl Opera presents…"   (SHARED refrain 4 — one clip, all 16 acts)
8 [Roshan | FINALE_MID — the splat-topiary garden]
                             "Big circles round their handprints! I'm painting a gold frame for them."
9 [Roshan | FINALE_MID — the arch-gallery terrace]
                             "Hang it up! A sunrise, a flower friend, and four imp faces."
10 [Roshan | CURTAIN_CALL]   "Banner — on the table! It goes up over my birthday cake."
11 [Roshan | LOBBY_RETURN]   "On the table! What shall we make next?"   (SHARED, Bible §7)

Instruction layer preserved verbatim: line 5 quotes the shipped SPLAT voice "Tap five happy
splatters!"; line 8 quotes STROKES "Paint grand circles for the crowd!"; line 9 sits on REVEAL
"Tap the glowing frame to hang the sunrise!". Line 10 fires immediately BEFORE the shipped
win_line (D2 repair).

BIRTHDAY LINK (exact line):
  [Roshan | CURTAIN_CALL] "Banner — on the table! It goes up over my birthday cake."

ESCALATION — how painter's imp trouble differs from its floor-mates
The imps put themselves INSIDE the party piece. They do not hide it or break it; they add four
little handprint faces to the corner of the wet banner, because on floor 3 the want is "please just
say we can come" and a picture is the closest thing to a guest list a non-reader owns. Roshan's
answer is to frame them rather than scrub them — so from act 10 onward the party table already has
the imps ON it, three acts before the invitation is spoken. (Astronaut = they set the piece off
early; racer = they parade it in public. No overlap.)

ASSET WISHES
- REUSE `assets/characters/friends/flower_friend.png` — the helper, at the arch-gallery terrace.
  Zero art cost, matches audit §5 casting.
- NEW `assets/opera/worlds/actors/flower_friend_pose.png` + `flower_friend_splat.png` — two stage
  poses: petal raised (the colour cue) and pink-splattered-but-blooming. Why: her petal-turn IS the
  story layer of the walk between paint pots, and the splat gag is the act's only wordless kindness
  beat. `flower_friend.png` is a portrait crop, not a stage actor at 1280x720 scale.
- NEW `assets/opera/worlds/props/imp_handprints_overlay.png` — transparent decal, four small
  coloured handprints. Why: tween it onto `prop_rect` at the steal and keep it through
  celebrate(); the escalation becomes visible in one image with no new goal art.
- NEW (high value, low cost) `assets/opera/worlds/props/goal_painter_v2.png` — the framed sunrise
  WITH the flower friend in it and the four handprints inside the gold frame. Why: this is the
  texture the lobby party-table shelf shows forever (Bible §2). One PNG makes the shelf itself say
  "the imps are already at this party."
- REUSE `rival_painter*.png` (13 poses shipped), `goal_painter.png`, `world_painter.png`.

===============================================================================
ACT 11 — ASTRONAUT — "The Rocket Repair Race"
===============================================================================
LOGLINE
Roshan builds the firework that will go up when her party gets dark — with a cat in a fishbowl
helmet as her leak detector, and imps who cannot wait until dark to set it off.

HELPER — Mewsha (meows only; Bible §6 casting, overriding the audit's Sparkle draft — Sparkle now
belongs to candymaker)
WHAT SHE WANTS: a cosy box. That is all a cat wants.
THE CLEVER HOOK (Lamba-tier): Mewsha is the ship's cat in a round glass helmet, and she is the LEAK
DETECTOR — wherever she stops and meows, that is where the bubbles are escaping, so the child learns
to follow the cat instead of scanning the pipes. Then the hook turns: the rocket is a rocket-shaped
box, so Mewsha climbs in and settles. The countdown cannot start until Roshan swaps her the fishbowl
helmet as a better box. Cat gets a box, rocket gets to fly, nobody is scolded, and the whole problem
is solved without one word from the helper. It is the biggest re-watch laugh on the floor and it
costs zero dialogue.

BEAT SCRIPT (9 new lines + 2 shared ritual lines)
1 [Roshan | ACT_OPEN]        "One more thing for my party! Tonight we build the party firework!"
2 [Imp Captain | SCUFFLE]    "Teehee! A firework! Can we set it off NOW? Now now now?"
3 [Roshan | STATION_1 — the brass-and-glass telescope on its stone stand]
                             "Mewsha, ship's cat! Through the telescope first — she spots things I miss."
4 [Roshan | STATION_2 — the giant glass zero-g ring]
                             "Mewsha's meowing at the ring! That's a leak — tap the sparkles!"
5 [Roshan | STATION_3 — the mint valve tower with the pink hand-wheel]
                             "Spin the pink wheel! Mewsha, that rocket is NOT a cosy box!"
6 [Imp Captain | STEAL]      "I pressed the silly button and WHOOSH! Off it went! Are we invited?"
7 [Maestro | FINALE_OPEN]    "Places, please! The Pearl Opera presents…"   (SHARED)
8 [Roshan | FINALE_MID — the linked glass bubble tanks on the bridge supports]
                             "It floated down on a parachute! Refill the tanks — tap in the green!"
9 [Roshan | FINALE_MID — the rocket on the pier launch pad]
                             "Out you hop, Mewsha, take my helmet. Imps — count! Three, two, one!"
10 [Roshan | CURTAIN_CALL]   "Rocket — on the table! It goes off when my party gets dark."
11 [Roshan | LOBBY_RETURN]   "On the table! What shall we make next?"   (SHARED)

Instruction layer preserved: line 4 quotes PATCH "Tap the sparkle leaks to patch them!"; line 5
quotes VALVE "Draw circles to turn the launch valve!"; line 8 quotes BOOST "Tap the boosters in the
green!"; line 9 quotes LAUNCH "Hold through the countdown... and launch!" — the shipped chase line
"the imp captain scooped up the little rocket and pressed the silly button!" is now paid off by
line 6 rather than being an unexplained joke.

BIRTHDAY LINK (exact line):
  [Roshan | CURTAIN_CALL] "Rocket — on the table! It goes off when my party gets dark."
(Deliberate quiet plant: Bible §5 has the Ember King take the light. The firework is the one thing
on the table that belongs to the dark. Nothing states this; it just sits there.)

ESCALATION — how astronaut's imp trouble differs from its floor-mates
The imps set the party piece OFF, early. This is the purest floor-3 "we can hear the party being
laid out and we cannot wait" beat: the Captain does not carry the rocket away, he launches it, and
it comes down on a little parachute completely unhurt (house law — nothing can be lost). The theft
is impatience made literal, which reads to a four-year-old as "he wanted to see it NOW" rather than
"he took it", and the finale is a re-fuel rather than a chase-down. Painter = get inside the piece;
racer = parade the piece. Astronaut is the only act where the piece leaves the ground.

ASSET WISHES
- NEW (BLOCKING) `assets/opera/worlds/actors/mewsha_helmet.png` — Mewsha in a round fishbowl helmet,
  floating. Why: the helper appears in every station beat and there is currently NO 2D Mewsha stage
  art anywhere in the repo. `find assets -iname "*cat*"` returns only `assets/book/doll_cat.png`
  (a plushy) and `assets/art35/cards/mg/cat_*.glb` (3D cards, banned per owner's 2D-only rule).
  INTERIM REUSE: `assets/book/doll_cat.png` under a circular glass highlight will ship the act.
- NEW `assets/opera/worlds/actors/mewsha_helmet_meow.png` — second pose, mouth open, one paw
  pointing. Why: the leak-detector mechanic only reads if she can visibly point at the zero-g ring.
- NEW `assets/opera/worlds/actors/mewsha_in_rocket.png` — cat curled inside the rocket nose. Why:
  the act's biggest laugh needs one frame.
- NEW `assets/opera/worlds/props/rocket_parachute.png` — `goal_astronaut.png` under a small pink
  parachute. Why: on-screen proof that the premature launch cost nothing; this is what makes the
  steal non-scary.
- NEW set dressing `assets/opera/worlds/props/cosy_box_helmet.png` — the empty fishbowl on its side
  with a cat cushion, placed at the rocket pad for the swap.
- REUSE `goal_astronaut.png`, `rival_astronaut*.png` (13 poses), `world_astronaut.png`.

===============================================================================
ACT 12 — RACER — "The Opera Grand Prix"
===============================================================================
LOGLINE
Roshan races for the shell trophy that goes in the middle of her party table, cheered by the only
two people left in the grandstand — because everyone else is already at the Opera setting up.

HELPER — Harper & Fiona (the only two-friend slot; `harper.ogg` and `harper_win.ogg` are shipped,
`two_friends.png` is shipped, Harper's Kokoro voice exists so new lines are cheap)
WHAT THEY WANT: to be the loudest pit crew in the sea, for an audience of nobody.
THE CLEVER HOOK (Lamba-tier): THE CHEER IS THE FUEL. Turbo only fires when the crowd cheers — and
the grandstand is empty except for Harper and Fiona, because the whole reef is at the Opera laying
the party table. So the shipped `harper_win.ogg` clip is retimed to fire on every green TURBO tap:
the child hears her friend scream every single time she gets the timing right. The mechanic stops
being a timing bar and becomes "my friends' cheering makes me go fast." Payoff at the finale: the
grandstand fills, and the trophy Roshan lifts is handed up from the pit wall by Harper and Fiona —
Bible §6 already says "the trophy is what they hand her," so she never wins it, she is GIVEN it,
which keeps the making-my-own-party thesis intact.

BEAT SCRIPT (9 new lines + 3 shared/shipped lines)
1 [Roshan | ACT_OPEN]        "One more thing for my party! Tonight we drive home the shell trophy!"
2 [Imp Captain | SCUFFLE]    "Teehee! Tires! Wheels! Is the party starting? We can HEAR it!"
3 [Roshan | STATION_1 — the scallop-shell archway with the purple velvet starting-gate curtains]
                             "Curtains up at the gate! Harper, Fiona — you two are my pit crew!"
4 [Harper | STATION_2 — the blue arched pit-garage bays]
                             "Fresh wheels on! Fiona and I will cheer — cheering makes you fast!"
5 [Roshan | STATION_2 — TURBO]
                             "Two friends in the whole grandstand! Tap turbo when I hear them!"
6 [Imp Captain | STEAL]      "Look at me — victory lap! Trophy up! Everybody clap! Are we invited?"
7 [Maestro | FINALE_OPEN]    "Places, please! The Pearl Opera presents…"   (SHARED)
8 [Roshan | FINALE_MID — the stacked purple and teal tire depot]
                             "He's still waving! Loop the loop — big circles round the tire stacks!"
9 [Roshan | FINALE_MID — the purple-seated grandstand]
                             "Captain, you're good at waving — take the checkered flag and wave it!"
- [Harper & Fiona | FINALE_MID] `harper_win.ogg` (SHIPPED — no new clip, fires on the FINISH crossing)
10 [Roshan | CURTAIN_CALL — the scallop-shell trophy stage at the ramp summit]
                             "Trophy — on the table! Right in the middle, where everyone can see."
11 [Roshan | LOBBY_RETURN]   "On the table! What shall we make next?"   (SHARED)

Instruction layer preserved: line 5 quotes TURBO "Tap TURBO when the marker hits green!"; line 8
quotes LAP TWO "Loop the loop! Draw big racing circles!"; line 9 sets up FINISH "Tap the zoom strips
and cross the line!". The shipped win_line — "Roshan takes the Opera Grand Prix as the audience
waves checkered flags!" — now pays off line 9 exactly and needs no edit.

BIRTHDAY LINK (exact line):
  [Roshan | CURTAIN_CALL] "Trophy — on the table! Right in the middle, where everyone can see."

ESCALATION — how racer's imp trouble differs from its floor-mates
The Captain does not hide the piece — he PARADES it. He takes the shell trophy and drives a victory
lap he has not won, holding it over his head and waving at a two-person grandstand, rehearsing being
the guest of honour. It is the floor-3 "if we HOLD it, you have to let us come" posture at its most
public and most funny, and it is the only steal on the floor that Roshan answers by out-driving him
rather than out-making him. Painter = get inside the piece; astronaut = set the piece off; racer =
show the piece off. Three distinct verbs, one escalating want.

ASSET WISHES
- REUSE `assets/characters/friends/two_friends.png` — Harper & Fiona, per audit §5. Zero cost.
- NEW `assets/opera/worlds/actors/harper_fiona_pit.png` — the pair in matching pit-crew caps, one
  with a tire, one with a lollipop board, mouths wide open mid-cheer. Why: the entire act's affection
  hook is that these two are the ONLY people in the grandstand, so they must read at grandstand
  distance; `two_friends.png` is a portrait crop.
- NEW `assets/opera/worlds/props/grandstand_two_fans.png` and `grandstand_full.png` — an overlay for
  the purple grandstand, two fans at act open, swapped to a packed crowd in celebrate(). Why: "empty
  stand -> full stand" is the act's emotional arc told in one image with no dialogue.
- NEW `assets/opera/worlds/props/checkered_flag.png` — the Captain's job at line 9. Why: the
  give-him-a-job-not-an-invitation beat needs exactly one visible object, and the shipped win_line
  already mentions checkered flags.
- REUSE `goal_racer.png` (shell trophy), `rival_racer*.png` (13 poses), `world_racer.png`.

===============================================================================
IMPLEMENTATION NOTES — defects that block these three scripts
===============================================================================
1. CAPTION OCCLUSION IS WORSE THAN THE BIBLE STATES. Bible §1 flags `OperaLobby2D.layer = 35` vs
   `hud_layer` at default 0. The SAME defect exists inside every act:
   `opera_career_world_2d.gd:286` sets `layer = 38` and `:318-321` adds a full-rect
   `CareerWorldBackdrop`, while `main.gd:_build_hud()` (:3004-3007) creates `hud_layer` with no
   `layer` assignment (default 0) and puts `hud_msg` at Vector2(230, 590). Grep confirms neither
   `opera_career_world_2d.gd` nor `opera_act.gd` references `hud_msg` or mirrors a caption. Every
   spoken line in these three scripts will play its audio and draw its text BEHIND the painted
   world. Fix: the same ~8-line `story_caption` mirror the Bible prescribes for the lobby must also
   be added to `OperaCareerWorld2D.root`. Do not raise `hud_layer` globally.
2. IMP CAPTAIN SPEAKS IN THE CREW VOICE. `audio_director.gd:112` `if "imp" in w: return "imp"`
   matches "Imp Captain" first. All three acts give the Captain his three most important lines
   (SCUFFLE, STEAL, and the floor-3 want). Add `if "captain" in w: return "captain"` ABOVE the imp
   branch, and the `"captain": ("am_puck", 1.16, 0.94)` entry from Bible §8.
3. HELPER ATTRIBUTION ALREADY HAS A HOOK. `opera_career_world_2d.gd:727` reads
   `phase.get("speaker", "Roshan")`, exactly as nursery does with `"speaker": "Faron"`. Harper's
   line 4 ships by adding `"speaker": "Harper"` to the racer TURBO phase; Mewsha's meows by adding
   `"speaker": "Mewsha"` to the astronaut PATCH phase (`_speaker_key:107` already routes
   `mewsha`/`kitty`). No new plumbing.
4. ONE CAPTION SLOT, OVERWRITE SEMANTICS. Each station beat's story line and that phase's shipped
   instruction line compete for the same slot. Order must be: `say_sequence` story line on
   phase-enter, then the instruction line (or let the 9 s idle re-hint carry it). Otherwise the
   instruction clobbers the story mid-word.
5. THE FLOWER FRIEND HAS NO VOICE ROUTE. `_speaker_key` has no `flower` branch, so any line tagged
   to her would speak in Roshan's voice (`return "roshan"` fallback at :113). She is silent by
   design in this script, so nothing is required — but if a rustle/chime SFX slot is ever wanted,
   the branch must be added first.
6. RACER'S `trophy_shell` STATION IS ORPHANED (see geography section above). The curtain call in my
   script anchors there; without fix (a) or (b) the act never visits its own title landmark.
7. PAINTER WIN_LINE CONTINUITY. The shipped win_line — "Roshan's sunrise wins the paint-off and
   hangs in the gallery!" — now competes with "it goes up over my birthday cake". Minimal edit that
   keeps the shipped cadence: "Roshan's sunrise wins the paint-off — and hangs over her party!"
   Astronaut and racer win_lines need no change.
8. VOICE CLIP INVENTORY CHECKED: `assets/audio/voices/` has `harper.ogg`, `harper_win.ogg`,
   `everyone.ogg`, `imp_op_captain.ogg`. There is no `maestro_*`, no `captain_*`, no `mewsha_*`
   clip yet — the Maestro's FINALE_OPEN refrain is one new clip shared across all sixteen acts, and
   Mewsha needs meow SFX only, not TTS.

LINE BUDGET FOR THIS FLOOR SLICE: 27 new Kokoro lines (9 per act) + 1 shared Maestro refrain +
1 shared lobby-return refrain. Every line is 10-13 words, one idea, ear-first, no threat language,
no moral spoken, and every "Oh no!" resolves inside the same breath.
# FLOOR 3B ACT SCRIPTS — Nursery · Pop Star · Midnight Maestro

Source files read: `scripts/opera_career_world_2d.gd` (PHASES `:134-150`, FINALE_START `:153-167`, GOAL_PROPS `:173-187`, station assignment `:521-533`, audience `:604-619`, celebrate `:1185`), `scripts/opera_house.gd` (ACTS `:98-112`), `scripts/opera_stage_paths.gd` (popstar `:142-152`), `scripts/opera_act.gd` (boss engine `:6035-6318`), `scripts/opera_competition.gd` (`:102-118`), `scripts/audio_director.gd` (`:95-113`), `OPERA_NARRATIVE_AUDIT_2026-08-02.md` §4-5.

**Play order on floor 3 (verified `opera_lobby_2d.gd:16`):** `SHOW_INDICES[2] = [10, 11, 12, 15, 13]` → painter, astronaut, racer, **nursery (card 4)**, **popstar (card 5, the 13th and final party piece)**, then **Midnight Maestro (act 14, the boss, the last act of Chapter 2)**. My three acts are the last three things that happen before the party. That ordering is the spine of everything below.

---

# ACT 12 — THE MOONBEAM NURSERY (career `nursery`, act index 15)

**LOGLINE** — Roshan makes the star ceiling for her party, and to get it she has to learn the one thing she has never been good at: being quiet.

**BIRTHDAY LINK (exact line):**
> **Roshan: "That's my party ceiling! Now everyone's giggling — shhh, come back!"** *(trigger STEAL)*

The `goal_nursery` prop is canonically "a moonbeam star-mobile with three hanging plush charms" (`OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md:534-537`). It becomes the party's ceiling — hung over the table, so the three babies can sleep at the party instead of missing it.

## HELPER — Nurse Faron

**What she wants:** to come to the party. She is the only helper in the chapter with a standing reason she can't: somebody has to stay with the babies at bedtime, and that somebody is always her.

**The clever hook (three moves, all free):**

1. **The ceiling is the invitation.** A mobile is not a toy here — it is a roof. If Roshan hangs a sleeping-ceiling over the party table, the babies can come, which means Faron can come. The party piece isn't a decoration; it's an *access ramp for the one guest who was never going to make it*. That is the same shape as the Lamba trick — a prop whose meaning belongs to a second character, not to Roshan.
2. **The Captain has to whisper.** The whole chapter is built on his refrain "Are we invited?", always giggled at volume. This is the one act where he physically cannot be loud. The loudest character in the game asks the most important question in the game at a whisper, three cards before he gets his answer. The running gag inverted by the act's own dynamic — no new mechanic, no new art.
3. **The theft has no chase-gasp; it has a giggle-crisis.** The shipped BABY CHASE line is already *"The imp captain is playing peek-a-boo with the babies!"* — so the harm isn't loss, it's that the babies are now **awake and laughing**. Roshan cannot win this back by being louder. She wins it back by out-*quieting* him. That is the only act in sixteen where the solution is to make less noise, and a 4-year-old reads it instantly.

## BEAT SCRIPT (9 lines)

Station triggers below use the **proposed** nursery station names — `opera_stage_paths.gd` has **no `"nursery"` key** today (see ASSET WISHES #1), so Roshan currently walks the generic `FALLBACK_PATH` and no landmark can be named. Phase→station mapping follows `_assign_stations()` (`:521-533`, non-bop phases left-to-right): WASH HANDS=1, CATCH BABIES=2, FEED=3, [BABY CHASE=steal], BURP=4, BEDTIME=5. `FINALE_START["nursery"] = 5`, so BURP and BEDTIME are the on-stage finale.

| # | Line | Trigger |
|---|---|---|
| 1 | **Roshan** *(whispering)*: "One more thing for my party! Tonight we make the star mobile." | ACT_OPEN |
| 2 | **Imp Captain** *(whispering)*: "Teehee… shhh… we only wanted to LOOK at the babies. Honest!" | SCUFFLE |
| 3 | **Faron**: "Such gentle feeding. Somebody always stays at bedtime — that's usually me." | STATION_3 *(bottle-warmer kiosk)* |
| 4 | **Imp Captain**: "Peek-a-BOO! I've got the stars! …Are we invited?" | STEAL |
| 5 | **Roshan**: "That's my party ceiling! Now everyone's giggling — shhh, come back!" | STEAL |
| 6 | **Maestro** *(whispering)*: "Places, please. The Pearl Opera presents… very, very quietly." | FINALE_OPEN *(BURP, pillow drift)* |
| 7 | **Roshan**: "Sleepy imps, there's a blanket each. Snuggle in. Goodnight, everybody." | FINALE_MID *(BEDTIME, moonbeam dome)* |
| 8 | **Roshan** *(whispering)*: "Star ceiling — on the table! Faron, bring the cradles too." | CURTAIN_CALL |
| 9 | **Roshan**: "On the table! What shall we make next?" | LOBBY_RETURN *(bible §7 canon, verbatim reuse)* |

**Optional 10th** if a station-2 helper cheer is wanted: **Faron** | STATION_2 *(cradle pods)*: "Every baby caught. You have the calmest hands in the sea."

**Instruction layer stays untouched** — the shipped phase `voice` strings carry every "how". WASH HANDS ("Hold the bubbly basin…"), CATCH BABIES ("Slide the soft cradle under five falling babies! Pillows keep every miss safe."), BEDTIME ("Swipe the blankets down and tuck every sleepy baby into bed!") already speak in Faron's `speaker` slot at phases 2/3/6 — my story lines sit on top of, never over, those.

**Protect the silence.** STATION_1 (WASH HANDS) and STATION_2 (CATCH BABIES) carry **no** story line by design. This is the fewest story lines of any act in the house and that is the point — the audit's own note (`:309`) is "the nursery act is the proof case: its silences are the content." Line 6 is the single deliberate joke inside that quiet.

**Line 6 is also a house-law fix:** the Maestro's refrain-4 house call is canon in all 16 acts, and it is *funnier* whispered than it ever is at volume. Do not cut it to save the dynamic — the dynamic is what makes it land.

## ESCALATION — how the nursery's imp trouble differs

Floor 3 posture is FRANTIC ("if we HOLD it, you have to let us come"). Against its floor-mates:

- **painter / astronaut / racer** — take, run, brandish. Loud, public, chase-shaped.
- **NURSERY — the only *private, whispered, gentle* theft in the chapter.** He doesn't run. He can't: running wakes babies. He hides behind the cradle and plays peek-a-boo, which means **the crime is affectionate** and its damage is entirely acoustic. He asks the guest-list question in a whisper because he genuinely does not want to wake anybody — which is the first evidence in sixteen acts that the Captain is *kind*, planted immediately before the two acts where the audience decides how to feel about him.
- **popstar (next card)** — the exact inverse: loud, amplified, public, no hiding at all.

Nursery and popstar are consecutive cards and are deliberately built as a whisper/shout pair. Played back-to-back they are the Captain's crescendo into the party.

## ASSET WISHES — nursery

1. **`opera_stage_paths.gd` → new `"nursery"` PATHS entry — DATA, NOT ART, and it is the blocker.** The world painting **has landed** as tiles (`assets/opera/worlds/backdrops/world_nursery_c0r0..c1r1.png`, all four present; `opera_world_backdrop_2d.gd:98-101` prefers tiles over the merged key, so nursery renders today). Only the geography is missing. **The file's own header comment is now stale** — `opera_stage_paths.gd:11` still says nursery is "without a painting yet", as does `OPERA_STAGE_INTERACTION_2026-08-02.md:13`. Five stations, matching the painting spec in `OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md:523-529` (crescent-moon lamps, cradle pods, pillow drifts, bottle-warmer kiosk, star mobiles):
   - `moon_basin` — "crescent-moon lamp over the bubbly hand-basin at the nursery entry" (WASH HANDS)
   - `cradle_pods` — "row of three shell cradle pods with soft pillow drifts beneath" (CATCH BABIES)
   - `bottle_kiosk` — "bottle-warmer kiosk with a rack of warm bottles and a low stool" (FEED)
   - `pillow_drift` — "deep drift of cream and lavender pillows below the blanket rail" (BURP)
   - `moonbeam_dome` — "the star-mobile dome at far right where the moonbeams cross" (BEDTIME, destination)
   Also drop the nursery exemption in `probe_opera_2d.gd` once the entry lands.
2. **`assets/opera/worlds/actors/imp_captain_tiptoe.png`** — Captain on tiptoe, one finger to his lips, gold bow intact. Why: the whisper act needs exactly one silent visual gag, and this is the pose that teaches a non-reader the act's rule before a word is spoken. **REUSE fallback:** `imp_captain.png` (shipped) works; the tiptoe is the upgrade, not the requirement.
3. **`assets/opera/worlds/actors/faron_party.png`** — Faron out of her nursery apron, at the party. One card. Why: her want is stated in line 3 and paid off in line 8; the §4 party tableau needs to *show* she made it, or the payoff is invisible.
4. **REUSE — `assets/opera/worlds/nursery/baby_0..2.png`** as three sleeping guests under the mobile in the §4 party tableau. They are the reason the ceiling exists; the climax should have them in shot.
5. **REUSE — `assets/opera/worlds/props/goal_nursery.png`** for both the prop dock and the party-table shelf slot. No new art.
6. **REUSE — audience band already contains `mama_baby.png`** (`opera_career_world_2d.gd:608`). A mama-and-baby already sitting in the nursery act's crowd is a free callback; bounce that portrait, not a new one, on the BEDTIME finish.

---

# ACT 13 — THE STARLIGHT SOUND-OFF (career `popstar`, act index 13)

**LOGLINE** — Roshan makes the microphone she will sing Happy Birthday into, and finds out what a microphone is actually for when the imps unplug it.

**BIRTHDAY LINK (exact line):**
> **Roshan: "You heard me, Daddy! This microphone is for my birthday song!"** *(trigger STATION_2, dance pads)*

## HELPER — Daddy Mermaid (existing `daddy1-3.ogg` ONLY — sacred audio, no new recording)

**What he wants:** nothing. He is sitting in the front row. That is the whole part, and it is the strongest part in the act.

**The clever hook — this is the Lamba-quality one:**

**A microphone cannot be tested alone. It is only real when somebody hears you.** So SOUND CHECK is not aimed at a meter — it is aimed at one person in the front row, and the child learns the mic is working because **her actual father's actual recorded voice answers back.** Then MIC CHASE fires the shipped line *"The imp captain unplugged the microphone!"* — and **the answering stops.** The theft's consequence is not a missing object; it is a missing voice. A 4-year-old reads that with no words at all.

**And it costs nothing.** `_build_audience()` (`opera_career_world_2d.gd:604-619`) already places `assets/characters/friends/daddy.webp` as **audience[0], the leftmost, front-row portrait, in every career world including this one.** The hook is a ~4-line change: bounce `audience[0]` and fire `m._say("daddy", "", …)` on the SOUND CHECK completion, and again as the curtain-call button. Zero new art, zero new audio, and it converts the sacred-audio *constraint* into the act's entire mechanic — the design requires no specific words from the clip, only that a real dad noise comes back, which is precisely why it can't be Kokoro.

**Second hook — the refrain, amplified.** This is the last piece made and the last time the Captain asks his question. He does not run and he does not whisper. He takes the microphone, stands centre stage, and asks **the entire opera house, amplified**: *"ARE WE INVITED?"* The prop he stole is the one that makes the question audible to everybody — which is only possible in this act, and only meaningful because it's the last one.

**And Roshan does not answer him.** No line replies. Bible §7 refrain 3 is explicit: never answered for sixteen acts, answered once at §4 beat 6. The silence after an amplified question is the loudest moment in Chapter 2 and it is free.

## BEAT SCRIPT (9 authored lines + 2 archive cues)

Stations by name from `opera_stage_paths.gd:142-152`. **See ASSET WISHES #1 — the current auto-assignment is off by one landmark;** lines below are written to the corrected mapping and work under either.

| # | Line | Trigger |
|---|---|---|
| 1 | **Roshan**: "One more thing for my party! Tonight we make the microphone!" | ACT_OPEN |
| 2 | **Imp Captain**: "Teehee! Boom boom boom! We're the band nobody put on the poster!" | SCUFFLE |
| 3 | **Roshan**: "Testing, testing! Daddy — can you hear me in the front row?" | STATION_1 *(mic_row — "row of golden vintage microphone stands lining the music-note railing walkway")* |
| — | **Daddy Mermaid** — **[ARCHIVE CLIP: `daddy1.ogg`]**, `audience[0]` bounces | STATION_1 *(response)* |
| 4 | **Roshan**: "You heard me, Daddy! This microphone is for my birthday song!" | STATION_2 *(dance_pads — "circular stage plaza inlaid with four hexagonal arrow dance pads")* |
| 5 | **Imp Captain** *(booming, into the stolen mic)*: "ARE WE INVITED? Teehee — the whole opera house heard that!" | STEAL |
| — | *(no reply — one full beat of air. The refrain stays unanswered.)* | — |
| 6 | **Maestro**: "Places, please! The Pearl Opera presents the very last party thing!" | FINALE_OPEN |
| 7 | **Roshan**: "Imps on backup! La la la — everybody sings the encore!" | FINALE_MID *(rainbow_bridge — "S-curved rainbow road with gold pearl-topped railings and lamp posts")* |
| 8 | **Roshan**: "Microphone — on the table! My party has ALL its things!" | CURTAIN_CALL *(encore_balcony)* |
| — | **Daddy Mermaid** — **[ARCHIVE CLIP: a different one of `daddy1-3.ogg`]** as the final button | CURTAIN_CALL |
| 9 | **Roshan**: "My table is full! Now who will play the music?" | LOBBY_RETURN |

Line 7 reuses the audit's own popstar beat-6 (`:279`) verbatim — it is already approved and already the right line.

**Line 9 is the hand-off to the boss and it is structurally load-bearing.** Popstar completes the 13th and final table piece, but the chapter is not over: the Midnight Maestro is still unplayed. "Who will play the music?" is what makes the boss legible as the last missing *non-object* the party needs — it turns act 14 from an unexplained fight into the last errand. **It must replace the generic lobby-return line for this act only.**

**Continuity note for the Chapter-2 cliffhanger writer (free foreshadow, zero art):** the popstar encore happens on a **rainbow road** — and the Ember King's own shipped line is *"race the rainbow road DOWN to my fortress, if you dare!"* (`scripts/arena/sky_lagoon.gd:2534`). The last happy thing Roshan does before her party is sing on a rainbow road; the road she will later be dared down is the same shape. Worth a visual echo in the §5 crash. Do **not** spend a spoken line on it here — it should be recognised later, not explained now.

## ESCALATION — how the pop star's imp trouble differs

- The scuffle is the only one where the imps **make music** rather than break something: they drum the speakers (shipped line), i.e. they audition. Their want is stated as a poster credit — the most explicit "put us on the playbill" in the chapter, arriving last on purpose.
- The theft is the only one that is **not a removal but a hijack.** He doesn't take the mic away; he takes it and *uses it correctly*, for its actual purpose, better than anybody expected. He is not stealing a prop, he is stealing the floor.
- It is the only theft with an **audible** consequence rather than a visual one (Daddy stops answering).
- And it is the only one that goes **unanswered**. Nursery (whispered, private, kind) → popstar (amplified, public, unanswered) → the party (small, from the doorway, answered). Three cards, three volumes, one release.

## ASSET WISHES — pop star

1. **`station_for_phase` override for popstar — DATA FIX, one dict, no art.** `_assign_stations()` (`:521-533`) walks non-bop phases left-to-right, which currently gives: SOUND CHECK→`stage_curtain`, DANCE→`mic_row`, RHYTHM→`dance_pads`, ENCORE→`rainbow_bridge` — so **the sound check happens at a doorway, the dance happens at the microphone stands, and `encore_balcony` is never visited by anything.** Correct mapping: SOUND CHECK→`mic_row`, DANCE→`dance_pads`, RHYTHM→`rainbow_bridge`, ENCORE→`encore_balcony`. Cheap and it makes the walk read left-to-right as a career.
2. **`assets/opera/worlds/props/mic_cable_loose.png`** — a magenta cable lying unplugged on the deck, coiled, with a small sad spark. Why: the theft's consequence is audible; a 4-year-old needs its visual twin on screen for the two seconds the answering stops. Small prop card, standard navy-field 1024.
3. **REUSE — `assets/characters/friends/daddy.webp`**, already loaded as `audience[0]` (`:606`). No new portrait needed. Wish is **behavioural**: a bounce/glow tween on `audience[0]` timed to the clip, and the same portrait dimmed for the unplugged beat.
4. **REUSE — `rival_popstar*.png`** (11 shipped states: idle, bopped, bow, charge, flee, guard, hop_a/b, recover, slash, stagger, taunt, windup) for the mischief band. Nothing new required for the scuffle or the chase.
5. **REUSE — `assets/opera/worlds/actors/imp_captain_bow.png`** for the curtain call, and it is the same card the §4 party invitation beat uses. One asset, two payoffs, both shipped.
6. **REUSE — `assets/opera/worlds/props/goal_popstar.png`** for the prop dock and the 13th shelf slot.
7. *(Optional)* **`assets/opera/worlds/actors/imp_captain_mic.png`** — the Captain holding the stolen microphone in both hands like a trophy, mid-shout. Why: line 5 is the single most important imp beat in the chapter and it currently plays against a generic idle pose. Highest-value optional card on this floor.

---

# ACT 14 — THE GRAND FINALE / MIDNIGHT MAESTRO (act index 14, floor-3 boss)

**Mechanics verified** (`opera_act.gd:6037-6318`): `finale: true` forces `dual`, 15 HP, **3 lanterns** (the `lanterns` key is unset so `_build_boss` takes the default at `:6097` — the Shadow Phantom has 5, the Maestro has 3), and `_hit_boss` (`:6192-6207`) **alternates SHINE-a-lantern cycles with SPARKLE-at-a-peek cycles on every star** — the shipped intro line already calls this "use everything you've learned". Authored puppet `assets/art35/opera/opera_maestro.glb` is present. The stage is dressed with the real proscenium, curtains and apron (`:6044-6051`). Audience: four shipped cutouts — `pearl_friend`, `two_friends`, `mama_baby`, `wacky_chuck` (`:1405`).

## ROLE IN THE BIRTHDAY PREPARATION — he is THE MUSIC

The three floor bosses are the three things a party needs that aren't objects: the Dragon gave the **place**, the Phantom gave the **light**, the Maestro gives the **music**. Per bible §3 he has been the house announcer since line 5 of the chapter open and has said *"Places, please! The Pearl Opera presents…"* at the curtain-rise of every single act — **sixteen times, and never once been in one.** He is the imps' story told by a grown-up: the one member of staff who was never allowed on stage.

So his "theft" is the only one in the chapter that isn't a thing. He takes the **show**. And his crime is genuinely funny rather than threatening: he stands centre stage conducting an orchestra that **isn't there**. Nothing is lost, nothing is broken, nobody is chased — a conductor waving a baton at an empty house is a joke a 4-year-old gets on sight.

**Free motif, zero cost: the three lanterns are the three floors.** Lagoon Lights, Starlight Balcony, Grand Gallery — one lantern each. Lighting them is literally *"turn all the lights on in my party house,"* it re-uses the SHINE verb the child learned from the Phantom, and it installs the light that the Ember King blows out eight lines later in §5. Three lanterns, three floors, three guests, and the last one goes dark at the crash. No new art, no new mechanic — just naming what is already on screen.

## BEAT SCRIPT (7 lines)

| # | Line | Trigger |
|---|---|---|
| 1 | **Maestro**: "Sixteen shows I have announced. Tonight I shall be IN one!" | ACT_OPEN |
| 2 | **Roshan**: "My table is full! I only need the music now." | ACT_OPEN *(reply)* |
| 3 | **Maestro**: "One conductor, no orchestra, every show at once! Watch me!" | FINALE_OPEN *(first `shadow` cycle)* |
| 4 | **Roshan**: "One light for the Lagoon! The whole floor is singing along!" | FINALE_MID *(each `_light_lantern()` — vary the floor name per lantern: Lagoon / Balcony / Gallery)* |
| 5 | **Imp Captain** *(offstage)*: "Teehee! We know this song! …Are we invited to THIS?" | FINALE_MID *(after the second lantern)* |
| 6 | **Maestro**: "You lit my whole house. And everybody stayed to listen." | CURTAIN_CALL |
| 7 | **Roshan**: "Maestro, my party needs a bandleader. Will you conduct it?" | CURTAIN_CALL *(immediately before the shipped `win_line`)* |

Then the **shipped `win_line` finally speaks** (the D2 repair): *"The Maestro just wanted to conduct the grand finale — now the whole opera sings together!"*

**Line 5 must be an offstage voice cue — there is no imp sprite in this scene.** Verified: the backstage imp crew is gated behind the act's `shell` flag (`opera_act.gd:522`, `:547-548`), and the Maestro's ACTS entry sets no `shell`, so `_build_backstage()` never runs and `imp_count` is never used. Same staging as the chapter-open's line 7 ("offstage giggle") — a voice from the wings, no art required.

**Line 4 fires up to three times, once per lantern lit.** Each repetition names a different floor. The child has played all three; hearing her own floors called back one at a time as she relights them is the chapter's whole progress made audible in eight seconds.

## KIND RESOLUTION — consistent with the shipped `win_line`

Nobody wins and nobody is driven off. **Roshan gives him the baton back and gives him the one thing sixteen acts of announcing never got him: a job on the stage.** He doesn't want the show, he wants to *conduct* one — and Roshan has a party with no band. The last sparkle is not a hit, it is a handover.

That makes him **Guest 3** and the payoff is already written into §4 beat 8: *"Then let us play! Everybody — one, two, three…"* — he is the one who conducts Happy Birthday at the climax. The shipped `win_line` needs not one word changed; it becomes a description of the party rather than the end of a fight.

**House law honoured:** never defeated, never sad, never banished — offered a post. Same shape as the Dragon (cast as doorman) and the Phantom (cast as lantern-lighter).

## LOBBY_RETURN — a structural flag for whoever implements this

The Maestro is act 14 of 16 bits, and starring him is what completes `ALL_STARS`. Two ordering issues at the return site:

- `opera_house.gd:661-664` (all-stars branch) fires the §4 party. `:680` is the floor-boss branch whose bible §7 line is *"[Boss] is coming to my party! Look — a whole new floor!"* — **there is no fourth floor.** Floor 3's boss needs its own branch, or she announces a floor that doesn't exist a half-second before the party cutscene.
- Recommended floor-3 boss return line, which then hands straight to §4: **Roshan: "The Maestro is coming to my party — and the table is FULL!"**

## ASSET WISHES — Midnight Maestro

1. **REUSE — `assets/art35/opera/opera_maestro.glb`** (shipped, authored). No new boss art required; the primitive fallback at `:6054-6064` is unused.
2. **REUSE — `assets/art35/opera/opera_lantern.glb`** ×3 (shipped, `:6106`). No new art for the floor-lantern motif; it is a naming change in the spoken layer only.
3. **`assets/opera/worlds/actors/maestro_baton_offered.png`** — the Maestro holding his baton out, handle-first, small bow. Why: line 7 is a *handover*, and a handover with no image of a hand is invisible. One card; also serves the §4 party tableau where he conducts.
4. **REUSE — the four boss-stage audience cutouts** (`pearl_friend`, `two_friends`, `mama_baby`, `wacky_chuck`, `:1405`). Line 6 says "everybody stayed to listen" and the bodies to prove it are already on the benches.
5. **No `imp_*` art needed** for this act (see line 5 note) — offstage audio only.

---

# CROSS-ACT NOTES FOR THE IMPLEMENTER

**Voice routing — both bible §8 defects bite all three of my acts.** `audio_director.gd:95-113`: `if "imp" in w: return "imp"` (`:112`) matches **"Imp Captain"**, so every Captain line above — including the amplified refrain, the chapter's single most important imp beat — currently speaks in the crew's 1.38-pitch chirp. A `if "captain" in w: return "captain"` branch must sit **above** `:112`. `"Maestro"` (`:110`) and `"Faron"` (`:102`) and `"Daddy"` (`:103`) all route correctly today.

**Nursery-specific:** Faron already has a shipped miss reaction — `m._say("faron", "miss", 3.0)` at `opera_career_world_2d.gd:1136` on a dropped baby. Do not let a story line queue over it; her comfort noise on a miss is doing real work in the whisper act.

**Both careers:** the audit's D5 defect applies — the 9-second idle re-hint passes vo `"hint"`, which has no clip, so a stuck child hears a pitched "yay" instead of the repeated instruction. In the nursery specifically that pitched yay would also detonate the act's entire dynamic. Fix before shipping the whisper act.

**Caption occlusion does NOT affect these three acts** — the `hud_layer` layer-0 vs `OperaLobby2D` layer-35 bug (bible §1 item 3) only hides captions drawn over the 2D lobby. The two career worlds are their own CanvasLayers and the Maestro boss is 3D. The bug does hit the LOBBY_RETURN lines above.

**Word budget:** every authored line above is 8-13 words. Total new Kokoro lines for floor 3b: **25** (9 nursery + 9 popstar + 7 Maestro), minus the four refrain lines which are recorded once and reused across all sixteen acts, plus **2 archive Daddy cues (no recording)**.

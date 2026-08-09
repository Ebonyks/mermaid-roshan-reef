# CHAPTER 2 BIBLE — "Roshan Makes Her Own Birthday"
**Binding canon for all 16 Pearl Opera act writers.** Every decision below is final; the open questions from `OPERA_NARRATIVE_AUDIT_2026-08-02.md` §4 are answered here.

---

## 0. VILLAIN CONTINUITY RESEARCH — what already exists (read this first)

**The named antagonist for the lava planet ALREADY EXISTS: the EMBER KING.** Do not invent a new villain. Verbatim shipped canon:

- `scripts/ember_fortress.gd:6-32` — "THE EMBER FORTRESS — the Volcanic Throne Planet… in the spirit of the classic infernal citadel at the edge of space (generic homage — no branded characters)… **theatrical menace, zero real threat: lava only makes Roshan hop, nothing can be lost.**"
- `scripts/ember_fortress.gd:589-590` — "**THE EMBER KING himself**: the great dragon-turtle perched above his gate, huge and theatrical — **all growl, zero bite**."
- His shipped speaking lines (already written, already non-scary):
  - `scripts/arena/sky_lagoon.gd:2534` — "So! You found my dark door... race the rainbow road DOWN to my fortress, if you dare!"
  - `scripts/ember_fortress.gd:186` — "RRRUMBLE! Who dares visit my volcano fortress? Light my five lanterns... if you are brave enough!"
  - `:704` — "WHAT?! All five lanterns?! Fine, little mermaid... my GATE IS OPEN."
  - `:1106` / `main.gd:2847` — "**My little hero friend!** Play in my fortress as long as you like!" / "Come back and play in my fortress any time, little hero!"
- His fortress **is defended by imps**: `ROOMS[0]` = "**Cinder Gate Imps**", `ROOMS[3]` = "**Ash Imp Ambush**" (`scripts/ember_fortress.gd:77-83`). The final room is "The Molten Throne", a dual fire/ice fight — the King himself.
- Objective is **five ember lanterns** (`const LANTERNS := 5`), lit to open his Great Gate.
- Art discrepancy to note: the code comment says "dragon-turtle", but the approved concept brief (`assets_src/concepts/ember_fortress_claude_2026-07-22/PROMPTS.md:33-37`) says "**a friendly regal Ember King… an original broad volcanic guardian with a natural basalt crest, not a turtle, dragon, or branded character.**" The **concept art wins** — write him as a mountain that talks, not a dragon.

**The northern kingdom has NO antagonist.** `scripts/arena/northern_kingdom.gd` contains exactly three lines of dialogue (`:223`, `:228`, `:233`), all wonder, no threat. Chapter 3 is therefore free to be "go north to *learn*", which is exactly what the owner brief says. `WORLD_MAP_2026-07-27.md` §2 warns the Magic Cave seam to the north **is currently orphaned** (`main.gd:4013-4017` returns early, so `_populate_courtyard_touch_interactables` never runs) — chapter 3's entry must be restored before the cliffhanger can pay off.

**Verdict: the Ember King is the party crasher.** He is already the chapter-4 confrontation, he is already spooky-silly-never-frightening, he already commands imps, and his shipped ending is friendship — which satisfies house law ("nobody is ever defeated") without one new word of fiction.

---

## 1. CHAPTER OPEN — the handoff from Chapter 1

**Trigger:** first entry to the Opera when `m.opera_stars == 0`, replacing `opera_house.gd:191`.
**Delivery:** `m.say_sequence([...])` — **this helper already exists** (`main.gd:3234` → `audio_director.gd:49-78`), timer-advanced, touch-to-skip. The audit listed it as "to build"; it has since shipped.

**Minimal visuals required (precise):**
1. The **party table shelf** (§2) exists and is drawn with all 13 slots dark. That empty shelf IS the cutscene — it states the goal without a word.
2. The existing `_update_guide()` pulse (`opera_lobby_2d.gd:345-362`) sits on the chef card.
3. **BLOCKING DEFECT — must be fixed before any of this is visible:** `hud_msg` lives on `hud_layer`, a `CanvasLayer` with the **default layer 0** (`main.gd:3005-3007`), while `OperaLobby2D` sets **`layer = 35`** with a full-rect opaque `backdrop` (`opera_lobby_2d.gd:59, 70-73`). **Every spoken caption over the 2D lobby is currently drawn behind it.** Audio plays; text is invisible. Fix: add a `story_caption` Label to `OperaLobby2D.root` that mirrors `m.hud_msg.text`/visibility each `_process` (~8 lines, no global z-order side effects). Do NOT raise `hud_layer` globally.
4. Set `lobby_2d.accepting_input = false` for the duration of any story sequence, or the child can tap a card mid-line. There is no public setter; it is a plain var.
5. No sparkles. `m._sparkle_burst()` is a **3D** call (`opera_house.gd:168`) and produces nothing visible under the 2D lobby. Use the shelf pop and the guide pulse instead.

**THE SEVEN LINES:**

| # | Speaker | Line | vo |
|---|---|---|---|
| 1 | Roshan | "The whole castle is clean… and today is MY birthday!" | `talk` |
| 2 | Roshan | "My party is at the Pearl Opera House!" | `talk` |
| 3 | Princess Huluu | "Happy birthday, Roshan! Shall I have it all made for you?" | `talk` |
| 4 | Roshan | "No thank you! I want to make my OWN party." | `talk` |
| 5 | Maestro | "Then welcome to the Pearl Opera! Thirteen shows — thirteen party things!" | `talk` |
| 6 | Roshan | "Look — my party table is empty. Let's fill it up!" | `hint` |
| 7 | Imp Captain | *(offstage giggle)* "Teehee… a party? WE love parties…" | `talk` |

Line 3 is the whole thesis in one exchange: it is offered to her and she refuses, so making is a **joy she chose**, not a chore. Line 7 plants the imps before act 1 — the audit's beat-2 principle applied to the whole chapter.

---

## 2. THE PARTY TABLE — accumulation in the lobby

**Derived entirely from the shipped `m.opera_stars` bitmask. Zero new save keys.**

**The smallest presentation a 4-year-old reads instantly: a permanent gold shelf across the bottom of the lobby holding thirteen dark silhouettes that turn into full-colour party things, left to right.** No numbers, no words, no navigation.

**Spec (small, no new art):**
- Shrink the existing stage panel: `lower_stage` `Rect2(22, 142, 1236, 556)` → `Rect2(22, 142, 1236, 470)`; cards `y=48,h=336` → `y=40,h=300`; `boss_button` `(326,394,584,134)` → `(326,342,584,118)`.
- Add `PartyTable` panel at `Rect2(22, 624, 1236, 84)` via `StorybookUI.add_panel(..., StorybookUI.GOLD, ...)`.
- Thirteen `TextureRect` slots, 88×76, step 94, start x=25.
- **Textures already exist**: `assets/opera/worlds/props/goal_<career>.png` — all 13 verified present (`goal_chef`, `goal_detective`, `goal_ballerina`, `goal_candymaker`, `goal_doctor`, `goal_farmer`, `goal_boxer`, `goal_magician`, `goal_painter`, `goal_astronaut`, `goal_racer`, `goal_popstar`, `goal_nursery`), keyed by the shipped `GOAL_PROPS` dict (`opera_career_world_2d.gd:173-187`).
- **Slot order = `SHOW_INDICES[0] + SHOW_INDICES[1] + SHOW_INDICES[2]`** = `[0,1,2,3, 5,6,7,8, 10,11,12,15,13]`. This is a one-line concatenation and it makes the shelf fill strictly left-to-right in earn order.
- State: `made := (stars & (1 << act_index)) != 0`. Not made → `modulate = Color(0,0,0,0.22)` (flat dark shape, silhouette still readable). Made → `Color.WHITE`.
- On lobby return after a win (`opera_house.gd:669-685`), tween the earned prop from screen-centre down into its slot with a scale pop (~1.0 s). **That single animation is the entire reward.**

**The three bosses are NOT table pieces — they are GUESTS.** They are already displayed: `opera_lobby_2d.gd:209` writes the floor tab as `"%d  STAR"` when the boss is starred. One-line upgrade: show the boss's shipped emoji instead (`🐉`, `🌙`, `🎼`). Sixteen bits, sixteen readable things: thirteen on the table, three at the head of it.

Replace `progress_label` text `"STAR %d / %d"` with `"%d / 13"` plus a small cake glyph — or drop the counter entirely. The shelf is the counter.

---

## 3. IMP ESCALATION AND THE THREE FLOOR BOSSES

**Binding imp canon** (ratified from audit §3, re-pointed at the birthday): *The mischief imps are the opera's stage-struck little fans. Nobody ever put an imp on the playbill and nobody has ever invited them to a party. The scuffle is overexcited play; the theft is the Captain borrowing the party piece to start a party of his own. Roshan wins it back by out-performing him, and at the end she invites them.* Imps are never defeated, never sad, never banished. A bop is a tag-out.

| Floor | Imp posture | What the Captain says at the steal | Their want, escalating |
|---|---|---|---|
| **F1 — Lagoon Lights** (chef, detective, ballerina, candymaker) | **PLAYING.** They want to touch the party things. Pure curiosity, hands everywhere. | "Teehee! Is that for the PARTY? Let me hold it!" | "We want to join in." |
| **F2 — Starlight Balcony** (doctor, farmer, boxer, magician) | **COPYING.** They are building a rival party backstage — a crate for a table, borrowed costumes. Every steal now goes onto *their* table. | "We're having our OWN party! You weren't invited either!" | "Fine — we'll make our own." |
| **F3 — Grand Gallery** (painter, astronaut, racer, nursery, popstar) | **FRANTIC.** They can hear the real party being laid out. They take the biggest pieces and hold them like a ticket. | "If we HOLD it, you have to let us come… right?" | "Please. Just say we can come." |

By act 13 the Captain has stopped hiding it, which makes the climax invitation land as a release, not a surprise.

**The three bosses are the three things a party needs that are not objects:**

| Boss | Act | What he does in the preparation story | Becomes |
|---|---|---|---|
| **Curtain Dragon** (F1) | 4 | **THE PLACE.** The party needs the big stage, and a grumbly dragon is asleep in the curtains. He is not evicted — he is *cast*. Shipped win_line already lands it: "he just wanted to be in the show!" | The party's **curtain-puller and doorman**. Guest 1. |
| **Shadow Phantom** (F2) | 9 | **THE LIGHT.** The balcony is dark. Lighting his lantern lights the whole floor. Shipped win_line: "the shadow was a lonely little phantom — now he's the star of the curtain call!" **This is the act that installs the light motif the Ember King later blows out.** | The party's **lantern-lighter**. Guest 2. |
| **Midnight Maestro** (F3) | 14 | **THE MUSIC.** He has been the Opera's announcer in every act since line 5 of the chapter open (see §8). At the finale he stops announcing and finally conducts. Shipped win_line: "the Maestro just wanted to conduct the grand finale!" | The party's **bandleader** — he conducts Happy Birthday at the climax. Guest 3. |

This answers the audit's open question §4 decisively: **option (c) — the Maestro is the house host from act 1.** His act-14 "wants to steal the whole show" now lands as the one member of staff who was never allowed on stage, mirroring the imps exactly.

---

## 4. THE PARTY — the climax

**Trigger:** the existing `m.opera_stars == ALL_STARS and not m.opera_done` branch in `opera_house.gd:661-664` — the same site that already sets `opera_done`, adds 50 pearls and awards the `"showtime"` sticker. Replace the single line at `:682` with the sequence.

**Visual, zero new art:** all 13 shelf slots pulse to full brightness in a left-to-right ripple; `backdrop` tweens to a warm gold; the three floor tabs show their boss emoji; `assets/opera/worlds/actors/imp_captain_bow.png` (**already shipped**) fades in centre-stage for the invitation beat.

| # | Speaker | Line |
|---|---|---|
| 1 | Maestro | "Ladies and gentlefish — the Pearl Opera presents… **Roshan's birthday party!**" |
| 2 | Roshan | "Everything on the table — and I made ALL of it!" |
| 3 | Princess Huluu | "The whole reef came, Roshan. Look at them all." |
| 4 | Evie | "Lamba wants to sit next to the cake!" |
| 5 | Imp Captain | *(small, from the doorway)* "…Are we invited?" |
| 6 | Roshan | "**Imps — you're invited.** Come and sit down. There's a bag for every one of you." |
| 7 | Imp crew | "TEEHEE!" *(the whole crew tumbles in)* |
| 8 | Maestro | "Then let us play! Everybody — one, two, three…" |
| 9 | Everyone (`everyone.ogg`, shipped) | *(the group cheer)* |
| 10 | Daddy Mermaid | *(one existing `daddy1-3.ogg` clip as the final button — NO new recording)* |

Beat 6 is the payoff of the Captain's 16-act refrain. It is enacted, never explained — no character says the lesson (audit trap 1).

---

## 5. THE CRASH — the cliffhanger

**Who arrives: the EMBER KING** (existing canon, §0).

**He is never seen.** No new art is required and the reveal is preserved for chapter 4. The child hears a huge voice and watches the light go out. This is the single most important non-scary decision in the chapter: what a 4-year-old cannot see, she cannot be frightened of, and the visual grammar — someone blowing out candles — is a birthday grammar she already owns.

**Visual (three tweens, zero new assets):**
1. `backdrop` tweens to `Color(0.06, 0.03, 0.05)` over 1.2 s.
2. `GoldProsceniumRail` (`opera_lobby_2d.gd:79-85`) tweens gold → `Color(1.0, 0.45, 0.15)`.
3. Every party-table slot dims to 35 % — **the shelf keeps its thirteen things; only the light is taken.** Then the backdrop returns to normal after he leaves, and the shelf relights. The lobby stays fully playable.

**What he does:** he blows out the birthday candles. He takes the candles home. He takes nothing else and hurts nobody.

| # | Speaker | Line |
|---|---|---|
| 1 | Ember King | *(a huge, slow rumble)* "RRRUMBLE… a party. **Nobody ever invited ME to a party.**" |
| 2 | Ember King | *(one long puff — every light goes out)* "So I shall take the candles. Every… single… one." |
| 3 | Roshan | "Hey! Those are MY birthday candles!" |
| 4 | Ember King | "Then come and get them, little mermaid — **all the way to my fire mountain.**" *(gone)* |
| 5 | Imp Captain | "We know him! That's the Ember King — **our cousins live at his gate.**" |
| 6 | Princess Huluu | "Nobody in the reef knows the way to a fire mountain." |
| 7 | Rosalina | "But the old folk in the **far north** do. Past the mountain pass, Roshan." |
| 8 | Roshan *(last line of Chapter 2)* | "**Then we're going north — and I'm getting my candles back.**" |

**Continuity payoffs, all using shipped content:**
- Beat 5 is `ROOMS[0]` "Cinder Gate Imps" and `ROOMS[3]` "Ash Imp Ambush" cashed in. The imps are not only invited — they are the ones who know the way. Their arc pays off twice and they become chapter 3's travelling companions.
- **Roshan's five birthday candles ARE the Ember Fortress's five lanterns** (`const LANTERNS := 5`, `scripts/ember_fortress.gd:33`). Chapter 4's shipped objective — light five lanterns to open the gate — becomes "get my candles lit and take them home." Zero mechanical change; enormous narrative gain. *(Owner call: if Roshan is turning four, make the fifth lantern the King's own and he lights it himself at the end. Both readings work.)*
- Chapter 4's shipped ending needs no rewrite: "how to stop him" turns out to be **"invite him."** `main.gd:2847` already says "Come back and play in my fortress any time, little hero!"
- **Chapter 3 blocker:** the Magic Cave / mountain-pass seam is orphaned today (`WORLD_MAP_2026-07-27.md` §2, `main.gd:4013-4017`). Beat 7 promises a road that currently does not exist. Restoring it is a chapter-3 precondition, not a polish task.

---

## 6. THE 13 PARTY JOBS

Every line: **piece → friend → why that friend.** Twelve distinct helpers; Evie deliberately doubles.

| # | Act | Career | Party piece | Friend | Why that friend |
|---|---|---|---|---|---|
| 1 | 0 | Pastry Chef | **the birthday cake** | **Kareem** (`shop`) | He sells cakes. She refuses to buy one and he becomes her ingredient supplier and taste judge — the chapter's thesis dramatised in act 1. |
| 2 | 1 | Detective | **the pearl tiara** = the birthday crown | **Princess Huluu** | It is HER tiara, lent for the day, and it goes missing — she is client and gift-giver at once. |
| 3 | 2 | Ballerina | **the music box** = the party's dancing music | **Rosalina** | The dreamy keeper winds it and teaches the dance Roshan will actually dance at the party. |
| 4 | 3 | Candy Maker | **wrapped candy** = the party bags | **Sparkle** (baby eagle, chirps only) | A bird stealing sweets off the line reads instantly at four; the counting game is one bag per guest. |
| 5 | 5 | Stuffie Surgeon | **the mended starfish plushy** = a present | **Evie** | It is Evie's starfish and it arrived torn. Roshan mends it — **which is why Evie trusts her with Lamba three acts later.** |
| 6 | 6 | Farmer | **the fed piggy** = the guest of honour | **Chuck** (existing barks/whimpers ONLY — sacred audio) | A herding dog needs no dialogue; the whole act is barks and piggies, the most wordless act on floor 2. |
| 7 | 7 | Boxer | **the championship belt** = the birthday sash | **Wacky** (corner coach) | A grandpa chuckle in the corner keeps a boxing match unmistakably silly. |
| 8 | 8 | Magician | **Lamba's reveal** = the party's big trick | **Evie + Lamba** | The owner's own quality bar: Lamba is the vanishing subject while Evie watches from the stage — and act 5 already earned that trust. |
| 9 | 10 | Painter | **the framed sunrise** = the party banner | **Flower Friend** (silent by design) | She IS the painting. The muse never speaks and never needs to. |
| 10 | 11 | Astronaut Engineer | **the rocket** = the party firework | **Mewsha** (meows only) | The ship's cat in a fishbowl helmet. A cat in a spacesuit is a complete joke with no dialogue. |
| 11 | 12 | Racecar Driver | **the shell trophy** = the party centrepiece | **Harper & Fiona** (`harper_win.ogg` shipped) | The pit-crew cheer duo; the only two-friend slot, and the trophy is what they hand her. |
| 12 | 15 | Nursery Nurse | **the star mobile** = the party's ceiling | **Nurse Faron** (shipped co-op) | Already built. The whisper-dynamic act — its silences are the content; protect them. |
| 13 | 13 | Pop Star | **the microphone** | **Daddy Mermaid** (existing `daddy1-3.ogg` ONLY — sacred) | The last piece made is the thing she sings Happy Birthday into, with her father in the front row. Deliberately the final card on floor 3. |

Sacred-audio constraint honoured: Daddy and Chuck perform entirely with existing clips. `assets/audio/voices/` contains `daddy1-3.ogg`, `chuck.ogg`, `chuck_bark.ogg`, `chuck_whimper.ogg`, `everyone.ogg`, `harper_win.ogg` — all verified present.

---

## 7. COHESION MOTIFS

**Four refrains. Verbatim every time. Ritual sameness is the feature — by act 3 the child says them with the game.**

1. **THE PARTY-LIST REFRAIN** — Roshan, opening every act (audit beat 1): *"One more thing for my party!"* → then the specific: *"Tonight we make the [piece]!"*
2. **"ON THE TABLE!"** — Roshan, at every curtain call (audit beat 7), immediately before the shipped `win_line`: *"[Piece] — **on the table!**"* This is the phrase the child will shout. It is also the audio cue timed to the shelf-pop animation.
3. **THE GUEST-LIST CALLBACK** — the Imp Captain, once per act, at the steal: *"**Are we invited?**"* Never answered for sixteen acts. Answered once, at §4 beat 6. This is the single strongest through-line in the chapter and the reason the climax has emotional weight instead of just confetti.
4. **THE MAESTRO'S HOUSE CALL** — the Maestro, at every curtain-rise (audit beat 5), verbatim: *"**Places, please! The Pearl Opera presents…**"* Plus the shipped imp *"Teehee!"* as the fifth, already-recorded ritual.

**What the lobby says between acts** — replaces `opera_house.gd:684` (and kill the double-"Yay!" defect D3 while you are in there):
- Normal return: **Roshan: "On the table! What shall we make next?"**
- After a floor boss (`:680`): **Roshan: "[Dragon/The phantom/The Maestro] is coming to my party! Look — a whole new floor!"**
- Idle re-hint in the lobby: **Roshan: "My table isn't full yet! Tap a picture!"** *(fix vo `"hint"` — audit D5 confirms `"hint"` has no clip and currently plays a pitched "yay")*

---

## 8. TTS VOICE RECOMMENDATIONS

Roster in `tools/make_voices.py:19` fetches eleven Kokoro voices. Nine are assigned (`CHARS`, `:31-42`). **Exactly two are unused: `af_sky` and `am_michael`.**

| New role | Recommended `CHARS` entry | One-line justification |
|---|---|---|
| **The Maestro** (house announcer, revealed as the act-14 Midnight Maestro) | `"maestro": ("am_michael", 1.00, 0.96)` | The last wholly-unused male model, given the **unprocessed** read because he speaks in all 16 acts — the highest-mileage new voice in the game deserves the cleanest signal. Distinct from George's British shopkeeper and Santa's grandpa. |
| **Imp Captain** (own slot, split from the crew) | `"captain": ("am_puck", 1.16, 0.94)` | Same actor as his crew (`imp` at 1.38/1.08) so he audibly *is* one of them, but lower and slower = the ringleader. Zero new model, and it satisfies the audit's demand for a captain slot distinct from Sparkle's 1.55 chirp. |
| **Ember King** (the crasher) | `"ember": ("am_santa", 0.72, 0.88)` | The deepest available model, shifted hard into a mountain that chuckles — grandpa DNA underneath is precisely why he reads as *big and silly* rather than frightening. Wacky at 0.98 vs the King at 0.72 is a wider gap than the shipped `evie` 1.30 / `sparkle` 1.55 pair the game already accepts. **Fallback if the owner hears Wacky in it:** `("af_sky", 0.66, 0.86)` — the other unused model; a heavily-lowered female read gives a stony, genderless rumble. |
| **Mewsha** (astronaut) | none — meow SFX only | Owner canon; `_speaker_key` already routes `"mewsha"`/`"kitty"`. |
| **Flower Friend** (painter) | none — silent by design | She is the painting. |

**Two code defects blocking the above** (`scripts/audio_director.gd:95-113`):
1. `if "imp" in w: return "imp"` matches **"Imp Captain"**, so the Captain speaks with the crew voice. Add `if "captain" in w: return "captain"` **above** the imp branch.
2. `"Ember King"` matches nothing and falls through to `return "roshan"` — **the Ember King currently speaks in Roshan's voice.** Add `if "ember" in w or "king" in w: return "ember"`.
Good news: the two latent bugs the audit flagged are already fixed — `:110` has a `maestro` branch and `:111` has `kareem → shop`.

**Line budget:** the audit's 75-85 line estimate stands for the 13-act spine. Chapter 2 adds ~30 more: 7 chapter-open, 10 party, 8 crash, plus the four refrains (which are recorded once and reused verbatim in all 16 acts — that is the whole point of ritual). Total ≈ 115 new Kokoro clips, well inside the pipeline's "80 lines ≈ 15-30 min CPU, 2-3 MB" measurement.

---

## KEY FILE PATHS

- `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/scripts/opera_house.gd` — ACTS roster, `_act_won` (climax trigger at `:661-664`), lobby-return lines `:669-685`
- `.../scripts/opera_lobby_2d.gd` — the Canvas hub; party table goes here; `layer = 35` occlusion bug at `:59`
- `.../scripts/opera_career_world_2d.gd` — `PHASES` `:36`, `GOAL_PROPS` `:173-187`
- `.../scripts/audio_director.gd` — `say_sequence` `:49`, `_speaker_key` `:95-113` (two branches to add)
- `.../scripts/main.gd` — `hud_msg` on layer-0 `hud_layer` `:3005-3041`; `opera_stars`/`opera_done` `:288-290`
- `.../scripts/ember_fortress.gd` — Ember King canon `:6-32`, `:44`, `:589-590`, `:704`, `:1097-1110`; `LANTERNS := 5` `:33`
- `.../tools/make_voices.py` — `CHARS` `:31-42`; fetch list `:19`
- `.../assets/opera/worlds/props/goal_*.png` — all 13 party pieces, shipped
- `.../assets/opera/worlds/actors/imp_captain_bow.png` — the invitation beat, shipped
- `.../OPERA_NARRATIVE_AUDIT_2026-08-02.md` — the 7-beat spine this bible sits on top of
- `.../WORLD_MAP_2026-07-27.md` — the orphaned northern seam chapter 3 needs

# Pearl Opera narrative audit — 2026-08-02 (analysis only)

Owner brief: gameplay is now strong, narrative is weak — it is unclear WHY
Roshan scuffles with the imps and what her goal is in each show; helpers
and spoken dialogue are candidate remedies. This audit determines what
would strengthen the interactions. **Nothing here is implemented.**

Method: five parallel audit lenses over the shipping code and docs —
(1) the story as literally heard today (every TTS line in play order),
(2) imp lore across the whole game, (3) helper casting from the existing
character roster, (4) a preschool story-spine design, (5) the dialogue
plumbing's real capabilities and limits. This document is the synthesis.

---

## 1. Verdict

The acts mechanically dramatize a complete story (imps intrude, the
captain steals the goal prop, the finale wins it back, everyone bows) —
but almost none of it is SPOKEN, so a non-reader never learns why any of
it happens. Roshan never states a want, the imps never state theirs, the
theft has no stakes line, the finale win is a generic "Yay! I did it!",
and the family never reacts. The fix is not new mechanics: it is a thin,
ritualized layer of spoken beats delivered by characters the child
already loves — plus repairing seven delivery defects where authored
narrative already exists but never reaches her ears.

## 2. Verified narrative-delivery defects (authored story that never plays)

| # | Defect | Evidence |
|---|--------|----------|
| D1 | The 13 rich per-act intro scripts (ACTS voice) NEVER fire on the shipping path — OperaAct.start() returns before the show_msg call. The child's first line of every act is "Mischief imps grabbed the spoons!" with zero setup. | opera_act.gd:537-540 vs :592 |
| D2 | The authored win_line texts are captioned but never spoken — vo event "win" plays generic roshan_win.ogg ("Yay! I did it!"). | opera_act.gd:7038-7048 |
| D3 | "Yay! I did it!" then plays a SECOND time ~3.5 s later when the lobby-return line overwrites the curtain caption. | opera_house.gd:669-684 |
| D4 | The per-career contest goal sentences ("Finish the brightest celebration cake") are defined but read by no code at all. | opera_competition.gd CAREERS |
| D5 | The 9 s idle re-hint — fired exactly when the child is stuck — passes vo "hint", which has no clip: she hears a pitched "yay" instead of the repeated instruction. | opera_career_world_2d.gd:1187 |
| D6 | The imp captain, the emotional engine of every act, has ONE shared line in the whole game; the steal moment itself is silent for him. | make_voices.py; _show_phase steal branch |
| D7 | celebrate() is vocally empty — confetti and tweens, no one says anything during the curtain call itself. | opera_career_world_2d.gd:1019-1058 |

These seven are the highest value-per-effort narrative wins available:
most are one-call-site changes that unlock already-written story.

## 3. The canon: who the imps are and why Roshan meets them

Three independent canon lines converge (boss win_lines; every scuffle
verb being a game — juggling, bouncing, peek-a-boo; the theft running
TOWARD the stage in costume):

> **The mischief imps are the opera's stage-struck little fans. They love
> the shows so much they cannot wait for them. The scuffle is overexcited
> play; the theft is the captain borrowing the star prop to start the
> show himself — because nobody ever put an imp on the playbill. The
> resolution is that Roshan casts them: the finale is the imp finally IN
> a show, and the curtain call is everyone bowing together.**

This is exactly the sentence-shape the three floor bosses already own
("The dragon isn't grumbly anymore — he just wanted to be in the show!").
House rules that follow: imps are never defeated, never sad, never
banished — a bop is a tag-out; the rival contest is a duet wearing an
opponent costume; "everything borrowed for the show comes back, and
everyone who wants in gets a bow." The dormant opera_pantry
RESCUE->GIFT fiction contributes its gratitude canon (helpers gift
Roshan things for the show) without reviving any mechanics.

Roshan's own want per act: perform tonight's show for the family (the
audience row IS the family). Every act needs her to say so in one breath
at the start — that is defect D1's repair.

## 4. The recommended story spine (7 spoken beats, fixed speaker slots)

Ritual sameness is the feature: by the third act the child narrates the
structure herself. Per-act line budget ~6-8 short ear-first lines.

| # | Beat | Speaker | Moment | Shape |
|---|------|---------|--------|-------|
| 1 | Arrival want | Roshan | act start | "Tonight we [job verb] [thing] for [someone]!" |
| 2 | Kind imp hello | Imp Captain | at the scuffle | giggle + a relatable want ("Cake smell! We're SO hungry!") — lands BEFORE the theft so the theft reads as wanting, not menace |
| 3 | Helper cheer | the act's helper | first station done | names the action just done + warm push ("Lovely stirring, little chef!") |
| 4 | Theft stakes | Roshan | the steal | gasp-into-giggle + what the prop is FOR — purpose, never peril |
| 5 | Finale frame | host slot (see open question) | curtain rises | "Show everybody your [skill]!" — the crowd is the goal, the rival a duet partner |
| 6 | Inclusion | Roshan invites, imps chirp | finale resolves | the beat-2 want granted on stage ("Imps, grab a spoon — everyone helps frost!") |
| 7 | Family pride | win_line voice + Hooray | curtain call | the authored win_lines, finally spoken; sacred daddy clips as the final button where they fit |

Rules: 8-14 words per line; praise actions, not the child; the scuffle
itself stays wordless (giggles/boings are SFX); silence between beats is
fine. Traps to avoid: moralizing, threat language, unexplained
competition.

**Open question for the owner:** the spine proposes a warm ringmaster
"Maestro" voice for beat 5. The Midnight Maestro is also the act-15 boss
the child has not met yet on floors 1-2. Options: (a) let the act's
helper deliver beat 5, (b) introduce a separate unnamed Announcer voice,
(c) embrace the Maestro as the house's host from the start (which makes
his act-15 "wants to steal the whole show" land harder). Needs a call
before any dialogue pass.

## 5. Helper casting (one per career, from the existing roster)

The nursery's Nurse Faron is the proven model: costumed actor on stage,
named HUD plate, her own TTS lines. Castings graded against it:

| Career | Helper | Role | Voice cost | Art cost |
|---|---|---|---|---|
| Chef | Kareem the shopkeeper | task-giver / taste judge | new Kokoro lines (voice exists) | NEW kareem_chef.png |
| Detective | Princess Huluu (it is HER tiara) | on-stage client | new Kokoro lines | reuse huluu.png as-is |
| Ballerina | Rosalina | recital mentor | new Kokoro lines | NEW rosalina_ballet.png |
| Candymaker | the whole audience row | cheer collective | everyone.ogg exists | none |
| Doctor | Evie (the patient IS Lamb-a') | worried plushy-parent | new Kokoro lines | NEW evie_scrubs.png |
| Farmer | Chuck the dog | herding dog | EXISTING bark/whimper only (sacred) | crop of wacky_chuck.png |
| Boxer | Wacky | corner coach (keeps boxing silly) | new Kokoro lines | NEW wacky_corner.png |
| Magician | Mewsha the cat | silent familiar | meow SFX only | NEW mewsha_topcat.png |
| Painter | Flower Friend | silent muse (she IS the painting) | none by design | reuse as-is |
| Astronaut | Sparkle the baby eagle | chirping mascot | chirps only | reuse baby_eagle.png (v1) |
| Racer | Harper & Fiona | pit-crew cheer duo | harper_win.ogg exists | reuse two_friends.png |
| Pop Star | Daddy Mermaid | front-row spotlight | EXISTING daddy1-3.ogg only (sacred) | reuse daddy.webp |
| Nursery | Nurse Faron | co-op partner | shipped | shipped |

Sacred-audio constraint honored throughout: daddy*/chuck* recordings are
never regenerated; those two helpers perform entirely with existing
clips. Two latent bugs to note for any implementer: _speaker_key has
no "kareem"->"shop" branch, and SPEAKER_PORTRAIT maps evie to Faron's
portrait.

## 6. What the dialogue plumbing can and cannot do (verified)

Already works: per-phase clips in per-speaker voices (92 opera clips
shipped), per-key cooldowns, music ducking, the phase-gap touch-skip
pattern, a dedicated imp voice, a TTS pipeline where 80 new lines cost
~15-30 minutes of CPU and ~2-3 MB.

Hard limits for a story pass: ONE caption slot with overwrite semantics
(no two-line exchanges possible today); no priority rules (the idle
re-hint can clobber a story line); voices never stop early (overlap at
act-win is already audible); celebrate() has no voice slot.

Smallest sufficient additions (est. 40-80 lines of GDScript total, no
architecture change): a say_sequence(lines) helper (timer-advanced,
touch-to-skip, suspends the re-hint), a per-act opening call site, a
win_vo slot with the lobby double-line suppressed, captain steal/pop
lines at the existing hooks, and the one-line D5 re-hint fix.

Line budget for the full 13-act pass: ~52 minimal, ~75-85 comfortable
(opening pairs, captain steal + grumble, voiced win_lines, ~5 shared
captain personality lines, helper cheers). Replay friction control:
auto-skip the opener once the act has a star (mirror first_time in
_act_won).

Risks: probe pump guard (every beat must be one-touch skippable, never
audio-gated — headless has no audio device); ~10-12 s added per first
run; caption churn if sequences do not suspend hints; keep shared captain
lines to ~5 variants so he stays a character, not a jingle.

## 7. Prioritized recommendations (not implemented)

| P | Work | Value | Effort |
|---|------|-------|--------|
| P0 | Fix D1-D7 (fire the intros, voice the win_lines, kill the double-yay, voice the re-hint, speak the contest goal, captain steal line, curtain-call voice slot) | Unlocks already-written narrative everywhere | small, code-only + ~30 TTS lines |
| P1 | say_sequence helper + the 7-beat spine data for all 13 acts (~80 lines TTS incl. captain personality set) | The full why/stakes/inclusion arc | moderate |
| P2 | Helper pass: cheer-row helpers first (zero art: Huluu, Daddy, Harper, Everyone, Flower Friend, Sparkle, Chuck) then the 5 new costumed portraits via codex | Warmth + relationships on stage | moderate + codex art |
| P3 | Curtain-call inclusion staging (imps join the bow visually; prop-return handled by imps) + pantry-gratitude VO flavor | Completes the canon loop | small-moderate |

Decision needed from the owner before implementation: the beat-5 host
question (helper vs Announcer vs Maestro), and approval of the imp canon
sentence in section 3 as the binding fiction.

---

## Appendix — full 13-career spine drafts (beat-by-beat example lines)

## THE 13 CAREERS — one example line per beat

Lines marked (reuse) keep or trim shipped text.

**1. PASTRY CHEF** (prop: the celebration cake)
1 Roshan: "Chef hat on! Tonight we bake the party cake for the whole reef!" (reuses "Chef hat on!"; the shipped 30-word six-step arrival line is over budget — the steps move to their own station beats, which `_say()` already supports)
2 Imp: "Teehee! Cake smell! We're SO hungry!"
3 Farmer friend (Wacky): "Lovely stirring, little chef! Our carrots make it extra yummy!"
4 Roshan: "Oh! The cake is for the party — everybody gets a slice, even imps!"
5 Maestro: "Places, please! Show the whole crowd how a chef bakes!"
6 Roshan: "Imps, grab a spoon — everyone helps frost the cake!"
7 (reuse): "The farmers' carrots made it a CARROT cake — the best one the reef has ever tasted!" + Hooray.

**2. DETECTIVE** (prop: the sparkly tiara)
1 Roshan: "Detective Roshan is on the case! Tonight we find the sparkly tiara!" (reuse)
2 Imp: "Teehee! Sparkly! We want to look fancy too!"
3 Stagehand (Shop): "Good peeking! Our lanterns will light the dark corners for you."
4 Roshan: "The tiara is for the show queen's bow — let's follow the glittery footprints!"
5 Maestro: "The crowd is watching, Detective! Show them how you solve it!"
6 Roshan: "You just wanted a turn! Everyone wears the tiara at the bow!" (keeps the redesign's "only borrowing it" happy ending)
7 (reuse): "Case closed! The tiara sparkles for the whole reef!" + Hooray.

**3. BALLERINA** (prop: the curtain-call bouquet)
1 Roshan: "Ballerina twirl! Tonight we dance the big recital for everyone!" (reuses "Ballerina twirl!")
2 Imp: "Teehee! Twirly! We want to dance too!"
3 Dancer (Huluu): "Beautiful steps! Take my ribbon — it loves to twirl with you."
4 Roshan: "That bouquet is for the final bow — every dancer gets a flower!"
5 Maestro: "Curtain up! Show everybody your biggest, twirliest twirl!"
6 Roshan: "Dancing imps! Come twirl the last dance with me!"
7 (reuse verbatim): "What a beautiful dance! The whole reef is clapping!" + Hooray.

**4. CANDYMAKER** (prop: the parade cart)
1 Roshan: "Candy Maker Roshan! Tonight we fill the parade cart with smiley candies!" (reuses opener)
2 Imp: "Teehee! Sweeties! Our tummies are rumbly!"
3 Sugar mouse (Sparkle chirp): "Squeak! Lovely wrapping! Here's more sugar for the pot!"
4 Roshan: "The candy cart is for the parade — one sweetie for every friend!"
5 Maestro: "Start the parade! Show the crowd your rainbow candies!"
6 Roshan: "Imps, push the cart with me — parade helpers get candy first!"
7 (reuse verbatim): "Nine smiley candies! The sweetest show the reef has ever tasted!" + Hooray.

**5. DOCTOR** (prop: the bandage bag)
1 Roshan: "Doctor Roshan! Tonight we make the poorly animal all better!"
2 Imp: "Teehee! Ouchie! I have a tiny scrape — see?"
3 Ward helper (Harper): "Such gentle hands! Your patient feels braver already!"
4 Roshan: "That's the bandage bag! The poorly animal needs it to feel better!"
5 Maestro: "The crowd is quiet as bubbles — show them how gently a doctor wraps."
6 Roshan: "Come here, little imp — a bandage for your scrape too!" (the beat-2 scrape pays off; strongest inclusion beat in the house)
7 (reuse verbatim): "The cast is on and the wiggle is back — best vet in the whole sea!" + Hooray.

**6. FARMER** (prop: the veggie basket)
1 Roshan: "Farmer Roshan! Tonight we grow yummy veggies for the piggy picnic!"
2 Imp: "Teehee! Piggies! We want to pat the piggies!"
3 Farmer friend (Wacky): "Ho ho, fine planting! The piggies are doing happy hops!"
4 Roshan: "That basket is the piggies' dinner — their tummies are rumbling!"
5 Maestro: "Sunset curtain! Show everyone how a farmer brings the piggies home!"
6 Roshan: "Imps, you can each pat a piggy — gentle and slow."
7 (reuse verbatim): "Twelve happy piggies with full tummies! Best picnic the farm has ever had!" + Hooray.

**7. BOXER** (prop: the championship belt)
1 Roshan: "Boxer Roshan, into the ring! Tonight we train for the big bout!" (reuses opener)
2 Imp: "Teehee! Bouncy ropes! We want to boing!"
3 Ring crew (Shop): "Great bopping! These gloves make your bops extra bouncy!"
4 Roshan: "The sparkly belt is for the winner's bow — the crowd wants to see it shine!"
5 Maestro: "Ding ding! Show the crowd your fastest bops and your best duck!"
6 Roshan: "Come bow in the ring, bouncy imps — everybody boings the ropes!"
7 (reuse verbatim): "And the winner is... ROSHAN! The sparkly championship belt is hers!" + Hooray.

**8. MAGICIAN** (prop: the magic hat — the bunny-fish's home)
1 Roshan: "Abracadabra! Tonight we do magic tricks for the whole opera!" (reuses "Abracadabra!")
2 Imp: "Teehee! Magic! Make MEEE disappear!"
3 Usher crab (Wacky): "Click click! Marvellous trick! Our scarves will hold the rope for you!"
4 Roshan: "The bunny-fish lives in that hat — it's his cosy home!"
5 Maestro: "Lights up! Show everybody the greatest trick in the sea!"
6 Roshan: "Ta-da! For my last trick — appearing IMPS! Take a bow!"
7 (reuse verbatim): "Magic! The bunny-fish says you have the sharpest eyes in the sea!" + Hooray.

**9. PAINTER** (prop: the sunrise painting)
1 Roshan: "Painter Roshan! Tonight we paint a big sunrise for the gallery!"
2 Imp: "Teehee! Squishy paint! We want to make splats!"
3 Painter friend (Huluu): "What lovely colours! Take my paints — red and gold and pink!"
4 Roshan: "That painting is for the gallery wall — everyone is coming to see it!"
5 Maestro: "Unveil it! Show the crowd your beautiful sunrise!"
6 Roshan: "Imps, dip a finger — everybody adds one sparkle splat!"
7 (reuse verbatim): "Your painting is hanging in the gallery for the whole opera to see!" + Hooray.

**10. ASTRONAUT** (prop: the golden launch valve)
1 Roshan: "Astronaut Roshan! Tonight we build the bubble rocket and fly to the stars!"
2 Imp: "Teehee! Shiny wheel! We want to see it spin!"
3 Bubble engineer (Shop): "Super pipe-fitting! Here's a spare pipe from the workshop!"
4 Roshan: "That's the launch valve — the rocket can't twinkle-off without it!"
5 Maestro: "Countdown time! Show everybody how a rocket flies!"
6 Roshan: "Imps, help me count — three... two... one!"
7 (reuse verbatim): "The bubbles reached the rocket! Three, two, one — TWINKLE-OFF!" + Hooray. (The count lands twice on purpose — beat 6 makes the imps do the ritual, beat 7 pays it off.)

**11. RACER** (prop: the checkered flag)
1 Roshan: "Racecar Roshan! Tonight we drive the Opera Grand Prix — vroom vroom!"
2 Imp: "Teehee! Fast wheels! We want a ride!"
3 Pit crew (Shop): "Speedy pit stop! Fresh wheel on — you're ready to zoom!"
4 Roshan: "That's the waving flag — it tells everyone the race is starting!"
5 Maestro: "Green light! Show the crowd your fastest, zoomiest lap!"
6 Roshan: "Hop in, imps — everyone gets a victory lap!"
7 (reuse verbatim): "What a race! The whole audience is waving checkered flags!" + Hooray.

**12. POPSTAR** (prop: the sparkly microphone)
1 Roshan: "Pop Star Roshan! Tonight we sing the big song for everyone!" (reuses opener)
2 Imp: "Teehee! La la la! We want to sing too!"
3 Band friend (Harper): "You've got the beat! Our instruments will play along with you!"
4 Roshan: "That microphone carries my song all the way to the back row!"
5 Maestro: "Spotlight on! Sing it out — the whole crowd wants to dance!"
6 Roshan: "Imps on backup! La la la — everybody sings the encore!"
7 (reuse verbatim): "The crowd is singing along! Pop Star Roshan, the reef's biggest star!" + Hooray.

**13. NURSERY — co-op with Nurse Faron** (prop: the lullaby music box; finale is WITH the partner, not vs a rival — and the whole act runs at whisper dynamics, which makes it the most distinctive-sounding act in the house)
1 Roshan: "Nurse Roshan reporting! Tonight we tuck the baby otters in for sleepy time!"
2 Imp (small, yawny): "Teehee... shh... nobody ever tucks US in..."
3 Faron (af_nicole, hushed — exactly her manifest register): "Gentle rocking, little nurse... the babies love your soft hands."
4 Roshan (whisper): "The music box plays the lullaby — the babies can't sleep without it!"
5 Faron: "Everyone is watching so quietly... let's sing the lullaby together."
6 Faron: "Sleepy imps... there's a blanket for each of you. Snuggle in."
7 Roshan (whisper): "Every baby is dreaming... best nurses in the whole sea." + a whispered group "hooray" (record a hush variant — the loud Hooray would wreck the act's whole dynamic arc).

## RULES

**Line length (Kokoro TTS, 4-year-old ear):**
- 5–12 words per sentence, max 2 sentences per beat, 3–6 seconds of audio. A 4yo holds the first and last content words — put the key noun or verb there.
- One idea per line. The shipped chef arrival (six steps in one breath) is the anti-pattern: split multi-step instructions across station beats, which the `_say()`-per-beat rule already mandates.
- Numbers as words; em-dashes for natural Kokoro pauses; exclamation marks lift the pitch contour but cap at one exclamatory sentence per beat or everything sounds shouted.
- No lip sync exists, so voice identity IS speaker identity: every slot keeps its fixed voice+pitch, and the Imp Captain needs his own new squeaky slot (distinct from Sparkle's 1.55 chirp) so "who's talking" is audible without reading.

**Repetition:**
- Ritual lines repeat EVERY act, verbatim, on purpose: "It's showtime!", "Follow the golden sparkle!", "Teehee!", the Hooray. Ritual is comfort and it teaches structure to a non-reader.
- Instruction lines re-fire after 8–10s of no input, at most twice, drawn from a 2–3 variant pool (the existing idle1..3 pattern) so the second hearing isn't identical. After two, drop to visual pointer only.
- Emotional lines (beats 2, 4, 6, 7) play ONCE per act, never auto-repeated. A repeated stakes line turns warmth into nagging; a repeated pride line devalues the pride.
- Across careers, beats share a TEMPLATE but never a full sentence — the concrete nouns (cake/tiara/piggies) are what make each act feel like its own show.

**When silence is better:**
- While her finger is mid-gesture (stirring, tracing, twirling) — never talk over the doing; queue lines to gesture end.
- During spectacle waits (oven rising, countdown glow, curtain lifting) — music and SFX carry these; a voice line here steals the wonder.
- After two unanswered prompts — a third is pressure. The pointer waits silently.
- One full beat of air after the theft gasp and after the pride button. The gasp needs room to become a giggle; the applause needs room to land. The nursery act is the proof case: its silences are the content.

**The 3 traps:**
1. **Moralizing.** Never "stealing is wrong," never "you should share," never a lesson spoken aloud. The fix is ENACTED — the hungry imps get cake at the bow — and a 4yo reads enacted generosity perfectly. The moment a character narrates the moral, it's a lecture, and lectures are skipped. (Bluey never says the lesson; Bingo just does the brave thing.)
2. **Threat language.** No "hurry!", no "before it's too late!", no "he'll ruin the show!" There are no fail states, so the words must not invent stakes the mechanics don't have. Beat 4 states what the prop is FOR, never what could be LOST — purpose reads as warm, loss reads as fear. Every "Oh no!" must resolve into a giggle inside the same breath.
3. **Unexplained competition.** An opponent who opposes for no spoken reason is genuinely scary at 4. Beat 2 exists precisely to install the captain's relatable want BEFORE the theft, beat 5 reframes the finale as performing FOR the crowd (the rival imp does the job badly-but-adorably beside her), and beat 6 grants the beat-2 want on stage. Want → take → share is a toddler's own social loop, told back to her with a happy ending.

**Recommended new audio work (for the eventual implementer, not this task):** one new Imp Captain voice slot; a whispered "hooray" variant; a Maestro host slot; ~5 new short lines per act (beats 2, 3, 5, 6 + one trimmed arrival) — beats 1 and 7 largely reuse shipped `voice`/`win_line` text. All fit the existing `<speaker>_<event>.ogg` auto-pickup in `tools/make_voices.py`. The three boss acts (Curtain Dragon, Shadow Phantom, Midnight Maestro) already speak this spine's beats 2/6 and need no rewriting.
# Rumi under-pool book — critical analysis against traditional comics

**Prepared by:** Claude, 2026-10-17, at the owner's request (see the
[README](README.md#owner-request-2026-10-17)). Written analysis only; no image
was made or edited.
**Subject:** the commissioned 32-page under-pool book, latest edition
*Mermaid Roshan: Here I Am!* (visual/detective edition of 2026-10-12).
**Where the book lives:** only on `rescue/peter-20261015-arborist-start` at
commit `c3e0da5107b9f3d18be4a07ffa3183196ddeb574`, under
`assets_src/books/`. It is not on `dev`. Paths below are relative to that
commit; hashes are SHA-256 of the git blob bytes.
**Status:** `SUPPORTING_CURRENT` evidence for the revision handoff. It judges a
static draft and grants no story, art, child or owner acceptance.

## 1. What exists

The book was rewritten six times in four days. Each edition answered the
previous owner note, so the lineage explains the current weaknesses.

| Edition (source folder at `c3e0da51`) | Owner note it answered | Story pages | Panels | Words | Silent panels | Longest run of pages with the same panel count | Page turns ending open (text proxy) |
|---|---|---:|---:|---:|---:|---:|---:|
| `rumi_underpool_20261010` first 32-page comic | "refine to 32 pages, more comic content" | 30 | 87 | 1,322 | 0 | 16 | 1 of 15 |
| `rumi_underpool_iteration_20261010` | bathhouse and interrupted couch downtime | 30 | 88 | 1,357 | 0 | 18 | 1 of 15 |
| `rumi_manga_feast_20261011` | "much larger and more extravagant" table; "more like manga" | 30 | 127 | 1,357 | 18 | 4 | 1 of 15 |
| `rumi_action_story_20261011` (script proof, no art) | "plot far, far too thin ... 1-2 detailed action sequences" | 30 | 128 | 1,535 | 0 | 7 | 0 of 15 |
| `rumi_voice_book_20261011` *Here I Am!* | "letting your voice be heard"; "all pictures must be unique" | 31 | 93 | 991 | 0 | 31 | 1 of 15 |
| `rumi_visual_detective_20261012` (latest) | 4.7/5 visuals; "rainbow candle should be hidden"; detective-hat montage | 31 | 101 | 1,050 | 0 | 28 | 1 of 15 |

Measured with [`tools/measure_book_pacing.py`](tools/measure_book_pacing.py)
(`--spreads`); full output, per-page rows and source hashes are in
[`data/current_book_metrics.json`](data/current_book_metrics.json). The first
illustrated draft (`rumi_underpool_20261009`, 15 spreads, 576 words) is prose,
not panels, and is not measured.

The latest edition in one paragraph: Roshan wants to sing the first line at
the under-pool Song Night. She tests a rainbow glint with her detective hat and
magnifier (it is reflected light) and stows both tools. In the town her friends
Rumi, Hana and Nari talk over her; the imps' giant fan traps Duri the turtle
courier; Roshan shouts Stop and the friends free him. In the bathhouse the
trio apologise; at the couch feast Roshan starts her line and the imps
interrupt. At the stage a bubble trick traps the magician; Roshan stops the
show, the friends catch and pop the bubble, the imps apologise and Roshan sings
"Here I am!". At home she asks to share an idea about the missing candle.

Its agent rubric scored 4.735/5 for drawing quality (character, line, contact,
lettering, composition). That rubric does not measure plot, pacing, world or
page turns, which is what the owner is now asking about.

## 2. How traditional comics carry a story of this length

Six benchmarks, chosen because each solves a problem this book has. Sources
are listed in section 6.

| Benchmark | What it shows | Craft principle to borrow |
|---|---|---|
| **TOON Books** levelled comics for early readers (Françoise Mouly's imprint) | Level 1 (K–1): 1–2 panels a page, about 200–300 words. Level 2: 1–4 panels, 300–600 words. Level 3: 800–1,000 words with a broad story world, chapters, and shifts in time and place. | Length must be matched by world and structure. A 1,000-word comic for young children is expected to carry chapters and a changing setting, not one conversation repeated. |
| **Carl Barks, "The Secret of Atlantis"** (Uncle Scrooge #5, 1954) — exactly 32 pages | A comic scheme, a lost object, a dive to the sea floor, and a sunken society with its own logic and an inhabitant who explains how it works, then a twist. | Thirty-two pages hold an *adventure plus a society*. The undersea place has rules, residents and a reason to exist, and the plot moves through it. |
| **Hergé, *The Adventures of Tintin*** | Pages built from four strips; panel widths change with the content. Small uniform panels read fast, a larger panel slows the reader. Pages end on a hook that pulls the turn; splash pages are rare. | Rhythm comes from *varying* panel size inside a stable grid, and from deliberately placed page-end hooks. |
| **Manga pacing (Scott McCloud, *Understanding Comics*)** | Western comics lean on action-to-action transitions. Japanese comics use aspect-to-aspect transitions — several views of one moment or place — to set mood, a type McCloud calls rare in the West. | "More like manga" is a pacing tool, not only a frame style: quiet place-setting sequences, silent panels, big reaction close-ups, and stretched emotional beats. |
| **Page-turn craft (contemporary graphic-novel practice)** | Readers take in a whole spread before reading its panels, so a reveal placed on the same spread is spoiled. Put the suspense bottom-right, the reveal in the first panel of the next left page. | Plan by spread, not by page. In a book whose page 1 is a lone right-hand page, every turn happens after an odd page. |
| **Richard Scarry's Goldbug** (*Cars and Trucks and Things That Go*) | A tiny recurring character hidden on (nearly) every spread; small side-stories fill the backgrounds. | A non-reading four-year-old needs something to *find* on every page and a reason to reread. Backgrounds should hold tiny stories, not undifferentiated sparkle. |

## 3. The book against those benchmarks

| Benchmark principle | This book (latest edition) | Verdict |
|---|---|---|
| Length matched by world, chapters, time and place (TOON Level 3) | 1,050 words is Level 3 length; the story has one want, no chapters, and 12 of 31 story pages (20–31) on the same stage; "tonight" never becomes night | **Fails** — Level 3 length with a Level 1 plot |
| A society with rules (Barks) | The town is never explained: who lives there, why it is under the pool, what Song Night is for, what happens if nobody answers | **Fails** |
| Varied rhythm inside a grid (Hergé) | Pages 5–32 all have exactly three panels: a run of 28 pages. No splash page, no double-page spread, no inset | **Fails** |
| Page-end hooks (Hergé; page-turn craft) | 1 of 15 turns ends open by text (page 17, "Here I..."); by eye, page 25 (magician trapped while his friend bows) also lands. 2 of 15 | **Fails** |
| Aspect-to-aspect place-setting and silent panels (manga) | 0 of 101 panels is silent; every panel carries text. No mood sequence in the bathhouse or on arrival | **Fails** — manga framing without manga pacing |
| Something to find on every spread (Goldbug) | Backgrounds are dense but generic: bubbles, pearls, columns, lanterns at one value. No recurring hidden character or side-story | **Fails** |
| Clear speaker and reading order | Balloons are tidy and correctly ordered; the rubric recorded only small limits (pages 3, 8, 16, 21, 27) | **Passes** |
| Consistent character identity | Rumi, Hana, Nari and Duri hold their designs across 32 pages | **Passes** (see W-V8 for Roshan) |

## 4. Critical weaknesses, ranked

Each weakness names its evidence and the section of the revision that answers
it. Page numbers are the latest edition's.

### Plot

| ID | Weakness | Evidence | Answered by |
|---|---|---|---|
| W-P1 | **One small want, resolved by permission.** "I want to sing the first line" is the only engine. The obstacles are people talking over Roshan, so every solution is someone agreeing to listen. | Want stated p2; granted p29 ("All right. We're listening.") | [STORY_REVISION §2](STORY_REVISION.md#2-the-new-spine): a community stake (the town's answer-song has gone silent) carries the personal want |
| W-P2 | **The same beat four times.** Unheard → speak up → apology repeats with friends (p5–7, p14), Duri and the imps (p4, p13), the imps and Roshan (p18–19), and the magician (p25–28). Stakes plateau after the rescue on p12. | Pages listed | [STORY_REVISION §3](STORY_REVISION.md#3-structure-five-chapters-on-fifteen-page-turns): each chapter escalates a different threat |
| W-P3 | **The detective montage is a dead end.** Hat and lens are fetched (p2–3), the glint is proven to be reflected light, both tools are stowed before the dive (p3) and never used again. The last page mentions an "idea about our candle" with nothing planted in between. | p2, p3, p32 | [STORY_REVISION §5](STORY_REVISION.md#5-page-by-page-manuscript): the montage finds the hidden door, and the detective method (look, ask a witness, test, follow the clue) solves the book's mystery |
| W-P4 | **No mystery, clock or opposing plan.** Song Night has no visible deadline; the imps have no plan, only manners; their change of heart arrives through a speech. | p18–19, p28 | The silent answer-song is a mystery with fair clues; dark lanterns are the visible clock; the imps' Boom Shell is a plan with a cause |
| W-P5 | **Midpoint sag.** Pages 13–17 are five consecutive seated conversations (15 panels) whose only new information is apologies and a towel preference. | p13–17 | The bathhouse becomes the investigation's centre: a clue, a test, a lesson and the reversal ([WORLD_BIBLE §5](WORLD_BIBLE.md#5-the-bubble-bathhouse)) |
| W-P6 | **Roshan directs the climax; others perform it.** At p27 Hana and Nari hold the cloth, the performer ties the curtain and Rumi pops the bubble. A four-year-old identifies with the hero's hands, and the game needs the child's touch to resolve the climax. | p27 | Roshan swims into the shell and her own whistle ends the danger (pages 25–27 of the revision) |
| W-P7 | **The lesson is spoken, not shown.** Social-emotional vocabulary replaces character voice and jokes: "I am speaking. Please listen. This is everyone's song. My friends have something to sing. And I do too." (p19, one 19-word balloon); "We hear you. We're here. We won't leave you." (p26); the page title "Room means doing something" (p29). | p19, p26, p29 | [STORY_REVISION §7](STORY_REVISION.md#7-dialogue-rules): one idea per balloon, humour, and a visual voice motif (whisper balloon grows into a full balloon) |
| W-P8 | **Short-range setups.** The fan (p4) pays off by p8; the last invitation (p4) is delivered on p21 with no consequence. Nothing planted in Act I pays off in Act III except the wish. | p4, p8, p21 | Five long setups pay off late (pinky promise, calm eye, whistle, nameless lantern, glint door) |
| W-P9 | **The world is entered, not discovered.** Rumi simply takes Roshan below; the threshold between castle and town is never staged. | p3→p4 | The glint is light rising from the hidden town; Roshan's investigation opens the door (pages 2–5) |

### Visual

| ID | Weakness | Evidence | Answered by |
|---|---|---|---|
| W-V1 | **Monotone grid.** 28 consecutive pages of exactly three panels; 0 splash pages, 0 spreads, 0 insets, 0 silent panels. Panels per page: median 3, mean 3.26, standard deviation 0.8. | Meter output | Page plan with 1–7 panels a page, no run longer than four pages, two double-page spreads, 18 large panels and 21 silent panels ([`data/page_plan.json`](data/page_plan.json)) |
| W-V2 | **Chorus-line staging.** Most pages line the cast up facing the camera in medium shot (for example p5, p7, p9, p13–17, p19, p22, p30–31). Few establishing shots, few emotional close-ups, almost no high or low angles. | Page review | Shot vocabulary per chapter in [STORY_REVISION §6](STORY_REVISION.md#6-art-direction-for-the-pages) |
| W-V3 | **No value hierarchy.** Every panel is filled edge to edge with saturated bubbles, pearls, coral and lanterns at one value, so the action competes with the backdrop (`DL-READ-01`, `DL-READ-03`, `DL-VIS-03`, `DL-VIS-04`). | Page review | Quiet backgrounds behind dialogue; detail clusters reserved for establishing panels and seek-and-find |
| W-V4 | **No colour script.** The story happens "tonight" but every page is daylight aqua and pink; the lanterns never go up and night never falls. | Page review | Sunset → blue dusk → night → dark-out → lantern gold ([WORLD_BIBLE §8](WORLD_BIBLE.md#8-colour-script-and-time)) |
| W-V5 | **The bathhouse is a pool with tea.** Same columns and lamps as the plaza; the cast sit in water wearing full performance jackets; tea and kelp rolls poolside; no rooms, rituals, attendants, robes or steam. Only Nari's rabbit towel says "bathhouse". | p14–16 | A complete bathhouse with five rooms, a keeper and rituals ([WORLD_BIBLE §5](WORLD_BIBLE.md#5-the-bubble-bathhouse)) |
| W-V6 | **One backdrop for a third of the book.** The shell stage fills pages 20–31; the market lane appears in about two panels; crowds are faceless silhouettes or generic mermaids; sea creatures are almost absent. | Page review | Seven districts, a sea-creature citizenry, named crowd vignettes |
| W-V7 | **Undecided physics.** Water surfaces and pools inside an underwater town (p14–16; the canal in the owner-liked city concept), hot tea in cups, imps walking in shoes. | p14–17, p20 | One medium rule: everything is underwater ([WORLD_BIBLE §2](WORLD_BIBLE.md#2-world-rules)) |
| W-V8 | **Roshan's look.** She wears her Pop Star career costume on every page and never her tiara. Owner decisions on dev: new art follows the base-world child, and she wears the tiara whenever she is outside a career costume (`ODR-ROSHAN-Q13`, `ODR-ROSHAN-Q14`). Her waist ribbons must stay readable as fabric (`MA-ROSHAN-005`). | Every page; `assets/characters/roshan_25d/roshan_base.png` | Costume progression: base look → bathhouse robe → Pop Star outfit for the show, which also marks the act change |
| W-V9 | **Low kinetic energy in the action.** The rescue is hands on a fan (p8–12); the stage sequence is mostly holding a cloth (p22–27). Contact is clear, but there are few motion lines, impact panels or dynamic angles. | p8–12, p22–27 | Choreographed set pieces with geography, a rule and an escalation ([STORY_REVISION §4](STORY_REVISION.md#4-the-two-action-set-pieces)) |

### World and inspirations

| ID | Weakness | Evidence | Answered by |
|---|---|---|---|
| W-W1 | **Narrow inspirations used as decoration.** The sources are one film's tropes (a performing trio, rival boy-band-like imps, a bathhouse fight, couch snacks), East Asian roof silhouettes, kelp rolls, Greek columns and a monorail. None of them supplies a rule, a custom or a resident. | Cover, p4, p14–17 | A widened reference palette with borrow/avoid lines ([WORLD_BIBLE §10](WORLD_BIBLE.md#10-reference-palette-borrow-and-avoid)) |
| W-W2 | **No rules or reason.** The first draft's best line — "Usually, the city sang back. Tonight, no answer came." — was dropped in later rewrites, and with it the town's purpose. | `rumi_underpool_20261009/MANUSCRIPT.txt` | Lantern Night and the answer-song become the town's central custom |
| W-W3 | **No map.** Districts are not connected; scale is unclear; only page 32's round opening links town and castle. | p4, p32 | A district map with routes the story and the game both use ([WORLD_BIBLE §3](WORLD_BIBLE.md#3-geography-of-pearl-hollow)) |

### Game integration

| ID | Weakness | Evidence | Answered by |
|---|---|---|---|
| W-G1 | **The story never uses the game's verbs.** The game's core verb is cleaning (Day One), plus drag, collect, hold, echo, dress-up and lane swimming. The book contains no cleaning at all. | Book versus [GAME_INTEGRATION §2](GAME_INTEGRATION.md#2-what-the-game-already-has) | Every chapter is built on an existing verb |
| W-G2 | **No way in.** The book never establishes a door the child could use in the Mermaid Pool room. | p2–4 | The glint door under the pool-room bench |
| W-G3 | **No voices for new characters.** Hana, Nari and Duri have no recordings; Rumi's three lines are provisional synthetic filler, and the birthday chapter's scope says "no invented Rumi voice". Every objective needs an exact spoken cue (`DL-SND-01`). | `assets/audio/voices/filler_v1/rumi_*.ogg`; `design/10_CHAPTER_REFERENCE_LIBRARY.md` | Voice plan and owner question Q5 |
| W-G4 | **Book rendering does not match the game.** The pages are glossy anime with sparkle at full saturation; the game's environments are a pastel toy playset with broad value bands and calm detail clusters (`DL-VIS-01`, `DL-VIS-03`). Book environments cannot become game backdrops without a style decision. | Pages versus `assets/flats/castle/rooms/` | Owner question Q4 |
| W-G5 | **The book is stranded.** All editions live on rescue branches; the latest edition's own full regression was recorded as FAIL (three throne-room assertions), so it never integrated, and its chapter document is not on `dev`. | `rumi_visual_detective_20261012/README.txt` | Work package RB0 |

## 5. What to keep

- **The cast.** Rumi, Hana, Nari and Duri are appealing and stay on model;
  faces are expressive; lettering order is reliable.
- **The refrain.** "Here I am!" / "Here you are!" is simple, singable
  call-and-response, and it is the book's heart.
- **The owner-commissioned set pieces.** Bathhouse, extravagant feast, couch
  downtime, two action sequences and the detective montage are all right; they
  need development and causal jobs, not removal.
- **Moments that already work:** the BOOM that swallows Roshan's sentence
  (p6), the tram pulse (p11), the bubble cascade (p20), the magician trapped
  while his partner keeps bowing (p25 — real comic irony), the POP catch (p27)
  and the call-and-response (p30).
- **Seeds worth growing:** Duri's wish for a turn of his own (p4), the imps'
  fear of being forgotten (p19), and the first draft's "Tap. Tap. Tap." and
  silent answer-song.

## 6. Sources

Comics craft:
[TOON Books catalogue](https://www.toon-books.com/complete-catalog.html) and
[overview](https://en.wikipedia.org/wiki/Toon_Books);
[The Secret of Atlantis](https://en.wikipedia.org/wiki/The_Secret_of_Atlantis);
[Hergé page structure review](https://madinkbeard.com/archives/adventures-of-tintin-review);
[McCloud's transitions](https://www.comicscube.com/2010/12/comic-book-glossary-transitions-part-2.html)
and [summary](https://design.tutsplus.com/es/tutorials/die-mechanik-der-comics--vector-1463);
[page turns and suspense](https://woodmanmaynard.substack.com/p/page-turns-crafting-suspense-in-comics)
and [the art of the page turn](https://sktchd.com/longform/the-art-of-the-page-turn/);
[Goldbug](https://www.weareteachers.com/richard-scarry-books/).

World references are cited in [WORLD_BIBLE §10](WORLD_BIBLE.md#10-reference-palette-borrow-and-avoid).

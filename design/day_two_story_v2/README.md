# Day Two story draft v2 — *Mermaid Roshan and the Rainbow Candle*

Status: `CANDIDATE` story-and-production draft, 2026-09-30, written from the
owner's direction of the same day. It is the next draft of the story that
makes Day Two (Chapter 2). Nothing in it is implemented or accepted yet, and
it does not change any binding document until the owner approves it (see
[owner decisions](#owner-decisions)).

## Read in this order

| File | What it is | Main reader |
|---|---|---|
| [00 Plotline](00_DAY_TWO_PLOTLINE.md) | **Start here.** The whole of Day Two, scene by scene: every room's story, the cast, the challenge decks mixing in Daddy, the dust bunnies, Grand Puff and Baby Eagle, Lamma from her first peek to the star of the stuffies' show, the party-preparation script (what each job gives the party and where that is on record, with a script card for each job), the eight jobs with their practice and real levels, the party with the battle of the bands, the Ember King and the Prince, the evening, and the map from the built levels to each scene | Everyone |
| [01 Story bible](01_STORY_BIBLE.md) | Canon from Book One, the Day Two premise and themes, the shape of the day, the practise-then-for-real routine, the cast, Lamma's arc, the rules for mixing Day One friends into challenges, what Day Two keeps from the August party-function script, and the job canon on record (section 12) | Owner, writers |
| [02 Book Two manuscript](02_PICTURE_BOOK_MANUSCRIPT.md) | The 32-page picture-book text in Book One's style; every page names the game beat it anchors | Owner, book team |
| [03 Level mechanics](03_LEVEL_DESIGN.md) | The plotline's build sheet: every step's gesture mode, object and save, and every new voice line, generated from the plotline | Designers, Astra |
| [04 Party chapter](04_FINALE_PARTY_CHAPTER.md) | The finale with the Ember King and the Prince, beat by beat | Owner, designers, animators |
| [05 Build audit](05_BUILD_AUDIT.md) | What is built today, in detail, and where the story and theme are thin | Owner, Astra |
| [06 Graphics audit](06_GRAPHICS_AUDIT.md) | Asset-by-asset graphic flaws in the Day Two stage, each with a written fix | Art, Astra |
| [07 Work packages](07_WORK_PACKAGES.md) | The whole draft broken into ID'd, self-contained packages with inputs, outputs, dependencies and acceptance | Astra |

## How the pieces connect

```text
Story bible (01) ── canon and rules ──►  PLOTLINE (00): the whole day, scene by scene
                                              │            │
              Book Two manuscript (02) ◄──────┘            ├──► Mechanics and voice lines (03)
              prints the first-play story                  └──► Party chapter production (04)
                                                                         │
              Build audit (05) + Graphics audit (06) ── what exists, what is wrong
                                                                         ▼
                                             Work packages (07) ──► Astra breaks down and builds
```

Stable IDs are used across all files:

- **P-1, P-2:** Lamma's two peeks in Episode One (Day One).
- **D2-OPEN-1…3:** the opening.
- **J1–J8:** the eight jobs in play order (J1 Astronaut, J2 Arborist, J3
  Farmer, J4 Chef, J5 Painter, J6 Ballerina, J7 Pop Star, J8 Detective), each
  with **-L1** (Opera practice) and **-L2**
  (in-world level); **Jn-DECK-xx:** each job's challenge cards; **R1–R8:**
  the Party Plan beat after each job; **Jn-FN:** each job's function line
  (what the party has now, and who it is for).
- **LAMMA-1…3, LAMMA-JOIN:** Lamma's moments.
- **F1–F8:** the finale; **BAND-01–14:** the battle of the bands' scenes, as
  numbered in the bands commission.
- **E1–E3:** the birthday evening.
- **ROOM-*:** each place's story.
- **GFX-*:** graphics fixes.
- **WP-*:** work packages.

## Relationship to existing documents

| Document | Status | What this draft does to it |
|---|---|---|
| `design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md` | Binding | Proposes changes: Arborist replaces Candy Maker; the Astronaut sends the invitations (the August ruling the owner restated on 2026-09-30) instead of building the candle-lighting rocket, and moves first; the Pop Star's job becomes the family band; the Ballerina waits for Lamma; the practise-then-for-real routine replaces "no tutorial prelude"; Chef gains the strawberry-topping step. The spine stays binding until the owner approves |
| `design/CHAPTER2_CAKE_VISUAL_PROGRESSION_2026-08-31.md` | Binding | Proposes Chef owning cake bits 5 and 6 |
| `design/CHAPTER2_LAWN_FINALE_DRAFT_2026-09-06.md` | Candidate | Revised in detail by [04](04_FINALE_PARTY_CHAPTER.md). On branch `codex/battle-of-bands-20260920` its "September 20 contest revision" records the owner's choice of a battle of the bands, which [04](04_FINALE_PARTY_CHAPTER.md) follows |
| `design/BATTLE_OF_BANDS_2026-09-20.md` and its review packet (branch `codex/battle-of-bands-20260920`, not on `dev`) | Candidate | The finale's contest (F5) and the Pop Star job follow it. On `dev` it is the open question `OQ-BANDS-VS-LAWN` (decision 15) |
| `design/ARBORIST_TREE_DOCTOR_HANDOFF_2026-09-30.md` | Candidate | Folded in as job J2 where it agrees with the owner's corrections of 2026-09-29 (`design/ARBORIST_TREE_BOOK_HANDOFF_2026-09-29.md` on `dev`), which supersede its conflicting defaults: the leaf-based three-decision loop, no broken-branch page, and no Candy Maker in the Kitchen |
| `design/OPERA_TREE_BOOK_TEST_2026-09-30.md` (on `dev`) | Supporting | J2's practice |
| `BALLERINA_PARTY_REBUILD_2026-08-09.md` | Binding (domain) | J6's three acts, "a recital, not a race" |
| `CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md`, sections 11-20 | Mixed authority | Its owner rulings and reconciled party-role map (section 15) are the source of the party-preparation script, including the Astronaut's invitations (section 14); the parts since superseded (the Imp Captain's invitation, the stage bosses) are not used ([01, sections 11 and 12](01_STORY_BIBLE.md#12-the-job-canon-on-record)) |
| `CHAPTER2_PARTY_ROLES_2026-08-03.md`, `CHAPTER2_BIBLE_ACT_SCRIPTS_2026-08-03.md` | Proposal deferred, historical | Parts adopted for Day Two as a candidate: the function-over-object rule, function lines, named guests where they fit, and "one more". They stay deferred until the owner approves (decision 12) |
| `docs/handoffs/codex_opera_imp_contest_2026-09-30/` and the design language's new Opera-contest rule (both on `dev`) | Candidate; binding target | Day Two has no imps: its rule C13 gives Chapter 2 story and tutorial runs no imp and no contest |
| `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` (`DL-INT-12`, `DL-INT-07`) | Binding | Unchanged unless the owner wants practices launched from the Opera Hall, or the Arborist added to freeplay |

## Owner decisions

Each item has a recommended default; nothing dependent is built before the
owner answers.

1. **Job order.** Recommended: the Astronaut first, sending the invitations
   ("It is the chapter's FIRST act": the August review, section 14), then the
   Arborist, Farmer, Chef, Painter, Ballerina (after Lamma joins), Pop Star
   and Detective (sequence `[11, 18, 6, 0, 10, 2, 13, 1]`). The alternative
   keeps the built order with the Astronaut at slot 7, so the invitations go
   out late in the day.
2. **Where Opera practices launch:** from each job's room card (recommended;
   keeps `DL-INT-12`), or all from the Opera Hall stage (needs a `DL-INT-12`
   change).
3. **Practise-then-for-real routine** replaces the spine's "no tutorial
   prelude" rule (the owner direction of 2026-09-30 already implies yes).
4. **Lamma's joining game** becomes her way to join (recommended), and her
   joining wakes the Ballerina job: the owner's 2026-09-30 direction is that
   the show has no star until Lamma. The owner's capture loop of 2026-07-20
   (`STUFFIE_COMPANIONS.md`) made Lamb-a' the first stuffie a battle can
   capture, but its `boss_lamma` round uses the retired `lamb.glb` body and
   has no authored entrance today, so it is not revived for her.
5. **Voices for the King and Prince:** new synthetic voices pending owner
   listening (recommended), or family recordings if the owner wishes.
6. **What the glowing door opens:** the Fairy Conservatory route already built
   for Chapter 3 (recommended, since it is implemented and gated on this
   ending), or the north, as in the Aug 3 day table. Chapter 3 must pick up
   "We'll find our light together".
7. **A name for the Prince** (canon currently has none).
8. **The Arborist's freeplay home.** The Candy Maker is no longer a decision
   here: the owner reserved it for a later section of the game and said "Do
   not place it in the Kitchen" (2026-09-29). Open: whether the Arborist's
   freeplay home is the Opera House, where the Tree Book test level already
   launches from the foyer floor on `dev`, or the Opera Hall card the handoff
   keeps only as a routing default.
9. **Lamma's name, and whose lamb she is.** The owner and the files say
   "Lamma"; the game shows "Lamb-a'" and the Opera says "Lamba". The Seek
   game pairs her with Evie, and Evie's protected portrait shows Evie hugging
   her. Recommended: she is called Lamma everywhere; she is a shy castle
   stuffie who joins Roshan's team; at the party Evie greets her, staged with
   Evie's Seek sheet so only one Lamma is on screen
   ([GFX-LAMMA-02](06_GRAPHICS_AUDIT.md#gfx-lamma-02)). If she is Evie's
   lamb, the party becomes a reunion and "joins the team" means she plays with
   them for the day.
10. **Roshan's costumes in the castle rooms.** Recommended: the approved
    Roshan with small costume overlays per job. The alternative is
    identity-matched redraws of the eight accepted costume sheets
    ([GFX-SYS-04](06_GRAPHICS_AUDIT.md#gfx-sys-04)).
11. **Repairs to protected art.** Whether to authorise non-destructive
    re-isolations of the book dolls Kitty and Bunny from their full book
    pages, and an alpha-only mask for the white patch in the Wacky and Chuck
    portrait, all as new files with the originals untouched
    ([GFX-CHAR-DOLLS-01](06_GRAPHICS_AUDIT.md#gfx-char-dolls-01)).
12. **The party-preparation script.** Recommended: adopt the August
    party-function rule for the eight jobs, as in the plotline's
    [what each job gives the party](00_DAY_TWO_PLOTLINE.md#what-each-job-gives-the-party):
    each job's contribution as the records have it (the Astronaut's
    invitations, the Pop Star's band, the Ballerina's show starring Lamma, the
    Detective's candle; [01, section 12](01_STORY_BIBLE.md#12-the-job-canon-on-record));
    a named friend where one fits (Wacky and Chuck, Faron, the dust bunnies,
    Evie, Flower Friend); a function line in each R-beat; and "one more" as
    Lamma, the star. Needs the August papers gave to careers not in Day Two
    wait for those careers.
13. **New lines for the party guests.** Recommended: none on Day Two.
    Roshan says each function line, and existing guest clips play unaltered
    where they fit (Wacky's hello, Faron's "Shhh...", Harper's "Wheee!" after
    the show, Huluu's thank-you). The alternative is new lines for Evie, Harper, Huluu,
    Wacky and Kareem in their provisional synthetic presets. Faron's
    recordings are protected, so she would get none, and Kareem's voice route
    plays the adult "Shop" preset, which does not fit his portrait (a boy), so
    he would need his own preset first.
14. **Who lights the candle.** The Astronaut's rocket now carries the
    invitations, so it no longer makes the candle's spark, as the spine and
    the lawn alpha have it (`OQ-LAWN-ROCKET` on `dev`). No record gives the
    lighting to anyone else, and the bands commission starts with the candle
    already lit. Recommended: Daddy lights it, as a grown-up lights a birthday
    candle at any party; the child touches the candle to ask. The alternative
    keeps the built walk-and-press ignition, with the rocket back from
    delivering the invitations, which gives the Astronaut a second job.
15. **The battle of the bands: confirm it, its stage and its song.** The owner
    chose a battle of the bands to the recorded Iko Iko on 2026-09-20, and on
    2026-09-30 said "The pop star already has the iko iko material". This
    draft follows it, and asks the owner to confirm three things: that it
    replaces the lawn finale's protection rounds (answering `OQ-BANDS-VS-LAWN`
    on `dev`, whose default keeps the lawn until then); where the healed party
    tree stands in the literal middle-meadow panorama, which the commission
    keeps free of invented geography; and whether the Iko Iko composition may
    ship in the game at all. Its archive says it "is not a runtime game cue or
    approval to reuse the composition in the game", and its workflow says the
    song's rights "would need a separate decision before any reuse in the
    game". Until then the band's song is a prototype binding only.

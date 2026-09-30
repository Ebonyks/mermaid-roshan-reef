# Day Two story draft v2 — *Mermaid Roshan and the Rainbow Candle*

Status: `CANDIDATE` story-and-production draft, 2026-09-30, written from the
owner's direction of the same day. It is the next draft of the story that
makes Day Two (Chapter 2). Nothing in it is implemented or accepted yet, and
it does not change any binding document until the owner approves it (see
[owner decisions](#owner-decisions)).

## Read in this order

| File | What it is | Main reader |
|---|---|---|
| [00 Plotline](00_DAY_TWO_PLOTLINE.md) | **Start here.** The whole of Day Two, scene by scene: every room's story, the cast, the challenge decks mixing in Daddy, the dust bunnies, Grand Puff and Baby Eagle, Lamma from her first peek to the stuffie team, the eight jobs with their practice and real levels, the party with the Ember King and the Prince, the evening, and the map from the built levels to each scene | Everyone |
| [01 Story bible](01_STORY_BIBLE.md) | Canon from Book One, the Day Two premise and themes, the shape of the day, the practise-then-for-real routine, the cast, Lamma's arc, and the rules for mixing Day One friends into challenges | Owner, writers |
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
- **J1–J8:** the eight jobs, each with **-L1** (Opera practice) and **-L2**
  (in-world level); **Jn-DECK-xx:** each job's challenge cards; **R1–R8:**
  the Party Plan beat after each job.
- **LAMMA-1…3, LAMMA-JOIN:** Lamma's moments.
- **F1–F8:** the finale.
- **E1–E3:** the birthday evening.
- **ROOM-*:** each place's story.
- **GFX-*:** graphics fixes.
- **WP-*:** work packages.

## Relationship to existing documents

| Document | Status | What this draft does to it |
|---|---|---|
| `design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md` | Binding | Proposes changes: Arborist replaces Candy Maker, new job order, the practise-then-for-real routine replacing "no tutorial prelude", Chef gains the strawberry-topping step. The spine stays binding until the owner approves |
| `design/CHAPTER2_CAKE_VISUAL_PROGRESSION_2026-08-31.md` | Binding | Proposes Chef owning cake bits 5 and 6 |
| `design/CHAPTER2_LAWN_FINALE_DRAFT_2026-09-06.md` | Candidate | Revised in detail by [04](04_FINALE_PARTY_CHAPTER.md) |
| `design/ARBORIST_TREE_DOCTOR_HANDOFF_2026-09-30.md` | Candidate | Folded in as job J1; its defaults stand unless noted |
| `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md` (`DL-INT-12`, `DL-INT-07`) | Binding | Unchanged unless the owner wants practices launched from the Opera Hall, or the Arborist added to freeplay |

## Owner decisions

Each item has a recommended default; nothing dependent is built before the
owner answers.

1. **Job order:** Arborist first (recommended), or Arborist at slot 3 in the
   current order.
2. **Where Opera practices launch:** from each job's room card (recommended;
   keeps `DL-INT-12`), or all from the Opera Hall stage (needs a `DL-INT-12`
   change).
3. **Practise-then-for-real routine** replaces the spine's "no tutorial
   prelude" rule (the owner direction of 2026-09-30 already implies yes).
4. **Lamma's joining game** becomes her way to join (recommended). The old
   `boss_lamma` capture battle has no authored entrance today and belongs to
   the retired 3D era, so it is not revived for her.
5. **Voices for the King and Prince:** new synthetic voices pending owner
   listening (recommended), or family recordings if the owner wishes.
6. **What the glowing door opens:** the Fairy Conservatory route already built
   for Chapter 3 (recommended, since it is implemented and gated on this
   ending), or the north, as in the Aug 3 day table. Chapter 3 must pick up
   "We'll find our light together".
7. **A name for the Prince** (canon currently has none).
8. **Freeplay:** whether the Candy Maker stays in the Kitchen for freeplay
   (recommended), and whether the Arborist's freeplay home is the Opera Hall
   (Arborist handoff default).
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

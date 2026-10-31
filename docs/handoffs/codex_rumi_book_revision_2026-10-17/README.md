# Codex handoff — revising the Rumi under-pool book for the game (2026-10-17)

**From:** Claude (written analysis and specification; no game change, no
image made or edited). **To:** Codex (every image, board, page, PDF, code and
probe). **Owner:** answers section 5 and accepts story, art and play.

**Status:** `PROPOSED / CANDIDATE`, revision 2. Baseline: `dev`
`7a65b9f0abacddeee70230f220955f4d18d551b5`; revision 1 was merged into `dev`
at `6fb96aeb441952c1053cc5ce18435fc57fc1d1ab` after branch CI run 39114484565
passed. Book sources: rescue snapshot
`c3e0da5107b9f3d18be4a07ffa3183196ddeb574`. No finding is repaired or closed;
related findings are `MA-OPERA-002`, `MA-OPERA-014`, `MA-ROSHAN-005`,
`MA-PLAY-005`, `MA-ACCESS-001` and `MA-CHILD-001`.

**Revision 2 (2026-10-18)** follows the owner's newer decision to rebuild the
Pop Star around a music-timed call and answer (`ODR-POPSTAR-CORE-20261018`,
`MA-OPERA-014`): [GAME_INTEGRATION](GAME_INTEGRATION.md) now builds the Echo
Dome and the Lantern Night finale on that engine and takes the quiet hold from
the shared hold gesture. The story, world and analysis are unchanged. This packet requests no generation and binds
no image: `ARCHIVE_COMPLETE` only after remote verification,
`GENERATION_READY` not applicable, `DELIVERY_ACCEPTED` false.

## Owner request (2026-10-17)

> Analyze the rumi book where the three mermaids meet the turtle and prepare a
> pop show. it is on repo, as a rough draft of next book. It needs significant
> plot revisions, and developments to be able to integrate smoothly into the
> game environment. Analyze best options and methods of doing so, identify
> weaknesses in the story (both visual and plot), and devise improvements.
> Focus on producing rich, robust undersea world, the inspirations are clearly
> in the comics, but they appear narrow, and a bathhouse scene is not truly
> developed. Also, not nearly enough plotting to hold together such a long
> book. Analyze traditional comic books for pacing and style, match against
> this model, identify critical weaknesses, and draft solutions in the form of
> a codex handoff

| Read | For |
|---|---|
| [ANALYSIS.md](ANALYSIS.md) | Six comics benchmarks, the book measured against them, and 26 ranked weaknesses (plot, visual, world, game) |
| [WORLD_BIBLE.md](WORLD_BIBLE.md) | Pearl Hollow: rules, map, citizens, a fully developed bathhouse, Lantern Night, the show, colour script, sound, a widened reference palette, continuity |
| [STORY_REVISION.md](STORY_REVISION.md) | **The proposed story:** spine, five chapters on fifteen page turns, both action set pieces, the complete 32-page manuscript, art direction, dialogue rules, targets, setups and payoffs |
| [GAME_INTEGRATION.md](GAME_INTEGRATION.md) | Options and the recommended method, existing systems to reuse, the chapter-to-activity map, navigation and save, asset shortlist, voices, risks, draft brief values |
| [data/page_plan.json](data/page_plan.json) | The manuscript as data (panels with size, silence, location, plot thread, page-turn role and game activity), ready to become `story_script.json` |
| [data/current_book_metrics.json](data/current_book_metrics.json) | Measured pacing of all six editions, with source hashes |
| [tools/measure_book_pacing.py](tools/measure_book_pacing.py) | Numbers-only pacing meter for any edition's script |
| [MANIFEST.json](MANIFEST.json) | SHA-256 of every packet file |

## 1. In short

The book's drawings are polished (its own rubric scored 4.735/5), but the
story cannot carry 32 pages: one small wish granted by permission, the same
unheard-then-apology beat four times, a detective montage that leads nowhere,
28 consecutive three-panel pages, no silent panels, one or two real page-turn
hooks out of fifteen, a town with no rules or residents, and a bathhouse that
is a pool with tea. It also never uses the game's verbs.

The revision keeps every owner-requested element and gives each a job. On
Lantern Night every answer wakes a lantern, and the answers are vanishing.
Detective Roshan's montage finds the hidden town; a whirlpool rescue, a
bathhouse investigation (clue, test, lesson, feast, dark-out), a show where a
giant Boom Shell swallows every voice, and Roshan's quiet whistle bring the
lanterns back. Each chapter maps to an existing game verb, so the book can
become a playable chapter reached from Rumi's pool.

## 2. Sources

All book files live only on `rescue/peter-20261015-arborist-start` at
[`c3e0da51`](https://github.com/Ebonyks/mermaid-roshan-reef/tree/c3e0da5107b9f3d18be4a07ffa3183196ddeb574/assets_src/books).
Read text with `git show c3e0da51:<path>`; hashes are SHA-256 of the git
blob bytes (a checkout with `core.autocrlf=true` changes text-file bytes).

| File at `c3e0da51` | SHA-256 |
|---|---|
| `design/chapters/RUMI_UNDERPOOL_BOOK_20261009.md` (chapter record with every dated owner note) | `bd5d7775501069af9db520ae68164801cfd8d8eb1f06041eaeb603a862ca8051` |
| `assets_src/books/rumi_visual_detective_20261012/story_script.json` (latest script) | `ab77f7740592a82b9185c10eb22a7b85ff785726b2f9eb8f01158861d54db6cd` |
| `assets_src/books/rumi_visual_detective_20261012/MANUSCRIPT.txt` | `38acb28035596b04f3f479f401cff7d407aaff90233ee6ade833bca186b12221` |
| `assets_src/books/rumi_visual_detective_20261012/selected_art.json` (the 32 selected pages) | `f3492f5eebeca5c29306e7e99ed7bec29c98d599f7177f3a3a43af64670d570f` |
| `assets_src/books/rumi_voice_book_20261011/story_script.json` | `febb9d5c7f6d82c29dcf8fa3556715577842b2284749fd2f1fea055a046d5967` |
| `assets_src/books/rumi_underpool_20261009/MANUSCRIPT.txt` (first draft, source of the silent answer-song) | `8c2515d9a3e8d213c1d5193546761598fc803e0db65bfa1e33dd3bb756337260` |

The other edition scripts and their hashes are in
[`data/current_book_metrics.json`](data/current_book_metrics.json). Claude
viewed all 32 selected page images at full size, the owner-liked city concept
and the first draft's bathhouse spread. The owner's earlier Rumi decisions
(`ODR-RUMI-BOOK-ACTION-20261011`, `ODR-RUMI-VOICE-UNIQUE-20261011`,
`ODR-RUMI-VISUAL-DETECTIVE-20261012`) are recorded in `audit/cycles/rumi-*` on
that branch and are not yet in `dev`'s register.

## 3. Rules for every package

- Follow `AGENTS.md`, the master-audit contract (`DL-AUTH-05`, `DL-AUTH-06`,
  `DL-AUTH-07`) and the [chapter guide](../../../design/09_CHAPTER_DEVELOPMENT_GUIDE.md)
  (`DL-PLAN-01` to `DL-PLAN-06`). Each package carries its own impact record.
- **Story first.** No page art until the owner has heard the revised text read
  aloud and approved it (Q3).
- Every picture is a unique, complete drawing — no crops, resizes or recycled
  panels (the owner's 2026-10-11 rule for this book). Preserve every earlier
  edition, take and reject at its original path.
- Identity anchors: Roshan `assets/characters/roshan_25d/roshan_base.png`
  (`ODR-ROSHAN-IDENTITY`; tiara outside career costume, `ODR-ROSHAN-Q14`), her
  Pop Star look `assets/opera/worlds/actors/roshan_popstar.png` with fabric
  ribbons (`MA-ROSHAN-005`), Rumi's identity sheet, the book's Hana and Nari,
  and the existing imp art. Name the tail light state per page.
- Keep the candle missing unless the owner answers Q1 otherwise; never paint
  a supposedly missing object into a search picture (`MA-OPERA-002`).
- Children's rules apply to every page and activity: no fail states, nothing
  frightening (`DL-AGE-03`, `DL-AGE-08`), no words in world art (`DL-READ-04`),
  backgrounds quiet behind dialogue (`DL-READ-01`, `DL-READ-03`).
- Protected originals stay untouched (`DL-ASSET-03`, `DL-SND-05`). New art
  records prompt, references, hashes and rejects (`DL-ASSET-02`); runtime
  assets get `ASSET_LICENSES.md` rows (`DL-ASSET-04`). No 3D resources.
- Keep generation within the caps the earlier Rumi cycles used (two takes per
  named page or board brief, cumulative accounting, a diagnosed method change
  after two failures) unless the owner sets another budget.
- Report implementation, machine evidence and owner, child and device
  acceptance separately.

## 4. Work packages

| Package | Work | Done when |
|---|---|---|
| **RB0** Land the sources | Make the book sources reachable from the work branch: bring the text sources and chapter record from `c3e0da51` onto a topic branch from current `dev` (byte-identical), or reference them by commit. The book folders hold 452 files and 759.1 MB at that commit, 752.0 MB of it in 145 images and PDFs; choose with the owner whether those binaries enter `dev`. Re-run the full suite at that head (the latest edition's own run recorded FAIL on three throne-room assertions). | Sources reachable at a pushed head with green CI; ledger and decision register updated |
| **RB1** Story script | Create a new edition folder (for example `assets_src/books/rumi_lantern_night_<date>/`) with `story_script.json` and `MANUSCRIPT.txt` converted from [`data/page_plan.json`](data/page_plan.json), applying the owner's answers to Q1–Q3. Run an independent editorial review and the meter ([STORY_REVISION §8](STORY_REVISION.md#8-targets-and-checks-for-the-new-script)). | Owner approves the read-aloud text; meter targets met |
| **RB2** Reference boards | Codex builds, from the [world bible](WORLD_BIBLE.md): the Pearl Hollow map; boards for Shell Market, the bridge gully, Kelp Park, the five bathhouse rooms, the practice room, Moon Plaza and the stage, and the inside of the Boom Shell; character sheets for Grandma Gobuk, the citizens, Duri, Hana, Nari, the imps and Roshan's three looks; prop sheets (lanterns dark and lit, clam-shell lantern, Boom Shell states, robes and sheep towels, feast dishes, detective hat and magnifier); a five-chapter colour-script strip. | Owner approves the boards; each records provenance and hashes |
| **RB3** Thumbnails | Thumbnail all 32 pages to the plan's panel sizes; check every spread's pull and reveal, seek-and-find items, quiet dialogue backgrounds and the colour script. | An editor's reading confirms at least 9 cliffhangers and every hidden item |
| **RB4** Page art | Draw unique pages from the approved boards. Extend the existing rubric with five story categories: page-turn pull, world specificity, seek-and-find present, value hierarchy behind dialogue, colour-script fidelity. Keep the owner's 4.7 target on the extended rubric. | Extended-rubric target met; owner review recorded |
| **RB5** Lettering, PDF, read-aloud | Letter the approved text with the three balloon styles and the swallowed-word effect; build the lossless PDF as before; record a read-aloud with the child if the owner chooses. | Owner and child observations recorded as observed, never inferred |
| **RB6** Chapter brief (proposal) | Fill `design/templates/CHAPTER_BRIEF_V1.md` from [GAME_INTEGRATION](GAME_INTEGRATION.md) sections 3–8: activities, asset shortlist with hashes, save plan, voice cues, risks; plan the representative activity `cleaning_station_scrub`. No runtime work. | Brief and its ledger row merged; owner asked Q6 |
| **RB7** After Q6 only | Build the representative activity, then the others, then the storybook reward — through the normal probes, impact records and device, child and owner review. | Per the chapter guide's acceptance matrix |

## 5. Owner questions

Codex proceeds on each default until the owner answers.

| # | Question | Default | Pages or work affected |
|---|---|---|---|
| Q1 | The rainbow candle: you asked for it to be "hidden". Should it (a) stay missing, with the detective montage solving this book's own mystery; (b) also leave a faint trail of ember sparks in a few backgrounds as a seed for a later chapter; or (c) be found under the pool? | (a). (b) needs your approval because it extends the Ember King story. (c) is not recommended: the Fairy route requires the candle to have been taken. | p3, p32; backgrounds for (b) |
| Q2 | Grandma Gobuk, the bathhouse keeper: an elder everyone calls Grandma, or Duri's own grandmother? | Everyone's Grandma (a new family tie is a reserved decision). The text works either way. | World bible only |
| Q3 | After hearing the revised story read aloud, may it go to art? Are the names right: Pearl Hollow, Lantern Night (or keep Song Night), the Tidebells, Grandma Gobuk, Pip? | Proceed to boards only after your yes; keep the names. | RB1–RB4 |
| Q4 | Should the book's places and characters be painted in the game's storybook style (calmer backgrounds, broad value bands, navy and purple outlines) so the same boards serve book and game, while keeping the manga page layouts? | Yes. | RB2, RB4 |
| Q5 | Who voices the new characters in the game, and may the finale optionally use the phone's microphone for "Here I am!" (tap always works alone)? | Provisional synthetic voices like the existing filler lines; no microphone until you sign off. | RB6, RB7 |
| Q6 | Commission the playable chapter "Lantern Night beneath the Pool" with the premise and boundaries in [GAME_INTEGRATION §8](GAME_INTEGRATION.md#8-draft-chapter-brief-values)? | Not yet: finish the book and the brief first, then ask. | RB7 |

## 6. Verification of this packet

Machine checks run on the packet commit are recorded in the impact record
[`design/audit_impacts/rumi-book-revision-handoff-20261017.json`](../../../design/audit_impacts/rumi-book-revision-handoff-20261017.json).
After pushing, every file listed in [MANIFEST.json](MANIFEST.json) is fetched
anonymously from the exact remote commit and its SHA-256 compared;
the receipt is `REMOTE_VERIFICATION.json` beside this README.

## 7. What this packet does not do

It changes no game file, makes or edits no image, generates nothing, accepts no
art or story, closes no finding and commissions no chapter. The game-wide
master audit remains `UNSATISFIED`.

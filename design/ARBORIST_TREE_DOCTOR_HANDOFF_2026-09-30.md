# Arborist Roshan — Tree Doctor handoff

Status: `CANDIDATE` owner-directed implementation handoff, 2026-09-30.
Nothing here is implemented yet. It grants no art, voice, device, child,
owner or release acceptance.

## Owner direction (2026-09-30)

- Two Day Two jobs in the Royal Kitchen (Chef and Candy Maker) do not make
  sense. Moving the Candy Maker to another room was rejected. Instead, replace
  the Candy Maker's Day Two slot with an unused job that has its own place.
- The replacement is **Arborist Roshan on the Sky Lagoon**, who helps a sick
  tree.
- It is a **matching game**: Arborist Roshan pulls out her book and picks
  out **the tree**, **the disease the tree has**, and **the best medicine**
  for it. **Strong visual cues** guide every decision.
- Deliver two things: a **lower-level Opera House training level** and an
  **event in the Sky Lagoon** (the Day Two job).
- Arborist artwork already exists.

The chapter guide delegates the detailed plan below (`DL-PLAN-01`). The
choices marked "default" in the open questions at the end are the agent's
recommendations, not owner decisions.

## Step 0 — locate and commit the Arborist art (blocking)

As of this handoff the Arborist art is **not in the repository on any
branch** (all 514 branch tips searched) and not in the connected Google
Drive. The master audit records it as untracked files in a local Codex
worktree, `codex/arborist-tree-doctor` (stale base `ecad384e`), alongside an
earlier surface/save/probe prototype with inspect, prune, root-water, wrap
and bloom phases.

1. Commit the art from that worktree on a fresh branch from `dev`. Do not
   modify originals; save derivatives separately. Textures ≤1024 px on the
   longest side or power-of-two. Add one `ASSET_LICENSES.md` line per file
   in the same commit, with provenance.
2. The old prototype's code predates the Canvas-room career routes and
   Chapter 2. Use it for reference only; build on current `dev`.
3. Fill in this role table with real paths. If a role has no art, record it
   as a gap and ask the owner; do not substitute invented art.

| Role | Used by | Must read clearly as |
|---|---|---|
| Arborist Roshan costume: idle, walk/swim, reach, book-open cells; career card portrait and crest | Both parts | Roshan in tree-doctor gear; same identity as `assets/characters/roshan_25d/` |
| Tree Book: closed, opening, open spread, page turn | Both parts | A big friendly picture book |
| Tree species cards (3–4) with matching in-world trees | Both parts | Each species has a distinct silhouette, leaf shape and trunk colour |
| Condition cards and badges (see the cue table) | Both parts | One icon and one colour per condition |
| Medicine props with badge labels | Both parts | Each medicine wears its condition's badge |
| Sky Lagoon party tree: sick, part-healed, healed, blooming | Part B and the lawn finale | Same tree in every state; matches the Sky Lagoon style |
| Training level set (greenhouse or tree nursery with potted patients) | Part A | Use the Arborist world art if it exists; otherwise the Sky Lagoon tiles, as the Farmer does |

## The game: Roshan's Tree Book

Every patient tree plays the same loop:

1. **Go to the tree.** Roshan travels to it; touching the tree makes her pull
   out her Tree Book (a short authored book-open action).
2. **Page 1 — Which tree?** Match the tree.
3. **Page 2 — What's wrong?** Match the sickness.
4. **Page 3 — Which medicine?** Match the medicine.
5. **Help.** Roshan carries the chosen medicine to the tree and uses it with
   one verb (pour, spray, tap or circle). The tree visibly changes.
6. **Bloom.** Payoff: the tree perks up and blooms; the book gets a sticker
   of that tree.

Roshan performs the help step herself at the tree, never through a detached
remote tool (`DL-INT-02`, `MA-PLAY-004`).

### Visual cue grammar

Every correct answer is tied to what the child sees by three redundant cues:
**the same picture, the same colour, and the same icon**. No reading is ever
needed.

- **Tree page.** A leaf from the real tree floats into the book and hovers
  over the page. Exactly one card shows the same leaf outline, silhouette and
  trunk colour.
- **Sickness page.** A magnifier bubble on the tree shows the symptom with
  its badge. Exactly one card shows the same badge.
- **Medicine page.** Each medicine wears its sickness's badge on the label,
  and its liquid, ribbon or glow is the badge colour. The chain is
  picture-to-picture: symptom badge → sickness card → medicine label.
- **Carry-over.** Each correct pick leaves its sticker in the page corner, so
  the next page shows what is already known.

| Sickness (gentle wording) | On the tree | Badge | Medicine | Help verb |
|---|---|---|---|---|
| Thirsty | Droopy leaves, cracked dry soil | Blue water drop | Watering can | Pour on the roots |
| Spotty leaves | Orange dots on leaves | Orange dots | Leaf spray | Hold to spray over the leaves |
| Bug tickles | A few little green bugs | Green bug | Ladybug helpers jar | Tap to let the ladybugs out |
| Broken branch | A zigzag crack in a branch | Zigzag crack | Bark bandage | Circle to wrap |
| Hungry roots | Pale yellow leaves, roots peeking out | Yellow leaf with sprout | Plant food | Pour a sprinkle at the roots |

Nothing is frightening or dying: bugs are small and cute, and sickness reads
as "not feeling well" (`DL-AGE-08`).

**Distinctness rules.** At the easy tier, wrong cards differ from the right
one in both colour and shape. At the harder tier a wrong card may share one
attribute but never both. Cards are at least 160×200 base-canvas pixels with
clear gaps (`DL-UI-03`).

### Help, wrong picks and assistance

- **0 s:** a voiced question plays, and the source (floating leaf or symptom
  badge) pulses.
- **5 s idle:** the correct card breathes gently, and a dotted sparkle trail
  runs from the source to it.
- **10 s idle:** a moving hand demonstrates tapping the correct card. The
  demonstration never answers (`DL-INT-06`).
- **Wrong tap:** the card wiggles back into place with a soft sound and a
  voiced cue repeat ("Look for the orange dots!"). That page's help jumps to
  the 5 s level. Nothing is lost, and wrong taps never answer (`DL-AGE-03`,
  `DL-AGE-05`, `DL-INT-05`).
- Only a fresh, intentional tap on the correct card answers. Waiting, holding
  or passive input never completes a page (`DL-AGE-04`).

### Voice lines

Every required objective needs an exact spoken cue (`DL-SND-01`). Alpha lines
use the existing synthetic Roshan configuration in a new folder; owner
listening is pending and no family voice is cloned. Captions are supplemental.

| Beat | Line |
|---|---|
| Book opens | "Let's check my Tree Book!" |
| Tree page | "Which tree is this? Find the same leaf!" |
| Sickness page | "What's making it sick? Find the same picture!" |
| Medicine page | "Which medicine helps? Find the same sticker!" |
| Right tree | "It's a <species> tree!" (one line per species) |
| Right sickness | "It's thirsty!" / "It has spots!" / "Bugs are tickling it!" / "A branch is broken!" / "Its roots are hungry!" |
| Right medicine | "Water!" / "Leaf spray!" / "Ladybug helpers!" / "A bark bandage!" / "Plant food!" |
| Help | "Pour it on the roots!" / "Spray the leaves!" / "Let the ladybugs out!" / "Wrap the branch!" / "Sprinkle the plant food!" |
| Wrong pick | "Let's look again at the <badge>!" |
| Healed | "The tree feels better!" |

## Part A — Opera House training level: "Tree Doctor Training"

- **New career:** Arborist, next free Opera save bit **18** (costume
  `arborist`). `OPERA_ACTIVE_STAR_MASK` becomes `0x7BDEF`. Retired tombstone
  slots 4, 9 and 14 stay untouched.
- **Home:** launched from the Opera Hall venue, per the owner's "Opera House
  training level" (the hall then hosts four careers). Update `DL-INT-12`, the
  career-count contract `DL-INT-07`, the room map in `design/01_GAME_DESIGN.md`,
  and `CastleCareerRoutes.ROOM_ACT_INDICES`.
- **Content:** three potted patient trees, about 2–3 minutes. Easy tier: two
  cards per page. In Day Two's practice the three sicknesses are Thirsty,
  Spotty leaves and Broken branch, so every verb the lawn needs (pour, hold to
  spray, circle to wrap) is practised first (Day Two story draft v2,
  `design/day_two_story_v2/00_DAY_TWO_PLOTLINE.md`, J1); Bug tickles joins
  the replay variety. Curtain call and career star at the end, like the other
  careers.
- **Replay growth:** copy the Teacher career's pattern.
  `scripts/teacher_lesson_plan.gd` already does deterministic, reading-free
  choice sets that grow from two to three cards after repeated clean wins.
  An `ArboristCasePlan` should do the same for trees, sicknesses and medicines.
- **Save:** the career star uses the Opera bit; mastery lives in a new
  additive dictionary key with defaults (`DL-SAVE-01`).

## Part B — Sky Lagoon event: "The Party Tree" (Day Two job 3)

### Story

The big tree beside the Sky Lagoon lawn, where the party will be, is sick.
Arborist Roshan heals it so her friends can gather under it. At the party it
shades the table in blossom, and when the Ember King takes the candle, the
tree they saved is still there.

### Where and how the child gets there

- The tree stands on the same central Sky Lagoon screen the lawn finale uses,
  reached by leaving the castle onto the Sky Lagoon promenade
  (`scripts/arena/sky_lagoon_promenade.gd`).
- Guidance: voice "The party tree is sick! Let's go help it!", an objective
  picture of the tree, and a moving pointer first on the castle door and then
  on the tree. No floating button; the tree itself is the hotspot.
- Roshan walks to the tree before the book opens.

### Play

The party tree is one species from the book, with **two sicknesses in
turn**: Thirsty (water), then Broken branch (bark bandage). Three cards per
page at the harder distinctness tier, with the same assistance ramp. Page one
also carries easy-tier help, so a child who never played the training level
still succeeds. The training level is not a prerequisite; the production
spine forbids a tutorial prelude.

Four story phases fit Chapter 2's existing four-phase slot:

| Phase | What completes it |
|---|---|
| TREE | The tree page is matched |
| THIRSTY | Sickness and medicine matched; Roshan waters the roots |
| BRANCH | Sickness and medicine matched; Roshan wraps the branch |
| BLOOM | The tree blooms; the job completes |

### Chapter 2 changes

- **Swap the job:** Arborist (bit 18) replaces Candy Maker (bit 3) at step 3.
  - Sequence `[6, 0, 3, 10, 2, 13, 11, 1]` becomes `[6, 0, 18, 10, 2, 13, 11, 1]`.
  - Chapter mask `0x2C4F` becomes `0x42C47`.
  - First wave `0x0449` becomes `0x40441`.
  - Update the production spine in the same change; the document audit checks
    its mask and sequence against `ChapterTwoPartyPlan`.
- **Persistent tree state:** new additive key `chapter2_party_tree_phase`
  (0 sick, 1 identified, 2 watered, 3 wrapped, 4 blooming). Save after every
  phase and resume mid-event. The promenade tree and the lawn finale both
  draw the saved state.
- **Cake:** without the Candy Maker, Chef finishes the cake. Chef gains a
  final PLACE STRAWBERRIES phase, reusing the existing five-strawberry cake
  art, and that phase sets cake bits 5 and 6. Update the cake visual
  progression contract (its `0x3F` and `0x7F` rows).
- **Lawn finale:** add a `PartyTree` earned node. Scene 1 gathers everyone
  under the blossoming tree; Scene 5 lists the tree among what the King could
  not take. Replace the Candy Maker row in the finale's earned-objects table.
- **Old saves:** a legacy Candy Maker bit 3 in `chapter2_party_piece_mask`
  credits the Arborist job and sets the tree to blooming, so no child is sent
  backwards and completed saves stay complete. A partial Candy Maker phase
  record resets that slot to not started. Never remove keys.
- **Candy Maker** remains a normal freeplay career in the Kitchen.

## Engineering map

Keep new logic out of `scripts/main.gd` (`DL-CODE-01`); give it thin
delegation only.

- **New:**
  - `scripts/arborist_case_plan.gd`: pure data for species, sicknesses,
    medicines, badges, tiers and choice sets.
  - `scripts/opera_arborist_surface.gd`: the Tree Book surface, modelled on
    `scripts/opera_teacher_surface.gd` (choice rectangles, guidance events,
    progress snapshot and restore).
  - A Sky Lagoon party-tree node that draws the saved tree state on the
    promenade and the lawn.
- **Change:** `opera_house.gd` (new act), `save_state.gd` (mask and keys),
  `castle_career_routes.gd`, `opera_career_world_2d.gd` (book mode),
  `chapter_two_party_plan.gd`, `chapter_two_director.gd`,
  `chapter_two_career_scene_adapter.gd` (Arborist phases and Chef PLACE),
  `chapter_two_giant_cake_2d.gd`, `chapter_two_lawn_finale_2d.gd`,
  `arena/sky_lagoon_promenade.gd`, and the voice catalog.
- **Probes:**
  - New `probe_arborist.gd` covering right answers, wrong taps and
    demonstrations never answering, passive input earning nothing, monotonic
    assistance timing, mid-page resume, focus loss and teardown.
  - Update `probe_chapter2.gd` (sequence, masks, migration),
    `probe_chapter2_lawn.gd` (tree node), the Opera career-count probes,
    and the trusted probe lists in both CI entry points.
- **Docs:** production spine, cake progression, lawn finale draft,
  `DL-INT-07` and `DL-INT-12`, the game design room map, the document ledger,
  and an audit-impact record covering every changed file.

## Acceptance

- Exact Godot 4.7.2 import and the full trusted probe suite green in CI.
- Mobile captures of every book page and every party-tree state at two
  aspects.
- Target device at 30 fps with repeated enter, leave and re-enter.
- Child check: the four-year-old picks the right card on the first or second
  try on each page without an adult reading anything.
- Owner review of the art, cues and voice lines.

## Open owner questions (defaults recommended)

1. Freeplay home for the training level: the Opera Hall venue (default,
   per "Opera House training level").
2. Party tree species and sicknesses: the book's blossom-style species with
   Thirsty then Broken branch (default).
3. Candy Maker leaves Day Two entirely and stays a freeplay career (default).

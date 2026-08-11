# OPERA CAREER DIVERSIFICATION — rough draft (2026-08-10)

> **STATUS: rough draft for discussion. Doc-only — nothing here is
> implemented.** This drafts where each of the thirteen careers should
> actually live, what replaces the boss fights, and how the dress-up
> element gets a context worth dressing for. It is built strictly from
> resources already in the repo and from owner rulings already on record;
> where it goes beyond a ruling it says so and asks.
>
> **Companion:** `OPERA_DIVERSIFICATION_STORY_THREAD_2026-08-11.md`
> supplies the connective story — the hub loop, the "why this room, why
> now" clockwork, and the per-act story cards that tie these venues into
> one birthday-day narrative.

---

## 1. The three complaints, diagnosed against the shipped build

**1a. "The opera house career games make little narrative sense."**
Correct, and the build shows why. Thirteen unrelated professions — a
farmer, a stuffie surgeon, an astronaut engineer — sit behind one Opera
House menu (`opera_lobby_2d.gd`: three floor tabs, 4/4/5 picture cards,
finale card per floor). The in-fiction excuse is that each career is
"tonight's show performed for the family," and `OPERA_NARRATIVE_AUDIT_
2026-08-02.md` never even questions it — it is a fig leaf. The child is
not visiting an opera; she is picking act 7 of 13 from a menu strip. The
castle she spent Chapter 1 learning — with a real kitchen, library,
playroom, and bath — sits unused one door away while a painted "pastry
district" pretends the cake is a stage act.

**1b. "The boss fights are terrible."** There are two different boss
problems, and they need different knives:

- **The three floor bosses** (Curtain Dragon, Shadow Phantom, Midnight
  Maestro — acts 4/9/14) are a legacy 3D hide/peek/tap-the-sparkle grind
  (`opera_act.gd` `kind == "boss"`, `boss_hp` 12–15). They are the *last
  live 3D proscenium content in the opera*, they gate floors that
  shouldn't exist, and they connect to no chapter's plot. The owner has
  already ruled them **cut** (`CHAPTER2_BIRTHDAY_REVIEW_2026-08-03.md`
  §16–17). This draft treats that as settled.
- **The per-career rival finales** are the subtler failure. The rival's
  score bar is a wall-clock fake — `opera_competition.gd` computes
  `wanted = (elapsed/par_time)*cap*rhythm`, and the player's own
  `competition_progress()` returns 0.0 until the finale starts. The
  costumed rival imp is hidden until the last ~30 seconds
  (`_set_finale_visible(false)`; the probe *asserts* he stays hidden),
  so a fully animated thirteen-state character appears for one beat and
  races a stopwatch for no spoken reason — which the narrative audit
  flags as its trap #3: "an opponent who opposes for no spoken reason is
  genuinely scary at 4."

**1c. "The dress-up element is fun, but starved of context."** There is
no interactive career wardrobe at all — career costume is one static
512×512 actor card (`assets/opera/worlds/actors/roshan_<career>.png`,
loaded at `opera_career_world_2d.gd:398`). The fun is currently entirely
narrative — and the canon that makes it sing (the mirror imps who copy
her costume because *they think the costume is the magic*, §18–19) is
barely used by the shipped game.

## 2. What is already ruled (not re-litigated here)

- **§10 — distribute the shows through the castle.** The Opera House
  stops being the hub and becomes one venue among many. Rooms promote
  the jobs that belong to them.
- **§11 — no forced fits.** A career that doesn't honestly fit a frame
  gets a structural role or is excused, never argued in. The racer is a
  transition/transport character, not a table piece.
- **§12 — the roster is a design variable.** Deferral is scheduling,
  not deletion; adding a career is the expensive direction.
- **§16/§17 — the three floor bosses are cut.** Real boss fights belong
  to the Ember King's henchmen (existing ember content), with the Ember
  Prince as the child-scale antagonist.
- **§18–§20 — the mirror imps are the spine.** The costumed imp arrives
  early in each act, copies badly, and the theft is procurement for the
  Prince's duplicate party — not mischief.

What those rulings *don't* yet have is an implementation-facing map
against the shipped rooms, engines, and release-gate state. That map is
this draft.

## 3. The stay/move map

The castle ships thirteen rooms (`arena/castle_rooms_25d.gd` ROOMS) plus
the courtyard. Every career already owns a painted walkable district
(`assets/opera/worlds/backdrops/world_<career>.png` + composed tiles +
`opera_stage_paths.gd` walk routes) — so **relocation is a re-homing of
entry points and framing, not a rebuild of thirteen worlds.** V1 keeps
each career's painted world exactly as shipped; only where you *enter it
from*, and the story told at the door, changes.

### Stays in the Opera Hall — the three real stage jobs

| Career | Why it belongs on a stage |
|---|---|
| **Ballerina** | dance is literally a performance; her finale is a recital |
| **Pop Star** | the concert; mic, echo song, encore — stage furniture already |
| **Magician** | the show you watch; the vanish/cabinet/portal set IS a stage act |

The Opera Hall room keeps `OperaLobby2D`, shrunk from three floors to
**one screen of three performance cards** (plus, later, whatever finale
the Ember arc stages there). The opera stops being the front door to
thirteen jobs and becomes what its art always was: the castle's theatre.

### Moves into a shipped castle room — entry point re-homing, cheap

| Career | New home | Grounding in shipped resources |
|---|---|---|
| **Pastry Chef** | **Royal Kitchen** | the room is already interactive: oven, sink, four copper pans, royal fridge with a food menu (`castle_rooms_25d.gd:270,:349,:442`); the career's own hearth-oven/mixing-bowl district reads as the kitchen's "big bake" |
| **Candy Maker** | **Royal Kitchen** (candy cart at the door) — see open question Q1 | same room, second maker; sweets are made where food is made |
| **Detective** | **Royal Library** | evidence shelves, magnifier tower and `lens` mode map directly onto a library's shelves and quiet searching |
| **Painter** | **Craft Room** | the room already hosts `castle_logo_studio.gd`; his easel-and-paint-pots district is the craft room's big project |
| **Stuffie Surgeon** | **Stuffie Playroom** | the patients ARE stuffies; the room already owns the stuffie companion wing (`companion.gd` care verbs) |
| **Boxer** | **Stuffie Playroom** (toy ring) — see Q2 | play-fighting belongs where the toys live; `stuffie_battle.gd`'s one-button + DODGE QTE machinery is resident |
| **Nursery Nurse** | **Bubble Bath** | bath-time and babies are Faron's own domain; the act's WASH/FEED/BEDTIME beats are bath beats already |
| **Astronaut Engineer** | **Mermaid Pool** | the bubble rocket launches through water; pool = launch pool. (Galaxy zone is the long-term candidate — see §7) |
| **Farmer** | **Courtyard** (outdoor picnic garden) — see Q3 | feeding animals is outdoor work; keeps the Family Dining Room purely for the party feast |

### Structural, not a room show

| Career | Role | Grounding |
|---|---|---|
| **Racecar Driver** | **the transport character** — the interstitial that carries her between rooms/zones; his act launches from the courtyard (the way out of the castle) | already ruled §11; the rebuild made RACE! a real 3D `KartGame` lap, and `kart.gd` (E4) is a full config-driven engine. The career act stays playable; it just isn't a "show" |

Count check: 3 stage + 9 room/courtyard + 1 structural = 13. Every
hosting room is **shipped today**; nothing waits on the unbuilt reef
promenade, the orphaned courtyard interactables (OW-6 must be fixed for
farmer/racer — see §8), or the un-migrated northern kingdom.

## 4. What replaces the boss fights

**4a. The floor bosses go, and take the last 3D opera branch with them.**
Retiring `kind == "boss"` deletes the only remaining path that builds
the 3D proscenium, avatar, camera and HUD. Their save bits (acts 4/9/14)
retire in place — bits kept, indices stable, no key removed
(save-compat rule). The dragon/phantom/maestro art stays in the repo as
characters-in-waiting, per the ruling.

**4b. The career finale stops being a fake race and becomes the §20
mirror arc.** The redesign per act, using only shipped animation states:

1. Opening scuffle vs plain `imp_mischief` rabble (unchanged).
2. **The costumed imp walks in** (`_hop_a/_hop_b` + stage-path
   movement) — announced with one line, e.g. the Captain's voice: *"You!
   Learn the cake!"* He is visible from here on.
3. During the job beats he **copies her badly** in the background —
   `_taunt`, `_windup`, `_stagger` are exactly this vocabulary. Wrong
   hat. Upside-down whisk. Funny, then a little sad.
4. The theft (unchanged mechanically): he can't make it, so he takes it.
5. The finale reframes from "beat the stopwatch" to **"she catches him
   doing her job."** Presentation change, not systems rewrite: the two
   bars become *her real thing* vs *his copy*, and `opera_competition
   .gd`'s unread `contest` sentences finally get spoken (fixing
   narrative-audit defect D4) so the competition is explained out loud.
   The nursery keeps its cooperative branch (no rival — Faron partners).
6. He loses gracefully and gets his one character line (§19's
   per-imp wants: the candy imp ate the evidence; the ballerina imp can
   actually dance and nobody ever watched).

One probe contract inverts deliberately: `probe_opera_2d`'s "keeps the
rival hidden during earlier minigames" becomes "the costumed imp arrives
after the opening scuffle and before the steal" — rewritten in the same
commit, per the refactor rules.

**4c. Real boss fights are ember henchmen, staged where the story is.**
The Ember Fortress already ships the cast and structure — "Cinder Gate
Imps" (4), "Ash Imp Ambush" (6), "The Molten Throne" (dual boss with
`boss_hp` and peek/shell phases), plus `ember_imp.glb` / `ember_boss
.glb` and the arena kit. Recommendation stands at **two henchman
encounters in Chapter 2**, staged in castle rooms (one mid-chapter as
the imps get organised, one just before the party), with the Ember
Prince sighted once, wordless, before his climax crash. This is the one
genuinely new *content* item in the draft (encounter staging + the
Prince's design), and it is flagged as such in §8.

**4d. Where the antagonist lives during the acts — the gap this draft
must close.** Under §17 the mischief imps are deliberately *not* the
antagonists: they are redeemable apprentices, and the dress-up mirror is
the sympathy engine that earns the invitation payoff. But that leaves a
hole the plan has to answer honestly: for most of the chapter the only
opposition on screen is designed to be funny and forgivable, while the
actual antagonist appears once, wordless, plus two boss fights. Played
straight, that is thirteen acts with no bad guy and then a climax crash
from a stranger. The fix is to make the imps legible as **the Prince's
hands** in every act — the antagonist constantly felt, never on screen:

- **The arrival line names the boss, every act.** *"The Prince says I
  have to learn the cake!"* Thirteen repetitions build the unseen Prince
  into the chapter's standing presence — and they are the same 13 clips
  §20 already recommends, doing double duty.
- **The copy escalates across acts** (§18's own ladder): early
  imitations are funny — wrong hats, upside-down tools; late ones are
  nearly convincing. The threat grows as *competence*, not meanness —
  the only kind of menace that is safe at 4.
- **The shadow table is visible.** The imps' crate table accumulates
  their copies of the stolen pieces, glimpsed in the rooms they have
  raided. The duplicate party assembling is the antagonist's progress
  bar, told as set dressing.
- **The ember henchmen are the enforcement.** When an ember encounter
  is staged (§4c), the mischief imps are visibly nervous around them —
  one shipped `_stagger`/`_flee` pose covers it. Showing who the funny
  imps are scared of tells the child who the real villain is without
  anyone ever being mean to *her*.
- **The stolen piece goes to the Prince's table, not into a sack** — the
  theft keeps its edge because its destination is the antagonist's
  project (§18 already assumes the piece is displayed, never destroyed).

## 5. Dress-up, given a context

The costume element becomes meaningful the moment the job happens where
the job lives — an apron means something *in a kitchen*. Three moves,
smallest first:

1. **The costume moment becomes diegetic.** Each act opens with a
   one-tap "get dressed" beat at the room's door — the career actor card
   swap she already gets, but shown as a choice she makes in place
   (kitchen: toque on). Zero new art; it re-uses the shipped
   `roshan_<career>.png` actors and the same tap-a-card grammar as the
   bedroom wardrobe (`wardrobe_ui.gd`).
2. **The mirror imp makes the costume load-bearing.** Because the
   costumed imp is now on screen from beat 2 (§4b), the child sees the
   *same outfit on both of them* for most of the act — the copy canon
   (§19) told visually, no words. The dress-up stops being a skin and
   becomes the act's central joke and its lesson.
3. **(Later, optional) the wardrobe learns careers.** `player.gd:170`
   ships a dormant `costume_id` contract for layered 2D outfit atlases.
   When outfit art beyond one pose per career exists, career costumes
   can join the bedroom wardrobe as unlockables ("dress as the chef
   anywhere"). This is the expensive direction — the logical-rebuild
   spec calls more Roshan poses "the largest unscoped art item" (R4) —
   so it is explicitly deferred, not promised.

## 6. Mechanical diversification comes free with the move

The quality audit's core mechanical complaint — verb census circle ×9 /
swipe ×9, four careers owning nothing bespoke, blur pairs
(ballerina↔popstar, candymaker↔chef, boxer-JAB↔any-scuffle) — is
*eased* by relocation, because host rooms bring resident systems the
opera menu never could:

| Career | Host-room system it can borrow (all shipped) |
|---|---|
| Chef | the kitchen's real oven/pans/fridge interactions (`castle_rooms_25d.gd:442`) replace generic widgets for at least one beat |
| Stuffie Surgeon | `companion.gd` care verbs — the patient is *her actual companion stuffie*, not a prop |
| Boxer | `stuffie_battle.gd`'s one-attack + DODGE QTE — a real, tested, no-fail duel grammar to replace the "identical bop ×3" opening |
| Racer | the real `KartGame` lap (already landed in the rebuild) |
| Detective | the library room's own shelves/signs as `lens` targets instead of a painted duplicate |
| Farmer | courtyard outdoor space; garden grammar exists in `picture_games.gd` (`_mg_build_garden`) if a planting beat wants it |

Rule of thumb for the build: **when a host room already owns an
interaction, the career beat should use the room's, not a widget copy of
it.** That is what makes each act feel like its place and not like the
same surface with a different backdrop — the actual "diversification"
the complaint is about.

## 7. Deferred zone-level moves (name them now, build them later)

Three careers have a *better* long-term home than any castle room, but
each waits on an unbuilt or orphaned zone. Per §12, deferral is
scheduling:

- **Astronaut → Galaxy.** `galaxy.gd` and 11.7 MB of orphaned art
  (OW-9) are space-shaped; §11 also floats the rocket serving Chapter
  4's departure. Until then: Mermaid Pool.
- **Farmer → Northern Kingdom town/mill**, when migration #5 lands.
  Until then: courtyard.
- **Racer → Courtyard/kart proper** as the game's transport spine —
  which is also the natural driver for finally fixing the orphaned
  courtyard hub (OW-6, `_enter_level2_now` early-return).

## 8. Costs, risks, and what this does NOT touch

- **Save compatibility intact.** `opera_stars` stays the 16-bit record;
  pieces/stars only *present* differently. No key removed or
  repurposed. Boss bits retire in place.
- **No career world art is rebuilt.** All 12 painted districts, stage
  tiles, walk paths, 156 rival files and 13 actor cards ship unchanged.
  (`world_nursery.png` remains the one missing backdrop — OW-14,
  pre-existing.)
- **Prerequisite: the release-gate blockers land first.**
  `RELEASE_GATE_VERDICT_2026-08-05.md` is DO-NOT-PROMOTE (B1 pipe
  dead-end, B2 infinite tray, B3 detective retry amputation, B4 BAKE
  self-completion, B5 kart never sets `m.game`, B6 real-merge/probes).
  Re-homing a broken act just moves the breakage into nicer rooms.
- **Main build cost is per-room affordances:** one themed hotspot/card
  per hosting room + one line of dialogue each (§10's own estimate),
  the lobby shrink, and the finale re-presentation. The genuinely new
  content is confined to §4c (ember encounters + Prince design).
- **Probe surface:** each phase below is probe-gated; the one deliberate
  assertion inversion is called out in §4b. Doc precedent for gating:
  every hosting room already has probe coverage via the castle suite
  (`probe_kitchen_props.gd` is in `ci.sh`).

## 9. Phased plan (each phase independently shippable, probe-gated)

1. **Phase 0 — gate fixes.** Land B1–B6. No design change.
2. **Phase 1 — re-homing.** Room hotspots for the nine moved careers;
   Opera Hall lobby shrinks to the three stage cards; floor-ladder
   gating replaced by spatial/thematic gating (a room's card marks done
   when its piece is made). Careers behave identically inside.
3. **Phase 2 — the mirror arc.** Rival arrival moves to beat 2 with
   background copying; finale re-presented as real-vs-copy with spoken
   contest lines; probe assertion rewritten same-commit.
4. **Phase 3 — boss surgery.** Retire the three floor bosses and the
   `kind == "boss"` 3D branch; stage the two ember henchman encounters
   (owner scoping needed first — Q5).
5. **Phase 4 — diegetic costumes.** The get-dressed beat per room door.
6. **Phase 5 (unscheduled) — zone moves.** §7's galaxy/northern/
   courtyard relocations, each riding its zone's own migration.

## 10. Open questions for the owner

- **Q1 — Candy Maker co-tenancy.** Kitchen with the chef (per §10) risks
  worsening the candymaker↔chef blur the quality audit flags. Keep both
  in the kitchen with strongly differentiated stations, or park her
  candy cart in the courtyard? *Recommendation: kitchen, cart at the
  door, differentiated by the room's own oven going to the chef only.*
- **Q2 — Boxer venue.** Playroom toy ring (per §10), or courtyard party
  games? The sash-as-passing-prize canon (§15) works in either.
  *Recommendation: playroom — the stuffie-battle machinery lives there.*
- **Q3 — Farmer venue.** §10 lists Family Dining Room; its own open
  question prefers the courtyard so the dining room stays the feast.
  *Recommendation: courtyard, with the dining room table as where his
  picnic lands.*
- **Q4 — Does the racer act remain playable in Chapter 2** (from the
  courtyard) once he is the transport character, or is the kart lap
  itself his whole presence? *Recommendation: keep the act playable —
  built content stays playable (§12), and B5 fixes it anyway.*
- **Q5 — Ember encounters:** confirm two for Chapter 2, and commission
  the Ember Prince design (the one new character this plan needs).
- **Q6 — Lobby afterlife:** when the lobby shrinks, do the floor names
  (Lagoon Lights / Starlight Balcony / Grand Gallery) survive anywhere,
  or retire with the floors?
- **Q7 — Are the imps meant to be the antagonists?** This draft keeps
  them sympathetic per §17–19, with the Prince carrying the menace
  through them (§4d). The other direction — restoring the imps as true
  antagonists, closer to what ships today — is available, but it
  reverses three recorded rulings, forfeits the invitation payoff and
  Chapter 5's fancy-dress inheritance, and re-reads the mirror costumes
  as imposters-in-her-clothes. *Recommendation: keep them sympathetic;
  close the felt-antagonist gap with §4d rather than by making the imps
  mean.*

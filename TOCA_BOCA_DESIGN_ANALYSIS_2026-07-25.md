# Toca Boca World — design analysis and integration evaluation (2026-07-25)

Task: analyse Toca Boca World, then evaluate which of its designs and elements
would benefit Mermaid Roshan: Reef of Light.

This is an evaluation document, not an implementation. Nothing in the game was
changed. Every recommendation is sized against the hard rules in CLAUDE.md
(no fail states, non-reader, one finger, mobile renderer, save compatibility,
extract-don't-rewrite) and anchored to files that already exist.

---

## 1. What Toca Boca World actually is

Toca Boca (Swedish studio, "digital toys" rather than games) ships an
open-ended sandbox: no scores, no levels, no timers, no win state, and no text
tutorials. The product is a dollhouse, not a game — the child supplies the
goal. Toca Boca World is the umbrella app that merged the old per-location
Toca Life apps into one connected world (90+ locations, 500+ characters), so
characters and objects can travel between places that used to be separate apps.

### 1.1 The design pillars, as they actually manifest

| Pillar | How it shows up |
|---|---|
| **No win/lose** | No score, no timer, no failure. The only outcome is the story the child made. |
| **Icon literalism / zero text** | No written instructions and no narrator telling you the "right" way. Every affordance is a recognisable picture of the real object. |
| **Everything is reactive** | Tap anything → it moves, changes, or makes a sound. Nothing on screen is inert scenery. |
| **Non-destructive design** | Nothing can be permanently broken or lost; there is no state a child can get stuck in and no action they can regret. |
| **Shallow menus, few options per screen** | Deliberately low cognitive load: small option sets, flat navigation, consistent placement. |
| **Drag-and-drop as the universal verb** | One grammar — pick up, carry, drop, give — reused in every location. |

### 1.2 The concrete feature set

- **Character Creator** — build your own characters (hair, face, skin tone,
  outfits); the free tier caps at 3 saved characters.
- **Home Designer** — build and decorate your own houses on plots inside
  designated districts, from templates plus a furniture/decoration library.
- **Universal carry** — pick up, move, and combine virtually any object;
  interactions are discovered by *putting an object into a character's hands*
  or feeding it to them.
- **Combination play** — the cooking combo: drop food items together and get
  surprising results; "wrong" combinations produce funny reactions, never errors.
- **Photo booth** — pose, pick a background, snap and keep the picture.
- **Scheduled surprise** — a Post Office gift arrives every Friday. A reason to
  return that is a present, not a streak you can break.
- **Hidden things** — secret rooms, hidden pets you can drag out and keep.
- **Mix-and-match locations** — take a character from one place to any other.
  Cross-location traffic is the whole point of merging the apps.

### 1.3 The thing most analyses miss

Toca's "no goals" works partly because **navigation is free**. Locations are
flat side-view dioramas: everything interactable is visible at once, one tap
away, and you can never be lost or facing the wrong direction. Remove goals
from a *3D* world and you get a lost child, not a free one. This is the single
most important caveat for us and it drives §4 below.

---

## 2. Where Reef of Light already agrees with Toca Boca

More than expected. The project independently arrived at most of Toca's
child-design pillars:

| Toca pillar | Already in this game |
|---|---|
| No fail states | Hard rule. MedalSystem is upgrade-only, a medal is always *added*, never denied, and no game ends early on performance (MEDALS.md). |
| Zero text dependency | Hard rule: every objective fires `_say()` plus a visual pointer. Sticker glyphs, medal glyphs 🥉🥈🥇, no gamerscore. |
| Non-destructive | GrottoPuzzle is explicitly deadlock-free *by construction* — she swims, so every block position is recoverable (`scripts/grotto.gd`). Save has backup/recovery and never drops keys. |
| Shallow menus | Overlays (craft, wardrobe, stickers, collection) are single-screen with big targets; ≥110 px tap targets is a stated rule. |
| Carry as a verb | `scripts/carry_system.gd` — scoop, carry, throw, with a generous no-fail 5 m hit window. |
| Make your own characters | `scripts/craft_studio.gd` — colour your own fish and friends; they persist (`custom_fish`, `custom_friends`) and get spawned into the world. |
| Your choices change the world | The Pearl Shop animal tanks: buying a stingray *releases it into the reef forever* on its real patrol route (`ANIMAL_SHOP`, `scripts/games/shop.gd`). This is a better idea than anything in Toca's shop. |
| Hidden things to find | Sticker book, `scripts/collection_system.gd` critters, singing shells. |

**Conclusion:** the gap is not philosophy. The gap is **surface area of
free play** — the number of things a child can touch with no objective attached.

---

## 3. Where the game structurally diverges (and what that costs)

1. **Objects are scenery, not toys.** The reef is dense with props
   (`_gen2_prop`, `KIT_GEN2`, flora, castle furniture) and almost none of them
   respond to being touched. Toca's rule is that *every* object rewards a tap.
   Here, only the two starfish, two singing shells, the playground toys
   (`_toy_anim`), and minigame props react. Everything else is wallpaper.
2. **Carry is hard-coded to four objects.** `CarrySystem._build()` spawns
   exactly 2 starfish and 2 shells at literal coordinates. The verb is built;
   the content is a rounding error.
3. **There is no room that belongs to the child.** There is a royal bedroom
   (`castle_hall.gd:build_bedroom`), five dream bedrooms, and a craft wing —
   all authored, none arrangeable. Nothing in the game persists a *placement*
   the child chose. Home Designer is Toca's most-played feature and we have
   zero of it.
4. **You are always Roshan.** Wardrobe skins are mutually exclusive full-body
   re-skins (`SKINS`), not a character roster. Toca's "who am I today" is a
   large part of its replay. Note that `scripts/stuffie_battle.gd` already
   proves the engine can hand the player a non-Roshan body.
5. **No photo/snapshot.** For a game literally built out of a family
   storybook, with a page-frame renderer already present
   (`_build_page_frame`), this is the most on-theme missing Toca feature.
6. **No combination play.** Nothing in the game says "put two things together
   and see what happens." The Can of Beans is the lone joke in that direction.
7. **Progression is almost entirely goal-shaped.** Sparkle the guide fish
   points at the next unwon friend; stars, medals, trophies, a finale. This is
   correct for a 3D world (§1.3) — but it means an unstructured session has
   little to do once the pointer has nothing to point at.

---

## 4. Recommendations, ranked

Ranking is by (value to *this* child) ÷ (risk + effort). Every item is
additive — none of them removes a goal, a medal, or the guide fish.

### Tier 1 — take these

#### R1. Reactive props pass ("everything answers")
**The single highest-value Toca idea for this codebase.** Give every world prop
a touch response: a wobble, a chime, a bubble puff, a sparkle. Bump the coral,
the coral bobs. Tap the castle chair, it rocks. Swim through the kelp, it parts.

- *Why it wins:* it multiplies perceived content across the entire existing
  world with **no new art, no new textures, no new lights** — the assets are
  already placed.
- *Where:* a new satellite `scripts/reactive_props.gd` (RefCounted, receives
  `main`, per the Phase 7 pattern), driven off the same proximity test
  `CarrySystem` already uses. Tag props at build time with a `react` meta in
  `_gen2_prop`, so one line covers every prop that helper places.
- *Cost:* low. *Risk:* low — cosmetic only, touches no progress state, so
  `probe_passive` stays silent as long as reactions award nothing.
- *Constraint check:* no new textures, no new OmniLights, mobile-safe.
  Cap concurrent reactions and reuse pooled tweens for Speedy tier.

#### R2. Generalise the carry system
Make "carryable" a prop tag instead of four hard-coded spawns. Any prop tagged
`carryable` can be scooped, carried, and set down. Shells, small corals,
starfish, a bucket, the beans can.

- *Why it wins:* the code exists and is proven; only the content gate is
  artificial. Universal carry is the Toca verb, and it's already 90% built.
- *Where:* `scripts/carry_system.gd` — replace the literal spawn list with a
  scan for the tag; keep the throw physics and the shell-chime reward exactly
  as-is.
- *Cost:* low. *Risk:* low. Must preserve: dropped objects return to a seat
  position (non-destructive — a child must never lose a toy under the terrain).
  Add a "goes home when you leave" rule rather than persisting positions.

#### R3. Roshan's room — the Home Designer idea, scoped down
Give the royal bedroom a small set of movable things and persist their
placement. Not a building tool: a **doll's-house shelf**. Six to ten props, a
"put it here" pointer, snap positions, done.

- *Why it wins:* it converts the Pearl Shop from a cosmetics vendor into a
  furniture shop — a real pearl sink, which the code comments already ask for
  ("real things to save up for instead of a number that only ever grows"). It
  gives the child a place that is *hers* and a reason to re-enter the castle
  outside a quest.
- *Where:* `scripts/arena/castle_hall.gd:build_bedroom` for the host room; a new
  satellite for the placement overlay. New save key `"room"` (dictionary of
  prop id → slot index), added with a default — never removes an existing key,
  same additive pattern as `"critters"` and `"medals"`.
- *Cost:* medium. *Risk:* medium — this is the only Tier 1 item that adds
  persisted state, so it needs a `probe_room.gd` covering place → save →
  reload → still there, and `probe_passive` must confirm zero-input play
  places nothing.
- *Scope discipline:* snap slots, not free 3D placement. Free placement on a
  phone with one finger at age 4 is a frustration generator, and it can bury
  props inside geometry — a non-destructive-design violation.

#### R4. Storybook snapshot (photo booth, on-theme)
A shell-shaped camera prop. Tap it, Roshan strikes a pose, the screen flashes,
and the picture lands as a page in the sticker book / storybook frame.

- *Why it wins:* highest charm-per-line in the list; the page-frame renderer
  (`_build_page_frame`) and the sticker book already exist, so this is mostly
  glue. It rewards the wardrobe and craft studio by giving their output a place
  to be admired — Toca's photo booth exists for exactly that reason.
- *Where:* new satellite; reuse the existing overlay layer conventions in
  `wardrobe_ui.gd`.
- *Cost:* low-medium. *Risk:* low. Store a small fixed-size set (e.g. last 6
  photos, ring buffer) as a new save key. Keep captures ≤1024 px per the
  texture rule and write them under `user://`, never into `assets/`.

### Tier 2 — take these next

#### R5. Bring a friend with you
Let a chosen story friend follow Roshan between areas, the way `companion.gd`
already does for stuffies. Toca's whole merged-world thesis is that characters
travel between locations.

- *Why:* huge perceived-content gain from existing characters; makes the world
  feel populated rather than a set of stations.
- *Cost:* medium — needs a follow path that survives arena transitions.
- *Risk:* medium — friends currently hide during minigames so they never
  photobomb an arena (`main.gd:2076`). That rule must hold; the follower parks
  at the arena entrance.

#### R6. The Friday shell (scheduled surprise)
On the first launch of a new calendar day, a wrapped gift shell sits at the
reef mouth. Tap it: a sparkle, a voice line, and a small treat — pearls, a
sticker, a craft swatch, a room prop.

- *Why:* a reason to come back that is a **present, not a streak**. Nothing is
  lost by not playing; there is no counter to break.
- *Cost:* low. *Risk:* low-medium — needs a new save key for the last gift day
  and must be robust to a device clock that moves backwards (clamp: if the
  stored date is in the future, treat it as today and grant nothing rather than
  granting forever).
- *Hard requirement:* the gift must require a tap. `probe_passive` asserts
  zero-input play wins nothing; a self-collecting gift would break it, and
  should — the child should get the moment of opening it.

#### R7. Be somebody else for a while
A "play as" pick for the stuffie companions in the overworld, extending what
`stuffie_battle.gd` already does inside its arena.

- *Why:* Toca's character swap is a major replay driver, and the hard part
  (a non-Roshan player body) is already solved once.
- *Cost:* medium-high — the swim controller is bespoke to Roshan's 26-bone rig
  (`player.gd`, CHARACTER_CUSTOMIZATION.md §0), so a swapped body needs its own
  locomotion or a shared simplified one.
- *Risk:* medium-high. Do this only after R1–R4 land; it is the one item that
  could destabilise the player controller.

### Tier 3 — optional, lower priority

#### R8. Combination play (the reef kitchen)
A small mixing station: drop two ingredients in, get a silly result, always
succeed. Genuinely Toca and genuinely no-fail.

- *Verdict:* charming but the minigame roster is already large and
  MINIGAME_ENGINES.md is actively trying to *reduce* per-game code. If built,
  build it as a client of an existing engine, not a new loop. Defer until the
  engine consolidation has landed.

#### R9. More hidden things
Toca's hidden pets. We have critters and stickers; this is a content pass on an
existing system rather than a new design. Cheap to top up whenever art lands.

---

## 5. What NOT to adopt

- **Do not remove goals, medals, or Sparkle the guide fish.** Toca's goal-free
  design depends on a flat 2D diorama where nothing can be missed (§1.3). In a
  3D reef, the pointer *is* the accessibility feature — DESIGN_3_0.md added it
  specifically to end "empty-ocean confusion". The right model is
  **Toca-style free play layered on top of the existing guided spine**, so the
  child can ignore the pointer without the world going quiet. That is the thesis
  of this whole document.
- **Do not adopt free-form 3D object placement.** One finger, age 4, phone
  screen. Snap slots only (see R3).
- **Do not adopt the content-drip / IAP model.** No purchase gates, no weekly
  paid drops, no unlock-count limits (Toca caps free character creation at 3 —
  we should cap nothing).
- **Do not adopt deep dresser menus.** Toca's newer UI has grown menu depth the
  original apps avoided. Our overlays are shallower today; keep them that way.
- **Do not copy Toca's art, characters, UI, or icons.** Same standing rule the
  art direction already applies to Wind Waker: reference the *interaction
  design*, never the assets. Toca Boca is a live commercial IP.
- **Note for planning:** Toca Boca Days — the studio's 3D multiplayer sibling —
  was shut down in August 2025, servers off, app non-functional. Their one
  attempt at 3D and at multiplayer is the one that didn't survive. Read that as
  a caution against any networked/multiplayer direction here, and as evidence
  that translating this design language into 3D is genuinely hard — which is
  what §1.3 and R3's scope discipline are guarding against.

---

## 6. Constraint compliance summary

Applies to all Tier 1–2 recommendations:

| Rule (CLAUDE.md) | How these proposals comply |
|---|---|
| Mobile renderer everywhere | All proposals are logic/tween-level. No new shaders, no Forward+-only effects. |
| No new OmniLights | None proposed. Reactions use sparkle particles and existing emissive materials. |
| Textures ≤1024 px or POT | No new source textures. R4's captures are runtime, `user://`, and must be clamped. |
| Every new asset in ASSET_LICENSES.md | R3 room props, if any are new, get their line in the same commit. Prefer reusing already-licensed `KIT_GEN2`/gen2 props. |
| No fail states, no reading | Nothing proposed can be failed. Every new objective-ish moment (R6 gift) fires `_say()` plus a visual pointer. |
| Save compatibility | R3/R4/R6 add keys with defaults (`"room"`, `"photos"`, `"gift_day"`); no key is removed, matching the `"critters"`/`"medals"` precedent. |
| main.gd refactor rules | Every item lands as a **new satellite** (RefCounted, receives `main`, state on main), following `carry_system.gd`/`grotto.gd`. None of them adds bulk to main.gd, which is at 7,345 lines against a <2,500 target. |
| Probe gating | R3, R4, R6 need probe coverage before merge; `probe_passive` must stay silent for all of them. Per CLAUDE.md, a probe that fails after a change is a revert signal, not a probe to patch. |

---

## 7. Recommended order

1. **R1 reactive props** — biggest world-feel gain per line, zero risk.
2. **R2 universal carry** — unlocks the Toca verb the codebase already built.
3. **R4 storybook snapshot** — charm, on-theme, mostly glue.
4. **R3 Roshan's room** — the real Home Designer idea, scoped to snap slots;
   first item needing new persisted state and a new probe.
5. **R6 Friday shell** — cheap returning-player warmth.
6. **R5 friend follows you** — after the arena-transition rule is confirmed safe.
7. **R7 play as somebody else** — last; it is the only one that can destabilise
   the player controller.

R8 waits for the minigame engine consolidation. R9 is a content top-up whenever
art lands.

---

## Sources

- [Toca Boca World — official](https://www.tocaboca.com/toca-boca-world)
- [Toca Boca World — App Store](https://apps.apple.com/us/app/toca-boca-world-game-play/id1208138685)
- [Toca Boca World — Google Play](https://play.google.com/store/apps/details?id=com.tocaboca.tocalifeworld&hl=en_US)
- [Toca Boca Days (discontinued) — official](https://www.tocaboca.com/kids/toca-boca-days)
- [Toca Boca — Grokipedia](https://grokipedia.com/page/Toca_Boca)
- [Toca Boca World: A Whole New Level of Dollhouse — PlayLab! Magazine, Tampere University](https://www.tuni.fi/playlab/toca-boca-world-a-whole-new-level-of-dollhouse/)
- [Character Creator Guide](https://bocatoca.com/blog/character-creator-guide/)
- [Toca Boca World — Toca Life: World Wiki](https://toca-life-world.fandom.com/wiki/Toca_Boca_World)
- [BlueStacks Beginner's Guide to Toca Life World](https://www.bluestacks.com/blog/game-guides/toca-life-world/tlw-beginner-guide-en.html)
- [Designing for Kids: UX Design Tips for Children Apps — Ungrammary](https://www.ungrammary.com/post/designing-for-kids-ux-design-tips-for-children-apps)
- [UX Design for Kids — Gapsy Studio](https://gapsystudio.com/blog/ux-design-for-kids/)
- [Coherent UI in Toca Boca Days — Toca Boca Tech Blog](https://medium.com/toca-boca-tech-blog/coherent-ui-in-toca-boca-days-caacb7909614)

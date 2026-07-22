# STORY_DAYS.md — The Week of Light (narrative day structure)

OWNER DECISION 2026-07-22: the game's plot is organized as a **days-of-the-week
structure**. Each story day opens one land to explore. Day 1 is the Pearl
Castle itself; the Great North (the northern kingdom, with its snow queen) is
one day; the Pearl Opera House is another. This document is the source of
truth for the narrative: the frame story, the seven days, what a "day" means
mechanically, save-schema and probe implications, and the phased plan for
wiring it in. It defines structure only — no code changes ship with this doc.

Everything below is weighed against the CLAUDE.md constants: one specific
4-year-old non-reader, one finger, short sessions, no fail states, no lost
progress, mobile renderer.

---

## 1. The frame story — "Roshan's Week of Light"

Princess Huluu is planning the **Festival of Lights** at the Pearl Castle at
the end of the week. Every morning the **storybook calendar** in the castle
turns a page, and a new land opens for the day. Each day Mermaid Roshan
visits that day's land, plays with its friends, and brings home that day's
**Light** — a glowing star that clips into the festival **lantern ring**
above the calendar. On the seventh day the ring is full, and the whole cast
gathers at the castle for the Festival of Lights: fireworks, music, and the
grand celebration. After the festival, every day is a free-play day — the
entire map stays open forever.

Why this frame works for this player:

- **It gives the title its plot.** "Reef of Light" now means something: the
  week is literally about gathering the lights.
- **One simple repeated sentence per day.** "Today we visit ___ and bring
  home its Light." A 4-year-old can hold the whole plot in one breath.
- **It teaches the days of the week** — a real preschool skill — through
  play, with each weekday announced by voice and color, never by text.
- **The ending already exists.** The current finale (friends circling
  Roshan, fireworks, celebration track) becomes the Day 7 festival with
  staging added, not a new system.

## 2. What a "day" is (mechanics of story time)

A story day is a **chapter, not a real calendar day**.

- **Advancing:** when the day's Light has been earned, a big glowing **bed**
  in the Pearl Castle starts to sparkle (golden pointer + voice: "Sleepy
  time! Tap the bed when you're ready for tomorrow!"). Tapping it plays the
  page-turn: Roshan sleeps, the calendar flips, and the morning voice line
  announces the new day. Advancing is always the child's choice — never a
  timer, never automatic mid-play.
- **Short sessions are safe:** if the app closes mid-day, the same day
  resumes next launch. If the Light was earned but the bed wasn't tapped,
  the next launch offers the page-turn first thing.
- **Nothing ever re-locks.** A land, once opened, stays open on every later
  day and in free play. Day gating controls *first opening only*. This is
  the no-lost-progress rule applied to narrative.
- **Lights cannot be failed.** Each day's Light comes from the day's core
  story beat: arrive in the land and complete one short, guided,
  voice-led activity (existing minigames — all already fail-free). Every
  other activity in the land is optional bonus for that day and for free
  play.
- **Replay:** tapping an already-finished calendar page replays that day's
  morning line and celebration — the storybook can be "read" again.
- **Real weekdays, story order.** The calendar pages are named and voiced
  Monday → Sunday to teach the sequence, but they advance at the child's
  pace — a "Monday" page can happen on a real Thursday.
- The existing each-launch day↔night flip (`plays` in the save) is
  repurposed inside the frame: days start in morning light; the page-turn
  at the bed passes through night. No save key changes for this.

**Rejected alternatives** (recorded so they aren't re-litigated):

- *Real-calendar gating* (Elsa's land only open on real Thursdays):
  rejected — a locked land on the day the child asks for it is a fail
  state in all but name.
- *Auto-advance per launch:* rejected — a session might be 4 minutes long;
  burning a story day on a car-ride session loses narrative, and losing
  things is intolerable here.

## 3. The seven days

| Day | Weekday | Name (voiced) | Land | Host | Light | Color/icon |
|---|---|---|---|---|---|---|
| 1 | Monday | Castle Day | Pearl Castle (itself) | Princess Huluu | Crown Light | pink / 👑 |
| 2 | Tuesday | Reef Day | The reef overworld | Daddy Mermaid + reef friends | Pearl Light | aqua / 🐚 |
| 3 | Wednesday | Lagoon Day | Sky Lagoon | Peng Pal | Cloud Light | sky-blue / ☁️ |
| 4 | Thursday | Snow Day | The Great North | The Snow Queen (§5) | Aurora Light | ice-white / ❄️ |
| 5 | Friday | Show Day | Pearl Opera House | The Midnight Maestro's stage | Star-of-the-Show Light | red-gold / 🎭 |
| 6 | Saturday | Butterfly Day | Kart courses → Butterfly World | The fairy | Butterfly Light | purple / 🦋 |
| 7 | Sunday | Festival Day | Pearl Castle, everyone visits | the whole cast | Roshan's Light | rainbow / ⭐ |

Non-reader rule: the child never reads these names. Every page is a color +
icon + voiced announcement ("It's Thursday! Snow Day! Let's visit the Great
North!").

### Day 1 — Monday — Castle Day (owner-specified: the castle itself)

The game now *begins at the Pearl Castle*, Roshan's home. Wake up, meet
Princess Huluu at the throne, and tour the castle as the day's story beat:
the Grand Hall, the crown star, the **gift box** (choose and paint the
stuffie companion — the existing picker), the courtyard and its train, the
Toy Castle playroom, the craft studio and wardrobe. Huluu explains the week:
"Every morning, the calendar opens a new place. Bring home a Light each day,
and on Sunday we'll have the Festival of Lights!" The Crown Light is earned
at the throne after the tour. Day 1 doubles as onboarding — the existing
three timed first-session hints live here.

### Day 2 — Tuesday — Reef Day

The castle doors open to the reef — the current main overworld. Sparkle the
guide fish leads to the five friend groups and their games (fetch with Wacky
and Chuck, hide-and-seek with Evie and Lamb-a', the rainbow slide with
Harper and Fiona, Faron's dolls, Daddy Mermaid's melody stage), plus pearls,
the Pearl Shop, and the Secret Cave. The Pearl Light comes from finding the
friends and winning any one game (voice-led; the rest remain as bonus and
free play). The existing trophy/star/pearl systems continue unchanged inside
this and later days.

### Day 3 — Wednesday — Lagoon Day

The Sky Lagoon (level 2). Peng Pal hosts; the Penguin Slide and the lagoon's
own activities are the day's play. The Cloud Light is earned at the lagoon's
central landmark after the guided beat. (The current trophies/stars/pearl
portal gate to the lagoon is superseded for new saves by the calendar —
§7 covers migration.)

### Day 4 — Thursday — Snow Day (the Great North)

Through the Alpine cave: the mountain pass, the wisp trail, the pine forest,
the fjord town and docks, and the northern castle — hosted by the **Snow
Queen** (§5). The ice-themed Penguin Slide chase and the dungeon's cellar
rooms fit this day where they already connect. The Aurora Light is earned in
the northern castle with the wisps. Coldest day, warmest welcome.

### Day 5 — Friday — Show Day

Friday night at the Pearl Opera House: the three-floor Showtime-style lobby,
twelve career doors, medallion bosses, and — eventually — the Midnight
Maestro's grand finale. The Star-of-the-Show Light is earned by starring in
any one show; the other eleven doors and the bosses stay as the deepest
optional wing of the game. (The opera keeps its own internal star/medallion
progression untouched.)

### Day 6 — Saturday — Butterfly Day

Race day and the sky: the kart courses, lifting off the float track into
**Butterfly World** (the galaxy level), and the fairy flight home. The
Butterfly Light is earned in Butterfly World; the fairy-skin prize remains
its own reward. Saturday is the "big trip" day — the most out-there land
right before the festival.

### Day 7 — Sunday — Festival Day

Everyone comes to the castle. The lantern ring is full but for one socket —
the seventh Light is **Roshan's own**, lit when the festival begins: the
existing finale (all friends in a swimming circle, rainbow fireworks, the
celebration track) staged as the Festival of Lights in the castle courtyard.
Afterward the calendar shows a permanent rainbow "every day" page: free
play, everything open, forever. Replaying Sunday replays the party.

## 4. After the week — free play

Post-festival, the game is exactly today's fully-unlocked sandbox. The
calendar remains as a menu of memories (replay any day's beat), the lantern
ring stays lit in the Grand Hall, and no activity, collectable, medal, or
wing is ever gated by days again. The week is a *telling order*, not a
completion checklist — medals, opera stars, dungeon rooms, crafts, and
stuffie battles all continue to progress on their own systems across and
after the week.

## 5. IP flag — "Elsa" needs an original name and design

The owner's shorthand for the Great North's host is "Elsa". Per the standing
art-direction rules (Wind Waker precedent; the northern castle's "Elsa
silhouette" is a *reference only*) and the Gabby precedent (removed on IP
hold), the shipped character must be an **original snow queen** — original
name, design, colors, and music. Proposed working names for owner approval:
**Queen Noora** (of the Northern Lights), **Queen Elivi**, or **the Wisp
Queen**. Until the owner picks, all code/docs say "Snow Queen"
(`snow_queen`). No Frozen names, designs, symbols, or songs anywhere in the
repo — including asset prompts and voice-line scripts.

## 6. Voice lines to record (family voices — new sessions needed)

All new narrative beats are voice-first (non-reader). Needed set, in
priority order; each also fires `_say()` + a golden pointer per hard rules:

1. Seven morning announcements ("It's Monday! Castle Day!…" — one per day).
2. Huluu's Day-1 week-opener (the festival promise) and castle-tour lines.
3. Bedtime line ("Sleepy time! Tap the bed…") + page-turn goodnight.
4. Light-earned fanfare line, one generic + optionally one per day.
5. Snow Queen host lines (record after the §5 name is approved).
6. Festival Day lines: arrival, countdown, celebration.

Until recordings land, ship with the existing synth/fallback voice path so
the structure is playable — recorded lines drop in as assets, never blocking.

## 7. Save schema & migration (never lose a child's progress)

- New keys, added with defaults, following the companion-keys pattern
  (deliberately NOT added to `KNOWN_KEYS`/`CORE_KEYS` so older saves still
  read as complete):
  - `story_day`: int — 1..7 = current day, 8 = festival seen / free play.
  - `day_lights`: dict of `"1".."7"` → bool.
- **Migration for the existing family save:** any save with meaningful
  progress (e.g. `level2`, `opera_progress`, `galaxy`, or `finale` set)
  loads as `story_day = 8` with all lights lit — the week is considered
  already told. The phone's current save must never wake up with the reef
  locked. Only a genuinely fresh save starts at Day 1.
- No existing keys are removed or repurposed. The Sky Lagoon's old
  trophies/stars/pearls portal condition remains in code as the free-play
  fast-path; the calendar becomes the narrative-first way in.

## 8. Probe / CI requirements

Day gating touches the whole map, so the probe contract is explicit:

- `probe_audit.gd` must drive the full week: earn each Light through real
  input paths, tap the bed seven times, assert the festival fires, and end
  in free play with everything open. Gating that strands the bot is a FAIL.
- `probe_passive.gd`: zero input must earn zero Lights and never advance
  `story_day` — page-turns are always deliberate taps.
- `probe_load.gd`: `story_day`/`day_lights` round-trip, plus the §7
  migration case (a progressed legacy save loads at day 8, nothing locked).
- Existing probes (`probe_l2`, `probe_train`, `probe_mg2d`,
  `probe_stuffie`, `probe_northern`) keep passing by starting from a save
  state with the relevant day open — day gating must be injectable for
  probes without UI-walking the whole week each time.
- Probe updates land in the same commit as the gating they test, called out
  as the explicit behavior change per the refactor rules.

## 9. Implementation phases (each probe-gated, in order)

- **W0 — this document.** Structure agreed; no code.
- **W1 — calendar + lantern ring, display only.** The storybook calendar
  and ring appear in the Grand Hall reading from the new save keys; morning
  announcement plays on load. No gating — pure additive, zero risk.
- **W2 — the bed and the page-turn.** Day advancement, Light-earned beats
  wired to existing win events, replay from the calendar.
- **W3 — first-open gating for fresh saves.** New-game starts at the
  castle on Day 1; lands open by calendar; legacy saves grandfather to day
  8 (§7). Probe updates are the explicit goal of this commit.
- **W4 — staging and cast.** Day-7 festival dressing on the existing
  finale, Snow Queen character (post §5 approval), per-day host beats,
  recorded voice lines as they arrive.

## 10. Open questions for the owner

1. Snow Queen name (§5) — pick or veto the candidates.
2. Day 5/6 order: opera on Friday ("Friday show night") and karts/Butterfly
   World on Saturday is the proposal — swap freely; nothing depends on it.
3. Should the family phone's existing save also get to *play* the week
   (a "read the story again" button that runs Days 1–7 without locking
   anything), or is day 8 free-play the right landing for it? Default: the
   replay-from-calendar path makes this possible later without a migration.
4. Where the dungeon narratively lives — proposed under the northern castle
   on Snow Day; could instead be a castle-cellar Day 1 tease.

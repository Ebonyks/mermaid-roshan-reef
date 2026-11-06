# Balloon Duel: study notes

What this is: a description, in our own words, of how the 2004 Flash game Balloon Duel plays. It was written so the Mermaid Roshan game can match the *feel* of the original without reusing any of its code, art, sound, text or names.

Nothing from the original SWF is in this repository except these notes. The game code under `src/` was written fresh from this description.

## Source

| Item | Value |
|---|---|
| Title | Balloon Duel |
| Author | John Su ("Mousekliks") |
| Released | June 24, 2004, Newgrounds portal 177120 |
| SWF | `https://uploads.ungrounded.net/177000/177120_Balloon_Duel.swf` (819,905 bytes, SHA-256 `e6cae626...ba470`) |
| Format | Compressed SWF, version 7, ActionScript 2 |
| Stage | 600 x 450 at 30 fps |
| Inspired by | Nintendo's *Balloon Fight* (1984) |

Third-party IP inside the original, all excluded here: Nintendo sound effects (`flap`, `bounce`, `bpop` and others), the overall Balloon Fight concept, and an accessory named after a Studio Ghibli creature. The author's art, characters, dialogue, shop names and UI are his own and are also excluded.

## How we studied it

1. Ran the SWF locally in Ruffle 0.7.1 (the separate `balloon-duel-local` folder, kept outside this repo).
2. Played through registration, the hub, the mode desk and a match against the CPU.
3. Parsed the SWF with our own reader (`balloon-duel-local/study-tools/`) and read the ActionScript bytecode for rules and numbers. Numbers and rules are game mechanics, not expression; we restate them below.

## Game structure

- **Profiles.** Several named fighters per save. Each has cash, rank and a full appearance.
- **Hub.** A taxi with destinations: Arena, Balloons & Accessories shop, HeadWear, Hair Salon, a "gene lab" (eyes, brows, skin), Clothing shop, Practice/Tutorial, plus Data/Options/Quit.
- **Arena desk.** Four modes:
  - vs CPU: pick an opponent by rank (or random). Win to raise rank and earn pay.
  - vs Player: two players on one keyboard.
  - Soldier Training: survive waves of weak drones. Unlocks at rank 100.
  - Balloon Trip: endless side-scroller, collect floating balloons and dodge sparks.
- **Economy.** Start with $200, rank 1. Pay after a CPU match is roughly `9.5 + 0.5 * rank`. Rank changes scale with the rank gap and the lives difference. Hair styling costs a flat amount per section; dye costs extra; no refunds; re-wearing owned items is free.

## Arena rules (the part we copy in feel)

World units below are the arena's own space: **400 wide by 300 tall**, with the water surface around y = 300. The original draws this at 1.5x.

### Movement

- Gravity: +0.25 to vertical velocity every frame. With no balloons: +0.3125 (x1.25).
- Each fighter has `maxX = 6`, `maxY = 5`, `strength = 3`.
- A flap fires once per *press* (not while held). Holding left/right only sets the direction used by the next flap.
- Flap impulse, where `n` is balloons left (0 to 2) and `infl` is balloon inflation (normally 100):
  - `s = strength * (infl + 50) / 150`
  - if `n > 0`: `vy -= s * (n + 6) / 8`
  - always: `vx += s * dir * 0.75 * (n + 2) / 4`
- Drag tier by balloons left: 2 balloons = 1.0, 1 balloon = 1.2, 0 balloons = 2.0. Whenever `|vy| > maxY * drag`, multiply `vy` by 0.9; same for `vx` with `maxX`. So it's a soft speed cap, not a clamp.
- Horizontal wrap: past x = 415, reappear at -15, and the reverse.
- Ceiling at y = 20: snap there, bounce `vy *= -0.8`, `vx *= 0.8`.
- Falling below y = 400 costs a life. Respawn at y = 300 with `vy = -25` (a launch), 2 fresh balloons, inflation reset, and 50 frames of blinking invincibility. No lives left = lose.
- At round start a downward drift of 0.5 per frame is added to everyone and decays by 0.002 per frame to zero.

### Combat

- **Popping:** A's feet touch B's balloons **and** A is at least 10 units higher than B **and** both still have balloons **and** B isn't invincible. B loses a balloon; both bounce.
- **Bumping:** When bodies touch, the two fighters swap x velocity (if more than 6 apart horizontally) and swap y velocity (if more than 6 apart vertically). One bounce per contact.
- **Energy:** each fighter has a 0 to 100 charge that refills by 1 per frame while they have balloons. Accessories spend charge. A "ready" light shows when there's enough.
- Balloons visibly sway with horizontal speed.

### Hazard

A big fish patrols below the water line on a slow back-and-forth (`x = 200 + 250 * cos(t / 40)`). When a fighter dips below y = 240 the fish rises toward the surface; if a low fighter is just ahead of its mouth it lunges and swallows them (unless they're invincible), which costs a life.

### Stage variants

Same arena, different balloon behavior:

- Normal.
- Balloons slowly inflate up to 125 (stronger flaps).
- Balloons slowly deflate down to 50 (weaker flaps).
- Inflation changes with height (the lower you are, the more they swell).

### CPU opponent

Every few frames (chance based on a "reflex" stat) the CPU decides. Inputs: wrapped horizontal distance to the player, relative height, a 10-frame history of the player's motion (to estimate velocity), and a short-term prediction of whether the player's path will cross its balloons.

Priority order, each gated by a skill-scaled random roll:

1. If the player is very high, chase from above if possible, otherwise evade.
2. If the fish is near and I'm low, rise.
3. If I'm dangerously low, evade upward.
4. If the player's predicted path hits my balloons, evade.
5. If I'm below the player, or very close, evade (get above).
6. Otherwise chase: flap toward the player, but stop accelerating near max speed, and only when I'm above them.

Skill ranges roughly 20 to 120. Higher-rank CPUs also get higher `maxX` and `maxY` (`2 + 0.04 * level` and `2 + 0.03 * level`).

### Accessories (one equipped "pack")

Ten exist. By function: auto-flap; anti-gravity (strength from charge); horizontal jet; a gun that fires poppers; a short-range heater that makes balloons easier to pop; reverse-gravity pull toward you; a pulse that drains both batteries (the opponent's more); a binding summon that freezes the opponent. Plus balloon cosmetics. We replace all of these with original Reef of Light items (see the design doc).

### Balloon Trip

The screen scrolls sideways. Floating balloons spawn for points; sparks fly in horizontal lines at random heights; touching a spark loses. Speed steps up over time with short pauses between sections.

## What we carry over vs. change

| Keep (mechanics) | Change (everything expressive) |
|---|---|
| Flap physics and its numbers | All characters, art, UI, fonts |
| Pop-from-above rule, bump swap | All names, dialogue, shop concepts |
| Lives, respawn launch, invincibility | All sound and music |
| Bottom hazard that lunges | Hazard is an original anglerfish |
| Energy meter + one accessory slot | Accessories are original sea charms |
| CPU priority logic (concept) | AI code written fresh, tuned gentler for kids |
| Stage inflation variants | Variants recast as reef places |
| Endless scroller bonus mode | Recast as a current ride |

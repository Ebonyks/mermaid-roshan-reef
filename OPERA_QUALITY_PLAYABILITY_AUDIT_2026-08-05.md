# OPERA_QUALITY_PLAYABILITY_AUDIT
**Pearl Opera career minigames — 13 acts, branch codex/opera-art-regeneration (worktree C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration)**
**Audited 2026-08-04/05, for the owner. Written for the question that matters: is this good for her, right now?**

**Evidence base and honesty note.** Four auditors reported (fun/uniqueness, balance, theming, capture); the dedicated graphics auditor's report never arrived, and the capture run crashed partway (a probe-harness bug, "trying to cast a freed object" at scripts/probe_opera_2d.gd:151 via _capture_viewport:380 — the game itself logged 98 contract checks, ALL OK, zero FAIL). What DID land: all 20 chef widget frames, chef's rival pair, chef + detective scuffle sequences (21 frames), and 1 stress frame. As synthesis editor I read the decisive PNGs myself, so every graphics claim below about chef/detective is pixel-verified; the other 11 careers' widget graphics are graded provisionally from asset/code reading and marked (est). Where an auditor's opinion conflicted with a read PNG, the PNG won.

---

## 1. SCOREBOARD

Scale 1–5. Columns: Unique / Graphics / Fun / Balance / Theming. Graphics marked (est) = not pixel-verified (capture run incomplete).

| # | Career | Unq | Gfx | Fun | Bal | Thm | One line |
|---|--------|-----|-----|-----|-----|-----|----------|
| 1 | Chef | 4 | **2** | 5 | 4 | 2 | Best new beat in the game (the oven) trapped inside the two worst widget cards in the game |
| 2 | Detective | 5 | 4 | 4 | 4 | **2** | Bravest structure of the 13 — undermined by the "missing" crown being painted in plain sight, and a bop-bop-bop ending |
| 3 | Ballerina | **1** | 4 (est) | 3 | 3 | 4 | Every beat is a shared template with different art; nothing she could name tomorrow |
| 4 | Candymaker | 2 | 3 (est) | 3.5 | 3 | 3 | Chef minus the oven; SHARE's waving friends is the one warm spark |
| 5 | Doctor | 3 | 4 (est) | 4 | 4 | 4 | The X-ray recontext works and the care-fantasy carries the generics; smeary circle+swipe finale |
| 6 | Farmer | 3 | 3 (est) | 4 | 5 | 3 | The rhythm gold standard (zero verb repeats) with the game's one abstract UI bar stuck in the middle |
| 7 | Boxer | 2 | 4 (est) | 3 | 3 | 4 | Three of the first four beats are the identical bop; the belt-tap coronation almost saves it |
| 8 | Magician | 4 | 4 (est) | 4.5 | 4 | 4 | The gliding shuffle is genuinely clever; two trace-swipes flank the chase |
| 9 | Painter | 3 | 4 (est) | 4 | 4 | 5 | No bespoke mechanic but the best fiction-mechanic fit of the generics — splats that STAY |
| 10 | Astronaut | 5 | 2 (est) | 4 | **1** | 3 | The biggest bespoke system in the rebuild is **unplayable by tapping** (P0 bug) and rendered in vector fallback |
| 11 | Racer | 5 | 4 (est) | 5 | 4 | 3 | The one beat where the world transforms — the 3D lap carries the act, and it can |
| 12 | Popstar | 4 | 3 (est) | 4 | 2 | 3 | Echo Song is lovely and self-paced — and corner-mashing beats it (economy leak) |
| 13 | Nursery | 5 | 4 (est) | 5 | 5 | 3 | Co-op baby care, cradle catch, the only beat that teaches restraint — peak 4-year-old |

**Best act: NURSERY.** 5/5 on uniqueness and fun, the cleanest economy of the 13, co-op with no rival contest, and mechanics (cradle catch, paced burping) tuned exactly to the target child. **Runner-up / biggest single wow: RACER** — the 2D painting giving way to a real 3D lap is the moment she will talk about.

**Weakest act: BALLERINA.** The only career scoring 1 on uniqueness: three shared-template beats, five phases, done. It is the one act with no answer to "why this one tomorrow?" **Most urgent act: ASTRONAUT** — not weak by design (uniqueness 5) but currently broken for a tap-first child (see Balance A1).

---

## 2. GRAPHICS INTEGRITY

The owner's bar: full graphics, no cutoffs anywhere. Verified against read PNGs where captures exist.

### SEVERE (fails the bar outright — pixel-confirmed)

**G1. Chef BAKE (oven gauge card) — the worst frame in the captured set.** chef_04_gauge_active_input.png: the painted oven sprite is **cut off mid-body at the left card edge** (roughly half the sprite renders, the rest is off-card); the center of the card is the old flat navy vector gauge fan **with the green wedge the code's own comment bans** ("NO green anywhere"); code-drawn brown window/handle/thermometer rectangles are collaged over it. This is the flagship new mechanic of the flagship first career, and it looks like clip-art pasted on a painting. The ledgered oven-face card never landed.

**G2. Chef POUR card.** chef_02_pour_active_input.png: the "pitcher" mover is a **duplicate bowl-with-whisk** hovering and tipping over the main bowl (voice says "Grab the pitcher and TIP it"); a stray **brown fallback outline rectangle is drawn straight across the painted bowl**; the pink fill-pill clips over the bowl's shell emblem. Three defects on one card. Candymaker SYRUP shares the mover problem (a smiling candy bow with un-cropped mold fragments baked into the sprite, standing in for a "syrup bottle") — not pixel-verified but confirmed in the asset file.

**G3. Astronaut pipe tray overflow (runtime-verified).** Because every tile lift duplicates a tile (bug A1 below), the tray grows without bound and **slot 8+ draws past the 852px card edge**. A child who taps a lot will watch tiles march off the card.

### MODERATE

**G4. Chef PIPE (trace card).** chef_06_trace_active_input.png: the trace path is a thick flat navy zigzag polyline drawn OVER the painted card, and the piping-bag art is not registered to it — the bag floats above the line, the frosting swirl sits below it, and the path crosses the bag sprite. Functional, but it reads as UI-on-top-of-art rather than one picture.

**G5. Player occlusion in scuffles.** chef_opening_03 and the stress frame: the imp cluster can stand directly in front of Roshan, **fully hiding her face and body** behind an enemy sprite. She should never lose sight of her own character mid-fight.

**G6. Ghost prop silhouettes in the career world.** chef_opening_02/03: faint translucent duplicates of props/characters are visible over the cauldron area and near the right-side stations. If these are intended station-hint ghosts they are too close to the "ghosting" failure mode this project has been burned by before; needs an owner look on-device.

**G7. Empty VO oval.** Every widget frame carries a blank yellow ellipse at the card's top center (the voice bubble with nothing in it). At minimum it should hold an icon; as shipped it reads as an unfinished element on all 20 captured frames.

**G8. Both new marquee mechanics have NO authored art.** Astronaut PIPES (tank/intake/tiles) and Popstar RHYTHM (star notes lit/unlit) load textures that do not exist in assets/opera/worlds/widgets/ — both render entirely as code-drawn vector fallbacks over lush painted worlds. (Ledgered as P1/P2 in code comments; still true at audit time.)

### MINOR
- Actor style split: roshan_racer.png and faron_nursery.png are markedly more anime-detailed than the chibi imp sheets — beautiful, but not one line language.
- Farmer FEED card is half painted (leaping piggy), half flat navy/green timing bar.
- Nursery WASH basin card has no basin and no water (a swaddled baby over an arc); the doctor's basin card shows exactly how it should read.
- Nursery backdrop's flat-teal bleed tiles are overscan only — coherent in view.

### What is confirmed GOOD (pixel-verified)
The chef stage and career-world frames are **superb**: proscenium, footlights, plush-animal audience, painted cake podium, coral-pearl city backdrop; the costumed rival imp reads instantly as "chef imp" (horns and tail through the toque); Roshan's chef outfit with the rainbow hair is lovely; the STIR crank card (painted bowl + whisk mover + soft ring guide) and the free-tap target card are exactly the standard the whole widget set should meet. 98/98 layout/contract checks passed with zero FAILs.

### Coverage gap — be aware
Widgets for 11 of 13 careers, rivals for 12 of 13, scuffles for 11 of 13, and 5 of 6 stress frames were **never captured** (probe crash, harness bug, not a game failure). Fix the probe (freed-object cast at probe_opera_2d.gd:151) and re-run before calling the graphics bar met anywhere but chef.

---

## 3. FUN & UNIQUENESS

**Verb census:** circle ×9 careers, swipe ×9, choice ×8, hold ×8, free-tap ×7 — versus six careers that own a beat existing nowhere else (chef's oven, detective's talk/lens hunt, astronaut's pipes, racer's kart, popstar's echo, nursery's catch+paced-burp; farmer owns the only timing beat and best hold-release). **Four careers own nothing bespoke: ballerina, candymaker, boxer, painter** (painter earns its keep anyway through fiction-mechanic fit).

**What genuinely lands** (the moments she will remember):
- Chef: yanking the mitt out of the oven inside the golden band — with the no-fail floor ("toasty is a KIND of cake").
- Racer: the whole 2D painting turning into a 3D rainbow track she drives. Every finishing place wins.
- Nursery: sliding the cradle under a falling baby; pillows make misses safe.
- Magician: the answer visibly gliding between lanes and failing to trick her.
- Popstar: singing a verse back at her own toddler tempo and hearing the song assemble.
- Astronaut: fuel gushing through a completed pipe path into the ringing rocket (once the tap bug is fixed).
- Painter: five splats exactly where her finger landed, and they STAY.
- Detective: the captain wearing the stolen crown AS A HAT; the mid-act footprint ambush.
- Tilt-pour (chef/candymaker): pouring is THE preschool verb, and the stream follows her finger, not a clock.

**Which careers blur together:**
1. **Ballerina ↔ Popstar-minus-echo** — identical performance spine (choice-dance + circle-flourish). Echo saves popstar; nothing saves ballerina.
2. **Candymaker ↔ Chef** — same pour+circle+tap spine; the oven separates chef, nothing separates candymaker.
3. **Boxer's JAB ↔ any imp scuffle anywhere** — literally the same beat with a "training pads" voice line over it.

**Flattest moments:** farmer FEED's abstract moving-marker bar (the only beat requiring a 4-year-old to read a UI contract); boxer's bop-bop-swipe-bop opening; detective's double-combat ending (CROWN CHASE straight into TEAM CORNER, then the finale is a third combat); doctor's circle-then-swipe smear finale; astronaut pipe round 3 (6-tile tray, two nappers, hint marks the cell but never the tray tile — the game's only near-stuck state); nine careers contain a circle beat and four finales end on one — played on consecutive days, "draw circles for the crowd" is the sameness she will actually feel.

**What the structure gets right:** the five-beat arc breathes. The wander layer is a real breath (the world stays hers between stations, the 2.2s completion hold lets her SEE what she made), and seven careers run zero or near-zero verb repeats — farmer (bop→choice→timing→hold→chase→push→tap) is the gold standard.

---

## 4. BALANCE

### Measured times (headless probe, speedy/casual/dreamy personas, sim-seconds; target ≈ 2 min real incl. ~15–20s entry/curtain overhead)

| Career | speedy | casual | dreamy | verdict |
|---|---|---|---|---|
| chef | 72.5 (fixed harness) | — | — | in band; the original "300s capped" row was a **harness artifact** (probe never ticked the surface, so the oven never heated) |
| detective | 38.6 | 69.8 | 88.7 | in band (understated — talk timers pumped) |
| ballerina | 31.2 | 54.6 | 77.1 | thin — only 5 phases |
| candymaker | 40.3 | 69.3 | 91.0 | in band |
| doctor | 42.1 | 64.3 | 94.4 | in band |
| farmer | 46.5 | 71.5 | 104.7 | longest; lands AT ~2 min real, not over |
| boxer | 30.0 | 44.6 | 68.9 | thinnest act (6 phases, 4 bop/tap) |
| magician | 40.6 | 65.0 | 92.9 | in band |
| painter | 37.1 | 60.9 | 81.2 | in band |
| astronaut | 35.3 | 57.2 | 77.1 | understated — pipe puzzle pumped, real ~30–90s more |
| racer | 22.6 | 39.0 | 56.8 | artifact-low — kart lap counted as one tap |
| popstar | 40.2 | 61.2 | 87.9 | understated — echo verses pumped |
| nursery | 48.2 | 65.9 | 77.3 | in band, tightest spread |

**Verdict vs the 2-minute target:** no career genuinely runs long; median spread 1.83× (racer 39.0 → farmer 71.5) is fair; boxer and ballerina are the two acts that could take one more beat. Caveat: the probe pumps the five NEW mechanics (pipes, echo, pour, talk, kart) as generic taps and bypasses the on-device swipe budget, so all "brisk" verdicts are floors — real-play medians land comfortably in band.

### Economy findings (runtime-verified with dedicated probes, not opinions)

**[P0 — A1] Astronaut PIPES is broken for tap-first play and duplicates tray tiles.** Tapping a tray tile lifts it, but the tap's own release immediately appends a DUPLICATE back to the tray and clears the selection; the follow-up tap places nothing. **729 simulated taps → zero placements, zero progress.** Drag works but also never removes the tile from the tray. The one career mode that cannot be played by tapping, in a game whose whole grammar is one-finger taps — and the tray visibly grows past the card edge. File: scripts/opera_gesture_surface.gd, press-on-tray branch (~1205–1212) never remove_at's; _pipe_release (~1252–1255) re-appends and kills the selection; the tap-place branch (~1231–1238) is unreachable.

**[P1 — A2] The maxf(0.04, amount) trickle floor lets mashing beat honest play in Echo Song.** scripts/opera_career_world_2d.gd:1321 pays every stray tap 0.04 progress in non-continuous modes. Verified worst case: mashing an empty corner completes popstar's RHYTHM in 30.1s/76 taps **without ever touching a correct star**, roughly tying honest play — and each junk tap also earns +10 applause (quality 0.6 ≥ 0.5), so a masher out-scores an honest child ~5× against the rival. Milder leaks: oven-peek mash completes BAKE with the cake never removed; pipe imp-taps and nursery BURP's gated fast pats all get paid 0.04 the pace-gate meant to zero.

**[P1 — A3] Goal desync:** PIPES (goal 3.0 = 3 rounds) and RHYTHM (3.0 = 3 verses) assume only 1.0-payments; crumb payments mean a fumbling child "completes" mid-song / mid-puzzle with the board unsolved. Gate on echo_verse ≥ 3 / pipe_round ≥ 3 instead.

**[P2 — A4] Pour goals inconsistent:** chef POUR goal exactly equals the full-brim payout (zero slack, fragile to any retune); candymaker SYRUP completes at ~90% fill, before the brim ding — the phase ends with the bowl visibly unfull. Otherwise pour has the cleanest economy of the new modes (mash pays zero, waiting is child-paced).

**[P2 — A5] Frozen frames while waiting:** echo's LISTENING state is a static card for 3–9s (no pulse; the idle-rescue ghost finger has no "echo" case so it points at dead center, not the next star). Oven, pipe, catch, talk, and wander all pass the 3-second liveliness test.

**What's sound:** miss cooldowns, the BURP pace gate, and the swipe budget (1.3/s refill, 34px/event cap — honest against scrubbing) are all correctly designed. Correct play strictly beats mashing in oven (6s vs 50s), pour, BURP, and bop; it ties/loses only in echo — that is the one genuine economy violation.

---

## 5. THEMING

Overall strong: the five-beat arc reads in every career, the gesture IS the action in ~34 of ~38 non-combat beats, widget cards are per-career painted objects, every costumed rival unmistakably reads as this career's imp, and **no fully generic voice lines were found** — every career's lines talk their own trade.

**P1 breaks:**
1. **Detective: the "missing" crown is painted in plain sight.** The whole 10-beat fiction is "the crown is GONE" — yet both the backdrop and the runtime tile kit paint the pearl tiara sitting in its open chest on the right-side dais, visible the entire hunt. The code even special-cases hiding the goal prop for exactly this reason; the art defeats it. Needs a region repaint (empty chest / bare cushion). Evidence crops saved (detective_chest_zoom.png, detective_runtime_chest.png).
2. **Chef POUR / Candymaker SYRUP: voice promises a pitcher/bottle, screen shows a bowl/candy-bow** (see G2). Art-vs-fiction break, pixel-confirmed.
3. **Chef BAKE: the promised oven face never landed** (see G1) — the flat gauge fan directly contradicts the fiction AND the code's own art notes.

**P2 flags:**
- Both new marquee mechanics (pipes, echo stars) are vector fallbacks in painted worlds (G8).
- Nursery WASH card has no basin/water; BURP — the flagship self-paced beat — has no card art at all: the child pats colored dots, not a baby's back.
- **Underwater rule inconsistency:** 11 of 13 backdrops are submerged pearl-city; farmer is above-water pastoral (sky, barn, apple trees) and doctor is an above-water garden campus. Shell/pearl motifs and the stage-door arch carry through, so "painted set of a land place" may be intended — but it needs a deliberate owner call, not drift.
- Racer TUNE UP: voice says "turn the wrench," art shows a kart driving a curved track section. Fix either.
- Farmer MUD HOP: hold-to-fill-meter maps to no farm verb; FEED's timing bar is rhythm-game grammar on a farm.
- Painter FILL: "Hold to fill the glowing shape!" — the only line in the table with no trade noun.
- The painted plush-animal audience (charming, pixel-confirmed) contradicts the "no audience" note, and the class header still advertises "audience energy and a graded curtain call" — stale doc either way.

---

## 6. RANKED IMPROVEMENTS

Ranked by impact-on-the-child ÷ effort. Severity of evidence noted where it drove the ranking.

### THE NEXT BUILD (top 5)

**1. [code] Fix the astronaut pipe tray (A1).** Small diff (remove_at on lift, re-add on failed drop, keep selection alive across release), unblocks the game's biggest bespoke system for tap-first play, and kills the tray-overflow graphics defect (G3) in the same stroke. Runtime-verified P0; highest impact/effort ratio in the audit.

**2. [code] Close the 0.04 economy floor and gate PIPES/RHYTHM on done-states (A2+A3).** Floor only quality ≥ 0.9 actions (or route crumbs through _miss_pay, which already does cooldowns right). Restores "correct play strictly beats mashing" — the invisible contract that makes every beat teachable — and stops acts advancing mid-song/mid-puzzle. Small diff.

**3. [art] Chef widget rescue: the authored oven-face card + a real pitcher mover (+ [code] suppress the fallback outline when authored art is present).** Fixes the two SEVERE pixel-confirmed defects (G1, G2) in the FIRST career every player meets — the current cards are the single worst thing a parent will see in an otherwise gorgeous game. Do the candymaker syrup-bottle mover in the same art pass.

**4. [art] Repaint the detective crown region (empty chest / bare cushion)** in both the backdrop and the runtime tile kit. One region repaint restores the entire 10-beat mystery fiction — the best story structure in the game currently contradicts itself on screen every second.

**5. [design][code] Give ballerina a bespoke beat.** The score-1 outlier. Cheapest fit in the house language: a leap/glide using the existing hold-release payoff (farmer's MUD HOP machinery) — a body in motion, which is what a ballerina act is missing.

### The rest, in order

6. [code] Pipe round 3: make the twinkle hint also glow the matching TRAY tile — closes the game's only near-stuck state (small diff).
7. [design][code] Differentiate boxer's JAB: real pad targets with positions/order (even the existing choice lanes reskinned as held pads breaks the triple-bop).
8. [design][code] Replace detective's TEAM CORNER verb — a lens-assisted trap or talk-then-single-tap capture; anything but a third consecutive bop.
9. [art] Authored art for pipes (tank/intake/tiles) and echo stars (lit/unlit) — the two marquee mechanics deserve better than vector fallback (G8).
10. [code] Echo liveliness: pulse the LISTENING state, add the "echo" case to the demo-finger so the idle rescue points at the next star (A5).
11. [code] Pour goal consistency: SYRUP 4.5 → 5.0 with the brim ding as completion (or both goals deliberately under-brim) (A4).
12. [art] Nursery care-beat art: a real bubbly basin, and a card for BURP (a baby's back to pat, not colored dots) — the flagship act deserves its flagship beat drawn.
13. [design][art][code] Diegetize farmer FEED: the pig's opening mouth IS the timing window — removes the last abstract UI element in an otherwise diegetic game.
14. [code] Rebalance-probe fixes: tick surface._process (B1), simulate the five new modes for real instead of pumping (B2), route swipes through the surface budget (B3) — then re-run; expect all 13 in the 55–110s sim band.
15. [code] Fix the capture-probe crash (freed-object cast, probe_opera_2d.gd:151) and re-run the full capture so the remaining 11 careers' graphics can actually be verified against the owner's bar.
16. [code] Widget layering: keep Roshan in front of (or ghosted through) imp clusters during scuffles (G5); check the translucent station-prop ghosts on-device (G6).
17. [design] Candymaker anchor beat — molds or taffy-stretching built from the existing pour/trace machinery, to break the chef shadow.
18. [code] Put magician's CABINET in the push-template list (currently a second trace flanking the chase); consider re-ordering doctor's CAST/BANDAGE finale so it isn't two smear verbs back to back.
19. [audio][art] Racer TUNE UP: align voice and art (wrench mover, or a "warm-up lap" line); give painter FILL a trade noun.
20. [design] Owner call: are farmer's and doctor's above-water backdrops intentional "painted sets of land places," or should they be repainted submerged? 2 of 13 currently break a rule the other 11 obey.
21. [art] Fill or icon the empty VO oval on widget cards (G7); longer-term, converge the racer/nursery anime actors and chibi imps toward one line language.
22. [code] Housekeeping: delete the stale "audience energy / graded curtain call" header comment; prune the unused widget shelf stock (detective trace/track/lanes, astronaut/racer gauges) before the next ledger pass confuses itself.

---

**Bottom line for the owner:** the rebuild's bones are excellent — six genuinely ownable careers, a five-beat arc that breathes, worlds and character art that are pixel-confirmed gorgeous, and kindness floors everywhere. What stands between this and "ship it to her" is small and concrete: one P0 code bug (pipes), one economy floor (echo), two broken widget cards in the very first career, one painted crown that shouldn't be there, and one career (ballerina) that hasn't earned its slot yet. Items 1–5 are roughly one code day and one focused art pass. After that, re-run the fixed capture probe across all 13 careers before declaring the no-cutoffs bar met — chef is the only career where that bar has actually been checked against pixels, and chef failed it in two places.
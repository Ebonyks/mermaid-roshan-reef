# Opera minigame widget audit - input integrity and 4-year-old patterns (2026-08-02)

Owner brief: the minigames are the weakest section - artwork below the
game's caliber, and touch input imprecise or misaligned with instructions
(mashing beats waiting for the green). Three-lens audit: input-math
forensics, preschool interaction critique, and the widget-art-vs-fiction
gap. The proven scoring-integrity defects are FIXED in this pass; pattern
replacements and art are specified but not yet built.

## 1. What was broken (forensics, verified with numbers) and its fix status

| # | Defect | Numbers | Status |
|---|--------|---------|--------|
| D1 | timing: misses paid 0.32 at unlimited rate | mash 2.1/s vs 0.75-0.90/s perfect play - mashing beat PERFECT play 2.4x | FIXED: miss pays 0.05 once per 1.0 s cooldown, then zero; green pays 1.0 |
| D2 | timing: 0.33-0.40 s green window = a precision gate (house law: never precision) | 4yo reaction is 600-900 ms | IMPROVED: window widened to 42% of bar, marker slowed (~0.76 s open per ~1.8 s pass); full dwell-cue replacement specified below |
| D3 | tap: miss-anywhere paid 0.3 unlimited | blind mash 1.2-2.0/s vs 0.83/s aimed | FIXED: 0.05 once per 0.5 s, then zero |
| D4 | choice: wrong lane paid 0.24 unlimited | random mash 1.97/s vs 0.5-0.67/s deliberate | FIXED: 0.05 once per 0.6 s, then zero |
| D5 | choice: answer re-flashed on CORRECT picks - memory game defeated itself | n/a | FIXED: mercy re-flash on wrong picks only |
| D6 | hold: 0.04/frame floor made holds frame-rate-dependent (2.4x-4.8x intended speed) + 600 score/s pump | goal "5 seconds" completed in ~2.1 s | FIXED: continuous modes bypass the floor (real seconds); applause capped 2/s |
| D7 | swipe: direction never checked (DUCK's down-arrow was a lie); any wiggle paid q1.0 | - | FIXED: declared-direction phases gate on alignment (wrong direction = kind fizzle) |
| D8 | swipe: no rate cap - scrubbing paid 8-10/s, goals gone in ~1 s | goal 9 in ~1 s | FIXED: per-event travel cap + 1.3/s refill budget |
| D9 | circle: straight-line scrubs through center paid ~0.5/crossing | scrub 2-6x honest circling | FIXED: only direction-consistent small angular steps count |
| D10 | lens: the ghost DEMO lens self-collected clues near its drift turning points | zero-input progress | FIXED: demo never collects |
| D11 | bop stray taps: 0.12 unlimited trickle | 0.48/s - honest play already won; hygiene fix | FIXED: 0.05 once per 0.45 s |

Design principle adopted (house precedent: fetch's press cooldown +
widening safe zone, melody's verb gating, dolls/catch's mercy
escalation): **trickle-by-assist, not trickle-by-payout** - wrong input
always celebrates (fizz, giggle, bounce) but pays ~nothing, while mercy
makes the RIGHT verb easier over time. No-dead-ends is preserved: the
0.04 floor remains on discrete gestures, first-misses still trickle, and
every phase remains completable by any child.

Validation after fixes: probe_opera_2d 287 checks green, nursery 19
green, balance sim in band (sim cadences were already honest, so pacing
holds; real-world mash runs simply stop finishing phases in seconds).

## 2. Are these the most effective patterns for a 4-year-old? (critique)

Mode ranking, best to worst, with prescriptions (art dependencies in P8):

| Rank | Mode | Verdict | Core reason |
|---|---|---|---|
| 1 | lens | KEEP | direct manipulation, masked reveal, self-paced, mash-proof - the best pattern in the project |
| 2 | bop | KEEP | world-level, big slow targets, tap OR sweep, physical comedy, captain reserve |
| 3 | catch | KEEP | the proven dolls grammar: verb gate, mercy lanes, pillow-safe misses |
| 4 | swipe | RESKIN | the best motor verb at 4 - but draws no response; needs visible cause-effect (frosting appears, ribbon trails, blanket moves) |
| 5 | hold | RESKIN | motorically right; needs a continuously filling world (batter rises, bottle drains) instead of a growing dot |
| 6 | tap | RESKIN | pattern fine, target abstract; make tap_marks the fiction (toppings stay on the cake) |
| 7 | circle | RESKIN | hard under 5 but salvageable - something must visibly ROTATE with the finger |
| 8 | choice | REPLACE | Drag-and-drop with always-visible pictured targets (recognition, not recall; structurally unmashable). Rhythm-fiction phases (STEPS/ROUND/DANCE) instead keep tap-while-lit with no dim timer. |
| 9 | timing | REPLACE | Watch-then-act on a big slow diegetic cue (>=2.5 s cycle, >=1.2 s open window, grows+glows+chimes; fetch pattern); the D2 parameter fix is an interim step only. |

Per-phase REPLACE mappings for both grammars and the full RESKIN
prescriptions are in Appendix B; the P8 art handoff encodes the same
per-phase fictions, so art and grammar land together.

## 3. Artwork: why the widgets feel below caliber, and the handoff

The voice lines promise diegesis ("Tap when the oven marker is green!",
"Hold the sparkling syrup bottle!") while the widget draws abstract
rings, lanes and a literal progress bar on a paper card. The nursery's
four drawn contexts (basin/bottle/cribs/blanket) prove the fix pattern
in shipping code. **PRIORITY 8** in
OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md is the complete codex
handoff: 60 phases grouped into 11 templates (gauge, track, pour, basin,
charge, crank, trace, push, target, lanes, catch), per-career skins with
exact filenames, 1024x608 backdrop + 256x256 mover/overlay layer splits,
engine-registration geometry (lane centers, timing-run pixels, green-zone
bake), the green-is-reserved rule (success-green appears ONLY in go
zones - the visual answer to "wait for it"), content locks, and the
engine work items that place every file (extending the proven
visual_context plumbing to template_career keys).

## 4. Recommended build order

1. DONE this pass: the D1-D11 integrity fixes.
2. P8 SET A art (T2 track + T10 lanes skins) + the two REPLACE grammars
   (dwell-cue timing, drag-and-drop choice) - the two worst modes get
   their new patterns and their art together.
3. P8 remaining templates as RESKIN feedback (fill/trace/crank/target
   responses) - each is art + a small draw-callback change.
4. Re-run the balance probe and hand-tune goals (holds now cost real
   seconds; swipes capped - expect +5-15 s per act, still in band).

---

## Appendix A - input-math forensics (full report)

# Opera Gesture Math — Forensic Audit (worktree codex-opera-art-regeneration)

Files audited:
- C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/scripts/opera_gesture_surface.gd
- C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/scripts/opera_career_world_2d.gd
- C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/scripts/opera_nursery_catch.gd
- C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/scripts/opera_competition.gd (scoring side, read to quantify double rewards)

## Assumptions (stated so the numbers are reproducible)
- 4yo sustained mash: 3-5 taps/s one-handed (bursts 6-8 two-handed drumming). Scrub/drag: 800-1500 px/s finger speed, drag events at touch sample rate ~60-120/s.
- Correct-play cadences: tap-aim ~1.2s/hit, choice ~1.5-2s/pick, timing green ~1 per pass at best, circle ~1.2s/revolution.
- Pipeline: every gesture event -> `_on_gesture` (opera_career_world_2d.gd:864). `gain = maxf(0.04, amount)` (line 882), `phase_progress += gain`, phase ends at `goal`. quality >= 0.5 -> `note_success(10)`; quality < 0.5 -> `note_miss()`. **There is NO cooldown, rate limit, or debounce anywhere in any press path.** Max wrong-action rate = raw input event rate. Additionally, `competition.active` is false until the finale (`begin()` at FINALE_START), so on ALL pre-finale phases `note_miss()` is a literal no-op — pre-finale mashing has zero cost of any kind.

## Master table: honest progress-per-second

| Mode | Correct action pays | Wrong action pays | Wrong-rate cap | Correct play (child) | Mindless mash | Verdict |
|---|---|---|---|---|---|---|
| tap | 1.0 (within 92px, surface:129-135) | 0.3, q0.4 | none | 0.83/s (1.2s cadence) | **1.2/s @4 taps/s floor; blind-center EV ~0.44-0.51/tap (point periodically lands under finger) -> ~1.8-2.0/s** | MASH WINS 1.4-2.4x |
| choice | 1.0 (surface:137-138) | 0.24, q0.0 | none | 0.5-0.67/s | **random-position mash EV = 1/3(1.0)+2/3(0.24) = 0.493/tap -> 1.97/s @4/s; even worst-case one-lane mash 0.96/s** | MASH WINS 1.4-3x |
| timing | 1.0 in green (surface:139-141) | 0.32, q0.32 | none | perfect = marker speed s = 0.75-0.90/s; realistic child ~0.3-0.5/s | **EV/tap = 0.3(1.0)+0.7(0.32) = 0.524 -> 2.1/s @4/s. Break-even vs PERFECT play: 1.43-1.72 taps/s** | MASH WINS 2.4x vs perfect, ~5x vs realistic — owner's report CONFIRMED (miss 0.32 verified at surface:140) |
| hold | delta/frame, q1.0 (world:1194-1195) but **floored to 0.04/frame** (world:882) | tap = 0.06, q0.6 (surface:146) | n/a | authored intent 1.0/s (goal = seconds) | **actual 2.4/s @60fps, 4.8/s @120fps, 1.2/s @30fps — frame-rate dependent; goal 5.0 "seconds" completes in 2.08s** | BROKEN MATH (floor bug) |
| swipe | distance/150 per drag event, q always 1.0 (surface:181-182) | none exists; bare press = 0.05, q0.6 | n/a | deliberate tracing 500-700px/s -> 3.3-4.7/s | scrub 1200-1500px/s -> **8-10/s; goal 9 in ~1s** | NO CORRECTNESS AT ALL; goals trivialized |
| circle | angle-change/TAU per event, q1.0, absf (surface:183-191) | none exists | n/a | 0.83/s (1 rev/1.2s) | **straight-line scrub through center: ~pi jump/crossing = 0.5/crossing -> 2/s @4 strokes/s; edge jitter up to ~5/s** | MASH WINS 2.4-6x |
| bop | 1.0/imp hit; reach 73px imp / 93px captain; drag sweeps hit, per-stroke re-hit guard (world:768-796) | stray tap 0.12, q0.2; drags never fizzle | none | ~0.8-1.0/s | 0.12 x 4/s = **0.48/s — honest wins**; captain reserve (world:893-899) blocks mash-past (needs 6 imps popped to spawn captain + his 2 reserved bops) | HEALTHY — the only tap mode where correct play dominates |
| lens | 1.0 per clue (0.45s dwell in 96px, world:1136-1149) | zero trickle (only mode with none) | n/a | ~0.5/s (goal 3: ~6s) | no mash vector, BUT **the ghost demo self-collects**: the found/dwell check runs while `lens_demo` is true (world:1128-1149) — zero-input progress near the drift path's turning points | IDLE-PROGRESS BUG |
| catch | +1 progress, note_success(18) (world:943-958) | miss = 0 progress + mercy (wider catch +0.013/miss, slower falls -0.011/miss, homing spawns after 2 misses, catch:117-134,178) | n/a | 5 catches in ~20-30s | no mash vector (extra taps only steer). **Park-and-hold passively completes**: center lane auto-catches, 2 edge misses trigger homing spawns -> rest auto-catch | HEALTHIEST ENGINE; mild passive-completion note |

## Defect table

| # | Mode | Severity | Defect (exact numbers) | Where |
|---|---|---|---|---|
| D1 | timing | **exploit** | Miss pays 0.32 at unlimited rate. Perfect play = s/s (0.75-0.90); mash EV 0.524/tap beats perfect at just 1.5 taps/s; @4/s mash = 2.1/s = 2.4x perfect, ~5x a real 4yo. Goal 6: mash 2.9s vs realistic 15-18s. | surface:139-141, world:1188-1190 |
| D2 | timing | **precision** | Green = 30% of bar = 89px of 298px; window 0.333-0.400s (s=0.90..0.75), pass every 1.11-1.33s. 4yo reaction time is 600-900ms — reaction is impossible, only rhythm anticipation works. This is the suite's lone precision gate and violates the house law (difficulty via speed/quantity, never precision). It is also WHY mashing feels rational. | surface:17, world:1188 |
| D3 | tap | **exploit** | Near-miss 0.3 unlimited-rate; blind mash EV 0.44-0.51/tap (92px radius covers ~29% of the 392x232 surface, relocation pattern periodically lands under a parked finger). Goal 7: correct 8.4s, mash 3.5-3.9s. Break-even 2.8 taps/s. | surface:129-135, 152-157 |
| D4 | choice | **exploit** | Wrong 0.24 unlimited; random mash 1.97/s vs 0.6/s correct. Wrong pick never rotates target, so one-lane mash pays 0.24 forever. Goal 7: mash 3.6s vs 11.7s correct. | surface:137-138 |
| D5 | choice | **mismatch** | The flash-then-dim memory mechanic is defeated: `reflash_choice()` fires on EVERY choice gesture including correct ones (world:891), re-revealing the NEWLY rotated answer gold for 1.2s. The child never needs recognition memory after the first tap — it degenerates to tap-the-highlight. Surface comment (line 37) says re-flash is for wrong picks only. | world:886-891, surface:83-85 |
| D6 | hold | **exploit** (math bug) | `maxf(0.04, amount)` floor swallows per-frame delta (0.0167 @60fps) -> 0.04/frame = 2.4/s. Hold goals authored in seconds finish in goal/2.4 s; frame-rate dependent (1.04s for a 5.0 goal on a 120Hz tablet). Also emits q1.0 per FRAME -> note_success(10)/frame = **600 score/s** during finale holds (astronaut LAUNCH) — the rival's whole-act ceiling is ~720. | world:882, 1194-1195 |
| D7 | swipe | **mismatch** | Direction never checked. Boxer DUCK (`dir: "down"`, world:94) draws a down arrow but ANY scribble in any direction pays q1.0. Same for farmer HERD "back and forth", racer STEER "through the coral gates" (no gates exist in input), nursery BEDTIME down-arrow. Voice/icon promise is not verified anywhere in `_drag`. | surface:178-182 vs surface:40 (visual only) |
| D8 | swipe | **exploit/fairness** | distance/150 per event, no per-second cap: scrubbing = 8-10/s, goal 9 in ~1s; even deliberate play is 3-5/s so goals last 2-3s. Plus q1.0 per drag event -> +10 score per event (~600-1200/s) in finale swipe phases (chef PIPE, doctor BANDAGE, farmer HERD, nursery BEDTIME). | surface:181-182 |
| D9 | circle | **exploit** | `absf(wrapf(...))` counts any angular change; a straight-line scrub through the 30px deadzone produces ~pi jumps = 0.5 progress per crossing -> 2/s+ vs 0.83/s honest circling. Direction (icon shows one rotation) unchecked — mild mismatch. q1.0 per event -> score pump as D8. | surface:183-191 |
| D10 | lens | **fairness** (idle progress) | Demo lens auto-collects: while `lens_demo` is true the drift position feeds the same dwell/found check; drift velocity ~0 at sine turning points (x = 640±420, y = 410±130), so any clue within 96px of a turning region self-collects after 0.45s with zero input. Also lens is the only mode with zero wrong-action trickle (inconsistent with trickle law, though dwell generosity covers it). | world:1128-1149 |
| D11 | catch | fairness (mild) | Park-and-hold completes the phase passively: lane 0.50 auto-catches (catch half-width 0.145 ≈ ±57px), lanes 0.17/0.83 miss twice, then mercy homing (spawn at catcher ±0.035-0.086 < width) auto-catches the rest. This is the intended dolls mercy contract, but note it makes zero steering optimal after two misses. Dead code: `_catch` always emits quality 1.0 so the `note_success(8)` low-quality branch (world:950) can never run. | catch:117-134, 178-186 |
| D12 | all | **fairness** (deterrent failure) | The only mash penalty is `mistakes` -> care_quality (-0.055 each, finale only; pre-finale note_miss is a no-op since competition is paused until FINALE_START). A masher finishes faster, so speed_quality ≈ 1.0 and overall quality = 0.58×1.0 + 0.42×0 = 0.58 -> still tier 2 "BIG CHEERS". Mashing is faster AND barely punished; careful play risks a lower speed_quality. Perverse incentive confirmed end-to-end. | competition:178-181, 242-251; world:874-880 |
| D13 | all success paths | fairness (**double reward**) | Every q>=0.5 event pays BOTH note_success(10) AND phase progress, and that same progress is paid AGAIN by `tick()` (+round(gained×760)) (competition:194-198). Discrete modes: bounded and fine. Continuous modes (hold/swipe/circle) emit success per frame/event, so the +10-per-event leg explodes (see D6/D8). | world:874-883, competition:183-198 |

## Precision windows vs 4yo motor control (audit result)
- Tap 92px radius on a 392x232 surface: generous, GOOD (and exploitable, see D3 — generosity is not the problem, the unlimited trickle is).
- Choice lanes: full-height columns 130.7px wide (392/3) — whole column counts, not just the drawn 54px circle. GOOD (child-favoring).
- Timing green: 89px, 0.333-0.400s window — the ONLY genuine precision gate; FAILS the house law (see D2).
- Bop reach: 73px (118px imp) / 93px (captain), imps drift 46-88px/s, drag sweeps count — GOOD.
- Lens: 0.45s dwell in 96px — GOOD.
- Catch: ±57px growing to ±86px with mercy homing — GOOD.
- Circle deadzone 30px, absf wobble-tolerance — GOOD for wobbly 4yo circles (the same tolerance enables D9).

## Recommended rebalance (each preserves no-dead-ends: misses still trickle, correct play strictly dominates)

Global mechanism (fixes D1/D3/D4 with one patch): add a low-quality refractory to `_on_gesture` — when quality < 0.5, credit the trickle only if >=0.6s since the last credited miss; otherwise still sparkle/sound (nothing feels dead) but amount -> 0. Also generalize the already-proven captain-reserve pattern (world:897-899): low-quality trickle may fill at most `goal - 1.0`; the final point must come from one correct action. Every phase remains finishable by one demo-guided correct action after unlimited kind trickle.

Per defect:
- D1 timing: miss 0.32 -> 0.12 with the 0.6s refractory (mash ceiling 0.2/s) and keep correct at 1.0. Post-fix: perfect 0.75-0.90/s, realistic 0.3-0.5/s, mash 0.2/s — correct strictly dominates at all skill levels.
- D2 timing: honor the house law — widen green to 0.30-0.72 (0.42 of bar, ~125px) and slow the marker to `min(0.70, 0.55 + 0.02*phase_index)` -> window 0.60-0.76s, pass every 1.43-1.82s. Add a 120ms edge-grace (a tap within 120ms after the marker exits green still counts) for touch latency. Difficulty can then scale via goal quantity, exactly per the pacing law.
- D3 tap: distance-scaled trickle (<=92px: 1.0; 92-180px: 0.3; beyond: 0.1) + 0.5s refractory on non-hits + goal-1 reserve. Mash ceiling ~0.5/s < 0.83/s correct.
- D4 choice: wrong 0.24 -> 0.15, 0.7s refractory, goal-1 reserve. Mash ceiling 0.21/s < 0.6/s correct.
- D5 choice: re-flash ONLY on wrong picks (guard `reflash_choice()` with quality < 0.5); after a correct pick the rotated target stays dim so the flash-then-dim memory design actually operates. Wrong picks keep the kind re-flash — no dead end.
- D6 hold: remove the 0.04 floor for continuous kinds — `var gain := amount if kind in ["hold"] else maxf(0.04, amount)` (or floor only in the discrete-press paths). Hold becomes exactly 1.0/s at any frame rate and goals mean seconds again. Throttle hold's note_success to one +10 per 0.35s of held time (fixes the 600/s score pump). Optionally drop tap-on-hold quality 0.6 -> 0.45 so a tap doesn't register as a scored success (it keeps its 0.06 trickle).
- D7 swipe: when a phase sets `dir`, check it: per drag event, `quality = 1.0 if drag_delta.normalized().dot(swipe_dir) > 0.3 else 0.6` and credit wrong-direction motion at 0.35x — still trickles, arrow now means something. DUCK finally verifies down.
- D8 swipe: divisor 150 -> 420px per unit AND clamp credited swipe progress to 1.8/s. Deliberate tracing (500-700px/s) = 1.2-1.7/s; scrubbing caps at the same 1.8/s — speed-capped, not precision-gated, so it obeys the pacing law. Batch note_success to >=0.35s apart.
- D9 circle: reject any per-event angle change > 0.5 rad as a no-op (honest 60Hz circling produces <=~0.35 rad/event; center-crossings produce ~pi — this kills the straight-line scrub without touching real circles). Clamp credit at 1.5 rev/s. Optional gentle direction check (wrong direction = 0.6x credit, still progress). Batch note_success as D8.
- D10 lens: `if lens_demo: skip the found/dwell block` — the ghost lens must tease, never collect. Optionally add a 0.05/s trickle while the child is actively dragging but not on a clue, so lens gains the same no-dead-end trickle as every other mode.
- D11 catch: acceptable as the intended mercy contract; if desired, trigger homing spawns at 3 misses instead of 2. Delete the dead `note_success(8)` branch or pass real quality from `_catch`.
- D12: resolves itself once mash is no longer faster (speed_quality stops rewarding it); optionally weight care_quality 0.55/speed 0.45 so a mash-heavy finale reads tier 1.
- D13: keep the double reward for discrete accomplishments (it is bounded and feels good); the continuous-mode throttles in D6/D8/D9 bound the +10 leg to ~29 points/s worst case.

## Bottom line
Mashing currently beats or trivializes 6 of 9 modes — timing (2.4x perfect play, worst), choice (3x), tap (1.4-2.4x), circle (2.4x+), swipe (no correctness exists), hold (frame-floor bug, 2.4x authored speed + 600/s score pump). Bop is the healthiest tap mode thanks to its captain reserve — that reserve plus a 0.6s miss refractory is the template: apply both globally and correct play strictly dominates in every mode while every miss still sparkles and trickles.

---

## Appendix B - preschool interaction critique (full report)

# Opera gesture surface — preschool interaction critique (Toca Boca / Sago Mini lens)

Sources read: `C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/codex-opera-art-regeneration/scripts/opera_gesture_surface.gd`, `scripts/opera_career_world_2d.gd` (PHASES + `_on_gesture` + `_process`), `scripts/opera_nursery_catch.gd`, house precedent `scripts/games/melody.gd`, `scripts/games/dolls.gd`, `scripts/games/fetch.gd`, and the designed-grammar doc `OPERA_JOB_GIMMICKS_2026-07-25.md`.

## The root defect: trickle-by-payout instead of trickle-by-assist

The no-fail law is implemented as a per-event cash payout for wrong input (`_on_gesture` floors every event at `maxf(0.04, amount)`, and the modes pay 0.24–0.32 for misses). Any payout on an unlimited-rate input creates a mashing economy. The math, from the actual constants:

- **timing**: green zone is 30% of the bar; marker speed 0.72–0.92/s means the window is open **0.33–0.42s** per pass, one pass every ~1.1–1.4s. Perfect play earns ~0.7–0.9/s. Mashing at 4 taps/s x 0.32 earns ~1.3/s. **Mashing beats perfect play roughly 2:1.** Worse, a 0.4s anticipation window is a precision demand — `fetch.gd` line 213 already documents the house learning this exact lesson: the old aim sweep "outran a 4yo's ~1s reaction (only ~1 in 4 finished)".
- **choice**: correct = 1.0, wrong = 0.24; random mash EV is 0.49/tap at unlimited rate (~1.5–2.0/s) vs. ~0.5–0.7/s for deliberate remembering. **Mash wins ~3:1**, and every wrong tap kindly re-flashes the answer, so mashing also dissolves the memory game.
- **tap**: hit = 1.0, miss-anywhere = 0.3. Mash-anywhere at 4 taps/s = 1.2/s, aimed play ~1.0/s. Mash wins without looking at the screen.
- hold (tap pays 0.06 vs. hold's 1.0/s), swipe/circle (need real displacement/angular travel), bop (stray tap 0.12, captain-HP reserve caps mash progress at goal-2), lens (taps do nothing), catch (verb-gated) are all mash-resistant. The exploit lives in exactly the three widget modes.

The house already owns the correct pattern, three times over: **melody** (orbs physically wait until she swims at them — wrong verb produces sparkle, never progress), **dolls/opera catch** (2s live-input verb gate, mercy steering, widening catch, pillow landings), **fetch** (1.0s press cooldown, sweep slows and the safe zone widens after each splash, 28s-style auto-assist in the painter act). No-fail should mean *the world leans in to make the right verb easier over time* (bigger windows, slower cues, magnet targets, eventual auto-finish), not *wrong input pays a wage*. Recommend globally: wrong input gets full celebration feedback (fizz, giggle, bounce) but 0.0–0.05 progress behind a 0.3–1.0s per-mode input cooldown, and mercy escalates with time as in fetch.

## Second defect: the card vs. the world

`bop` and `lens` play on the painted stage itself and are the two best things in the file. Everything else plays inside a 392x232 "light paper inset window" of abstract rings, arcs and a literal progress bar. For a 4-year-old the painting IS the game; the card reads as a form to fill out. The nursery `visual_context` branch (basin, bottle, cribs, blanket arrow) proves the team knows the fix — it just never shipped for the other twelve careers. Meanwhile the PHASES voice lines promise diegesis the widget doesn't deliver: farmer FEED says "tap when the veggie reaches a piggy" and the child sees... a ping-pong slider on a bar.

What already works and must be kept: the ghost-finger demo, the 9s idle re-demo + voice reprompt, the choice re-flash mercy, the captain two-bop reserve, swipe-sweep hitting in bop (a dragged finger across the screen hits imps — perfect toddler motor fit), hold-release pausing rather than resetting progress.

## Mode-by-mode ranking, best to worst for a 4-year-old

| # | Mode | Verdict | Why |
|---|------|---------|-----|
| 1 | **lens** | **KEEP** | Direct manipulation, masked reveal (the designed detective grammar, actually expressed), fully self-paced, mash-proof (taps only move the lens), dwell ring shows progress, ghost lens demos itself. The best 4yo pattern in the project. Minor polish: hide pictured clue objects (footprint, button, bow) instead of generic sparkle dots. |
| 2 | **bop** | **KEEP** | World-level, big slow targets (118–150px at 46–74px/s), tap OR sweep both work, squash/spin/puff cause-effect, physical comedy, captain reserve defeats mashing. This is the template the other modes should aspire to. |
| 3 | **catch** | **KEEP** | The proven dolls grammar faithfully ported: verb gate, mercy lanes after 2 misses, widening catch, slower falls, pillow-safe misses, caught babies visibly accumulate in the cradle (collection = huge at 4). Nothing to change. |
| 4 | **swipe** | **RESKIN** | The motor verb is the single best fit at this age (drag/scrub beats everything), and it's mash-resistant. But it draws nothing in response — no frosting rope, no ribbon, no blanket movement — and the direction arrow is a lie (direction is never checked; any wiggle pays). Zero visible cause-effect is the cardinal preschool sin. |
| 5 | **hold** | **RESKIN** | Motorically fine as built — press-and-hold *anywhere* (position isn't checked), release pauses rather than resets, taps barely pay. But the only feedback is a white dot growing 16px→24px. A sustained gesture demands a continuously filling world: batter rising, bottle draining, thrust bubbles climbing. |
| 6 | **tap** | **RESKIN** | Tap-a-big-moving-thing is age-right and the 92px hit radius is generous (~1.5cm on tablet). But the target is an abstract ringed dot on the card, and the 0.3 miss payout makes aiming pointless. The persistent `tap_marks` are a quietly great idea — make them the fiction (toppings stay on the cake). |
| 7 | **circle** | **RESKIN** | Circles are genuinely hard under 5; the engine partly knows it (absolute angular change accumulates, so back-and-forth scrubbing near the rim counts — matching the gimmicks doc's stir finding). What's missing is any reason to circle: nothing rotates. Salvageable with feedback; the ~30px center dead zone is acceptable. |
| 8 | **choice** | **REPLACE** | Flash-then-dim turns three *identical* blue circles into a delayed spatial-recall test — that's working memory, not recognition, and the Toca school never dims. And it's the second-most mashable mode. The fiction ("match clue to place", "candy to chute", "seed to row") is screaming drag-and-drop, a designed grammar the act layer already proved with the conveyor sort. |
| 9 | **timing** | **REPLACE** | Worst on every axis: the most abstract widget on the surface (a literal UI meter), an imposed external rhythm (anti-self-pacing), a 0.33–0.42s anticipation window that violates the "never precision" law and shrinks further as `timing_phase` speeds up per phase index, and mashing strictly dominates correct play. The voice lines already describe the right design — the engine just never drew it. |

## REPLACE prescriptions (one new engine grammar per mode)

### timing → "watch-then-act on a big slow diegetic cue" (the fetch pattern)

One engine change: the cue is a *dwell state* on a world object, not a flying marker. The object charges up slowly (>=2.5s cycle), holds an open window >=1.2s, signals three ways at once (grows + glows gold + a chime, exactly like fetch's swelling green arrow with its tick sound — timing by ear, not just color). Tap during the window = 1.0. Tap outside = fizz + 0.05 behind a 1.0s input cooldown (fetch's `press_cool`), so mashing yields ~0.05/s vs. ~0.4/s for watching. Mercy per fetch: after misses the window widens and the cycle slows; after ~25s the phase assists itself closed (painter-act precedent). Difficulty across the act rises by cue *frequency*, never window size.

Per phase: chef BAKE — oven window slowly glows golden, tap the oven. detective NAME — the spotlight drifts and settles on the answer, tap while lit (the line already says this). ballerina DUET — the partner rises into the pose, tap on the held pose. candymaker PARADE — the cart rolls under the arch, tap as it passes (window = the arch width). farmer FEED — the piggy trots up and opens its mouth, tap the piggy. boxer JAB — pads pop up on a 1.6s audible beat (port the act-layer boxer's 72%-of-bar window). magician CABINET — the star on the cabinet swells and flashes. astronaut BOOST — the booster flame swells, tap at full flame (LAUNCH right after stays hold, giving a nice tap-then-hold payoff pair). racer TURBO — the boost pad glows as the kart approaches. popstar RHYTHM — each rainbow note swells in turn. nursery BURP — the baby's cheeks slowly puff, pat the back at full puff (keep the existing nursery context art, drop the meter drawn under it).

### choice → drag-and-drop with always-visible, visually distinct targets

One engine change: three pictured targets that never dim; a draggable item spawns center-bottom; drag ends inside the right target = 1.0 with a snap + pop; wrong target giggles the item back to start (no payout — structurally unmashable, since a drag must complete); item released nowhere drifts home (the act-layer magician's hat behavior, already written). Ghost finger demos the drag. Memory flavor, where wanted, comes from *distinct pictures* ("the sparkly candy goes in the RED chute"), which is recognition — age-appropriate — not recall of identical circles.

Per phase: detective MATCH — drag each clue card onto its glowing place. candymaker SORT — drag candies to colour chutes (this is literally the designed conveyor sort). farmer PLANT — drag the seed pouch to the glowing row. doctor FIND — drag the bandage/kiss to the plushy showing the ouch pictogram (the act-layer doctor's symbol system). astronaut PIPES — drag the pipe piece to the glowing socket. magician TRACK — the one legitimate memory fiction: keep watch-then-pick, but hats stay visibly distinct and shuffle slowly on screen; better, open with the act-layer perspective flip (drag the hat over Lamba yourself, then track it). ballerina STEPS, boxer ROUND, popstar DANCE — these are rhythm fictions, not matching: use the existing choice engine minus the dim timer (tap the pad/tile/arrow *while lit* — a parameter change, not a new grammar).

## RESKIN prescriptions

- **tap**: move the target out of the card onto the stage painting near the phase's station (the plumbing exists — bop and lens already do it). The target is a sprite from the codex flat-card pipeline: a topping (chef TOP), snack (farmer PICNIC, candymaker SHARE), paint splat (painter SPLAT), sparkle leak (astronaut PATCH), zoom strip (racer FINISH), cracked-bone glow (doctor X-RAY), the belt itself (boxer BELT, goal 1 — a single ceremonial tap, fine). Placed `tap_marks` persist as the fiction: toppings stay on the cake, snacks appear in trotters. Miss payout down to 0.05 with a 0.3s cooldown.
- **hold**: keep the engine; add a fill visual per fiction — batter level rising in the pan (chef POUR), bubbles filling the basin (doctor WASH / nursery WASH), milk level dropping (nursery FEED), syrup filling the mould (candymaker SYRUP), Lamba fading out (magician VANISH), a mic-level ribbon (popstar SOUND CHECK), thrust column climbing the rocket (astronaut LAUNCH), Roshan's wind-up crouch deepening (farmer MUD HOP), the glowing dance playing out while held (ballerina WATCH). The `visual_context` system is the template; give every career one.
- **swipe**: draw the stroke — the finger leaves a frosting rope (chef PIPE), ribbon trail (ballerina RIBBON), bandage wrap (doctor BANDAGE), rope ribbon (magician ROPE), sketch line (painter SKETCH), herd-sweep dust (farmer HERD), steering wake (racer STEER), and for nursery BEDTIME the blanket sprite tracks the finger down the crib. Either enforce direction with a generous ~90-degree cone (so the DUCK down-arrow is honest) or drop the arrow and present it as a scrub patch — the gimmicks doc's scratch-to-reveal shows how satisfying an honest scrub is.
- **circle**: put the rotating thing at the center and rotate it with the accumulated angle — the valve turns (astronaut VALVE), the wrapper twists (candymaker WRAP), the cast winds visibly around the arm (doctor CAST), Roshan pirouettes (ballerina TWIRL), the star portal irises open (magician PORTAL), the stir swirls the batter (chef STIR). Keep the abs-angle scrub forgiveness; add a painted circular track to invite the rim.

## Summary counts

KEEP: lens, bop, catch. RESKIN: swipe, hold, tap, circle. REPLACE: timing (→ watch-then-act big slow cue, 11 phases), choice (→ drag-and-drop, 6 phases; 3 rhythm-fiction phases become tap-while-lit via parameter change). Plus the global economy fix: wrong input celebrates but pays ~0, behind short cooldowns; no-fail is delivered by escalating assistance (wider windows, slower cues, magnet targets, ~25s auto-finish), which is the pattern melody, dolls, fetch, and the act-layer rebuilds already established as house law.

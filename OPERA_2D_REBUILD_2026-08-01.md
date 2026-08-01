# Pearl Opera career rebuild — five-beat structure (2026-08-01)

Owner direction: finish the semi-complete opera career minigames. Every career
act is rebuilt to one reliable arc, aimed at ~2 minutes of play, using the
accepted codex art wherever it can be used, on the shipping 2D path.

This doc sits on top of OPERA_CAREER_COMPETITION_SYSTEM_2026-07-29.md (which
stays authoritative for architecture: 2D lobby, OperaCareerWorld2D, hidden
rival until the finale, 3D floor bosses unchanged). It supersedes the per-career
phase lists that doc describes.

## The five-beat arc (identical shape for all 12 careers)

| # | Beat | Mechanic | Target |
|---|------|----------|--------|
| 1 | Short scuffle | 3 mischief imps invade the job world; tap each to bop | ~10 s |
| 2 | Learn the job | one gentle signature verb (teach) | ~8 s |
| 3 | Do the job | 2–3 distinct verbs, no verb repeated in an act | ~30 s |
| 4 | Big scuffle | the imp captain (2 bops) + crew steal the career's goal prop | ~15 s |
| 5 | Finale on stage | proscenium backdrop swap; dressed rival enters; the existing competition (score bars, cheer tiers) runs the last 2 phases; curtain call wins the prop back | ~35 s |

- Beat 4 → 5 narrative: the captain runs to the stage with the prop, the
  dressed rival challenges Roshan in front of the family crowd, winning the
  contest wins the prop back (it reappears at the curtain call).
- Combat is kid-safe: imps are friendly mischief, taps anywhere fizzle
  sparkles and still trickle progress (no dead ends), nothing can be lost.
- The finale competition start == the stage backdrop swap == FINALE_START,
  normalized to the last 2 phases (~30% of the act) for every career
  (fixes the old 17%–86% inconsistency).

## Mechanics inventory (gesture surface)

Existing modes kept: tap, hold, swipe, circle, choice, timing.
New mode: **bop** — the surface draws bobbing imp targets (vector fallback;
`assets/opera/worlds/actors/imp_mischief.png` / `imp_captain.png` override
when present); a press on an imp pops it (1 hit), the captain takes 2;
presses elsewhere emit a gentle fizzle (amount 0.12, quality 0.2). During
bop phases the action panel widens so the scuffle has room.

Phase gaps: each completed phase plays a 0.8 s sparkle sting; any touch
skips it (probe pumps therefore cost at most one extra gesture per phase).

## Per-career phase plans

Combat beats: B1 = 3 imps (boxer: 4, themed sparring). B4 = 5 imps + captain
(7 hits). FINALE_START = first stage phase. Goal prop = matted codex card
(assets/opera/worlds/props/) shown at the rival-side workbench until beat 4
steals it.

| Career | B2–B3 verbs | Stage finale | Goal prop (codex card) |
|---|---|---|---|
| chef | POUR hold, STIR circle, BAKE timing | PIPE swipe, TOP tap | finished_cake |
| detective | PEEK hold, TRAIL swipe, CLUES tap | MATCH choice, NAME choice | pearl_tiara |
| ballerina | WATCH hold, STEPS choice, RIBBON swipe | DUET timing, TWIRL circle | music_box |
| candymaker | SYRUP hold, SORT choice, WRAP circle | PARADE timing, SHARE tap | wrapped_candy_reward |
| doctor | WASH hold, FIND choice, X-RAY tap | CAST circle, BANDAGE swipe | recovered_starfish |
| farmer | PLANT choice, FEED timing, MUD HOP hold | HERD swipe, PICNIC tap | piggy_fed |
| boxer | JAB timing, DUCK swipe | ROUND choice, BELT tap | championship_belt |
| magician | VANISH hold, TRACK choice, ROPE swipe | CABINET timing, PORTAL circle | bunny_fish_reveal |
| painter | SKETCH swipe, FILL hold, SPLAT tap | STROKES circle, REVEAL choice | framed_sunrise |
| astronaut | PIPES choice, PATCH tap, VALVE circle | BOOST timing, LAUNCH hold | rocket_front |
| racer | STEER swipe, TURBO timing | LAP TWO swipe, FINISH tap | shell_trophy |
| popstar | SOUND CHECK hold, DANCE choice | RHYTHM timing, ENCORE circle | microphone_finale |

Detective keeps its 40 s rival clock and guided-reveal rematch across its two
stage phases. Racer/popstar/boxer run 6 phases; the rest 7.

## Codex art utilization

- Runtime today: 24 actor sprites (actors/), 12 goal-prop cards matted by
  `tools/prepare_opera_2d_props.py` into `assets/opera/worlds/props/`
  (navy-field removal, same non-destructive derivation as the actor slicer).
- Reference (unchanged): 36 flat sheets + 576 cards (prop/state/pictogram
  vocabulary), 2p5d keys/kits (composition), hybrid finale keys (bosses),
  opera_house_flat kits (stage grammar for the proscenium drawing).
- The proscenium stage overlay in `opera_world_backdrop_2d.gd` follows the
  stage/backstage kit grammar: elliptical arch, curtain swags, footlight
  apron row, career-accent trim.

## Pacing + validation

- Target: ~2 minutes of real play per act. New advisory probe
  `probe_opera_2d_balance.gd` simulates 3 personas × 12 careers on the real
  2D path and prints BALANCE2D| medians (the old balance probe measures the
  legacy 3D engines only). Calibration: sim seconds exclude act-entry
  narration, curtain call and return (~15–20 s), and sim children never
  fumble or re-listen — the advisory band is therefore 70–150 s sim-median.
- Measured 2026-08-01 (sim medians, casual child): chef 87, candymaker 86,
  astronaut 83, popstar 81, doctor 79, ballerina/magician 78, farmer 77,
  racer 74, painter 72, detective 68, boxer 67 — ten "ok", detective and
  boxer intentionally snappiest (clock drama / metronomic archetype).
  Dreamiest persona tops out at 134 s; nothing caps out; no fail states.
- `probe_opera_2d.gd` gains structural assertions: bop opener, pre-finale
  captain scuffle, stage-mode backdrop flip at the finale, rival still hidden
  through both scuffles.
- Bug fixed in passing: `OperaAct._hit_boss` drove `chime.pitch_scale`
  negative for bosses with >3 HP (error spam on every boss star).

## Owner corrections, same day (supersede the sections above where they differ)

1. **The codex career paintings ARE the backdrops.** The twelve accepted
   1024x576 scene keys in `assets_src/concepts/opera_jobs_2p5d_2026-07-24/`
   are copied verbatim to `assets/opera/worlds/backdrops/world_<career>.png`
   and drawn full-bleed (same 16:9 aspect as the 1280x720 viewport; within
   the 1024px-longest-side texture rule). This supersedes the 07-29 doc's
   "not loaded or stretched at runtime" demotion. The code-native vector
   sets remain as fallback only. Native >=2048 masters stay requested in
   OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md P3.
2. **The imp battles use the special imp costumes.** Scuffle crews and the
   captain render with the career's accepted costume slice
   (`rival_<career>.png`); the captain wears a drawn plain-gold band ring.
   Hits burst the accepted boxer bubble-puff card (`fx_bop_puff.png`). The
   captain scuffle happens under the proscenium (stage_mode from the steal
   phase onward) — the battles have a stage. The basic PIL imps remain
   fallback only. The costumed rival GLBs stay 3D/boss-path material.
3. **Every phase now actually speaks.** 81 per-phase lines plus the imp
   captain and detective-retry lines are Kokoro-rendered
   (`tools/make_voices.py`, `roshan_op_*` / `imp_op_*` keys wired through
   each phase's `vo` key and `audio_director._speaker_key`'s new imp voice).
4. **Playability audit (subagent judge panel, 8 auditors) applied:** frozen
   choice-target rotation fixed (was an identity at phase index 2 in five
   careers); choice lanes flash-then-dim so picks use recognition memory;
   ghost-finger demo acts out every gesture until first touch, and re-runs
   with the re-spoken prompt after 9 s idle; tap phases aim at a moving
   target that leaves marks; swipe phases can point down (DUCK); hold/
   swipe/circle presses fizzle-trickle (no silent dead input); emulated
   mouse events are ignored (no tablet double-input); panel/root/fill no
   longer swallow touches; the captain can never be mashed past (his two
   bops are reserved); the theft is a visible fly-away event; detective's
   rematch keeps the child's bar and score, shows the true answer steady,
   and pre-fills the remembered clues; detective NAME is a spotlight-timing
   reveal; racer LAP TWO is a loop-the-loop circle; timing pace escalates
   gently with phase index; grind-flagged goals trimmed. Remaining design
   options recorded by the panel (new gesture grammars: scrub-reveal,
   charge-and-release, drag-and-drop; per-career widget flavoring) are
   future polish, not blockers.

## Save / probe safety

ACTS, star bitmask, floor gating, save keys: untouched. All twelve rebuilt
acts live entirely inside OperaCareerWorld2D phase data. The legacy 3D
engines and their probes are untouched. Boss acts unchanged apart from the
pitch clamp.

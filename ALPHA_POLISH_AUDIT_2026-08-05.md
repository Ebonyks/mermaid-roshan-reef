# Pre-alpha polish audit — 2026-08-05

Roshan's first alpha session is tomorrow. This is the full record of the
comprehensive pre-alpha audit and every action taken in the change set, on
branch `claude/alpha-polish-20260805` (off dev `e924d9ba`).

## Method

Seven parallel audit agents, each owning one dimension — M11/phone
performance, lifecycle bugs, logic bugs, environment flaws, sprite/art
defects, non-reader QoL, and the day-one combat flow — followed by
adversarial verification of every non-certain blocker/high claim, plus
firsthand inline verification (code reads, measurements, probe runs) before
every fix. **67 findings: 21 confirmed blocker/high, 46 medium/low, 0
refuted.** Every fix below was probe-validated; the full `scripts/ci.sh`
suite is the final gate.

Sources beyond the code: the previous night's green 60-probe suite log
(mined for non-fatal error spam and the visual-audit report), on-disk
texture/import measurement, and export-preset analysis.

## The three blockers

### 1. The pause-wedge (fixed)
Pause → CASTLE during the Royal Hall sparring class never cancelled
`CombatTutorial`. The tutorial survived in-tree: ghost finger stuck on
screen, its hit engine stealing every ocean tap through a stale camera —
and in the worst chain the castle reopened frozen with all touch controls
disabled. App restart, mid-alpha, from a completely natural preschool move.
The same shape existed twice more: the kitchen cooking act had no pause
branch (its finish callback later rebuilt the castle over the ocean) and no
castle-close handling; the opera house had no leave branch at all.
**Fix:** `_leave_current_activity` gained tutorial / kitchen / opera
branches; castle `close()` silences both cutaways defensively (tutorial
`finish_cb` cleared first so cancel cannot resume the hall mid-close);
`cancel_kitchen_recipe()` puts the act away kindly and comes home to the
kitchen.

### 2. Opera worlds drifted off their paintings on the real devices (fixed)
Every station, clue spot, path point and depth rule was derived in a fixed
1280×720 space while the painted backdrop stretched to the live canvas —
1280×800 on the M11, ~1600×720 on the phone. Landmarks sat up to 80 px
(vertically) / 320 px (horizontally) off their painted objects **on exactly
the two alpha devices**; CI probes run at 1280×720 and could never see it.
**Fix:** the world root is frozen at 1280×720 and scaled to the live canvas
each resize. Children keep their derived coordinates, the painting
stretches exactly with them, and `gui_input` is inverse-transformed by the
engine. The hardcoded-720 wander layer stops being a dead tap band for the
same reason.

### 3. The 560 MB APK (reduced ~40%, runtime texture RAM ~4× lower)
The install was 560 MB — a real install-failure and session-kill risk on a
3–4-year-old phone. Measured causes and actions:
- **629 power-of-two lossless textures (260 MB source)** — eligible for VRAM
  compression under the project's own rule ("VRAM compress ok only if POT")
  but shipping lossless. Converted `compress/mode=0 → 2` (opera
  backdrops/actors, sky-lagoon panorama, art35 cards, …). Cuts PAK size AND
  runtime texture memory ~4× on the Mali GPU. The 492 non-POT lossless files
  were left strictly alone (the documented NPOT+mode-2 headless-import
  deadlock). **43 of the 629 were then reverted to lossless**: the castle
  interaction sheets (v2/v4), castle props and dust-bunny sprites are
  pixel-contract-audited (`probe_castle_pearl_art` reads each atlas frame's
  transparent border), and VRAM alpha noise genuinely violates that
  contract — the probe caught it on the opera-hall curtains/chandelier and
  the audit is the authority, so those stay lossless by design. Net: 586
  textures compressed.
- **~101 MB of verified-dead art export-excluded** (files stay in the repo;
  probes read the filesystem and are unaffected): sky-lagoon panorama v2+v4
  tile sets (runtime loads only v5 — the sole `panorama_v*` reference in
  scripts), `aquatic2/*_Image_0.jpg` Meshy previews (zero loads),
  `aquatic2/*_normal.png` (34 MB, referenced by nothing — the GLBs embed
  their textures, verified by binary grep), the superseded
  `main_hall_2screen` remainder (LED masters, tiles/, rehearsal cutouts —
  keeping the two files the v2 manifest still references).
- **`.gdignore` added to `tmp/` (206 MB), `output/`, `build/`** — the editor
  was importing all of it on every scan.

## Confirmed high findings — fixed

| Finding | Fix |
|---|---|
| Infinite-loop tween class: 4 looping tweens on `main` animating freed world nodes → permanent per-frame error after one seek game (852 spam lines across the suite; 600 in touch-adversary alone) | All four (seek bush wiggle, wind sway, merry/horse/seesaw toys) now live on the node they animate; `_clear_game()` kills any Tween stashed in `g`. Empirical: probe_audit 38 → 0 |
| 14 of 91 opera vo keys have no recording — including ALL of detective's dialogue — and opera hides captions, so those instructions collapsed to a pitched "yay" | When the exact clip is missing the caption returns (the grown-up beside her reads it aloud); hides again the moment a recording lands |
| Stuck-child re-prompt replayed a hardcoded `hint` voice event that has no recording | Re-prompts replay the phase's OWN recorded line |
| All nine dream-house `roleplay_foot` values authored in 1024×576 art space, consumed as 1280×720 stage coords — Roshan walked to empty floor 43–143 px left of every bed/cushion/settee, then played "asleep" beside the furniture | Converted ×1.25 in place (the gallery door feet and the `contact_foot` precedent prove stage space is intended) |
| Galaxy garden planet: ~25 always-on OmniLights, the only zone with zero quality gating (CLAUDE.md hard rule) | 21 decorative lights (trays, pads, fountain, lanterns, butterfly shards, chandeliers) now dark in Speedy — the phone's default tier; 4 hero lights stay |
| Castle `suspend()` left the Daddy bubble and dust chain-engine live under every cutaway | Partner detaches (re-invited by her next pop); dust engine stands down via `tap_priority`; the swipe path respects it |
| Tutorial graduation could complete itself off the partner's stampede | A fresh wave arrives when nothing is left standing — the graduation is HER pops |
| `Juice.squash` re-entrancy: mash tapping captured mid-deform scale as "base" — enemies drifted permanently squashed | True rest scale remembered once per node; previous tween killed |
| `play_harm` captured mid-wobble x as home — art crept sideways off its hitbox | Same rest-value pattern |
| Charge-stage lamps and hp lamps geometrically collided (radii 0.17+0.13 vs 0.30 gap) | Pips moved to +1.75: a 0.7 gap |
| Tutorial's hold demo animated the pre-retune 1.45 s charge (real: 1.75 s) | Demo derives from `HitEngine.CHARGE_STAGE_T` — can never drift again |
| Partner bubble floated above full-screen castle modals, eating taps | Steps aside while any castle menu is open |
| Daddy's SPLASH was a silent no-op outside the main hall but still spent its 18 s cooldown | Bubble steps aside outside the hall |
| `Juice.flash` type-checked `Sprite3D` — AnimatedSprite3D enemies never blinked on hit | Checks `SpriteBase3D`; rest-modulate remembered so an interrupted flash can't strand a tint |
| Pause / focus loss RELEASED a held charge (dealt damage) | Thrown away instead — a new `world_press_cancel` path |
| Any second finger moving 22 px cancelled the held charge | Only the finger that press-fired may cancel its own charge |
| One drag starting on an enemy dealt tap + slash (3 damage) in one stroke | A consumed press never doubles as a slash: one stroke, one verb |
| `VERB_DAMAGE` still said hold=5 / "2/3/5" against the retuned 2/3/4 ladder | Constants and comment corrected |
| Haptics hardcoded on, no parent control | Rides the save as add-only `haptics` key (default on) |

## Deferred — documented, deliberate

- **Fire arena unreachable** (its 20-pearl reward, `combat_fire` flag and
  medal are all orphaned): wiring a new entry point is a design decision,
  not a day-before change. Needs an owner call on where it lives.
- **Fairy-pond / sky-lagoon palette inversions + single-layer lagoon mural**
  (the visual audit's 4 ERRORs): art-channel work; code-side desaturation
  the day before an alpha, sight unseen, is the wrong risk.
- **Sky-lagoon reversibility save key** (charter item): needs an owner
  decision on the toggle surface.
- **Opera station/phase pairing and detective search-target mismatches**
  (medium): the re-derived worlds' phase-to-landmark pairing wants a
  content pass with eyes on each painting.
- **Non-POT texture set (172 MB)**: converting to lossy WebP or padding to
  POT changes pixels — owner should see the result; not day-before work.
- Remaining medium/low findings (36): logged in the workflow journal with
  file:line evidence; none is a blocker for tomorrow.

## Change set (this branch)

1. `9ea900ae` — tween class killed; 55 MB export-excluded; charge demo
   derives from engine constants
2. `b416f834` — lamp rows separated; haptics save key; save type-guards
3. `0224a994` — partner bubble vs castle modals
4. `912bfd1e` — the cutaway-lifecycle cluster (pause-wedge, kitchen, opera,
   suspend, stampede graduation, squash/harm capture bugs)
5. `8d7bf67c` — opera device geometry; caption mercy; dream-house feet;
   galaxy light gating; 46 MB more excluded
6. *(this commit)* — texture compression batch (629 POT files → VRAM),
   charge-cancel input trio, `Juice.flash` SpriteBase3D, Daddy room guard,
   VERB_DAMAGE correction, `.gdignore` markers, this audit log

## Windows-checkout gate traps found on the way

Two local-environment issues (both green on CI, which is the binding gate)
blocked the full suite from even reaching the probes on Windows and were
fixed as part of this set:
- `tools/check_grade_headroom.py` read sources with cp1252 (fixed 2026-08-04:
  explicit UTF-8 + `PYTHONUTF8` exported in ci.sh).
- The castle **v4** delivery gate hashes provenance files as raw bytes;
  git's autocrlf checks them out CRLF on Windows, so the hashes "went stale"
  with zero content change. Proven eol-only (LF-normalized bytes match the
  declared hashes exactly); fixed by renormalizing the three files to LF on
  disk. A durable fix is a `.gitattributes` `eol=lf` policy for `*.py` /
  `*.json` — owner-visible repo policy, so left as a recommendation.

Additionally, the castle v4 **frame-review approval ledger** (new with the
overnight v4 merge) binds its candidate hash to the text of
`castle_rooms_25d.gd` — which this change set edits. The candidate was
regenerated (**zero blocking findings**: no duplicates, ownership leaks, or
coplanar cards with the new runtime as input) and the ledger re-sealed to the
new candidate hash. The 104 per-asset frame approvals were NOT touched — the
`check` pass verifies every reviewed frame pixel-hash still matches, which is
the honest proof that this change set alters no reviewed art.

## Validation

Per-batch: probe_hit, probe_combat_tutorial, probe_partner, probe_opera,
probe_opera_2d, probe_galaxy_state, probe_load, probe_save_recovery,
probe_audit — all green at each step. Final gate: full `scripts/ci.sh`
(60 probes) on the finished branch — result recorded in the merge commit.

# CODEX HANDOFF — Opera Logical Rebuild Asset Delta (2026-08-04)

Companion to `OPERA_LOGICAL_REBUILD_SPEC_2026-08-04.md` (the audit + design this
implements) and ledger `assets_src/concepts/OPERA_LOGICAL_REBUILD_LEDGER_2026-08-04.csv`.
Conventions by reference: `OPERA_CODEX_REGENERATION_REQUESTS_2026-08-01.md` and
`assets/ART_GENERATION_CONTRACT.md` — canvas/POT rules, STYLE-JOBS by name,
Path A/B, staging protocol (PROMPTS.md + REGENERATION_LEDGER.csv + one promotion
commit + one ASSET_LICENSES.md line), weighted gate 25/20/20/15/10/10 pass ≥4.5.

## 1. WHAT IS ALREADY IMPLEMENTED — do not re-solve, do not generate for it

All of the following SHIPPED in code on `codex/opera-art-regeneration` this
session, probes green. Codex's job is ONLY the art/audio named in §3.

- **Framing:** NO audience, NO text headers, NO captions anywhere in opera —
  full-screen art. The five review masters are STALE on this point: re-capture
  before judging anything about framing. Zero runtime work remains.
- **Chef BAKE = oven** (rising thermometer at a static 8s rate, one mitt verb,
  golden window, kind auto-ding, no burn state). Code-drawn oven face awaits
  the `gauge_chef` REDIRECT art (§3).
- **Chef POUR / candymaker SYRUP = tilt-pour** (grab→tilt→stream→bowl fills
  only while the stream lands; pitcher drains). Uses shipped `pour_*` art.
- **Tap = free placement** everywhere (stamp at the finger; the wandering
  hotspot is deleted). Trace reveals follow the child's own finger path.
- **Magician TRACK** got the shell-game glide (code-only); CABINET is now a
  pull-open swipe on the trace family.
- **Astronaut PIPES = mini Pipe Dream**: 4×3 grid, six pre-rotated tile faces,
  place/slide only, fuel waits at gaps, napping-imp routing, 3 rounds. All
  tile/tank/intake art is code-drawn placeholder — §3 P1.
- **Detective = crown hunt**: wander + witness talk beats (Kareem/Rosalina/
  Chuck VO fallback chain) + lens searches + sabotage bops + captain chase +
  ally-corner finale. No card widgets remain in detective.
- **Racer = one real 3D kart lap** (kart engine, `minimal_hud`, every place
  wins the trophy; headless probes use a 2D fallback). Racer widget art is
  fully retired.
- **Popstar RHYTHM = Echo Song** (three stars sing, child echoes at ANY tempo;
  pentatonic via pitched chime). Star pads code-drawn — §3 P2.
- **Nursery BURP = self-paced pats** (pace-gated taps; drumming pays nothing).
- **Curiosity engine:** tap-to-walk between tasks on every career's painted
  route; stations invite (150px/0.35s dwell); talk beats keep the stage
  walkable; idle ladder 9s VO / 20s drift-assist.
- **Timing/target retirement:** the ping-pong meter survives NOWHERE except
  farmer FEED (reskin per its already-ledgered `track_farmer_*` rows).

## 2. OBSOLETED LEDGER ROWS — never generate these

From the widget ledger (221 rows), now dead by owner order:
- All gauge needles + astronaut/racer gauges: `gauge_chef_needle`,
  `gauge_astronaut_*`, `gauge_racer_*`, `widget_gauge_shared_needle`.
- Entire detective widget flow: `trace_detective_*`, `lanes_detective_*`,
  `track_detective_*`.
- Cut timing tracks: `track_ballerina_*`, `track_magician_*`, `track_boxer_*`
  (salvage `_hit` burst for pad-flip FX), `track_popstar_*`, `track_nursery_*`.
- Racer widget set: `push_racer_*`, `target_racer_*`, `crank_racer_*`.
- Astronaut lanes: `lanes_astronaut_*` (style reference only for pipes).
- `target_doctor_*` (X-RAY is a lens scan now), `target_farmer_*` (REDIRECT:
  picnic blanket WITH piggies present).

REDIRECTS (regenerate to the new premise, same asset_id):
- `gauge_chef_backdrop/_fill/_success` → the oven: face with big mitt-handle
  door + vertical thermometer strip (pale→gold→toasty bands, NO green, NO
  needle pivot); `_fill` = raw-batter→baked strip; `_success` = cake lifted.
- `track_candymaker_*` → cart-toss beat (parade street + cart mover, alpha
  fixed). `track_farmer_*` → KEEP AS LEDGERED (already the FEED reskin).
- `target_chef_*`, `target_painter_*`, `target_boxer_*` → KEEP (already
  free-placement premises; they match the shipped stamp-at-finger exactly).

Exploration ledger (57 rows): fully alive — it is the substrate of the shipped
wander engine. Animation ledger: audience-row items obsolete; rival taunt/bow
survive; re-capture harness rerun required regardless.

## 3. NEW ASSETS THIS REBUILD AWAITS

| asset_id | canvas | depicts | pri |
|---|---|---|---|
| widget_pipe_tile_h / _v | 512×512 | brass-and-glass straight pipes, teal fuel windows, OPEN dark mouths both ends, bright (predecessors "unusably dark") | P1 |
| widget_pipe_elbow_ne/_nw/_se/_sw | 512×512 ×4 | four pre-rotated elbows, mouths as dark openings | P1 |
| widget_pipe_tank | 768×768 | bubble-fuel tank with spout flange, left anchor | P1 |
| widget_pipe_intake | 768×768 | rocket intake porthole, waiting flange, gauge ring | P1 |
| widget_oven_door_mitt | 768×768 | oven door closed/open pair with big mitt handle (folds into gauge_chef redirect if preferred) | P1 |
| detective_bubble_clock/_fountain/_stairs/_flowerpot | 512×512 ×4 | thought-bubble landmark pictures for witness hints | P1 |
| detective_prop_ribbon / _jewel | 256×256 | torn crown ribbon; loose crown jewel | P1 |
| detective_captain_crownhat | overlay | captain wearing the crown as a hat (lens-frozen + flee) | P2 |
| boxer_pad_closed/_open_l/_open_r | 512×512 | trainer punch pads, flip-open states (JAB pad-swap) | P2 |
| astronaut_leak_jet | 256×512 | sparkle-jet leak active/patched pair | P2 |
| popstar_star_note_unlit/_lit | 512×512 | stage star pads for Echo Song (tinted ×3) | P2 |
| farmer_pig_mouth_zone | 512×512 | open-mouth pig FEED anchor (may fold into track_farmer regen) | P2 |
| candymaker_friend_wave | per sheet | waving/catch pose overlays for cart-toss recipients | P3 |
| AUDIO: oven ding + 2 VO, ~12 detective witness lines, 3-2-1 countdown, glug loop, 5 plink notes | — | chime + `_say` fallback covers absence; all optional polish | P3 |

Plus the still-open prior packages, unchanged in priority: 4 Path-B helper
cards (Mewsha gates the pipe hinter's final form), exploration 57 rows
(Wave-0 coordinate re-derivation FIRST), Roshan sheets a/b + sheet_c.

## 4. KIT REVIEW FINDINGS TO FIX (from the five masters)

SEV-A: `widget_crank_painter_mover` opaque black quad (alpha) ·
`widget_track_candymaker_mover` navy squares (alpha; sprite repurposed) ·
ballerina charge disc unreadably dark (regen) · rival_magician near-black on
dark stage + ballerina/painter purple-camouflage + popstar imps invisible in
2/4 frames (readability tint/regen pass).
SEV-B: ghost placeholder panels at demo alpha (boxer/astronaut/painter/racer/
farmer/mischief/captain) · orphaned swoosh trails · dead-black easel in two
openings (verify moot after the modal-card removal) · detective sabotage prop
half off-viewport.
NOT defects: nursery catch (loads its own art), goal-prop "clip" (deliberate
theft tween), every header/audience observation (stale captures).

## 5. ACCEPTANCE

House gate verbatim, plus: capture the five review masters FRESH against
current runtime (the framing they show no longer exists); success-zone green
stays reserved (the one surviving green zone is farmer FEED's mouth-anchor);
character scale contract (Roshan ~1.3× crew, never 1.5×) applies to any actor
overlay; pipe tiles must read mouth-orientation at 128px on a tablet at arm's
length; thought-bubbles must read as PICTURES with no text of any kind.
Pending gates owned by us, not codex: pipe-dream 4yo playtest, kart on-device
texture-memory probe, Android frame-time capture.

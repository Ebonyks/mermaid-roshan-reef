# Codex handoff — Day One pacing round (2026-08-31)

_Implementation work orders for the Pacing and session flow wing's first
evaluation (`DAY_ONE_PACING_REVIEW_2026-08-31.md`; findings
`MA-PACE-001`–`MA-PACE-005`; rules `DL-PACE-01`–`DL-PACE-06`, design 06
§21). Owner direction 2026-08-31: the biggest need is pacing, timing, and
additional feedback — **more small victories** — and the chapter's movie
layer is largely missing for pacing and plot; the runtime must therefore
pace perfectly with zero movies while every story moment keeps a named
slot the cinematic pipeline can fill later. This is a SEPARATE round from
the 2026-08-26 code-refinement handoff: it may run before or independently
of Stage A, and it must not absorb or reorder that round's packages._

## Owner decisions required before the run (defaults proposed)

| # | Decision | Default if unchanged |
|---|---|---|
| D1 | What day-one completion unlocks (`MA-PACE-003`): (A) the close clears `day_one_active` → castle jobs/doors open as free play; (B) bedtime close, castle rests until chapter 2; (C) keep `day_one_active` with a new completed-state door language | **A** |
| D2 | Rumi's voice: proposed `("af_sky", 1.12, 0.99)` — calm, watery glow; `af_sky` is downloaded and free since Gabby's removal | Generate, owner listens before acceptance |
| D3 | Daddy Mermaid's redirect lines: his voice is a SACRED family recording; TTS in his name would break voice identity (`DL-SND-03/05`). (A) reassign the spoken redirect to Roshan (`roshan_day1_resting`), Daddy keeps captions + his real recordings; (B) the owner records one real hint line | **A** |
| D4 | Supply hunt (`DL-PACE-06`): (A) collapse to one honest beat ("We got the sponge and the brush!"); (B) restore a real two-find hunt (tap each tool, then the basket — the `MAX_SUPPLIES = 2` machinery exists) | **A** (smallest truthful change) |
| D5 | Boss first-contact window (`DL-PACE-05`): baseline 1.2 s, final round 1.0 s, narrowing to today's 0.75/0.65 on demonstrated success; mercy unchanged as the floor | Proposed numbers |
| D6 | `.github/workflows/probes.yml` twin edits (day-one probe promotion + beat-lint wiring): workflows are explicit-task-only, so WP-P7's workflow half runs ONLY with this authorization | Withheld until granted |

## Ground rules (binding on every package)

All ground rules of `CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md`
apply verbatim — governance home on branch
`claude/master-audit-game-analysis-qiko9l` (read and write governance
there; dev's copies are stale), branch law (`codex/<topic>` off fresh
`origin/dev`, suite green, never `master`), smallest truthful change,
invariants outrank goals, additive save keys only, probes as the gate,
reversibility-is-part-of-done (delegating shims, recorded inverses),
single-writer governance, and its escalation triggers. Round-specific
additions:

- **No cinematic production.** This round builds slots and runtime
  fallback beats only. Generating, commissioning, or accepting movie
  frames belongs to the Imagine/cinematic pipeline under the AGENTS.md
  full-frame rule — out of scope here, always.
- **Protected voices are untouchable** (`DL-SND-05`): `daddy1..3.ogg`,
  `chuck.ogg`, `chuck_bark.ogg`, `voice_yay.mp3`. New clips are new files
  via `tools/make_voices.py` per its manifest; never regenerate the
  library wholesale.
- **The growth law applies now, not just in the platform era**: new
  day-one logic lands in `scripts/day_one_director.gd` or the
  `day_one_*` game files. `scripts/main.gd` may gain only thin
  delegations when a seam demands it, and the package report must show
  the main diff (`MA-CODE-001` is the round's standing constraint).
- **Wings**: conform to the Animation improvement wing (use
  `scripts/juice.gd`, `tools/audit_animation_polish.py` stays green) and
  do not touch the tablet performance wing's scope (thresholds, capture,
  device measurement — report expected deltas instead).
- **Behavior contract**: probe-visible completion logic, state keys,
  reward agency (`DL-AGE-04/05`, `DL-MOT-05`), and the no-fail rules are
  unchanged unless a package's Do explicitly names the change.

## Stage 0 — verify first (every package)

Before implementing, re-verify the package's finding mechanism at your
head exactly as recorded (file:line anchors in the finding). "No change
needed" with evidence is a valid outcome; report it instead of
manufacturing a change.

---

## The voice line script (WP-P1's content — implement verbatim)

New `CHARS` row: `"rumi": ("af_sky", 1.12, 0.99)` (D2).
New `LINES` entries (key → speaker, text). Wiring contract: the call site
passes the key's suffix as `show_msg`'s `vo` (e.g.
`show_msg("Roshan", "...", "day1_sink")` → `roshan_day1_sink.ogg`);
`show_msg` remains the ONLY voice+caption entry — delete trailing
suppressed `_say` calls as you rewire each site.

| Key | Text |
|---|---|
| `roshan_day1_castle` | Our castle needs us! Follow the path! |
| `roshan_day1_dust` | Dust bunnies! This castle needs our help! |
| `roshan_day1_golden` | Follow the golden rainbow door! |
| `roshan_day1_resting` | That door is resting! Let's find the golden door! |
| `roshan_day1_room_clean` | This room is sparkly clean! |
| `roshan_day1_finish_first` | Let's finish the glowing room first! |
| `roshan_day1_basket` | Tap the cleaning basket! |
| `roshan_day1_supplies` | We got the sponge and the brush! Let's clean together! |
| `roshan_day1_sink` | Scrub the sink in little circles! |
| `roshan_day1_sink_win` | Ooh, shiny sink! |
| `roshan_day1_tub_tap` | Tap the tub to drain the yucky water! |
| `roshan_day1_tub_scrub` | Brush the tub back and forth! |
| `roshan_day1_bathroom_win` | The bathroom is sparkling! |
| `roshan_day1_pool_route` | The sparkle pool needs us! Tap the pool picture! |
| `roshan_day1_skimmer` | Sweep up every piece of trash! |
| `roshan_day1_skimmer_win` | The water is getting cleaner! |
| `roshan_day1_waterfall` | Pull the trash down from the rainbow waterfall! |
| `roshan_day1_waterfall_win` | The waterfall is flowing again! |
| `roshan_day1_seahorse` | Tap tap tap! Help the seahorse! |
| `rumi_intro` | Thank you, Roshan! You saved our pool. I'm Rumi! |
| `roshan_day1_pool_next` | Baby Eagle needs us! Follow the golden door! |
| `sparkle_day1_help` | Chirp! Two dust bunnies have me! Bump them away! |
| `sparkle_day1_win` | Chirp! You saved me! |
| `roshan_day1_stuffie_next` | One more room! Follow the golden door! |
| `roshan_day1_art_collect` | Tap the loose art supplies! |
| `roshan_day1_art_collect_win` | All the supplies are put away! |
| `roshan_day1_art_scrub` | Now tap the grime away! |
| `roshan_day1_art_scrub_win` | The craft room shines! |
| `roshan_day1_desk` | The magic paint desk is glowing! Tap it! |
| `roshan_day1_all_rooms` | All four rooms are clean! The big back door is glowing! |
| `roshan_dustboss_show` | Ooh, he's the GREAT dust bunny! He's too puffy to bonk! |
| `roshan_dustboss_tell` | When he jumps and his star flashes — tap him! |
| `roshan_dustboss_closer` | Closer! Get under him and tap! |
| `roshan_dustboss_again` | So close! Wait for the flash and tap fast! |
| `roshan_dustboss_hit` | BONK! Great tapping! |
| `roshan_day1_close1` | We cleaned the whole castle! It's all sparkly! |
| `roshan_day1_close2` | What a big day! More adventures tomorrow! |

Reuse without generation: `everyone.ogg` ("Hooray!", 1.95 s) at the
four-rooms beat; `roshan_win`/`roshan_oops` where a dedicated line is
overkill; `wacky_fail` stays the tub bunny's comic yelp (it reads as a
character bit, not Roshan).

## The movie slot inventory (WP-P6 builds slots + fallbacks; production is the cinematic pipeline's)

| Slot key | Moment | Plot purpose | Target length | Today |
|---|---|---|---|---|
| `grok_opening_flight` | Arrival over the lagoon | Establish home and the goal | 10–15 s | Request key only; nothing renders |
| `grok_dirty_castle_video_2` | First castle entry | Inciting incident — dust bunnies took the castle | 8–12 s | Request key only |
| `day_one_bathroom_entry_movie` | Bathroom reveal | First job framing | 6–10 s | `.ogv` seam exists; fails open silently |
| `day_one_bathroom_end_movie` | Clean-bathroom payoff | First victory writ large | 6–10 s | `.ogv` seam exists; fails open silently |
| `day_one_rumi_reveal` | Pool climax | A new friend joins the story | 8–12 s | Runtime-rendered rise (KEEP as the permanent fallback) |
| `day_one_boss_door_open` | Fourth room done → royal hall | Act turn | 8–12 s | Nothing |
| `day_one_close` | Post-boss | Chapter resolution / bedtime | 10–15 s | Nothing (chapter currently ends in the reef) |

**Slot contract**: each slot is a named seam that (a) plays delivered,
accepted media when present, (b) otherwise runs an in-engine fallback
beat — a short `say_sequence` (touch-skippable by design) plus a held
camera and Juice payoff — so the chapter is FULLY paced with zero movies,
and (c) reports played/fallback state for the probe layer. Silent
fail-open is the defect being fixed.

---

## Work packages

### WP-P1 — Voice the chapter (`MA-PACE-001`, P1) — runs first
**Do:** Add the `CHARS` row and all `LINES` above to
`tools/make_voices.py`; generate per-line (`--line <key>` per the
manifest — never a wholesale regeneration); add each clip's all-audio
ledger row (`DL-SND-10`, measurements per `DL-SND-12`); update
`VOICE_MANIFEST.md`'s character map. Rewire every Day One `show_msg` call
site to its semantic `vo` key per the script table, deleting the dead
trailing `_say` calls the 0.5 s gap suppresses (they are no-ops today —
removal is behavior-preserving); fix the art studio's uncooled
`_say("roshan","talk")` repeat (`day_one_art_studio.gd:393`) by deleting
it. The sink line's structural silence disappears with its own key (the
collision was on the shared `roshan_talk` cooldown).
**Non-goals:** no timing/beat changes (WP-P2/P3 own those); no touching
protected clips; no new speakers beyond Rumi.
**Gate:** a static check that every key in the script table resolves to
an existing OGG (extend `probe_voice` or the WP-P7 tool); no yay-fallback
on the Day One core path; suite green; owner listen note for Rumi (D2).
**Inverse:** clips are new files (delete to revert); call-site `vo`
strings revert by commit; ledger rows removed in the same inverse.

### WP-P2 — The micro-victory kit (`MA-PACE-002` payoff half, P1 priority per owner)
Every sub-completion gets the one-breath beat (`DL-PACE-01`): payoff on
the earned thing (Juice vocabulary + chime), its short win line, ~0.5 s
breath, then the next instruction.
**Do:** sink completion gains `day1_sink_win` inside the existing 0.70 s
busy window; pool skimmer and waterfall completions gain their win lines
in the existing 0.58 s / 0.42 s gaps (seahorse's payoff is the Rumi
finale — leave it); art studio celebrates 4/4 collected and 3/3 cleaned
(`day1_art_collect_win` / `day1_art_scrub_win`) with per-tap
chime+`Juice.pop` replacing per-tap captions; supply hunt per D4 default
— one honest beat (`day1_supplies`) replacing the three stacked captions;
stuffie second pin gets an escalated chime before the eagle's win line.
Also fix "Tap the loose loose brushes!" (the format string duplicates the
label's "loose") and align the art verb with its input per the script
("tap the grime away") unless the owner upgrades the input to a rub.
**Non-goals:** no completion-condition, count, or reward-agency changes;
no new textures.
**Gate:** probe_day_one_* state flows unchanged; probe_passive green
(beats pay nothing); `tools/audit_animation_polish.py` green; suite
green.
**Inverse:** per-file commits; each beat is additive and reverts cleanly.

### WP-P3 — Un-stack the macro beats (`MA-PACE-002` transitions half)
**Do:** castle entry becomes a two-line `say_sequence`
(`day1_dust` hold ~3.2 s → `day1_golden`) instead of the same-frame
overwrite; pool and stuffie completions gain their next-destination lines
(`day1_pool_next`, `day1_stuffie_next`) plus a golden-door pointer
refresh; the fourth room fires the four-rooms celebration on the REAL
path — `everyone` Hooray + `day1_all_rooms` + a hall pointer at the royal
mist (the line exists today only in the unused generic branch,
`main.gd:6939`); art announcements move to phase boundaries only (three
lines, not eight).
**Non-goals:** no door-language changes; no reordering of rooms.
**Gate:** no same-frame `show_msg` pair remains on the Day One path
(WP-P7's lint, report-only, must show zero for day-one files); suite
green.
**Inverse:** each transition is one bounded commit with its revert noted.

### WP-P4 — Chapter close and resume (`MA-PACE-003`, P1; consumes D1)
**Do:** the dust-boss win returns INTO the Main Hall over the restored
castle (a return-context seam instead of `_leave_arena_now`'s reef
teleport), then the `day_one_close` slot's fallback beat
(`day1_close1`/`day1_close2` + Hooray); introduce the explicit
day-one-complete state per D1 (default A: the close clears
`day_one_active`; door language and job gating consume the new state;
save key additive). Resume: once `day_one_dirty_castle_discovered`,
Continue lands at the castle doorstep (or hall) instead of promenade
x 610; suppress the reef-plane guidance line while Day One is active and
the castle undiscovered, replacing it with `day1_castle` and a castle-door
focus ring.
**Non-goals:** no reef/free-play content changes; no start-menu visual
redesign; the boss fight itself is WP-P5's only.
**Gate:** probe_day_one_director completion/gating extended for the new
state; probe_start_menu_routing updated for the new resume point (its
old claims change — that is the explicit goal, documented in the report);
no door left permanently `BLOCKED` without a recorded story reason; suite
green.
**Inverse:** the state key is additive; the routing change is one commit
with the old spawn as its recorded revert.

### WP-P5 — Assistance ladder and boss first contact (`MA-PACE-004`)
**Do:** one idle helper on the day-one announce path (director or a
small satellite): ~8 s idle → re-speak the current instruction's key;
~16 s → refresh the pointer/demonstration; never completes anything
(`DL-AGE-04`); retire the dead `SINK/TUB_MAX_GESTURE_SECONDS` constants
or implement them as the 16 s demo-refresh trigger. Boss per D5:
`VULNERABILITY_WINDOW` 1.2, `FINAL_ROUND_VULNERABILITY_WINDOW` 1.0,
narrowing stepwise to today's 0.75/0.65 on demonstrated success
(a per-round success counter — invisible ramp); mercy ladder unchanged
as the floor.
**Non-goals:** no new pointer art; no changes to non-day-one activities'
assistance.
**Gate:** probe_passive green across the idle windows (escalation pays
nothing); dust-boss probe green at the new constants; suite green.
**Inverse:** constants revert by commit; the idle helper is one
removable unit.

### WP-P6 — Movie slots and fallback beats (`MA-PACE-005`)
**Do:** a small slot registry in the day-one layer (director-owned; not
on main.gd) implementing the slot contract above for all seven slots;
the two bathroom `.ogv` seams keep their play path and GAIN their
fallback beats (today they fail open silently); `grok_*` request keys
route through the same registry; the Rumi runtime rise is registered as
`day_one_rumi_reveal`'s permanent fallback; `day_one_boss_door_open` and
`day_one_close` get their fallback beats (close beat shared with WP-P4).
Deliver the slot inventory table (state per slot) in the final report for
the owner's cinematic pipeline.
**Non-goals:** NO media generation, commissioning, or acceptance; no
change to the full-frame rule's domain; no autoplay of unaccepted media.
**Gate:** with zero movies present every slot demonstrably runs its
fallback (probe-assertable via slot state); with a placeholder `.ogv`
present the play path still works for the bathroom seams; suite green.
**Inverse:** the registry is additive and removable; seams revert to
today's silent fail-open.

### WP-P7 — Gates for the wing (`MA-CI-004` + the wing's candidate checker)
**Do:** promote the remaining day-one probes (pool cleanup, director,
integration, art attack state, castle dressing, start-menu routing;
shot probes stay advisory) into `scripts/ci.sh`'s trusted loop after
three consecutive local greens each; NEW `tools/audit_beat_spacing.py`
(+ unittest), **report-only first**: flags same-frame/near-frame
`show_msg` bursts in day-one files and verifies every script-table voice
key resolves to a file; wire into `ci.sh`. The `probes.yml` twin edits
(roster + lint) happen ONLY under D6's authorization, as their own
commit, exactly bounded.
**Non-goals:** no probe behavior rewrites beyond the assertions the other
packages name; no arming the lint as blocking (Stage R proposes arming).
**Gate:** promoted probes green ×3 locally then on CI; lint reports zero
day-one bursts after WP-P3; suite wall time inside the workflow ceiling.
**Inverse:** roster lines and the tool are additive removals.

### WP-PR — Independent re-audit (the round's Stage R)
An agent that implemented nothing re-executes every package gate,
verifies each beat against this handoff and `DL-PACE-01..06`, runs the
deliberate-break demo for WP-P7's promotions, confirms the growth-law
posture (main.gd diff reviewed; day-one logic in director/satellites),
then — alone — applies lifecycle transitions and ledger/`CHG` entries
serially ON THE GOVERNANCE BRANCH, finishing with
`python3 tools/audit_document_authority.py` → ALL OK there. Expected
transitions on full success: `MA-PACE-001/002/004/005` →
`FIXED_PENDING_VERIFICATION` (device/child look pending), `MA-PACE-003`
→ per D1's recorded decision; `MA-CI-004` history updated with the new
roster counts.

## Sequencing

`WP-P1` first — every other package consumes its clips. Then `WP-P2` and
`WP-P3` (parallel; minigame files vs main/director seams). Then `WP-P4`,
`WP-P5`, `WP-P6` (parallel, distinct seams; P6's close beat lands after
P4's return seam). `WP-P7` any time after P1 (lint after P3 to show
zero). `WP-PR` last. One package per agent per branch; workflow edits
(D6) as their own branch, never batched.

## Escalation triggers (stop and surface to the owner)

Everything the refinement handoff lists, plus: any D1–D6 answer found
insufficient in practice; any need to generate or accept media; any
save key beyond additive; any beat that cannot be built without growing
`main.gd` beyond a thin delegation; any protected-voice question.

## Reporting format

Per package: Stage 0 verdict → what landed (files, key constants,
lines) → gate evidence (probe names + results, lint output) → main.gd
diff stat → exact inverse. Final report additionally: the slot inventory
table with per-slot state, the voice-clip ledger additions, agent-per-
package and the WP-PR separation proof, and proposed lifecycle
transitions (WP-PR applies them).

## Kickoff prompt (owner pastes verbatim after review)

```text
Work the repo Ebonyks/mermaid-roshan-reef. The governance branch is
claude/master-audit-game-analysis-qiko9l: read every governance document
named below at that branch head, not from dev (dev's copies are stale),
and land all governance edits on that branch; implementation branches
fork off fresh origin/dev. You are the orchestrator for the Day One
pacing round. Read first: CODEX_DAY_ONE_PACING_HANDOFF_2026-08-31.md
(your work orders — obey its ground rules, owner-decision defaults D1-D6,
Stage 0, and escalation triggers exactly), then
DAY_ONE_PACING_REVIEW_2026-08-31.md, then design/06 section 21, then the
refinement handoff's ground rules it inherits.

Run WP-P1 first on its own agent and branch; then divide WP-P2..P6
across agents per the handoff's sequencing (one package per agent, one
branch per package off fresh origin/dev); WP-P7's probes.yml half only
under D6 and as its own branch. Per package: Stage 0 re-verify the
finding first ("no change needed" with evidence is a valid outcome),
implement only that package's Do within its Non-goals, full local suite
(scripts/ci.sh) green before pushing, CI green at each branch head.
Implementation agents never edit the governance files — deliver the
handoff's reporting format including each package's exact inverse.

Then run WP-PR with an agent that implemented nothing: re-execute every
gate, verify the beats against DL-PACE-01..06, then apply lifecycle
transitions and CHG/ledger entries serially on the governance branch,
finishing with python3 tools/audit_document_authority.py -> ALL OK there.

Deliver: per-package branches/PRs plus one final report with
agent-per-package, the WP-PR separation proof, gate evidence, the movie
slot inventory, and the voice-ledger additions. No cinematic media may
be generated or accepted in this round. Stop and surface to the owner on
any escalation trigger.
```

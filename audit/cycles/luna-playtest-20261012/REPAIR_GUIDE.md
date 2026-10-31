# Gameplay repair stages — 2026-10-12

Status: PROPOSED_REPAIR_SEQUENCE; all 57 independent reviews are retained, with a new rapid-input defect and fresh evidence on existing route/pipe findings; supporting implementation guide, not accepted gameplay. Baseline `e2b3c73789707aa49a91b4f42e2a9dd4b68225df`. This owner commission authorizes audit and guides; no runtime patch has been made.

## Stage 0: make evidence trustworthy

Freeze the build, preserve every failed baseline, classify internal probes versus viewport input, map every visible entry/exit/re-entry, and inventory live/dormant/debug surfaces from source. Reproduce the strongest reports before creating canonical MA records. Each repair must satisfy master section 9 and carry exact impact coverage. Retain source/line and raw log references. Do not adjust probes to fit a defect.

## Stage 1: preserve input and progress

Prioritize stuck routes, lost milestones, hidden controls stealing input, wrong target/cue, ghost completion after pause/exit, and duplicate rewards. Use one finger, visible choices and exact voice/pointer cues. Verify intentional/wrong/passive/repeated/second-finger/cancel/re-entry/save cases and sibling callers. Progress already earned survives; unfinished actions cancel.

## Stage 2: make actions legible and tactile

Match hit geometry to painted objects, keep required targets at least 110 base pixels or equivalent generous hit area, and show press acknowledgment within two rendered frames at 30 fps. Roshan travels, arrives, visibly works/contact occurs, then progress pays out. Separate immediate intent acknowledgment from physical action time. Device latency proof requires actual M11 recording; headless probes cannot provide it.

## Stage 3: tune timing with agency

Measure first successful action, consecutive forced wait, input-effective time, required repetitions, recovery after miss, natural stopping points, first-time/revisit/replay durations and interrupted resume. Constants are code facts; modeled child input/attention durations are assumptions. Preserve a teaching beat when it helps, permit honest replay shortcuts, avoid shortening action until contact becomes unreadable, and retain intentional advantage over spam. Validate the specific timing change with routed input and capture, then the full suite.

## Stage 4: improve play variety and replay

Agent hypotheses identify opportunities for meaningful choice, visible changing world states, different verbs and varied but readable repetitions. Reuse approved art and existing authorized mechanics. First make the actual child route work; dormant mechanics do not establish shipping completeness. Any new chapter or story change follows the current brief/owner boundaries. No inflated numerical fun grade.

## Stage 5: confirm on the actual device and with the child

Run short separate sessions on the exact M11 APK: new player, repeated activity and mid-action resume. Record touch-to-first-visible-response in video frames, missed intended touches, accidental adjacent actions, adult help, attention shifts, voluntary replay, stopping and preserved progress. Use no new identifying child media. Owner/child/device evidence remains separately pending until actually supplied. Publish/integrate only after required unchanged gates are green; no release is authorized by this audit.

## Ready repair brief: restore Chapter Two story entry — MA-PLAY-005

This existing **P0** leads the product repair queue. [L27](reports/L27.json) identified a passing resume fixture that manually opens hidden Farmer targets. Independent retained diagnostics confirm both branches: the [normal production config](verification/farmer_production_config/receipt.json) reports `house_reports_started=true` with zero phases, zero stations, no surface and setup rejection/script errors; the [phase-supplied diagnostic](verification/farmer_supplied_phases/receipt.json) builds three Farmer phases and five room stations, but still has `armed_station=-1`. These run the actual Director → House → Act config chain with injected post-boss state. They do not prove fresh-save visible-room traversal.

First resolve story phases without treating an absent override as an explicit empty list (`opera_career_world_2d.gd:665–705`). Ensure a rejected world setup cannot return a healthy started Act/House (`opera_act.gd:76–80`, `opera_house.gd:254–264`). Then map every commissioned story phase to its authored room object or an explicit story-owned visible entry (`opera_career_world_2d.gd:1890–1911`, `2497–2524`); do not add arbitrary sequential fallback stations or debug-only entry. Preserve the director's order, per-pick masks, additive save keys, owned Castle routes and no-free-star reward policy.

The retained diagnostics intentionally fail and remain outside the trusted suite. Make a new focused normal-room route probe for all eight party careers, completing each real touch/gesture and exit/re-entry. Include zero input, wrong room/phase, duplicate completion, saved partial resume and invalid config cleanup. Then the unchanged Chapter Two/resume/lawn/milestone/Opera/passive/full gates, exact-head CI and a normal fresh-save M11 route from Grand Puff through the party/lawn. Do not lower a probe, invent party completion or close `MA-PLAY-005` on a direct `_open_task()` pass. Visual, device, child and owner acceptance remain separate.

## Ready repair brief: seahorse fast input — MA-TOUCH-004

Start with the [canonical record](../../findings/ACTIVE_FINDINGS_2026-08-13.md#ma-touch-004) and [four-run confirmation](verification/seahorse_confirmation.json). Two fresh viewport bursts each send eight on-target press/releases on a nominal 300 ms schedule and settle at six tugs. Two 1.2 s counterparts reach all eight; the corrected slow fixture exits 0. The first fixture's stale dirty-waterfall assertion is preserved as a harness failure, distinct from observed tug counts. This is simulated desktop input, not a child or device result.

The edit target is `scripts/games/pool_seahorse_rescue_activity.gd:303`: `_register_tap` caps waiting work at `MAX_QUEUED_TUGS=3` while still displaying bubbles. `_finish_tug` must continue paying only after each local contact action. Preserve zero-input, wrong-target, second-finger and excess-after-completion negatives. Flush queued unfinished work on pause/focus/back/exit; preserve earned saved steps. Use the smallest input/cue repair, without new art, protected voice replacement or remote progress.

Reproduce with a fresh evidence name, for example `python -X utf8 -B audit/cycles/luna-playtest-20261012/review_tools/capture_pool.py --burst --output seahorse_baseline_new`. The same program with `--slow` is the cadence counterpart. The restored saved-state/clip-cancellation fixture is explicitly diagnostic; add a separate normal scene-entry/input path for repair acceptance. Do not overwrite old evidence. After the candidate, run eight fast/slow valid requests, off-target/zero input, repeated taps beyond completion, and interrupted queued work with reload/re-entry; retain source/fixture/PNG/log hashes. Then unchanged full gates, exact-head CI, M11 audio/touch, child comprehension and owner review. A positive fixture alone cannot close the finding.

## Ready verification brief: capture and route fidelity — MA-CI-008 / MA-PLAY-001

The [unmodified Pool capture](captures/pool/receipt.json) emits 11 images and seven failing checks; the inspected arrival/scoop images show the opening airplane. Its requested 1280 size became 2560×1369. The [declared 1280 adapter](captures/pool_diagnostic/receipt.json) exposes the room, but still fails two finale checks because its fast internal requests do not establish eight completed tugs. Keep both failures. Do not accept a file-exists or internal-state assertion as proof of the pictured activity.

Before each authoritative capture, check actual Mobile renderer, viewport dimensions, active location, visible scene layer and clip/overlay ownership, earned progress and intended motion beat. Reach final states by sufficient actual actions, not a helper's optimistic boolean. The normal route must start from a genuinely fresh or declared saved profile and show entry, understanding, action, reward, exit, return and re-entry. Fixture skips remain labeled. Workflow changes still require their separate explicit task; this audit changes no workflow.

[L52](reports/L52.json) also identifies a passing adversary invocation that sent no touch events. Its CLEAR lines cannot certify wrong-touch handling. In the next technical input review, record attempted, dispatched and accepted events, the actual active controller, and a positive first action alongside the wrong/off-target/second-finger negatives. Zero exercised input is `NOT_MEASURED` for that action scenario; retain the valid passive result separately. Do not lower or silently replace an existing gate.

## Review candidates requiring measurement

### Family Evening: semantic guidance and a return worth choosing — L57

[L57](reports/L57.json) finds the ingredient, stirring, movie and bedtime objectives use generic `talk` events (`scripts/comfy_games.gd:364–415`), consistent with the existing `MA-ACCESS-001` gap. The passed UI probe normalizes state but never plays this sequence. First hear the actual routed cue with captions unread, verify the pictured target and partial-step save, and observe discovery without naming the gesture. Any exact semantic replacement must use approved recordings or an independently sufficient authorized diegetic cue; preserve family voice originals. Source resolution does not prove what the player hears.

After completion, the source changes the room to a friend visit (`comfy_games.gd:312–315`). Test whether the child chooses that visit, leaves contentedly or tries to repeat the cozy sequence. A missing reset in this source does not prove a replay defect. Add a repeat path only after observed demand supports it, preserving completion, existing save keys and once-only rewards.

### Pipe ownership: verify the prior repair — MA-OPERA-013 / L30

The guard added by prior commit `32aee3361` is present at `opera_gesture_surface.gd:1249–1267`. The independent [corrected routed first-round diagnostic](verification/pipe_touch_local/receipt.json) passes six checks: the first touch acquires a real tile, a second touch and its release cannot steal it, the owner places it, the remaining tile is still available, census stays two, and the first round completes. The original failed fixture is retained; it never acquired its initial tile and cannot support a gameplay defect claim. Corrected initialization/local viewport coordinates are declared in the sources.

`MA-OPERA-013` is now `IN_PROGRESS` for a partial prior repair. This study changes no gameplay. Next cover all rounds, owner/unowned drags and releases, focus/pause, mid-carry exit/re-entry and the ordinary career route with actual viewport input. Confirm target-device behavior before closure. Reproduce any remaining loss before adding another guard or changing placement grammar; a direct private `_press` call does not establish the routed touch defect.

### Racer authority, duration and contest coverage — L19

[L19](reports/L19.json) separates the current working strip/`op_racer_steer` path from the painted circle/`op_racer_lap_two` target in `DL-INT-10`. Recheck the current ledger and owner decisions before choosing either as the repair contract. Do not change protected recordings or rewrite a design target based only on a passing probe. The same review identifies an untested imp-first finish under the target `DL-INT-14` contest contract; related `MA-OPERA-010` remains pending its existing external acceptance.

The two 800-unit laps at nominal 33.3 units/second suggest about 48 seconds of sustained unboosted driving, before the 1.5-second countdown, acceleration, steering, pauses and the two preceding phases. This is a source calculation, not an observed child session. First measure the normal TUNE → TO THE LINE → RACE route, longest continuous hold, lift/resume, time to trophy and voluntary replay. Confirm the applicable imp-first rematch contract in a separate controlled scenario before changing speed, lap count or mercy. Keep the no-input freeze and earned non-race progress.

L35 flags a default Hybrid source-rule gap: its large lower-left movement bay is assigned STICK while its hint/base/knob are hidden, contrary to `DL-UI-02`; its assigned passing probe forces Classic and cannot resolve that gap. First trace the active screen/context and competing world target at each bay boundary through actual input and Mobile capture. If the hidden bay owns the press, provide a clear existing movement affordance or let the intended direct-world interaction own it; preserve the 22-pixel drag threshold, direction anchoring, one-finger access and cancellation. Test discovery and adjacent target selection on the M11 before choosing a control change. No canonical closure or new finding is inferred from the Classic pass.

L04's source review suggests a scrub can claim a press before visible acknowledgment; it is not a measured two-frame violation. L08 notes narrow nominal waterfall lane strips; measure effective hit regions and separation before treating that as a target-size defect. L06 reports absent older optional bathroom movie resources; current selected story clips have their own manifest and source-specific contract, so that is not proof the shipping clips are missing. Do not regenerate, retime or replace owner-selected footage. These candidates need caller/runtime checks, not automatic canonical defect promotion.

For play appeal, test a concrete behavior rather than vote on a score: whether the child discovers the first action, notices its effect, chooses to repeat it, handles a miss, finds the exit and voluntarily returns. Prioritize meaningful world change and readable contact over more particle noise. In first-time and repeat visits, separate teaching/narrative holds from forced waiting and action time. Preserve legitimate short pauses/voice beats and save continuity; proposals are not accepted timing floors.

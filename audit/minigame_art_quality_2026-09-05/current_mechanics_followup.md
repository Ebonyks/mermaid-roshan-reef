# Current Opera mechanics: source follow-up

Date: 2026-09-05. Source context: published art base 9df000999a94572b64537c98f558841f6f3e3260, navigation parent aad0d450d8b8f1381badeeb4bcb939181115ab00 and the accompanying pose repair. Luna traced the definitions; the parent checked runtime expansion, stage timing and enabled scope. This source review does not invent measured child completion times or replace historical screenshot scores.

## Count the actual replay flow

There are 15 careers and **61 base lesson phases** in `scripts/opera_career_world_2d.gd` (PHASES). `OperaPerformancePlan.build` prepends three practice lessons to each of the three enabled Hall performances. The replayable runtime therefore contains **70 phases**, including nine practice additions. The older five-beat tables in the world file are explicitly legacy/audit-only; they are not current lesson authority.

| Current game | Base lesson sequence | Additional practice | Replay total |
|---|---|---:|---:|
| Geologist | RIVER, FOSSIL, PAN, GEODE | 0 | 4 |
| Teacher | PATTERN, COUNT, ADD, MATCH | 0 | 4 |
| Racer | TUNE, TO THE LINE, RACE | 0 | 3 |
| Ballerina | PEARL MIRROR, RIBBON TRAIL, GRAND TWIRL | First 3 | 6 |
| Magician | VANISH, TRACK, ROPE, CABINET, PORTAL | First 3 | 8 |
| Pop Star | SOUND CHECK, DANCE, RHYTHM, ENCORE | First 3 | 7 |

Only Ballerina, Magician and Pop Star enable the practice-to-stage plan. Chapter 2 story tutorials, overrides and scene adapters opt out. The other twelve careers retain their ordinary lesson flows. The `OperaMastery` table contains future calibration data for all fifteen careers, but that does not enable medals or the new competition structure outside the three Hall games.

## Rebuilt mechanics: strengths and next improvements

**Geologist.** The new surface has four distinct physical tasks: follow a 13-cell river route, clear 26 fossil cells, wash the pan through nine directional reversals of at least 46 pixels, and work five geode seam spots before a 120-pixel opening pull. The phase goal of 1.0 means one completed task, not one second. There is no authored failure timeout in the specialist surface. This gives geology more causal play than the retired generic sequence. Remaining questions are whether the fixed river route stays interesting, whether nine reversals suit a four-year-old's attention and motor control, and whether the fossil/geode reveal convincingly follows the child's contact. The coarse materials and unfinished cave/workbench presentation remain art defects; a more attractive brush alone does not close them. Spoken onboarding also remains uneven: RIVER, PAN and GEODE reuse `grotto_discovered`, while FOSSIL reuses `bathroom_tub_brush`. A voice cue is present, but three tasks do not yet have a distinct spoken description of their geology objective. Clear phase-specific narration and the existing visual demonstration should be reviewed together before calling the introduction complete.

**Teacher.** Tier 0 begins with ABAB continuation and two choices; counting is limited to 1–3; addition uses 1+1 and 1+2; shape matching offers two choices. Each kind has independently saved progress. Three clean successes promote that kind, up to tier 2. Later pattern tiers use AAB and ABC sequences, counting expands to 5 then 10, addition expands up to 10, and matching reaches four choices. The answer-driven surface has no failure timer. These are appropriate introductory design choices, but a claim that a four-year-old can consistently complete them still requires observed play. Improve the classroom objects and pointer contact while preserving exact quantities, different shapes and the two-choice opening; do not hide educational distinctions under decoration.

**Racer.** The race surface directly preloads `scripts/kart_driving.gd`, the existing driving kernel shared with KartGame. Two pit-stop activities lead to an actual two-lap steering task on the approved circuit composition. Constants are 800 distance units per lap, 24 seconds nominal lap calibration and two seconds input grace. These constants are not measured finish times. The repair is mechanically substantive: the historical 324-degree finale diagnosis no longer describes RACE. Remaining art work is clearer small drivers, control meaning and visible contact/boost feedback. The rejected tire-thumb experiment is not current art. The new held wrench and ready/steering poses address preparation-phase prop switching; RACE hides that separate actor and uses its driving presentation.

## Introduction and timing boundaries

Ordinary between-phase gaps are 1.0 second; entering the finale uses 2.6 seconds. Ballerina uses no generic phase gap because its specialist controls demonstration and voice holds. The panel reveal scales over 0.28 seconds and fades over 0.20 seconds. These are transition values, not tutorial length.

Ballerina's configured demonstrations are 2.15 seconds for a pose and 1.55 seconds for ribbon/twirl, with a 0.12-second cue. Assistance begins after five seconds and becomes stronger at ten. Between-lesson voice holds are at least 3.10 seconds, with a 0.05-second margin and longer holds for longer clips. The source therefore still warrants a natural-input timing audit: a short visual demonstration does not imply a short complete instruction cycle.

The Hall mastery clock is narrower than task-open wall time. `_performance_input` begins it on real stage input; `_performance_tick` counts only while the stage is active, the task is open, no phase advance is pending, and competition timing is active. Each new stage task resets the start boundary. Practice, discovery, between-phase gaps and pauses are excluded. Once interaction begins, a child pausing within the open activity can still consume active time. Test the complete spoken/demo/input sequence before changing medal calibration.

## Active Hall medals and future currency

| Hall game | Required unique quarter milestones | Gold: active time | Silver: active time | Silver correction allowance |
|---|---:|---:|---:|---|
| Ballerina | 12 | ≤54 seconds | ≤86 seconds | ≤2 misses, ≤1 assist |
| Magician | 20 | ≤40 seconds | ≤68 seconds | ≤2 misses, ≤1 assist |
| Pop Star | 16 | ≤40 seconds | ≤66 seconds | ≤2 misses, ≤1 assist |

Gold also requires zero misses and zero assists; both higher tiers require valid telemetry and all listed milestones. A completed stage earns at least Bronze, including when optional telemetry is missing or malformed. Practice-only and incomplete acts earn no medal. Four unique progress-quarter milestones are counted per stage lesson; repeated taps or held frames do not manufacture mastery credit. The three Hall games do not use Detective's timed-rematch retry path.

Encore values are cumulative best-medal values: Bronze 1, Silver 3, Gold 6. Bronze→Silver grants two additional tokens; Silver→Gold grants three. Repeating an unchanged medal grants zero, and a lower later medal does not reduce the best result. This preserves a useful future reward without encouraging repetitive currency farming. The thresholds are initial calibration data, not a validated distribution of child outcomes. Observe short sessions and assistance use before introducing spending pressure or expanding the system beyond the user-approved three games.

## Historical findings that must not be reused as current conclusions

The original mechanics report's 14-career/57-phase count predates Teacher and runtime Hall expansion. Racer's old circle-only finale and Geologist's three abstract tasks are superseded by the current specialist implementations. Historical scores remain attached to their original captured builds; neither this code trace nor green automated probes grants a new visual score. Fresh natural-navigation captures, complete action timing and target-device play remain required.

## September 6 material-feedback references

This targeted follow-up uses publisher descriptions and educational references, not timed hands-on competitor tests. Store claims below are attributed to their authors. No competitor tutorial duration, performance score or child outcome was measured.

- **Fossil reveal and assembly:** the current Android listing for [Poppu Dino Dig: Fossil Museum](https://play.google.com/store/apps/details?id=com.poppuworld.fossilmuseum) describes brush-led uncovering, large pieces that snap to silhouettes, gentle return of incorrect pieces and a completed-fossil transformation. Its advertised audience is ages 3–7, with no timers or losing. The useful design inference for Roshan is a readable material change under each brush stroke and a clear assembled result. The existing no-fail fossil mechanic supports that direction; the rectangular dirt cover currently weakens its feedback.
- **Geological cause and effect:** [Tinybop's The Earth](https://tinybop.com/apps/the-earth) presents erosion, deposition, earthquakes and volcanoes as processes children manipulate; its [publisher handbook](https://tinybop.com/assets/handbooks/the-earth/Tinybop-EL05-Earth-Handbk-EN.pdf) describes tap, swipe and exploration of geological features. This is a cross-platform design reference, not a claim of current Android availability. For Roshan's river, use a visible wet channel and displaced sediment to explain the traced path. Keep the initial short guided route before considering free shaping in later levels.
- **Scene changes as the reward:** [Toca Boca's Nature description](https://www.tocaboca.com/toca-boca-jr) emphasizes shaping terrain and watching it develop, including raising mountains. The inference for Roshan is to leave a changed material state visible after success. Do not immediately cover the washed minerals or opened geode with unrelated UI.
- **Panning should reveal separation:** [USGS's account of gold concentration](https://pubs.usgs.gov/gip/prospect1/goldgip.html) describes density-based separation from clay, silt, sand and gravel. For the child-facing art, show lighter sediment leaving while the finds remain visible in the pan. A gold pan need not resemble a handled cooking pan; the audit's defect is weak vessel/material depth and sediment feedback, not the absence of a handle.

These references support the next material-feedback work order. They do not authorize copied competitor artwork, establish exact introductory timing or make the current Geologist art pass.

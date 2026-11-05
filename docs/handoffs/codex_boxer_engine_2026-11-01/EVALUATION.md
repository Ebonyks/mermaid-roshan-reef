# Boxer engine evaluation (2026-11-01)

Status: `SUPPORTING_CURRENT` evidence for the
[Codex work order](README.md) and finding
[`MA-OPERA-015`](../../../audit/findings/ACTIVE_FINDINGS_2026-08-13.md#ma-opera-015).
It claims no authority over the Boxer's rules; the work order and the owner
decisions it records do.

- Branch evaluated: `codex/boxer-contact-engine-20261031` at
  `22df5b7541c7ddc28f8b7acd7f4947c8807e5dc0` (CI Probe Suite green on that
  commit; not merged into dev).
- Engine: Godot 4.7.2.stable.official.ed1daf0bf, headless, a fresh
  APPDATA/LOCALAPPDATA per run (`harness/run_iso.sh`).
- Method: numbers only. No screenshot, capture or image was made. Every
  number below comes from [`data/results_22df5b75.txt`](data/results_22df5b75.txt),
  printed by the scripts in [`harness/`](harness/).
- Not covered: real devices, the intended child, the owner's visual review,
  and the visual readability of the star, the demo hand and the warning.

## 1. Collision engine

| # | Finding | Evidence | What the child would notice |
|---|---|---|---|
| C1 | `OperaBoxingContact.sweep` is exact. | 340,000 cases (random, game-scale, constructed near-tangent at 0.02–5 px, growing pads, same velocity, 100,000 px sweeps) against an independent convex-search reference: 0 missed, 0 false. The worst first-contact time error was 0.000000122 px on long sweeps. All 5 invalid inputs were rejected. About 1.9 µs per call on desktop. | Nothing; this part is done. |
| C2 | A still glove anywhere in a punch's path blocks it, as the owner asked (`ODR-BOXER-CONTACT-CONTROLS-20261031`). | Grid of still gloves over both lanes, both gloves, guard drill and Title Imp: 14,592 placements at 60 fps on a 16 px grid, and 3,648 at 30 fps on a 32 px grid with a random 0.25 s stutter, all matching continuous geometry. 103 placements within 1 px of the contact edge also matched. | Holding a glove in the way always works. |
| C3 | Moving gloves are judged one frame at a time, alternately. In `_handle_drag` the glove is swept against a frozen fist. In `_process` the fist is swept against a frozen glove, because `_frame_start_gloves` is assigned at the start of `_process`, which makes its interpolation inert. | 10,000 swipes at 300–3,000 px/s in Godot's real frame order (`harness/crossing_v3.gd`). Guard drill: wrong calls 0.6% at 30 fps and 0.3% at 60 fps, none in mid-flight. Title Imp: 4.7% at 30 fps and 2.6% at 60 fps, with mid-flight errors at most one frame of fist travel (16.2 px at 30 fps, 8.1 px at 60 fps). At launch, a fast swat can be missed by up to one frame of glove travel (up to 39.7 px). At landing, a glove arriving up to one frame late still blocks (up to 67 px). A 0.25 s stutter raises Title Imp errors to 17.4%. | Rarely, a fast swat right as a punch launches does not count. A glove one frame late still blocks, which is kind. |
| C4 | The two punch lanes are too close. | Lanes are 179 px apart at the top, 141 px in the middle and 102 px at the bottom. A glove parked at x=640 blocked both lanes at every height tested (y 250–570) in both phases. About a quarter of all blocking positions block both lanes (share 0.253–0.263). Keeping one maximum-size glove from touching both fists needs each lane at least 132 px from the centre line. | Direction never matters: one parked glove stops everything. |
| C5 | In Title Imp, a high guard counts as punching too early. | Moving a glove from rest into the upper 60% of either lane (70% once help is maxed) touches the imp's closed target with forward motion, so `_try_forward_punch` emits a zero-amount try. That covers the guard drill's own demo point, `guard_target_position()` = lane progress 0.58. | She guards as just taught; the game replays the demo hand and raises help. |
| C6 | In Title Imp, lifting the finger after guarding counts as a failed try. | Guard, then lift: one zero-amount event, help 0 → 2, demo replayed (`RELEASE` line). The guard drill already exempts this. | A good block followed by a natural lift reads as a mistake. |
| C7 | Help rises two levels on one slip and never steps back. | The surface calls `restart_demo()` and emits a zero-amount gesture; `OperaCareerWorld2D._on_boxing_gesture` then calls `restart_demo()` again. One sideways jab try or one punch on the closed guard gives level 2 (target radius 114 px, windup 1.6 s, counter 2.2 s). Three accepted jabs later it is still 2. Help was maxed in 99–100% of simulated Title Imp rounds for every player. Dev `27c88288` has the same double call. | Targets swell and timings stretch for the rest of the phase. |
| C8 | Title Imp opens the counter whether she blocks or not. | Unblocked, the counter window still opens at 3.45 s. A block opens it at most 0.9 s sooner (0.2–0.4 s in the three measured placements). | Blocking barely matters in the main bout. |
| C9 | Missing sound cues. | `_play_player` calls: windup ring, block pop, friendly bonk, accepted pop, even-count bell, belt bell. There is no sound when the counter opens or when a punch launches, and no sound for any Soft Guard punch. | The "punch now" moment is silent. |

## 2. Rule checks behind the findings

| Check | Result |
|---|---|
| Counter gate, unblocked | Window opens at 3.450 s after a friendly contact; window 1.70 s |
| Counter gate, held guard at lane progress 0.2 / 0.5 / 0.8 | Opens at 3.017 / 3.250 / 3.067 s. The first two placements also raised help through C5, lengthening the windup. |
| Help after one sideways jab try | Level 2, target radius 114 px |
| Help after one punch on the closed guard | Level 2, windup 1.60 s, counter window 2.20 s |
| Help after one unblocked guard-drill punch | Level 1 (the career ignores cosmetic contact) |
| Help after three accepted jabs from level 2 | Still 2 |
| Finger lift after a guard | Title Imp: 1 failed try, help 0 → 2. Soft Guard: 0, help unchanged. |
| High guard registering as a punch | Lane progress up to 0.60 at help 0 and up to 0.70 at help 2, both lanes |

## 3. Nine hundred playthroughs

`harness/playthrough.gd` plays all five phases through the real surface with a
mock that mirrors `OperaCareerWorld2D._on_boxing_gesture`. Each simulated child
reacts at a lognormal speed taken from the research in section 5: medians of
0.60 s quick, 0.76 s typical and 1.10 s slow. Finger speed (180, 120, 80 mm/s),
aim error (2, 3, 4.5 mm), pauses and habits are estimates where research is
thin. Device scale: Lenovo Tab M11 0.1842 mm per stage pixel, a 6.4-inch
2400x1080 phone 0.0927 mm. Walking between stations is not simulated. The
instruction lines total 16.53 s (3.12, 3.41, 2.89, 3.96 and 3.15 s).

Times are medians, with the 10th–90th percentile in brackets, in seconds of
play inside the five phases.

| Player | Device | All five phases | Title Imp | Counter chances taken | Wait between Title Imp points (median, p90) |
|---|---|---|---|---|---|
| Quick | Tablet | 46.3 (41.8–51.9) | 26.4 (25.1–34.8) | 6 of 6 | 4.28, 5.15 |
| Quick | Phone | 43.4 (39.2–51.0) | 25.7 (24.5–33.9) | 6 of 6 | 4.20, 8.00 |
| Typical | Tablet | 74.8 (58.6–93.6) | 49.2 (32.8–64.6) | 6 of 11 | 7.98, 14.15 |
| Typical | Phone | 65.8 (55.1–86.0) | 41.5 (30.5–59.6) | 6 of 9 | 4.95, 14.07 |
| Slow | Tablet | 156.8 (109.3–210.9) | 118.3 (71.5–173.1) | 6 of 25 | 14.50, 48.25 |
| Slow | Phone | 114.3 (86.0–149.1) | 74.4 (49.5–111.5) | 6 of 15 | 10.25, 24.57 |
| Random scribbler | Tablet | 123.7 (92.3–152.9) | 50.0 (32.9–75.3) | 6 of 10 | 5.60, 16.20 |
| Random scribbler | Phone | 90.4 (74.8–109.5) | 41.3 (30.6–56.4) | 6 of 9 | 4.87, 14.22 |
| Parks one glove in the middle | Tablet | 72.0 (60.6–85.2) | 47.1 (33.4–58.8) | 6 of 10 | 5.10, 14.90 |

Each row is 120 games for the timing profiles and 60 for the last three: 900 in all.

What the playthroughs show:

- Title Imp is about two-thirds to three-quarters of all play for typical and
  slow players. For the three timing profiles, the other four phases take
  1.9–16.3 s each (medians).
- Purposeful play beats random scribbling in Glove Guide, Jab Practice and
  Soft Guard: about 2.4–2.8 times faster on tablet and 1.8–2.1 times on phone.
  In Title Imp the two tie (tablet 49.2 against 50.0 s; phone 41.5 against
  41.3 s), which breaches `DL-AGE-05`.
- Parking one glove in the middle is as good as following the punches (47.1
  against 49.2 s): C4 in play.
- For slow players, gaps between Title Imp points reach 24.6–48.3 s at the
  90th percentile.
- The model plays slightly faster on phone than on tablet because the edge
  controls multiply thumb movement. The same multiplier makes sideways aim
  2.4 times touchier, which only a real phone can judge.

## 4. Timing against child norms

| Moment | Now | What a 4-year-old needs | Read |
|---|---|---|---|
| Title Imp warning start to punch arrival | 2.05 s (2.50 s with help) | Simple visual reaction about 0.74–0.76 s, plus about 0.31 s to move a finger on an iPad; drags are slower. Reaching mid-lane from rest (282 px, 52 mm on the Tab M11) takes about 1.42 s typical and 1.98 s slow. | Tight. Aim for at least 2.0 s at entry level, 2.4 s on phone. |
| Title Imp counter window | 1.70 s (2.20 s with help) | React, sometimes pull back, then punch: 1.11–1.35 s typical and 1.55–1.84 s slow, before pauses. | Too short. At least 2.4 s, or open until she acts. |
| One Title Imp exchange | 4.17–4.83 s median; windup 1.15, flight 0.9, window 1.7, reset 0.65–0.85 s | Preschoolers tap naturally every 0.30–0.45 s and do not hold intervals much over 1.5 s by feel. | No steady pulse. Put cues on a beat. |
| Soft Guard punch | 0.8 s windup and 2.4 s flight, silent | Comfortable for every profile | Fine; add a sound (C9). |
| Warning signal | Not built | A warning tone speeds 4–5-year-olds by only about 50 ms; random waits after a warning give no benefit and cause more early responses. | Keep windups fixed in length. |
| Hit areas | Counter target plus glove: 28 mm radius on the Tab M11, 14 mm on the phone. Belt: 24 / 12 mm. | At age 4, about 90% accuracy on 24 mm mouse targets and 43% on 6 mm ones; no preschool touch standard exists. | Generous on tablet. On phone the 2.4x sideways gain leaves about 12 mm of thumb leeway; check on a real phone. |
| Whole visit | 43–157 s of play plus 16.5 s of instructions plus walking | A standard attention test for ages 4–7 lasts 7.5 minutes. | Fine overall. The risk is Title Imp's dry spells. |

Flash safety, for the planned warning: no more than 3 flashes in any one
second (WCAG 2.3.1). ITU-R BT.1702-3 accepts flashes whose starts are at least
334 ms apart at any size, warns that more than 5 s of flashing may still be
risky, and names children as at risk. Saturated red transitions always count
as flashes.

## 5. Sources

| Topic | Source |
|---|---|
| Simple and choice reaction time at age 4 (740 ± 162 ms simple; 1,145 ms two-choice) | [Kiselev 2015](https://benthamopen.com/ABSTRACT/TOBSJ-9-23) |
| iPad reaction and movement at ages 4–5 (simple 756.81 ± 297.07 ms reaction plus 308.12 ± 130.79 ms movement; five-choice 751.45 + 354.25 ms), n = 21 | [Moss et al. 2023](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2023.1134647/full) |
| Warning tones at ages 3–6 | [Casagrande et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC9170641) |
| Random warning delays at ages 4–5 | [Vallesi and Shallice 2007](https://neuroscienze.unipd.it/sites/neuroscienze.unipd.it/files/efl/publications/vallesishallicejephpp07.pdf) |
| Two-hand drag success 53.7% at ages 3–6 (reporting Vatavu 2015) | [Nacher and Jaén 2015](https://riunet.upv.es/bitstream/10251/77963/4/shortpaperVersionAutor.pdf) |
| Natural tapping tempo in young children | [Hammerschmidt et al. 2021](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2021.677201/full) |
| Beat following at ages 2.5–5 | [Bobin-Bègue et al. 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4256987) |
| Target size and accuracy at age 4 (mouse) | [Hourcade et al. 2003](https://drum.lib.umd.edu/items/f3e5dc45-7acc-40c6-8dfd-a258b9c0bc9b) |
| Attention test for ages 4–7 | [Conners K-CPT 2](https://cad.storefront.mhs.com/collections/conners-k-cpt-2) |
| Flash thresholds | [WCAG 2.2, 2.3.1](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html); [ITU-R BT.1702-3](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.1702-3-202311-I!!PDF-E.pdf); [Fisher et al. 2022](https://pubmed.ncbi.nlm.nih.gov/35132632/) |
| Lenient glove-contact blocking in VR boxing | [Reality Remake guide to The Thrill of the Fight](https://www.realityremake.com/articles/the-thrill-of-the-fight-beginners-guide-and-knockout-tips) |
| Touch boxing precedents (one side per fist; tap and swipe gloves) | [Macworld: Touch KO](https://www.macworld.com/article/201268/touchko.html); [Avenging Boxing](https://apps.apple.com/ae/app/avenging-boxing/id1644034232) |

Research gaps: no millisecond norms for intercepting moving objects at ages
4–5, and no touch target standard for preschoolers. The target sizes rest on
mouse studies.

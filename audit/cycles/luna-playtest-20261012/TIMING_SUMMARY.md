# Scripted timing evidence — 2026-10-12

Status: PARTIAL_MEASUREMENT. These are simulated game-clock seconds from the unchanged advisory runner on the frozen baseline, with its declared personas and manual 0.1-second ticks. They are not child sessions, physical input, normal Castle entry or observed enjoyment. [Receipt](verification/opera_pacing/receipt.json) · [Raw output](verification/opera_pacing/opera-pacing.log) · [Sensor verdict](verification/opera_pacing/opera-pacing.json).

The run attempted all 15 free-play career configurations with three scripted personas each. **12/45 completed**, **3/45 reached the 300-second simulation cap**, and **30/45 stopped at an unsupported gesture policy**. The overall sensor verdict is **CAPPED**, with wrapper exit 1; it is outside the trusted regression roster and must not be reported as a complete pacing pass. It does not bypass the separate Chapter Two progression blocker.

| Career with completed simulation | Speedy | Casual | Dreamy | What this helps test next |
|---|---:|---:|---:|---|
| Detective | 25.2 s | 30.2 s | 34.2 s | Compare objective discovery with decorative exploration; measure actual clue-search and hint waits. |
| Pop Star | 78.6 s | 96.1 s | 127.0 s | Observe phrase changes, sustained attention, natural stopping points and voluntary repeat; separate cue/turn-taking from forced waiting. |
| Nursery | 52.8 s | 60.8 s | 68.1 s | Observe whether the changing catch/feed/care actions stay clear and the player can stop/recover kindly. |
| Teacher | 21.6 s | 28.5 s | 34.0 s | Observe comprehension and choice of another lesson; a short successful lesson is not automatically too short. |

The persona constants are assumptions, not calibrated child measurements: prompt-listening allowance 1.2/2.4/3.2 seconds, discrete reaction interval 0.7/1.3/2.0 seconds, modeled clumsiness 0.05/0.14/0.28, and authored drag/circle speeds. Entry narration, celebration, return transitions, exploration and re-listening are excluded or simplified. The runner's historical 70–150-second comparison band is an advisory reference from the shared-shell brief; later specialist rules and actual child/device evidence control each activity. Do not lengthen Teacher or Detective merely to hit that band.

Chef capped in the same final tap phase at progress 2/7 for all three personas. The runner repeatedly supplies its generic tap policy; a cap is incomplete measurement and does not prove that a child cannot finish or that the activity lasts 300 seconds. Ballet, Candy Maker, Doctor, Farmer, Boxer, Magician, Painter, Astronaut, Racer and Geologist stop at their named specialist modes. Their partial elapsed times are not complete-activity durations and are intentionally omitted from the timing table.

Before using this sensor to tune those activities, give each unsupported mode an explicit input policy using its actual accepted target/gesture and preserve cancellation, wrong-action and no-input negatives. A solver must perform the physical verb and demonstrate the complete result instead of injecting progress. Keep each policy's assumptions, attempted/completed counts, caps, raw output and source hashes. The existing sampler and workflow are unchanged by this study; any later workflow modification requires its separate explicit task.

For game changes, follow the [repair stages](REPAIR_GUIDE.md) and repeat the [normal-route timing worksheet](PLAYTEST_GUIDE.md#timing-worksheet-and-repair-decision). Test first action, longest forced wait, input-effective time, repeated work, visible payoff, lift/resume, exit and voluntary replay. A shorter script duration is not evidence that the game became more fun.

# Production plan under Grok's 15-second maximum

The final cinematic is 42.5 seconds. No Grok request may exceed 15 seconds. Generate individual shots for reliability, then edit them into four continuity blocks. Do not ask one 15-second prompt to invent six camera cuts.

## Editorial blocks

| Block | Timeline | Duration | Shots | Narrative continuity |
|---|---|---:|---|---|
| B1 — Safety in flight | 0:00–0:12 | 12.0s | 1–6 | Plane → cabin uncertainty → chosen handhold → hug. |
| B2 — We arrived | 0:12–0:23.5 | 11.5s | 7–11 | Touchdown → Daddy demonstrates → Roshan copies → rise → door approach. |
| B3 — Crossing the threshold | 0:23.5–0:34.75 | 11.25s | 12–15 | Door/sky → countable route → descent → invitation. |
| B4 — Wonder | 0:34.75–0:42.5 | 7.75s | 16–18 | Reaction → exact Sky Lagoon reveal → quiet final handoff. |

These are assembly blocks, not recommended single-generation prompts.

## Shot generation schedule

Generate the authored duration plus approximately one second of editorial handles, rounded to an available Grok duration. Trim; do not time-stretch.

| Shot | Authored | Suggested Grok request | Output basename |
|---:|---:|---:|---|
| 1 | 2.0s | 6s | `B1_S01_open-sky` |
| 2 | 2.0s | 6s | `B1_S02_safe-room` |
| 3 | 2.0s | 6s | `B1_S03_roshan-notices` |
| 4 | 1.5s | 6s | `B1_S04_daddy-notices` |
| 5 | 2.0s | 6s | `B1_S05_the-choice` |
| 6 | 2.5s | 6s | `B1_S06_reassurance` |
| 7 | 2.25s | 6s | `B2_S07_arrival-felt` |
| 8 | 2.5s | 6s | `B2_S08_daddy-demonstrates` |
| 9 | 1.75s | 6s | `B2_S09_roshan-copies` |
| 10 | 3.0s | 6s | `B2_S10_offered-hand` |
| 11 | 2.0s | 6s | `B2_S11_to-door` |
| 12 | 2.5s | 6s | `B3_S12_new-air` |
| 13 | 2.5s | 6s | `B3_S13_safe-route` |
| 14 | 4.0s | 6s | `B3_S14_crossing` |
| 15 | 2.25s | 6s | `B3_S15_invitation` |
| 16 | 2.75s | 6s | `B4_S16_wonder-arrives` |
| 17 | 3.5s | 6s | `B4_S17_reef-waiting` |
| 18 | 1.5s | continue within the accepted 6s shot-17 take when possible, otherwise a separate 6s continuation | `B4_S18_final-handoff` |

## Transition inheritance

- Shots 2–3, 4–10, 10–12, 13–15, and 17–18 benefit from accepted-frame inheritance.
- Cuts that reverse camera direction—especially 15→16 and 16→17—need a new approved still rather than a forced video continuation.
- Shot 17 must start from the approved final-composition still. Do not make Grok discover the castle offscreen during a crane move.

## Assembly rule

Edit the accepted native clips to the exact authored times above. Preserve the 24 fps timeline. Use straight cuts unless the direction brief explicitly calls for a hold; do not ask Grok to generate title cards or UI.

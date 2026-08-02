# Sky Lagoon living-card implementation audit (2026-07-29)

## Authority reviewed

The requested v2 document was read and critiqued before implementation. Its
first paragraph now declares it superseded by
`SKY_LAGOON_LIVING_CARD_ANIMATION_V3_2026-07-28.md`, so v3 was also read in
full and treated as the newer proposal. Owner feedback in this task overrides
both documents: fireplace smoke must be thin wisps, not discrete thick puffs.

Working lineage was `cd741f556d2e7457aea00d4b53c1b0f4ab464a20`, not the
documents' stale `08c9adaa`.

## Initial critique

| Proposal | Verdict | Reason |
|---|---|---|
| Sprite3D living-card metadata | Accept | Makes structural audits and portability concrete. |
| One bounded ambient tick | Accept, adapted | Fits the existing promenade. The final loop reads the persistent array directly and creates no per-frame default array. |
| Coordinate-derived phases | Accept | Reproducible without random state. |
| Stage wind and deterministic gust | Accept, adapted | State must remain on `ReefMain.g` under repository architecture, not inside the persistent RefCounted helper. Integrated wind distance prevents a gust-boundary position jump. |
| Per-screen loop and overdraw budgets | Accept | Directly protects the Mali-G52 target and visual calm. |
| Night congruence | Accept, expanded | Tinting ambient cards alone would leave the mural and major cards in daylight. The implementation coordinates mural and world-card tint. |
| Cabin smoke | Accept with owner amendment | The document's puff art was rejected. Three staggered thin-wisp cards form one fireplace column. |
| `foliage_near` sway shader/reactive bend | Defer | The current stage has no approved extracted NEAR_Z flora card. Applying it to painted foliage is impossible; adding a duplicate card would violate the extraction rule and recreate the scrapbook defect. |
| V3 E1–E6 extraction table | Reject for this batch pending correction | V3 pins a `2de9b63d…13d4c5` master, while the actual approved v5 master is `017532ae864e534d9b356472e2e29150855ede6583a7f63f02f0401d28c7be41`. V3 also requires owner review after the E3 pilot. Old boxes must not be used against a different approved image. |
| V3 “current 43 nodes” baseline | Reject | The live revisit baseline was 27 cards before this change; Day One and revisit counts differ because the plane is temporary. |
| Pixel-identical cold screenshots as the only determinism gate | Adapt | Renderer/driver timing can produce false negatives. The probe compares complete placement/phase/motion signatures across cold builds and records day/night captures. |

## Experimental implementation and error ledger

Up to 20 alternatives were permitted. Four visual attempts were needed; the
loop stopped when the in-scene art and all applicable gates passed.

| Attempt | Result | Evidence / corrective action |
|---|---|---|
| 1 — rounded smoke puff | Rejected | In-scene capture read as a detached small cloud and contradicted the owner's thin-wisp direction. Preserved as rejected source evidence only. |
| 2 — pale thin wisp at provisional `(20.7, 14.0)` | Rejected | Structurally passed, but the wide playground capture showed it too faint and on the wrong cabin coordinate. |
| 3 — v1 wisp at v3 native chimney coordinate | Rejected | Correct cabin, but pale values vanished against cyan sky. Perspective correction also showed the card base needed to move from mural y `21.312` to landmark-plane y `20.040`. |
| 4 — regenerated v2 wisp | Accepted | Preserved the narrow S-ribbon, added a clear lavender edge/midtone, used a 46×256 RGBA runtime card, and remained attached/readable in day and night captures. |

Tool/test errors encountered:

1. The first attempt-2 run had no Godot import record for the new PNG.
   Godot reported “No loader found”; smoke count was correctly zero. The
   asset was imported before visual judgment.
2. The legacy full-project importer rewrote unrelated tracked `.import`
   records while reporting missing retired assets. Every tracked import
   mutation from that process was restored; only the final wisp import is
   retained.
3. The first focused inventory expectation used the old handoff total rather
   than the live revisit tree. The measured revisit inventory is 31 cards,
   while Day One is 34 because the plane contributes three transient cards.
4. A first lifecycle assertion counted all SceneTree tweens. Exit UI/music
   legitimately starts unrelated tweens, causing a false failure. The final
   gate directly verifies old stage/card instances are freed and all ambient
   state keys are erased.
5. The full local `scripts/ci.sh` wrapper could not pass its import phase:
   the repository's retired legacy assets produced invalid/unrecognized UID
   errors and repeated null-texture imports until the known importer
   deadlock. The process was stopped; 226 unrelated tracked `.import` changes
   were restored exactly. Before import, parser/lint, visual-audit stress
   (18/18), fairy-art checks, and Sky Lagoon congruency all passed.
6. A direct broader probe run confirmed unrelated baseline failures before
   reaching the Sky Lagoon probes: `probe_ocean_kingdoms` return-gate
   debounce, `probe_audit` storybook/tank/portal assertions and legacy tween
   loops, `probe_rank` pre-populated medals, and
   `probe_galaxy_state` partial rescue. The run was stopped rather than
   misrepresent those pre-existing red checks as regressions from this work.
   The exact-commit Linux CI import/probe result remains required before
   integration.

No runtime crash, gameplay regression, failed visual gate, or unresolved
ambient error remains.

## Implemented result

- One 6-second fireplace column at the actual upper-cabin chimney:
  3 staggered thin-wisp Sprite3D cards, 46×256 RGBA, LANDMARK_Z, rise/scale/
  fade, +x wind lean, peak alpha 0.72.
- Five living cards total: one far tree, one cloud, and three smoke cards.
- One deterministic 24-second wind envelope, with a 2-second rise to 1.5,
  3-second fall, and integrated drift distance.
- Grounded tree now has the required Sprite3D contact shadow.
- Coordinated night tint on mural cards and all `_add_sprite` world cards.
- Explicit teardown on promenade rebuild, castle entry, and level exit.
- Reusable contract documented in
  `LIVING_CARD_DESIGN_LANGUAGE_2026-07-29.md`.

## Node-type inventory

| Scope | Day One | Revisit / plane departed |
|---|---:|---:|
| Sprite3D world-art nodes | 34 | 31 |
| Visible Sprite3D cards | 29 | 26 |
| Backdrop Sprite3D cards | 12 | 12 |
| Living ambient Sprite3D cards | 5 | 5 |
| Smoke cards / visual loops | 3 / 1 | 3 / 1 |
| MeshInstance3D world-art nodes | 0 | 0 |
| CanvasItem world-art nodes | 0 | 0 |
| Shaded Sprite3D cards | 0 | 0 |
| Contact-shadow cards | 6 | 5 |
| Interactive targets | 5 | 4 |

HUD, touch controls, messages, and full-screen overlays are outside the stage
root and excluded.

## Acceptance evidence

Focused probe results:

- living-card contract: 5/5 conforming;
- quiet loops by screen: `0 / 1 / 2`;
- transparent-card coverage by screen: `12.6% / 18.9% / 39.5%`;
- cards over 10% coverage: `0 / 0 / 1`;
- ambient tick proxy: `1.71–21.09 µs` across audited 2,000-tick runs;
- deterministic phase/gust and cold-build signature: pass;
- night congruence: 12 backdrop cards + 5 living cards pass;
- teardown and rebuild: pass.

Captures:

- `audit/living_card_v2/attempt_04_playground_wide.jpg`
- `audit/living_card_v2/attempt_04_cabin_smoke_wisp_day.jpg`
- `audit/living_card_v2/attempt_04_cabin_smoke_wisp_night.jpg`
- `audit/living_card_v2/final_screen_1_runway_revisit.jpg`
- `audit/living_card_v2/final_screen_2_playground.jpg`
- `audit/living_card_v2/final_screen_3_castle_smoke.jpg`

## Repeat critique after implementation

| Goal | Final status |
|---|---|
| Living-card contract and structural Sprite3D compliance | Met |
| Deterministic ambient/weather hierarchy | Met |
| Thin fireplace smoke, readable in context | Met after four attempts |
| Per-screen restraint and Speedy budgets | Met |
| Night congruence | Met |
| Lifecycle ownership/cleanup | Met |
| Authored playground and plane remain dominant | Met; existing interactions unchanged |
| Near-card pinned-tip sway and Roshan brush-past | Not applicable yet; no conforming near extracted card exists |
| V3 E1–E6 extraction/heal batch | Correctly not performed against a hash-mismatched master; requires a revised inventory pinned to `017532ae…be41` and the document's mandated E3 owner review |
| V3 master/seam/congruency evidence for a v6 | Not applicable because no master pixels changed |

The appropriate adjustment was to make sway/reactive behavior conditional in
the shared design language, rather than manufacture duplicate foreground
cards. The stage is more alive without compromising the approved cohesive
painting.

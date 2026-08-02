# Master design — consolidated open work

_Every unresolved finding from all 149 documents, deduped and **re-verified
against the tree at `claude/audit-consolidation-design-1m5yd2`, 2026-08-02.**_

Each item states how it was checked. "Verified open" means I confirmed it in
today's code or by running the repo's own gate. "Reported" means it comes from
a document and I did not independently re-measure it.

| # | Item | Class | Status |
|---|---|---|---|
| [OW-1](#ow-1) | `CLAUDE.md` and `AGENTS.md` contradict each other | process | verified open |
| [OW-2](#ow-2) | No `world_style` reversibility toggle | process | verified open |
| [OW-3](#ow-3) | Promenade parallax never runs — one mural, not a stack | art/engine | verified open |
| [OW-4](#ow-4) | Roshan can never pass behind anything | art/engine | verified open |
| [OW-5](#ow-5) | Background out-saturates foreground | art | reported (tool needs PIL) |
| [OW-6](#ow-6) | The world is not stitched; no reachability probe | design/code | verified open |
| [OW-7](#ow-7) | The reef pilot was skipped | process | verified open |
| [OW-8](#ow-8) | Engine consolidation backlog (steps 2–7) | code | verified open |
| [OW-9](#ow-9) | Asset hygiene, orphans and APK weight | art/build | reported |
| [OW-10](#ow-10) | Visual-design audit still advisory | process | verified open |
| [OW-11](#ow-11) | Living-world layer has no depth | art | verified open |
| [OW-12](#ow-12) | 45 probes exist outside the CI gate | test | verified open |
| [OW-13](#ow-13) | World-map geography needs four owner decisions | owner-gated | open |
| [OW-14](#ow-14) | Opera art requests P3-04 / P3-05 / P6 / P7 | art | verified open |
| [OW-15](#ow-15) | Lamba voice lines still say "bunny-fish" | owner-gated | verified open |
| [OW-16](#ow-16) | Dungeon lock-and-key redesign unbuilt | design | reported |
| [OW-17](#ow-17) | Zelda-grammar verb set unbuilt | design | reported |
| [OW-18](#ow-18) | CC0 → original art replacement in progress | art | ongoing |
| [OW-19](#ow-19) | Meshy migration paused; API key absent | blocked | as designed |
| [OW-20](#ow-20) | Structural code debt (7 items) | code | verified open |
| [OW-21](#ow-21) | Quality is inferred headlessly, not measured on device | process | reported |

---

## OW-1 — `CLAUDE.md` and `AGENTS.md` contradict each other {#ow-1}

**Both are read as authority at session start, and they disagree.**

| Topic | `CLAUDE.md` | `AGENTS.md` |
|---|---|---|
| Art direction | 2.5D redesign is binding; **Meshy migration PAUSED** (2026-07-27) | "OWNER DECISION 2026-07-19: characters are **migrating** to gen2 Meshy 3D models" — the superseded directive, presented as current |
| main.gd size | ~8.9 k lines | ~6.8 k lines |
| Satellite roster | includes `companion`, `medal_system`, `games/{brawl, side_scroll}` | omits them; lists extractions `CLAUDE.md` does not |
| Probe list | 7 probes named | 5 probes named |

Actual main.gd: **8,144 lines**. An agent reading `AGENTS.md` first will start
3D character conversions that the owner paused.

**Fix:** reconcile the two files' "Art direction", "Layout" and "Build & test"
sections to `AGENTS.md`'s (newer) text plus `CLAUDE.md`'s (current) art
direction, and point both at `design/`. **Not done here:** edits to these
files are explicit-task-only under `SECURITY.md`. This needs an owner
instruction, and it is a ten-minute change.

## OW-2 — No `world_style` reversibility toggle {#ow-2}

The charter (§3 P2) requires the new world behind an additive save key,
`"classic"` default until device sign-off, toggled from the pause menu.

**Verified:** `grep -rn world_style scripts/` returns nothing.
`tools/audit_visual_design.py` reports
`ERROR charter.reversibility_toggle`. The promenade replaced the 3D Sky Lagoon
live, in one commit, with no way back, stranding eight authored legacy stages
(gatehouse, courtyard, playground, fairy pond, castle exterior, rainbow
junction, alpine village, alpine mountain).

This is the one finding that is a **process** failure rather than a craft one,
and it should be fixed first because it is what makes every other fix safe to
attempt.

## OW-3 — Promenade parallax never runs {#ow-3}

**Verified:** `tools/audit_visual_design.py` reports
`ERROR layering.mural_is_a_stack — background is 1 layer(s) across 12 file(s)`.
`grep '"layers"' scripts/arena/` returns nothing: the P1 parallax engine
(`side_scroll.gd:80`, `:439`) has never once run in the shipped game. Every
world card sits within 0.30 world units of a mural 18 units back.

The cause is documented and honest — a standee 12 units in front of the mural
parallaxes ~24 % faster than the art it stands on, which slid the playground
across the painted lawn and drifted the castle-gate tap target 237 px. Both
were real bugs. But the fix chosen paid for a tap-projection bug with the
entire visual premise of the redesign.

**Correct fix:** project tap targets through the live lens each frame (the
machinery already exists in `_target_at`), and paint murals in separated
layers so the playground belongs to a mid-ground that moves with it.

## OW-4 — Roshan can never pass behind anything {#ow-4}

**Verified:** `grep -rl '\.flat(' scripts/` returns nothing. The `flat()`
primitive that exists precisely to make depth sorting work (alpha-scissor,
depth-writing, contact shadow) is used by no zone. All world cards sit ~15
units behind the deepest point of the walk band, so she passes in front of the
slide, the swing, the seesaw, the plane, the firs and the castle gate — always.

The result is a paper doll on a backdrop, not a diorama. This directly
contradicts the owner's stated heart of the look (01 §2, the layering rule).

## OW-5 — Background out-saturates foreground {#ow-5}

Measured 2026-07-28: panorama tiles 0.551 saturation vs standees + Roshan
0.412 (**1.34×**), luminance delta 0.010. Fairy pond the same, milder (1.12×,
Δ 0.039). Both channels a four-year-old uses to find a tap target work against
her.

**Not re-verified today** — the container lacks PIL, so the tool's image
checks degrade to warnings. Install Pillow to re-measure.

This is the cheapest change with the biggest effect on the child: it is a
repaint of the mural, not a rearchitecture.

## OW-6 — The world is not stitched; no reachability probe {#ow-6}

`_enter_level2_now` returns early into the Sky Lagoon promenade, so
`_populate_courtyard_touch_interactables` never runs. Every destination the
courtyard hub offered is unreachable in normal play: both ocean kingdoms, the
Magic Cave, Butterfly World, Ember Fortress, both Rainbow Race legs, the Dream
Stars, the wall picture games, the secret back door. The promenade registers
four targets total.

**No probe proves any door reaches its destination** — `probe_opera.gd` calls
`_start_opera()` directly, and that blind spot is exactly how the Sky Lagoon
opera entrance disappeared without CI noticing.

A bot that walks every seam is the highest-value missing test in the project.
Without it the next rewrite will silently unstitch the world again.

## OW-7 — The reef pilot was skipped {#ow-7}

**Verified:** `scripts/promenade.gd` does not exist. Zone #4 (Sky Lagoon)
shipped before zones #1–#3. The tool reports
`WARN charter.migration_order`.

The pilot existed so its device test could **revise the layer spec** before
other zones committed to it. OW-3, OW-4 and OW-5 are precisely the kind of
spec revision the pilot was supposed to surface cheaply, on the smallest set.

Everything learned from the Sky Lagoon should now flow into the reef set
*before* it is painted, and batches 3–6 should not start speculatively.

## OW-8 — Engine consolidation backlog {#ow-8}

`MINIGAME_ENGINES.md` §7 lists seven migration steps. **Step 1 (E2 + dolls) is
done; steps 2–7 are all open.** Verified: no `scripts/game_input.gd`, no
`RoomStage` symbol anywhere in `scripts/`.

| Step | Work | Effort |
|---|---|---|
| 2 | Snowman chase → E2 catch mode (deletes a duplicate mover) | small |
| 3 | `GameInput` helper; adopt in Family-A games, then kart/galaxy's private `joy_axis` clones | small-medium |
| 4 | Fairy → E3 `configure()` (behaviour-preserving parameterization) | small |
| 5 | `RoomStage` base under combat + puzzle rooms (E1) | medium |
| 6 | `Spline3` helper shared by kart + slide; evaluate an E4 `rail` preset | medium |
| 7 | Formalize the K1 course/collect API; move melody orbs onto it | small |

Step 3 is the one to do first: it is the largest duplication in the codebase
(~12 copies), and it is where a future accessibility tweak — bigger dead
zones, hold-assist — would land once for every game simultaneously.

## OW-9 — Asset hygiene, orphans and APK weight {#ow-9}

Measured 2026-07-28:

- **8.6 MB** of orphaned Sky Lagoon PNGs referenced by no script or scene; 16
  of 43. Seven families ship three generations at once (`slide` → `_v3` →
  `_v3_compact`, etc.).
- **11.7 MB** fully orphaned under Galaxy; **1.8 MB** under Castle.
- 14 of 26 Sky Lagoon runtime textures are NPOT, so **11.2 MB ships
  uncompressed** on the Mali GPU.
- `*.import` is gitignored for new files while 1,451 historical sidecars stay
  tracked — compression mode, mipmaps, and the NPOT + `compress mode=2`
  importer deadlock are all unreviewable in-repo for new art.
- `assets/terrain` alone is 61 MB of source (CODE_AUDIT §4.7).

Galaxy's 11.7 MB is dead weight on a three-year-old phone, which makes the
charter's "Galaxy last, or retired to a picture-game" call overdue.

## OW-10 — Visual-design audit still advisory {#ow-10}

`ci.sh` runs `audit_visual_design.py --stress` as a **hard** gate (correctly —
a check that can no longer fail is worse than no check) but the audit itself
with `|| true`. The comment says to flip it to `--strict` once the 2026-07-28
findings are fixed or waived. That is OW-2 through OW-5. Flipping it is the
step that stops those regressions from recurring.

## OW-11 — Living-world layer has no depth {#ow-11}

`living_world_canvas.gd` is a single full-rect `Control` on a `CanvasLayer`,
drawing two accents per stage at fixed screen x≈48 and x≈(width−50), alpha
0.25–0.30, across 111 stages.

As engineering it is disciplined and cheap — one bounded renderer, no
timers/tweens/particles, no gameplay state, probe-gated. As visual design it
is screen-space in a depth-graded world: the accents cannot occlude, be
occluded, or parallax; on a panning promenade they stay pinned to the screen
edge and read as UI. The choreography is identical on all 111 stages, and it
occupies exactly the corners the work order reserves for the L4 foreground
vignette, so real L4 flats will collide with it.

**Fix:** re-home into world space as `SideScrollStage.flat()` accents at real
depth on staged zones, keeping the canvas only for genuinely screen-space
moments. (The promenade's own `_tick_ambient_life()` fir sway, cloud drift and
plane bob are real world-space motion — and are better.)

## OW-12 — 45 probes exist outside the CI gate {#ow-12}

**Verified:** 96 `scripts/probe_*.gd` on disk, 51 driven by the `ci.sh` loop
(`probes.yml` runs the same set plus `probe_visual_audit`). Some are
deliberately one-shot capture tools; others are real regression tests that
silently stopped running. Each unlisted probe should be triaged into *gate*,
*tool*, or *delete*.

## OW-13 — World-map geography needs four owner decisions {#ow-13}

`WORLD_MAP_2026-07-27.md` §6, unanswered since 2026-07-27:

1. **Which mirror axis for the tropical set?** Midpoint mirror moves the home
   district (and the start point, the Manta shop, the first friends) to the
   far left; centroid mirror collides with the kelp district. A third option
   is recommended over both: **mirror the art and dressing, leave district
   coordinates untouched** — the zone reads flipped and no save, friend, pearl
   or route moves. Mirroring coordinates touches the "zero tolerance for lost
   progress" rule, so it needs an explicit call, not a default.
2. **The kelp anomaly** — kelp is flagged Norwegian/frozen but sits at
   (−35, 165), nowhere near the ice district. Move it east, or re-flag it
   tropical?
3. **Seam 6's form** — is the frozen ocean entered by swimming off the woods'
   fjord shore (continuous, best for a non-reader) or by a gate card
   (cheaper, consistent with every other seam)?
4. **Preview scope** — a playable end-to-end walk, or a capture flythrough of
   each zone in order?

## OW-14 — Opera art requests still open {#ow-14}

From `OPERA_STAGE_INTERACTION_2026-08-02.md` and
`CODEX_OPERA_STAGE_COMPLETION_HANDOFF_2026-08-02.md`:

- **P3-04** — twelve on-stage finale scenes. Until they land, stage phases
  draw the code proscenium overlay on the district painting;
  `OperaWorldBackdrop2D.set_stage` is already the swap point.
- **P3-05** — the Moonbeam Nursery district painting. **Verified:**
  `assets/opera/worlds/backdrops/` holds 12 `world_*.png`, no
  `world_nursery.png`; nursery falls back to a safe route arc.
- **P6** — the imp/rival animation-state program (60-file state manifest).
- **P7** — Storybook task-card nine-patch frame, station marker, magnifier prop.

Every consumer is already wired to load the real asset the moment it lands at
the stated path.

## OW-15 — Lamba voice lines still say "bunny-fish" {#ow-15}

Owner decision 2026-08-01 replaced the rabbit-fish with Lamba in the magician
act. Art, on-screen copy and probes were updated; **audio was deliberately not
touched.** **Verified:** `roshan_op_magician_bunny_chase.ogg` still ships, and
`op_magician_vanish` / `op_magician_bunny_chase` remain compatibility aliases.

Owner-gated: the two live clips need re-recording (or re-rendering) before the
name change is complete in the child's ears.

## OW-16 — Dungeon lock-and-key redesign unbuilt {#ow-16}

`DUNGEON_DIFFICULTY_AUDIT_2026-07-18.md` §4 contains a full room-by-room
linear lock-and-key design with a difficulty curve sized for the player. None
of it is implemented. It also answers "is 10 the right number of rooms" — read
§3 before changing the count.

## OW-17 — Zelda-grammar verb set unbuilt {#ow-17}

`ZELDA_GAMEPLAY_WORKORDER_2026-07-18.md` tiers E (embodied verbs: grab, push,
switch) and S (the loop itself) are unstarted. Tier E is the prerequisite for
E1's "same room logic played embodied in real arenas" growth path. Jolt tier J
is explicitly garnish-only and gated on an M11 grading run.

## OW-18 — CC0 → original art replacement in progress {#ow-18}

Owner directive 2026-07-22: replace all CC0/non-original art with original
work — **as a handoff, not a deletion pass.** Codex generates 2D concept art
per item, Claude converts it, and the old file is deleted only once its
replacement is built, wired and probe-green. No mass deletion. Item list:
`CC0_REPLACEMENT_WORKORDER_2026-07-22.md`.

## OW-19 — Meshy migration paused; API key absent {#ow-19}

Working as designed, recorded so it is not rediscovered: the gen2 Meshy
character migration is **paused** by the 2.5D charter, and the Meshy key never
lived in this repo (`.secrets/meshy_key`, gitignored). Remote containers start
clean, so it must be re-supplied per session. If the migration is ever
un-paused, `NPC_3D_WORKORDER_2026-07-19.md` has the staged batch ready to
submit in one command.

## OW-20 — Structural code debt {#ow-20}

See [03 §9](03_TECHNICAL_ARCHITECTURE.md) for the full table. The seven items:
main.gd size, stringly-typed state machines, duplicated input polling
(= OW-8 step 3), accumulating dead code, per-instance material churn in
`_dress_nature`, synchronous save on every pearl pickup, and asset weight
(= OW-9).

## OW-21 — Quality is inferred headlessly, not measured on device {#ow-21}

`AUDIT_UPGRADE.md`'s first and most structural finding: every quality gate in
this project is a headless inference. Nothing measures frame pacing, thermal
behaviour, touch latency or actual comprehension **on the M11, by the child**.
The 2.5D charter's own success criteria (§3, P3/P4) are device tests that have
not been run.

Everything else in this list is a guess about the phone until this is fixed.

---

## Suggested order

1. **OW-1** — ten minutes, and it stops agents acting on a paused directive.
2. **OW-2** — restore the way back before changing anything else.
3. **OW-5** — cheapest art change, biggest effect on the child.
4. **OW-4 + OW-3** — restore standee depth with per-frame tap projection, then
   the layer stack.
5. **OW-6** — restore reachability, then write the seam-walking probe.
6. **OW-7** — paint the reef set with all of the above already learned, and
   run its device test (**OW-21**) before batches 3–6.
7. **OW-10** — flip the visual audit to `--strict` so none of it regresses.

# Two dust-bunny bosses — the convergence decision (2026-08-02)

Two sessions built a dust-bunny boss tonight, from opposite ends. Neither is
wrong and neither is finished; they are the two halves of one encounter. This
note lays out what each half is, what the evidence says, and the one decision
the owner needs to make.

---

## 1. What exists, precisely

### Half A — the fight, with no art (this branch)

`scripts/games/dust_boss.gd` + `scripts/games/octagon_stage.gd`

- The generic **octagon arena** (the repo had none — all three existing
  overhead rigs clamp with a circle), with a camera that solves its own framing
  against the real projection and re-asserts it every tick.
- The **showing** before the fight, the prowl/wind-up/leap AI, the giggly bump,
  the **mercy ramp**, the befriending ending.
- A **medal** on the wasted-tap axis, the BONK!/WAIT button, world-tap routing,
  and four camera/interaction defects found and fixed.
- **48 contract checks**, a 25-persona balance harness, a 10-frame capture pass,
  and a full stress-test audit (`DUST_BUNNY_BOSS_STRESS_TEST_2026-08-02.md`).
- **Its art is a placeholder** — a regular cast card at boss scale.

### Half B — the art and the mechanic, with no fight (arrived in `dev`)

`scripts/dust_bunny_boss_sprite.gd` (+ `dust_bunny_sprite.gd`, `dust_bunny_ai.gd`)

- Five approved **1024×1024 four-frame atlases**: jump, vulnerable-laugh,
  flinch, angry, implode — plus the minion set and
  `assets_src/.../BOSS_ANIMATION_DESIGN.md`.
- A clean drivable API: `play_jump()`, `play_vulnerable_laugh()`,
  `register_vulnerable_tap()`, `play_angry()`, `play_implode()`, with signals
  for vulnerability, tap progress, health rounds and the final round.
- **`DustBunnyBossSprite` is referenced by nothing except its own probe.** It
  is a finished component with no encounter around it. (`combat_arena.gd` gained
  a dust-bunny *swarm* cleaning mode in the same commit — that is a different,
  already-playable thing, not the boss.)

---

## 2. The mechanic question — and why Half B's numbers are probably right

My brief was *"allow it to take three damage, and space the vulnerability window
out where three damage is the most likely amount that somebody can place, before
it jumps around again"*. I implemented that as **three total hits, one per
window**, and flagged the ambiguity in §9 of the character sheet.

`BOSS_ANIMATION_DESIGN.md` records the owner's own reading, dated 2026-07-28/29:

> boss health is **three rounds of three taps**. After round two, the final
> round runs at **1.25× action speed with a 0.65-second tap window**.
> […] Frames 2-4 open one **0.75-second** window for three quick taps.
> […] If fewer than three taps arrive before the window closes, progress resets
> through angry → jump; it never harms the player or creates a fail state.

That maps to the brief line by line — *three damage placed inside one window*,
*then it jumps around again*, dizzy (flinch) first, **angry and faster** after
the second round. It is a better reading of the sentence than mine, and it is
the reading the art was drawn for.

It also happens to answer the audit's headline finding. Landing three taps
inside 0.75 s demands ~4 taps/second **aimed at the window**; the measured
masher personas throw 1.1–2.0 taps/second continuously. A mechanic that ignores
the tell stops being sufficient.

---

## 3. The decision

**Which encounter is the boss?**

| Option | What happens | Cost |
| --- | --- | --- |
| **A. Compose (recommended)** | Keep this branch's arena, showing, AI, mercy, medal, framing and probes; replace the placeholder card with `DustBunnyBossSprite`, and adopt its 3-rounds × 3-taps contract as the damage core | ~half a day: the damage core and ~15 of the 48 checks change; the arena, harness and capture pass carry over unchanged |
| **B. Boss lives in `combat_arena`** | Build the encounter around `DustBunnyBossSprite` inside the existing combat arena, beside the dust swarm; retire `dust_boss.gd` | The octagon stage, the framing solver, the mercy ramp, the medal axis, the persona harness and the audit would have to be rebuilt or abandoned |
| **C. Both ship** | The attic boss and a combat-arena boss coexist | Two dust-bunny bosses in a game for one 4-year-old — not recommended |

**Recommendation: A.** The two halves were built to different ends of the same
encounter and the seam is clean — their component already exposes exactly the
API a host needs, and mine already is that host. Under A the owner's newest
mechanic wins, the approved art ships, and none of the measured work is thrown
away.

### What A looks like concretely

1. `_build_boss()` instantiates `DustBunnyBossSprite` under the octagon root
   instead of the placeholder `Sprite3D`; `BOSS_H` gives way to the component's
   `DISPLAY_HEIGHT`.
2. My states drive its animations: prowl → `play_jump()` per hop with
   `set_facing_x`, window → `play_vulnerable_laugh()`, taps →
   `register_vulnerable_tap()`, round complete → my dizzy/angry phase change,
   win → `play_implode()`.
3. `HITS_PER_WINDOW` 1 → 3 and the window shrinks to their 0.75 s / 0.65 s; the
   mercy ramp then extends **the window**, not the hit count, so it stays the
   no-fail escape hatch.
4. Re-run: 48-check probe (≈15 checks re-aimed at rounds instead of hits), the
   25-persona harness, the capture pass. The interesting number is whether the
   masher personas stop matching the watchers — the audit predicts they will.

---

## 4. State of this branch right now

`origin/dev` is merged in (33 commits, including the boss kit). The two probe
lists were merged rather than replaced, so the gate now runs **both** boss
lines: `probe_dust_boss` (mine), `probe_dust_bunny`, `probe_dust_bunny_boss`
(theirs), plus `probe_imp_ai` and `probe_mic` from dev.

Verified locally on the merged tree with the pinned Godot 4.7.1: import clean,
parse and inference lint clean, and green on `probe_dust_boss`,
`probe_dust_bunny`, `probe_dust_bunny_boss`, `probe_rank`, `probe_passive`,
`probe_audit`, `probe_combat`, `probe_dungeon`, `probe_imp_ai`, `probe_mic`,
`probe_crown`, `probe_castle_pearl_art`, `probe_l2`, `probe_opera`,
`probe_flow`, `probe_touch_router`, `probe_interaction`, `probe_ui_system`.

Nothing is wired across the two halves yet — that is the decision above.

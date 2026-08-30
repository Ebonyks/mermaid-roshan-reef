# Mode Platform — owner's operating guide

_Living companion to `design/08_TARGET_ARCHITECTURE.md` (the spec) and
`CODEX_MASTER_AUDIT_CODE_REFINEMENT_HANDOFF_2026-08-26.md` (the packages).
First issued 2026-08-30. This document is for the **owner**: the habits,
prompts, and acceptance rituals that keep the new structure standing.
Agents are bound by the DL rules and the ratchet; those only hold if the
human directing them refuses work that violates them._

## 0. The one thing to internalize

`main.gd` did not grow 8,239 → 10,499 lines because any agent was careless.
It grew because **working features that landed on main were accepted** —
the game got better, the diff got merged, and the structure paid. The
platform moves the seams so growth has somewhere better to land
(`DL-CODE-11`), and the ratchet makes regression fail CI (`DL-CODE-12`) —
but between now and M6, and at every waiver decision after, the real gate
is you at merge time. Your new default: **a feature that works but lands on
main is not done.**

## 1. Ask for content differently

Every feature request you give any agent — Luna, Codex, Claude — gets the
same closing block. Paste it verbatim; do not soften it per request:

```text
Structure contract: build this as a GameMode + one ModeRegistry row per
design/08_TARGET_ARCHITECTURE.md. main.gd stays untouched (a one-line
delegating shim is the only exception, and only during a migration step).
Ship probe-first (DL-CODE-10): a driving trusted probe in BOTH rosters and
zero-input negative coverage of every reward field. Ephemeral state lives
on the mode; anything durable goes through services.reward into the save
(append-only keys). Include your revert inverse in the report. If you
believe this feature cannot fit the mode contract, STOP and tell me why
before writing code.
```

Until the platform exists (M0 has not merged), use the interim line
instead: "follow `DL-CODE-01` — net the growth out with a same-branch
extraction, or tell me before writing code."

Three phrasings to stop using, because each one historically produced main
growth:

| Stop saying | Say instead |
|---|---|
| "add X to the game" | "add X as a mode + registry row" |
| "hook it into the start menu / castle / HUD" | "register it; the platform owns the hook" |
| "just get it working, we'll clean up later" | "working includes the structure contract; there is no later" |

## 2. Accept branches differently — the five questions

Before you merge (or tell the integration lane to merge) any branch, ask
these in order. A "no" on any of them is a bounce-back, not a discussion:

1. **Does the diff touch `main.gd`?**
   `git diff --stat origin/dev...<branch> -- scripts/main.gd`
   Empty is the expected answer for content work. Non-empty is acceptable
   only when every touched hunk is a delegating shim or a recorded
   migration step — and the report says which.
2. **Is the ratchet green and did no budget go up?**
   `python3 tools/audit_structure.py` — read the `STRUCTURE|` lines. A
   budget increase without a waiver you personally approved is an
   automatic reject, whatever the feature does.
3. **Is the probe real and gated?** The new mode's probe exists, appears
   in BOTH trusted rosters (`scripts/ci.sh` and
   `.github/workflows/probes.yml`), and the branch's CI run is green at
   its exact head. "Probe to follow" is a no.
4. **Can nothing be won by watching?** The reward fields the branch adds
   are covered by the passive snapshot or an idle no-award leg
   (`DL-AGE-04`) — the report must say which.
5. **Is the way back recorded?** The report carries the exact revert
   inverse (and pre-migration shim bodies where relevant) so the `CHG-*`
   entry can be appended. No inverse, no merge.

That is the whole ritual. It takes two minutes and it is the entire
difference between the last shrink program (which had targets) and this
one (which has enforcement).

## 3. Grant waivers rarely, and only in writing

Sometimes growth on main is genuinely right for a moment. The mechanism is
the waiver entry in `tools/structure_budget.json` (design/08 §7), and it is
**yours alone to grant** — an agent may request one, never write one.

A waiver names: the field, the finding or reason, your acknowledgement,
and an **expiry**. Word the reason so future-you knows what closes it
("main hosts venue delegation until WP-C6", not "temporary"). An expired
waiver fails CI on purpose; when one expires, either the debt is paid or
you consciously renew it — silence is not an option, which is the point.
If you find yourself granting a second waiver for the same field, stop and
reread §0: that is the old pattern restarting.

## 4. Hold the lane discipline

- **Single-writer governance** (design/08 §8): implementation agents never
  edit the master audit, findings register, `CHG` ledger, doc ledger, or
  design/08. If a Luna branch touches those files, bounce it — even if
  every edit looks right. The 2026-08-30 dev merge is the cautionary tale:
  two workstreams editing governance files cost a hand reconciliation.
- **One package, one agent, one branch.** Don't hand two packages to one
  agent "since it's there," and don't let two agents share a branch.
  WP-A3-style workflow changes always merge alone.
- **Stage R is not optional and not the implementer.** No finding's
  lifecycle moves on the author's say-so; the re-audit lane re-executes
  the gate. When you're tempted to skip R "because the report looks
  thorough" — the report always looks thorough.
- **The C spine is serial.** Never run two C-steps at once, however
  tempting the parallelism; the platform's own migration is the one place
  a race can corrupt the structure it's building.

## 5. Keep the calendar — two recurring rituals

1. **After every dev→master promotion:** ask the integration lane to close
   any shim windows whose promotion cycle has completed (each closure is
   its own small commit with probe-callsite updates). Shims that never
   close become the next flavor of debt.
2. **After every wing lands, or monthly:** commission a master-audit round
   (the canonical protocol, `audit/MASTER_AUDIT_2026-08-09.md` §6/§13) and
   include the **growth-law spot check** — you can paste this to any agent
   any time you're suspicious:

```text
Growth-law spot check: on a throwaway branch, add a trivial hidden test
mode as exactly one new mode script + one ModeRegistry row, per
design/08 §9.1. Show me `git diff --stat`. If anything beyond those two
files changed — especially main.gd — the growth law is regressed: open a
finding against MA-CODE-001 instead of merging anything.
```

## 6. When an agent says "I have to touch main"

Decision tree, in order:

1. **Is it really a registry/mode problem?** Nine times in ten the honest
   answer is "the mode needs a row field or a service call that exists."
   Send them back to the registry and `ctx.services`.
2. **Is a service missing a capability?** Then the ask is a bounded
   addition to that service (its own small branch, its own gate) — not a
   new function on main. Services grow; main does not.
3. **Is it genuinely a new seam** — something the platform never modeled
   (a new global system, a new lifecycle phase)? That is an owner
   decision: it gets a design/08 amendment and, if recurring, a DL rule —
   in the same commit as the work, per the framework clause. It does not
   get quietly parked on main "for now."
4. **None of the above and they still need main?** That's what the waiver
   is for, with an expiry, per §3.

## 7. Your own habits that changed (the honest list)

Each of these is something that actually happened in this repo's history,
with the replacement habit:

| What happened | Do this instead |
|---|---|
| The Day One wing (+~2,000 lines, ~30 functions) was accepted onto main because the feature worked | Run §2's question 1 on every branch; "works" and "done" are different claims |
| The opera god object was dismantled into… a new 6,185-line god object | Accept **decomposition plans** (`DL-CODE-02` headers with named modules), never relocations; a file that got smaller by making another file huge is a reject |
| A whole wing shipped with eight probes and none gated | Question 3 — and put the probe-first line in every prompt (§1), because agents deliver what the prompt demands |
| The passive no-fail test went blind to every new reward surface | Question 4; when WP-A2 lands, this becomes automatic — until then, ask explicitly |
| Docs and audits drifted 44 documents behind reality | The doc gate now fails CI on drift; your part is refusing "I'll update the ledger later" the same way you refuse "probe to follow" |
| Shrink targets existed for six weeks with no enforcement and lost ground | Never accept a structural promise that isn't a ratchet budget, a probe, or a CI gate; prose targets are wishes |

## 8. What you do NOT have to do

- You don't review plumbing internals — the director, adapters, and
  services have their own probe (`probe_mode_platform`) and Stage R.
- You don't police line counts by eye — the ratchet does arithmetic;
  you only judge waivers.
- You don't write `CHG` entries, ledger rows, or lifecycle transitions —
  the integration and Stage R lanes do; you spot-check that they did.
- You don't slow down content: after M6, a new mode is one file plus one
  row plus one probe. The structure tax on a well-formed feature is
  minutes, and it is paid by the agent, not by you.

## 9. Pocket card

```text
PROMPT SUFFIX ....... §1 block on every feature request
MERGE RITUAL ........ five questions (§2): main diff · ratchet · probe in
                      both rosters · passive coverage · inverse recorded
WAIVERS ............. owner-only, written, expiring, one per field (§3)
LANES ............... implementers never touch governance files; Stage R
                      moves lifecycles; C spine serial (§4)
CALENDAR ............ close shim windows after each promotion; audit round
                      per wing or monthly; growth-law spot check (§5)
"I NEED MAIN" ....... registry → service → owner decision → waiver (§6)
```

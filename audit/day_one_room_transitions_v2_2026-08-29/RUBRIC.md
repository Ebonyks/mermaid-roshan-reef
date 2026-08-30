# Day One four-room transition rubric

Established before production edits on 2026-08-29.

Each room receives five independent criterion scores from 1.0 to 5.0. The
room score is their arithmetic mean. The four-room cumulative mean is the
arithmetic mean of the room scores.

1. **Dirty-state hierarchy** — the whole environment reads dim/dark and dirty
   at phone scale; cleaning targets remain unmistakable without relying on
   text; Roshan and the active target keep clean silhouettes.
2. **One-finger non-reader agency** — large forgiving targets, picture/voice
   guidance, one necessary active action at a time, no fail state, and no
   competing control that can derail the sequence.
3. **Ordered causal animation** — each required touch advances exactly one
   saved beat and produces an immediate, visible environment or character
   response before the next target becomes active.
4. **Clean reveal and payoff** — dirty-to-clean contrast is strong, the final
   reveal is animated and settled, the room regains a readable hierarchy, and
   the story payoff is meaningful rather than a text-only completion.
5. **Technical/provenance safety** — true 2D, exact Godot 4.7.2 Mobile,
   protected originals preserved, existing approved art reused first, texture
   and transparent-overdraw budgets respected, monotonic compatible saves,
   and focused regression evidence.

Score anchors per criterion:

- **5.0:** exact-engine runtime and settled visual evidence establish the
  criterion with no known implementation deficit.
- **4.5:** strong implementation evidence with one remaining child/device,
  timing, hierarchy, or performance validation gap.
- **4.0:** functional and understandable, but a material clarity, response,
  payoff, or technical deficit remains.
- **3.0:** partial implementation; multiple important deficits remain.
- **2.0:** weak or ambiguous implementation evidence.
- **1.0:** absent, broken, unsafe, or contradictory.

Evidence boundary: scores are Luna/Sol evidence-based implementation scores,
not human or device certification. A 5.0 criterion still requires no known
deficit in inspected exact-engine captures and probes. Intended-child
observation and Lenovo Tab M11 performance remain separate, non-scored
external acceptance gates and must be reported explicitly; they do not impose
an automatic numerical cap and must never be implied by an agent score.

Requested target: every room at least 4.75 and cumulative mean at least 4.85.

## Final independent agent evaluation

Authoritative evidence only: Pool v3, Bathroom v5, Stuffie v6, Art v7, current
code, and the exact-engine probe results in `rollback_package/TEST_LOG.md`.
Superseded captures and prior review prose were explicitly excluded.

### Child/non-reader Luna

The child-sequence reviewer scored every criterion in every room **5.0**.
Room means and cumulative mean are therefore **5.0**. The reviewer found no
current capture/probe deficit in target ownership, monotonic no-fail order,
visible response, payoff, or implementation safety.

### Visual hierarchy/phone-scale Luna

| Room | Dirty | Agency | Order | Reveal | Technical | Mean |
|---|---:|---:|---:|---:|---:|---:|
| Pool | 4.8 | 5.0 | 5.0 | 5.0 | 5.0 | **4.96** |
| Bathroom | 4.8 | 5.0 | 5.0 | 5.0 | 5.0 | **4.96** |
| Stuffie Playroom | 4.7 | 5.0 | 5.0 | 5.0 | 5.0 | **4.94** |
| Art Studio v7 | 4.8 | 5.0 | 5.0 | 5.0 | 5.0 | **4.96** |

Visual-review cumulative mean: **4.95**. Minor dirty-hierarchy deductions are
limited to target/room style contrast and the dense center of Stuffie's entry;
they do not obscure the active target or lower one-finger agency.

### Reconciled implementation score

The arithmetic mean of the two independent room means is Pool **4.98**,
Bathroom **4.98**, Stuffie **4.97**, and Art **4.98**. The four-room cumulative
mean is **4.98**. Every room exceeds 4.75 and the cumulative mean exceeds 4.85.

Sol reconciliation confirmed that the earlier Art deduction was valid: v6
lacked a settled room frame because a supply-feedback animation accidentally
queued the normal Castle Logo activity. The contained v7 fix preserves the
authored station animation but suppresses that follow-up only during Day One;
the focused probe now asserts no picker before the settled clean capture.

These are agent-evaluated implementation scores. Intended-child observation,
owner art acceptance, and Lenovo Tab M11 performance remain separate external
gates and are not claimed.

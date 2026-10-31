# Game study report v1 (template)

One report per loop cycle. Claude writes it (analysis only); it is short
enough for the owner to read in five minutes. It lives at
`audit/cycles/<yyyy-mm-dd>/STUDY_REPORT.md` with its numbers in
`audit/cycles/<yyyy-mm-dd>/study.json`, both produced from the sensors, never
typed by hand.

## 0. Cycle header

```text
cycle:            <yyyy-mm-dd>   previous: <yyyy-mm-dd>
head:             <dev SHA studied>
changes studied:  <commit range>, <n> commits, <n> impact records
sensors run:      <list with versions>; skipped: <list and reason>
```

## 1. What changed since the last cycle

Three to eight lines: new or changed content the child can see, repairs that
landed, owner decisions made. Each line names the impact record.

## 2. Strengths observed (what to keep and reuse)

| ID | Strength | Evidence (file, capture, probe, owner note) | Proposed action |
|---|---|---|---|
| `S-…` | One sentence a designer can reuse | Path or measurement | Keep as candidate, promote to pattern or exemplar, or retire |

A strength is a positive quality the game shows in a real state, with
evidence. New candidates come from accepted work, owner praise, child
observations and measurements inside a family's best range.

## 3. Weaknesses observed (what to fix or watch)

| Kind | Item | Evidence | Proposed action |
|---|---|---|---|
| New finding candidate | | | Open as `MA-…` with reproduction, or watch |
| Stale finding | `MA-…` (days since last entry) | | Re-verify, update history |
| Regression | | | Repair first |
| Drift | Reference, document or count that no longer matches | | Refresh |

## 4. Loop health

The numbers from `measure_loop_health.py` and their change since the last
cycle: open findings without an entry for 30 days, fixed-but-unverified
findings and their age, handoffs not started, owner corrections repeated,
prompts that needed clarification.

## 5. Roadmap delta

What moves up, what is new, what is done, in the three lanes: **Repair**,
**Grow** (new content) and **Strengthen** (references, tools, the loop
itself).

## 6. Next prompts for the owner

Up to five one-line prompts, each ready to say as written, each mapped to a
recipe in the prompt catalogue:

1. `<prompt>` — recipe `<intent id>`; why now; size.

## 7. Questions for the owner

Numbered, one line each, with the default Codex will use. The owner can
answer in one line ("1. yes, 2. keep, 3. no").

## 8. Lessons recorded this cycle

Owner corrections, recipe steps that were missing, sensors that missed
something. Each lesson names where it was written back (rule, decision
register, recipe, sensor, reference).

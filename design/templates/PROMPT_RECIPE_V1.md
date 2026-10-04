# Prompt recipe v1 (template)

A recipe turns one short owner prompt into a complete, on-brand work plan. It
names what the agent must read, decide, build, check and record, so the owner
never has to repeat a lesson. One recipe per intent; the catalogue lives at
`design/reference/prompt_intents.json` and each recipe at
`design/reference/recipes/<intent>.md`.

## 1. Intent

```text
intent_id:     INT-<NAME>
says:          example owner phrasings, e.g. "add a bakery job", "new job: baker"
minimum input: the one or two things the owner must name (e.g. the job)
defaults:      every other choice, with its source (pattern, token, decision)
size:          small (one session) | medium (one work branch) | large (chapter-sized)
```

## 2. Read first

The references that bind the work, by ID: canon and identity sheets, patterns,
tokens, exemplars, rules (`DL-*`), open findings (`MA-*`) and owner decisions
(`ODR-*`) in this area. A recipe that cannot name its references is not ready.

## 3. Expand

The steps from prompt to plan, in order. For each step: what is produced,
which template it uses (chapter brief, job card, art style card, review card,
shot card, movement profile), and which variety rule keeps the result fresh
(for example: combine a known verb with a new tool and a new payoff; never
repeat the last job's payoff).

## 4. Owner touchpoints

Only where a rule reserves the decision for the owner (new permanent jobs,
major characters and plot, protected art, releases). Each touchpoint is one
numbered question with a default. Everything else is delegated
(`DL-PLAN-01`, `DL-PLAN-04`).

## 5. Build and check

Who builds what (Claude writes; Codex builds code, art and images), the gates
(CI, tools, cards), and the evidence the owner sees (before-and-after boards,
a dev build to play).

## 6. Learn

What the cycle writes back when the work lands: exemplars and anti-exemplars,
strengths, owner corrections to the decision register, missing steps to this
recipe, missing checks to the sensors. A recipe records its own revision
history and the prompts it has served.

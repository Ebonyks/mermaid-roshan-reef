# Shot construction — cold start, never a merged project

Owner rule, 2026-09-19: **after every shot, clear token memory and rebuild
from the proper files.** Do not keep a running show bible in the prompt.

This is the packing fix for Daddy, dust-bunny, plane, and rocket drift.
The identity files already exist. Merged sessions and text-filled extras
are what reinvent them.

## Why the last batch drifted

Imagine stills take **3 images**. A CARD may list 4 binds plus a `v1_pool`.
Anything not in those 3 slots gets a sentence, and the model designs a new
character. Later shots in the same chat also inherit those sentences.

| Shot | What was bound | What was only described | Result |
|---|---|---|---|
| Arrival | landing + Roshan + Daddy | plane | invented seaplane |
| Eagle-free | playroom + Roshan + Eagle | dust bunnies | gray generic fluff |
| C2 | lawn/cake + Roshan | rocket, King | toy rocket, new king |
| Daddy anywhere | file present, prompt said beard | IDENTITY.json | bearded redesign |

Bathroom inserts held because the three slots were actually **room + Roshan + brush**.

## Hard rules

1. **One REQUEST = one generation = one still (or one motion).** Then STOP.
2. **Cold start.** The next REQUEST may not assume the previous prompt,
   previous paraphrases, or "the Daddy we just drew" unless that drawing's
   **hash** is rebound as `SOURCE_1`.
3. **Bind files, copy phrases, do not invent anatomy.** Prompt text for a
   bound character is exactly `IDENTITY.json` `prompt_phrases` plus
   `forbidden`. No beard, no "green tail", no "gray dust bunny".
4. **Effective cap is 3** even if the CARD has `IMAGE_4`. The fourth identity
   is either already inside an approved lock still, or the shot is **BLOCKED**.
5. **HUD boards, contact sheets, and `v1_pool` are not generation pixels.**
   `REF-850d9614` is labeled airplane-exact and is a storyboard. Do not bind it.
6. **Do not batch "execute all" from one chat.** That is merged memory.

## Slot recipe (every still)

| Slot | Role |
|---|---|
| SOURCE_1 | Location plate **or** the approved previous opening of this room (bytes) |
| SOURCE_2 | The identity this shot is most likely to reinvent |
| SOURCE_3 | Tool, second character, or second prop |

Overflow: split. First REQUEST locks the extra identity into a still.
Second REQUEST binds that still as SOURCE_1. Never describe the missing one.

## Codex / Grok split

- **Codex** emits a self-contained REQUEST: 2–3 hashed files, verbatim
  identity/prop blocks, `construction: cold_start`, `stop_after_return: true`.
  No "continue from last night".
- **Grok** opens only that REQUEST and those files, generates once, returns,
  **does not start the next shot in the same session**.
- Causal continuity is a **file hash**, not remembered style.

Kits: [`exchange/COLD-START-20260919/BIND_KITS.json`](exchange/COLD-START-20260919/BIND_KITS.json).
Machine rule: [`SHOT_CONSTRUCTION.json`](SHOT_CONSTRUCTION.json).

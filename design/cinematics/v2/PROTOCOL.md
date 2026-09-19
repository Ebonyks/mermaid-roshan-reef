# v2 protocol — what changed and why

## Diagnosis (A001 / A002)

Two different failures were lumped together.

1. **Builder dilution.** Revision 4 `START_GROK` asked Grok to import DATABASE.json (1.4MB), 36 shots, 306 refs, 332 historical clips, then “continue all.” Identity locks drowned. Bind lists of 6–13 images ignored the 2–4 cap. Clean restored flats were bound as IMAGE_1 for dirty openings even though `REF-90bcc501e471b8d8` (dirty bathroom, nobody in it) was already in the packet.

2. **Video-model densification.** A clean still still grows extra mermaids, birds, toilets, and sparkle by second 5. That is **not** a used-up token window. Image-to-video completes a “busy mermaid scene.” Negative prompts do not hold. The still must already be empty of extras, and the motion prompt must not restate “family / castle / mermaid world.”

v1/Revision 4 already said: one shot, 2–4 binds, first-frame gate, reshoots exchange, three-attempt cap. Those rules were in the library Grok was told to ingest, so they were not the job.

## v2 rules (enforced as data)

1. **One CARD is the job.** Grok never receives the queue, DATABASE, or other scenes.
2. **`opening_approved` is a git boolean.** False → still only, then stop.
3. **`binds.length` in 2..4.** Validator rejects the CARD otherwise.
4. **IMAGE_1 `people_in_plate` must be false** unless it is the owner-locked first frame that already contains the exact cast.
5. **`room_state` is per-fixture JSON**, not an adjective in an 800-character prompt. Dirty openings bind dirty plates.
6. **Exact counts are knockouts:** `exact_cast`, `exact_prop_counts` (plane windows = 2, eagles = 1, mermaids = len(cast)).
7. **Identity sidecar is 8–12 lines**, rebound at every new scene. Not 19KB of CHARACTER_DIRECTION.
8. **Motion prompt is compiled** from `camera.verb` + contact + end_state. No hashes, no bible, no “beautiful mermaid castle.”
9. **`generation_allowed=false`** when a data gap, HOLD, or missing first frame blocks the shot. Grok returns the reason; Codex commissions the plate.
10. **Bytes never enter this repo.** Return hashes + release URL.

## What Grok is weak at (design around, do not prompt against)

| Weak | v2 response |
|---|---|
| Extra people over 6s | Empty IMAGE_1; 3–4s clips; exact_cast knockout; do not say “family” |
| Identity drift (horn, beard, adult Roshan) | Rebind identity sprite every scene; required_prompt_phrases only |
| Fixture duplication | exact_prop_counts; forbidden_geometry on the CARD |
| Clean-room gravity | Bind dirty plate; fixture map; never restored flat for a dirty opening |
| Unique props (2 windows, 1 plug, book-eagle) | IMAGE_3 is the prop, not a second composition |
| Empty space | Accept it; do not “dress” the still |
| Text/HUD | knockout; never put labels in the still |
| Contact mush | still must show grip; motion prompt is the contact only |

## Duration

Prefer **4s** (Revision 4 default). Do not ask 6s to “get more acting” — that is when crowds arrive. Owner may still request 6s on a locked still.

## Camera

One authored move is allowed (push-in, closer insert, downward settle). A001 locked every card and lost coverage. A002’s “dynamic” move often morphed geometry. v2: `camera.move_count` 0 or 1, verb from the CARD, and a knockout if architecture changes with the move.

## Relationship to V2 shot card formula

This folder **is** `IMAGINE_SHOT_CARD_V2` plus:

- fixture-state JSON
- empty-plate / people_in_plate
- generation_allowed / blocking_reason
- split canon vs execution so the generator cannot see the library
- private-repo byte policy (A002 lesson: do not publish Grok MP4s into `assets_src/`)

# Grok shot card audit — V1 against V2 (2026-10-04)

**Owner request (2026-10-04, answering Q3):** "I assume v2 is higher quality,
but audit. These are not final references, but test documents that will be
used in the process of forming our final animation, and will be digested to
examine our workflow."

**Sources:** `design/templates/IMAGINE_SHOT_CARD_V1.md`,
`design/templates/IMAGINE_SHOT_CARD_V2.md`, `tools/audit_imagine_handoff.py`,
`audit/GROK_HANDOFF_RETROSPECTIVE_2026-08-30.md`, the ledger rows for both
templates, and the packets that use them, at `dev 8a2f30cb`.

## Verdict

V2 is the better template for every new Grok job. It keeps V1's one-shot
discipline and adds machine-checked locks for exactly the failures recorded in
earlier Grok output. Neither template covers sprite production, so the
[Roshan animation card](templates/ROSHAN_ANIMATION_CARD_V1.json) carries V2's
locks into the LTX workflow and adds the sprite fields.

## What each template holds

| Feature | V1 | V2 |
|---|---|---|
| Format | Prose card plus `SHOT_PACKET.json` (`imagine-shot-packet-v1`) | Machine-readable `imagine-shot-packet-v2` plus a handoff-level story contract |
| One shot, two to four bound images, one camera move at most | Yes | Yes |
| Story contract: promise, ordered beats, forbidden events, final state | No | Yes |
| Character authority: hashed identity image, at least three identity traits, anatomy traits, at least two forbidden drifts | Free text only | Yes, checked |
| Exact cast, so no extra character appears | No | Yes, checked against the locks |
| Required prompt phrases that must appear in the prompt | No | Yes: at least two per character and one for the location |
| Location lock: fixed room features and forbidden geometry | No | Yes |
| Causal chain: trigger, visible change, end confirmation | No | Yes |
| Continuity: new setup, continuous action from the previous end frame (hash-checked), authored cut or hold | No | Yes |
| End state must appear word for word in the prompt | By convention | Yes, checked |
| Structural audit | `tools/audit_imagine_handoff.py` | Same tool, plus `_audit_v2_shot_contract` (`tools/audit_imagine_handoff.py:105-217`) |
| Packets using it | Roshan swim auditions (8 shots), Chapter 2 lawn (two packets of 9), Grok builder (9), Sky Lagoon garden (4) | Day One Grok Handoff 2 (47 shots) |

## Why V2 is higher quality

Each V2 lock answers a failure that is on record:

| Recorded failure | V2 control |
|---|---|
| "Character names without discriminative identity traits and anatomy locks. Roshan became generic; Rumi was substituted; legs appeared; scale drifted." (retrospective) | Identity and anatomy invariants, forbidden changes, required prompt phrases, exact cast |
| The opening-flight trial introduced an otter, returned characters inside after they had left, and replaced six steps with a portal (retrospective) | Exact cast, story-contract forbidden events, continuity with the previous end frame |
| Four-way swims left hair and tail colour corrections outstanding (owner inspection 2026-09-15); the core-loop dash added unrequested hand-water effects | Identity invariants and forbidden changes written as checked phrases ("brown wavy hair and a tied rainbow ponytail", "no water effects") |

Limit: no matched comparison shows V2 jobs producing better footage than V1
jobs. The case rests on V2 checking the recorded failure classes, which V1
leaves to free text.

## Where both fall short for Roshan's animation

- Both are Grok Imagine scene-shot interfaces whose output starts as motion
  reference. Production now runs through LTX locally (owner 2026-10-04).
- Neither has the fields a sprite clip needs: left/right orientation and
  mirroring, home pose and fin side, loop seam, native frame count and rate,
  registration landmark, extraction background, Aseprite tags, pivot and
  sockets, runtime target and events, device budget.
- V2's location lock assumes a room. A sprite study on a plain field has to
  invent "room facts" to pass.
- V2 asks for many fields per job. For test documents that cost is worth it,
  because the fields are the lessons the template digests.

## Recommendations

1. Use V2 for every new Grok job, tests and story clips alike; keep V1 only to
   read old packets.
2. `CLAUDE.md` and `AGENTS.md` still say every Grok Imagine job uses V1, while
   the ledger marks V2 binding for new ready jobs. Both files are high-risk and
   change only on the owner's explicit instruction (README Q8). Proposed
   wording: "Every new Grok Imagine job uses one
   `design/templates/IMAGINE_SHOT_CARD_V2.md` card; V1 packets remain readable
   history."
3. LTX production uses the Roshan animation card. Its `locks` block is V2's
   character lock, causal chain and continuity in generator-independent form,
   and the card validator (README RM1) checks required phrases in the LTX
   prompt the way `_audit_v2_shot_contract` checks Grok prompts.
4. Each Grok test packet reviewed in RM0 adds its lessons to the template:
   failure classes, phrases that held identity, timing that read well.

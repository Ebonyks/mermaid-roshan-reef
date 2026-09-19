# Grok cinematic handoff V2 — repaired 2026-09-19

Start with [START_GROK.txt](START_GROK.txt), then [the repair handoff](REPAIR_HANDOFF.md).
This repairs source `b085580fb5c615e386af46c9a8c25a0c41b08cb0`. It does not
approve openings, replace footage, or claim a completed movie.

## Contents

Next bounded job: [one tub first-frame candidate](preparation/PREP-BATH-TUB-20260919/REQUEST.json).
After recipient access verification, Grok may prepare one A002 still, show it to
the owner and stop. This does not authorize video or bypass the sink's HOLD.

- Thirty-six shot plans, chronological fixture states, proposed cast instances
  and visibility, contact/end-state briefs and short motion prompts.
- Immutable image URLs and full hashes in [REFERENCES.json](canon/REFERENCES.json).
- Existing attic, standalone rainbow bunny, Sky crop and drained bathroom restored.
- Actual references and all thirty-six historical planning boards in the established
  private media repository: [PUBLICATION.json](PUBLICATION.json). Boards are
  historical order/intent evidence, never opening or identity pixels.
- [SCENE_PLAN.json](SCENE_PLAN.json) describes shot boundaries and game-event prerequisites.
- [DATA_GAPS.json](canon/DATA_GAPS.json) distinguishes true preparation/approval gaps
  from resolved registration errors. No local folder is a handoff destination.

## Planning is not permission to animate

`shots/<id>/CARD.json` uses `reef.grok.shot-plan.v2`. It is not a ready Imagine
packet. Missing opening is null, not a fallback room. Each folder includes
`FIRST_FRAME_BRIEF.txt` and `PROMPT.txt`.

The compiler exports canonical `imagine-shot-packet-v2` only after exact input,
approval and request checks. The exported private packet must also pass the
project's `tools/audit_imagine_handoff.py --require-ready` gate.

```text
python -B design/cinematics/v2/tools/validate_v2.py
python -B -m unittest discover -s design/cinematics/v2/tools -p "test_*.py"
python -B design/cinematics/v2/tools/validate_v2.py --require-ready
```

The last command must FAIL while openings remain unapproved. Planning PASS
prints blocked/ready counts and does not authorize generation.
ARCHIVE_COMPLETE depends on the visual manifest and recipient access.
GENERATION_READY and DELIVERY_ACCEPTED remain false. No finding is closed.

Earlier explanations blaming library size or six-second duration are hypotheses,
not established model limits. Small jobs isolate defects; actual frame review
determines success. The planner may use the library; the render executor gets
one card and its two-to-four approved inputs.

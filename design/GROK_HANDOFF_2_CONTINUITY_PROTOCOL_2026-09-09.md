# Grok Handoff 2: sequence continuity and repair

Status: `SUPPORTING_CURRENT`. Implements the 2026-09-09 owner commission under
`DL-CIN-01` through `DL-CIN-15`; does not change cinematic delivery rules.
Use with [MASTER](GROK_MASTER_HANDOFF_FORMULA_2026-08-30.md), the mandatory
[V1 shot card](templates/IMAGINE_SHOT_CARD_V1.md), and the
[Day One packet](../assets_src/cinematics/day_one_grok_handoff_2_2026-09-09/README.md).
The name Handoff 2 is the owner's new repair commission, not a renaming of the
historical September 4 third-pass archive. Historical verdicts remain intact.

## Why the previous controls did not protect the footage

The written formula already required identity, topology, approved openings and
endpoint review. Its implementation left three gaps. A draft binding could put
a location plate in IMAGE_1 while separately declaring the opening missing;
the same card could have an empty blocking-findings list. The strict review
classified clips individually, allowing a stable wrong room to receive
KEEP_HIGH_QUALITY. Later edited exports could use a different variant from the
preferred file in that review. These are observed artifact contradictions;
the actual Grok upload history/settings are unavailable, so their precise
causal contribution to each generation is unproven.

## One location and identity register

Use one location ID per actual room, shared across discovery, rescue,
restoration and recap. Dirty and clean are states of that room. Record the
canonical image hash, camera address, ordered landmarks, fixture count and
fixture placement. A new camera address needs a complete approved setup that
preserves the room. An unshown wall is unknown, not permission to invent it.

Keep swimming bunny, playroom rescue bunny and Grand Puff as distinct identity
IDs. Never use a bunny reference's incidental background as location authority.
The Pool seahorse is the blue/lavender, violet-crested, peach-bellied fixture on
its coral pedestal. Sick and restored are state variants of that identity;
neither a yellow animal nor a moss-covered stone replacement is acceptable.
Remove only authorized grime/obstruction. Preserve body, curl, crest, pedestal,
relative scale and location through cleaning.

For every setup, record at least three fixed landmark points and subject boxes
in normalized coordinates. Review first, last and action/contact frames. For a
locked camera, flag movement over 0.015 canvas width/height or a scale change
over 5% for inspection. These are conservative review triggers, not measured
device limits or substitutes for visual judgment. Any identity/topology failure
rejects the shot even below those numbers. For a moving camera, compare against
the approved camera transform; raw screen-coordinate differences alone cannot
establish drift. Record measured values, never prefill fictional observations.

## Build a setup before requesting motion

1. Inventory approved sources. Keep historical rejects and boards outside image
   bindings. Select the exact room, subject and critical-object authorities.
2. Prepare a complete, flattened opening candidate in the approved storybook
   medium. A plate alone is insufficient when cast, dirt, pins or props are
   missing. No composite repair becomes a cinematic frame.
3. Review that candidate beside the room master, identities, predecessor and
   planned successor. Record a named human decision tied to its exact hash.
4. Bind IMAGE_1 only after approval. A missing opening has `path: null` and an
   explicit blocker; a fallback location path is forbidden.
5. Bind two to four images total, one job each. Keep other references in the
   archive. If the visible cast cannot fit the identity budget, first use a complete
   approved opening that already proves the ensemble. Do not delete actors or
   split an authored beat automatically; record any remaining authority gap.

Retain the [V1 card](templates/IMAGINE_SHOT_CARD_V1.md) discipline and the existing
[V2 controls](templates/IMAGINE_SHOT_CARD_V2.md): character invariants, anatomy,
required prompt phrases, causal chain, exact cast, location lock and cut state.
V2 remains the execution framework; this repair overlay must not downgrade it. A repair queue entry is not an executable card.
Draft PROMPT.txt files must not be sent until the shot readiness gate passes.

## Generate and review in dependency order

Pilot the Stuffie establish/entry/reveal group and Pool seahorse group before
batching their descendants. Preserve each authored camera move; lock only shots
whose direction calls for stillness. A moving shot needs approved start/end
composition and camera-aware landmark review. One clip has
one dominant action, one camera setup and at most one camera move. The prompt
states the time-ordered trigger, visible change, fixed objects and settled end,
and ends with `Sound:`. Keep hash/audit/approval prose in the sidecar.

A continuation uses the exact accepted endpoint hash. An authored cut uses its
own approved first frame and receives a cross-cut review. A gameplay cut begins
after the real player action, not after a movie invents a victory. A recap
depends on its room's accepted clean endpoint, not on an independently attractive
new room. Changing a parent clip, opening, identity or location invalidates all
dependent approvals until reviewed again. Missing dependencies block only their
descendants; unrelated setup work continues.

Do not restore the omitted swing, wing-trail or basket-search actions. Day One
has two visible rescue-pin bunnies holding Baby Eagle. Discovery does not release
him. Restoration must follow the actual completed rescue. Preserve the Pool's
surface, waterfall, seahorse gameplay order; do not use cinematic shot numbering
as a second gameplay progression.

## Review the clip and the cut, then record the selection

Record exact filename, source hash, generation prompt/settings if available,
native fps and frame interval. No OFFICIAL, REGEN, v2 or prior KEEP filename
grants approval. Review the native clip at speed, frame-step contact/motion,
inspect sampled interior frames, then place its end beside the next opening.
Record these decisions independently:

- local shot: room, identity, anatomy, count, style and action;
- incoming/outgoing cut: landmarks, screen side, scale, ownership and state;
- runtime seam: actual entry/completion state and no unearned payoff;
- editorial selection: exact variant and in/out frame range;
- delivery: independent full-frame evidence and remaining acceptance gates.

Any hard failure overrides an aesthetic score or prior keep. A sampled board can
prove a visible defect, but cannot prove the absence of one-frame errors or
audio problems. An unchanged shot without a detected defect is a retain
candidate, not newly accepted footage. Keep rejected candidates and correction
reasons; after two repeats of the same failure, revisit the opening and authority
conflict before spending another generation.

## Publish and enforce honest status

Run `python -B tools/audit_grok_handoff_2.py <packet>` for archive integrity and
draft consistency. `--require-ready` must fail while openings, measurements,
human approvals or accepted dependencies are missing. This additional gate does
not replace `tools/audit_imagine_handoff.py --require-ready` on completed V1/V2
execution packets, or `tools/audit_cinematic.py` on delivery evidence.

Publish the complete reference archive on a durable branch. Record immutable
content-commit URLs and verify every payload file against GitHub's commit tree
and blob identity in a subsequent evidence commit. Report ARCHIVE_COMPLETE,
GENERATION_READY and DELIVERY_ACCEPTED separately. No new returned footage is
accepted by this protocol. The full-frame generation rule remains binding for
final cinematic frames; Grok clips remain motion/editorial reference.

## Revision 2: preserve stronger original direction

The first Handoff 2 draft introduced regressions. Before changing a shot, compare
its August direction, later detailed repair card, exact selected variant and
current event contract. Record the source hash, original action/camera/cast,
proposed delta, defect evidence and reason for each semantic change. A summary
matrix is an index, not a replacement for detailed direction. Preserve original
sound, physical contact, identity traits and negatives in the executable prompt.

Use `COMPARATIVE_AUDIT.json` for all 74 shot decisions and each repair card's
`source_direction` / `previous_detailed_card` for inspectable original text.
Those archival snapshots are not alternative image bindings. Later two-pin
rescue and front-facing Art Room contracts supersede obsolete original actions;
restoring detail does not restore a swing, basket search or invented side wall.

Bind one material state per object per job. The similarly named Pool sources
are different: `objects/seahorse_sick.png` has the lodged pink obstruction;
`handoff_art/seahorse_sick.png` has an open nozzle with remaining grime. Never
bind both to a discovery shot. The first pull ends dry; the next shot begins
water. Review object-state variants visually rather than trusting filenames.

A recap may deliberately show a later visit, but that time change needs explicit
support. C12-S03's original Eagle/bunny friendship beat conflicts with the later
rescue departure; preserve the proposed beat and flag the conflict. Do not
silently authorize either a reunion or an empty-room replacement. C12-S03/S04
were omitted from V03, so their cards are conditional reconstruction proposals.

The archive gate checks file integrity, bound-state contradictions and camera
count, not artistic quality or all V2 fields. It cannot promote this draft queue.
Complete the retained V2 execution fields and run the existing Imagine readiness
gate when actual approved openings and reviews exist. No threshold or passing
unit test substitutes for that work.

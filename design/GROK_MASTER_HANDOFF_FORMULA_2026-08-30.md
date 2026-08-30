# Grok master handoff formula

## Purpose

Use this system for every new Grok Imagine scene. It turns a scene idea into a
self-contained archive and a series of small executable generation jobs while
keeping character identity, room geometry, causality, and acceptance outside
the generator's discretion.

The short formula is **MASTER**:

1. **M — Mission:** one sentence, one causal promise, one final state.
2. **A — Authorities:** approved room, characters, objects, and grade, each
   with exactly one declared domain.
3. **S — Shots:** one camera setup and one dominant action per generation.
4. **T — Topology:** exact cast, anatomy, scale, ownership, contact, and
   forbidden drift.
5. **E — Endpoints:** every continuing shot starts from the accepted previous
   ending frame; authored cuts start from a separately approved master.
6. **R — Review/regenerate:** knockouts first, then rubric; regenerate the
   complete failed frame or shot and retain the reject.

## The master packet

Store every handoff under:

```text
assets_src/cinematics/<handoff_id>/
  IMAGINE_HANDOFF.json
  HANDOFF_PACKET.json
  README.md
  handoff_art/
    <approved room/background>
    <approved character identities>
    <approved object/material identities>
    <approved grade/style reference>
  storyboards/
    <shot board; narrative only>
  shots/<shot_id>/
    PROMPT.txt
    SHOT_PACKET.json
    <approved clean first frame>
```

`HANDOFF_PACKET.json` is the human/archive inventory: source path, role,
dimensions, SHA-256, licence/provenance, modification status, and sorted packet
payload hash. `IMAGINE_HANDOFF.json` is the status and sequence contract.
`SHOT_PACKET.json` is one executable job. Never paste archive metadata into
`PROMPT.txt`.

## Stage 1 — write the story contract

Before generating art, write:

- one sentence describing the irreversible change the audience sees;
- ordered beats, each with a physical trigger and visible result;
- final visible state;
- at least two forbidden events, including the most plausible premature
  payoff or invented shortcut.

If a beat cannot be expressed as `trigger → visible change → confirmed end`,
it is not ready to become a shot.

## Stage 2 — lock the room as a volume

Use one approved room/background authority. Record:

- cardinal orientation or equivalent entrance/exit compass;
- wall/zone inventory and fixed landmark order;
- shared surfaces and topology, such as “one giant pool”;
- immutable fixtures;
- forbidden geometry, such as “no local fountain basin”;
- dirty/clean/time-of-day state;
- physical camera address for each shot, not merely “another angle.”

When the reference omits part of the room, create and approve a coherent room
turnaround before shot work. A new wall must physically join known walls. Do
not ask Grok to discover room architecture while also animating a story beat.

For a close-up, keep one quiet context anchor: a character edge, recognizable
arch, waterline, pedestal contact, or adjoining fixture. This prevents the
subject from becoming isolated product art.

## Stage 3 — build the character lock

For each visible character, the archive must contain:

- stable ID and approval status;
- one canonical identity image and SHA-256;
- at least three discriminative identity traits;
- species/anatomy topology;
- forbidden changes;
- relative scale and relationship/contact rules when another character is
  present;
- allowed motion vocabulary and emotional range.

Use visual facts, not adjectives. “Rumi: enormous violet braided high ponytail,
pointed ears, star-shell earrings, navy/lavender gold-trimmed sea-jacket,
turquoise-to-lavender tail, broad coral-pink split fin; exactly two arms and one
continuous mer-tail” is executable. “Beautiful purple mermaid” is not.

Every shot repeats the exact cast and, for each visible character:

- identity reference ID;
- screen role;
- opening and ending pose/state;
- identity, anatomy, and forbidden-change lists;
- at least two short phrases that must literally appear in the prompt.

For a two-character interaction, prefer this four-image set:

1. approved complete first frame/layout lock;
2. character A identity;
3. character B identity;
4. approved relationship/scale/contact authority.

If an object identity is more important than relationship art, encode the
relationship as explicit scale, screen-side, hand ownership, and contact text.
Do not exceed four images. Split a crowded shot instead.

## Stage 4 — approve opening images

Each shot requires a complete, clean, UI-free, human-approved opening image.

- A new setup or authored cut uses an `approved_master`.
- A continuing action uses the exact `accepted_previous_end` and repeats its
  SHA-256 in the continuity contract.
- A storyboard, contact sheet, HUD capture, runtime-boundary capture, or audit
  montage is never the opening pixel authority.

The first image already contains the right room, cast, state, scale, and
composition. Grok animates a bounded change; it does not repair the setup.

## Stage 5 — make one card per shot

Use `design/templates/IMAGINE_SHOT_CARD_V2.md`. A card contains:

- one sequence position and one or more story beat IDs;
- duration 2–8 seconds;
- one camera verb and zero or one move;
- two to four role-labeled images with immutable GitHub URLs;
- exact cast and character locks;
- room lock and forbidden geometry;
- causal chain;
- inherited state and allowed changes;
- must-move and must-not-move lists;
- exact visible end state and negatives;
- one short paste-ready prompt ending with `Sound:`.

Generate one clip per card. Assemble clips later with authored straight cuts.
Never ask one generation to create a multi-shot movie.

## Stage 6 — use the authority budget

Every bound image has one job:

| Slot | Default job | It must not control |
|---|---|---|
| IMAGE_1 | approved complete first frame and layout | redesign of identity/style |
| IMAGE_2 | primary subject identity | room geography |
| IMAGE_3 | second character or critical object identity | a competing composition |
| IMAGE_4 | relationship/contact or lighting/grade | new story content |

If two images disagree in a domain, stop for a human decision. Do not ask Grok
to blend them. Related-but-unused assets stay in the archive and out of the
generation job; this is how the opening-flight otter failure is prevented.

## Stage 7 — write the executable prompt

The prompt is short, action-first, and chronological:

```text
<one camera verb> on IMAGE_1.

0.0–<t>s: <physical trigger/contact>.
<t>–<end>s: <visible consequence and settle>.

keep <room facts> locked. preserve <exact character lock phrases>. no <highest
risk character, topology, geometry, timing, UI, or style failures>.

end: <exact SHOT_PACKET end_state>.
Sound: <foley and room tone only; no protected voice synthesis>.
```

Do not paste hashes, licence text, audit language, scores, branch history, or
the whole story bible. Those belong in the archive. The prompt states what
moves, what stays fixed, and what the final image visibly proves.

## Stage 8 — review in the right order

Review each native clip and its lossless extracted frames before creating a
dependent shot.

1. **Knockouts:** wrong actor; identity/anatomy drift; extra/missing limbs;
   wrong room or topology; wrong cast count; premature payoff; missing contact;
   forbidden object; UI/text; method violation; unapproved first frame.
2. **Continuity:** first frame equals its authority; previous endpoint, screen
   side, object ownership, lighting, and geography persist.
3. **Causality:** trigger, visible change, and settled end are all readable.
4. **Style/readability:** approved 2D storybook finish and phone-size clarity.
5. **Technical:** duration, resolution, frame rate, audio policy, native hashes,
   prompt/settings, and lossless frames.

Any knockout is a fresh complete regeneration, regardless of attractiveness or
numeric score. Keep the rejected candidate and record one targeted correction.
Do not stack many repairs in one retry. A score never overrides a knockout.

## Stage 9 — publish and report three claims

Use a two-commit publication flow to avoid self-referential hashes:

1. Commit/push packet art and first-frame authorities.
2. Put immutable URLs from that content commit into ready shot cards; audit,
   commit/push the cards and remote verification record.
3. Verify the remote manifest and every referenced asset resolves.

Report independently:

- `ARCHIVE_COMPLETE`: the self-contained GitHub packet, manifest, hashes,
  provenance, references, and board resolve.
- `GENERATION_READY`: every shot card passes the structural audit and every
  bound image has been opened and human accepted.
- `DELIVERY_ACCEPTED`: the returned full-frame cinematic evidence passes
  identity, topology, continuity, method, device, child, and owner gates.

Run:

```text
python tools/audit_imagine_handoff.py assets_src/cinematics/<handoff_id> --require-ready
```

Grok image-to-video output remains motion/editorial reference. It does not
become final cinematic delivery without the independent full-frame evidence
required by `tools/audit_cinematic.py`.

## Stop conditions

Do not generate when any of these is true:

- a character is concept/pending or lacks a stable identity authority;
- the room compass/topology is unknown;
- a shot lacks a complete approved opening image;
- two references conflict in the same authority domain;
- the prompt contains more than one camera move or dominant action;
- a dependent previous endpoint has not been accepted;
- a board or HUD capture is being used as pixel authority;
- the packet is called ready only because its archive is complete.

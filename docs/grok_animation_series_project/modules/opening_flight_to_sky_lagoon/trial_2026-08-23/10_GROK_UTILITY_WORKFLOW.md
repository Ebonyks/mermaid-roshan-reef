# Making Grok Imagine useful for this project

## Recommended role split

Grok is most useful as a **bounded shot renderer**. It is substantially less reliable as the writer, continuity database, editor and multi-shot director at the same time.

- Project/branch files own canon and reusable references.
- The external shot script owns causality, timing and cut order.
- Grok creates one approved still or one uncut shot.
- A human or stronger orchestration agent performs audit, selects variants and updates the ledger.
- DaVinci Resolve, Premiere, ffmpeg or another deterministic editor performs trimming, assembly and audio.

## Fresh generation versus conversational correction

For structural failures—wrong location, wrong scale, surprise animal, wrong castle reveal, teleport, time reversal—start a new generation from the last approved canonical still. Conversational coaching often preserves the bad latent composition while changing superficial details.

Use conversational correction only for a candidate that is already structurally correct and needs one small change, such as reducing hair motion or keeping a hand still.

Do not attach the rejected 46.5-second video to replacement generations. Its images are evidence for the written audit, not appearance authority.

## Context isolation

Use one Project chat per sequence and, for difficult shots, one short chat per anchor/shot family. Keep global constitution and cast records in the Project, but reattach only the exact two to four images controlling the current generation.

The full PNW pack belongs in the asset library, not in the reference set for every shot. Attaching semantically rich fauna and flora while asking for a landing made an otter become a principal actor. For the opening:

- cabin shots: cabin anchor + required character identities;
- route shots: route anchor + airplane + rear character authorities;
- final reveal: exact geography + exact castle + rear characters;
- no PNW fauna reference at any point.

## Risk-first trial order

Do not generate shots 1–15 sequentially on the first pass. Prove the hard constraints first:

1. `ROUTE_ANCHOR_V2` — six steps, two rails, separate platform, no lawn.
2. `FINAL_REVEAL_ANCHOR_V2` — exact geography and small rear characters.
3. `CABIN_ANCHOR_V2` — exact two seats, belts and identity.
4. V2-S11 route motion.
5. V2-S14 final reveal motion.
6. V2-S07/S08 belt ownership.
7. Only then generate the easier reaction and travel shots.

This prevents spending most of the generation budget before discovering that the engine cannot hold the hardest topology.

## Candidate strategy

For a difficult anchor, generate two or three candidates from the same prompt and reference order. Compare them outside Grok. Never ask a later conversational message to average two candidates.

Promote one candidate to `APPROVED`; mark every other result `REJECT` with a reason. Only an approved still becomes an image-to-video starting frame.

## Prompt density

Detailed prompts help only when the generation unit is small. Put these items first:

1. one-shot/no-cut instruction;
2. exact start state;
3. one action;
4. exact end state;
5. reference-domain order;
6. three to eight shot-specific prohibitions.

Avoid burying the essential action beneath the entire series bible. The Project already holds global style/canon; the shot prompt should remain executable.

## When to use another engine

If Grok fails the same approved anchor or topology gate three times, stop spending attempts on that shot. Preserve the reference pack and prompt, then trial a model with stronger image-to-video adherence or camera/first-last-frame control. Grok can still contribute:

- environment and pose ideation;
- alternate reaction coverage;
- low-motion atmospheric inserts;
- style/keyframe candidates;
- fast visual exploration before outsourcing final motion.

Do not lower the castle, identity, hand-ownership or route gates merely because Grok is convenient.

## Practical conclusion

A full fresh rebuild is the right approach, but “from scratch” should mean **from approved canonical stills, one shot at a time**, not one new request for another complete 42.5-second movie. The rejected trial has already supplied its value: it tells us exactly which constraints must be isolated.

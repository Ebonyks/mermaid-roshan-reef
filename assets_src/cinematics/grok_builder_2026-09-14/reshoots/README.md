# Persistent reshoot exchange

This is the ongoing back-and-forth folder, not another handoff that expires after one batch. Stable shot IDs join the scene, current direction, references, request, returned media, exact QC spans and next attempt. Never overwrite an earlier attempt or promote a returned clip automatically.

## Folder contract

```text
reshoots/
  QUEUE.json                         derived shot inventory, not a live approval ledger
  templates/RETURN.json              copy and fill; placeholders deliberately fail validation
  templates/REVIEW.json              exact defects and reconstruction targets
  inbox/<shot_id>/A001/<media>        operator-staged returned bytes, never executed
  attempts/<shot_id>/A001/
    REQUEST.json                     frozen source/prompt snapshot and hashes
    RETURN.json                      validated media receipt, not artistic acceptance
    REVIEW.json                      named QC decision, never owner approval
    SUPERSEDED.json                  only when source contract changed
  attempts/<shot_id>/A002/…           correction links back to previous review
automation/grok_reshoot_exchange.py   same tool as repository tools/ version
```

Empty inbox/attempt folders are created when used. Do not check secrets, credentials, expiring signed URLs or executable downloads into this project. Preserve rejected media and exact filenames/hashes. Large clips can live as versioned GitHub release assets with immutable hash receipts; download them into this inbox for ingest, then retain the original release and hash. The tool rejects source URLs containing query strings, fragments or credentials; use the stable GitHub release-download link instead of its signed redirect. It does not download or execute URLs. Never substitute a URL-only receipt for verified bytes.

## Round trip

The packet already contains `attempts/SHOT-BUNNY-SOAP/A001/REQUEST.json` as a planning pilot. Use that frozen request; do not run its initial export again before a return and review exist. The first export below illustrates starting a shot with no attempt yet. Later exports of that same shot are permitted only after a `REGENERATE` review or an explicitly superseded stale request. The 90 `JOBSHOT` career proposals must first become scoped shot contracts in the main library before they can enter this exchange.

From the repository root, using Python 3:

```text
python -B tools/grok_reshoot_exchange.py assets_src/cinematics/grok_builder_2026-09-14 status
python -B tools/grok_reshoot_exchange.py assets_src/cinematics/grok_builder_2026-09-14 export SHOT-POOL-SKIM
python -B tools/grok_reshoot_exchange.py assets_src/cinematics/grok_builder_2026-09-14 ingest <filled-return.json>
python -B tools/grok_reshoot_exchange.py assets_src/cinematics/grok_builder_2026-09-14 review <filled-review.json>
python -B tools/grok_reshoot_exchange.py assets_src/cinematics/grok_builder_2026-09-14 export SHOT-POOL-SKIM
```

For an extracted packet, use its `automation/grok_reshoot_exchange.py` and the packet's local directory instead. Builder can implement the same data contract if it cannot run Python; do not claim a CLI, filesystem or Imagine API is available without checking. No scheduler, paid API calls, voice synthesis or autonomous generation is installed here.

1. **Export planning request.** Resolve scene before/after states and the exact shot. The request freezes its prompt, active identities, room, event, dependencies and authority conflicts. It is explicitly **not permission to generate**.
2. **Approve opening outside this tool.** Show the owner the complete first frame, exact filename and SHA-256. Resolve missing views, cast and scales. Create a V1 execution card with the additional V2 sidecar controls. Bind only 2–4 images. Run the independent Imagine readiness gate. Keep that separately reviewed execution card beside the frozen request; it must identify the request hash. No board or gameplay capture can be IMAGE_1.
3. **Return one shot.** Grok supplies the prompt/settings actually used, model/version, native duration/fps/count, clip plus useful first/end/contact frames, hashes and a manifest matching the exact request hash. Stage bytes inside inbox, then ingest. Expected editorial rate is 24fps; do not silently conform a different native rate. This metadata check does not probe the stream or inspect pixels. Verify native metadata with ffprobe before QC.
4. **Review clip and cut.** Watch normal speed; inspect first/last and contact frames, then relevant interior intervals. Compare against room/character references, incoming endpoint, next opening and real gameplay state. Describe the observed failure, expected source fact and specific reconstruction. Use zero-based, end-exclusive native frame intervals; at 24fps `[48,72)` means 2.0–3.0 seconds. Sampled QC does not establish every-frame delivery acceptance.
5. **Iterate one correction.** `REGENERATE` requires a concrete defect; the next request adds its reconstruction and records the previous review hash. `HOLD` stops. `ROUGH_REFERENCE_CANDIDATE` is only a candidate for editorial review. Three attempts is the hard cap; repeated defects need reconsidered references/opening rather than a blind loop. No decision in this folder grants owner approval or final delivery.

If identities, layout, direction or upstream shot contracts change, old requests become `STALE`. Preserve them. Run `supersede <shot_id> <attempt_number>` only for a stale attempt, then export the next attempt. The retry cap still applies. Do not edit a frozen REQUEST to make a return match. Changes to accepted endpoint files must be recorded in the shot/dependency contract with hashes before successor work; undocumented endpoint changes are not automatically discoverable.

## Reconstruction quality

Weak: “make Daddy better.” Useful: “frames 38–57: brush bristles point away from Grand Puff while the hand intersects the head. Reconstruct the complete frames using the approved Daddy master and accepted neighboring endpoints: the same hand wraps the handle behind the ferrule, bristles remain on the wet bunny surface, and foam grows only at that contact. Keep glasses, crown, rainbow tail and attic windows unchanged.” This is an illustrative issue, not a newly observed defect in a returned clip.

Review identity, topology, exact cast, room anchors, contact causality, state persistence, camera, pacing, sound and technical integrity separately. One attractive frame cannot rescue a wrong room or premature payoff. Do not fix an error with interpolation, morphing, crossfades, composites, duplicated action frames or a new unrelated camera angle.

## Publication and claims

After each exchange, commit the new attempt records and updated authoring inputs on a durable project branch, rebuild the packet manifest, and verify the remote payload. Return immutable commit/tree/manifest links to Grok. The older remote receipt proves only its named content commit. A fresh local request does not inherit `ARCHIVE_COMPLETE` from that receipt.

`ARCHIVE_COMPLETE`, `GENERATION_READY` and `DELIVERY_ACCEPTED` are separate. The automation always leaves the latter two false. First-frame approval, independent readiness, cinematic frame provenance and final human/device gates remain external and blocking. This folder changes no game runtime, save state or media selection.

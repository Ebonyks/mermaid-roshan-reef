# Animation job card — V1

Status: `CANONICAL_CURRENT` production/derivation sidecar template under
`DL-MOT-14` through `DL-MOT-16` and `DL-CIN-11`. Complete one per action/shot;
mark non-applicable fields with reasons. Empty review fields mean pending.
This card records evidence and grants no asset, runtime or release acceptance.
Use the [production protocol](../animation/ANIMATION_PRODUCTION_PROTOCOL.md).
Grok's executable prompt still uses [IMAGINE V1](IMAGINE_SHOT_CARD_V1.md).

## Brief and limits

| Field | Value to supply |
|---|---|
| Identity | Job ID, revision, author/date, exact source commit, character/profile version |
| Output lane | Gameplay sprite, cinematic footage, or reference-only study |
| Intention | Who wants what, does what, and what visibly changes |
| Required action | Axis, support, contact, view changes and readable payoff |
| Fixed elements | Camera, room landmarks, fixture/support and identity constraints |
| Entry / exit | Source frame/pose, facing, pivot, prop ownership, safe end state |
| Reuse / gap | Exact approved source coverage; specific missing art/action |
| Method | Aseprite/authored 2D, image-to-video, guided video-to-video, targeted still repair, or bounded combination; why it suits the action |
| Runtime size | Native dimensions and timing; viewport/actor scale, legal texture layout |
| Motion tolerances | Pivot, fixture, contact and required excursion in stated units; loop/exit criteria set before evaluation |
| Limits | Total attempts (default two generated takes), local wall-time ceiling, cleanup-time ceiling, monetary cap and existing spending authority; aggregate task cap |
| Stop / fallback | Defect classification, change to diagnose, and alternative after two nonviable takes; never an automatic per-frame ImageGen batch |

## Bound inputs and production provenance

For each input: stable source ID/path, SHA-256, dimensions, role,
license/provenance, exact acceptance scope and permitted modifications.
An approved reference is not an approved output. Preserve originals.

For every attempt and derivation, retain:

- Attempt ID/number, job/brief revision, prompt/workflow hash, seed if exposed,
  provider/endpoint or local code/node revision, checkpoint/LoRA hashes when
  available, precision, dimensions, frame count/rate and settings. If a hosted
  model revision is hidden, record that limit and retain its request/response ID.
- Native output path/hash, provider request ID, elapsed load/encode/sample/decode
  and cleanup time when measurable, observed billing, disposition and exact
  failure frames/events. Credentials and authenticated URLs are excluded.
- Aseprite version, master path/hash, source-to-timeline mapping, changed
  layers/frames, matte cleanup, registration, repaint/in-between/composite work,
  hold/retime/interpolation declarations and each derivative's parent/hash.
- Exported atlas/sequence/movie and timing data paths/hashes; pivot/socket and
  trim-offset data; tags, durations and loop/one-shot behavior; reversible
  round-trip/export comparison. Describe encoding/whole-canvas normalization.
- Position-only guide path/hash/role and `used_as_delivery_pixels: false`, if
  used. Keep guides excluded from runtime and delivered pixels.

## Reviews and integration

| Evidence lane | Required actual result |
|---|---|
| Human identity / topology / style | Reviewer/date, exact hashes, normal-speed plus frame-step review; compare approved identities and changing surfaces |
| Human motion / contact / seam | Reviewer/date, action/axis/support, fixture/landmark measurements, contact spans, entry/exit or loop pose/velocity, every repaired transition |
| Source / export machine | Commands/log hashes; real alpha, no bleed/crops, native/atlas geometry and master-to-export equality |
| Cinematic machine | Production-profile `tools/audit_cinematic.py --manifest` and report hash; optional full-frame provenance audit only for that declared method |
| Gameplay machine | Actual engine atlas sampling, event/target ownership, passive negative, repeat/cancel/pause/return/save probes and required full gates |
| Device | Exact build/APK hash, Mobile/Speedy, device, scene/capture, 30-fps timing/hitch/memory/load/playback measurements against applicable limits |
| Child / owner | Named session/build/output and recorded result when required; agent review cannot fill this row |

Record `ARCHIVE_COMPLETE`, `GENERATION_READY`, `DELIVERY_ACCEPTED`, runtime
integration and release status independently. List missing evidence explicitly.
Method eligibility never accepts old rejected pixels, and a successful machine
report cannot replace provenance, human, device, child or owner review.

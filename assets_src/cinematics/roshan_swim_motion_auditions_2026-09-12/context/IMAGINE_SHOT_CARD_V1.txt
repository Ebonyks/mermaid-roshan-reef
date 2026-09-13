# Imagine shot card v1

Use one completed copy of this card for one Grok Imagine generation job. Keep
the compliance/archive manifest beside it; do not paste hashes, licences,
policy, audit scores, or storyboard prose into the generator prompt.

## Readiness fields

```text
movie_id: <stable movie id>
shot_id: <one unique shot id>
status: DRAFT | GENERATION_READY | GENERATED_PENDING_REVIEW | ACCEPTED_REFERENCE
duration: <2–8 seconds>
aspect: 16:9
size: 1280x720
mode: image-to-video
output_disposition: motion_reference_only
```

`GENERATION_READY` is allowed only after every image binding below has been
opened from GitHub and the first frame is an approved clean UI-free image.
Image-to-video output remains motion reference under the project full-frame
cinematic rule; this status never means delivery acceptance.

Store the machine-readable card as
`assets_src/cinematics/<handoff_id>/shots/<shot_id>/SHOT_PACKET.json` and the
paste-ready prose as `PROMPT.txt`. After committing and pushing the content,
write a separate remote-verification record that points back to that immutable
content commit. Do not put the card's own future commit SHA inside the card.

## Bound images — two to four only

```text
IMAGE_1: <GitHub/raw URL>
job: approved clean first frame and layout lock

IMAGE_2: <GitHub/raw URL>
job: subject identity

IMAGE_3: <GitHub/raw URL, when needed>
job: object or material identity

IMAGE_4: <GitHub/raw URL, when needed>
job: lighting or grade
```

Do not bind a generated storyboard/contact sheet, HUD-bearing gameplay capture,
audit montage, UI frame, or a reference with a second conflicting room layout.
Put storyboard order and gameplay seam constraints into words instead.

## Shot controls

```text
start_frame: IMAGE_1
camera: <one verb only; e.g. locked, slow push-in, gentle pan right>
must_move: <short subject/action list>
must_not_move: <locked fixtures, room geometry, unaffected subjects>
end_state: <one visible sentence>
negative_constraints: no HUD, no text, no extra fixtures, no identity drift, <shot-specific negatives>
sound_intent: <foley/room-tone direction only; never protected family voice generation>
```

## Paste-ready prompt

Write lowercase prose, action first, in visible time order. Use one camera move
at most and one dominant action. Keep it short enough to paste without the
archive sidecar.

```text
<camera verb> on the approved bathroom from IMAGE_1.

0.0–<t>s: <first visible action and physical contact>.
<t>–<t>s: <single consequence; name material behaviour>.
<t>–<end>s: <reaction and readable settle>.

keep <fixed fixtures/subjects> locked. preserve <identity/object/material>
from IMAGE_2[/IMAGE_3/IMAGE_4]. no HUD, no text, no extra fixtures, no
camera drift, no morphing, no identity or costume changes.

end: <same visible end-state sentence as above>.
Sound: <brief foley and room tone; no protected voice synthesis>.
```

## Audit decisions

Record these separately; never collapse them into one numeric score.

```text
ARCHIVE_COMPLETE: true | false
GENERATION_READY: true | false
DELIVERY_ACCEPTED: true | false
reviewer: <name>
reviewed_at: <ISO-8601>
blocking_findings: <none or explicit list>
```

Generation readiness checks input count, roles, clean first frame, URL access,
one-shot scope, one camera move, executable timeline, end state, negatives, and
sound. Delivery acceptance is a later independent full-frame/human/device audit.

Run the structural gate with:

```text
python tools/audit_imagine_handoff.py <packet-directory> --require-ready
```

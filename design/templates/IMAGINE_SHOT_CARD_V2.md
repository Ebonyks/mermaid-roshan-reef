# Imagine shot card V2

V2 adds machine-audited character, room, causality, and endpoint locks to the
V1 one-shot discipline. Use one card for one Grok Imagine image-to-video job.
The complete process is `design/GROK_MASTER_HANDOFF_FORMULA_2026-08-30.md`.

## Handoff-level requirements

`IMAGINE_HANDOFF.json` uses schema `imagine-handoff-v2` and retains the three
independent statuses from V1. It also contains:

```json
{
  "story_contract": {
    "one_sentence_promise": "<one irreversible visible story change>",
    "ordered_beats": [
      {"beat_id": "B01", "trigger": "<physical cause>", "visible_result": "<visible effect>"}
    ],
    "forbidden_events": ["<premature payoff>", "<likely invented shortcut>"],
    "final_state": "<exact visible final state>"
  },
  "character_authorities": [
    {
      "character_id": "<stable_id>",
      "path": "handoff_art/<identity>.png",
      "sha256": "<64 lowercase hex>",
      "status": "approved | approved_private_canon",
      "immutable_traits": ["<three or more discriminative traits>"],
      "anatomy_traits": ["<species/topology>"],
      "forbidden_drift": ["<two or more explicit failures>"]
    }
  ],
  "location_authority": {
    "path": "handoff_art/<approved room>.png",
    "sha256": "<64 lowercase hex>",
    "immutable_features": ["<three or more fixed room facts>"],
    "forbidden_geometry": ["<at least one likely topology failure>"]
  }
}
```

Every file is inside the packet and hashed. A ready packet also retains the V1
immutable `archive_remote`, ordered `shot_packets`, and empty
`blocking_findings`.

## Machine-readable shot card

Store as `shots/<shot_id>/SHOT_PACKET.json`:

```json
{
  "schema": "imagine-shot-packet-v2",
  "movie_id": "<stable movie id>",
  "shot_id": "<unique shot id>",
  "sequence_position": 0,
  "beat_ids": ["B01"],
  "mode": "image_to_video",
  "output_disposition": "motion_reference_only",
  "duration_seconds": 4,
  "aspect_ratio": "16:9",
  "delivery_size": [1280, 720],
  "bound_references": [
    {
      "id": "IMAGE_1",
      "role": "approved_clean_first_frame",
      "authority_domain": "exact opening pixels, cast placement, room layout",
      "source_kind": "approved_master",
      "path": "shots/<shot_id>/FIRST_FRAME.png",
      "remote_url": "https://raw.githubusercontent.com/<owner>/<repo>/<40-char-content-commit>/<packet-path>/shots/<shot_id>/FIRST_FRAME.png",
      "sha256": "<64 lowercase hex>",
      "hud_present": false,
      "human_decision": "accepted"
    },
    {
      "id": "IMAGE_2",
      "role": "subject_identity",
      "authority_domain": "<character> identity, age, costume, and anatomy",
      "path": "handoff_art/<character>.png",
      "remote_url": "https://raw.githubusercontent.com/<owner>/<repo>/<40-char-content-commit>/<packet-path>/handoff_art/<character>.png",
      "sha256": "<same hash as character authority>",
      "hud_present": false,
      "human_decision": "accepted"
    }
  ],
  "exact_cast": ["<character_id>"],
  "character_locks": [
    {
      "character_id": "<character_id>",
      "reference_id": "IMAGE_2",
      "identity_invariants": ["<three or more>"],
      "anatomy_invariants": ["<at least one>"],
      "forbidden_changes": ["<two or more>"],
      "screen_role": "<side, scale, and story function>",
      "start_state": "<visible opening state>",
      "end_state": "<visible ending state>",
      "required_prompt_phrases": ["<exact short identity phrase>", "<exact anatomy/scale phrase>"]
    }
  ],
  "location_lock": {
    "reference_id": "IMAGE_1",
    "immutable_features": ["<at least two visible room facts>"],
    "forbidden_geometry": ["<at least one likely failure>"],
    "required_prompt_phrases": ["<exact short room-lock phrase>"]
  },
  "causal_chain": {
    "trigger": "<physical contact/cause>",
    "visible_change": "<consequence>",
    "end_confirmation": "<settled proof>"
  },
  "continuity": {
    "kind": "new_setup",
    "previous_shot_id": null,
    "inherited_state": ["<what must remain from the sequence>"],
    "allowed_changes": ["<only what this shot may change>"]
  },
  "non_pixel_references": [],
  "camera": {"verb": "locked", "move_count": 0},
  "must_move": ["<subject/action>"],
  "must_not_move": ["<fixtures/unaffected subjects>"],
  "end_state": "<exact sentence repeated in PROMPT.txt>",
  "negative_constraints": ["no HUD", "no text", "no identity drift", "<shot-specific>"],
  "prompt_path": "shots/<shot_id>/PROMPT.txt",
  "prompt_sha256": "<64 lowercase hex>"
}
```

For a continuous action, change `continuity.kind` to `continuous_action`, set
`previous_shot_id` to the immediately preceding shot, set IMAGE_1
`source_kind` to `accepted_previous_end`, and add
`continuity.previous_end_sha256` equal to IMAGE_1's hash. An authored cut uses
an independently approved master and `authored_cut`. An intentional hold must
be story-directed, uses an approved master, and cannot replace required action.

Allowed bound-reference roles are:

- `approved_clean_first_frame` — IMAGE_1 only;
- `subject_identity`;
- `relationship_scale_contact`;
- `object_or_material_identity`;
- `lighting_or_grade`.

Use two to four images only. Every V2 image needs a single authority domain,
immutable GitHub URL, local hash, `hud_present: false`, and human acceptance.

## Paste-ready prompt

```text
<one camera verb> on IMAGE_1.

0.0–<t>s: <single physical trigger/contact>.
<t>–<end>s: <visible change and readable settle>.

keep <exact room-lock phrase> locked. preserve <each character's required
prompt phrases>. no HUD, no text, no extra character, no identity or costume
drift, no forbidden topology, no premature payoff, no morphing.

end: <exact end_state sentence>.
Sound: <brief foley and room tone; no protected voice synthesis>.
```

Run:

```text
python tools/audit_imagine_handoff.py assets_src/cinematics/<handoff_id> --require-ready
```

The audit is structural and fail-closed. Human frame review, full-frame method
evidence, device/child review, and owner acceptance remain separate gates.

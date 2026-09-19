# Execution CARD schema (`imagine-shot-packet-v2-reef`)

Required keys on `shots/<id>/CARD.json`:

| Key | Rule |
|---|---|
| `schema` | `imagine-shot-packet-v2-reef` |
| `shot_id` | stable SHOT-* id |
| `generation_allowed` | boolean. false if any blocking_reason |
| `opening_approved` | boolean. false blocks motion |
| `delivery_accepted` | always false until owner yes |
| `exact_cast` | list of CHAR-* ids. count is a knockout |
| `exact_prop_counts` | map of named unique props to integers |
| `room_state` | map fixture → `dirty` \| `clean` \| `partial` \| `absent` |
| `binds` | 2–4 items. IMAGE_1 first |
| `binds[].people_in_plate` | IMAGE_1 must be false unless opening_approved |
| `binds[].role` | `empty_dirty_plate` \| `approved_first_frame` \| `subject_identity` \| `object_or_material_identity` \| `relationship_scale_contact` |
| `camera.move_count` | 0 or 1 |
| `duration_seconds` | 3–6, prefer 4 |
| `prompt_path` | `PROMPT.txt` next to the CARD |
| `blocking_reason` | string or null |

Forbidden on a CARD: storyboards, DATABASE excerpts, historical clip URLs, licence blocks, other shots’ prompts.

`PROMPT.txt` is ≤ 1,200 characters, action-first, ends with `Sound:`, contains no hashes and no word “family” unless `exact_cast` has two or more named CHAR ids who are actually in the still.

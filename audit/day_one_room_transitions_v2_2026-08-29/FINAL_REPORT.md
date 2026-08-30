# Day One four-room transition re-audit and correction report

Status: implemented review candidate; manual review required before any fix
process or integration is established.

## Outcome

All four rooms retain a true dirty-to-clean sequence with one active
voice-and-pointer-guided target, ordered visible feedback, monotonic saves, no
fail state, and a distinct clean payoff. Fresh Luna review of only the current
authoritative captures passes every room at or above 4.75 and the four-room
mean at 4.96. These are agent-evaluated implementation scores, not child or
device certification.

Bathroom's bathtub overdraw remains specifically fixed. The complete dirty
Bathroom plate is hidden before the clean fixture layers become visible.
Exact Mobile state confirms `dirty_plate_visible=false` together with
`clean_fixture_layer_visible=true`; the v5 reveal contains one tub, one sink,
and one toilet rather than blended duplicates.

## Per-room review

### Pool — strongest causal reference

Pool retains the clearest environmental chain: algae task, six skimmer
catches, three waterfall scrub lanes, staged seahorse extraction, rainbow
flow, then Rumi. Every action visibly changes the environment or a character,
and the final state removes nearly all competing debris.

### Bathroom

Bathroom adds a soap-splat wipe before the established basket handoff. Basket,
sink circle, tub drain, `WHEE!` response, tub arrows, fixture sparkles, clean
room, and Pool route form a staged non-reader path. The old negative-feeling
`NO!` response is absent. The v5 transition is the accepted no-overdraw
evidence.

### Stuffie Playroom correction v2

The rescue concept is preserved and extended without changing Baby Eagle's
approved identity. Dirty entry hides both hanging room banners and begins with
one ceiling-hung dust bunny using approved existing bunny art. Roshan removes
it first, then clears the left and right bunnies pinning Eagle. Eagle responds,
stands in the purpose-built teal/pink rescue sprite, and departs; the room
brightens and restores both banners only in the settled clean state. The
focused adoption tutorial then uses the same full standing Eagle silhouette
with contain-fit padding.

### Craft/Art Studio correction v3 — narrowest current score

Craft now has eleven ordered saved interactions: the floor-only rainbow spill,
six supply pickups, three grime scrubs, and desk confirmation. All intended
clutter is visible at entry, but only one target is responsive and cued. The
legacy palette duplicate is suppressed. The rainbow alpha bounds stay within
the open floor and clear both foreground tables. Each table has exactly one
owner using a deterministic alpha-clean derivative of approved project pixels;
no generated table replacement was used. The v3 isolation and runtime frames
show continuous silhouettes without the torn/scalloped edges that caused v2
rejection, and no halo, hole, seam, rectangular pickup, or persistent rainbow
overdraw remains. The clean reveal removes temporary clutter and restores a
bright, settled room before any later optional picker.

## Strong-room qualities absent from weaker baselines

- One unmistakable active target rather than several equally live objects.
- A large target-specific pointer physically attached to that target.
- Competing controls and ambient handlers suppressed during focused work.
- Ordered touches with an immediate visible result before the next action.
- Character, fixture, or environment response after each meaningful beat.
- Strong dirty-versus-clean value and occupancy separation.
- A payoff that changes the room and advances the story, not only a counter.
- Immediate monotonic save before celebratory animation.
- Stable true-2D silhouettes at 1280×720 Mobile scale.

## Remaining deficit list

- Craft's later grime marks are narrow and less prominent at phone scale than
  its large rainbow and supply targets. The pointer preserves interaction
  clarity, but this is the clearest remaining room-art hierarchy deficit.
- Stuffie's dirty entry remains visually dense around Roshan because pinned
  Eagle, three bunnies, loose stuffing, and the active pointer share the center.
- Pool and Bathroom dirty entries also remain intentionally detailed beneath
  their dirty treatment, though their active targets remain legible.
- The generated Playroom wall healing and bold generated room targets remain
  owner art/taste gates.
- Intended-child observation and Lenovo Tab M11 performance/touch acceptance
  remain external gates.
- The canonical legacy Day One integration probe retains one unrelated stale
  `complete_tutorial("bathroom")` route assertion; focused production paths
  pass. See `rollback_package/TEST_LOG.md`.

## Authoritative review images

- Pool dirty: `visuals/candidate_v3/pool/00_dirty_arrival.png`
- Pool clean: `visuals/candidate_v3/pool/08_rumi_reveal.png`
- Bathroom dirty: `visuals/candidate_v5/bathroom/00_dirty_basket_prompt.png`
- Bathroom no-overdraw reveal: `visuals/candidate_v5/bathroom/08_whole_room_sparkle.png`
- Bathroom clean: `visuals/candidate_v5/bathroom/09_clean_pool_route.png`
- Stuffie dirty/no banners: `visuals/correction_v2/stuffie/00_dirty_no_banners_hanging_bunny_pending.png`
- Stuffie ceiling-bunny target: `visuals/correction_v2/stuffie/01_dirty_hanging_bunny_target.png`
- Stuffie purpose-built Eagle rescue: `visuals/correction_v2/stuffie/04_purpose_built_eagle_rescue.png`
- Stuffie clean/banners restored: `visuals/correction_v2/stuffie/05_settled_clean_banners_restored.png`
- Stuffie adoption: `visuals/correction_v2/stuffie/06_focused_adoption_tutorial.png`
- Art dirty/no overdraw: `visuals/correction_v3/art/00_dirty_all_clutter_grime_no_overdraw.png`
- Art rainbow feedback: `visuals/correction_v3/art/01_rainbow_floor_wipe_feedback.png`
- Art ordered counter stages: `visuals/correction_v3/art/08_ordered_scrub_left_counter.png` through `10_ordered_scrub_right_counter.png`
- Art reveal: `visuals/correction_v3/art/15_whole_room_reveal.png`
- Art clean: `visuals/correction_v3/art/16_settled_clean_art_room.png`
- Art ownership isolation: `visuals/correction_v3/art_layer_isolation/01_table_ownership_isolation.png`

Art correction v1 and v2 are rejected comparison evidence only. V2's derived
tables had torn/scalloped inner alpha edges. The generated table-edit candidate
was never accepted or wired. Only correction v3 and the exact approved-source
provenance in the rollback manifest are authoritative.

Final scores and evidence boundaries are recorded in `RUBRIC.md`.

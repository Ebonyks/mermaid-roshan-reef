# Day One four-room transition re-audit and candidate report

Status: implemented review candidate; manual review required before any fix
process or integration is established.

## Outcome

All four Day One rooms now begin in a materially dim/dirtier state with one
large room-specific generated cleaning target, one active pointer, a saved
one-finger/no-fail response, ordered room-specific beats, and a distinct clean
payoff. The strongest Pool qualities were carried into the other rooms without
replacing their concepts.

Bathroom’s bathtub overdraw is specifically fixed: the complete dirty Bathroom
plate is hidden before the clean fixture layers become visible. Exact Mobile
probe state confirms `dirty_plate_visible=false` together with
`clean_fixture_layer_visible=true`, and the v5 reveal capture contains one tub,
one sink, and one toilet rather than blended duplicates.

## Per-room review

### Pool — strongest reference

Pool retains the clearest causal chain: generated algae task, six visible
skimmer catches, three waterfall scrub lanes, staged seahorse extraction,
rainbow flow, then Rumi. Every action changes a readable part of the room or a
character, and the final state removes almost all competing debris.

### Bathroom

Bathroom now adds a room-specific soap-splat wipe before its established basket
handoff. Basket, sink circle, tub drain, WHEE response, tub arrows, fixture
sparkles, clean room, and Pool picture route form a staged non-reader path.
The old negative-feeling `NO!` response is absent; `WHEE!` is the authored
response. The v5 no-overdraw swap is the acceptance evidence.

### Stuffie Playroom

The rescue concept is preserved: Baby Eagle is blocked by two dust bunnies;
Roshan clears left then right; Eagle visibly responds, stands, and departs;
the room becomes bright and clean; then one focused adoption action appears.
The two bunnies are wider apart, the inactive one is dimmed, Roshan’s silhouette
stays clear, and the rescue-only picker now uses the same restored teal/pink
standing Eagle rather than switching to the generic beige bird.

### Art Studio — weakest baseline, materially improved

Art had the weakest original dirty/clean hierarchy. It now begins with a
generated rainbow spill, then exposes the existing grime from entry instead of
revealing it late. Loose supplies remain visible as clutter, but only the
pointer-owned item responds; out-of-order material and grime taps are proven
unable to skip. Final confirmation removes all temporary supplies/grime and
lands a whole-room ring/sparkle into the bright settled studio. The supply
feedback animation no longer queues the regular Castle Logo activity, so the
clean room settles visibly before any later optional picker is opened by a new
tap.

## Strong-room qualities absent from weaker baselines

- One unmistakable active target instead of several equally live objects.
- A large target-specific pointer physically attached to that target.
- Competing controls and ambient actors suppressed during focused work.
- Ordered actions whose result is visible before the next action begins.
- A character or fixture response after each meaningful beat.
- A strong value/occupancy difference between dirty and clean states.
- A payoff that changes the room and advances the story, not only a counter.
- Immediate monotonic save before celebratory animation.
- Stable 2D silhouettes at 1280×720 Mobile scale.

## Remaining deficit list

- Generated targets are intentionally bold and sticker-readable; owner art
  review must decide whether their saturation/outline weight fits the rooms.
- Pool remains the richest character/environment payoff; Art’s reward is
  primarily restoration plus the attack customizer rather than a new friend.
- Child observation and Lenovo Tab M11 performance remain external gates.
- The canonical legacy Day One integration probe has one unrelated stale
  `complete_tutorial("bathroom")` assertion; see `rollback_package/TEST_LOG.md`.
- Superseded captures remain under ignored audit paths for comparison and must
  not be mistaken for final evidence.

## Review images

- Pool dirty: `visuals/candidate_v3/pool/00a_dirty_algae_tangle.png`
- Pool clean: `visuals/candidate_v3/pool/08_rumi_reveal.png`
- Bathroom dirty: `visuals/candidate_v5/bathroom/00a_dirty_soap_splatter.png`
- Bathroom clean: `visuals/candidate_v5/bathroom/09_clean_pool_route.png`
- Bathroom no-overdraw reveal: `visuals/candidate_v5/bathroom/08_whole_room_sparkle.png`
- Stuffie dirty: `visuals/candidate_v6/stuffie/00_dirty_loose_stuffing.png`
- Stuffie rescue: `visuals/candidate_v6/stuffie/03_standing_rescue_payoff.png`
- Stuffie clean: `visuals/candidate_v6/stuffie/04_settled_clean_playroom.png`
- Stuffie adoption: `visuals/candidate_v6/stuffie/05_focused_adoption_tutorial.png`
- Art dirty: `visuals/candidate_v7/art/00a_dirty_rainbow_spill.png`
- Art ordered cleanup: `visuals/candidate_v7/art/00_loose_supplies.png`
- Art reveal: `visuals/candidate_v7/art/07_whole_room_sparkle.png`
- Art clean: `visuals/candidate_v7/art/08_clean_art_room.png`

Final Luna/Sol implementation scores are recorded in `RUBRIC.md`. They are
agent-evaluated implementation evidence, not human/device certification.

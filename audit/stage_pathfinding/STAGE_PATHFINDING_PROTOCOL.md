# Stage Pathfinding Protocol v1

This protocol applies to every `avatar_locomotion` stage and to every source
stage that launches a `fixed_minigame`. It is a child-readable travel rule:
Roshan moves to the thing first, then the thing responds.

For each interactive object, the runtime manifest must declare a stable
`object_id`, `approach_point` in stage coordinates, `arrival_radius`, `action`
and `return_target`. A tap on the object and a drag ending on the object both
create the same travel request. The request is idempotent: repeated taps do not
stack actions or teleport Roshan. While travelling, the pointer and a short
voice cue identify the destination. On arrival, stop movement, clear velocity,
confirm the distance test, and invoke the action exactly once. A direct tap may
only invoke immediately when Roshan is already within `arrival_radius`.

Doors follow the same contract. Tapping or dragging to a door selects its
visible destination; arrival at the door activates the transition. Releasing a
drag over the door/object commits the same queued action; releasing over an
allowed floor commits movement only. An interrupt, back action, or new target
cancels the prior request without changing progress. On return, restore
the exact source stage, room variant, camera coordinate and save state.

Accessibility is explicit and defaults to closed. Only declared connected floor
lanes (or declared swim lanes in a swimming stage) permit travel. Painted walls,
fixture bodies, furniture, railings, garden beds, canal water, backdrop-only
platforms and off-screen areas are inaccessible unless that exact stage declares
a usable route. A visible doorway is a transition target, not permission to walk
through its wall. An object is approached at its reachable floor contact; its
painted center is never used as a fallback destination. Sitting, lying down or
other object acting may use a separately authored action socket after arrival,
but cannot turn the fixture into a free-walking shortcut.

Routes retain every corner and junction. Disconnected destinations fail closed
without awarding or losing progress; they never fall back to a straight chord.
Route review checks the whole Roshan silhouette and fixture clearance as well as
her feet. Diagnostic line widths in the review atlas are not a playable corridor
or proof that the sprite clears nearby furniture.

Every walkable stage needs an authored walk lane, obstacle envelopes, a safe
spawn, and a safe recovery point. Leaving the playable polygon must clamp to
the nearest lane point or recover to the last safe point, clear velocity, and
keep all rewards/progress. OOB is never a fail state. The recovery cue must be
picture-first and voiced; it must not depend on reading.

Validation is a matrix, per stage and per object: (1) tap from far away reaches
the approach point before action; (2) drag from far away does the same; (3) tap
while already near performs once; (4) cancellation does not perform; (5) OOB
recovers without progress loss; (6) door arrival reaches the declared target;
(7) back/finish returns to the exact source variant and coordinate; (8) zero
input does not advance or win. Opera act entries are avatar-locomotion seam
entries even when they enter a fixed activity: they prove room travel, pointer
release/arrival, and exact board return. Separate `opera.surface.*` entries
cover fixed board internals. Other fixed minigames run the seam rows only; their
internal board does not need avatar pathfinding. Spatial 3D debt is reported as
debt until its 2D migration passes the same matrix.

Minimal reproductions should retain the real minigame controller and approved
existing art references while reducing the scene to one route, one object,
one door, and one OOB edge. They are diagnostic fixtures, never replacement
gameplay or new art. The Opera Doctor fixture is mandatory because its patient
station must demonstrate approach-before-care for every patient action.

# Pearl Castle Runtime Evidence

These screenshots are review evidence, not runtime textures. Godot does not
load these folders into the castle. They remain in the repository so rejected
art decisions can be compared instead of silently overwritten.

## `runtime_rejected_8d9c25e/`

First six-view Mobile capture. Rejected because the retained generic throne
crossed Huluu's cutout, outdoor cloud landmarks did not read as furniture,
sconces read as bulbs attached to columns, and two cameras failed to frame the
work they claimed to review.

## `runtime_rejected_7a65ec7/`

Second eleven-view Mobile capture. Structural CI was green, but the art pass
was rejected as incomplete. The return gate opened onto a blank wall; the Toy
Room, bedroom, music room, undercroft, pantry, craft room, bath, Dreaming Floor,
and back chamber still contained uncaptured or newly exposed blockout props.
Several room cameras also clipped walls or ceilings.

## `runtime_rejected_50b1907/`

Third seventeen-view Mobile capture from fully green CI run `29663467793`.
Rejected after human inspection because opaque navy wrapper meshes hid the
colored bodies of the Toy Room blocks, storage barrels/crates, wardrobe sides,
and chest lids. The same pass exposed a thin Toy Room composition, a repeated
straight storage row, a weak music-room focal point, and an incomplete craft
fish bitmap. These frames are the negative control for the material-visibility
correction; green CI and complete capture count did not make them acceptable.

## Final Candidate

The final seventeen-view Mobile evidence belongs in a sibling folder named
`runtime_candidate_<commit>/` only after the full import, analyzer, gameplay,
and capture workflow is green. Candidate does not mean owner-accepted 5/5.

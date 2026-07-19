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

## `runtime_rejected_2920da1/`

Fourth seventeen-view Mobile capture from fully green CI run `29665038876`.
The material-visibility repairs worked, but the set was rejected because the
Royal Bedroom camera sat behind the wardrobe and the undercroft sightline hid
most of its supposedly improved storage composition. It also predates the
merged Opera House gate, whose primitive marquee required its own authored-art
pass. These frames prove that technical validity and an apparently complete
shot list still fail when review cameras do not expose the claimed work.

## `runtime_rejected_37c238a/`

Fifth eighteen-view Mobile capture from fully green CI run `29666433765`.
The bedroom camera and Opera asset integration were technically corrected, but
the undercroft props showed their undecorated backs and crowded the cart, the
treasure arch missed the chest along the oblique review sightline, and the
Opera veil revealed glowing stone rather than reading as a destination. The
wardrobe front was also outside the evidence radius. These frames are retained
as the negative control for orientation, portal-depth, and sightline alignment.

## `runtime_rejected_affb617/`

Sixth nineteen-view Mobile capture from fully green CI run `29667302052`.
The undercroft facing, treasure niche, Royal Loo, bedroom bed, music room, toy
room, Cloud Lounge, and star chamber remained sound. Promotion was still
rejected because the transparent Opera field transmitted masonry and read as a
painted wall, the wardrobe evidence still read primarily as a giant mirror
rather than a dress-up storage object, the pantry shelf reduced to repeated
cylinders, and the entrance motif frame exposed a broad flat mauve wall around
the exit gate. These frames are retained as the negative control for role
readability, container variety, opaque destination fields, and full-room
material treatment.

## `runtime_rejected_dec3a2c/`

Seventh nineteen-view Mobile capture from fully green CI run `29676117040`.
This short-lived entrance-reveal experiment added tall gold trim strips around
the return gate. The run passed import, analyzer, gameplay probes, and capture
upload, but visual review rejected the strips as floating construction lines
that made the entrance read worse. Commit `ffae3fe` reverts the experiment.

## `runtime_candidate_ffae3fe/`

Current nineteen-view Mobile candidate from fully green CI run `29676569723`.
This is the `13b58d1` role-readability correction with the rejected `dec3a2c`
entrance experiment reverted. It keeps the opaque Opera vista, remodeled
wardrobe, remodeled pantry, entrance wall treatment, Royal Loo correction,
undercroft facing, treasure alignment, and all prior accepted room fixes.
Candidate evidence means ready for owner review; it is not self-awarded 5/5.

## Final Candidate

The current final candidate is `runtime_candidate_ffae3fe/`. Future candidates
must use a sibling folder named `runtime_candidate_<commit>/` only after the
full import, analyzer, gameplay, and capture workflow is green. Candidate does
not mean owner-accepted 5/5.

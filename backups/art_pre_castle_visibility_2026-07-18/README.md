# Pearl Castle Material-Visibility Rollback

This folder preserves the complete pearl-castle source/runtime snapshot and the
fifteen directly affected runtime GLBs replaced after the Mobile review of
commit `50b1907`. The rejected renders showed that complete navy outline shells
were hiding the intended colored bodies on blocks, chests, storage, wardrobe,
music keys, pantry jars, and the craft easel.

`pearl_castle_kit_50b1907.zip` contains the full forty-nine-asset kit, editable
Blender source, generator, castle integration, and acceptance probe exactly as
committed. SHA-256:

`FC573357EF917A5E9032AE3B1C25FAA6FBD537F0797E16C43563FBCE5BB277C6`

The files retain their repository-relative path below this folder. To restore a
specific prior object, copy only that GLB back to
`assets/castle/pearl_kit/`, run the Godot import, and review the affected room.
The earlier full pre-pass archive remains at
`backups/art_pre_castle_pearl_2026-07-18/`.

The corresponding seventeen rejected Mobile captures are retained at
`assets_src/blender/qa_pearl_castle_kit/runtime_rejected_50b1907/`.

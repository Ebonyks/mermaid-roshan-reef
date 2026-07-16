# Pre-landmark art backup

This folder preserves the external assets that supplied the previous Butterfly
Gate routes before the 2026-07-15 landmark rebuild. The prior procedural stars
and clouds live in Git history immediately before the rebuild commit; they did
not have standalone source-art files to copy.

The live game no longer loads these backup copies. Restore an individual asset
only together with its former runtime constructor from Git, because the new
gate, stars, and clouds share `scripts/landmark_art.gd`.

Protected book art and family character assets are not included or modified.

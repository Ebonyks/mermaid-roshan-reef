# Pre-remediation art backup

This folder contains the original `origin/master` versions of every raster file
overwritten by art-remediation Batches 02-04, plus the complete replaceable fish
layer trio and dormant terrain inventory promoted in the systematic pass. Paths
below this folder mirror their runtime paths.

`manifest.json` records the source commit and SHA-256 hashes for both the old and
current files. Rebuild the archive with:

```powershell
C:\Users\Peter\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe tools/archive_art_before_replacement.py
```

To restore one disputed asset, copy its mirrored file back to the same path in
the repository, then run the normal Godot import and probe gates. Example:

```powershell
Copy-Item backups/art_pre_remediation_2026-07-15/assets/mg/tree.png assets/mg/tree.png -Force
```

Legacy low-score GLBs are not duplicated here because the remediation routes
retain them at their original `assets/` paths as missing-file fallbacks. Reverting
the relevant route restores them immediately without adding duplicate model data.

Protected book art, family cutouts, voices, and child-owned toy art are not
copied or modified by this archive.

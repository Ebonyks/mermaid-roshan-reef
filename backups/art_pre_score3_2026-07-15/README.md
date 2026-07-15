# Pre-score-3 art backup

This folder mirrors every runtime raster overwritten by the score-3 rebuild.
It contains the previous dirt, grass, sand, snow, soft-snow, garden seed, and
garden butterfly files. Protected book art, family cutouts, voices, and toy
references were not modified or copied.

Restore every archived raster from the repository root with:

```powershell
powershell -ExecutionPolicy Bypass -File backups/art_pre_score3_2026-07-15/restore.ps1
```

To restore one file, copy its mirrored path back into `assets/`, then run the
normal Godot import and probe gates. Code routes and newly added story cards are
reverted through Git; this archive exists for fast visual A/B testing of the
overwritten files.

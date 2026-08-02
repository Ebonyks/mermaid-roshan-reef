# Pearl Castle Final-Polish Rollback

Created: 2026-07-18

Source commit: `affb617d2323ef9ddb3d22c12d678efb9e02a35c`

This archive preserves the two runtime GLBs replaced by the final-polish pass
after the `affb617` Mobile review. These files are kept under `backups/` and
are not loaded by the game.

## Files

| Archived file | Original runtime path | SHA-256 |
|---|---|---|
| `pearl_pantry_shelf_affb617.glb` | `assets/castle/pearl_kit/pearl_pantry_shelf.glb` | `FA41D8201EF96628062FC8CCCC13530A7B8A625D6D65DE54B4E821E3236A14A1` |
| `pearl_shell_wardrobe_affb617.glb` | `assets/castle/pearl_kit/pearl_shell_wardrobe.glb` | `E18E2936C9C94A1DF8ADE1221B062706A770EE9BF35BB5DF88C75B3DF646AF57` |

## Rollback

To inspect the exact pre-polish source code and scene state, use:

```powershell
git show affb617d2323ef9ddb3d22c12d678efb9e02a35c:tools/build_pearl_castle_kit.py
git show affb617d2323ef9ddb3d22c12d678efb9e02a35c:scripts/arena/castle_hall.gd
git show affb617d2323ef9ddb3d22c12d678efb9e02a35c:scripts/probe_castle_pearl_art.gd
```

The final-polish pass supersedes these two GLBs with a clearer wardrobe role
and a pantry shelf whose contents vary by silhouette and organization, not
only by color.

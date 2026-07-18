# Mermaid Roshan Art Asset Library

This document is the entry point for finding game art, source files, rejected
experiments, review renders, and rollback copies. No artwork is discarded just
because it is not currently used by the game.

## Storage map

| Location | Meaning | Included in Godot imports |
| --- | --- | --- |
| `assets/` | Approved runtime pool. These files are available to scenes and scripts, although not every file is necessarily referenced by the current build. | Yes |
| `assets_src/` | Editable Blender files, image-generation originals, and QA renders used to make approved assets. | No (`.gdignore`) |
| `gen2/generated/` | Earlier generated candidates, alternates, and rejected experiments retained for comparison or future rework. Presence here is not approval. | No (`gen2/.gdignore`) |
| `backups/` | Exact pre-replacement art retained for one-step visual rollback. | No (`.gdignore`) |
| `audit/` | Contact sheets, screenshots, score ledgers, and visual review evidence. | No (`.gdignore`; probes may still write screenshots by absolute path) |
| `art_library/candidates/` | Unintegrated art recovered from work in progress or parallel branches. Files remain byte-for-byte candidates until reviewed. | No (`.gdignore`) |
| `tools/out/` | Tool-source packs, generated model renders, and QA output retained for development reference. | No (`tools/.gdignore`; probes may still write screenshots by absolute path) |
| `disabled_addons/` | Art shipped with disabled development add-ons. | No |
| Other indexed paths | Project icons or support artwork outside the main collections. | As recorded per file in the inventory |

## Disposition rules

- **Integrated / success:** the shipping copy belongs under `assets/`; its
  editable source and QA render remain under `assets_src/`.
- **Candidate / undecided:** keep it under `gen2/generated/` or
  `art_library/candidates/`. Do not silently promote it into `assets/`.
- **Rejected but worth retaining:** keep the original generation in
  `gen2/generated/`; record the reason in the relevant audit ledger when known.
- **Replaced / rollback:** store the exact superseded runtime file under the
  dated directory in `backups/`.
- **Book and family originals:** retain their canonical files in the protected
  `assets/book/`, `assets/audio/voices/`, and `assets/characters/friends/`
  locations. Archiving must never alter or recompress them.

## Inventory

`art_library/ART_INVENTORY.csv` lists every raster image, texture, model, HDRI,
and Blender source currently retained in the project. It records collection,
disposition, Godot import scope, byte size, and SHA-256 so exact duplicates and
changed versions can be identified without relying on filenames.

Regenerate it after adding or moving art:

```powershell
python tools/build_art_inventory.py
```

The generated `art_library/ART_INVENTORY_SUMMARY.json` contains collection and
status totals. The inventory is descriptive: it never promotes a candidate,
deletes a reject, or rewrites an asset.

## Current candidate vault

`art_library/candidates/castle_differentiation_2026-07-17/` preserves nine
unintegrated castle and kitchen texture studies recovered from the parallel
castle-differentiation worktree. They are intentionally not wired into the
runtime pending visual review and material-level integration.

The Northern Kingdom models are not in the candidate vault: they were reviewed
and merged into `assets/northern/`, with Blender and QA sources under
`assets_src/blender/`.

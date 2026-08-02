# Decommissioned wing — quarantine for audit and deletion

Everything under `decommissioned/` is **out of service**. It is kept in the
repository only so a human can audit it before it is deleted for good. Nothing
here ships, nothing here is imported by Godot, and nothing here should be cited
as current guidance.

## Rules

- **Do not read a document in this wing as instruction.** These are superseded
  work orders, one-shot batch logs, and audits of builds that no longer exist.
  If a rule matters it lives in `CLAUDE.md` / `AGENTS.md`, not here.
- **Do not add new work here.** This wing only shrinks.
- **Do not delete anything without owner sign-off.** That is the whole point of
  the staging step — see "Deletion process" below.
- Nothing in this wing may be referenced by `scripts/`, `scenes/`,
  `project.godot`, or the shipped `assets/` tree. If you find such a reference,
  the item was quarantined in error — restore it and fix `MANIFEST.md`.

## How it is kept inert

| Guard | Effect |
| --- | --- |
| `decommissioned/.gdignore` | Godot's importer skips the whole wing — no import time, no NPOT deadlock risk, no `.godot` cache churn. |
| `exclude_filter` in `export_presets.cfg` | `decommissioned/*` is stripped from both APK presets, so the phone build does not grow. |

**Neither guard is what keeps the APK small — this wing was never in it.**
Every directory moved here except `tmp/pdfs` already carried a `.gdignore`
before the move, so Godot never saw any of it and the APK never contained it.
Decommissioning this content therefore saves **0 bytes** on the phone. See
`MANIFEST.md` § "Size accounting" for the real numbers.

The guards still matter, for a narrower reason: four items lost their *parent*
`.gdignore` when they were moved out from under `audit/`, `assets_src/` and
`disabled_addons/` — about 37 MB that would have become importable. The
wing-level `.gdignore` re-covers them; the export filter is belt-and-braces.

## What is NOT here (deliberately)

- **Kart racing** — `assets/kart/`, `scripts/kart.gd`, `KART_FEEL.md`,
  `RACE_ENGINE.md`, `RACE_FEEL_WORKORDER.md`. Owner-protected, stays live.
- **Fairy games** — `assets/fairy/`, `assets_src/fairy_v2|v4|v5/`,
  `scripts/games/fairy.gd`. Owner-protected, stays live.
- **Any audio.** See `MANIFEST.md` § "Audio — nothing decommissioned".
- **`assets/book/`, `assets/audio/voices/`, `assets/characters/friends/`** —
  irreplaceable per `CLAUDE.md`.
- **`attic/gabby/`** — already quarantined under its own documented path
  (IP hold). Left where `CLAUDE.md` says it is.

## Deletion process

1. Owner reads `MANIFEST.md` and marks entries **keep** / **delete**.
2. For anything marked delete, confirm the "Blast radius" column is still
   accurate (`grep -rn "<path>" scripts scenes tools project.godot`).
3. Delete in one commit per manifest group, referencing this file.
4. History still holds the bytes — the weekly CI backup bundle
   (`.github/workflows/backup.yml`, restore recipes in `BACKUP.md`) is the
   real safety net, not this directory.

Established 2026-08-02.

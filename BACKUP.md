# BACKUP.md — how this project is backed up, and how to restore it

The repo holds things that cannot be recreated: the scanned book art
(`assets/book/`), the recorded family voices (`assets/audio/voices/`), and
the friend portraits (`assets/characters/friends/`). Git history protects
against ordinary mistakes, but not against a bad force-push, a botched
history rewrite, or losing the GitHub repository itself. The child's save
file on the phone is equally irreplaceable and lives outside git entirely.

Four layers cover all of that:

| # | Layer | Where it lives | Cadence |
|---|-------|----------------|---------|
| 1 | In-game transactional save + `.bak` recovery (`scripts/save_state.gd`) | on the phone | every save |
| 2 | Save-file snapshot pulled off the phone (`./backup.sh` with phone on adb) | your backup folder | whenever you run it |
| 3 | CI full-repo git bundle (`.github/workflows/backup.yml`) | `project-backup` release tag | weekly + on demand |
| 4 | Offline full-repo git bundle (`./backup.sh`) | your backup folder / external drive | whenever you run it |

Layers 3 and 4 are *full mirrors*: every branch, every tag, all history,
verified with `git bundle verify` and restore-drilled (the bundle is cloned
back and the irreplaceable asset folders are checked non-empty) before they
count as a backup. A drill failure fails the run — a backup that can't
restore is treated as no backup.

## Making a backup

- **CI**: runs automatically Mondays 09:00 UTC once the workflow is on the
  default branch; run it any time from the Actions tab → "Project backup
  (git bundle)" → Run workflow. The two newest dated bundles are kept on
  the [`project-backup` release](https://github.com/Ebonyks/mermaid-roshan-reef/releases/tag/project-backup);
  older ones are pruned automatically.
- **Offline**: from a clone on your computer, `./backup.sh` (optionally
  `./backup.sh /media/usb-drive`). If the phone is plugged in with USB
  debugging on, it also snapshots the save file. Keeps the newest 5 bundles
  and 20 save snapshots in the destination.

## Restoring

### The whole repository (GitHub repo lost or wrecked)

```sh
git clone --branch master roshan-reef-YYYY-MM-DD.bundle roshan-reef
cd roshan-reef
git remote set-url origin git@github.com:Ebonyks/mermaid-roshan-reef.git
git push --mirror origin        # only onto a FRESH/empty repo
```

Check the checksum first if in doubt: `sha256sum -c roshan-reef-YYYY-MM-DD.bundle.sha256`.

### One branch or file that a bad push destroyed

```sh
# from inside your existing clone — bring in everything the bundle holds:
git fetch /path/to/roshan-reef-YYYY-MM-DD.bundle '+refs/*:refs/backup/*'
git branch dev-restored refs/backup/heads/dev        # rescue a branch
git checkout refs/backup/heads/master -- assets/book # rescue files only
```

(Bundles made by `backup.sh` from a work clone carry the remote branches
under `refs/backup/remotes/origin/...` — same commands, longer ref name.)

### The save file back onto the phone

```sh
adb push reef_save-YYYY-MM-DD_HHMMSS.json /data/local/tmp/reef_save.json
adb shell run-as com.ebonyks.roshanreef cp /data/local/tmp/reef_save.json files/reef_save.json
adb shell rm /data/local/tmp/reef_save.json
```

Do this with the game closed; the next launch loads it (and the in-game
recovery logic in `save_state.gd` re-validates it before trusting it).

## Limits worth knowing

- Release assets max out at **2 GiB**; the CI workflow fails loudly at
  1.9 GiB. If that ever trips, split the bundle (e.g. yearly incremental
  bundles via `git bundle create --since`) rather than shrinking history.
- GitHub pauses cron schedules after ~60 days without repo activity —
  re-enable from the Actions tab, or just run `./backup.sh` meanwhile.
- The CI bundle lives in the same GitHub account as the repo. It protects
  against repo-level damage, not account-level loss — that's what the
  offline `./backup.sh` copy on a drive at home is for. Aim for the 3-2-1
  rule: the GitHub repo, the `project-backup` release, and an offline copy.

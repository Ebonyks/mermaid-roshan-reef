#!/usr/bin/env bash
# backup.sh — one-command offline backup of the whole project, and of the
# phone's save file if a phone is plugged in.
#
#   ./backup.sh                    backup into ~/roshan-reef-backups
#   ./backup.sh /media/usb-drive   backup onto an external drive
#
# Run it from inside a clone of the repo. It fetches everything from GitHub,
# writes a verified full-history git bundle (every branch and tag — including
# the book art and recorded family voices), does a restore drill, and if a
# phone is on adb it also copies reef_save.json off the phone. The newest 5
# bundles and 20 save snapshots are kept; older ones are removed.
#
# CI runs the same kind of bundle weekly (.github/workflows/backup.yml, the
# `project-backup` release tag) — this script is the OFFLINE copy of the
# 3-2-1 rule: one copy that lives outside GitHub entirely.
#
# Restore instructions: BACKUP.md.

set -euo pipefail

PKG="com.ebonyks.roshanreef"
DEST="${1:-$HOME/roshan-reef-backups}"
STAMP=$(date +%Y-%m-%d_%H%M%S)
BUNDLE="${DEST}/roshan-reef-${STAMP}.bundle"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
	echo "Run this from inside the mermaid-roshan-reef clone." >&2
	exit 1
fi
mkdir -p "${DEST}"

echo "== Fetching everything from origin..."
git fetch --prune origin '+refs/heads/*:refs/remotes/origin/*' --tags

echo "== Writing full-history bundle to ${BUNDLE}"
git bundle create "${BUNDLE}" --all
git bundle verify "${BUNDLE}"
sha256sum "${BUNDLE}" > "${BUNDLE}.sha256"

echo "== Restore drill (cloning the bundle back and checking the irreplaceable assets)..."
DRILL=$(mktemp -d)
trap 'rm -rf "${DRILL}"' EXIT
git init -q "${DRILL}"
git -C "${DRILL}" fetch -q "${BUNDLE}" '+refs/*:refs/backup/*'
git -C "${DRILL}" checkout -q --detach refs/backup/remotes/origin/master 2>/dev/null \
	|| git -C "${DRILL}" checkout -q --detach refs/backup/heads/master
for d in assets/book assets/audio/voices assets/characters/friends; do
	N=$(find "${DRILL}/${d}" -type f 2>/dev/null | wc -l)
	if [ "${N}" -eq 0 ]; then
		echo "RESTORE DRILL FAILED: no files in ${d} — this bundle is NOT a good backup." >&2
		exit 1
	fi
	echo "   ${d}: ${N} files ok"
done
test -f "${DRILL}/project.godot" || { echo "RESTORE DRILL FAILED: project.godot missing." >&2; exit 1; }
echo "   restore drill passed"

# --- phone save file (the child's progress) --------------------------------
# Debug builds allow `adb exec-out run-as` to read the app's private files.
if command -v adb >/dev/null 2>&1 && adb get-state >/dev/null 2>&1; then
	echo "== Phone detected on adb — copying the save file..."
	SAVE_OUT="${DEST}/reef_save-${STAMP}.json"
	if adb exec-out run-as "${PKG}" cat files/reef_save.json > "${SAVE_OUT}" 2>/dev/null \
		&& grep -q '"pearls"' "${SAVE_OUT}"; then
		echo "   saved $(wc -c < "${SAVE_OUT}") bytes to ${SAVE_OUT}"
		adb exec-out run-as "${PKG}" cat files/reef_save.json.bak \
			> "${DEST}/reef_save-${STAMP}.json.bak" 2>/dev/null || true
	else
		rm -f "${SAVE_OUT}"
		echo "   could not read the save (game not installed, or not a debug build) — skipped."
	fi
else
	echo "== No phone on adb — repo backed up; save file skipped."
fi

# --- rotation --------------------------------------------------------------
{ ls -1t "${DEST}"/roshan-reef-*.bundle 2>/dev/null || true; } | tail -n +6 | while read -r OLD; do
	echo "== Pruning old backup $(basename "${OLD}")"
	rm -f "${OLD}" "${OLD}.sha256"
done
{ ls -1t "${DEST}"/reef_save-*.json 2>/dev/null || true; } | tail -n +21 | while read -r OLD; do
	rm -f "${OLD}" "${OLD}.bak"
done

echo
echo "Done. Backup lives in ${DEST}:"
ls -lh "${DEST}" | tail -n +2
echo
echo "Tip: copy ${DEST} to a second place (external drive / cloud folder) now and then."

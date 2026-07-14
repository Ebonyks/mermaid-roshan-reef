#!/usr/bin/env bash
# pull-apk.sh — one-command shortcut to grab the latest CI-built APK.
#
#   ./pull-apk.sh              latest master build (android-test channel)
#   ./pull-apk.sh graphics     graphics-fork channel (android-graphics)
#
# Downloads roshan-reef.apk into the current directory. If a phone is
# plugged in with USB debugging enabled (adb sees a device), it also
# installs it (`adb install -r` keeps the save file intact).
#
# On the phone itself, skip this script and bookmark the direct link:
#   https://github.com/Ebonyks/mermaid-roshan-reef/releases/download/android-test/roshan-reef.apk

set -euo pipefail

REPO="Ebonyks/mermaid-roshan-reef"
CHANNEL="android-test"
if [ "${1:-}" = "graphics" ]; then
	CHANNEL="android-graphics"
fi

URL="https://github.com/${REPO}/releases/download/${CHANNEL}/roshan-reef.apk"
OUT="roshan-reef.apk"

echo "Pulling ${CHANNEL} build from ${URL}"
curl -fSL --retry 3 --progress-bar -o "${OUT}" "${URL}"

# The first "updated_at" in the release JSON belongs to the APK asset
# (releases themselves only carry created_at/published_at).
BUILT=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/tags/${CHANNEL}" \
	| sed -n 's/.*"updated_at": *"\([^"]*\)".*/\1/p' | head -1) || BUILT=""
echo "Saved ${OUT}${BUILT:+ (built ${BUILT})}"

if command -v adb >/dev/null 2>&1 && adb get-state >/dev/null 2>&1; then
	echo "Phone detected on adb — installing (save data is kept)..."
	adb install -r "${OUT}"
	echo "Installed. Look for the Reef of Light icon on the phone."
else
	echo "No phone on adb — copy ${OUT} to the phone and open it to install."
fi

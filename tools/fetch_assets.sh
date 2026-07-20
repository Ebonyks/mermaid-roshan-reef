#!/usr/bin/env bash
# fetch_assets.sh — download candidate free-source marine assets into a staging
# dir and validate them. Safe: it does NOT overwrite assets/aquatic/. After it
# runs, review staging/ and run the swap step (see ASSET_AUDIT.md §5).
#
# REQUIRES: a Claude Code web session created with **Full** (or Custom-with these
# hosts) network access. The default "Trusted" level blocks every asset CDN.
# A policy change only applies to sessions started AFTER the change — a running
# session keeps the egress policy it booted with.
#
# Usage:  bash tools/fetch_assets.sh
set -uo pipefail
cd "$(dirname "$0")/.."
STAGE="assets/_staging"
mkdir -p "$STAGE"

ok=0; bad=0
# valid_glb <file> : true if the file begins with the glTF binary magic ("glTF")
valid_glb(){ [ -s "$1" ] && [ "$(head -c4 "$1" | tr -d '\0')" = "glTF" ]; }

note(){ printf '  %s\n' "$*"; }
hr(){ printf '%s\n' "----------------------------------------------------------------"; }

# --- 0. connectivity gate ---------------------------------------------------
hr; echo "[0] Connectivity check (expect 2xx/3xx if Full access is live)"
for h in poly.pizza github-cloud.githubusercontent.com; do
  c=$(curl -s -o /dev/null -w "%{http_code}" --max-time 12 "https://$h" 2>/dev/null)
  note "$c  $h"
  if [ "$c" = "000" ]; then
    echo "!! $h unreachable — this session is still on a restricted policy."
    echo "!! Start a FRESH web session after setting network access to Full, then re-run."
    [ "$h" = "poly.pizza" ] && exit 2
  fi
done

# --- 1. iR Engine ocean pack via Git-LFS (deterministic, matches many species)
hr; echo "[1] iR Engine ocean pack (Git-LFS) -> $STAGE/ocean"
if ! command -v git-lfs >/dev/null 2>&1 && ! git lfs version >/dev/null 2>&1; then
  echo "   installing git-lfs…"
  (apt-get update -qq && apt-get install -y -qq git-lfs) >/dev/null 2>&1 || \
    note "apt install failed — if git-lfs is missing the LFS pull will no-op (pointers stay)."
fi
git lfs install >/dev/null 2>&1 || true
rm -rf "$STAGE/ocean_src"
if GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --filter=blob:none \
     https://github.com/ir-engine/ir-engine-assets-basic "$STAGE/ocean_src" >/dev/null 2>&1; then
  ( cd "$STAGE/ocean_src" && git sparse-checkout set assets/ocean >/dev/null 2>&1 || true
    git lfs pull --include "assets/ocean/*" >/dev/null 2>&1 || true )
  mkdir -p "$STAGE/ocean"
  find "$STAGE/ocean_src/assets/ocean" -maxdepth 1 -iname '*.glb' 2>/dev/null | while read -r f; do
    cp "$f" "$STAGE/ocean/" 2>/dev/null
  done
else
  note "clone failed (host blocked?)"
fi

# --- 1b. sanitize staging: models only, no third-party instruction files ----
# The clone above is third-party content. Agent-instruction / config files
# inside it (CLAUDE.md, AGENTS.md, .claude/, .codex/, .github/, .vscode/)
# would be loaded as *trusted* context by coding agents that later work in
# this tree — a prompt-injection path. Keep only the extracted models.
hr; echo "[1b] Sanitize staging (drop clone + any agent-instruction files)"
rm -rf "$STAGE/ocean_src"
find "$STAGE" -depth \( -name 'CLAUDE.md' -o -name 'AGENTS.md' -o -name 'GEMINI.md' \
  -o -name '.claude' -o -name '.codex' -o -name '.github' -o -name '.vscode' \
  -o -name '*.sh' -o -name '*.py' -o -name '*.gd' \) \
  -exec rm -rf {} + 2>/dev/null || true

# --- 2. validate everything we pulled --------------------------------------
hr; echo "[2] Validate staged GLBs (real glTF vs LFS-pointer/HTML)"
shopt -s nullglob
for f in "$STAGE"/ocean/*.glb; do
  if valid_glb "$f"; then ok=$((ok+1)); printf '  ✓ %6sB  %s\n' "$(wc -c <"$f")" "${f#"$STAGE"/}"
  else bad=$((bad+1)); printf '  ✗ POINTER/INVALID  %s\n' "${f#"$STAGE"/}"; fi
done

hr
echo "Valid GLBs: $ok   Invalid/pointers: $bad"
echo "Staged under: $STAGE/"
echo
echo "NEXT: review $STAGE/ocean, map names to assets/aquatic/ per ASSET_AUDIT.md §5,"
echo "      then copy the chosen files over the old itch.io pack and commit."
echo "      (For species the ocean pack lacks — Penguin/Turtle/Squid/Lobster/shells/rocks —"
echo "       pull Quaternius CC0 sets from poly.pizza; URLs verified live in that session.)"

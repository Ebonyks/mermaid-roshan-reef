#!/usr/bin/env bash
# Bake the game's four outfits onto a clip atlas with the production builder
# (tools/build_fashion_outfits.gd -- --fit=... --out=...), in a throwaway Godot project that holds
# only the builder, its garment/fit inputs and the clip atlas, so the game's own outputs are untouched.
#   scripts/bake_clip_outfits.sh <clip dir relative to the repo root>   (GODOT=path to 4.7.2)
set -euo pipefail
ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"; CLIP="$1"; GODOT="${GODOT:-godot}"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
for f in tools/build_fashion_outfits.gd assets_src/fashion_designer/party_garment_v1/pose_fit.json \
         assets_src/fashion_designer/party_garment_v1/native.png "$CLIP/atlas.png" "$CLIP/pose_fit_clip.json"; do
  mkdir -p "$T/$(dirname "$f")"; cp "$ROOT/$f" "$T/$f"
done
printf 'config_version=5\n\n[application]\nconfig/name="clip_outfits"\n' > "$T/project.godot"
"$GODOT" --headless --path "$T" -s tools/build_fashion_outfits.gd -- "--fit=res://$CLIP/pose_fit_clip.json" "--out=res://$CLIP/outfits/" | grep FASHION_ASSETS
mkdir -p "$ROOT/$CLIP/outfits"; cp "$T/$CLIP/outfits/"*.png "$ROOT/$CLIP/outfits/"

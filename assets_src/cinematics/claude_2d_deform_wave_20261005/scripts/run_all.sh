#!/bin/sh
# Rebuild the Roshan 2D-deformation wave study from the approved atlas. CPU only; ~5 minutes.
# Requires: python3 with numpy scipy opencv-python-headless pillow; ffmpeg; git (for the Codex comparison frames).
set -e
cd "$(dirname "$0")"
python3 -B masks.py          # arm/body split per key (skin component + outline ring)
python3 -B track.py          # waist root per key (template match)
python3 -B anchors.py        # strong body anchors K0 -> K1..K3
python3 -B corr.py           # dense body correspondences, consistency-filtered
python3 -B fill.py           # arm-occluded body pixels filled from donor keys (approved pixels)
python3 -B codex_inputs.py   # Codex comparison take + K0 guide from the pinned commit
python3 -B fit_codex_canvas.py
python3 -B produce.py        # native frames (committed) + review frames (work dir)
python3 -B master.py         # layered Aseprite master + round-trip check
python3 -B videos.py         # review/comparison videos and sheets
python3 -B verify.py
python3 -B manifest.py

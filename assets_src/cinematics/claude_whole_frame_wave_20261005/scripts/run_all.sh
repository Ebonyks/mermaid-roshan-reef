#!/bin/sh
# Rebuild the Roshan whole-frame wave (revision 2) from the approved atlas. CPU only; about 8 minutes.
# Requires: python3 with numpy scipy opencv-python-headless pillow; ffmpeg.
set -e
cd "$(dirname "$0")"
python3 -B masks.py      # per key: where its own arm is, so the arm can bend with the rest of that drawing
python3 -B track.py      # waist root per key
python3 -B anchors.py    # strong body anchors K0 -> K1..K3
python3 -B corr.py       # dense whole-figure correspondences, consistency-filtered
python3 -B schedule.py   # one source drawing per frame, one switch per beat
python3 -B produce.py    # native whole frames (committed) + 3x review frames (work dir)
python3 -B master.py     # one-layer Aseprite master + round-trip check
python3 -B videos.py     # review movie, native 3x movie, GIF
python3 -B verify.py
python3 -B manifest.py

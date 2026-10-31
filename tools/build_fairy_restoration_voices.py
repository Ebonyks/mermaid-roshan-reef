"""Add isolated prototype cues using the existing Roshan Kokoro voice pipeline.

Never writes to protected assets/audio/voices/. Model and voice stay local.
"""
import json
from pathlib import Path
import sys

import make_voices


def main():
    root = Path(__file__).resolve().parents[1]
    cues = json.loads((root / "assets_src/prototypes/fairy_restoration_2026-09-30/VOICE_CUES.json").read_text(encoding="utf-8"))
    destination = root / "assets/prototypes/fairy_restoration/voices"
    destination.mkdir(parents=True, exist_ok=True)
    arguments = [sys.argv[0], "--out", str(destination)]
    for key, text in cues.items():
        make_voices.LINES[key] = ("roshan", text)
        arguments.extend(["--line", key])
    sys.argv = arguments
    make_voices.main()


if __name__ == "__main__":
    main()

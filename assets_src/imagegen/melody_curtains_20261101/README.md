# R120 painted theatre curtain sources

Two static built-in ImageGen calls create a pink left curtain and lavender right curtain for the existing Melody composition. Native outputs are preserved byte-for-byte; editable Aseprite masters reproduce their RGBA pixels exactly. Whole uniform exports use bilinear scaling only. No crop, stretch, repaint, alpha edit or new animation is used.

[Derivation and exact hashes](DERIVATION.json), [call accounting](GENERATION_ACCOUNTING.json), [actual scene/material binding](REFERENCE_BINDING.json), [left prompt](LEFT_PROMPT.txt), [right prompt](RIGHT_PROMPT.txt), [left native inspection](LEFT_NATIVE_INSPECTION.json), and [right native inspection](RIGHT_NATIVE_INSPECTION.json).

The current runtime files are `assets/melody/curtain_left_painted.png` and `assets/melody/curtain_right_painted.png`, both 384×768. The earlier 512×1024 whole exports and masters remain technical intermediates outside runtime. Two runtime PNGs and four technical exports are different counts, not four accepted art pieces. The backend exposes no model selector/version; no ImageGen version or price is claimed.

The native viewport, static object comparison, full machine validation and formal/device/child/owner acceptance are separate. These sources grant no Dev integration or final acceptance. The owner specifically resumed candidate production while keeping Dev frozen.

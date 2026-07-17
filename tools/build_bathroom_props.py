#!/usr/bin/env python3
"""Rebuild the three image-guided Royal Bathroom fixtures in Blender.

Each fixture has its own audited builder so its sculpted geometry, material
roles, exact runtime bounds, editable source scene, and QA render stay easy to
review. Run this orchestrator with Blender, not the system Python:

  blender --background --python tools/build_bathroom_props.py
"""

from __future__ import annotations

from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]
BUILDERS = (
	"build_bathroom_bathtub_v2.py",
	"build_bathroom_sink_v2.py",
	"build_bathroom_toilet_v2.py",
)

for builder_name in BUILDERS:
	builder_path = ROOT / "tools" / builder_name
	print(f"BATHROOM_BUILD|START|{builder_name}", flush=True)
	runpy.run_path(str(builder_path), run_name=f"__bathroom_{builder_path.stem}__")
	print(f"BATHROOM_BUILD|OK|{builder_name}", flush=True)

#!/usr/bin/env python3
"""Create a hashed, pre-generation job for one full-frame cinematic repair."""
from __future__ import annotations

import argparse
import hashlib
import json
import string
from pathlib import Path


ALLOWED_FIELDS = {
    "canvas_height",
    "canvas_width",
    "delta",
    "frame",
    "frame06",
    "previous_edge",
    "previous_frame",
    "previous_frame06",
    "target_edge",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_job(
    template: Path,
    previous_frame_path: Path,
    position_guide: Path,
    output: Path,
    frame: int,
    previous_frame: int,
    target_edge: int,
    previous_edge: int,
    canvas_width: int,
    canvas_height: int,
) -> dict[str, object]:
    if "build" not in {part.lower() for part in output.resolve().parts}:
        raise ValueError("regeneration jobs must stay under an ignored build directory")
    if output.exists():
        raise ValueError(f"output already exists: {output}")
    if frame <= previous_frame:
        raise ValueError("frame must be after previous-frame")
    if not 0 <= previous_edge < canvas_width:
        raise ValueError("previous-edge must be inside the canvas")
    if not 0 <= target_edge < canvas_width:
        raise ValueError("target-edge must be inside the canvas")
    fields = {
        "canvas_height": canvas_height,
        "canvas_width": canvas_width,
        "delta": target_edge - previous_edge,
        "frame": frame,
        "frame06": f"{frame:06d}",
        "previous_edge": previous_edge,
        "previous_frame": previous_frame,
        "previous_frame06": f"{previous_frame:06d}",
        "target_edge": target_edge,
    }
    template_text = template.read_text(encoding="utf-8")
    formatter_fields = {
        field_name
        for _, field_name, _, _ in string.Formatter().parse(template_text)
        if field_name
    }
    unknown_fields = formatter_fields - ALLOWED_FIELDS
    if unknown_fields:
        raise ValueError(
            "unsupported template fields: " + ", ".join(sorted(unknown_fields))
        )
    prompt_text = template_text.format_map(fields)
    if not prompt_text.endswith("\n"):
        prompt_text += "\n"

    output.mkdir(parents=True)
    prompt_path = output / "prompt.txt"
    prompt_path.write_text(prompt_text, encoding="utf-8")
    job = {
        "schema": "cinematic-regeneration-job-v1",
        "frame": frame,
        "previous_frame": previous_frame,
        "target_edge": target_edge,
        "previous_edge": previous_edge,
        "delta": target_edge - previous_edge,
        "canvas": [canvas_width, canvas_height],
        "generation_method": "full_frame_image_generation",
        "temporal_derivation": "none",
        "prompt": {
            "path": str(prompt_path.resolve()),
            "sha256": sha256_file(prompt_path),
        },
        "template": {
            "path": str(template.resolve()),
            "sha256": sha256_file(template),
        },
        "generation_references": [
            {
                "path": str(previous_frame_path.resolve()),
                "sha256": sha256_file(previous_frame_path),
                "role": "accepted_neighbor",
                "used_as_delivery_pixels": False,
            },
            {
                "path": str(position_guide.resolve()),
                "sha256": sha256_file(position_guide),
                "role": "position_only",
                "used_as_delivery_pixels": False,
            },
        ],
    }
    job_path = output / "job.json"
    job_path.write_text(json.dumps(job, indent=2) + "\n", encoding="utf-8")
    return job


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--previous-frame-path", type=Path, required=True)
    parser.add_argument("--position-guide", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--frame", type=int, required=True)
    parser.add_argument("--previous-frame", type=int, required=True)
    parser.add_argument("--target-edge", type=int, required=True)
    parser.add_argument("--previous-edge", type=int, required=True)
    parser.add_argument("--canvas-width", type=int, required=True)
    parser.add_argument("--canvas-height", type=int, required=True)
    args = parser.parse_args()
    for source in (
        args.template,
        args.previous_frame_path,
        args.position_guide,
    ):
        if not source.is_file():
            parser.error(f"source does not exist: {source}")
    if args.canvas_width < 2 or args.canvas_height < 2:
        parser.error("canvas dimensions must be at least 2")
    try:
        job = render_job(
            args.template,
            args.previous_frame_path,
            args.position_guide,
            args.output,
            args.frame,
            args.previous_frame,
            args.target_edge,
            args.previous_edge,
            args.canvas_width,
            args.canvas_height,
        )
    except ValueError as error:
        parser.error(str(error))
    print(
        "REGENERATION_JOB|"
        f"frame={job['frame']}|target_edge={job['target_edge']}|"
        f"output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

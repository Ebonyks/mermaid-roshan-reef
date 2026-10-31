"""Lossless PNG runtime preparation; no painting, recoloring or alpha repair.

Preserve every generated native. Uniformly downsample its alpha bounds to the
old plant's visible height and register the stem at the existing soil anchor.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "assets/mg/painted_quality_20261018"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    prompts = json.loads((HERE / "prompts.json").read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for entry in prompts["images"]:
        name = entry["id"]
        original = ROOT / f"assets/mg/{name}.png"
        native = HERE / f"{name}_native.png"
        if not native.exists():
            source = Path(re.search(r"as (C:.*?\.png) by default", entry["output_hint"]).group(1))
            shutil.copyfile(source, native)
        image = Image.open(native)
        assert image.mode == "RGBA", (name, image.mode)
        alpha = image.getchannel("A")
        assert alpha.getextrema() == (0, 255), name
        # ImageGen includes extremely faint isolated alpha wisps far outside
        # the object. Do not let those invisible pixels determine its size or
        # soil contact. Keep four native pixels around the solid silhouette,
        # preserving its antialiasing; no alpha values are repainted.
        solid = alpha.point(lambda value: 255 if value >= 16 else 0)
        solid_bounds = solid.getbbox()
        assert solid_bounds is not None
        bounds = (max(0, solid_bounds[0] - 4), max(0, solid_bounds[1] - 4),
            min(image.width, solid_bounds[2] + 4), min(image.height, solid_bounds[3] + 4))
        assert bounds is not None
        crop = image.crop(bounds)
        old = Image.open(original).convert("RGBA")
        old_bounds = old.getchannel("A").getbbox()
        target_height = 430 if name == "wateringcan" else old_bounds[3] - old_bounds[1]
        factor = min(target_height / crop.height, 440 / crop.width)
        size = (round(crop.width * factor), round(crop.height * factor))
        scaled = crop.resize(size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (512, 512))
        bottom = 471 if name == "wateringcan" else 451
        # Flowers may lean. Register the actual stem/soil contact rather than
        # centering an asymmetrical flower-head bounding box over the pot.
        strip_top = max(solid_bounds[1], solid_bounds[3] - 16)
        weights = [sum(alpha.getpixel((x, y)) for y in range(strip_top, solid_bounds[3]))
            for x in range(solid_bounds[0], solid_bounds[2])]
        contact_x = sum((solid_bounds[0] + x) * weight for x, weight in enumerate(weights)) / sum(weights)
        offset = (round(256 - (contact_x - bounds[0]) * factor),
            round(bottom - (solid_bounds[3] - bounds[1]) * factor))
        # Copy the RGBA pixels directly: using alpha as a paste mask a second
        # time would darken the authored antialiased contour.
        canvas.paste(scaled, offset)
        destination = OUT / f"{name}.png"
        canvas.save(destination, compress_level=9)
        rows.append({"id": name, "original": str(original.relative_to(ROOT)).replace("\\", "/"),
            "original_sha256": sha(original), "native": str(native.relative_to(ROOT)).replace("\\", "/"),
            "native_sha256": sha(native), "native_size": list(image.size), "native_mode": image.mode,
            "native_alpha_bounds": list(bounds), "runtime": str(destination.relative_to(ROOT)).replace("\\", "/"),
            "runtime_sha256": sha(destination), "runtime_size": [512, 512],
            "runtime_alpha_bounds": list(canvas.getchannel("A").getbbox()),
            "modifications": {"alpha_bounds_crop": list(bounds), "solid_alpha_bounds": list(solid_bounds),
                "registration_alpha_threshold": 16, "contact_x_native": contact_x, "uniform_scale": factor,
                "resample": "Pillow LANCZOS", "paste_offset": list(offset), "painting_or_alpha_repair": False},
            "status": "CANDIDATE_PENDING_RUNTIME_REVIEW", "attempts": 1})
    pot_native = HERE / "pot_native.png"
    pot = Image.open(pot_native)
    assert pot.mode == "RGBA" and pot.getchannel("A").getextrema() == (0, 255)
    pot_out = OUT / "pot.png"
    pot.resize((512, 512), Image.Resampling.LANCZOS).save(pot_out, compress_level=9)
    pot_record = {"native": str(pot_native.relative_to(ROOT)).replace("\\", "/"),
        "native_sha256": sha(pot_native), "runtime": str(pot_out.relative_to(ROOT)).replace("\\", "/"),
        "runtime_sha256": sha(pot_out), "attempts": 2,
        "rejected_take": {"path": "assets_src/imagegen/artwork_quality_20261018/pot_attempt01_rejected.png",
            "sha256": sha(HERE / "pot_attempt01_rejected.png"),
            "reason": "Gritty soil and insufficient illustrated contour"},
        "modifications": "Uniform 512 square downsample preserving alpha; soil center mounts at existing y615"}
    (HERE / "provenance.json").write_text(json.dumps({"provider": prompts["provider"],
        "model_revision": "unexposed", "seed": "unexposed", "request_ids": "unexposed",
        "scope": "Static game props; protected originals untouched; no animation or cinematic generation",
        "references": [{"path": "assets/castle/day_one_art_studio/magic_cleaning_brush.png",
            "role": "paint/contour quality only", "sha256": sha(ROOT / "assets/castle/day_one_art_studio/magic_cleaning_brush.png")}],
        "assets": rows, "pot": pot_record}, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(rows) + 1} RGBA 512x512 candidates; native originals preserved")

if __name__ == "__main__":
    main()

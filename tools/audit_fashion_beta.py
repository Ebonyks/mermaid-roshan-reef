"""Independent read-only beta clothing geometry/provenance gate; visual fit stays pending."""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("assets_src/fashion_designer/beta_20261025")
THEMES = ("ballet", "magician", "candy", "astronaut")
SLOTS = ("head", "body", "tail")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(path):
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def catalog(path):
    return json.loads(path.read_text(encoding="utf-8").split("data = ", 1)[1])


def check_layer(source, layer, row, spec):
    assert source.shape == layer.shape, ("geometry", row["path"])
    cw, ch = map(int, spec["cell"])
    columns = source.shape[1] // cw
    allowed = np.zeros(source.shape[:2], dtype=bool)
    count = 0
    for index, box in enumerate(row["fit"]):
        x0, y0, x1, y1 = map(int, box)
        assert 0 <= x0 < x1 <= cw and 0 <= y0 < y1 <= ch, ("slot bounds", row)
        x, y = index % columns * cw, index // columns * ch
        allowed[y+y0:y+y1, x+x0:x+x1] = True
        assert np.any(layer[y+y0:y+y1, x+x0:x+x1, 3]), ("empty fitted cell", row["path"], index)
        count += 1
    active = layer[:, :, 3] > 0
    assert not np.any(active & ~allowed), ("outside slot", row["path"])
    for x0, y0, x1, y1 in spec.get("protected_boxes", []):
        assert not np.any(active[y0:y1, x0:x1]), ("protected hand", row["path"])
    if row["slot"] != "head":
        assert np.all(layer[:, :, 3][active] == 255), ("layer alpha", row["path"])
        assert np.all(source[:, :, 3][active] == 255), ("source contour", row["path"])
        rgb = source[:, :, :3].astype(float) / 255
        skin = (rgb[:, :, 0] > rgb[:, :, 2] + .09) & (rgb[:, :, 1] > rgb[:, :, 2] + .025)
        assert not np.any(active & skin), ("skin exclusion", row["path"])
    return count


def run(root=ROOT):
    root = Path(root)
    generation = json.loads((root / SOURCE / "generation_manifest.json").read_text(encoding="utf-8"))
    expected = {f"{theme}_{slot}" for theme in THEMES for slot in SLOTS}
    assert {r["id"] for r in generation["rows"]} == expected and len(generation["rows"]) == 12
    for row in generation["rows"]:
        assert sha(root / row["path"]) == row["sha256"], ("native hash", row["path"])
        assert sha(root / row["reference"]) == row["reference_sha256"], ("style reference", row["id"])
        with Image.open(root / row["path"]) as image:
            assert image.mode == "RGBA" and image.getchannel("A").getextrema()[0] == 0, ("native transparency", row["id"])
    old = catalog(root / "assets/fashion/slots_v1/catalog.tres")
    beta = catalog(root / "assets/fashion/beta_20261025/catalog.tres")
    assert beta["fits"] == old["fits"], "Existing registration must not move"
    assert beta["items"][:len(old["items"])] == old["items"], "Existing clothing definitions changed"
    assert len(beta["items"]) == len(old["items"]) + 12
    for family, layers in old["layers"].items():
        assert all(beta["layers"][family].get(key) == value for key, value in layers.items()), "Existing layer replaced"
    derivations = json.loads((root / SOURCE / "derivations.json").read_text(encoding="utf-8"))
    assert sha_text(root / "tools/build_fashion_beta.gd") == derivations["builder_sha256"], "Builder changed after bake"
    assert sha_text(root / "assets/fashion/slots_v1/catalog.tres") == derivations["old_catalog_sha256"]
    outputs = derivations["outputs"]
    expected_rows = {(family, f"{slot}_{theme}_v1") for family in old["fits"] for slot in SLOTS for theme in THEMES}
    assert {(r["family"], r["item_id"]) for r in outputs} == expected_rows and len(outputs) == len(expected_rows)
    families = catalog(root / "assets/fashion/skin_engine_v2/catalog.tres")["families"]
    cells = 0
    for row in outputs:
        for field, digest in [("path", "sha256"), ("source", "source_sha256"), ("garment", "garment_sha256")]:
            assert sha(root / row[field].removeprefix("res://")) == row[digest], ("derivation hash", row[field])
        assert row["full_source_rect"] and not row["fixed_opacity_reduction"]
        source = np.array(Image.open(root / row["source"].removeprefix("res://")).convert("RGBA"))
        layer = np.array(Image.open(root / row["path"].removeprefix("res://")).convert("RGBA"))
        cells += check_layer(source, layer, row, families[row["family"]])
    licenses = (root / "ASSET_LICENSES.md").read_text(encoding="utf-8")
    for directory in [root / SOURCE / "native", root / "assets/fashion/beta_20261025"]:
        for path in directory.rglob("*.png"):
            relative = path.relative_to(root).as_posix()
            assert relative in licenses, ("missing license", relative)
            if "assets_src" not in relative:
                with Image.open(path) as image:
                    w, h = image.size
                    assert max(w, h) <= 1024 or (not w & (w-1) and not h & (h-1)), ("texture budget", relative)
    return {"new_pieces": 12, "new_layers": len(outputs), "cells": cells, "visual_fit_device_child_owner": "PENDING"}


if __name__ == "__main__":
    result = run()
    print("FASHION_BETA_AUDIT|ALL OK|", json.dumps(result))

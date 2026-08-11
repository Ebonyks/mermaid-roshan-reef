#!/usr/bin/env python3
"""Blocking artifact/provenance audit for the generated Opera rope hotspot."""

from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src/imagegen/opera_diegetic_hotspots_2026-08-09"
NATIVE = SOURCE / "native/magician_rope_native.png"
ALPHA = SOURCE / "magician_rope_alpha_native.png"
RUNTIME = ROOT / "assets/opera/worlds/hotspots/magician_rope.png"
REFERENCE = ROOT / "assets/opera/worlds/widgets/widget_trace_magician.png"
PROVENANCE = SOURCE / "PROVENANCE.json"
PROMPTS = SOURCE / "PROMPTS.md"
REVIEW = SOURCE / "REVIEW.md"
LICENSES = ROOT / "ASSET_LICENSES.md"

EXPECTED = {
    REFERENCE: ("7999afc7ea691a47dbd8b7d175e1f902a6d21ed8947f30da548e7f1bea37d1cd", (1024, 608)),
    NATIVE: ("00dc8d2ecba5f42720b883f0271baecd75c943a56f09f745c93635325bbed953", (1254, 1254)),
    ALPHA: ("89b39db5e096fd5cd1fda4bcd496deadf147d74c509bdff6cd510b44f553bed3", (1254, 1254)),
    RUNTIME: ("f38205f3e00ab8de0b1dd176a52c7535abcfa369eafa1fe1032eacb003fc9843", (512, 128)),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _component_sizes(mask: np.ndarray) -> list[int]:
    height, width = mask.shape
    seen = np.zeros(mask.shape, dtype=np.bool_)
    sizes: list[int] = []
    for y, x in zip(*np.nonzero(mask)):
        if seen[y, x]:
            continue
        seen[y, x] = True
        pending: deque[tuple[int, int]] = deque([(int(y), int(x))])
        size = 0
        while pending:
            cy, cx = pending.popleft()
            size += 1
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < height and 0 <= nx < width \
                        and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    pending.append((ny, nx))
        sizes.append(size)
    return sizes


def _audit_alpha(path: Path, expected_bbox: tuple[int, int, int, int],
                 expected_margins: tuple[int, int, int, int]) -> list[str]:
    failures: list[str] = []
    image = Image.open(path).convert("RGBA")
    pixels = np.asarray(image, dtype=np.uint8)
    alpha = pixels[:, :, 3]
    visible = alpha >= 16
    ys, xs = np.nonzero(visible)
    if not len(xs):
        return [f"{path}: empty alpha"]
    bbox = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    margins = (bbox[0], bbox[1], image.width - bbox[2], image.height - bbox[3])
    if bbox != expected_bbox:
        failures.append(f"{path}: alpha bbox {bbox}, expected {expected_bbox}")
    if margins != expected_margins:
        failures.append(f"{path}: alpha margins {margins}, expected {expected_margins}")
    components = _component_sizes(visible)
    if len(components) != 1:
        failures.append(f"{path}: {len(components)} alpha components, expected one")
    opaque = alpha >= 230
    green_spill = (pixels[:, :, 1] > pixels[:, :, 0] * 1.35) \
        & (pixels[:, :, 1] > pixels[:, :, 2] * 1.35) & opaque
    if int(green_spill.sum()) != 0:
        failures.append(f"{path}: {int(green_spill.sum())} opaque green-spill pixels")
    return failures


def main() -> int:
    failures: list[str] = []
    for path, (expected_hash, expected_size) in EXPECTED.items():
        if not path.is_file():
            failures.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        actual_hash = _sha256(path)
        if actual_hash != expected_hash:
            failures.append(
                f"{path.relative_to(ROOT)}: sha256 {actual_hash}, expected {expected_hash}")
        with Image.open(path) as image:
            if image.size != expected_size:
                failures.append(
                    f"{path.relative_to(ROOT)}: size {image.size}, expected {expected_size}")

    if ALPHA.is_file():
        failures.extend(_audit_alpha(ALPHA, (40, 509, 1215, 714), (40, 509, 39, 540)))
    if RUNTIME.is_file():
        failures.extend(_audit_alpha(RUNTIME, (16, 22, 496, 106), (16, 22, 16, 22)))

    for document in (PROVENANCE, PROMPTS, REVIEW):
        if not document.is_file():
            failures.append(f"missing evidence: {document.relative_to(ROOT)}")
    if PROVENANCE.is_file():
        try:
            record = json.loads(PROVENANCE.read_text(encoding="utf-8"))
            if record.get("qa_summary", {}).get("owner_human_review") != "pending":
                failures.append("PROVENANCE.json must not claim owner acceptance")
            if record.get("qa_summary", {}).get("floating_parts") != "pass":
                failures.append("PROVENANCE.json floating-parts review is not pass")
        except (json.JSONDecodeError, OSError) as error:
            failures.append(f"invalid PROVENANCE.json: {error}")
    if PROMPTS.is_file():
        prompt_text = PROMPTS.read_text(encoding="utf-8")
        if "exec-21e14c4c-d66c-40be-9c12-c41133917125.png" not in prompt_text \
                or "rejected" not in prompt_text.lower():
            failures.append("PROMPTS.md does not retain the rejected artifact attempt")
    if REVIEW.is_file() and "owner/human review pending" not in REVIEW.read_text(
            encoding="utf-8").lower():
        failures.append("REVIEW.md must leave owner/human review pending")
    if LICENSES.is_file() and "assets/opera/worlds/hotspots/magician_rope.png" \
            not in LICENSES.read_text(encoding="utf-8"):
        failures.append("ASSET_LICENSES.md is missing the runtime rope")

    if failures:
        for failure in failures:
            print(f"HOTSPOT_ART|FAIL|{failure}")
        return 1
    print("HOTSPOT_ART|result: ALL OK (4 hashes, 2 alpha states, 1 connected object)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

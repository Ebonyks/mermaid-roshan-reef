#!/usr/bin/env python3
"""Build the accepted Arborist 2D art package from preserved ImageGen natives.

The generated environment clean plates remain whole images.  This tool adds
only appearance-neutral edge continuation to reach the Opera 2048-square
master contract, then slices four non-overlapping 1024-square runtime tiles.

Chroma sheets are separated by an edge-connected matte.  The standard
imagegen chroma helper was run first and its alpha derivatives are preserved
in the source packet; edge connectivity is the accepted refinement because a
global colour-dominance matte erased coral wrap and aqua-water pixels inside
the subjects.  No delivered subject pixels are painted, warped, or repaired.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src/imagegen/opera_arborist_2026-08-09"
BACKDROPS = ROOT / "assets/opera/worlds/backdrops"
ARBORIST = ROOT / "assets/opera/worlds/arborist"
ACTORS = ROOT / "assets/opera/worlds/actors"
ANIMATION = ACTORS / "animation"
CRESTS = ROOT / "assets/opera/worlds/ui/crests"
PROPS = ROOT / "assets/opera/worlds/props"

RUNTIME_TREE_SIZE = 768
RUNTIME_CARD_SIZE = 512


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save(image: Image.Image, path: Path, outputs: list[dict[str, object]], role: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)
    outputs.append(
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256(path),
            "dimensions": [image.width, image.height],
            "role": role,
        }
    )


def _sample_key(rgb: np.ndarray) -> np.ndarray:
    height, width = rgb.shape[:2]
    span = max(8, min(height, width) // 40)
    samples = np.concatenate(
        [
            rgb[:span, :span].reshape(-1, 3),
            rgb[:span, width - span :].reshape(-1, 3),
            rgb[height - span :, :span].reshape(-1, 3),
            rgb[height - span :, width - span :].reshape(-1, 3),
        ],
        axis=0,
    )
    return np.median(samples, axis=0)


def connected_chroma(
    source: Path,
    output: Path,
    helper_alpha: Path | None = None,
    enclosed_key_threshold: int | None = None,
) -> Image.Image:
    """Remove the edge-connected key field and optional strict enclosed islands.

    Dense foliage can completely enclose holes of the generated key field, so
    connectivity alone cannot classify those background pixels.  The optional
    threshold is deliberately strict RGB distance from the sampled key (rather
    than colour dominance) and is used only on the tree boards.  This removes
    fluorescent-magenta field islands without erasing the coral wrap, aqua
    beads, or purple bark that the broad helper matte incorrectly classified.
    """

    image = Image.open(source).convert("RGB")
    rgb = np.asarray(image).astype(np.int16)
    key = _sample_key(rgb)
    distance = np.max(np.abs(rgb - key.reshape(1, 1, 3)), axis=2)

    border = np.concatenate(
        [distance[0, :], distance[-1, :], distance[:, 0], distance[:, -1]]
    )
    threshold = int(np.clip(np.percentile(border, 99.0) + 12.0, 28.0, 64.0))
    candidate = distance <= threshold
    labels, count = ndimage.label(
        candidate, structure=np.ones((3, 3), dtype=np.uint8)
    )
    edge_labels = np.unique(
        np.concatenate(
            [labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1]]
        )
    )
    edge_labels = edge_labels[edge_labels > 0]
    if count <= 0 or edge_labels.size == 0:
        raise RuntimeError(f"no edge-connected chroma field found in {source}")
    background = np.isin(labels, edge_labels)
    if enclosed_key_threshold is not None:
        background |= distance <= enclosed_key_threshold

    alpha = np.full(distance.shape, 255, dtype=np.uint8)
    alpha[background] = 0
    output_rgb = rgb.astype(np.uint8)
    if helper_alpha is not None and helper_alpha.exists():
        helper = np.asarray(Image.open(helper_alpha).convert("RGBA"))
        if helper.shape[:2] != output_rgb.shape[:2]:
            raise RuntimeError(f"helper alpha size mismatch: {helper_alpha}")
        # The standard imagegen helper has the better despilled outline, but
        # its global dominance matte can erase aqua water and coral wrap well
        # inside a subject.  Borrow only its RGB on our two-pixel exterior
        # edge shell; the connected matte remains the sole alpha authority.
        interior_distance = ndimage.distance_transform_edt(~background)
        exterior_edge = (interior_distance > 0.0) & (interior_distance <= 4.0)
        output_rgb = output_rgb.copy()
        output_rgb[exterior_edge] = helper[:, :, :3][exterior_edge]
        alpha[exterior_edge] = helper[:, :, 3][exterior_edge]
    else:
        edge_shell = ndimage.binary_dilation(background, iterations=2) & ~background
        opaque_distance = threshold + 72.0
        ramp = np.clip(
            (distance.astype(np.float32) - threshold) / (opaque_distance - threshold),
            0.0,
            1.0,
        )
        ramp = ramp * ramp * (3.0 - 2.0 * ramp)
        alpha[edge_shell] = np.minimum(
            alpha[edge_shell], (ramp[edge_shell] * 255.0).astype(np.uint8)
        )
    # The helper edge can carry a few semi-opaque key pixels back into a dense
    # enclosed foliage gap.  Reassert the strict, tree-only classification
    # after borrowing its edge colour so the matte remains authoritative.
    if enclosed_key_threshold is not None:
        alpha[distance <= enclosed_key_threshold] = 0
    rgba = np.dstack([output_rgb, alpha])
    rgba[alpha == 0, :3] = 0
    result = Image.fromarray(rgba, "RGBA")
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output, optimize=True)
    return result


def cell_edges(length: int, count: int) -> list[int]:
    return [round(index * length / count) for index in range(count + 1)]


def cell_image(sheet: Image.Image, cols: int, rows: int, index: int) -> Image.Image:
    x_edges = cell_edges(sheet.width, cols)
    y_edges = cell_edges(sheet.height, rows)
    col = index % cols
    row = index // cols
    return sheet.crop((x_edges[col], y_edges[row], x_edges[col + 1], y_edges[row + 1]))


def fitted_subject(cell: Image.Image, size: int, padding: int) -> Image.Image:
    cell = cell.convert("RGBA")
    bbox = cell.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("empty sprite-sheet cell")
    subject = cell.crop(bbox)
    scale = min((size - padding * 2) / subject.width, (size - padding * 2) / subject.height)
    width = max(1, round(subject.width * scale))
    height = max(1, round(subject.height * scale))
    subject = subject.resize((width, height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x = (size - width) // 2
    y = size - padding - height
    canvas.alpha_composite(subject, (x, y))
    return canvas


def native_master(source: Path) -> Image.Image:
    """Create the established 2048 master without enlarging the accepted key."""

    src = Image.open(source).convert("RGB")
    active_size = (2048, 1152)
    continuation = ImageOps.fit(
        src, active_size, method=Image.Resampling.BICUBIC
    ).filter(ImageFilter.GaussianBlur(24))
    veil = Image.new("RGBA", active_size, (36, 28, 72, 38))
    active = Image.alpha_composite(continuation.convert("RGBA"), veil)
    x = (active_size[0] - src.width) // 2
    y = (active_size[1] - src.height) // 2
    mask = Image.new("L", src.size, 255)
    draw = ImageDraw.Draw(mask)
    for inset in range(24):
        draw.rectangle(
            (inset, inset, src.width - 1 - inset, src.height - 1 - inset),
            outline=min(255, inset * 12),
            width=1,
        )
    active.paste(src.convert("RGBA"), (x, y), mask)
    master = Image.new("RGBA", (2048, 2048), active.getpixel((1024, 8)))
    master.paste(active, (0, 448))
    return master


def promote_backgrounds(outputs: list[dict[str, object]]) -> None:
    for kind in ("world", "stage"):
        source = SOURCE / f"{kind}_arborist_clean_native.png"
        master = native_master(source)
        master_path = SOURCE / f"{kind}_arborist_master_2048.png"
        save(master, master_path, outputs, f"{kind}_master_clean_plate")
        active = master.crop((0, 448, 2048, 1600)).resize(
            (1024, 576), Image.Resampling.LANCZOS
        )
        save(active, BACKDROPS / f"{kind}_arborist.png", outputs, f"{kind}_fallback")
        for row in range(2):
            for col in range(2):
                tile = master.crop(
                    (col * 1024, row * 1024, (col + 1) * 1024, (row + 1) * 1024)
                )
                save(
                    tile,
                    BACKDROPS / f"{kind}_arborist_c{col}r{row}.png",
                    outputs,
                    f"{kind}_tile_{col}_{row}",
                )


def compose_roshan(outputs: list[dict[str, object]]) -> None:
    base = connected_chroma(
        SOURCE / "roshan_arborist_sheet_a_candidate_01.png",
        SOURCE / "roshan_arborist_sheet_a_candidate_01_alpha_connected.png",
        SOURCE / "roshan_arborist_sheet_a_candidate_01_alpha.png",
    )
    work = connected_chroma(
        SOURCE / "roshan_arborist_work_native.png",
        SOURCE / "roshan_arborist_work_alpha_connected.png",
        SOURCE / "roshan_arborist_work_alpha_native.png",
    )
    final = base.copy()
    x_edges = cell_edges(final.width, 4)
    y_edges = cell_edges(final.height, 4)
    row = 2
    for col in range(4):
        replacement = cell_image(work, 2, 2, col)
        target_width = x_edges[col + 1] - x_edges[col]
        target_height = y_edges[row + 1] - y_edges[row]
        target_size = min(target_width, target_height)
        fitted = fitted_subject(replacement, target_size, 9)
        target = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
        target.alpha_composite(
            fitted,
            ((target_width - fitted.width) // 2, target_height - fitted.height),
        )
        final.paste(
            (0, 0, 0, 0),
            (x_edges[col], y_edges[row], x_edges[col + 1], y_edges[row + 1]),
        )
        final.alpha_composite(target, (x_edges[col], y_edges[row]))

    alpha_path = SOURCE / "roshan_arborist_sheet_a_alpha_native.png"
    save(final, alpha_path, outputs, "roshan_alpha_native_16_frames")
    chroma = Image.new("RGB", final.size, (0, 255, 0))
    chroma.paste(final.convert("RGB"), (0, 0), final.getchannel("A"))
    save(
        chroma,
        SOURCE / "roshan_arborist_sheet_a_native.png",
        outputs,
        "roshan_composite_chroma_native",
    )

    # Use the established clip-safe 4x4 packer after this script returns.


def promote_tree_and_props(outputs: list[dict[str, object]]) -> None:
    tree = connected_chroma(
        SOURCE / "tree_states_native.png",
        SOURCE / "tree_states_alpha_connected.png",
        SOURCE / "tree_states_alpha_native.png",
        enclosed_key_threshold=96,
    )
    intermediate = connected_chroma(
        SOURCE / "tree_intermediate_native.png",
        SOURCE / "tree_intermediate_alpha_connected.png",
        SOURCE / "tree_intermediate_alpha_native.png",
        enclosed_key_threshold=96,
    )
    tree_sources = {
        "tree_needs_care.png": cell_image(tree, 2, 2, 0),
        "tree_checked.png": cell_image(tree, 2, 2, 1),
        "tree_treated.png": cell_image(tree, 2, 2, 2),
        "tree_bloom.png": cell_image(tree, 2, 2, 3),
        "tree_pruned.png": cell_image(intermediate, 2, 1, 0),
        "tree_watered.png": cell_image(intermediate, 2, 1, 1),
    }
    for name, image in tree_sources.items():
        save(
            fitted_subject(image, RUNTIME_TREE_SIZE, 20),
            ARBORIST / name,
            outputs,
            "hero_tree_state",
        )

    imp = connected_chroma(
        SOURCE / "imp_arborist_states_native.png",
        SOURCE / "imp_arborist_states_alpha_connected.png",
        SOURCE / "imp_arborist_states_alpha_native.png",
    )
    imp_names = [
        "imp_arborist_ready.png",
        "imp_arborist_catch.png",
        "imp_arborist_water.png",
        "imp_arborist_cheer.png",
    ]
    imp_cards: list[Image.Image] = []
    for index, name in enumerate(imp_names):
        card = fitted_subject(cell_image(imp, 2, 2, index), RUNTIME_CARD_SIZE, 16)
        imp_cards.append(card)
        save(card, ARBORIST / name, outputs, "cooperative_imp_state")
    save(imp_cards[0], ACTORS / "rival_arborist.png", outputs, "arborist_partner")

    props = connected_chroma(
        SOURCE / "arborist_props_native.png",
        SOURCE / "arborist_props_alpha_connected.png",
        SOURCE / "arborist_props_alpha_native.png",
    )
    prop_names = [
        "opera_crest_arborist.png",
        "arborist_pruner.png",
        "arborist_water_pearl.png",
        "arborist_wrap.png",
    ]
    prop_cards: list[Image.Image] = []
    for index, name in enumerate(prop_names):
        size = 256 if index == 0 else RUNTIME_CARD_SIZE
        card = fitted_subject(cell_image(props, 2, 2, index), size, 10 if index == 0 else 18)
        prop_cards.append(card)
        destination = CRESTS / name if index == 0 else ARBORIST / name
        save(card, destination, outputs, "arborist_crest" if index == 0 else "arborist_tool")
    goal = prop_cards[0].resize((512, 512), Image.Resampling.LANCZOS)
    save(goal, PROPS / "goal_arborist.png", outputs, "arborist_goal_crest")


def promote_roshan_runtime(outputs: list[dict[str, object]]) -> None:
    runtime = ANIMATION / "roshan_arborist_sheet_a.png"
    if not runtime.exists():
        raise RuntimeError(
            "run tools/prepare_opera_roshan_animation.py for Arborist before final promotion"
        )
    sheet = Image.open(runtime).convert("RGBA")
    idle = fitted_subject(cell_image(sheet, 4, 4, 0), 512, 16)
    save(idle, ACTORS / "roshan_arborist.png", outputs, "arborist_roshan_idle")


def main() -> int:
    outputs: list[dict[str, object]] = []
    promote_backgrounds(outputs)
    compose_roshan(outputs)
    promote_tree_and_props(outputs)
    runtime = ANIMATION / "roshan_arborist_sheet_a.png"
    if runtime.exists():
        promote_roshan_runtime(outputs)
    report = {
        "pass": True,
        "method": "whole-frame clean-plate continuation; connected-edge chroma matte; whole-cell fit",
        "source_directory": SOURCE.relative_to(ROOT).as_posix(),
        "outputs": outputs,
    }
    path = SOURCE / "DERIVATION_REPORT.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"prepared {len(outputs)} Arborist art outputs; run Roshan packer next")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

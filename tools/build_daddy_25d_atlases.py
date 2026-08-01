#!/usr/bin/env python3
"""Build Daddy Mermaid's topology-safe 2.5D animation atlases.

The accepted ImageGen sheets use a vivid green backing, but Daddy's rainbow
tail also contains authored green pixels.  A dominant-green key therefore
removes anatomy.  This builder instead removes only key-colored pixels that
are connected to the *outer sheet border*, extracts each complete Daddy as a
global connected component, and assigns those components to the intended
grid slots.  Nominal grid cells are ownership hints only; they are never used
as source crops because several generated poses cross those boundaries.

The bundled imagegen chroma helper was run once both with and without despill
for every accepted source.  Its outputs are retained beside the chroma sheets
for review.  Only the despilled helper RGB is sampled for the two-pixel soft
outer matte.  Helper alpha is deliberately ignored: the border-connected
matte and the pre-sticker full-subject connectivity audit are authoritative.

No morphology is used to attach body parts.  White sticker rim and navy drop
shadow are added only after every resized colored Daddy has passed the
single-component anatomy gate.
"""

from __future__ import annotations

import hashlib
import statistics
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

try:
    from scipy import ndimage as _ndimage
except ImportError:  # CI installs NumPy/Pillow; retain a dependency-free path.
    _ndimage = None


CELL_SIZE = 256
NORMALIZED_SPAN = 188.0
TORSO_TARGET = (98.0, 94.0)
KEY_THRESHOLD = 32
SOFT_TRANSPARENT = 16
SOFT_OPAQUE = 32
SOFT_RING_RADIUS = 2
COMPONENT_MIN_AREA = 1000
SIGNIFICANT_OUTPUT_AREA = 12
RIM_RADIUS = 5
SHADOW_OFFSET = (3, 5)
SHADOW_BLUR = 2.0
TAIL_REGION_Y = 110

SOURCE_DIR = Path("assets_src/imagegen/daddy_25d_tailmotion_2026-08-01")
OUTPUT_DIR = Path("assets/characters/daddy_25d")

PROTECTED_HASHES = {
    Path("assets_src/daddy_master.png"):
        "2eda6f76760b85984692dd35bf9ce69b631f6d9db4c8b7b8c013bb92cb632b77",
    Path("assets/characters/friends/daddy.webp"):
        "9031736498f05662716988b6c9a8091dc148edf92ae1e8422fb5e4f2fd17c089",
    Path("assets/characters/stickers/daddy.png"):
        "402024ac72c5365aae8562d422b9f888a6f5cdef7b6539409747e8f965cd0122",
}


@dataclass(frozen=True)
class ClipSpec:
    name: str
    source_name: str
    output_name: str
    columns: int
    rows: int
    expected_hash: str

    @property
    def frame_count(self) -> int:
        return self.columns * self.rows


SPECS = (
    ClipSpec(
        "idle", "daddy_idle_chroma.png", "daddy_idle.png", 4, 2,
        "cee3b12bd0b8db3b29d79569f313f4e2a1d3fabad18b071dd0fc4e3546dfc73d",
    ),
    ClipSpec(
        "swim", "daddy_swim_chroma.png", "daddy_swim.png", 4, 4,
        "2c3a41ffb600d84e5de03db251a432f5054e7779c98fa27607b647e88b29a798",
    ),
    ClipSpec(
        "gesture_a", "daddy_gesture_a_chroma.png", "daddy_gesture_a.png", 4, 4,
        "e768a6ca596721d3734d4e9743845a18d6471b7ce733b2900c501e5e5ea6dee9",
    ),
    ClipSpec(
        "victory", "daddy_victory_chroma.png", "daddy_victory.png", 4, 2,
        "803add39f92af2220222a513966de66ea6bfa661fe079efcfd35dda8833d59b3",
    ),
)


@dataclass
class Component:
    label: int
    area: int
    bbox: tuple[int, int, int, int]
    centroid: tuple[float, float]
    row: int
    column: int
    anchor: tuple[float, float] = (0.0, 0.0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def label_components(mask: np.ndarray) -> tuple[np.ndarray, int]:
    """Label eight-connected True pixels, using SciPy when available."""
    if _ndimage is not None:
        labels, count = _ndimage.label(mask, structure=np.ones((3, 3), bool))
        return labels.astype(np.int32, copy=False), int(count)

    height, width = mask.shape
    labels = np.zeros((height, width), dtype=np.int32)
    label = 0
    for y, x in np.argwhere(mask):
        if labels[y, x] != 0:
            continue
        label += 1
        labels[y, x] = label
        queue: deque[tuple[int, int]] = deque([(int(y), int(x))])
        while queue:
            cy, cx = queue.popleft()
            for dy in (-1, 0, 1):
                ny = cy + dy
                if ny < 0 or ny >= height:
                    continue
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx = cx + dx
                    if nx < 0 or nx >= width:
                        continue
                    if mask[ny, nx] and labels[ny, nx] == 0:
                        labels[ny, nx] = label
                        queue.append((ny, nx))
    return labels, label


def border_connected_background(candidate: np.ndarray) -> np.ndarray:
    """Return only candidate pixels connected to an outer sheet edge."""
    if _ndimage is not None:
        labels, _ = _ndimage.label(candidate, structure=np.ones((3, 3), bool))
        edge_labels = np.unique(np.concatenate((
            labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1],
        )))
        edge_labels = edge_labels[edge_labels != 0]
        return np.isin(labels, edge_labels)

    height, width = candidate.shape
    connected = np.zeros_like(candidate)
    queue: deque[tuple[int, int]] = deque()
    for x in range(width):
        if candidate[0, x]:
            queue.append((0, x))
        if candidate[height - 1, x]:
            queue.append((height - 1, x))
    for y in range(1, height - 1):
        if candidate[y, 0]:
            queue.append((y, 0))
        if candidate[y, width - 1]:
            queue.append((y, width - 1))

    while queue:
        y, x = queue.popleft()
        if connected[y, x] or not candidate[y, x]:
            continue
        connected[y, x] = True
        for dy in (-1, 0, 1):
            ny = y + dy
            if ny < 0 or ny >= height:
                continue
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx = x + dx
                if 0 <= nx < width and not connected[ny, nx] and candidate[ny, nx]:
                    queue.append((ny, nx))
    return connected


def border_mode(rgb: np.ndarray) -> np.ndarray:
    border = np.concatenate((
        rgb[0, :, :], rgb[-1, :, :], rgb[1:-1, 0, :], rgb[1:-1, -1, :],
    ))
    color, _ = Counter(map(tuple, border.tolist())).most_common(1)[0]
    return np.asarray(color, dtype=np.int16)


def assign_components(
    labels: np.ndarray,
    spec: ClipSpec,
) -> list[Component]:
    areas = np.bincount(labels.ravel())
    large_ids = [
        int(index) for index, area in enumerate(areas)
        if index != 0 and area >= COMPONENT_MIN_AREA
    ]
    if len(large_ids) != spec.frame_count:
        raise ValueError(
            f"{spec.name}: expected {spec.frame_count} full-body components, "
            f"found {len(large_ids)} at area >= {COMPONENT_MIN_AREA}"
        )
    unexpected = [
        int(area) for index, area in enumerate(areas)
        if index != 0 and index not in large_ids and area >= 32
    ]
    if unexpected:
        raise ValueError(f"{spec.name}: unexpected detached fragments {unexpected}")

    height, width = labels.shape
    cell_width = width / spec.columns
    cell_height = height / spec.rows
    slots: dict[tuple[int, int], Component] = {}
    for label in large_ids:
        ys, xs = np.nonzero(labels == label)
        left, top = int(xs.min()), int(ys.min())
        right, bottom = int(xs.max()) + 1, int(ys.max()) + 1
        centroid = (float(xs.mean()), float(ys.mean()))
        column = min(spec.columns - 1, max(0, int(centroid[0] / cell_width)))
        row = min(spec.rows - 1, max(0, int(centroid[1] / cell_height)))
        slot = (row, column)
        if slot in slots:
            raise ValueError(f"{spec.name}: two full bodies claim grid slot {slot}")
        slots[slot] = Component(
            label, int(areas[label]), (left, top, right, bottom),
            centroid, row, column,
        )

    expected_slots = {
        (row, column)
        for row in range(spec.rows)
        for column in range(spec.columns)
    }
    if set(slots) != expected_slots:
        raise ValueError(
            f"{spec.name}: missing grid slots {sorted(expected_slots - set(slots))}"
        )
    return [slots[(row, column)] for row in range(spec.rows) for column in range(spec.columns)]


def detect_torso_anchor(
    component: Component,
    labels: np.ndarray,
    hsv: np.ndarray,
    spec: ClipSpec,
) -> tuple[float, float]:
    """Find the stable navy upper-body mass; tail pixels are outside the ROI."""
    height, width = labels.shape
    cell_width = width / spec.columns
    cell_height = height / spec.rows
    center_x = (component.column + 0.5) * cell_width
    x0 = max(0, int(center_x - 0.32 * cell_width))
    x1 = min(width, int(center_x + 0.32 * cell_width))
    y0 = max(0, int(component.row * cell_height))
    y1 = min(height, int(component.row * cell_height + 0.58 * cell_height))

    hue = hsv[y0:y1, x0:x1, 0]
    saturation = hsv[y0:y1, x0:x1, 1]
    value = hsv[y0:y1, x0:x1, 2]
    navy = (
        (labels[y0:y1, x0:x1] == component.label)
        & (hue >= 145) & (hue <= 190)
        & (saturation >= 80)
        & (value >= 35) & (value <= 175)
    )
    ys, xs = np.nonzero(navy)
    if len(xs) < 1000:
        raise ValueError(
            f"{spec.name} r{component.row + 1}c{component.column + 1}: "
            f"torso anchor mask too small ({len(xs)} pixels)"
        )
    return x0 + float(xs.mean()), y0 + float(ys.mean())


def dilate_mask(mask: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return mask.copy()
    source = Image.fromarray(mask.astype(np.uint8) * 255, "L")
    expanded = source.filter(ImageFilter.MaxFilter(radius * 2 + 1))
    return np.asarray(expanded) > 0


def component_rgba(
    raw_rgb: np.ndarray,
    helper_rgb: np.ndarray,
    distance: np.ndarray,
    background: np.ndarray,
    labels: np.ndarray,
    component: Component,
) -> tuple[Image.Image, tuple[int, int, int, int]]:
    core = labels == component.label
    ring = dilate_mask(core, SOFT_RING_RADIUS) & background
    ramp = np.clip(
        (distance.astype(np.float32) - SOFT_TRANSPARENT)
        / float(SOFT_OPAQUE - SOFT_TRANSPARENT),
        0.0,
        1.0,
    )
    alpha = np.zeros(core.shape, dtype=np.uint8)
    alpha[core] = 255
    alpha[ring] = np.rint(ramp[ring] * 255.0).astype(np.uint8)

    visible = alpha > 0
    ys, xs = np.nonzero(visible)
    if len(xs) == 0:
        raise ValueError("empty component matte")
    left, top = int(xs.min()), int(ys.min())
    right, bottom = int(xs.max()) + 1, int(ys.max()) + 1

    rgba = np.zeros((bottom - top, right - left, 4), dtype=np.uint8)
    local_alpha = alpha[top:bottom, left:right]
    local_core = core[top:bottom, left:right]
    rgba[:, :, :3] = raw_rgb[top:bottom, left:right]
    # The helper's alpha can erase authored green, but its edge RGB is useful
    # for decontaminating only the custom matte's partial-alpha ring.
    edge = (local_alpha > 0) & ~local_core
    helper_crop = helper_rgb[top:bottom, left:right]
    rgba[edge, :3] = helper_crop[edge, :3]
    rgba[:, :, 3] = local_alpha
    rgba[local_alpha == 0, :3] = 0
    return Image.fromarray(rgba, "RGBA"), (left, top, right, bottom)


def resize_rgba_premultiplied(image: Image.Image, scale: float) -> Image.Image:
    width = max(1, int(round(image.width * scale)))
    height = max(1, int(round(image.height * scale)))
    rgba = np.asarray(image, dtype=np.float32)
    alpha = rgba[:, :, 3] / 255.0
    premultiplied = rgba[:, :, :3] * alpha[:, :, None]

    alpha_resized = np.asarray(
        Image.fromarray(alpha.astype(np.float32), "F").resize(
            (width, height), Image.Resampling.LANCZOS,
        ),
        dtype=np.float32,
    )
    color_channels = []
    for channel in range(3):
        color_channels.append(np.asarray(
            Image.fromarray(premultiplied[:, :, channel], "F").resize(
                (width, height), Image.Resampling.LANCZOS,
            ),
            dtype=np.float32,
        ))
    premultiplied_resized = np.stack(color_channels, axis=2)
    alpha_resized = np.clip(alpha_resized, 0.0, 1.0)
    rgb = np.zeros_like(premultiplied_resized)
    visible = alpha_resized > (1.0 / 255.0)
    rgb[visible] = (
        premultiplied_resized[visible] / alpha_resized[visible, None]
    )
    output = np.zeros((height, width, 4), dtype=np.uint8)
    output[:, :, :3] = np.rint(np.clip(rgb, 0.0, 255.0)).astype(np.uint8)
    output[:, :, 3] = np.rint(alpha_resized * 255.0).astype(np.uint8)
    output[output[:, :, 3] == 0, :3] = 0
    return Image.fromarray(output, "RGBA")


def significant_component_areas(mask: np.ndarray) -> list[int]:
    labels, _ = label_components(mask)
    areas = np.bincount(labels.ravel())
    return sorted(
        [int(area) for area in areas[1:] if area >= SIGNIFICANT_OUTPUT_AREA],
        reverse=True,
    )


def validate_colored_subject(frame: Image.Image, label: str) -> tuple[int, int, int, int]:
    alpha = np.asarray(frame.getchannel("A"))
    for threshold in (32, 128, 224):
        areas = significant_component_areas(alpha >= threshold)
        if len(areas) != 1:
            raise ValueError(
                f"{label}: colored Daddy has {len(areas)} significant components "
                f"before sticker at alpha >= {threshold}: {areas}"
            )
    ys, xs = np.nonzero(alpha >= 32)
    if len(xs) == 0:
        raise ValueError(f"{label}: empty colored Daddy")
    bounds = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    if bounds[0] < 4 or bounds[1] < 4 or bounds[2] > 252 or bounds[3] > 252:
        raise ValueError(f"{label}: insufficient pre-sticker inset {bounds}")
    return bounds


def sticker_treatment(subject: Image.Image) -> Image.Image:
    alpha = np.asarray(subject.getchannel("A"))
    core = Image.fromarray((alpha >= 32).astype(np.uint8) * 255, "L")
    rim_alpha = core.filter(ImageFilter.MaxFilter(RIM_RADIUS * 2 + 1))

    shadow_base = Image.new("L", (CELL_SIZE, CELL_SIZE), 0)
    shadow_base.paste(rim_alpha, SHADOW_OFFSET)
    shadow_alpha = shadow_base.filter(ImageFilter.GaussianBlur(SHADOW_BLUR))
    shadow_values = np.asarray(shadow_alpha, dtype=np.float32) * 0.46
    shadow = Image.new("RGBA", (CELL_SIZE, CELL_SIZE), (47, 35, 76, 0))
    shadow.putalpha(Image.fromarray(np.rint(shadow_values).astype(np.uint8), "L"))

    rim = Image.new("RGBA", (CELL_SIZE, CELL_SIZE), (255, 252, 244, 0))
    rim.putalpha(rim_alpha)
    result = Image.new("RGBA", (CELL_SIZE, CELL_SIZE), (0, 0, 0, 0))
    result = Image.alpha_composite(result, shadow)
    result = Image.alpha_composite(result, rim)
    result = Image.alpha_composite(result, subject)
    pixels = np.asarray(result).copy()
    pixels[pixels[:, :, 3] == 0, :3] = 0
    return Image.fromarray(pixels, "RGBA")


def edge_alpha(frame: Image.Image) -> int:
    alpha = np.asarray(frame.getchannel("A"))
    return int(max(
        alpha[0, :].max(), alpha[-1, :].max(),
        alpha[:, 0].max(), alpha[:, -1].max(),
    ))


def xor_union(mask_a: np.ndarray, mask_b: np.ndarray) -> float:
    union = np.logical_or(mask_a, mask_b).sum()
    if union == 0:
        return 0.0
    return float(np.logical_xor(mask_a, mask_b).sum() / union)


def tail_motion_metrics(frames: list[Image.Image], spec: ClipSpec) -> dict[str, float | int]:
    masks = []
    tail_hashes = set()
    for frame in frames:
        mask = np.asarray(frame.getchannel("A")) >= 128
        mask[:TAIL_REGION_Y, :] = False
        masks.append(mask)
        tail_hashes.add(hashlib.sha256(mask.tobytes()).hexdigest())

    scores: list[float] = []
    if spec.name == "gesture_a":
        for row in range(spec.rows):
            start = row * spec.columns
            for index in range(start, start + spec.columns - 1):
                scores.append(xor_union(masks[index], masks[index + 1]))
    else:
        for index in range(len(masks) - 1):
            scores.append(xor_union(masks[index], masks[index + 1]))

    if not scores or max(scores) < 0.08 or statistics.median(scores) < 0.025:
        raise ValueError(
            f"{spec.name}: tail motion too weak; scores "
            f"min/median/max={min(scores, default=0):.3f}/"
            f"{statistics.median(scores) if scores else 0:.3f}/"
            f"{max(scores, default=0):.3f}"
        )
    if len(tail_hashes) < max(3, spec.frame_count // 2):
        raise ValueError(
            f"{spec.name}: only {len(tail_hashes)} distinct tail silhouettes"
        )
    return {
        "tail_min": min(scores),
        "tail_median": statistics.median(scores),
        "tail_max": max(scores),
        "tail_unique": len(tail_hashes),
    }


def validate_protected_files(root: Path) -> None:
    for relative_path, expected in PROTECTED_HASHES.items():
        path = root / relative_path
        actual = sha256(path)
        if actual != expected:
            raise ValueError(
                f"protected original changed: {relative_path} "
                f"expected {expected}, found {actual}"
            )


def build_clip(root: Path, spec: ClipSpec) -> tuple[Path, dict[str, float | int]]:
    source_path = root / SOURCE_DIR / spec.source_name
    if sha256(source_path) != spec.expected_hash:
        raise ValueError(f"{spec.name}: accepted source hash mismatch")

    helper_keyed_path = source_path.with_name(
        source_path.stem.replace("_chroma", "_helper_keyed") + ".png"
    )
    helper_despilled_path = source_path.with_name(
        source_path.stem.replace("_chroma", "_helper_despilled") + ".png"
    )
    if not helper_keyed_path.exists() or not helper_despilled_path.exists():
        raise ValueError(
            f"{spec.name}: bundled-helper keyed/despilled intermediates are required"
        )

    raw_image = Image.open(source_path).convert("RGB")
    helper_keyed = Image.open(helper_keyed_path).convert("RGBA")
    helper_despilled = Image.open(helper_despilled_path).convert("RGBA")
    if helper_keyed.size != raw_image.size or helper_despilled.size != raw_image.size:
        raise ValueError(f"{spec.name}: helper intermediate dimensions do not match source")

    raw_rgb = np.asarray(raw_image)
    helper_rgb = np.asarray(helper_despilled)[:, :, :3]
    key = border_mode(raw_rgb)
    difference = np.abs(raw_rgb.astype(np.int16) - key[None, None, :])
    distance = np.max(difference, axis=2)
    candidate_background = distance <= KEY_THRESHOLD
    background = border_connected_background(candidate_background)
    foreground = ~background
    labels, component_count = label_components(foreground)
    components = assign_components(labels, spec)
    hsv = np.asarray(raw_image.convert("HSV"))
    for component in components:
        component.anchor = detect_torso_anchor(component, labels, hsv, spec)

    max_span = max(
        max(component.bbox[2] - component.bbox[0], component.bbox[3] - component.bbox[1])
        for component in components
    )
    scale = NORMALIZED_SPAN / float(max_span)
    colored_frames: list[Image.Image] = []
    anchor_drifts = []
    pre_bounds = []

    for frame_index, component in enumerate(components):
        cutout, crop = component_rgba(
            raw_rgb, helper_rgb, distance, background, labels, component,
        )
        resized = resize_rgba_premultiplied(cutout, scale)
        anchor_in_crop = (
            component.anchor[0] - crop[0], component.anchor[1] - crop[1],
        )
        paste_x = int(round(TORSO_TARGET[0] - anchor_in_crop[0] * scale))
        paste_y = int(round(TORSO_TARGET[1] - anchor_in_crop[1] * scale))
        if (
            paste_x < 0 or paste_y < 0
            or paste_x + resized.width > CELL_SIZE
            or paste_y + resized.height > CELL_SIZE
        ):
            raise ValueError(
                f"{spec.name} frame {frame_index}: normalized cutout does not fit "
                f"at {(paste_x, paste_y)} size {resized.size}"
            )
        frame = Image.new("RGBA", (CELL_SIZE, CELL_SIZE), (0, 0, 0, 0))
        frame.alpha_composite(resized, (paste_x, paste_y))
        pre_bounds.append(validate_colored_subject(frame, f"{spec.name} frame {frame_index}"))
        actual_anchor = (
            paste_x + anchor_in_crop[0] * scale,
            paste_y + anchor_in_crop[1] * scale,
        )
        anchor_drifts.append(max(
            abs(actual_anchor[0] - TORSO_TARGET[0]),
            abs(actual_anchor[1] - TORSO_TARGET[1]),
        ))
        colored_frames.append(frame)

    if max(anchor_drifts) > 0.51:
        raise ValueError(f"{spec.name}: torso anchor drift exceeds one half pixel")

    motion = tail_motion_metrics(colored_frames, spec)
    final_frames = [sticker_treatment(frame) for frame in colored_frames]
    frame_hashes = {hashlib.sha256(np.asarray(frame).tobytes()).hexdigest() for frame in final_frames}
    if len(frame_hashes) != spec.frame_count:
        raise ValueError(
            f"{spec.name}: expected {spec.frame_count} unique frames, "
            f"found {len(frame_hashes)}"
        )
    worst_edge = max(edge_alpha(frame) for frame in final_frames)
    if worst_edge >= 8:
        raise ValueError(f"{spec.name}: cell-edge alpha {worst_edge} is not safe")

    atlas = Image.new(
        "RGBA", (spec.columns * CELL_SIZE, spec.rows * CELL_SIZE),
        (0, 0, 0, 0),
    )
    for index, frame in enumerate(final_frames):
        atlas.alpha_composite(
            frame, ((index % spec.columns) * CELL_SIZE, (index // spec.columns) * CELL_SIZE),
        )
    expected_size = (spec.columns * CELL_SIZE, spec.rows * CELL_SIZE)
    if atlas.size != expected_size:
        raise ValueError(f"{spec.name}: atlas dimensions {atlas.size} != {expected_size}")

    output_path = root / OUTPUT_DIR / spec.output_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(output_path, "PNG", optimize=True, compress_level=9)
    metrics: dict[str, float | int] = {
        "source_components": len(components),
        "raw_component_labels": component_count,
        "scale": scale,
        "max_anchor_drift": max(anchor_drifts),
        "pre_left": min(bounds[0] for bounds in pre_bounds),
        "pre_top": min(bounds[1] for bounds in pre_bounds),
        "pre_right": max(bounds[2] for bounds in pre_bounds),
        "pre_bottom": max(bounds[3] for bounds in pre_bounds),
        "edge_alpha": worst_edge,
        "unique_frames": len(frame_hashes),
        **motion,
    }
    print(
        f"{spec.name}: key=#{key[0]:02x}{key[1]:02x}{key[2]:02x} "
        f"components={len(components)} scale={scale:.6f} "
        f"anchor_drift={max(anchor_drifts):.3f}px "
        f"pre_bounds=({metrics['pre_left']},{metrics['pre_top']})-"
        f"({metrics['pre_right']},{metrics['pre_bottom']}) "
        f"tail={motion['tail_min']:.3f}/{motion['tail_median']:.3f}/"
        f"{motion['tail_max']:.3f} unique_tail={motion['tail_unique']} "
        f"edge_alpha={worst_edge}"
    )
    print(
        f"  helper validated: {helper_keyed_path.name}, "
        f"{helper_despilled_path.name}; helper alpha ignored"
    )
    print(f"  wrote {output_path.relative_to(root)} sha256={sha256(output_path)}")
    return output_path, metrics


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    validate_protected_files(root)
    outputs = []
    for spec in SPECS:
        outputs.append(build_clip(root, spec))
    validate_protected_files(root)
    print(
        "PASS: 48 topology-good colored frames; helper intermediates validated; "
        "sticker treatment applied only after anatomy audit"
    )


if __name__ == "__main__":
    main()

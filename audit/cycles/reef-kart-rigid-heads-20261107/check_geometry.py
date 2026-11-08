"""Check exported paint against the independently applied rigid head transform."""
import json
import math
from pathlib import Path
from statistics import mean

from PIL import Image

NAMES = ("roshan", "sparkle", "huluu", "bunny", "kitty", "baby_doll",
         "dolly", "sleepy", "imp", "rumi", "daddy", "mama_baby")
ANGLES = (7.5, 7.5, 8, 7, 6, 6, 6.5, 5.5, 7, 8, 7.5, 5.5)
DROPS = (7, 6, 7, 5, 5, 6, 6, 5, 6, 7, 6, 5)
TURNS = (0, -0.5, -1, 0.5, 1, 0, 0)
TUCKS = (0, 0, 0, 0, 0, 0.52, 1)
RIDE_SCALE = (1, 1.13, 0.92)
RATIO = 200 / 256
ROOT = Path("assets/racer/rider_poses_v3")


def card(atlas, ride, key):
    index = ride * len(TURNS) + key
    x, y = index % 5 * 200, index // 5 * 200
    return atlas.crop((x, y, x + 200, y + 200))


def region(character, ride):
    if character == 0:
        raw_top = (94, 65, 82)[ride]
        raw_pivot = (110, 82, 103)[ride]
        fit = 230 / 256
        return (220 + (raw_pivot - 220) * fit) * RATIO, int((220 + (raw_top - 220) * fit) * RATIO - 10)
    grip = (97, 69, 94)[ride] - (3 if character == 1 else 0)
    return grip * RATIO, int(grip * RATIO - 13)


def expected_head(neutral, pivot_y, angle, drop):
    cx = 100.0
    cy = pivot_y
    c, s = math.cos(angle), math.sin(angle)
    tx = cx - c * cx - s * (cy + drop)
    ty = cy + s * cx - c * (cy + drop)
    return neutral.transform(
        neutral.size, Image.Transform.AFFINE, (c, s, tx, -s, c, ty),
        resample=Image.Resampling.BICUBIC,
    )


def measure(actual, expected, upper):
    intersection = union = 0
    differences = []
    for ref, sample in zip(expected.crop((44, 0, 156, upper)).getdata(),
                           actual.crop((44, 0, 156, upper)).getdata()):
        inside_ref = ref[3] >= 96
        inside_sample = sample[3] >= 96
        union += inside_ref or inside_sample
        intersection += inside_ref and inside_sample
        if ref[3] >= 225 and sample[3] >= 225:
            differences.extend(abs(x - y) for x, y in zip(ref[:3], sample[:3]))
    assert union > 100 and differences, (union, len(differences))
    return intersection / union, mean(differences)


def run():
    summary = []
    rejected = []
    for character, name in enumerate(NAMES):
        atlas = Image.open(ROOT / f"{name}.png").convert("RGBA")
        assert atlas.size == (1000, 1000)
        old_atlas = Path(f"assets/racer/rider_poses_v2/{name}.png")
        old = Image.open(old_atlas).convert("RGBA") if old_atlas.is_file() else None
        for ride in range(3):
            frames = [card(atlas, ride, key) for key in range(len(TURNS))]
            assert len({frame.tobytes() for frame in frames}) == len(TURNS)
            pivot_y, upper = region(character, ride)
            floor = math.ceil(max((125, 90, 120)[ride] * RATIO, pivot_y)) + 4
            assert len({frame.crop((0, floor, 200, 200)).tobytes() for frame in frames}) == 1, (name, ride)
            for key in range(1, len(TURNS)):
                angle = math.radians(TURNS[key] * ANGLES[character] * RIDE_SCALE[ride])
                drop = math.floor(TUCKS[key] * DROPS[character] + 0.5) * RATIO
                wanted = expected_head(frames[0], pivot_y, angle, drop)
                iou, color_error = measure(frames[key], wanted, upper)
                summary.append({"driver": name, "ride": ride, "key": key,
                                "silhouette_iou": round(iou, 4), "mean_rgb_error": round(color_error, 3)})
                if old is not None and key in (2, 4, 6):
                    ref = expected_head(card(old, ride, 0), pivot_y, angle, drop)
                    old_iou, old_error = measure(card(old, ride, key), ref, upper)
                    rejected.append((name, ride, key, old_iou, old_error))
    print("Rigid keys:", len(summary), "minimum IoU", min(row["silhouette_iou"] for row in summary),
          "maximum RGB error", max(row["mean_rgb_error"] for row in summary))
    print("Worst candidate rows", sorted(summary, key=lambda row: row["silhouette_iou"])[:6])
    rejected_failures = sum(iou < 0.90 or color > 12.0 for _, _, _, iou, color in rejected)
    print("Previous full-turn/boost failures under the rigid standard:", rejected_failures, "/", len(rejected))
    assert all(row["silhouette_iou"] >= 0.90 and row["mean_rgb_error"] <= 12.0 for row in summary)
    assert rejected_failures >= 24
    return {"candidates": summary, "previous_checked": len(rejected), "previous_failed": rejected_failures}


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, separators=(",", ":")))

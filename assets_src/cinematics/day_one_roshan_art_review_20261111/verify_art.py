"""Check the static art exports without changing any image pixels."""
from pathlib import Path
from hashlib import sha256
import json
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent

def rgba(name):
    return np.asarray(Image.open(ROOT / name).convert("RGBA"))

def lab(rgb):
    linear = rgb.astype(np.float64) / 255
    linear = np.where(linear > .04045, ((linear + .055) / 1.055)**2.4, linear / 12.92)
    xyz = linear @ np.array([[.4124564,.3575761,.1804375],
                             [.2126729,.7151522,.0721750],
                             [.0193339,.1191920,.9503041]]).T
    xyz /= np.array([.95047,1,1.08883])
    f = np.where(xyz > (6/29)**3, np.cbrt(xyz), xyz / (3 * (6/29)**2) + 4/29)
    return np.stack((116*f[:,:,1]-16, 500*(f[:,:,0]-f[:,:,1]), 200*(f[:,:,1]-f[:,:,2])), axis=2)

def centroid(mask):
    y,x = np.where(mask)
    return np.array([x.mean(),y.mean()])

def verify():
    result = {"scope":"Static art and registration only", "fixtures":{}, "hands":{}, "grime":{}}
    union = np.zeros((576,1024),dtype=bool)
    for name, matte in (("sink_clean_registered","sink_matte"),("toilet_clean_registered","toilet_matte"),
                        ("tub_water_registered","tub_interior_matte")):
        alpha = rgba(f"art/{name}.png")[:,:,3]
        reference = rgba(f"evidence/{matte}.png")[:,:,0]
        assert alpha.shape == (576,1024)
        assert np.array_equal(alpha,reference),name
        source = reference >= 128
        output = alpha >= 128
        iou = float((source & output).sum() / (source | output).sum())
        offset = float(np.linalg.norm(centroid(source)-centroid(output)))
        spill = int(((alpha > 0)&(reference == 0)).sum())
        assert iou >= .95 and offset <= 2 and spill == 0
        result["fixtures"][name] = {"matte_iou_alpha128":iou,"centroid_offset_px":offset,"spill_px":spill}
        union |= alpha > 0
    preview = rgba("evidence/bathroom_registered_preview.png")[:,:,:3]
    dirty = rgba("references/dirty_room.png")[:,:,:3]
    union[231:252,285:307] = True  # separate duck in review preview
    changed = np.any(preview != dirty,axis=2)
    result["preview_pixels_changed_outside_fixture_and_duck"]=int((changed & ~union).sum())
    assert result["preview_pixels_changed_outside_fixture_and_duck"] == 0
    for path in sorted((ROOT/"art").glob("*.png")):
        im = rgba(path.relative_to(ROOT))
        alpha = im[:,:,3]
        assert max(alpha.shape) <= 1024 and alpha.max() >= 128 and alpha.min() == 0,path
        assert max(alpha[0].max(),alpha[-1].max(),alpha[:,0].max(),alpha[:,-1].max()) == 0,path
        if path.name.startswith("hand_"):
            value = int(alpha[117,64])
            assert alpha.shape == (128,128) and value >= 128,path
            result["hands"][path.stem] = {"wrist":[64,117],"alpha_at_wrist":value}
    assert len(result["hands"]) == 6
    assert len(list((ROOT/"art").glob("face_*.png"))) == 7
    delta = np.linalg.norm(lab(preview)-lab(rgba("evidence/grime_reuse_preview.png")[:,:,:3]),axis=2)
    geometry = json.loads((ROOT/"registration.json").read_bytes())
    for name, (x,y,w,h) in zip(("sink","tub","toilet"),geometry["reuse"]["grime_reuse_display"]):
        q = delta[y:y+h,x:x+w]
        footprint = q[q >= 2]  # ignore untouched pixels and antialias noise
        result["grime"][name] = {"method":"CIE76 on visibly changed footprint at opacity 0.74",
                                 "pixels":len(footprint),"median_delta_e":round(float(np.median(footprint)),3),
                                 "fraction_ge_15":round(float(np.mean(footprint>=15)),4)}
        assert np.median(footprint) >= 15,name
    if (ROOT/"manifest.json").exists():
        manifest = json.loads((ROOT/"manifest.json").read_bytes())
        rows = sorted(manifest["files"],key=lambda row:row["path"])
        for row in rows:
            data = (ROOT/row["path"]).read_bytes()
            assert len(data) == row["bytes"] and sha256(data).hexdigest() == row["sha256"],row["path"]
        payload = "".join(f'{row["sha256"]}  {row["path"]}\n' for row in rows).encode()
        assert sha256(payload).hexdigest() == manifest["payload_sha256"]
    print(json.dumps(result,indent=2))

if __name__ == "__main__":
    verify()

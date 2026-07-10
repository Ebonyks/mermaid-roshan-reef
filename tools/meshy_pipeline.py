#!/usr/bin/env python3
"""GEN2 Meshy lane: gen-2 sprite -> 3D mesh -> auto-rigged skeleton.

Pipeline per role: image-to-3D (meshy, low-poly for the phone target) ->
optional auto-rig -> GLB into gen2/meshy/<role>/ for registry flips.
Key from .secrets/meshy_key or $MESHY_API_KEY - never committed.

Usage:
  python3 tools/meshy_pipeline.py submit <image> <role> [--rig]
  python3 tools/meshy_pipeline.py status
  python3 tools/meshy_pipeline.py harvest
"""
import base64
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.meshy.ai/openapi"
OUT = os.path.join(ROOT, "gen2", "meshy")
STATE = os.path.join(OUT, "tasks.json")
TARGET_POLYCOUNT = 8000  # mobile budget (3-4 year old phone)


def key():
    p = os.path.join(ROOT, ".secrets", "meshy_key")
    return open(p).read().strip() if os.path.exists(p) else os.environ["MESHY_API_KEY"]


def call(method, path, body=None, tries=5):
    for a in range(tries):
        try:
            req = urllib.request.Request(
                API + path,
                data=json.dumps(body).encode() if body is not None else None,
                headers={"Authorization": "Bearer " + key(),
                         "Content-Type": "application/json"},
                method=method)
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa: BLE001
            print(f"  retry {a+1}/{tries}: {e}", flush=True)
            time.sleep(30 * (a + 1))
    raise RuntimeError(f"meshy API failed: {path}")


def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {}


def save_state(st):
    os.makedirs(OUT, exist_ok=True)
    json.dump(st, open(STATE, "w"), indent=1)


def submit(image_path, role, rig=False):
    from PIL import Image
    import io
    im = Image.open(image_path).convert("RGB")
    im.thumbnail((1024, 1024))
    buf = io.BytesIO()
    im.save(buf, "PNG")
    uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    r = call("POST", "/v1/image-to-3d", {
        "image_url": uri,
        "should_remesh": True,
        "should_texture": True,
        "enable_pbr": False,
        "topology": "triangle",
        "target_polycount": TARGET_POLYCOUNT,
    })
    st = load_state()
    st[role] = {"i23d": r["result"], "rig": rig, "src": image_path, "stage": "i23d"}
    save_state(st)
    print(f"submitted {role}: task {r['result']}", flush=True)


def status():
    st = load_state()
    for role, t in st.items():
        r = call("GET", f"/v1/image-to-3d/{t['i23d']}")
        print(f"{role}: {t['stage']} {r['status']} {r.get('progress', '')}%", flush=True)


def harvest():
    st = load_state()
    for role, t in st.items():
        if t.get("stage") == "done":
            continue
        if t["stage"] == "i23d":
            r = call("GET", f"/v1/image-to-3d/{t['i23d']}")
            if r["status"] != "SUCCEEDED":
                print(f"{role}: i23d {r['status']} {r.get('progress', 0)}%", flush=True)
                continue
            d = os.path.join(OUT, role)
            os.makedirs(d, exist_ok=True)
            url = r["model_urls"]["glb"]
            urllib.request.urlretrieve(url, os.path.join(d, "static.glb"))
            print(f"{role}: static.glb downloaded", flush=True)
            if t.get("rig"):
                try:
                    rr = call("POST", "/v1/rigging", {"input_task_id": t["i23d"]}, tries=2)
                    t["rig_task"] = rr["result"]
                    t["stage"] = "rigging"
                    print(f"{role}: rigging task {rr['result']}", flush=True)
                except RuntimeError:
                    # 422 = pose estimation failed (non-biped: tails, fish).
                    # Keep the static mesh; animation stays procedural.
                    t["stage"] = "done"
                    t["note"] = "rigging rejected (pose estimation); static only"
                    print(f"{role}: rigging rejected, keeping static.glb", flush=True)
            else:
                t["stage"] = "done"
        elif t["stage"] == "rigging":
            r = call("GET", f"/v1/rigging/{t['rig_task']}")
            if r["status"] != "SUCCEEDED":
                print(f"{role}: rigging {r['status']} {r.get('progress', 0)}%", flush=True)
                continue
            d = os.path.join(OUT, role)
            urls = r.get("result", r).get("rigged_model_urls", r.get("model_urls", {}))
            glb = urls.get("glb") or urls.get("rigged_character_glb_url")
            if glb:
                urllib.request.urlretrieve(glb, os.path.join(d, "rigged.glb"))
                print(f"{role}: rigged.glb downloaded", flush=True)
            t["stage"] = "done"
        save_state(st)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "status"
    if mode == "submit":
        rig = "--rig" in sys.argv
        submit(sys.argv[2], sys.argv[3], rig)
    elif mode == "status":
        status()
    elif mode == "harvest":
        harvest()

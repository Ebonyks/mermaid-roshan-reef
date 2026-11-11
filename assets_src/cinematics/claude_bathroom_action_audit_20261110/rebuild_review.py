"""Build the offline review from manifest-bound scene inputs with silent cues."""
from argparse import ArgumentParser
from pathlib import Path
import base64
import io
import json
import wave

ROOT = Path(__file__).resolve().parent

def read(name):
    return (ROOT / name).read_bytes()

def load(name):
    return json.loads(read(name))

def encode(data):
    return base64.b64encode(data).decode("ascii")

def silent_cue():
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setparams((1, 1, 8000, 0, "NONE", "not compressed"))
        wav.writeframes(bytes([128]) * 160)
    return "data:audio/wav;base64," + encode(buffer.getvalue())

def data_url(row):
    return row["prefix"] + encode(read(row["path"]))

def build():
    inputs = load("raw/scene/inputs.json")
    payload = {name: data_url(row) for name, row in inputs["room_and_prop"].items()}
    for name in ("sinkVoice", "tubVoice", "toiletVoice"):
        payload[name] = silent_cue()
    payload.update({
        "rig": encode(read("raw/rig/roshan_arm_rebound.rigby")),
        "rigbyLicense": read("raw/renderer/LICENSE-MIT.txt").decode(),
        "outlines": load("raw/scene/fixture_outlines.json"),
        "visibility": load("raw/scene/visible_triangles.json"),
        "acting": load("raw/scene/acting_profile.json"),
    })
    for name, group in inputs["groups"].items():
        payload[name] = {key: data_url(row) for key, row in group.items()}
    imports = {"imports": {key: "data:text/javascript;base64," + encode(read(path))
                           for key, path in inputs["modules"].items()}}
    html = read("raw/scene/scene_template.html").decode()
    scene = read("raw/scene/scene.mjs").decode()
    return html.replace("@@IMPORTS@@", json.dumps(imports)).replace(
        "@@PAYLOAD@@", json.dumps(payload)).replace("@@SCENE@@", scene).encode()

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "bathroom_playtest.html")
    args = parser.parse_args()
    args.output.write_bytes(build())
    print(args.output)

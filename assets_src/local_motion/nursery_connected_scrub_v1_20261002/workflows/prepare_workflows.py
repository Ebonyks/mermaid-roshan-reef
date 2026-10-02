"""Prepare native-node Wan workflows and a neutral installation test fixture."""
import copy
import hashlib
import json
from pathlib import Path
import uuid

from PIL import Image, ImageDraw
import requests

ROOT = Path(r"H:\MermaidReefTools\LocalVideo")
PRESETS = {
    "quick": dict(width=512, height=288, frames=33, steps=12, weight_dtype="fp8_e4m3fn"),
    "study": dict(width=640, height=352, frames=49, steps=20, weight_dtype="fp8_e4m3fn"),
    "detail": dict(width=960, height=544, frames=81, steps=30, weight_dtype="default"),
    "smoke": dict(width=256, height=160, frames=5, steps=2, weight_dtype="default"),
}
POSITIVE = (
    "Locked camera. Preserve the illustrated input composition, palette and painted style. "
    "Only the specified subject moves gently; all other objects remain stationary. "
    "One continuous shot, no scene change. Sound: silence."
)
NEGATIVE = (
    "camera movement, zoom, pan, cut, photorealism, 3D shading, new objects, "
    "changing architecture, moving shoreline, moving roots, flicker, color pumping, "
    "warped shapes, subtitles, text, watermark"
)
MODEL = "wan2.2_ti2v_5B_fp16.safetensors"
ENCODER = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
VAE = "wan2.2_vae.safetensors"


def api_graph(preset, image="neutral_calibration.png", prompt=POSITIVE, seed=20260930, prefix="local_reference/test"):
    setting = PRESETS[preset]
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": MODEL, "weight_dtype": setting["weight_dtype"]}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": ENCODER, "type": "wan", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "4": {"class_type": "LoadImage", "inputs": {"image": image}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": NEGATIVE}},
        "7": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["1", 0], "shift": 8.0}},
        "8": {"class_type": "Wan22ImageToVideoLatent", "inputs": {
            "vae": ["3", 0], "width": setting["width"], "height": setting["height"],
            "length": setting["frames"], "batch_size": 1, "start_image": ["4", 0]}},
        "9": {"class_type": "KSampler", "inputs": {
            "model": ["7", 0], "positive": ["5", 0], "negative": ["6", 0],
            "latent_image": ["8", 0], "seed": seed, "steps": setting["steps"], "cfg": 5.0,
            "sampler_name": "uni_pc", "scheduler": "simple", "denoise": 1.0}},
        "10": {"class_type": "VAEDecodeTiled", "inputs": {
            "samples": ["9", 0], "vae": ["3", 0], "tile_size": 256,
            "overlap": 64, "temporal_size": 16, "temporal_overlap": 4}},
        "11": {"class_type": "SaveWEBM", "inputs": {
            "images": ["10", 0], "filename_prefix": prefix, "codec": "vp9", "fps": 24.0, "crf": 18.0}},
    }


def main():
    source_url = "https://comfyanonymous.github.io/ComfyUI_examples/wan22/image_to_video_wan22_5B.json"
    response = requests.get(source_url, timeout=60)
    response.raise_for_status()
    source = response.json()
    (ROOT / "workflows" / "official_wan22_5b_i2v.json").write_bytes(response.content)
    (ROOT / "workflows" / "SOURCE_RECEIPT.json").write_text(json.dumps({
        "source": source_url, "sha256": hashlib.sha256(response.content).hexdigest(),
        "derived_presets": PRESETS, "status": "LOCAL_MOTION_REFERENCE_ONLY",
    }, indent=2), encoding="utf-8")

    image = Image.new("RGB", (512, 288), (238, 232, 219))
    draw = ImageDraw.Draw(image)
    draw.ellipse((185, 94, 279, 188), fill=(60, 155, 183))
    image.save(ROOT / "input" / "neutral_calibration.png")

    user_workflows = ROOT / "user" / "default" / "workflows" / "LocalVideo"
    user_workflows.mkdir(parents=True, exist_ok=True)
    for name, setting in PRESETS.items():
        workflow = copy.deepcopy(source)
        workflow["id"] = str(uuid.uuid4())
        workflow["nodes"] = [n for n in workflow["nodes"] if n["id"] != 28]
        workflow["links"] = [link for link in workflow["links"] if link[0] != 56]
        for node in workflow["nodes"]:
            if node["type"] == "VAEDecode":
                node["type"] = "VAEDecodeTiled"
                node["properties"]["Node name for S&R"] = "VAEDecodeTiled"
                node["widgets_values"] = [256, 64, 16, 4]
                for output in node["outputs"]:
                    output["links"] = [link for link in output.get("links", []) if link != 56]
            elif node["type"] == "KSampler":
                node["widgets_values"] = [20260930, "fixed", setting["steps"], 5.0, "uni_pc", "simple", 1.0]
            elif node["type"] == "UNETLoader":
                node["widgets_values"] = [MODEL, setting["weight_dtype"]]
            elif node["type"] == "Wan22ImageToVideoLatent":
                node["widgets_values"] = [setting["width"], setting["height"], setting["frames"], 1]
            elif node["type"] == "LoadImage":
                node["widgets_values"] = ["neutral_calibration.png", "image"]
            elif node["type"] == "CLIPTextEncode":
                node["widgets_values"] = [NEGATIVE if node["id"] == 7 else POSITIVE]
            elif node["type"] == "SaveWEBM":
                node["widgets_values"] = [f"local_reference/{name}", "vp9", 24.0, 18.0]
            elif node["type"] == "Note":
                node["widgets_values"] = [
                    f"{name.upper()} — local motion reference only. Choose a source image and describe one action. "
                    "This does not establish cinematic delivery acceptance. Native 24 fps; no interpolation. "
                    "All model/input/output storage is on H:. Tiled decode limits VRAM. "
                    "The neutral calibration image is an installation fixture, not game artwork."
                ]
        payload = json.dumps(workflow, indent=2, ensure_ascii=False)
        filename = f"Wan22_3060Ti_{name}.json"
        (ROOT / "workflows" / filename).write_text(payload, encoding="utf-8")
        (user_workflows / filename).write_text(payload, encoding="utf-8")
        (ROOT / "workflows" / f"{name}.api.json").write_text(
            json.dumps(api_graph(name), indent=2), encoding="utf-8")
    prompts = {
        "water": "Locked camera. Preserve the input painted water and its colors. Only the broad water highlights drift gently sideways. Shoreline, rocks, bridge and castle remain completely still. One continuous shot. Sound: silence.",
        "plant": "Locked camera. Preserve the input illustrated plant, exact leaves, berries, colors and outline. One tiny breeze bends the upper branches, with slight leaf lag, then they settle. Roots stay exactly fixed. No new foliage. Sound: silence.",
        "shoreline": "Locked camera. Preserve the exact input painted shoreline and rocks. One small water lap reaches the fixed rocks and gently recedes. No neon foam, no moving shore, no camera movement. Sound: silence.",
    }
    (ROOT / "SKY_LAGOON_PROMPTS.json").write_text(json.dumps(prompts, indent=2), encoding="utf-8")
    print("Created native-node UI and API workflows: quick, study, detail, smoke.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render a non-runtime A/B set for a lighter synthetic Roshan voice.

The output is review evidence only. It never writes under runtime ``assets/``.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
from pathlib import Path

import soundfile as sf
import torch
from huggingface_hub import snapshot_download
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer, set_seed


ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = "parler-tts/parler-tts-mini-v1.1"
MODEL_REVISION = "fbb2dd281092c5b414ef29cf9d8895f386f1feef"
DESCRIPTION_TOKENIZER_REVISION = "0613663d0d48ea86ba8cb3d7a44f0f65dc596a2a"
PARLER_CODE_REVISION = "d108732cd57788ec86bc857d99a6cabd66663d68"
DEFAULT_OUT = ROOT / "assets_src" / "audio" / "roshan_voice_auditions_2026-08-31"

LINES = {
    "happy": "Yay! This is so much fun!",
    "calm": "It's okay, little fish. I'll help you.",
    "urgent": "Quick! The dust bunnies are getting away!",
    "wonder": "Wow! The whole castle is sparkling!",
    "castle_context": "This castle is so dusty!",
}

PRESETS = {
    "jenna_child_bright": (
        "Jenna's voice is a very young, tiny, bright feminine storybook-child voice "
        "with a very high natural pitch. She sounds playful, curious, spontaneous, and "
        "warm, never adult, breathy, sultry, or low. Her delivery is lively and naturally "
        "varied, with crisp child-readable consonants and a small youthful vocal size."
    ),
    "lea_child_light": (
        "Lea's voice is a very young, light, sweet feminine storybook-child voice with a "
        "very high natural pitch. She sounds innocent, eager, affectionate, and naturally "
        "animated, never adult, breathy, sultry, or low. Her words are crisp and easy for "
        "a young child to understand from a small tablet speaker."
    ),
    "laura_high_baseline": (
        "Laura's voice is a very young, tiny feminine storybook-child voice with an "
        "extremely high natural pitch and a small youthful vocal size. She sounds playful "
        "and spontaneous, never adult, breathy, sultry, or low. Her delivery has bright "
        "crisp consonants and naturally varied childlike intonation."
    ),
    "tina_child_tiny": (
        "Tina's voice is a very young, tiny, clear feminine storybook-child voice with a "
        "very high natural pitch and a small youthful vocal size. She sounds curious, "
        "playful, warm, and spontaneous, never adult, breathy, squeaky, sultry, or low. "
        "Her delivery has crisp child-readable consonants and naturally varied intonation."
    ),
    "joy_child_spark": (
        "Joy's voice is a very young, bright, clear feminine storybook-child voice with a "
        "very high natural pitch and a small youthful vocal size. She sounds eager, "
        "affectionate, playful, and spontaneous, never adult, breathy, sultry, or low. "
        "Her delivery has crisp child-readable consonants and naturally varied intonation."
    ),
}

MOOD_DIRECTION = {
    "happy": "She is delighted and giggly, with a quick bright rise and genuine excitement.",
    "calm": "She is tender and reassuring, with soft warmth but no loss of clarity or pitch.",
    "urgent": "She is breathlessly urgent but never frightened, harsh, shouted, or rushed into slurring.",
    "wonder": "She is openly amazed, with a bright rising melody and one natural pause.",
    "castle_context": "She has just noticed a funny mess and reacts with surprised playful disbelief.",
}

QUALITY_DIRECTION = (
    " The studio recording is very clear, dry, close-up, clean, and free of noise, "
    "reverberation, hiss, distortion, robotic cadence, and vocoder artifacts. She speaks "
    "the provided line exactly once with no skipped, substituted, repeated, or extra words."
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seed_for(preset: str, line_key: str, attempt: int) -> int:
    payload = f"reef-roshan-audition-v1:{preset}:{line_key}:{attempt}".encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:4], "big") & 0x7FFFFFFF


def artifact_hashes(snapshot: Path) -> dict[str, str]:
    suffixes = {".json", ".model", ".safetensors", ".txt"}
    return {
        path.relative_to(snapshot).as_posix(): sha256(path)
        for path in sorted(snapshot.rglob("*"))
        if path.is_file() and path.suffix in suffixes
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--attempt", type=int, default=1)
    parser.add_argument("--preset", action="append", choices=sorted(PRESETS))
    parser.add_argument("--line", action="append", choices=sorted(LINES))
    args = parser.parse_args()

    out = args.out.resolve()
    if ROOT not in out.parents or "assets" in out.parts:
        parser.error("--out must be a non-runtime path inside this repository")
    raw_dir = out / "raw"
    review_dir = out / "review"
    raw_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    presets = args.preset or list(PRESETS)
    lines = args.line or list(LINES)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device.startswith("cuda") else torch.float32
    model = ParlerTTSForConditionalGeneration.from_pretrained(
        MODEL_ID, revision=MODEL_REVISION, torch_dtype=dtype, local_files_only=True,
    ).to(device)
    prompt_tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, revision=MODEL_REVISION, local_files_only=True,
    )
    description_tokenizer = AutoTokenizer.from_pretrained(
        model.config.text_encoder._name_or_path,
        revision=DESCRIPTION_TOKENIZER_REVISION,
        local_files_only=True,
    )
    model_snapshot = Path(snapshot_download(
        MODEL_ID, revision=MODEL_REVISION, local_files_only=True,
    ))
    tokenizer_snapshot = Path(snapshot_download(
        model.config.text_encoder._name_or_path,
        revision=DESCRIPTION_TOKENIZER_REVISION,
        local_files_only=True,
    ))
    ffmpeg_version = subprocess.run(
        ["ffmpeg", "-version"], check=True, capture_output=True, text=True,
    ).stdout.splitlines()[0]

    run = {
        "purpose": "NON_RUNTIME_SYNTHETIC_ROSHAN_PRESET_AUDITION",
        "rights": "Apache-2.0 model; named preset synthesis; no voice cloning or reference audio",
        "model": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "model_artifact_sha256": artifact_hashes(model_snapshot),
        "description_tokenizer": model.config.text_encoder._name_or_path,
        "description_tokenizer_revision": DESCRIPTION_TOKENIZER_REVISION,
        "description_tokenizer_artifact_sha256": artifact_hashes(tokenizer_snapshot),
        "parler_code_revision": PARLER_CODE_REVISION,
        "python": sys.version,
        "platform": platform.platform(),
        "device": device,
        "cuda_version": torch.version.cuda,
        "packages": {
            name: importlib.metadata.version(name)
            for name in ("parler-tts", "torch", "transformers", "soundfile")
        },
        "ffmpeg": ffmpeg_version,
        "generator_sha256": sha256(Path(__file__)),
        "attempt": args.attempt,
    }
    (out / "run_provenance.json").write_text(
        json.dumps(run, indent=2, sort_keys=True) + "\n", encoding="utf-8",
    )

    manifest_path = out / "manifest.json"
    manifest_by_key: dict[tuple[str, str], dict[str, object]] = {}
    if manifest_path.exists():
        for row in json.loads(manifest_path.read_text(encoding="utf-8")):
            manifest_by_key[(str(row["preset_id"]), str(row["line_key"]))] = row
    for preset in presets:
        for line_key in lines:
            text = LINES[line_key]
            seed = seed_for(preset, line_key, args.attempt)
            description = PRESETS[preset] + " " + MOOD_DIRECTION[line_key] + QUALITY_DIRECTION
            set_seed(seed)
            description_inputs = description_tokenizer(description, return_tensors="pt").to(device)
            prompt_inputs = prompt_tokenizer(text, return_tensors="pt").to(device)
            with torch.inference_mode():
                generation = model.generate(
                    input_ids=description_inputs.input_ids,
                    attention_mask=description_inputs.attention_mask,
                    prompt_input_ids=prompt_inputs.input_ids,
                    prompt_attention_mask=prompt_inputs.attention_mask,
                )
            audio = generation.float().cpu().reshape(-1).numpy()
            stem = f"{preset}__{line_key}"
            raw_path = raw_dir / f"{stem}.wav"
            review_path = review_dir / f"{stem}.ogg"
            sf.write(raw_path, audio, model.config.sampling_rate)
            ffmpeg_command = [
                "ffmpeg", "-y", "-i", str(raw_path), "-ac", "1", "-ar", "48000",
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "libvorbis",
                "-b:a", "96k", str(review_path),
            ]
            subprocess.run(ffmpeg_command, check=True, capture_output=True)
            manifest_by_key[(preset, line_key)] = {
                "preset_id": preset,
                "named_speaker": PRESETS[preset].split("'", 1)[0],
                "line_key": line_key,
                "text": text,
                "description": description,
                "seed": seed,
                "attempt": args.attempt,
                "sampling_rate_raw": model.config.sampling_rate,
                "raw_path": raw_path.relative_to(ROOT).as_posix(),
                "raw_sha256": sha256(raw_path),
                "review_path": review_path.relative_to(ROOT).as_posix(),
                "review_sha256": sha256(review_path),
                "ffmpeg_command": ffmpeg_command,
                "model": MODEL_ID,
                "model_revision": MODEL_REVISION,
                "status": "OPEN_HUMAN_LISTENING_REVIEW",
            }
            print(f"ROSHAN_AUDITION|{preset}|{line_key}|seed={seed}|{review_path}", flush=True)
    manifest = [manifest_by_key[key] for key in sorted(manifest_by_key)]
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

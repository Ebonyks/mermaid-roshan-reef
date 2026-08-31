#!/usr/bin/env python3
"""Render fixed-speaker, mood-described Parler-TTS candidates for A/B review."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import platform
import subprocess
import sys
from pathlib import Path

import soundfile as sf
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer, set_seed
from huggingface_hub import snapshot_download


ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = "parler-tts/parler-tts-mini-v1.1"
MODEL_REVISION = "fbb2dd281092c5b414ef29cf9d8895f386f1feef"
DESCRIPTION_TOKENIZER_REVISION = "0613663d0d48ea86ba8cb3d7a44f0f65dc596a2a"
PARLER_CODE_REVISION = "d108732cd57788ec86bc857d99a6cabd66663d68"
DEFAULT_OUT = ROOT / "tmp" / "parler_voice_trials"

SPEAKERS = {
    "roshan": "Laura",
    "huluu": "Lea",
    "evie": "Jenna",
    "harper": "Lauren",
    "wacky": "Gary",
    "shop": "Jon",
    "sparkle": "Tina",
    "rosalina": "Rose",
    "imp": "Mike",
    "rumi": "Emily",
    "mewsha": "Joy",
    "daddy": "Will",
}

# Delivery-only components for the live group cheer.  They are rendered with
# the same pinned synthetic presets as ordinary lines, then mixed into the
# single ``everyone.ogg`` runtime cue by master_filler_voices.py.  Component
# WAVs remain build evidence and never ship as separate dialogue keys.
GROUP_COMPONENTS = {
    "everyone_roshan": ("roshan", "Hooray!"),
    "everyone_huluu": ("huluu", "Hooray!"),
    "everyone_evie": ("evie", "Hooray!"),
}

MOODS = {
    "gentle": "soft, warm, tender and soothing, with slow natural pacing and restrained expression",
    "guiding": "friendly, encouraging and clearly articulated, with lively natural pacing",
    "wonder": "genuinely amazed and delighted, with bright rising intonation and natural pauses",
    "celebrate": "joyful, proud and warmly excited, with animated but controlled expression",
    "concern": "gently worried yet reassuring, with sincere emotion and clear articulation",
    "mischief": "playfully mischievous and theatrical, with a cheeky grin in the voice",
    "comic": "playful and funny, with expressive timing and a harmless cartoon energy",
}


def load_legacy_module():
    spec = importlib.util.spec_from_file_location("legacy_make_voices", ROOT / "tools" / "make_voices.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load tools/make_voices.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mood_for(key: str, text: str) -> str:
    low = f"{key} {text}".lower()
    if key.startswith("imp_"):
        if "_steal" in key or key.endswith("captain"):
            return "mischief"
        if "_bop" in key or key.endswith("retry"):
            return "comic"
        return "guiding"
    if any(word in low for word in ("bedtime", "sleep", "shhh", "snuggle", "little star")):
        return "gentle"
    if any(word in low for word in ("oh no", "storm", "aww", "try again", "hungry", "not yet")):
        return "concern"
    if any(word in low for word in ("yay", "hooray", "you did it", "great job", "hero", "amazing", "saved")):
        return "celebrate"
    if any(word in low for word in ("wow", "ooh", "treasure", "sparkly", "rainbow pearl", "what's inside")):
        return "wonder"
    if any(word in low for word in ("beans", "oops", "bumper", "wet", "ho ho")):
        return "comic"
    return "guiding"


def seed_for(key: str, attempt: int) -> int:
    digest = hashlib.sha256(f"reef-parler-v1:{key}:{attempt}".encode()).digest()
    return int.from_bytes(digest[:4], "big") & 0x7FFFFFFF


def artifact_hashes(snapshot: Path) -> dict[str, str]:
    suffixes = {".json", ".model", ".safetensors", ".txt"}
    return {
        path.relative_to(snapshot).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(snapshot.rglob("*"))
        if path.is_file() and path.suffix in suffixes
    }


def spoken_text_for(text: str) -> str:
    """Use pronunciation-friendly spellings without changing line meaning."""
    spoken = text.replace("\ufffd", " — ")
    for authored, spoken_form in {
        "Woooow": "Wow", "Whoooaa": "Whoa", "Wheee": "Whee",
        "Aww": "Aw", "Tee hee": "Tee-hee", "Lamb-a'": "Lamba",
        "Shhhh": "Shh", "SHHH": "Shh", "Shhh": "Shh",
    }.items():
        spoken = spoken.replace(authored, spoken_form)
    return spoken


KEY_SPOKEN_TEXT = {
    "mewsha_win": "I'm coming along beside you now! Swish swish!",
    "roshan_op_detective_tiara_chase": (
        "The thief ran away! Tap every lookout!"
    ),
    "roshan_op_ballerina_ribbon_chase": (
        "The ribbon thief ran away! Spin and tap everyone!"
    ),
    "roshan_op_farmer_piggy_chase": (
        "The piggy gate is open! Tap everyone!"
    ),
    "roshan_op_painter_imps": "What a paint mess! Tap each one!",
    "imp_op_chef_bop": "Fine! The cake needed more sugar anyway!",
    "imp_op_farmer_bop": "Bleh! I got mud in my mouth.",
    "imp_op_boxer_arrive": "I was sent to learn the bouncing. Put them up!",
    "imp_op_astronaut_arrive": (
        "I was sent to learn the sending. Nobody sends us anything."
    ),
    "imp_op_popstar_arrive": "I learned a new song. Listen to me sing!",
    "imp_op_nursery_copy": "I tried to be quiet. Sorry! Sorry!",
    "roshan_op_magician_work": "Watch closely... magic!",
}

KEY_SPOKEN_SEGMENTS = {
    "mewsha_win": ["I'm coming along beside you now!", "Swish swish!"],
    "roshan_op_detective_tiara_chase": [
        "The thief ran away!", "Tap every lookout!",
    ],
    "roshan_op_ballerina_ribbon_chase": [
        "The ribbon thief ran away!", "Spin and tap everyone!",
    ],
    "roshan_op_farmer_piggy_chase": [
        "The piggy gate is open!", "Tap everyone!",
    ],
    "imp_op_chef_bop": ["Fine!", "The cake needed more sugar anyway!"],
    "roshan_op_magician_work": ["Watch closely.", "Magic!"],
    "rosalina_win": [
        "You saved the Butterfly World!",
        "Fairy Roshan is waiting in the castle wardrobe!",
    ],
    "roshan_dustboss_dizzy_first": [
        "He is dizzy!", "His ears are spinning!",
    ],
    "roshan_dustboss_dizzy_round": [
        "Bonk, bonk, bonk! He is all dizzy.", "His ears are spinning!",
    ],
    "roshan_dustboss_tell_dim": [
        "Wait! Do not tap the dim star.", "Tap the big gold star!",
    ],
    "roshan_dustboss_dodge": [
        "The dust boss is coming close!", "Press the twirl button!",
    ],
    "roshan_day_two_begins": [
        "The second day is here!",
        "Visit castle jobs and the Opera House!",
    ],
    "roshan_op_chef_cake_chase": [
        "The imp captain snatched the cake!", "Bop the crew to the stage door!",
    ],
    "roshan_op_candymaker_candy_chase": [
        "The candy cart rolled away!", "Tap each tiny troublemaker!",
    ],
    "roshan_op_doctor_plushy_chase": [
        "The plushy patient is missing!", "Tap the imp crew!",
    ],
    "roshan_op_magician_bunny_chase": [
        "Find the little lamb!", "Tap each tiny troublemaker!",
    ],
    "roshan_op_astronaut_rocket_chase": [
        "Our rocket rolled away!", "Tap each tiny troublemaker!",
    ],
    "roshan_op_popstar_mic_chase": [
        "The microphone is unplugged!", "Tap the noisy band!",
    ],
}


def description_for(character: str, mood: str, text: str) -> str:
    speaker = SPEAKERS[character]
    identity = {
        "roshan": "a youthful, bright feminine voice with a moderately high natural pitch",
        "huluu": "an elegant, gentle feminine storybook-princess voice",
        "evie": "a bubbly, youthful feminine voice",
        "harper": "a warm big-sister feminine voice",
        "wacky": "a kindly older masculine voice",
        "shop": "a welcoming adult masculine voice",
        "sparkle": "a tiny, bright and chirpy feminine creature voice",
        "rosalina": "a dreamy, calm feminine fairy-tale voice",
        "imp": "a youthful, impish masculine cartoon voice with a moderately high natural pitch",
        "rumi": "a warm, friendly youthful feminine voice",
        "mewsha": "a playful, bright feminine storybook-kitty voice",
        "daddy": "a warm, reassuring adult masculine voice",
    }[character]
    pronoun = "He" if character in {"wacky", "shop", "imp", "daddy"} else "She"
    pronunciation_hints: list[str] = []
    for token, hint in {
        "Roshan": "ROH-shahn", "Huluu": "hoo-LOO", "Rumi": "ROO-mee",
        "Mewsha": "MYOO-sha", "Kareem": "kuh-REEM", "Rosalina": "roh-zah-LEE-nah",
        "Lamba": "LAM-bah", "Lamb-a": "LAM-bah", "tiara": "tee-AR-uh",
        "plushy": "PLUSH-ee", "flour": "FLOW-er, the baking ingredient",
        "kart": "KART", "pearl": "PURL", "quiet": "KWY-et",
        "mending": "MEN-ding", "bouncing": "BOWN-sing",
        "sending": "SEN-ding", "singing": "SING-ing",
        "BONK": "BONK with a crisp final k", "Blegh": "BLEH",
        "Ta-daa": "tah-DAH", "TA-DAA": "tah-DAH",
    }.items():
        if token.lower() in text.lower():
            pronunciation_hints.append(f"{token} as {hint}")
    if "imp" in text.lower():
        pronunciation_hints.append("imp and imps with a clear short i and a crisp final p")
    if "bop" in text.lower():
        pronunciation_hints.append("bop with a voiced initial b and crisp final p, never pop or bought")
    if "shh" in text.lower():
        pronunciation_hints.append("shh as a short soft breathy hush, never shay, she, or a spoken word")
    pronunciation = (
        " Pronounce " + ", and ".join(pronunciation_hints) + "."
        if pronunciation_hints else ""
    )
    return (
        f"{speaker}'s voice is {identity}, {MOODS[mood]}. "
        f"{pronoun} speaks the provided line exactly as written, with crisp consonants, "
        "complete words, steady identity and no skipped, substituted, repeated, or extra words. "
        "Even in a soft mood the pitch stays consistent and every consonant remains bright enough "
        "for a small tablet speaker. The studio recording is very clear, dry, close-up, and free "
        "of background noise, reverberation, hiss, distortion, robotic cadence, and vocoder artifacts."
        + pronunciation
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--line", action="append", default=[])
    parser.add_argument("--keys-file", type=Path)
    parser.add_argument("--missing-from", type=Path)
    parser.add_argument("--attempt", type=int, default=1)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    legacy = load_legacy_module()
    requested = set(args.line)
    if args.keys_file:
        requested.update(
            line.strip() for line in args.keys_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    if args.missing_from:
        available: set[tuple[str, str]] = set()
        for path in sorted(args.missing_from.glob("attempt_*/*manifest.json")):
            for row in json.loads(path.read_text(encoding="utf-8")):
                available.add((str(row["key"]), str(row.get("speaker", ""))))
        requested.update(
            key for key, (character, _text) in legacy.LINES.items()
            if character != "faron" and (key, SPEAKERS[character]) not in available
        )
    catalog = dict(legacy.LINES)
    catalog.update(GROUP_COMPONENTS)
    unknown = sorted(requested - set(catalog))
    if unknown:
        parser.error("unknown --line key(s): " + ", ".join(unknown))
    selected = {
        key: value for key, value in catalog.items()
        if value[0] != "faron" and (not requested or key in requested)
    }
    out_dir = args.out.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device.startswith("cuda") else torch.float32
    model = ParlerTTSForConditionalGeneration.from_pretrained(
        MODEL_ID, revision=MODEL_REVISION, torch_dtype=dtype,
    ).to(device)
    prompt_tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    description_tokenizer = AutoTokenizer.from_pretrained(
        model.config.text_encoder._name_or_path,
        revision=DESCRIPTION_TOKENIZER_REVISION,
    )
    model_snapshot = Path(snapshot_download(MODEL_ID, revision=MODEL_REVISION, local_files_only=True))
    tokenizer_snapshot = Path(snapshot_download(
        model.config.text_encoder._name_or_path,
        revision=DESCRIPTION_TOKENIZER_REVISION,
        local_files_only=True,
    ))
    ffmpeg_version = subprocess.run(
        ["ffmpeg", "-version"], capture_output=True, text=True, check=True,
    ).stdout.splitlines()[0]
    run_provenance = {
        "model": MODEL_ID, "model_revision": MODEL_REVISION,
        "model_artifact_sha256": artifact_hashes(model_snapshot),
        "description_tokenizer": model.config.text_encoder._name_or_path,
        "description_tokenizer_revision": DESCRIPTION_TOKENIZER_REVISION,
        "description_tokenizer_artifact_sha256": artifact_hashes(tokenizer_snapshot),
        "parler_code_revision": PARLER_CODE_REVISION,
        "packages": {
            name: importlib.metadata.version(name)
            for name in ("parler-tts", "torch", "transformers", "soundfile")
        },
        "python": sys.version, "platform": platform.platform(),
        "cuda_available": torch.cuda.is_available(),
        "cuda_version": torch.version.cuda, "device": device,
        "ffmpeg": ffmpeg_version,
        "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "attempt": args.attempt,
    }
    (out_dir / "run_provenance.json").write_text(
        json.dumps(run_provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest: list[dict[str, object]] = []
    for key, (character, text) in selected.items():
        mood = mood_for(key, text)
        description = description_for(character, mood, text)
        spoken_text = KEY_SPOKEN_TEXT.get(key, spoken_text_for(text))
        spoken_segments = KEY_SPOKEN_SEGMENTS.get(key, [spoken_text])
        seed = seed_for(key, args.attempt)
        description_inputs = description_tokenizer(description, return_tensors="pt").to(device)
        audio_parts: list[torch.Tensor] = []
        segment_seeds: list[int] = []
        for segment_index, segment_text in enumerate(spoken_segments):
            segment_seed = (seed + segment_index * 104729) & 0x7FFFFFFF
            segment_seeds.append(segment_seed)
            set_seed(segment_seed)
            prompt_inputs = prompt_tokenizer(segment_text, return_tensors="pt").to(device)
            with torch.inference_mode():
                generation = model.generate(
                    input_ids=description_inputs.input_ids,
                    attention_mask=description_inputs.attention_mask,
                    prompt_input_ids=prompt_inputs.input_ids,
                    prompt_attention_mask=prompt_inputs.attention_mask,
                )
            if audio_parts:
                audio_parts.append(torch.zeros(round(model.config.sampling_rate * 0.12)))
            audio_parts.append(generation.float().cpu().reshape(-1))
        rendered_audio = torch.cat(audio_parts).numpy()
        raw_path = out_dir / f"{key}.wav"
        sf.write(raw_path, rendered_audio, model.config.sampling_rate)
        manifest.append({
            "key": key, "character": character, "text": text,
            "generation_text": spoken_text, "generation_segments": spoken_segments,
            "segment_seeds": segment_seeds, "mood": mood,
            "speaker": SPEAKERS[character], "description": description,
            "seed": seed, "attempt": args.attempt, "raw_path": str(raw_path),
            "raw_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
            "model": MODEL_ID, "model_revision": MODEL_REVISION,
            "description_tokenizer_revision": DESCRIPTION_TOKENIZER_REVISION,
        })
        print(f"PARLER_VOICE|{key}|{mood}|seed={seed}|{raw_path}", flush=True)
    (out_dir / "trial_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

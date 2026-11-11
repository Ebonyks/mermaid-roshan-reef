
"""Generate the neutral Grand Puff Guide cue with the pinned local Kokoro model."""
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import onnxruntime as ort
import soundfile as sf
from kokoro_onnx.tokenizer import Tokenizer

ROOT = Path(__file__).resolve().parents[3]
SOURCE = Path(__file__).resolve().parent
TEXT = "Help scrub the dust off now!"
KEY = "guide_puff_scrub"
EXPECTED = {
    "model.onnx": "8fbea51ea711f2af382e88c833d9e288c6dc82ce5e98421ea61c058ce21a34cb",
    "voices.bin": "b58979d4eb5b1fdbe783c93f9f43c21217cb8f07af9d3860547371a5b2c8b646",
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def ffmpeg(*args):
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args],
                          capture_output=True, text=True, check=True).stderr


def main(cache):
    assert {name: digest(cache / name) for name in EXPECTED} == EXPECTED
    native = SOURCE / f"{KEY}.wav"
    output = ROOT / "assets/audio/objective_guides" / f"{KEY}.ogg"
    assert not native.exists() and not output.exists()
    tokenizer = Tokenizer()
    phonemes = tokenizer.phonemize(TEXT, lang="en-us")
    tokens = tokenizer.tokenize(phonemes)
    options = ort.SessionOptions()
    options.intra_op_num_threads = 2
    options.inter_op_num_threads = 1
    options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
    session = ort.InferenceSession(str(cache / "model.onnx"), sess_options=options,
                                   providers=["CPUExecutionProvider"])
    audio = session.run(None, {
        "input_ids": np.array([[0, *tokens, 0]], dtype=np.int64),
        "style": np.load(cache / "voices.bin")["af_heart"][len(tokens)],
        "speed": np.full(1, 1.0, dtype=np.float32),
    })[0].reshape(-1)
    assert audio.size and np.isfinite(audio).all() and np.max(np.abs(audio)) < 1.0
    sf.write(native, audio, 24000, subtype="FLOAT")
    audible = np.flatnonzero(np.abs(audio) > 0.001)
    first = max(0, int(audible[0]) - 960)
    end = min(audio.size, int(audible[-1]) + 2401)
    conditioning = (f"atrim=start_sample={first}:end_sample={end},asetpts=PTS-STARTPTS,"
                    "highpass=f=40,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80")
    target = "loudnorm=I=-16:TP=-2.8:LRA=7"
    report = ffmpeg("-i", str(native), "-af", f"{conditioning},{target}:print_format=json", "-f", "null", "-")
    measured = json.JSONDecoder().raw_decode(report[report.rfind("{"):])[0]
    mastering = (f"{conditioning},{target}:measured_I={measured['input_i']}"
                 f":measured_TP={measured['input_tp']}:measured_LRA={measured['input_lra']}"
                 f":measured_thresh={measured['input_thresh']}:offset={measured['target_offset']}:linear=true")
    ffmpeg("-n", "-i", str(native), "-af", mastering, "-ar", "48000", "-ac", "1",
           "-c:a", "libvorbis", "-q:a", "4", "-map_metadata", "-1", str(output))
    metadata = {
        "text": TEXT, "voice": "af_heart", "language": "en-us", "speed": 1.0,
        "phonemes": phonemes, "local_synthesis_calls": 1, "paid_api_calls": 0,
        "upstream_model": "https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX",
        "model_license": "Apache-2.0",
        "input_hashes": EXPECTED,
        "versions": {p: version(p) for p in ("onnxruntime", "kokoro-onnx", "numpy", "soundfile")},
        "ffmpeg_version": subprocess.check_output(["ffmpeg", "-version"], text=True).splitlines()[0],
        "generator_sha256": digest(Path(__file__)),
        "native_sha256": digest(native), "native_sample_rate": 24000,
        "output_sha256": digest(output), "output_codec": "Vorbis 48 kHz mono, q4",
        "mastering_filter": mastering,
        "family_recordings_used": False,
    }
    (SOURCE / "provenance.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]))

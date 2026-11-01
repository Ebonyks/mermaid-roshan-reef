"""Adapt the sealed, inspected neutral-Guide recipe for this owner task only.

The historical source and all family audio remain unchanged. This preparation
step performs no synthesis; the resulting frozen producer has its own guards.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
source = ROOT / 'assets_src/audio/objective_guides_20261014/generate_candidates_source.py'
text = source.read_text(encoding='utf-8')


def replace_once(old: str, new: str) -> None:
    global text
    if text.count(old) != 1:
        raise RuntimeError('Sealed recipe anchor changed: ' + old[:80])
    text = text.replace(old, new, 1)


replace_once('Two owner-authorized neutral Guide review candidates',
             'Five owner-directed Grand Puff care-story neutral Guide candidates')
replace_once('OUT = Path(__file__).resolve().parent / "candidates"',
             'OUT = Path(__file__).resolve().parent / "generated"')
replace_once('MODEL = ROOT / "tools/kokoro/model.onnx"\nVOICES = ROOT / "tools/kokoro/voices.bin"',
             'CACHE = Path("C:/Users/Peter/Documents/mermaid-roshan-reef/tools/kokoro")\n'
             'MODEL = CACHE / "model.onnx"\nVOICES = CACHE / "voices.bin"')
replace_once('''CUES = (
    ("guide_seek_tap_wiggly_tree", "Tap the wiggly tree!"),
    ("guide_dolls_catch_three", "Move left and right. Catch three sleepy dolls!"),
)''', '''CUES = (
    ("guide_puff_cold_intro", "Grand Puff has a cold. Let's help!"),
    ("guide_puff_clean", "Tap his star to clean!"),
    ("guide_puff_relief", "Ahh! That feels better!"),
    ("guide_puff_almost", "Nearly clean! One more gentle wash!"),
    ("guide_puff_healthy", "All clean! Feeling better!"),
)''')
text = text.replace('2026-10-14', '2026-10-17')
text = text.replace('Two bounded neutral Guide cues; no cloning, protected-voice mutation or paid API',
                    'Five new care-story Guide lines for the owner-directed Grand Puff rework; '
                    'neutral adult, no family imitation, protected-voice mutation or paid API')
text = text.replace('TP=-2:', 'TP=-2.8:').replace('"true_peak_target_dbtp": -2,',
                                               '"true_peak_target_dbtp": -2.8,')
replace_once('        measured, first_command = measure(derived)', '''        trimmed = derived
        derived = OUT / "derived" / (key + "_dc_compressed.wav")
        conditioning = [FFMPEG, "-hide_banner", "-loglevel", "error", "-n", "-i", str(trimmed),
                        "-af", "highpass=f=40,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80",
                        "-c:a", "pcm_f32le", str(derived)]
        run(conditioning)
        record["conditioning"] = {"command": conditioning,
            "input_sha256": digest(trimmed), "output_sha256": digest(derived),
            "purpose": "Remove DC and restrain peaks before lossless loudness mastering"}
        measured, first_command = measure(derived)''')
target = HERE / 'generate_care_guides.py'
if target.exists():
    raise RuntimeError('No-overwrite guard: prepared producer already exists')
target.write_text(text, encoding='utf-8')
print(target)

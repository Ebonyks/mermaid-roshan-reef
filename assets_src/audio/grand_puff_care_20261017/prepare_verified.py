"""Reuse all five native takes; add measured crest headroom to the final cue."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
text = (HERE / 'generate_care_guides_delivery.py').read_text(encoding='utf-8')
changes = {
    'OUT = Path(__file__).resolve().parent / "generated_delivery"':
        'OUT = Path(__file__).resolve().parent / "generated_verified"',
    'prior_path = OUT.parent / "generated_peak_safe/generation_manifest.json"':
        'prior_path = OUT.parent / "generated_delivery/generation_manifest.json"',
    'original = OUT.parent / "generated_peak_safe" / known_native[key]["path"]':
        'original = OUT.parent / "generated_delivery" / known_native[key]["path"]',
    '"path": "generated_peak_safe/generation_manifest.json",':
        '"path": "generated_delivery/generation_manifest.json",',
    '"highpass=f=40,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80",':
        '("acompressor=threshold=0.08:ratio=4:attack=8:release=80:makeup=1,highpass=f=40"\n'
        '                         if key == "guide_puff_healthy" else\n'
        '                         "highpass=f=40,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80"),',
}
for old,new in changes.items():
    if text.count(old) != 1:
        raise RuntimeError('Producer anchor changed: ' + old)
    text = text.replace(old,new,1)
target = HERE / 'generate_care_guides_verified.py'
if target.exists():
    raise RuntimeError('Verified producer already exists')
target.write_text(text,encoding='utf-8')
print(target)

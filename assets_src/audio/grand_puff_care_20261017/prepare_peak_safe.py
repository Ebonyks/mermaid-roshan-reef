"""Keep all native takes; constrain codec gain by both loudness and peak margin."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
text = (HERE / 'generate_care_guides_final.py').read_text(encoding='utf-8')
changes = {
    'OUT = Path(__file__).resolve().parent / "generated_final"':
        'OUT = Path(__file__).resolve().parent / "generated_peak_safe"',
    'prior_path = OUT.parent / "generated/generation_manifest.json"':
        'prior_path = OUT.parent / "generated_final/generation_manifest.json"',
    '"synthesis_calls": prior["synthesis_calls"],':
        '"synthesis_calls": prior["synthesis_calls"] + prior["previous_run"]["synthesis_calls"],',
    'original = OUT.parent / "generated" / known_native[key]["path"]':
        'original = OUT.parent / "generated_final" / known_native[key]["path"]',
    '"path": "generated/generation_manifest.json",':
        '"path": "generated_final/generation_manifest.json",',
    'correction = -16.0 - float(post["input_i"])':
        'correction = min(-16.0 - float(post["input_i"]), -2.0 - float(post["input_tp"]))',
}
for old,new in changes.items():
    if text.count(old) != 1:
        raise RuntimeError('Producer anchor changed: ' + old)
    text = text.replace(old,new,1)
target = HERE / 'generate_care_guides_peak_safe.py'
if target.exists():
    raise RuntimeError('Peak-safe producer already exists')
target.write_text(text,encoding='utf-8')
print(target)

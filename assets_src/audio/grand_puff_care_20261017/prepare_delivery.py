"""Use measured per-line codec headroom; retain native takes and strict floors."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
text = (HERE / 'generate_care_guides_peak_safe.py').read_text(encoding='utf-8')
changes = {
    'OUT = Path(__file__).resolve().parent / "generated_peak_safe"':
        'OUT = Path(__file__).resolve().parent / "generated_delivery"',
    'prior_path = OUT.parent / "generated_final/generation_manifest.json"':
        'prior_path = OUT.parent / "generated_peak_safe/generation_manifest.json"',
    'original = OUT.parent / "generated_final" / known_native[key]["path"]':
        'original = OUT.parent / "generated_peak_safe" / known_native[key]["path"]',
    '"path": "generated_final/generation_manifest.json",':
        '"path": "generated_peak_safe/generation_manifest.json",',
    'correction = min(-16.0 - float(post["input_i"]), -2.0 - float(post["input_tp"]))':
        'master_target = -16.8 if key == "guide_puff_relief" else -16.4\n'
        '        correction = min(master_target - float(post["input_i"]), -2.0 - float(post["input_tp"]))',
}
for old,new in changes.items():
    if text.count(old) != 1:
        raise RuntimeError('Producer anchor changed: ' + old)
    text = text.replace(old,new,1)
target = HERE / 'generate_care_guides_delivery.py'
if target.exists():
    raise RuntimeError('Delivery producer already exists')
target.write_text(text,encoding='utf-8')
print(target)

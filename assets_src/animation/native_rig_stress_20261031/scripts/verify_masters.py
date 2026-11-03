"""Compare reopened Aseprite exports against every authoritative Godot RGBA frame."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
report={'aseprite_version':'1.3.18.4-x64','timing':'33,33,34 ms repeating; integer-ms review-master quantization, not runtime retiming','clips':{}}
for clip in ['arm_bend','blink','tail_bend']:
    frames=sorted((ROOT/'evidence/render_v10'/clip).glob('*.png'))
    differences=[]
    for source in frames:
        target=ROOT/'masters/reopened'/clip/source.name
        before=Image.open(source).convert('RGBA').tobytes()
        after=Image.open(target).convert('RGBA').tobytes()
        if before!=after:differences.append(source.name)
    master=ROOT/'masters'/f'{clip}.aseprite'
    report['clips'][clip]={'frames':len(frames),'mismatched_frames':differences,'master_sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'exact_rgba_roundtrip':not differences}
report['pass']=all(v['exact_rgba_roundtrip'] for v in report['clips'].values())
(ROOT/'evidence/aseprite_roundtrip.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['pass'] else 1)

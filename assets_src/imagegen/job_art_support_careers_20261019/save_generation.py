from pathlib import Path
import hashlib,json,re,shutil,sys
from PIL import Image
root=Path(__file__).resolve().parents[3]
src=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=src/'prompts.json'
rows=json.loads(manifest.read_text()) if manifest.exists() else []
batch=json.loads((src/sys.argv[1]).read_text())
for s in batch:
    assert not any(x['id']==s['id'] for x in rows),s['id']
    original=Path(s['output_hint'].split(' as ',1)[1].split(' by default.',1)[0])
    assert original.resolve().is_relative_to(Path('C:/Users/Peter/.codex/generated_images').resolve())
    target=src/(s['id']+'_native.png');assert not target.exists()
    shutil.copyfile(original,target)
    assert sha(original)==sha(target)
    image=Image.open(target)
    s.update(native_path=target.relative_to(root).as_posix(),native_sha256=sha(target),dimensions=list(image.size),
        inputs=[{'path':Path(p).relative_to(root).as_posix(),'sha256':sha(Path(p)),
            'role':'position_only' if '/tmp/' in p.replace(chr(92),'/') else 'appearance/identity reference; protected originals unchanged',
            'used_as_delivery_pixels':False if '/tmp/' in p.replace(chr(92),'/') else 'Source-bound ImageGen appearance input; output separately reviewed'} for p in s['refs']],
        provider='Available builtin ImageGen; model revision/seed/paid charges unexposed; user approved available tool',
        prompt_sha256=hashlib.sha256(s['prompt'].encode('utf-8')).hexdigest(),
        disposition='CANDIDATE_PENDING_SOURCE_CONTEXT_4.5_TECHNICAL_MOTION_REVIEW')
    rows.append(s)
manifest.write_text(json.dumps(rows,indent=2)+'\n')
p=root/'ASSET_LICENSES.md';text=p.read_text('utf-8')
for row in rows:
    path=row['native_path']
    if '| `'+path+'` |' not in text:
        text+='\n| `'+path+'` | Available builtin ImageGen2026-10-19; revision unexposed | Project original; OpenAI output terms and original reference rights retained | https://openai.com/policies/terms-of-use/ | Native unchanged SHA256 '+row['native_sha256']+'; prompt/input/provider-output and attempt records in adjacent prompts.json; no owner/device acceptance. |'
p.write_text(text+'\n' if not text.endswith('\n') else text,encoding='utf-8')
p=root/'design/audit_impacts/job-art-support-careers-20261019.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+['ASSET_LICENSES.md']+[p.relative_to(root).as_posix() for p in src.rglob('*') if p.is_file()]));p.write_text(json.dumps(d,indent=2)+'\n')
print('Preserved',len(batch),'native outputs, prompts, hashes and licenses;',len(rows),'total calls recorded')

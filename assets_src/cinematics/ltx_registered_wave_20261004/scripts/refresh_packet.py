"""Refresh only this source packet's license rows, payload manifest and impact coverage."""
from pathlib import Path
import json,hashlib,subprocess
p=Path(__file__).resolve().parents[1];r=p.parents[2]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
license_path=r/'ASSET_LICENSES.md';text=license_path.read_text(encoding='utf-8');marker='\n## Registered LTX wave sample — 2026-10-04\n'
if marker in text:text=text.split(marker)[0]
rows=[]
for f in sorted(p.rglob('*')):
 if f.is_file() and f.suffix.lower() in ['.png','.mp4','.webm','.gif','.aseprite']:
  rel=f.relative_to(r).as_posix()
  mod='Source-only registered/isolation/composite/preview derivative; native outputs and exact modifications/hashes in packet manifest and receipts. Original source unchanged; not accepted runtime art.'
  if 'previous_unregistered' in rel:mod='Byte-identical copy of prior published LTX guided reference take; no modification.'
  rows.append(f'| `{rel}` | Project-owned Roshan gesture artwork and/or LTX-Video 2B generated derivative; source provenance inherited, model terms retained in packet | https://github.com/Ebonyks/mermaid-roshan-reef/blob/f07c1a4820fb5222289802ad712db677b56400bc/assets/characters/roshan_25d/roshan_gesture_a.png | {mod} |')
text+=marker+'\n| Asset | Source/license | Source URL | Modifications |\n|---|---|---|---|\n'+'\n'.join(rows)+'\n';license_path.write_text(text,encoding='utf-8')
payload=[]
for f in sorted(p.rglob('*')):
 if f.is_file() and f.name not in ['manifest.json','remote_verification.json']:
  item={'path':f.relative_to(p).as_posix(),'sha256':sha(f),'bytes':f.stat().st_size}
  if f.suffix.lower()=='.png':
   from PIL import Image
   with Image.open(f) as im:item['dimensions']=list(im.size);item['mode']=im.mode
  item['role']='native_generated_frame' if '/native_frames/' in item['path'] else 'source_or_derivative_reference_study'
  payload.append(item)
manifest={'schema':'source-study-payload-v1','status':'REFERENCE_ONLY','baseline':'f07c1a4820fb5222289802ad712db677b56400bc','source':{'path':'assets/characters/roshan_25d/roshan_gesture_a.png','sha256':sha(r/'assets/characters/roshan_25d/roshan_gesture_a.png')},'payload':payload,'payload_sha256':hashlib.sha256('\n'.join(x['path']+' '+x['sha256'] for x in payload).encode()).hexdigest(),'acceptance':'No production/runtime/device/child/owner acceptance; see README/review receipts.'}
(p/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
impact_path=r/'design/audit_impacts/ltx-registered-wave-20261004.json';impact=json.loads(impact_path.read_text())
impact['files']=[f.relative_to(r).as_posix() for f in sorted(p.rglob('*')) if f.is_file()]+['ASSET_LICENSES.md','audit/animation/README.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','design/animation/ANIMATION_PRODUCTION_PROTOCOL.md']
impact_path.write_text(json.dumps(impact,indent=2)+'\n')
print('REFRESHED',len(payload),'payload files',len(rows),'asset rows')

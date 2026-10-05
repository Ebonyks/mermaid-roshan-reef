"""Hash exact source-study payload and add each new derivative's license row."""
import hashlib,json,struct,sys
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from prepare import P,ROOT,OLD,digest
prefix=P.relative_to(ROOT).as_posix();old_prefix=OLD.relative_to(ROOT).as_posix()
plan=json.loads((P/'registration_plan.json').read_text());payload=[];licenses=[]
for f in sorted(P.rglob('*')):
    if not f.is_file() or '__pycache__' in f.parts or f.name in {'manifest.json','remote_verification.json','receipt_publication.json'}:continue
    rel=f.relative_to(P).as_posix();parents=[];role='recipe_or_measured_evidence';mod='Source-only recipe or measured evidence, no runtime acceptance.'
    if f.parent.name=='frames':
        i=int(f.stem);parents=[plan['frames'][i]['source'],prefix+'/registration_plan.json']
        role='registered_complete_native_frame';mod='Aseprite single continuous uniform affine from same native frame; anatomy defects retained; constant24px stage offset.'
    elif f.name in {'registered_review.aseprite','registered_review.mp4'}:
        parents=[prefix+f'/frames/{i:04d}.png' for i in range(41)];role='editable_review_master' if f.suffix=='.aseprite' else 'encoded_review'
        mod='Complete41-frame timeline at24fps; PNG pixels retained in Aseprite master; H264 CRF15 yuv420p preview.'
    elif f.name=='raw_v1_v2_comparison.mp4':
        parents=[row['source'] for row in plan['frames']]+[old_prefix+f'/scale_continuity/decoded_filtered/{i:04d}.png' for i in range(41)]+[prefix+f'/frames/{i:04d}.png' for i in range(41)]
        role='same_frame_comparison';mod='Aseprite1:1 three-column raw/v1/v2 native frames then H264 CRF15 yuv420p encoding; no temporal replacement.'
    elif f.name=='registration_plan.json':
        parents=[old_prefix+'/scale_continuity/decoded_registration_plan.json']+[row['source'] for row in plan['frames']]
    elif f.name=='prepare.py':parents=[old_prefix+'/scripts/measure_scale_landmarks.py']
    row={'path':rel,'bytes':f.stat().st_size,'sha256':digest(f),'role':role,'modification_status':mod,
         'source_paths':parents,'source_sha256':{x:digest(ROOT/x) for x in parents},
         'license_provenance':'Project-owned Roshan derivatives and source study. Generated source footage under LTX-2.x community model terms; no weights redistributed.'}
    if f.suffix=='.png':
        with Image.open(f) as im:row.update(dimensions=list(im.size),mode=im.mode)
    elif f.suffix=='.aseprite':
        header=f.read_bytes()[:14];row.update(dimensions=list(struct.unpack_from('<HH',header,8)),frames=struct.unpack_from('<H',header,6)[0])
    elif f.suffix=='.mp4':row.update(dimensions=[1728 if f.name.startswith('raw_') else 576,832],frames=41,fps='24/1')
    if f.suffix in {'.png','.mp4','.aseprite'}:
        licenses.append('| `'+prefix+'/'+rel+'` | '+row['license_provenance']+' | https://github.com/Ebonyks/mermaid-roshan-reef/tree/c51075fff13cfd8f4795b5ef7da232fc7462e7f4/'+old_prefix+' | '+mod+' Reference only. |')
    payload.append(row)
manifest={'schema':'source-study-payload-v1','status':'REJECTED_REFERENCE_ONLY','baseline':'476ceda18ab83139696e4f8f705dbdc486a30250',
          'payload':payload,'payload_sha256':hashlib.sha256('\n'.join(x['path']+' '+x['sha256'] for x in payload).encode()).hexdigest(),
          'new_model_jobs':0,'new_imagegen_calls':0,'previous_model_job_cap':5,'previous_named_key_cap':1,
          'model_weights_redistributed':False,'accepted':False,'previous_source_manifest':old_prefix+'/manifest.json'}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
marker='\n## LTX-2.5 continuous scale filter v2 — 2026-10-04\n';path=ROOT/'ASSET_LICENSES.md';text=path.read_text(encoding='utf-8')
if marker in text:
    start=text.index(marker);end=text.find('\n## ',start+len(marker));text=text[:start]+(text[end:] if end>=0 else '')
text+=marker+'\n| Asset | Source/license | Source URL | Modifications |\n|---|---|---|---|\n'+'\n'.join(licenses)+'\n';path.write_text(text,encoding='utf-8',newline='')
path=ROOT/'design/audit_impacts/ltx25-scale-filter-v2-20261004.json';impact=json.loads(path.read_text())
impact['files']=sorted(set(impact['files']+[f.relative_to(ROOT).as_posix() for f in P.rglob('*') if f.is_file() and '__pycache__' not in f.parts]))
path.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8')
assert all(x['bytes']<104857600 for x in payload),'GitHub file hard limit'
print('PAYLOAD',len(payload),'LICENSE_ROWS',len(licenses),'BYTES',sum(x['bytes'] for x in payload),'MAX_FILE',max(x['bytes'] for x in payload))

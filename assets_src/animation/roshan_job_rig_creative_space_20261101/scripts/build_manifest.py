"""Hash the frozen review payload. Manifest/transport receipt are outside its hash set."""
from pathlib import Path
import hashlib,json
from PIL import Image

P=Path(__file__).resolve().parents[1];R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
seed=json.loads((P/'fixtures/frozen_inputs_v8.json').read_text(encoding='utf8'))['files']
seed_revision='b700b846d1d2f4b1843279f268e2bb12e4b1f4ec'
known={v:(k,seed_revision) for k,v in seed.items()}
known[sha(P/'fixtures/frozen_inputs_v8.json')]=('assets_src/animation/native_rig_costumes_20261031/replacement_v6/evidence/frozen_inputs_v8.json',seed_revision)
inventory=json.loads((P/'source_inventory.json').read_text(encoding='utf8'))
known.update({x['sha256']:(x['path'],inventory['baseline']) for x in inventory['sources']})
files=[]
for f in sorted(P.rglob('*')):
    rel=f.relative_to(P)
    if not f.is_file() or any(x in rel.parts for x in ['raw','.godot','__pycache__']) or f.name.endswith(('.uid','.import','.ffconcat')) or rel.as_posix()=='manifest.json':continue
    digest=sha(f);part=rel.parts[0];origin=known.get(digest);source=origin[0] if origin else None
    if part=='art' and not source:
        if f.stem.startswith(('painter_','astronaut_')):source='native/'+f.stem.split('_')[0]+'_fit_take01.png'
        elif f.stem=='neck_patch':source='native/neck_source.png'
        elif f.stem=='brush_grip':source='native/brush_grip_source.png'
        elif f.stem=='brush':source='native/brush_source.png'
    if part=='masters':source='art/'+f.stem+'.png'
    role={'art':'source/derivative RGBA; candidate only','references':'exact existing appearance reference; source acceptance scope only','fixtures':'frozen seed fixture','native':'preserved native appearance source','masters':'editable RGBA Aseprite master','review':'diagnostic review; never generation pixels','evidence':'measurement/history; acceptance scope retained','godot':'isolated executable Canvas prototype','scripts':'reproduction/verification source','jobs':'bounded action derivation record','contract':'owner-local contract freeze; not owner-published'}.get(part,'source packet metadata/instructions')
    item=dict(path=f.relative_to(R).as_posix(),bytes=f.stat().st_size,sha256=digest,role=role,source_path=source or rel.as_posix(),source_note='Exact reused bytes' if digest in known else 'Authored/derived in this packet; provenance.json, corrective_attempts.json, registration.json and source code record derivation. Evidence raw paths are ignored reproducible build products.',license_provenance='Project-owned code/art or existing project-generated art; source scope and ASSET_LICENSES.md apply; no downstream artistic acceptance',modification_status='UNCHANGED_SOURCE_COPY' if digest in known else 'DECLARED_DERIVATIVE_OR_NEW_RECORD')
    item['source_revision']=origin[1] if origin else 'THIS_PAYLOAD; owner-local contract limitation retained where applicable'
    if f.suffix.lower() in ['.png','.jpg','.jpeg']:
        with Image.open(f) as im:item['dimensions']=list(im.size)
    files.append(item)
files.sort(key=lambda x:x['path'])
payload=''.join(x['path']+'\0'+x['sha256']+'\n' for x in files).encode('utf8')
d=dict(schema_version=1,id='roshan_job_rig_creative_space_20261101',classification='REVIEW_CANDIDATE_NUMERICALLY_REJECTED',production_integration=False,source_baseline=inventory['baseline'],verification_base='93166ab1828ab9857227d038f8833b92dfb2f9f1',recipient_access='Public GitHub anonymous HTTPS; exact remote receipt required',payload_sha256=hashlib.sha256(payload).hexdigest(),payload_algorithm='UTF-8 sorted repository path + NUL + lowercase file SHA-256 + LF',exclusions=['manifest.json (self-reference)','separate audit/receipts transport verification (binds exact payload revision)','evidence/raw, .godot, __pycache__, generated .uid/.import and local ffconcat build playlists'],readiness=dict(ARCHIVE_COMPLETE='Established only by a later anonymous remote receipt for its exact payload commit',GENERATION_READY=False,DELIVERY_ACCEPTED=False),files=files)
(P/'manifest.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf8')
print('MANIFEST',len(files),'FILES',sum(x['bytes'] for x in files),'BYTES',d['payload_sha256'])

"""Seal R16 candidate and all immutable inherited R15 dependency bytes."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;V=H/'r15_geode_cue_reuse';OLD='1910dc272025ca53b049f559245eb0c4ee8675fb';PAYLOAD='f83c1ddf43eb8b0a81bf661fe85081071cccb88a'
def sha(b):return hashlib.sha256(b).hexdigest()
rows={}
def add(path,rev=None,role='R16 current candidate/evidence'):
 b=(R/path).read_bytes() if rev is None else subprocess.check_output(['git','show',rev+':'+path],cwd=R,stderr=subprocess.PIPE);rows[(rev,path)]={'path':path,'revision':rev,'bytes':len(b),'sha256':sha(b),'role':role}
for x in json.loads((V/'MANIFEST.json').read_text())['files']:
 rev=x['revision'] or PAYLOAD;rows[(rev,x['path'])]=dict(x,revision=rev,role='Inherited exact R15 dependency; preserves prior scope/history')
for base in [P,R/'assets_src/flat_vector_pointer_20261013']:
 for f in base.rglob('*'):
  if f.is_file() and f.name not in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json'] and '__pycache__' not in f.parts:add(f.relative_to(R).as_posix())
for path in ['.gitattributes',(H/'CURRENT.json').relative_to(R).as_posix(),(H/'README.md').relative_to(R).as_posix(),'audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','ASSET_LICENSES.md','design/audit_impacts/flat-vector-pointer-candidate-20261013.json']:add(path)
for x in json.loads((P/'SOURCES.json').read_text())['sources']:add(x['path'],x['revision'],x['role'])
for path in ['scripts/opera_geology_surface.gd','scripts/opera_gesture_surface.gd','scripts/opera_career_world_2d.gd','scripts/opera_act.gd','scripts/opera_house.gd','scripts/ci.sh','design/templates/ANIMATION_JOB_CARD_V1.md','design/animation/ANIMATION_PRODUCTION_PROTOCOL.md']:
 add(path,OLD,'Exact unchanged source/caller or whole-unit job-card authority')
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','REVIEW.json','SOURCE_PARITY.json','CURRENT_PARTIAL_CONTEXT_UNION.json','GATES.json']:
 add((V/name).relative_to(R).as_posix(),OLD,'Immutable R15 receipt and current canonical history')
rows=sorted(rows.values(),key=lambda x:(x['revision'] or 'CURRENT',x['path']))
d={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261013-R16','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join((x['revision'] or 'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'excluded_post_publication_record':'REMOTE_VERIFICATION.json and RECEIPT_GATES.json','candidate_sample_count':1,'accepted_removed':0,'mission_complete':False}
(P/'MANIFEST.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');print('R16_MANIFEST',len(rows),d['required_bytes'],d['payload_sha256'])

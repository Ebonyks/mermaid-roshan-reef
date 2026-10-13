"""Seal additive R10 technical sample/current-context and immutable dependencies."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent
OLD='0c2732204bec7f882db26d835e2ce32ee12c7471'
def sha(b):return hashlib.sha256(b).hexdigest()
rows=[]
extras=[R/'.gitattributes',H/'CURRENT.json',H/'README.md',R/'ASSET_LICENSES.md',R/'audit/MASTER_AUDIT_2026-08-09.md',R/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md',R/'design/05_DOC_LEDGER.md',R/'design/audit_impacts/flat-vector-geode-marker-fit-20261013.json']
local=[x for base in [P] for x in base.rglob('*') if x.is_file() and x.name not in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json'] and '__pycache__' not in x.parts]+extras
for x in sorted(local):
 b=x.read_bytes();rows.append({'path':x.relative_to(R).as_posix(),'revision':None,'bytes':len(b),'sha256':sha(b),'role':'R10 source-reuse/preview/provenance/current evidence delta'})
for x in json.loads((P/'SOURCES.json').read_text(encoding='utf-8'))['sources']:
 rows.append({'path':x['path'],'revision':x['immutable_revision'],'bytes':x['bytes'],'sha256':x['sha256'],'role':'Inherited exact production/appearance/source/provenance dependency'})
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','REVIEW.json','DERIVATIVES.json','REUSE_JOB.json','FIT_MEASUREMENTS.json','SOURCE_PARITY.json']:
 path=(H/'r9_geode_reuse'/name).relative_to(R).as_posix();b=subprocess.check_output(['git','show',OLD+':'+path],cwd=R,stderr=subprocess.PIPE);rows.append({'path':path,'revision':OLD,'bytes':len(b),'sha256':sha(b),'role':'Immutable R9 context/registry/count/history/public verification; inherited earlier dependency closure stays bound through exact R9/R8/R7/R6 manifests and receipts'})
for path in ['AGENTS.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','design/02_ART_DIRECTION.md','ART_STYLE_GUIDE.md','tools/sprite_pipeline_bridge.lua']:
 b=subprocess.check_output(['git','show',OLD+':'+path],cwd=R,stderr=subprocess.PIPE);rows.append({'path':path,'revision':OLD,'bytes':len(b),'sha256':sha(b),'role':'Binding authority/scoped primary local technical bridge'})
rows.sort(key=lambda x:(x['revision'] or 'CURRENT',x['path']))
data={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261013-R10','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join((x['revision'] or 'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'inherited_context_limit':'Reverify every declared exact delta/source/authority/history dependency. Earlier unchanged context remains bound through previously verified immutable manifests/receipts; no new whole-game or acceptance closure.','excluded_post_publication_record':'REMOTE_VERIFICATION.json and RECEIPT_GATES.json','accepted_removed':0,'mission_complete':False}
(P/'MANIFEST.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n');print('R10_MANIFEST',len(rows),data['required_bytes'],data['payload_sha256'])

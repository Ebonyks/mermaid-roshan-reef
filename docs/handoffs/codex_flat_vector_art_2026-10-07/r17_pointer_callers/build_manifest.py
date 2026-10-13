"""Seal additive R17 source audit plus exact inherited R16 dependencies."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;V=H/'r16_pointer_candidate';OLD='182f2e522a330b89bf7329b26516583160f343e0';PAYLOAD='a75dff44fdb594323b09069e9e53ccfeb42bc653'
def sha(b):return hashlib.sha256(b).hexdigest()
rows={}
def add(path,rev=None,role='Current R17 source-only evidence'):
 b=(R/path).read_bytes() if rev is None else subprocess.check_output(['git','show',rev+':'+path],cwd=R,stderr=subprocess.PIPE);rows[(rev,path)]={'path':path,'revision':rev,'bytes':len(b),'sha256':sha(b),'role':role}
for x in json.loads((V/'MANIFEST.json').read_text())['files']:
 rev=x['revision'] or PAYLOAD;rows[(rev,x['path'])]=dict(x,revision=rev,role='Inherited immutable R16 dependency; acceptance scope unchanged')
for f in P.rglob('*'):
 if f.is_file() and f.name not in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','receipt_gates.log'] and '__pycache__' not in f.parts:add(f.relative_to(R).as_posix())
for path in ['.gitattributes',(H/'CURRENT.json').relative_to(R).as_posix(),(H/'README.md').relative_to(R).as_posix(),'audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','design/audit_impacts/flat-vector-pointer-callers-20261013.json']:add(path)
for x in json.loads((P/'SOURCES.json').read_text())['sources']:add(x['path'],x['revision'],x['role'])
for x in json.loads((P/'SCRIPT_CENSUS.json').read_text())['files']:add(x['path'],x['revision'],'Exact complete declared-script scan input; not proof of live reachability')
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','REVIEW.json','SOURCES.json','GATES.json','FULL_VALIDATION.json']:
 add((V/name).relative_to(R).as_posix(),OLD,'Immutable R16 receipt/canonical evidence and unchanged82-probe runtime baseline')
rows=sorted(rows.values(),key=lambda x:(x['revision'] or 'CURRENT',x['path']))
d={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261013-R17','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join((x['revision'] or 'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'excluded_post_publication_record':'REMOTE_VERIFICATION.json,RECEIPT_GATES.json and receipt_gates.log; exact final receipt bytes verified separately','candidate_sample_count':1,'accepted_removed':0,'mission_complete':False}
(P/'MANIFEST.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');print('R17_MANIFEST',len(rows),d['required_bytes'],d['payload_sha256'])

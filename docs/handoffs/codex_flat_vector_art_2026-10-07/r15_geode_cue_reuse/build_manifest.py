"""Seal R15 plus every immutable inherited R14 payload dependency."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;OLD='42ef9083c07d15e0436ad981d23a35c6309871c8';V=H/'r14_geode_lifecycle';PAYLOAD='53c511b0ec5b0fbf5a697e6e64d216540060fc43'
def sha(b):return hashlib.sha256(b).hexdigest()
rows={}
def add(path,rev=None,role='R15 current evidence'):
 b=(R/path).read_bytes() if rev is None else subprocess.check_output(['git','show',rev+':'+path],cwd=R,stderr=subprocess.PIPE);rows[(rev,path)]={'path':path,'revision':rev,'bytes':len(b),'sha256':sha(b),'role':role}
for x in json.loads((V/'MANIFEST.json').read_text())['files']:
 rev=x['revision'] or PAYLOAD;rows[(rev,x['path'])]=dict(x,revision=rev,role='Inherited exact R14 payload dependency; retains original scope')
for f in P.rglob('*'):
 if f.is_file() and f.name not in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json'] and '__pycache__' not in f.parts:add(f.relative_to(R).as_posix())
for path in ['.gitattributes',(H/'CURRENT.json').relative_to(R).as_posix(),(H/'README.md').relative_to(R).as_posix(),'audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','ASSET_LICENSES.md','design/audit_impacts/flat-vector-geode-cue-reuse-20261013.json']:add(path)
for x in json.loads((P/'SOURCES.json').read_text())['sources']:add(x['path'],x['revision'],x['role'])
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','REVIEW.json','SOURCE_PARITY.json','GATES.json','FULL_VALIDATION.json']:
 add((V/name).relative_to(R).as_posix(),OLD,'Current immutable R14 receipt/canonical evidence; unchanged production validation inherited')
for f in ['native/1280x720/prepare/geode_closed_ready.png','native/1280x720/resume/geode_disk_resume060_task.png']:add((V/f).relative_to(R).as_posix(),OLD,'Original current context inspected before cue trial')
rows=sorted(rows.values(),key=lambda x:(x['revision'] or 'CURRENT',x['path']))
d={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261013-R15','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join((x['revision'] or 'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'excluded_post_publication_record':'REMOTE_VERIFICATION.json and RECEIPT_GATES.json','accepted_removed':0,'mission_complete':False}
(P/'MANIFEST.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');print('R15_MANIFEST',len(rows),d['required_bytes'],d['payload_sha256'])

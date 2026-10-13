"""Seal additive R18 source audit plus exact inherited R16 dependencies."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;V=H/'r17_pointer_callers';OLD='90d19ceddb20d624f134a3429dfa2afd25e5faaa';PAYLOAD='0606fbc0f94d3d60fa332dc430f44af70c7a812a'
def sha(b):return hashlib.sha256(b).hexdigest()
rows={}
def add(path,rev=None,role='Current R18 source-only evidence'):
 b=(R/path).read_bytes() if rev is None else subprocess.check_output(['git','show',rev+':'+path],cwd=R,stderr=subprocess.PIPE);rows[(rev,path)]={'path':path,'revision':rev,'bytes':len(b),'sha256':sha(b),'role':role}
for x in json.loads((V/'MANIFEST.json').read_text())['files']:
 rev=x['revision'] or PAYLOAD;rows[(rev,x['path'])]=dict(x,revision=rev,role='Inherited immutable R17 dependency; acceptance scope unchanged')
for f in P.rglob('*'):
 if f.is_file() and f.name not in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','receipt_gates.log'] and '__pycache__' not in f.parts:add(f.relative_to(R).as_posix())
for path in ['.gitattributes',(H/'CURRENT.json').relative_to(R).as_posix(),(H/'README.md').relative_to(R).as_posix(),'audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','ASSET_LICENSES.md','design/audit_impacts/flat-vector-candy-pointer-context-20261013.json']:add(path)
for x in json.loads((P/'SOURCES.json').read_text())['sources']:add(x['path'],x['revision'],x['role'])
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','SOURCES.json','GATES.json','SOURCE_AUDIT.json','SCRIPT_CENSUS.json','SOURCE_EXCERPTS.json']:
 add((V/name).relative_to(R).as_posix(),OLD,'Immutable R17 receipt/canonical evidence; earlier82-probe runtime baseline remains inherited')
rows=sorted(rows.values(),key=lambda x:(x['revision'] or 'CURRENT',x['path']))
d={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261013-R18','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join((x['revision'] or 'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'excluded_post_publication_record':'REMOTE_VERIFICATION.json,RECEIPT_GATES.json and receipt_gates.log; exact final receipt bytes verified separately','candidate_sample_count':1,'accepted_removed':0,'mission_complete':False}
(P/'MANIFEST.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');print('R18_MANIFEST',len(rows),d['required_bytes'],d['payload_sha256'])

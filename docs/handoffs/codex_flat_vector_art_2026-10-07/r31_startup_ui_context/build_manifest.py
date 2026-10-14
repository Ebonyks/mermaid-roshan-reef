"""Seal additive bounded Startup UI context evidence and every immutable inherited dependency."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r30_startup_ambience_retirement';BASE='849a7de5fa65270d354cb7973ded63b464668988';PAYLOAD='b6606504598fc0d32736918c9a23f7af102f7eb7'
def sha(b):return hashlib.sha256(b).hexdigest()
rows={}
def add(path,revision=None,role='R31 bounded Startup UI context nonruntime diagnostic;no pixel acceptance'):
 b=(R/path).read_bytes() if revision is None else subprocess.check_output(['git','show',revision+':'+path],cwd=R,stderr=subprocess.PIPE);rows[(revision,path)]={'path':path,'revision':revision,'bytes':len(b),'sha256':sha(b),'role':role}
for row in json.loads((O/'MANIFEST.json').read_text())['files']:
 rev=row['revision'] or PAYLOAD;rows[(rev,row['path'])]=dict(row,revision=rev,role='Inherited immutable R30/prior evidence;acceptance scope unchanged')
for f in P.rglob('*'):
 if f.is_file() and f.name not in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','receipt_gates.log'] and '__pycache__' not in f.parts:add(f.relative_to(R).as_posix())
for path in ['.gitattributes','ASSET_LICENSES.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/audit_impacts/flat-vector-startup-ui-context-20261014.json',(H/'README.md').relative_to(R).as_posix(),(H/'CURRENT.json').relative_to(R).as_posix()]:add(path)
for x in json.loads((P/'SOURCES.json').read_text())['sources']:add(x['path'],x['revision'],x['role'])
for f in O.iterdir():
 if f.is_file() and f.suffix in ['.json','.log'] and f.name not in ['native_capture.log','import.log','gates.log']:add(f.relative_to(R).as_posix(),BASE,'Immutable R30 canonical/receipt/history reference at final exact head')
rows=sorted(rows.values(),key=lambda x:(x['revision'] or 'CURRENT',x['path']))
d={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261014-R31','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join((x['revision'] or 'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'excluded_post_publication_record':'REMOTE_VERIFICATION,RECEIPT_GATES,receipt_gates.log;final metadata exact bytes verified separately','new_artwork_drawings':0,'new_generation_calls':0,'accepted_removed':0,'mission_complete':False}
(P/'MANIFEST.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');print('R31_MANIFEST',len(rows),d['required_bytes'],d['payload_sha256'])

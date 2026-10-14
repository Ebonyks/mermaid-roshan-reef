"""Seal source glyph audit and exact immutable inherited dependencies."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r37_current_source_inventory';BASE='8f48a0003a8a098658a3414414bd3da3c94f29c2';OLD_PAYLOAD='efd1f89827ee1dc7d0531474b210c6d457c5a903';rows={}
def sha(b):return hashlib.sha256(b).hexdigest()
def add(path,revision=None,role='R38 glyph-source audit/canonical/document evidence;not runtime/art acceptance'):
 b=(R/path).read_bytes() if revision is None else subprocess.check_output(['git','show',revision+':'+path],cwd=R,stderr=subprocess.PIPE);rows[(revision,path)]={'path':path,'revision':revision,'bytes':len(b),'sha256':sha(b),'role':role}
for x in json.loads((O/'MANIFEST.json').read_text(encoding='utf-8'))['files']:
 rev=x['revision'] or OLD_PAYLOAD;rows[(rev,x['path'])]=dict(x,revision=rev,role='Inherited immutable R37/prior evidence;declared acceptance unchanged')
for f in P.iterdir():
 if f.is_file() and f.name not in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','receipt_gates.log','FINAL_BYTE_RECEIPT.json']:add(f.relative_to(R).as_posix())
for path in ['audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/audit_impacts/flat-vector-glyph-reconciliation-20261014.json',(H/'README.md').relative_to(R).as_posix(),(H/'CURRENT.json').relative_to(R).as_posix()]:add(path)
for path in ['.gitattributes','ASSET_LICENSES.md']:add(path,BASE,'Unchanged immutable authority/license baseline;no current modification')
for x in json.loads((P/'GLYPH_SOURCE_FILES.json').read_text(encoding='utf-8'))['inputs']:rows[(x['revision'],x['path'])]={'path':x['path'],'revision':x['revision'],'bytes':x['bytes'],'sha256':x['sha256'],'role':'Exact historical/current full glyph-source input; source glyph binding only,no visibility/acceptance'}
historical_o_paths=set(subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--',O.relative_to(R).as_posix()],cwd=R,text=True).splitlines())
for f in O.iterdir():
 if f.is_file() and f.relative_to(R).as_posix() in historical_o_paths and f.suffix in ['.json','.log'] and f.name not in ['gates.log','receipt_gates.log']:add(f.relative_to(R).as_posix(),BASE,'Immutable R37 canonical/receipt/source history at final exacthead')
for x in json.loads((P/'CONTEXT_PREREQUISITE.json').read_text(encoding='utf-8'))['checks']:add(x['path'],x['revision'],'Current anonymous glyph/source/canonical prerequisite beforeimplementation')
ret=json.loads((P/'RETAINED_SOURCE_RETIREMENT.json').read_text(encoding='utf-8'))['records'][0]
for key in ['before_revision','retirement_payload_revision']:add(ret['path'],ret[key],'Exact already-published R31/R32 source retirement evidence;notnewacceptedremoval')
# Current authored R37 format aliases/parts/readers are part of this material revision.
changed=set(subprocess.check_output(['git','diff','--name-only',BASE],cwd=R,text=True,stderr=subprocess.PIPE).splitlines()+subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R,text=True).splitlines())
for path in sorted(changed):
 if path.startswith(P.relative_to(R).as_posix()+'/') and Path(path).name in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','receipt_gates.log','FINAL_BYTE_RECEIPT.json']:continue
 if path.startswith((P/'REMOTE_VERIFICATION.fragment').relative_to(R).as_posix()):continue
 add(path,role='Current R38 evidence/canonical/document andR37exact-logical-byte format repair;notartacceptance')
rows=sorted(rows.values(),key=lambda x:(x['revision'] or 'CURRENT',x['path']));d={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261014-R38','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join((x['revision'] or 'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'excluded_post_publication_record':'REMOTE_VERIFICATION,RECEIPT_GATES,receipt_gates.log,FINAL_BYTE_RECEIPT;finalmetadata exact bytes verified separately','new_artwork_drawings':0,'new_generation_calls':0,'new_source_retirements':0,'accepted_removed':0,'mission_complete':False};(P/'MANIFEST.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');print('R38_MANIFEST',len(rows),d['required_bytes'],d['payload_sha256'])

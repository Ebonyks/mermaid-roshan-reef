"""Seal source audit and immutable inherited dependencies; metadata receipts follow publication."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r36_menu_ornament_retirement';BASE='01f670d7ab4933fe2c2e6605bbca4ef2105f200f';OLD_PAYLOAD='5c03eda2735887995322b9f603dba0b135038622';rows={}
def sha(b):return hashlib.sha256(b).hexdigest()
def add(path,revision=None,role='R37 source-only audit/canonical/document evidence;no runtime/art acceptance'):
 b=(R/path).read_bytes() if revision is None else subprocess.check_output(['git','show',revision+':'+path],cwd=R,stderr=subprocess.PIPE);rows[(revision,path)]={'path':path,'revision':revision,'bytes':len(b),'sha256':sha(b),'role':role}
for x in json.loads((O/'MANIFEST.json').read_text(encoding='utf-8'))['files']:
 rev=x['revision'] or OLD_PAYLOAD;rows[(rev,x['path'])]=dict(x,revision=rev,role='Inherited immutable R36/prior evidence;declared acceptance unchanged')
for f in P.iterdir():
 if f.is_file() and f.name not in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','receipt_gates.log','FINAL_BYTE_RECEIPT.json']:add(f.relative_to(R).as_posix())
for path in ['audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/audit_impacts/flat-vector-current-source-inventory-20261014.json',(H/'README.md').relative_to(R).as_posix(),(H/'CURRENT.json').relative_to(R).as_posix()]:add(path)
for path in ['.gitattributes','ASSET_LICENSES.md']:add(path,BASE,'Unchanged immutable authority/license baseline; no current modification')
# validate.py binds all1510 input bytes/hash/blob IDs to exactGit BASE before this seal;
# anonymous remote verification independently rechecks every declared dependency.
for x in json.loads((P/'CURRENT_SOURCE_INVENTORY.json').read_text(encoding='utf-8'))['input_files']:
 rows[(BASE,x['path'])]={'path':x['path'],'revision':BASE,'bytes':x['bytes'],'sha256':x['raw_sha256'],'role':'Current exact source/resource/UID/import-sidecar audit input;syntax only,no reachability/acceptance'}
for f in O.iterdir():
 if f.is_file() and f.suffix in ['.json','.log'] and f.name not in ['native_capture.log','import.log','gates.log']:add(f.relative_to(R).as_posix(),BASE,'Immutable R36 canonical/receipt/history reference at final exact head')
for x in json.loads((P/'CONTEXT_PREREQUISITE.json').read_text(encoding='utf-8'))['checks']:add(x['path'],x['revision'],'Current anonymous prerequisite before source scanner implementation')
rows=sorted(rows.values(),key=lambda x:(x['revision'] or 'CURRENT',x['path']));d={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261014-R37','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join((x['revision'] or 'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'excluded_post_publication_record':'REMOTE_VERIFICATION,RECEIPT_GATES,receipt_gates.log andFINAL_BYTE_RECEIPT;finalmetadata exact bytes verified separately','new_artwork_drawings':0,'new_generation_calls':0,'accepted_removed':0,'mission_complete':False};(P/'MANIFEST.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');print('R37_MANIFEST',len(rows),d['required_bytes'],d['payload_sha256'])

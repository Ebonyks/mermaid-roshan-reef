"""Seal additive R21 source audit plus exact inherited R16 dependencies."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;V=H/'r20_candy_stream_contact';OLD='29e90b7acbde7b2c0960979535960af8f0bd3df3';PAYLOAD='005d031c75159efa78bfaab859db7150bc0c3dae'
def sha(b):return hashlib.sha256(b).hexdigest()
rows={}
def add(path,rev=None,role='Current R21 nonruntime candidate-trial evidence'):
 b=(R/path).read_bytes() if rev is None else subprocess.check_output(['git','show',rev+':'+path],cwd=R,stderr=subprocess.PIPE);rows[(rev,path)]={'path':path,'revision':rev,'bytes':len(b),'sha256':sha(b),'role':role}
for x in json.loads((V/'MANIFEST.json').read_text())['files']:
 rev=x['revision'] or PAYLOAD;rows[(rev,x['path'])]=dict(x,revision=rev,role='Inherited immutable R20 dependency; acceptance scope unchanged')
for f in P.rglob('*'):
 if f.is_file() and f.name not in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','receipt_gates.log'] and '__pycache__' not in f.parts:add(f.relative_to(R).as_posix())
for asset in (R/'assets_src/flat_vector_candy_stream_20261013').iterdir():
 if asset.is_file():add(asset.relative_to(R).as_posix(),role='Whole generated nonruntime draft; localQCfailed; original/editable/provenance preserved')
for path in ['.gitattributes',(H/'CURRENT.json').relative_to(R).as_posix(),(H/'README.md').relative_to(R).as_posix(),'audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','ASSET_LICENSES.md','design/audit_impacts/flat-vector-candy-stream-material-20261013.json']:add(path)
for x in json.loads((P/'SOURCES.json').read_text())['sources']:add(x['path'],x['revision'],x['role'])
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','SOURCES.json','GATES.json','CAPTURE_INDEX.json','REVIEW.json','CURRENT_PARTIAL_CONTEXT_UNION.json','receipt_gates.log']:
 add((V/name).relative_to(R).as_posix(),OLD,'Immutable R20 receipt/canonical evidence; earlier82-probe runtime baseline remains inherited')
for initial_path in ['docs/handoffs/codex_flat_vector_art_2026-10-07/r21_candy_stream_material/REVIEW.json','assets_src/flat_vector_candy_stream_20261013/GENERATION.json']:
 add(initial_path,'408b11972571d9ad148a25deb9a255799bcf295c','Initial R21 isolated-light inference superseded by exact alpha inspection;provenance/history preserved')
rows=sorted(rows.values(),key=lambda x:(x['revision'] or 'CURRENT',x['path']))
d={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261013-R21','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join((x['revision'] or 'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'excluded_post_publication_record':'REMOTE_VERIFICATION.json,RECEIPT_GATES.json and receipt_gates.log; exact final receipt bytes verified separately','candidate_sample_count':1,'candidate_sample_count_scope':'Existing R16 hand pending;new R21 stream failed localQC and is not queued','new_generated_drafts':1,'new_local_qc_failed_drafts':1,'accepted_removed':0,'mission_complete':False}
(P/'MANIFEST.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');print('R21_MANIFEST',len(rows),d['required_bytes'],d['payload_sha256'])

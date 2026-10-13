"""Seal additive R8 delta and immutable source/history/authority dependencies."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent
OLD='c1e466a8a9e605f43b4c7a181b3d7b702d7677aa';R6='4aceae967de9da7c8f479e358a008188ba1f6304';REC6='70879a91ddcbba51ba09c7d0be81cc65f340e3b5'
def sha(b):return hashlib.sha256(b).hexdigest()
rows=[]
extra=[H/'CURRENT.json',H/'README.md',R/'ASSET_LICENSES.md',R/'audit/MASTER_AUDIT_2026-08-09.md',R/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md',R/'design/05_DOC_LEDGER.md',R/'design/audit_impacts/flat-vector-geode-context-20261013.json']
for x in sorted([x for x in P.rglob('*') if x.is_file() and x.name not in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json'] and '__pycache__' not in x.parts]+extra):
 b=x.read_bytes();rows.append({'path':x.relative_to(R).as_posix(),'revision':None,'bytes':len(b),'sha256':sha(b),'role':'R8 context delta'})
for s in json.loads((P/'SOURCES.json').read_text(encoding='utf-8'))['sources']:
 rows.append({'path':s['path'],'revision':s['immutable_revision'],'bytes':s['bytes'],'sha256':s['sha256'],'role':s['role']})
deps=[(OLD,'r7_craft_context/'+n) for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','MANIFEST.json','REMOTE_VERIFICATION.json','REVIEW.json','R6_EXACT_HEAD_CI.json','ORIGIN_DEV_RECONCILIATION.json']]+[(OLD,'r7_ci_correction/'+n) for n in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json']]+[(R6,n) for n in ['per_piece.json','scene_coverage.json','tally.json','MANIFEST.json']]+[(REC6,'REMOTE_VERIFICATION.json')]
for rev,name in deps:
 path=(H/name).relative_to(R).as_posix();b=subprocess.check_output(['git','show',rev+':'+path],cwd=R,stderr=subprocess.PIPE);rows.append({'path':path,'revision':rev,'bytes':len(b),'sha256':sha(b),'role':'Immutable prior registry/count/capture/delivery/CI context; earlier manifests/receipts retain their exact inherited dependency verification scope'})
for path in ['AGENTS.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','design/02_ART_DIRECTION.md','ART_STYLE_GUIDE.md']:
 b=subprocess.check_output(['git','show',OLD+':'+path],cwd=R,stderr=subprocess.PIPE);rows.append({'path':path,'revision':OLD,'bytes':len(b),'sha256':sha(b),'role':'Current binding authority with scoped historical precedence'})
rows.sort(key=lambda x:(x['revision'] or 'CURRENT',x['path']))
manifest={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261013-R8','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join((x['revision'] or 'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'inherited_context_limit':'This exact delta/source/history/authority closure is reverified. Unchanged inherited R7/R6 full context remains bound through previously verified immutable manifests/receipts; no new whole-game closure or acceptance.','excluded_post_publication_record':'REMOTE_VERIFICATION.json and RECEIPT_GATES.json','accepted_removed':0,'mission_complete':False}
(P/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n');print('R8_MANIFEST',len(rows),manifest['required_bytes'],manifest['payload_sha256'])

"""Seal additive R13 audit, exact source dependencies and inherited publication context."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;OLD='d26512b120500492be8e2694ac552a187f0091ca';PREV=H/'r12_geode_layered_reveal'
def sha(b):return hashlib.sha256(b).hexdigest()
rows={}
def add(path,rev=None,role='R13 audit/current metadata'):
 b=(R/path).read_bytes() if rev is None else subprocess.check_output(['git','show',rev+':'+path],cwd=R,stderr=subprocess.PIPE);rows[(rev,path)]={'path':path,'revision':rev,'bytes':len(b),'sha256':sha(b),'role':role}
for f in P.rglob('*'):
 if f.is_file() and f.name not in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json'] and '__pycache__' not in f.parts:add(f.relative_to(R).as_posix())
for path in ['.gitattributes',(H/'CURRENT.json').relative_to(R).as_posix(),(H/'README.md').relative_to(R).as_posix(),'audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','design/audit_impacts/flat-vector-geode-source-closure-20261013.json']:add(path)
audit=json.loads((P/'SOURCE_AUDIT.json').read_text());review=json.loads((P/'REVIEW.json').read_text())
for path in audit['scope']['production_text_paths']:add(path,OLD,'Complete declared production-text search input')
for x in audit['image_inventory']+audit['source_files']+audit['provenance']+review['existing_native_images_reinspected']+review['same_scene_reference_bindings']:add(x['path'],x['revision'],'Exact named-source/caller/current native/appearance evidence')
for x in json.loads((PREV/'SOURCES.json').read_text())['sources']:add(x['path'],x['immutable_revision'],'Inherited exact production/provenance/same-scene reference')
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','REVIEW.json','PREFLIGHT.json','REUSE_JOB.json','FIT_MEASUREMENTS.json','SOURCE_PARITY.json','PARTITION_PROOF.json','DERIVATIVES.json','candidate_geode_surface.gd']:
 add((PREV/name).relative_to(R).as_posix(),OLD,'Immutable R12 context/history/technical method; preceding dependency closure retains its own exact manifest/receipt')
for path in ['AGENTS.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','design/02_ART_DIRECTION.md','ART_STYLE_GUIDE.md','design/animation/ANIMATION_PRODUCTION_PROTOCOL.md']:add(path,OLD,'Binding scoped authority')
rows=sorted(rows.values(),key=lambda x:(x['revision'] or 'CURRENT',x['path']))
d={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261013-R13','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join((x['revision'] or 'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'excluded_post_publication_record':'REMOTE_VERIFICATION.json and RECEIPT_GATES.json','accepted_removed':0,'mission_complete':False}
(P/'MANIFEST.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');print('R13_MANIFEST',len(rows),d['required_bytes'],d['payload_sha256'])

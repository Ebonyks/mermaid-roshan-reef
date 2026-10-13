"""Seal additive R14 audit, exact source dependencies and inherited publication context."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;OLD='8a0db03f72735b67ebb581927051c92ca62eaef9';PREV=H/'r13_geode_source_closure'
def sha(b):return hashlib.sha256(b).hexdigest()
rows={}
def add(path,rev=None,role='R14 audit/current metadata'):
 b=(R/path).read_bytes() if rev is None else subprocess.check_output(['git','show',rev+':'+path],cwd=R,stderr=subprocess.PIPE);rows[(rev,path)]={'path':path,'revision':rev,'bytes':len(b),'sha256':sha(b),'role':role}
for f in P.rglob('*'):
 if f.is_file() and f.name not in ['MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json'] and '__pycache__' not in f.parts:add(f.relative_to(R).as_posix())
for path in ['.gitattributes',(H/'CURRENT.json').relative_to(R).as_posix(),(H/'README.md').relative_to(R).as_posix(),'audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','ASSET_LICENSES.md','design/audit_impacts/flat-vector-geode-lifecycle-20261013.json']:add(path)
source=json.loads((P/'SOURCES.json').read_text());review=json.loads((P/'REVIEW.json').read_text())
for x in source['sources']:add(x['path'],x['immutable_revision'],'Current exact code/appearance/provenance dependency; baseline bindings separate')
old_audit=json.loads((PREV/'SOURCE_AUDIT.json').read_text())
for path in old_audit['scope']['production_text_paths']:
 add(path,None if path in ['scripts/opera_geology_surface.gd','scripts/probe_opera_2d.gd'] else OLD,'Complete current declared source/caller text input')
for path in ['scripts/opera_geology_surface.gd','scripts/probe_opera_2d.gd']:add(path,OLD,'Exact original expected-failing source/probe baseline')
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','REVIEW.json','PREFLIGHT.json','SOURCE_AUDIT.json','ORIGIN_DEV_RECONCILIATION.json']:
 add((PREV/name).relative_to(R).as_posix(),OLD,'Immutable R13 published context/history/whole-unit scope; earlier dependencies retain exact previously verified manifests/receipts')
for path in ['AGENTS.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','design/02_ART_DIRECTION.md','ART_STYLE_GUIDE.md','design/animation/ANIMATION_PRODUCTION_PROTOCOL.md','scripts/ci.sh','tools/audit_game_2d.py','tools/audit_document_authority.py','tools/audit_development.py','tools/lint_inference.py','tools/resolve_godot.py','tools/godot_baseline.json']:add(path,OLD,'Binding scoped authority')
rows=sorted(rows.values(),key=lambda x:(x['revision'] or 'CURRENT',x['path']))
d={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261013-R14','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join((x['revision'] or 'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'excluded_post_publication_record':'REMOTE_VERIFICATION.json and RECEIPT_GATES.json','accepted_removed':0,'mission_complete':False}
(P/'MANIFEST.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');print('R14_MANIFEST',len(rows),d['required_bytes'],d['payload_sha256'])

from pathlib import Path
import json,hashlib,subprocess,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r73_hand_consumer_audit';B='0f99b32d98729d11f114dbebcf5b90aba39ca545';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
s=importlib.util.spec_from_file_location('a74manifest',P/'bounded_json.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def sha(b):return hashlib.sha256(b).hexdigest()
rows={}
def add(path,rev=None,role='Current R74 bounded embedded source evidence; no acceptance'):
 raw=(R/path).read_bytes()if rev is None else git('show',rev+':'+path);rows[(rev,path)]={'path':path,'revision':rev,'bytes':len(raw),'sha256':sha(raw),'role':role}
post={'MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','receipt_gates.log','FINAL_BYTE_RECEIPT.json'}
for path in sorted(set(git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines())):
 if path.startswith(P.relative_to(R).as_posix()+'/')and(Path(path).name in post or Path(path).name.startswith(('MANIFEST.fragment','REMOTE_VERIFICATION.fragment'))):continue
 add(path)
for x in A.read_document(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:add(x['path'],x['revision'],'Exact current source/art/license/domain dependency')
for path in git('ls-tree','-r','--name-only',B,'--',O.relative_to(R).as_posix()).decode().splitlines():
 if Path(path).name in {'README.md','SUMMARY.json','per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','WORK_IN_PROGRESS.json','MANIFEST.json','REMOTE_VERIFICATION.json','FINAL_BYTE_RECEIPT.json','CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json','SOURCE_GUARDS.json'}or Path(path).name.startswith(('MANIFEST.fragment','REMOTE_VERIFICATION.fragment')):add(path,B,'Immutable prior R73 canonical/history, no renewed whole-game acceptance')
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:add((H/n).relative_to(R).as_posix(),B,'Frozen original registry preserved exactly')
add((H/'r51_farmer_context/RUNTIME_BYTE_BASELINE.json').relative_to(R).as_posix(),B,'Retained source/import byte baseline')
for n in ['NEW_ART_REVIEW_REQUEST.json','README.md','FINAL_BYTE_RECEIPT.json']:add((H/'r72_skyway_hand_reuse'/n).relative_to(R).as_posix(),B,'Prior unapproved exact ImageGen request and receipt; no retry/export')
rows=sorted(rows.values(),key=lambda x:(x['revision']or'CURRENT',x['path']));m={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261015-R74','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','audited_source_revision':D,'topic_baseline':B,'files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes']for x in rows),'payload_sha256':sha(''.join((x['revision']or'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n'for x in rows).encode()),'historical_parent':{'receipt':B,'prior_payload':'5a46e06c26be03099967e665d7407b507f9cf010','freshly_reverified_transitive_payload':False},'metrics':A.read_document(P/'SUMMARY.json'),'post_publication_records':'Receipt metadata anonymously checked separately after push to avoid recursive self-hash claim.','accepted_removed':0,'mission_complete':False};A.write_document(P/'MANIFEST.json',m);print('R74_MANIFEST',len(rows),m['required_bytes'],flush=True)

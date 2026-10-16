from pathlib import Path
import json,hashlib,subprocess,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r74_tree_book_context';B='715c7a230c159e70acae1cd0ddad727e88910cb9';D='dd799b2d43871b29d1d6e0503646308a194dad1e'
s=importlib.util.spec_from_file_location('a75manifest',P/'bounded_json.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def sha(b):return hashlib.sha256(b).hexdigest()
rows={}
def add(path,rev=None,role='Current R75 source-bound hand registration diagnostics;0acceptance'):
 raw=(R/path).read_bytes()if rev is None else git('show',rev+':'+path);rows[(rev,path)]={'path':path,'revision':rev,'bytes':len(raw),'sha256':sha(raw),'role':role}
post={'MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','receipt_gates.log','FINAL_BYTE_RECEIPT.json'}
for path in sorted(set(git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines())):
 if path.startswith(P.relative_to(R).as_posix()+'/')and(Path(path).name in post or Path(path).name.startswith(('MANIFEST.fragment','REMOTE_VERIFICATION.fragment'))):continue
 add(path)
for x in A.read_document(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:add(x['path'],x['revision'],'Exact selected current-source/painted-context/provenance or immutable prior context dependency')
for path in git('ls-tree','-r','--name-only',B,'--',O.relative_to(R).as_posix()).decode().splitlines():
 if Path(path).name in {'README.md','SUMMARY.json','per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','WORK_IN_PROGRESS.json','MANIFEST.json','REMOTE_VERIFICATION.json','FINAL_BYTE_RECEIPT.json','CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json','SOURCE_GUARDS.json'}or Path(path).name.startswith(('MANIFEST.fragment','REMOTE_VERIFICATION.fragment')):add(path,B,'Immutable prior R74 canonical/history; no renewed transitive native/acceptance claim')
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:add((H/n).relative_to(R).as_posix(),B,'Frozen original registry byte-preserved')
add((H/'r51_farmer_context/RUNTIME_BYTE_BASELINE.json').relative_to(R).as_posix(),B,'Retained exact prior raw source/import baseline used for EOL recovery')
for n in ['NEW_ART_REVIEW_REQUEST.json','README.md','FINAL_BYTE_RECEIPT.json']:add((H/'r72_skyway_hand_reuse'/n).relative_to(R).as_posix(),B,'Prior exact unapproved ImageGen request/receipt; no retry/export')
rows=sorted(rows.values(),key=lambda x:(x['revision']or'CURRENT',x['path']));m={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261015-R75','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','audited_source_revision':D,'topic_baseline':B,'files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes']for x in rows),'payload_sha256':sha(''.join((x['revision']or'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n'for x in rows).encode()),'historical_parent':{'receipt':B,'prior_payload':'23ace33abc1d74b938dbaead53a0b4e421c22e1a','freshly_reverified_transitive_payload':False},'metrics':A.read_document(P/'SUMMARY.json'),'post_publication_records':'Receipt own metadata bytes/head anonymously checked after push separately, avoiding recursive self hash.','accepted_removed':0,'mission_complete':False};A.write_document(P/'MANIFEST.json',m);print('R75_MANIFEST',len(rows),m['required_bytes'],flush=True)

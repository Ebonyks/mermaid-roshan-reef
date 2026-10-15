from pathlib import Path
import json,hashlib,subprocess,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r51_farmer_context';B='65adbc4ace23d5988b0c444c269f43142a7127e3';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
s=importlib.util.spec_from_file_location('bound51manifest',P/'bounded_json.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def sha(b):return hashlib.sha256(b).hexdigest()
rows={}
def add(path,rev=None,role='Current R52 audit evidence; acceptance open'):
 b=(R/path).read_bytes()if rev is None else git('show',rev+':'+path);rows[(rev,path)]={'path':path,'revision':rev,'bytes':len(b),'sha256':sha(b),'role':role}
post={'MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','receipt_gates.log','FINAL_BYTE_RECEIPT.json'}
for path in sorted(set(git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines())):
 if path.startswith(P.relative_to(R).as_posix()+'/')and(Path(path).name in post or Path(path).name.startswith(('MANIFEST.fragment','REMOTE_VERIFICATION.fragment'))):continue
 add(path)
for x in json.loads((P/'SOURCE_REFERENCES.json').read_text())['files']:add(x['path'],x['revision'],'Exact current source/domain/same-scene reference')
# Historical dependencies remain bound to their independently verified immutable packet.
# Verify every immediate canonical/manifest/receipt dependency, without claiming a fresh historical image review.
for path in git('ls-tree','-r','--name-only',B,'--',O.relative_to(R).as_posix()).decode().splitlines():
 if Path(path).name in {'RUNTIME_BYTE_BASELINE.json','SAVE_REGRESSION.json','SOURCE_REFERENCES.json','REVIEW.json','CAPTURE_INDEX.json','README.md','per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','WORK_IN_PROGRESS.json','MANIFEST.json','REMOTE_VERIFICATION.json','FINAL_BYTE_RECEIPT.json','bounded_json.py'}or Path(path).name.startswith(('MANIFEST.fragment','REMOTE_VERIFICATION.fragment')):add(path,B,'Immutable R51 parent canonical/complete dependency manifest/verification receipt; historical transitive pixels retain prior exact verification time')
for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:add((H/name).relative_to(R).as_posix(),B,'Preserved frozen original registry')
union='docs/handoffs/codex_flat_vector_art_2026-10-07/r48_grand_puff_context/CURRENT_PARTIAL_CONTEXT_UNION.json';add(union,B,'Unchanged73existing partial ID union; no new unique partial piece credit')
rows=sorted(rows.values(),key=lambda x:(x['revision']or'CURRENT',x['path']));m={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261015-R52','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','audited_source_revision':D,'topic_baseline':B,'files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes']for x in rows),'payload_sha256':sha(''.join((x['revision']or'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n'for x in rows).encode()),'scope':'All new R52 evidence and direct current source/canonical dependencies. Immutable R51 manifest and full receipt index/allparts preserve independent historical transitive verification; no fresh historical pixels/reviews or global exhaustiveness claimed.','historical_parent':{'payload':'8cdf8df7373615d827357e9cfa8ecce4aa373e05','receipt':'1a86a9cee4cd061be60c8d9cc7b8ae4689f3551f','final_proof':B,'historical_direct_required_file_count':257,'historical_direct_required_bytes':218477317,'freshly_reverified_transitive_payload':False},'post_publication_records':'Receipt/gates/final metadata separately bound to immutable commits to avoid recursive selfhash.','new_native_captures':81,'new_bounded_contexts':74,'nonruntime_candidate_captures':44,'current_source_control_captures':30,'new_generation_calls':0,'accepted_removed':0,'mission_complete':False};files=A.write_document(P/'MANIFEST.json',m);print('R52_MANIFEST',len(rows),m['required_bytes'],len(files),'physical files',flush=True)

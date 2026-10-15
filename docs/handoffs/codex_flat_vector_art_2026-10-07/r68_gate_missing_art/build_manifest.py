from pathlib import Path
import json,hashlib,subprocess,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r67_painted_gate_cue';B='348116d6dc82c5a4f9e0a6a0b856de0ff6416349';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
s=importlib.util.spec_from_file_location('bounded67manifest',P/'bounded_json.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def sha(b):return hashlib.sha256(b).hexdigest()
rows={}
def add(path,rev=None,role='Current R68 evidence; acceptance open'):
 b=(R/path).read_bytes()if rev is None else git('show',rev+':'+path);rows[(rev,path)]={'path':path,'revision':rev,'bytes':len(b),'sha256':sha(b),'role':role}
post={'MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','receipt_gates.log','FINAL_BYTE_RECEIPT.json'}
for path in sorted(set(git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines())):
 if path.startswith(P.relative_to(R).as_posix()+'/')and(Path(path).name in post or Path(path).name.startswith(('MANIFEST.fragment','REMOTE_VERIFICATION.fragment'))):continue
 add(path)
for x in json.loads((P/'DELIVERY_SOURCE_REFERENCES.json').read_text(encoding='utf-8'))['files']:add(x['path'],x['revision'],'Exact source/reuse/current-scene dependency')
for x in json.loads((P/'CONTEXT_PREREQUISITE.json').read_text(encoding='utf-8'))['checks']:add(x['path'],x['revision'],'Before-candidate remote context prerequisite')
for path in git('ls-tree','-r','--name-only',B,'--',O.relative_to(R).as_posix()).decode().splitlines():
 if Path(path).name in {'README.md','per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','WORK_IN_PROGRESS.json','MANIFEST.json','REMOTE_VERIFICATION.json','FINAL_BYTE_RECEIPT.json','CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json'}or Path(path).name.startswith(('MANIFEST.fragment','REMOTE_VERIFICATION.fragment')):add(path,B,'Immutable R67 canonical/history/manifest/receipt; historical verification times retain scope')
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:add((H/n).relative_to(R).as_posix(),B,'Frozen original registry, byte-preserved')
add((H/'r51_farmer_context/RUNTIME_BYTE_BASELINE.json').relative_to(R).as_posix(),B,'Initialized native source/sidecar baseline; historical import scope preserved')
rows=sorted(rows.values(),key=lambda x:(x['revision']or'CURRENT',x['path']));summary=json.loads((P/'SUMMARY.json').read_text(encoding='utf-8'));m={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261015-R68','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','audited_source_revision':D,'topic_baseline':B,'files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes']for x in rows),'payload_sha256':sha(''.join((x['revision']or'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n'for x in rows).encode()),'historical_parent':{'payload':'ceda23cfb6a65d8685906b3599f97ddb28044e68','receipt':'f886b5fd530fe33125060dd7b845181cb3f19fc1','final_proof':B,'historical_direct_required_file_count':174,'historical_direct_required_bytes':85775245,'freshly_reverified_transitive_payload':False},'metrics':{k:v for k,v in summary.items()if k!='cases'},'post_publication_records':'Receipt metadata is bound and anonymously verified separately to avoid recursive self hash.','accepted_removed':0,'mission_complete':False};A.write_document(P/'MANIFEST.json',m);print('R68_MANIFEST',len(rows),m['required_bytes'],flush=True)

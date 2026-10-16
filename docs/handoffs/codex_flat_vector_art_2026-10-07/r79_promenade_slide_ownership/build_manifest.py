from pathlib import Path
import json,hashlib,subprocess,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r78_game_payload_closure';B='ce4a454f65fc5b61f915ce41176af866fdf633ab';D='dd799b2d43871b29d1d6e0503646308a194dad1e'
s=importlib.util.spec_from_file_location('a76manifest',P/'bounded_json.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def sha(b):return hashlib.sha256(b).hexdigest()
rows={}
def add(path,rev=None,role='Current R79 source-bound current original-input playground owner/context audit;0production/art/acceptance'):
 if (rev,path)in rows:return
 raw=(R/path).read_bytes()if rev is None else git('show',rev+':'+path);rows[(rev,path)]={'path':path,'revision':rev,'bytes':len(raw),'sha256':sha(raw),'role':role}
 if path.endswith('.json'):
  x=json.loads(raw)
  if isinstance(x,dict)and x.get('schema')==A.INDEX_SCHEMA:
   for part in x['fragments']:add(str(Path(path).parent/part['path']).replace('\\','/'),rev,role+' physical JSON fragment')
post={'MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','receipt_gates.log','FINAL_BYTE_RECEIPT.json'}
for path in sorted(set(git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines())):
 if path.startswith(P.relative_to(R).as_posix()+'/')and(Path(path).name in post or Path(path).name.startswith(('MANIFEST.fragment','REMOTE_VERIFICATION.fragment'))):continue
 add(path)
for x in A.read_document(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:add(x['path'],x['revision'],'Exact current source scripts/config/resources; source-only named boundary review, no visual acceptance')
for name in ['README.md','SUMMARY.json','per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json','WORK_IN_PROGRESS.json','MANIFEST.json','REMOTE_VERIFICATION.json','FINAL_BYTE_RECEIPT.json','CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json','SEMANTIC_SOURCE_GUARD.json','scan_game_payload.py','bounded_json.py','SOURCE_PAYLOAD_GRAPH.json']:add((O/name).relative_to(R).as_posix(),B,'Immutable R78 history, no renewed transitive native quality or acceptance claim')
add((H/'r75_tree_book_registration/RUNTIME_BYTE_BASELINE.json').relative_to(R).as_posix(),B,'Exact preserved R75 runtime/import baseline used by current guards')
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:add((H/n).relative_to(R).as_posix(),B,'Frozen original registry, exact bytes preserved; occurrences not piece totals')
for n in ['NEW_ART_REVIEW_REQUEST.json','README.md','FINAL_BYTE_RECEIPT.json']:add((H/'r72_skyway_hand_reuse'/n).relative_to(R).as_posix(),B,'Prior unapproved external payload request, no retry/export')
for n in ['README.md','LEGACY_POLICY_MISMATCH.json']:add((H/'r66_display_entry_context'/n).relative_to(R).as_posix(),B,'Retained prior R66 entry/policy failure scope;not retested by fresh DayOne profiles')
for n in ['USERDIR_PREFLIGHT.json','capture_entry.gd']:add((H/'r77_intro_entry_ownership'/n).relative_to(R).as_posix(),B,'Exact retained private-userdir/normal-path bootstrap provenance; not a new or relabeled preflight')
rows=sorted(rows.values(),key=lambda x:(x['revision']or'CURRENT',x['path']));m={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261016-R79','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','audited_source_revision':D,'topic_baseline':B,'files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes']for x in rows),'payload_sha256':sha(''.join((x['revision']or'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n'for x in rows).encode()),'historical_parent':{'receipt':B,'prior_payload':'c641283bba1c1bb2dfe56faa2341f474f45543bd','freshly_reverified_transitive_payload':False},'metrics':A.read_document(P/'SUMMARY.json'),'post_publication_records':'Receipt own final changed metadata bytes/head checked after push separately;no recursive self hash.','accepted_removed':0,'mission_complete':False};A.write_document(P/'MANIFEST.json',m);print('R79_MANIFEST',len(rows),m['required_bytes'],flush=True)

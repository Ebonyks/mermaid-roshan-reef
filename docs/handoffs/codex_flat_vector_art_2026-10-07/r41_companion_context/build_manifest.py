from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r40_craft_whole_fish_trial';BASE='de44f9bb67ae7cb41a33d6eba25d56d9ed074f21';OLD='0466a6e5300da701215010b6c072a167e2e00d0d';rows={}
def sha(b):return hashlib.sha256(b).hexdigest()
def add(path,revision=None,role='R41 source-only candidate/evidence; no artwork acceptance'):
 b=(R/path).read_bytes() if revision is None else subprocess.check_output(['git','show',revision+':'+path],cwd=R,stderr=subprocess.PIPE);rows[(revision,path)]={'path':path,'revision':revision,'bytes':len(b),'sha256':sha(b),'role':role}
for x in json.loads((O/'MANIFEST.json').read_text(encoding='utf-8'))['files']:
 rev=x['revision'] or OLD;rows[(rev,x['path'])]=dict(x,revision=rev,role='Inherited immutable R39/prior evidence; acceptance unchanged')
post={'MANIFEST.json','REMOTE_VERIFICATION.json','RECEIPT_GATES.json','receipt_gates.log','FINAL_BYTE_RECEIPT.json'}
for f in sorted(P.rglob('*')):
 if f.is_file() and f.name not in post and not f.name.startswith('REMOTE_VERIFICATION.fragment'):add(f.relative_to(R).as_posix())
changed=set(subprocess.check_output(['git','diff','--name-only',BASE],cwd=R,text=True,stderr=subprocess.PIPE).splitlines()+subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R,text=True).splitlines())
for path in sorted(changed):
 if path.startswith(P.relative_to(R).as_posix()+'/') and (Path(path).name in post or Path(path).name.startswith('REMOTE_VERIFICATION.fragment')):continue
 add(path)
for x in json.loads((P/'CONTEXT_PREREQUISITE.json').read_text(encoding='utf-8'))['checks']:add(x['path'],x['revision'],'Published source/context prerequisite before edit')
for x in json.loads((P/'REVIEW.json').read_text(encoding='utf-8'))['source_references']:add(x['path'],x['revision'],x['role'])
for path in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--',O.relative_to(R).as_posix()],cwd=R,text=True).splitlines():add(path,BASE,'Immutable R39 payload/final receipt/proof at baseline')
rows=sorted(rows.values(),key=lambda x:(x['revision'] or 'CURRENT',x['path']));d={'schema':'reef.flat_vector_delta_manifest/1','revision':'FV-AUDIT-20261014-R41','repository':'Ebonyks/mermaid-roshan-reef','branch':'codex/flat-vector-r6-20261012','files':rows,'required_file_count':len(rows),'required_bytes':sum(x['bytes'] for x in rows),'payload_sha256':sha(''.join((x['revision'] or 'CURRENT')+'\t'+x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in rows).encode()),'excluded_post_publication_record':'REMOTE_VERIFICATION/index/allfragments,RECEIPT_GATES,receipt_gates.log,FINAL_BYTE_RECEIPT; final exact metadata and own proof separately verified','new_unique_whole_drawing_samples':0,'new_generation_calls':0,'new_source_retirements':0,'accepted_removed':0,'mission_complete':False};(P/'MANIFEST.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');print('R41_MANIFEST',len(rows),d['required_bytes'],d['payload_sha256'])

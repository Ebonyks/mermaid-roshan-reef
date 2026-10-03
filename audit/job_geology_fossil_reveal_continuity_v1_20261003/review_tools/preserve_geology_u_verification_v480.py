from pathlib import Path
import json,hashlib,datetime,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');K=R/'audit/job_geology_fossil_reveal_continuity_v1_20261003';src=R/'tmp/geology_review_u_remote_v474';out=K/'previous_u_remote_verified'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
receipt=read(src/'RESULT.json');assert receipt['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and receipt['revision']=='c5977ebb29bb2011b20fc149ad350290f045045c' and receipt['files_including_manifest']==20087 and not receipt['failed_files']
assert not out.exists();out.mkdir();shutil.copyfile(src/'RESULT.json',out/'RESULT.json')
raw=(src/'VERIFICATION_JOURNAL.jsonl').read_bytes();lines=raw.splitlines(keepends=True);assert len(lines)==20087 and all(json.loads(x)['matches'] for x in lines)
parts=[];chunk=bytearray()
def flush():
 if not chunk:return
 p=out/f'JOURNAL_{len(parts)+1:02d}.jsonl';p.write_bytes(chunk);parts.append({'path':p.relative_to(R).as_posix(),'sha256':sha(chunk),'bytes':len(chunk),'rows':len(chunk.splitlines())});chunk.clear()
for line in lines:
 if len(chunk)+len(line)>900000:flush()
 chunk.extend(line)
flush();assert b''.join((R/x['path']).read_bytes() for x in parts)==raw
write(out/'JOURNAL_INDEX.json',{'status':'EXACT_LOSSLESS_ALL20087_U_REMOTE_ROWS','revision':receipt['revision'],'original_sha256':sha(raw),'original_bytes':len(raw),'rows':len(lines),'ordered_parts':parts,'qualification':'Exact full anonymous normal-TLS no-Authorization verification journal, line-boundary shards only. Preserves every success/attempt/time/hash; no row omitted. Current U remote byte receipt, not new reveal-trial visual or hosted/device/child/owner acceptance. Staged for the next publication; no K delivery claim.'})
shutil.copyfile(Path(__file__),K/'review_tools'/Path(__file__).name)
write(K/'MACHINE_REVIEW_STATUS.json',{'status':'BOTH_INPUT_CAPTURES_PASS_DIRECT_REVIEW_PENDING','frames':437,'selected_views':58,'ordered_boards':48,'native_full_details_seen_so_far':[{'path':K.relative_to(R).as_posix()+'/attempt01/native_views/geologist_1280_phase1_task_open.webp','scope':'One native spot inspection; not a complete sequence score.'},{'path':K.relative_to(R).as_posix()+'/attempt01/native_views/geologist_1280_phase1_brushed.webp','scope':'One native spot inspection; not a complete sequence score.'}],'score':None,'production_binding':False,'owner_acceptance':None,'qualification':'All six explicit checks pass. Each of437 input/wait frames and58 selected canvases still requires direct review; no inferred current or counterfactual action floor.'})
ip=R/'design/audit_impacts/job-geology-fossil-reveal-continuity-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in K.rglob('*') if x.is_file()});d['validation'][0].update(result='PASS',evidence=K.relative_to(R).as_posix()+'/runtime_gate_a1/;all six explicit checks,783 unchanged production hashes.');d['acceptance_gaps']='Complete native direct review pending:437 consecutive frames,58 selected views,48 boards. No score assigned. Only two1280 spot-native canvases inspected. Current production/coarse dirt/ghost target/hands/room/completion/natural timing/story/device/child/owner/all-job/finding closure/integration/release remain open. U20087 anonymous remote files all verified; new U hosted run37093610815 is separate and in progress. Full U remote journal copied losslessly for next publication; K is unfinished staging, not delivered.';write(ip,d)
print(json.dumps({'U':'ALL20087_REMOTE_BYTES_VERIFIED','lossless_journal_parts':len(parts),'journal_rows':len(lines),'new_reveal_trial':'MACHINE_PASS_VISUAL_REVIEW_PENDING','production':'UNCHANGED','goal':'ACTIVE'}))

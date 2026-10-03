from pathlib import Path
import datetime, hashlib, json, shutil

B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';Q=P/'comparison_a2'
IP=B/'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):
    task_next=p.with_name(p.name+'.v549_next');task_next.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n');task_next.replace(p)
review={'status':'DIRECT_COMPLETE_NATIVE_A2_INPUT_REVIEWED','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'path':(Q/'inputs/CANDY-FOLD-A2.png').relative_to(B).as_posix(),'sha256':sha(Q/'inputs/CANDY-FOLD-A2.png'),'size':[896,512],'observations':'Complete unchanged A11 pose is visible at uniform scale with two connected mittens. Screen-left mitten holds the raised far-edge flap; screen-right braces beside the same red oval. Sweet, paper, lavender support, hat/hair/rainbow ribbon and costume remain intact on a plain mat. Requested near-edge role remains rejected. Source resemblance cannot pass actual folding or the full wrap.','source_score_transfer':False,'owner_acceptance':None,'runtime_binding':False}
write(Q/'INPUT_DIRECT_REVIEW.json',review)
m=read(Q/'MANIFEST.json');assert m['status']=='BOUND_FAR_FOLD_INPUT_PENDING_DIRECT_REVIEW'
m['input_visual_review']={'status':review['status'],'evidence':(Q/'INPUT_DIRECT_REVIEW.json').relative_to(B).as_posix(),'source_score_transfer':False};m['status']='BOUND_FAR_FOLD_INPUT_REVIEWED_READY_FOR_QUIET_IDLE_DISPATCH';write(Q/'MANIFEST.json',m)
write(Q/'NORMALIZATION_SCRIPT_GATES.json',{'status':'PASS_PARSER_AND_TYPED_INFERENCE','observed_utc':review['reviewed_utc'],'script':(Q/'review_tools/normalize_complete_fold_source.gd').relative_to(B).as_posix(),'script_sha256':sha(Q/'review_tools/normalize_complete_fold_source.gd'),'commands':[{'command':'python -X utf8 -B -m gdtoolkit.parser assets_src/local_motion/candy_wrap_continuity_v1_20261003/comparison_a2/review_tools/normalize_complete_fold_source.gd','process_exit':0,'tool_output':''},{'command':'python -X utf8 -B tools/lint_inference.py assets_src/local_motion/candy_wrap_continuity_v1_20261003/comparison_a2/review_tools/normalize_complete_fold_source.gd','process_exit':0,'tool_output':''}],'qualification':'Exact helper parser/lint and prior official4.7.2 normalization process only; no full action/runtime pass.'})
source=B/'audit/job_shared_entrance_sources_v1_20261003/review_tools/run_shared_report_gates_v535.py'
code=source.read_text(encoding='utf-8')
changes={"c=b/'audit/job_shared_entrance_sources_v1_20261003'":"c=b/'assets_src/local_motion/candy_wrap_continuity_v1_20261003'","run_shared_report_gates_v535.py":"run_candy_local_review_gates_v549.py","job-shared-entrance-source-review-20261003.json":"job-candy-local-wrap-continuity-20261003.json"}
for a,z in changes.items():assert a in code;code=code.replace(a,z)
target=P/'review_tools/run_candy_local_review_gates_v549.py';compile(code,str(target),'exec');target.write_text(code,encoding='utf-8',newline='\n')
write(P/'GATE_RUNNER_DERIVATION.json',{'source_path':source.relative_to(B).as_posix(),'source_sha256':sha(source),'changes':changes,'qualification':'Only artifact/impact/runner identifiers. Authority, actual --base auto coverage,52 document tests, no-regression command and raw receipt preservation unchanged. Run after completed new review metadata.'})
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
d=read(IP);d['files']=sorted(set(d['files'])|{x.relative_to(B).as_posix() for x in P.rglob('*') if x.is_file()})
d['validation'].append({'command':'Direct complete A2 technical input inspection; exact helper parser/inference/engine normalization and unchanged developed dispatcher --check','result':'PASS','evidence':(Q/'INPUT_DIRECT_REVIEW.json').relative_to(B).as_posix()+'; '+(Q/'NORMALIZATION_SCRIPT_GATES.json').relative_to(B).as_posix()})
write(IP,d)
print('A2_NATIVE_INPUT_REVIEWED|one far-fold component ready|full wrapping acceptance remains open|later validators unchanged')

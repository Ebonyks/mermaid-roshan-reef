from pathlib import Path
import json,subprocess,time,datetime,hashlib,urllib.request,urllib.parse,concurrent.futures
S=Path(__file__).parent;U=Path.cwd();W=S/'dev_integration_ci_recovered';RUN='41210387137';SRC='218ae766f8e60afb3f6338b8fafce28ec9fab7f2';OLD='a290753627a06ca7b251c3423cce6cf6f5d13827';BR='codex/flat-vector-geologist-pan-runtime-20261017';REPO='Ebonyks/mermaid-roshan-reef'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def state(n,**k):wr(W/'CONTINUATION_STATE.json',dict(state=n,at_utc=now(),**k))
def gh(*a):
 for i in range(5):
  q=subprocess.run(['gh',*a],cwd=U,capture_output=True,text=True,encoding='utf8',timeout=90)
  if q.returncode==0:return json.loads(q.stdout)
  if i==4:raise RuntimeError('Read failed: '+q.stderr[-1000:])
  time.sleep(15)
def git(*a):return subprocess.check_output(['git',*a],cwd=U,stderr=subprocess.PIPE)
def gs(*a):return git(*a).decode('utf8').strip()
assert U==Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef')
assert W.is_dir() and not (W/'FINAL_RESULT.json').exists()
try:
 pub=rd(S/'SOURCE_PUBLICATION_FINAL.json');receipt=rd(S/'SOURCE_REMOTE_VERIFICATION.json');assert pub['source_revision']==SRC==receipt['revision'] and all(x['verified']for x in receipt['files']);assert rd(S/'full_validation/FINAL_RESULT.json')['status']=='PASS_ALL_82_AND_CURRENT_STATIC'
 dispatch=rd(W/'RETRY_DISPATCH.json');assert dispatch['exit_code']==0 and dispatch['retry_cap']==1 and dispatch['command']==['gh','run','rerun',RUN,'--failed','--repo',REPO]
 d=rd(W/'ORIGINAL_ATTEMPT1.json');jobs={j['name']:j for j in d['jobs']};assert d['headSha']==SRC and jobs['probes']['conclusion']=='success'
 original_api=rd(W/'ATTEMPT1_JOBS_API.json');original_probes=next(j for j in original_api['jobs']if j['name']=='probes');assert original_probes['id']==124563970967
 log=(S/'source_ci_failure_attempt1/area-music-provenance.log').read_bytes();assert b'503 (Service Unavailable)'in log
 state('MONITORING_EXISTING_ATTEMPT2_AREA_MUSIC_JOB_NO_DISPATCH',workflow_run=RUN,area_music_job=124577616760,retry_cap_spent=True,source_revision=SRC)
 start=time.monotonic()
 while True:
  api=gh('api','repos/'+REPO+'/actions/runs/'+RUN);assert api['head_sha']==SRC and api['run_attempt']==2;wr(W/'ATTEMPT2_RUN_API.json',api)
  new=gh('api','repos/'+REPO+'/actions/runs/'+RUN+'/attempts/2/jobs?per_page=100');wr(W/'ATTEMPT2_JOBS.json',new)
  assert len(new['jobs'])==2 and {j['name']for j in new['jobs']}=={'area-music-provenance','probes'}
  copied=next(j for j in new['jobs']if j['name']=='probes');area=next(j for j in new['jobs']if j['name']=='area-music-provenance');assert copied['id']==124577617530 and area['id']==124577616760
  fields=['name','status','conclusion','started_at','completed_at','runner_id','runner_name','steps','labels']
  assert all(original_probes[k]==copied[k]for k in fields),'Successful probes execution metadata changed; stop without dispatch'
  assert copied['completed_at']<'2026-10-31T15:28:25Z' and area['started_at']>'2026-10-31T15:28:25Z'
  proof=dict(state='ORIGINAL_SUCCESSFUL_PROBES_METADATA_COPIED_WITHOUT_NEW_EXECUTION',source_revision=SRC,original_job=original_probes['id'],copied_metadata_job=copied['id'],newly_executing_area_music_job=area['id'],compared_equal_fields=fields,original_started_at=original_probes['started_at'],original_completed_at=original_probes['completed_at'],retry_dispatched_at=dispatch['at_utc'],only_new_execution_started_at=area['started_at'],original_snapshot_sha256=sha((W/'ATTEMPT1_JOBS_API.json').read_bytes()),current_snapshot_sha256=sha((W/'ATTEMPT2_JOBS.json').read_bytes()),prior_assertion='Stopped observer assumed attempt2 job listing would omit successful jobs. GitHub copied completed successful probes metadata with a new id and unchanged execution timestamps/steps.',metadata_only_difference_allowed='runner_group_id may be 0/null; execution fields and steps exact',no_new_dispatch=True,retry_cap_spent=True,checked_at_utc=now())
  wr(W/'HEALTHY_JOB_REUSE_PROOF.json',proof)
  if api['status']=='completed':break
  assert time.monotonic()-start<3600;time.sleep(30)
 assert api['conclusion']=='success' and all(j['conclusion']=='success'for j in new['jobs']),'Existing bounded failed-job retry did not pass; no additional retry authorized'
 latest=gh('run','view',RUN,'--repo',REPO,'--json','status,conclusion,headSha,headBranch,url,jobs');wr(W/'ATTEMPT2_RUN_VIEW.json',latest);assert latest['status']=='completed' and latest['conclusion']=='success' and latest['headSha']==SRC
 # Normalize the raw attempt2 area job to gh-view shape; retain the attempt1 trusted job unchanged.
 fresh=[j for j in latest['jobs']if j['name']=='area-music-provenance'];assert len(fresh)==1 and fresh[0]['conclusion']=='success'
 composed=dict(latest);composed['jobs']=[jobs['probes'],fresh[0]];composed['evidence_composition']=dict(method='Successful job per exactsource revision across original attempt1 and failed-job-only attempt2',probes_attempt=1,area_music_attempt=2,original_failure_retained=True,healthy_probes_restarted=False,raw_snapshots=['ORIGINAL_ATTEMPT1.json','ORIGINAL_RUN_API.json','ATTEMPT2_JOBS.json','ATTEMPT2_RUN_API.json','ATTEMPT2_RUN_VIEW.json']);composed['evidence_composition']['copied_successful_job_metadata_proof']='HEALTHY_JOB_REUSE_PROOF.json';composed['evidence_composition']['raw_snapshots']+=['ATTEMPT1_JOBS_API.json','HEALTHY_JOB_REUSE_PROOF.json'];wr(W/'SOURCE_CI_GREEN.json',composed)
 recovery=dict(state='EXACT_SOURCE_CI_GREEN_FAILED_JOB_ONLY_RECOVERY',source_revision=SRC,workflow_run=int(RUN),original_attempt=1,retry_attempt=2,failed_job='area-music-provenance',failed_job_id=jobs['area-music-provenance']['databaseId'],failure='Pinned FFmpeg8.1.2 download returned HTTP503; build_area_music lacked FFmpeg. No candidate/audio/source defect established.',original_failure_log_sha256=sha(log),preserved_healthy_job='probes',preserved_trusted_step='success',only_failed_job_rerun=True,healthy_engine_native_local82_or_remote_probes_restarted=False,source_or_pixels_changed=False,retry_cap=1,new_generation_calls=0,new_frame_events=0,attempt2_conclusion=api['conclusion'],at_utc=now());recovery['successful_job_copied_metadata_proof']='HEALTHY_JOB_REUSE_PROOF.json';recovery['observer_assertion_stop_preserved']='STOP.json';recovery['continuation_runner']=Path(__file__).name;recovery['no_new_retry_dispatched_by_continuation']=True;wr(W/'CI_RECOVERY.json',recovery)
 state('SOURCE_CI_GREEN_FRESH_RECONCILIATION');assert gs('rev-parse','HEAD')==SRC and gs('branch','--show-current')==BR and not gs('status','--porcelain')
 subprocess.run(['git','fetch','origin'],cwd=U,check=True,capture_output=True);assert gs('rev-parse','origin/'+BR)==SRC;dev=gs('rev-parse','origin/dev');assert dev in [OLD,SRC],'Dev advanced, reconcile exactsource before integration'
 if dev==OLD:
  subprocess.run(['git','merge-base','--is-ancestor',dev,SRC],cwd=U,check=True,capture_output=True);q=subprocess.run(['git','push','origin',SRC+':refs/heads/dev'],cwd=U,capture_output=True);(W/'DEV_PUSH.log').write_bytes(q.stdout+q.stderr);assert q.returncode==0,q.stderr.decode(errors='replace')
 subprocess.run(['git','fetch','origin','dev'],cwd=U,check=True,capture_output=True);assert gs('ls-remote','origin','refs/heads/dev').split()[0]==SRC
 paths=['scripts/games/dolls.gd','assets/dolls/cradle_sling_painted.png','assets/dolls/cradle_sling_painted.png.import']
 def verify(p):
  expected=git('show',SRC+':'+p);req=urllib.request.Request('https://raw.githubusercontent.com/'+REPO+'/'+SRC+'/'+urllib.parse.quote(p,safe='/'),headers={'User-Agent':'MermaidReef-anonymous-integration-verifier'})
  with urllib.request.urlopen(req,timeout=90)as r:code=r.status;b=r.read()
  assert code==200 and b==expected;return dict(path=p,revision=SRC,bytes=len(b),sha256=sha(b),http_status=code,anonymous_exact=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:rows=list(pool.map(verify,paths))
 handles=gh('run','list','--repo',REPO,'--branch','dev','--limit','12','--json','databaseId,headSha,status,conclusion,url,workflowName');handles=[x for x in handles if x['headSha']==SRC];wr(W/'DEV_WORKFLOW_HANDLES.json',handles)
 result=dict(state='PAINTED_DOLLS_CRADLE_EXACT_GREEN_FAILED_JOB_RECOVERY_INTEGRATED_DEV',source_revision=SRC,integrated_dev_revision=SRC,prior_dev=OLD,source_branch=BR,source_CI_run=int(RUN),source_CI_url='https://github.com/'+REPO+'/actions/runs/'+RUN+'/attempts/2',source_CI_conclusion='success',trusted_step='success',source_CI_evidence_composition=composed['evidence_composition'],CI_recovery='CI_RECOVERY.json',Dev_head_verified_by_anonymous_runtime_bytes_and_git_remote=True,runtime_files=rows,retired_runtime_paths_absent_at_integrated_revision=[],access_mode='Anonymous immutable exact runtime bytes; all95source manifestfiles independently verified before CI.',source_clean=not bool(gs('status','--porcelain')),local_dev_master_untouched=True,PR_created=False,Dev_workflows=handles,exact_new_Dev_APK_verified=False,new_generation_calls=0,new_native_frame_events=0,new_implementation_artifact_credits=0,partial_dev_artifact_credit=1,whole_role_closed=False,formal_QA11=None,device=None,child=None,owner=None,accepted_removed=0,mission_complete=False,completed_at_utc=now());assert result['source_clean'];wr(W/'FINAL_RESULT.json',result);state('TERMINAL_DEV_INTEGRATION_SUCCESS',revision=SRC);print('R118_FAILED_JOB_ONLY_RECOVERY_DEV_SUCCESS',SRC,flush=True)
except Exception as e:
 wr(W/'CONTINUATION_STOP.json',dict(state='STOPPED_NO_AUTOMATIC_RETRY',error=str(e),at_utc=now(),next='Inspect exactrunattempt/source/recovery boundary. Never rerun healthyjobs or forcepush.'));state('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise

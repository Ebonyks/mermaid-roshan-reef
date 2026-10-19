from pathlib import Path
import json,hashlib,shutil,subprocess,re
from datetime import datetime,timezone
r=Path.cwd();s=r/'assets_src/imagegen/job_art_nursery_20261019';b=r/'assets_src/imagegen/job_art_boxer_20261019';v=s/'verification';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.now(timezone.utc).isoformat()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
# Final current-context review is separate from fullmotion and external acceptance.
p=b/'review/art_review.json';old=b/'review/art_review_matte_failure.json';assert not old.exists();shutil.copyfile(p,old);d=json.loads(p.read_text());rows=json.loads((b/'runtime_provenance.json').read_text())['records'];byname={x['path']:x for x in rows};frames=json.loads((b/'review_current04/capture.json').read_text())['captures'];assert len(frames)==152
for x in d['assets']:
 if x['path'] in byname:
  x['sha256']=byname[x['path']]['sha256']
  if 'fx_invite_' in x['path']:
   x['ratings']['technical']=4.6;x['minimum_scored_dimension']=4.5;x['status']='PASS_LOCAL_AI_STATIC_APPEARANCE_CANDIDATE_MOTION_PENDING';x['observations']='ImageGen clean-matte replacement preserves the same painted pearl/gold hoop and whole-key registration, with contained source-painted glints only in opening. Current04all152GUIstills reviewed, bothaspects: crisp under-pad targets/guard/imp/belt cues, no prior lavender haze. All37P5runtimecutouts now CUTOUT_OK. Prior technical3.5failure/profile/oldnative/derivedfiles retained; fullmotion/full02/external acceptance still pending.'
d['checked_utc']=now;d['evidence_scope']='AI inspection of all152combined Garden/Chef/P5 actual current04Mobile GUIstills via19labeled pages, bothaspects, and two regeneratednative/5derivedwhole invitation pictures plus unchanged other sourceobjects/guide. Staticappearance minimum4.5eachscored dimension only; motion/canonical/device/child/owner remainpending.';d['captures']={'path':'assets_src/imagegen/job_art_boxer_20261019/review_current04/capture.json','sha256':sha(b/'review_current04/capture.json'),'count':152,'receipt_sha256':sha(b/'capture_current04_receipt.json'),'frames':[{'id':x['id'],'path':x['path'],'sha256':sha(r/x['path'])} for x in frames]};write(p,d)
p=s/'review/art_review.json';d=json.loads(p.read_text());d['reconciliation_capture']={'receipt':'assets_src/imagegen/job_art_nursery_20261019/capture_current08_receipt.json','status':'PASS100GUI_NO_SOURCE_DRIFT_ACTUAL_SAVE_UNCHANGED','limits':'Supplementary combined-source machine/GUI evidence. Original all100current06staticvisual review retains its exactsource scope;25NurseryPNGand3sharedpearls are unchanged, latestcombinedcareearlyreturn/beam-exemptionpredicate retainsNurserybehavior. Fullmotion/canonical/device/child/owner not accepted.'};write(p,d)
for folder in [s,b]:
 prompts=json.loads((folder/'prompts.json').read_text());selected={x['source'] for x in json.loads((folder/'runtime_provenance.json').read_text())['records']}
 for x in prompts:
  if folder==b and x['id'] in ['invite_ring','invite_open']:x['disposition']='REJECTED_FINAL_C2_MATTE: genericprofile flags broadfaintoutsidehaze/translucentbody; exactoriginal and earlierderived5files preserved, last2within4aggregatecapcleanmatte sources replace them.'
  elif x['native_path'] in selected:x['disposition']='SELECTED_LOCAL_AI_STATIC_APPEARANCE_CANDIDATE:4.5floor every scored dimension; C2runtimeprofilePASS. Motion/full02/canonical/device/child/owner pending.'
 write(folder/'prompts.json',prompts)
 write(folder/'generation_accounting.json',{'checked_utc':now,'builtin_calls':len(prompts),'reported_elapsed_ms_sum':sum(x['elapsed_ms'] for x in prompts),'selected_native_ids':[x['id'] for x in prompts if x['native_path'] in selected],'rejected_or_retired_ids':[x['id'] for x in prompts if x['native_path'] not in selected],'provider_model_revision':'unexposed','seed':'unexposed','monetary_usage':'unexposed; no paidAPI/CLI used','cleanup_minutes':'not instrumented, no fabricated timing','cap_status':'Nurseryquilt6/6,bottle4/4,hand2/2 reached; Boxerring/open4/4aggregate reached, no further generation in exhausted actions.'})
# License every retained native/diagnostic/capture PNG, including late combined captures.
p=r/'ASSET_LICENSES.md';t=p.read_text(encoding='utf-8');listed={m[1] for m in re.finditer(r'^\| `([^`]+)` \|',t,re.M)};added=0
for folder in [s,b]:
 for x in sorted(folder.rglob('*.png')):
  n=x.relative_to(r).as_posix()
  if n in listed:continue
  t+='\n| `'+n+'` | Project painted source/current exact4.7.2 Mobile review capture or labeled technical sheet; adjacent provenance records bind source roles | Project/source/OpenAI output terms retained | https://openai.com/policies/terms-of-use/ | Non-runtime reference, retained reject or review evidence; exact source rights retained, no pixel/keyframe acceptance. SHA256 '+sha(x)+'. |';listed.add(n);added+=1
p.write_text(t+'\n',encoding='utf-8');print('Licensed',added,'latePNGpaths',flush=True)
# New combined runner; unchanged source CI/deadlines/classifiers, all families pinned.
for old,new in [('windows_native_capture_01.py','windows_native_capture_02.py'),('run_ci_native_capture_01.sh','run_ci_native_capture_02.sh'),('run_full_ci_01.py','run_full_ci_02.py')]:
 p=v/new;assert not p.exists();txt=(v/old).read_text(encoding='utf-8').replace('native_capture_01','native_capture_02');
 if old.startswith('run_full'):
  txt=txt.replace("['job-art-teacher-20261018','job-art-astronaut-20261018']","['job-art-teacher-20261018','job-art-astronaut-20261018','job-art-chef-20261019','artwork-quality-20261018']")
  anchor='pins = {p.relative_to(root).as_posix(): sha(p) for p in sources}';assert anchor in txt;txt=txt.replace(anchor,"sources += [root/'tools/prepare_opera_minigame_art.py',root/'tools/tests/test_prepare_opera_minigame_art.py']\n"+anchor)
 p.write_text(txt,encoding='utf-8')
for n in ['full_ci_native_capture_02.log','native_capture_02_events.jsonl']:
 p=v/n;assert not p.exists();p.touch()
p=v/'full_ci_native_capture_02.json';assert not p.exists();write(p,{'status':'PENDING','scope':'Combined Garden90FC+ChefEB6+P5cleanmattes+Teacher/Astronaut; unchanged82trustedprobes, exact4.7.2/privatehomes, originaldeadlines/classifiers/noretries, allruntimefamilies pinned.'})
note='CHG-107 combined-source/matte review2026-10-19: original P5local01passes82orderedzeroexitprobes/no source drift (logSHA256150938b1b5c2b9e33c316514daff697d4e4ee7711de9f6f89f80ded4e821f83e). SubsequentC2review flags4sharedringFXforhaze; twoImageGen clean-matte repairs withinring/open4aggregatecap changeonly5PNGkeys, retainoriginal/rejected sources and explicit technical3.5failure. All37newruntimepictures nowCUTOUT_OK. TotalP5calls24(13Nursery/11Boxer). Garden90fc5d56andChefeb6f0de4 are reconciled on the P5topic; source-guarded current08Nursery100/current04Boxer152GUIstills pass, actual desktop saves unchanged. All152newBoxerstills inspected at bothaspects, localAIstatic4.5floor restored for correctedmatte keys. Complete currentcombinedlocal02/exactheadremoteCI and motion/canonical/device/child/owner/finalcampaign acceptance remain pending; lifecycle/master unchanged.'
for name in ['audit/MASTER_AUDIT_2026-08-09.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md']:
 p=r/name;t=p.read_text(encoding='utf-8');assert note not in t;p.write_text(t+'\n'+note+'\n',encoding='utf-8')
commands=[['python','-B','-m','unittest','tools.tests.test_prepare_opera_minigame_art'],['python','-B','tools/prepare_opera_minigame_art.py','--check-only'],['python','-B','tools/audit_document_authority.py'],['python','-B','tools/audit_development.py','--base','auto']]
for i in range(len(commands)):(v/f'pre_full02_gate_{i}.log').touch()
p=r/'design/audit_impacts/job-art-nursery-20261019.json';d=json.loads(p.read_text());d['validation'] += [{'command':'P5sourcefull01 unchanged82trustedprobes, prior matte source','result':'PASS','evidence':'verification/full_ci_native_capture_01.json/log;82zeroexits/0drift3052.192sec SHA256150938b1b5c2b9e33c316514daff697d4e4ee7711de9f6f89f80ded4e821f83e. LaterC2matte defect is separate and notwaived; currentcombined02required.'},{'command':'C2runtimecutout_profile and new152currentBoxerstaticreview after2matteImageGenrepairs','result':'PASS','evidence':'verification/runtime_technical02.json37/37CUTOUT_OK; Boxernative+19current04pagesallinspected, latestreview/art_review.json4.5eachscored dimension. Four original3.5failures/rejects retained; animation/formal/device/owner pending.'},{'command':'Complete combined Garden90FC/ChefEB6/P5/Teacher/Astronautfull82nativecapture02','result':'PENDING','evidence':'verification/full_ci_native_capture_02.json/log, exactcurrentrawsourcepinsallfamilies/no retry/originaldeadlines/classifiers; commit+exactheadremoteCIrequiredbeforeDev.'}]
# Explicit imports/UIDs are technical runtime metadata, generated by approvedimport06.
extra=[]
for name in [x['path'] for folder in [s,b] for x in json.loads((folder/'runtime_provenance.json').read_text())['records']]:
 if (r/(name+'.import')).is_file():extra.append(name+'.import')
for name in ['scripts/nursery_painted_art.gd.uid','scripts/painted_feedback_art.gd.uid']:
 if (r/name).is_file():extra.append(name)
d['files']=sorted(set(d['files']+[p.relative_to(r).as_posix()]+extra+[x.relative_to(r).as_posix() for folder in [s,b] for x in folder.rglob('*') if x.is_file()]));write(p,d)
for i,c in enumerate(commands):
 q=subprocess.run(c,capture_output=True,text=True,encoding='utf-8');(v/f'pre_full02_gate_{i}.log').write_text(q.stdout+q.stderr,encoding='utf-8');print('gate',i,q.returncode,(q.stdout+q.stderr)[-1800:],flush=True);assert q.returncode==0
print('Combinedfull02prepared; sourcefrozen, onlymetadata/evidence may update while fullsuite runs.',flush=True)

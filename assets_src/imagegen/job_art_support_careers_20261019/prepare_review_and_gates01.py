from pathlib import Path
import json,hashlib,re,subprocess
from datetime import datetime,timezone
r=Path.cwd();s=r/'assets_src/imagegen/job_art_support_careers_20261019';v=s/'verification';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Refresh the two render functions changed after current08. Other actual frames remain source-scoped.
p=s/'capture_current09.gd';assert not p.exists();t=(s/'capture_current08.gd').read_text(encoding='utf-8').replace('current08','current09')
anchor='\t\t\tfor phase in range(world.phases.size()):';assert anchor in t
t=t.replace(anchor,anchor+'\n\t\t\t\tvar name := String(world.phases[phase].get("name",""))\n\t\t\t\tif not ((career == "farmer" and name == "PICNIC") or (career == "magician" and name == "CABINET")):\n\t\t\t\t\tcontinue')
p.write_text(t,encoding='utf-8')
p=s/'run_capture.py';t=p.read_text(encoding='utf-8');t=t.replace("'current08']","'current08','current09','current10','current11','current12']");p.write_text(t,encoding='utf-8')
p=s/'review/context_failures04.json';d=json.loads(p.read_text());d['reviewed_pages']=list(range(1,41));d['not_yet_reviewed_pages']=[];p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
# Complete native output/deadline adapter, same CI commands and assertion classifiers.
parent=r/'assets_src/imagegen/job_art_nursery_20261019/verification'
for old,new in [('windows_native_capture_02.py','windows_native_capture_01.py'),('run_full_ci_02.py','run_full_ci_01.py'),('run_ci_native_capture_02.sh','run_ci_native_capture_01.sh')]:
 t=(parent/old).read_text(encoding='utf-8').replace('native_capture_02','native_capture_01')
 if new.endswith('.sh'):
  t=t.replace('art-ci-control-20261018','art-teacher-20261018').replace('job_art_nursery_20261019/verification/windows_native','job_art_support_careers_20261019/verification/windows_native')
 if new.startswith('run_full'):
  t=t.replace("'assets/opera/worlds/nursery_quality_20261019'","'assets/opera/worlds/support_quality_20261019','assets/opera/worlds/nursery_quality_20261019'")
  t=t.replace("'baseline':'e90c0daa83cf05644f0e9942e85c1198ed7901f7'","'baseline':'58339deb6cb25d5793c3623981e66fad5be0858a'")
  t=t.replace('import subprocess, json, hashlib, time, re','import subprocess, json, hashlib, time, re, os')
  t=t.replace("started = datetime.now(timezone.utc).isoformat()", "actual = Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light'\ndef savepins(): return {p.name:sha(p) for p in actual.glob('reef_save*') if p.is_file()}\nbefore = savepins()\nhome = root/'tmp/p6_full01_private'; assert not home.exists()\n(home/'Roaming').mkdir(parents=True); (home/'Local').mkdir()\nenv = os.environ.copy(); env['APPDATA']=str(home/'Roaming'); env['LOCALAPPDATA']=str(home/'Local')\nstarted = datetime.now(timezone.utc).isoformat()")
  t=t.replace('stdout=f,stderr=subprocess.STDOUT)','stdout=f,stderr=subprocess.STDOUT,env=env)')
  t=t.replace("and not drift else 'FAIL'","and not drift and before==savepins() else 'FAIL'")
  t=t.replace("'process_exit':run.returncode,","'process_exit':run.returncode,'actual_save_unchanged':before==savepins(),'actual_desktop_save_sha256_before':before,'actual_desktop_save_sha256_after':savepins(),")
 p=v/new;assert not p.exists();p.write_text(t,encoding='utf-8')
for name in ['full_ci_native_capture_01.log','native_capture_01_events.jsonl']:(v/name).touch(exist_ok=False)
(v/'full_ci_native_capture_01.json').write_text(json.dumps({'status':'PENDING','scope':'P6with green256and documentation-reconciled859parent, sixproductionGD including one stronger asset-binding assertion; unchanged82trustedcommands/deadlines/classifiers, private homes, no retry; actual save hashes and allruntime families pinned.'},indent=2)+'\n',encoding='utf-8')
prompts=json.loads((s/'prompts.json').read_text());records=json.loads((s/'runtime_provenance04.json').read_text())['records'];selected={x['source'] for x in records}
(s/'generation_accounting.json').write_text(json.dumps({'checked_utc':datetime.now(timezone.utc).isoformat(),'builtin_calls':len(prompts),'reported_elapsed_ms_sum':sum(x['elapsed_ms'] for x in prompts),'selected_native_ids':[x['id'] for x in prompts if x['native_path'] in selected],'rejected_or_retired_ids':[x['id'] for x in prompts if x['native_path'] not in selected],'model_revision':'unexposed builtin, userapproved; no2.5claim','seed':'unexposed','paid_usage':'unexposed; no paidAPI/CLI','cleanup_minutes':'not instrumented, no invented timing','caps':'HERD B2/2 exhausted after anatomically rejectedB1; scanner_found2/2,hands_ready2/2,bed2/2,cast1and2each2/2 exhausted. Other cards retained; no further take in exhausted states.'},indent=2)+'\n',encoding='utf-8')
p=r/'ASSET_LICENSES.md';t=p.read_text(encoding='utf-8');listed={m[1] for m in re.finditer(r'^\| `([^`]+)` \|',t,re.M)};added=0
for p in sorted(s.rglob('*.png')):
 name=p.relative_to(r).as_posix()
 if name in listed:continue
 t+='\n| `'+name+'` | Source-bound project cutout, exactMobile capture, retained reject or labeled diagnostic; adjacent source provenance retains all input roles | Project/source rights and OpenAI output terms retained | https://openai.com/policies/terms-of-use/ | Non-runtime evidence/reference; no new art acceptance. SHA256 '+sha(p)+'. |';added+=1
(r/'ASSET_LICENSES.md').write_text(t+'\n',encoding='utf-8')
impact=r/'design/audit_impacts/job-art-support-careers-20261019.json';d=json.loads(impact.read_text());d['scope']+=' Laterreview of all40context pages rejects FarmerPICNICghosting/codedmarkers, TOSSfinishedprojectilefaceocclusion, flatMagicianLamb-a/cabinetfinish/VANISHcodedoverlay and Painterstamp at3.5. Three named builtinImageGen repairs under predeclaredcaps bring59calls/56runtimePNG/C2PASS; all original/native/rejects retained. Whole registeredcabinet key replaces crossfade, originalSeekatlasunchanged. One outdated274-probe binding is explicitly updated from hardcoded old256AtlasTexture to exact new512path/dimension/hash AND exact retained sourceatlas hash, no earning assertion relaxed. Retained native07failure1/274 and native08PASS all274/Opera2D; current08actual238GUIPASS before final two renderfunction changes, freshcurrent09 supplementrequired. Latest parent859a8e09 adds sixRumi handofffiles only to independentlygreen256; no inherited production change.'
production=['scripts/support_career_painted_art.gd','scripts/support_career_painted_art.gd.uid','scripts/opera_gesture_surface.gd','scripts/opera_career_world_2d.gd','scripts/opera_world_hotspot_2d.gd','scripts/opera_world_backdrop_2d.gd','scripts/probe_opera_gesture_quality.gd']
for name in ['pre_full01_parser.log','pre_full01_inference.log','pre_full01_authority.log','pre_full01_development.log','pre_full01_builder_tests.log','pre_full01_builder.log']:(v/name).touch(exist_ok=False)
d['files']=sorted(set(d['files']+production+['ASSET_LICENSES.md']+[x.relative_to(r).as_posix() for x in s.rglob('*') if x.is_file()]+[x.relative_to(r).as_posix() for x in (r/'assets/opera/worlds/support_quality_20261019').glob('*') if x.is_file()]))
d['validation'].append({'command':'P6fresh exact native08focused and current08GUI/sourcepin/save checks','result':'PASS','evidence':'verification/native08.json original274and70phase Opera2D PASS; capture_current08_receipt.json238actualGUIstills/source0drift/actualsaveunchanged. FinalPICNICguide/cabinetwholekey supplement09pending; full82pending. Native07oldbindingfailure retained.'})
impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
commands=[('parser',['python','-B','-m','gdtoolkit.parser',*[n for n in production if n.endswith('.gd')]]),('inference',['python','-B','tools/lint_inference.py',*[n for n in production if n.endswith('.gd')]]),('authority',['python','-B','tools/audit_document_authority.py']),('development',['python','-B','tools/audit_development.py','--base','auto']),('builder_tests',['python','-B','-m','unittest','tools.tests.test_prepare_opera_minigame_art']),('builder',['python','-B','tools/prepare_opera_minigame_art.py','--check-only'])]
for name,command in commands:
 q=subprocess.run(command,capture_output=True,text=True,encoding='utf-8');(v/('pre_full01_'+name+'.log')).write_text(q.stdout+q.stderr,encoding='utf-8');print(name,q.returncode,(q.stdout+q.stderr)[-800:],flush=True);assert q.returncode==0
print('Preparedcoverage/licenses/fullrunner; productionfrozen, finalcontext review and metadata continue. Late capture09files require coverage refresh beforecommit.',len(records),len(prompts),'licensed',added,flush=True)

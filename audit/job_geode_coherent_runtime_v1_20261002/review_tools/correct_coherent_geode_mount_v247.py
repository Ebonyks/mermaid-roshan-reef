from pathlib import Path
import datetime,hashlib,html,json,re,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_coherent_runtime_v1_20261002';prefix=f.relative_to(b).as_posix()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
ci=f/'full_ci_v1';assert (ci/'INTERRUPTION.json').exists()
snap=read(ci/'SOURCE_BEFORE.json')['source_files'];checks=[dict(path=x['path'],before_sha256=x['sha256'],after_sha256=sha(b/x['path']),match=x['sha256']==sha(b/x['path'])) for x in snap];assert len(checks)==367 and all(x['match'] for x in checks)
raw=(ci/'stdout.log').read_text(errors='replace');err=(ci/'stderr.log').read_text(errors='replace')
diag=[dict(stream=name,line=i,text=line) for name,text in [('stdout',raw),('stderr',err)] for i,line in enumerate(text.splitlines(),1) if line.startswith(('ERROR:','WARNING:','SCRIPT ERROR:'))]
write(ci/'ENGINE_DIAGNOSTICS.json',dict(status='PARTIAL_RAW_DIAGNOSTICS_PRESERVED',items=diag))
write(ci/'RECEIPT.json',dict(status='INTERRUPTED_FOR_OBSERVED_MOUNTING_DEFECT_NO_FULL_SUITE_PASS',checked_utc=now,source_checks=checks,source_unchanged=True,probe_results=[dict(probe=p,process_exit=int(c)) for p,c in re.findall(r'^PROBE (\w+) process exit: (\d+)',raw,re.M)],stdout_sha256=sha(ci/'stdout.log'),stderr_sha256=sha(ci/'stderr.log'),raw_diagnostic_count=len(diag),qualification='Only own exact task runner tree stopped, recorded in INTERRUPTION.json. All367 sources unchanged before interruption; no full-suite pass. Later production correction requires new snapshot/run.'))
frames=[];boards=[]
for width in [1280,1600]:
 m=read(f/f'BOARD_MANIFEST_{width}.json')
 for x in m['frames']:
  x=dict(x);assert sha(b/x['path'])==x['sha256'];n=x['index']
  x.update(direct_review=True,native_detail_review=n in [31,32,41,42],owner_acceptance=None,priority=True)
  x['review_method']='Every12 cells on every complete ordered board directly inspected, row-major; frames31/32/41/42 also at native size for both widths.'
  x['scores']=dict(material=4.6,rooted_crystals=4.6,static_state=4.5,opening_mount=4.3,working_contact=2.7 if n<92 else None,clap_transition=4.0 if 92<=n<112 else None,production_return=None)
  x['evaluation']='Seven authored states show two separate stone cavities with crystals rooted inside. Material4.6/static cutout4.5. Actual renderer wrongly inherits centerX=770+pull/2, sliding the whole stone up to50 canvas pixels right through opening; mounting4.3 fails the floor.'
  x['evaluation']+=(' Empty-callback fixture tail does not exercise real production return.' if n>=112 else ' Abrupt working-to-clap transition4.0 remains.' if n>=92 else ' Roshan remains away from the raised object, hands at the floor: contact2.7.')
  frames.append(x)
 for x in m['boards']:
  x=dict(x);assert sha(b/x['path'])==x['sha256'];x.update(direct_review=True);boards.append(x)
assert len(frames)==312 and len(boards)==26
sp=b/'scripts/opera_geology_surface.gd';shutil.copyfile(sp,f/'attempt_01/PRODUCTION_SCRIPT_FAILED.gd')
report=dict(status='REJECTED_ACTUAL_MOUNT4.3',reviewed_utc=now,baseline=read(f/'PLAN.json')['baseline'],production_script=dict(path=prefix+'/attempt_01/PRODUCTION_SCRIPT_FAILED.gd',sha256=sha(sp)),frames=frames,boards=boards,counts=dict(frames=312,boards=26,native_details=8),scores=dict(geode_material=4.6,embedded_crystals=4.6,opening_mount=4.3,contact=2.7,clap_transition=4.0),qualification='Actual production render/input capture. Pilot fixed-center4.5 was not inherited. Incorrect helper reuse exposed by native actual inspection; failed captures/script and interrupted fullsuite preserved. No owner/global/return acceptance.')
write(f/'attempt_01/REVIEW.json',report)
esc=html.escape
bc=''.join('<figure><a href="../../../'+x['path']+'"><img src="../../../'+x['path']+'" alt="'+str(x['width'])+' frames '+str(x['first_frame'])+' to '+str(x['last_frame'])+'"></a><figcaption>'+str(x['width'])+' frames '+str(x['first_frame'])+'–'+str(x['last_frame'])+'; every cell inspected</figcaption></figure>' for x in boards)
fc=''.join('<article><a href="../../../'+x['path']+'">'+str(x['width'])+' frame '+str(x['index'])+'</a><p>'+esc(x['evaluation'])+'</p><small>'+x['sha256']+'</small></article>' for x in frames)
(f/'attempt_01/index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rejected geode mount1</title><style>body{font:17px/1.5 system-ui;background:#eef4fa;color:#25304a;margin:0}main{max-width:1460px;margin:auto;padding:24px}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,600px),1fr));gap:16px}figure,article{background:white;padding:14px;border-radius:12px;margin:0;min-width:0}img{width:100%}small{overflow-wrap:anywhere}.frames{grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}</style><main><h1>Rejected actual geode mount —4.3/5</h1><p>The legacy pair helper shifts the entire geode up to50 canvas pixels during the pull. Every312 actual frames was inspected on26 boards plus8 native details. Crystals remain embedded4.6; material4.6, remote contact2.7 and clap transition4.0 retain separate opinions.</p><p>The in-progress full suite was interrupted before source correction; no complete-suite pass. Exact failed script, all frames and raw logs remain preserved.</p><a href="REVIEW.json">Individual evaluations and hashes</a><section>'+bc+'</section><h2>Every frame evaluation</h2><section class="frames">'+fc+'</section></main></html>',encoding='utf-8',newline='\n')
ip=b/'design/audit_impacts/job-geode-coherent-runtime-20261002.json';d=read(ip)
d['scope']+=' Actual capture1 exposed50px center drift from inherited _geode_pair_rect; preserve failed312-frame review4.3 and interrupted unmodified fullCI1. Correct that geometry helper to fixed center only, then newactual capture2 and freshCI2. All other behavior remains unchanged.'
d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()})
d['validation'].append(dict(command='Direct every312 actual capture1 frames plus8 native thresholds',result='FAIL',evidence=prefix+'/attempt_01/REVIEW.json: object mount4.3 due50px inherited center shift; embedded/material4.6 separate.'))
write(ip,d)
old=sp.read_text();needle='GEODE_RECT.get_center().x + geode_pull * 0.5';assert old.count(needle)==1
new=old.replace(needle,'GEODE_RECT.get_center().x');sp.write_text(new,encoding='utf-8',newline='\n')
write(f/'CURRENT_BINDING_V2.json',dict(status='FIXED_CENTER_PRODUCTION_CAPTURE2_REVIEW_PENDING',previous_failed_script=prefix+'/attempt_01/PRODUCTION_SCRIPT_FAILED.gd',before_sha256=hashlib.sha256(old.encode()).hexdigest(),after_sha256=sha(sp),changed_method='_geode_pair_rect',center_x=770,base_y=515,qualification='One render-geometry correction only; no texture regeneration or pixel repair. Rejected actual mounting4.3 retained; source/pilot scores not inherited.'))
s=(f/'capture.gd').read_text().replace('/attempt_01','/attempt_02');(f/'capture_v2.gd').write_text(s,encoding='utf-8',newline='\n')
s=(f/'review_tools/run_coherent_runtime_gates_v245.py').read_text().replace(prefix+'/capture.gd',prefix+'/capture_v2.gd').replace('run_coherent_runtime_gates_v245.py','run_coherent_runtime_gates_v247.py').replace("'_v236'","'_v247'")
(f/'review_tools/run_coherent_runtime_gates_v247.py').write_text(s,encoding='utf-8',newline='\n')
s=(f/'review_tools/run_coherent_geode_full_ci_v245.py').read_text().replace("folder=family/'full_ci_v1'","folder=family/'full_ci_v2'").replace(prefix+'/full_ci_v1/process.exit',prefix+'/full_ci_v2/process.exit').replace("paths.add('"+prefix+"/capture.gd')","paths.add('"+prefix+"/capture.gd')\n paths.add('"+prefix+"/capture_v2.gd')").replace('coherent-geode production full suite1','coherent-geode production full suite2')
(f/'review_tools/run_coherent_geode_full_ci_v247.py').write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
lp=b/'ASSET_LICENSES.md';s=lp.read_text()+'\n### Preserved rejected actual geode mounting attempt1 (2026-10-02)\n\n';bt=chr(96)
for x in frames+boards:
 if x['path'] not in s:s+='| '+bt+x['path']+bt+' | Godot4.7.2 Mobile review capture of licensed project art | Project review evidence | '+bt+prefix+'/attempt_01/REVIEW.json'+bt+' | '+('Ordered12 native-frame board by uniform whole-canvas ffmpeg scale/tiling' if 'first_frame' in x else 'Exact native losslessWebP capture')+'; failed mounting4.3 retained; SHA256 '+x['sha256']+' |\n'
lp.write_text(s,encoding='utf-8',newline='\n')
d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d)
print('Failed actual312/26/8 mounting4.3 and interruptedCI retained. Fixed geode center; actual capture2/fullCI2 pending.')

from pathlib import Path
import datetime,hashlib,json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geology_room_route_v1_20261002';prefix=f.relative_to(b).as_posix()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert read(f/'runtime_gate/capture1280v1.receipt.json')['status']=='FAIL_PRESERVED'
snap=read(b/'audit/job_geode_coherent_runtime_v1_20261002/full_ci_v2/SOURCE_BEFORE.json')['source_files'];assert len(snap)==368 and all(sha(b/x['path'])==x['sha256'] for x in snap)
failure=dict(status='FAILED_ENTRY_FIXTURE_NO_ROUTE_PASS',recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),fixture=prefix+'/capture.gd',sha256=sha(f/'capture.gd'),receipt=prefix+'/runtime_gate/capture1280v1.receipt.json',own_process_stopped=dict(pid=21444,parent_pid=36636,executable='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe',reason='Assertion-stopped coroutine; only exact route-capture process killed after Cim executable/arguments verification.'),cause='Entry fixture omitted normal g.t initialization used by the trusted room probe and touched the job while its entrance fade could still block input. These fixture mistakes do not establish production defects.',preserved_images=[dict(path=p.relative_to(b).as_posix(),sha256=sha(p),direct_review=False,score=None) for p in (f/'attempt_01').rglob('*.webp')])
write(f/'FAILED_ENTRY_ATTEMPT_01.json',failure)
s=(f/'capture.gd').read_text(encoding='utf-8').replace('/attempt_01/','/attempt_02/')
s=s.replace('main.game = "level2"\n\tmain._enter_castle_interior_now(false)','main.game = "level2"\n\tmain.g["t"] = 0.0\n\tmain._enter_castle_interior_now(false)')
needle='assert(main.opera_game != null and main.opera_game.act != null)\n\tvar world:'
s=s.replace(needle,'assert(main.opera_game != null and main.opera_game.act != null)\n\tfor tick: int in range(180):\n\t\tif main.fade_rect == null or main.fade_rect.modulate.a <= 0.02:\n\t\t\tbreak\n\t\tawait _wait(1)\n\tassert(main.fade_rect == null or main.fade_rect.modulate.a <= 0.02)\n\tawait _wait(8)\n\tvar world:')
(f/'capture_v2.gd').write_text(s,encoding='utf-8',newline='\n')
s=(f/'review_tools/run_geology_room_gates_v251.py').read_text().replace(prefix+'/capture.gd',prefix+'/capture_v2.gd').replace('run_geology_room_gates_v251.py','run_geology_room_gates_v252.py').replace('_v251','_v252')
(f/'review_tools/run_geology_room_gates_v252.py').write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geology-room-route-review-20261002.json';d=read(ip);d['scope']+=' Preserve failed entry1 and its raw errors/images; correct only new non-runtime fixture entry timer and wait for normal entrance fade before touch. No production defect inferred from fixture omission.';d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d)
print('Preserved failed entry1; corrected fixture timer and fade readiness only; all368 production/currentCI sources unchanged.')

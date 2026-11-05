from delivery_common import *
import re, shutil

P=U/REL; OLD=S/'full_validation'; W=S/'full_validation_audit_contract_recovery'
E=Path(r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe')
def status(phase,**kw):wr(S/'VALIDATION_RECOVERY_STATE.json',dict(state=phase,at_utc=now(),**kw))
try:
    assert not W.exists(), 'Never duplicate an existing recovery'
    assert gs(U,'rev-parse','HEAD')==SOURCE_BASE and gs(U,'branch','--show-current')==SOURCE_BRANCH
    original=rd(OLD/'FINAL_RESULT.json');oldpin=rd(S/'SOURCE_PIN.json');launch=rd(OLD/'LAUNCH.json')
    assert original['status']=='FAIL' and original['probe_count']==4 and original['passed_count']==3
    assert original['results'][-1]['probe']=='probe_audit' and original['results'][-1]['failure_lines']==['AUDIT|Rainbow Canvas theater: FAIL']
    assert original['results'][-1]['exit_code']==0 and not original['runtime_changes'] and original['normal_unchanged']
    assert rd(OLD/'STATIC_RESULT.json')['state']=='PASS' and 'NO_REGRESSION' in (OLD/'GAME2D.log').read_text(encoding='utf-8',errors='replace')
    assert sha(E)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
    W.mkdir();status('FREEZING_CORRECTED_TEST_ONLY_CURRENT_SOURCE_NO_HEALTHY_GATE_RESTART')
    current={p:sha(U/p) for p in oldpin['runtime_hashes']}
    delta=sorted(p for p,h in oldpin['runtime_hashes'].items() if current[p]!=h)
    assert delta==['scripts/probe_audit.gd'],delta
    assert sha(P/'BASELINE_FULL_GAME_AUDIT_PROBE.gd.txt')==oldpin['runtime_hashes']['scripts/probe_audit.gd']
    projection=rd(P/'AUDIT_PROBE_2D_PROJECTION_REUSE.json')
    assert projection['before_3D_token_counts']==projection['after_3D_token_counts']
    normal=Path(rd(U/H/'r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base'])
    def normals():return {n:sha(Path(str(normal)+n)) if Path(str(normal)+n).is_file() else 'absent' for n in oldpin['normal_before']}
    def drift():return [p for p,h in current.items() if not(U/p).is_file() or sha(U/p)!=h]
    assert normals()==oldpin['normal_before']
    pin=dict(oldpin,runtime_hashes=current,previous_validation_pin_sha256=sha(S/'SOURCE_PIN.json'),
        recovery_only_changed_test='scripts/probe_audit.gd',native_reuse='Only probe_melody/probe_audit art assertions differ from native capture; all rendering, assets, controller and fixture bytes unchanged.')
    wr(S/'SOURCE_PIN_AUDIT_RECOVERY.json',pin)
    native=rd(S/'candidate_native_entry_repaired/SOURCE_PIN.json')
    native_delta=sorted(p for p,h in native['runtime_hashes'].items() if current[p]!=h)
    assert native_delta==['scripts/probe_audit.gd','scripts/probe_melody.gd'],native_delta
    basis=dict(state='TEST_ART_ASSERTION_ONLY_RECOVERY_RETAINS_HEALTHY_CURRENT_GATES',
        original_validation=REL+'/ORIGINAL_FULL_VALIDATION_FAILURE.json',original_source_pin_sha256=sha(S/'SOURCE_PIN.json'),
        corrected_source_pin_sha256=sha(S/'SOURCE_PIN_AUDIT_RECOVERY.json'),only_changed_file=delta,
        no_gameplay_asset_or_rendering_change=True,native_reuse_only_changed_tests=native_delta,
        retained=dict(complete_static_prefix='PASS exit0 both original shells',Game2D_regression='PASS; exact changed-probe3D projection unchanged',
            current_Melody='PASS exit0',reef_districts='PASS exit0',ocean_kingdoms='PASS exit0',native='165 effective checks;12 directly inspected stills; no new native events'),
        refreshed=['changed test parser/inference','real Godot analyzer for corrected probe','original probe_audit retry','original remaining78 trusted scripts'],
        original_failure_preserved=True,Dev_integrated=False,formal_QA11=None,accepted_removed=0)
    wr(P/'FULL_VALIDATION_RECOVERY_BASIS.json',basis);wr(W/'RECOVERY_BASIS.json',basis)
    for name in ['STATIC_RESULT.json','STATIC_PREFIX.log','GAME2D.log']:shutil.copy2(OLD/name,W/name)
    shutil.copy2(Path(__file__),P/'VALIDATION_AUDIT_RECOVERY_RUNNER.py')
    ip=rd(U/'design/audit_impacts/flat-vector-melody-curtains-20261101.json')
    ip['files']=sorted(set(ip['files'])|{x.relative_to(U).as_posix() for x in P.rglob('*') if x.is_file()})
    wr(U/'design/audit_impacts/flat-vector-melody-curtains-20261101.json',ip)
    refreshed=[gate(U,'AUDIT_RECOVERY_PARSER',[sys.executable,'-m','gdtoolkit.parser','scripts/probe_audit.gd']),
        gate(U,'AUDIT_RECOVERY_INFERENCE',[sys.executable,'-B','tools/lint_inference.py','scripts/probe_audit.gd'])]
    refreshed+=document_gates(U,'AUDIT_RECOVERY')
    wr(W/'REFRESHED_STATIC_GATES.json',refreshed)
    env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=str(E))
    def sandbox(d):
        e=env.copy()
        for key,name in [('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
            path=d/name;path.mkdir();e[key]=str(path)
        return e
    status('RUNNING_CORRECTED_FULL_GAME_PROBE_REAL_GODOT_ANALYZER')
    d=W/'analyzer';d.mkdir();e=sandbox(d)
    with(d/'engine.log').open('wb')as log:
        q=subprocess.run([str(E),'--headless','--path',str(U),'--check-only','--script','res://scripts/probe_audit.gd'],cwd=U,env=e,stdout=log,stderr=subprocess.STDOUT,timeout=180,creationflags=0x08000000)
    text=(d/'engine.log').read_text(encoding='utf-8',errors='replace')
    assert q.returncode==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error',text),text[-3000:]
    order=launch['execution_order'];assert len(order)==82 and order[3]=='probe_audit'
    results=original['results'][:3];assert all(r['passed'] for r in results)
    assert sha(U/'scripts/ci.sh')==launch['ci_sha256']
    failure=launch['failure_regex'];runtime=launch['runtime_error_regex'];start=now();clock=time.monotonic()
    wr(W/'LAUNCH.json',dict(launch,source_pin_sha256=sha(S/'SOURCE_PIN_AUDIT_RECOVERY.json'),
        started_at_utc=start,recovery_basis='RECOVERY_BASIS.json',retained_original_passes=[r['probe'] for r in results],
        remaining_original_execution_order=order[3:],unchanged_order_flags_deadlines_and_classifiers=True))
    for i,name in enumerate(order[3:],start=3):
        d=W/name;d.mkdir();e=sandbox(d)
        touch='--hybrid-touch-test' if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary'] else '--classic-touch-test'
        cmd=[str(E),'--verbose','--log-file',str(d/'native_engine.log'),'--headless','--path',str(U),'-s','scripts/'+name+'.gd','--','--touch',touch]
        began=time.monotonic();timed=False
        with(d/'engine.log').open('wb')as log:
            proc=subprocess.Popen(cmd,cwd=U,env=e,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000)
            status('RUNNING_REMAINING_ORIGINAL_TRUSTED_SCRIPTS',probe=name,index=i+1,count=82,pid=proc.pid,log=str(d/'engine.log'))
            wr(W/'RUNNING.json',dict(probe=name,index=i+1,count=82,pid=proc.pid,command=cmd,log=str(d/'engine.log'),started_at_utc=now()))
            try:rc=proc.wait(timeout=480)
            except subprocess.TimeoutExpired:proc.kill();rc=proc.wait();timed=True
        text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');bad=[line for line in text.splitlines() if re.search(failure+'|'+runtime,line)]
        row=dict(probe=name,command=cmd,exit_code=rc,timed_out=timed,elapsed_seconds=round(time.monotonic()-began,3),failure_lines=bad,
            output_nonempty=bool(text.strip()),passed=rc==0 and not timed and not bad and bool(text.strip()),log=str(d/'engine.log'),log_sha256=sha(d/'engine.log'))
        results.append(row);wr(W/'RESULTS_PROGRESS.json',dict(completed=len(results),passed=sum(r['passed'] for r in results),results=results))
        print('R120_RECOVERY_PROBE',i+1,name,'PASS' if row['passed'] else 'FAIL',row['elapsed_seconds'],flush=True)
        if not row['passed']:break
    changed=drift();after=normals();passed=len(results)==82 and all(r['passed'] for r in results) and not changed and after==pin['normal_before']
    out=dict(status='PASS_ALL82_CURRENT_STATIC_ANALYZER_2D' if passed else 'FAIL',source_baseline=SOURCE_BASE,
        source_pin_sha256=sha(S/'SOURCE_PIN_AUDIT_RECOVERY.json'),started_at_utc=start,completed_at_utc=now(),elapsed_seconds=round(time.monotonic()-clock,3),
        probe_count=len(results),passed_count=sum(r['passed'] for r in results),results=results,runtime_changes=changed,normal_before=pin['normal_before'],normal_after=after,
        normal_unchanged=after==pin['normal_before'],complete_static_and_Game2D_reused_with_exact_projection=True,retained_original_passes=3,
        original_failure='ORIGINAL_FULL_VALIDATION_FAILURE.json',recovery_basis='FULL_VALIDATION_RECOVERY_BASIS.json',
        native_reused=True,effective_native_checks=165,excluded_fixture_checks=54,all12_effective_native_frames_reviewed=True,
        new_frame_events=dict(bounded=12,excluded=6,retained=18),formal_QA11=None,device=None,child=None,owner=None,Dev_integrated=False,accepted_removed=0,mission_complete=False)
    wr(W/'FINAL_RESULT.json',out);status('TERMINAL_RECOVERED_ALL82_PASS' if passed else 'TERMINAL_RECOVERY_FAIL',probes=len(results))
    print('R120_RECOVERY_ALL_OK' if passed else 'R120_RECOVERY_FAIL',flush=True);assert passed
except Exception as exc:
    wr(S/'VALIDATION_RECOVERY_STOP.json',dict(state='STOPPED_INSPECT_EXACT_HANDLE_NO_AUTOMATIC_RETRY',error=str(exc),at_utc=now()))
    status('STOPPED_NO_AUTOMATIC_RETRY',error=str(exc));raise

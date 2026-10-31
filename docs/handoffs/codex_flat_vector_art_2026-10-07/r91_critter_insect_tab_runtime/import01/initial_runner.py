from pathlib import Path
import json,hashlib,subprocess,os,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
Q=Path.cwd();S=Path(__file__).parent;P=Q/'docs/handoffs/codex_flat_vector_art_2026-10-07/r91_critter_insect_tab_runtime';R=Path('C:/Users/Peter/.codex/worktrees/flat-vector-r6-20261012/mermaid-roshan-reef')
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=rd(Q/'docs/handoffs/codex_flat_vector_art_2026-10-07/r88_critter_book_runtime/CANDIDATE_SOURCE_PIN.json');paths=list(old['runtime_hashes']);side=list(old['sidecars']);assert all((Q/x).is_file()for x in set(paths)|set(side))
g=subprocess.check_output(['python','-B','tools/resolve_godot.py'],cwd=Q,text=True).strip();version=subprocess.check_output([g,'--version'],cwd=Q,text=True).strip();assert version.startswith('4.7.2.stable.official.ed1daf0bf');assert sha(Path(g))=='c8f0a6bc45a19b33541501e57f6f7cd972ab18453743266339d495cbbe846643'
pre={'baseline':'d5e63a1ec6e79745da504ee3c3945e59ae35ea79','runtime_hashes':{x:sha(Q/x)for x in paths},'sidecars':{x:sha(Q/x)for x in side},'scope':'Fresh Q measurement after single tab edit; no copied R88 raw hashes.'};wr(S/'SOURCE_PRE_IMPORT_PIN.json',pre)
record=rd(R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r77_intro_entry_ownership/USERDIR_PREFLIGHT.json');normal=Path(json.loads(next(x['output']for x in record['checks']if 'R77_USERDIR_PREFLIGHT|'in x['output']).split('R77_USERDIR_PREFLIGHT|',1)[1].strip())['normal_path']);suffixes=['','.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.tmp','.before_new_game.old']
def normals():return {x:sha(Path(str(normal)+x))if Path(str(normal)+x).is_file()else 'absent'for x in suffixes}
before=normals();job=S/'import01';job.mkdir(exist_ok=False);env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
for key,sub in [('APPDATA','roaming'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:env[key]=str(job/sub);Path(env[key]).mkdir()
cmd=[g,'--headless','--path',str(Q),'--rendering-method','mobile','--editor','--import','--quit','--verbose'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();wr(S/'IMPORT_LAUNCH.json',{'command':cmd,'engine_version':version,'normal_before':before,'started_at_utc':start,'scope':'Isolated headless import only, no gameplay or visual acceptance.'});print('R91_IMPORT_STARTED',version,flush=True)
with(S/'IMPORT01.log').open('wb')as log:
 proc=subprocess.Popen(cmd,cwd=Q,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000);wr(S/'IMPORT_PROCESS.json',{'pid':proc.pid,'command':cmd,'started_at_utc':start});exit_code=proc.wait()
changes={k:[x for x,v in pre[k].items()if not(Q/x).is_file()or sha(Q/x)!=v]for k in ['runtime_hashes','sidecars']};after=normals();wr(S/'IMPORT_RESULT.json',{'exit_code':exit_code,'source_changes':changes,'normal_before':before,'normal_after':after,'log_sha256':sha(S/'IMPORT01.log'),'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});assert exit_code==0 and not any(changes.values())and before==after,changes
pre['scope']='Fresh postimport R91 candidate raw source/sidecars; only one authorized tab code change from sourceF. No formalQA11/device/child/owner acceptance.';pre['changed_from_baseline']=['scripts/collection_system.gd'];wr(S/'SOURCE_POST_IMPORT_PIN.json',pre);wr(P/'CANDIDATE_SOURCE_PIN.json',pre)
checks=[]
for i,c in enumerate([['python','-B','-m','gdtoolkit.parser','scripts/collection_system.gd'],['python','-B','tools/lint_inference.py','scripts/collection_system.gd'],[g,'--headless','--path',str(Q),'--check-only','--script','res://scripts/collection_system.gd']]):
 z=subprocess.run(c,cwd=Q,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,creationflags=0x08000000);(S/('ANALYZER_'+str(i)+'.log')).write_bytes(z.stdout);checks.append({'command':c,'exit_code':z.returncode,'sha256':hashlib.sha256(z.stdout).hexdigest(),'output':z.stdout.decode(errors='replace')});assert z.returncode==0,checks[-1]
wr(P/'ANALYZER.json',{'checks':checks,'candidate_pin_sha256':sha(P/'CANDIDATE_SOURCE_PIN.json'),'normal_before':before,'normal_after':normals(),'runtime_source_changes':[x for x,v in pre['runtime_hashes'].items()if sha(Q/x)!=v],'sidecar_changes':[x for x,v in pre['sidecars'].items()if sha(Q/x)!=v]});assert normals()==before
print('R91_IMPORT_AND_ANALYZER_PASS_ZERO_SOURCE_SIDECAR_NORMAL_DRIFT',flush=True)
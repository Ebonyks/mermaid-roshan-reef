from pathlib import Path
import subprocess,os,json,hashlib,datetime,time,re
T=Path.cwd();S=Path(os.environ.get('R91_JOB_ROOT',str(Path(__file__).parent)));P=T/'docs/handoffs/codex_flat_vector_art_2026-10-07/r91_critter_insect_tab_runtime';A=Path('C:/Users/Peter/.codex/worktrees/flat-vector-r6-20261012/mermaid-roshan-reef');H=A/'docs/handoffs/codex_flat_vector_art_2026-10-07'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
pin=json.loads((P/'CANDIDATE_SOURCE_PIN.json').read_text(encoding="utf-8-sig"));assert pin['changed_from_baseline']==['assets/mg/butterfly.png.import','scripts/collection_system.gd']
assert all(sha(T/p)==v for p,v in pin['runtime_hashes'].items())and all(sha(T/p)==v for p,v in pin['sidecars'].items())
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==pin['baseline']
G=subprocess.check_output(['python','-B','tools/resolve_godot.py'],text=True).strip()
pre=json.loads((H/'r77_intro_entry_ownership/USERDIR_PREFLIGHT.json').read_text(encoding="utf-8-sig"));normal=Path(json.loads(next(x['output']for x in pre['checks']if'R77_USERDIR_PREFLIGHT|'in x['output']).split('R77_USERDIR_PREFLIGHT|',1)[1].strip())['normal_path'])
def normals():return {x:sha(Path(str(normal)+x))if Path(str(normal)+x).is_file()else'absent'for x in ['','.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.tmp','.before_new_game.old']}
owned=S/'ci_temp';owned.mkdir(exist_ok=False);logfile=S/'FULL_CI.log';assert not logfile.exists();before=normals();start=time.monotonic();ci_hash=sha(T/'scripts/ci.sh')
script='''set -eu
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
export TMPDIR="$(cygpath -u "$R91_TMPROOT")"
export R91_CANON_TMP="$(realpath "$TMPDIR")"
rm() {
  if [ "$#" -ne 2 ] || [ "$1" != "-rf" ]; then echo "R86 cleanup shape rejected" >&2; return 98; fi
  local resolved
  resolved="$(realpath "$2")" || return 98
  case "$resolved" in "$R91_CANON_TMP"/*) command rm -rf -- "$resolved";; *) echo "R86 cleanup outside owned temp rejected" >&2; return 98;; esac
}
export -f rm
bash scripts/ci.sh
'''
env=dict(os.environ,R91_TMPROOT=str(owned),PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=G)
for key,sub in [('APPDATA','roaming'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:env[key]=str(owned/sub);Path(env[key]).mkdir()
cmd=['C:/Program Files/Git/bin/bash.exe','--noprofile','--norc','-c',script]
wr(S/'FULL_CI_LAUNCH.json',{'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'engine':G,'engine_sha256':sha(Path(G)),'ci_script_sha256':ci_hash,'runtime_pin_sha256':sha(P/'CANDIDATE_SOURCE_PIN.json'),'normal_before':before,'isolation':'Unmodified scripts/ci.sh, private pre-engine APPDATA/XDG and stock per-probe namespaces; verified owned TMPDIR cleanup. No gate or probe modifications.','scope':'One insect-tab leaf, code plus mip metadata; no new PNGpixels. Machine lane only; formal QA11, integration and device/child/owner remain separate.'})
print('R91_FULL_CI_STARTED',str(logfile),flush=True)
with logfile.open('wb')as log:q=subprocess.run(cmd,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,env=env,cwd=T,creationflags=0x08000000)
data=logfile.read_bytes();text=data.decode(errors='replace');exits=re.findall(r'^PROBE (\S+) process exit: (\d+)',text,re.M)
runtime_changes=[p for p,v in pin['runtime_hashes'].items()if not(T/p).is_file()or sha(T/p)!=v];sidecar_changes=[p for p,v in pin['sidecars'].items()if not(T/p).is_file()or sha(T/p)!=v]
out={'exit_code':q.returncode,'elapsed_seconds':round(time.monotonic()-start,3),'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'log_sha256':hashlib.sha256(data).hexdigest(),'probe_exits':[{'probe':p,'exit_code':int(c)}for p,c in exits],'probe_count':len(exits),'nonzero_probe_count':sum(int(c)!=0 for p,c in exits),'normal_before':before,'normal_after':normals(),'normal_unchanged':before==normals(),'runtime_source_changes':runtime_changes,'sidecar_changes':sidecar_changes,'ci_script_unchanged':sha(T/'scripts/ci.sh')==ci_hash,'scope':'Unmodified full local trusted CI. Machine evidence only; no formal QA11, target-device, child or owner acceptance or game-wide closure.'}
wr(S/'FULL_CI_RESULT.json',out);print('R91_FULL_CI_FINISHED',q.returncode,'probes',len(exits),'seconds',out['elapsed_seconds'],flush=True)
assert q.returncode==0 and len(exits)==82 and not out['nonzero_probe_count']and out['normal_unchanged']and not runtime_changes and not sidecar_changes and out['ci_script_unchanged'],text[-5000:]

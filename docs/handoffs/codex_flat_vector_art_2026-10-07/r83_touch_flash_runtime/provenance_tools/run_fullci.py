from pathlib import Path
import subprocess,os,json,hashlib,datetime,time,re
T=Path.cwd(); S=Path(__file__).parent; R=Path('C:/Users/Peter/.codex/worktrees/flat-vector-r6-20261012/mermaid-roshan-reef'); H=R/'docs/handoffs/codex_flat_vector_art_2026-10-07'
G=subprocess.check_output(['python','-B','tools/resolve_godot.py'],text=True).strip()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,d): p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
pre=json.loads((H/'r77_intro_entry_ownership/USERDIR_PREFLIGHT.json').read_text(encoding='utf-8'))
native=json.loads(next(x['output'] for x in pre['checks'] if 'R77_USERDIR_PREFLIGHT|'in x['output']).split('R77_USERDIR_PREFLIGHT|',1)[1].strip()); normal=Path(native['normal_path'])
def normals():return {x:sha(Path(str(normal)+x)) if Path(str(normal)+x).is_file() else 'absent' for x in ['', '.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.tmp','.before_new_game.old']}
base=json.loads((H/'r75_tree_book_registration/RUNTIME_BYTE_BASELINE.json').read_text(encoding='utf-8'))
raw={p:sha(T/p) for p in base['runtime_raw_hashes']}; dif=[p for p,v in raw.items() if v!=base['runtime_raw_hashes'][p]]; assert dif==['scripts/touch_ui.gd'],dif
owned=S/'ci_temp'; owned.mkdir(exist_ok=False); logfile=S/'FULL_CI.log'; assert not logfile.exists()
before=normals(); start=time.monotonic(); wr(S/'SOURCE_PIN.json',{'baseline':'dd799b2d43871b29d1d6e0503646308a194dad1e','runtime_file_count':len(raw),'runtime_hashes':raw,'changed_from_baseline':dif,'ci_script_sha256':sha(T/'scripts/ci.sh'),'normal_save_hashes_before':before})
# An exported rm function verifies each computed CI cleanup target remains in
# this job's owned temporary root before delegating to the stock rm binary.
script='''set -eu
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
export TMPDIR="$(cygpath -u "$R83_TMPROOT")"
export R83_CANON_TMP="$(realpath "$TMPDIR")"
rm() {
  if [ "$#" -ne 2 ] || [ "$1" != "-rf" ]; then echo "R83 cleanup shape rejected" >&2; return 98; fi
  local resolved
  resolved="$(realpath "$2")" || return 98
  case "$resolved" in "$R83_CANON_TMP"/*) command rm -rf -- "$resolved";; *) echo "R83 cleanup outside owned temp rejected" >&2; return 98;; esac
}
export -f rm
bash scripts/ci.sh
'''
env=dict(os.environ,R83_TMPROOT=str(owned),PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
cmd=['C:/Program Files/Git/bin/bash.exe','--noprofile','--norc','-c',script]
wr(S/'FULL_CI_LAUNCH.json',{'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'engine':G,'script_sha256':sha(T/'scripts/ci.sh'),'source_pin':'SOURCE_PIN.json','normal_before':before,'isolation':'Stock per-probe APPDATA/LOCALAPPDATA/XDG plus verified owned TMPDIR cleanup; no probe or gate modification.'})
print('R83_FULL_CI_STARTED',str(logfile),flush=True)
with logfile.open('wb')as log: q=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,env=env,cwd=T,creationflags=0x08000000)
data=logfile.read_bytes(); s=data.decode(errors='replace'); exits=re.findall(r'^PROBE (\S+) process exit: (\d+)',s,re.M)
out={'exit_code':q.returncode,'elapsed_seconds':round(time.monotonic()-start,3),'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'log_sha256':hashlib.sha256(data).hexdigest(),'probe_exits':[{'probe':p,'exit_code':int(c)}for p,c in exits],'probe_count':len(exits),'nonzero_probe_count':sum(int(c)!=0 for p,c in exits),'normal_before':before,'normal_after':normals(),'normal_unchanged':before==normals(),'runtime_source_unchanged':all(sha(T/p)==v for p,v in raw.items()),'ci_script_unchanged':sha(T/'scripts/ci.sh')==json.loads((S/'SOURCE_PIN.json').read_text())['ci_script_sha256'],'scope':'Unchanged full local trusted CI; machine lane only. No device/child/owner/QA11 or visual acceptance.'}
wr(S/'FULL_CI_RESULT.json',out);print('R83_FULL_CI_FINISHED',q.returncode,'probes',len(exits),'seconds',out['elapsed_seconds'],flush=True)
assert q.returncode==0 and len(exits)==82 and not out['nonzero_probe_count'] and out['normal_unchanged'] and out['runtime_source_unchanged'] and out['ci_script_unchanged'],s[-6000:]

"""Run canonical CI, or resume its recorded coverage checkpoint without changing gates."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parents[1];REPO=R.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 source=REPO/'scripts/ci.sh';canonical=source.read_bytes().replace(b'\r\n',b'\n');resume='--resume-at-coverage' in sys.argv;helper=REPO/('tmp/native_costume_ci_resume.sh' if resume else 'tmp/native_costume_full_ci.sh')
 if resume:
  marker=b'python3 tools/audit_development.py --base auto';expected=canonical[:canonical.index(b'export GODOT\n')+len(b'export GODOT\n')]+canonical[canonical.index(marker):]
  checkpoint=json.loads((R/'evidence/project_ci_checkpoint.json').read_text());assert checkpoint['source_ci_sha256']==sha(source)
 else:expected=canonical
 assert helper.read_bytes()==expected,'Canonical CI command drift'
 env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe')
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();command=['C:/Program Files/Git/bin/bash.exe','-c','export PATH="$PWD/tmp/native_costume_ci_bin:$PATH"; exec bash '+helper.relative_to(REPO).as_posix()]
 with (R/'evidence/project_ci.log').open('wb') as out,(R/'evidence/project_ci.err').open('wb') as err:result=subprocess.run(command,cwd=REPO,env=env,stdout=out,stderr=err,timeout=14400,creationflags=subprocess.CREATE_NO_WINDOW)
 record={'exit':result.returncode,'resumed_at_coverage':resume,'checkpoint':'project_ci_checkpoint.json' if resume else None,'single_uninterrupted_full_run_pass':not resume and result.returncode==0,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':command,'source_ci_sha256':sha(source),'executed_lf_helper_sha256':sha(helper),'canonical_commands_classifiers_deadlines_unchanged':True,'scope':'Complete canonical scripts/ci.sh gates across recorded prefix plus coverage resume, or a full standalone run. Direct stdout/stderr files avoid PowerShell NativeCommandError on normal unittest stderr.'}
 (R/'evidence/project_ci_receipt.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');(R/'evidence/project_ci.exit').write_text(str(result.returncode)+'\n');print('FULL_PROJECT_CI_EXIT',result.returncode,flush=True);raise SystemExit(result.returncode)
if __name__=='__main__':main()

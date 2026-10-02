from pathlib import Path
import json,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
P=R/'assets_src/local_motion/nursery_connected_scrub_v1_20261002'
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json'
def git(*args,input=None):return subprocess.run(['git',*args],cwd=R,input=input,capture_output=True,check=True).stdout
assert git('rev-parse','HEAD').decode().strip()=='e4e26aeaa1f7e55985cb3915d35dca5aeba00d40'
assert git('branch','--show-current').decode().strip()=='codex/job-art-review-v2-20261001'
target=F/'review_tools'/Path(__file__).name
if Path(__file__).resolve()!=target.resolve():shutil.copyfile(Path(__file__),target)
imp=json.loads(ip.read_text(encoding='utf-8'))
scope=set(imp['files'])|{ip.relative_to(R).as_posix()}
scope|={x.relative_to(R).as_posix() for base in [F,P] for x in base.rglob('*') if x.is_file()}
for x in scope:
    p=R/x
    assert p.resolve().is_relative_to(R.resolve()) and p.is_file(),x
    assert not x.startswith(('.git/','.secrets/','.codex/','.claude/','.github/','assets/book/','assets/audio/voices/','assets/characters/friends/')),x
staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}
assert staged<=scope,'Unrelated staged changes must remain untouched.'
imp['files']=sorted(scope-{ip.relative_to(R).as_posix()})
ip.write_text(json.dumps(imp,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',input=''.join(x+'\0' for x in sorted(scope)).encode())
after={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}
assert after<=scope
print('SCOPED_NURSERY_STAGE|'+str(len(after))+' changed files; '+str(len(scope))+' exact covered paths. Unrelated import changes remain unstaged. No commit/push/acceptance yet.')

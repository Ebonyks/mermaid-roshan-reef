"""Extract the published Codex comparison take and K0 guide from the pinned commit (read-only, via git)."""
import sys,os,subprocess,hashlib,json; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import *
def git_bytes(path):
    return subprocess.run(['git','-C',REPO,'show','%s:%s'%(CODEX_COMMIT,path)],check=True,capture_output=True).stdout
os.makedirs(W('codex'),exist_ok=True)
rec={'commit':CODEX_COMMIT,'files':[]}
for f in range(41):
    b=git_bytes(CODEX_TAKE%f); open(W('codex','%04d.png'%f),'wb').write(b)
    rec['files'].append({'path':CODEX_TAKE%f,'sha256':hashlib.sha256(b).hexdigest()})
b=git_bytes(CODEX_GUIDE0); open(W('codex','guide_0000.png'),'wb').write(b)
rec['guide_0000']={'path':CODEX_GUIDE0,'sha256':hashlib.sha256(b).hexdigest()}
json.dump(rec,open(P('comparison','codex_source.json'),'w'),indent=1)

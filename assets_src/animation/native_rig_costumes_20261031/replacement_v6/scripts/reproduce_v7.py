"""Reproduce current painted cutout outputs without touching live capture inputs."""
from pathlib import Path
import importlib.util,json,hashlib,shutil,datetime
R=Path(__file__).resolve().parents[1];REPO=R.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=REPO/'tmp/native_costume_reproduction_v8'
 if out.exists():raise RuntimeError('Use a fresh reproduction directory; never overwrite prior evidence')
 for n in ['art','godot','review','native']:(out/n).mkdir(parents=True,exist_ok=True)
 for p in (R/'native').glob('*'):
  if p.is_file():shutil.copyfile(p,out/'native'/p.name)
 for theme in ['ballet','magician']:
  for part in ['head','scalp']:shutil.copyfile(R/'art'/f'{theme}_{part}.png',out/'art'/f'{theme}_{part}.png')
 spec=importlib.util.spec_from_file_location('builder',R/'scripts/build_replacements.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 # P and O retain the real immutable source roots. Redirect only builder R,
 # after import, to the disposable asset-output fixture inside this worktree.
 m.R=out;m.main()
 cases=[]
 for p in sorted([*(out/'art').glob('*.png'),*(out/'godot').glob('*.json')]):
  source=R/p.relative_to(out);cases.append({'path':p.relative_to(out).as_posix(),'reproduced_sha256':sha(p),'frozen_sha256':sha(source),'byte_exact':sha(p)==sha(source)})
 frozen=json.loads((R/'evidence/frozen_inputs_v8.json').read_text(encoding='utf-8'));drift=[n for n,h in frozen['files'].items() if sha(REPO/n)!=h]
 report={'pass':bool(cases) and all(x['byte_exact'] for x in cases) and not drift,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':cases,'frozen_input_drift':drift,'method':'Exact frozen builder, same immutable source roots; only output root redirected. No live input mutations.'}
 (R/'evidence/reproduction_v7.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('REPRODUCTION',report['pass'],len(cases));raise SystemExit(0 if report['pass'] else 1)
if __name__=='__main__':main()

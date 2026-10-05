"""Export visible complete keys from named Aseprite tags, with editable-parent hashes."""
from pathlib import Path
import argparse,json,subprocess,hashlib
p=Path(__file__).resolve().parents[1];ap=argparse.ArgumentParser();ap.add_argument('--master',default='inputs/repair_keys.aseprite');ap.add_argument('--output',default='inputs/tagged_exports');a=ap.parse_args()
master=(p/a.master).resolve();out=(p/a.output).resolve()
if not master.is_relative_to(p) or not out.is_relative_to(p):raise SystemExit('Use paths within this source packet; preserve external originals')
out.mkdir(parents=True,exist_ok=True)
subprocess.run([r'C:\Program Files\Aseprite\Aseprite.exe','-b','--script-param','input='+str(master),'--script-param','output='+str(out),'--script',str(p/'scripts/export_tagged_keys.lua')],check=True,timeout=180)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
j=json.loads((out/'tagged_keys.json').read_text());j['editable_parent']={'path':str(master.relative_to(p)).replace('\\','/'),'sha256':sha(master)};j['method']='Flatten visible complete-canvas layers; no crop, warp, interpolation or isolated-limb compositing by exporter'
for row in j['keys']:
 row['sha256']=sha(out/row['path']);row['human_whole_figure_continuity_review']='PENDING'
if len(j['keys'])>4:j['next_job_state']='REVIEW_KEY_SELECTION_REQUIRED; do not automatically submit a job per key'
else:j['next_job_state']='GUIDES_EXPORTED; budget/readiness/identity/motion acceptance independent'
(out/'tagged_keys.json').write_text(json.dumps(j,indent=2)+'\n');print('TAGGED_COMPLETE_KEY_EXPORT',len(j['keys']))

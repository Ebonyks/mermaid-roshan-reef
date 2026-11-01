"""Refresh current payload hashes, per-asset licensing and bounded impact coverage."""
from pathlib import Path
import hashlib,json,subprocess,datetime
R=Path(__file__).resolve().parents[1];P=R.parent;REPO=R.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def paths():
 out=subprocess.run(['git','ls-files','--cached','--others','--exclude-standard','--',str(P.relative_to(REPO)).replace('\\','/')],cwd=REPO,capture_output=True,text=True,check=True).stdout
 return sorted(set(REPO/n for n in out.splitlines() if (REPO/n).is_file()))
def main():
 files=paths();media=[p for p in files if p.is_relative_to(R) and p.suffix.lower() in ['.png','.jpg','.mkv','.mp4','.aseprite']]
 license=REPO/'ASSET_LICENSES.md';text=license.read_text(encoding='utf-8');start='<!-- NATIVE_RIG_REPLACEMENT_20261101 -->';end='<!-- NATIVE_RIG_REPLACEMENT_20261101_END -->'
 block=start+'\n\n### Native rig true wardrobe replacement correction (source study)\n\n| Asset | Source / license / modifications |\n|---|---|\n'
 for p in media:
  n=p.relative_to(REPO).as_posix();kind='Built-in ImageGen crown-only clean plate, unexposed provider revision; only scalp window extracted. Project-generated candidate; exact prompt/input/hash in owner_correction.json.' if p.name=='hair_clean_plate.png' else 'Project-owned/generated derivative of original native rig, Fashion Designer fitting plates and headpieces; source-only candidate or explicitly retained reject. Registration/matte/exclusive skin selection or actual Godot capture/Aseprite/media export. Originals preserved; see replacement_v6 provenance, fitting, frozen inputs and archive receipts. No production/owner acceptance.'
  block+=f'| `{n}` | {kind} |\n'
 block+=end
 if start in text:a=text.index(start);b=text.index(end,a)+len(end);text=text[:a]+block+text[b:]
 else:text+='\n\n'+block+'\n'
 license.write_text(text,encoding='utf-8')
 impact=REPO/'design/audit_impacts/native-rig-costume-replacement-20261101.json';d=json.loads(impact.read_text(encoding='utf-8'))
 changed=subprocess.run(['git','diff','--name-only','26bd6d1f0573f7b1ad76511c22abf584e44b7e24'],cwd=REPO,capture_output=True,text=True,check=True).stdout.splitlines()
 untracked=subprocess.run(['git','ls-files','--others','--exclude-standard'],cwd=REPO,capture_output=True,text=True,check=True).stdout.splitlines()
 d['files']=sorted(set(changed+untracked+d.get('planned_files',[]))-{impact.relative_to(REPO).as_posix()});impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
 files=paths();manifest=P/'manifest.json';payload=[p for p in files if p!=manifest and p!=R/'manifest.json']
 record={'schema':2,'scope':'Current study payload; overlay v5 remains OWNER_REJECTED, corrective candidate acceptance separately recorded.','generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[{'path':p.relative_to(P).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in payload]}
 manifest.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
 new=[p for p in payload if p.is_relative_to(R)];(R/'manifest.json').write_text(json.dumps({'schema':1,'files':[{'path':p.relative_to(R).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in new]},indent=2)+'\n',encoding='utf-8')
 # The parent manifest includes the corrective manifest (no cyclic self-hash).
 record['files'].append({'path':(R/'manifest.json').relative_to(P).as_posix(),'sha256':sha(R/'manifest.json'),'bytes':(R/'manifest.json').stat().st_size});manifest.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
 print('RECORDS_REFRESHED',len(d['files']),len(record['files']),len(media))
if __name__=='__main__':main()

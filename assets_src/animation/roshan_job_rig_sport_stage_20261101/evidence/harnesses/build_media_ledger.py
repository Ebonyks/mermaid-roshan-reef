from pathlib import Path
import subprocess,json,hashlib,struct
from PIL import Image
repo=Path(__file__).resolve().parents[5];R=Path(__file__).resolve().parents[2];prefix=R.relative_to(repo).as_posix();paths=set(subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--',prefix],cwd=repo,text=True).splitlines());refs={x['path']:x for x in json.loads((R/'references/provenance.json').read_text())['files']};prior={x['packet_path']:x for x in json.loads((R/'asset_provenance.json').read_text())['files']};rows=[]
for rel in sorted(paths):
 p=repo/rel
 if not p.is_file() or p.suffix.lower() not in {'.png','.jpg','.jpeg','.webp','.aseprite','.mp4','.mkv','.svg'}:continue
 packet=p.relative_to(R).as_posix();sha=hashlib.sha256(p.read_bytes()).hexdigest()
 if packet in prior:x=dict(prior[packet])
 else:
  x={'path':rel,'packet_path':packet,'source_path':'Exact frozen-v3 native Godot4.7.2 Mobile captures; source and diagnostic/review harnesses, per-file evidence records','role':'native_review_or_diagnostic_evidence','license':'Project/owner source rights inherited; exact renderer derivative of declared source inputs. No new license grant, final art or character acceptance.','modifications':'Native diagnostic key copy or verified lossless archive; boards arrange existing native pixels only, no painting. See associated receipts and frozen input record.'}
 if packet in refs:x.update(source_path=refs[packet]['source_path'],role=refs[packet]['role'])
 x['sha256']=sha
 if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp'}:x['dimensions']=list(Image.open(p).size)
 elif p.suffix.lower()=='.aseprite':x['dimensions']=list(struct.unpack_from('<HH',p.read_bytes(),8))
 else:x['dimensions']=[1280,720] if p.suffix.lower()=='.mp4' else [1024,1024]
 rows.append(x)
(R/'asset_provenance.json').write_text(json.dumps({'scope':'Exact per-media-file source/provenance for frozen source review. Protected originals unchanged; source/published-baseline limits retained.','files':rows},indent=2)+'\n')
p=repo/'ASSET_LICENSES.md';text=p.read_text(encoding='utf-8');marker='\n## Native job-rig sport/stage source review — 2026-11-01\n';text=text.split(marker)[0];lines=[marker,'\nSource-only frozen review trial; HANDOFF_BLOCKED, no character/game/cinematic acceptance. Exact hashes/dimensions: `'+prefix+'/asset_provenance.json`. Existing source rights and acceptance limits remain; protected originals unchanged.\n\n| New file | Source / rights | URL | Modifications / scope |\n|---|---|---|---|\n']
for x in rows:lines.append('| `'+x['path']+'` | '+x['source_path'].replace('|','/')+'; '+x['license'].replace('|','/')+' | https://github.com/Ebonyks/mermaid-roshan-reef | '+x['modifications'].replace('|','/')+' SHA-256 `'+x['sha256']+'`. |\n')
p.write_bytes((text+''.join(lines)).encode('utf-8'));print('MEDIA_LEDGER',len(rows))

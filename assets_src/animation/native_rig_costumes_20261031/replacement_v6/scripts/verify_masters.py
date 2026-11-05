from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];rows=[]
for theme in ['ballet','magician']:
 for clip,count in [('arm_bend',97),('blink',73),('tail_bend',121)]:
  frames=sorted((ROOT/f'evidence/render_{theme}_v8'/clip).glob('*.png'));reopened=ROOT/'masters_v8/reopened'/theme/clip;bad=[]
  for p in frames:
   q=reopened/p.name
   if not q.exists() or Image.open(p).convert('RGBA').tobytes()!=Image.open(q).convert('RGBA').tobytes():bad.append(p.name)
  master=ROOT/'masters_v8'/theme/f'{clip}.aseprite'
  rows.append({'theme':theme,'clip':clip,'expected_frames':count,'frames':len(frames),'mismatches':bad,'pass':len(frames)==count and not bad,'master_sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'master_bytes':master.stat().st_size})
report={'pass':all(r['pass'] for r in rows),'aseprite_version':'1.3.18.4-x64','timing':'33/33/34ms integer review cadence; native AnimationPlayer unchanged','clips':rows}
(ROOT/'evidence/aseprite_roundtrip.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2));raise SystemExit(0 if report['pass'] else 1)

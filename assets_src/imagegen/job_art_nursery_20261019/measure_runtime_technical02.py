from pathlib import Path
import json,hashlib,importlib.util
from PIL import Image
r=Path.cwd();s=r/'assets_src/imagegen/job_art_nursery_20261019';b=r/'assets_src/imagegen/job_art_boxer_20261019';spec=importlib.util.spec_from_file_location('job_art_measure',r/'docs/handoffs/codex_job_art_imagegen_2026-10-17/tools/measure_job_art.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rows=[]
for folder in [s,b]:
 for row in json.loads((folder/'runtime_provenance.json').read_text())['records']:
  p=r/row['path'];im=Image.open(p);c=m.cutout_profile(p.read_bytes());rows.append({'path':row['path'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'dimensions':list(im.size),'decoded_RGBA_bytes':im.width*im.height*4,'cutout':c})
d={'runtime_picture_count':len(rows),'decoded_RGBA_bytes':sum(x['decoded_RGBA_bytes'] for x in rows),'records':rows,'limits':'DecodedRGBA inventory only, not actual deviceVRAM/overdraw/FPS evidence. Sharedpictures are countedonce in37unique paths. Existing3baby/fullbottle/Teacherhand assets notadded.'};(s/'verification/runtime_technical02.json').write_text(json.dumps(d,indent=2)+'\n');print('pictures',len(rows),'decodedMiB',d['decoded_RGBA_bytes']/1048576,'cutoutFailures',[(x['path'],x['cutout']['verdict']) for x in rows if x['cutout']['verdict']!='CUTOUT_OK'])

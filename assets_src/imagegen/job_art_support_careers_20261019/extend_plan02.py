from pathlib import Path
import json,importlib.util,hashlib
from PIL import Image
r=Path.cwd();s=r/'assets_src/imagegen/job_art_support_careers_20261019'
p=s/'job_cards.json';d=json.loads(p.read_text());assert not any(x['id']=='farmer-plants' for x in d['jobs'])
d['jobs'] += [
 {'id':'farmer-plants','states':['sprout','flower0','flower1','flower2','flower3','flower4'],'generation_call_cap':12,'default_takes_per_state':2,'verb':'Existing five earned planting slots grow into different pastel flowers; same seed/holes/progress/anchors.','fixed':'Source soil palette/camera, whole stem/leaves/flower, common base socket. Existing authored drag seed reused at correct aspect.','geometry':'128square uniformly fitted whole plant, base socket at centre-bottom; flowers authored separately, never tint/code redraw.','entry_exit':'Seed to sprout to flower on existing timer; named progress pictures, not frame generation.','cleanup_minutes_cap':35,'stop':'Two per state/twelve aggregate; diagnose/change method after cap; source/context/motion/technical/device gates remain separate.'},
 {'id':'painter-cloud-cover','states':['puff0','puff1','puff2','puff3','puff4','puff5'],'generation_call_cap':12,'default_takes_per_state':2,'verb':'Existing wipe clears authored irregular cloud puffs from the same sunrise painting at original grid/thresholds.','fixed':'Same ivory/lilac/dust-puff painted family, no new painting/scene, varied silhouettes with opaque soft body.','geometry':'256square cutouts, tidy translucent contour only; fill original affected patches without square seams, irregular overlap.','entry_exit':'Whole puffs alpha fade only on actual existing wiped patches, no added progress or timer.','cleanup_minutes_cap':30,'stop':'Two per puff/twelve aggregate then diagnose/change method. Existing profile and actual painting/HUD/neighbors >=4.5 separately.'}]
p.write_text(json.dumps(d,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('measure',r/'docs/handoffs/codex_job_art_imagegen_2026-10-17/tools/measure_job_art.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rows=[]
for p in sorted(s.glob('*_native.png')):
 im=Image.open(p);rows.append({'path':p.relative_to(r).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'dimensions':list(im.size),'cutout':m.cutout_profile(p.read_bytes()),'scope':'native source measurement only; no runtime acceptance'})
(s/'source_technical01.json').write_text(json.dumps({'records':rows},indent=2)+'\n')
print('Native profiles',len(rows),'non-OK',[(Path(x['path']).name,x['cutout']['verdict']) for x in rows if x['cutout']['verdict']!='CUTOUT_OK'])

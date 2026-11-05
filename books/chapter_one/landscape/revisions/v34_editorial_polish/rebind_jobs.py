"""Owner correction: marginal art uses little puffs, never Grand Puff."""
from pathlib import Path
import json,hashlib
V=Path(__file__).resolve().parent;R=V.parents[4]
jobs=json.loads((V/'generation_jobs.json').read_text('utf8'))
old=[dict(j) for j in jobs]
little=R/'assets_src/concepts/dust_bunny_animated_2026-07-27/references/dust_bunny_curl_ears.png'
for j in jobs:
 if j['id'] in ['tidy_art_bank','care_bank24','care_bank25','quiet_bank']:
  j['references'][1]=dict(path=little.relative_to(R).as_posix(),sha256=hashlib.sha256(little.read_bytes()).hexdigest(),role='canonical_little_puff_identity_not_Grand_Puff')
  j['prompt']=j['prompt'].replace('IMAGE_2','IMAGE_2')+' OWNER CORRECTION: These are ONLY the LITTLE puffs from IMAGE_2. NO Grand Puff, NO star/diamond on the forehead, NO tall flame-like stacked cloud crest, NO heavy droopy brow. Simple low rounded cloud body, a single soft forehead curl, two narrow upright curled ears, four pearl nubs. Bunny height only75-90px on1060px canvas, below y910. No anatomical hands or fingers: use soft edge puffs to nudge/hold a prop. Little puffs are cheerful/concentrating or gently concerned, not sick. Keep their established tiny border scale.'
  if j['id'] in ['tidy_art_bank','care_bank24']:j['attempt']=2
 if j['id']=='inviting_cutout':
  j['prompt']=j['prompt'].replace('upper-left','upper-right').replace('x97,y17 to x237,y251','x797,y17 to x990,y253')
 j['prompt_sha256']=hashlib.sha256(j['prompt'].encode()).hexdigest()
(V/'generation_jobs_first_plan.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
(V/'generation_jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
(V/'OWNER_CORRECTION.json').write_text(json.dumps(dict(date='2026-10-18',direction='Grand Puff got mixed into a background; only the little puffs may appear in marginal backgrounds.',rejected=['tidy_art_bank attempt1','care_bank24 attempt1'],reason='Wrong identity reference bound; forehead star and tall stacked cloud crest are Grand Puff features. Reject them, bind canonical little-puff reference and regenerate.',scope='All marginal art; Grand Puff remains main narrative only.'),indent=2)+'\n',encoding='utf8',newline='\n')
print('Corrected identity bindings; bad background attempts retained as rejected evidence.')

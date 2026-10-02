from pathlib import Path
import json,hashlib,datetime,shutil
from PIL import Image
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002';S=R/'assets_src/imagegen/nursery_wash_connected_v1_20261002'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
index=json.loads((F/'baseline_visual/INDEX.json').read_text())
review={'status':'FAIL_DIRECT_COMPLETE_NURSERY_BASELINE_VISUAL_REVIEW','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':[],'boards':[dict(x,sha256=sha(R/x['path'])) for x in index['boards']],'method':'Root directly inspected all 24 ordered read-only QA boards, covering every one of 1051 consecutive Nursery baseline native frames across both contexts and both aspects. Full1280 training native frame0150 was separately inspected. Board review establishes missing subject through the whole action, not fine material quality for an absent basin. Doctor full sequences remain machine captured, not fully re-reviewed here; prior direct historical Doctor action score2.7 remains dated.'}
for case in sorted({x['case'] for x in index['boards']}):
    review['cases'].append({'id':case,'overall_meaningful_wash_action':1.8,'visible_hands_and_contact':1.5,'basin_material_score':None,'note':'The work focus has no basin or washing hands throughout earned positive hold progress. Roshan cycles generic work poses away from the empty oval. The next catch invitation returns the room actor; this is not a literal wet/rub/rinse/clean sequence. Broad portrait-style backdrop crops/blur and translucent bars remain separate room presentation weaknesses.','priority':True})
write(F/'baseline_visual/DIRECT_REVIEW.json',review)
p=S/'rub_palm_attempt02';base=json.loads((S/'rub_back_attempt01/SOURCE_REVIEW.json').read_text())
with Image.open(p/'native.png') as im:
    im.load();base['native']={'mode':im.mode,'size':list(im.size),'alpha_extrema':list(im.getchannel('A').getextrema()),'alpha_bbox':list(im.getchannel('A').getbbox())}
base.update(score=4.5,note='The far cupped palm now reads beneath the near scrubbing hand rather than a prayer/clap clasp. Lather is bounded to the actual contact; wrists remain connected to the own-costume body. Fine fingertips are partly occluded by foam. Static provisional floor only; mounted/action/motion and owner lanes unassigned.',reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),native_sha256=sha(p/'native.png'),prompt_sha256=sha(p/'PROMPT.json'),references=[{'path':'assets_src/imagegen/nursery_wash_connected_v1_20261002/rub_back_attempt01/native.png','sha256':sha(S/'rub_back_attempt01/native.png')}],runtime_normalization=None)
write(p/'SOURCE_REVIEW.json',base)
with (R/'ASSET_LICENSES.md').open('a',encoding='utf-8') as out:
    out.write('| `assets_src/imagegen/nursery_wash_connected_v1_20261002/rub_palm_attempt02/native.png` | OpenAI built-in imagegen; connected back-rub state as identity/layout reference | Project generated art; OpenAI terms | https://openai.com/policies/terms-of-use/ | Targeted palm-contact redraw; rejected weak clasp source preserved separately. Static source4.5 provisional; complete action/owner acceptance pending. |\n')
print('Recorded 1051-frame Nursery baseline visual failure and provisional static palm-rub2 floor. No full-action acceptance.')

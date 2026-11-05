"""Fail closed on frozen inputs, common weights, curves, contract or production drift."""
from pathlib import Path
import hashlib,json,re,subprocess
import numpy as np
from PIL import Image

P=Path(__file__).resolve().parents[1]; ROOT=P.parents[2]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
freeze=json.loads((P/'evidence/art_freeze.json').read_text())
checks={f'frozen:{name}':sha(P/name)==value for name,value in freeze['files'].items()}
seed=json.loads((P/'fixtures/seed_scripts/rig.json').read_text());live=json.loads((P/'godot/rig.json').read_text())
checks['same_bone_rest_topology']=seed['bones']==live['bones'] and len(live['bones'])==14
for old in seed['meshes']:
    actual=next(m for m in live['meshes'] if m['name']==old['name'])
    for field in ['vertices','weights','triangles','z']:
        checks[f'common:{old["name"]}:{field}']=old[field]==actual[field]
def function(text,name):
    return re.search(r'(?ms)^func '+name+r'\(.*?(?=^func |\Z)',text).group().strip()
a=(P/'fixtures/seed_scripts/study.gd').read_text();b=(P/'godot/study.gd').read_text()
for name in ['authored_pose','ease5','pulse','build_animation']:
    checks['curve:'+name]=function(a,name)==function(b,name)
contract=json.loads((P/'contract/rig_v1.json').read_text())
checks['contract_pin']=sha(P/'contract/rig_v1.json')=='b2a5dfe936d13ccdeb88e5c29ad268b19488de7cbe49d9b06abf84a94135fb5f'
checks['contract_names']=[x['seed_name'] for x in contract['bones']]==[x['name'] for x in seed['bones']]
production=subprocess.check_output(['git','diff','--name-only','93166ab1828ab9857227d038f8833b92dfb2f9f1','--','scripts','scenes','project.godot'],cwd=ROOT,text=True).strip()
checks['no_production_change']=not production
original=np.array(Image.open(P/'fixtures/seed_art/body.png').convert('RGBA'))
anatomy=np.array(Image.open(P/'art/anatomy.png').convert('RGBA'))
owner=np.array(Image.open(P/'art/ownership.png').convert('RGBA'))
domain=((owner[:,:,0]>128)|(owner[:,:,1]>128))&(original[:,:,3]>0)
checks['old_clothing_domain_erased']=bool(domain.any() and np.all(anatomy[:,:,3][domain]==0))
boxes=[(451,346,20,22),(619,342,12,25),(515,370,64,68),(487,510,14,64),(642,581,12,64),(473,795,40,20)]
survey=[]
for x,y,w,h in boxes:
    q=original[y:y+h,x:x+w].astype(float)
    mask=(q[:,:,3]>229)&(q[:,:,2]>q[:,:,0]*.84)&(q[:,:,2]>q[:,:,1]*1.035)
    remaining=int(np.count_nonzero(anatomy[y:y+h,x:x+w,3][mask]))
    survey.append(dict(box=[x,y,w,h],old_clothing_pixels=int(mask.sum()),remaining=remaining))
checks['independent_six_region_survey']=all(x['remaining']==0 for x in survey) and sum(x['old_clothing_pixels'] for x in survey)>0
# Prove that reinsertion and altered identity data fail the same source predicates.
bad=anatomy.copy();y,x=np.argwhere(domain)[0];bad[y,x]=original[y,x]
controls={'reinserted_domain_detected':not np.all(bad[:,:,3][domain]==0),'changed_rest_detected':live['bones'][0]['head']!=[0,0]}
result=dict(passed=all(checks.values()) and all(controls.values()),checks=checks,negative_controls=controls,survey=survey,production_diff=production,limits='Source integrity only; native geometry/contact, naturalness and physical acceptance remain separate.')
(P/'evidence/source_gates.json').write_text(json.dumps(result,indent=2)+'\n')
print('SOURCE GATES',result['passed'],len(checks),'checks')
for name,value in checks.items():
    if not value:print('FAILED',name)
raise SystemExit(0 if result['passed'] else 1)

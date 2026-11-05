"""Fail-closed shared-contract validation and legacy-name migration; no game writes."""
from pathlib import Path
import json,hashlib,copy,math
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def migrate_seed_names(names,contract):
 mapping={x['seed_name']:x['id'] for x in contract['bones']}
 if any(x not in mapping for x in names):raise ValueError('Unknown legacy bone; no partial migration')
 return {mapping[k]:v for k,v in names.items()}
def validate(binding,c):
 errors=[]
 if binding.get('contract_id')!=c['id'] or binding.get('contract_version')!=c['version']:errors.append('contract/version mismatch: explicit migration required')
 views={x['id']:x for x in c['views']}
 if binding.get('view') not in views or views[binding['view']]['status']!='SEED_AVAILABLE':errors.append('missing/unauthorized authored view')
 if not binding.get('skin'):errors.append('missing skin')
 p=binding.get('prop',{});grips=p.get('grips',[]);ids={x['id'] for x in c['sockets'] if x['type']=='palm'}
 if not 1<=len(grips)<=2 or len({x.get('socket') for x in grips})!=len(grips):errors.append('one/two distinct grip sockets required')
 for x in grips:
  if x.get('socket') not in ids:errors.append('unknown socket')
  if not isinstance(x.get('prop_px'),list) or len(x['prop_px'])!=2 or any(not isinstance(v,(int,float)) or not math.isfinite(v) for v in x['prop_px']):errors.append('invalid prop coordinate')
 for field in ['path','native_size','orientation','support_point_px','occlusion']:
  if field not in p:errors.append('missing '+field)
 return errors

def main():
 c=load(R/'contract/rig_v1.json');f=load(R/'contract/FREEZE.json');seed=load(R/'seed/rig.json');live=load(R/'demo/rig.json');binding=load(R/'contract/example_binding.json');checks={}
 checks['frozen_contract_hash']=f['sha256']==sha(R/'contract/rig_v1.json')==sha(R/'demo/contract.json')
 checks['same_fourteen_bones_and_rest']=len(seed['bones'])==len(c['bones'])==14 and seed['bones']==live['bones'] and [x['seed_name'] for x in c['bones']]==[x['name'] for x in seed['bones']]
 checks['all_original_common_vertex_weights']=all(all(a[k]==b[k] for k in ['vertices','triangles','weights']) for a,b in zip(seed['meshes'],live['meshes']))
 a=(R/'seed/study.gd').read_text();b=(R/'demo/seed_study.gd').read_text();extract=lambda s:s[s.index('func authored_pose('):s.index('func set_pose(')]
 checks['original_three_curves_exact']=extract(a)==extract(b)
 checks['example_binding_valid']=not validate(binding,c)
 controls={}
 for name,mutate in [('unknown_socket',lambda b:b['prop']['grips'][0].update(socket='hand.fake')),('rest_version_fork',lambda b:b.update(contract_version='2.0.0')),('missing_view',lambda b:b.update(view='quarter_right')),('bad_coordinate',lambda b:b['prop']['grips'][0].update(prop_px=[0,float('nan')])),('duplicate_grip',lambda b:b['prop']['grips'][1].update(socket='grip.screen_left')),('unknown_legacy_bone',None)]:
  bad=copy.deepcopy(binding)
  if mutate:mutate(bad);controls[name]=bool(validate(bad,c))
  else:
   try:migrate_seed_names({'Unknown':1},c);controls[name]=False
   except ValueError:controls[name]=True
 checks['legacy_adapter_roundtrip']=set(migrate_seed_names({x['name']:i for i,x in enumerate(seed['bones'])},c))=={x['id'] for x in c['bones']}
 # Mathematical local-rest reconstruction independently checks the published transforms.
 errors=[]
 for b,s in zip(c['bones'],seed['bones']):
  parent=next((x for x in seed['bones'] if x['name']==s['parent']),None);ph=parent['head'] if parent else [0,0];pa=math.atan2(parent['tail'][1]-ph[1],parent['tail'][0]-ph[0]) if parent else 0.;x,y=b['rest_local']['position'];point=[ph[0]+x*math.cos(pa)-y*math.sin(pa),ph[1]+x*math.sin(pa)+y*math.cos(pa)];errors.append(math.dist(point,s['head']))
 checks['rest_reconstruction']=max(errors)<1e-9
 report={'pass':all(checks.values()) and all(controls.values()),'checks':checks,'negative_controls':controls,'max_rest_error_native_px':max(errors),'contract_sha256':sha(R/'contract/rig_v1.json'),'acceptance':'Source compatibility only; no naturalness, output or device acceptance.'};(R/'evidence/contract_validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(0 if report['pass'] else 1)
if __name__=='__main__':main()

from pathlib import Path
import json,hashlib,copy,re
R=Path(__file__).resolve().parents[1]
load=lambda p:json.loads(p.read_text())
C=load(R/'contract/rig_v1.json');SEED=load(R/'contract/seed_rig.json');RIG=load(R/'demo/rig.json')
def validate_rig(rig):
 errors=[];by_name={b['seed_name']:b for b in C['bones']};by_id={b['id']:b for b in C['bones']}
 if len(rig['bones'])!=14:errors.append('bone_count')
 for b in rig['bones']:
  if b['name'] not in by_name:errors.append('unknown_bone');continue
  spec=by_name[b['name']];parent=None if spec['parent'] is None else by_id[spec['parent']]['seed_name']
  if b['parent']!=parent or b['head']!=spec['head_canvas_px'] or b['tail']!=spec['tail_canvas_px']:errors.append('rest_or_parent')
 for mesh,seed in zip(rig['meshes'],SEED['meshes']):
  for name in ['vertices','triangles','weights']:
   if mesh[name]!=seed[name]:errors.append('original_common_'+name)
 return errors
def validate_binding(binding):
 errors=[]
 if binding['contract_id']!=C['id'] or binding['contract_version']!=C['version']:errors.append('contract_pin')
 if binding['view']!='front':errors.append('missing_authored_view')
 sockets={s['id'] for s in C['sockets']}
 for grip in binding['prop']['grips']:
  if grip['socket'] not in sockets:errors.append('unknown_socket')
 if not isinstance(binding['prop']['scale'],(float,int)):errors.append('nonuniform_scale')
 if binding['prop']['hold_interval_seconds']!=[0,6.4]:errors.append('ownership_timing')
 return errors
def main():
 results={'rig_errors':validate_rig(RIG),'seed_rig_sha256':hashlib.sha256((R/'contract/seed_rig.json').read_bytes()).hexdigest(),'contract_sha256':hashlib.sha256((R/'contract/rig_v1.json').read_bytes()).hexdigest(),'bindings':{},'new_garment_mesh_errors':[]}
 for job in ['detective','geologist']:results['bindings'][job]=validate_binding(load(R/'contract'/f'{job}_binding.json'))
 known={b['name'] for b in RIG['bones']}
 for m in load(R/'demo/garment_meshes.json')['meshes']:
  if set(m['weights'])!=known:results['new_garment_mesh_errors'].append(m['name']+':bones')
  for i in range(len(m['vertices'])):
   w=[v[i] for v in m['weights'].values()]
   if min(w)<0 or max(w)>1 or abs(sum(w)-1)>1e-6:results['new_garment_mesh_errors'].append(m['name']+':weights');break
 controls={};b=load(R/'contract/detective_binding.json')
 bad=copy.deepcopy(b);bad['view']='profile_right';controls['unauthored_view']=bool(validate_binding(bad))
 bad=copy.deepcopy(b);bad['prop']['grips'][0]['socket']='grip.retired';controls['unknown_socket']=bool(validate_binding(bad))
 bad=copy.deepcopy(b);bad['prop']['scale']=[.29,.35];controls['perspective_squash']=bool(validate_binding(bad))
 bad=copy.deepcopy(RIG);bad['bones'][0]['head'][0]+=1;controls['rest_drift']=bool(validate_rig(bad))
 bad=copy.deepcopy(RIG);bad['meshes'][0]['weights']['Torso'][0]+=.1;controls['common_weight_edit']=bool(validate_rig(bad))
 bad=copy.deepcopy(RIG);bad['bones'].append({'name':'IndependentRig','parent':None,'head':[0,0],'tail':[1,0]});controls['extra_bone']=bool(validate_rig(bad))
 results['negative_controls']=controls
 def function(text,name):return re.search(r'^func '+name+r'\(.*?(?=^func |\Z)',text,re.M|re.S).group(0).rstrip()
 s=(R/'demo/study.gd').read_text();t=(R/'contract/seed_study.gd.txt').read_text();results['curves_preserved']={n:function(s,n)==function(t,n) for n in ['ease5','pulse','authored_pose','clip_length','build_animation']}
 results['pass']=not results['rig_errors'] and not any(results['bindings'].values()) and not results['new_garment_mesh_errors'] and all(controls.values()) and all(results['curves_preserved'].values())
 results['compatibility_scope']='Pinned14-bone rest/common weights/front grip only. Shared waist join, all mixed outline acceptance and unpublished shared contract remain separate blockers.'
 (R/'evidence/contract_validation.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2));raise SystemExit(0 if results['pass'] else 1)
if __name__=='__main__':main()

from pathlib import Path
import json, hashlib, shutil
ROOT=Path.cwd(); P=ROOT/'assets_src/animation/roshan_wave_repair_20261010'; RT=Path('H:/MermaidReefTools/LocalVideo/ltx25')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x): p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes((json.dumps(x,indent=2)+'\n').encode())
old=RT/'results/rig_pilot/g1_slowwave'; g=json.loads((old/'workflow.api.json').read_text()); old_job=json.loads((old/'job.json').read_text())
R=P/'native640_01'; R.mkdir(exist_ok=True)
for i in list(g):
 if int(i) in list(range(21,32))+[50,51,52,123]: del g[i]
g['8']['inputs'].update(width=640,height=896)
g['14']['inputs']['lane']='half'
g['20']['inputs']['filename_prefix']='wave_repair_20261010/native640_01/stage1_video'
g['42']['inputs']['filename_prefix']='wave_repair_20261010/native640_01/native/frame'
g['90']['inputs']['label']='wave_repair_native640_01'
write(R/'workflow.api.json',g)
refs=[]
for f in old_job['inputs']:
 if 'guide_quarter' in f['path']: continue
 src=RT/'input'/f['path']; assert sha(src)==f['sha256'],src
 dst=P/'sources/run7'/Path(f['path']).relative_to('rig_pilot'); dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
 refs.append({'path':dst.relative_to(ROOT).as_posix(),'sha256':sha(dst),'runtime_path':'input/'+f['path'],'role':'identity_candidate_from_prior_approved_source' if 'identity' in f['path'] else 'structural_motion_control_only','used_as_delivery_pixels':False})
write(R/'sources.json',{'sources':refs,'model_workflow_pins':{'base_workflow_sha256':sha(old/'workflow.api.json'),'comfy_core':'87465b8f1f64a27a46f16f22b13b410494dca66d','official_union_nodes':'3bf3ca62595f1764c47d01c35c8e5dfe47e1a88f','adapter':'LTX2.3 Union on LTX2.5','adapter_sha256':'a1b888a87f661d27f08b394ae559e8e1050be33900bcc36a5cdf659e48f88d18'},'settings':{'method':'native-resolution-union','canvas':[640,896],'control_canvas':[320,448],'frames':41,'fps':24,'steps':8,'seed':20261004,'change_vs_g1':'Generate entire figure natively at640x896 with half-sized320x448 control, no low-resolution320x448 generation or separate upscale/refine. Guide/identity/prompt/seed held fixed.','new_refine_details':False,'ordinary_negatives_active':False}})
write(R/'outputs.json',{'images':[{'node':'42','name':'native_frames','count':41,'canvas':[640,896]}],'latents':[{'node':'20','name':'stage1_video','count':1}]})
prior=[]
for d in sorted((RT/'results/rig_pilot').iterdir()):
 if not (d/'receipt.json').is_file(): continue
 rec=json.loads((d/'receipt.json').read_text()); j=json.loads((d/'job.json').read_text())
 prior.append({'id':d.name,'status':rec['status'],'elapsed_seconds':rec.get('elapsed_seconds'),'sampled_card_peak_mib':rec.get('sampled_card_peak_mib'),'workflow_sha256':sha(d/'workflow.api.json'),'job_sha256':sha(d/'job.json'),'source':'Local owner rig-pilot queue results, not previously archived in this repo','note':rec.get('note'), 'review':'Inspected selected lower frames in g1/f1/e1; no complete acceptance. Existing native outputs preserved at original paths.'})
write(P/'prior_local_history.json',{'status':'SOURCE_INVENTORY_NOT_ACCEPTANCE','takes':prior,'scope':'Eight actual later local LTX takes retained in cumulative history; current renewed user commission is explicit.'})
print('PREPARED_NATIVE640',len(refs),'SOURCES',len(g),'NODES')
